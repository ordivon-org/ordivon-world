---
schema_version: 1
id: world.w5.presence
title: W5-B Agent Presence Research Boundary
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
summary: W5-B studies when an Agent needs fresh owner-observed subject/body relation evidence and whether that need can remain query-shaped rather than becoming global Presence state.
evidence_status: experimental
readiness: RESEARCH
applies_to:
  - ordivon-world
  - ordivon-harness
  - ordivon-game
  - ordivon-security
related:
  - world.w5.agent-embodiment
  - world.w4.agency-authority-boundaries
---
# W5-B Agent Presence Research Boundary

## Starting point

W5-A closed with a negative architectural result: current Presence is not a durable property of an Agent or Body. A bounded embodiment occurrence can be proven, but its historical evidence does not remain current. A4-P1 showed that a query-bound owner observation can distinguish `present-within-scope`, `absent-through-body` and `unknown` without a Presence registry.

W5-B therefore does **not** begin by defining a Presence service. It begins by asking when current relation evidence changes an Agent's next decision and which owner must produce that evidence.

## B0: fresh-Agent Presence consumption

B0 tests the most basic Agent-facing need:

> If a fresh Agent must choose a Body for an immediate new action, is historical embodiment/materialization evidence sufficient, or does it need fresh current relation evidence?

Two bounded decision inputs were constructed for the same `continuity-subject:medic-reyes` and the same candidate bodies.

The historical-only input contained:

- a real bounded Game embodiment occurrence and native movement Fact from W5-A A3;
- a real Security Entity materialization history whose terminal migration state was `materialized`;
- no current relation observation for either Body.

The final commit-bound rerun retained the same history and added two freshly reconstructed owner relations:

```text
Game Actor Body
  → fresh r0 destination admission
  → present-within-scope

Security B1 KVM Body
  → exact Host clean closure
  → absent-through-body
```

The Game relation used the non-main W5-A admission candidate; the Security relation used the exact B1 materialization Body after `qemuClosed`, ledger removal, run-directory removal and zero residual objects.

A fresh live DeepSeek Harness Run received each input independently under a structured completion contract with only three possible decisions:

```text
game-body
security-body-a
insufficient-current-evidence
```

The decision rule explicitly prohibited treating historical success as current evidence and stated that the relation projection is informational rather than action authority.

### Result

The historical-only Agent chose:

```text
insufficient-current-evidence
```

The fresh-observation Agent chose:

```text
game-body
```

Both Runs completed durably and were reloaded by a fresh Harness process from the same terminal receipt.

B0 therefore proves a concrete Agent-facing value for Presence evidence:

> **Current relation evidence resolves an uncertainty that safe historical evidence cannot resolve.**

The value is not that World maintains an always-on online roster. The value appears exactly when the Agent needs to decide whether a Body is currently usable for its next action.

This yields the first W5-B law:

```text
Historical Embodiment Knowledge
!=
Actionable Current Relation Knowledge
```

and a practical Agent-first pattern:

```text
Agent has a body-bound decision
        │
        ▼
identify the specific Body relation that matters
        │
        ▼
request fresh owner observation
        │
        ▼
reason with PRESENT / ABSENT-through-body / UNKNOWN
        │
        ▼
propose action
        │
        ▼
destination performs its own current admission
```

World does not choose the Body for the Agent and the Presence projection does not authorize the action.

## What B0 does not prove

B0 does not justify automatic prefetch of Presence for every Body, a subscription bus, heartbeat daemon, global location map or persistent online/offline flag. It also does not prove that every Agent decision needs Presence. The requirement is currently **decision-scoped**: query current relation only when a concrete next action depends on it.

[`../evidence/acceptance/w5b-b0-agent-current-relation-e40842d.json`](../evidence/acceptance/w5b-b0-agent-current-relation-e40842d.json) is the B0 commit-bound rerun receipt, SHA-256 `ec475b179f274595c78002e99d9760afe3dd25dff4048a4621ecefe6050e14a9`. It binds current Harness revision `98d295582dd9a5034413d87cc488089a1c75b138`, Game canonical plus the non-main W5-A destination-admission candidate, and the exact Security B1 closure. The historical-only Agent returned `insufficient-current-evidence`; the fresh-relation Agent selected `game-body`; both Runs were recovered from durable Harness receipts.

## B1: Security as a second bounded subject-active destination

B1 audited the current Security Windows KVM substrate rather than inventing a Presence daemon. Two existing physical channels were initially separate:

```text
Entity Migration
  ORDIVON_MIG
  continuityPayloadDigest
  real KVM Body
  guestClaimAuthority = not-used

Evaluation / Guest Runner
  ORDIVON_RUN
  bounded Guest action
  Host-readable result
```

A P1 Evaluation VM could not prove Entity activation because it is a different Body. B1 therefore required the same Entity KVM Body to carry both independently bound media.

### Physical acceptance

The accepted research path keeps materialization and activation evidence separate while co-launching them in one exact KVM Body:

```text
continuity subject claim
        ↓
Security stages ORDIVON_MIG
        │
        ├──── same materializationId + generation ────┐
        │                                             │
Security validates activation binding                │
  subjectRef                                          │
  migrationId                                        │
  entityId                                           │
  continuityPayloadDigest                            │
  materializationId                                  │
  generation                                         │
        ↓                                             │
Security stages ORDIVON_RUN                          │
        ↓                                             │
sealed Guest Runner                                  │
        ↓                                             │
fixed benign activation fixture                      │
        ↓                                             │
Guest reads ORDIVON_RUN + ORDIVON_MIG ───────────────┘
        ↓
Host verifies exact result + native Body currentness
```

The Security materialization receipt remained explicitly `guestClaimAuthority = not-used`; Guest output never became the authority for native Body liveness. Host QMP independently observed the exact Body running with no network device before the Guest action.

The fixed research fixture verified the exact `subjectRef`, `migrationId`, `entityId`, `continuityPayloadDigest`, `materializationId`, `generation` and one activation identity from inside the Guest. Host then verified the returned bounded result against the same activation coordinates.

Subject, migration, continuity digest, Body identity and generation substitution were rejected before activation. A historical result could not satisfy a fresh activation identity.

The accepted Guest action completed in 392 ms once the Runner invoked the fixture. The exact Body was still natively current when Host observed the completed result. Host then performed clean closure with QEMU closed, swtpm closed, ledger removed, run directory removed and zero residual objects.

### Corrected shutdown finding

Several exploratory runs originally treated QEMU shutdown as the success signal. A diagnostic later found a complete Guest result and `fixture-completed` log while QEMU was still running. Therefore:

```text
Guest bounded action completion
!=
Body shutdown completion
```

The earlier hot-plug experiments are consequently **inconclusive**, not a proof that post-materialization reactivation is impossible. B1 acceptance proves only bounded co-launch subject activation.

### What B1 proves

Security is now a second materially different **subject-active destination** for research purposes: destination admission, exact Body generation, Guest consumption and Host native observation can jointly prove one bounded Subject/Body occurrence.

This is deliberately weaker than saying Security is a second live-cognition destination. Game A3 binds a real Harness cognition instance to an Actor action; Security B1 binds a fixed destination activation fixture to a KVM Body. Cognition therefore cannot yet be promoted into the cross-domain minimum merely because Game needs it.

[`../evidence/acceptance/w5b-b1-security-active-destination-e40842d.json`](../evidence/acceptance/w5b-b1-security-active-destination-e40842d.json) is the World B1 acceptance receipt, SHA-256 `e5416f7097a51abfe9d3f52d736d70ad669461eb3d857afb09d7cb99c1d3a6d6`. It binds Security experiment revision `072ef473cea7e51c2347ef387b20fbd12b39f23d`, detached Security research candidate `22c94ff64182a018029c3cc2f94cd453e0266520`, a successful current production-control KVM run, the exact physical activation result and clean closure.

## B2: the cross-domain minimum is a proof interface

B2 compared Game A3 and Security B1 by intersection rather than union. The two domains have different native vocabularies:

```text
Game-only
  cognitionRunId
  planningId
  intentDigest

Security-only
  migrationId
  generation
  activationId
```

Requiring the union as one shared schema rejects both domains for fields they do not own. Cognition remains real and mandatory inside the Game admission path, but Security B1 proves a bounded Subject/Body occurrence without a Harness cognition Run. Migration/generation are mandatory Security coordinates but meaningless to Game. Planning/Intent are mandatory Game coordinates but meaningless to Security.

The smallest research intersection that survived the falsifiers is therefore six proof roles:

```text
subjectRef
ownerId
bodyRef
scopeDigest
admissionDigest
occurrenceDigest
```

These names do **not** define shared domain semantics. `scopeDigest` means “the owning domain's exact currentness/action scope evidence”; `admissionDigest` means “the owning domain's exact destination admission evidence”; `occurrenceDigest` means “the owning domain's bounded result/effect evidence.” World can bind these proof roles without understanding Game Planning or Security KVM generation.

### Owner-native falsifiers

Game rejected a Medic subject binding when it was presented for the `security-chen` Actor Body, and rejected the same r0 binding when replayed into r1 Planning. Security B1 independently rejected substitution of subject, migration, continuity digest, materialization Body and generation.

The generic omission falsifier then removed each of the six proof roles in turn. In both domain projections, omitting the corresponding role allowed exactly that coordinate to be substituted while the reduced comparison still matched. Keeping all six rejected each substitution. This is research evidence of necessity for the current two-domain intersection, not proof that no future representation can encode the same information differently.

`ownerId` is especially important because current Body, scope, admission and occurrence references are owner-native. Removing it would force World either to guess which system interprets a reference or to create the global Body/evidence namespace that W5 has repeatedly failed to justify.

`admissionDigest` and `occurrenceDigest` remain separate because an admitted action is not the same fact as an action that actually occurred. Game has missing-admission and native-effect evidence; Security has an exact activation binding and an independently observed Guest result.

### B2 result

> **Shared World invariant is a proof interface, not a universal domain model.**

The current W5-B cross-domain shape is therefore:

```text
             WORLD research proof role

subjectRef ────────────────────────────────┐
ownerId                                   │
bodyRef                                   │
scopeDigest          owner-authored       │
admissionDigest      evidence roles       │
occurrenceDigest                          │
                                           ▼
                         bounded Subject/Body occurrence

Game owner-native internals:      Harness Run / Planning / Intent / Actor / Fact
Security owner-native internals:  Migration / generation / activation / KVM / Guest result
```

No authority translation occurs. The common layer never turns a Game cognition into Security authority or a Security migration into Game semantics.

[`../evidence/acceptance/w5b-b2-cross-domain-minimum-5f5a253.json`](../evidence/acceptance/w5b-b2-cross-domain-minimum-5f5a253.json) is the mechanical cross-domain falsifier receipt, SHA-256 `7f9cdeb0f32a50954d06ec5d3083b386ac337b1c18f72b9229f5d26abb06dacb`. [`../evidence/acceptance/w5b-b2-cross-domain-minimum-acceptance-5f5a253.json`](../evidence/acceptance/w5b-b2-cross-domain-minimum-acceptance-5f5a253.json) is the owner-native supported B2 acceptance receipt, SHA-256 `3254a947dc98aaf757f5b63b7d834717d505b655df84722180825bf79ba1d62a`.

## W5-B stopping condition

B0 proved that fresh current relation evidence changes an Agent decision. B1 proved a second materially different bounded subject-active destination. B2 found a small cross-domain proof intersection without importing either domain's semantics. That is enough to close the current Presence research line **without** a production Presence service.

W5-B therefore stops here with three negative product decisions:

```text
no PresenceRegistry
no EmbodimentManager
no shared production occurrence schema yet
```

The six-coordinate proof interface remains research vocabulary until a third materially different consumer reproduces the same need. A future browser session, remote A2A Agent or physical device is a better next falsifier than another Game/Security refinement.

The next W5 line should move to **Discovery & Connection**: how an Agent discovers another body/entity/Agent, determines reachability, and establishes a relationship without letting discovery or reachability mint authority.
