---
schema_version: 2
id: world.resource-option-capability-model
title: Resource / Option / Capability Doctrine
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
updated: 2026-08-16
summary: Canonical R10 doctrine distilled from R0-R9 falsification and cross-domain dogfood: keep owner-native truth native, treat Resource/Actionability/Option and conditional ecology relations as context-bound projections, preserve Action/Effect/Outcome/Attribution/Knowledge boundaries, and promote shared machinery only after repeated missing executable responsibility is proven.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.start
  - world.authority
  - world.resource-opportunity-flywheel
  - world.resource-ontology-r9-cross-domain-dogfood
---
# Resource / Option / Capability Doctrine

This document is the canonical production-facing result of Resource Ontology R0-R10.

The research path is intentionally much larger than the doctrine. R0-R9 preserve the census, theory comparison, falsifiers, matrices, negative results and real owner dogfood that earned these laws. This document keeps only the distinctions whose deletion changed a real decision.

The compact topology is:

```text
OWNER-NATIVE REALITY / TRUTH
Events · Claims · authority · access · quantities · evidence
                    │
                    ▼
          CONTEXTUAL PROJECTION
Resource / ResourceFor / ActionableResourceFor / Option
                    │
                    ▼
             BOUNDED FEASIBILITY
Requirements + Assignments + native Constraints
                    │
                    ▼
             DECISION / ACTION
                    │
                    ▼
            OWNER-NATIVE EFFECT
                    │
                    ▼
             DOMAIN OUTCOME
                    │
                    ▼
          ATTRIBUTION if supported
                    │
                    ▼
        KNOWLEDGE promotion if earned
```

This is **not** a universal persisted schema, lifecycle, graph or service.

---

## 1. Resource is a supported relation, not a global record

Relative to a declared actor/system boundary, a **Resource** is an identifiable aspect of Reality for which sufficient current evidence supports at least one bounded, admissible path by which that actor can intentionally enroll the aspect as a means, input or enabling relation for a class of future state transitions.

The precise form is conceptually:

```text
ResourceFor(actor, aspect, transition, as_of)
```

and the coarse form:

```text
Resource(actor, aspect, as_of)
```

is an existential projection over at least one supported transition witness.

A Resource can be:

- bytes, compute, a machine or network path;
- a provider/API/model/tool;
- a right, entitlement, account or relationship;
- capital or attention;
- evidence or knowledge;
- another owner's exported capability.

Resource is therefore not an object class and not a record containing every fact about a thing.

Deleting any of these three coordinates changes real decisions:

```text
actor/system boundary
exact aspect identity
at least one supported transition witness
```

---

## 2. Native truth stays with its native owner

World may consume and join truth from multiple owners. It must not become a second source authority for facts those owners can reconcile directly.

Examples:

```text
Workstation   owns physical path / resolver / failure-domain observations
Runtime       owns execution/result/recovery facts inside its effect boundary
Finance       owns financial admission, capital and performance semantics
Game          owns game rules, reducer effects and product-state semantics
Studio        owns Production / Output / creative review semantics
Security      owns bounded security experiment/admission semantics
Human         owns Human research/measurement policy and Human-specific outcomes
Providers     own provider-native terms, capability and quota claims
```

World's normal role is projection and boundary binding:

```text
owner-native Claims / Events
          ↓
context-specific World question
          ↓
projected relation / admissible external action
```

A repeated label across projects does not transfer truth ownership.

---

## 3. Candidate labels are hypotheses; capability truth needs claim-bound evidence

Discovery optimizes recall. Therefore a `ResourceCandidate` may carry capability labels supplied by an aggregator, index or discovery process.

Those labels are **not semantic capability truth**.

For the current generic discovery pipeline:

```text
ResourceCandidate.capabilities
    = discovery / ranking hypotheses

OwnerVerification.verified_capabilities
    = current owner-attested capability claims
```

A current demand-fit projection may use owner-attested capabilities. It must not convert an aggregator/candidate label into `consumable-now` merely because owner identity, terms and interface were separately verified.

This is the R10 correction to the R3/R8/R9 claim-level provenance falsifier.

The more general evidence law is:

> **Evidence is a provenance/method/time-bound support, contradiction, bounding or unresolved relation to an explicit Claim. Resource-level provenance does not establish every transition/capability claim about the resource.**

Owner-attested capability fields are the smallest current implementation treatment. They are not a global Capability registry or EvidenceGraph.

---

## 4. Historical truth is not current applicability

A Resource does not have one universal lifecycle state.

Keep native history:

```text
observed
authorized
acquired
materialized
used
revoked
expired
failed
succeeded
```

as owner-native Events/Claims where those facts matter.

Then derive current projections as-of a particular time.

The same historical Resource can simultaneously be:

```text
ActionableFor(demand A)
not ActionableFor(demand B)
UNKNOWN for demand C because one required claim is stale
```

Therefore there is no canonical:

```text
Resource.current
Resource.state
Resource.lifecycle
```

and later evidence must not silently rewrite earlier point-in-time decisions.

---

## 5. Resource, Actionable Resource and Option answer different questions

A Resource may exist before the actor currently possesses every authority, path or complement needed to use it.

**ActionableResourceFor** answers whether the conditions required for a target demand are sufficiently established now:

```text
ResourceFor
+ required current authority
+ required current access/materialization
+ semantic fit
+ binding constraints
→ ActionableResourceFor
```

**Option** is the selectable feasible relation available to a decision-maker under the current demand/context.

Thus:

```text
Resource
≠ Actionable Resource
≠ Option
≠ selected Action
```

A gated but credibly acquirable entitlement may be a Resource without being currently actionable. A current actionable resource may be an Option but remain unselected.

World normally recomputes these projections rather than persisting global registries.

---

## 6. Feasibility is conjunctive, but composition stays owner-local

Real transitions frequently require several conditions at once.

Use the conceptual vocabulary:

```text
Requirement
Assignment
Constraint
Projection
```

For target transition `T`:

```text
R(T)  = explicit hard requirements
A     = contextual assignment of current ResourceFor/ActionableResourceFor projections
C     = material compatibility / authority / quantity / time / semantic constraints

Feasible(T, demand, load, as_of)
    = requirements satisfied under A and C
```

This does not imply a global `DependencyGraph` or `CompositionEngine`.

Finance admission, Game reducers, Studio Production checks, Security experiment admission and Human experiment protocols already own their real conjunctions.

World should gain a shared composition executor only after multiple materially different consumers reproduce the same missing executable responsibility above their owner boundaries.

---

## 7. Capacity is conditional native quantity, not one scalar

Capability asks whether a transition can be supported. Capacity-like facts answer how much, how often, how concurrently, for how long or under what budget.

Examples include:

```text
Finance   minimum notional / deployable capital / leverage / survival budget
Game      Zone slots / provider concurrency / latency / attention
Runtime   task/process/output/time ceilings
Human     review time / interruption burden / recording cost
Network   throughput / quota / path capacity
```

These facts have different units, clocks, owners and recovery semantics.

Use capacity/rate/budget only when deleting the quantity would change:

- feasibility;
- throughput;
- contention;
- risk/survival;
- waiting/burden;
- recovery.

A useful conceptual query is:

```text
CapacityFor(actor, transition, demand_or_load, as_of)
```

but there is no global scalar `Resource.capacity` and no `CapacityService` today.

---

## 8. Substitution, complementarity, bottlenecks and redundancy are derived relations

Two resources are substitutes only when they are alternative feasible assignments for the **same requirement under the same relevant context**.

Complementarity follows when joint assignment satisfies requirements or changes the transition in a way neither assignment supplies alone.

A bottleneck is the currently binding constraint under requested load—not a permanent resource type.

Redundancy requires more than cardinality:

```text
>= 2 feasible substitutes
+ enough current capacity for the requested load
+ sufficient independence under a declared disturbance/failure class
```

Therefore:

```text
2 endpoints        != redundancy
2 API keys         != concurrency if they are the same key
415 route variants != 415 independent capabilities
region diversity   != physical failure-domain independence
```

Failure-domain evidence remains with the owner that can observe it.

---

## 9. Capability is boundary-relative supported transition ability

A **Capability** is the supported ability of a system boundary to cause or obtain a class of state transition under bounded conditions.

It is not merely a feature label and does not require a universal `CapabilityManager`.

A lower owner's exported capability may become a higher owner's Resource:

```text
Workstation scoped egress capability
        ↓
Finance network Resource

Runtime contained execution capability
        ↓
Harness / domain execution Resource

Harness cognition capability
        ↓
Game / Finance / Security Resource
```

The export does not transfer internal state, authority, evidence ownership or lifecycle to the consumer.

The consumer normally needs the narrow semantic capability, not every mechanism that constructs it.

---

## 10. Decision, Action, Effect, Outcome, Attribution and Knowledge must not collapse

These are different semantic boundaries:

### Decision / selection

Chooses an Option or feasible assignment. It can exist without external dispatch.

### Action

An identity-bound admitted/committed attempt to cause or obtain a transition.

### Effect

The direct consequence that the effect owner can truthfully establish inside its boundary, including:

```text
success
failure
no-effect
partial
UNKNOWN
```

### Outcome

A domain-owned evaluation over Effects plus relevant exogenous facts under an objective, observer, horizon, comparison and evidence context.

### Attribution

A separate causal/credit Claim about why an Outcome occurred.

### Knowledge

A deliberately promoted reusable Claim that changes future prediction, selection or policy.

Therefore:

```text
process exit 0
!= semantic completion
!= domain success
!= causal value-added
!= reusable Knowledge
```

One Action may produce many Effects. One Outcome may depend on many Effects and exogenous Reality. Failed or invalid episodes can still produce Knowledge if the domain deliberately promotes a bounded reusable conclusion.

---

## 11. UNKNOWN and negative evidence are first-class

Missing evidence is not falsehood.

Stale evidence is not current truth.

A failed trial, rejected treatment or explicit no-observation result can remain valuable Evidence without becoming a universal negative claim.

For an absence claim, ask whether the relevant observable surfaces were sufficiently covered.

Examples:

```text
empty Capital Ledger
!= proof of no external capital flow

no downstream effect observed in bounded Security surfaces
!= package harmless everywhere

provider read failure
!= weak financial carrier
```

Do not force every projection into complete-looking success/failure states when the supported answer is `UNKNOWN`, `STALE` or `insufficient evidence`.

---

## 12. Evidence transport and acquisition are decision-scoped

Source evidence may be useful outside its original context, but it does not automatically become target truth.

Use the least specialized evidence that can resolve the real decision:

```text
external/source evidence
→ mechanism / moderator / boundary analysis
→ owner/system structural transport analysis
→ natural target dogfood
→ bounded residual direct evidence only if still decision-relevant
```

When deciding whether to collect more evidence, consider:

- current uncertainty;
- target applicability;
- evidence independence;
- coverage;
- consequence of being wrong;
- reversibility;
- cost/burden;
- whether the result can actually change action.

Measurement availability alone is not a reason to measure.

No universal persisted Transfer Contract is currently earned.

---

## 13. Persistence follows ownership and recovery need

Persist owner-native history where consequence identity, recovery, audit or future semantic promotion requires it.

Examples already justified in World include exact external dispatch/trajectory identities and receipts across effect boundaries.

Do **not** persist by default:

- every discovered Resource relation;
- every current Option;
- every feasible planning composition;
- every intermediate score;
- every critique;
- every possible causal edge;
- every outcome projection;
- every capability label.

Before owner admission, much of resource planning is intentionally recomputable.

---

## 14. Shared semantics do not imply shared machinery

R9 dogfood across Finance, Game, Studio, Security and Human found many repeated semantic laws but no new repeated shared executable owner.

The extraction test is:

```text
repeated semantics
+ repeated missing executable responsibility
+ owner-local resolution fails
+ moving responsibility downward reduces total system complexity
→ candidate shared production seam
```

Without all four, keep the semantic law and leave the mechanism owner-local.

This rule is intentionally hard to satisfy because duplicated authority and giant optional-field schemas are expensive long-term failure modes.

---

## 15. Conditional query templates

The following concepts are useful **only when the question activates them**. They are not mandatory Resource fields.

| Query template | Activate when |
|---|---|
| access / transport / materialization | current path, bytes or interface determines exercisability |
| requirements / assignments / constraints | a transition needs conjunction, compatibility or admission checks |
| capacity / rate / budget | quantity changes feasibility or bottleneck |
| substitution / redundancy | alternatives are compared under a named purpose/load/disturbance |
| evidence coverage | completeness or absence claims depend on observable surfaces |
| source → target transport | evidence is applied outside its original population/context |
| reversibility / consequence / VOI | deciding whether more evidence is worth acquiring |
| exact composition identity | replay/recovery/effect identity depends on exact members/versions |
| consumption accounting | stock/flow/quota/budget continuity matters for that resource family |

If the query does not require one of these relations, do not add it merely for schema completeness.

---

## 16. Explicit non-promotions

R0-R9 evidence does **not** justify these production structures:

```text
universal Resource lifecycle/state machine
global persisted Resource registry/entity
universal CapabilityManager/object
global dependency/composition graph or engine
global Capacity scalar/service
global EvidenceGraph / BeliefStore / confidence service
universal persisted Transfer Contract
generic Outcome / Attribution service
universal Resource value / maturity scalar
generic cross-domain consumer / workflow platform
```

They may be reconsidered only when the extraction test in §14 is satisfied by real consumers.

---

## 17. Current production implication after `resource_discovery` retirement

At the R10 closeout the generic Resource Opportunity Board remained a bounded planning surface. The 2026-08-27 deletion tournament re-adjudicated that historical approximation against current Ordivon owner capability and found no remaining natural production consumer: real acquisition, value, admission and composition decisions are already owner/domain-local, while the generic module was consumed only by its own tests and compatibility facade.

The executable `resource_discovery` / `ResourceOpportunityBoard` surface is therefore retired from World production. Its surviving semantics remain useful as reasoning constraints:

- candidate/discovery vocabulary is not owner truth;
- owner-native current evidence must ground a capability claim;
- Resource / Actionability / Option are relation- and demand-relative;
- transport/currentness/value clocks remain distinct;
- scalar ranking is at most a consumer-local heuristic, never World authority;
- joint composition stays with the owner that owns the actual requirements/constraints;
- shared machinery re-enters only through the R10 extraction law.

This is a responsibility-placement change, not a rejection of the R0–R10 research. The detailed planning implementation remains recoverable through Git history and the R0–R10 evidence corpus. Current recovery starts at [`research/world/RESOURCE-AND-CAPABILITY.md`](research/world/RESOURCE-AND-CAPABILITY.md).

---

## 18. Final R10 doctrine

The smallest durable formulation is:

> **Keep Reality truth with the owner that can reconcile it. Treat Resource, Actionability, Option and conditional ecology concepts as context-bound supported relations over that truth. Require explicit claim-bound evidence for semantic transition claims. Compose only through explicit requirements and native constraints. Keep Decision/Action, Effect, domain Outcome, Attribution and Knowledge promotion separate. Promote shared machinery only after multiple materially different consumers reproduce the same missing executable responsibility above owner boundaries.**

This is the canonical Resource/Option/Capability doctrine. The R0-R9 research artifacts remain the evidence history and falsification record behind it.
