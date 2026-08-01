import { WorkflowEntrypoint, type WorkflowEvent, type WorkflowStep, type WorkflowStepContext } from "cloudflare:workers";
import { NonRetryableError } from "cloudflare:workflows";
import { sha256Hex } from "./auth.js";
import { validateBrowserRunRequest } from "./browser-policy.js";
import { executeBrowserRun, type BrowserSnapshotRunner } from "./browser-run.js";
import type {
  ArtifactReference,
  BrowserReceiptDetails,
  EdgeOperation,
  FetchReceiptDetails
} from "./contracts.js";
import { EVIDENCE_RUN_CAPABILITY_VERSION, validateEvidenceRunRequest, type EvidenceRunRequest, type EvidenceRunStep } from "./evidence-run-contracts.js";
import type { ExecutionLease } from "./execution.js";
import { executeExternalFetch, type ExternalFetcher } from "./external-fetch.js";
import { validateFetchRequest } from "./fetch-policy.js";
import { effectivePolicyVersion } from "./policy.js";
import { CAPABILITY_VERSIONS } from "./version.js";

export interface EvidenceWorkflowEnvironment {
  readonly ARTIFACTS: R2Bucket;
  readonly BROWSER: BrowserRun;
  readonly FETCH_ALLOWED_HOSTS: string;
  readonly CF_VERSION_METADATA: WorkerVersionMetadata;
}

export interface EvidenceRunSubmission {
  readonly request_id: string;
  readonly request_digest: string;
  readonly policy_version: string;
  readonly capability_version: typeof EVIDENCE_RUN_CAPABILITY_VERSION;
  readonly worker_version: WorkerVersionMetadata;
}

export interface EvidenceRunParameters {
  readonly request: EvidenceRunRequest;
  readonly submission: EvidenceRunSubmission;
}

export interface EvidenceStepResult {
  readonly schema_version: 1;
  readonly step_id: string;
  readonly operation: "fetch" | "browser.run";
  readonly provider_request_id: string;
  readonly provider_request_digest: string;
  readonly attempt: number;
  readonly started_at: string;
  readonly completed_at: string;
  readonly execution: {
    readonly policy_version: string;
    readonly capability_version: string;
    readonly worker_version_id: string;
    readonly lease_generation: number;
  };
  readonly artifacts: readonly ArtifactReference[];
  readonly details: FetchReceiptDetails | BrowserReceiptDetails;
}

export interface EvidenceRunOutput {
  readonly schema_version: 1;
  readonly workflow_instance_id: string;
  readonly workflow_name: string;
  readonly consumer: string;
  readonly workload: string;
  readonly status: "succeeded";
  readonly input_manifest: ArtifactReference;
  readonly result_manifest: ArtifactReference;
  readonly steps: readonly EvidenceStepResult[];
  readonly artifacts: readonly ArtifactReference[];
}

const encoder = new TextEncoder();

function safeInstanceSegment(value: string): string {
  const normalized = value.toLowerCase().replace(/[^a-z0-9._-]/g, "-").slice(0, 100);
  if (normalized.length === 0) throw new NonRetryableError("Workflow instance ID is invalid.");
  return normalized;
}

export function evidenceWorkflowInstanceId(requestId: string): string {
  return `evidence-${requestId}`;
}

export function evidenceManifestKey(instanceId: string, kind: "submission" | "input" | "result" | "failure"): string {
  return `evidence-runs/v1/${safeInstanceSegment(instanceId)}/${kind}.json`;
}

async function jsonArtifact(
  environment: EvidenceWorkflowEnvironment,
  key: string,
  value: unknown,
  kind: string,
  instanceId: string,
  immutable: boolean
): Promise<ArtifactReference> {
  const body = encoder.encode(JSON.stringify(value));
  const sha256 = await sha256Hex(body);
  const existing = await environment.ARTIFACTS.get(key);
  if (existing !== null) {
    if (existing.customMetadata?.sha256 !== sha256 || existing.size !== body.byteLength) {
      throw new NonRetryableError(`Immutable evidence Artifact conflict: ${key}`);
    }
    return {key, sha256, bytes: existing.size, media_type: "application/json; charset=utf-8", etag: existing.etag};
  }
  const stored = await environment.ARTIFACTS.put(key, body, {
    httpMetadata: {contentType: "application/json; charset=utf-8"},
    customMetadata: {
      sha256,
      kind,
      workflow_instance_id: instanceId,
      worker_version_id: environment.CF_VERSION_METADATA.id
    },
    ...(immutable ? {onlyIf: {etagDoesNotMatch: "*"}} : {})
  });
  if (stored === null) {
    const raced = await environment.ARTIFACTS.get(key);
    if (raced === null || raced.customMetadata?.sha256 !== sha256) {
      throw new Error(`Evidence Artifact could not be persisted: ${key}`);
    }
    return {key, sha256, bytes: raced.size, media_type: "application/json; charset=utf-8", etag: raced.etag};
  }
  return {key, sha256, bytes: body.byteLength, media_type: "application/json; charset=utf-8", etag: stored.etag};
}

export async function persistEvidenceSubmission(
  environment: EvidenceWorkflowEnvironment,
  instanceId: string,
  parameters: EvidenceRunParameters
): Promise<ArtifactReference> {
  return jsonArtifact(environment, evidenceManifestKey(instanceId, "submission"), parameters, "evidence_run_submission", instanceId, true);
}

export interface EvidenceExecutionDependencies {
  readonly fetcher?: ExternalFetcher;
  readonly browserRunner?: BrowserSnapshotRunner;
  readonly now?: () => Date;
}

async function workflowLease(
  environment: EvidenceWorkflowEnvironment,
  parameters: EvidenceRunParameters,
  instanceId: string,
  item: EvidenceRunStep,
  context: WorkflowStepContext,
  now: Date
): Promise<ExecutionLease> {
  const digest = await sha256Hex(JSON.stringify({instanceId, step: item}));
  const operation: EdgeOperation = item.operation;
  return {
    request_id: `wfr_${digest.slice(0, 48)}`,
    request_digest: await sha256Hex(JSON.stringify(item)),
    operation,
    lease_token: `workflow-attempt-${context.attempt}`,
    acquired_at: now.toISOString(),
    lease_expires_at: new Date(now.getTime() + 30 * 60 * 1000).toISOString(),
    state_etag: `workflow:${instanceId}:${item.id}:${context.attempt}`,
    policy_version: parameters.submission.policy_version,
    capability_version: CAPABILITY_VERSIONS[operation],
    worker_version_id: environment.CF_VERSION_METADATA.id,
    worker_version_tag: environment.CF_VERSION_METADATA.tag,
    worker_version_timestamp: environment.CF_VERSION_METADATA.timestamp,
    lease_generation: context.attempt
  };
}

export async function executeEvidenceStep(
  environment: EvidenceWorkflowEnvironment,
  parameters: EvidenceRunParameters,
  instanceId: string,
  item: EvidenceRunStep,
  context: WorkflowStepContext,
  dependencies: EvidenceExecutionDependencies = {}
): Promise<EvidenceStepResult> {
  const started = dependencies.now?.() ?? new Date();
  const lease = await workflowLease(environment, parameters, instanceId, item, context, started);
  if (item.operation === "fetch") {
    const input = validateFetchRequest(item.input, environment);
    const result = await executeExternalFetch(environment, lease, input, dependencies.fetcher);
    const completed = dependencies.now?.() ?? new Date();
    return {
      schema_version: 1,
      step_id: item.id,
      operation: item.operation,
      provider_request_id: lease.request_id,
      provider_request_digest: lease.request_digest,
      attempt: context.attempt,
      started_at: started.toISOString(),
      completed_at: completed.toISOString(),
      execution: {policy_version: lease.policy_version, capability_version: lease.capability_version, worker_version_id: lease.worker_version_id, lease_generation: lease.lease_generation},
      artifacts: result.artifacts,
      details: result.fetch
    };
  }
  const input = validateBrowserRunRequest(item.input, environment);
  const result = await executeBrowserRun(environment, dependencies.browserRunner ?? environment.BROWSER, lease, input);
  const completed = dependencies.now?.() ?? new Date();
  return {
    schema_version: 1,
    step_id: item.id,
    operation: item.operation,
    provider_request_id: lease.request_id,
    provider_request_digest: lease.request_digest,
    attempt: context.attempt,
    started_at: started.toISOString(),
    completed_at: completed.toISOString(),
    execution: {policy_version: lease.policy_version, capability_version: lease.capability_version, worker_version_id: lease.worker_version_id, lease_generation: lease.lease_generation},
    artifacts: result.artifacts,
    details: result.browser
  };
}

export class EvidenceRunWorkflow extends WorkflowEntrypoint<EvidenceWorkflowEnvironment, EvidenceRunParameters> {
  override async run(event: Readonly<WorkflowEvent<EvidenceRunParameters>>, step: WorkflowStep): Promise<EvidenceRunOutput> {
    const request = validateEvidenceRunRequest(event.payload.request, this.env);
    const parameters: EvidenceRunParameters = {request, submission: event.payload.submission};
    const currentPolicy = await effectivePolicyVersion(this.env);
    if (currentPolicy !== parameters.submission.policy_version) {
      throw new NonRetryableError("Evidence run policy binding no longer matches the submitted revision.");
    }
    const inputManifest = await step.do("persist-input-manifest", async () =>
      jsonArtifact(this.env, evidenceManifestKey(event.instanceId, "input"), {
        schema_version: 1,
        workflow_instance_id: event.instanceId,
        workflow_name: event.workflowName,
        triggered_at: event.timestamp.toISOString(),
        parameters
      }, "evidence_run_input", event.instanceId, true)
    );
    const results: EvidenceStepResult[] = [];
    try {
      for (const item of request.steps) {
        const result = await step.do(
          `execute:${item.id}`,
          {retries: {limit: 2, delay: "2 seconds", backoff: "exponential"}, timeout: "2 minutes"},
          async (context) => executeEvidenceStep(this.env, parameters, event.instanceId, item, context)
        );
        results.push(result);
      }
    } catch (error) {
      const failure = {
        schema_version: 1,
        workflow_instance_id: event.instanceId,
        workflow_name: event.workflowName,
        consumer: request.consumer,
        workload: request.workload,
        status: "failed",
        input_manifest: inputManifest,
        completed_steps: results,
        error: {name: error instanceof Error ? error.name : "Error", message: error instanceof Error ? error.message : "Evidence run failed."}
      };
      await step.do("persist-failure-manifest", async () =>
        jsonArtifact(this.env, evidenceManifestKey(event.instanceId, "failure"), failure, "evidence_run_failure", event.instanceId, true)
      );
      throw new NonRetryableError(failure.error.message, failure.error.name);
    }
    const artifacts = results.flatMap((result) => result.artifacts);
    const manifestValue = {
      schema_version: 1,
      workflow_instance_id: event.instanceId,
      workflow_name: event.workflowName,
      consumer: request.consumer,
      workload: request.workload,
      status: "succeeded",
      input_manifest: inputManifest,
      submission: parameters.submission,
      steps: results,
      artifacts
    };
    const resultManifest = await step.do("persist-result-manifest", async () =>
      jsonArtifact(this.env, evidenceManifestKey(event.instanceId, "result"), manifestValue, "evidence_run_result", event.instanceId, true)
    );
    return {
      schema_version: 1,
      workflow_instance_id: event.instanceId,
      workflow_name: event.workflowName,
      consumer: request.consumer,
      workload: request.workload,
      status: "succeeded",
      input_manifest: inputManifest,
      result_manifest: resultManifest,
      steps: results,
      artifacts: [...artifacts, resultManifest]
    };
  }
}
