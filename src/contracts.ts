import {
  CAPABILITY_VERSIONS,
  EDGE_POLICY_VERSION
} from "./version.js";

export const EDGE_SCHEMA_VERSION = 1 as const;
export const REQUEST_STATE_SCHEMA_VERSION = 2 as const;

export type CapabilityState = "ready" | "planned" | "disabled";

export type EdgeOperation =
  | "fetch"
  | "browser.run"
  | "artifact.put"
  | "artifact.get"
  | "artifact.delete";

export type ReceiptStatus = "succeeded" | "failed" | "rejected";

export interface EdgeCapability {
  readonly id: EdgeOperation | "receipt";
  readonly version: string;
  readonly state: CapabilityState;
  readonly reason: string;
}

export interface EdgeCapabilitiesDocument {
  readonly schema_version: typeof EDGE_SCHEMA_VERSION;
  readonly service: "ordivon-edge";
  readonly policy_version: string;
  readonly capabilities: readonly EdgeCapability[];
}

export interface EdgeExecutionMetadata {
  readonly policy_version: string;
  readonly capability_version: string;
  readonly worker_version_id: string;
  readonly worker_version_tag: string;
  readonly worker_version_timestamp: string;
  readonly lease_generation: number;
}

export interface ArtifactReference {
  readonly key: string;
  readonly sha256: string;
  readonly bytes: number;
  readonly media_type: string;
  readonly etag?: string;
}

export interface FetchReceiptDetails {
  readonly requested_url: string;
  readonly final_url: string;
  readonly http_status: number;
  readonly redirect_count: number;
}

export interface BrowserReceiptDetails {
  readonly requested_url: string;
  readonly page_title: string;
  readonly page_status: number;
  readonly browser_ms: number;
  readonly viewport: {
    readonly width: number;
    readonly height: number;
  };
  readonly full_page: boolean;
}

export interface EdgeReceipt {
  readonly schema_version: typeof EDGE_SCHEMA_VERSION;
  readonly receipt_id: string;
  readonly request_digest: string;
  readonly operation: EdgeOperation;
  readonly status: ReceiptStatus;
  readonly started_at: string;
  readonly completed_at: string;
  readonly duration_ms: number;
  readonly execution: EdgeExecutionMetadata;
  readonly artifact?: ArtifactReference;
  readonly artifacts?: readonly ArtifactReference[];
  readonly fetch?: FetchReceiptDetails;
  readonly browser?: BrowserReceiptDetails;
  readonly error_code?: string;
}

export interface EdgePendingReceipt {
  readonly schema_version: typeof EDGE_SCHEMA_VERSION;
  readonly receipt_id: string;
  readonly request_digest: string;
  readonly operation: EdgeOperation;
  readonly status: "pending";
  readonly started_at: string;
  readonly lease_expires_at: string;
  readonly execution: EdgeExecutionMetadata;
}

export type EdgeReceiptRecord = EdgeReceipt | EdgePendingReceipt;

export interface EdgeReceiptEnvelope {
  readonly receipt: EdgeReceipt;
  readonly replayed: boolean;
}

export const CAPABILITIES: EdgeCapabilitiesDocument = {
  schema_version: EDGE_SCHEMA_VERSION,
  service: "ordivon-edge",
  policy_version: EDGE_POLICY_VERSION,
  capabilities: [
    {
      id: "artifact.put",
      version: CAPABILITY_VERSIONS["artifact.put"],
      state: "ready",
      reason: "Bounded Edge operations can persist private artifacts in R2."
    },
    {
      id: "artifact.get",
      version: CAPABILITY_VERSIONS["artifact.get"],
      state: "ready",
      reason: "Authenticated clients can retrieve validated private artifact keys."
    },
    {
      id: "artifact.delete",
      version: CAPABILITY_VERSIONS["artifact.delete"],
      state: "planned",
      reason: "Deletion remains internal until a receipt-backed deletion contract is added."
    },
    {
      id: "fetch",
      version: CAPABILITY_VERSIONS.fetch,
      state: "ready",
      reason: "Signed requests can execute allowlisted, bounded HTTPS fetches with transactional receipts."
    },
    {
      id: "browser.run",
      version: CAPABILITY_VERSIONS["browser.run"],
      state: "ready",
      reason: "Signed requests can capture allowlisted same-origin browser snapshots with transactional artifacts."
    },
    {
      id: "receipt",
      version: "receipt.v2",
      state: "ready",
      reason: "Pending state, fenced leases, committed receipts, replay, and conflict detection are implemented."
    }
  ]
};
