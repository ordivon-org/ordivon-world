# Architecture

## Purpose

World is the boundary between Host-owned work semantics and independently authoritative environments. The production package now contains one provider-adapter shape and three inter-World trajectory shapes:

```text
external provider: Bind → Observe → Act → Reconcile
inter-World Resource: Source Egress → Bind → Destination Ingress → Reconcile
inter-World Message: Source Issuance → Bind → Destination Admission → Reconcile
inter-World Entity: Source Departure → Bind Continuity → Destination Materialization → Reconcile
```

It does not centralize all external systems into one World object. Each provider keeps its native request, operation, state and error model. World retains only the facts required to bind those provider facts to one Host Dispatch and continue the Task safely.

## Ownership

| Layer | Owns | Does not own |
|---|---|---|
| Host | Task, Effect, Dispatch, revision fencing, authority, UNKNOWN, Verification, completion | provider execution and remote bytes |
| Harness | model loop, Tool proposal, Provider Call, Tool Step and Run evidence | provider infrastructure truth |
| Runtime | local Workspace, Job, process, cancellation and local Artifacts | remote provider success or domain truth |
| World provider adapter | provider request binding, current capability condition, provider reconciliation and evidence mapping | Task strategy, workflow or completion |
| World Resource Transfer | cross-World transfer identity, source-egress/payload binding, Host-retained uncertainty and destination receipt correlation | source World truth, destination materialization truth, global resource ownership database |
| World Message Delivery | cross-World Message identity, source-issuance/provenance/payload binding, Host-retained uncertainty and destination receipt correlation | source World truth, destination belief/knowledge/world-truth, global Message bus |
| World Entity Migration | cross-World migration identity, source-departure/continuity binding, Host-retained uncertainty and destination receipt correlation | source-local history, portable cognition ownership, destination current Presence, global Presence database |
| Source domain (Game first) | native source occurrence, egress/departure policy and source-specific evidence | portable cognition ownership, destination admission/materialization |
| Destination domain (Security first) | ingress policy, Resource/Message admission, KVM Entity carrier materialization and native-substrate `not_committed` proof | source-domain truth, global Presence truth or cross-relay source authentication unless explicitly configured |
| Cloudflare | Worker execution, R2 request state, lease generation, Receipt, Artifact and deployment identity | Host Task meaning |
| Domain verifier | whether observed external facts satisfy the Task | provider transport or retry |

## Components

```text
src/ordivon_world/
├── cloudflare.py       signed provider transport and adapter
├── browser.py          Browser Receipt/Manifest/Artifact bundle verification
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

A succeeded Browser operation is a three-Artifact bundle: PNG screenshot, UTF-8 rendered HTML and JSON Manifest. `BrowserArtifactBundle` verifies the shared request ID and lease generation, the Receipt primary Manifest, exact Artifact order and media types, byte counts, SHA-256 values, PNG signature, UTF-8 decoding, and Manifest equality with Receipt execution and page facts. This proves bundle integrity, not that the page content is truthful or satisfies the Task.

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

## Contract boundary

JSON Schema Draft 2020-12 is the machine-readable authority for public provider, Resource Transfer, Message Delivery and Entity Migration request/response surfaces. TypeScript emits real fixture documents; Python validates them using a local packaged Registry, so offline recovery never retrieves a remote Schema URL.

See [`docs/contracts.md`](docs/contracts.md) and [`docs/compatibility.md`](docs/compatibility.md).

## Deliberately absent

World does not currently contain:

- a daemon or database;
- a universal `WorldInteraction` record;
- automatic provider or network routing;
- callbacks, queues or fan-out/join orchestration;
- a general MCP, RAG or connector platform;
- a Sandbox or code-execution runtime;
- domain verification logic.

A new shared abstraction requires two materially different workloads, two real consumers and a reproduced failure that direct Host plus provider adapters cannot own cleanly.
