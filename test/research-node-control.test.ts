import assert from "node:assert/strict";
import { chmod, mkdir, mkdtemp, readdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import type {
  LocalExperimentExecutor,
  LocalExperimentResult
} from "../src/local-node-adapter.js";
import {
  ResearchNodeControlSession,
  type ResearchNodeControlResponse
} from "../src/research-node-control.js";
import {
  sha256Hex,
  type EdgeNodeIdentityInput
} from "../src/node-contracts.js";

const NOW = new Date("2026-07-29T00:00:00.000Z");
const ENTRYPOINT = new TextEncoder().encode("printf 'edge-control-ok\\n'\n");

async function removeControlRoot(root: string): Promise<void> {
  async function makeWritable(path: string): Promise<void> {
    let entries;
    try {
      entries = await readdir(path, { withFileTypes: true });
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") return;
      throw error;
    }
    await chmod(path, 0o700);
    for (const entry of entries) {
      const child = join(path, entry.name);
      if (entry.isDirectory()) {
        await makeWritable(child);
      } else if (!entry.isSymbolicLink()) {
        await chmod(child, 0o600);
      }
    }
  }
  await makeWritable(root);
  await rm(root, { recursive: true, force: true });
}

class FakeExecutor implements LocalExperimentExecutor {
  prepareCalls = 0;
  runCalls = 0;

  async prepare(rootfs: string, entrypoint: Uint8Array): Promise<void> {
    this.prepareCalls += 1;
    await mkdir(join(rootfs, "experiment"), { recursive: true });
    await writeFile(join(rootfs, "experiment", "entrypoint.sh"), entrypoint, {
      mode: 0o555
    });
  }

  async run(): Promise<LocalExperimentResult> {
    this.runCalls += 1;
    return {
      exitCode: 0,
      stdout: new TextEncoder().encode("edge-control-ok\n"),
      stderr: new Uint8Array(),
      startedAt: NOW,
      completedAt: new Date(NOW.getTime() + 5)
    };
  }
}

async function identityInput(): Promise<EdgeNodeIdentityInput> {
  return {
    node_class: "container",
    provider: {
      id: "local-unshare-v1",
      kind: "local-unshare",
      location: "range-local"
    },
    source: {
      kind: "fixture",
      name: "security-composition-v0",
      sha256: await sha256Hex(ENTRYPOINT)
    },
    capability: {
      id: "security.composition.v0",
      version: "1",
      profile: "research",
      consequence_scope: "range-local-only",
      planes: ["experiment", "observation"],
      budget: {
        wall_time_ms: 1_000,
        actions: 1,
        artifact_bytes: 8_192
      }
    },
    policy_revision: {
      id: "research-policy-v1",
      sha256: "b".repeat(64),
      profile: "research"
    },
    resource_profile: {
      id: "security-composition-tiny",
      cpu_millis: 250,
      memory_bytes: 64 * 1024 * 1024,
      storage_bytes: 16 * 1024 * 1024,
      process_limit: 4
    },
    membership: {
      campaign_id: "urn:ordivon:security:campaign:composition-v0",
      world_id: "urn:ordivon:security:world:composition-v0",
      generation: 1
    },
    profile: "research",
    generation: 1
  };
}

function successful(response: ResearchNodeControlResponse) {
  if (!response.ok) throw new Error(response.error.message);
  return response.result;
}

async function declare(session: ResearchNodeControlSession) {
  return successful(await session.handle({
    schema_version: 1,
    request_id: "declare-1",
    action: "declare",
    input: await identityInput(),
    entrypoint_base64: Buffer.from(ENTRYPOINT).toString("base64")
  }));
}

async function execute(
  session: ResearchNodeControlSession,
  operation: string,
  operationId: string
) {
  return session.handle({
    schema_version: 1,
    request_id: `request-${operationId}`,
    action: "execute",
    operation,
    operation_id: operationId
  });
}

test("research control drives one complete disposable Node lifecycle", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-control-"));
  t.after(() => removeControlRoot(root));
  const executor = new FakeExecutor();
  let token = 0;
  const session = new ResearchNodeControlSession({
    root,
    executorFactory: () => executor,
    now: () => NOW,
    token: () => `${String(++token).padStart(4, "0")}${"a".repeat(60)}`
  });

  const declaration = await declare(session);
  const snapshot = declaration.snapshot as Record<string, unknown>;
  assert.match(String(snapshot.native_id), /^edge-[a-f0-9]{32}$/);
  assert.match(String(snapshot.root_digest), /^sha256:[a-f0-9]{64}$/);

  successful(await execute(session, "prepare", "prepare-1"));
  const started = successful(await execute(session, "start", "start-1"));
  assert.equal(
    ((started.detail as Record<string, unknown>).execution as Record<string, unknown>).status,
    "succeeded"
  );
  const replay = successful(await execute(session, "start", "start-1"));
  assert.deepEqual(replay, started);
  assert.equal(executor.runCalls, 1);

  const frozen = successful(await execute(session, "freeze", "freeze-1"));
  const frozenDetail = frozen.detail as Record<string, unknown>;
  assert.ok(frozenDetail.evidence);

  const reset = successful(await execute(session, "reset", "reset-1"));
  assert.equal(reset.provider_epoch, 2);
  assert.deepEqual((reset.detail as Record<string, unknown>).snapshot, snapshot);

  successful(await execute(session, "destroy", "destroy-1"));
  const residual = successful(await session.handle({
    schema_version: 1,
    request_id: "residual-1",
    action: "residual"
  }));
  const checks = residual.checks as Array<Record<string, unknown>>;
  assert.equal(checks[0]?.status, "clean");
  assert.equal(checks[1]?.status, "expected_retained");

  const reconstructed = successful(
    await execute(session, "reconstruct", "reconstruct-1")
  );
  assert.deepEqual(
    (reconstructed.detail as Record<string, unknown>).snapshot,
    snapshot
  );
  assert.equal(
    (reconstructed.detail as Record<string, unknown>).fresh_root_removed,
    true
  );
  successful(await execute(session, "verify", "verify-1"));
});

test("control state and completed operation receipts survive a process restart", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-control-restart-"));
  t.after(() => removeControlRoot(root));
  const executor = new FakeExecutor();
  let token = 0;
  const options = {
    root,
    executorFactory: () => executor,
    now: () => NOW,
    token: () => `${String(++token).padStart(4, "0")}${"b".repeat(60)}`
  };
  const first = new ResearchNodeControlSession(options);
  await declare(first);
  successful(await execute(first, "prepare", "prepare-persisted"));

  const restarted = new ResearchNodeControlSession(options);
  await declare(restarted);
  const reconciled = successful(await restarted.handle({
    schema_version: 1,
    request_id: "reconcile-prepare",
    action: "reconcile",
    operation: "prepare",
    operation_id: "prepare-persisted"
  }));
  assert.equal(reconciled.operation, "prepare");
  assert.equal(executor.prepareCalls, 1);
});

test("request validation and operation rebinding fail closed", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "ordivon-edge-control-invalid-"));
  t.after(() => removeControlRoot(root));
  const session = new ResearchNodeControlSession({
    root,
    executorFactory: () => new FakeExecutor(),
    now: () => NOW
  });
  const invalid = await session.handle({ schema_version: 2 });
  assert.equal(invalid.ok, false);
  if (!invalid.ok) assert.equal(invalid.error.code, "invalid_request");

  await declare(session);
  successful(await execute(session, "prepare", "bound-operation"));
  const rebound = await execute(session, "destroy", "bound-operation");
  assert.equal(rebound.ok, false);
  if (!rebound.ok) assert.equal(rebound.error.code, "invalid_request");
});
