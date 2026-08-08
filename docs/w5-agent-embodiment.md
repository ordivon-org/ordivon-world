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

## A3: destination action-scoped embodiment admission

A3 asked a narrower question than “does an Agent live in this body?”:

> Can one independently owned continuity subject bind one exact current cognition instance to one domain-native body, have the destination admit that relation in its unavoidable action path, and then produce a verified native World effect?

The answer is **yes for one bounded action occurrence under the trusted-local owner-originated caller profile**. This is still weaker than durable embodiment or current Presence.

### A3.0: the admission cut point must be unavoidable

Game first falsified two tempting shortcuts.

Provider attribution is lost before final per-Actor action admission. From one identical Station Zero World/Planning snapshot, replacing only `provider:w5a:alpha` with `provider:w5a:mallory` produced the same Rescue Faction Plan and the same Actor Intents. `providerId` identifies one Decision producer; it is not retained as the identity of the subject acting through the Actor.

Plan Preview is also not the authority boundary. A lower-level `StationZeroV3TurnService` can submit Faction Plans and execute a Turn without creating Preview infrastructure at all. Therefore a subject binding attached only to Preview or Provider output would remain bypassable metadata.

The experimental destination cut point was placed at durable Faction Plan / Turn Batch commitment and fresh-process recovery instead. When W5-A strict admission is enabled, every relevant Agent-controlled Actor Intent must have a destination-local admission bound to the exact Planning, World revision/digest, Actor and submitted Plan before commitment.

### A3.1: an evidence digest is not semantic admission

The first destination candidate accepted a caller-supplied `subjectRef` plus an opaque evidence digest. A falsifier reused a genuine binding digest whose content named `continuity-subject:medic-reyes` while claiming `continuity-subject:mallory` to Game. Game accepted the false subject because it had never interpreted the evidence coordinates.

This establishes:

```text
Evidence Reference
!=
Evidence Interpretation
!=
Destination Admission
```

The candidate was tightened so Game receives the complete external binding plus its exact digest and verifies only the coordinates Game owns: Game Run, Planning, World revision/digest, Actor and exact submitted Intent. Game does not parse Harness-internal Provider records and does not mint the continuity subject.

### A3.2: owner-separated structural chain

The successful structural chain is:

```text
continuity subject owner claim
        │
        ▼
Harness Run
  exact cognition evidence
        │
        ▼
World experimental binding
  subject × cognition × Game candidate
        │
        ▼
Game destination admission
  exact Actor × exact Intent × exact Planning
        │
        ▼
committed Turn
        │
        ▼
verified domain-native Fact
```

The destination rejects missing admission, subject substitution, cognition/Intent substitution and digest laundering. It retains the complete binding and revalidates it on fresh-process recovery; tampering the retained binding makes recovery fail closed.

The experimental Game candidate is commit `cf4a011adb64fac8a3eb274eb266cfe707eec8f9`. It remains a detached research commit and is **not** part of Game production. Its focused W5-A test and the complete Game suite passed, with 256 of 256 tests green plus TypeScript typecheck and `git diff --check`.

### A3.3: live cognition through a domain body

The structural chain was then repeated with the current Harness revision `9d9eb929beeb1c0372c7c163692e664bb9cb1682` and live `deepseek-v4-flash` cognition rather than a scripted choice.

Both live Runs used the same Station Zero Agent Context, the same long-term `continuity-subject:medic-reyes`, and a structured completion contract whose `candidateId` enum contained only Game-admitted movement candidates. The model therefore chose among domain-admitted actions rather than inventing a new action.

Two independent cognition instances deliberately produced different decisions from the same World snapshot:

```text
Cognition A
  Harness Run: ...current-medic-cognition-1
  → move Medic Reyes to Command Deck

Cognition B
  Harness Run: ...current-medic-cognition-2
  → move Medic Reyes to Junction Console
```

Each Harness Run completed with a durable terminal receipt and was recovered by a fresh Harness process with the same receipt, Trace and conclusion.

World bound each terminal cognition to its exact Game candidate. Game then admitted the binding through the `medic-reyes` Actor. Both actions produced verified `actor_moved` Facts and survived fresh Game verification.

### A3.4: subject continuity does not make cognition instances interchangeable

The two live Runs share the same continuity subject and the same domain body, but have different Harness Run identities and different Intent digests. Cross-use was rejected in both directions:

```text
Command Deck Plan + Junction cognition binding → reject
Junction Plan      + Command cognition binding → reject

Command Deck Plan + Command cognition binding → execute
Junction Plan      + Junction cognition binding → execute
```

Therefore:

```text
Continuity Subject
!=
Current Cognition Instance
```

and:

> Subject continuity does not grant blanket action authority to every cognition instance associated with that subject.

The current A3 hypothesis is that one actionable embodiment admission must bind at least:

```text
Subject
× Current Cognition Instance
× Domain Body
× exact Action / Plan coordinates
```

A successful native effect proves one **bounded active embodiment occurrence**. It does not prove that the subject remains currently Present in that body after the occurrence.

## Current W5-A decomposition

The experiments now force the following concepts apart:

```text
Continuity Subject
!=
Current Cognition Instance
!=
Source Entity
!=
Destination Body / Carrier
!=
Action-scoped Embodiment Admission
!=
Bounded Embodiment Occurrence
!=
Current Presence
```

The ownership hypothesis is:

| Concept | Candidate owner |
|---|---|
| continuity subject identity / semantics | external subject owner; not World or Harness by default |
| current cognition instance | Harness Run and its owner-authored terminal evidence |
| source Entity departure | source domain, Game in A0/A1 |
| migration binding and recovery | World + Host extension seam |
| destination Body / Carrier | destination domain |
| subject/cognition → Body action admission | destination domain, using bounded external binding evidence |
| cross-owner subject/cognition binding | World research boundary; not an authority translation |
| bounded embodiment occurrence | proved jointly by exact cognition evidence, destination admission and native effect receipt/fact |
| current Presence | current native observation; never inferred from historical admission/effect evidence |

## Promotion rule

Do not add a production `AgentIdentity`, `EmbodimentBinding` or Presence registry yet.

A3 proves that one real active destination can require owner-separated, action-scoped subject/cognition admission and that the mechanism prevents reproduced subject, cognition, Intent and evidence-laundering confusion. That is still insufficient for a shared production `EmbodimentBinding`: a second materially different destination domain should consume materially similar semantics before World turns the candidate into a cross-domain contract. The current Game implementation remains a detached research candidate.

## Evidence

[`../evidence/acceptance/w5a-embodiment-binding-d322947.json`](../evidence/acceptance/w5a-embodiment-binding-d322947.json) is the commit-bound A0/A1 receipt. It uses Game revision `8d89410e24ba486173ae6f3474962bb26433a6f5` and World research revision `d322947b891cf67749e879ca0c94663b8e067ce2`. The receipt records the conflicting-payload baseline, three rejected substitutions and the explicit decision not to promote a production contract.

[`../evidence/acceptance/w5a-game-active-controller-df396e5.json`](../evidence/acceptance/w5a-game-active-controller-df396e5.json) is the commit-bound A2 receipt. The same Game revision retained five active Agent-controlled Actors across two planning generations while provider attribution changed from `provider:w5a:alpha` to `provider:w5a:mallory`; no durable continuity-subject admission existed or was inferred.

[`../evidence/acceptance/w5a-a3-real-embodiment-083d619.json`](../evidence/acceptance/w5a-a3-real-embodiment-083d619.json) is the A3 commit-bound acceptance receipt, SHA-256 `cc119343e920dabe4623619de1833b04b26f527d0b71427706ebe6221ce1c448`. It binds World research revision `083d6195eb79e511ebb4abfe63ca5cc7a9d11644`, current Harness revision `9d9eb929beeb1c0372c7c163692e664bb9cb1682`, canonical Game revision `8d89410e24ba486173ae6f3474962bb26433a6f5`, and detached Game admission candidate `cf4a011adb64fac8a3eb274eb266cfe707eec8f9`. The receipt records two live DeepSeek cognition instances for the same continuity subject, two non-interchangeable World bindings, two destination admissions, two verified `actor_moved` effects, digest-laundering rejection, cross-cognition rejection and fresh Harness/Game recovery.

## Next experiment

A4 should target **current Presence**, not add more admission metadata.

A3 now has historical proof that one subject/cognition/body/action relation produced a real native effect. A4 must ask what remains true after that occurrence ends. In particular, it should independently test:

1. Body liveness/currentness after the cognition Run has already terminated;
2. whether a new cognition instance for the same subject may reuse the same Body only after fresh destination admission;
3. whether body loss makes current Presence false or unknown without rewriting the historical A3 occurrence;
4. whether Game Actor liveness and Security KVM carrier liveness share any honest cross-domain Presence invariant;
5. whether any current-Presence projection is actually needed by an Agent before its next body-bound action.

Do not create a global Presence database. A4 should first compare native owner observations and retain the earlier law that historical evidence never proves current state.

Production Entity Migration remains unchanged, and the A3 Game admission implementation remains a detached research candidate until another materially different destination reproduces the same need.
