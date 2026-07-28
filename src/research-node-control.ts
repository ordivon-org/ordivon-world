import { access, mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

import {
  LinuxUnshareExecutor,
  LocalDisposableNodeAdapter,
  type LocalExperimentExecutor,
  type LocalLeaseGrant,
  type LocalNodeInspection
} from "./local-node-adapter.js";
import {
  canonicalJson,
  sha256Hex,
  type EdgeEvidenceExportReceipt,
  type EdgeNodeIdentity,
  type EdgeNodeIdentityInput,
  type EdgeProfileAuthority,
  type EdgeReconstructionInput
} from "./node-contracts.js";
import { EDGE_NODE_PROFILE_POLICY } from "./node-policy.js";

const CONTROL_SCHEMA_VERSION = 1 as const;
const MAX_REQUEST_BYTES = 1024 * 1024;
const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/;
const SECURITY_OPERATION = /^(prepare|start|freeze|reset|destroy|reconstruct|verify)$/;

export type SecurityNodeOperation =
  | "prepare"
  | "start"
  | "freeze"
  | "reset"
  | "destroy"
  | "reconstruct"
  | "verify";

export interface ResearchNodeControlOptions {
  readonly root: string;
  readonly executorFactory?: () => LocalExperimentExecutor;
  readonly now?: () => Date;
  readonly token?: () => string;
}

export interface BindingSnapshot {
  readonly native_id: string;
  readonly revision: string;
  readonly root_digest: string;
  readonly metadata: Readonly<Record<string, unknown>>;
}

interface ControlState {
  readonly schema_version: typeof CONTROL_SCHEMA_VERSION;
  readonly current_epoch: number;
  readonly node_id: string;
  readonly identity_digest: string;
}

interface OperationJournal {
  readonly schema_version: typeof CONTROL_SCHEMA_VERSION;
  readonly operation_id: string;
  readonly operation: SecurityNodeOperation;
  readonly epoch_before: number;
  readonly state: "prepared" | "succeeded";
  readonly result?: Readonly<Record<string, unknown>>;
}

interface DeclareRequest {
  readonly schema_version: typeof CONTROL_SCHEMA_VERSION;
  readonly request_id: string;
  readonly action: "declare";
  readonly input: EdgeNodeIdentityInput;
  readonly entrypoint_base64: string;
}

interface SnapshotRequest {
  readonly schema_version: typeof CONTROL_SCHEMA_VERSION;
  readonly request_id: string;
  readonly action: "snapshot" | "residual";
}

interface ExecuteRequest {
  readonly schema_version: typeof CONTROL_SCHEMA_VERSION;
  readonly request_id: string;
  readonly action: "execute" | "reconcile";
  readonly operation: SecurityNodeOperation;
  readonly operation_id: string;
}

export type ResearchNodeControlRequest = DeclareRequest | SnapshotRequest | ExecuteRequest;

export interface ResearchNodeControlSuccess {
  readonly schema_version: typeof CONTROL_SCHEMA_VERSION;
  readonly request_id: string;
  readonly ok: true;
  readonly result: Readonly<Record<string, unknown>>;
}

export interface ResearchNodeControlFailure {
  readonly schema_version: typeof CONTROL_SCHEMA_VERSION;
  readonly request_id: string;
  readonly ok: false;
  readonly error: {
    readonly code: "invalid_request" | "not_declared" | "operation_unknown" | "operation_failed";
    readonly message: string;
  };
}

export type ResearchNodeControlResponse =
  | ResearchNodeControlSuccess
  | ResearchNodeControlFailure;

const RESEARCH_AUTHORITY: EdgeProfileAuthority = {
  authority_id: EDGE_NODE_PROFILE_POLICY.research.authority_id,
  profile: "research",
  credential_mode: "none",
  credential_scope: EDGE_NODE_PROFILE_POLICY.research.credential_scope,
  policy_revision_id: "research-policy-v1"
};

export class ResearchNodeControlSession {
  readonly #root: string;
  readonly #executorFactory: () => LocalExperimentExecutor;
  readonly #now: () => Date;
  readonly #token: () => string;
  #epoch = 1;
  #adapter: LocalDisposableNodeAdapter;
  #identityInput: EdgeNodeIdentityInput | undefined;
  #identity: EdgeNodeIdentity | undefined;
  #entrypoint: Uint8Array | undefined;
  #grant: LocalLeaseGrant | undefined;

  constructor(options: ResearchNodeControlOptions) {
    this.#root = resolve(options.root);
    this.#executorFactory = options.executorFactory ?? (() => new LinuxUnshareExecutor());
    this.#now = options.now ?? (() => new Date());
    this.#token = options.token ?? (() => crypto.randomUUID().replaceAll("-", ""));
    this.#adapter = this.#newAdapter(this.#epoch);
  }

  async handle(raw: unknown): Promise<ResearchNodeControlResponse> {
    let requestId = "invalid-request";
    try {
      const request = validateRequest(raw);
      requestId = request.request_id;
      const result = await this.#dispatch(request);
      return {
        schema_version: CONTROL_SCHEMA_VERSION,
        request_id: requestId,
        ok: true,
        result
      };
    } catch (error) {
      const message = boundedMessage(error);
      return {
        schema_version: CONTROL_SCHEMA_VERSION,
        request_id: requestId,
        ok: false,
        error: {
          code: classifyError(message),
          message
        }
      };
    }
  }

  async #dispatch(
    request: ResearchNodeControlRequest
  ): Promise<Readonly<Record<string, unknown>>> {
    switch (request.action) {
      case "declare":
        return this.#declare(request.input, request.entrypoint_base64);
      case "snapshot":
        return this.#snapshotResult();
      case "execute":
        return this.#execute(request.operation, request.operation_id);
      case "reconcile":
        return this.#reconcile(request.operation, request.operation_id);
      case "residual":
        return this.#residual();
    }
  }

  async #declare(
    input: EdgeNodeIdentityInput,
    entrypointBase64: string
  ): Promise<Readonly<Record<string, unknown>>> {
    if (!/^[A-Za-z0-9+/]*={0,2}$/.test(entrypointBase64)) {
      throw new Error("invalid_request: entrypoint_base64 is not canonical base64 text");
    }
    const entrypoint = Uint8Array.from(Buffer.from(entrypointBase64, "base64"));
    if (entrypoint.byteLength === 0) {
      throw new Error("invalid_request: entrypoint is empty");
    }
    const source = input.source;
    if (source.kind !== "fixture") {
      throw new Error("invalid_request: research control v0 accepts only fixture sources");
    }
    if (await sha256Hex(entrypoint) !== source.sha256) {
      throw new Error("invalid_request: entrypoint digest differs from declared source");
    }
    const candidate = await this.#restoreControlState(input);
    const identity = await this.#adapter.declare(input);
    if (candidate !== undefined && (
      candidate.node_id !== identity.node_id ||
      candidate.identity_digest !== identity.digest
    )) {
      throw new Error("operation_failed: persisted control identity differs from declaration");
    }
    if (this.#identity !== undefined && canonicalJson(this.#identity.input) !== canonicalJson(input)) {
      throw new Error("invalid_request: control session is already bound to another identity");
    }
    this.#identityInput = JSON.parse(canonicalJson(input)) as EdgeNodeIdentityInput;
    this.#identity = identity;
    this.#entrypoint = entrypoint;
    await this.#writeControlState();
    return {
      identity,
      snapshot: this.#bindingSnapshot(identity),
      inspection: this.#adapter.inspect(identity.node_id)
    };
  }

  async #restoreControlState(input: EdgeNodeIdentityInput): Promise<ControlState | undefined> {
    const persisted = await readJsonIfExists<ControlState>(this.#statePath());
    if (persisted === undefined) return undefined;
    if (
      persisted.schema_version !== CONTROL_SCHEMA_VERSION ||
      !Number.isSafeInteger(persisted.current_epoch) ||
      persisted.current_epoch < 1
    ) {
      throw new Error("operation_failed: invalid research control state");
    }
    const digest = await sha256Hex(canonicalJson(input));
    const nodeId = `edge-${digest.slice(0, 32)}`;
    if (persisted.node_id !== nodeId || persisted.identity_digest !== digest) {
      throw new Error("operation_failed: research control root belongs to another Node");
    }
    if (this.#epoch !== persisted.current_epoch) {
      this.#epoch = persisted.current_epoch;
      this.#adapter = this.#newAdapter(this.#epoch);
    }
    return persisted;
  }

  #snapshotResult(): Readonly<Record<string, unknown>> {
    const identity = this.#requireIdentity();
    return {
      snapshot: this.#bindingSnapshot(identity),
      inspection: this.#adapter.inspect(identity.node_id),
      provider_epoch: this.#epoch
    };
  }

  async #execute(
    operation: SecurityNodeOperation,
    operationId: string
  ): Promise<Readonly<Record<string, unknown>>> {
    const journal = await this.#readOperation(operationId);
    if (journal !== undefined) {
      if (journal.operation !== operation) {
        throw new Error("invalid_request: operation ID is bound to another operation");
      }
      if (journal.state === "succeeded" && journal.result !== undefined) return journal.result;
      return this.#reconcile(operation, operationId);
    }
    const epochBefore = this.#epoch;
    await this.#writeOperation({
      schema_version: CONTROL_SCHEMA_VERSION,
      operation_id: operationId,
      operation,
      epoch_before: epochBefore,
      state: "prepared"
    });
    const result = await this.#apply(operation, operationId);
    await this.#writeOperation({
      schema_version: CONTROL_SCHEMA_VERSION,
      operation_id: operationId,
      operation,
      epoch_before: epochBefore,
      state: "succeeded",
      result
    });
    return result;
  }

  async #apply(
    operation: SecurityNodeOperation,
    operationId: string
  ): Promise<Readonly<Record<string, unknown>>> {
    const identity = this.#requireIdentity();
    const entrypoint = this.#requireEntrypoint();
    switch (operation) {
      case "prepare": {
        const provision = await this.#adapter.provision(
          identity.node_id,
          await nativeOperationId(operationId, "provision"),
          entrypoint
        );
        if (provision.reconciliation_required) {
          throw new Error("operation_unknown: provision requires native reconciliation");
        }
        const admit = await this.#adapter.lifecycle(
          identity.node_id,
          await nativeOperationId(operationId, "admit"),
          "admit"
        );
        requireApplied(admit, "prepare admission");
        return this.#operationResult(operation, operationId, { provision, admit });
      }
      case "start": {
        const start = await this.#adapter.lifecycle(
          identity.node_id,
          await nativeOperationId(operationId, "start"),
          "start"
        );
        requireApplied(start, "start");
        const inspection = this.#adapter.inspect(identity.node_id);
        this.#grant = await this.#adapter.issueLease(
          identity.node_id,
          "security-campaign",
          inspection.highest_lease_generation + 1,
          300_000
        );
        const execution = await this.#adapter.execute(
          identity.node_id,
          this.#grant.lease,
          this.#grant.token
        );
        if (execution.status !== "succeeded") {
          throw new Error(`operation_failed: Edge execution ${execution.status}`);
        }
        return this.#operationResult(operation, operationId, { start, execution });
      }
      case "freeze": {
        const state = this.#adapter.inspect(identity.node_id).lifecycle.state;
        const freeze = state === "running"
          ? await this.#adapter.lifecycle(
              identity.node_id,
              await nativeOperationId(operationId, "freeze"),
              "freeze"
            )
          : undefined;
        if (freeze !== undefined) requireApplied(freeze, "freeze");
        let evidence: EdgeEvidenceExportReceipt | undefined;
        if (this.#grant !== undefined) {
          evidence = await this.#adapter.exportEvidence(
            identity.node_id,
            this.#grant.lease,
            this.#grant.token
          );
        }
        return this.#operationResult(operation, operationId, { freeze, evidence });
      }
      case "reset":
        return this.#reset(operationId);
      case "destroy":
        return this.#destroy(operationId);
      case "reconstruct":
        return this.#reconstruct(operationId);
      case "verify":
        return this.#operationResult(operation, operationId, {
          inspection: this.#adapter.inspect(identity.node_id)
        });
    }
  }

  async #reset(operationId: string): Promise<Readonly<Record<string, unknown>>> {
    const identity = this.#requireIdentity();
    await this.#destroyCurrent(`${operationId}:old`);
    this.#epoch += 1;
    this.#adapter = this.#newAdapter(this.#epoch);
    const recreated = await this.#adapter.declare(this.#requireInput());
    const provision = await this.#adapter.provision(
      recreated.node_id,
      await nativeOperationId(operationId, "reset-provision"),
      this.#requireEntrypoint()
    );
    if (provision.reconciliation_required) {
      throw new Error("operation_unknown: reset provision requires native reconciliation");
    }
    const admit = await this.#adapter.lifecycle(
      recreated.node_id,
      await nativeOperationId(operationId, "reset-admit"),
      "admit"
    );
    requireApplied(admit, "reset admission");
    this.#grant = undefined;
    await this.#writeControlState();
    return this.#operationResult("reset", operationId, {
      previous_node_id: identity.node_id,
      provider_epoch: this.#epoch,
      provision,
      admit,
      snapshot: this.#bindingSnapshot(recreated)
    });
  }

  async #destroy(operationId: string): Promise<Readonly<Record<string, unknown>>> {
    const outcomes = await this.#destroyCurrent(operationId);
    return this.#operationResult("destroy", operationId, outcomes);
  }

  async #destroyCurrent(operationId: string): Promise<Readonly<Record<string, unknown>>> {
    const identity = this.#requireIdentity();
    let state = this.#adapter.inspect(identity.node_id).lifecycle.state;
    let freeze: unknown;
    let evidence: unknown;
    if (state === "running") {
      freeze = await this.#adapter.lifecycle(
        identity.node_id,
        await nativeOperationId(operationId, "freeze"),
        "freeze"
      );
      state = this.#adapter.inspect(identity.node_id).lifecycle.state;
    }
    if (this.#grant !== undefined && (state === "frozen" || state === "running")) {
      evidence = await this.#adapter.exportEvidence(
        identity.node_id,
        this.#grant.lease,
        this.#grant.token
      );
      state = this.#adapter.inspect(identity.node_id).lifecycle.state;
    }
    const destroy = await this.#adapter.destroy(
      identity.node_id,
      await nativeOperationId(operationId, "destroy")
    );
    if (destroy.reconciliation_required) {
      throw new Error("operation_unknown: destroy requires native reconciliation");
    }
    if (destroy.state !== "destroyed") {
      throw new Error(`operation_failed: destroy ended in ${destroy.state}`);
    }
    this.#grant = undefined;
    return { freeze, evidence, destroy };
  }

  async #reconstruct(operationId: string): Promise<Readonly<Record<string, unknown>>> {
    const identity = this.#requireIdentity();
    const token = (await sha256Hex(operationId)).slice(0, 24);
    const root = join(this.#root, "reconstruction", token);
    await rm(root, { recursive: true, force: true });
    const adapter = new LocalDisposableNodeAdapter({
      root,
      authority: RESEARCH_AUTHORITY,
      executor: this.#executorFactory(),
      now: this.#now,
      token: this.#token
    });
    try {
      const recreated = await adapter.declare(this.#requireInput());
      const provision = await adapter.provision(
        recreated.node_id,
        await nativeOperationId(operationId, "reconstruct-provision"),
        this.#requireEntrypoint()
      );
      if (provision.state !== "provisioned") {
        throw new Error("operation_failed: reconstructed body was not provisioned");
      }
      const reconstruction = await adapter.reconstructionReceipt(
        recreated.node_id,
        await reconstructionInputs(recreated.input)
      );
      await adapter.destroy(
        recreated.node_id,
        await nativeOperationId(operationId, "reconstruct-destroy")
      );
      return this.#operationResult("reconstruct", operationId, {
        reconstruction,
        snapshot: this.#bindingSnapshot(identity),
        fresh_root_removed: true
      });
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  }

  async #reconcile(
    operation: SecurityNodeOperation,
    operationId: string
  ): Promise<Readonly<Record<string, unknown>>> {
    const journal = await this.#readOperation(operationId);
    if (journal === undefined || journal.operation !== operation) {
      throw new Error("operation_unknown: no matching native operation journal");
    }
    if (journal.state === "succeeded" && journal.result !== undefined) return journal.result;
    const identity = this.#requireIdentity();
    const inspection = this.#adapter.inspect(identity.node_id);
    const state = inspection.lifecycle.state;
    const proved =
      (operation === "prepare" && ["admitted", "running", "frozen", "evidence-captured"].includes(state)) ||
      (operation === "start" && ["running", "frozen", "evidence-captured"].includes(state)) ||
      (operation === "freeze" && ["frozen", "evidence-captured", "retired", "destroyed"].includes(state)) ||
      (operation === "reset" && this.#epoch > journal.epoch_before && state === "admitted") ||
      (operation === "destroy" && state === "destroyed") ||
      operation === "verify";
    if (!proved) {
      throw new Error("operation_unknown: native state does not prove the operation outcome");
    }
    const result = this.#operationResult(operation, operationId, {
      reconciled: true,
      inspection
    });
    await this.#writeOperation({ ...journal, state: "succeeded", result });
    return result;
  }

  async #residual(): Promise<Readonly<Record<string, unknown>>> {
    const identity = this.#requireIdentity();
    const inspection = this.#adapter.inspect(identity.node_id);
    const body = dirname(inspection.planes.experiment);
    const bodyExists = await pathExists(body);
    const checks = [
      {
        component: "edge",
        subject_id: `edge-node:${identity.node_id}:body`,
        status: bodyExists ? "unexpected_residual" : "clean",
        detail: bodyExists
          ? "provider body remains after requested destruction"
          : "provider body is absent",
        evidence_ref: null
      },
      {
        component: "edge",
        subject_id: `edge-node:${identity.node_id}:management`,
        status: "expected_retained",
        detail: "identity and lifecycle journal are retained as management evidence",
        evidence_ref: `file://${inspection.planes.management}`
      },
      {
        component: "edge",
        subject_id: `edge-node:${identity.node_id}:evidence`,
        status: "expected_retained",
        detail: "generation-scoped evidence is retained outside the disposable body",
        evidence_ref: `file://${inspection.planes.evidence_export}`
      }
    ];
    return { checks, inspection };
  }

  #operationResult(
    operation: SecurityNodeOperation,
    operationId: string,
    detail: Readonly<Record<string, unknown>>
  ): Readonly<Record<string, unknown>> {
    const identity = this.#requireIdentity();
    return {
      schema_version: CONTROL_SCHEMA_VERSION,
      project: "edge",
      operation,
      operation_id: operationId,
      node_id: identity.node_id,
      identity_digest: identity.digest,
      provider_epoch: this.#epoch,
      detail: Object.fromEntries(
        Object.entries(detail).filter(([, value]) => value !== undefined)
      ),
      inspection: this.#adapter.inspect(identity.node_id)
    };
  }

  #bindingSnapshot(identity: EdgeNodeIdentity): BindingSnapshot {
    return {
      native_id: identity.node_id,
      revision: `edge-node-v1:${identity.digest}`,
      root_digest: `sha256:${identity.digest}`,
      metadata: {
        schema_version: CONTROL_SCHEMA_VERSION,
        provider_id: identity.input.provider.id,
        provider_kind: identity.input.provider.kind,
        profile: identity.input.profile,
        node_class: identity.input.node_class,
        node_generation: identity.input.generation,
        membership_generation: identity.input.membership.generation,
        source_kind: identity.input.source.kind,
        consequence_scope: identity.input.capability.consequence_scope
      }
    };
  }

  #newAdapter(epoch: number): LocalDisposableNodeAdapter {
    return new LocalDisposableNodeAdapter({
      root: join(this.#root, "epochs", String(epoch).padStart(4, "0")),
      authority: RESEARCH_AUTHORITY,
      executor: this.#executorFactory(),
      now: this.#now,
      token: this.#token
    });
  }

  #requireIdentity(): EdgeNodeIdentity {
    if (this.#identity === undefined) throw new Error("not_declared: Node is not declared");
    return this.#identity;
  }

  #requireInput(): EdgeNodeIdentityInput {
    if (this.#identityInput === undefined) throw new Error("not_declared: Node is not declared");
    return this.#identityInput;
  }

  #requireEntrypoint(): Uint8Array {
    if (this.#entrypoint === undefined) throw new Error("not_declared: Node is not declared");
    return this.#entrypoint;
  }

  #statePath(): string {
    return join(this.#root, "control", "state.json");
  }

  async #writeControlState(): Promise<void> {
    const identity = this.#requireIdentity();
    await writeJsonAtomic(this.#statePath(), {
      schema_version: CONTROL_SCHEMA_VERSION,
      current_epoch: this.#epoch,
      node_id: identity.node_id,
      identity_digest: identity.digest
    } satisfies ControlState);
  }

  async #operationPath(operationId: string): Promise<string> {
    return join(this.#root, "control", "operations", `${await sha256Hex(operationId)}.json`);
  }

  async #readOperation(operationId: string): Promise<OperationJournal | undefined> {
    const journal = await readJsonIfExists<OperationJournal>(
      await this.#operationPath(operationId)
    );
    if (journal !== undefined && journal.operation_id !== operationId) {
      throw new Error("operation_failed: operation journal identity mismatch");
    }
    return journal;
  }

  async #writeOperation(journal: OperationJournal): Promise<void> {
    await writeJsonAtomic(await this.#operationPath(journal.operation_id), journal);
  }
}

function validateRequest(raw: unknown): ResearchNodeControlRequest {
  if (raw === null || Array.isArray(raw) || typeof raw !== "object") {
    throw new Error("invalid_request: request must be an object");
  }
  if (Buffer.byteLength(JSON.stringify(raw), "utf8") > MAX_REQUEST_BYTES) {
    throw new Error("invalid_request: request exceeds byte limit");
  }
  const value = raw as Record<string, unknown>;
  if (value.schema_version !== CONTROL_SCHEMA_VERSION) {
    throw new Error("invalid_request: unsupported schema_version");
  }
  if (typeof value.request_id !== "string" || !REQUEST_ID.test(value.request_id)) {
    throw new Error("invalid_request: request_id is invalid");
  }
  if (!new Set(["declare", "snapshot", "execute", "reconcile", "residual"]).has(String(value.action))) {
    throw new Error("invalid_request: action is unsupported");
  }
  if ((value.action === "execute" || value.action === "reconcile") && (
    typeof value.operation !== "string" ||
    !SECURITY_OPERATION.test(value.operation) ||
    typeof value.operation_id !== "string" ||
    !REQUEST_ID.test(value.operation_id)
  )) {
    throw new Error("invalid_request: operation or operation_id is invalid");
  }
  if (value.action === "declare" && (
    value.input === null ||
    Array.isArray(value.input) ||
    typeof value.input !== "object" ||
    typeof value.entrypoint_base64 !== "string"
  )) {
    throw new Error("invalid_request: declaration input is invalid");
  }
  return value as unknown as ResearchNodeControlRequest;
}

async function nativeOperationId(operationId: string, suffix: string): Promise<string> {
  return `security:${suffix}:${(await sha256Hex(operationId)).slice(0, 40)}`;
}

function requireApplied(
  outcome: { readonly disposition: string; readonly reason?: string },
  label: string
): void {
  if (outcome.disposition !== "applied") {
    throw new Error(`operation_failed: ${label} rejected: ${outcome.reason ?? "unknown"}`);
  }
}

async function reconstructionInputs(
  input: EdgeNodeIdentityInput
): Promise<EdgeReconstructionInput[]> {
  const source = input.source;
  if (source.kind !== "fixture") throw new Error("operation_failed: unsupported source kind");
  return [
    { name: "policy", kind: "policy", sha256: input.policy_revision.sha256, required: true },
    {
      name: "capability",
      kind: "capability",
      sha256: await sha256Hex(canonicalJson(input.capability)),
      required: true
    },
    {
      name: "resource",
      kind: "resource",
      sha256: await sha256Hex(canonicalJson(input.resource_profile)),
      required: true
    },
    { name: "source", kind: "source", sha256: source.sha256, required: true }
  ];
}

async function pathExists(path: string): Promise<boolean> {
  try {
    await access(path);
    return true;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw error;
  }
}

async function readJsonIfExists<T>(path: string): Promise<T | undefined> {
  try {
    return JSON.parse(await readFile(path, "utf8")) as T;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
    throw error;
  }
}

async function writeJsonAtomic(path: string, value: unknown): Promise<void> {
  await mkdir(dirname(path), { recursive: true, mode: 0o700 });
  const temporary = `${path}.${crypto.randomUUID()}.tmp`;
  await writeFile(temporary, `${canonicalJson(value)}\n`, { mode: 0o600, flag: "wx" });
  await rename(temporary, path);
}

function boundedMessage(error: unknown): string {
  const text = error instanceof Error ? error.message : String(error);
  return (text.trim() || "operation failed").slice(0, 2048);
}

function classifyError(message: string): ResearchNodeControlFailure["error"]["code"] {
  if (message.startsWith("invalid_request:")) return "invalid_request";
  if (message.startsWith("not_declared:")) return "not_declared";
  if (message.startsWith("operation_unknown:")) return "operation_unknown";
  return "operation_failed";
}
