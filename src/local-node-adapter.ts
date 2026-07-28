import { execFile, spawn } from "node:child_process";
import { constants as fsConstants } from "node:fs";
import {
  chmod,
  copyFile,
  lstat,
  mkdir,
  open,
  readFile,
  readdir,
  realpath,
  rename,
  rm,
  stat
} from "node:fs/promises";
import { basename, dirname, join, parse, relative, resolve, sep } from "node:path";
import { promisify } from "node:util";

import { EdgeNodeLifecycle } from "./node-lifecycle.js";
import {
  EDGE_NODE_SCHEMA_VERSION,
  canonicalJson,
  edgeNodeIdentity,
  sha256Hex,
  type EdgeEvidenceArtifact,
  type EdgeEvidenceExportReceipt,
  type EdgeLifecycleOperation,
  type EdgeLifecycleOutcome,
  type EdgeLifecycleSnapshot,
  type EdgeNodeExecutionReceipt,
  type EdgeNodeIdentity,
  type EdgeNodeIdentityInput,
  type EdgeNodeLease,
  type EdgeObservation,
  type EdgePlaneBindings,
  type EdgeProfileAuthority,
  type EdgeReconstructionInput,
  type EdgeReconstructionReceipt
} from "./node-contracts.js";
import {
  EDGE_NODE_PROFILE_POLICY,
  LOCAL_UNSHARE_POLICY
} from "./node-policy.js";

const execFileAsync = promisify(execFile);
const HEX_64 = /^[a-f0-9]{64}$/;
const OPERATION_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/;
const LOCAL_STATE_SCHEMA_VERSION = 1 as const;
const BODY_SEAL_NAME = ".ordivon-body.json";

interface PersistedLocalState {
  readonly schema_version: typeof LOCAL_STATE_SCHEMA_VERSION;
  readonly identity_digest: string;
  readonly lifecycle: EdgeLifecycleSnapshot;
  readonly highest_lease_generation: number;
}

interface LocalNodeRecord {
  readonly identity: EdgeNodeIdentity;
  readonly lifecycle: EdgeNodeLifecycle;
  readonly planes: EdgePlaneBindings;
  readonly leaseTokens: Map<string, string>;
  readonly leaseActions: Map<string, number>;
  readonly observations: Map<string, { descriptor: EdgeObservation; body: Uint8Array }>;
  highestLeaseGeneration: number;
}

interface BodySeal {
  readonly schema_version: typeof EDGE_NODE_SCHEMA_VERSION;
  readonly node_id: string;
  readonly identity_digest: string;
  readonly source_sha256: string;
  readonly manifest_sha256: string;
}

interface RootfsEntry {
  readonly path: string;
  readonly sha256: string;
  readonly bytes: number;
  readonly mode: number;
}

export interface LocalLeaseGrant {
  readonly lease: EdgeNodeLease;
  readonly token: string;
}

export interface LocalExperimentResult {
  readonly exitCode: number;
  readonly stdout: Uint8Array;
  readonly stderr: Uint8Array;
  readonly startedAt: Date;
  readonly completedAt: Date;
}

export interface LocalExperimentExecutor {
  prepare(rootfs: string, entrypoint: Uint8Array): Promise<void>;
  run(rootfs: string, budget: {
    readonly wallTimeMs: number;
    readonly outputBytes: number;
    readonly memoryBytes: number;
    readonly processLimit: number;
  }): Promise<LocalExperimentResult>;
}

export interface LocalAdapterFaults {
  afterProvisionEffect?(): void | Promise<void>;
  afterDestroyEffect?(): void | Promise<void>;
  beforeEvidenceCommit?(): void | Promise<void>;
  afterEvidenceCommit?(): void | Promise<void>;
}

export interface LocalAdapterOptions {
  readonly root: string;
  readonly authority: EdgeProfileAuthority;
  readonly executor: LocalExperimentExecutor;
  readonly faults?: LocalAdapterFaults;
  readonly now?: () => Date;
  readonly token?: () => string;
}

export class LocalDisposableNodeAdapter {
  readonly #root: string;
  readonly #authority: EdgeProfileAuthority;
  readonly #executor: LocalExperimentExecutor;
  readonly #faults: LocalAdapterFaults;
  readonly #now: () => Date;
  readonly #token: () => string;
  readonly #nodes = new Map<string, LocalNodeRecord>();
  readonly #locks = new Map<string, Promise<void>>();

  constructor(options: LocalAdapterOptions) {
    if (
      options.authority.profile !== "research" ||
      options.authority.authority_id !== EDGE_NODE_PROFILE_POLICY.research.authority_id ||
      options.authority.credential_scope !== EDGE_NODE_PROFILE_POLICY.research.credential_scope ||
      options.authority.credential_mode !== "none"
    ) {
      throw new Error("local adapter requires credential-free research authority");
    }
    const resolvedRoot = resolve(options.root);
    if (resolvedRoot === parse(resolvedRoot).root) {
      throw new Error("local adapter root must not be a filesystem root");
    }
    this.#root = resolvedRoot;
    this.#authority = options.authority;
    this.#executor = options.executor;
    this.#faults = options.faults ?? {};
    this.#now = options.now ?? (() => new Date());
    this.#token = options.token ?? (() => crypto.randomUUID().replaceAll("-", ""));
  }

  async declare(input: EdgeNodeIdentityInput): Promise<EdgeNodeIdentity> {
    this.#validateLocalIdentity(input);
    const identity = await edgeNodeIdentity(input);
    await this.#withLock(identity.node_id, async () => {
      if (this.#nodes.has(identity.node_id)) return;
      await this.#ensureProviderRoot();
      const planes = this.#planeBindings(identity.node_id);
      await Promise.all([
        assertSafeOptionalDirectory(planes.management),
        assertSafeOptionalDirectory(dirname(planes.experiment)),
        assertSafeOptionalDirectory(planes.observation),
        assertSafeOptionalDirectory(planes.evidence_export)
      ]);
      await cleanupManagementTemps(planes.management);
      const persistedIdentity = await readJsonIfExists<EdgeNodeIdentity>(
        join(planes.management, "identity.json")
      );
      const persistedState = await readJsonIfExists<PersistedLocalState>(
        join(planes.management, "state.json")
      );
      if (persistedIdentity === undefined && persistedState !== undefined) {
        throw new Error("local management journal has state without identity");
      }
      if (
        persistedIdentity !== undefined &&
        canonicalJson(persistedIdentity) !== canonicalJson(identity)
      ) {
        throw new Error("deterministic node ID is bound to different identity data");
      }
      if (
        persistedState !== undefined &&
        (persistedState.schema_version !== LOCAL_STATE_SCHEMA_VERSION ||
          persistedState.identity_digest !== identity.digest ||
          !Number.isSafeInteger(persistedState.highest_lease_generation) ||
          persistedState.highest_lease_generation < 0)
      ) {
        throw new Error("invalid local management journal");
      }
      const record: LocalNodeRecord = {
        identity,
        lifecycle: new EdgeNodeLifecycle(persistedState?.lifecycle),
        planes,
        leaseTokens: new Map(),
        leaseActions: new Map(),
        observations: await loadObservations(planes.observation, identity.node_id),
        highestLeaseGeneration: persistedState?.highest_lease_generation ?? 0
      };
      this.#nodes.set(identity.node_id, record);
      await this.#recoverCommittedEvidence(record);
    });
    return identity;
  }

  planes(nodeId: string): EdgePlaneBindings {
    return { ...this.#record(nodeId).planes };
  }

  async provision(
    nodeId: string,
    operationId: string,
    entrypoint: Uint8Array
  ): Promise<EdgeLifecycleOutcome> {
    validateOperationId(operationId);
    return this.#withLock(nodeId, async () => {
      const record = this.#record(nodeId);
      const prior = outcomeFor(record.lifecycle, operationId);
      if (prior !== undefined) return replayOrConflict(prior, "provision", record.lifecycle.state);
      if (record.lifecycle.state !== "declared") {
        return record.lifecycle.apply(operationId, "provision");
      }
      if (entrypoint.byteLength > LOCAL_UNSHARE_POLICY.max_entrypoint_bytes) {
        throw new Error("entrypoint exceeds local profile policy");
      }
      if (await sha256Hex(entrypoint) !== sourceDigest(record.identity)) {
        throw new Error("entrypoint does not match declared source digest");
      }

      const uncertain = record.lifecycle.apply(operationId, "provision", "uncertain");
      await this.#persist(record);
      const nodeRoot = dirname(record.planes.experiment);
      const staging = join(nodeRoot, `.staging-${await sha256Hex(operationId)}`);
      try {
        await mkdir(nodeRoot, { recursive: true, mode: 0o700 });
        await mkdir(staging, { mode: 0o700 });
        await this.#executor.prepare(staging, entrypoint);
        const manifest = await rootfsManifest(staging);
        const totalBytes = manifest.reduce((sum, entry) => sum + entry.bytes, 0);
        if (totalBytes > record.identity.input.resource_profile.storage_bytes) {
          throw new Error("prepared rootfs exceeds declared storage budget");
        }
        const seal: BodySeal = {
          schema_version: EDGE_NODE_SCHEMA_VERSION,
          node_id: nodeId,
          identity_digest: record.identity.digest,
          source_sha256: sourceDigest(record.identity),
          manifest_sha256: await sha256Hex(canonicalJson(manifest))
        };
        await writeJsonDurable(join(staging, BODY_SEAL_NAME), seal, 0o400);
        await syncTree(staging);
        await rename(staging, record.planes.experiment);
        await fsyncDirectory(nodeRoot);
      } catch {
        await rm(staging, { recursive: true, force: true });
        return uncertain;
      }
      try {
        await this.#faults.afterProvisionEffect?.();
      } catch {
        return uncertain;
      }
      const reconciled = record.lifecycle.reconcile(
        `reconcile:${operationId}`,
        await verifyProviderBody(record)
      );
      await this.#persist(record);
      if (reconciled.state !== "provisioned") {
        throw new Error("new local body failed sealed reconciliation");
      }
      return record.lifecycle.apply(operationId, "provision");
    });
  }

  async reconcile(nodeId: string, operationId: string): Promise<EdgeLifecycleOutcome> {
    validateOperationId(operationId);
    return this.#withLock(nodeId, async () => {
      const record = this.#record(nodeId);
      const snapshot = record.lifecycle.snapshot();
      const uncertain = snapshot.uncertain;
      if (uncertain === undefined) {
        return record.lifecycle.reconcile(operationId, false);
      }
      let providerBodyExists: boolean;
      if (uncertain.operation === "provision") {
        providerBodyExists = await verifyProviderBody(record);
        if (!providerBodyExists) {
          await rm(dirname(record.planes.experiment), { recursive: true, force: true });
        }
      } else {
        providerBodyExists = await pathExists(dirname(record.planes.experiment));
      }
      const outcome = record.lifecycle.reconcile(operationId, providerBodyExists);
      await this.#persist(record);
      return outcome;
    });
  }

  async lifecycle(
    nodeId: string,
    operationId: string,
    operation: Exclude<EdgeLifecycleOperation, "provision" | "destroy">
  ): Promise<EdgeLifecycleOutcome> {
    validateOperationId(operationId);
    if (operation === "snapshot" || operation === "restore") {
      throw new Error("local unshare does not implement filesystem checkpoint/restore");
    }
    return this.#withLock(nodeId, async () => {
      const record = this.#record(nodeId);
      if (operation === "admit" && !await verifyProviderBody(record)) {
        throw new Error("cannot admit an unsealed or modified local body");
      }
      const outcome = record.lifecycle.apply(operationId, operation);
      if (outcome.disposition === "applied") await this.#persist(record);
      return outcome;
    });
  }

  async issueLease(
    nodeId: string,
    holder: string,
    generation: number,
    ttlMs: number
  ): Promise<LocalLeaseGrant> {
    if (!/^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/.test(holder)) {
      throw new Error("invalid lease holder");
    }
    return this.#withLock(nodeId, async () => {
      const record = this.#record(nodeId);
      if (
        record.lifecycle.state !== "admitted" &&
        record.lifecycle.state !== "running" &&
        record.lifecycle.state !== "frozen"
      ) {
        throw new Error("leases require an admitted node");
      }
      if (
        !Number.isSafeInteger(generation) ||
        generation <= record.highestLeaseGeneration
      ) {
        throw new Error("lease generation must monotonically fence prior leases");
      }
      if (!Number.isSafeInteger(ttlMs) || ttlMs < 1 || ttlMs > LOCAL_UNSHARE_POLICY.max_lease_ms) {
        throw new Error("lease TTL exceeds local profile policy");
      }
      const token = this.#token();
      const issuedAt = this.#now();
      const lease: EdgeNodeLease = {
        lease_id: `lease-${this.#token().slice(0, 24)}`,
        node_id: nodeId,
        generation,
        holder,
        authority_id: this.#authority.authority_id,
        profile: this.#authority.profile,
        issued_at: issuedAt.toISOString(),
        expires_at: new Date(issuedAt.getTime() + ttlMs).toISOString()
      };
      record.highestLeaseGeneration = generation;
      record.leaseTokens.clear();
      record.leaseActions.clear();
      record.leaseTokens.set(lease.lease_id, token);
      record.leaseActions.set(
        lease.lease_id,
        record.identity.input.capability.budget.actions
      );
      await this.#persist(record);
      return { lease, token };
    });
  }

  async execute(
    nodeId: string,
    lease: EdgeNodeLease,
    token: string
  ): Promise<EdgeNodeExecutionReceipt> {
    return this.#withLock(nodeId, async () => {
      const record = this.#authorized(nodeId, lease, token);
      const startedAt = this.#now();
      if (record.lifecycle.state !== "running") {
        return failedExecutionReceipt(
          record,
          lease,
          startedAt,
          this.#now(),
          "rejected",
          "node_not_running"
        );
      }
      const remainingActions = record.leaseActions.get(lease.lease_id) ?? 0;
      if (remainingActions < 1) {
        return failedExecutionReceipt(
          record,
          lease,
          startedAt,
          this.#now(),
          "rejected",
          "action_budget_exhausted"
        );
      }
      record.leaseActions.set(lease.lease_id, remainingActions - 1);
      let result: LocalExperimentResult;
      try {
        result = await this.#executor.run(record.planes.experiment, {
          wallTimeMs: record.identity.input.capability.budget.wall_time_ms,
          outputBytes: record.identity.input.capability.budget.artifact_bytes,
          memoryBytes: record.identity.input.resource_profile.memory_bytes,
          processLimit: record.identity.input.resource_profile.process_limit
        });
      } catch {
        const failed = await failedExecutionReceipt(
          record,
          lease,
          startedAt,
          this.#now(),
          "failed",
          "executor_failure"
        );
        await persistExecution(record, failed, []);
        return failed;
      }

      const observations = await observationDescriptors(record, lease.generation, result);
      const receipt: EdgeNodeExecutionReceipt = {
        schema_version: EDGE_NODE_SCHEMA_VERSION,
        receipt_id: `execution-${await sha256Hex(
          `${nodeId}:${lease.lease_id}:${lease.generation}`
        )}`,
        node_id: nodeId,
        capability_id: record.identity.input.capability.id,
        lease_id: lease.lease_id,
        lease_generation: lease.generation,
        status: result.exitCode === 0 ? "succeeded" : "failed",
        started_at: result.startedAt.toISOString(),
        completed_at: result.completedAt.toISOString(),
        exit_code: result.exitCode,
        observations: observations.map(({ descriptor }) => descriptor),
        ...(result.exitCode === 0 ? {} : { error_code: "nonzero_exit" })
      };
      await persistExecution(record, receipt, observations);
      for (const observation of observations) {
        record.observations.set(observation.descriptor.observation_id, observation);
      }
      return receipt;
    });
  }

  async exportEvidence(
    nodeId: string,
    lease: EdgeNodeLease,
    token: string
  ): Promise<EdgeEvidenceExportReceipt> {
    return this.#withLock(nodeId, async () => {
      const record = this.#authorized(nodeId, lease, token);
      const observations = [...record.observations.values()]
        .map(({ descriptor }) => descriptor)
        .filter(({ generation }) => generation === lease.generation)
        .sort((left, right) => left.observation_id.localeCompare(right.observation_id));
      if (observations.length === 0) throw new Error("no observations to export");

      const artifacts: EdgeEvidenceArtifact[] = [];
      for (const observation of observations) {
        const stored = record.observations.get(observation.observation_id);
        if (
          stored === undefined ||
          stored.body.byteLength !== observation.bytes ||
          await sha256Hex(stored.body) !== observation.sha256
        ) {
          throw new Error("observation integrity check failed");
        }
        artifacts.push({
          artifact_id: `evidence-${observation.observation_id}`,
          uri: `edge-evidence://${nodeId}/g${lease.generation}/evidence-${observation.observation_id}.bin`,
          node_id: nodeId,
          generation: lease.generation,
          sha256: observation.sha256,
          bytes: observation.bytes,
          media_type: "application/octet-stream"
        });
      }
      const evidenceRoot = await sha256Hex(canonicalJson({
        node_id: nodeId,
        identity_digest: record.identity.digest,
        generation: lease.generation,
        observation_ids: observations.map(({ observation_id }) => observation_id),
        artifacts
      }));
      const receipt: EdgeEvidenceExportReceipt = {
        schema_version: EDGE_NODE_SCHEMA_VERSION,
        receipt_id: `evidence-${evidenceRoot}`,
        node_id: nodeId,
        identity_digest: record.identity.digest,
        generation: lease.generation,
        observation_ids: observations.map(({ observation_id }) => observation_id),
        artifacts,
        evidence_root_sha256: evidenceRoot,
        exported_at: this.#now().toISOString(),
        direction: "observation-to-evidence"
      };

      const committed = join(record.planes.evidence_export, `g${lease.generation}`);
      if (await pathExists(committed)) {
        return verifyCommittedEvidence(committed, receipt);
      }
      await cleanupEvidenceStaging(record.planes.evidence_export, lease.generation);
      const staging = join(
        record.planes.evidence_export,
        `.staging-g${lease.generation}-${evidenceRoot}`
      );
      await mkdir(staging, { mode: 0o700 });
      try {
        for (const artifact of artifacts) {
          const observationId = artifact.artifact_id.slice("evidence-".length);
          const stored = record.observations.get(observationId);
          if (stored === undefined) throw new Error("observation disappeared during export");
          await writeBytesDurable(
            join(staging, `${artifact.artifact_id}.bin`),
            stored.body,
            0o400
          );
        }
        await writeJsonDurable(join(staging, "receipt.json"), receipt, 0o400);
        await fsyncDirectory(staging);
        await this.#faults.beforeEvidenceCommit?.();
        await rename(staging, committed);
        await fsyncDirectory(record.planes.evidence_export);
        await chmod(committed, 0o500);
        await this.#faults.afterEvidenceCommit?.();
      } catch (error) {
        await rm(staging, { recursive: true, force: true });
        throw error;
      }
      const capture = record.lifecycle.apply(
        `capture:evidence:g${lease.generation}`,
        "capture"
      );
      if (capture.disposition !== "applied") {
        throw new Error(capture.reason ?? "evidence capture lifecycle transition failed");
      }
      await this.#persist(record);
      return receipt;
    });
  }

  async reconstructionReceipt(
    nodeId: string,
    inputs: readonly EdgeReconstructionInput[]
  ): Promise<EdgeReconstructionReceipt> {
    return this.#withLock(nodeId, async () => {
      const record = this.#record(nodeId);
      if (inputs.length === 0 || inputs.some((input) => !HEX_64.test(input.sha256))) {
        throw new Error("reconstruction inputs require SHA-256 digests");
      }
      if (
        inputs.some(
          ({ name }) => !/^[a-z][a-z0-9._-]{0,63}$/.test(name)
        )
      ) {
        throw new Error("reconstruction input names must be bounded identifiers");
      }
      const byKind = new Map(inputs.map((input) => [input.kind, input]));
      const names = new Set(inputs.map(({ name }) => name));
      if (byKind.size !== inputs.length || names.size !== inputs.length) {
        throw new Error("reconstruction input names and kinds must be unique");
      }
      const expected = new Map<EdgeReconstructionInput["kind"], string>([
        ["source", sourceDigest(record.identity)],
        ["policy", record.identity.input.policy_revision.sha256],
        ["capability", await sha256Hex(canonicalJson(record.identity.input.capability))],
        ["resource", await sha256Hex(canonicalJson(record.identity.input.resource_profile))]
      ]);
      for (const [kind, sha256] of expected) {
        const input = byKind.get(kind);
        if (input === undefined || !input.required || input.sha256 !== sha256) {
          throw new Error(`reconstruction ${kind} input does not match node identity`);
        }
      }
      const snapshot = byKind.get("snapshot");
      if (snapshot !== undefined && record.lifecycle.state !== "snapshotted") {
        throw new Error("snapshot input is invalid for a node without a coherent snapshot");
      }
      const normalized = [...inputs].sort((left, right) =>
        compareCodeUnits(left.kind, right.kind) ||
        compareCodeUnits(left.name, right.name)
      );
      const inputsRoot = await sha256Hex(canonicalJson({
        node_id: nodeId,
        identity_digest: record.identity.digest,
        campaign_id: record.identity.input.membership.campaign_id,
        world_id: record.identity.input.membership.world_id,
        node_generation: record.identity.input.generation,
        membership_generation: record.identity.input.membership.generation,
        inputs: normalized
      }));
      return {
        schema_version: EDGE_NODE_SCHEMA_VERSION,
        receipt_id: `reconstruct-${await sha256Hex(`${nodeId}:${inputsRoot}`)}`,
        node_id: nodeId,
        identity_digest: record.identity.digest,
        inputs: normalized,
        inputs_root_sha256: inputsRoot,
        created_at: this.#now().toISOString()
      };
    });
  }

  async destroy(nodeId: string, operationId: string): Promise<EdgeLifecycleOutcome> {
    validateOperationId(operationId);
    return this.#withLock(nodeId, async () => {
      const record = this.#record(nodeId);
      const prior = outcomeFor(record.lifecycle, operationId);
      if (prior !== undefined) return replayOrConflict(prior, "destroy", record.lifecycle.state);
      const allowed = [
        "provisioned",
        "admitted",
        "frozen",
        "evidence-captured",
        "snapshotted",
        "retired"
      ];
      if (!allowed.includes(record.lifecycle.state)) {
        return record.lifecycle.apply(operationId, "destroy");
      }
      const uncertain = record.lifecycle.apply(operationId, "destroy", "uncertain");
      await this.#persist(record);
      try {
        await rm(dirname(record.planes.experiment), { recursive: true, force: true });
      } catch {
        return uncertain;
      }
      try {
        await this.#faults.afterDestroyEffect?.();
      } catch {
        return uncertain;
      }
      record.lifecycle.reconcile(
        `reconcile:${operationId}`,
        await pathExists(dirname(record.planes.experiment))
      );
      record.leaseTokens.clear();
      record.leaseActions.clear();
      await this.#persist(record);
      return record.lifecycle.apply(operationId, "destroy");
    });
  }

  async #persist(record: LocalNodeRecord): Promise<void> {
    await mkdir(record.planes.management, { recursive: true, mode: 0o700 });
    await assertSafeOptionalDirectory(record.planes.management);
    const identityPath = join(record.planes.management, "identity.json");
    const existing = await readJsonIfExists<EdgeNodeIdentity>(identityPath);
    if (existing === undefined) {
      await writeJsonDurable(identityPath, record.identity, 0o600);
    } else if (canonicalJson(existing) !== canonicalJson(record.identity)) {
      throw new Error("management identity changed during persistence");
    }
    const state: PersistedLocalState = {
      schema_version: LOCAL_STATE_SCHEMA_VERSION,
      identity_digest: record.identity.digest,
      lifecycle: record.lifecycle.snapshot(),
      highest_lease_generation: record.highestLeaseGeneration
    };
    await replaceJsonDurable(join(record.planes.management, "state.json"), state, 0o600);
  }

  async #recoverCommittedEvidence(record: LocalNodeRecord): Promise<void> {
    if (
      record.highestLeaseGeneration < 1 ||
      (record.lifecycle.state !== "running" && record.lifecycle.state !== "frozen")
    ) {
      return;
    }
    const committed = join(
      record.planes.evidence_export,
      `g${record.highestLeaseGeneration}`
    );
    const receipt = await readJsonIfExists<EdgeEvidenceExportReceipt>(
      join(committed, "receipt.json")
    );
    if (
      receipt === undefined ||
      receipt.node_id !== record.identity.node_id ||
      receipt.identity_digest !== record.identity.digest ||
      receipt.generation !== record.highestLeaseGeneration
    ) {
      return;
    }
    await verifyCommittedEvidence(committed, receipt);
    const capture = record.lifecycle.apply(
      `capture:evidence:g${record.highestLeaseGeneration}`,
      "capture"
    );
    if (capture.disposition === "applied") await this.#persist(record);
  }

  #authorized(nodeId: string, lease: EdgeNodeLease, token: string): LocalNodeRecord {
    const record = this.#record(nodeId);
    const expiry = Date.parse(lease.expires_at);
    if (
      lease.node_id !== nodeId ||
      lease.authority_id !== this.#authority.authority_id ||
      lease.profile !== this.#authority.profile ||
      lease.generation !== record.highestLeaseGeneration ||
      record.leaseTokens.get(lease.lease_id) !== token ||
      !Number.isFinite(expiry) ||
      expiry <= this.#now().getTime()
    ) {
      throw new Error("invalid, stale, or expired local node lease");
    }
    return record;
  }

  #record(nodeId: string): LocalNodeRecord {
    const record = this.#nodes.get(nodeId);
    if (record === undefined) throw new Error(`unknown local node: ${nodeId}`);
    return record;
  }

  #planeBindings(nodeId: string): EdgePlaneBindings {
    const nodeRoot = join(this.#root, "nodes", nodeId);
    return {
      management: join(this.#root, "management", nodeId),
      experiment: join(nodeRoot, "rootfs"),
      observation: join(this.#root, "observation", nodeId),
      evidence_export: join(this.#root, "evidence", nodeId)
    };
  }

  async #ensureProviderRoot(): Promise<void> {
    await mkdir(this.#root, { recursive: true, mode: 0o700 });
    if (await realpath(this.#root) !== this.#root) {
      throw new Error("local adapter root must not traverse a symbolic link");
    }
    const planeRoots = ["nodes", "management", "observation", "evidence"].map(
      (name) => join(this.#root, name)
    );
    await Promise.all(
      planeRoots.map((path) => mkdir(path, { recursive: true, mode: 0o700 }))
    );
    for (const path of planeRoots) {
      if (!await isRealDirectory(path) || await realpath(path) !== path) {
        throw new Error("local provider plane root must not traverse a symbolic link");
      }
    }
  }

  #validateLocalIdentity(input: EdgeNodeIdentityInput): void {
    if (
      input.provider.kind !== "local-unshare" ||
      input.provider.location !== "range-local" ||
      input.node_class !== "container" ||
      input.profile !== this.#authority.profile ||
      input.policy_revision.id !== this.#authority.policy_revision_id
    ) {
      throw new Error("node identity is outside this adapter authority");
    }
    if (input.source.kind !== "fixture") {
      throw new Error("local unshare accepts only digest-pinned fixture scripts");
    }
    if (
      !input.capability.planes.includes("experiment") ||
      input.capability.planes.includes("management") ||
      input.capability.planes.includes("evidence-export")
    ) {
      throw new Error("local capability cannot bind authoritative planes");
    }
    if (
      input.capability.budget.wall_time_ms > LOCAL_UNSHARE_POLICY.max_wall_time_ms ||
      input.capability.budget.actions > LOCAL_UNSHARE_POLICY.max_actions ||
      input.capability.budget.artifact_bytes > LOCAL_UNSHARE_POLICY.max_output_bytes ||
      input.resource_profile.memory_bytes > LOCAL_UNSHARE_POLICY.max_memory_bytes ||
      input.resource_profile.storage_bytes > LOCAL_UNSHARE_POLICY.max_rootfs_bytes ||
      input.resource_profile.process_limit > LOCAL_UNSHARE_POLICY.max_processes
    ) {
      throw new Error("node request exceeds local profile policy");
    }
  }

  async #withLock<T>(nodeId: string, action: () => Promise<T>): Promise<T> {
    const prior = this.#locks.get(nodeId) ?? Promise.resolve();
    let release!: () => void;
    const current = new Promise<void>((resolveLock) => {
      release = resolveLock;
    });
    const tail = prior.then(() => current);
    this.#locks.set(nodeId, tail);
    await prior;
    try {
      return await action();
    } finally {
      release();
      if (this.#locks.get(nodeId) === tail) this.#locks.delete(nodeId);
    }
  }
}

export class LinuxUnshareExecutor implements LocalExperimentExecutor {
  readonly #unshare: string;
  readonly #shell: string;

  constructor(unshare = "/usr/bin/unshare", shell = "/bin/bash") {
    this.#unshare = unshare;
    this.#shell = shell;
  }

  async prepare(rootfs: string, entrypoint: Uint8Array): Promise<void> {
    const rootMetadata = await lstat(rootfs);
    if (!rootMetadata.isDirectory() || rootMetadata.isSymbolicLink()) {
      throw new Error("rootfs staging path must be a real directory");
    }
    await mkdir(join(rootfs, "bin"), { mode: 0o755 });
    await mkdir(join(rootfs, "experiment"), { mode: 0o755 });
    await copyExecutable(rootfs, this.#shell, "/bin/sh");
    await writeBytesDurable(
      join(rootfs, "experiment", "entrypoint.sh"),
      entrypoint,
      0o555
    );
    await chmod(rootfs, 0o755);
  }

  async run(
    rootfs: string,
    budget: {
      readonly wallTimeMs: number;
      readonly outputBytes: number;
      readonly memoryBytes: number;
      readonly processLimit: number;
    }
  ): Promise<LocalExperimentResult> {
    if (!await isRealDirectory(rootfs)) throw new Error("sealed rootfs is missing");
    const startedAt = new Date();
    const args = [
      "--user",
      "--map-root-user",
      "--mount",
      "--propagation=private",
      "--pid",
      "--net",
      "--ipc",
      "--uts",
      "--fork",
      "--kill-child=KILL",
      this.#shell,
      "-c",
      "set -e; /usr/bin/mount --bind \"$1\" \"$1\"; /usr/bin/mount -o remount,bind,ro \"$1\"; ulimit -u \"$2\"; ulimit -v \"$3\"; exec /usr/bin/chroot \"$1\" /bin/sh /experiment/entrypoint.sh",
      "ordivon-local",
      rootfs,
      String(budget.processLimit),
      String(Math.floor(budget.memoryBytes / 1024))
    ];
    return new Promise((resolveRun, rejectRun) => {
      const child = spawn(this.#unshare, args, {
        env: {
          PATH: "/usr/bin:/bin",
          HOME: "/nonexistent",
          LANG: "C",
          LC_ALL: "C"
        },
        stdio: ["ignore", "pipe", "pipe"]
      });
      const stdout: Buffer[] = [];
      const stderr: Buffer[] = [];
      let bytes = 0;
      let exceeded = false;
      let timedOut = false;
      let settled = false;
      const rejectOnce = (error: Error) => {
        if (settled) return;
        settled = true;
        rejectRun(error);
      };
      const collect = (target: Buffer[]) => (chunk: Buffer) => {
        bytes += chunk.byteLength;
        if (bytes > budget.outputBytes) {
          exceeded = true;
          child.kill("SIGKILL");
          return;
        }
        target.push(chunk);
      };
      child.stdout.on("data", collect(stdout));
      child.stderr.on("data", collect(stderr));
      const timer = setTimeout(() => {
        timedOut = true;
        child.kill("SIGKILL");
      }, budget.wallTimeMs);
      child.once("error", (error) => {
        clearTimeout(timer);
        rejectOnce(error);
      });
      child.once("close", (code) => {
        clearTimeout(timer);
        if (exceeded) {
          rejectOnce(new Error("local experiment exceeded output budget"));
          return;
        }
        if (timedOut) {
          rejectOnce(new Error("local experiment exceeded wall-time budget"));
          return;
        }
        if (settled) return;
        settled = true;
        resolveRun({
          exitCode: code ?? 255,
          stdout: Buffer.concat(stdout),
          stderr: Buffer.concat(stderr),
          startedAt,
          completedAt: new Date()
        });
      });
    });
  }
}

function validateOperationId(operationId: string): void {
  if (!OPERATION_ID.test(operationId)) throw new Error("invalid lifecycle operation ID");
}

function sourceDigest(identity: EdgeNodeIdentity): string {
  const source = identity.input.source;
  if (source.kind === "fixture" || source.kind === "source-archive") return source.sha256;
  if (source.kind === "oci-image") return source.digest.slice("sha256:".length);
  throw new Error("worker versions are not executable by the local adapter");
}

function outcomeFor(
  lifecycle: EdgeNodeLifecycle,
  operationId: string
): EdgeLifecycleOutcome | undefined {
  return lifecycle.snapshot().outcomes.find(
    (outcome) => outcome.operation_id === operationId
  );
}

function replayOrConflict(
  prior: EdgeLifecycleOutcome,
  operation: EdgeLifecycleOperation,
  state: EdgeLifecycleOutcome["state"]
): EdgeLifecycleOutcome {
  if (prior.operation === operation) return prior;
  return {
    operation_id: prior.operation_id,
    operation,
    disposition: "rejected",
    state,
    reconciliation_required: prior.reconciliation_required,
    reason: "operation ID is bound to another operation"
  };
}

async function verifyProviderBody(record: LocalNodeRecord): Promise<boolean> {
  try {
    if (!await isRealDirectory(record.planes.experiment)) return false;
    const seal = await readJsonNoFollow<BodySeal>(
      join(record.planes.experiment, BODY_SEAL_NAME)
    );
    if (
      seal.schema_version !== EDGE_NODE_SCHEMA_VERSION ||
      seal.node_id !== record.identity.node_id ||
      seal.identity_digest !== record.identity.digest ||
      seal.source_sha256 !== sourceDigest(record.identity)
    ) {
      return false;
    }
    const manifest = await rootfsManifest(record.planes.experiment);
    return await sha256Hex(canonicalJson(manifest)) === seal.manifest_sha256;
  } catch {
    return false;
  }
}

async function rootfsManifest(rootfs: string): Promise<RootfsEntry[]> {
  const entries: RootfsEntry[] = [];
  async function walk(directory: string): Promise<void> {
    const children = await readdir(directory, { withFileTypes: true });
    children.sort((left, right) => compareCodeUnits(left.name, right.name));
    for (const child of children) {
      const path = join(directory, child.name);
      const relativePath = relative(rootfs, path).split(sep).join("/");
      if (relativePath === BODY_SEAL_NAME) continue;
      const metadata = await lstat(path);
      if (metadata.isSymbolicLink()) throw new Error("rootfs must not contain symbolic links");
      if (metadata.isDirectory()) {
        await walk(path);
        continue;
      }
      if (!metadata.isFile()) throw new Error("rootfs contains a non-regular file");
      const body = await readBytesNoFollow(path);
      entries.push({
        path: relativePath,
        sha256: await sha256Hex(body),
        bytes: body.byteLength,
        mode: metadata.mode & 0o777
      });
    }
  }
  await walk(rootfs);
  return entries;
}

async function observationDescriptors(
  record: LocalNodeRecord,
  generation: number,
  result: LocalExperimentResult
): Promise<Array<{ descriptor: EdgeObservation; body: Uint8Array }>> {
  const bodies: ReadonlyArray<{
    kind: EdgeObservation["kind"];
    body: Uint8Array;
  }> = [
    { kind: "stdout", body: result.stdout },
    { kind: "stderr", body: result.stderr },
    { kind: "exit", body: new TextEncoder().encode(String(result.exitCode)) }
  ];
  return Promise.all(
    bodies.map(async ({ kind, body }) => {
      const sha256 = await sha256Hex(body);
      return {
        descriptor: {
          observation_id: `g${generation}-${kind}-${sha256}`,
          node_id: record.identity.node_id,
          generation,
          captured_at: result.completedAt.toISOString(),
          kind,
          sha256,
          bytes: body.byteLength
        },
        body
      };
    })
  );
}

async function persistExecution(
  record: LocalNodeRecord,
  receipt: EdgeNodeExecutionReceipt,
  observations: readonly { descriptor: EdgeObservation; body: Uint8Array }[]
): Promise<void> {
  const committed = join(record.planes.observation, `g${receipt.lease_generation}`);
  const staging = join(
    record.planes.observation,
    `.staging-g${receipt.lease_generation}-${receipt.receipt_id}`
  );
  if (await pathExists(committed)) throw new Error("observation generation already committed");
  await mkdir(record.planes.observation, { recursive: true, mode: 0o700 });
  await rm(staging, { recursive: true, force: true });
  await mkdir(staging, { mode: 0o700 });
  try {
    for (const observation of observations) {
      const base = join(staging, observation.descriptor.observation_id);
      await writeBytesDurable(`${base}.bin`, observation.body, 0o600);
      await writeJsonDurable(`${base}.json`, observation.descriptor, 0o600);
    }
    await writeJsonDurable(join(staging, "execution-receipt.json"), receipt, 0o600);
    await fsyncDirectory(staging);
    await rename(staging, committed);
    await fsyncDirectory(record.planes.observation);
  } catch (error) {
    await rm(staging, { recursive: true, force: true });
    throw error;
  }
}

async function loadObservations(
  observationRoot: string,
  nodeId: string
): Promise<Map<string, { descriptor: EdgeObservation; body: Uint8Array }>> {
  const observations = new Map<
    string,
    { descriptor: EdgeObservation; body: Uint8Array }
  >();
  if (!await pathExists(observationRoot)) return observations;
  for (const generationEntry of await readdir(observationRoot, { withFileTypes: true })) {
    if (!generationEntry.isDirectory() || !/^g[1-9][0-9]*$/.test(generationEntry.name)) {
      continue;
    }
    const generationRoot = join(observationRoot, generationEntry.name);
    for (const entry of await readdir(generationRoot, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith(".json") || entry.name === "execution-receipt.json") {
        continue;
      }
      const descriptor = await readJsonNoFollow<EdgeObservation>(
        join(generationRoot, entry.name)
      );
      const body = await readBytesNoFollow(
        join(generationRoot, `${entry.name.slice(0, -".json".length)}.bin`)
      );
      if (
        descriptor.node_id !== nodeId ||
        descriptor.observation_id !== entry.name.slice(0, -".json".length) ||
        descriptor.generation !== Number(generationEntry.name.slice(1)) ||
        descriptor.bytes !== body.byteLength ||
        descriptor.sha256 !== await sha256Hex(body)
      ) {
        throw new Error("persisted observation integrity check failed");
      }
      observations.set(descriptor.observation_id, { descriptor, body });
    }
  }
  return observations;
}

async function failedExecutionReceipt(
  record: LocalNodeRecord,
  lease: EdgeNodeLease,
  startedAt: Date,
  completedAt: Date,
  status: "failed" | "rejected",
  errorCode: string
): Promise<EdgeNodeExecutionReceipt> {
  return {
    schema_version: EDGE_NODE_SCHEMA_VERSION,
    receipt_id: `execution-${await sha256Hex(
      `${record.identity.node_id}:${lease.lease_id}:${lease.generation}:${errorCode}`
    )}`,
    node_id: record.identity.node_id,
    capability_id: record.identity.input.capability.id,
    lease_id: lease.lease_id,
    lease_generation: lease.generation,
    status,
    started_at: startedAt.toISOString(),
    completed_at: completedAt.toISOString(),
    observations: [],
    error_code: errorCode
  };
}

async function verifyCommittedEvidence(
  committed: string,
  expected: EdgeEvidenceExportReceipt
): Promise<EdgeEvidenceExportReceipt> {
  const receipt = await readJsonNoFollow<EdgeEvidenceExportReceipt>(
    join(committed, "receipt.json")
  );
  const recomputedRoot = await sha256Hex(canonicalJson({
    node_id: receipt.node_id,
    identity_digest: receipt.identity_digest,
    generation: receipt.generation,
    observation_ids: receipt.observation_ids,
    artifacts: receipt.artifacts
  }));
  if (
    receipt.schema_version !== EDGE_NODE_SCHEMA_VERSION ||
    receipt.direction !== "observation-to-evidence" ||
    receipt.receipt_id !== `evidence-${receipt.evidence_root_sha256}` ||
    !Number.isFinite(Date.parse(receipt.exported_at)) ||
    receipt.node_id !== expected.node_id ||
    receipt.identity_digest !== expected.identity_digest ||
    receipt.generation !== expected.generation ||
    receipt.evidence_root_sha256 !== recomputedRoot ||
    receipt.evidence_root_sha256 !== expected.evidence_root_sha256 ||
    canonicalJson(receipt.artifacts) !== canonicalJson(expected.artifacts) ||
    canonicalJson(receipt.observation_ids) !== canonicalJson(expected.observation_ids)
  ) {
    throw new Error("committed evidence conflicts with requested export");
  }
  const observationIds = new Set(receipt.observation_ids);
  if (
    observationIds.size !== receipt.observation_ids.length ||
    receipt.artifacts.length !== receipt.observation_ids.length
  ) {
    throw new Error("committed evidence has ambiguous observation membership");
  }
  const artifactIds = new Set<string>();
  for (const artifact of receipt.artifacts) {
    const observationId = artifact.artifact_id.slice("evidence-".length);
    if (
      artifactIds.has(artifact.artifact_id) ||
      artifact.artifact_id !== `evidence-${observationId}` ||
      !/^g[1-9][0-9]*-(stdout|stderr|exit)-[a-f0-9]{64}$/.test(observationId) ||
      !observationIds.has(observationId) ||
      artifact.node_id !== receipt.node_id ||
      artifact.generation !== receipt.generation ||
      artifact.sha256 !== observationId.slice(observationId.lastIndexOf("-") + 1) ||
      !Number.isSafeInteger(artifact.bytes) ||
      artifact.bytes < 0 ||
      artifact.media_type !== "application/octet-stream" ||
      artifact.uri !==
        `edge-evidence://${receipt.node_id}/g${receipt.generation}/${artifact.artifact_id}.bin`
    ) {
      throw new Error("committed evidence contains an invalid artifact reference");
    }
    artifactIds.add(artifact.artifact_id);
    const artifactPath = join(committed, `${artifact.artifact_id}.bin`);
    const artifactMetadata = await lstat(artifactPath);
    if (!artifactMetadata.isFile() || artifactMetadata.size !== artifact.bytes) {
      throw new Error("committed evidence artifact size mismatch");
    }
    await verifyEvidenceArtifact(
      artifactPath,
      artifact.sha256
    );
  }
  return receipt;
}

async function cleanupEvidenceStaging(root: string, generation: number): Promise<void> {
  await mkdir(root, { recursive: true, mode: 0o700 });
  for (const entry of await readdir(root, { withFileTypes: true })) {
    if (
      entry.isDirectory() &&
      entry.name.startsWith(`.staging-g${generation}-`)
    ) {
      await rm(join(root, entry.name), { recursive: true, force: true });
    }
  }
}

async function cleanupManagementTemps(managementRoot: string): Promise<void> {
  if (!await isRealDirectory(managementRoot)) return;
  for (const entry of await readdir(managementRoot, { withFileTypes: true })) {
    if (
      entry.isFile() &&
      entry.name.startsWith(".state.json.") &&
      entry.name.endsWith(".tmp")
    ) {
      await rm(join(managementRoot, entry.name), { force: true });
    }
  }
}

async function assertSafeOptionalDirectory(path: string): Promise<void> {
  if (!await pathExists(path)) return;
  if (!await isRealDirectory(path) || await realpath(path) !== path) {
    throw new Error("local provider path must be a real directory");
  }
}

function parseLddDependencies(output: string): Array<{
  readonly source: string;
  readonly installPaths: readonly string[];
}> {
  const dependencies = new Map<string, Set<string>>();
  for (const rawLine of output.split("\n")) {
    const line = rawLine.trim();
    if (line.length === 0 || line.startsWith("linux-vdso")) continue;
    if (line.includes("not found")) throw new Error("local shell dependency is missing");
    const alias = /^(\/\S+)\s+=>\s+(\/\S+)\s+\(0x[0-9a-f]+\)$/i.exec(line);
    const resolved = /^(?:\S+\s+=>\s+)?(\/\S+)\s+\(0x[0-9a-f]+\)$/i.exec(line);
    const source = alias?.[2] ?? resolved?.[1];
    if (source === undefined) continue;
    const paths = dependencies.get(source) ?? new Set<string>();
    paths.add(source);
    if (alias?.[1] !== undefined) paths.add(alias[1]);
    dependencies.set(source, paths);
  }
  if (dependencies.size === 0) throw new Error("could not resolve local shell dependencies");
  return [...dependencies].map(([source, installPaths]) => ({
    source,
    installPaths: [...installPaths]
  }));
}

function compareCodeUnits(left: string, right: string): number {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

async function copyExecutable(
  rootfs: string,
  executable: string,
  installedPath: string
): Promise<void> {
  const trustedExecutable = await realpath(executable);
  const metadata = await stat(trustedExecutable);
  if (!metadata.isFile()) throw new Error("configured executable is not a regular file");
  await copyIntoRootfs(rootfs, trustedExecutable, installedPath, 0o555);
  const { stdout, stderr } = await execFileAsync("ldd", [trustedExecutable], {
    env: { PATH: "/usr/bin:/bin", LANG: "C", LC_ALL: "C" },
    maxBuffer: 64 * 1024
  });
  if (stderr.trim().length > 0) throw new Error("ldd emitted unexpected diagnostics");
  for (const dependency of parseLddDependencies(stdout)) {
    for (const installPath of dependency.installPaths) {
      const mode = /(?:^|\/)ld-[^/]*\.so|(?:^|\/)ld-linux[^/]*\.so/.test(
        dependency.source
      )
        ? 0o555
        : 0o444;
      await copyIntoRootfs(rootfs, dependency.source, installPath, mode);
    }
  }
}

async function copyIntoRootfs(
  rootfs: string,
  source: string,
  installedPath: string,
  mode: number
): Promise<void> {
  if (!installedPath.startsWith("/") || installedPath.includes("\0")) {
    throw new Error("invalid rootfs installation path");
  }
  const target = join(rootfs, installedPath);
  if (!isWithin(rootfs, target)) throw new Error("rootfs installation escaped staging");
  await mkdir(dirname(target), { recursive: true, mode: 0o755 });
  if (await pathExists(target)) {
    const existing = await readBytesNoFollow(target);
    const sourceBody = new Uint8Array(await readFile(source));
    if (await sha256Hex(existing) !== await sha256Hex(sourceBody)) {
      throw new Error("rootfs dependency path collision");
    }
    return;
  }
  await copyFile(source, target, fsConstants.COPYFILE_EXCL);
  await chmod(target, mode);
}

function isWithin(root: string, candidate: string): boolean {
  const path = relative(root, candidate);
  return path.length > 0 && path !== ".." && !path.startsWith(`..${sep}`);
}

async function syncTree(root: string): Promise<void> {
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = join(root, entry.name);
    if (entry.isDirectory()) {
      await syncTree(path);
      await fsyncDirectory(path);
    } else if (entry.isFile()) {
      const handle = await open(path, "r");
      try {
        await handle.sync();
      } finally {
        await handle.close();
      }
    }
  }
  await fsyncDirectory(root);
}

async function writeBytesDurable(
  path: string,
  body: Uint8Array | string,
  mode: number
): Promise<void> {
  const handle = await open(path, "wx", mode);
  try {
    await handle.writeFile(body);
    await handle.sync();
  } finally {
    await handle.close();
  }
}

async function writeJsonDurable(path: string, value: unknown, mode: number): Promise<void> {
  await writeBytesDurable(path, `${canonicalJson(value)}\n`, mode);
  await fsyncDirectory(dirname(path));
}

async function replaceJsonDurable(
  path: string,
  value: unknown,
  mode: number
): Promise<void> {
  const temporary = join(
    dirname(path),
    `.${basename(path)}.${crypto.randomUUID()}.tmp`
  );
  await writeJsonDurable(temporary, value, mode);
  try {
    await rename(temporary, path);
    await fsyncDirectory(dirname(path));
  } catch (error) {
    await rm(temporary, { force: true });
    throw error;
  }
}

async function fsyncDirectory(path: string): Promise<void> {
  const handle = await open(path, "r");
  try {
    await handle.sync();
  } finally {
    await handle.close();
  }
}

async function readJsonIfExists<T>(path: string): Promise<T | undefined> {
  try {
    return await readJsonNoFollow<T>(path);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
    throw error;
  }
}

async function readJsonNoFollow<T>(path: string): Promise<T> {
  return JSON.parse(new TextDecoder().decode(await readBytesNoFollow(path))) as T;
}

async function readBytesNoFollow(path: string): Promise<Uint8Array> {
  const handle = await open(
    path,
    fsConstants.O_RDONLY | (fsConstants.O_NOFOLLOW ?? 0)
  );
  try {
    const metadata = await handle.stat();
    if (!metadata.isFile()) throw new Error("expected a regular file");
    return new Uint8Array(await handle.readFile());
  } finally {
    await handle.close();
  }
}

async function isRealDirectory(path: string): Promise<boolean> {
  try {
    const metadata = await lstat(path);
    return metadata.isDirectory() && !metadata.isSymbolicLink();
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw error;
  }
}

async function pathExists(path: string): Promise<boolean> {
  try {
    await lstat(path);
    return true;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw error;
  }
}

export async function verifyEvidenceArtifact(
  path: string,
  expectedSha256: string
): Promise<void> {
  if (!HEX_64.test(expectedSha256)) throw new Error("invalid expected SHA-256");
  if (await sha256Hex(await readBytesNoFollow(path)) !== expectedSha256) {
    throw new Error("evidence artifact digest mismatch");
  }
}
