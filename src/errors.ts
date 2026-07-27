import type { ReceiptStatus } from "./contracts.js";

export class EdgeError extends Error {
  readonly code: string;
  readonly httpStatus: number;
  readonly receiptStatus: ReceiptStatus;

  constructor(
    code: string,
    httpStatus: number,
    message: string,
    receiptStatus: ReceiptStatus = httpStatus >= 500 ? "failed" : "rejected"
  ) {
    super(message);
    this.name = "EdgeError";
    this.code = code;
    this.httpStatus = httpStatus;
    this.receiptStatus = receiptStatus;
  }
}

export function asEdgeError(error: unknown): EdgeError {
  if (error instanceof EdgeError) {
    return error;
  }
  if (error instanceof DOMException && error.name === "AbortError") {
    return new EdgeError("fetch_timeout", 504, "The external request exceeded its time budget.", "failed");
  }
  return new EdgeError("internal_error", 500, "The Edge operation failed.", "failed");
}
