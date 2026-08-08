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

## A4-P0: Presence is current relation evidence, not durable history

A4 tested whether current Presence can be inferred from the durable facts A3 already creates. Two materially different destination domains falsified that shortcut.

### Game: current Body does not make an old subject binding current

A3 was replayed through the `medic-reyes` Actor and produced the accepted movement to Command Deck. After the Turn completed:

```text
historical A3 subject/cognition admission = retained
Harness cognition Run                    = terminal
Game Actor lifeState                     = active
Game Actor position                      = command-deck
```

A fresh next Planning opened at World revision 1. The old revision-0 subject/cognition binding was rejected, and strict destination admission refused to commit the next Agent-controlled Intent without a fresh current binding.

Therefore:

```text
Body current = true
historical embodiment occurrence = true
current Subject Presence = UNKNOWN
```

The durable A3 occurrence remains valid history, but it cannot authorize or prove the next relation merely because the same Actor body survived.

### Security: historical materialization can survive physical Body absence

A4 then used current Security revision `d532014dc4ff1d3fc9e825b5c087f1d2f1bac4ee` to physically materialize a real Windows KVM Entity carrier. Before destruction, QEMU was alive and the exact ledger/run path existed. The materialization receipt explicitly carried `historicalMaterializationReceipt = true` and still had `guestClaimAuthority = not-used`.

The native carrier was then cleanly destroyed. QEMU was no longer the recorded process, the ledger and run path were absent, and the retained migration receipt remained. Calling the current Entity `reconcile` path after destruction still returned `status = materialized` with the exact same retained receipt, because `materialized` is migration terminal history rather than a liveness claim.

Therefore:

```text
historical materialization receipt = true
reconcile migration status         = materialized
current Body Presence              = false
```

and, because Guest subject activation was never proven, Subject Presence was already unknown even before the carrier was destroyed.

### A4-P0 presence matrix

The current evidence supports an asymmetric, relation-scoped model rather than a global boolean:

| Native Body current? | Current subject/body binding? | Honest result |
|---|---|---|
| yes | yes, for one exact action scope | `present-within-scope` |
| yes | stale, missing or unproven | `unknown` |
| owner-proven absent | irrelevant for that Body | `absent-through-this-body` |

`absent-through-this-body` is not global Agent absence. A future Agent may have another Body elsewhere. Likewise, a durable `present-within-scope` observation becomes historical evidence when its Planning, World revision, body generation or other currentness fence changes.

The candidate law is:

> **Presence is an owner-observed, scope-bound current relation. Durable evidence of Presence may survive after its currentness expires, but the historical evidence itself does not remain current.**

This yields several narrower laws:

```text
Historical Embodiment Occurrence != Current Presence
Historical Materialization Receipt != Current Body Presence
Body Currentness != Subject Presence
Owner-proven Body Absence => Subject absent through that exact Body
Body current + no current Subject binding => UNKNOWN
```

A4-P0 does not justify `PresenceRegistry`, `AgentLocationTable` or a global Presence epoch. The next hypothesis should first test whether an Agent needs a bounded owner-authored **current relation observation** before its next body-bound action, and whether that observation can stay query-shaped rather than becoming new durable global state.

## A4-P1: current relation queries without a Presence registry

A4-P1 tested whether a fresh caller can obtain a useful current answer without introducing durable global Presence state. The successful experimental shape is query-oriented:

```text
CurrentRelationQuery
  queryId
  subjectRef
  bodyRef
  ownerId
  exact owner scope
      │
      │ queryDigest
      ▼
destination owner
  re-observes native current state
      │
      ▼
CurrentRelationObservation
  queryDigest
  bodyCurrentness
  bindingCurrentness
  owner evidence
      │
      ▼
World projection
  present-within-scope
  absent-through-body
  unknown
```

The projection is explicitly `informational-current-observation-not-action-authority`. The destination's normal action admission remains authoritative for an effect.

### Query identity prevents cross-query replay

The owner observation binds the exact query digest. Replaying one observation against a fresh query ID is rejected even when subject, body and scope are otherwise identical. Subject substitution and body substitution are rejected for the same reason.

This does not make an observation permanently fresh. Once returned, it is historical evidence that the owner observed a relation for that exact query. A later action still requires destination-native current checks. The query nonce prevents accidental reuse as a different current query; it does not replace liveness or authority.

### Game: the same Subject/Body can move PRESENT → UNKNOWN → PRESENT

Using the non-main Game A3 research candidate and one persistent `medic-reyes` Actor body, A4-P1 observed three scopes:

```text
r0
  Body current
  exact r0 subject/cognition admission current
  → present-within-scope

r1 before new cognition/admission
  same Body current
  old r0 binding stale
  → unknown

r1 after fresh cognition/admission
  same Body current
  new exact r1 binding current
  → present-within-scope
```

The r1 cognition was a new live DeepSeek Harness Run on Harness revision `98314d30de68412c3089fbe934eb049c2843bc98`. It saw the new r1 Station Zero Context and independently selected a legal `guard` action on Command Deck. The first attempt was rejected before any Provider call because the request upper-bound estimate was 15,378 tokens while the Run had only 12,000 total tokens remaining; the experiment raised the explicit Run token budget to 24,000 and then completed normally. This is Harness budget fencing, not a Presence failure.

The successful r1 cognition was bound through the same A3 cross-owner mechanism and admitted by Game for the exact r1 Planning. A new current relation query then returned `present-within-scope`. The old r0 observation could not answer the new r1 query.

Therefore Presence did not “stay on” because the Subject and Actor were unchanged. The relation became unknown when its scope expired and became present again only after a fresh cognition/body/action relation was admitted.

### Security: native observation failure degrades to UNKNOWN

A4-P1 also asked Security for a fresh relation observation of a physically materialized KVM carrier. A fresh QMP observation exceeded the bounded Runtime deadline. The probe retained the historical Receipt and residual process/ledger evidence but did **not** promote that incomplete evidence to current Body truth:

```text
fresh native observation timed out
→ bodyCurrentness = unknown
→ bindingCurrentness = unknown
→ relation = unknown
```

After Security cleanly destroyed the exact carrier, a new query was answered from current owner evidence showing the recorded QEMU identity absent, run ledger absent and run path absent while the historical materialization Receipt remained. That query projected `absent-through-body`.

This establishes a useful fail-soft rule:

> Current observation failure yields `UNKNOWN`; historical success must not fill the gap.

### Exact-body absence is not global Agent absence

A4-P1 finally issued fresh queries for the same `continuity-subject:medic-reyes` across two different domain bodies after the Game r1 admission and Security carrier destruction:

```text
Game Actor body
  → present-within-scope

Security KVM body A
  → absent-through-body
```

Both are simultaneously consistent because the body references differ. Therefore:

```text
absent-through-body-A
!=
Subject absent everywhere
```

A replacement Security carrier B was also physically materialized during exploration and had a different materialization/body identity. Its long-lived current-observation attempt was discarded because the Runtime holder expired before a valid owner observation completed; no Presence claim from that failed attempt is retained. The old Body-A observation was nevertheless correctly rejected when presented for Body B. This failure is evidence for keeping Body identity and owner-lifecycle boundaries explicit, not evidence that B was current.

### P1 result

The current minimal model is therefore relational and query-shaped:

```text
(subject, body, owner scope, one exact query)
    ↓ owner observation
bodyCurrentness
bindingCurrentness
    ↓
present-within-scope | absent-through-body | unknown
```

No experiment required a global Presence database, Agent location table, liveness daemon, global epoch or World-owned heartbeat. World only needed to bind the question to the answer and preserve the distinction between current owner observation and historical evidence.

The stronger laws are:

```text
Presence is not a durable boolean property of Subject or Body.
Presence observation is query-bound informational evidence, not action authority.
Fresh-query replay of an old observation is stale and rejected.
Current native observation failure => UNKNOWN.
Body current + current scoped subject binding => present-within-scope.
Exact Body absence => absent-through-that-body.
Absent through one Body != global Subject absence.
Scope change requires a fresh relation; Subject continuity does not preserve Presence automatically.
```

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
| current Presence | destination owner current observation of the subject/body relation; World may bind bounded evidence but must not infer it from historical admission/effect/materialization state |

## Promotion rule

Do not add a production `AgentIdentity`, `EmbodimentBinding` or Presence registry yet.

A3 proves that one real active destination can require owner-separated, action-scoped subject/cognition admission and that the mechanism prevents reproduced subject, cognition, Intent and evidence-laundering confusion. That is still insufficient for a shared production `EmbodimentBinding`: a second materially different destination domain should consume materially similar semantics before World turns the candidate into a cross-domain contract. The current Game implementation remains a detached research candidate.

## Evidence

[`../evidence/acceptance/w5a-embodiment-binding-d322947.json`](../evidence/acceptance/w5a-embodiment-binding-d322947.json) is the commit-bound A0/A1 receipt. It uses Game revision `8d89410e24ba486173ae6f3474962bb26433a6f5` and World research revision `d322947b891cf67749e879ca0c94663b8e067ce2`. The receipt records the conflicting-payload baseline, three rejected substitutions and the explicit decision not to promote a production contract.

[`../evidence/acceptance/w5a-game-active-controller-df396e5.json`](../evidence/acceptance/w5a-game-active-controller-df396e5.json) is the commit-bound A2 receipt. The same Game revision retained five active Agent-controlled Actors across two planning generations while provider attribution changed from `provider:w5a:alpha` to `provider:w5a:mallory`; no durable continuity-subject admission existed or was inferred.

[`../evidence/acceptance/w5a-a3-real-embodiment-083d619.json`](../evidence/acceptance/w5a-a3-real-embodiment-083d619.json) is the A3 commit-bound acceptance receipt, SHA-256 `cc119343e920dabe4623619de1833b04b26f527d0b71427706ebe6221ce1c448`. It binds World research revision `083d6195eb79e511ebb4abfe63ca5cc7a9d11644`, current Harness revision `9d9eb929beeb1c0372c7c163692e664bb9cb1682`, canonical Game revision `8d89410e24ba486173ae6f3474962bb26433a6f5`, and non-main Game admission candidate `cf4a011adb64fac8a3eb274eb266cfe707eec8f9`. The receipt records two live DeepSeek cognition instances for the same continuity subject, two non-interchangeable World bindings, two destination admissions, two verified `actor_moved` effects, digest-laundering rejection, cross-cognition rejection and fresh Harness/Game recovery.

[`../evidence/acceptance/w5a-a4-presence-888ca4e.json`](../evidence/acceptance/w5a-a4-presence-888ca4e.json) is the A4-P0 Presence falsifier receipt, SHA-256 `450023b63b13d05f6937e1a90925650906904810ccd854a8cc8794df539743c9`. It binds World base `888ca4efd10cb063e6603025c991e5a3a797ff49`, current Harness `9d9eb929beeb1c0372c7c163692e664bb9cb1682`, Game canonical plus the non-main A3 admission candidate, and current Security `d532014dc4ff1d3fc9e825b5c087f1d2f1bac4ee`. Game proved that an active surviving Body plus a historical A3 occurrence leaves current Subject Presence unknown at the next Planning; Security physically proved that a retained historical materialization receipt can survive after QEMU, ledger and run path are gone while `reconcile` still returns migration status `materialized`.

## W5-A closeout

W5-A has now reached its research stopping condition. The experiments proved enough structure to distinguish a real bounded Agent embodiment occurrence from carrier creation, Provider attribution, durable history and current Presence, while repeatedly failing to justify a shared production `AgentIdentity`, `EmbodimentBinding` or `PresenceRegistry`.

The retained W5-A laws are:

```text
Continuity Subject != Current Cognition Instance
Continuity Integrity != Continuity Ownership
Provider Attribution != Agent Embodiment
Carrier Materialization != Subject Activation
Evidence Reference != Evidence Interpretation != Destination Admission
Actionable Embodiment Admission = scoped Subject × Cognition × Body × Action relation
Bounded Embodiment Occurrence != Current Presence
Presence Observation != Action Authority
Body Currentness != Subject Presence
Absent Through One Body != Subject Absent Everywhere
```

The productive World responsibility is therefore narrow: bind independently owned subject/cognition/body evidence across a transition or question, preserve exact currentness coordinates, and refuse to upgrade historical or incomplete evidence. Native domains continue to own Bodies, liveness and final action admission.

No W5-A experiment requires World to own a global Agent identity service, live Body registry, location table, heartbeat service, universal embodiment manager or Presence database. The non-main Game admission candidate remains research evidence rather than product code.

## Hand-off to W5-B Presence

W5-B may start from the A4 laws, but it should not begin by implementing a Presence service. Its first question should be whether materially different active destinations reproduce a need for the same current subject/body relation beyond one bounded Game action. Priority falsifiers include:

1. a second active destination, ideally Security Guest-side subject activation or another independently owned environment;
2. a genuinely longer-lived relation where several actions occur without confusing subject continuity with action authority;
3. one subject with multiple concurrently meaningful Bodies, where Body-local absence must remain local;
4. fresh-Agent consumption of owner-authored relation observations without turning those observations into authority;
5. untrusted-relay authentication only if the workload leaves the current trusted-local owner boundary.

Until those workloads reproduce the need, the query-shaped A4-P1 projection is research vocabulary, not a production World contract.
