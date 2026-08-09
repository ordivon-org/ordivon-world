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

## B2 next falsifier: cross-domain minimum

B2 should compare Game A3 and Security B1 without taking the union of their fields. The question is:

> Which relation coordinates are genuinely unavoidable in both domains, and which are only owner-native semantics?

The candidate common core is deliberately small:

```text
subject reference
body owner + body identity
owner-native scope/currentness fence
destination admission evidence
bounded occurrence/result evidence
```

Game-specific cognition Run identity, Planning/Intent coordinates, and Security-specific migration/generation coordinates should remain owner-native unless a falsifier proves they belong in the shared core.

B2 must try to break this candidate from both directions. If removing a field permits subject/body/action substitution in either domain, the field may be invariant. If a field cannot be interpreted honestly by the other domain without importing foreign semantics, it must stay domain-owned.

Do not create a production `EmbodimentBinding` merely because two domains now have positive evidence. First prove a minimal intersection that both can consume without authority translation or schema laundering.
