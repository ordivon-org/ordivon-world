---
schema_version: 1
id: world.w5.interaction
title: W5-D Interaction Research Boundary
type: research
profile: engineering
lifecycle: historical
source_role: historical-research
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

[`../evidence/acceptance/w5d-d0-interaction-families-e165cfe.json`](../../../evidence/acceptance/w5d-d0-interaction-families-e165cfe.json) is the D0 acceptance receipt. It binds current World, Game and Security revisions; 9/9 Game Resource/Message source-semantic tests; 30/30 Security Resource/Message/Entity destination tests; 7/7 Cloudflare adapter tests; and a compact current-code projection showing all three cross-World journals already inherit `_HostTrajectoryJournal` while Cloudflare direct effects do not fit a source→destination transfer plan.

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

## D1: mixed-family composition converges forward

D1 moved from static classification to one current durable workflow. A single Host Task retained both a Message Delivery and a Resource Transfer under one objective.

The first controller produced:

```text
Message A
  → delivered
  → retained receipt
  → destination delivery count = 1

Resource B
  → first materialization attempt
  → destination dies before semantic commit
  → Host Resource state = UNKNOWN
```

The Message remained committed while the Resource became uncertain. Host Task meaning itself remained `ready`; the two World extensions recorded their own independent causal state.

### Fresh Agent recovery

A fresh Host process reopened the same durable Task and constructed a bounded owner-authored view from retained state rather than trusting the first controller's memory:

```text
Message
  status = delivered
  retained receipt = present

Resource
  status = unknown
  retained receipt = absent
  nextAction = reconcile-original-transfer
```

A current Harness fresh Agent received four candidate actions:

```text
reconcile-resource
retry-resource
resend-message
rollback-message
```

and selected `reconcile-resource`. The Run used current Harness `487e0ac8eb945256842347b5371cbbdd70bfce55`, one Provider call, zero Tool calls, and produced durable receipt `sha256:b704230a3c4b14c4e0cf741b10db428dd1ef52ff8252255537276dc14fd55e2e`.

This is important because the earlier Message receipt was informative history, not Resource retry authority.

### Reconcile before retry

A second fresh Host controller executed only the Agent-selected Resource reconciliation. The destination returned an exact `ResourceTransferNotCommitted` proof with `exactOriginalRetrySafe=true`.

The transition was:

```text
Resource UNKNOWN
  ↓ exact NOT_COMMITTED proof
Resource PREPARED
```

No second materialization occurred during reconciliation:

```text
materialization attempts = 1
reconcile calls          = 1
```

The Message receipt digest and destination delivery count remained unchanged.

Only after that proof did a third fresh Host controller perform the exact original Resource retry. The destination committed on materialization attempt 2. A fourth fresh Host process then independently reopened the final durable state and observed:

```text
Message A   delivered
  destination deliveries = 1
  same retained receipt

Resource B  materialized
  materialization attempts = 2
  reconcile calls          = 1
  retained materialization receipt
```

The Host Task contained no global rollback, transaction, federation head or generic interaction state.

## What D1 proves

The current composition law is forward-only and typed:

```text
Interaction A committed
        │
        ├── remains historical fact
        │
Interaction B UNKNOWN
        ↓
reconcile B under B's own identity/owner evidence
        ↓
exact retry only if B proves retry-safe
        ↓
continue forward
```

Therefore:

```text
Interaction A success != Interaction B success

Downstream UNKNOWN
!= rollback authorization for upstream commit

Upstream receipt
!= downstream authority

Partial causal chain
→ forward reconciliation
!= distributed rollback
```

The Resource retry remained grounded in its own retained source egress plus its own exact `NOT_COMMITTED` proof. The Message's source issuance and delivery receipt never became Resource authority.

[`../evidence/acceptance/w5d-d1-mixed-composition-3ce688d.json`](../../../evidence/acceptance/w5d-d1-mixed-composition-3ce688d.json) is the D1 acceptance receipt. It binds the four fresh Host phases, current Harness Agent decision, exact Message and Resource receipt identities, destination counters and absence of global interaction transaction state.

## W5-D stopping condition

D0 shows that Interaction consists of typed semantic families over a smaller shared causal/recovery skeleton. D1 shows that different families already compose safely under one durable Host objective and recover forward after partial completion without semantic promotion, global rollback or a generic manager.

That is enough to stop the current Interaction line. Do not add:

```text
GenericInteraction
InteractionManager
UniversalWorldTrajectory
GlobalInteractionTransaction
CrossFamilyRollbackProtocol
```

A future materially different interaction should first attempt to reuse the current causal skeleton and retain its owner-native semantics. Only reproduced mechanical friction should widen the private shared layer.

D1 also exposed the next unresolved problem cleanly at that time: the fresh Agent succeeded only because the experiment supplied a bounded current interaction view. Host `task.resume` still must not learn World schemas, while the Agent needs a way to discover outstanding external commitments after controller replacement. That question belongs to **W5-E External Commitment Continuity**, not to Interaction semantics, and is now closed in [`w5-external-commitment-continuity.md`](w5-external-commitment-continuity.md): typed owner journals are projected through `WorldTaskInspector`, while pre-admission capability/path selection remains recomputable rather than becoming another durable commitment layer.
