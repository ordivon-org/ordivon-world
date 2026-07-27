export const EDGE_SCHEMA_VERSION = 1 as const;

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
  readonly state: CapabilityState;
  readonly reason: string;
}

export interface EdgeCapabilitiesDocument {
  readonly schema_version: typeof EDGE_SCHEMA_VERSION;
  readonly service: "ordivon-edge";
  readonly capabilities: readonly EdgeCapability[];
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
  readonly artifact?: ArtifactReference;
  readonly artifacts?: readonly ArtifactReference[];
  readonly fetch?: FetchReceiptDetails;
  readonly browser?: BrowserReceiptDetails;
  readonly error_code?: string;
}

export interface EdgeReceiptEnvelope {
  readonly receipt: EdgeReceipt;
  readonly replayed: boolean;
}

export const CAPABILITIES: EdgeCapabilitiesDocument = {
  schema_version: EDGE_SCHEMA_VERSION,
  service: "ordivon-edge",
  capabilities: [
    {
      id: "artifact.put",
      state: "ready",
      reason: "Bounded Edge operations can persist private artifacts in R2."
    },
    {
      id: "artifact.get",
      state: "ready",
      reason: "Authenticated clients can retrieve validated private artifact keys."
    },
    {
      id: "artifact.delete",
      state: "planned",
      reason: "Deletion remains internal until a receipt-backed deletion contract is added."
    },
    {
      id: "fetch",
      state: "ready",
      reason: "Signed requests can execute allowlisted, bounded HTTPS fetches with R2 receipts."
    },
    {
      id: "browser.run",
      state: "ready",
      reason: "Signed requests can capture allowlisted same-origin browser snapshots with bounded artifacts."
    },
    {
      id: "receipt",
      state: "ready",
      reason: "Receipt schema v1, idempotency locks, replay, and conflict detection are implemented."
    }
  ]
};
