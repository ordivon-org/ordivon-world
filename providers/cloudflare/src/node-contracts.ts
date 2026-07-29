export const EDGE_NODE_SCHEMA_VERSION = 1 as const;

export type EdgeProfile = "production" | "research" | "adversarial-range";
export type EdgeNodeClass =
  | "worker"
  | "browser"
  | "container"
  | "virtual-machine"
  | "service-emulator"
  | "sensor"
  | "decoy";
export type EdgePlane =
  | "management"
  | "experiment"
  | "observation"
  | "evidence-export";

export interface EdgeProvider {
  readonly id: string;
  readonly kind: "cloudflare-worker" | "local-unshare" | "test";
  readonly location: string;
}

export type EdgeNodeSource =
  | {
      readonly kind: "oci-image";
      readonly reference: string;
      readonly digest: `sha256:${string}`;
    }
  | {
      readonly kind: "source-archive";
      readonly uri: string;
      readonly sha256: string;
    }
  | {
      readonly kind: "worker-version";
      readonly version_id: string;
      readonly source_commit: string;
    }
  | {
      readonly kind: "fixture";
      readonly name: string;
      readonly sha256: string;
    };

export interface EdgeCapabilityBudget {
  readonly wall_time_ms: number;
  readonly actions: number;
  readonly artifact_bytes: number;
}

export interface EdgeNodeCapabilityDescriptor {
  readonly id: string;
  readonly version: string;
  readonly profile: EdgeProfile;
  readonly consequence_scope: "production-allowlist" | "range-local-only";
  readonly planes: readonly EdgePlane[];
  readonly budget: EdgeCapabilityBudget;
}

export interface EdgePolicyRevision {
  readonly id: string;
  readonly sha256: string;
  readonly profile: EdgeProfile;
}

export interface EdgeResourceProfile {
  readonly id: string;
  readonly cpu_millis: number;
  readonly memory_bytes: number;
  readonly storage_bytes: number;
  readonly process_limit: number;
}

export interface EdgeMembership {
  readonly campaign_id: string;
  readonly world_id: string;
  readonly generation: number;
}

export interface EdgeNodeIdentityInput {
  readonly node_class: EdgeNodeClass;
  readonly provider: EdgeProvider;
  readonly source: EdgeNodeSource;
  readonly capability: EdgeNodeCapabilityDescriptor;
  readonly policy_revision: EdgePolicyRevision;
  readonly resource_profile: EdgeResourceProfile;
  readonly membership: EdgeMembership;
  readonly profile: EdgeProfile;
  readonly generation: number;
}

export interface EdgeNodeIdentity {
  readonly schema_version: typeof EDGE_NODE_SCHEMA_VERSION;
  readonly node_id: string;
  readonly digest: string;
  readonly input: EdgeNodeIdentityInput;
}

export type EdgeNodeLifecycleState =
  | "declared"
  | "provisioned"
  | "provision-uncertain"
  | "admitted"
  | "running"
  | "frozen"
  | "evidence-captured"
  | "snapshotted"
  | "retired"
  | "destroy-uncertain"
  | "destroyed";

export type EdgeLifecycleOperation =
  | "provision"
  | "admit"
  | "start"
  | "freeze"
  | "capture"
  | "snapshot"
  | "restore"
  | "retire"
  | "destroy";

export interface EdgeLifecycleOutcome {
  readonly operation_id: string;
  readonly operation: EdgeLifecycleOperation;
  readonly disposition: "applied" | "uncertain" | "rejected";
  readonly state: EdgeNodeLifecycleState;
  readonly reconciliation_required: boolean;
  readonly reason?: string;
}

export interface EdgeLifecycleSnapshot {
  readonly schema_version: typeof EDGE_NODE_SCHEMA_VERSION;
  readonly state: EdgeNodeLifecycleState;
  readonly uncertain?: {
    readonly operation_id: string;
    readonly operation: "provision" | "destroy";
  };
  readonly outcomes: readonly EdgeLifecycleOutcome[];
}

export interface EdgeNodeLease {
  readonly lease_id: string;
  readonly node_id: string;
  readonly generation: number;
  readonly holder: string;
  readonly authority_id: string;
  readonly profile: EdgeProfile;
  readonly issued_at: string;
  readonly expires_at: string;
}

export interface EdgeObservation {
  readonly observation_id: string;
  readonly node_id: string;
  readonly generation: number;
  readonly captured_at: string;
  readonly kind: "stdout" | "stderr" | "exit" | "snapshot" | "lifecycle";
  readonly sha256: string;
  readonly bytes: number;
}

export interface EdgeNodeExecutionReceipt {
  readonly schema_version: typeof EDGE_NODE_SCHEMA_VERSION;
  readonly receipt_id: string;
  readonly node_id: string;
  readonly capability_id: string;
  readonly lease_id: string;
  readonly lease_generation: number;
  readonly status: "succeeded" | "failed" | "rejected";
  readonly started_at: string;
  readonly completed_at: string;
  readonly exit_code?: number;
  readonly observations: readonly EdgeObservation[];
  readonly error_code?: string;
}

export interface EdgeEvidenceArtifact {
  readonly artifact_id: string;
  readonly uri: string;
  readonly node_id: string;
  readonly generation: number;
  readonly sha256: string;
  readonly bytes: number;
  readonly media_type: string;
}

export interface EdgeEvidenceExportReceipt {
  readonly schema_version: typeof EDGE_NODE_SCHEMA_VERSION;
  readonly receipt_id: string;
  readonly node_id: string;
  readonly identity_digest: string;
  readonly generation: number;
  readonly observation_ids: readonly string[];
  readonly artifacts: readonly EdgeEvidenceArtifact[];
  readonly evidence_root_sha256: string;
  readonly exported_at: string;
  readonly direction: "observation-to-evidence";
}

export interface EdgeReconstructionInput {
  readonly name: string;
  readonly kind: "source" | "policy" | "capability" | "resource" | "snapshot";
  readonly sha256: string;
  readonly required: boolean;
}

export interface EdgeReconstructionReceipt {
  readonly schema_version: typeof EDGE_NODE_SCHEMA_VERSION;
  readonly receipt_id: string;
  readonly node_id: string;
  readonly identity_digest: string;
  readonly inputs: readonly EdgeReconstructionInput[];
  readonly inputs_root_sha256: string;
  readonly created_at: string;
}

export interface EdgeProfileAuthority {
  readonly authority_id: string;
  readonly profile: EdgeProfile;
  readonly credential_mode: "none" | "external-profile-scoped";
  readonly credential_scope: string;
  readonly policy_revision_id: string;
}

export interface EdgePlaneBindings {
  readonly management: string;
  readonly experiment: string;
  readonly observation: string;
  readonly evidence_export: string;
}

function canonicalValue(value: unknown): unknown {
  if (
    value === null ||
    typeof value === "string" ||
    typeof value === "boolean"
  ) {
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new Error("canonical JSON rejects non-finite numbers");
    return value;
  }
  if (Array.isArray(value)) return value.map(canonicalValue);
  if (typeof value === "object") {
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) {
      throw new Error("canonical JSON accepts only plain objects");
    }
    return Object.fromEntries(
      Object.entries(value)
        .sort(([left], [right]) => compareCodeUnits(left, right))
        .map(([key, child]) => [key, canonicalValue(child)])
    );
  }
  throw new Error("canonical JSON rejects undefined and non-JSON values");
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(canonicalValue(value));
}

export async function sha256Hex(value: string | Uint8Array): Promise<string> {
  const bytes = typeof value === "string" ? new TextEncoder().encode(value) : value;
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)]
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

export async function edgeNodeIdentity(
  input: EdgeNodeIdentityInput
): Promise<EdgeNodeIdentity> {
  validateIdentityInput(input);
  const serialized = canonicalJson(input);
  const normalized = JSON.parse(serialized) as EdgeNodeIdentityInput;
  const digest = await sha256Hex(serialized);
  return {
    schema_version: EDGE_NODE_SCHEMA_VERSION,
    node_id: `edge-${digest.slice(0, 32)}`,
    digest,
    input: normalized
  };
}

export function validateIdentityInput(input: EdgeNodeIdentityInput): void {
  if (
    input.profile !== input.capability.profile ||
    input.profile !== input.policy_revision.profile
  ) {
    throw new Error("identity profile, capability, and policy revision must match");
  }
  if (
    input.profile === "production" &&
    input.capability.consequence_scope !== "production-allowlist"
  ) {
    throw new Error("production nodes require production-allowlist consequence scope");
  }
  if (
    input.profile !== "production" &&
    input.capability.consequence_scope !== "range-local-only"
  ) {
    throw new Error("disposable nodes require range-local-only consequence scope");
  }
  if (!Number.isSafeInteger(input.generation) || input.generation < 1) {
    throw new Error("node generation must be a positive integer");
  }
  if (
    !Number.isSafeInteger(input.membership.generation) ||
    input.membership.generation < 1
  ) {
    throw new Error("membership generation must be a positive integer");
  }
  if (!/^[a-f0-9]{64}$/.test(input.policy_revision.sha256)) {
    throw new Error("policy revision requires a SHA-256 digest");
  }
  const source = input.source;
  if (
    (source.kind === "fixture" || source.kind === "source-archive") &&
    !/^[a-f0-9]{64}$/.test(source.sha256)
  ) {
    throw new Error("source requires a SHA-256 digest");
  }
  if (
    source.kind === "oci-image" &&
    !/^sha256:[a-f0-9]{64}$/.test(source.digest)
  ) {
    throw new Error("OCI image requires a SHA-256 digest");
  }
  if (
    input.capability.planes.length === 0 ||
    new Set(input.capability.planes).size !== input.capability.planes.length
  ) {
    throw new Error("capability planes must be non-empty and unique");
  }
  const sortedPlanes = [...input.capability.planes].sort(compareCodeUnits);
  if (
    sortedPlanes.some((plane, index) => plane !== input.capability.planes[index])
  ) {
    throw new Error("capability planes must use canonical lexical order");
  }
  for (const [name, value] of Object.entries({
    wall_time_ms: input.capability.budget.wall_time_ms,
    actions: input.capability.budget.actions,
    artifact_bytes: input.capability.budget.artifact_bytes,
    cpu_millis: input.resource_profile.cpu_millis,
    memory_bytes: input.resource_profile.memory_bytes,
    storage_bytes: input.resource_profile.storage_bytes,
    process_limit: input.resource_profile.process_limit
  })) {
    if (!Number.isSafeInteger(value) || value < 1) {
      throw new Error(`${name} must be a positive integer`);
    }
  }
}

function compareCodeUnits(left: string, right: string): number {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

export function validateProfileAuthorities(
  authorities: readonly EdgeProfileAuthority[]
): void {
  const profiles = new Set<EdgeProfile>();
  const authorityIds = new Set<string>();
  const credentialScopes = new Set<string>();
  for (const authority of authorities) {
    if (profiles.has(authority.profile)) {
      throw new Error(`duplicate authority for profile: ${authority.profile}`);
    }
    if (authorityIds.has(authority.authority_id)) {
      throw new Error("authority IDs must not be shared across profiles");
    }
    if (credentialScopes.has(authority.credential_scope)) {
      throw new Error("credential scopes must not be shared across profiles");
    }
    profiles.add(authority.profile);
    authorityIds.add(authority.authority_id);
    credentialScopes.add(authority.credential_scope);
  }
}
