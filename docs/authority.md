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
updated: 2026-08-04
summary: Authority map for Host-facing World bindings, Cloudflare provider truth, network operator state, operational health and archived experiments.
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

Executable source, locked dependencies and machine-readable Schemas are stronger than prose when a discrepancy exists.

## Host-facing facts

Host remains authoritative for Task, Effect, Dispatch, Task revision, Ready Frontier, authority, UNKNOWN, Verification and completion. World owns only the extension objects and events it emits:

```text
world.dispatch-prepared
world.outcome-unknown
world.dispatch-observed
```

`PreparedWorldDispatch` and `WorldObservation` are World-owned CAS schemas embedded in Host storage. Host owns their admission order and revision fence. A World object cannot alter Task meaning merely because it is stored by Host.

## Cloudflare facts

The following are authoritative for current provider reality:

- live `/health` and `/v1/capabilities` output;
- Worker Version and deployment state;
- R2 request records, committed Receipts and Artifact bytes;
- effective Worker bindings and policy inputs;
- R2 lifecycle API state;
- source-input release digest;
- private release and GC receipts.

[`../providers/cloudflare/README.md`](../providers/cloudflare/README.md) documents the callable capability surface. Its operation, reliability, security and release documents own provider-local procedures. World JSON Schemas own the external adapter contract; TypeScript fixtures prove the Worker documents still conform.

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
