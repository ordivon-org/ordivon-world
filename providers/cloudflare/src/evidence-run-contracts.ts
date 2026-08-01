import { validateBrowserRunRequest } from "./browser-policy.js";
import { EdgeError } from "./errors.js";
import { validateFetchRequest, type FetchPolicyEnvironment } from "./fetch-policy.js";

export const EVIDENCE_RUN_SCHEMA_VERSION = 1 as const;
export const EVIDENCE_RUN_CAPABILITY_VERSION = "evidence.run.v1" as const;
const SAFE_ID = /^[a-z0-9][a-z0-9._-]{0,63}$/;
const SAFE_LABEL = /^[a-zA-Z0-9][a-zA-Z0-9 ._:/-]{0,127}$/;
const MAX_STEPS = 8;

export interface EvidenceFetchStep {
  readonly id: string;
  readonly operation: "fetch";
  readonly input: {
    readonly url: string;
    readonly maximum_bytes?: number;
    readonly timeout_ms?: number;
    readonly accept?: string;
  };
}

export interface EvidenceBrowserStep {
  readonly id: string;
  readonly operation: "browser.run";
  readonly input: {
    readonly url: string;
    readonly viewport_width?: number;
    readonly viewport_height?: number;
    readonly full_page?: boolean;
    readonly wait_until?: "load" | "domcontentloaded" | "networkidle0" | "networkidle2";
    readonly timeout_ms?: number;
    readonly wait_after_ms?: number;
  };
}

export type EvidenceRunStep = EvidenceFetchStep | EvidenceBrowserStep;

export interface EvidenceRunRequest {
  readonly schema_version: typeof EVIDENCE_RUN_SCHEMA_VERSION;
  readonly consumer: string;
  readonly workload: string;
  readonly steps: readonly EvidenceRunStep[];
}

function object(value: unknown, context: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new EdgeError("invalid_evidence_run", 422, `${context} must be an object.`, "rejected");
  }
  return value as Record<string, unknown>;
}

function exactKeys(value: Record<string, unknown>, allowed: readonly string[], context: string): void {
  const unknown = Object.keys(value).filter((key) => !allowed.includes(key));
  if (unknown.length > 0) {
    throw new EdgeError("unsupported_evidence_run_field", 422, `${context} contains unsupported fields.`, "rejected");
  }
}

function label(value: unknown, context: string): string {
  if (typeof value !== "string" || !SAFE_LABEL.test(value)) {
    throw new EdgeError("invalid_evidence_run", 422, `${context} is invalid.`, "rejected");
  }
  return value;
}

function step(value: unknown, environment: FetchPolicyEnvironment): EvidenceRunStep {
  const item = object(value, "evidence run step");
  exactKeys(item, ["id", "operation", "input"], "evidence run step");
  if (typeof item.id !== "string" || !SAFE_ID.test(item.id)) {
    throw new EdgeError("invalid_evidence_run", 422, "Evidence step ID is invalid.", "rejected");
  }
  const input = object(item.input, "evidence step input");
  if (item.operation === "fetch") {
    exactKeys(input, ["url", "maximum_bytes", "timeout_ms", "accept"], "fetch evidence input");
    validateFetchRequest(input, environment);
    return {id: item.id, operation: "fetch", input: input as unknown as EvidenceFetchStep["input"]};
  }
  if (item.operation === "browser.run") {
    exactKeys(input, ["url", "viewport_width", "viewport_height", "full_page", "wait_until", "timeout_ms", "wait_after_ms"], "browser evidence input");
    validateBrowserRunRequest(input, environment);
    return {id: item.id, operation: "browser.run", input: input as unknown as EvidenceBrowserStep["input"]};
  }
  throw new EdgeError("invalid_evidence_run", 422, "Evidence step operation is unsupported.", "rejected");
}

export function validateEvidenceRunRequest(value: unknown, environment: FetchPolicyEnvironment): EvidenceRunRequest {
  const root = object(value, "evidence run");
  exactKeys(root, ["schema_version", "consumer", "workload", "steps"], "evidence run");
  if (root.schema_version !== EVIDENCE_RUN_SCHEMA_VERSION) {
    throw new EdgeError("invalid_evidence_run", 422, "Evidence run schema version is unsupported.", "rejected");
  }
  if (!Array.isArray(root.steps) || root.steps.length < 1 || root.steps.length > MAX_STEPS) {
    throw new EdgeError("invalid_evidence_run", 422, `Evidence run requires 1-${MAX_STEPS} steps.`, "rejected");
  }
  const steps = root.steps.map((value) => step(value, environment));
  if (new Set(steps.map((item) => item.id)).size !== steps.length) {
    throw new EdgeError("invalid_evidence_run", 422, "Evidence step IDs must be unique.", "rejected");
  }
  return {
    schema_version: EVIDENCE_RUN_SCHEMA_VERSION,
    consumer: label(root.consumer, "consumer"),
    workload: label(root.workload, "workload"),
    steps
  };
}
