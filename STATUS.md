# Status

## Current release line

Repository package version: `0.4.0`.

Ordivon World is an operational owner-preserving adapter/trajectory boundary for the currently admitted provider and cross-World workloads. It is not a standalone World service or a global source of external truth.

The active production surface consists of:

- direct Host-facing Cloudflare Fetch/Browser exact binding and response-loss reconciliation;
- Browser screenshot/rendered-HTML/Manifest bundle verification;
- temporally explicit provider observations with separate provider and World availability coordinates;
- production Resource Transfer, Message Delivery, and Entity Migration contracts;
- bounded read-only owner inspection through `WorldTaskInspector`;
- owner-native doctor aggregation and operator-scoped network condition tools.

The co-located Cloudflare Worker/operations subtree remains provider-owned and independently extractable. Foreign-egress/effect-path projection APIs and other research-only shared layers were removed from the product after high-pressure deletion tests failed to justify them as default Agent surfaces.

## Current capability matrix

| Capability | State | What it proves |
| --- | --- | --- |
| Cloudflare Fetch / Browser adapter | operational and live-verified | exact provider binding, one-request recovery, provider Receipt/Artifact mapping; not Task completion |
| Browser Artifact bundle | retained production module | cross-Artifact/Receipt/Manifest integrity; not page truth or Task satisfaction |
| Resource Transfer | production contract | exact source-egress → destination-ingress trajectory with UNKNOWN recovery; not global resource ownership |
| Message Delivery | production contract | exact issuance/delivery trajectory with UNKNOWN recovery; not destination knowledge or belief |
| Entity Migration | production contract | source departure + destination carrier materialization/recovery under the accepted trust profile; not current global Presence |
| temporal provider observation | verified narrow provenance | provider start/completion and World `availableAt` remain separate owner-native times; no generic temporal ontology |
| WorldTaskInspector | verified read-only projection | revision-coherent retained commitment inspection; no action authority or external currentness |
| World doctor | operational | aggregates owner-native repository/machine/provider health; does not become provider control-plane authority |
| network condition tools | operational, operator-scoped | observe or explicitly alter operator-controlled paths; no automatic routing authority |

## Stable laws retained from research

The large W/HP/Sense–Connect–Act research programme has been contracted into a smaller set of current laws:

- native providers and domains retain occurrence/current-state authority;
- historical truth and currentness are distinct;
- response loss is `UNKNOWN` until the original external identity is reconciled;
- pre-admission discovery/selection is generally recomputable; durable World continuity begins at exact consequence admission;
- transport delivery does not imply destination cognition;
- source and destination semantics remain different even when trajectory recovery skeletons resemble one another;
- provider time, World availability time, and Host admission time are not interchangeable;
- structural provenance is not a universal authentication mechanism;
- new execution contexts do not authorize replay of old admitted consequences;
- a narrow shared projection still has to prove decision value before becoming a default product surface.

Exact experiments, receipts, counterexamples, and reopening conditions remain in [`docs/research-closeouts.md`](docs/research-closeouts.md), [`docs/high-pressure-survival-hp6-hp8.md`](docs/high-pressure-survival-hp6-hp8.md), and the archived research tree.

## Known limits

- World has no independent daemon or database; durable typed trajectory state is retained through Host extension state and owner/provider systems.
- Current production Resource/Message/Entity integrations use explicit trust profiles and do not claim universal source authentication through an untrusted relay.
- Entity Migration remains one migration per Host Task in `0.4.0`; no real multi-migration failure has justified a map yet.
- `WorldTaskInspector` is World-local and does not establish a generic cross-domain Observation or Owner registry.
- Historical receipts cannot establish current Presence, reachability, capability, or provider state without applicable owner-native re-observation.
- Network observation tools do not automatically choose or activate routes for an Agent.
- World does not own Runtime execution migration or immutable-input transport. Runtime now supports exact immutable-input materialization on both admitted execution targets within its proven target-specific authority boundaries; future physical execution/input gaps remain Runtime/Workstation responsibilities.
- Provider success remains evidence for later Host/domain verification, not automatic completion.

## Live state is owner-native

This page does not own current deployment health, provider versions, R2 state, installed controller digests, network state, active Host Tasks, or current external Presence. Query the systems that own those facts.

Repository-only health:

```bash
uv run ordivon-world-doctor --repo . --offline
```

Live machine/provider health:

```bash
uv run ordivon-world-doctor --repo /root/projects/ordivon-world
```

Cloudflare health, capability, Receipt, Artifact, deployment, and lifecycle facts remain provider-native. Host Task/Dispatch/Verification facts remain Host-native. Local network facts remain operating-system/operator-native.

## Verification

For repository changes:

```bash
uv sync --locked
cd providers/cloudflare && pnpm install --frozen-lockfile && cd ../..
scripts/local-acceptance
```

External-effect or provider changes additionally require the live acceptance/doctor gates documented in [`docs/verification.md`](docs/verification.md) and [`docs/operations.md`](docs/operations.md). CI cannot claim live provider or machine health.

## Reopen conditions

Reopen the active World boundary when a current workload demonstrates one of the following:

- direct Host + provider/domain composition cannot preserve an external consequence correctly;
- a third materially different consumer forces a shared relation/Presence/interaction contract that current typed owner paths cannot express;
- independent source authentication is required across an untrusted relay;
- current trajectory addressing fails under real multi-trajectory use;
- Agent decisions repeatedly fail because a removed shared projection provides information that owner-native evidence cannot supply compactly;
- a provider/domain ownership change invalidates the current authority map.

Research history alone is not a reopening condition.
