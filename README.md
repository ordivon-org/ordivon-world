---
schema_version: 1
id: world.start
title: Ordivon World
type: start
profile: organization
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - builder
  - operator
  - agent
updated: 2026-08-04
summary: Recoverable external-provider adapters plus a production cross-World Resource Transfer contract with explicit source-egress and destination-ingress authority.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.authority
  - world.boundaries
---
# Ordivon World

Ordivon World connects Host-owned work to independently authoritative environments. The released package retains the direct external-provider adapter path and now also exposes one production inter-World trajectory: Resource Transfer with source-egress authority, destination-ingress authority and durable uncertainty recovery.

```text
Host Task / Effect / Dispatch
        ↓
World provider adapter
        ↓
external provider request / operation
        ↓
Receipt / Artifact / condition observation
        ↓
Host Observation / independent Verification
```

World is a repository and adapter boundary. It is **not** a World daemon, workflow engine, provider broker, general connector platform, network control plane, Sandbox service, Task database, or completion authority.

## Start here

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — ownership and execution flow.
- [`STATUS.md`](STATUS.md) — what is implemented, deployed, verified, or still pending.
- [`docs/operations.md`](docs/operations.md) — setup, doctor, GC, deployment and recovery.
- [`docs/contracts.md`](docs/contracts.md) — JSON Schema, deterministic identities and Host mapping.
- [`docs/verification.md`](docs/verification.md) — deterministic, provider and live-system gates.
- [`SECURITY.md`](SECURITY.md) and [`docs/data-and-privacy.md`](docs/data-and-privacy.md) — trust and data boundaries.
- [`docs/authority.md`](docs/authority.md) — which source owns each fact.
- [`docs/retained-boundaries.md`](docs/retained-boundaries.md) — why the active scope remains narrow.

## Active capabilities

### Cross-World Resource Transfer

The Python package exposes `ResourceEgressReceipt`, `ResourceTransferBundle`, `HostResourceTransferJournal`, `ResourceTransferWireDestination` and the packaged Resource JSON contracts. The first production trajectory is Station Zero Game → Security SampleVault.

The source World must first issue an exact `ResourceEgressReceipt`; the destination then independently admits/materializes the transfer. A response loss remains UNKNOWN until the original destination operation is reconciled. A destination-authored, identity-bound `not_committed` proof may release UNKNOWN back to PREPARED for the exact original retry.

The current Security CLI trusts its local caller to carry an authentic source-authority receipt. Untrusted-relay deployments require independent source-authority authentication; World 0.2 does not claim a universal PKI. See [`docs/w2-resource-transfer-production.md`](docs/w2-resource-transfer-production.md).

### Host-facing Cloudflare adapter

The Python package in `src/ordivon_world/` provides:

- current Cloudflare capability snapshots;
- deterministic Dispatch-to-provider request identity;
- Fetch and Browser Snapshot request construction;
- pre-dispatch capability-condition fencing;
- response-loss reconciliation by the original provider request ID;
- Cloudflare Receipt and R2 Artifact mapping into Host `ObservationEnvelope` and `ArtifactRef` values;
- Browser screenshot, rendered HTML and Manifest bundle verification across Receipt, Host evidence and downloaded bytes;
- Host CAS/Journal persistence through `HostWorldExtension`;
- W3C Trace Context propagation as non-authoritative telemetry.

The public package depends on exact remote-reachable Host and Protocol revisions. It does not copy Host Task semantics into World.

### Cloudflare provider

[`providers/cloudflare/`](providers/cloudflare/) contains the TypeScript Worker and operator controllers for:

- bounded HTTPS Fetch;
- bounded Browser Rendering snapshots;
- private R2 Artifacts;
- pending and committed request state;
- generation-fenced leases;
- replay and idempotency conflict detection;
- release, rollback, lifecycle and deferred garbage collection.

Cloudflare remains authoritative for Worker execution, R2 state, provider versions and provider Receipts.

### Network condition tools

[`modules/network-observation/`](modules/network-observation/) retains workstation-specific WireGuard and Surfshark tools. They report or explicitly alter operator-controlled network conditions. They do not automatically select routes or grant an Agent network mutation authority.

## Core rules

1. **Native owners keep authority.** Source Worlds own egress facts, destination Worlds own ingress/materialization facts, and Host owns Task/uncertainty continuity.
2. **Provider owns provider truth.** World maps exact provider identities and evidence; it does not reinterpret a successful provider response as Task completion.
3. **Reconcile before redispatch.** A lost response creates UNKNOWN. Recovery queries the original provider request before another external action is considered.
4. **Conditions are explicit.** A Dispatch binds the capability condition on which it relies. Drift fences the old binding.
5. **Telemetry is not evidence.** Trace headers help operations but do not replace durable request identity, Receipt, Artifact digest or Host CAS.
6. **Trust is explicit.** Structural receipts do not magically authenticate a source across an untrusted relay.
7. **No universal abstraction without proof.** A second provider or workload may share a small contract only after a real duplicated failure demonstrates the need.

## Development

```bash
uv sync --locked
cd providers/cloudflare && pnpm install --frozen-lockfile && cd ../..
scripts/local-acceptance
```

Repository-only health:

```bash
uv run ordivon-world-doctor --repo . --offline
```

Live machine and provider health:

```bash
uv run ordivon-world-doctor --repo /root/projects/ordivon-world
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing an external action, request identity, Receipt, Artifact, retention or recovery contract.
