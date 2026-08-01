import assert from "node:assert/strict";
import test from "node:test";

import { handleRequest, type Env } from "../src/index.js";
import { MemoryR2, makeEnv, signedRequest } from "./helpers.js";

class FakeWorkflowInstance {
  constructor(public readonly id: string) {}
  current: InstanceStatus = {status: "queued"};
  async status(): Promise<InstanceStatus> { return this.current; }
  async terminate(): Promise<void> { this.current = {status: "terminated"}; }
  async pause(): Promise<void> { this.current = {status: "paused"}; }
  async resume(): Promise<void> { this.current = {status: "running"}; }
  async restart(): Promise<void> { this.current = {status: "queued"}; }
  async sendEvent(): Promise<void> {}
}

class FakeWorkflow {
  readonly instances = new Map<string, FakeWorkflowInstance>();
  createCalls = 0;
  async create(options?: WorkflowInstanceCreateOptions): Promise<WorkflowInstance> {
    this.createCalls += 1;
    const id = options?.id;
    if (id === undefined) throw new Error("missing id");
    if (this.instances.has(id)) throw new Error("already exists");
    const instance = new FakeWorkflowInstance(id);
    this.instances.set(id, instance);
    return instance as unknown as WorkflowInstance;
  }
  async get(id: string): Promise<WorkflowInstance> {
    const instance = this.instances.get(id);
    if (instance === undefined) throw new Error("not found");
    return instance as unknown as WorkflowInstance;
  }
  async createBatch(): Promise<WorkflowInstance[]> { throw new Error("not used"); }
}

function environment(memory = new MemoryR2(), workflow = new FakeWorkflow()): Env {
  return {...makeEnv(memory), EVIDENCE_WORKFLOW: workflow as unknown as Workflow} as Env;
}

const body = JSON.stringify({
  schema_version: 1,
  consumer: "ordivon-computer",
  workload: "research-source-capture",
  steps: [{id: "source", operation: "fetch", input: {url: "https://allowed.example.org/data", maximum_bytes: 1024}}]
});

test("signed evidence submission returns provider-native Workflow handle and replays by request ID", async () => {
  const memory = new MemoryR2();
  const workflow = new FakeWorkflow();
  const env = environment(memory, workflow);
  const requestId = "request_evidence_route_001";
  const first = await handleRequest(signedRequest("https://edge.invalid/v1/evidence-runs", {method: "POST", body, requestId}), env);
  assert.equal(first.status, 202);
  const firstValue = await first.json() as {foreign_operation_ref: {instance_id: string}; replayed: boolean};
  assert.equal(firstValue.foreign_operation_ref.instance_id, `evidence-${requestId}`);
  assert.equal(firstValue.replayed, false);
  assert.ok(memory.objects.has(`evidence-runs/v1/evidence-${requestId}/submission.json`));

  const replay = await handleRequest(signedRequest("https://edge.invalid/v1/evidence-runs", {method: "POST", body, requestId}), env);
  assert.equal(replay.status, 202);
  assert.equal((await replay.json() as {replayed: boolean}).replayed, true);
  assert.equal(workflow.createCalls, 2);
});

test("evidence status and terminate preserve provider-native lifecycle", async () => {
  const workflow = new FakeWorkflow();
  const env = environment(new MemoryR2(), workflow);
  const requestId = "request_evidence_route_002";
  await handleRequest(signedRequest("https://edge.invalid/v1/evidence-runs", {method: "POST", body, requestId}), env);
  const id = `evidence-${requestId}`;
  const status = await handleRequest(signedRequest(`https://edge.invalid/v1/evidence-runs/${id}`, {requestId: "request_evidence_status_001"}), env);
  assert.equal(status.status, 202);
  assert.equal((await status.json() as {provider_status: InstanceStatus}).provider_status.status, "queued");
  const terminated = await handleRequest(signedRequest(`https://edge.invalid/v1/evidence-runs/${id}/terminate`, {method: "POST", requestId: "request_evidence_stop_001"}), env);
  assert.equal(terminated.status, 200);
  assert.equal((await terminated.json() as {provider_status: InstanceStatus}).provider_status.status, "terminated");
});

test("same request ID cannot be rebound to different evidence input", async () => {
  const env = environment();
  const requestId = "request_evidence_route_003";
  const first = await handleRequest(signedRequest("https://edge.invalid/v1/evidence-runs", {method: "POST", body, requestId}), env);
  assert.equal(first.status, 202);
  const changed = body.replace("research-source-capture", "deployment-acceptance");
  const conflict = await handleRequest(signedRequest("https://edge.invalid/v1/evidence-runs", {method: "POST", body: changed, requestId}), env);
  assert.equal(conflict.status, 409);
  assert.equal((await conflict.json() as {error: string}).error, "evidence_run_conflict");
});
