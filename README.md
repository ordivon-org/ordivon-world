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
updated: 2026-08-10
summary: Owner-preserving external relationships, temporally explicit provider observations, recoverable effects and cross-World transfers, with Agent-facing choice that never becomes action authority.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.authority
  - world.boundaries
---
# Ordivon World

Ordivon World connects Host-owned work to independently authoritative environments. The released production boundary centers on the direct external-provider seam, three language-neutral inter-World trajectories (Resource Transfer, Message Delivery and Entity Migration), bounded owner inspection and narrow temporal provenance. W-X1/W-X3 foreign-egress/effect-path laws remain historical research evidence, but HP8 removes their executable Python APIs and packaged contracts after HP4 failed to prove a fresh-Agent decision advantage.

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

World is a repository and adapter boundary. It is **not** a World daemon, workflow engine, provider broker, general connector platform, network control plane, Sandbox service, Task database, or completion authority. HP0–HP8 are now closed for the current evidence; there is no numbered next foundation stage. New World work starts from a reproduced workload/failure.

## Start here

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — ownership and execution flow.
- [`STATUS.md`](STATUS.md) — what is implemented, deployed, verified, or still pending.
- [`docs/operations.md`](docs/operations.md) — setup, doctor, GC, deployment and recovery.
- [`docs/contracts.md`](docs/contracts.md) — JSON Schema, deterministic identities and Host mapping.
- [`docs/verification.md`](docs/verification.md) — deterministic, provider and live-system gates.
- [`docs/high-pressure-provider-verification-hp5.md`](docs/high-pressure-provider-verification-hp5.md) — HP5 provider/verification ownership and deletion court.
- [`docs/high-pressure-survival-hp6-hp8.md`](docs/high-pressure-survival-hp6-hp8.md) — final knowledge-GC, chaos and Minimal World tournament closeout.
- [`docs/research-closeouts.md`](docs/research-closeouts.md) — compact laws/evidence index for closed W4/W5/Sense-Connect-Act research.
- [`SECURITY.md`](SECURITY.md) and [`docs/data-and-privacy.md`](docs/data-and-privacy.md) — trust and data boundaries.
- [`docs/authority.md`](docs/authority.md) — which source owns each fact.
- [`docs/retained-boundaries.md`](docs/retained-boundaries.md) — why the active scope remains narrow.

## Active capabilities

### Closed relationship/effect-path research

W-X1/W-X3 established that capability/path evidence is owner-, path- and time-scoped, but HP4 failed to show fresh-Agent decision advantage from the executable `ForeignEgressCapability` / `EffectPathQuery` projection layer. HP8 therefore removes those research-only Python APIs and packaged contracts from the product package. The accepted laws, counterexamples and immutable evidence remain in [`docs/research-closeouts.md`](docs/research-closeouts.md) and `evidence/acceptance/`. Reopening requires a new real consumer failure.

### External commitment continuity

W5-E tested whether Agent path choice itself needs another durable World journal. A historical Surfpath reference remained structurally intact after expiry, but the Workstation owner rejected it before the child effect. Fresh rediscovery of the same logical `jp-tok / openvpn-udp` intent produced new observation, path and capability identities; an exact new reference was then revalidated and reached OpenAI with HTTP 401.

The retained law is that pre-admission observation/query/selection is recomputable planning state. World durability begins when an owner admits an exact consequence-capable operation whose outcome may later be Receipt or UNKNOWN. Those durable boundaries already exist in the typed Provider, Resource, Message and Entity journals and are discoverable through `WorldTaskInspector`; no `CapabilityManager`, selection journal or generic commitment registry is required. See [`docs/research-closeouts.md`](docs/research-closeouts.md#external-commitment-continuity); the full experiment is historical under `docs/archive/research/`.

### Execution mobility

W-X4 moved one Host-correlated objective across Runtime `local_linux` and `windows_native` Jobs. Runtime terminal evidence kept target/provider/Job/Artifact lineage exact while both targets independently verified the same canonical source bytes. World did not gain process, filesystem or execution-target ownership.

The post-admission half then split one Cloudflare Effect across fresh Runtime controller workspaces: the source controller freshly observed provider capability, emitted one POST, lost the committed response and durably entered UNKNOWN; the destination controller restored the original prepared dispatch and reconciled the exact provider request with zero recovery POSTs. A fresh execution context did not become authority to repeat an old consequence.

One physical gap remains outside World: current Runtime `windows_native` cannot use the `workspace.execBound` immutable external-input path because that path requires `contained_local` while Windows-native currently supports `trusted_local`. World deliberately does not implement a byte-copy compatibility layer. See [`docs/research-closeouts.md`](docs/research-closeouts.md#execution-mobility); the full experiment is historical under `docs/archive/research/`.

### Temporal provider observations

Cloudflare provider Receipts retain provider-native `started_at` / `completed_at`. World `WorldObservation` separately records `availableAt`: when the complete provider observation first becomes available to the World controller. `WorldTaskInspector` projects both time sources without treating either as current external truth or action authority.

P2 was forced by a real response-loss experiment: one fresh Cloudflare Fetch completed at `07:04:39.956Z`, while the reconciled observation first became available to World at `07:04:51.422995Z` after a deliberate delay; Host admitted the evidence milliseconds later. Raw Host revision history could recover admission time, but the prior World observation and Agent-facing projection could not. World therefore added one availability coordinate rather than a generic temporal ontology. Provider time, World availability time and Host event time remain owned by their respective layers.

`availableAt` is not truth time, source-occurrence time, Host admission time or Agent read time. Historical observations lacking it remain structurally readable; new Cloudflare observations emit it, and repeated reconciliation preserves the first retained availability rather than rewriting history.

### Cross-World Resource Transfer

The Python package exposes `ResourceEgressReceipt`, `ResourceTransferBundle`, `HostResourceTransferJournal`, `ResourceTransferWireDestination` and the packaged Resource JSON contracts. The first production trajectory is Station Zero Game → Security SampleVault.

The source World must first issue an exact `ResourceEgressReceipt`; the destination then independently admits/materializes the transfer. A response loss remains UNKNOWN until the original destination operation is reconciled. A destination-authored, identity-bound `not_committed` proof may release UNKNOWN back to PREPARED for the exact original retry.

The current Security CLI trusts its local caller to carry an authentic source-authority receipt. Untrusted-relay deployments require independent source-authority authentication; World does not claim a universal PKI. See [`docs/w2-resource-transfer-production.md`](docs/w2-resource-transfer-production.md).

A Host Task may retain multiple Resource trajectories addressed by `transferId`. A Task with multiple trajectories requires explicit selection; implicit ambiguous lookup fails closed.

### Cross-World Message Delivery

The Python package exposes `MessageIssuanceReceipt`, `MessageDeliveryBundle`, `HostMessageDeliveryJournal`, `MessageDeliveryWireDestination` and the packaged Message JSON contracts. The first production trajectory is Station Zero Game → Security durable Message inbox.

Game issues a Message only from a retained Fact visible to the issuing faction. Security independently admits the exact Message as management-classified information. Delivery does **not** promote the foreign claim into destination knowledge or world-truth. Response loss remains UNKNOWN until the original Message is reconciled; a destination-authored `not_committed` proof can release only that exact UNKNOWN Message for one exact original retry.

A Host Task may retain multiple Message trajectories addressed by `messageId`. Pre-W2 flat Message state remains recoverable and migrates atomically on the first later mutation. See [`docs/w2-message-delivery-production.md`](docs/w2-message-delivery-production.md).

The Message experiments did not force a first-class `WorldLink`: authenticated endpoint discovery and destination identity were sufficient across endpoint replacement, process/socket rematerialization and endpoint relocation.

### Cross-World Entity Migration

The Python package exposes `EntityDepartureReceipt`, `EntityMigrationBundle`, `HostEntityMigrationJournal`, `EntityMigrationWireDestination` and the packaged Entity Migration JSON contracts. The first production trajectory is Station Zero Game verified departure → Security Windows KVM continuity carrier.

Game owns only source Presence departure; opaque continuity is retained by Host and delivered to the destination. Security durably binds the migration before native launch, stages continuity on an `ORDIVON_MIG` FAT volume, and uses KVM/QMP/native evidence rather than Guest self-report as materialization authority. The accepted first deployment is a trusted local owner-originated caller: a fresh Game process re-read the exact departure authority before World transported it, while Security still declares `sourceAuthorityAuthentication=caller-trust-boundary`.

Migration `not_committed` is stronger than receipt absence. Provably body-free abandoned staging or TPM-only preparation may be compensated to zero residuals and released only with `nativeSubstrateChecked=true` plus `exactOriginalRetrySafe=true`; ambiguous QEMU launch evidence remains UNKNOWN. Recovery never rewrites the historical predecessor owner. A historical migration receipt does not claim current live Presence, and this profile does not authenticate Game authority through an untrusted relay. See [`docs/w2-entity-migration-production.md`](docs/w2-entity-migration-production.md).

Entity Migration remains one migration per Host Task in 0.4.0. No real workload has yet forced multi-migration Task addressing, Guest cognition activation, a global Presence database, or a first-class `WorldLink`.

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
- multiple provider trajectories per Host Task, addressed by Host `dispatchId`;
- backward recovery/migration for pre-0.2.1 flat provider extension state;
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

Cloudflare remains authoritative for Worker execution, R2 state, provider versions and provider Receipts. HP5 proved that this provider subtree can pass its full CI as an independent Git root while the World Python package/wheel passes with the subtree absent. Co-location is therefore an operational convenience, not World ownership; the provider implementation is owner-separated and extractable.

### Network condition tools

[`modules/network-observation/`](modules/network-observation/) retains workstation-specific WireGuard and Surfshark tools. They report or explicitly alter operator-controlled network conditions. They do not automatically select routes or grant an Agent network mutation authority.

## Core rules

1. **Native owners keep authority.** Source Worlds own egress/departure facts, destination Worlds own ingress/materialization facts, and Host owns Task/uncertainty continuity.
2. **Provider owns provider truth.** World maps exact provider identities and evidence; it does not reinterpret a successful provider response as Task completion.
3. **Reconcile before redispatch.** A lost response creates UNKNOWN. Recovery queries the original provider request before another external action is considered.
4. **Conditions are explicit.** A Dispatch binds the capability condition on which it relies. Drift fences the old binding.
5. **Telemetry is not evidence.** Trace headers help operations but do not replace durable request identity, Receipt, Artifact digest or Host CAS.
6. **Trust is explicit.** Structural receipts do not magically authenticate a source across an untrusted relay.
7. **Task identity is not trajectory identity.** Trajectories retain native semantic identity (`transferId` / `messageId` / `migrationId` / `dispatchId`). Resource, Message and provider paths use per-ID maps after real multi-trajectory failures; Entity Migration remains one-per-Task until such a failure exists.
8. **Share views before sharing ownership.** W-X3 proved that a narrow shared projection can preserve provider-native evidence without transferring ownership; HP4 then showed that such a projection still has to prove Agent decision value before becoming a default product surface. Physical owners revalidate before effect.
9. **Keep time sources separate.** Provider occurrence/completion time, World observation availability and Host admission time are different owner-native facts. Availability is not truth, currentness, authority or completion.
10. **Persist consequences, not every choice.** Owner observations, effect-path queries and pre-admission Agent selections may be recomputed from current reality. Durable World continuity begins at owner admission of an exact consequence-capable operation; after that fence, Receipt/UNKNOWN/reconciliation must survive controller replacement.
11. **Move lineage by owner, not by abstraction.** Host semantic Task identity, Runtime execution/input/Artifact lineage and World external-effect state remain separate through execution migration. A new execution target re-observes pre-admission World reality; already-admitted consequences retain exact identity and reconcile before retry.

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
