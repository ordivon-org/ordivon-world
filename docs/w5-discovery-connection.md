---
schema_version: 1
id: world.w5.discovery-connection
title: W5-C Discovery & Connection Research Boundary
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
summary: W5-C studies how Agents discover and reach entities or peers without promoting discovery, transport reachability, protocol relationships or sessions into authority.
evidence_status: experimental
readiness: RESEARCH
applies_to:
  - ordivon-world
  - ordivon-game
  - ordivon-security
related:
  - world.w5.presence
  - world.w4.agency-authority-boundaries
---
# W5-C Discovery & Connection Research Boundary

## Starting question

W5-A and W5-B established how a subject can be bound to a Body for a bounded occurrence and why current Presence must remain owner-observed. W5-C asks the next external-world question:

> How does an Agent discover another entity, Body, endpoint or Agent, determine whether it can currently reach it, and establish whatever relation a protocol needs without letting discovery or transport state mint action authority?

Do not begin with `WorldLink`, a global Agent registry, a reachability database or a universal relationship manager. First determine whether the underlying concepts are actually one lifecycle.

## C0: the four concepts are orthogonal

C0 tested four notions that are easy to collapse:

```text
Discovery
Reachability
Relationship / Session
Authority / Admission
```

Current Game, Security and Message Delivery evidence rejects a universal monotonic ladder between them.

### Game: discovery does not mint peer affordance

Station Zero exposes owner-authored knowledge separately from owner-compiled action candidates. In the current initial snapshot, Engineer Imani knows both Medic Reyes and Security Chen with confirmed last-known zones and life state. The Engineer has no target-specific candidate for either known peer; its current candidate kinds are only `extract`, `guard`, `move` and `wait`.

A contrasting Hive Alpha context knows civilian Kade and, under the Hive's own capabilities/action rules, generates an `attack` candidate targeting that civilian.

Therefore:

```text
known entity
!=
generic peer action
```

Discovery is an epistemic input. Game's domain-native capability, range, topology and action compiler decide which affordances exist.

### Security: reachability and authority admission are orthogonal

Security Range exposes Actor Presence and effect authority as separate concepts. C0 explicitly marked `actor:red` as `unreachable` and submitted an effect with the exact owned authority, zone and `range-network` capability. `RangeSession.admit_effect()` admitted it.

Then the Actor was marked `active` and requested an ungranted `destroy-world` capability. Admission rejected it with `capability-not-granted`.

Thus both implications fail:

```text
unreachable
  does not erase valid authority admission

active / reachable
  does not mint missing authority
```

This is not an execution claim. Range admission intentionally answers whether one effect is authorized; it does not claim that the backend can currently execute the admitted effect.

### Message Delivery: a durable relationship object is not a universal prerequisite

Current production Message Delivery and Message Wire tests pass 19 of 19 cases including delivery, response-loss recovery, reconciliation and exact identity checks. The production proof objects contain message, source/destination World, provenance/payload, issuance, delivery and destination evidence coordinates. They contain no first-class relationship, session or `WorldLink` identity.

Transport-specific endpoint and reachability semantics remain provider-native. The result only rejects a mandatory durable World relationship object as a prerequisite for Message delivery/recovery.

This is consistent with retained W2 endpoint research: authenticated discovery, authenticated destination identity and direct delivery were sufficient, while a first-class `WorldLink` did not acquire an independent responsibility. Relay hops also could not be promoted into relationship identity merely because traffic passed through them.

## C0 model

The concepts should currently be treated as separate questions:

| Dimension | Question | Current owner pattern |
|---|---|---|
| Discovery | What entity/address/identity is known to exist? | domain/provider knowledge owner |
| Reachability | Is a current path, endpoint or Body usable/reachable? | transport/body/provider owner |
| Relationship / Session | Does this protocol need durable or scoped relation state? | protocol/domain owner, only when required |
| Authority / Admission | May this exact effect occur? | destination/domain authority owner |

No dimension automatically upgrades another.

The retained laws are:

```text
Discovery != Affordance != Authority
Reachability != Authority
Authority Admission != Execution Feasibility
Relationship/Session is optional owner-native protocol state
Traffic/relay traversal != Relationship Identity
```

World may bind owner-authored evidence when an Agent needs it, but must not create authority by interpreting discovery, reachability or relationship metadata.

## C0 evidence

[`../evidence/acceptance/w5c-c0-discovery-connection-d1a65a4.json`](../evidence/acceptance/w5c-c0-discovery-connection-d1a65a4.json) is the current C0 acceptance receipt. It combines a current Game discovery/affordance falsifier, a current Security reachability/authority falsifier, and the current 19-test Message Delivery/Wire production suite. The older W2 endpoint-discovery conclusion is referenced only as retained historical research, not as the current acceptance source.

## Product decision

C0 does **not** justify:

```text
WorldLink
GlobalAgentRegistry
GlobalReachabilityTable
UniversalRelationshipManager
```

A first-class relationship object should be introduced only when a real protocol or workload reproduces durable relationship-level responsibility that neither endpoint/owner can own cleanly.

## C1 next falsifier: Agent-facing current discovery/reachability value

C1 should ask a decision-scoped question analogous to W5-B B0:

> When a fresh Agent must contact or act toward a peer/endpoint, which current evidence actually changes its decision: discovery identity, reachability, a protocol-native session, authority, or some combination?

A useful experiment should compare historical/stale endpoint knowledge with a fresh owner-authored endpoint/reachability observation and require the Agent to choose among `contact`, `defer/rediscover`, or `not-authorized` without conflating those outcomes.

Prefer current Message endpoint semantics or a provider-native remote-Agent protocol. Do not build a registry merely to run C1.
