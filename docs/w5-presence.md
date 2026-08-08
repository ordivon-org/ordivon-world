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

The fresh input retained the same history and added only the W5-A A4-P1 owner-authored current relation projections:

```text
Game Actor Body    → present-within-scope
Security KVM Body A → absent-through-body
```

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

B0 also uses Game as the only destination where a subject/cognition/body action relation has been positively admitted. Security can currently prove native carrier currentness/absence but still cannot prove Guest-side subject activation. W5-B therefore still needs a second materially different active destination before any shared production Presence contract is credible.

## B1 next falsifier: second active destination

The preferred next candidate is Security because it already owns a real KVM Body and strong native recovery evidence. B1 should first audit whether the existing Guest/host channel can prove a bounded subject activation without granting Guest self-report authority over native liveness.

The target chain is:

```text
external continuity subject claim
        ↓
Security-owned KVM carrier
        ↓
Guest consumes exact bounded subject binding
        ↓
Guest performs a bounded observable domain action
        ↓
Security independently observes the native effect/current carrier
        ↓
owner-authored current subject/body observation
```

A Guest claim alone is insufficient. Security must retain native ownership of Body/liveness truth and must distinguish “Guest says I am subject X” from “Security admitted subject X for this bounded carrier/action scope.”

If the current Security architecture lacks a trustworthy activation cut point, B1 should report that structural gap rather than add a generic World Presence API.
