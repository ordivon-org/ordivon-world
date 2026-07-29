import assert from "node:assert/strict";
import {
  chmod,
  lstat,
  mkdir,
  mkdtemp,
  readFile,
  readdir,
  rm,
  symlink,
  writeFile
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test, { type TestContext } from "node:test";

import {
  LinuxUnshareExecutor,
  LocalDisposableNodeAdapter,
  verifyEvidenceArtifact,
  type LocalAdapterFaults,
  type LocalExperimentExecutor
} from "../src/local-node-adapter.js";
import {
  canonicalJson,
  edgeNodeIdentity,
  sha256Hex,
  validateProfileAuthorities,
  type EdgeNodeIdentityInput,
  type EdgeProfileAuthority,
  type EdgeReconstructionInput
} from "../src/node-contracts.js";
import { EdgeNodeLifecycle } from "../src/node-lifecycle.js";

const ENTRYPOINT = new TextEncoder().encode("printf 'range-local-ok\\n'\n");
const LIVE_ENTRYPOINT = new TextEncoder().encode(
  [
    "if [ -n \"${CLOUDFLARE_API_TOKEN-}\" ]; then exit 20; fi",
    "if [ -e /etc/passwd ] || [ -e /proc/self ] || [ -e /dev/null ]; then exit 21; fi",
    "if printf x > /experiment/write-test 2>/dev/null; then exit 22; fi",
    "if ( : > /dev/tcp/127.0.0.1/1 ) 2>/dev/null; then exit 23; fi",
    "printf 'range-local-ok\\n'"
  ].join("\n")
);
const FIXED_NOW = new Date("2026-07-28T00:00:00.000Z");

async function removeTestTree(root: string): Promise<void> {
  try {
    const metadata = await lstat(root);
    if (!metadata.isDirectory() || metadata.isSymbolicLink()) {
      await rm(root, { force: true });
      return;
    }
    await makeDirectoriesWritable(root);
    await rm(root, { recursive: true, force: true });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== "ENOENT") throw error;
  }
}

async function makeDirectoriesWritable(directory: string): Promise<void> {
  await chmod(directory, 0o700);
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.isDirectory() && !entry.isSymbolicLink()) {
      await makeDirectoriesWritable(join(directory, entry.name));
    }
  }
}
const RESEARCH_AUTHORITY: EdgeProfileAuthority = {
  authority_id: "edge-research-local",
  profile: "research",
  credential_mode: "none",
  credential_scope: "local-research-no-credentials",
  policy_revision_id: "research-policy-v1"
};

class FakeExecutor implements LocalExperimentExecutor {
  prepareCalls = 0;
  runCalls = 0;
  failPrepare = false;
  failRun = false;

  async prepare(rootfs: string, entrypoint: Uint8Array): Promise<void> {
    this.prepareCalls += 1;
    await mkdir(join(rootfs, "experiment"), { recursive: true });
    await writeFile(join(rootfs, "experiment", "entrypoint.sh"), entrypoint, {
      mode: 0o555
    });
    if (this.failPrepare) throw new Error("injected prepare failure");
  }

  async run() {
    this.runCalls += 1;
    if (this.failRun) throw new Error("injected run failure");
    return {
      exitCode: 0,
      stdout: new TextEncoder().encode("range-local-ok\n"),
      stderr: new Uint8Array(),
      startedAt: FIXED_NOW,
      completedAt: new Date(FIXED_NOW.getTime() + 10)
    };
  }
}

async function identityInput(
  overrides: Partial<EdgeNodeIdentityInput> = {}
): Promise<EdgeNodeIdentityInput> {
  return {
    node_class: "container",
    provider: {
      id: "local-unshare-v1",
      kind: "local-unshare",
      location: "range-local"
    },
    source: {
      kind: "fixture",
      name: "range-local-smoke",
      sha256: await sha256Hex(ENTRYPOINT)
    },
    capability: {
      id: "local.fixture.v1",
      version: "1",
      profile: "research",
      consequence_scope: "range-local-only",
      planes: ["experiment", "observation"],
      budget: {
        wall_time_ms: 1_000,
        actions: 1,
        artifact_bytes: 4_096
      }
    },
    policy_revision: {
      id: "research-policy-v1",
      sha256: "b".repeat(64),
      profile: "research"
    },
    resource_profile: {
      id: "local-tiny",
      cpu_millis: 250,
      memory_bytes: 64 * 1024 * 1024,
      storage_bytes: 16 * 1024 * 1024,
      process_limit: 4
    },
    membership: {
      campaign_id: "campaign-test",
      world_id: "world-test",
      generation: 1
    },
    profile: "research",
    generation: 1,
    ...overrides
  };
}

interface FixtureOptions {
  readonly root?: string;
  readonly executor?: FakeExecutor;
  readonly faults?: LocalAdapterFaults;
  readonly clock?: { now: Date };
}

async function adapterFixture(t: TestContext, options: FixtureOptions = {}) {
  const root = options.root ?? await mkdtemp(join(tmpdir(), "ordivon-edge-node-"));
  if (options.root === undefined) {
    t.after(async () => removeTestTree(root));
  }
  const executor = options.executor ?? new FakeExecutor();
  const clock = options.clock ?? { now: FIXED_NOW };
  let sequence = 0;
  const adapter = new LocalDisposableNodeAdapter({
    root,
    authority: RESEARCH_AUTHORITY,
    executor,
    ...(options.faults === undefined ? {} : { faults: options.faults }),
    now: () => clock.now,
    token: () => `${String(++sequence).padStart(4, "0")}${"a".repeat(60)}`
  });
  return { root, adapter, executor, clock };
}

async function provisionAndStart(
  adapter: LocalDisposableNodeAdapter,
  providedInput?: EdgeNodeIdentityInput,
  entrypoint: Uint8Array = ENTRYPOINT
) {
  const input = providedInput ?? await identityInput();
  const identity = await adapter.declare(input);
  assert.equal(
    (await adapter.provision(identity.node_id, "provision-1", entrypoint)).state,
    "provisioned"
  );
  assert.equal(
    (await adapter.lifecycle(identity.node_id, "admit-1", "admit")).state,
    "admitted"
  );
  assert.equal(
    (await adapter.lifecycle(identity.node_id, "start-1", "start")).state,
    "running"
  );
  return identity;
}

async function reconstructionInputs(
  declaredInput: EdgeNodeIdentityInput
): Promise<EdgeReconstructionInput[]> {
  return [
    { name: "policy", kind: "policy", sha256: declaredInput.policy_revision.sha256, required: true },
    {
      name: "capability",
      kind: "capability",
      sha256: await sha256Hex(canonicalJson(declaredInput.capability)),
      required: true
    },
    {
      name: "resource",
      kind: "resource",
      sha256: await sha256Hex(canonicalJson(declaredInput.resource_profile)),
      required: true
    },
    {
      name: "source",
      kind: "source",
      sha256: declaredInput.source.kind === "fixture" ? declaredInput.source.sha256 : "",
      required: true
    }
  ];
}

test("identity is canonical, immutable by input copy, and binds World/Campaign/generation", async () => {
  const input = await identityInput();
  const first = await edgeNodeIdentity(input);
  const reordered = await edgeNodeIdentity(
    JSON.parse(canonicalJson(input)) as EdgeNodeIdentityInput
  );
  assert.equal(first.node_id, reordered.node_id);
  assert.equal(first.digest, reordered.digest);

  (input.membership as { world_id: string }).world_id = "mutated-at-runtime";
  assert.equal(first.input.membership.world_id, "world-test");
  for (const changedInput of [
    await identityInput({ membership: { campaign_id: "other", world_id: "world-test", generation: 1 } }),
    await identityInput({ membership: { campaign_id: "campaign-test", world_id: "other", generation: 1 } }),
    await identityInput({ generation: 2 }),
    await identityInput({ policy_revision: { id: "research-policy-v1", sha256: "c".repeat(64), profile: "research" } })
  ]) {
    assert.notEqual(first.node_id, (await edgeNodeIdentity(changedInput)).node_id);
  }
  const unsorted = await identityInput();
  await assert.rejects(() =>
    edgeNodeIdentity({
      ...unsorted,
      capability: {
        ...unsorted.capability,
        planes: ["observation", "experiment"]
      }
    })
  );
});

test("lifecycle is idempotent, rejects operation-ID rebinding, and persists uncertainty", () => {
  const lifecycle = new EdgeNodeLifecycle();
  const uncertain = lifecycle.apply("provision-1", "provision", "uncertain");
  assert.deepEqual(lifecycle.apply("provision-1", "provision"), uncertain);
  assert.match(
    lifecycle.apply("provision-1", "destroy").reason ?? "",
    /another operation/
  );
  assert.equal(lifecycle.apply("admit-blocked", "admit").reconciliation_required, true);
  assert.equal(lifecycle.reconcile("reconcile-1", true).state, "provisioned");
  assert.equal(lifecycle.apply("provision-1", "provision").state, "provisioned");

  const restored = new EdgeNodeLifecycle(lifecycle.snapshot());
  assert.equal(restored.state, "provisioned");
  assert.equal(restored.reconcile("reconcile-1", false).state, "provisioned");
  assert.throws(
    () =>
      new EdgeNodeLifecycle({
        schema_version: lifecycle.snapshot().schema_version,
        state: "provision-uncertain",
        outcomes: lifecycle.snapshot().outcomes
      }),
    /uncertainty/
  );
});

test("ambiguous provision and destroy reconcile sealed provider state before replay", async (t) => {
  let provisionFault = true;
  let destroyFault = true;
  const fixture = await adapterFixture(t, {
    faults: {
      afterProvisionEffect() {
        if (provisionFault) {
          provisionFault = false;
          throw new Error("lost provision response");
        }
      },
      afterDestroyEffect() {
        if (destroyFault) {
          destroyFault = false;
          throw new Error("lost destroy response");
        }
      }
    }
  });
  const identity = await fixture.adapter.declare(await identityInput());
  const [uncertainProvision, concurrentReplay] = await Promise.all([
    fixture.adapter.provision(identity.node_id, "provision-1", ENTRYPOINT),
    fixture.adapter.provision(identity.node_id, "provision-1", ENTRYPOINT)
  ]);
  assert.equal(uncertainProvision.state, "provision-uncertain");
  assert.deepEqual(concurrentReplay, uncertainProvision);
  assert.deepEqual(
    await fixture.adapter.provision(identity.node_id, "provision-1", ENTRYPOINT),
    uncertainProvision
  );
  assert.equal(fixture.executor.prepareCalls, 1);
  assert.equal(
    (await fixture.adapter.reconcile(identity.node_id, "reconcile-provision")).state,
    "provisioned"
  );
  assert.equal(
    (await fixture.adapter.provision(identity.node_id, "provision-1", ENTRYPOINT)).state,
    "provisioned"
  );
  await fixture.adapter.lifecycle(identity.node_id, "admit-1", "admit");
  const uncertainDestroy = await fixture.adapter.destroy(identity.node_id, "destroy-1");
  assert.equal(uncertainDestroy.state, "destroy-uncertain");
  assert.deepEqual(
    await fixture.adapter.destroy(identity.node_id, "destroy-1"),
    uncertainDestroy
  );
  assert.equal(
    (await fixture.adapter.reconcile(identity.node_id, "reconcile-destroy")).state,
    "destroyed"
  );
  assert.equal(
    (await fixture.adapter.destroy(identity.node_id, "destroy-1")).state,
    "destroyed"
  );
});

test("partial provision is never admitted and restart resumes the durable journal", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-restart-"));
  t.after(async () => removeTestTree(root));
  const failing = new FakeExecutor();
  failing.failPrepare = true;
  const first = await adapterFixture(t, { root, executor: failing });
  const input = await identityInput();
  const identity = await first.adapter.declare(input);
  assert.equal(
    (await first.adapter.provision(identity.node_id, "provision-failed", ENTRYPOINT)).state,
    "provision-uncertain"
  );

  const second = await adapterFixture(t, { root });
  await second.adapter.declare(input);
  await assert.rejects(
    () => second.adapter.lifecycle(identity.node_id, "admit-too-early", "admit"),
    /unsealed|modified/
  );
  assert.equal(
    (await second.adapter.reconcile(identity.node_id, "reconcile-failed")).state,
    "declared"
  );
  assert.equal(
    (await second.adapter.provision(identity.node_id, "provision-2", ENTRYPOINT)).state,
    "provisioned"
  );
  assert.equal(
    (await second.adapter.lifecycle(identity.node_id, "admit-2", "admit")).state,
    "admitted"
  );

  const third = await adapterFixture(t, { root });
  await third.adapter.declare(input);
  assert.equal(
    (await third.adapter.lifecycle(identity.node_id, "start-after-restart", "start")).state,
    "running"
  );
});

test("sealed rootfs tampering prevents admission", async (t) => {
  const { adapter } = await adapterFixture(t);
  const identity = await adapter.declare(await identityInput());
  await adapter.provision(identity.node_id, "provision-1", ENTRYPOINT);
  const entrypoint = join(
    adapter.planes(identity.node_id).experiment,
    "experiment",
    "entrypoint.sh"
  );
  await chmod(entrypoint, 0o600);
  await writeFile(entrypoint, "printf tampered");
  await assert.rejects(
    () => adapter.lifecycle(identity.node_id, "admit-1", "admit"),
    /unsealed|modified/
  );
});

test("rootfs symlinks and provider-plane symlink traversal fail closed", async (t) => {
  class SymlinkExecutor extends FakeExecutor {
    override async prepare(rootfs: string, entrypoint: Uint8Array): Promise<void> {
      await super.prepare(rootfs, entrypoint);
      await symlink("/etc/passwd", join(rootfs, "experiment", "escape"));
    }
  }
  const symlinkFixture = await adapterFixture(t, {
    executor: new SymlinkExecutor()
  });
  const identity = await symlinkFixture.adapter.declare(await identityInput());
  assert.equal(
    (
      await symlinkFixture.adapter.provision(
        identity.node_id,
        "provision-symlink",
        ENTRYPOINT
      )
    ).state,
    "provision-uncertain"
  );
  assert.equal(
    (
      await symlinkFixture.adapter.reconcile(
        identity.node_id,
        "reconcile-symlink"
      )
    ).state,
    "declared"
  );

  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-plane-link-"));
  const external = await mkdtemp(join(tmpdir(), "ordivon-edge-plane-target-"));
  t.after(async () => {
    await rm(root, { recursive: true, force: true });
    await rm(external, { recursive: true, force: true });
  });
  await symlink(external, join(root, "nodes"));
  const adapter = new LocalDisposableNodeAdapter({
    root,
    authority: RESEARCH_AUTHORITY,
    executor: new FakeExecutor()
  });
  const linkedInput = await identityInput();
  await assert.rejects(
    () => adapter.declare(linkedInput),
    /symbolic link/
  );
});

test("profile separation requires credential-free authority, not shared labels", async (t) => {
  assert.throws(() =>
    validateProfileAuthorities([
      RESEARCH_AUTHORITY,
      {
        authority_id: "edge-research-local",
        profile: "production",
        credential_mode: "external-profile-scoped",
        credential_scope: "cloudflare-production",
        policy_revision_id: "production-policy"
      }
    ])
  );
  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-profile-"));
  t.after(async () => removeTestTree(root));
  for (const authority of [
    { ...RESEARCH_AUTHORITY, credential_mode: "external-profile-scoped" as const },
    { ...RESEARCH_AUTHORITY, credential_scope: "cloudflare-production" },
    {
      authority_id: "edge-production",
      profile: "production" as const,
      credential_mode: "external-profile-scoped" as const,
      credential_scope: "cloudflare-production",
      policy_revision_id: "production-policy"
    }
  ]) {
    assert.throws(
      () =>
        new LocalDisposableNodeAdapter({
          root,
          authority,
          executor: new FakeExecutor()
        }),
      /credential-free research authority/
    );
  }
});

test("leases expire, monotonically fence replay, serialize execution, and invalidate on restart", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-lease-"));
  t.after(async () => removeTestTree(root));
  const clock = { now: FIXED_NOW };
  const first = await adapterFixture(t, { root, clock });
  const input = await identityInput();
  const identity = await provisionAndStart(first.adapter, input);
  const lease1 = await first.adapter.issueLease(identity.node_id, "manager", 1, 10_000);
  const lease2 = await first.adapter.issueLease(identity.node_id, "manager", 2, 10_000);
  await assert.rejects(
    () => first.adapter.execute(identity.node_id, lease1.lease, lease1.token),
    /stale/
  );
  const concurrent = await Promise.all([
    first.adapter.execute(identity.node_id, lease2.lease, lease2.token),
    first.adapter.execute(identity.node_id, lease2.lease, lease2.token)
  ]);
  assert.deepEqual(concurrent.map(({ status }) => status).sort(), ["rejected", "succeeded"]);
  assert.equal(first.executor.runCalls, 1);

  const restarted = await adapterFixture(t, { root, clock });
  await restarted.adapter.declare(input);
  await assert.rejects(
    () => restarted.adapter.execute(identity.node_id, lease2.lease, lease2.token),
    /stale/
  );
  const lease3 = await restarted.adapter.issueLease(identity.node_id, "manager", 3, 1);
  clock.now = new Date(FIXED_NOW.getTime() + 2);
  await assert.rejects(
    () => restarted.adapter.execute(identity.node_id, lease3.lease, lease3.token),
    /expired/
  );
  await assert.rejects(
    () => restarted.adapter.issueLease(identity.node_id, "manager", 3, 10),
    /monotonically/
  );
});

test("executor failures are bounded, receipted, and consume the leased action", async (t) => {
  const executor = new FakeExecutor();
  executor.failRun = true;
  const { adapter } = await adapterFixture(t, { executor });
  const identity = await provisionAndStart(adapter);
  const grant = await adapter.issueLease(identity.node_id, "manager", 1, 10_000);
  const failed = await adapter.execute(identity.node_id, grant.lease, grant.token);
  assert.equal(failed.status, "failed");
  assert.equal(failed.error_code, "executor_failure");
  assert.deepEqual(failed.observations, []);
  assert.doesNotMatch(JSON.stringify(failed), new RegExp(grant.token));
  const replay = await adapter.execute(identity.node_id, grant.lease, grant.token);
  assert.equal(replay.status, "rejected");
  assert.equal(replay.error_code, "action_budget_exhausted");
  assert.equal(executor.runCalls, 1);
});

test("evidence commit is atomic, idempotent, generation-scoped, and tamper-evident", async (t) => {
  let failBeforeCommit = true;
  const fixture = await adapterFixture(t, {
    faults: {
      beforeEvidenceCommit() {
        if (failBeforeCommit) {
          failBeforeCommit = false;
          throw new Error("injected evidence failure");
        }
      }
    }
  });
  const identity = await provisionAndStart(fixture.adapter);
  const grant = await fixture.adapter.issueLease(identity.node_id, "manager", 1, 10_000);
  const execution = await fixture.adapter.execute(identity.node_id, grant.lease, grant.token);
  assert.equal(execution.status, "succeeded");
  await assert.rejects(
    () => fixture.adapter.exportEvidence(identity.node_id, grant.lease, grant.token),
    /injected evidence failure/
  );
  const partial = join(
    fixture.adapter.planes(identity.node_id).evidence_export,
    ".staging-g1-orphan"
  );
  await mkdir(partial, { recursive: true });
  await writeFile(join(partial, "partial"), "partial");

  const evidence = await fixture.adapter.exportEvidence(
    identity.node_id,
    grant.lease,
    grant.token
  );
  const replay = await fixture.adapter.exportEvidence(
    identity.node_id,
    grant.lease,
    grant.token
  );
  assert.deepEqual(replay, evidence);
  assert.equal(evidence.identity_digest, identity.digest);
  assert.equal(evidence.generation, 1);
  assert.equal(evidence.artifacts.length, 3);
  assert.doesNotMatch(JSON.stringify(evidence), new RegExp(grant.token));

  const artifactPath = join(
    fixture.adapter.planes(identity.node_id).evidence_export,
    "g1",
    `${evidence.artifacts[0]!.artifact_id}.bin`
  );
  await verifyEvidenceArtifact(artifactPath, evidence.artifacts[0]!.sha256);
  await chmod(artifactPath, 0o600);
  await writeFile(artifactPath, "tampered");
  await assert.rejects(
    () => fixture.adapter.exportEvidence(identity.node_id, grant.lease, grant.token),
    /mismatch/
  );

  const linkPath = join(fixture.root, "evidence-link");
  await symlink(artifactPath, linkPath);
  await assert.rejects(
    () => verifyEvidenceArtifact(linkPath, evidence.artifacts[0]!.sha256),
    /ELOOP|symbolic/i
  );
});

test("committed evidence recovers lifecycle after a crash between rename and journal update", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-evidence-recovery-"));
  t.after(async () => removeTestTree(root));
  let crash = true;
  const first = await adapterFixture(t, {
    root,
    faults: {
      afterEvidenceCommit() {
        if (crash) {
          crash = false;
          throw new Error("simulated manager crash");
        }
      }
    }
  });
  const input = await identityInput();
  const identity = await provisionAndStart(first.adapter, input);
  const grant = await first.adapter.issueLease(identity.node_id, "manager", 1, 10_000);
  await first.adapter.execute(identity.node_id, grant.lease, grant.token);
  await assert.rejects(
    () => first.adapter.exportEvidence(identity.node_id, grant.lease, grant.token),
    /simulated manager crash/
  );

  const restarted = await adapterFixture(t, { root });
  await restarted.adapter.declare(input);
  assert.equal(
    (await restarted.adapter.lifecycle(identity.node_id, "retire-after-recovery", "retire")).state,
    "retired"
  );
});

test("reconstruction rejects duplicate, ambiguous, incomplete, and mismatched inputs", async (t) => {
  const { adapter } = await adapterFixture(t);
  const declaredInput = await identityInput();
  const identity = await adapter.declare(declaredInput);
  const inputs = await reconstructionInputs(declaredInput);
  const first = await adapter.reconstructionReceipt(identity.node_id, inputs);
  const reordered = await adapter.reconstructionReceipt(identity.node_id, [...inputs].reverse());
  assert.equal(first.inputs_root_sha256, reordered.inputs_root_sha256);
  assert.equal(first.receipt_id, reordered.receipt_id);
  assert.deepEqual(first.inputs.map(({ kind }) => kind), [
    "capability",
    "policy",
    "resource",
    "source"
  ]);
  for (const invalid of [
    inputs.slice(1),
    [...inputs, { ...inputs[0]!, name: "duplicate-policy" }],
    inputs.map((input, index) => index === 1 ? { ...input, name: inputs[0]!.name } : input),
    inputs.map((input) => input.kind === "source" ? { ...input, sha256: "c".repeat(64) } : input),
    [...inputs, { name: "snapshot", kind: "snapshot" as const, sha256: "d".repeat(64), required: true }]
  ]) {
    await assert.rejects(() => adapter.reconstructionReceipt(identity.node_id, invalid));
  }
});

test(
  "live unshare executor exposes no host tree, credentials, writable root, proc/dev, or usable network",
  { skip: process.env.ORDIVON_EDGE_LIVE_TEST !== "1" },
  async (t) => {
    const root = await mkdtemp(join(tmpdir(), "ordivon-edge-unshare-"));
    t.after(async () => removeTestTree(root));
    const executor = new LinuxUnshareExecutor("/usr/sbin/unshare", "/usr/sbin/bash");
    const adapter = new LocalDisposableNodeAdapter({
      root,
      authority: RESEARCH_AUTHORITY,
      executor
    });
    const baseInput = await identityInput();
    const input: EdgeNodeIdentityInput = {
      ...baseInput,
      source: {
        kind: "fixture",
        name: "live-isolation",
        sha256: await sha256Hex(LIVE_ENTRYPOINT)
      }
    };
    const identity = await provisionAndStart(adapter, input, LIVE_ENTRYPOINT);
    const lease = await adapter.issueLease(identity.node_id, "live-test", 1, 10_000);
    const receipt = await adapter.execute(identity.node_id, lease.lease, lease.token);
    assert.equal(receipt.status, "succeeded");
    assert.equal(receipt.exit_code, 0);
    const stdout = receipt.observations.find(({ kind }) => kind === "stdout");
    assert.notEqual(stdout, undefined);
    assert.equal(
      await readFile(
        join(
          adapter.planes(identity.node_id).observation,
          "g1",
          `${stdout!.observation_id}.bin`
        ),
        "utf8"
      ),
      "range-local-ok\n"
    );
    assert.equal(
      (
        await readFile(
          join(
            adapter.planes(identity.node_id).experiment,
            "experiment",
            "entrypoint.sh"
          )
        )
      ).byteLength,
      LIVE_ENTRYPOINT.byteLength
    );
    await assert.rejects(() =>
      readFile(
        join(
          adapter.planes(identity.node_id).experiment,
          "experiment",
          "write-test"
        )
      )
    );
  }
);
