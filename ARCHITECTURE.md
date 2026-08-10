# Architecture

## Purpose

World is the boundary between Host-owned work semantics and independently authoritative environments. The production package contains one provider-adapter shape, three inter-World trajectory shapes, one owner-observed foreign-egress projection and one narrow Agent-facing effect-path comparison shape:

```text
external provider: Bind → Observe → Act → Reconcile
inter-World Resource: Source Egress → Bind → Destination Ingress → Reconcile
inter-World Message: Source Issuance → Bind → Destination Admission → Reconcile
inter-World Entity: Source Departure → Bind Continuity → Destination Materialization → Reconcile
Agent effect-path choice: Owner Observation → Provider-native Evidence → Query → Agent Selection → Owner Revalidation → Act → Reconcile
```

It does not centralize all external systems into one World object. Each owner/provider keeps its native request, operation, currentness, state and error model. World may project a small shared comparison view when two materially different real paths force it, but that projection does not rank candidates, grant action authority or erase provider-native evidence.

## Ownership

| Layer | Owns | Does not own |
|---|---|---|
| Host | Task, Effect, Dispatch, revision fencing, authority, UNKNOWN, Verification, completion | provider execution and remote bytes |
| Harness | model loop, Tool proposal, Provider Call, Tool Step and Run evidence | provider infrastructure truth |
| Runtime | local Workspace, Job, process, cancellation and local Artifacts | remote provider success or domain truth |
| World provider adapter | provider request binding, current capability condition, provider reconciliation, local observation availability and evidence mapping | provider occurrence time, Host admission time, Task strategy, truth, workflow or completion |
| World relationship/capability projection | owner-preserving semantic relationship evidence plus bounded Agent-facing effect-path comparison | physical route/provider control, ranking, implicit selection, current action authority or a global capability registry |
| World Resource Transfer | cross-World transfer identity, source-egress/payload binding, Host-retained uncertainty and destination receipt correlation | source World truth, destination materialization truth, global resource ownership database |
| World Message Delivery | cross-World Message identity, source-issuance/provenance/payload binding, Host-retained uncertainty and destination receipt correlation | source World truth, destination belief/knowledge/world-truth, global Message bus |
| World Entity Migration | cross-World migration identity, source-departure/continuity binding, Host-retained uncertainty and destination receipt correlation | source-local history, portable cognition ownership, destination current Presence, source-authority translation, global Presence database |
| Source domain (Game first) | native source occurrence, egress/departure policy and source-specific evidence | portable cognition ownership, destination admission/materialization |
| Destination domain (Security first) | ingress policy, Resource/Message admission, KVM Entity carrier materialization, physical re-observation/compensation and native-substrate `not_committed` proof | source-domain truth, global Presence truth or cross-relay source authentication unless explicitly configured |
| Cloudflare | Worker execution, R2 request state, lease generation, Receipt, Artifact and deployment identity | Host Task meaning |
| Domain verifier | whether observed external facts satisfy the Task | provider transport or retry |

## Components

```text
src/ordivon_world/
├── cloudflare.py       signed provider transport and adapter
├── browser.py          Browser Receipt/Manifest/Artifact bundle verification
├── foreign_egress.py   Workstation-owned foreign-egress capability projection
├── effect_paths.py     informational Agent-facing effect-path comparison
├── host.py             opaque Host extension persistence
├── resource_egress.py  source-World Resource Egress contract
├── resource_transfer.py durable Resource Transfer / Host journal
├── resource_wire.py    Resource destination wire mapping and failure classification
├── message_delivery.py Message issuance/delivery contracts and Host journal
├── message_wire.py     Message destination wire mapping and failure classification
├── entity_migration.py Entity departure/migration contracts and Host journal
├── entity_wire.py      Entity destination wire mapping and failure classification
├── schemas.py          local Draft 2020-12 Schema Registry
├── telemetry.py        W3C Trace Context validation and propagation
├── doctor.py           repository, installation and live health projection
└── contracts/          packaged provider and Host-facing contracts

providers/cloudflare/
├── src/                Cloudflare Worker
├── scripts/            client, release, lifecycle and GC controllers
├── config/             provider policy authority
└── test/               provider state-machine and operations tests

modules/network-observation/
└── scripts/            private path observation and explicit VPN operations
```

## Dispatch flow

### Preparation

1. Read and validate `/v1/capabilities`.
2. Derive a condition digest from policy, capability, Worker and deployment identity.
3. Validate the provider-local request against packaged JSON Schema.
4. Derive the provider request ID from Host Dispatch, Effect, operation and request digest.
5. Construct a Host `DispatchEnvelope` with the provider request ID as its idempotency key.
6. Persist `PreparedWorldDispatch` in Host CAS before external delivery.

The captured timestamp is excluded from the condition digest. Re-observing identical provider conditions therefore does not invalidate a binding merely because time advanced.

### Delivery

Before POST, the adapter can reread capabilities and compare the exact condition digest. Drift fails before the external action. The provider receives:

- the exact deterministic request ID;
- the canonical request body;
- HMAC authentication;
- optional W3C trace headers and Dispatch correlation for telemetry.

The provider request digest remains provider-native and is verified against the returned Receipt.

### Response loss

```text
Provider commits Receipt and Artifact
→ caller loses response
→ Host records world.outcome-unknown
→ process is replaced
→ fresh Host loads PreparedWorldDispatch from CAS
→ adapter queries /v1/receipts/<original-request-id>
→ no second POST
→ Receipt becomes Host Observation
```

A missing Receipt remains UNKNOWN. It is not proof that no Effect occurred and does not authorize automatic redispatch.

### Observation and verification

World maps provider Artifacts to Host `ArtifactRef` values and the complete provider Receipt to an `ObservationEnvelope` payload digest. Provider success remains an observation. A separate domain or product verifier constructs a Host `VerificationReceipt`; only Host decides whether completion may be proposed or committed.

Cloudflare Receipt `started_at` / `completed_at` remain provider-native times. `WorldObservation.availableAt` is a separate World-owned fact: the instant a validated complete provider observation first becomes available to the World controller. Response loss can therefore produce a real interval between provider completion and World availability. Host's event `recordedAt` remains a third Host-owned admission coordinate and is not copied into World.

These timestamps are not interchangeable. `availableAt` does not mean source occurrence, provider completion, Host admission, Agent read time, truth, freshness or authority. New observations retain it in World CAS; legacy observations without it remain readable with unknown availability. If the same provider receipt is reconciled again, World returns the first retained observation instead of rewriting availability history.

A succeeded Browser operation is a three-Artifact bundle: PNG screenshot, UTF-8 rendered HTML and JSON Manifest. `BrowserArtifactBundle` verifies the shared request ID and lease generation, the Receipt primary Manifest, exact Artifact order and media types, byte counts, SHA-256 values, PNG signature, UTF-8 decoding, and Manifest equality with Receipt execution and page facts. This proves bundle integrity, not that the page content is truthful or satisfies the Task.

## Agent-facing Effect Path Query

W-X3 reproduced the same exact HTTP GET through two materially different owner domains: a Workstation-owned Surfpath foreign-egress relationship and an account-authorized, fixed-target Cloudflare connector. The shared production surface is intentionally a **query projection**, not a generic Capability owner.

```text
provider-native owner observation
        +
provider-native usability evidence
        ↓
EffectPathCandidate
        ↓
EffectPathQuery
        ↓
Agent selects exact candidateDigest
        ↓
activation owner revalidates current state
```

The query preserves `ownerAuthority`, `activationAuthority`, request-control mode, owner observation identity/time, an owner-native validity horizon when one exists, usability evidence and the complete provider-native source projection. `ownerObservation.validUntil` is nullable: Surfpath owns a 180-second freshness law, while the Cloudflare experiment proved only point-in-time control-plane resource state and therefore receives no invented TTL. Every candidate states `currentActionAuthority=false` and `requiresOwnerRevalidation=true`.

A historical successful effect cannot be promoted to current capability. In W-X3, the earlier Cloudflare connector later had no DNS record, Worker route or Worker; a new connector had all three resources present yet initially returned HTTP 522, then the exact same connector completed the OpenAI GET with HTTP 401. Thus owner resource existence, relation usability, historical success and current action authority remain separate coordinates. Deterministic candidate ordering exists only for stable serialization; there is no rank, recommendation or automatic provider routing.

## Host extension trajectory addressing

Host Task identity is not used as the semantic identity of a World extension trajectory. The two production consumers retain independent maps:

```text
worldResourceTransfers[transferId]
worldMessageDeliveries[messageId]
worldDispatches[dispatchId]
```

These maps are Host extension evidence/correlation storage, not an authority system. Host remains authoritative for Effect/Binding/Dispatch admission and Task-level work semantics. World therefore does not infer cross-trajectory concurrency policy from another trajectory being `unknown`.

Entity Migration is also semantically identified by `migrationId`, but 0.4.0 deliberately retains one migration per Task. No real multi-migration Task failure has yet justified another map.

Legacy flat Resource, Message and provider extension state is read as one virtual instance and migrates atomically on the first later mutation.

See [`docs/w2-host-trajectory-addressing.md`](docs/w2-host-trajectory-addressing.md).

## Persistence model

World has no database. Durable state is divided by authority:

- Host CAS/Journal: prepared provider Dispatches plus Resource/Message/Entity plans, source authority receipts, payload/provenance/continuity, uncertainty / `not_committed` proofs and destination receipts;
- R2: provider pending/committed request state, Receipt mirror and Artifact bytes;
- Cloudflare control plane: Worker Version, Deployment, bindings and lifecycle;
- local private storage: release, GC and acceptance receipts;
- systemd and the operating system: installed controller and timer state.

World's Host-backed journals read only the schema-v5 Host extension namespace `world`. A later Host core Event such as `task.context-checkpointed` may become the current Task head without shadowing an outstanding World Provider/Resource/Message/Entity commitment; a fresh World controller reloads the exact `world` namespace together with the current Host `TaskProjection`. This durability boundary does not promote World state into Task meaning or authority. A namespace migrated from Host schema v4 remains legacy/read-only until its owner explicitly recovers the exact legacy digest into native v5 state; World does not claim that Host migration can reconstruct owner state that was already lost before v5.

`WorldTaskInspector` is the bounded read-only projection over that owner state. It is deliberately an aggregator, not a second state model: Provider dispatches project their own bounded request/observation evidence, and the private typed trajectory journal projects Resource, Message and Entity plan/receipt/uncertainty evidence. For retained Provider observations it also projects `temporalEvidence` with provider `started_at` / `completed_at` and World `availableAt`, identifying their separate time sources. The aggregator consumes one revision-coherent `HostExtensionPort.load_namespace_snapshot(..., expected_revision=...)` plus the four owner-local projector interfaces; it never reaches through the Port into `HostStorage`, never decodes trajectory storage fields, and never returns payload, provenance or continuity bodies. Temporal projection does not grant currentness: every result still carries `authority=not-granted-by-inspection` and `externalCurrentness=not-claimed`. There is no OwnerRegistry, universal Observation ontology or shared cross-domain inspection schema.

W5-E fixes the durability fence on the consequence boundary rather than on every Agent decision. `ForeignEgressCapability`, `EffectPathQuery`, one selected `candidateDigest` and the digest-only handoff reference remain informational/planning objects until the activation owner admits an exact effect. If the controller disappears before that admission, current owner reality is re-observed and the Agent may re-query/re-select. Persisting the old selection would be unsafe because owner freshness may expire and physical path identity may change. Once a typed provider/transfer operation is prepared or dispatched, its retained World journal becomes durable because an external consequence may already exist and UNKNOWN must be reconciled before retry.

```text
Observe → Query → Select     recomputable planning
                 │
                 ▼
        owner admits exact consequence
                 │
          durability fence
                 │
                 ▼
       Prepared / Dispatched / Bound
                 │
          Receipt | UNKNOWN
                 │
              Reconcile
```

This is why World has no separate capability-selection or generic commitment journal. Fresh-Agent recovery projects the existing typed owner journals instead of copying planning state into another database.

W-X4 extends the same ownership rule across physical execution mobility. Runtime may execute one semantic objective through different target/provider contracts while retaining exact Workspace/Job/Attempt/source/Artifact lineage and opaque foreign references. World does not translate those physical facts into a shared execution model. Before a new consequence is admitted in the destination execution context, current external capability is observed again. If an external consequence crossed its owner-admission fence before migration, the destination controller restores the exact World prepared identity and reconciles it before any new dispatch.

```text
Host Task
   │ semantic continuity
   ├──────────────┐
   ▼              ▼
Runtime A       Runtime B
physical       physical
lineage        lineage
   │              │
   └──────┬───────┘
          ▼
     World planning       recompute before admission
          │
     owner admission
          │
     Receipt | UNKNOWN    durable exact effect identity
          │
       Reconcile
```

Runtime `foreignReferences` are identity/correlation commitments, not Artifact transport. Likewise, a shared canonical Git revision is not evidence that an external immutable input was materialized for every target. W-X4 physically found that current Windows-native Runtime admission cannot consume `workspace.execBound`; that is a Runtime substrate requirement rather than justification for a World filesystem, byte-transfer or execution-migration manager.

## Contract boundary

JSON Schema Draft 2020-12 is the machine-readable authority for public provider, Effect Path Query, Resource Transfer, Message Delivery and Entity Migration surfaces. The Effect Path Query schema standardizes only the informational comparison wrapper; provider-native evidence remains embedded rather than translated into one generic capability ontology. TypeScript emits real provider fixture documents; Python validates contracts using a local packaged Registry, so offline recovery never retrieves a remote Schema URL.

See [`docs/contracts.md`](docs/contracts.md) and [`docs/compatibility.md`](docs/compatibility.md).

## Deliberately absent

World does not currently contain:

- a daemon or database;
- a universal `WorldInteraction` record;
- automatic provider or network routing;
- a global capability registry, generic Capability owner or automatic candidate ranker;
- callbacks, queues or fan-out/join orchestration;
- a general MCP, RAG or connector platform;
- a Sandbox or code-execution runtime;
- domain verification logic.

A new shared abstraction requires two materially different workloads, two real consumers and a reproduced failure that direct Host plus provider adapters cannot own cleanly.
