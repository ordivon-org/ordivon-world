import type {
  EdgeExecutionMetadata,
  EdgeOperation
} from "./contracts.js";
import {
  CAPABILITY_VERSIONS,
  EDGE_POLICY_VERSION
} from "./version.js";

const LEASE_MILLISECONDS = {
  fetch: 60_000,
  "browser.run": 120_000,
  "artifact.put": 60_000,
  "artifact.get": 30_000,
  "artifact.delete": 60_000
} as const satisfies Record<EdgeOperation, number>;

export interface ExecutionLease extends EdgeExecutionMetadata {
  readonly request_id: string;
  readonly request_digest: string;
  readonly operation: EdgeOperation;
  readonly lease_token: string;
  readonly acquired_at: string;
  readonly lease_expires_at: string;
  readonly state_etag: string;
}

export function executionMetadata(
  operation: EdgeOperation,
  workerVersion: WorkerVersionMetadata,
  leaseGeneration: number
): EdgeExecutionMetadata {
  return {
    policy_version: EDGE_POLICY_VERSION,
    capability_version: CAPABILITY_VERSIONS[operation],
    worker_version_id: workerVersion.id,
    worker_version_tag: workerVersion.tag,
    worker_version_timestamp: workerVersion.timestamp,
    lease_generation: leaseGeneration
  };
}

export function leaseDurationMilliseconds(operation: EdgeOperation): number {
  return LEASE_MILLISECONDS[operation];
}
