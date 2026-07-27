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
}

export interface EdgeReceipt {
  readonly schema_version: typeof EDGE_SCHEMA_VERSION;
  readonly receipt_id: string;
  readonly operation: EdgeOperation;
  readonly status: ReceiptStatus;
  readonly started_at: string;
  readonly completed_at: string;
  readonly artifact?: ArtifactReference;
  readonly error_code?: string;
}

export const CAPABILITIES: EdgeCapabilitiesDocument = {
  schema_version: EDGE_SCHEMA_VERSION,
  service: "ordivon-edge",
  capabilities: [
    {
      id: "artifact.put",
      state: "ready",
      reason: "The production Worker is bound to the private Ordivon R2 artifact bucket."
    },
    {
      id: "artifact.get",
      state: "ready",
      reason: "Artifact reads are owned by the Edge storage adapter; no public route is exposed yet."
    },
    {
      id: "artifact.delete",
      state: "ready",
      reason: "Artifact deletion is available to internal adapters after authentication is designed."
    },
    {
      id: "fetch",
      state: "planned",
      reason: "Bounded external fetch requires an allow policy, response limits, and receipt persistence."
    },
    {
      id: "browser.run",
      state: "planned",
      reason: "Browser Run requires an explicit binding, budgets, and artifact output policy."
    },
    {
      id: "receipt",
      state: "ready",
      reason: "Receipt schema v1 is implemented independently from transport and HTTP exposure."
    }
  ]
};
