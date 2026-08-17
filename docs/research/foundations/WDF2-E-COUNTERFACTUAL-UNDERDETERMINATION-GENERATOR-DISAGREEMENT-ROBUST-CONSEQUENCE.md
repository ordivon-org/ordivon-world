# WDF2-E — Counterfactual Underdetermination / Generator Disagreement / Robust Consequence

Status: **complete for WDF2-E**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-E residuals:

```text
WDF2-F — Counterfactual Multi-Locus Surgery / Composition / Nested Dependence
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-D established that several generators can independently satisfy all known hard admissibility constraints while still yielding different counterfactual answers.

Therefore:

```text
MultipleAdmissibleGenerators != SemanticFailure
```

WDF2-E asks what follows when uniqueness is not earned.

The round must answer:

```text
What kinds of disagreement exist?
What kinds of equivalence exist?
What conclusions survive generator disagreement?
When is a point answer justified?
When are set/bound/interval/plural outputs required?
How should stochasticity remain separate from structural underdetermination?
How should evidence shrink admissible families without changing semantic type?
What does robustly-would / robustly-might mean when both generators and alternatives may be plural?
When does disagreement indicate model revision rather than ordinary uncertainty?
```

WDF2-E does **not** treat uncertainty as one scalar.

---

# 2. Initial anti-collapse law

The central danger is to compress everything into:

```text
CounterfactualUncertainty
```

This fails immediately.

At least the following are different:

```text
Generator-family underdetermination
Model-structure underdetermination
Parameter uncertainty
Counterfactual coupling underdetermination
Alternative-ordering underdetermination
Identity/correspondence underdetermination
Normality/normative underdetermination
Irreducible stochasticity
Sampling/statistical uncertainty
Measurement error
Model misspecification
Open-world model incompleteness
```

### Earned firewall E-U-1

```text
StructuralUnderdetermination
!= Stochasticity
!= StatisticalUncertainty
!= MeasurementError
!= ModelMisspecification
```

These can coexist, but they must not be represented as one generic probability number.

---

# 3. First decisive result — uncertainty lives at different truth roles

WDF2-E distinguishes three broad locations.

## 3.1 Semantic / structural multiplicity

There are several semantically admissible generators or counterfactual structures:

```text
G ∈ A_sem
```

No empirical weighting is implied.

---

## 3.2 Epistemic/model compatibility multiplicity

Evidence and background assumptions leave several models/generators compatible:

```text
G ∈ A_evid
```

where:

```text
A_evid ⊆ A_sem
```

if the evidential audit is coherent.

---

## 3.3 Within-generator aleatory plurality

One generator itself returns:

```text
multiple admissible outcomes
or
probability measure μ_G
```

because the modeled process is nondeterministic/stochastic.

### Earned firewall E-U-2

```text
UncertaintyOverWhichGenerator
!= ProbabilityWithinAGenerator
```

A probability over outcomes does not automatically define a probability over generator choice.

---

# 4. No automatic Bayesian collapse

One tempting move is:

```text
assign P(G_i)
then average all counterfactual distributions
```

WDF2-E rejects this as a foundation-level default.

Why:

1. some generator multiplicity is semantic rather than epistemic;
2. no prior over generators may be grounded;
3. averaging can hide mutually incompatible structural commitments;
4. the averaged distribution may correspond to no admissible generator;
5. a point mixture destroys information about worst/best/robust consequences.

### Earned firewall E-MIX-1

```text
GeneratorDisagreement != MixtureDistribution by default
```

Bayesian model averaging remains a legitimate **epistemic strategy when a justified prior/model posterior exists**. It is not the definition of counterfactual underdetermination.

---

# PART I — TAXONOMY OF COUNTERFACTUAL DISAGREEMENT

# 5. D-family — generator-family disagreement

Two admissible semantic architectures answer the same typed query differently.

Example:

```text
Q: If server had been healthy at t2, would r succeed?

G1: forward/local surgery
G2: backtracking accommodation
```

If the QueryRole remains genuinely ambiguous after all role constraints, both can survive.

This is **generator-family underdetermination**.

It is not stochasticity in the server.

---

# 6. M-family — model-structure disagreement

Two models use different causal/structural assumptions but both fit current domain constraints and evidence.

```text
M1: X -> Y
M2: X <- U -> Y with additional mechanism
```

or more subtly:

```text
same observed/interventional behavior
but different structural response functions / cross-world couplings
```

This is **model-structure underdetermination**.

Current causal research directly confirms that observational and even interventional equivalence need not imply counterfactual equivalence.

---

# 7. P-family — parameter uncertainty

Same generator family and same structural model class:

```text
G fixed
M fixed
θ uncertain
```

Counterfactual variation arises from uncertainty in parameters.

This is ordinary epistemic/model parameter uncertainty.

It should not be labeled generator disagreement.

---

# 8. C-family — coupling underdetermination

WDF2-B's binary-treatment construction already proved:

```text
same P(Y|do(X=0))
same P(Y|do(X=1))
```

can coexist with radically different:

```text
Joint(Y0,Y1)
```

The unknown object is the across-alternative coupling/correspondence.

This is **counterfactual coupling underdetermination**.

It can remain even after all interventional marginals are known exactly.

---

# 9. O-family — ordering / relevance disagreement

Two admissible Lewis-style or premise-style architectures preserve the same hard constraints but rank admissible alternatives differently.

```text
G1: prioritize historical match
G2: prioritize mechanism/rule preservation
```

if domain/query facts do not settle the ordering.

This is **selection-order underdetermination**.

---

# 10. X-family — identity/correspondence disagreement

Two domain-legitimate correspondence criteria can track the counterfactual subject differently.

Examples:

```text
same service by deployment role
vs
same binary by exact code identity
```

or institutional continuity under charter change.

This is not parameter error. It is a disagreement about the comparison relation required by the query.

---

# 11. N-family — normality/normative disagreement

Actual-causation/responsibility roles can admit several plausible normality/default orderings.

This can change attribution even when the physical counterfactual structure is identical.

```text
PhysicalResult fixed
NormalityOrdering differs
Attribution differs
```

This is **role-gated normative/normality underdetermination**.

---

# 12. S-family — irreducible stochasticity

A nondeterministic/probabilistic generator can say:

```text
G fixed
M fixed
alteration fixed
μ_G(Y) non-degenerate
```

No structural disagreement is implied.

Random outcome plurality can be a feature of the modeled Reality/process.

### Earned firewall E-S-1

```text
ManyPossibleOutcomesWithinG
!= ManyCandidateGenerators
```

---

# 13. E-family — sampling/statistical uncertainty

Even if the true counterfactual estimand were point identified under one fixed model, finite data make an estimator uncertain.

```text
EstimatorUncertainty != CounterfactualSemanticUnderdetermination
```

Confidence intervals answer a different question from partial-identification bounds.

---

# PART II — IDENTIFICATION SETS VS CONFIDENCE SETS

# 14. Identification region

Suppose a counterfactual quantity θ(G) is defined for every evidence-compatible model/generator:

```text
G ∈ A_evid
```

Then the identified set is schematically:

```text
Θ_ID = { θ(G) : G ∈ A_evid }
```

or its sharp closure/range under declared assumptions.

This is a set of values **compatible with the assumptions/evidence**, not a sampling-confidence statement.

---

# 15. Confidence set

A confidence procedure concerns repeated-sample coverage of an unknown target or identified set.

Therefore:

```text
IdentificationInterval != ConfidenceInterval
```

and:

```text
WideIdentificationRegion != NoisyEstimator by definition
```

One can have:

```text
infinite data
+ wide identification region
```

because the counterfactual structure remains underdetermined.

---

# 16. External research pressure

2025 partial-identification work on tiered benefit explicitly studies pure counterfactual quantities that remain unidentifiable without additional assumptions and derives sharp bounds rather than forcing point estimates.

Robust counterfactual MDP work similarly computes bounds across all compatible causal models instead of choosing one arbitrary SCM.

This is direct evidence that **set-valued counterfactual outputs are scientifically normal, not pathological**.

---

# 17. Earned firewall E-ID-1

```text
PointEstimate
!= PointIdentification
!= CounterfactualTruth
```

A point estimate can be numerically precise while the underlying quantity is not point identified.

---

# PART III — EQUIVALENCE IS QUERY-RELATIVE

# 18. One universal “same counterfactual model” relation fails

WDF2-E tests several equivalence strengths.

They form a hierarchy rather than one identity predicate.

---

# 19. Structural isomorphism

Two models can be isomorphic after variable/exogenous relabeling.

This is a strong internal structural relationship.

But structural isomorphism is not required for agreeing on the user's target query.

---

# 20. Full counterfactual equivalence

Two models are fully counterfactually equivalent relative to a language/query class when they agree on all counterfactual queries in that class.

2025 work on exogenous isomorphism explicitly studies a strong form of L3/counterfactual identifiability where all SCMs satisfying assumptions give consistent answers to all causal questions.

This is much stronger than needed for many practical queries.

---

# 21. Query equivalence

For one query Q:

```text
G1 ≡_Q G2
```

if both return the same result under Q's declared semantics.

They may disagree elsewhere.

---

# 22. Target-distribution equivalence

For target Y under Q:

```text
μ_G1(Y | Q) = μ_G2(Y | Q)
```

while internal alternative structure can differ.

This is weaker than full query-structure equivalence.

---

# 23. Verdict equivalence

For Boolean proposition C:

```text
Verdict_G1(C,Q) = Verdict_G2(C,Q)
```

while probabilities/distributions differ.

Example:

```text
G1: P(C)=0.99
G2: P(C)=0.72
```

can both support the same thresholded decision while not being distribution-equivalent.

---

# 24. Decision equivalence

Two generators can yield different counterfactual distributions but induce the same optimal action/policy under a specific utility/risk criterion.

```text
argmax_a U_G1(a) = argmax_a U_G2(a)
```

This is even coarser.

### Earned firewall E-EQ-1

```text
StructuralEquivalence
=> maybe CounterfactualEquivalence
=> maybe QueryEquivalence
=> maybe VerdictEquivalence
=> maybe DecisionEquivalence
```

but the converses generally fail.

---

# 25. Why equivalence must carry a scope

Without scope, saying:

```text
G1 and G2 are equivalent
```

is incomplete.

The missing type may be:

```text
structural
observational
interventional
full counterfactual
query-local
target-distribution
verdict
decision
```

This directly extends WDF0's criterion-relative identity discipline.

---

# PART IV — ROBUST CONSEQUENCE

# 26. Admissible generator family

Let:

```text
A = {G1,...,Gn,...}
```

be the generator/model family surviving WDF2-D semantic admissibility and whatever explicitly declared adequacy/evidence filter is relevant.

WDF2-E insists that the family carry provenance:

```text
A_sem
A_rep
A_evid
```

must not be silently conflated.

---

# 27. Result family

Each generator returns some result object:

```text
R_G(Q)
```

which may be:

```text
single alternative
set of alternatives
ordered alternatives
structural solutions
probability distribution
interval/bounds
failure/model-revision requirement
```

Robust consequence must operate over typed result semantics.

---

# 28. Boolean internal modal operators

For a generator G with relevant alternative set Alt_G(Q):

```text
Would_G(C) := ∀a ∈ Alt_G(Q), C(a)
Might_G(C) := ∃a ∈ Alt_G(Q), C(a)
```

This is schematic only; some generator families implement `would/might` differently.

The important point is the **within-generator quantifier**.

---

# 29. Across-generator quantifiers

Once A itself is plural, another quantifier appears.

This yields several non-equivalent notions.

## RobustWould

```text
RobustWould_A(C)
:= ∀G ∈ A, Would_G(C)
```

Expanded:

```text
∀G ∈ A, ∀a ∈ Alt_G(Q): C(a)
```

This is a strong invariant consequence.

---

# 30. RobustMight

There are at least two plausible meanings.

### Generator-universal might

```text
RobustMight_A(C)
:= ∀G ∈ A, Might_G(C)
```

Expanded:

```text
∀G ∈ A, ∃a ∈ Alt_G(Q): C(a)
```

Every admissible generator allows C somewhere.

### Merely admissible possibility

```text
SomeMight_A(C)
:= ∃G ∈ A, ∃a ∈ Alt_G(Q): C(a)
```

This is far weaker.

### Earned firewall E-MOD-1

```text
∀G∃a C
!= ∃G∃a C
```

Both must not be labeled simply `might`.

---

# 31. SomeWould

Another weak operator:

```text
SomeWould_A(C)
:= ∃G ∈ A, Would_G(C)
```

Expanded:

```text
∃G ∈ A, ∀a ∈ Alt_G(Q): C(a)
```

This can coexist with another admissible generator that guarantees not-C.

Therefore it is not a robust conclusion.

---

# 32. Quantifier lattice

For Boolean C, at minimum:

```text
∀G∀a C     robust would
∀G∃a C     robust might
∃G∀a C     some-generator would
∃G∃a C     some-generator might
```

These operators encode genuinely different information.

### Strong result

The phrase:

```text
robust counterfactual
```

is incomplete until both quantifier axes are declared.

---

# 33. Supervaluation analogy — useful but limited

There is a formal analogy to supervaluationism:

```text
statement robustly true
iff true under every admissible precisification/generator
```

Supervaluationist semantics uses truth across all admissible precisifications to preserve determinate consequences amid semantic indeterminacy.

WDF2-E borrows only the **invariance pattern**.

It does **not** infer that counterfactual underdetermination is linguistic vagueness.

### Earned firewall E-SUPER-1

```text
RobustAcrossAdmissibleGenerators
is formally analogous to supertruth
but
CounterfactualUnderdetermination != LinguisticVagueness
```

The admissible family here can represent scientific model/coupling underdetermination rather than incomplete word meaning.

---

# PART V — ROBUST PROBABILISTIC CONSEQUENCE

# 34. Generator-specific probability

Suppose each evidence-compatible generator produces:

```text
p_G = P_G(C | Q)
```

The family:

```text
{p_G : G ∈ A}
```

should generally remain visible.

---

# 35. Lower and upper counterfactual probability

Define:

```text
LowerP_A(C) = inf_G∈A P_G(C|Q)
UpperP_A(C) = sup_G∈A P_G(C|Q)
```

This is a robust envelope over generator/model disagreement.

It is not automatically a confidence interval.

It is not automatically an objective chance interval.

It is not automatically a Bayesian credible interval.

---

# 36. Set can be disconnected

A one-dimensional interval:

```text
[LowerP, UpperP]
```

can be only a hull.

The actual feasible set may be:

```text
[0.1,0.2] ∪ [0.8,0.9]
```

or a higher-dimensional nonconvex set.

Current partial-identification work explicitly produces feasible sets that can be disconnected.

### Earned firewall E-SET-1

```text
IdentificationSet != ConvexInterval by definition
```

Intervals are convenient summaries only when order/hull semantics are appropriate.

---

# 37. Bounds can be sharp or conservative

If:

```text
LowerP = exact inf over all admissible/evidence-compatible models
UpperP = exact sup
```

then the bounds are sharp relative to the assumption class.

If optimization/relaxation enlarges the set, the bounds are conservative.

This is an epistemic/computational status, not a different semantic counterfactual.

---

# 38. Robust threshold verdict

Suppose a decision criterion needs:

```text
P(C) ≥ τ
```

Then:

```text
if LowerP_A(C) ≥ τ:
    threshold verdict is robust across A

if UpperP_A(C) < τ:
    rejection is robust across A

otherwise:
    threshold verdict is generator-sensitive
```

This is one legitimate route from plural counterfactual distributions to a robust decision claim.

But τ comes from the downstream decision criterion, not counterfactual semantics itself.

---

# PART VI — ROBUST CONSEQUENCE VS ROBUST DECISION

# 39. Robust truth is stronger than robust action

It can happen that:

```text
P_G1(C)=0.55
P_G2(C)=0.85
```

so the generators disagree materially about C.

Yet both still recommend action a under the same utility/cost function.

Therefore:

```text
CounterfactualRobustness != DecisionRobustness
```

---

# 40. Decision robustness

Let:

```text
A*(G) = optimal action under generator G
```

A decision is strongly robust if:

```text
∀G ∈ A: A*(G)=a*
```

or if a* dominates according to an explicitly declared robust decision criterion.

This can hold even when counterfactual predictions differ.

---

# 41. Minimax is not semantic truth

Robust-control/robust-MDP methods often choose:

```text
argmax_policy min_G Value_G(policy)
```

This is a legitimate decision rule under ambiguity aversion.

But:

```text
WorstCaseDecisionCriterion != CounterfactualTruthSemantics
```

The minimax policy does not prove that the worst-case generator is the true generator.

This distinction is essential when importing robust-MDP results into World foundations.

---

# PART VII — EVIDENCE CAN FILTER, NOT REWRITE, SEMANTIC TYPE

# 42. Evidence filtering

Start with:

```text
A_sem
```

Then domain/model adequacy may yield:

```text
A_rep ⊆ A_sem
```

Evidence/identification assumptions may yield:

```text
A_evid ⊆ A_rep
```

The evidence does not change a forward generator into a backtracking generator.

It can rule out models/parameters or increase/decrease warrant.

---

# 43. Model posterior as a second layer

If one has a justified posterior:

```text
P(G | Evidence)
```

then posterior-weighted counterfactual quantities can be computed.

But the posterior must remain tagged as epistemic weighting over models/generators.

It is not the same as:

```text
P_G(Y | counterfactual)
```

inside each generator.

### Earned firewall E-PROB-1

```text
P(G | Evidence)
!= P_G(Y | CounterfactualQuery)
```

These are probabilities at different levels.

---

# 44. No double-counting

If uncertainty about θ is already integrated inside each model posterior and one then also ranges over θ as separate admissible models, the uncertainty can be counted twice.

A robust architecture must state whether uncertainty is represented as:

```text
set of models
probability over models
set of parameters within model
probability within model
```

and how these layers compose.

---

# PART VIII — WHEN SHOULD WORLD RETURN WHAT?

# 45. Point result

A point result is justified when the target is invariant across the declared admissible/evidence-compatible family at the required resolution.

Examples:

```text
all G yield same Boolean verdict
all G yield same scalar
all G yield same target distribution
```

depending on query requirement.

Full model equivalence is not necessary.

---

# 46. Finite plural result

Return explicit alternatives when:

```text
small number of qualitatively distinct admissible verdicts/models
```

and preserving their structure matters more than scalar summarization.

Example:

```text
forward consequence = success
backtracking diagnosis = failure
```

if role ambiguity itself remains unresolved.

---

# 47. Set-valued result

Return a set when the object has no natural total ordering or the feasible region is nonconvex/disconnected.

Examples:

```text
possible institutional statuses
possible causal graphs
possible policy classes
```

---

# 48. Interval/bounds

Return bounds when:

```text
target scalar/probability is ordered
and lower/upper envelope is decision-informative
```

but retain whether bounds are:

```text
sharp
conservative
assumption-relative
```

---

# 49. Partial order

Return a partial order when generators agree on some dominance relations but not a total ranking.

Example:

```text
policy A dominates C under all G
A vs B unresolved
B vs C unresolved
```

Forcing a total order would create information not present in the foundations/evidence.

---

# 50. Robust invariant verdict

Return a robust verdict when:

```text
all admissible generators entail the target conclusion
```

at the declared modal/probabilistic resolution.

This may be the highest-value output even when internal models disagree strongly.

---

# 51. ModelRevisionRequired

Return model revision rather than uncertainty when disagreement reveals that the current representation cannot type the comparison itself.

Examples:

```text
competing models lack a cross-model identity mapping
query targets an institutional status absent from one model
alteration changes ontology/variable domains so current generator result is undefined
```

### Earned firewall E-REV-1

```text
DisagreementWithinAdequateModels
!= ModelInadequacy
```

The first supports plural/bounded answers.
The second requires structural revision.

---

# PART IX — MATCHED DISAGREEMENT CASES

# 52. Case A — same interventional marginals, different individual effect

Generator/model family:

```text
G1 stable-response coupling
G2 flip-response coupling
```

Both satisfy:

```text
P(Y=1|do(X=0))=0.5
P(Y=1|do(X=1))=0.5
```

but disagree completely on who benefits/harmed.

Correct output without extra coupling assumption:

```text
individual response not point identified
```

not:

```text
average the two response tables
```

---

# 53. Case B — multiple causal models same MDP

Current robust counterfactual MDP work begins from exactly this condition:

```text
many causal models agree with observational + interventional MDP distributions
but induce different counterfactual transitions
```

The proposed response is tight bounds across compatible causal models and robust policy optimization.

This is a direct real research instance of WDF2-E's architecture.

---

# 54. Case C — deterministic vs nondeterministic causal representation

Suppose both representations match known factual/interventional behavior.

A deterministic SCM hides all randomness in latent variables; a nondeterministic model preserves irreducible stochasticity.

They may imply different individualized counterfactual couplings.

The August 2026 robust-policy work explicitly separates latent confounding from irreducible stochasticity using nondeterministic causal models.

Correct representation:

```text
model-family disagreement
+
within-model stochasticity
```

not one uncertainty scalar.

---

# 55. Case D — DAG ambiguity

Several plausible DAGs satisfy known constraints.

2025 causal-learning work derives bounds over a collection of plausible causal graphs rather than assuming the chosen DAG is correct.

If all DAGs imply positive effect:

```text
sign(effect) is robust
magnitude may be underdetermined
```

This demonstrates **resolution-relative robustness**.

---

# 56. Case E — software patch

Two adequate models differ in low-level implementation details but both predict:

```text
patch eliminates crash
```

They disagree on latency side effect.

Thus:

```text
CrashPrevention robust
LatencyImpact not robust
```

A counterfactual result should support field-wise/target-wise invariance rather than requiring whole-world agreement.

---

# 57. Case F — institution rule reform

Two legitimate legal/institutional interpretations agree that:

```text
Actor gains access
```

but disagree whether the status is:

```text
license
exception
provisional authority
```

If target query asks only operational access, a robust answer may exist.
If it asks legal status identity, disagreement remains.

Again:

```text
Robustness is query/grain relative.
```

---

# 58. Case G — Agent provider change

Two coupling assumptions for stochastic model M -> M' both preserve observed prompt/output facts but yield different token-level counterfactual continuations.

They may nevertheless agree that:

```text
both providers refuse unsafe request
```

while disagreeing on wording/reasoning trace.

Therefore robust semantic outcome can exist without token-level counterfactual equivalence.

---

# PART X — ROBUSTNESS HAS A RESOLUTION

# 59. Outcome projection

Let:

```text
π_target(R_G)
```

extract the aspect relevant to Q.

Two generators can disagree on full result while agreeing after projection.

Examples:

```text
exact trajectory differs
terminal success same

exact legal basis differs
operational access same

exact generated tokens differ
semantic decision same
```

---

# 60. Earned firewall E-RES-1

```text
FullCounterfactualAgreement
!= TargetRelevantAgreement
```

A robust result must declare its projection/grain.

Otherwise `all models agree` can be misleading.

---

# 61. Robustness monotonicity under coarsening

If a coarse projection forgets distinctions, agreement can increase.

Schematically:

```text
fine-grain disagreement
may become
coarse-grain agreement
```

The reverse need not hold.

This is not information creation; it is loss of resolution.

Therefore robust claims must not hide the coarsening operation.

---

# PART XI — ROBUSTNESS IS ASSUMPTION-RELATIVE

# 62. Admissible family depends on assumptions

Any robust statement:

```text
∀G ∈ A: C
```

is only as meaningful as A.

If A excludes plausible generators without justification, robust truth is fake.

If A includes semantically invalid generators, robust truth can become unnecessarily weak.

### Earned firewall E-ROB-1

```text
RobustAcrossA
!= UnconditionallyRobust
```

The admissible-family definition is part of provenance.

---

# 63. Assumption ladder

Counterfactual results can be reported under nested assumption sets:

```text
A0 minimal assumptions
A1 + monotonicity
A2 + rank preservation
A3 + specific coupling
```

Then one can observe how bounds/conclusions tighten.

This is preferable to silently injecting strong assumptions solely to get a point answer.

---

# 64. Strong assumptions can point-identify

Current research on counterfactual identifiability explicitly studies assumptions such as bijectivity/monotonicity that can make all SCMs in a class agree at the counterfactual level.

WDF2-E's rule:

```text
PointIdentificationFromStrongAssumption is legitimate
iff assumption provenance and truth role remain explicit.
```

It does not become assumption-free truth.

---

# PART XII — ROBUSTNESS VS SENSITIVITY

# 65. Robustness question

```text
Does conclusion C hold over all models/generators in A?
```

---

# 66. Sensitivity question

```text
How does result vary as assumption/model/coupling parameter changes?
```

Sensitivity can be informative even when robust invariance fails.

### Earned firewall E-SENS-1

```text
NotRobust != Uninformative
```

A narrow sensitivity region can be decision-useful even without exact invariance.

---

# 67. Breakpoint

One useful object is the smallest assumption perturbation that flips a target verdict.

Examples:

```text
how much unmeasured confounding needed to reverse sign?
how much coupling variation needed to change policy?
how much normality-order change needed to alter cause attribution?
```

This is downstream robustness analysis, not counterfactual semantics itself.

---

# PART XIII — MODEL MISSPECIFICATION VS UNDERDETERMINATION

# 68. Underdetermination

Several models survive known adequacy/evidence constraints.

```text
M1 adequate
M2 adequate
M1 != M2
```

---

# 69. Misspecification

A model contradicts observed/domain constraints or lacks required structures.

```text
RepAdeq(M)=false
```

It should be removed/revised, not retained as one possibility in the robust family.

---

# 70. Open-world incompleteness

Even if all current models agree, WDF0 prohibits claiming the family is complete unless completeness is justified.

Thus:

```text
AgreementAcrossCurrentModels
!= NecessarilyRealityTruth
```

Model-family closure remains provenance-sensitive.

---

# PART XIV — NEGATIVE AND POSITIVE ROBUST CONSEQUENCES

# 71. Robust positive

```text
∀G ∈ A: C
```

---

# 72. Robust negative

```text
∀G ∈ A: not-C
```

---

# 73. Genuine unresolved

```text
∃G1: C
∃G2: not-C
```

No robust Boolean verdict.

---

# 74. Robust disjunction

It can happen that no particular disjunct is robust but a disjunction is:

```text
∀G: C or D
```

while:

```text
not ∀G:C
not ∀G:D
```

This mirrors the useful structural insight behind supervaluation-style reasoning without importing its metaphysics.

Counterfactual uncertainty can therefore preserve nontrivial logical invariants even without point verdicts.

---

# PART XV — COUNTERFACTUAL ROBUSTNESS ALGEBRA

# 75. Target invariant set

For propositions Φ of interest:

```text
Inv(A,Q) = { φ ∈ Φ : ∀G ∈ A, Verdict_G(Q,φ) agrees }
```

This defines what is stable across generator disagreement.

The invariant set can be useful even when no full model is identified.

---

# 76. Numeric envelope

For numeric target f:

```text
Envelope_A(f) = { f(R_G(Q)) : G ∈ A }
```

Then report:

```text
exact set
or
inf/sup
or
convex hull
```

according to the target's mathematical structure and consumer need.

---

# 77. Order invariant

For actions a,b:

```text
RobustPreference_A(a,b)
iff
∀G ∈ A: U_G(a) ≥ U_G(b)
```

This yields a partial order across actions.

A complete ranking is not guaranteed.

---

# 78. Dominance frontier

Actions not robustly dominated under A form a robust candidate frontier.

This can be more faithful than forcing one robust-minimax action when the consumer has not declared ambiguity attitude.

---

# PART XVI — AMBIGUITY ATTITUDE IS A DECISION-LAYER INPUT

# 79. Maximin

```text
choose a maximizing worst-case value
```

---

# 80. Minimax regret

```text
choose action minimizing worst-case regret
```

---

# 81. Bayesian averaging

```text
choose expected utility under model posterior
```

---

# 82. Set-valued choice

```text
retain all undominated actions
```

These are downstream choice attitudes.

### Earned firewall E-DEC-1

```text
AmbiguityAttitude != CounterfactualSemantics
```

World foundations should expose the uncertainty structure before a consumer chooses how to act under it.

---

# PART XVII — DELETION TESTS

# 83. Delete generator-family distinction

**FAIL**.

Structural disagreement collapses into ordinary randomness.

---

# 84. Collapse model uncertainty into outcome probability

**FAIL**.

Mixture can hide incompatible mechanisms and unsupported prior weighting.

---

# 85. Require point output whenever a mean exists

**FAIL**.

Mean can correspond to no admissible generator and erase bounds/disconnected feasible sets.

---

# 86. Replace identification set with confidence interval

**FAIL**.

Infinite-data underidentification remains possible.

---

# 87. Require full model equivalence before any robust statement

**FAIL**.

Models can disagree internally while target consequence is invariant.

---

# 88. Call any ∃G possibility “robust might”

**FAIL**.

`∃G∃a` is too weak to express generator-robust possibility.

---

# 89. Define robust would as majority vote

**FAIL** as foundation semantics.

No measure/weight over generator family is automatically given.

---

# 90. Treat worst-case generator as true

**FAIL**.

Worst-case is a decision construction, not a truth claim.

---

# 91. Delete model-revision escape

**FAIL**.

Some disagreement comes from incompatible/unmappable representation, not ordinary model ambiguity.

---

# 92. Require unique generator for semantic success

**FAIL**.

Current causal/counterfactual research supplies direct counterexamples where observational/interventional constraints leave multiple L3/counterfactual models.

---

# PART XVIII — EXTERNAL RESEARCH PRESSURE

# 93. Robust counterfactual MDPs

Lally, Kazemi and Paoletti's 2025 robust counterfactual MDP work starts from the fact that many causal models can agree with an MDP's observational and interventional distributions while yielding different counterfactual distributions.

Instead of fixing one causal model, they derive tight bounds on counterfactual transition probabilities across compatible models and optimize policies robustly against the resulting interval uncertainty.

WDF2-E uses this as a direct worked example of:

```text
InterventionalAgreement != CounterfactualAgreement
BoundsAcrossCompatibleModels can be preferable to arbitrary point selection
```

---

# 94. Nondeterministic robust policy optimization

The August 2026 work by Lally, Kazemi, Paoletti, Watson and Beckers extends robust counterfactual policy optimization to probabilistic nondeterministic causal models.

Its foundational significance here is the explicit separation of:

```text
latent confounding
```

from:

```text
irreducible stochasticity
```

while still performing sensitivity/robust counterfactual optimization.

This independently supports WDF2-E's typed uncertainty architecture.

---

# 95. Nondeterministic causal models

Beckers' 2025 PMLR paper drops deterministic uniqueness assumptions and permits multiple counterfactual solutions.

This proves that plurality can live **inside one causal model**, independently of generator/model uncertainty across competing models.

---

# 96. Counterfactual influence in MDPs

Kazemi et al. 2025 show that counterfactual trajectories can cease to be influenced by the factual path and become interventional.

This reinforces that individualized correspondence/coupling is a semantic dimension whose adequacy can vary across generators.

---

# 97. Counterfactual identifiability

Chen and Du 2025 investigate strong L3/counterfactual identifiability requiring all SCMs satisfying assumptions to provide consistent causal answers.

This supports WDF2-E's distinction between:

```text
full counterfactual equivalence
```

and weaker query/target equivalence.

---

# 98. Counterfactually equivalent learned SCMs

Balgi, Peña and Daoud 2024 emphasize that observational/interventional equivalence is not enough for individual causal effects; counterfactual equivalence requires stronger conditions.

This again supports the equivalence hierarchy.

---

# 99. Counterfactual graphical inference

Correa and Bareinboim 2025 develop graphical constraints and a counterfactual calculus extending intervention-level graphical reasoning into multi-world/counterfactual queries.

This shows that counterfactual query structure itself can have constraints richer than ordinary interventional distributions.

---

# 100. Partial identification

De Aguas et al. 2025 derive sharp bounds for a counterfactual benefit quantity that is not point identified without extra assumptions.

Padh et al. 2025 derive causal-query bounds across collections of plausible DAGs.

These are direct scientific precedents for set/bound outputs under model ambiguity.

---

# 101. Supervaluation analogy

The philosophy of vagueness uses truth across all admissible precisifications to recover determinate consequences despite unresolved precisification.

WDF2-E borrows this only as a mathematical analogy for invariant consequences across an admissible model/generator family.

It explicitly rejects the inference that causal/counterfactual underdetermination is thereby semantic vagueness.

---

# PART XIX — WDF0 / WDF1 REOPEN AUDIT

# 102. WDF0

No FoundationReopenCondition fires.

WDF2-E strongly reinforces:

```text
Model != Reality
PredictiveSuccess != OntologicalTruth
WithinModelUpdate != StructuralModelRevision
Same_X != Same_Y without criterion
Relative != Subjective
```

The equivalence hierarchy is a direct application of WDF0 criterion-relative identity.

The open-world warning that current model agreement is not proof of complete Reality coverage also remains intact.

WDF0 stays frozen.

---

# 103. WDF1

No FoundationReopenCondition fires.

WDF1 already required separation of:

```text
modal support
probability weight
probability interpretation
model provenance
evidence provenance
```

WDF2-E's two-axis modal quantifiers and probability-layer separation are consistent extensions.

WDF1 stays frozen.

---

# PART XX — RECONSTRUCTION AFTER WDF2-E

# 104. Counterfactual answer object — research grammar

A faithful research answer may need:

```text
QueryFrame
AdmissibleGeneratorFamily provenance
TargetProjection/grain
Generator-local result family
Agreement/Disagreement classification
Robust invariant consequences
Numeric/set-valued envelope when relevant
Identification status
Statistical uncertainty status
Model-revision warnings
Decision-layer handoff only if requested
```

This is **not** a production schema.

---

# 105. Robust answer ladder

A useful conceptual ladder is:

```text
Level 0: no well-typed counterfactual query
Level 1: semantically admissible generator family exists
Level 2: adequate model family exists
Level 3: target set/envelope identified relative to assumptions
Level 4: robust qualitative consequence exists
Level 5: point target identified
Level 6: statistical estimate with uncertainty
Level 7: downstream action/decision under declared ambiguity attitude
```

Higher level does not erase provenance from lower levels.

---

# 106. Strong result — robust consequence can exceed model identification

One need not identify the true model to know some counterfactual consequence robustly.

If:

```text
∀G ∈ A_evid: C
```

then C is invariant relative to A_evid even though:

```text
true G is not identified.
```

This is epistemically valuable.

### Earned firewall E-RC-1

```text
RobustConsequence does not require FullModelIdentification
```

---

# 107. Strong result — point identification is target-relative

Two models can disagree on full counterfactual trajectories yet agree exactly on one target scalar.

Thus:

```text
TargetIdentified != ModelIdentified
```

This is the counterfactual analogue of asking only as much structure as the query requires.

---

# 108. Strong result — robust might is not dual to robust would under naive generator quantification

Within one classical model:

```text
Might C ≈ not Would not-C
```

may hold under suitable semantics.

Across generator families, depending on quantifier choice:

```text
∀G∃a C
```

is not generally the simple negation of:

```text
∀G∀a not-C
```

without careful domain/nonemptiness assumptions.

Therefore WDF2 must not assume ordinary modal dualities automatically survive robustification.

This remains an open logical detail for later freeze/falsification.

---

# 109. Strong result — robust consequence requires a family boundary

The deepest fragility is not the quantifier but the set A.

If `admissible` is under-specified, robust truth is meaningless.

Therefore WDF2-D and WDF2-E are inseparable:

```text
Admissibility architecture defines family A.
Robustness architecture quantifies over A.
```

Neither can substitute for the other.

---

# PART XXI — LARGEST REMAINING RESIDUAL

# 110. Why multi-locus surgery now rises to the top

WDF2-E resolves how to remain honest when one alteration/query has multiple admissible generators.

But most real counterfactuals are not one-coordinate surgeries.

Examples:

```text
change policy + tool access + environment
change rule + credential + enforcement
change model provider + prompt + memory
change software version + config + dependency
change treatment + mediator policy over time
```

WDF2-A/B typed these loci separately but did not yet solve their composition.

Once several changes occur together, new problems appear:

```text
order effects
nested counterfactuals
cross-world substitution
conflicting preservation requirements
intervention interference
policy adaptation
structural revision halfway through evaluation
identity across sequential surgeries
```

This residual is now more upstream than another general uncertainty round.

---

# 111. Composition cannot be assumed commutative

For alterations Δ1 and Δ2:

```text
Apply(Δ2, Apply(Δ1,M))
```

need not equal:

```text
Apply(Δ1, Apply(Δ2,M))
```

Examples:

```text
change rule then evaluate credential
vs
change credential then change rule
```

or:

```text
change policy then model provider
vs
change provider then derive policy
```

Thus:

```text
MultiAlterationSet != UnorderedBagOfIndependentChanges
```

---

# 112. Nested counterfactual pressure

Counterfactual language can contain nested/dependent structures such as:

```text
If X had been x, then if Y had later been y, would Z...?
```

or mediation-style cross-world quantities involving outcomes under one intervention evaluated with mediator values from another.

These raise composition and cross-world consistency questions not solved by WDF2-E robust envelopes alone.

---

# 113. Exact next round

The next canonical round is therefore:

# **WDF2-F — Counterfactual Multi-Locus Surgery / Composition / Nested Dependence**

WDF2-F should test:

```text
simultaneous vs sequential surgery
commutativity / noncommutativity
idempotence
conflicting alterations
alteration-precedence rules
preservation-profile recomputation after surgery
policy/mechanism/rule/model changes in one query
nested counterfactual operators
cross-world substitution / mediation pressure
identity/correspondence across sequential transformations
probability coupling under multiple interventions
model revision during a counterfactual chain
```

It must preserve WDF2-E's underdetermination architecture rather than resolving composition ambiguity through arbitrary ordering.

Only WDF2-F residuals may determine WDF2-G.

---

# 114. Production disposition

No production changes are admitted.

Do **not** add:

```text
CounterfactualUncertainty type
RobustCounterfactualEngine
CredalCounterfactual object
GeneratorEnsemble
CounterfactualBounds API
RobustWould operator
```

Current production remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

The Counterfactual Foundation is not yet frozen.

---

# 115. Closeout

```text
WDF2-E: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D reopen: NO
Production refactor: NO

StructuralUnderdetermination != Stochasticity
IdentificationInterval != ConfidenceInterval
UncertaintyOverGenerator != ProbabilityWithinGenerator
GeneratorDisagreement != MixtureDistribution by default
StructuralEquivalence != QueryEquivalence != DecisionEquivalence
RobustAcrossA != UnconditionallyRobust
CounterfactualRobustness != DecisionRobustness
WorstCaseDecisionCriterion != CounterfactualTruth
ModelDisagreement != ModelInadequacy
RobustConsequence does not require FullModelIdentification
TargetIdentified != ModelIdentified
FullCounterfactualAgreement != TargetRelevantAgreement

RobustWould_A(C) := ∀G ∈ A, Would_G(C)
RobustMight_A(C) := ∀G ∈ A, Might_G(C)
SomeWould_A(C) := ∃G ∈ A, Would_G(C)
SomeMight_A(C) := ∃G ∈ A, Might_G(C)

Exact next round:
WDF2-F — Counterfactual Multi-Locus Surgery / Composition / Nested Dependence
```

Compressed result:

> **WDF2-E treats counterfactual disagreement as structured information rather than a defect to be averaged away. Several generators can remain admissible for distinct reasons, and their disagreement must be typed separately from irreducible stochasticity, parameter uncertainty and sampling error. Counterfactual equivalence is itself scoped: models may differ structurally yet agree on one target, verdict or decision. Robust consequence is therefore defined relative to an explicit admissible family and target grain. Boolean robust claims require two quantifier layers—across generators and within each generator's alternative set—while probabilistic claims naturally produce lower/upper envelopes or richer feasible sets. Identification bounds are not confidence intervals; minimax policies are not truth claims; model averaging requires an independently justified epistemic weighting. The strongest positive result is that full model identification is unnecessary for useful counterfactual knowledge: conclusions invariant across all admissible evidence-compatible generators can be robust even when the true generator remains unidentified. After this underdetermination architecture is in place, the largest remaining structural gap is composition: real counterfactuals often alter several loci at once or sequentially, and those surgeries need not commute. WDF2 therefore advances next to multi-locus surgery, composition and nested dependence.**
