import {
  EDGE_SCHEMA_VERSION,
  type ArtifactReference,
  type BrowserReceiptDetails,
  type EdgeExecutionMetadata,
  type EdgeOperation,
  type EdgeReceipt,
  type FetchReceiptDetails,
  type ReceiptStatus
} from "./contracts.js";

export interface ReceiptFactoryOptions {
  readonly operation: EdgeOperation;
  readonly status: ReceiptStatus;
  readonly requestDigest: string;
  readonly startedAt: Date;
  readonly completedAt: Date;
  readonly receiptId: string;
  readonly execution: EdgeExecutionMetadata;
  readonly artifact?: ArtifactReference;
  readonly artifacts?: readonly ArtifactReference[];
  readonly fetch?: FetchReceiptDetails;
  readonly browser?: BrowserReceiptDetails;
  readonly errorCode?: string;
}

const ERROR_CODE_PATTERN = /^[a-z][a-z0-9_]{0,63}$/;
const DIGEST_PATTERN = /^[a-f0-9]{64}$/;

export function createReceipt(options: ReceiptFactoryOptions): EdgeReceipt {
  const durationMs = options.completedAt.getTime() - options.startedAt.getTime();
  if (durationMs < 0) {
    throw new Error("completedAt must not precede startedAt");
  }
  if (!DIGEST_PATTERN.test(options.requestDigest)) {
    throw new Error("requestDigest must be a SHA-256 digest");
  }
  if (options.status === "succeeded" && options.errorCode !== undefined) {
    throw new Error("a succeeded receipt cannot carry an error code");
  }
  if (options.status !== "succeeded" && options.errorCode === undefined) {
    throw new Error("a non-succeeded receipt requires an error code");
  }
  if (
    options.errorCode !== undefined &&
    !ERROR_CODE_PATTERN.test(options.errorCode)
  ) {
    throw new Error("errorCode must be a bounded snake_case identifier");
  }
  if (options.artifacts !== undefined && options.artifacts.length === 0) {
    throw new Error("artifacts must not be empty");
  }
  if (!Number.isSafeInteger(options.execution.lease_generation) || options.execution.lease_generation < 1) {
    throw new Error("lease generation must be a positive integer");
  }

  return {
    schema_version: EDGE_SCHEMA_VERSION,
    receipt_id: options.receiptId,
    request_digest: options.requestDigest,
    operation: options.operation,
    status: options.status,
    started_at: options.startedAt.toISOString(),
    completed_at: options.completedAt.toISOString(),
    duration_ms: durationMs,
    execution: {
      policy_version: options.execution.policy_version,
      capability_version: options.execution.capability_version,
      worker_version_id: options.execution.worker_version_id,
      worker_version_tag: options.execution.worker_version_tag,
      worker_version_timestamp: options.execution.worker_version_timestamp,
      lease_generation: options.execution.lease_generation
    },
    ...(options.artifact === undefined ? {} : { artifact: options.artifact }),
    ...(options.artifacts === undefined ? {} : { artifacts: options.artifacts }),
    ...(options.fetch === undefined ? {} : { fetch: options.fetch }),
    ...(options.browser === undefined ? {} : { browser: options.browser }),
    ...(options.errorCode === undefined ? {} : { error_code: options.errorCode })
  };
}
