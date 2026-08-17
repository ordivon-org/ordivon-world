# WDF2-K — Counterfactual Consequence / Inference / Detachment / Iteration

Status: **complete for WDF2-K**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D/E/F/G/H/I/J remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-K residuals:

```text
WDF2-L — Counterfactual Context / Supposition / Update / Dynamic Re-Anchoring
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-A through J reconstructed counterfactual antecedent content, generator admissibility, underdetermination, multi-locus composition, cross-world coherence, impossible antecedents, hyperintensional relevance and Boolean/alternative structure.

WDF2-K asks the next question:

> **Given those structures, what inferences among counterfactual claims are actually sound, and relative to which evaluation frame, model class, antecedent semantics and truth role?**

The round stress-tests:

```text
factual detachment / modus ponens
modus tollens
contraposition
transitivity / hypothetical syllogism
strengthening / weakening
SDA as inference
substitution of equivalents
Conditional Excluded Middle
Conditional Non-Contradiction
would/might duality
import-export
nested / iterated counterfactuals
KLM-style nonmonotonic principles
probabilistic counterfactual inference
semantic validity vs supposition / action / explanation
```

No Lewis, Stalnaker, Williamson, SCM/interventionist, premise, KLM/preferential or probabilistic logic is preselected as universal.

---

# 2. First decisive result — counterfactual inference is frame-indexed

The object manipulated by an inference is not merely a formula.

At minimum, counterfactual evaluation can depend on:

```text
Anchor
AntecedentContent
Alternative/RouteStructure
Generator/ModelClass
PreservationProfile
BacktrackingPolicy
Identity/Correspondence
CompositionPlan
DomainExtension
TruthRole
RouteAggregator
ProbabilityInterpretation
QueryRole
```

Call the relevant bundle an **EvaluationFrame**.

### Earned firewall K-FRAME-1

```text
SameFormula != SameEvaluationFrame
```

Many apparent inference failures are cases where premise and conclusion silently use different frames.

---

# 3. Inference validity is not one relation

Distinguish:

```text
formula validity within one semantics
model-class validity
truth preservation at actual anchor
suppositional consequence
conditional-assertion closure
intervention execution consequence
epistemic acceptance
explanatory consequence
decision/action recommendation
```

### Earned firewall K-INF-1

```text
SemanticValidity
!= SuppositionalAcceptability
!= Actionability
!= ExplanatorySupport
```

---

# PART I — FACTUAL DETACHMENT / MODUS PONENS

# 4. Familiar pattern

```text
A
A □→ C
----------
C
```

For material implication this is ordinary modus ponens.

For counterfactuals it is not foundation-safe without extra conditions.

---

# 5. Strong-centering route

If the actual world/state is itself among the selected/closest A alternatives whenever A is actually true, then:

```text
A actual
+
A □→ C
```

forces C at the actual state.

This is the familiar strong-centering path to factual detachment.

---

# 6. Interventionist failure

Briggs' extended interventionist semantics provides a direct counterexample to universal modus ponens.

In that framework, even when antecedent A is already factually true, evaluating the counterfactual can still **intervene** to set A true, replacing its structural equation.

Thus:

```text
factual A
```

and:

```text
A-under-intervention
```

can differ causally.

### Earned firewall K-MP-1

```text
AntecedentTruth != AntecedentRealizationMatch
```

---

# 7. Actual value vs intervention on same value

Suppose factual model has:

```text
X = f(P)
X factual value = 1
```

Counterfactual antecedent:

```text
do(X:=1)
```

replaces the mechanism for X.

Although the value remains 1, downstream behavior under nested or mechanism-sensitive queries can differ.

### Earned firewall K-MP-2

```text
ActualValueEquality != NoOpIntervention
```

---

# 8. Exogenous-intervention recovery

Vandenburgh's exogenous-intervention model takes the opposite structural stance for actual antecedents: if A already holds, the exogenous A-intervention can be empty.

That strong-centering-style property restores modus ponens.

Foundational lesson:

```text
MP validity depends on antecedent realization semantics.
```

---

# 9. Contextually restricted strict conditional

Williamson's contextually restricted strict-conditional semantics provides another striking rival: transitivity, contraposition and antecedent strengthening can hold while modus ponens fails because the contextual restriction need not contain the actual world.

Therefore:

### Earned firewall K-MP-3

```text
CounterfactualMP != MinimalRequirementForEveryCoherentCounterfactualLogic
```

---

# 10. Typed factual detachment condition

A safe research rule is:

```text
A factual
A □→ C
RealizationMatch(actual A, antecedent A)
ActualAnchorIncluded
same target/content grain
same framework/preservation
--------------------------------
C factual
```

This is stronger than surface truth of A.

---

# 11. Factual consistency link

WDF2-G's typed factual consistency is the relevant bridge:

```text
ObservedLabelEquality != InterventionIdentity
```

If actual realization and antecedent realization are not the same intervention/content object, factual detachment is not licensed.

---

# PART II — MODUS TOLLENS VS CONTRAPOSITION

# 12. Actual modus tollens

Pattern:

```text
A □→ C
NOT C actual
-----------
NOT A actual
```

This can be derived only when factual detachment plus ordinary actual-level classical reasoning is available.

If MP/factual detachment fails, this route fails too.

---

# 13. Counterfactual contraposition

Different pattern:

```text
A □→ C
-------------
NOT C □→ NOT A
```

This changes the antecedent and generator target.

### Earned firewall K-MT-1

```text
ActualModusTollens != CounterfactualContraposition
```

---

# 14. Why contraposition can fail

Suppose:

```text
A = sprinkler is on
C = lawn is wet
```

`A □→ C` may be true.

But:

```text
NOT C □→ NOT A
```

can fail because a dry-lawn antecedent can be realized through evaporation, covering, drainage or other mechanisms while sprinkler remains on.

Negation route multiplicity from WDF2-J blocks unrestricted contraposition.

---

# 15. Rival strict semantics

Williamson's strict context-restricted theory validates contraposition inside its semantics.

So the failure is not a theorem of every conditional logic.

### Earned firewall K-CP-1

```text
Contraposition is model/semantics-class indexed.
```

---

# PART III — TRANSITIVITY / HYPOTHETICAL SYLLOGISM

# 16. Familiar pattern

```text
A □→ B
B □→ C
----------
A □→ C
```

This is not generally sound under nearest-alternative semantics.

---

# 17. Minimal anchor-shift countermodel

Let actual anchor be w0.

Suppose:

```text
closest A-world from w0 = w1
w1 satisfies B but not C

closest B-world from w0 = w2
w2 satisfies C
```

Then:

```text
A □→ B   true
B □→ C   true
A □→ C   false
```

The middle proposition B is reached through different routes.

---

# 18. Strong result — middle-content equality is insufficient

### Earned firewall K-TRANS-1

```text
SameIntermediatePropositionB
!= SameBRealization/Frame
```

Transitivity needs more than formula matching.

---

# 19. Frame-stable transitivity

A local transitivity theorem can hold if:

```text
B-realization selected under A
matches the B-frame assumed by B □→ C
C evaluation preserves the A-induced frame
no re-anchoring changes relevant alternatives
```

This is a strong compatibility condition.

---

# 20. Strict-conditional rival

Contextually restricted strict implication naturally supports transitivity if all conditionals quantify over the same relevant domain.

Again:

```text
GeneralTransitivityInvalid
!= NoTransitiveCounterfactualSemantics
```

---

# PART IV — CONSEQUENT WEAKENING

# 21. Right weakening

If under the same object logic/framework:

```text
C entails D
```

and:

```text
A □→ C
```

then one expects:

```text
A □→ D
```

when the same selected alternatives and truth role are used.

---

# 22. Typed validity

### Earned firewall K-RW-1

```text
RightWeakening is safe only relative to the same consequent logic/content interpretation.
```

Semantic revision or hyperintensional consequent operators can break a naive syntactic application.

---

# 23. Conjoining consequents

If:

```text
A □→ B
A □→ C
```

are evaluated over exactly the same nonempty selected alternative family, then:

```text
A □→ (B AND C)
```

holds for universal would semantics.

---

# 24. Provenance mismatch

If the two premises survive under different generator families or different domain extensions, conjunction is not automatic.

### Earned firewall K-AND-1

```text
SameAntecedentText != SameAdmissibleAlternativeFamily
```

Need a shared model/completion witness or robustness across their intersection.

---

# PART V — ANTECEDENT STRENGTHENING / WEAKENING

# 25. General strengthening remains invalid

WDF2-J already showed:

```text
A □→ C
```

does not entail:

```text
A AND B □→ C
```

because B can alter surgery, mechanism, preservation or route structure.

---

# 26. Cautious strengthening possibility

If B is already a robust consequence of A and adding B does not intervene on/fix its mechanism, strengthening can sometimes preserve C.

But this is stronger than syntactic conjunction.

---

# 27. Premise addition vs intervention addition

This distinction becomes central:

```text
add premise B to supposition
```

can mean:

```text
restrict to A-cases where B naturally holds
```

whereas:

```text
intervene to enforce B
```

can destroy the route by which B arose.

### Strong firewall K-ADD-1

```text
PremiseStrengthening != InterventionAugmentation
```

---

# PART VI — SDA AS AN INFERENCE RULE

# 28. Route-wise SDA

Under WDF2-J route semantics:

```text
(A OR B) □→ C
```

can encode:

```text
A-route □→ C
AND
B-route □→ C
```

Then SDA is essentially projection from an all-route claim.

---

# 29. Global-union SDA failure

Under a closest-within-union semantics, the disjunct not represented among selected closest worlds can be unconstrained.

Thus SDA is not globally valid.

---

# 30. Inference status

### Earned firewall K-SDA-1

```text
SDA is valid only after antecedent route semantics is fixed.
```

It cannot be inferred from classical `or` truth conditions alone.

---

# PART VII — SUBSTITUTION OF EQUIVALENTS

# 31. Left logical equivalence

KLM-style/default logics often adopt a Left Logical Equivalence rule.

WDF2-I/J already falsified this as a universal counterfactual rule.

---

# 32. Typed substitution

Safe replacement requires preserving the equivalence criterion relevant to the inference:

```text
Boolean truth condition
alternative structure
surgery semantics
framework revision
topic/grain
preservation consequences
```

### Earned firewall K-LLE-1

```text
LogicalEquivalence != Inference-LevelSubstitutability
```

---

# PART VIII — CONDITIONAL EXCLUDED MIDDLE

# 33. CEM

```text
(A □→ C)
OR
(A □→ NOT C)
```

---

# 34. Unique-selected-alternative route

If each antecedent A selects exactly one determinate alternative and C is bivalent there, CEM follows.

This is Stalnaker-like pressure.

---

# 35. Plural alternatives

If closest/admissible A alternatives include:

```text
some C
some NOT C
```

then neither universal would-claim holds.

Lewis-style plurality therefore allows CEM failure.

---

# 36. Nondeterministic causal models

Barbero's work on interventionist counterfactuals under indeterministic causal laws shows that deterministic and indeterministic model classes require materially different axiomatizations.

This directly undermines universalizing deterministic CEM-style reasoning.

---

# 37. Potential-outcome pressure

Lin 2024 connects CEM to the traditional Rubin/potential-outcome framework, where unit-level potential outcomes are typically determinate enough to support CEM-like reasoning for bivalent targets.

He then develops a causal-inference theory that dispenses with CEM while retaining inferential success by integrating potential-outcome and causal-Bayes-net structure.

### Earned firewall K-CEM-1

```text
CEM is not indispensable to causal inference as such.
```

---

# 38. Williamson rival

Williamson's 2020 account also rejects CEM because `would` may quantify over multiple relevant worlds.

Thus both philosophical and causal-model pressure reject universal CEM.

---

# PART IX — CONDITIONAL NON-CONTRADICTION

# 39. CNC candidate

```text
NOT[(A □→ C) AND (A □→ NOT C)]
```

---

# 40. Nonempty classical selected family

For universal would over a nonempty set of classical A alternatives, both claims cannot hold simultaneously.

---

# 41. Empty antecedent family

Under vacuous possible-world semantics for impossible A:

```text
A □→ C
```

and:

```text
A □→ NOT C
```

can both be vacuously true.

### Earned firewall K-CNC-1

```text
ConditionalNonContradiction depends on antecedent-domain/nonvacuity assumptions.
```

---

# PART X — WOULD / MIGHT

# 42. Fixed-family quantifiers

For one explicit nonempty alternative family S_A:

```text
Would(A,C) := for all a in S_A, C(a)
Might(A,C) := exists a in S_A, C(a)
```

Then standard universal/existential relations are available.

---

# 43. Fixed-family duality

Under classical bivalent C and the same S_A:

```text
Might(A,C)
iff
NOT Would(A,NOT C)
```

can hold.

---

# 44. Robust-family failure

WDF2-E distinguished:

```text
RobustMight := for all generators G, exists alternative a with C
```

from:

```text
NOT RobustWouldNot
= exists generator G, exists alternative a with C
```

These are not equivalent.

### Earned firewall K-WM-1

```text
Would/MightDualityAtFixedFamily != RobustCrossFamilyDuality
```

---

# 45. Route quantification adds another axis

For disjunctive antecedents:

```text
for every route, exists an outcome C
```

is different from:

```text
exists route and outcome C
```

WDF2-J and WDF2-E quantifier order jointly apply.

---

# PART XI — IMPORT / EXPORT

# 46. Candidate principle

Compare:

```text
A □→ (B □→ C)
```

with:

```text
(A AND B) □→ C
```

---

# 47. WDF2-F obstruction

Nested evaluation can re-anchor:

```text
factual world -> A-branch -> evaluate B from A-branch
```

while the conjunctive query can instead evaluate:

```text
factual world -> joint A+B branch
```

These need not coincide.

### Earned firewall K-IE-1

```text
NestedSupposition != JointAntecedent by default
```

---

# 48. Frame-stable import-export condition

A local import-export theorem requires something like:

```text
Sel_B(Sel_A(F))
=
Sel_{A AND B}(F)
```

plus:

```text
stable preservation
stable identity/correspondence
same composition semantics
no model revision
no cross-world stitch difference
```

---

# 49. Causal unnesting is not generic import-export

Correa, Lee and Bareinboim prove a Counterfactual Unnesting Theorem for nested counterfactuals in their causal-model framework, enabling reduction of arbitrary nested counterfactuals to unnested forms for identification analysis.

This is a strong model-class theorem.

### Earned firewall K-CUT-1

```text
SCMCounterfactualUnnesting != UniversalLogicalImportExport
```

---

# PART XII — ITERATED COUNTERFACTUALS

# 50. Same-branch continuation

```text
A □→ (B □→ C)
```

can mean:

```text
evaluate A
then from that A-world/frame evaluate B
```

This preserves A-induced surgery/background unless explicitly reset.

---

# 51. Re-evaluated supposition

A nested conditional can instead trigger a fresh B-evaluation under a new contextual restriction.

---

# 52. Cross-world import

Nested expressions can import a branch-generated value into another branch.

WDF2-F/G already separated this from same-branch continuation.

---

# 53. Iteration requires explicit scope

### Earned firewall K-ITER-1

```text
NestedCounterfactualSyntax != OneUniversalIterationSemantics
```

AnchorScope and frame inheritance must be explicit.

---

# PART XIII — TRANSFORMING A CONDITIONAL ITSELF

# 54. Conditional antecedent

Expressions such as:

```text
If (A □→ B) were true, then C
```

are higher-order relative to ordinary object-level counterfactuals.

They can concern:

```text
model structure
semantic fact
law/counterfactual dependence
agent belief about a conditional
```

---

# 55. Truth about a conditional vs making it true

### Earned firewall K-HO-1

```text
SupposeCounterfactualClaimTrue
!= InterventionThatMakesItsConsequentTrue
```

Higher-order conditional antecedents need truth-role typing.

---

# PART XIV — KLM / PREFERENTIAL CONSEQUENCE PRESSURE

# 56. Why KLM is relevant

Kraus, Lehmann and Magidor develop nonmonotonic consequence relations and preferential semantics, including System P.

Counterfactual consequence shares a key structural feature:

```text
adding antecedent information can retract conclusions.
```

But the match is not exact.

---

# 57. System P rule family

System P includes familiar closure patterns such as:

```text
Reflexivity
Left Logical Equivalence
Right Weakening
And
Or
Cautious Monotony
Cut
```

Rational consequence adds stronger ranked-model behavior such as Rational Monotony.

---

# 58. Typed reflexivity

A successful antecedent realization generally supports:

```text
A □→ A
```

when A's content is stable and realization actually satisfies A.

But impossible/no-admissible-alternative statuses must not be silently converted into ordinary truth.

---

# 59. Left Logical Equivalence fails universally

WDF2-I/J already supplied direct hyperintensional counterexamples.

Thus System-P closure cannot be imported wholesale.

---

# 60. Right Weakening often survives locally

If the consequent logic is fixed and C entails D at every selected alternative, right weakening is safe.

---

# 61. And rule often survives under a shared frame

If the same selected alternatives all satisfy B and all satisfy C, they satisfy B∧C.

But provenance mismatch across different generator/model families can block combination.

---

# 62. Or rule and route semantics

From:

```text
A □→ C
B □→ C
```

route-wise disjunction naturally supports:

```text
(A OR B) □→ C
```

This mirrors System P's Or rule.

A holistic/non-route disjunctive reading need not.

---

# 63. Cautious Monotony pressure

KLM Cautious Monotony roughly says:

```text
A ~ B
A ~ C
----------
A AND B ~ C
```

In premise-restriction semantics this is natural.

In interventionist counterfactual semantics, explicitly adding B can intervene on a variable that previously arose naturally under A and thereby change C.

### Strong firewall K-KLM-1

```text
KLMConjunctionAsPremiseRestriction
!= CounterfactualConjunctionAsPossibleSurgery
```

---

# 64. Cut pressure

KLM Cut roughly:

```text
A ~ B
A AND B ~ C
----------
A ~ C
```

Again, if `A∧B` means an intervention forcing B rather than selecting A-cases where B naturally holds, the inference can fail.

---

# 65. Rational Monotony pressure

Ranked/preferential logics can license a form of rational strengthening when B is compatible with the normal A-cases.

Counterfactual surgery can still make B's explicit addition mechanistically active.

Therefore:

```text
RationalMonotony
```

is not foundation-universal.

---

# 66. KLM remains valuable as a comparison algebra

System P/R provide a mature taxonomy of nonmonotonic closure principles and representation theorems.

WDF2-K uses them as falsification probes, not as the ontology/semantics of counterfactuals.

---

# PART XV — CUT AND CAUTIOUS MONOTONY RECONSTRUCTED

# 67. Natural-B restriction

Define a special operation:

```text
Restrict(A-worlds, B naturally true)
```

This differs from:

```text
Intervene(B:=true)
```

---

# 68. Local cumulative behavior

Within a premise/background or fixed preferential semantics, Cut and Cautious Monotony can survive.

Within a surgery semantics, they require a **naturalization condition**:

```text
B is added as a selection/restriction,
not as a new mechanism-changing intervention.
```

---

# 69. Strong result

### Earned firewall K-NAT-1

```text
ConditionOnB != Do(B)
```

This familiar causal distinction reappears at the level of inference rules.

---

# PART XVI — NONMONOTONICITY TYPES

# 70. Antecedent nonmonotonicity

Adding B can retract C:

```text
A □→ C
but
A AND B □→ NOT C
```

---

# 71. Model nonmonotonicity

Adding evidence/model structure can remove an admissible generator and change a counterfactual verdict.

---

# 72. Context nonmonotonicity

Supposing or asserting new material can change which alternatives are relevant/closest.

---

# 73. Rule-revision nonmonotonicity

Changing institutional/semantic rules can alter proposition content itself.

### Earned firewall K-NM-1

```text
CounterfactualNonmonotonicity != OneSinglePreferentialPhenomenon
```

---

# PART XVII — PROBABILISTIC COUNTERFACTUAL INFERENCE

# 74. Probability is not truth

From:

```text
P(C_A | evidence)=0.99
```

one cannot infer:

```text
A □→ C
```

as a determinate truth without a threshold/truth convention.

### Earned firewall K-PROB-1

```text
HighCounterfactualProbability != CounterfactualTruth
```

---

# 75. Probability locations remain separated

Distinguish:

```text
P(route)
P(outcome | route)
P(generator/model)
P(cross-world completion)
P(counterfactual variable | evidence)
```

---

# 76. Probabilistic interventionist logic exists

Barbero and Virtema provide a strongly complete axiomatization for a logic combining probabilities and interventionist counterfactuals.

This demonstrates that probability/counterfactual inference can be formalized jointly.

It does not collapse their truth roles.

---

# 77. Identification is not logical consequence

A target can be semantically well-defined but empirically unidentified.

Conversely, an identification formula is a theorem about recoverability from distributions under assumptions, not an inference rule turning evidence into unconditional Reality truth.

### Earned firewall K-ID-1

```text
IdentificationTheorem != CounterfactualTruthInference
```

---

# PART XVIII — OBSERVATION VS INTERVENTION IN INFERENCE

# 78. Conditioning

```text
observe B
```

updates which factual/model states remain compatible.

---

# 79. Intervention

```text
do(B)
```

changes a mechanism/structural equation.

---

# 80. Counterfactual supposition

```text
suppose B counterfactually
```

can use intervention, backtracking, premise revision or another generator.

### Earned firewall K-OIC-1

```text
ObservationUpdate != Intervention != CounterfactualSupposition
```

This is central to inference architecture.

---

# PART XIX — MODEL-CLASS RELATIVE AXIOMS

# 81. Halpern causal axiomatization

Halpern provides different complete axiomatizations for:

```text
recursive models
unique-solution models
arbitrary models
```

showing directly that valid causal/counterfactual principles change with the model class.

---

# 82. Indeterministic interventionist axioms

Barbero 2023 explicitly studies how indeterministic causal laws change the axiomatization relative to deterministic causal models.

### Strong firewall K-AX-1

```text
OneCounterfactualAxiomSystem != AllCounterfactualModelClasses
```

---

# PART XX — MATCHED PHYSICAL CASES

# 83. Factual antecedent with intervention difference

Actual thermostat already set to 20°C by control law.

Counterfactual:

```text
If thermostat were forcibly clamped to 20°C...
```

can differ downstream from factual 20°C because the adaptive controller has been disabled.

Factual A does not detach without realization match.

---

# 84. Transitivity failure

```text
If valve opened, pressure would drop.
If pressure dropped, emergency controller would activate.
```

Directly supposing pressure drop can select a different mechanism than pressure drop produced by valve opening.

No automatic transitivity.

---

# 85. Contraposition failure

```text
If heater on, room warm.
```

does not imply:

```text
If room not warm, heater off.
```

window-open route can preserve heater-on.

---

# PART XXI — SOFTWARE MATCHED CASES

# 86. Factual flag value

Actual:

```text
flag=false because policy engine disabled feature
```

Counterfactual:

```text
if flag were hard-forced false
```

can bypass policy engine.

Same value, different realization.

---

# 87. Transitivity through deployment state

```text
If patch P deployed -> schema changes.
If schema changes -> migration M runs.
```

Direct schema change can select an environment where migration trigger differs.

No generic transitivity.

---

# 88. Cautious monotony failure via forced mediator

```text
P -> cache naturally invalidates -> request succeeds
```

Adding explicit `cache invalidated=true` by a different mechanism can remove the diagnostic route.

Premise addition and intervention addition differ.

---

# PART XXII — INSTITUTIONAL MATCHED CASES

# 89. Actual status vs imposed status

Actor factually licensed because criteria C were satisfied.

Counterfactual:

```text
if Actor were declared licensed by emergency decree
```

has same label but different constitutive route.

No surface factual detachment.

---

# 90. Contraposition

```text
If credential C granted, Actor would qualify.
```

does not imply:

```text
If Actor did not qualify, C would not have been granted.
```

other disqualifying rules can intervene.

---

# 91. Cut under constitutive rules

Natural consequence under rule K and explicit rule revision under `A∧B` must be kept separate.

---

# PART XXIII — AGENT-ERA MATCHED CASES

# 92. Actual tool use vs forced tool use

Agent actually used tool T because policy selected it.

Counterfactual:

```text
if Agent were forced to use T
```

can change policy state, exploration behavior or future tool choice.

### Earned firewall K-AGENT-1

```text
ActualActionToken != ForcedActionCounterfactual
```

---

# 93. Provider transitivity

```text
If provider M1 handled turn -> answer style S.
If answer style S -> user reacts R.
```

Directly forcing style S can differ from style generated by M1 because content/latent state differs.

---

# 94. Negative action contraposition

```text
If Agent called tool T -> data updated.
```

does not imply:

```text
If data not updated -> Agent did not call T.
```

tool call may fail or update may be rolled back.

---

# PART XXIV — SEMANTIC TRUTH VS SUPPOSITION

# 95. Suppositional reasoning

A user can rationally reason under assumption A and accept C within that supposition without asserting the categorical counterfactual:

```text
A □→ C
```

under every semantic theory.

---

# 96. Contextual heuristics

Williamson explicitly separates semantic logic from a suppositional heuristic that can make valid semantic principles appear invalid—or vice versa—through context shifts.

This creates a major residual.

### Earned firewall K-SUPP-1

```text
SuppositionalInferencePattern != CounterfactualSemanticValidity by default
```

---

# PART XXV — SEMANTIC TRUTH VS ACTION EXECUTION

# 97. Planning inference

From:

```text
If action a, desired outcome C
```

one still cannot infer:

```text
do a
```

without preferences, authority, cost, risk and alternatives.

---

# 98. Action success

Even if counterfactual claim is true under a model, operational execution can fail due access/capability constraints.

### Earned firewall K-ACT-1

```text
CounterfactualConsequence != ActionRecommendation != ExecutionGuarantee
```

---

# PART XXVI — SEMANTIC TRUTH VS EXPLANATION

# 99. Explanatory inference

A factor can support a counterfactual dependence while being a poor explanation due grain, normality or competing mechanisms.

WDF2-D/I remain binding.

### Earned firewall K-EXPL-1

```text
CounterfactualDependence != ExplanatoryAdequacy
```

---

# PART XXVII — INFERENCE FRAME CONTRACT

# 100. Research-only frame

```text
InferenceFrame =
  Anchor
  ContentAnalysis
  RouteStructure
  Generator/ModelClass
  Preservation
  Composition/BacktrackingPolicy
  Identity/Correspondence
  DomainExtension
  ConditionalOperator
  RouteAggregator
  TruthRole
  ProbabilityInterpretation
  QueryRole
```

This is diagnostic, not production schema.

---

# 101. Same-frame inference

Rules such as right weakening and conjunction of consequents are strongest when premises/conclusion share exactly the same frame.

---

# 102. Frame-transforming inference

Rules such as transitivity, import-export, contraposition and antecedent strengthening transform:

```text
anchor
antecedent
route family
or generator
```

and therefore require explicit compatibility laws.

### Strong firewall K-FT-1

```text
FormulaRule != FrameTransformationRule
```

---

# PART XXVIII — RULE CLASSIFICATION

# 103. Near-structural local rules

Under a shared classical frame, candidates often survive:

```text
Reflexivity / effectiveness
Right weakening
Conjunction of consequents
```

---

# 104. Route-structure rules

Depend strongly on antecedent decomposition:

```text
SDA
Or
some negation rules
```

---

# 105. Frame-transforming risky rules

Require major assumptions:

```text
MP/factual detachment
transitivity
contraposition
SA
Cut
Cautious Monotony
Rational Monotony
import-export
```

---

# 106. Selection-cardinality rules

Depend on unique/plural alternatives:

```text
CEM
some would/might dualities
```

---

# PART XXIX — CEM AND SCIENTIFIC MODELING

# 107. Determinate potential outcomes

A classical binary potential outcome `Y(a)` gives one value per unit/antecedent.

This supports CEM-like bivalence for the target.

---

# 108. Scientific success does not prove logical necessity

Lin's 2024 construction shows causal-inference success can be recovered without treating CEM as indispensable.

Therefore scientific utility is not a proof of universal counterfactual logic.

---

# PART XXX — EMPTY / IMPOSSIBLE ANTECEDENTS

# 109. Vacuity alters inference

If impossible antecedents are vacuously true under the chosen semantics:

```text
A □→ C
A □→ NOT C
```

can both hold.

This blocks treating CEM/CNC exactly like ordinary bivalent conditionals.

---

# 110. Non-vacuist extension

Under WDF2-H impossible-world/domain-extension semantics, inference depends on the admitted impossible alternatives and their logic.

Counterpossible inference therefore cannot be recovered from ordinary rules alone.

---

# PART XXXI — WOULD / MIGHT WITH MULTIPLE UNCERTAINTY AXES

# 111. Internal alternative axis

```text
forall a / exists a
```

---

# 112. Route axis

```text
forall route / exists route
```

---

# 113. Generator axis

```text
forall G / exists G
```

---

# 114. Completion/extension axes

```text
forall completion
forall domain extension
```

can be required for robust claims.

---

# 115. Inference cannot ignore quantifier order

### Earned firewall K-Q-1

```text
CounterfactualWould/MightInference != OneBinaryModalDualityOnceRobustnessAxesAreAdded
```

---

# PART XXXII — CONDITIONAL PROBABILITY VS COUNTERFACTUAL INFERENCE

# 116. Observational conditional

```text
P(C | A)
```

is not:

```text
P(C_A)
```

---

# 117. Interventional conditional

```text
P(C | do(A))
```

is not individualized cross-world probability by default.

---

# 118. Counterfactual posterior

```text
P(C_A | evidence)
```

requires cross-world coupling/model assumptions.

WDF2-B/G remain binding.

---

# PART XXXIII — DELETION TESTS

# 119. Universal modus ponens

**FAIL**.

Briggs interventionist semantics and Williamson strict-context semantics provide independent counterexamples.

---

# 120. Delete factual detachment entirely

**FAIL**.

Strong-centering/exogenous-intervention architectures can justify it when actual realization matches antecedent realization.

---

# 121. Universal contraposition

**FAIL** across route-sensitive causal/prevention cases.

---

# 122. Universal transitivity

**FAIL** through anchor/route shift.

---

# 123. Delete all transitivity

**FAIL** because fixed-domain strict semantics can validate it and local frame-stable cases exist.

---

# 124. Universal CEM

**FAIL** under plural/nondeterministic alternatives and contemporary causal-inference alternatives.

---

# 125. Universal CNC without nonvacuity qualification

**FAIL** for vacuous impossible antecedents.

---

# 126. Universal import-export

**FAIL** under nested re-anchoring/composition differences.

---

# 127. Delete all unnesting

**FAIL** because causal-model-specific unnesting theorems exist.

---

# 128. Import System P wholesale

**FAIL** because Left Logical Equivalence and cumulative rules can conflict with hyperintensional/surgery semantics.

---

# 129. Reject all KLM principles

**FAIL** because several local same-frame rules are useful and preferential logics provide a strong comparison algebra.

---

# 130. Identify conditioning with intervention

**FAIL**.

---

# 131. Identify premise strengthening with intervention augmentation

**FAIL**.

---

# 132. Infer truth from high probability

**FAIL** without threshold/truth semantics.

---

# 133. Infer action from counterfactual benefit

**FAIL** without decision/authority/risk structure.

---

# PART XXXIV — EXTERNAL RESEARCH PRESSURE

# 134. Briggs 2012

`Interventionist Counterfactuals` extends causal-model semantics to a richer counterfactual language and proves a sound/complete axiomatization. The extension has striking inferential consequences: modus ponens fails and classical logical equivalents cannot be freely substituted in antecedents.

Foundational pressure:

```text
causal realization semantics can alter basic conditional logic.
```

---

# 135. Vandenburgh 2023

The exogenous-intervention model distinguishes itself from Pearl/Briggs-style endogenous intervention for actual antecedents. Actual A can correspond to an empty intervention, delivering strong centering and restoring modus ponens.

Foundational pressure:

```text
MP turns on what it means to realize an already-actual antecedent.
```

---

# 136. Williamson 2020

Williamson's contextually restricted strict-conditional semantics validates transitivity, contraposition and antecedent strengthening while allowing modus ponens to fail when the actual world lies outside the context restriction; his account also denies CEM because `would` can range over multiple relevant worlds.

Foundational pressure:

```text
familiar rule package is theory-dependent rather than fixed by the word “counterfactual”.
```

---

# 137. Halpern 2000 / causal axiomatization

Halpern gives distinct complete axiomatizations for recursive, unique-solution and arbitrary structural causal models.

Foundational pressure:

```text
causal counterfactual validities are model-class sensitive.
```

---

# 138. Barbero 2023

Indeterministic causal-law models require significant changes to the axiomatization of interventionist counterfactuals compared with deterministic models.

Foundational pressure:

```text
determinism assumptions are logical assumptions about the counterfactual language, not implementation details.
```

---

# 139. Lin 2024

Lin connects CEM to the Rubin causal-model tradition, then constructs a causal-inference theory that avoids CEM while preserving core inferential achievements through integration with causal Bayes nets.

Foundational pressure:

```text
CEM can be scientifically dispensable.
```

---

# 140. Kraus / Lehmann / Magidor

KLM's preferential and cumulative logics provide a representation-theoretic account of nonmonotonic consequence. System P supplies a conservative family of rules such as Or, Cut and Cautious Monotony; later rational consequence adds ranked-model structure.

Foundational pressure:

```text
nonmonotonicity has a rich algebra, but its premise semantics must not be confused with intervention semantics.
```

---

# 141. Correa / Lee / Bareinboim 2021

Their Counterfactual Unnesting Theorem provides a complete causal-model route for converting arbitrary nested counterfactuals into unnested forms for identification analysis.

Foundational pressure:

```text
nested counterfactual simplification can be a model-class theorem rather than a universal conditional-logic axiom.
```

---

# 142. Barbero / Virtema 2023

A strongly complete logic exists combining probabilistic expressions and interventionist counterfactuals.

Foundational pressure:

```text
probability and counterfactual consequence can be jointly axiomatized while remaining semantically distinct.
```

---

# PART XXXV — WDF0 / WDF1 REOPEN AUDIT

# 143. WDF0

No FoundationReopenCondition fires.

WDF2-K reinforces:

```text
Cause != Constraint != Constitution
Action != Intervention
Model != Reality
Relative != Subjective
Same_X != Same_Y without criterion
```

Inference-frame plurality is a semantic/model interface, not a new Reality root.

WDF0 remains frozen.

---

# 144. WDF1

No FoundationReopenCondition fires.

WDF1 already keeps:

```text
alternative specification
generator
modal operator/quantifier
measure interpretation
model provenance
```

explicit.

WDF2-K shows exactly why inference rules depend on those fields.

WDF1 remains frozen.

---

# PART XXXVI — RECONSTRUCTION

# 145. Counterfactual inference is typed

A rule should be stated as:

```text
Rule R is sound
relative to
  frame class F
  model class M
  antecedent-content equivalence E
  conditional operator O
  route aggregator Q
```

not simply:

```text
Counterfactuals obey R.
```

---

# 146. Rule result shapes

An inference audit can yield:

```text
UniversallyInvalid
ValidInDeclaredModelClass
ValidUnderStrongCentering
ValidUnderRouteWiseSemantics
ValidUnderSharedFrame
ValidUnderNaturalizationRestriction
UnderdeterminedAcrossSemantics
FailsByFrameShift
FailsByRouteShift
FailsByInterventionAugmentation
FailsByVacuity
```

---

# 147. Strong result — frame preservation is a hidden premise of many rules

Factual detachment, transitivity, Cut, Cautious Monotony and import-export all become much safer when the rule preserves:

```text
anchor
realization mode
relevant background
model/generator
content grain
```

Their failure often corresponds to one of these changing.

### Earned firewall K-PRES-1

```text
InferenceSchemaMatching != FramePreservation
```

---

# 148. Strong result — counterfactual logic is not one fixed package

Different coherent semantics support sharply different rule bundles:

```text
Briggs: extended interventionist logic, MP fails
Vandenburgh: strong-centering exogenous intervention, MP restored
Williamson: transitivity/contraposition/SA valid, MP and CEM fail
Stalnaker-like unique selection: CEM pressure
Lewis-like plural selection: CEM may fail
KLM preferential: cumulative/default rule package
indeterministic causal models: different axioms from deterministic models
```

No universal bundle survives deletion tests.

---

# 149. Strong result — inference failures classify structural mismatches

Rather than recording only `rule invalid`, WDF2-K can classify why:

```text
anchor shift
route shift
realization mismatch
intervention augmentation
model-class change
content-equivalence failure
empty/vacuous antecedent
quantifier-order change
probability/truth-role mismatch
```

This is more informative than a flat logic table.

---

# PART XXXVII — LARGEST REMAINING RESIDUAL

# 150. Why context/supposition dynamics become upstream

WDF2-K repeatedly encounters a phenomenon that cannot be settled by static frame typing alone:

```text
supposing A
```

can itself change:

```text
which worlds/states are contextually relevant
which background premises remain active
which similarity/relevance dimensions matter
which alternatives are salient
which normality assumptions are live
which model variables are interpreted as fixed
```

---

# 151. Context shift can mimic semantic invalidity

Williamson explicitly explains several apparently invalid logical principles through the behavior of suppositional heuristics and context restriction rather than through the truth conditions themselves.

Other frameworks treat the supposition/update itself as part of semantics.

WDF2-K has no foundation yet for deciding between:

```text
static semantics + pragmatic context shift
```

and:

```text
dynamic/update semantics
```

or typed plural combinations.

---

# 152. Nested inference makes this unavoidable

For:

```text
A □→ (B □→ C)
```

we need to know not only the A-frame and B-frame but **how the act of supposing A transforms the context in which B is interpreted**.

This is stronger than WDF2-F's mechanical frame evolution because it includes:

```text
information state
salience/relevance
premise acceptance
normality
linguistic/discourse context
```

---

# 153. Observation / supposition / revision remain under-modeled

WDF2-K established:

```text
ObservationUpdate != Intervention != CounterfactualSupposition
```

but does not yet provide a theory of the third operation.

That is now the largest upstream gap.

---

# 154. Exact next round

The next canonical round is therefore:

# **WDF2-L — Counterfactual Context / Supposition / Update / Dynamic Re-Anchoring**

WDF2-L should test:

```text
static truth conditions vs dynamic update semantics
suppositional context transformation
context restriction and accommodation
premise-set revision
salience / relevance update
normality/default update
anchor migration under nested counterfactuals
information-state update vs Reality intervention
observation vs supposition vs belief revision
context dependence of similarity/orderings
whether apparent rule failures are semantic or context-shift effects
iteration as sequential context update
cross-speaker / Agent context alignment
robustness across admissible context-update policies
```

It must not preselect Williamson-style heuristic/context accounts, dynamic semantics, premise revision, AGM belief revision, inquisitive update or causal intervention as universal.

Only WDF2-L residuals may determine WDF2-M.

---

# 155. Production disposition

No production changes are admitted.

Do **not** add:

```text
CounterfactualInferenceEngine
InferenceFrame
RuleValidityMatrix
ContextUpdater
DetachmentChecker
CounterfactualProofSystem
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

Counterfactual Foundations remain open.

---

# 156. Closeout

```text
WDF2-K: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D/E/F/G/H/I/J reopen: NO
Production refactor: NO

SameFormula != SameEvaluationFrame
SemanticValidity != SuppositionalAcceptability != Actionability != ExplanatorySupport
AntecedentTruth != AntecedentRealizationMatch
ActualValueEquality != NoOpIntervention
CounterfactualMP != MinimalRequirementForEveryCoherentCounterfactualLogic
ActualModusTollens != CounterfactualContraposition
SameIntermediateProposition != SameIntermediateRealization
SameAntecedentText != SameAdmissibleAlternativeFamily
PremiseStrengthening != InterventionAugmentation
LogicalEquivalence != InferenceLevelSubstitutability
CEM is not indispensable to causal inference as such
ConditionalNonContradiction depends on nonvacuity assumptions
WouldMightDualityAtFixedFamily != RobustCrossFamilyDuality
NestedSupposition != JointAntecedent
SCMCounterfactualUnnesting != UniversalLogicalImportExport
NestedCounterfactualSyntax != OneUniversalIterationSemantics
ConditionOnB != Do(B)
CounterfactualNonmonotonicity != OneSinglePreferentialPhenomenon
HighCounterfactualProbability != CounterfactualTruth
IdentificationTheorem != CounterfactualTruthInference
ObservationUpdate != Intervention != CounterfactualSupposition
OneCounterfactualAxiomSystem != AllCounterfactualModelClasses
FormulaRule != FrameTransformationRule
InferenceSchemaMatching != FramePreservation

Exact next round:
WDF2-L — Counterfactual Context / Supposition / Update / Dynamic Re-Anchoring
```

Compressed result:

> **WDF2-K establishes that there is no context-free universal package of counterfactual inference rules. The central hidden variable is the evaluation frame: anchor, antecedent realization mode, route structure, generator/model class, preservation, identity/correspondence, domain extension, conditional operator, route aggregation, probability interpretation and query role. Familiar formula patterns can therefore fail because a rule silently transforms the frame. Factual detachment is the clearest case: Briggs' interventionist semantics can invalidate modus ponens because even an actually true antecedent is re-realized by intervention, whereas an exogenous-intervention/strong-centering semantics can restore it; surface truth of A is weaker than realization match. Transitivity fails when the B reached from A differs from the B selected directly, contraposition fails under plural negation/prevention routes, and import-export fails when nested supposition re-anchors differently from joint conjunction. Conversely, strict fixed-domain semantics can validate several of these principles, proving that their failure is not universal either. Conditional Excluded Middle depends on unique/determinate selection and can fail under plural or indeterministic models; contemporary causal-inference work shows it is not scientifically indispensable. KLM preferential logic supplies a powerful taxonomy of nonmonotonic rules, but Cautious Monotony, Cut and Rational Monotony cannot be imported wholesale because premise restriction is not intervention augmentation: conditioning on B differs from doing B. Probability, identification, semantic truth, explanation and action remain separate truth roles. The strongest reconstruction is therefore rule-by-frame: state exactly which model/semantics/frame class makes an inference sound and classify failures by anchor shift, route shift, realization mismatch, intervention augmentation, vacuity, quantifier-order or truth-role mismatch. The largest remaining residual is dynamic rather than static: the act of supposing an antecedent can itself change relevance, normality, background premises, context restrictions and the interpretation of later nested suppositions. WDF2 therefore advances next to counterfactual context, supposition, update and dynamic re-anchoring.**
