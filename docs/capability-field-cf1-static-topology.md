# CF1 — Minimum Static Capability Topology

Status: **COMPLETE**
Base: CF0 frozen problem space at `803f54a`
Scope: static current-state reasoning only.

## 1. Question

CF1 asks the smallest question that survived CF0:

> Given an Actor/system boundary, a target transition and current Reality, what is the minimum structure required to derive current ResourceFor, Actionability, Option and effective Capability without inventing a global Environment/Institution ontology?

The strongest baseline is current World doctrine itself:

```text
owner-native Claims / Events / authority / access / quantities / evidence
        + actor boundary
        + target transition
        + demand/load
        + as_of
        + requirements / assignments / native constraints
        ↓
ResourceFor / ActionableResourceFor
        ↓
Option
        ↓
boundary-relative Capability
```

## 2. Static result

CF1 finds **no missing production primitive**.

The minimum static analytical query is:

```text
StaticCapabilityQuery(
    actor_or_system_boundary,
    target_transition,
    demand_or_load,
    as_of,
    relevant owner-native claims/events,
    requirements,
    assignments,
    constraints,
    evidence envelope
)
```

This is notation for a bounded question, not a schema.

### Environment does not need to become a mandatory tuple coordinate

Environment matters when a realized external condition changes a current prediction: network path, available tool, peer/information exposure, physical condition, infrastructure, workload, shock, or another query-relevant exposure.

But those facts already arrive through owner-native claims and constraints. If the current decision needs only `path current = false`, a new object such as:

```text
Environment{id, pathState, ...}
```

adds no truth and risks pretending that the omitted environment is complete.

### Institution does not need to become a mandatory tuple coordinate

Institution matters when the counterfactual depends on a durable rule/process relation: authority, access, admissibility, incentive, enforcement, ownership/appropriation, coordination, recovery or exit.

Those are real causal roles, but their facts have different owners. A legal permission, Finance admission rule, Security authority manifest and provider entitlement should not become fields of one World `Institution` record.

## 3. Why M2 remains the strong static baseline

M0 wins when standardized conditions leave an actor-state difference as the only decision-relevant distinction.

M1 wins when context contributes an independent fixed main effect.

M2 is required when complements or interactions alter feasibility:

```text
skill × tool
authority × target
resource A × resource B
path × provider
ownership rule × effect
```

But M2 is a **functional claim** that the current output/feasible transition depends jointly on those inputs. It does not require storing one `F(X,E,I,R,D)` object.

## 4. Deletion results

The 12-case CF1 matrix gives the following dispositions:

- deleting actor/system boundary fails;
- deleting transition/demand scope fails;
- deleting owner-native authority/currentness fails;
- deleting explicit conjunction/constraint logic fails when composition matters;
- deleting Environment as a causal role fails for path/tool/infrastructure/exposure counterfactuals;
- deleting Institution as a causal role fails for authority/ownership/recovery counterfactuals;
- **adding mandatory Environment/Institution records does not improve any frozen current decision**;
- requiring complete Environment closure blocks bounded truthful decisions;
- decomposed transition topology adds no static predictive distinction over strong M2.

## 5. The important compression

The static theory is therefore not:

```text
Actor × Environment × Institution × Resource → CapabilityField
```

It is thinner:

```text
Reality remains owner-native
        ↓
one named actor/transition/demand/as_of query
        ↓
select only the owner-native relations that can change that query
        ↓
derive current Option / Capability
```

Environment and Institution are **causal-role labels used to ask better counterfactual questions**, not new truth owners.

## 6. CF1 boundary

CF1 cannot answer:

- whether prior exposure changed Actor state;
- whether high-capability actors selected the observed environment;
- whether an institution caused the observed outcome;
- whether a static interaction transports to another population;
- whether rules change endogenously after outcomes.

Those are CF4–CF8 questions, not reasons to expand the static schema.

## 7. CF2 handoff

With static representation contracted, the next question becomes epistemic:

> What evidence distinguishes retained Actor capability, situated/joint-system effective Capability, and one realized performance episode?
