---
schema_version: 1
id: world.w5.agent-embodiment
title: W5-A Agent Embodiment Research Boundary
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
summary: W5-A distinguishes source Entity departure, continuity ownership, carrier materialization, active embodiment and current Presence without making World a global Agent identity or carrier owner.
evidence_status: experimental
readiness: RESEARCH
applies_to:
  - ordivon-world
  - ordivon-game
  - ordivon-security
related:
  - world.w2.entity-migration-production
  - world.w4.agency-authority-boundaries
---
# W5-A Agent Embodiment Research Boundary

## Question

W5-A asks whether the current production Entity Migration proves that an Agent can lose, acquire or replace a World embodiment.

The answer is currently **no**. Production proves a narrower trajectory:

```text
source-domain verified Entity departure
→ opaque continuity payload binding
→ destination-native carrier materialization
→ durable historical receipt / reconciliation
```

It does not yet prove:

```text
same Agent continuity subject
→ bound to the departing Entity
→ activated in the destination carrier
→ currently present there
```

This distinction is deliberate. W5-A must not create a global Agent identity service, World-owned carrier lifecycle, universal Presence database or cross-domain authority translator merely to make the vocabulary look complete.

## A0 falsifier: integrity is not ownership

The current `EntityDepartureReceipt` proves one Game-owned Station Zero Actor departure. It binds migration, Entity, source World, destination World and the exact source departure occurrence. It does not bind a continuity payload or Agent identity.

`EntityMigrationBundle.create_departed()` subsequently accepts opaque continuity material and binds only its digest. The published destination request intentionally permits any JSON continuity payload.

A real Station Zero extraction was therefore used to issue one canonical Game departure receipt. The same receipt was then combined with two conflicting payloads:

```text
payload A: identityRef = agent-identity:alpha
payload B: identityRef = agent-identity:mallory
```

Both current production requests validate. Both can also be prepared under independent Host Tasks. They share the same migration identity, Entity identity and source departure digest while carrying different continuity payload digests.

This does not demonstrate a production exploit that creates two destination bodies: the destination retains exact migration identity and rejects conflicting completed materialization. It demonstrates a more fundamental semantic limit:

> A payload digest proves continuity bytes are unchanged; it does not prove who owns those bytes or that they belong to the departed Entity.

Therefore a Security KVM `entity-continuity-carrier` is not by itself an Agent embodiment.

## A1 candidate: two-owner binding

W5-A next tests a minimal hypothesis without changing the production wire contract.

Two independently owned receipts are required:

```text
Body / Entity owner
  → EntityDepartureReceipt

Continuity subject owner
  → exact subject + payload + departure trajectory receipt
```

World may bind them only when the exact migration, Entity, source World, destination World, source departure digest and continuity payload digest agree.

The experiment uses an opaque `continuitySubjectRef`. World neither mints nor interprets it. The fixture authority is explicitly experimental; it does not claim Harness currently owns a durable global Agent identity. Harness has caller and Run identities plus Agent-owned Working Set state, but no canonical cross-Run Agent identity owner has yet been established.

The candidate rejects:

- continuity payload substitution;
- destination substitution;
- Entity substitution.

It retains current production `EntityMigrationBundle` after the two receipts agree, so destination-native carrier ownership and recovery remain unchanged.

## What A1 proves

A1 can remove one reproduced ambiguity:

```text
continuity integrity
!=
continuity ownership
```

A separate continuity owner can prove the relationship without World becoming that owner.

A1 does **not** prove active embodiment. The current Security destination deliberately stages an opaque continuity disk with `guestClaimAuthority = not-used`; the Guest does not consume the payload as an Agent identity/cognition claim. Production evidence therefore still proves carrier materialization, not activation of an Agent subject.

A1 also does not prove current Presence. Historical materialization remains historical evidence.

## A2 falsifier: active controller attribution is not embodiment

Game supplies the complementary failure mode to Security. Station Zero Actors can be `controllerKind = "agent"`, and each `StationZeroV3AgentDecision` retains the `providerId` that produced the decision. This is real active agency through a domain-owned Actor, but it still does not establish a durable continuity subject.

A bounded two-turn probe reopened one Station Zero run with two different provider identities. Five Actors remained active across both planning generations. In generation one all five decisions were attributed to `provider:w5a:alpha`; in generation two all five were attributed to `provider:w5a:mallory`. Game accepted the second planning generation without any durable continuity-subject admission because the current product contract never claims that `providerId` is Agent identity.

Therefore:

```text
active Actor
+ controllerKind = agent
+ provider attribution
!=
continuity-subject embodiment
```

This is not a Game defect. Provider identity answers which implementation produced a bounded decision. Treating it as persistent Agent identity would create the exact identity conflation W5-A is trying to avoid.

Together, Security and Game now expose opposite halves of the missing relation:

```text
Security: destination carrier exists, continuity subject is not activated
Game:     active Agent-controlled body exists, continuity subject is not identified/admitted
```

A production Embodiment abstraction is justified only if a destination domain needs to close this relation in its actual action-admission path.

## Current W5-A decomposition

The experiments currently force five distinct concepts:

```text
Continuity Subject
!=
Source Entity
!=
Destination Carrier
!=
Active Embodiment
!=
Current Presence
```

The ownership hypothesis is:

| Concept | Candidate owner |
|---|---|
| continuity subject identity / semantics | external Agent or cognition owner; not World |
| source Entity departure | source domain, Game in A0/A1 |
| migration binding and recovery | World + Host extension seam |
| destination carrier | destination domain, Security in current production |
| embodiment activation | destination/domain-specific; not yet proven |
| current Presence | current native observation; not inferred from receipt |

## Promotion rule

Do not add a production `AgentIdentity`, `EmbodimentBinding` or Presence registry yet.

A production contract is justified only if a real active destination requires the same owner-separated binding and the experiment proves that it prevents an otherwise reproduced identity/continuity confusion. A second materially different domain should consume the same semantics before World turns the candidate into a shared abstraction.

## Evidence

[`../evidence/acceptance/w5a-embodiment-binding-d322947.json`](../evidence/acceptance/w5a-embodiment-binding-d322947.json) is the commit-bound A0/A1 receipt. It uses Game revision `8d89410e24ba486173ae6f3474962bb26433a6f5` and World research revision `d322947b891cf67749e879ca0c94663b8e067ce2`. The receipt records the conflicting-payload baseline, three rejected substitutions and the explicit decision not to promote a production contract.

[`../evidence/acceptance/w5a-game-active-controller-df396e5.json`](../evidence/acceptance/w5a-game-active-controller-df396e5.json) is the commit-bound A2 receipt. The same Game revision retained five active Agent-controlled Actors across two planning generations while provider attribution changed from `provider:w5a:alpha` to `provider:w5a:mallory`; no durable continuity-subject admission existed or was inferred.

## Next experiment

A3 must target **destination subject activation**, not more migration or provider metadata.

The falsifier should place a continuity subject into a destination that can actually consume a bounded subject binding and then demonstrate all of the following independently:

1. the carrier exists;
2. the destination admitted the subject binding;
3. the subject became active through that carrier;
4. a conflicting subject cannot claim the same activation occurrence;
5. later liveness loss makes current Presence false/unknown without rewriting historical embodiment evidence.

Until such a workload exists, W5-A stops at the experimental two-owner binding plus the Game active-controller falsifier and keeps production Entity Migration unchanged.
