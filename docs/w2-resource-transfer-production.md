---
schema_version: 1
id: world.w2-resource-transfer
title: W2 Production Resource Transfer
type: decision
profile: engineering
lifecycle: active
source_role: supporting
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
evidence_status: cross-repository-verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.start
  - world.authority
  - world.boundaries
  - world.w1-trajectories
---
# W2 Production Resource Transfer

## Purpose

W2 promotes one W1 trajectory only after it survives a real production integration across independently owned repositories.

The stable Resource Transfer path is:

```text
Source World
  native consequence + source-local replay/verification
        ↓
ResourceEgressReceipt
  exact transfer / destination / payload / source occurrence
        ↓
World ResourceTransfer
  Host-retained plan, egress receipt, payload and uncertainty
        ↓
Destination World ingress
  destination-local admission + materialization
        ↓
ResourceTransferReceipt
```

The first production consumer pair is Station Zero Game → Security SampleVault. Game and Security do not import each other's domain implementation, and Security does not import the Python `ordivon-world` package. Their shared boundary is the packaged World JSON contract.

## Two authority boundaries

A Resource Transfer is not established by destination materialization alone.

W2 reproduced a false-positive path where an arbitrary JSON object was digest-bound to `sourceWorldId`; Security materialized the payload even though no Game/source owner had admitted the resource departure. That falsifier blocked the first attempted 0.2.0 promotion.

The corrected path crosses two independent boundaries:

1. **Source egress authority** — the source World binds one exact native resource occurrence to one transfer and destination.
2. **Destination ingress authority** — the destination admits that exact transfer and materializes or rejects it under destination-local policy.

`ResourceEgressReceipt` is the shared source statement. It binds:

- `transferId`;
- source and destination World identities;
- resource kind;
- portable payload digest;
- source occurrence identity and digest;
- source authority identity, mechanism and evidence.

`PreparedResourceTransfer` derives its identity from the egress receipt. Callers do not supply a second independent copy of source/destination/resource identity.

## Station Zero source authority

`StationZeroV3ResourceEgress` is a Game-owned integration component, not a WorldState field.

It obtains the native source fact through `StationZeroV3Store.turnReceiptByBatch()`. That persistence API validates Event/Record/Batch alignment, digests and deterministic replay before returning the retained Turn Receipt.

The first production acceptance used the real persisted `medic-reyes` extraction of `medkit`. The resulting egress receipt bound the retained `item_extracted` Fact to one transfer. The Game egress ledger enforces:

- exact retry returns the same receipt;
- the same transfer identity cannot silently change destination or payload;
- one source occurrence cannot authorize a second transfer;
- reopen preserves the egress receipt;
- Game historical state is not rewritten to represent current cross-World custody.

The Game receipt and Python World parser produced the same canonical digest across TypeScript/Python.

## Security destination authority

Security owns `WorldResourceInbox`, its SampleVault bytes and transfer-specific admission record.

A SampleVault object with identical bytes is **not** sufficient evidence that a transfer was admitted. Reconciliation requires the transfer-specific admission record binding the exact plan, source egress digest and payload digest.

The destination uses a per-transfer exclusive file lock plus an atomic create-only admission record. This creates a precise semantic commit point independent of CAS staging.

## UNKNOWN and `not_committed`

W2 deliberately crashed the destination after SampleVault import but before transfer admission commit:

```text
payload CAS present          ✓
transfer admission record   ✗
Host                         UNKNOWN
```

Without stronger evidence this was a safe deadlock: blind retry remained forbidden, but reconciliation could not complete.

Security now returns `not_committed` only while holding the exact transfer lock and observing no admission record. The proof binds transfer, plan, destination and payload and states `exactOriginalRetrySafe=true`.

World persists that proof before changing:

```text
UNKNOWN
  ↓ destination not_committed proof
PREPARED
  ↓ exact original transfer only
MATERIALIZED
```

A concurrent-process race test holds the transfer lock after CAS staging and before admission. Reconciliation blocks behind the live materializer; if it commits, reconciliation returns the same materialized receipt and never emits a false `not_committed` proof.

## Historical finality and current Presence

A retained destination receipt proves that the destination semantic admission committed. It does not assert that the resource is still present later.

W2 deletes native SampleVault bytes after admission and preserves the historical receipt. Current resource presence must be obtained from the native destination Reality owner.

## Trust boundary

`ResourceEgressReceipt` proves what a source authority **states and binds**. Its authenticity across an untrusted relay is not implied by JSON structure.

The current Security CLI declares:

```text
sourceAuthorityAuthentication = caller-trust-boundary
```

A deliberate falsifier constructed a structurally valid but fake Game-like egress receipt and called the Security ingress directly. Security accepted it, exactly as expected inside this trust model.

Therefore the stable contract is explicit:

- trusted local orchestration may carry source egress receipts across the boundary;
- an endpoint exposed to an untrusted relay/caller must independently authenticate source authority before admission;
- signature/PKI/trust-graph semantics remain deployment-specific until multiple real consumers force one shared mechanism.

This preserves the W1 rule:

```text
source semantic authority
  ≠ structural receipt validity
  ≠ end-to-end cryptographic authentication
```

## What W2 does not add

Resource Transfer does not introduce:

- a global resource database;
- a universal resource UUID requirement;
- automatic inventory copying;
- source historical-state rewriting;
- distributed atomic rollback;
- a global World revision/head;
- a World daemon;
- mandatory PKI;
- generic Entity/Message promotion.

Resource Transfer is the first production inter-World contract because it has an actual source producer, destination consumer, recovery story and deletion/failure evidence. Entity Migration and Message Delivery remain experimental until they receive equivalent production pressure.
