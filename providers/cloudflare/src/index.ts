import {
  isValidRequestId,
  verifySignedRequest,
  type AuthEnvironment
} from "./auth.js";
import { validateArtifactKey } from "./artifacts.js";
import { parseJsonObject, readBodyLimited } from "./body.js";
import { validateBrowserRunRequest } from "./browser-policy.js";
import {
  executeBrowserRun,
  type BrowserExecutionEnvironment,
  type BrowserSnapshotRunner
} from "./browser-run.js";
import {
  capabilitiesDocument,
  EDGE_SCHEMA_VERSION,
  type EdgeOperation,
  type EdgeReceipt,
  type EdgeReceiptEnvelope
} from "./contracts.js";
import { asEdgeError, EdgeError } from "./errors.js";
import type { ExecutionLease } from "./execution.js";
import {
  executeExternalFetch,
  type ExternalFetcher,
  type FetchExecutionEnvironment
} from "./external-fetch.js";
import { validateFetchRequest } from "./fetch-policy.js";
import {
  validateEvidenceRunRequest,
  EVIDENCE_RUN_CAPABILITY_VERSION
} from "./evidence-run-contracts.js";
import {
  EvidenceRunWorkflow,
  evidenceManifestKey,
  evidenceWorkflowInstanceId,
  persistEvidenceSubmission,
  type EvidenceRunParameters,
  type EvidenceWorkflowEnvironment
} from "./evidence-run.js";
export { EvidenceRunWorkflow };
import {
  beginRequest,
  commitReceipt,
  loadReceiptRecord
} from "./idempotency.js";
import {
  errorResponse,
  jsonResponse,
  methodNotAllowed
} from "./http.js";
import {
  consoleLogWriter,
  emitOperationLog,
  type EdgeLogWriter
} from "./observability.js";
import {
  effectivePolicyVersion,
  REQUEST_POLICY
} from "./policy.js";
import { createReceipt } from "./receipts.js";
import { workerDeploymentIdentity } from "./version.js";
const RECEIPT_PREFIX = "/v1/receipts/";
const ARTIFACT_PREFIX = "/v1/artifacts/";
const EVIDENCE_RUN_PREFIX = "/v1/evidence-runs/";

export interface Env
  extends AuthEnvironment,
    FetchExecutionEnvironment,
    BrowserExecutionEnvironment,
    EvidenceWorkflowEnvironment {
  readonly ARTIFACTS: R2Bucket;
  readonly BROWSER: BrowserRun;
  readonly FETCH_RATE_LIMIT: RateLimit;
  readonly BROWSER_RATE_LIMIT: RateLimit;
  readonly EVIDENCE_WORKFLOW: Workflow<EvidenceRunParameters>;
  readonly CF_VERSION_METADATA: WorkerVersionMetadata;
}

export interface HandlerDependencies {
  readonly fetcher?: ExternalFetcher;
  readonly browserRunner?: BrowserSnapshotRunner;
  readonly now?: () => Date;
  readonly tokenFactory?: () => string;
  readonly logWriter?: EdgeLogWriter;
  readonly rateLimit?: (
    operation: Extract<EdgeOperation, "fetch" | "browser.run">,
    key: string
  ) => Promise<boolean>;
}

function nowFrom(dependencies: HandlerDependencies): Date {
  return dependencies.now?.() ?? new Date();
}

function logWriterFrom(dependencies: HandlerDependencies): EdgeLogWriter {
  return dependencies.logWriter ?? consoleLogWriter;
}

function envelopeResponse(
  envelope: EdgeReceiptEnvelope,
  status = 200,
  retryAfterSeconds?: number
): Response {
  const response = jsonResponse(envelope, status);
  response.headers.set("x-ordivon-replayed", String(envelope.replayed));
  response.headers.set(
    "x-ordivon-worker-version",
    envelope.receipt.execution.worker_version_id
  );
  if (retryAfterSeconds !== undefined) {
    response.headers.set("retry-after", String(retryAfterSeconds));
  }
  return response;
}

async function enforceRateLimit(
  environment: Env,
  operation: Extract<EdgeOperation, "fetch" | "browser.run">,
  keyId: string,
  dependencies: HandlerDependencies
): Promise<void> {
  let allowed: boolean;
  try {
    if (dependencies.rateLimit !== undefined) {
      allowed = await dependencies.rateLimit(operation, keyId);
    } else {
      const limiter =
        operation === "browser.run"
          ? environment.BROWSER_RATE_LIMIT
          : environment.FETCH_RATE_LIMIT;
      allowed = (await limiter.limit({ key: keyId })).success;
    }
  } catch {
    throw new EdgeError(
      "rate_limit_unavailable",
      503,
      "The execution budget could not be checked.",
      "failed",
      10
    );
  }
  if (!allowed) {
    const browser = operation === "browser.run";
    throw new EdgeError(
      browser ? "browser_rate_limited" : "fetch_rate_limited",
      429,
      browser
        ? "Browser Run is rate limited."
        : "External Fetch is rate limited.",
      "failed",
      browser ? 10 : 60
    );
  }
}

async function persistReceipt(
  environment: Env,
  lease: ExecutionLease,
  receipt: EdgeReceipt,
  artifactKeys: readonly string[],
  dependencies: HandlerDependencies
): Promise<EdgeReceipt> {
  const writer = logWriterFrom(dependencies);
  try {
    const committed = await commitReceipt({
      bucket: environment.ARTIFACTS,
      lease,
      receipt,
      artifactKeys,
      onMirrorFailure(error) {
        emitOperationLog(writer, {
          event: "receipt_mirror_failed",
          operation: lease.operation,
          requestId: lease.request_id,
          lease,
          status: receipt.status,
          errorCode: error instanceof Error ? error.name : "unknown"
        });
      }
    });
    emitOperationLog(writer, {
      event: "operation_completed",
      operation: lease.operation,
      requestId: lease.request_id,
      lease,
      receipt: committed
    });
    return committed;
  } catch (error) {
    const edgeError = asEdgeError(error);
    emitOperationLog(writer, {
      event: "operation_commit_lost",
      operation: lease.operation,
      requestId: lease.request_id,
      lease,
      status: edgeError.receiptStatus,
      errorCode: edgeError.code
    });
    throw edgeError;
  }
}

async function beginOperation(
  environment: Env,
  requestId: string,
  requestDigest: string,
  operation: Extract<EdgeOperation, "fetch" | "browser.run">,
  dependencies: HandlerDependencies
): Promise<
  | { readonly kind: "replayed"; readonly response: Response }
  | { readonly kind: "acquired"; readonly lease: ExecutionLease }
> {
  const begin = await beginRequest({
    bucket: environment.ARTIFACTS,
    requestId,
    requestDigest,
    operation,
    policyVersion: await effectivePolicyVersion(environment),
    workerVersion: environment.CF_VERSION_METADATA,
    now: nowFrom(dependencies),
    ...(dependencies.tokenFactory === undefined
      ? {}
      : { tokenFactory: dependencies.tokenFactory })
  });
  const writer = logWriterFrom(dependencies);
  if (begin.kind === "replayed") {
    emitOperationLog(writer, {
      event: "operation_replayed",
      operation,
      requestId,
      receipt: begin.receipt,
      replayed: true
    });
    return {
      kind: "replayed",
      response: envelopeResponse({ receipt: begin.receipt, replayed: true })
    };
  }
  emitOperationLog(writer, {
    event: "operation_acquired",
    operation,
    requestId,
    lease: begin.lease,
    status: "pending"
  });
  return { kind: "acquired", lease: begin.lease };
}

async function handleFetchOperation(
  environment: Env,
  body: Uint8Array,
  requestId: string,
  requestDigest: string,
  keyId: string,
  dependencies: HandlerDependencies
): Promise<Response> {
  const begin = await beginOperation(
    environment,
    requestId,
    requestDigest,
    "fetch",
    dependencies
  );
  if (begin.kind === "replayed") return begin.response;

  const lease = begin.lease;
  const startedAt = new Date(lease.acquired_at);
  let result: Awaited<ReturnType<typeof executeExternalFetch>>;
  try {
    await enforceRateLimit(environment, "fetch", keyId, dependencies);
    const input = validateFetchRequest(parseJsonObject(body), environment);
    result = await executeExternalFetch(
      environment,
      lease,
      input,
      dependencies.fetcher
    );
  } catch (error) {
    const edgeError = asEdgeError(error);
    const receipt = createReceipt({
      operation: "fetch",
      status: edgeError.receiptStatus,
      requestDigest,
      receiptId: requestId,
      startedAt,
      completedAt: nowFrom(dependencies),
      execution: lease,
      errorCode: edgeError.code
    });
    const committed = await persistReceipt(
      environment,
      lease,
      receipt,
      [],
      dependencies
    );
    return envelopeResponse(
      { receipt: committed, replayed: false },
      edgeError.httpStatus,
      edgeError.retryAfterSeconds
    );
  }

  const receipt = createReceipt({
    operation: "fetch",
    status: "succeeded",
    requestDigest,
    receiptId: requestId,
    startedAt,
    completedAt: nowFrom(dependencies),
    execution: lease,
    artifact: result.artifact,
    artifacts: result.artifacts,
    fetch: result.fetch
  });
  const committed = await persistReceipt(
    environment,
    lease,
    receipt,
    result.artifacts.map((artifact) => artifact.key),
    dependencies
  );
  return envelopeResponse({ receipt: committed, replayed: false });
}

async function handleBrowserOperation(
  environment: Env,
  body: Uint8Array,
  requestId: string,
  requestDigest: string,
  keyId: string,
  dependencies: HandlerDependencies
): Promise<Response> {
  const begin = await beginOperation(
    environment,
    requestId,
    requestDigest,
    "browser.run",
    dependencies
  );
  if (begin.kind === "replayed") return begin.response;

  const lease = begin.lease;
  const startedAt = new Date(lease.acquired_at);
  let result: Awaited<ReturnType<typeof executeBrowserRun>>;
  try {
    await enforceRateLimit(environment, "browser.run", keyId, dependencies);
    const input = validateBrowserRunRequest(parseJsonObject(body), environment);
    result = await executeBrowserRun(
      environment,
      dependencies.browserRunner ?? environment.BROWSER,
      lease,
      input
    );
  } catch (error) {
    const edgeError = asEdgeError(error);
    const receipt = createReceipt({
      operation: "browser.run",
      status: edgeError.receiptStatus,
      requestDigest,
      receiptId: requestId,
      startedAt,
      completedAt: nowFrom(dependencies),
      execution: lease,
      errorCode: edgeError.code
    });
    const committed = await persistReceipt(
      environment,
      lease,
      receipt,
      [],
      dependencies
    );
    return envelopeResponse(
      { receipt: committed, replayed: false },
      edgeError.httpStatus,
      edgeError.retryAfterSeconds
    );
  }

  const receipt = createReceipt({
    operation: "browser.run",
    status: "succeeded",
    requestDigest,
    receiptId: requestId,
    startedAt,
    completedAt: nowFrom(dependencies),
    execution: lease,
    artifact: result.artifact,
    artifacts: result.artifacts,
    browser: result.browser
  });
  const committed = await persistReceipt(
    environment,
    lease,
    receipt,
    result.artifacts.map((artifact) => artifact.key),
    dependencies
  );
  return envelopeResponse({ receipt: committed, replayed: false });
}

async function handleReceiptGet(
  environment: Env,
  requestId: string
): Promise<Response> {
  if (!isValidRequestId(requestId)) {
    throw new EdgeError(
      "invalid_receipt_id",
      400,
      "The receipt ID is invalid."
    );
  }
  const receipt = await loadReceiptRecord(environment.ARTIFACTS, requestId);
  if (receipt === null) {
    return jsonResponse({ error: "receipt_not_found" }, 404);
  }
  return jsonResponse(receipt, receipt.status === "pending" ? 202 : 200);
}

function decodeArtifactKey(pathname: string): string {
  const encoded = pathname.slice(ARTIFACT_PREFIX.length);
  if (/%2f|%5c/i.test(encoded)) {
    throw new EdgeError(
      "invalid_artifact_key",
      400,
      "The artifact key is invalid."
    );
  }
  let decoded: string;
  try {
    decoded = encoded
      .split("/")
      .map((segment) => decodeURIComponent(segment))
      .join("/");
  } catch {
    throw new EdgeError(
      "invalid_artifact_key",
      400,
      "The artifact key is invalid."
    );
  }
  try {
    return validateArtifactKey(decoded);
  } catch {
    throw new EdgeError(
      "invalid_artifact_key",
      400,
      "The artifact key is invalid."
    );
  }
}

async function handleArtifactGet(
  environment: Env,
  pathname: string
): Promise<Response> {
  const key = decodeArtifactKey(pathname);
  const object = await environment.ARTIFACTS.get(key);
  if (object === null || object.body === undefined) {
    return jsonResponse({ error: "artifact_not_found" }, 404);
  }
  const originalMediaType =
    object.httpMetadata?.contentType ?? "application/octet-stream";
  const headers = new Headers({
    "cache-control": "no-store, no-transform",
    "content-type": "application/octet-stream",
    "content-disposition": "attachment; filename=artifact.bin",
    "content-length": String(object.size),
    etag: object.httpEtag,
    "x-content-type-options": "nosniff",
    "x-ordivon-media-type": originalMediaType,
    "content-security-policy": "default-src 'none'; frame-ancestors 'none'"
  });
  const sha256 = object.customMetadata?.sha256;
  if (sha256 !== undefined) {
    headers.set("x-ordivon-sha256", sha256);
  }
  return new Response(object.body, { headers });
}

const EVIDENCE_INSTANCE_ID = /^evidence-[a-z0-9][a-z0-9_-]{7,72}$/;

async function manifestReference(environment: Env, key: string) {
  const object = await environment.ARTIFACTS.get(key);
  if (object === null) return null;
  const sha256 = object.customMetadata?.sha256;
  if (sha256 === undefined) return null;
  return {
    key,
    sha256,
    bytes: object.size,
    media_type: object.httpMetadata?.contentType ?? "application/json; charset=utf-8",
    etag: object.etag
  };
}

async function evidenceRunStatus(environment: Env, instanceId: string): Promise<Response> {
  if (!EVIDENCE_INSTANCE_ID.test(instanceId)) {
    throw new EdgeError("invalid_evidence_run_id", 400, "The evidence run ID is invalid.");
  }
  let instance: WorkflowInstance;
  try {
    instance = await environment.EVIDENCE_WORKFLOW.get(instanceId);
  } catch {
    return jsonResponse({error: "evidence_run_not_found"}, 404);
  }
  const status = await instance.status();
  const resultManifest = await manifestReference(environment, evidenceManifestKey(instanceId, "result"));
  const failureManifest = await manifestReference(environment, evidenceManifestKey(instanceId, "failure"));
  const pending = ["queued", "running", "waiting", "waitingForPause", "paused", "unknown"].includes(status.status);
  return jsonResponse({
    schema_version: EDGE_SCHEMA_VERSION,
    foreign_operation_ref: {provider: "cloudflare-workflows", workflow: "ordivon-evidence-run", instance_id: instanceId},
    provider_status: status,
    result_manifest: resultManifest,
    failure_manifest: failureManifest
  }, pending ? 202 : 200);
}

async function createEvidenceRun(
  environment: Env,
  body: Uint8Array,
  requestId: string,
  requestDigest: string,
  dependencies: HandlerDependencies
): Promise<Response> {
  const evidenceRequest = validateEvidenceRunRequest(parseJsonObject(body), environment);
  const instanceId = evidenceWorkflowInstanceId(requestId);
  const parameters: EvidenceRunParameters = {
    request: evidenceRequest,
    submission: {
      request_id: requestId,
      request_digest: requestDigest,
      policy_version: await effectivePolicyVersion(environment),
      capability_version: EVIDENCE_RUN_CAPABILITY_VERSION,
      worker_version: environment.CF_VERSION_METADATA
    }
  };
  let submissionArtifact;
  try {
    submissionArtifact = await persistEvidenceSubmission(environment, instanceId, parameters);
  } catch (error) {
    const conflict = error instanceof Error && error.message.includes("conflict");
    throw new EdgeError(
      conflict ? "evidence_run_conflict" : "evidence_run_submission_unavailable",
      conflict ? 409 : 503,
      conflict ? "The evidence run request ID is already bound to different input." : "The evidence run submission could not be persisted.",
      conflict ? "rejected" : "failed"
    );
  }
  let instance: WorkflowInstance;
  let replayed = false;
  try {
    instance = await environment.EVIDENCE_WORKFLOW.create({
      id: instanceId,
      params: parameters,
      retention: {successRetention: "3 days", errorRetention: "3 days"}
    });
  } catch {
    try {
      instance = await environment.EVIDENCE_WORKFLOW.get(instanceId);
      replayed = true;
    } catch {
      throw new EdgeError("evidence_run_unavailable", 503, "The evidence run could not be created or reconciled.", "failed", 10);
    }
  }
  const status = await instance.status();
  return jsonResponse({
    schema_version: EDGE_SCHEMA_VERSION,
    foreign_operation_ref: {provider: "cloudflare-workflows", workflow: "ordivon-evidence-run", instance_id: instance.id},
    request_digest: requestDigest,
    submission_artifact: submissionArtifact,
    provider_status: status,
    replayed
  }, status.status === "complete" ? 200 : 202);
}

async function terminateEvidenceRun(environment: Env, instanceId: string): Promise<Response> {
  if (!EVIDENCE_INSTANCE_ID.test(instanceId)) {
    throw new EdgeError("invalid_evidence_run_id", 400, "The evidence run ID is invalid.");
  }
  let instance: WorkflowInstance;
  try {
    instance = await environment.EVIDENCE_WORKFLOW.get(instanceId);
    await instance.terminate({rollback: false});
  } catch {
    throw new EdgeError("evidence_run_not_terminable", 409, "The evidence run does not exist or cannot be terminated.", "rejected");
  }
  return jsonResponse({
    schema_version: EDGE_SCHEMA_VERSION,
    foreign_operation_ref: {provider: "cloudflare-workflows", workflow: "ordivon-evidence-run", instance_id: instanceId},
    provider_status: await instance.status()
  });
}

export async function handleRequest(
  request: Request,
  environment: Env,
  dependencies: HandlerDependencies = {}
): Promise<Response> {
  try {
    const body = await readBodyLimited(request, REQUEST_POLICY.max_body_bytes);
    const auth = await verifySignedRequest(request, body, environment);
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      if (request.method !== "GET") return methodNotAllowed("GET");
      return jsonResponse({
        schema_version: EDGE_SCHEMA_VERSION,
        service: "ordivon-edge",
        status: "ok",
        policy_version: await effectivePolicyVersion(environment),
        worker_version: environment.CF_VERSION_METADATA,
        deployment_identity: workerDeploymentIdentity(
          environment.CF_VERSION_METADATA
        )
      });
    }

    if (url.pathname === "/v1/capabilities") {
      if (request.method !== "GET") return methodNotAllowed("GET");
      return jsonResponse({
        ...capabilitiesDocument(await effectivePolicyVersion(environment)),
        worker_version: environment.CF_VERSION_METADATA,
        deployment_identity: workerDeploymentIdentity(
          environment.CF_VERSION_METADATA
        )
      });
    }

    if (url.pathname === "/v1/fetch") {
      if (request.method !== "POST") return methodNotAllowed("POST");
      return await handleFetchOperation(
        environment,
        body,
        auth.requestId,
        auth.requestDigest,
        auth.keyId,
        dependencies
      );
    }

    if (url.pathname === "/v1/browser/run") {
      if (request.method !== "POST") return methodNotAllowed("POST");
      return await handleBrowserOperation(
        environment,
        body,
        auth.requestId,
        auth.requestDigest,
        auth.keyId,
        dependencies
      );
    }

    if (url.pathname === "/v1/evidence-runs") {
      if (request.method !== "POST") return methodNotAllowed("POST");
      return await createEvidenceRun(
        environment,
        body,
        auth.requestId,
        auth.requestDigest,
        dependencies
      );
    }

    if (url.pathname.startsWith(EVIDENCE_RUN_PREFIX)) {
      const remainder = url.pathname.slice(EVIDENCE_RUN_PREFIX.length);
      if (remainder.endsWith("/terminate")) {
        if (request.method !== "POST") return methodNotAllowed("POST");
        return await terminateEvidenceRun(
          environment,
          remainder.slice(0, -"/terminate".length)
        );
      }
      if (request.method !== "GET") return methodNotAllowed("GET");
      return await evidenceRunStatus(environment, remainder);
    }

    if (url.pathname.startsWith(RECEIPT_PREFIX)) {
      if (request.method !== "GET") return methodNotAllowed("GET");
      return await handleReceiptGet(
        environment,
        url.pathname.slice(RECEIPT_PREFIX.length)
      );
    }

    if (url.pathname.startsWith(ARTIFACT_PREFIX)) {
      if (request.method !== "GET") return methodNotAllowed("GET");
      return await handleArtifactGet(environment, url.pathname);
    }

    return jsonResponse({ error: "not_found" }, 404);
  } catch (error) {
    return errorResponse(asEdgeError(error));
  }
}

export default {
  fetch(request: Request, environment: Env): Promise<Response> {
    return handleRequest(request, environment);
  }
} satisfies ExportedHandler<Env>;
