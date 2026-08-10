---
schema_version: 1
id: world.authority
title: World Content Authority
type: decision
profile: organization
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - operator
  - agent
updated: 2026-08-10
summary: Authority map for Host-facing World bindings, provider and World observation timing, Cloudflare provider truth, network operator state, operational health and archived experiments.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.start
  - world.boundaries
---
# World Content Authority

## Repository facts

- [`../README.md`](../README.md) is the public entry and scope summary.
- [`../ARCHITECTURE.md`](../ARCHITECTURE.md) owns component responsibilities and execution flow.
- [`../STATUS.md`](../STATUS.md) owns current maturity and known limits.
- [`retained-boundaries.md`](retained-boundaries.md) owns deletion and reactivation decisions.
- [`contracts.md`](contracts.md) owns adapter contract and identity semantics.
- [`compatibility.md`](compatibility.md) owns supported revisions and migration expectations.
- [`operations.md`](operations.md) owns current commands and recovery procedures.
- [`verification.md`](verification.md) owns evidence interpretation and gates.
- [`research-closeouts.md`](research-closeouts.md) is the current authority for **closed** W4/W5/Sense-Connect-Act laws, evidence locators and reopening conditions. The full studies live under [`archive/research/`](archive/research/) as historical research and cannot compete with current product truth.
- [`high-pressure-survival-hp6-hp8.md`](high-pressure-survival-hp6-hp8.md) owns the final HP-series contraction decision: knowledge GC, mixed-chaos result, removal of the research-only Foreign Egress / Effect Path executable surfaces, and the demand-triggered reopening rule.

Executable source, locked dependencies and machine-readable Schemas are stronger than prose when a discrepancy exists.

## Host-facing facts

Host remains authoritative for Task, Effect, Dispatch, Task revision, Ready Frontier, authority, UNKNOWN, Verification and completion. World owns only the extension objects and events it emits:

```text
world.dispatch-prepared
world.outcome-unknown
world.dispatch-observed
```

`PreparedWorldDispatch` and `WorldObservation` are World-owned CAS schemas embedded in Host storage. Host owns their admission order and revision fence. `WorldObservation.availableAt` is World-owned observation-availability evidence; the `world.dispatch-observed` Event recorded time remains Host-owned admission evidence and is not copied into the World object. A World object cannot alter Task meaning merely because it is stored by Host.

`WorldTaskInspector` is informational projection authority only for World-owned retained commitments. Host owns the exact Task/namespace revision fence and opaque namespace metadata through `HostExtensionPort.load_namespace_snapshot()`; each World family interprets only its own retained fields, and the aggregator combines those bounded projections without reading Host storage directly. Retained provider observations may expose `temporalEvidence` containing provider Receipt times plus World `availableAt`; those time sources do not grant action authority or external currentness. An inspected `nextOwnerOperation` is a recovery hint, not an Effect admission, capability grant, current external observation, or proof that an owner is reachable. Missing or stale owner evidence remains unresolved. This World-local interface does not establish a generic Owner registry, Observation ontology or inspection contract for Security, Game, Harness or other domains.

## Cloudflare facts

The following are authoritative for current provider reality:

- live `/health` and `/v1/capabilities` output;
- Worker Version and deployment state;
- R2 request records, committed Receipts and Artifact bytes;
- effective Worker bindings and policy inputs;
- R2 lifecycle API state;
- source-input release digest;
- private release and GC receipts.

[`../providers/cloudflare/README.md`](../providers/cloudflare/README.md) documents the callable capability surface. Its operation, reliability, security and release documents own provider-local procedures. Cloudflare Receipt `started_at` / `completed_at` are provider-owned temporal facts. World JSON Schemas own the external adapter contract; TypeScript fixtures prove the Worker documents still conform.

## Temporal facts

Temporal provenance follows the same owner rule as other World evidence:

- Cloudflare/provider `started_at` and `completed_at` describe provider execution under the provider's clock;
- `WorldObservation.availableAt` describes when the validated complete observation first became available to the World controller under the World process clock;
- Host Event `recordedAt` / Task projection `updatedAt` describe Host admission under the Host clock.

None is silently substituted for another. Cross-clock subtraction is useful experimental evidence when clocks are sufficiently aligned, but is not promoted into a universal latency invariant without explicit clock synchronization. Availability does not imply truth, freshness, current external state, action authority or Task completion.

## Local machine facts

For current installation and network reality, the stronger owners are:

- installed file digests;
- systemd unit and timer state;
- root-only configuration and file modes;
- WireGuard interface, namespace and key/profile validation;
- live network observations;
- `ordivon-world-doctor` output derived from those sources.

CI cannot claim live health. Repository-only doctor output marks these checks as skipped.

## Historical facts

[`archive/world-negative-experiments.md`](archive/world-negative-experiments.md) and [`archive/research/`](archive/research/) are historical reproduction/explanation authorities for removed World, Edge, Link, WCP, WXP and network experiments. It cannot reactivate a deleted component. Reactivation requires a named current workload and a new failure proof under [`retained-boundaries.md`](retained-boundaries.md).

## Precedence

When sources conflict, use this order:

1. provider, Host and operating-system durable state;
2. executable source and locked machine-readable contracts;
3. commit-bound acceptance receipts;
4. current operational and status documents;
5. design explanation;
6. historical studies and archives.
