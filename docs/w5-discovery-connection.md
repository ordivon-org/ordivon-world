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

## C1: current evidence changes Agent contact decisions

C1 tested whether the C0 distinctions matter to a fresh Agent rather than only to code structure. The experiment used the current Harness independent no-Tool DeepSeek profile, current Message issuance semantics, and a live loopback destination endpoint. Three Runs were kept separate:

```text
A  historical discovery
   + source issuance authority
   + current reachability unknown
   → rediscover-or-defer

B  known endpoint identity
   + fresh reachable observation
   + source issuance authority
   → contact

C  known endpoint identity
   + fresh reachable observation
   + no source issuance authority
   → not-authorized
```

All three current Harness Runs completed with one Provider call and zero Runtime Tool calls. Durable Harness stores were reopened after completion and independently returned the same terminal receipts and structured decisions.

This gives the C0 dimensions different Agent-facing roles:

- discovery tells the Agent what identity/address it currently knows about;
- fresh reachability changes whether an immediate contact attempt is physically plausible;
- source issuance authority decides whether the Message effect is admissible at all.

Fresh reachability never upgrades missing authority.

### The `contact` decision was followed by one real Message effect

The authorized case was not left as a model answer. Before effect dispatch, the caller made another nonce-bound health observation against endpoint generation `endpoint-generation:w5c-c1:r2`. `MessageDeliveryWireDestination.deliver()` then sent the exact current Message plan through the live endpoint.

The destination owner's event log recorded exactly one Message delivery POST with:

```text
messageId      = message:w5c:c1
planDigest     = sha256:bf9157d263b8cf4df728c152aaa20b79ae45c2a47788c52ef310d9605053570e
source issuance= sha256:91387f85683d7429879f8a84e180f74dcccfc8eb231ed89ee0b998f3ba804cab
```

The no-authority case was then presented to the current Message production API as an unissued delivery bundle. It was rejected before transport with:

```text
production Message delivery requires a source issuance receipt
```

Its transport request list remained empty. Therefore:

```text
fresh reachability
!=
permission to send
```

### A useful failure inside the experiment

The authorized caller process failed *after* the external Message effect because the research script tried to access a nonexistent convenience property, `MessageDeliveryReceipt.digest`, after `deliver()` had already returned a valid receipt object.

The correct recovery action was not redispatch. World first reconciled the physical owner evidence. The endpoint log showed exactly one POST. The expected receipt identity was then reconstructed from the exact current Message contract with `sha256_digest(receipt.to_dict())`.

This adds a concrete instance of an existing World law:

```text
caller process failure after external effect
!=
effect absence
```

A failed local wrapper is not retry authorization.

## C1 retained laws

C1 supports:

```text
Discovery freshness has epistemic value, not authority value.
Reachability freshness changes contact feasibility, not issuance authority.
Authority determines whether a contact effect may be attempted.
Agent decision evidence != external effect evidence.
Caller process failure after external effect != effect absence.
```

Current discovery/reachability evidence should therefore be obtained when an Agent decision needs it. Mirroring all known endpoints and reachability state into a World-global registry would create stale duplicated truth without adding authority.

[`../evidence/acceptance/w5c-c1-agent-contact-decision-c393f19.json`](../evidence/acceptance/w5c-c1-agent-contact-decision-c393f19.json) is the C1 acceptance receipt, SHA-256 `299d43e1cadc1c8066391f2ec9663da042f52f9464998815692e04cb42d63951`. It binds current World `c393f192cbd5ba1c1c3cce1ae216fe0146bc9bb7`, Harness `487e0ac8eb945256842347b5371cbbdd70bfce55`, all three durable Agent decisions, the live endpoint generation, exact Message plan/source issuance identities, endpoint owner POST count and the no-authority pre-transport rejection.

## W5-C stopping condition

C0 proves that discovery, reachability, relationship/session and authority are not one monotonic lifecycle. C1 proves that fresh discovery/reachability evidence has real decision value while authority remains independent, and that a valid contact can complete through current Message semantics without first-class World relationship state.

There is currently no reproduced responsibility for a World-owned durable relationship/session object. W5-C therefore stops here with the existing negative product decisions:

```text
no WorldLink
no GlobalAgentRegistry
no GlobalDiscoveryRegistry
no GlobalReachabilityTable
no UniversalRelationshipManager
```

A future real protocol-native workload may reopen the relationship/session question. Examples include a long-lived negotiated peer session or a remote-Agent protocol whose native task/session lifecycle creates responsibility that neither endpoint can own cleanly. Until then, such state belongs to the protocol/domain that actually has it.

The next W5 line should move to **Interaction**: whether Resource, Message and Entity are merely three implemented features or evidence of a smaller set of recurring Agent↔World and Agent↔Agent interaction primitives.
