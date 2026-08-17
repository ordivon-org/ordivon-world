# WDF2-G — Counterfactual Cross-World Coherence / Consistency / Compatibility

Status: **complete for WDF2-G**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D/E/F remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-G residuals:

```text
WDF2-H — Counterfactual Impossibility / Counterpossibles / Domain-Revising Antecedents
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-F established that nested counterfactuals and cross-world stitching are not ordinary compound interventions.

Typical object:

```text
Y_{a,M_{a'}}
```

This requires a value generated in one branch to participate in the evaluation of another branch.

WDF2-G asks the deeper question:

> **When do several branch-indexed counterfactual claims belong to one coherent counterfactual system, and when are they merely individually meaningful but jointly incompatible, unidentified, unmappable, or impossible?**

The round separates:

```text
well-typedness
local branch satisfiability
cross-branch correspondence
shared-background coupling
joint satisfiability
cross-world independence
identifiability
evidential warrant
physical realizability
```

None of these is allowed to collapse into one word such as `consistency`.

---

# 2. First anti-collapse law

The central separation is:

```text
CrossWorldCoherence
!= CrossWorldIndependence
!= PointIdentification
!= ExperimentalRealizability
!= PhysicalCoexistence
```

A nested quantity can be coherent in a formal counterfactual system while not corresponding to one physically executable same-world intervention.

A coherent quantity can also remain empirically unidentified.

And a cross-world independence condition can be much stronger than anything required merely for joint coherence.

---

# 3. Counterfactual system vs collection of sentences

Suppose we have claims:

```text
Y_0 = 0
Y_1 = 1
M_0 = 0
M_1 = 1
Y_{1,M_0} = 1
```

WDF2-G distinguishes:

```text
EachSentenceIndividuallySatisfiable
```

from:

```text
AllSentencesJointlySatisfiableInOneCounterfactualCompletion
```

### Earned firewall G-JOINT-1

```text
IndividualSatisfiability != JointSatisfiability
```

A counterfactual architecture must be able to reject a jointly impossible family without claiming that each sentence is meaningless in isolation.

---

# PART I — COHERENCE LAYERS

# 4. Layer 0 — expression typing

Before truth evaluation, each expression must have:

```text
branch/index scope
target variable/entity
alteration semantics
correspondence criterion
model/domain language
```

If the receiving branch no longer contains the imported target type, the expression can be ill-typed.

Example:

```text
rule K' abolishes institutional status S
then query imports S_K from old-rule branch into K'-branch
```

The problem may be target-type loss rather than falsehood.

---

# 5. Layer 1 — local branch coherence

Each branch must independently satisfy its own declared:

```text
model equations / transition constraints
intervention semantics
preservation profile
constitutive rules
boundary conditions
```

Call this schematically:

```text
LocalCoherent(B_i)
```

Local coherence does not yet license cross-branch stitching.

---

# 6. Layer 2 — correspondence coherence

A cross-world expression needs an admissible mapping:

```text
Corr(B_i.entity, B_j.entity)
```

Possible forms include:

```text
strict token identity
criterion-relative continuity
same structural variable role
counterpart mapping
explicit no-correspondence
```

### Earned firewall G-ID-1

```text
SameVariableName != CrossWorldIdentity
```

Two models can both call something `M` while representing different quantities, grains, roles, or constitutive statuses.

---

# 7. Layer 3 — coupling/background coherence

If two branches are individualized counterfactuals for the same factual token, their relationship often depends on a coupling/background policy.

Examples:

```text
same exogenous U
same latent seed
same factual history to intervention time
matched initial microstate
probabilistic coupling family
```

But none is universal.

### Earned firewall G-BG-1

```text
SameIndividualAcrossBranches != SameExogenousRepresentation by definition
```

Shared exogenous variables are one modeling implementation of cross-world coupling, not an ontological definition of individual identity.

---

# 8. Layer 4 — stitch compatibility

For an imported branch value:

```text
v := M_{a'}
```

and a receiving branch:

```text
Y_{a,v}
```

one must check that `v` lies in the receiving target's admissible domain and that the stitch operation does not violate protected constraints.

### Earned firewall G-STITCH-1

```text
ValueGeneratedInBranchB
!= AutomaticallyAdmissibleInputInBranchA
```

---

# 9. Layer 5 — joint satisfiability

The strongest local-system question is whether there exists at least one complete counterfactual structure satisfying every declared branch and stitch constraint:

```text
Exists Completion C:
  C |= Claims
```

Call this:

```text
JointCoherent(Claims | ModelClass, Correspondence, Coupling)
```

This is still model-class relative.

---

# 10. Layer 6 — robust cross-world consequence

If multiple coherent completions remain:

```text
C in Completions
```

then WDF2-E robustness applies again.

A target can be:

```text
true in every coherent completion
false in every coherent completion
completion-dependent
undefined in some completions
```

### Earned firewall G-ROB-1

```text
OneCoherentCompletionExists
!= CrossWorldResultIdentified
```

---

# PART II — FACTUAL CONSISTENCY

# 11. Standard consistency intuition

A familiar potential-outcome principle says roughly:

```text
if factual treatment A=a,
then factual outcome Y equals Y(a)
```

This is often called consistency.

WDF2-G retains only a **typed** version.

---

# 12. Typed factual consistency

A safer research law is:

```text
If factual branch already realizes exactly the same intervention specification I
and target/correspondence semantics are stable,
then evaluating I should reproduce the factual target at the declared grain.
```

This is stronger than surface equality `A=a`.

---

# 13. Why surface treatment equality is insufficient

`A=a` can hide:

```text
different treatment versions
different delivery mechanisms
different timing
different authority context
different policy generation process
different constitutive meaning
```

Therefore:

### Earned firewall G-CONS-1

```text
ObservedLabelEquality != InterventionIdentity
```

Factual consistency is conditional on the intervention object being the same in the relevant sense.

---

# 14. Software matched case

Factual state:

```text
version = 2.1
config = safe
```

Counterfactual antecedent says:

```text
set version label to 2.1
```

but refers to a rebuilt binary with different compile flags.

Surface version equality does not license factual-consistency substitution.

---

# 15. Institutional matched case

Factual actor has status label `member` under charter K.

A counterfactual branch under charter K' also contains status label `member` but with different rights.

Again:

```text
LabelSame != ConstitutiveStatusSame
```

---

# PART III — EFFECTIVENESS

# 16. Intervention effectiveness

In fixed-model hard-intervention semantics, if one explicitly sets:

```text
X := x
```

then X has value x in the resulting intervened model.

Halpern's causal-model axiomatization includes this kind of effectiveness property for interventions.

---

# 17. Scope of effectiveness

WDF2-G retains:

```text
HardSet(X,x) entails X=x within that intervention semantics
```

but rejects universalization to:

```text
policy aimed at X=x guarantees X=x
recommendation for X=x guarantees X=x
institutional authorization of X=x guarantees X=x
mechanism modification intended to produce X=x guarantees X=x
```

### Earned firewall G-EFF-1

```text
InterventionEffectiveness != GoalAchievement
```

---

# PART IV — COMPOSITION / RECURSIVE SUBSTITUTION

# 18. Structural composition intuition

In deterministic unique-solution structural models, a familiar composition principle is roughly:

```text
if under intervention X=x,
Y naturally takes value y and W takes value w,
then additionally fixing Y=y should preserve W=w
```

Halpern's C3 axiom captures this kind of property in the relevant structural-model class.

---

# 19. Why this is not a universal counterfactual law

The principle depends on assumptions such as:

```text
same fixed structural equations
unique-solution semantics
same context/background
ordinary hard interventions
no model-language change
```

Beckers' nondeterministic causal models explicitly reject the universal assumption that an actual world determines one unique counterfactual world and replace deterministic equations with multivalued functions plus a different preservation semantics.

Therefore:

### Earned firewall G-COMP-1

```text
StructuralCompositionAxiom
!= UniversalCrossWorldSubstitutionLaw
```

---

# 20. Local recursive substitution

WDF2-G admits a conditional rule:

```text
if branch B under Δ entails Y=y
and a second hard surgery fixes Y to the same y
and all structures relevant to downstream W remain unchanged,
then preserving W can be licensed in fixed deterministic settings.
```

But the antecedent conditions are part of the law.

---

# PART V — SINGLE-WORLD VS MULTIPLE-WORLD ASSUMPTIONS

# 21. Critical model-class distinction

Richardson/Robins distinguish a single-world model family (FFRCISTG/SWIG style) from the stronger NPSEM with independent errors, described as a multiple-world model in the intervention hierarchy literature.

The multiple-world model is a submodel with stronger cross-world constraints.

---

# 22. Why this matters

A SWIG associated with one intervention represents counterfactual independences inside that intervention world.

It is specifically attractive because it can avoid many experimentally untestable cross-world independence assumptions.

The stronger NPSEM-IE can imply relationships among potential outcomes from different worlds.

### Earned firewall G-SW-1

```text
SingleWorldCoherence != MultipleWorldCrossWorldIndependence
```

---

# 23. Cross-world independence is optional model strength

For example, independence assumptions linking:

```text
M(a)
and
Y(a',m)
```

may be available under stronger structural/error-independence models but are not consequences of mere well-typedness or branch coherence.

Thus:

```text
CrossWorldIndependence
```

belongs in model assumption provenance.

It is not a default logical law.

---

# 24. Coherence before independence

A pair of random variables can be jointly well-defined and highly dependent.

Therefore:

```text
JointlyDefined != Independent
```

This simple fact blocks a major counterfactual modeling collapse.

---

# PART VI — SHARED EXOGENOUS BACKGROUND

# 25. Deterministic SCM coupling

In a deterministic SCM, holding one exogenous assignment `u` fixed while changing interventions creates a natural coupling among counterfactual outcomes:

```text
Y_x(u)
Y_x'(u)
```

This is one powerful semantics for individualized counterfactual comparison.

---

# 26. Shared-U is substantive

The same `u` across branches encodes a particular cross-world relationship.

WDF2-B already showed that interventional marginals do not determine this coupling.

WDF2-G strengthens:

### Earned firewall G-U-1

```text
SameMarginalInterventions
!= SameSharedBackgroundCoupling
```

---

# 27. Mechanism change breaks naive shared-U transport

If surgery changes:

```text
mechanism family
provider architecture
variable dimension
institutional rule ontology
```

then old exogenous variable `U` may no longer have a valid counterpart.

One must either provide:

```text
U-to-U' transport mapping
coarser shared background
partial coupling
no correspondence
```

or admit failure.

---

# 28. Cross-model background mapping

A valid background map can be:

```text
bijective
many-to-one
one-to-many/set-valued
partial
measure-preserving
unavailable
```

No universal exact-noise identity is earned.

---

# PART VII — EXOGENOUS ISOMORPHISM AND FULL COUNTERFACTUAL IDENTIFIABILITY

# 29. Strong recent result

Chen and Du's 2025 work studies complete L3/counterfactual identifiability: all SCMs satisfying assumptions give consistent answers to all causal queries.

They introduce exogenous isomorphism as a model-level notion strong enough to support this goal in special SCM classes.

---

# 30. Foundational lesson

Full counterfactual coherence/equivalence across candidate SCMs can require substantially stronger structure than observational or interventional agreement.

Thus:

```text
L2Agreement != L3Agreement
```

remains binding.

---

# 31. Exogenous isomorphism is not universal identity

Even if exogenous isomorphism is sufficient/useful in a class of SCMs, WDF2-G does not promote it to a Reality-level identity criterion.

### Earned firewall G-EI-1

```text
ExogenousIsomorphism
is a model-class relation,
not universal transworld identity.
```

---

# PART VIII — CROSS-WORLD DEPENDENCE WITHOUT IDENTIFICATION

# 32. Retrospective query

Consider:

```text
E[Y(1) | X=x, Y(0)=y]
```

This conditions a counterfactual outcome on a factual/other-world outcome for the same individual.

Bodik 2026 shows such quantities are generally not identified without extra assumptions and parameterizes the missing relationship through cross-world correlation.

---

# 33. Critical distinction

This query can be perfectly coherent as a joint-potential-outcome object while still empirically underdetermined.

### Earned firewall G-RETRO-1

```text
CrossWorldNonidentification != CrossWorldIncoherence
```

---

# 34. Endpoint assumptions hide coupling commitments

Methods that effectively act as though cross-world correlation is 0 or 1 may provide point-like answers while silently choosing a coupling extreme.

WDF2-G rule:

```text
Coupling assumptions must be provenance-visible.
```

---

# PART IX — COUNTERFACTUAL FAIRNESS PRESSURE

# 35. Infinite data is not enough

2026 counterfactual-fairness work emphasizes that counterfactual quantities require additional nontrivial counterfactual identifiability assumptions; without them, even infinite data do not reliably identify the needed counterfactuals.

---

# 36. Foundational lesson

Again:

```text
PerfectObservedDistributionKnowledge
!= CrossWorldCompletionUniqueness
```

This reinforces WDF2-E/G separation of evidence from semantic/coupling structure.

---

# PART X — RECANTING WITNESS RECONSTRUCTION

# 37. Important correction to an overstrong reading

WDF2-F used recanting-witness pressure to expose incompatible branch requirements.

WDF2-G sharpens this carefully:

### Earned firewall G-RW-1

```text
RecantingWitness != LogicalContradictionOfEveryNestedCounterfactual
```

A nested path-specific counterfactual may remain formally definable under a strong multiple-world structural model even when it lacks a single-world intervention interpretation or is not identified under weaker assumptions.

---

# 38. What recanting witness actually proves for foundations

It demonstrates that one cannot assume:

```text
Every path-specific cross-world quantity
=
One coherent ordinary intervention on existing variables
```

A treatment-induced variable can be required to transmit incompatible treatment components along different paths.

This can block edge/path intervention identification or ordinary-world realization without making every stronger nested semantics meaningless.

---

# 39. Three statuses must remain separate

For a recanting-witness case:

```text
A. nested expression well-defined under strong model
B. identifiable from available/allowed data assumptions
C. realizable as one ordinary intervention
```

can differ.

### Earned firewall G-RW-2

```text
WellDefined != Identified != SingleWorldRealizable
```

---

# PART XI — SIMPLE JOINT-SATISFIABILITY FALSIFIERS

# 40. Same-index contradiction

Claims:

```text
Y_0 = 0
Y_0 = 1
```

for one deterministic token/model/context are jointly incoherent.

Each proposition can be individually satisfiable across different models.

Therefore model/class scope matters.

---

# 41. Different-index plurality

Claims:

```text
Y_0 = 0
Y_1 = 1
```

are not contradictory merely because Y takes different values across branches.

### Earned firewall G-CONTR-1

```text
CrossWorldDifference != Contradiction
```

---

# 42. Nondeterministic same-index case

Under a nondeterministic model, saying:

```text
Y_0 may be 0
Y_0 may be 1
```

can be coherent.

But saying one selected/token solution is simultaneously exactly 0 and exactly 1 at the same locus remains contradictory unless semantics are set-valued.

Thus result-shape typing matters.

---

# 43. Set-valued coherence

For nondeterministic semantics:

```text
Y_0 in {0,1}
```

is different from two exact equality claims.

### Earned firewall G-SET-1

```text
PluralSolutionSet != ContradictoryExactValues
```

---

# PART XII — SOFTWARE CROSS-WORLD CASES

# 44. Same configuration key across versions

Version V has:

```text
cache_mode ∈ {safe,fast}
```

Version V' removes the key and replaces it with a policy object.

Importing:

```text
cache_mode_V = safe
```

into V' is not automatically meaningful.

Status:

```text
CrossModelCorrespondenceRequired
```

not false.

---

# 45. Recompiled binary and seed

Two builds use different PRNG algorithms.

Holding numeric seed `42` fixed does not prove the same latent stochastic realization.

```text
SeedLabelEquality != RandomnessCouplingIdentity
```

---

# 46. Shared test input

By contrast, identical serialized request bytes can often be transported across versions as an explicit input token even if internal latent states cannot.

Cross-world correspondence can therefore be field-specific.

---

# PART XIII — INSTITUTIONAL CROSS-WORLD CASES

# 47. Rule-dependent status

Under K:

```text
credential C constitutes license L
```

Under K':

```text
C constitutes provisional permit P
```

Cross-world query:

```text
What if Actor had C_{K} under K'?
```

needs a decision:

```text
import physical credential token?
import legal status L?
import underlying evidence represented by C?
```

These are different objects.

---

# 48. Constitution firewall

```text
SamePhysicalTokenAcrossRules
!= SameInstitutionalStatusAcrossRules
```

WDF0's physical-token/institutional-status separation is directly preserved.

---

# PART XIV — AGENT / MODEL CROSS-WORLD CASES

# 49. Provider latent-state import

Suppose branch M' generates latent hidden state h'.

Query:

```text
What would provider M output if initialized with h' from M'?
```

may be ill-typed if latent representations differ in dimension/meaning.

Token-level hidden-state import is not guaranteed by both systems being called language models.

---

# 50. Semantic-level correspondence

A coarser cross-world object such as:

```text
conversation facts / tool outputs / user-visible message prefix
```

may transport even when hidden-state identity fails.

Therefore:

```text
CrossWorldCorrespondence can exist at one grain and fail at another.
```

---

# 51. Shared random seed after provider change

Using the same integer seed is merely a control convention unless the providers define compatible random-generation semantics.

Again:

```text
SharedControlToken != SharedExogenousState
```

---

# PART XV — PHYSICAL CASES

# 52. Same initial macrostate, different microstate

Two physical branches can share:

```text
same temperature
same pressure
same visible geometry
```

while differing microscopically.

A chaotic future can diverge dramatically.

Thus macro correspondence does not define micro-level same-background coupling.

---

# 53. Grain-relative coherence

A query about macro outcome can remain coherent under coarse correspondence even if exact particle/token identity is unavailable.

### Earned firewall G-GRAIN-1

```text
CoherenceAtGrain_g
!= CoherenceAtAllFinerGrains
```

---

# PART XVI — COUNTERFACTUAL COMPLETIONS

# 54. Completion concept

A **cross-world completion** is a research construct containing enough branch-indexed assignments/relations to evaluate the requested family of counterfactual claims while satisfying the declared model/correspondence/coupling constraints.

It is not a Reality entity.

---

# 55. Completion need not enumerate all possible worlds

Only the structure needed by the query/domain may be represented.

### Earned firewall G-COMPLETE-1

```text
CounterfactualCompletionForQ != CompleteRealityModalDomain
```

This preserves WDF1 open-world discipline.

---

# 56. Completion statuses

A typed query can yield:

```text
NoCoherentCompletion
OneCoherentCompletion
ManyCoherentCompletions
CompletionFamilyOnlyPartiallyCharacterized
ModelRevisionRequiredBeforeCompletion
AlternativeDomainExtensionRequired
```

---

# 57. Multiple completions are not failure

If several completions survive, WDF2-E applies:

```text
robust invariant
set/bound
completion-dependent verdict
```

No arbitrary completion should be selected.

---

# PART XVII — COHERENCE VS IDENTIFICATION

# 58. Four-way matrix

A counterfactual object can be:

```text
coherent + identified
coherent + unidentified
incoherent + formally typed
ill-typed / model-revision required
```

These statuses are not ordered by one scalar confidence score.

---

# 59. Data cannot repair incoherence

Infinite observational/interventional data cannot make:

```text
Y_0=0 AND Y_0=1
```

true in one deterministic exact-value completion.

### Earned firewall G-DATA-1

```text
EvidenceCannotRepairSemanticContradiction
```

---

# 60. Strong assumptions can shrink completion family

Conversely, monotonicity, bijectivity, rank preservation, exogenous isomorphism, or independence assumptions may reduce the coherent completion family.

But each such assumption stays explicit.

---

# PART XVIII — COHERENCE VS PHYSICAL REALIZABILITY

# 61. Nested cross-world object

`Y(a',M(a))` cannot generally be physically realized by assigning one unit to two incompatible values of A at one time.

Robins/Richardson/Shpitser explicitly describe this as a cross-world counterfactual rather than an ordinary joint experimental intervention.

---

# 62. Yet formal coherence can survive

A structural model can still define the nested variable by recursive substitution.

Therefore:

### Earned firewall G-PHYS-1

```text
NotSingleWorldExecutable
!= FormallyIncoherent
```

---

# 63. Actionability remains role-gated

For planning/recourse:

```text
non-executable nested quantity
```

may be unsuitable as an action prescription.

For explanation/decomposition:

it can remain mathematically meaningful.

WDF2-D remains intact.

---

# PART XIX — MODEL-CLASS RELATIVITY OF CONSISTENCY AXIOMS

# 64. Recursive deterministic models

These support strong structural axioms such as effectiveness and composition under their semantics.

---

# 65. Unique-solution but nonrecursive models

Halpern shows that changing model class changes the correct axiomatization; recursive-model properties cannot simply be assumed unchanged.

---

# 66. Arbitrary/multiple-solution models

Further language and semantic changes are needed.

Beckers 2025 supplies a modern nondeterministic alternative with its own sound/complete axiomatization and preservation policy.

### Strong result

```text
CounterfactualConsistencyLaw is model-class indexed.
```

---

# 67. No universal C3/C4 promotion

WDF2-G therefore treats familiar SCM axioms as:

```text
powerful conditional laws inside declared counterfactual model classes
```

not metaphysical axioms of Reality.

---

# PART XX — JOINT DISTRIBUTIONS OVER POTENTIAL OUTCOMES

# 68. Marginals do not determine joint

Knowing:

```text
P(Y_0)
P(Y_1)
```

is insufficient to determine:

```text
P(Y_0,Y_1)
```

This was central in WDF2-B/E.

---

# 69. Joint distributions require coupling

A cross-world joint distribution is itself a substantive object.

Bodik's 2026 retrospective prediction makes this explicit through cross-world correlation.

---

# 70. Coherent coupling set

Instead of one coupling, a foundation-safe answer can preserve:

```text
Couplings compatible with marginals + declared assumptions
```

Then return robust/bounded cross-world conclusions.

---

# PART XXI — CROSS-WORLD INDEPENDENCE PRESSURE

# 71. Independent errors

NPSEM-IE-style assumptions can induce strong cross-world independences because potential outcomes are functions of independent exogenous disturbances.

These assumptions may yield identification unavailable in weaker single-world models.

---

# 72. Independence is epistemically strong

Because cross-world pairs cannot generally be jointly observed for the same unit, many such independence relations are not directly experimentally testable.

This is one reason SWIG/single-world approaches deliberately avoid treating them as default.

---

# 73. Foundation rule

```text
CrossWorldIndependence
must declare:
  model class
  variable decomposition
  error/background semantics
  evidence status
```

No silent import.

---

# PART XXII — IMPOSSIBLE / COUNTERCONVENTIONAL BRANCH PRESSURE

# 74. A branch can be locally inadmissible under current domain semantics

Examples:

```text
logical contradiction
nomologically impossible antecedent
constitutively impossible status
model-inconsistent assignment
semantic/conventional revision
```

WDF2-A typed these cases but did not solve their semantics.

---

# 75. Cross-world coherence now exposes the gap

Suppose one nested expression imports a value from an impossible branch.

Questions arise:

```text
Can the source branch produce any value?
Does impossible-world extension provide a counterpart value?
Does import preserve logical explosion or avoid it?
Can a constitutively impossible status be reinterpreted under revised rules?
```

WDF2-G cannot answer these without a theory of counterpossible/domain-revising antecedents.

This becomes the largest residual.

---

# PART XXIII — COUNTERFACTUAL CONTRADICTION VS DOMAIN REVISION

# 76. Contradiction

Within a fixed typed model:

```text
same exact locus/index simultaneously required to equal distinct exclusive values
```

can be contradiction.

---

# 77. Domain revision

If antecedent changes the meaning/range/constitution of the locus, then ordinary contradiction rules may not apply until the revised domain is defined.

Example:

```text
“What if a revoked credential were still legally valid under the same revocation rule?”
```

may be constitutively inconsistent.

But:

```text
“What if the rule were changed so revoked credentials remained valid?”
```

is a rule-revision counterfactual.

### Earned firewall G-REV-1

```text
ContradictoryWithinFixedDomain
!= DomainRevisingAntecedent
```

---

# PART XXIV — ROBUSTNESS OVER COMPLETIONS

# 78. Completion-robust would

Let:

```text
Coh = coherent completions for Q
```

Then:

```text
CompletionRobustWould(C)
:= for all K in Coh, Would_K(C)
```

This is another quantifier layer beyond generator and composition-plan uncertainty.

---

# 79. Quantifier stack

A maximally explicit robust claim may require:

```text
for all admissible generators G
for all admissible composition plans P
for all coherent cross-world completions K
for all relevant internal alternatives a
  C(a)
```

### Earned firewall G-Q-1

```text
GeneratorRobust
!= CompositionRobust
!= CompletionRobust
```

---

# 80. Collapse only when equivalence is proved

If several axes induce identical target results, they can be quotient/abstracted for that query.

But collapse must follow an equivalence proof, not precede it.

---

# PART XXV — MINIMAL COHERENCE CONTRACT

# 81. Research grammar

A cross-world stitched query needs at least:

```text
BranchSet
Branch-local model semantics
Index/anchor scope
Target correspondence map
Background/coupling policy
Stitch/import operations
Joint constraints
Result shape
Model-class provenance
```

plus evidence/identification status when making Reality-facing claims.

This is not a production schema.

---

# 82. Candidate coherence diagnostic

Research-only:

```text
Coh(Claims | F,MC) iff
  WellTyped
  ∧ AllBranchesLocallyCoherent
  ∧ CorrespondenceValid
  ∧ CouplingDefinedWhereRequired
  ∧ StitchOperationsCompatible
  ∧ JointConstraintsSatisfiable
  ∧ NoHiddenDomainRevision
```

`Coh` does not imply uniqueness or identification.

---

# PART XXVI — DELETION TESTS

# 83. Identify coherence with cross-world independence

**FAIL**.

Single-world models permit coherent causal reasoning while avoiding strong multiple-world independence assumptions.

---

# 84. Identify coherence with point identification

**FAIL**.

Retrospective cross-world prediction and counterfactual fairness provide direct modern counterexamples.

---

# 85. Identify coherence with physical executability

**FAIL**.

Nested mediation quantities can be formally defined without corresponding to one ordinary joint intervention.

---

# 86. Treat same variable name as identity

**FAIL** across model/rule/grain changes.

---

# 87. Require exact same exogenous U for all cross-world identity

**FAIL** across model/mechanism changes and as an ontological claim.

---

# 88. Remove factual consistency entirely

**FAIL**.

Typed consistency between factual realization and exactly matching intervention semantics is essential.

---

# 89. Apply factual consistency from surface treatment label alone

**FAIL** due versions/timing/constitutive differences.

---

# 90. Promote SCM effectiveness/composition axioms to Reality laws

**FAIL** across nondeterministic/general/model-changing cases.

---

# 91. Treat recanting witness as universal logical contradiction

**FAIL**.

It can instead separate nested-model definability from single-world realization/identification.

---

# 92. Treat recanting witness as irrelevant

**FAIL**.

It exposes genuine limits on collapsing path-specific cross-world objects into ordinary interventions.

---

# 93. Select one coherent completion arbitrarily

**FAIL**.

WDF2-E robustness/set-valued semantics applies.

---

# 94. Let data rescue no-coherent-completion cases

**FAIL**.

Semantic/structural contradiction is prior to statistical estimation.

---

# PART XXVII — EXTERNAL RESEARCH PRESSURE

# 95. Halpern axiomatization

Halpern's causal-model work provides explicit model-class-specific axiomatizations. In recursive deterministic settings, composition/effectiveness-like principles follow from the intervention semantics; more general model classes require different treatment.

Foundational pressure:

```text
counterfactual laws depend on model class.
```

---

# 96. Beckers nondeterministic models

Beckers 2025 drops unique structural response and unique counterfactual-world assumptions and supplies a sound/complete logic for multivalued causal equations with a different preservation semantics.

Foundational pressure:

```text
unique-world consistency is not universal.
```

---

# 97. SWIG / single-world model

Richardson and Robins' SWIG framework represents independences for one hypothetical intervention and highlights a weaker single-world causal model that avoids many untestable cross-world independence assumptions.

Foundational pressure:

```text
cross-world independence is extra structure.
```

---

# 98. Intervention hierarchy

Shpitser/Tchetgen's graphical hierarchy explicitly distinguishes the single-world model from the stronger multiple-world NPSEM-IE submodel.

Foundational pressure:

```text
stronger cross-world constraints buy stronger identification but are not free.
```

---

# 99. Interventionist mediation

Robins, Richardson and Shpitser show nested `Y(a',M(a))` is a genuine cross-world object that generally cannot be implemented by assigning one unit two incompatible treatment values simultaneously; separable-component interventionist reformulations move assumptions rather than erase them.

Foundational pressure:

```text
formal cross-world definability != ordinary intervention realizability.
```

---

# 100. Exogenous isomorphism

Chen and Du 2025 study complete counterfactual/L3 identifiability and use exogenous isomorphism to characterize strong model agreement in special SCM classes.

Foundational pressure:

```text
full cross-world agreement requires stronger structure than L1/L2 agreement.
```

---

# 101. Retrospective cross-world prediction

Bodik 2026 shows `E[Y(1)|Y(0)=y,X=x]` is generally unidentified and introduces cross-world correlation as explicit sensitivity structure.

Foundational pressure:

```text
coherent cross-world joint quantities can remain unidentified.
```

---

# 102. Counterfactual fairness

Ma et al. 2026 emphasize that nontrivial counterfactual-identifiability assumptions are required and that infinite data alone do not guarantee the needed counterfactual identification.

Foundational pressure:

```text
observational perfection does not identify cross-world structure.
```

---

# 103. Counterfactual influence over trajectories

Kazemi et al. 2025 show factual influence can vanish in long counterfactual MDP trajectories, turning individualized counterfactual reasoning effectively interventional.

Foundational pressure:

```text
branch correspondence/coupling can degrade over sequential evolution.
```

---

# PART XXVIII — WDF0 / WDF1 REOPEN AUDIT

# 104. WDF0

No FoundationReopenCondition fires.

WDF2-G reinforces:

```text
IdentifierEquality != OntologicalIdentity
Same_X != Same_Y without criterion
Constitution != Causation
PhysicalToken != InstitutionalStatus
Model != Reality
```

Cross-world identity is criterion/model/grain relative; no universal transworld identity primitive is earned.

WDF0 remains frozen.

---

# 105. WDF1

No FoundationReopenCondition fires.

WDF1 already prohibited:

```text
CurrentAlternativeDomain != CompleteRealityModalDomain
ModelModalProjection != RealityModalTruth
```

WDF2-G's query-relative completion concept and model-class-relative coherence fit those constraints.

WDF1 remains frozen.

---

# PART XXIX — RECONSTRUCTION

# 106. Cross-world result ladder

A research-facing evaluation can now distinguish:

```text
IllTyped
LocallyIncoherentBranch
CorrespondenceMissing
CouplingMissing
StitchConflict
NoJointCompletion
ManyCoherentCompletions
CompletionRobustResult
CompletionDependentResult
CoherentButUnidentified
IdentifiedWithinAssumptions
ModelRevisionRequired
AlternativeDomainExtensionRequired
```

These statuses should never be compressed to `unknown`.

---

# 107. Strong result — coherence is existential, robustness is universal

At the completion level:

```text
Coherent(Q)
:= exists at least one admissible completion
```

while:

```text
RobustResult(Q,C)
:= C holds across all relevant admissible completions
```

### Earned firewall G-EXFORALL-1

```text
ExistenceOfCoherentInterpretation
!= RobustCounterfactualTruth
```

---

# 108. Strong result — correspondence is not coupling

One can know which entity in branch B corresponds to branch A without knowing the probabilistic joint/coupling of their outcomes.

Therefore:

```text
CorrespondenceRelation != CrossWorldProbabilityCoupling
```

This separation is now mandatory.

---

# 109. Strong result — coherence is model-class relative but not arbitrary

A sentence family can be coherent under NPSEM-IE and not evaluable under a weaker single-world model.

This does not mean coherence is subjective.

It means:

```text
Coherent relative to explicitly declared semantics/model class.
```

### Earned firewall G-REL-1

```text
Relative != Subjective
```

WDF0 firewall survives directly.

---

# 110. Strong result — stronger semantics can both enable and overcommit

Adding a stronger cross-world model can:

```text
define more joint quantities
identify more targets
```

but also:

```text
assert untestable independence/coupling structure
exclude coherent weaker-model completions
```

Thus model strength is not monotonic goodness.

---

# PART XXX — LARGEST REMAINING RESIDUAL

# 111. Why impossible antecedents now become upstream

WDF2-G can evaluate coherence when all branches live inside an interpretable model/domain extension.

But WDF2-A already identified several impossible-antecedent types:

```text
logical
nomological
metaphysical candidate
constitutive
model inconsistent
semantic/conventional shift
unknown
```

Cross-world stitching now forces the unresolved question:

> **What can a branch contribute if its antecedent is impossible under the current domain/model?**

---

# 112. Current architecture cannot answer uniformly

For:

```text
logical contradiction
```

ordinary classical semantics threatens vacuity/explosion.

For:

```text
nomological impossibility
```

one may revise laws or extend alternative domain.

For:

```text
constitutive impossibility
```

one may need rule/convention revision.

For:

```text
model inconsistency
```

one may need model revision rather than Reality impossibility.

These are not one case.

---

# 113. Cross-world import makes counterpossible semantics unavoidable

Suppose:

```text
branch B antecedent impossible
branch B generates value v
branch A imports v
```

Without a counterpossible/domain-extension semantics, even `v` has no grounded status.

Thus impossible antecedents are no longer a peripheral modal issue; they block completion semantics directly.

---

# 114. Exact next round

The next canonical round is therefore:

# **WDF2-H — Counterfactual Impossibility / Counterpossibles / Domain-Revising Antecedents**

WDF2-H should test:

```text
logical vs nomological vs constitutive vs model impossibility
vacuous truth vs non-vacuous counterpossibles
impossible-world semantics
law-revising counterfactuals
rule/convention-revising counterfactuals
model-revision antecedents
branch generation under impossible antecedents
cross-world import from impossible branches
identity/correspondence under domain revision
whether preservation can survive law/rule revision
robustness across alternative-domain extensions
```

It must not preselect impossible-world semantics or declare all impossible-antecedent counterfactuals vacuously true.

Only WDF2-H residuals may determine WDF2-I.

---

# 115. Production disposition

No production changes are admitted.

Do **not** add:

```text
CrossWorldCompletion
CoherenceSolver
PotentialOutcomeJoint
ExogenousIsomorphismMapper
CrossWorldCoupling
ConsistencyValidator
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

Counterfactual Foundations remain open.

---

# 116. Closeout

```text
WDF2-G: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D/E/F reopen: NO
Production refactor: NO

CrossWorldCoherence != CrossWorldIndependence
IndividualSatisfiability != JointSatisfiability
ObservedLabelEquality != InterventionIdentity
SameVariableName != CrossWorldIdentity
Correspondence != Coupling
SameIndividual != SameExogenousRepresentation by definition
OneCoherentCompletionExists != ResultIdentified
CrossWorldNonidentification != CrossWorldIncoherence
WellDefined != Identified != SingleWorldRealizable
RecantingWitness != LogicalContradictionOfEveryNestedCounterfactual
NotSingleWorldExecutable != FormallyIncoherent
CounterfactualConsistencyLaw is model-class indexed
CoherenceAtGrain_g != CoherenceAtAllFinerGrains
ContradictoryWithinFixedDomain != DomainRevisingAntecedent
GeneratorRobust != CompositionRobust != CompletionRobust

Exact next round:
WDF2-H — Counterfactual Impossibility / Counterpossibles / Domain-Revising Antecedents
```

Compressed result:

> **WDF2-G establishes that cross-world coherence is neither cross-world independence nor empirical identifiability. A nested counterfactual system must pass several distinct gates: expressions must be well typed; each branch must be locally coherent; entities/variables must have an explicit cross-branch correspondence; any shared-background or probabilistic coupling must be declared; imported branch values must be admissible in the receiving branch; and the resulting claim family must have at least one joint counterfactual completion. Familiar factual-consistency, effectiveness and composition principles survive only as typed, model-class-relative laws: deterministic recursive SCM axioms cannot be promoted into universal laws once nondeterminism, model revision, constitutive change or different coupling semantics are admitted. Richardson/Robins single-world models show that coherent causal reasoning need not import the stronger cross-world independence assumptions available in NPSEM-IE multiple-world models. Conversely, modern retrospective prediction and counterfactual-fairness results show that cross-world quantities can be coherent yet remain unidentified even with extensive or infinite data. Recanting-witness cases are correspondingly sharpened: they do not prove that every nested counterfactual is logically contradictory, but they do block the collapse of path-specific cross-world objects into ordinary single-world interventions under weaker semantics. The correct research object is therefore a family of coherent cross-world completions, with WDF2-E robustness applied across that family. The largest remaining gap now concerns branches that cannot be generated inside the current domain at all—logical, nomological, constitutive or model-level impossibilities. Cross-world import makes this unavoidable, so WDF2 advances next to counterpossibles and domain-revising antecedents.**
