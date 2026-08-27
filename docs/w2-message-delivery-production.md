---
schema_version: 1
id: world.w2-message-delivery
title: W2 Production Message Delivery
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
  - world.w2-resource-transfer
  - world.w2-host-trajectory-addressing
  - world.authority
  - world.boundaries
---
# W2 Production Message Delivery

## Purpose

W2 promotes Message Delivery only after a real Game source, World durable trajectory and Security destination independently exercised the contract.

```text
Game / source World
  retained visible Fact
        ↓
MessageIssuanceReceipt
  exact message / destination / provenance / payload
        ↓
World MessageDelivery
  Host-retained plan + uncertainty
        ↓
direct destination transport
        ↓
Security WorldMessageInbox
  message-specific admission
        ↓
MessageDeliveryReceipt
```

Delivery is informational. It does not transfer custody and it does not promote the claim into destination knowledge or world-truth.

## Source issuance is not provenance integrity

The first direct Game → Security experiment used a real persisted Station Zero Fact and recovered correctly after response loss. A deliberate falsifier then constructed a fully self-consistent Game-like provenance and payload without consulting Game. Security accepted the bytes under the local caller trust boundary.

Therefore:

```text
provenance integrity != source issuance authority
```

Game now owns `StationZeroV3MessageIssuance`. It reopens the retained Turn Receipt, requires that the issuing faction could observe the Fact, and commits an immutable `MessageIssuanceReceipt` keyed by `messageId`.

Message issuance deliberately differs from Resource Egress. A Resource occurrence cannot be transferred twice under exclusive custody semantics. A retained Fact is not consumed by communication: one source occurrence may legitimately authorize multiple independently identified Messages and destinations.

```text
same messageId -> immutable meaning
same source Fact -> multiple messageIds are allowed
```

## Destination admission is not belief

The first production destination is Security `WorldMessageInbox`. Security implements the versioned JSON boundary without importing the Python `ordivon-world` package.

An admitted Message is durably classified as `management`. Its admission record and receipt explicitly retain:

```text
knowledgePromoted = false
worldTruthPromoted = false
```

This preserves the Range plane distinction:

```text
foreign claim received
!= sensor evidence
!= contested Reality
!= world-truth
```

A later Security/domain decision may use the claim as input, but Message ingress itself has no authority to make that promotion.

## Message identity is independent of Host Task identity

A real Station Zero Turn produced two distinct faction-visible Facts. Preparing both under one Host Task reproduced the old singleton failure: the second Message was rejected only because the first occupied flat Task extension fields.

Message now opts into the private per-trajectory Host addressing rule:

```text
Host Task
  └── worldMessageDeliveries
        ├── message:A -> independent state / receipt / uncertainty
        └── message:B -> independent state / receipt / uncertainty
```

When one Message exists, implicit lookup remains convenient. When multiple Messages exist, omission of `messageId` fails closed.

Current Message state uses the per-message map. The 0.6 line retires transparent pre-M5 flat-state migration; any retained historical flat Message state must be recovered/upgraded with a pre-0.6 client before package upgrade.

## UNKNOWN recovery has two different outcomes

W2 verified both branches on one real Host Task with two Game-issued Messages sharing one source Fact.

### Destination committed, ACK lost

```text
Security admission committed
→ response lost
→ Host Message = UNKNOWN
→ Game export removed
→ fresh Host reconcile only
→ retained Security receipt found
→ delivered
```

No second delivery was issued.

### Destination was never committed

A transport failure was deliberately classified as ambiguous even though the Security process was never invoked:

```text
Host Message = UNKNOWN
→ Security reconcile under exact message lock
→ no admission record
→ MessageDeliveryNotCommitted
→ exactOriginalRetrySafe = true
→ Host persists proof
→ only that Message returns to prepared
→ exact original delivery once
```

A live-commit race test holds the same message lock before admission commit. Concurrent reconciliation blocks; after the writer commits, reconciliation returns the retained delivery receipt rather than a false `not_committed` proof.

## Endpoint identity without a first-class WorldLink

The Message experiments intentionally tried to force a `WorldLink` abstraction and failed to do so.

A Unix socket path was replaced by a process that did not import Security. The replacement could return a structurally valid receipt while claiming the same destination World. Endpoint path, UID and self-declared World identity were insufficient authentication.

A second experiment pinned an Ed25519 destination public key and required a request-bound attestation over destination World, nonce, plan digest and receipt digest. The replacement endpoint could no longer authenticate and direct delivery failed closed.

Then the legitimate Security process and socket inode both changed while the destination key and durable receipt remained stable. A fresh Host reconciled the original Message without redispatch.

Finally Security moved from socket A to socket B. A signed endpoint advertisement advanced discovery revision `1 -> 2`; the old address failed before dispatch, the new advertisement and destination response authenticated successfully.

The evidence supports:

```text
World continuity
!= process identity
!= socket identity
!= endpoint address
```

and, for the tested Message trajectory:

```text
authenticated discovery + authenticated destination identity + direct delivery
is sufficient
```

No independent Link identity, Link lifecycle, shared Link head or Link-scoped ordering was required. `WorldLink` therefore remains unpromoted. A future workload must reproduce a relationship-level responsibility that the two endpoint Worlds cannot own cleanly before a first-class Link is introduced.

## Trust boundary

`MessageIssuanceReceipt` binds what a source authority states. JSON structure alone does not authenticate that authority through an untrusted relay.

The first Security production consumer declares:

```text
sourceAuthorityAuthentication = caller-trust-boundary
```

Deployments that cross an untrusted relay must add independent source-authority authentication. The endpoint-identity experiments prove that cryptographic peer binding is feasible; 0.3.0 does not prescribe one universal PKI, trust graph or transport.

## What 0.3.0 does not add

Message Delivery does not add:

- a global Message bus;
- automatic broadcast/fan-out orchestration;
- global Message ordering;
- destination knowledge promotion;
- a global Reality database;
- a universal public `WorldTrajectory`;
- a first-class `WorldLink`;
- mandatory PKI;
- Entity Migration production semantics.

The stable contract is intentionally smaller: source issuance, exact Message identity, per-Message Host continuity, destination admission, durable receipt and identity-bound reconciliation.
