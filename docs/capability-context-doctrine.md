---
schema_version: 2
id: world.capability-context-doctrine
title: Actor / Environment / Institution / Capability Doctrine
type: doctrine
profile: research
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
summary: Compact CF0-CF9 doctrine for reasoning about realized performance, relational capability, environment exposure, institutional rules, capability production, endogenous selection, causal transport and feedback without creating universal Capability, Environment, Institution or causal-graph state.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.resource-option-capability-model
  - world.research.closeouts
---
# Actor / Environment / Institution / Capability Doctrine

This document is the compressed reusable result of Capability Field CF0–CF9.

It does **not** add a new production object, schema, service, registry, state machine or causal graph. It constrains how World and its consumers should reason when a decision depends on Actor capability, current environment, institutional rules or historical exposure.

## 1. Capability is relational and query-bound

World's existing definition remains authoritative:

> **Capability is the supported ability of a declared system boundary to cause or obtain a class of state transition under bounded conditions.**

Therefore:

```text
Capability
!= intrinsic scalar trait
!= feature label
!= one performance score
```

A current capability claim inherits at least the boundary, target transition, relevant conditions, horizon/currentness and supporting evidence of the observations that justify it.

Use existing:

```text
ResourceFor
ActionableResourceFor
Requirement / Assignment / Constraint
Option
Capability
```

rather than creating a `CapabilityField` record.

## 2. Realized performance is not Actor capability identity

One outcome episode can support a bounded claim about the system and conditions actually tested.

It does not automatically establish:

```text
independent Actor capability
transfer capability
recovery capability
retained learning
causal mechanism
intrinsic ranking against another Actor
```

When a stronger claim matters, obtain evidence that discriminates it: varied support, transfer, recovery, support removal, reconstruction, intervention or another appropriate owner-native test.

If the stronger claim is not identified, preserve `UNKNOWN`.

## 3. Environment is a causal role, not a complete object

Environment means the realized external conditions/exposures relevant to the current question: physical state, tools, information, peers, infrastructure, workload, path state, shocks or other owner-native facts.

Environment is query-relative and intentionally incomplete.

Do not create or require a universal:

```text
EnvironmentSnapshot
EnvironmentState
complete dependency closure
```

Use the smallest current owner-native facts whose deletion changes the target decision.

## 4. Institution is a causal role for durable rule/process relations

Institution deserves separate causal attention when a durable repeated rule/process changes a counterfactual about:

```text
allocation / access
authority / admission
incentive / cost
enforcement / sanction
ownership / appropriation
coordination / information
recovery / exit
```

Institutional state may be part of an Actor's realized environment. The distinction exists because changing a rule/authority/ownership/recovery process is a different intervention from changing a physical path or adding skill.

These mechanism roles are diagnostic. They do not define one universal Institution schema or truth owner.

## 5. Static default: project from owner-native truth

For a current decision, prefer:

```text
owner-native Claims / Events / authority / access / evidence
        + Actor/system boundary
        + target transition
        + demand/load
        + as_of
        + relevant requirements/assignments/constraints
        ↓
current ResourceFor / Actionability / Option / Capability
```

A strong static interaction model is often sufficient. Do not activate history, selection or coevolution merely because they are theoretically possible.

## 6. Mechanism decomposition is for action localization, not ontology growth

A generic interaction model may correctly predict `no action` while hiding why.

When the next intervention depends on the cause, localize the blocker:

```text
missing access?
missing authority?
wrong incentive/cost?
unenforced rule?
wrong ownership relation?
coordination/search failure?
unsafe recovery/exit?
physical environment failure?
missing complement/capability?
```

Expose enough mechanism to choose the right owner and treatment. Stop there.

## 7. Capability production and current expression are different claims

Current support can change performance without changing retained Actor state.

```text
expression / exercisability
= current conditions change current supported performance/Options
```

Capability production is stronger:

```text
prior exposure / practice / feedback / investment
→ later capability state changes
```

A production claim requires evidence about the later capability state and a causal design strong enough for the claim. Otherwise classify the result as expression, candidate production, or `UNKNOWN`.

“Capability unmasking” is a derived expression case, not a new state primitive.

## 8. Joint-system gain and retained component capability may move differently

A Human–Agent, Agent–Tool or multi-owner system can become more capable while one component's independent capability stays flat or declines.

Possible patterns include:

```text
complementation: joint ↑, retained/recovery ↑
substitution/dependence: joint ↑, independent ↓/flat
expression: current supported output ↑, retained state not established as changed
```

None is universally good or bad. The relevant objective, recovery need, verification burden, consequence and future support availability determine the decision.

## 9. Exposure assignment is separate from exposure effect

Observed environments are partly produced by selection:

```text
Actor → environment choice
Institution → admission/exclusion
search/information/cost → assignment
common causes → assignment + outcome
exit/survival → observed composition
```

Therefore keep three questions separate:

1. effect of the environment/institution after entry;
2. effect of changing the assignment/search/admission mechanism;
3. effect of changed entrant composition on aggregate outcomes.

An observed environment/outcome gap is not automatically a causal exposure effect.

## 10. Causal claims must match the identified query

Do not let evidence answer a stronger question than its design and assumptions identify.

Keep distinct:

```text
association / description
prediction
intervention effect
counterfactual
longitudinal/dynamic policy effect
mechanism / Attribution
transport to a target domain
coevolution / feedback
```

Randomization is powerful for the assigned intervention it tests, but it does not automatically identify mechanism, long-horizon state change, target transport or feedback.

Observational causal work should make the target intervention/comparison and assignment assumptions explicit rather than treating adjusted association as causal by default.

## 11. Source evidence does not become target truth automatically

For transport, state separately:

```text
source claim
source conditions/population
proposed stable mechanism/invariance
known source-target differences/moderators
target claim
target evidence still required
negative-transfer boundary
```

Structural analogies are useful for generating questions and falsifiers. They do not establish target effect sizes or owner-native truth.

Controlled Agent experiments can test system distinctions without becoming Human learning evidence. Human experiments can constrain Ordivon hypotheses without automatically deciding an individual user's policy.

## 12. Feedback and coevolution require direction-specific Attribution

A repeated sequence such as:

```text
Capability → Resources → Options → Capability
```

or:

```text
Institution → resource distribution → power → future Institution
```

is a causal hypothesis, not an accounting identity.

Promote a feedback claim only when time-indexed owner-native states, direction, rival causes and Attribution evidence support it, and when feedback changes a prediction/intervention relative to treating the future trajectory as externally supplied.

Shared loop shape does not imply shared mechanism.

## 13. Descriptive and normative questions remain separate

This doctrine can represent how rules/environments change capability and outcomes. It does not define the institution that *should* be chosen.

Output, autonomy, fairness, distribution, resilience, option value, innovation, maintenance, safety and recovery can move in different directions.

No universal `InstitutionQuality` or `CapabilityValue` scalar follows.

## 14. Compact decision procedure

When a capability/context question appears, ask only what is needed:

1. **What boundary and transition are we claiming capability for?**
2. **What current owner-native facts make it feasible or infeasible?**
3. **Would changing the Actor, physical/environment support, or a durable rule/process change the decision?**
4. **Is the observed result current expression or evidence of later capability production?**
5. **How was the exposure/Actor assignment generated?**
6. **What causal query is actually identified by the evidence?**
7. **If importing evidence, what mechanism is assumed to transport and what differs?**
8. **Does feedback matter on this horizon, or can future context be treated as exogenous?**
9. **What remains UNKNOWN, and can more evidence still change the action?**

Load no broader theory when direct owner facts already answer the decision.

## 15. Explicit non-promotions

CF0–CF9 does not justify:

```text
CapabilityField object/service
intrinsic global Capability score
EnvironmentSnapshot / complete environment state
universal Institution entity/schema/service
InstitutionQuality scalar
universal transition-topology model
EnvironmentalCapital stock
universal Actor learning/update equation
SelectionScore / automatic deconfounder
Global CausalGraph / causal confidence service
universal TransportContract service
UniversalCoevolutionGraph / Power scalar
normative institution optimizer
```

## 16. Final compression

The smallest durable formulation is:

> **Treat capability as a boundary-, transition- and condition-relative supported relation over owner-native Reality. Treat Environment and Institution as query-activated causal roles, not universal objects. Separate realized performance from retained capability, current expression from capability production, and exposure assignment from exposure effect. Admit causal and transported claims only to the strength identified by their design, assumptions and target boundary. Treat feedback as a direction-specific attributed hypothesis. Add mechanism detail only when it changes the next intervention, owner, recovery, attribution or promotion decision.**
