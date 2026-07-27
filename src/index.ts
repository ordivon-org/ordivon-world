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
  CAPABILITIES,
  EDGE_SCHEMA_VERSION,
  type EdgeReceiptEnvelope
} from "./contracts.js";
import { asEdgeError, EdgeError } from "./errors.js";
import {
  executeExternalFetch,
  type ExternalFetcher,
  type FetchExecutionEnvironment
} from "./external-fetch.js";
import { validateFetchRequest } from "./fetch-policy.js";
import {
  beginRequest,
  loadReceipt,
  storeReceipt
} from "./idempotency.js";
import {
  errorResponse,
  jsonResponse,
  methodNotAllowed
} from "./http.js";
import { createReceipt } from "./receipts.js";

const MAX_REQUEST_BODY_BYTES = 8_192;
const RECEIPT_PREFIX = "/v1/receipts/";
const ARTIFACT_PREFIX = "/v1/artifacts/";

export interface Env
  extends AuthEnvironment, FetchExecutionEnvironment, BrowserExecutionEnvironment {
  readonly ARTIFACTS: R2Bucket;
  readonly BROWSER: BrowserRun;
}

export interface HandlerDependencies {
  readonly fetcher?: ExternalFetcher;
  readonly browserRunner?: BrowserSnapshotRunner;
  readonly now?: () => Date;
}

function nowFrom(dependencies: HandlerDependencies): Date {
  return dependencies.now?.() ?? new Date();
}

function envelopeResponse(
  envelope: EdgeReceiptEnvelope,
  status = 200
): Response {
  const response = jsonResponse(envelope, status);
  response.headers.set("x-ordivon-replayed", String(envelope.replayed));
  return response;
}

async function handleFetchOperation(
  environment: Env,
  body: Uint8Array,
  requestId: string,
  requestDigest: string,
  dependencies: HandlerDependencies
): Promise<Response> {
  const begin = await beginRequest(
    environment.ARTIFACTS,
    requestId,
    requestDigest,
    "fetch",
    nowFrom(dependencies)
  );
  if (begin.kind === "replayed") {
    return envelopeResponse({ receipt: begin.receipt, replayed: true });
  }

  const startedAt = nowFrom(dependencies);
  try {
    const input = validateFetchRequest(parseJsonObject(body), environment);
    const result = await executeExternalFetch(
      environment,
      requestId,
      input,
      dependencies.fetcher
    );
    const receipt = createReceipt({
      operation: "fetch",
      status: "succeeded",
      requestDigest,
      receiptId: requestId,
      startedAt,
      completedAt: nowFrom(dependencies),
      artifact: result.artifact,
      fetch: result.fetch
    });
    await storeReceipt(environment.ARTIFACTS, receipt);
    return envelopeResponse({ receipt, replayed: false });
  } catch (error) {
    const edgeError = asEdgeError(error);
    const receipt = createReceipt({
      operation: "fetch",
      status: edgeError.receiptStatus,
      requestDigest,
      receiptId: requestId,
      startedAt,
      completedAt: nowFrom(dependencies),
      errorCode: edgeError.code
    });
    await storeReceipt(environment.ARTIFACTS, receipt);
    return envelopeResponse(
      { receipt, replayed: false },
      edgeError.httpStatus
    );
  }
}

async function handleBrowserOperation(
  environment: Env,
  body: Uint8Array,
  requestId: string,
  requestDigest: string,
  dependencies: HandlerDependencies
): Promise<Response> {
  const begin = await beginRequest(
    environment.ARTIFACTS,
    requestId,
    requestDigest,
    "browser.run",
    nowFrom(dependencies)
  );
  if (begin.kind === "replayed") {
    return envelopeResponse({ receipt: begin.receipt, replayed: true });
  }

  const startedAt = nowFrom(dependencies);
  try {
    const input = validateBrowserRunRequest(parseJsonObject(body), environment);
    const result = await executeBrowserRun(
      environment,
      dependencies.browserRunner ?? environment.BROWSER,
      requestId,
      input
    );
    const receipt = createReceipt({
      operation: "browser.run",
      status: "succeeded",
      requestDigest,
      receiptId: requestId,
      startedAt,
      completedAt: nowFrom(dependencies),
      artifact: result.artifact,
      artifacts: result.artifacts,
      browser: result.browser
    });
    await storeReceipt(environment.ARTIFACTS, receipt);
    return envelopeResponse({ receipt, replayed: false });
  } catch (error) {
    const edgeError = asEdgeError(error);
    const receipt = createReceipt({
      operation: "browser.run",
      status: edgeError.receiptStatus,
      requestDigest,
      receiptId: requestId,
      startedAt,
      completedAt: nowFrom(dependencies),
      errorCode: edgeError.code
    });
    await storeReceipt(environment.ARTIFACTS, receipt);
    return envelopeResponse(
      { receipt, replayed: false },
      edgeError.httpStatus
    );
  }
}

async function handleReceiptGet(
  environment: Env,
  requestId: string
): Promise<Response> {
  if (!isValidRequestId(requestId)) {
    throw new EdgeError("invalid_receipt_id", 400, "The receipt ID is invalid.");
  }
  const receipt = await loadReceipt(environment.ARTIFACTS, requestId);
  return receipt === null
    ? jsonResponse({ error: "receipt_not_found" }, 404)
    : jsonResponse(receipt);
}

function decodeArtifactKey(pathname: string): string {
  const encoded = pathname.slice(ARTIFACT_PREFIX.length);
  if (/%2f|%5c/i.test(encoded)) {
    throw new EdgeError("invalid_artifact_key", 400, "The artifact key is invalid.");
  }
  let decoded: string;
  try {
    decoded = encoded
      .split("/")
      .map((segment) => decodeURIComponent(segment))
      .join("/");
  } catch {
    throw new EdgeError("invalid_artifact_key", 400, "The artifact key is invalid.");
  }
  try {
    return validateArtifactKey(decoded);
  } catch {
    throw new EdgeError("invalid_artifact_key", 400, "The artifact key is invalid.");
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

export async function handleRequest(
  request: Request,
  environment: Env,
  dependencies: HandlerDependencies = {}
): Promise<Response> {
  try {
    const body = await readBodyLimited(request, MAX_REQUEST_BODY_BYTES);
    const auth = await verifySignedRequest(request, body, environment);
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      if (request.method !== "GET") {
        return methodNotAllowed("GET");
      }
      return jsonResponse({
        schema_version: EDGE_SCHEMA_VERSION,
        service: "ordivon-edge",
        status: "ok"
      });
    }

    if (url.pathname === "/v1/capabilities") {
      if (request.method !== "GET") {
        return methodNotAllowed("GET");
      }
      return jsonResponse(CAPABILITIES);
    }

    if (url.pathname === "/v1/fetch") {
      if (request.method !== "POST") {
        return methodNotAllowed("POST");
      }
      return await handleFetchOperation(
        environment,
        body,
        auth.requestId,
        auth.requestDigest,
        dependencies
      );
    }

    if (url.pathname === "/v1/browser/run") {
      if (request.method !== "POST") {
        return methodNotAllowed("POST");
      }
      return await handleBrowserOperation(
        environment,
        body,
        auth.requestId,
        auth.requestDigest,
        dependencies
      );
    }

    if (url.pathname.startsWith(RECEIPT_PREFIX)) {
      if (request.method !== "GET") {
        return methodNotAllowed("GET");
      }
      return await handleReceiptGet(
        environment,
        url.pathname.slice(RECEIPT_PREFIX.length)
      );
    }

    if (url.pathname.startsWith(ARTIFACT_PREFIX)) {
      if (request.method !== "GET") {
        return methodNotAllowed("GET");
      }
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
