import { sha256Hex } from "./auth.js";
import {
  browserRunOptions,
  type ValidatedBrowserRunRequest
} from "./browser-policy.js";
import type {
  ArtifactReference,
  BrowserReceiptDetails
} from "./contracts.js";
import { EdgeError } from "./errors.js";

const MAX_BROWSER_RESPONSE_BYTES = 8 * 1_048_576;
const MAX_SCREENSHOT_BYTES = 4 * 1_048_576;
const MAX_CONTENT_BYTES = 1_048_576;

interface SnapshotSuccess {
  readonly success: true;
  readonly result: {
    readonly content: string;
    readonly screenshot: string;
  };
  readonly meta: {
    readonly status: number;
    readonly title: string;
  };
}

export interface BrowserSnapshotRunner {
  quickAction(
    action: "snapshot",
    options: BrowserRunSnapshotOptions
  ): Promise<Response>;
}

export interface BrowserExecutionEnvironment {
  readonly ARTIFACTS: R2Bucket;
}

export interface BrowserExecutionResult {
  readonly artifact: ArtifactReference;
  readonly artifacts: readonly ArtifactReference[];
  readonly browser: BrowserReceiptDetails;
}

async function readLimited(response: Response, maximumBytes: number): Promise<Uint8Array> {
  const declaredLength = response.headers.get("content-length");
  if (declaredLength !== null) {
    const parsed = Number.parseInt(declaredLength, 10);
    if (Number.isSafeInteger(parsed) && parsed > maximumBytes) {
      await response.body?.cancel("Browser Run response exceeded limit");
      throw new EdgeError("browser_output_too_large", 502, "Browser Run output exceeded its budget.", "failed");
    }
  }
  if (response.body === null) {
    return new Uint8Array();
  }
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > maximumBytes) {
        await reader.cancel("Browser Run response exceeded limit");
        throw new EdgeError("browser_output_too_large", 502, "Browser Run output exceeded its budget.", "failed");
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }
  const body = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    body.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return body;
}

function browserFailure(status: number): EdgeError {
  if (status === 429) {
    return new EdgeError("browser_rate_limited", 429, "Browser Run is rate limited.", "failed");
  }
  if (status === 503) {
    return new EdgeError("browser_unavailable", 503, "Browser Run is temporarily unavailable.", "failed");
  }
  return new EdgeError("browser_run_failed", 502, "Browser Run failed.", "failed");
}

function decodeScreenshot(value: string): Uint8Array {
  const encoded = value.startsWith("data:") ? value.slice(value.indexOf(",") + 1) : value;
  if (!/^[A-Za-z0-9+/]*={0,2}$/.test(encoded)) {
    throw new EdgeError("invalid_browser_output", 502, "Browser Run returned an invalid screenshot.", "failed");
  }
  let decoded: string;
  try {
    decoded = atob(encoded);
  } catch {
    throw new EdgeError("invalid_browser_output", 502, "Browser Run returned an invalid screenshot.", "failed");
  }
  if (decoded.length > MAX_SCREENSHOT_BYTES) {
    throw new EdgeError("browser_output_too_large", 502, "Browser screenshot exceeded its budget.", "failed");
  }
  return Uint8Array.from(decoded, (character) => character.charCodeAt(0));
}

function parseSnapshot(body: Uint8Array): SnapshotSuccess {
  let value: unknown;
  try {
    value = JSON.parse(new TextDecoder("utf-8", { fatal: true, ignoreBOM: false }).decode(body));
  } catch {
    throw new EdgeError("invalid_browser_output", 502, "Browser Run returned invalid JSON.", "failed");
  }
  if (
    value === null ||
    typeof value !== "object" ||
    (value as { success?: unknown }).success !== true
  ) {
    throw new EdgeError("browser_run_failed", 502, "Browser Run failed.", "failed");
  }
  const snapshot = value as Partial<SnapshotSuccess>;
  if (
    snapshot.result === undefined ||
    typeof snapshot.result.content !== "string" ||
    typeof snapshot.result.screenshot !== "string" ||
    snapshot.meta === undefined ||
    !Number.isInteger(snapshot.meta.status) ||
    typeof snapshot.meta.title !== "string"
  ) {
    throw new EdgeError("invalid_browser_output", 502, "Browser Run returned an invalid snapshot.", "failed");
  }
  return snapshot as SnapshotSuccess;
}

function parseBrowserMilliseconds(response: Response): number {
  const value = response.headers.get("x-browser-ms-used");
  if (value === null) return 0;
  const parsed = Number.parseInt(value, 10);
  return Number.isSafeInteger(parsed) && parsed >= 0 ? parsed : 0;
}

async function storeArtifact(
  bucket: R2Bucket,
  key: string,
  body: Uint8Array,
  mediaType: string,
  requestId: string,
  kind: string
): Promise<ArtifactReference> {
  const sha256 = await sha256Hex(body);
  const stored = await bucket.put(key, body, {
    httpMetadata: { contentType: mediaType },
    customMetadata: {
      receipt_id: requestId,
      sha256,
      kind
    }
  });
  if (stored === null) {
    throw new EdgeError("artifact_store_failed", 500, "Browser artifact could not be persisted.", "failed");
  }
  return {
    key,
    sha256,
    bytes: body.byteLength,
    media_type: mediaType,
    etag: stored.etag
  };
}

export async function executeBrowserRun(
  environment: BrowserExecutionEnvironment,
  runner: BrowserSnapshotRunner,
  requestId: string,
  request: ValidatedBrowserRunRequest
): Promise<BrowserExecutionResult> {
  let response: Response;
  try {
    response = await runner.quickAction("snapshot", browserRunOptions(request));
  } catch {
    throw new EdgeError("browser_unavailable", 503, "Browser Run is temporarily unavailable.", "failed");
  }
  const browserMs = parseBrowserMilliseconds(response);
  const body = await readLimited(response, MAX_BROWSER_RESPONSE_BYTES);
  if (!response.ok) {
    throw browserFailure(response.status);
  }
  const snapshot = parseSnapshot(body);
  const content = new TextEncoder().encode(snapshot.result.content);
  if (content.byteLength > MAX_CONTENT_BYTES) {
    throw new EdgeError("browser_output_too_large", 502, "Rendered HTML exceeded its budget.", "failed");
  }
  const screenshot = decodeScreenshot(snapshot.result.screenshot);
  const base = `browser/v1/${requestId}`;
  const writtenKeys: string[] = [];
  try {
    const screenshotArtifact = await storeArtifact(
      environment.ARTIFACTS,
      `${base}/screenshot.png`,
      screenshot,
      "image/png",
      requestId,
      "screenshot"
    );
    writtenKeys.push(screenshotArtifact.key);
    const contentArtifact = await storeArtifact(
      environment.ARTIFACTS,
      `${base}/content.html`,
      content,
      "text/html; charset=utf-8",
      requestId,
      "rendered_content"
    );
    writtenKeys.push(contentArtifact.key);

    const browser: BrowserReceiptDetails = {
      requested_url: request.url.toString(),
      page_title: snapshot.meta.title.slice(0, 512),
      page_status: snapshot.meta.status,
      browser_ms: browserMs,
      viewport: request.viewport,
      full_page: request.fullPage
    };
    const manifestBody = new TextEncoder().encode(JSON.stringify({
      schema_version: 1,
      receipt_id: requestId,
      browser,
      artifacts: [screenshotArtifact, contentArtifact]
    }));
    const manifestArtifact = await storeArtifact(
      environment.ARTIFACTS,
      `${base}/manifest.json`,
      manifestBody,
      "application/json; charset=utf-8",
      requestId,
      "manifest"
    );
    writtenKeys.push(manifestArtifact.key);
    return {
      artifact: manifestArtifact,
      artifacts: [screenshotArtifact, contentArtifact, manifestArtifact],
      browser
    };
  } catch (error) {
    if (writtenKeys.length > 0) {
      await environment.ARTIFACTS.delete(writtenKeys);
    }
    throw error;
  }
}
