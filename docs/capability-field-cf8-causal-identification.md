# CF8 — Causal Identification and Intervention Admission

Status: **COMPLETE**

## 1. CF8 changes the question from “what model fits?” to “what claim is identified?”

CF1–CF7 showed that the same observed pattern can support very different claims. CF8 therefore treats causal reasoning as a query/admission problem.

A compact causal question names:

```text
population / Actor boundary
+ exposure or intervention
+ comparator
+ assignment process
+ outcome
+ horizon
+ estimand / target claim
+ assumptions
+ evidence
+ source/target domain if transported
```

This is a research grammar, not a database schema.

## 2. Different causal queries require different evidence

### Association / description

```text
P(Y | X)
```

Useful for observation and prediction. It does not by itself answer what happens if `X` is changed.

### Intervention

```text
P(Y | do(X))
```

Asks the effect of changing an exposure/action under a stated comparison.

### Counterfactual

Asks what would have happened to a unit/population under an alternative condition. It requires stronger structural assumptions than merely observing association.

### Dynamic policy

Asks about a sequence of interventions where later treatment/exposure can depend on evolving state. Time-varying confounding makes this different from one static exposure coefficient.

### Mechanism / attribution

Asks why the effect occurred or which path/owner deserves causal credit. An identified total effect does not automatically identify the mechanism.

### Transport

Asks whether a source causal claim applies to a changed target environment/population. Source internal validity and target transportability are separate burdens.

### Coevolution

Asks whether earlier effects change later rule/resource/Actor state and thereby future effects. This requires direction-specific time-indexed evidence rather than a one-time treatment contrast.

## 3. Randomization is powerful but not a universal answer

A well-designed randomized experiment can identify an assigned intervention for its study population under its assumptions. It may still leave unresolved:

- treatment uptake/noncompliance;
- mechanism attribution;
- longer-horizon state change;
- target-population transport;
- post-treatment selection;
- institution feedback;
- outcomes never measured by the experiment.

Therefore CF8 rejects a single evidence ladder where `RCT` automatically dominates every design for every causal query.

## 4. Observational causal analysis must specify the hypothetical intervention

Hernán and Robins' target-trial framework provides a useful discipline: when observational data are used for a causal decision, make explicit the trial/question being emulated—eligibility, strategies, assignment, follow-up, outcome and causal contrast—rather than treating regression adjustment as causal by default.

For time-varying treatments/confounders, g-methods such as the g-formula exist precisely because naive conditioning can fail under longitudinal feedback.

CF8 imports the specification discipline, not a health-specific analysis stack.

## 5. Causal admission states

CF8 retains categorical states rather than a confidence scalar:

```text
DESCRIPTIVE
PREDICTIVE_CONDITIONAL
CAUSAL_ASSUMPTION_BOUND
IDENTIFIED_INTERVENTION
PARTIALLY_IDENTIFIED
TRANSPORTED_UNDER_EXPLICIT_ASSUMPTIONS
UNKNOWN / NOT_IDENTIFIED
```

One claim can move between these states as evidence or assumptions change. Historical evidence is not rewritten.

## 6. Attribution remains stricter than outcome difference

World R10 already requires Attribution to be a separate causal/credit Claim. CF8 sharpens its admission test:

```text
Outcome difference
+ temporal order
+ plausible mechanism
```

is still insufficient if selection, common causes, alternative mechanisms or external shocks remain decision-relevant rivals.

The correct result can be:

```text
Effect identified
Mechanism UNKNOWN
```

or:

```text
Association strong
Intervention effect UNKNOWN
```

## 7. Evidence acquisition stopping rule

More evidence is not automatically better. Continue only when an unresolved causal distinction can still change:

- action/intervention choice;
- admission or recovery;
- capability-production versus expression classification;
- attribution;
- transport decision;
- promotion to reusable Knowledge.

If no feasible evidence can resolve the claim at acceptable cost/consequence, preserve bounded uncertainty instead of manufacturing a point conclusion.

## 8. CF8 result

The durable rule is:

> **Never ask evidence to prove a stronger causal query than the design, assignment process, assumptions, outcome/horizon and transport boundary can identify. Make the target intervention/comparison explicit; separate total effect, mechanism, dynamic state change and transport; preserve partially identified or UNKNOWN states when the query is not resolved.**

No global causal graph, causal confidence score or automatic causal-admission service is earned.
