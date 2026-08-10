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
- [`w4-agency-authority-boundaries.md`](w4-agency-authority-boundaries.md) owns the cross-repository Agency/Authority decision: Presence is not authority, authority remains owner-scoped, source evidence does not become destination authority, and no global World capability/delegation service is justified by current evidence.
- [`w5-agent-embodiment.md`](w5-agent-embodiment.md) owns the active W5-A research boundary: source Entity departure, continuity ownership, destination carrier materialization, active embodiment and current Presence remain distinct until experiments prove otherwise.
- [`w5-presence.md`](w5-presence.md) owns the active W5-B research boundary: Agent-facing current subject/body relation evidence is query-scoped informational truth, not a global Presence registry or action authority.
- [`w5-discovery-connection.md`](w5-discovery-connection.md) owns the active W5-C research boundary: discovery, reachability, protocol-native relationship/session state and authority are separate dimensions; none may be promoted into another without owner-native evidence.
- [`w5-interaction.md`](w5-interaction.md) owns the W5-D interaction research closeout: typed interaction families share private causal/recovery mechanics and compose forward under partial completion, while source authority, destination consequence and receipt meaning remain owner-native semantics.
- [`w5-external-commitment-continuity.md`](w5-external-commitment-continuity.md) owns the W5-E continuity closeout: capability/reference history is not current applicability, pre-admission Agent selection is recomputable planning, and durable continuity begins at the first owner-admitted consequence boundary already retained by typed World journals.

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

[`archive/world-negative-experiments.md`](archive/world-negative-experiments.md) is historical reproduction authority for removed World, Edge, Link, WCP, WXP and network experiments. It cannot reactivate a deleted component. Reactivation requires a named current workload and a new failure proof under [`retained-boundaries.md`](retained-boundaries.md).

## Precedence

When sources conflict, use this order:

1. provider, Host and operating-system durable state;
2. executable source and locked machine-readable contracts;
3. commit-bound acceptance receipts;
4. current operational and status documents;
5. design explanation;
6. historical studies and archives.
