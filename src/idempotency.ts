import { EDGE_SCHEMA_VERSION, type EdgeOperation, type EdgeReceipt } from "./contracts.js";
import { EdgeError } from "./errors.js";

const LOCK_STALE_AFTER_MS = 60_000;

interface RequestLock {
  readonly schema_version: typeof EDGE_SCHEMA_VERSION;
  readonly request_id: string;
  readonly request_digest: string;
  readonly operation: EdgeOperation;
  readonly acquired_at: string;
}

export type BeginRequestResult =
  | { readonly kind: "acquired" }
  | { readonly kind: "replayed"; readonly receipt: EdgeReceipt };

export function receiptKey(requestId: string): string {
  return `receipts/v1/${requestId}.json`;
}

function requestKey(requestId: string): string {
  return `requests/v1/${requestId}.json`;
}

async function readJson<T>(object: R2ObjectBody): Promise<T> {
  return JSON.parse(await object.text()) as T;
}

export async function loadReceipt(
  bucket: R2Bucket,
  requestId: string
): Promise<EdgeReceipt | null> {
  const object = await bucket.get(receiptKey(requestId));
  return object === null ? null : readJson<EdgeReceipt>(object);
}

async function loadLock(
  bucket: R2Bucket,
  requestId: string
): Promise<{ object: R2ObjectBody; lock: RequestLock } | null> {
  const object = await bucket.get(requestKey(requestId));
  return object === null ? null : { object, lock: await readJson<RequestLock>(object) };
}

function assertSameDigest(existingDigest: string, requestDigest: string): void {
  if (existingDigest !== requestDigest) {
    throw new EdgeError(
      "idempotency_conflict",
      409,
      "The request ID is already bound to different request content."
    );
  }
}

export async function beginRequest(
  bucket: R2Bucket,
  requestId: string,
  requestDigest: string,
  operation: EdgeOperation,
  now = new Date()
): Promise<BeginRequestResult> {
  const existingReceipt = await loadReceipt(bucket, requestId);
  if (existingReceipt !== null) {
    assertSameDigest(existingReceipt.request_digest, requestDigest);
    return { kind: "replayed", receipt: existingReceipt };
  }

  const existingLock = await loadLock(bucket, requestId);
  if (existingLock !== null) {
    assertSameDigest(existingLock.lock.request_digest, requestDigest);
    const acquiredAt = Date.parse(existingLock.lock.acquired_at);
    if (Number.isFinite(acquiredAt) && now.getTime() - acquiredAt < LOCK_STALE_AFTER_MS) {
      throw new EdgeError("request_in_progress", 409, "The request is already in progress.");
    }

    const replacement: RequestLock = {
      ...existingLock.lock,
      acquired_at: now.toISOString()
    };
    const replaced = await bucket.put(
      requestKey(requestId),
      JSON.stringify(replacement),
      {
        onlyIf: { etagMatches: existingLock.object.etag },
        httpMetadata: { contentType: "application/json; charset=utf-8" },
        customMetadata: { request_digest: requestDigest, operation }
      }
    );
    if (replaced === null) {
      throw new EdgeError("request_in_progress", 409, "The request is already in progress.");
    }
    return { kind: "acquired" };
  }

  const lock: RequestLock = {
    schema_version: EDGE_SCHEMA_VERSION,
    request_id: requestId,
    request_digest: requestDigest,
    operation,
    acquired_at: now.toISOString()
  };
  const created = await bucket.put(requestKey(requestId), JSON.stringify(lock), {
    onlyIf: { etagDoesNotMatch: "*" },
    httpMetadata: { contentType: "application/json; charset=utf-8" },
    customMetadata: { request_digest: requestDigest, operation }
  });
  if (created === null) {
    return beginRequest(bucket, requestId, requestDigest, operation, now);
  }
  return { kind: "acquired" };
}

export async function storeReceipt(
  bucket: R2Bucket,
  receipt: EdgeReceipt
): Promise<void> {
  await bucket.put(receiptKey(receipt.receipt_id), JSON.stringify(receipt), {
    httpMetadata: { contentType: "application/json; charset=utf-8" },
    customMetadata: {
      request_digest: receipt.request_digest,
      operation: receipt.operation,
      status: receipt.status
    }
  });
}
