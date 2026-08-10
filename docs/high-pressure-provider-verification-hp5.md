---
schema_version: 1
id: world.hp5-provider-verification
title: High-Pressure Provider and Verification Court HP5
type: decision
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
summary: Destructive provider/verification audit retaining exact cross-owner binding and Browser bundle integrity while demoting Trace Context and moving provider physical truth behind owner-native projections.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
---
# High-Pressure Provider and Verification Court — HP5

HP5 treated the Cloudflare adapter, Browser bundle verifier, Trace Context, World doctor provider checks and the co-located Cloudflare implementation as removable or relocatable. The question was not whether they were implemented well; it was which owner must hold each invariant after deletion, corruption and repository-separation tests.

## Browser integrity survives, but not as root convenience

The deletion candidate skipped `BrowserArtifactBundle` and read each retained Artifact independently through the provider adapter. Every individual body still matched its `ArtifactRef` digest and media type. That thinner path nevertheless accepted three corrupted cross-owner states that the bundle verifier rejected:

- Manifest page facts differed from the provider Receipt while every Artifact digest remained valid;
- the Receipt byte count drifted while the downloaded screenshot still matched its own digest;
- Receipt browser facts drifted from the immutable Manifest while all individual bytes remained valid.

Provider-local tests separately prove that native non-PNG output and unsupported Browser requests are rejected before Artifact commit. These are different boundaries. The provider owns valid generation/commit; World owns the later Receipt ↔ Host ArtifactRef ↔ downloaded bytes ↔ Manifest binding needed to interpret one recovered Browser observation. A later domain/product verifier may decide whether that intact observation satisfies a Task.

`BrowserArtifactBundle` therefore remains a production implementation in `ordivon_world.browser`, but HP5 removes it from the root package facade. Integrity survival does not imply that every verifier helper is a default Agent entry point.

## CloudflareWorldAdapter survives as cross-owner binding

A provider Receipt can be structurally valid yet belong to another consequence. HP5 mutated a valid Fetch Receipt's `request_digest` and `receipt_id`. Both variants remained valid `edge-receipt` documents, but `CloudflareWorldAdapter` rejected them against the exact `PreparedWorldDispatch`.

The surviving responsibility is not generic HTTP transport. It is the exact relation:

```text
Host/World prepared consequence identity
        ↕ exact binding
provider request / Receipt / Artifact identity
```

Removing that relation would force Host to understand Cloudflare-native request digests and Receipt identity, or would allow a structurally valid provider object to be admitted for the wrong prepared consequence. The adapter remains production.

## Trace Context fails the current production court

With and without W3C Trace Context, the same response-loss/fresh-controller scenario produced the same provider request ID, provider request digest, Host request digest, one external POST, UNKNOWN state, exact reconciliation and final Task state. Current Cloudflare structured logs already retain request ID, operation, policy/capability version, Worker identity and lease generation, and do not consume `traceparent`/`tracestate`.

New World dispatches therefore stop authoring and propagating Trace Context. `traceContext` remains an optional legacy field in `world-prepared-dispatch` so already retained pre-HP5 objects can still be decoded and round-tripped without rewriting history. `TraceContext` remains an explicit legacy helper in `ordivon_world.telemetry`, but it is no longer a root facade API or a current effect/reconciliation signal.

## Doctor survives only as an aggregator

Before HP5, World doctor directly read the Cloudflare control credential, called the R2 lifecycle API and independently rebuilt the provider's lifecycle policy. That duplicated an existing provider controller and made World an accidental owner of Cloudflare control-plane truth.

The Cloudflare lifecycle controller now exposes a read-only `--check` projection and its install surface materializes the exact provider policy alongside the controller. World doctor checks source/installed policy digest equality before consuming it. It GETs current provider state, compares it with provider-owned policy, performs no PUT, and returns explicit expected/actual managed rules. World doctor consumes that projection. Likewise capability health comes from the installed owner-native `ordivon-edge capabilities` projection and is validated against the published contract. World doctor no longer reads the Cloudflare control credential or calls the lifecycle API itself.

A live HP5 read proved both owner projections healthy: all four Edge capabilities were `ready`, and R2 lifecycle reported five expected and five actual managed rules with `ok=true`.

## Provider implementation is owner-separated even when co-located

The entire current `providers/cloudflare` subtree was copied into an independent Git root. Its own full CI passed: TypeScript, Worker/state-machine tests, client/release/GC/lifecycle controller tests, policy, operations and Wrangler dry-run. In the opposite direction, the entire provider subtree was temporarily removed from the World workspace; 139 World Python tests and the isolated World wheel gate still passed.

Therefore repository co-location is not a semantic requirement. The Cloudflare Worker, policy, R2 state, deployment/release, lifecycle and GC are provider-owned implementation. They may remain co-located today because it is operationally cheap, but World architecture must not treat their directory location as World authority. A future extraction to another repository is a packaging/deployment decision, not a new World abstraction.

## Private transport duplication

World `SignedHttpTransport` and the provider's `ordivon_edge_client.py` currently implement equivalent HMAC request signing. Three compatibility vectors produced identical Authorization, request ID and timestamp fields; only User-Agent differed. This is real mechanical duplication, but there is not yet a clean provider-client package boundary that lets the World wheel remain self-contained without creating another shared layer. HP5 therefore keeps the World transport private and removes `CloudflareConfig` from the default facade rather than inventing a client manager.

## Surviving HP5 boundary

```text
Provider owner
  Worker / policy / request state / Receipt / Artifact bytes
  deployment / release / lifecycle / GC
  owner-native capability + lifecycle projections
             │
             ▼
World adapter
  exact prepared-dispatch ↔ provider identity binding
  UNKNOWN / reconcile original provider request
  provider evidence → Host Observation/ArtifactRef mapping
  Browser cross-owner bundle integrity
             │
             ▼
Independent domain/product Verification
  whether intact evidence satisfies the Task
```

No ProviderManager, VerificationManager, TraceManager or repository-control abstraction was added.

## Verdicts

- `CloudflareWorldAdapter`: **RETAIN-PRODUCTION** — exact cross-owner binding/reconciliation.
- `BrowserArtifactBundle`: **RETAIN-PRODUCTION, EXPLICIT MODULE** — reproduced integrity failures; not root facade.
- `TraceContext`: **DEMOTE-LEGACY** — no current consequence/recovery value; legacy decode only.
- World doctor: **RETAIN-AGGREGATOR** — consume owner-native provider projections, do not duplicate provider API/control truth.
- `providers/cloudflare`: **PROVIDER-OWNED / EXTRACTABLE / CURRENTLY CO-LOCATED**.
- `CloudflareConfig`: **PRIVATE EXPLICIT MODULE** — not root facade.
- `SignedHttpTransport`: **RETAIN-PRIVATE-MECHANIC** pending a real provider-client packaging need.
- Host `VerificationReceipt`: **KEEP OUTSIDE WORLD CORE** — verification remains a separate semantic action after observation integrity.
