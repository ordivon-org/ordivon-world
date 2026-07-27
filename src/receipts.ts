import {
  EDGE_SCHEMA_VERSION,
  type ArtifactReference,
  type EdgeOperation,
  type EdgeReceipt,
  type ReceiptStatus
} from "./contracts.js";

export interface ReceiptFactoryOptions {
  readonly operation: EdgeOperation;
  readonly status: ReceiptStatus;
  readonly startedAt: Date;
  readonly completedAt: Date;
  readonly receiptId?: string;
  readonly artifact?: ArtifactReference;
  readonly errorCode?: string;
}

const ERROR_CODE_PATTERN = /^[a-z][a-z0-9_]{0,63}$/;

export function createReceipt(options: ReceiptFactoryOptions): EdgeReceipt {
  if (options.completedAt.getTime() < options.startedAt.getTime()) {
    throw new Error("completedAt must not precede startedAt");
  }
  if (options.status === "succeeded" && options.errorCode !== undefined) {
    throw new Error("a succeeded receipt cannot carry an error code");
  }
  if (
    options.errorCode !== undefined &&
    !ERROR_CODE_PATTERN.test(options.errorCode)
  ) {
    throw new Error("errorCode must be a bounded snake_case identifier");
  }

  const receipt: EdgeReceipt = {
    schema_version: EDGE_SCHEMA_VERSION,
    receipt_id: options.receiptId ?? crypto.randomUUID(),
    operation: options.operation,
    status: options.status,
    started_at: options.startedAt.toISOString(),
    completed_at: options.completedAt.toISOString()
  };

  return {
    ...receipt,
    ...(options.artifact === undefined ? {} : { artifact: options.artifact }),
    ...(options.errorCode === undefined ? {} : { error_code: options.errorCode })
  };
}
