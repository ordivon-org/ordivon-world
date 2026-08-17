# WDF2-N — Counterfactual Baseline / Reference Class / Contrast / Comparison Set

Status: **complete for WDF2-N**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D/E/F/G/H/I/J/K/L/M remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-N residuals:

```text
WDF2-O — Counterfactual Effect / Estimand / Aggregation / Heterogeneity
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-M showed that normality claims are incomplete without reference scope. WDF2-N asks the more general question:

> **Relative to what comparison, population, baseline, foil, treatment strategy, time, regime and comparison set is a counterfactual claim being evaluated?**

The round must distinguish:

```text
FactualAnchor
ComparisonBaseline
ReferenceValue
ReferenceClass / ReferencePopulation
TargetPopulation
AlternativeDomain
ComparisonSet
ContrastiveFoil
ControlCondition
NoTreatment
StatusQuo
StandardPolicy / StandardOfCare
BestAlternative
NormativeBaseline
HistoricalBaseline
TemporalBaseline
ModelVersionBaseline
```

No member is preselected as universal.

---

# 2. First anti-collapse law

### Earned firewall N-TYPE-1

```text
FactualAnchor
!= ComparisonBaseline
!= ReferenceClass
!= ComparisonSet
!= ContrastiveFoil
```

A counterfactual can be anchored in actuality, evaluated against a nonactual baseline, averaged over a target population, and explained relative to a foil—all simultaneously.

---

# 3. Why the distinction matters

Suppose actual policy is P0.

Questions:

```text
What would happen under P1?
How much better is P1 than P0?
How much better is P1 than best available P2?
Why did outcome Y occur rather than Y*?
What is the average effect of P1 vs P0 in population R?
```

share objects but are not identical queries.

---

# PART I — FACTUAL ANCHOR

# 4. Factual anchor

The factual anchor supplies the token actuality/history/evidence relative to which a counterfactual may be asked.

It may include:

```text
actual state
actual history
actual evidence
actual model anchor
```

---

# 5. Anchor does not specify baseline

A query can begin from actual world w0 but compare two nonactual policies P1 and P2.

### Earned firewall N-ANCHOR-1

```text
ActualAnchor != RequiredComparator
```

---

# 6. Anchor can be abnormal

WDF2-M remains binding:

```text
ActualStatusQuo != NormalState
```

Therefore factual anchoring cannot be justified by normality alone.

---

# PART II — COMPARISON BASELINE

# 7. Baseline as comparator

A baseline is a designated comparator relative to which a difference/effect/contrast is stated.

Research form:

```text
Compare(TargetScenario, BaselineScenario)
```

---

# 8. Baseline is role-bearing

Possible roles:

```text
reference for effect size
control condition
status quo comparator
policy comparator
zero point
normative benchmark
historical benchmark
explanation foil
```

These roles need not coincide.

---

# 9. Same target, different baseline

For outcome values:

```text
Y(P1)=10
Y(P0)=8
Y(P2)=12
```

then:

```text
P1 vs P0 = +2
P1 vs P2 = -2
```

The target scenario did not change; the comparative claim did.

### Strong firewall N-BASE-1

```text
CounterfactualDifferenceSignCanDependOnBaseline
```

---

# 10. Baseline choice can reverse verdict

A policy can be an improvement over status quo and worse than the best alternative.

Thus:

```text
BeneficialRelativeToBaselineB
```

is incomplete without B.

---

# PART III — ZERO / NO-TREATMENT

# 11. Zero baseline

A mathematical zero may be a convenient reference but need not correspond to a physically realizable or semantically meaningful state.

### Earned firewall N-ZERO-1

```text
ZeroReference != NaturalBaseline by definition
```

---

# 12. No-treatment baseline

`No treatment` can itself have versions:

```text
no drug but supportive care
watchful waiting
placebo
no clinical contact
existing background therapy
```

### Earned firewall N-NOTRT-1

```text
NoTreatment != OneUniqueIntervention
```

---

# 13. Multiple versions pressure

VanderWeele/Hernán show that treatment labels can hide multiple versions producing different potential outcomes.

The same applies to control/no-treatment labels.

### Earned firewall N-VERS-1

```text
SameBaselineLabel != SameBaselineRealization
```

---

# PART IV — STATUS QUO

# 14. Status quo baseline

The actual/current policy is often used for decision comparison.

---

# 15. Status quo can be unstable or transient

Current state can be:

```text
temporary outage
emergency policy
legacy version
disallowed workaround
```

so status quo does not automatically deserve normative or statistical privilege.

### Earned firewall N-SQ-1

```text
StatusQuoComparator != NormativelyPreferredComparator
```

---

# PART V — STANDARD-OF-CARE / STANDARD POLICY

# 16. Standard baseline

A domain can define a canonical comparator:

```text
standard of care
approved protocol
baseline architecture
reference implementation
```

---

# 17. Standard is institutional

A standard comparator can differ from actual practice.

```text
ObservedTypicalPractice != OfficialStandard
```

WDF2-M applies.

---

# 18. Standard can change by regime/time

### Earned firewall N-STD-1

```text
StandardBaselineRequiresRule/Version/TimeScope
```

---

# PART VI — BEST ALTERNATIVE

# 19. Best-alternative baseline

Decision theory often asks whether action A outperforms the best available alternative.

This differs from factual counterfactual comparison.

---

# 20. Best requires objective

`Best` is incomplete without:

```text
utility/value objective
constraints
risk attitude
time horizon
information set
authority/capability
```

### Earned firewall N-BEST-1

```text
BestAlternative != NearestAlternative != NormalAlternative
```

---

# PART VII — NORMATIVE BASELINE

# 21. Normative comparator

One can ask:

```text
What happened relative to what should have happened?
```

This is a legitimate responsibility/compliance query.

---

# 22. Normative baseline is not causal control

### Earned firewall N-NORM-1

```text
NormativeBaseline != CausalControlCondition by default
```

A legally required action can be infeasible in a particular token situation; a control condition may be normatively neutral.

---

# PART VIII — HISTORICAL / TEMPORAL BASELINES

# 23. Historical baseline

Comparison can be relative to:

```text
last year
pre-intervention period
previous release
previous regime
```

---

# 24. Historical comparator may differ structurally

If population, model, environment or rules changed, historical comparison mixes counterfactual contrast with regime change.

### Earned firewall N-HIST-1

```text
HistoricalDifference != CounterfactualEffect without transport assumptions
```

---

# PART IX — REFERENCE CLASS PROBLEM

# 25. Hájek pressure

An individual event belongs to many reference classes, and probability can differ by class.

Examples:

```text
all servers
servers in region R
servers of model M
servers running version V
servers under high load
```

### Strong firewall N-RC-1

```text
TokenEventDoesNotSelectOneUniqueReferenceClassByItself
```

---

# 26. Reference class is not just a frequentist problem

Hájek argues structurally analogous reference-class problems affect several interpretations of probability.

Foundation lesson:

```text
making dependence explicit is necessary even when probability is not interpreted frequentistically.
```

---

# 27. Conditionalization helps but does not finish selection

Writing:

```text
P(Y | R)
```

makes the class explicit.

It does not tell us why R rather than R'.

### Earned firewall N-RC-2

```text
ExplicitConditioning != JustifiedReferenceClassSelection
```

---

# 28. Narrowest-class rule fails generally

The narrowest class can have:

```text
insufficient data
idiosyncratic variables
post-treatment variables
colliders
irrelevant features
```

and multiple equally narrow classes may disagree.

### Earned firewall N-RC-3

```text
MostSpecificAvailableClass != AutomaticallyBestReferenceClass
```

---

# PART X — REFERENCE CLASS SELECTION CRITERIA

# 29. Causal relevance criterion

One candidate is to condition on effect-modifying/causally relevant attributes.

Strength:

```text
avoids irrelevant partitioning
```

Risk:

```text
requires causal knowledge and can introduce post-treatment selection if misused.
```

---

# 30. Predictive criterion

Choose features improving predictive calibration.

Strength:

```text
empirical performance
```

Risk:

```text
predictive relevance != causal/contrastive relevance.
```

---

# 31. Mechanistic criterion

Group cases sharing relevant mechanism/regime.

Strength:

```text
scientific transport plausibility
```

Risk:

```text
mechanism may itself be under-modeled.
```

---

# 32. Institutional criterion

Use rule-defined population/role.

Strong for legal/policy queries, weak for unrelated physical outcomes.

---

# 33. Query-role criterion

Target population/reference class should match the population over which the question asks for a claim.

This is supported by target-trial/generalizability practice.

### Strong result N-RC-4

```text
ReferenceClassMustBeQuery/TargetLinked,
not selected after seeing desired result.
```

---

# PART XI — TARGET POPULATION

# 34. Target population

A population-level causal estimand is always relative to a defined population.

Target-trial methodology explicitly requires eligibility and treatment strategies to define the population and contrast before estimation.

---

# 35. Study population vs target population

### Earned firewall N-TARGET-1

```text
StudyPopulation != TargetPopulation
```

Even a perfectly estimated effect in study population may differ in target population under effect heterogeneity.

---

# 36. Generalizability vs transportability

A result can generalize to one population but not another.

Bareinboim/Pearl formalize transportability across environments using assumptions about similarities/differences.

### Earned firewall N-TRANS-1

```text
KnownSourceEffect != TargetPopulationEffect without transport conditions
```

---

# PART XII — COMPARISON SET VS REFERENCE CLASS

# 37. Comparison set

The set of counterfactual alternatives being compared can be:

```text
possible actions
possible policies
possible worlds/states
possible treatment strategies
possible model revisions
```

---

# 38. Reference class is about cases/tokens/population

The reference class may instead classify units:

```text
patients
servers
users
organizations
```

### Strong firewall N-SET-1

```text
ReferenceClassOfUnits != ComparisonSetOfAlternatives
```

A treatment effect can compare two actions over one target population.

---

# PART XIII — ALTERNATIVE DOMAIN VS COMPARISON SET

# 39. Alternative domain

WDF1/WDF2-C/H use alternative domain to determine what alternatives are semantically admitted at all.

---

# 40. Comparison set is a selected subset/structure

One can admit many possibilities but compare only:

```text
A vs B
```

for a particular estimand.

### Earned firewall N-DOM-1

```text
AdmissibleAlternativeDomain != ActiveComparisonSet
```

---

# PART XIV — CONTRASTIVE FOIL

# 41. Why P rather than Q?

Contrastive-explanation traditions treat foil Q as part of the explanatory question.

Schaffer similarly argues for contrastive structure in causation:

```text
c rather than c*
causes
e rather than e*
```

---

# 42. Foil changes relevance

A factor can explain:

```text
why P rather than Q1
```

but not:

```text
why P rather than Q2
```

### Strong firewall N-FOIL-1

```text
SameFactDifferentFoil != SameExplanationQuestion
```

---

# 43. Foil is not simply negation

`Why P rather than not-P?` may be too broad to identify the intended contrast.

A specific foil can constrain explanatory relevance much more strongly.

### Earned firewall N-FOIL-2

```text
SpecificFoilQ != GenericNegationNotP
```

---

# 44. Contrast is not conjunction

Lipton-style contrastive analysis rejects reducing `P rather than Q` to merely `P and not Q`.

The relation to Q determines what difference needs explanation.

### Earned firewall N-FOIL-3

```text
Contrast(P,Q) != Conjunction(P,NotQ)
```

---

# PART XV — FACT / FOIL COMPATIBILITY

# 45. Foils need not always be mutually exclusive

Some explanatory contrasts compare alternatives that could co-occur but differ in degree/route/location.

Thus:

```text
Foil != NecessarilyLogicalComplement
```

---

# 46. Counterfactual realization must still be typed

If foil Q is itself underspecified or multiply realizable, WDF2-A/J apply.

### Earned firewall N-FOIL-4

```text
FoilLabel != UniqueCounterfactualRoute
```

---

# PART XVI — TREATMENT STRATEGIES / CAUSAL CONTRAST

# 47. Causal estimand requires explicit strategies

Target-trial work emphasizes defining the treatment strategies compared and the causal contrast before analysis.

### Strong firewall N-EST-1

```text
CausalQuestion != OutcomePredictionWithoutSpecifiedContrast
```

---

# 48. Assignment effect vs adherence effect

Intention-to-treat and per-protocol contrasts compare different counterfactual regimes.

### Earned firewall N-EST-2

```text
EffectOfAssignment != EffectOfFollowingStrategy
```

---

# 49. Baseline time / time zero

Target-trial methodology also requires alignment of eligibility, treatment assignment and follow-up start.

### Earned firewall N-T0-1

```text
ComparisonBaselineValue != BaselineTime
```

The word `baseline` itself is overloaded.

---

# PART XVII — MULTIPLE VERSIONS OF TREATMENT

# 50. Treatment label can hide versions

VanderWeele/Hernán show potential outcomes under treatment A can depend on version k:

```text
Y(a,k)
```

---

# 51. Coarse treatment contrast can be policy-dependent

An average `treatment vs control` effect may implicitly depend on the current policy assigning treatment versions.

### Strong firewall N-VERS-2

```text
CoarseTreatmentContrast != VersionInvariantEffect
```

---

# 52. Baseline versions matter symmetrically

The comparator/control can also have multiple versions.

This prevents treating baseline as a passive zero point.

---

# PART XVIII — REFERENCE-CLASS REVERSAL

# 53. Simpson-style pressure

Aggregate and subgroup comparisons can differ or reverse when group composition changes.

The lesson is not `always stratify`.

It is:

```text
the target estimand and relevant population structure must be declared.
```

---

# 54. Population effect can differ without individual contradiction

A treatment can benefit subgroup R1 and harm R2, while aggregate effect depends on weights.

### Earned firewall N-RC-REV-1

```text
PopulationAverageVerdict != UniversalUnitLevelVerdict
```

---

# PART XIX — POPULATION WEIGHTS

# 55. Target population supplies weights

An average outcome/effect requires a distribution over units/covariates.

Changing target population changes those weights.

---

# 56. Weights are not merely statistical nuisance

They partly define the population estimand.

### Earned firewall N-WEIGHT-1

```text
TargetPopulationWeighting != MereEstimatorImplementationDetail
```

---

# PART XX — OPEN-WORLD COMPARISON SET

# 57. Current comparison set may be incomplete

WDF1 warns:

```text
CurrentAlternativeDomain != CompleteRealityModalDomain
```

Similarly:

```text
CurrentComparisonSet != AllRelevantAlternatives
```

---

# 58. Dominated conclusion can disappear after expansion

An action may be best among {A,B} but not after adding C.

### Earned firewall N-OPEN-1

```text
BestInCurrentSet != GloballyBest
```

---

# 59. Open-world expansion must not silently rewrite question

Adding alternative C is legitimate only if C belongs to the query's comparison role and scope.

### Earned firewall N-OPEN-2

```text
ComparisonSetExpansion != AutomaticQueryImprovement
```

---

# PART XXI — BASELINE SELECTION WITHOUT ANSWER-DRIVEN CHOICE

# 60. Bad route

```text
choose baseline after seeing which yields desired sign/magnitude
```

This is rejected.

---

# 61. Pre-specification route

Target-trial practice demonstrates a strong discipline:

```text
specify population
strategies
outcome
time
causal contrast
before estimation
```

### Strong result N-PRE-1

```text
ComparatorSelectionShouldPrecedeOutcomeDrivenEstimationWhenPossible
```

---

# 62. Semantically supplied baseline

Sometimes query itself supplies:

```text
instead of P0
rather than Q
compared with last version
```

Then baseline is part of content.

---

# 63. Domain-standard baseline

Sometimes professional/scientific convention supplies a comparator, but provenance remains required.

---

# 64. Multiple admissible baselines

If no unique baseline is justified, preserve several.

### Strong firewall N-PLURAL-1

```text
MultipleAdmissibleBaselines != NeedToChooseOneArbitrarily
```

---

# PART XXII — BASELINE-ROBUST CLAIMS

# 65. Baseline family

Let:

```text
B in AdmissibleBaselines(Q,D)
```

---

# 66. Baseline-robust sign

```text
forall B: Delta_B > 0
```

is stronger than positive effect under one baseline.

---

# 67. Baseline-sensitive result

If sign/magnitude changes:

```text
report dependence explicitly.
```

### Earned firewall N-ROB-1

```text
BaselineSensitivity != StatisticalSamplingUncertainty
```

---

# 68. Reference-class robustness

Similarly:

```text
forall R in admissible reference classes:
  conclusion C
```

can define reference-class robustness.

---

# PART XXIII — TRANSPORT ACROSS POPULATIONS

# 69. Source-to-target transport

Bareinboim/Pearl show causal effects can sometimes be transported when differences between source and target domains are explicitly represented.

---

# 70. Transport is not baseline identity

Even if the same treatment labels exist, their versions/background mechanisms can differ.

### Earned firewall N-TRANS-2

```text
SameTreatmentNamesAcrossDomains != SameCounterfactualStrategies
```

---

# 71. Reference-class migration requires effect-modifier analysis

A target population can differ exactly in variables modifying the effect.

Thus source average cannot be copied blindly.

---

# PART XXIV — NESTED SUPPOSITION

# 72. Outer supposition can change reference class

In:

```text
A □→ (B □→ C)
```

B may be evaluated relative to:

```text
units/worlds consistent with A
original population
A-conditioned regime
new institutional class
```

---

# 73. Reference-class inheritance

### Earned firewall N-NEST-1

```text
NestedReferenceClassInheritance != OneUniversalPolicy
```

WDF2-L context inheritance applies.

---

# 74. Baseline inheritance

The inner B contrast may inherit outer baseline, reset it, or establish a new comparator.

---

# PART XXV — MODEL / VERSION CHANGE

# 75. Software baseline transport

Comparing v4 patch against v3 behavior can require mapping:

```text
features
state variables
APIs
performance measures
```

---

# 76. Same named baseline across versions can be ill-typed

### Earned firewall N-VERSION-1

```text
SameBaselineNameAcrossVersions != SameComparatorSemantics
```

---

# 77. Agent provider baseline

`baseline model M` can drift under provider updates even with stable model label.

Baseline provenance therefore requires concrete version/time evidence.

---

# PART XXVI — INSTITUTIONAL / JURISDICTION CHANGE

# 78. Rule-relative baseline

A compliant baseline under rule system K can be noncompliant under K'.

---

# 79. Normative foil migration

If law changes, `what should have happened` changes even when physical alternatives remain same.

### Earned firewall N-INST-1

```text
NormativeBaselineTransportRequiresRuleMapping
```

---

# PART XXVII — PHYSICAL MATCHED CASES

# 80. Temperature effect

Question:

```text
What if temperature were 310K?
```

is not yet an effect contrast.

Need comparator:

```text
actual 300K
nominal 298K
safety limit 305K
```

Different differences answer different questions.

---

# 81. Rare actual anchor

An actual abnormal pressure state can remain the baseline for a token intervention, even if a normal-pressure comparator is used for engineering benchmark reporting.

---

# PART XXVIII — SOFTWARE MATCHED CASES

# 82. Patch baseline

`Patch improved latency` can mean relative to:

```text
current production
previous release
unpatched same commit
reference implementation
best competitor
```

### Earned firewall N-SW-1

```text
SoftwareImprovementClaimRequiresComparator
```

---

# 83. Feature flag control

`feature off` may be a clean baseline only if disabling it does not alter other configuration/mechanism assumptions unexpectedly.

---

# PART XXIX — INSTITUTIONAL MATCHED CASES

# 84. Compliance comparison

Question:

```text
What would have happened if Actor complied?
```

requires identifying which compliant action/version counts as foil.

---

# 85. Multiple compliant actions

### Earned firewall N-COMP-1

```text
ComplianceCondition != UniqueCompliantAction
```

Responsibility analysis cannot silently select the easiest foil.

---

# PART XXX — FINANCE / DECISION MATCHED CASES

# 86. Performance baseline

A portfolio return can be:

```text
positive vs cash
negative vs index
positive vs risk-matched benchmark
negative vs best ex-post asset
```

---

# 87. Benchmark selection matters

### Earned firewall N-FIN-1

```text
AbsoluteGain != RelativeOutperformance
```

Decision quality also requires ex ante feasible alternatives, not ex post hindsight optimum.

---

# PART XXXI — AGENT-ERA MATCHED CASES

# 88. Agent quality baseline

`Agent improved task success` can mean relative to:

```text
no agent
human alone
previous agent version
same model without tools
best competitor
```

---

# 89. Ablation is one comparator family

Ablation compares system with/without component under controlled preservation assumptions.

### Earned firewall N-AGENT-1

```text
AblationBaseline != UniversalNoComponentCounterfactual
```

Removing a component may trigger architectural adaptation rather than a clean subtraction.

---

# 90. Model baseline drift

Provider changes can invalidate historic benchmark comparators without explicit version pinning.

---

# PART XXXII — CONTRASTIVE EXPLANATION

# 91. Explanatory fact is foil-relative

Why did classifier output `cat` rather than `dog`?

Relevant features can differ from:

```text
why cat rather than airplane?
```

---

# 92. Contrast restricts relevance

WDF2-I relevance now acquires an explicit foil argument:

```text
Relevant(r | Fact P, Foil Q, QueryRole)
```

### Strong firewall N-REL-1

```text
ExplanatoryRelevance != FoilIndependent
```

---

# 93. Contrastive explanation is not automatically causal effect

A feature can explain classification contrast semantically/mechanistically without corresponding to one treatment-effect estimand.

---

# PART XXXIII — CONTRASTIVE CAUSATION PRESSURE

# 94. Schaffer architecture

Contrastive causation proposes a richer relation:

```text
c rather than C*
causes
e rather than E*
```

WDF2-N does not yet adopt this as universal causal ontology.

---

# 95. Foundation lesson

Actual-causation queries later must expose:

```text
cause foil
outcome foil
```

when they matter.

### Earned firewall N-CAUSE-1

```text
BinaryCauseClaimCanHideContrastStructure
```

---

# PART XXXIV — BASELINE VS PRESERVATION

# 96. Comparator difference is not preservation policy

Choosing B as baseline does not imply every feature of B should be imported into the target branch.

### Earned firewall N-PRES-1

```text
BaselineScenario != PreservationTemplate by definition
```

---

# 97. Matched comparison requires controlled mapping

To compare A and B, identify which dimensions are intended to vary and which remain matched.

This reconnects WDF2-A/F.

---

# PART XXXV — BASELINE VS NORMALITY

# 98. WDF2-M firewall strengthened

```text
ReferenceBaseline != NormalState
```

A baseline can be:

```text
arbitrary convention
regulatory control
worst case
zero point
actual exception
```

---

# 99. Normality can choose a baseline only for some query roles

For `compared with usual practice`, statistical/conventional typicality is content-relevant.

Not for all effects.

---

# PART XXXVI — BASELINE VS COUNTERFACTUAL GENERATOR

# 100. Baseline does not choose realization algorithm

Given comparator B, one still needs to decide how target A is generated/evaluated.

### Earned firewall N-GEN-1

```text
ComparatorChoice != CounterfactualGeneratorChoice
```

---

# PART XXXVII — REFERENCE CLASS VS CAUSAL CONDITIONING

# 101. Reference class can include pre-treatment covariates

Useful for target population definition/effect heterogeneity.

---

# 102. Post-treatment conditioning can change estimand/bias

The narrowest/descriptively precise class may include descendants of treatment.

### Earned firewall N-POST-1

```text
DescriptiveSpecificity != CausalAdmissibilityOfConditioningSet
```

---

# PART XXXVIII — REFERENCE CLASS VS IDENTITY

# 103. Class membership is not identity

A token can belong to many classes without becoming different entities.

### Earned firewall N-ID-1

```text
ReferenceClassMembership != CounterfactualCounterpartIdentity
```

WDF2-B/G correspondence remains separate.

---

# PART XXXIX — REFERENCE CLASS VS SAMPLING FRAME

# 104. Target population

The population about which estimand is defined.

---

# 105. Sampling frame

The operational list/process from which data are sampled.

### Earned firewall N-SAMPLE-1

```text
SamplingFrame != TargetPopulation
```

Coverage errors can separate them.

---

# PART XL — MULTIPLE LEGITIMATE TARGET POPULATIONS

# 106. Same study, several questions

One trial can support estimands for:

```text
all eligible patients
older patients
current clinic population
future national population
```

if transport/generalization conditions permit.

---

# 107. No universal target population

### Strong firewall N-TARGET-2

```text
DatasetDoesNotDetermineOneCanonicalTargetPopulation
```

The target is question-defined and must be justified.

---

# PART XLI — EFFECT HETEROGENEITY PRESSURE

# 108. Population dependence emerges

If unit/subgroup effects differ, changing reference population changes the average causal contrast.

---

# 109. Same comparator, different population

```text
ATE_R1(A,B) != ATE_R2(A,B)
```

can hold without contradiction.

### Earned firewall N-HET-1

```text
SameTreatmentContrast != SamePopulationEffect
```

---

# 110. This is not solved by better baseline selection

Even after A/B and population are specified, the manner of aggregating heterogeneous unit-level contrasts remains unresolved.

This becomes a key residual for WDF2-O.

---

# PART XLII — EFFECT MEASURE PRESSURE

# 111. Same baseline, multiple effect measures

For binary outcome one can use:

```text
risk difference
risk ratio
odds ratio
```

For continuous outcome:

```text
mean difference
ratio
quantile shift
distributional distance
```

---

# 112. Baseline alone does not determine metric

### Strong firewall N-MEASURE-1

```text
SpecifiedComparator != SpecifiedEffectMeasure
```

Thus baseline foundations do not finish effect semantics.

---

# PART XLIII — INDIVIDUAL VS POPULATION CONTRAST

# 113. Unit-level contrast

```text
Y_i(A) vs Y_i(B)
```

---

# 114. Population contrast

```text
E_R[Y(A)] vs E_R[Y(B)]
```

requires population R and aggregation.

### Earned firewall N-LEVEL-1

```text
IndividualCounterfactualContrast != PopulationAverageEffect
```

---

# 115. Population average can hide sign heterogeneity

Average zero can arise from large positive and negative unit effects.

### Earned firewall N-AVG-1

```text
ZeroAverageEffect != NoUnitLevelEffects
```

---

# PART XLIV — CONTROL CONDITION

# 116. Control is design-relative

A randomized control arm is defined by a protocol, not metaphysically by `nothing happens`.

---

# 117. Active comparator

Many useful trials compare two active strategies.

### Earned firewall N-CTRL-1

```text
ControlCondition != NoAction
```

---

# PART XLV — REFERENCE CLASS AND NORMALITY

# 118. WDF2-M dependence formalized

```text
Typicality(E | R)
```

requires R.

---

# 119. Reference class can reverse normality

An event can be typical in R1 and atypical in R2.

### Earned firewall N-NORM-1

```text
NormalityVerdictCanBeReferenceClassRelativeWithoutBeingSubjective
```

---

# PART XLVI — REFERENCE CLASS AND PROBABILITY

# 120. Probability claim is scope-bearing

Hájek's problem motivates explicit conditional/reference structure.

---

# 121. Reference class remains epistemically underdetermined

Knowing all candidate classes does not guarantee a unique rational choice.

### Earned firewall N-RC-4B

```text
ReferenceClassEnumeration != ReferenceClassResolution
```

---

# PART XLVII — COMPARISON SET AND DECISION

# 122. Feasible set matters

Decision comparison should often restrict to:

```text
available
feasible
authorized
time-compatible
```

alternatives.

---

# 123. Counterfactual truth need not restrict to feasible set

One can ask a scientifically meaningful counterfactual about an infeasible or unauthorized intervention.

### Earned firewall N-DEC-1

```text
DecisionComparisonSet != CounterfactualModalDomain
```

---

# PART XLVIII — QUERY-ROLE ROUTING

# 124. Prediction role

Baseline may be unnecessary if asking only:

```text
what happens under A?
```

---

# 125. Effect role

Requires at least two counterfactual regimes/comparators.

---

# 126. Explanation role

Requires a fact/foil contrast when the question is contrastive.

---

# 127. Decision role

Requires feasible alternatives and objective.

---

# 128. Responsibility role

Can require normative and feasible-action foils.

### Strong firewall N-ROLE-1

```text
OneComparatorPolicy != AllCounterfactualQueryRoles
```

---

# PART XLIX — RECONSTRUCTION

# 129. Research-level comparison contract

```text
ComparisonFrame =
  FactualAnchor?
  TargetScenario/Strategy
  BaselineScenario/Strategy?
  ContrastiveFoil?
  ReferenceClass/TargetPopulation?
  ActiveComparisonSet
  AlternativeDomain
  Time/Horizon
  Version/Regime/RuleScope
  QueryRole
  ComparatorProvenance
  TransportAssumptions?
```

Not every field is universal.

---

# 130. Baseline status

```text
ExplicitInQuery
DomainStandard
FactualStatusQuo
NoTreatment/Control
BestFeasibleAlternative
NormativeComparator
HistoricalComparator
MultipleAdmissibleBaselines
BaselineMissing
```

---

# 131. Reference-class status

```text
ExplicitTargetPopulation
MechanismDefinedClass
InstitutionDefinedClass
EvidenceDefinedClass
MultipleAdmissibleClasses
ReferenceClassUnderdetermined
TransportRequired
```

---

# 132. Contrast status

```text
ExplicitFoil
ImplicitBinaryComplement
FoilFamily
OpenFoilSet
FoilUnderdetermined
```

---

# 133. Robustness status

```text
BaselineRobust
ReferenceClassRobust
FoilRobust
ComparisonSetSensitive
TransportSensitive
```

---

# PART L — DELETION TESTS

# 134. Factual anchor = baseline

**FAIL** for nonactual strategy-vs-strategy comparisons.

---

# 135. Baseline = normal state

**FAIL** through arbitrary/control/status-quo/normative comparators.

---

# 136. Baseline = zero/no-treatment

**FAIL** across active-comparator and multiple-version cases.

---

# 137. Control = no action

**FAIL** in active-control protocols.

---

# 138. Reference class = comparison set

**FAIL**; units and alternatives are different axes.

---

# 139. Reference class = sampling frame

**FAIL** under coverage/generalization mismatch.

---

# 140. Reference class = narrowest available class

**FAIL** through data scarcity, irrelevant features and causal-conditioning issues.

---

# 141. Target population = study sample

**FAIL** under generalization/transport questions.

---

# 142. Same treatment labels imply same strategies

**FAIL** under multiple versions and domain drift.

---

# 143. Foil = not-P

**FAIL** for specific contrastive explanations.

---

# 144. Contrast(P,Q)=P AND not-Q

**FAIL** because explanatory relevance depends on Q.

---

# 145. Baseline selection after results

**FAIL** as answer-driven contrast selection.

---

# 146. Force one baseline

**FAIL** when several comparators are semantically legitimate.

---

# 147. Force one reference class

**FAIL** when query leaves population genuinely underspecified.

---

# 148. Average across baselines by default

**FAIL**; baselines are semantic alternatives, not random events.

---

# 149. Copy source population effect to target

**FAIL** absent transport/generalization conditions.

---

# 150. Best current comparison set = globally best

**FAIL** in open-world settings.

---

# 151. Baseline determines effect measure

**FAIL**; difference/ratio/distributional measures remain open.

---

# 152. Population average = unit-level truth

**FAIL** under heterogeneity.

---

# PART LI — EXTERNAL RESEARCH PRESSURE

# 153. Hájek 2007

`The Reference Class Problem is Your Problem Too` argues that an event can be classified in multiple ways yielding different probabilities and that analogues of the problem extend beyond frequentism. He distinguishes metaphysical and epistemological dimensions and emphasizes conditional/reference structure.

Foundational pressure:

```text
reference scope must be explicit;
explicitness alone does not solve justified selection.
```

---

# 154. Target-trial framework

Hernán/Robins-style target-trial methodology requires explicit eligibility criteria, treatment strategies, assignment, time zero, outcome, follow-up and causal contrast before estimation.

Foundational pressure:

```text
causal estimand is question/design-defined, not extracted from data after the fact.
```

---

# 155. VanderWeele/Hernán 2013

Multiple versions of treatment can make coarse treatment labels insufficient to determine unique potential outcomes, and overall effects can depend on version-assignment policy.

Foundational pressure:

```text
comparator/treatment labels require realization/version semantics.
```

---

# 156. Bareinboim/Pearl

Transportability theory formally represents differences between source and target domains and derives when source experimental effects can be transferred.

Foundational pressure:

```text
population/domain scope is part of causal effect semantics and identification.
```

---

# 157. Schaffer 2005

`Contrastive Causation` argues for a contrastive causal relation involving both cause and effect contrasts.

Foundational pressure:

```text
binary causal claims can hide unspoken foils.
```

WDF2-N does not yet adopt the full ontology.

---

# 158. Lipton / contrastive explanation tradition

Contrastive explanation treats `Why P rather than Q?` as a different explanatory problem from unqualified `Why P?`, and the contrast cannot generally be reduced to `P and not-Q`.

Foundational pressure:

```text
foil is content-bearing, not report formatting.
```

---

# PART LII — WDF0 / WDF1 REOPEN AUDIT

# 159. WDF0

No FoundationReopenCondition fires.

WDF2-N reinforces:

```text
Relative != Subjective
Same_X != Same_Y without criterion
Cause != Constitution
Model != Reality
```

Reference relativity is typed/objective when the class/comparator is explicit.

WDF0 remains frozen.

---

# 160. WDF1

No FoundationReopenCondition fires.

TMCG already demands:

```text
alternative/contrast specification
dependence/background
anchor
operator/measure provenance
```

WDF2-N deepens the contrast/reference component without falsifying WDF1.

WDF1 remains frozen.

---

# PART LIII — STRONG RESULTS

# 161. Strong result — comparison is multi-axis

A counterfactual comparison can simultaneously specify:

```text
unit/world anchor
strategy contrast
population/reference class
foil
comparison set
```

No one axis determines the others.

---

# 162. Strong result — baseline belongs to query semantics when comparative language requires it

`better`, `effect`, `increase`, `rather than`, `improved` are incomplete without comparator semantics.

---

# 163. Strong result — reference class selection is epistemic/semantic, not purely statistical

Data cannot choose its own target population.

Domain/query knowledge is required.

---

# 164. Strong result — comparison-set completeness is open-world

A robust decision conclusion must disclose whether it is:

```text
best among enumerated alternatives
```

or:

```text
best under a justified closed set.
```

---

# 165. Strong result — contrastive foil changes explanatory relevance

The same causal history supports different explanations under different foils.

---

# 166. Strong result — comparator uncertainty is structural underdetermination

Multiple baselines/reference classes can survive even with perfect data.

This is not sampling noise.

---

# PART LIV — LARGEST REMAINING RESIDUAL

# 167. Baseline/reference foundations still do not define an effect

After WDF2-N we can specify:

```text
A vs B
in population R
for outcome Y
at horizon t
```

But we still have not specified **what mathematical/semantic summary of the contrast is the target**.

---

# 168. Effect measure plurality

Possible targets include:

```text
individual difference Y_i(A)-Y_i(B)
mean difference
risk difference
risk ratio
odds ratio
quantile effect
distributional shift
probability of benefit
median effect
policy value difference
set-valued robust contrast
```

These can disagree in sign/interpretation or vary under transformation.

---

# 169. Aggregation is substantive

Population effect requires aggregating heterogeneous unit-level counterfactuals.

```text
AverageOfDifferences
```

is not the only possible aggregate.

---

# 170. Heterogeneity cannot be treated as noise

A zero average can hide large positive/negative individual effects.

Target population changes can alter aggregate effect even with invariant unit mechanisms.

---

# 171. Estimand is not estimator

Target-trial literature already forces the separation:

```text
causal estimand
!= statistical estimator
```

WDF2 has not yet built a general counterfactual estimand ontology.

---

# 172. Effect vs causal attribution

Even a well-defined average causal effect is not the same question as:

```text
Did this token event cause this outcome?
```

Before actual causation, WDF2 should explicitly separate effect/estimand/aggregation from token causal attribution.

---

# 173. Exact next round

The next canonical round is therefore:

# **WDF2-O — Counterfactual Effect / Estimand / Aggregation / Heterogeneity**

WDF2-O should test:

```text
unit-level contrast
conditional effect
average treatment effect
ATT / ATU / overlap-population effects
risk difference / ratio / odds ratio
quantile/distributional effects
probability of benefit/harm
policy value
heterogeneous treatment effects
aggregation weights
non-collapsibility / aggregation reversal
population transport
multiple treatment versions
set/bound/robust estimands
estimand vs estimator vs identification
```

and ask:

```text
What makes two effect measures answer the same or different counterfactual question?
When can population aggregation erase/reverse unit-level structure?
Which aggregation weights are semantic vs statistical?
How should heterogeneity be represented rather than averaged away?
When is an estimand stable under target-population transport?
How do model/version/baseline changes alter estimand identity?
```

It must not preselect average difference, ATE, risk ratio, expectation, scalar utility or one population aggregation as universal.

Only WDF2-O residuals may determine WDF2-P.

---

# 174. Production disposition

No production changes are admitted.

Do **not** add:

```text
BaselineRegistry
ReferenceClassResolver
ComparisonSetManager
ContrastiveFoilEngine
TargetPopulationSelector
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

Counterfactual Foundations remain open.

---

# 175. Closeout

```text
WDF2-N: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D/E/F/G/H/I/J/K/L/M reopen: NO
Production refactor: NO

FactualAnchor != ComparisonBaseline != ReferenceClass != ComparisonSet != ContrastiveFoil
ActualAnchor != RequiredComparator
CounterfactualDifferenceSignCanDependOnBaseline
ZeroReference != NaturalBaseline
NoTreatment != OneUniqueIntervention
SameBaselineLabel != SameBaselineRealization
StatusQuoComparator != NormativelyPreferredComparator
BestAlternative != NearestAlternative != NormalAlternative
NormativeBaseline != CausalControlCondition
HistoricalDifference != CounterfactualEffect without transport assumptions
TokenEventDoesNotSelectOneUniqueReferenceClassByItself
ExplicitConditioning != JustifiedReferenceClassSelection
MostSpecificAvailableClass != AutomaticallyBestReferenceClass
StudyPopulation != TargetPopulation
KnownSourceEffect != TargetPopulationEffect without transport conditions
ReferenceClassOfUnits != ComparisonSetOfAlternatives
AdmissibleAlternativeDomain != ActiveComparisonSet
SameFactDifferentFoil != SameExplanationQuestion
SpecificFoil != GenericNegation
Contrast(P,Q) != Conjunction(P,NotQ)
EffectOfAssignment != EffectOfFollowingStrategy
ComparisonBaselineValue != BaselineTime
CoarseTreatmentContrast != VersionInvariantEffect
PopulationAverageVerdict != UniversalUnitLevelVerdict
TargetPopulationWeighting != MereEstimatorImplementationDetail
BestInCurrentSet != GloballyBest
MultipleAdmissibleBaselines != NeedToChooseOneArbitrarily
BaselineSensitivity != SamplingUncertainty
SameTreatmentNamesAcrossDomains != SameCounterfactualStrategies
NestedReferenceClassInheritance != OneUniversalPolicy
SameBaselineNameAcrossVersions != SameComparatorSemantics
NormativeBaselineTransportRequiresRuleMapping
AbsoluteGain != RelativeOutperformance
AblationBaseline != UniversalNoComponentCounterfactual
ExplanatoryRelevance != FoilIndependent
BinaryCauseClaimCanHideContrastStructure
BaselineScenario != PreservationTemplate
ComparatorChoice != CounterfactualGeneratorChoice
DescriptiveSpecificity != CausalAdmissibilityOfConditioningSet
ReferenceClassMembership != CounterfactualCounterpartIdentity
SamplingFrame != TargetPopulation
DatasetDoesNotDetermineOneCanonicalTargetPopulation
SameTreatmentContrast != SamePopulationEffect
SpecifiedComparator != SpecifiedEffectMeasure
IndividualCounterfactualContrast != PopulationAverageEffect
ZeroAverageEffect != NoUnitLevelEffects
ControlCondition != NoAction
DecisionComparisonSet != CounterfactualModalDomain
OneComparatorPolicy != AllCounterfactualQueryRoles

Exact next round:
WDF2-O — Counterfactual Effect / Estimand / Aggregation / Heterogeneity
```

Compressed result:

> **WDF2-N establishes that factual anchor, comparison baseline, reference class/target population, active comparison set and contrastive foil are orthogonal counterfactual dimensions rather than aliases. An actual state can anchor a query without serving as its comparator; a control arm need not be no-action; no-treatment and coarse treatment labels can hide multiple realization versions; and a target scenario can improve relative to status quo while worsen relative to a best feasible alternative. Hájek-style reference-class pressure shows that token events belong to many legitimate classes yielding different probabilities, while explicit conditionalization only exposes rather than solves the epistemological selection problem. Target-trial and transportability frameworks independently demonstrate that population, treatment strategies, time zero and causal contrast must be specified before estimation and that source effects cannot simply be copied to different populations. Contrastive explanation and contrastive-causation traditions add another axis: `Why P rather than Q?` can change which facts are relevant, and a specific foil is not reducible to generic `not-P` or conjunction. WDF2-N therefore reconstructs comparison as a provenance-bearing frame with separate target scenario, baseline, target population/reference class, foil, comparison set, alternative domain and transport assumptions. When several baselines or reference classes remain legitimate, plural/set-valued or robust reporting is safer than answer-driven selection. The strongest residual is now no longer comparator identity but the meaning of `effect` itself: once A, B and population R are fixed, unit differences, mean effects, risks, ratios, quantiles, probability-of-benefit, policy value and robust set-valued contrasts remain distinct estimands, and heterogeneous unit effects can be hidden or reversed by aggregation. WDF2 therefore advances next to effect, estimand, aggregation and heterogeneity before any attempt to enter token actual-causation foundations.**
