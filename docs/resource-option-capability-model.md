---
schema_version: 1
id: world.resource-option-capability-model
title: Resource → Option → Capability World Model
type: doctrine
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
updated: 2026-08-15
summary: Defines how World reasons from observed resources to actionable options, redundancy, capability, effects, learning and further resource acquisition without inventing a global capability registry.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.start
  - world.authority
  - world.resource-opportunity-flywheel
---
# Resource → Option → Capability World Model

World should not treat “more resources” as synonymous with “more capability”. A resource becomes valuable only through a sequence of current, owner-grounded transformations.

The compact model is:

```text
Reality
  ↓ observe / discover
Resources
  ↓ owner truth + possessed authority + current access
Actionable Resources
  ↓ workload fit + current qualification
Options
  ↓ substitutability + failure-domain diversity
Optionality / Redundancy
  ↓ selection + coordination + composition
Capability
  ↓ bounded action
Effect
  ↓ evidence + attribution
Knowledge
  ↓ better acquisition / composition / retirement
More useful Resources and Options
```

This is a **planning and world-model law**, not a new durable global graph. Before an owner admits a consequence, resource/option selection remains recomputable. World persists exact consequence trajectories only at the existing owner-admission boundary.

## 1. Resource is not capability

A **Resource** is something in reality that may be useful: a provider endpoint, dataset, model, machine, account entitlement, tool, human contribution, network path, capital allocation, software component, or another system's exported capability.

Existence alone proves little:

```text
resource exists
!= authority to use it
!= reachable now
!= useful for this workload
!= reliable state transition
```

A resource may be known but inaccessible, authorized but currently unreachable, reachable but semantically useless, or useful only under conditions that are no longer current.

## 2. Actionable Resource requires relation evidence

A discovered resource becomes **actionable** only when the facts needed by the workload are established through their native owners.

Typical coordinates include:

- owner and current terms;
- possessed authority, not merely willingness to obtain it;
- current transport/reachability where transport is required;
- workload fit and semantic interface;
- capacity/quota where it can bind execution;
- cost and maintenance burden;
- trust/risk assumptions;
- relevant dependencies and failure domains;
- evidence currentness.

World may consume these facts, but it does not take ownership of them. Workstation still owns physical path truth; providers own provider capability/quota; domains own their own admission and state.

## 3. Option is the bridge between resource and capability

An **Option** is an actionable resource/path that can presently participate in a target state transition under known conditions.

Options are demand-scoped and time-scoped. A resource can be an option for one workload and irrelevant to another. A historical option can cease to be current without ceasing to exist as historical evidence.

```text
415 VPN transport variants
        ↓ qualification
some currently usable for OKX
        ↓ workload binding
current egress options
```

The 415 catalog entries are resource candidates. They are not 415 current Finance capabilities.

World should generally recompute options from current owner evidence instead of persisting an ambient global Option registry.

## 4. Redundancy is substitutable independent optionality

Resource abundance is not automatically redundancy.

For a target capability, useful redundancy requires at least:

```text
substitutability
× current actionability
× failure-domain independence
```

Two paths that can both reach the same destination may still share the same physical ISP, gateway, provider control plane or credential root. They provide some diversity, but not independence against the shared domain.

Therefore:

```text
Resource count = 100
Effective redundancy may still be ≈ 1
```

The current Finance egress example makes this concrete:

- SG OpenVPN-TCP and JP WireGuard provide protocol, node, endpoint and tunnel diversity;
- both currently descend through the same physical access domain;
- moving one member from `native-b` to `native-a` would not create physical redundancy because both route profiles share the same device/gateway/access-domain digest.

**Failure-domain diversity, not raw cardinality, is the decisive coordinate.** Failure-domain facts remain owner-native observations; World must not invent them from labels such as region or protocol.

## 5. Capability is a reliable state-transition possibility

A **Capability** is not merely a named feature. It is the presently supportable ability to cause or obtain a class of state transition under bounded conditions.

Conceptually:

```text
World State A
  + current options
  + authority
  + selection/composition policy
  + capacity
  + effect boundary
        ↓
World State B
```

A capability should be reasoned about with at least:

- preconditions/currentness;
- authority owner;
- available options and dependencies;
- capacity and concurrency limits;
- reliability and failure domains;
- cost/latency where material;
- effect identity and reconciliation requirements;
- evidence supporting the claim.

World does **not** need a universal `CapabilityManager` to preserve this law. Owner-native capability surfaces and demand-scoped projections remain preferable until a reproduced workload proves a missing shared responsibility.

## 6. Capacity is distinct from capability

Capability answers **can this transition be supported?** Capacity answers **how much / how often / how concurrently?**

Examples:

- an API may be reachable but limited to 100 requests/minute;
- a model may be callable but limited by token budget;
- one path may reach OKX but have poor latency or low sustained throughput;
- one executor may support an effect type but only one in-flight operation per bounded scope.

Two resources with the same nominal capability can therefore have materially different capacity. Resource acquisition that does not relieve the binding capacity constraint may have little marginal value.

## 7. Capability can become a higher-level resource

Resource and capability are relative to the system boundary.

A lower layer's exported capability is a higher layer's resource:

```text
Workstation scoped egress capability
        ↓
Finance network resource

Runtime contained execution capability
        ↓
Harness / domain execution resource

Harness cognition capability
        ↓
Game / Finance / Security resource
```

This creates a capability ecology rather than a flat project list. Each owner consumes selected lower-level capabilities and may export new capabilities/resources upward or sideways.

## 8. Capability can increase future resource acquisition

The flywheel is bidirectional:

```text
Resources → Options → Capability
Capability → better discovery/acquisition/composition → more Resources
```

Examples:

- better network capability widens reachable providers and data;
- better execution capability reduces the cost of integrating tools;
- better Security capability can permit safe use of a wider untrusted-resource universe;
- better Harness capability increases effective work per unit compute/token;
- better Finance capability may increase capital available for compute, data and infrastructure.

This is a positive feedback loop only when the resulting effects are correctly attributed. Capability claims without evidence do not justify resource expansion.

## 9. Knowledge closes the loop

Every attempted consumption should improve future selection when it yields attributable evidence.

```text
Option selected
→ consumed
→ effect/outcome observed
→ attribution
→ knowledge update
→ future ranking / acquisition / retirement changes
```

Knowledge includes negative results: a resource may be useful only on one path, one endpoint may repeatedly fail, two apparent routes may share the same failure domain, or a nominal entitlement may have no semantic workload value.

Historical evidence remains historical. Current action still requires current owner facts where currentness matters.

## 10. The five useful stocks

For reasoning—not as a new database schema—Ordivon can distinguish five stocks:

1. **Resource Capital** — reality we know about or possess that might be useful.
2. **Authority Capital** — current legitimate authority actually held.
3. **Option Capital** — current actionable alternatives across plausible future states.
4. **Capability Capital** — reliable state transitions the composed system can support.
5. **Knowledge Capital** — evidence about what works, under which conditions, and why.

They transform into one another but are not interchangeable. A large Resource Capital with weak authority or conversion ability can produce little Capability Capital.

## 11. Resource → Capability conversion rate is often the scarce variable

Modern external resource universes are often abundant: open-source software, public data, APIs, models, compute offers and network endpoints are plentiful.

The scarce process is frequently:

```text
discover
→ verify owner truth
→ acquire authority
→ establish current access
→ qualify
→ package
→ compose
→ consume semantically
→ attribute outcome
→ learn
```

This suggests a useful research variable: **Resource-to-Capability Conversion Rate (RCR)** — how efficiently the system converts candidate reality into proven reusable capability. RCR is currently a research concept, not a production metric; it should not be assigned a scalar until a workload demonstrates a defensible measurement.

## 12. More resources also create negative feedback

Resource abundance has costs:

- verification work;
- coordination complexity;
- maintenance and expiry;
- attack surface;
- state-space growth;
- stale evidence;
- selection latency;
- correlated failure hidden by superficial diversity.

So the correct objective is not `maximize resource count`.

A better qualitative objective is:

```text
Marginal World Value
≈ ΔCapability
 + ΔOptionality
 + ΔFailure-Domain Independence
 + ΔCapacity
 + ΔInformation
 - Acquisition/Maintenance Cost
 - Coordination Complexity
 - Risk
```

This explains why a second genuinely independent physical ISP may add more World value than a 143rd VPN node behind the same physical access domain.

## 13. World as a reality-to-action compiler

The old Sense → Connect → Act vocabulary remains useful when interpreted narrowly:

```text
Observation
  → discover resource universe and current evidence

Connection / relation evidence
  → establish whether a resource is presently actionable under owner-native facts

Action
  → select/compose current options and cross an exact owner admission/effect boundary
```

The deeper interpretation is:

> **World compiles an enormous external reality into a bounded, current, owner-grounded set of actionable possibilities for Agents.**

It is not trying to mirror all reality. It compresses reality into the evidence and choices that can change a decision while preserving who owns each fact.

This also sharpens the design rule:

> **Resources sink downward; capabilities surface upward.**

A Finance Agent should normally see `finance-okx = AVAILABLE`, not 415 provider transport variants. Workstation owns the candidate/path market underneath. Similarly, a higher layer should consume a narrow semantic capability instead of learning every mechanism used to construct it.

## 14. World compression is part of capability

The external resource universe can grow much faster than Agent attention. Therefore World must support compression and retirement, not only discovery.

Useful projections include concepts such as:

```text
cold candidate universe
qualified/warm options
hot active options
current bottleneck
shared failure domains
promotion/demotion candidates
```

These are owner/domain projections, not a mandate for one global World scheduler. The principle is to expose enough structure for good selection while keeping low-level mechanics below the consumer boundary.

## 15. Acquisition should maximize marginal capability, not catalog size

When deciding what to acquire next, ask:

1. Which current bottleneck does it relieve?
2. Does it create a new option for an already valuable state transition?
3. Does it add a genuinely independent failure domain?
4. Does it add capacity rather than duplicate idle capacity?
5. Does it unlock dependent resources or capabilities?
6. What coordination/maintenance/risk cost comes with it?
7. What evidence would falsify the expected value?

This is the resource-acquisition counterpart of Ordivon's broader problem-driven search discipline.

## 16. Non-promotions

This doctrine deliberately does **not** create:

- a global Capability registry;
- a universal Option database;
- a World-owned network router;
- a universal failure-domain ontology;
- one scalar “World value” score;
- a persistent pre-admission selection journal;
- a global resource ownership service.

Current `resource_discovery` already carries useful coordinates such as authority, acquisition option value, current transport, reuse potential, diversity potential and semantic consumption outcome. These remain demand-scoped planning projections. `diversity_potential` is only a candidate-level heuristic; it must never be interpreted as proof of redundancy or failure-domain independence.

A stronger shared abstraction should be promoted only after a named workload repeatedly fails because owner-native evidence plus current demand-scoped projection cannot answer the required selection question.

## 17. Reopening / research questions

The next research questions are empirical:

- Can owner-native failure-domain evidence improve fresh-Agent resource selection without creating a global graph?
- Can we measure RCR in a way that predicts actual capability growth rather than documentation activity?
- When does a large cold resource universe justify a warm qualified reservoir or hot active set?
- Which bottleneck signals best predict the marginal value of acquiring one more resource?
- How much independent optionality is enough before maintenance/coordination cost dominates?
- Can capability exported by one Ordivon owner be consumed as a resource by another without leaking implementation detail or authority?

Until those questions reproduce a real failure, the doctrine stays above the current narrow production boundary.
