import assert from "node:assert/strict";
import test from "node:test";

import {
  evidenceManifestKey,
  evidenceWorkflowInstanceId,
  executeEvidenceStep,
  persistEvidenceSubmission,
  type EvidenceRunParameters
} from "../src/evidence-run.js";
import { effectivePolicyVersion } from "../src/policy.js";
import { MemoryR2, makeEnv } from "./helpers.js";

async function parameters(environment: ReturnType<typeof makeEnv>): Promise<EvidenceRunParameters> {
  return {
    request: {
      schema_version: 1,
      consumer: "ordivon-computer",
      workload: "research-source-capture",
      steps: [{id: "source", operation: "fetch", input: {url: "https://allowed.example.org/data", maximum_bytes: 1024}}]
    },
    submission: {
      request_id: "request_evidence_001",
      request_digest: "a".repeat(64),
      policy_version: await effectivePolicyVersion(environment),
      capability_version: "evidence.run.v1",
      worker_version: environment.CF_VERSION_METADATA
    }
  };
}

test("evidence run derives one recoverable provider instance ID", () => {
  assert.equal(evidenceWorkflowInstanceId("request_evidence_001"), "evidence-request_evidence_001");
  assert.equal(
    evidenceManifestKey("evidence-request_evidence_001", "result"),
    "evidence-runs/v1/evidence-request_evidence_001/result.json"
  );
});

test("submission Artifact is immutable, replayable, and conflict detecting", async () => {
  const memory = new MemoryR2();
  const environment = makeEnv(memory);
  const input = await parameters(environment);
  const instanceId = evidenceWorkflowInstanceId(input.submission.request_id);
  const first = await persistEvidenceSubmission(environment, instanceId, input);
  const replay = await persistEvidenceSubmission(environment, instanceId, input);
  assert.deepEqual(replay, first);
  assert.ok(memory.objects.has(evidenceManifestKey(instanceId, "submission")));
  await assert.rejects(
    persistEvidenceSubmission(environment, instanceId, {
      ...input,
      request: {...input.request, workload: "different"}
    }),
    /conflict/
  );
});

test("durable fetch step writes source bytes directly to R2 and returns provider refs", async () => {
  const memory = new MemoryR2();
  const environment = makeEnv(memory);
  const input = await parameters(environment);
  const ticks = [
    new Date("2026-08-02T00:00:00.000Z"),
    new Date("2026-08-02T00:00:00.250Z")
  ];
  const result = await executeEvidenceStep(
    environment,
    input,
    evidenceWorkflowInstanceId(input.submission.request_id),
    input.request.steps[0]!,
    {
      step: {name: "execute:source", count: 1},
      attempt: 1,
      config: {}
    },
    {
      now: () => ticks.shift()!,
      fetcher: async () => new Response("remote-source", {status: 200, headers: {"content-type": "text/plain"}})
    }
  );
  assert.equal(result.operation, "fetch");
  assert.equal(result.attempt, 1);
  assert.match(result.provider_request_id, /^wfr_[0-9a-f]{48}$/);
  assert.equal(result.artifacts.length, 1);
  assert.equal(result.artifacts[0]?.bytes, 13);
  assert.ok(memory.objects.has(result.artifacts[0]!.key));
  assert.equal(result.execution.lease_generation, 1);
});
