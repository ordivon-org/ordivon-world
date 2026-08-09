---
schema_version: 1
id: world.w5.interaction
title: W5-D Interaction Research Boundary
type: research
profile: engineering
lifecycle: active
source_role: current-research
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
summary: W5-D studies the smallest stable interaction laws across typed cross-World transfers and direct external effects without replacing owner-native semantics with a universal interaction model.
evidence_status: experimental
readiness: RESEARCH
applies_to:
  - ordivon-world
  - ordivon-game
  - ordivon-security
related:
  - world.w5.discovery-connection
  - world.w4.agency-authority-boundaries
---
# W5-D Interaction Research Boundary

## Starting question

Resource Transfer, Message Delivery and Entity Migration are all production World trajectories. It is tempting to call them three fundamental interaction primitives simply because three modules exist.

W5-D starts by trying to falsify that interpretation:

> Are Resource, Message and Entity genuinely the primitive ontology of Agent interaction, or are they typed semantic families sitting on top of smaller causal/recovery mechanics?

The answer matters because a premature `GenericInteraction` would move source custody, communication, embodiment and provider-effect meaning into World merely to reduce class count.

## D0: shared mechanics, distinct semantics

The current implementation already performs one useful compression. Resource, Message and Entity Host journals inherit the private `_HostTrajectoryJournal`, which owns the repeated durable mechanics:

```text
exact semantic identity
plan / bound payload retention
        ↓
execute exact operation
        ↓
receipt OR UNKNOWN
        ↓
identity-bound reconcile
        ↓
exact not_committed retry proof where supported
```

That private base is intentionally mechanical. It does not decide what a Resource, Message or Entity *means*.

The remaining public differences are not naming noise.

### Resource is custody/materialization semantics

Current Station Zero Resource Egress has a database uniqueness rule on the source occurrence. The focused owner tests prove:

```text
one source Resource occurrence
→ at most one transfer / destination
```

An exact retry is idempotent, but another transfer identity for the same source occurrence is rejected.

Security's Resource destination materializes the portable object into a SampleVault and commits a transfer-specific admission. Existing identical CAS bytes alone do not prove that the Resource Transfer occurred.

### Message is non-consuming informational semantics

Current Station Zero Message Issuance deliberately has no uniqueness constraint on source occurrence. The focused owner tests prove:

```text
one retained visible Fact
→ multiple independently identified Messages are allowed
```

Security Message ingress records an admitted foreign claim while explicitly retaining:

```text
knowledgePromoted = false
worldTruthPromoted = false
```

Communication therefore neither transfers custody nor automatically changes destination belief/Reality.

Resource and Message cannot honestly be one semantic primitive with only a different label: their accepted source reuse laws are opposite.

### Entity is continuity/body materialization semantics

Entity Migration binds an exact source departure and Entity identity while keeping continuity payload opaque to World. The destination owns a KVM continuity-carrier materialization. The receipt proves historical materialization, not current Presence and not cognition activation.

This is not ordinary portable-object custody. The source and destination consequences concern the continuity of an existence across independently authoritative Worlds.

### Direct external effect does not fit the three-transfer model

Cloudflare Fetch/Browser provides a fourth materially different interaction family already in production:

```text
Host Dispatch / Effect
+ current capability condition
        ↓
exact provider request identity
        ↓
provider-native operation
        ↓
receipt / Artifact / WorldObservation
        ↓
UNKNOWN reconcile by exact provider request
```

There is no source World egress/issuance/departure and no destination World materialization contract. Therefore Resource/Message/Entity do not exhaust World Interaction.

## D0 classification

The current evidence supports two broad families without claiming they are exhaustive:

```text
Interaction
├─ Cross-World semantic transfer
│  ├─ Resource: custody / object materialization
│  ├─ Message: informational delivery
│  └─ Entity: continuity / body materialization
│
└─ Direct external effect / observation
   └─ provider-native Fetch / Browser / future effects
```

What is genuinely shared is lower than these names:

```text
exact bounded intent
        ↓
current owner/provider condition where required
        ↓
owner-native admission / execution
        ↓
native consequence
        ↓
receipt OR UNKNOWN
        ↓
identity-bound reconciliation before retry
```

This is a causal/recovery skeleton, not a universal domain model.

## Why no `GenericInteraction`

A public generic abstraction has only two options.

### Erase semantic fields

If it keeps only generic identity/source/destination/payload fields, it loses facts such as:

- whether a source occurrence is consuming or reusable;
- whether destination admission transfers custody, receives a claim or materializes a Body;
- whether a receipt may imply belief, Presence or neither;
- whether a current capability condition must fence dispatch.

That is unsound.

### Retain `kind + opaque semantic payload`

If the generic object retains every typed contract behind a kind tag and dispatches to Resource/Message/Entity/provider-specific code, it has not discovered a new invariant. It has added a wrapper around the existing typed families.

The useful common mechanics are already shared privately. No public abstraction is needed merely to make the class diagram smaller.

## D0 evidence

[`../evidence/acceptance/w5d-d0-interaction-families-e165cfe.json`](../evidence/acceptance/w5d-d0-interaction-families-e165cfe.json) is the D0 acceptance receipt. It binds current World, Game and Security revisions; 9/9 Game Resource/Message source-semantic tests; 30/30 Security Resource/Message/Entity destination tests; 7/7 Cloudflare adapter tests; and a compact current-code projection showing all three cross-World journals already inherit `_HostTrajectoryJournal` while Cloudflare direct effects do not fit a source→destination transfer plan.

## Retained laws

```text
Shared interaction mechanics != shared interaction semantics.

Source consumption / fan-out semantics belong to the source owner.

Destination consequence meaning belongs to the destination/provider owner.

Receipt meaning is family-specific and historical.

Direct external effect and cross-World transfer are distinct interaction families
that share a lower causal/reconciliation skeleton.
```

## Product decision

D0 does not justify:

```text
GenericInteraction
UniversalWorldTrajectory
WorldInteractionManager
Resource|Message|Entity tagged-union replacement
```

Keep `_HostTrajectoryJournal` private and mechanical. Keep public contracts typed by the semantic consequence they actually promise.

## D1 next falsifier: composition without semantic promotion

The next question is not whether to rename the families. It is whether successful interactions compose safely:

> When one Agent workflow performs several different interaction families in sequence, which facts may flow forward, and which must be re-admitted by the next owner?

A useful D1 should compose at least two materially different interactions under one durable Host objective and deliberately create partial completion. It should test whether:

- Message delivery can inform a later Resource/Effect decision without minting its authority;
- a completed first interaction remains historically committed if the second fails;
- the Agent can recover the partial causal chain after replacement without global rollback or a generic transaction manager.

Existing W1/W2 partial-federation evidence is a good source of hypotheses, but D1 should use a current Agent-facing workflow rather than merely restating those older tests.
