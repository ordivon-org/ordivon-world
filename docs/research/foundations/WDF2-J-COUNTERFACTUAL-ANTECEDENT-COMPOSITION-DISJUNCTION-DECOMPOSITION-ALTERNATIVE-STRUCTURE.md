# WDF2-J — Counterfactual Antecedent Composition / Disjunction / Decomposition / Alternative Structure

Status: **complete for WDF2-J**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D/E/F/G/H/I remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-J residuals:

```text
WDF2-K — Counterfactual Consequence / Inference / Detachment / Iteration
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-I established that counterfactual antecedent content is hyperintensional and multi-resolution: syntax, possible-world intension, topic, truthmaker structure, typed surgery, premise structure and framework revision cannot be collapsed into one universal content carrier.

WDF2-J asks the next structural question:

> **How do the internal logical constructors of an antecedent—conjunction, disjunction, exclusive disjunction, negation and nested Boolean structure—generate counterfactual alternatives, surgeries, truthmakers, premises or route families, and which classical equivalences/inference principles survive after this structure becomes semantically active?**

The key pressure points are:

```text
Simplification of Disjunctive Antecedents (SDA)
Strengthening of the Antecedent (SA)
substitution of logical equivalents
De Morgan equivalence in antecedent position
conjunction as joint surgery vs premise accumulation
disjunction as union vs alternative family
exclusive choice vs inclusive disjunction
negation as complement vs falsemaker/prevention family
route weighting and probability
route overlap
nested Boolean decomposition
```

No classical, inquisitive, truthmaker, causal-model or alternative-semantics account is preselected as universal.

---

# 2. First decisive result — truth conditions and antecedent alternatives separate

The strongest surviving distinction is:

```text
TruthCondition(A)
```

versus:

```text
AntecedentAlternatives(A)
```

Two expressions can have the same ordinary truth conditions while exposing different counterfactual assumption/realization structures.

### Earned firewall J-TCALT-1

```text
SameTruthConditions != SameAntecedentAlternativeStructure
```

Champollion, Ciardelli and Zhang's switch experiment is a direct empirical falsifier of truth-condition-only antecedent semantics: truth-conditionally equivalent antecedents involving a disjunction and a De-Morgan-equivalent negated conjunction contributed differently inside counterfactual conditionals.

---

# 3. Alternative structure is not automatically lexical semantics

The fact that a counterfactual reading distinguishes alternatives does not by itself prove that natural-language `or` lexically denotes an alternative set.

Competing explanations include:

```text
lexical/semantic alternatives
inquisitive lifting
truthmaker decomposition
correlative syntax
exhaustification
pragmatic enrichment
query-role-sensitive reinterpretation
```

2026 SDA acquisition work explicitly compares alternative-based and exhaustification-style accounts.

### Earned firewall J-ORIGIN-1

```text
ObservedAlternativeSensitiveReading
!= ProofOfOneUniqueLexicalSemantics
```

---

# PART I — THE SDA / SA TRILEMMA

# 4. Simplification of Disjunctive Antecedents

The familiar SDA pattern is:

```text
(A OR B) □→ C
----------------
A □→ C
B □→ C
```

Natural-language judgments often strongly favor this reading for ordinary disjunctive antecedents.

Alonso-Ovalle and inquisitive-semantic approaches derive it by treating the disjuncts as separate assumptions/alternatives.

---

# 5. Strengthening of the Antecedent

The familiar SA pattern is:

```text
A □→ C
----------------
(A AND B) □→ C
```

This is not valid in general.

Example:

```text
If the match had been struck, it would have lit.
```

need not support:

```text
If the match had been struck and soaked in water, it would have lit.
```

The additional conjunct can alter the mechanism/preservation profile.

---

# 6. Fine-style derivation pressure

Classically:

```text
A
≡
(A AND B) OR (A AND NOT-B)
```

Suppose all three principles are globally accepted:

```text
1. substitution of logical equivalents in antecedent position
2. SDA
3. ordinary Boolean equivalence above
```

From:

```text
A □→ C
```

substitution yields:

```text
[(A AND B) OR (A AND NOT-B)] □→ C
```

SDA then yields:

```text
(A AND B) □→ C
```

which is SA.

Since unrestricted SA fails, at least one universal principle must be restricted.

### Strong firewall J-TRILEMMA-1

```text
Universal SDA
+ Unrestricted Logical-Equivalent Substitution
+ General SA Failure
cannot coexist without refining antecedent content/equivalence.
```

This is not a local linguistic curiosity; it is a structural constraint on any compositional counterfactual architecture.

---

# 7. Foundation response to the trilemma

WDF2-J does not simply delete SDA.

Instead it preserves:

```text
ordinary truth-conditional equivalence
```

separately from:

```text
counterfactual alternative equivalence
```

Thus:

```text
A
```

and:

```text
(A AND B) OR (A AND NOT-B)
```

can agree in truth conditions while differing in exposed antecedent routes.

---

# PART II — DISJUNCTION

# 8. Boolean-union semantics

At ordinary truth-condition level:

```text
Worlds(A OR B)
=
Worlds(A) UNION Worlds(B)
```

This is correct as a classical extension.

But the union does not preserve which disjunct licenses a world.

---

# 9. Route-erasure problem

Suppose:

```text
w1 satisfies A only
w2 satisfies B only
w3 satisfies both
```

The bare union records membership but not route identity.

If counterfactual semantics needs to compare:

```text
A-route consequences
B-route consequences
```

that information is lost.

### Earned firewall J-UNION-1

```text
DisjunctiveTruthSet != DisjunctiveRouteStructure
```

---

# 10. Alonso-Ovalle alternative structure

Alonso-Ovalle's disjunctive counterfactual analysis treats each disjunct as introducing a propositional alternative; the closest worlds are selected from each alternative separately.

This validates the ordinary SDA intuition without global antecedent strengthening.

Foundational lesson:

```text
Disjunction can expose several counterfactual assumptions rather than one undifferentiated union.
```

---

# 11. Inquisitive lifting

Ciardelli's lifting construction generalizes this idea: an antecedent can provide multiple propositions/possibilities, each treated as a separate conditional assumption.

For a disjunctive antecedent, truth of the whole conditional can require the consequent under each antecedent alternative.

### Earned firewall J-ALT-1

```text
OneTruthConditionalProposition
can carry
MultipleCounterfactualAssumptionAlternatives.
```

---

# 12. Alternative-wise would

For an antecedent alternative family:

```text
Alt(A OR B) = {A-route, B-route}
```

a strong alternative-wise `would` can be schematized:

```text
For every route r in Alt(A OR B):
  Would_r(C)
```

This directly yields SDA.

---

# 13. Route-wise might

A route-sensitive `might` can have several readings:

```text
exists route r such that Might_r(C)
```

or the stronger:

```text
for every relevant route r, Might_r(C)
```

WDF2-E quantifier-order discipline therefore reappears inside antecedent structure.

### Earned firewall J-MIGHT-1

```text
MightUnderDisjunction is incomplete without route quantification semantics.
```

---

# 14. Closest-in-union reading

A Lewis-style union treatment can instead select the closest A-or-B worlds globally.

If all closest A-or-B worlds happen to realize A, then B may never be evaluated.

This can invalidate SDA.

### Earned firewall J-SELECT-1

```text
ClosestWithinUnion != ClosestWithinEachAlternative
```

These are different counterfactual questions, not two implementations of the same algorithm.

---

# 15. No universal declaration that union reading is wrong

Some queries may intentionally ask:

```text
If one of A or B happened, whichever is the nearest way for that disjunction to occur, would C?
```

For such a role, global union selection may be meaningful.

WDF2-J therefore preserves route semantics as typed/query-relative rather than making SDA a metaphysical axiom.

---

# PART III — EXCLUSIVE DISJUNCTION

# 16. Inclusive OR vs XOR

Ordinary inclusive disjunction permits overlap:

```text
A and B
```

Exclusive disjunction does not.

A natural decomposition is:

```text
XOR(A,B)
=
(A AND NOT-B)
OR
(NOT-A AND B)
```

at truth-condition level.

---

# 17. XOR routes carry exclusion constraints

If XOR is interpreted as alternatives:

```text
route1 = A with B excluded
route2 = B with A excluded
```

then route semantics is not merely `{A,B}`.

### Earned firewall J-XOR-1

```text
ExclusiveDisjunctionRoutes != InclusiveDisjunctionRoutes
```

---

# 18. Choice semantics pressure

In planning/Agent contexts:

```text
do A or B
```

can mean:

```text
choose one policy/action from a menu
```

rather than assert an ordinary disjunctive proposition.

This introduces a choice architecture:

```text
AvailableAlternatives
ChoiceRule
OutcomeUnderChosenAlternative
```

### Earned firewall J-CHOICE-1

```text
DisjunctiveFact != DisjunctiveChoiceSet
```

---

# PART IV — ROUTE OVERLAP

# 19. Inclusive disjuncts can overlap

If A and B are not mutually exclusive, a world/state/submodel can realize both.

Therefore:

```text
Alt = {A,B}
```

is not necessarily a partition.

---

# 20. Alternative identity vs partition identity

Semantic alternatives can overlap in extension.

### Earned firewall J-OVERLAP-1

```text
AlternativeFamily != MutuallyExclusiveEventPartition
```

This becomes critical for probability.

---

# 21. Double-counting risk

If route probabilities are assigned by naively summing:

```text
P(A-route) + P(B-route)
```

when A and B overlap, the A∧B region can be double-counted.

Probability semantics therefore needs either:

```text
partition refinement
inclusion-exclusion
route-label latent variable
submodel weighting semantics
```

or another explicit construction.

---

# PART V — ROUTE WEIGHTING

# 22. Alternatives need not have probabilities

A semantic alternative family:

```text
{r1,r2,...}
```

does not by itself supply:

```text
P(r_i)
```

### Earned firewall J-WEIGHT-1

```text
AntecedentAlternativeSet != ProbabilityDistributionOverAlternatives
```

---

# 23. Rosella/Sprenger weighted submodels

Rosella and Sprenger extend causal-model semantics to disjunctive and arbitrary Boolean antecedents by considering truthmaking submodels and assigning weights based on inverse distance to the original model.

This is a substantive probabilistic counterfactual semantics.

It demonstrates that complex Boolean antecedents can be represented inside causal-model architecture.

---

# 24. Weighting is not semantic inevitability

The inverse-distance weighting rule is one architecture.

Other queries may require:

```text
uniform alternative treatment
objective chance weights
epistemic weights
policy probabilities
robust all-route quantification
worst-case route
o weighting at all
```

### Earned firewall J-WEIGHT-2

```text
RouteWeightingRule != AntecedentMeaning by foundation default
```

---

# 25. Mixture firewall survives

If routes correspond to semantically distinct ways the antecedent can be realized, averaging them produces a mixture quantity.

WDF2-E remains binding:

```text
MixtureResult != EachRouteCounterfactualTruth
```

An average can hide one route that makes C true and another that makes C false.

---

# PART VI — CONJUNCTION

# 26. Classical truth condition

```text
Worlds(A AND B)
=
Worlds(A) INTERSECT Worlds(B)
```

This is straightforward extensionally.

Counterfactual realization is not always straightforward.

---

# 27. Conjunction as compound constraint

One reading requires both A and B to hold in the receiving branch.

This can map to:

```text
joint compound surgery
joint premise set
fused truthmaker
intersected constraint set
```

depending architecture.

---

# 28. Conjunction as multi-locus surgery

If:

```text
A = X:=x
B = Z:=z
```

then:

```text
A AND B
```

can map naturally to a simultaneous or ordered compound surgery.

WDF2-F compatibility rules immediately apply.

---

# 29. Joint satisfiability gate

Two individually admissible conjuncts need not compose.

```text
Admissible(A)
AND
Admissible(B)
```

does not imply:

```text
Admissible(A AND B)
```

### Earned firewall J-CONJ-1

```text
IndividuallyAdmissibleConjuncts != JointlyAdmissibleConjunction
```

---

# 30. Same-locus contradiction

```text
A: X:=0
B: X:=1
```

then `A AND B` at one time/locus can be jointly inconsistent under exact hard-assignment semantics.

This is not merely a low-probability branch.

---

# 31. Dependent conjuncts

If:

```text
B is causally/constitutively downstream of A
```

then explicitly imposing both can differ from imposing A and letting B arise naturally.

Example:

```text
A = grant credential
B = license status becomes true
```

Under current rule, A may normally entail/constitute B.

Counterfactually setting both can preserve less diagnostic information than setting A alone.

### Earned firewall J-REDUND-1

```text
A causes/constitutes B
!=
InterveningOnAAndB is semantically identical to intervening on A only.
```

---

# 32. Conjunction can over-specify

Adding a conjunct can:

```text
block a natural mechanism
fix a mediator
remove adaptive policy freedom
force a downstream state
```

Hence ordinary SA failure is structurally expected.

---

# PART VII — CONJUNCTION ORDER

# 33. Boolean conjunction is commutative extensionally

```text
A AND B
≡
B AND A
```

at ordinary truth-condition level.

---

# 34. Sequential surgery descriptions can be order-sensitive

If the intended antecedent content is:

```text
first A, then B
```

this is not bare conjunction.

WDF2-F established that sequential surgery can be noncommutative.

### Earned firewall J-ORDER-1

```text
BooleanConjunction != TemporalSequentialComposition
```

Natural-language `and then` / temporal indices must not be normalized into unordered conjunction.

---

# 35. Simultaneous conjunction

If syntax/query explicitly requests simultaneous A∧B, no arbitrary serialization should be introduced.

---

# PART VIII — NEGATION

# 36. Negation as truth-set complement

At classical truth-condition level:

```text
Worlds(NOT A)
=
W \ Worlds(A)
```

This provides a correct Boolean extension.

But complement alone does not say **how A fails**.

---

# 37. Failure-route multiplicity

For:

```text
A = service is available
```

`NOT A` may arise through:

```text
process crash
network partition
authorization failure
power loss
DNS failure
```

These can have different consequences.

### Earned firewall J-NEG-1

```text
NegatedTruthCondition != OneCounterfactualFailureRoute
```

---

# 38. Atomic finite-domain negation

If:

```text
X ∈ {0,1,2}
A = X=0
```

then:

```text
NOT A
```

can expose:

```text
X=1
X=2
```

as alternative realizations.

But whether both must be evaluated depends on query semantics.

---

# 39. Binary special case

If X is genuinely binary and semantics stable:

```text
NOT(X=0)
```

can normalize to:

```text
X=1
```

This is a local equivalence, not a universal negation architecture.

---

# 40. Prevention-family reading

For event antecedent A:

```text
NOT A
```

can be interpreted as a family of A-preventing alterations.

Examples:

```text
remove trigger
block mechanism
change policy
change background condition
```

### Earned firewall J-PREV-1

```text
NotA != OneUniquePreventionIntervention
```

This becomes important for later causation/prevention analysis.

---

# 41. Falsemaker/truthmaker route

Truthmaker-style semantics can represent negation using states incompatible with/verifying failure of the proposition according to the chosen framework.

This can expose more structure than plain set complement.

But falsemaker individuation itself is theory-dependent.

---

# PART IX — DE MORGAN PRESSURE

# 42. Classical equivalence

Classically:

```text
A OR B
≡
NOT(NOT A AND NOT B)
```

and:

```text
NOT(A AND B)
≡
NOT A OR NOT B
```

at truth-condition level.

---

# 43. Counterfactual antecedent difference

Champollion, Ciardelli and Zhang experimentally compare a disjunctive antecedent to a De-Morgan-equivalent negated conjunction and find different conditional contributions.

In inquisitive terms:

```text
A OR B
```

introduces multiple assumptions,
while the equivalent negated-conjunction form can introduce one truth-conditional assumption.

### Strong firewall J-DEMORGAN-1

```text
DeMorganTruthConditionalEquivalence
!= CounterfactualAlternativeEquivalence
```

---

# 44. This is not rejection of De Morgan's law simpliciter

The two antecedents can remain classically truth-conditionally equivalent.

What fails is unrestricted substitution inside a hyperintensional counterfactual environment.

---

# PART X — NESTED BOOLEAN STRUCTURE

# 45. `(A OR B) AND C`

A route-preserving decomposition may yield:

```text
A AND C
B AND C
```

as alternatives when C is a shared conjunct.

But this transformation requires compatibility and content-preservation checks.

---

# 46. Distributive truth equivalence is insufficient

Classically:

```text
(A OR B) AND C
≡
(A AND C) OR (B AND C)
```

Yet counterfactual alternative structure can depend on whether C is represented as:

```text
one shared preservation/constraint
```

or duplicated into each alternative.

### Earned firewall J-DIST-1

```text
BooleanDistributivity != AutomaticCounterfactualDecompositionEquivalence
```

---

# 47. Shared-background representation can quotient duplicates

If C plays exactly the same role in all disjunct routes, a normalized antecedent representation can factor it as:

```text
Shared(C)
+
Alternatives{A,B}
```

rather than duplicating C.

This reduces overfitting.

---

# 48. `(A AND B) OR C`

Alternative semantics can expose:

```text
route1: joint A+B
route2: C
```

The first route itself may require WDF2-F multi-surgery compatibility.

Thus alternative trees can be nested, not flat lists.

---

# PART XI — ALTERNATIVE TREES

# 49. Flat alternative sets are sometimes insufficient

A Boolean antecedent can contain internal composition:

```text
(A AND B) OR (C AND (D OR E))
```

Flattening everything can erase which conjuncts belong together.

---

# 50. Research-level alternative tree

A safe diagnostic representation can preserve nodes such as:

```text
ALL / conjunction
ANY / inclusive alternative
ONE-OF / exclusive alternative
NOT / negation
ATOM / typed content
```

with domain-specific normalization after parsing.

This is not a production AST proposal.

---

# 51. Boolean tree != surgery plan tree automatically

An `ALL` node can map to:

```text
simultaneous surgery
ordered surgery
joint constraint
premise accumulation
```

depending on typed atoms and temporal semantics.

### Earned firewall J-TREE-1

```text
LogicalCompositionTree != CounterfactualSurgeryPlan by definition
```

---

# PART XII — TRUTHMAKER DECOMPOSITION

# 52. Exact truthmaker view

Truthmaker semantics gives a natural reason to preserve disjunct alternatives:

```text
truthmakers(A OR B)
```

can include exact A-truthmakers and exact B-truthmakers separately.

This keeps route structure unavailable in a bare world-set union.

---

# 53. Conjunction in truthmaker semantics

A conjunction can require fusion/combination of truthmakers for A and B.

This mirrors WDF2-F's multi-locus composition pressure.

---

# 54. Negation remains framework-dependent

Fine-style truthmaker systems require a systematic account of verification/falsification states.

Therefore truthmaker decomposition is powerful but not assumption-free.

---

# 55. Truthmaker route != causal route

An exact truthmaker alternative for A∨B need not correspond to a distinct causal mechanism.

### Earned firewall J-TMROUTE-1

```text
TruthmakingAlternative != CausalRealizationRoute by definition
```

The two can coincide in some domains but must not be globally identified.

---

# PART XIII — CAUSAL-MODEL COMPLEX ANTECEDENTS

# 56. Standard SCM antecedent restriction

Traditional causal-model counterfactual languages are naturally centered on conjunctions of atomic assignments/interventions.

This makes disjunction and arbitrary Boolean antecedents nontrivial extensions.

---

# 57. Briggs extension pressure

Briggs develops an extended interventionist counterfactual language and shows that the logical behavior diverges sharply from Lewis-style systems; among the consequences, classical logical equivalents cannot be freely substituted in antecedents.

This independently supports WDF2-I/J hyperintensional composition.

---

# 58. Halpern disjunction lesson

Halpern's comparison of causal models and possible-world counterfactual structures notes that an axiom involving disjunction cannot be dismissed simply because the original causal language lacked disjunction.

Foundational lesson:

```text
Expressive language restriction can hide real semantic constraints.
```

---

# 59. Rosella/Sprenger complex Boolean semantics

Their framework extends causal modeling semantics to arbitrary Boolean combinations using truthmaking submodels.

This demonstrates one concrete bridge:

```text
Boolean antecedent
-> truthmaking submodels
-> distance/weight
-> counterfactual probability
```

---

# 60. Foundation does not universalize weighted-average truth

That bridge is an existence proof for a coherent architecture, not proof that every counterfactual with complex antecedent means an inverse-distance weighted average over submodels.

---

# PART XIV — INQUISITIVE / ALTERNATIVE SEMANTICS

# 61. Alternative semantics advantage

Disjunction naturally contributes multiple propositions/assumptions rather than one union proposition.

This validates SDA without unrestricted SA.

---

# 62. Inquisitive lifting advantage

A general conditional operation over classical propositions can be lifted to antecedents with multiple alternatives.

This modularity is structurally attractive:

```text
base counterfactual evaluator
+
alternative-sensitive antecedent layer
```

---

# 63. But natural-language source remains contested

The same SDA judgments can potentially be modeled through semantic alternatives or exhaustification/pragmatic machinery.

WDF2-J therefore distinguishes:

```text
SemanticRepresentationNeededForAReading
```

from:

```text
LexicalOriginOfThatRepresentation
```

---

# PART XV — SDA IS NOT UNIVERSAL BY FOUNDATION DEFAULT

# 64. Strong SDA reading

For route-preserving `or`:

```text
Would(A OR B,C)
```

can require C under every disjunct route.

Then SDA follows.

---

# 65. Global-union reading

For an undifferentiated union antecedent, closest alternatives may come from one disjunct only.

SDA can fail.

---

# 66. Epistemic/uncertainty reading

“If either A or B happened, but we do not know which” can call for robust evaluation across both live hypotheses.

This often supports SDA-like reasoning.

---

# 67. Choice/policy reading

“If we choose A or B” can denote a policy/menu whose outcome depends on a later choice mechanism.

It need not mean both routes individually guarantee C.

### Earned firewall J-SDA-1

```text
SDAValidity is antecedent-structure/query-role sensitive.
```

---

# 68. Acquisition evidence does not prove semantic universality

Zani, Ciardelli and Sanfelici's 2026 acquisition study confirms the continued empirical importance of SDA and compares multiple explanatory theories.

It does not settle every philosophical/scientific counterfactual use of disjunction.

---

# PART XVI — SA FAILURE RECONSTRUCTED

# 69. Why strengthening fails structurally

Adding B to A can:

```text
change the generator
change preservation
introduce surgery conflict
fix a mediator
disable a mechanism
change rule context
change relevant alternative family
```

Therefore:

```text
A □→ C
```

need not survive:

```text
A AND B □→ C
```

---

# 70. Conditional strengthening can still hold locally

If B is guaranteed irrelevant under the query and compatible with A, strengthening may preserve the result.

A research condition could be:

```text
B is admissible
B does not alter relevant/preserved structure
A+B remains jointly coherent
C is invariant across the strengthened alternative family
```

Then SA can hold locally.

### Earned firewall J-SA-1

```text
GeneralSAInvalid != NoValidAntecedentStrengtheningCases
```

---

# PART XVII — REDUNDANCY / ENTAILMENT INSIDE CONJUNCTION

# 71. Redundant conjunct

If A already semantically entails B under the current framework, then:

```text
A AND B
```

has the same classical truth condition as A.

---

# 72. Counterfactual redundancy is stronger

To normalize away B, one must ensure B adds no:

```text
mode-of-presentation structure
surgery instruction
preservation implication
alternative decomposition
query-role information
```

### Earned firewall J-REDUND-2

```text
LogicalRedundancy != CounterfactualContentRedundancy by default
```

---

# 73. Example

```text
A = system is offline because process crashed
B = system is offline
```

A may entail B.

But adding B can be redundant if it is merely descriptive, or can become an explicit target constraint if interpreted interventionally.

The role must be typed.

---

# PART XVIII — TAUTOLOGICAL ANTECEDENT PRESSURE

# 74. Truth-condition tautology

```text
A OR NOT A
```

is classically true at all worlds.

---

# 75. Alternative-sensitive content can still be nontrivial

An alternative semantics can expose:

```text
{A, NOT A}
```

as a live partition/question/assumption structure.

Thus:

### Earned firewall J-TAUT-1

```text
TautologicalTruthCondition != CounterfactualNoOp under every antecedent semantics
```

---

# 76. Foundation caution

This does not mean every utterance of “A or not A” should generate a rich counterfactual partition.

Natural-language pragmatics/query role can suppress or activate the alternative structure.

---

# PART XIX — NEGATION OF COMPLEX ANTECEDENTS

# 77. `NOT(A OR B)`

Classically equivalent to:

```text
NOT A AND NOT B
```

This often specifies a joint exclusion condition.

---

# 78. `NOT(A AND B)`

Classically equivalent to:

```text
NOT A OR NOT B
```

But the latter syntactically exposes at least two failure routes, while the negated conjunction may be processed as one unresolved failure condition.

This is exactly the sort of distinction observed in De-Morgan counterfactual experiments.

---

# 79. Prevention decomposition

For `NOT(A AND B)`, prevention routes can include:

```text
prevent A
prevent B
prevent both
alter relationship that made conjunction meaningful
```

These need not be equivalent in downstream effects.

---

# PART XX — PHYSICAL MATCHED CASES

# 80. Disjunctive trigger

```text
If sensor A or sensor B had triggered, shutdown would have occurred.
```

Route-wise reading:

```text
A-trigger route -> shutdown?
B-trigger route -> shutdown?
```

This can matter if the sensors connect to different mechanisms.

---

# 81. Union-nearest reading

If A triggering requires a tiny perturbation and B requires a massive physical change, a global minimal-change semantics may evaluate only A-route.

That is a different reading from route-wise robust shutdown.

---

# 82. Conjunctive physical intervention

```text
If pressure increased and cooling failed...
```

requires joint compatibility and can be strongly nonmonotonic relative to either antecedent alone.

---

# PART XXI — SOFTWARE MATCHED CASES

# 83. Disjunctive mitigation

```text
If cache were disabled or dependency patched, crash would stop.
```

Route-wise SDA reading claims:

```text
disable cache -> no crash
patch dependency -> no crash
```

A global-union reading can be true even if only the easier/closer mitigation works.

---

# 84. Conjunctive patch conflict

```text
patch P AND downgrade dependency D
```

can be jointly invalid even when each alteration works independently against factual software.

WDF2-F joint composability applies.

---

# 85. Negated feature

```text
if feature F were not active
```

can mean:

```text
config off
code removed
license absent
runtime guard false
```

Different failure routes.

---

# PART XXII — INSTITUTIONAL MATCHED CASES

# 86. Disjunctive qualification

Rule:

```text
credential A OR credential B qualifies Actor
```

The institutional status truth condition may be disjunctive.

But counterfactual route questions can distinguish:

```text
qualification via A
qualification via B
```

because rights, provenance or downstream review differ.

---

# 87. Exclusive category

Some regimes specify:

```text
exactly one of A/B statuses
```

Then XOR semantics is constitutive, not merely pragmatic exclusion.

---

# 88. Negation under open-world rules

`not authorized by A` does not imply `authorized by B`.

Negation therefore cannot silently become a closed-world complement unless the institutional model says so.

### Earned firewall J-OWA-1

```text
NegationUnderOpenWorldRegime != ClosedWorldEnumeratedAlternative
```

---

# PART XXIII — AGENT-ERA MATCHED CASES

# 89. Tool-choice antecedent

```text
If Agent used tool A or tool B, would task succeed?
```

Can mean:

```text
robust across either tool
best available tool
policy chooses one tool
unknown which tool was used
```

These are different disjunctive query roles.

---

# 90. Provider disjunction

```text
If provider M1 or M2 handled the turn...
```

route identity matters because providers differ in:

```text
latent state
policy
capabilities
randomness
```

No averaging by default.

---

# 91. Conjunctive Agent antecedent

```text
new provider AND memory disabled
```

requires WDF2-F multi-locus composition; provider change can invalidate the memory representation itself.

---

# 92. Negated action

```text
If Agent had not called tool T...
```

can be realized by:

```text
choosing different tool
answering without tool
refusing
failing before tool call
lacking authorization
```

These have different consequences and causal interpretations.

---

# PART XXIV — PROBABILITY SEMANTICS

# 93. Three probability locations

For disjunctive antecedents distinguish:

```text
P(route)
P(outcome | route)
P(model/generator)
```

and potentially:

```text
P(completion)
```

These are not one probability.

---

# 94. Route uncertainty vs outcome stochasticity

```text
uncertain whether A-route or B-route realizes antecedent
```

is distinct from:

```text
stochastic outcome under fixed A-route
```

### Earned firewall J-PROB-1

```text
RouteUncertainty != WithinRouteStochasticity
```

---

# 95. Route mixture

A quantity:

```text
Σ_r w_r P(C | route r)
```

requires interpretation of `w_r`.

It can represent:

```text
policy randomization
objective chance of route
epistemic uncertainty
semantic weighting architecture
```

These are different.

---

# 96. Robust route envelope

If weights are unjustified, WDF2-E suggests preserving:

```text
min/max or set of route-specific outcomes
```

rather than inventing a mixture.

---

# PART XXV — SEMANTIC VS PRAGMATIC DECOMPOSITION

# 97. Semantic alternative theory

Disjunction itself contributes several semantic alternatives.

Strength:

```text
direct SDA explanation
compositional route preservation
```

---

# 98. Exhaustification/pragmatic theory

A simpler semantic representation may be enriched by a non-Gricean or pragmatic process that yields SDA-like interpretation.

Strength:

```text
can preserve simpler truth-conditional lexical semantics
```

---

# 99. Foundation verdict

The empirical facts do not force one source universally.

What WDF2-J does require is that the **resolved counterfactual query representation** can preserve relevant alternative structure when the reading demands it.

### Earned firewall J-LEVEL-1

```text
CounterfactualQueryAlternativeStructure
!= NecessarilyLexicalAlternativeStructure
```

---

# PART XXVI — COMPOSITION CONTRACT

# 100. Research-level antecedent composition representation

A complex antecedent may need:

```text
TruthConditionProjection
Alternative/ResolutionStructure
LogicalCompositionStructure
TypedAtomicContents
SharedBackground/Preservation
RouteCompatibility
RouteExclusion/Overlap
TemporalOrder when explicit
QueryRole
```

Not all fields are required in every case.

---

# 101. Atomic leaf

An atomic leaf resolves using WDF2-I content typing:

```text
state claim
surgery
rule revision
model revision
logical/mathematical supposition
```

---

# 102. ALL node

Conjunction-like node requires:

```text
joint satisfiability
composition semantics
compatibility
```

and does not imply arbitrary sequential order.

---

# 103. ANY node

Inclusive alternative node exposes multiple realization routes while allowing overlap unless excluded.

---

# 104. ONE-OF node

Exclusive alternative node includes mutual-exclusion constraints.

---

# 105. NOT node

Negation node requires a domain-relative complement/failure-family interpretation.

Its decomposition cannot be inferred from syntax alone in open or infinite domains.

---

# PART XXVII — NORMALIZATION

# 106. Truth-conditional normalization

Classical rewrites can normalize truth conditions:

```text
De Morgan
associativity
commutativity
distributivity
idempotence
```

---

# 107. Counterfactual-content normalization is stricter

A rewrite is safe only if it preserves the semantic projections relevant to the query:

```text
alternative structure
surgery identity
framework revision
topic/relevance
preservation implications
```

### Earned firewall J-NORM-1

```text
BooleanNormalization != CounterfactualContentNormalization
```

---

# 108. Safe local normalization example

Within a binary stable variable domain:

```text
NOT(X=0)
```

and:

```text
X=1
```

may normalize safely.

---

# 109. Unsafe normalization example

```text
A OR B
```

and:

```text
NOT(NOT A AND NOT B)
```

can share truth conditions but differ in alternative structure.

---

# PART XXVIII — EQUIVALENCE RELATIONS

# 110. Boolean equivalence

```text
A ≡_bool B
```

same truth conditions in declared logic.

---

# 111. Alternative equivalence

```text
A ≡_alt B
```

same counterfactual alternative/resolution family up to declared quotienting.

---

# 112. Surgery equivalence

```text
A ≡_surg B
```

same typed alterations/composition plans.

---

# 113. Query equivalence

```text
A ≡_Q B
```

same target counterfactual result for Q across relevant admissible semantics.

### Earned firewall J-EQ-1

```text
BooleanEquivalence != AlternativeEquivalence != SurgeryEquivalence != QueryEquivalence
```

---

# PART XXIX — ASSOCIATIVITY / COMMUTATIVITY / IDEMPOTENCE

# 114. Boolean disjunction/conjunction

At truth-condition level:

```text
A OR B = B OR A
(A OR B) OR C = A OR (B OR C)
A OR A = A
```

and corresponding laws for conjunction.

---

# 115. Alternative representation can quotient these laws

A well-designed route representation should often treat reordering/bracketing as irrelevant when it carries no additional syntax/pragmatics.

---

# 116. Duplicate-alternative idempotence needs care

`A OR A` should generally not create two probabilistically distinct routes merely because A appeared twice syntactically.

### Earned firewall J-DUP-1

```text
DuplicateSyntax != TwoIndependentCounterfactualRoutes
```

unless repetition itself has an independently meaningful operation/time interpretation.

---

# 117. Temporal and causal bracketing can remain significant

```text
(A then B) OR C
```

cannot be normalized by ordinary commutative Boolean algebra if temporal sequence is part of content.

---

# PART XXX — ALTERNATIVE GRANULARITY

# 118. Too coarse

One union proposition erases routes.

---

# 119. Too fine

Every syntactic parse path as a distinct alternative overfits.

---

# 120. Principled quotienting

Alternative routes can be collapsed when they are equivalent under declared criteria such as:

```text
same typed surgery
same framework revision
same target grain
same preservation effects
same query-relevant downstream behavior
```

WDF2-I equivalence discipline applies.

---

# PART XXXI — DELETION TESTS

# 121. Treat disjunction as only possible-world union

**FAIL** for SDA/De-Morgan alternative-sensitive readings.

---

# 122. Treat every disjunction as route-wise universal

**FAIL** for global-union, choice/menu and some pragmatic readings.

---

# 123. Validate universal SDA

**FAIL** as foundation-wide axiom without antecedent-structure/query-role typing.

---

# 124. Delete SDA entirely

**FAIL** because strong ordinary readings and established semantic frameworks validate it systematically.

---

# 125. Validate unrestricted SA

**FAIL** through mechanism-changing strengthened antecedents.

---

# 126. Forbid all antecedent strengthening

**FAIL** because irrelevant/compatible strengthening can preserve conclusions locally.

---

# 127. Substitute all logical equivalents freely

**FAIL** through Fine/Briggs/De-Morgan pressure.

---

# 128. Reject Boolean truth equivalence entirely

**FAIL**.

The point is not that classical truth conditions disappear; they are one projection among several.

---

# 129. Treat conjunction as unordered independent assignments

**FAIL** when conjuncts are dependent, conflicting, temporal or framework-changing.

---

# 130. Treat conjunction as always sequential

**FAIL** for simultaneous/joint constraints.

---

# 131. Treat negation as one unique surgery

**FAIL** across multi-valued/open-world/failure-route cases.

---

# 132. Treat negation as semantically structureless complement only

**FAIL** when route/prevention decomposition affects counterfactual consequence.

---

# 133. Treat XOR as ordinary OR

**FAIL** because exclusion constraints alter admissible routes.

---

# 134. Assume alternatives form a partition

**FAIL** for overlapping inclusive disjuncts.

---

# 135. Assign probability weights to alternatives by default

**FAIL**; route identity does not determine probability interpretation.

---

# 136. Average route outcomes automatically

**FAIL** under WDF2-E mixture firewall.

---

# 137. Treat truthmaker route as causal route

**FAIL** universally.

---

# 138. Treat semantic alternative origin as settled by SDA data

**FAIL**; 2026 work still compares semantic alternatives and exhaustification-style accounts.

---

# PART XXXII — STRONG RESULTS

# 139. Strong result — antecedents have at least two semantic projections

For counterfactual foundation purposes:

```text
TruthConditionProjection
```

and:

```text
Alternative/RealizationProjection
```

must be separable.

They can coincide in simple atomic cases and diverge in disjunction/negation cases.

---

# 140. Strong result — Boolean equivalence survives only at one layer

Classical equivalence remains valid for ordinary truth conditions while failing to guarantee counterfactual substitution.

This reconciles:

```text
preserve logic
```

with:

```text
respect hyperintensional antecedent behavior.
```

---

# 141. Strong result — disjunction can denote route pluralism

A resolved counterfactual antecedent can expose several routes without turning those routes into probabilistic worlds or ontological entities.

---

# 142. Strong result — conjunction invokes WDF2-F composition

Once conjuncts carry typed alterations, `AND` becomes a joint-composability question, not merely a Boolean intersection.

---

# 143. Strong result — negation is domain-relative route generation

`NOT A` can require:

```text
complement states
falsemakers
prevention surgeries
premise deletions
```

and the correct representation depends on domain/query role.

---

# 144. Strong result — route semantics and route weighting separate

The antecedent can tell us **which routes matter** without telling us **how much weight each route has**.

This preserves WDF1/WDF2-E measure interpretation firewalls.

---

# 145. Strong result — the SDA/SA conflict is a content-grain theorem

The tension between SDA and SA is not accidental.

It proves that an antecedent representation fine enough to preserve disjunct alternatives cannot simultaneously identify all classical logical equivalents for unrestricted counterfactual substitution.

---

# PART XXXIII — EXTERNAL RESEARCH PRESSURE

# 146. Alonso-Ovalle 2009

`Counterfactuals, Correlatives, and Disjunction` argues that disjunctive antecedents naturally require selecting closest worlds separately from the alternatives introduced by each disjunct; standard Boolean `or` does not expose this structure.

Foundational pressure:

```text
DisjunctionAlternativeStructure is semantically real for important counterfactual readings.
```

---

# 147. Ciardelli 2016 / inquisitive semantics

`Lifting conditionals to inquisitive semantics` gives a general method where antecedents can contribute multiple propositions and disjunction introduces multiple assumptions.

Foundational pressure:

```text
alternative-sensitive antecedent structure can be layered over multiple base conditional theories.
```

---

# 148. Champollion/Ciardelli/Zhang 2016

`Breaking de Morgan's law in counterfactual antecedents` experimentally finds that truth-conditionally equivalent disjunctive and negated-conjunctive antecedents make different semantic contributions in counterfactuals.

Foundational pressure:

```text
TruthConditionalEquivalence != CounterfactualAlternativeEquivalence.
```

---

# 149. Zani/Ciardelli/Sanfelici 2026

Their SDA acquisition work confirms the continued empirical significance of disjunctive-antecedent simplification and explicitly compares alternative-generation with exhaustification-style explanations.

Foundational pressure:

```text
SDA remains live; its representational origin is not settled by one theory.
```

---

# 150. Briggs 2012

`Interventionist counterfactuals` extends causal-model counterfactual language beyond restricted antecedents and shows major logical consequences, including failure of unrestricted substitution of classical logical equivalents in antecedents.

Foundational pressure:

```text
complex antecedent semantics changes inference logic, not merely parsing.
```

---

# 151. Rosella/Sprenger 2024

Their causal-model semantics handles disjunctive and arbitrary Boolean antecedents using truthmaking submodels and a distance-based weighting scheme.

Foundational pressure:

```text
complex Boolean antecedents can be represented through structured submodels rather than bare formula truth sets.
```

---

# 152. Halpern 2011

`From Causal Models To Counterfactual Structures` identifies a disjunction-involving axiom as crucial to the comparison between recursive causal models and possible-world counterfactual structures.

Foundational pressure:

```text
excluding disjunction from a formal language can conceal substantive counterfactual constraints.
```

---

# PART XXXIV — WDF0 / WDF1 REOPEN AUDIT

# 153. WDF0

No FoundationReopenCondition fires.

WDF2-J reinforces:

```text
Representation != Reality
Same_X != Same_Y without criterion
Cause != Constitution
PhysicalPattern != SemanticContent
Relative != Subjective
```

Alternative structure is a semantic/representational interface, not a new Reality root.

WDF0 remains frozen.

---

# 154. WDF1

No FoundationReopenCondition fires.

WDF1's typed modal claim grammar already requires alternative specification/generator and keeps probability measure separate from interpretation.

WDF2-J strengthens exactly these separations:

```text
AlternativeSet != ProbabilityDistribution
RouteUncertainty != WithinRouteStochasticity
```

WDF1 remains frozen.

---

# PART XXXV — RECONSTRUCTION

# 155. Complex antecedent research grammar

A resolved antecedent can be represented diagnostically as:

```text
Antecedent =
  TruthConditionProjection
  + ContentLeaves
  + CompositionStructure
  + Alternative/ResolutionStructure
  + RouteCompatibility/Exclusion
  + TypedSurgeryMapping where applicable
  + SharedPreservation/Background
  + QueryRole
  + WeightingInterpretation when present
```

This is not a production object.

---

# 156. Alternative result shapes

Antecedent resolution can yield:

```text
SingleRoute
RouteFamily
OverlappingRouteFamily
ExclusiveRouteFamily
JointCompoundRoute
NestedAlternativeTree
NoJointlyAdmissibleRoute
ModelRevisionRequired
AlternativeDomainExtensionRequired
```

---

# 157. Route-level evaluation

Each route then enters prior WDF2 machinery:

```text
WDF2-C/D generator admissibility
WDF2-E underdetermination/robustness
WDF2-F multi-surgery composition
WDF2-G cross-world completion
WDF2-H impossible-domain extension
WDF2-I content/relevance
```

WDF2-J therefore closes a major representational gap between antecedent language and generator evaluation.

---

# 158. No single route aggregator earned

After route evaluation, possible aggregators include:

```text
universal/all-route would
existential/some-route might
closest-route selection
weighted expectation
robust lower/upper envelope
set-valued answer
```

Which one is correct depends on conditional operator/query role.

This leads directly to the next residual.

---

# PART XXXVI — LARGEST REMAINING RESIDUAL

# 159. Antecedent semantics is now much stronger than consequence logic

WDF2-A through J can now say a great deal about:

```text
what antecedent means
which routes it exposes
how alternatives are generated
which surgeries compose
which models/completions/extensions survive
```

But we have not systematically established the **logic of consequence among counterfactual claims themselves**.

---

# 160. Existing local inference results conflict across architectures

Already encountered:

```text
SDA can hold under route semantics
SA fails generally
logical-equivalent substitution can fail
Briggs' extended interventionist logic can invalidate modus ponens
nested counterfactual associativity/import-export is not automatic
counterfactual consequence is nonmonotonic
```

These are no longer isolated curiosities.

They form a new research object:

```text
CounterfactualInferenceArchitecture
```

---

# 161. Detachment is not yet settled

For:

```text
A
A □→ C
```

when can one infer C?

In ordinary material/strict settings this seems straightforward; in some extended interventionist systems the relevant formal `modus ponens` behavior changes because antecedent formulas and intervention semantics are hyperintensional.

A foundation must distinguish:

```text
actuality detachment
intervention execution
suppositional consequence
model-valid inference
pragmatic acceptance
```

---

# 162. Transitivity is not yet settled

From:

```text
A □→ B
B □→ C
```

one cannot generally infer:

```text
A □→ C
```

because the B-worlds reached from A can differ from the B-worlds selected directly.

This needs systematic model-class analysis.

---

# 163. Contraposition is not yet settled

From:

```text
A □→ C
```

counterfactuals do not generally license:

```text
NOT C □→ NOT A
```

Causal direction, relevance and alternative structure interfere.

---

# 164. Conditional excluded middle remains open

Whether:

```text
(A □→ C) OR (A □→ NOT C)
```

holds depends on uniqueness/plurality/nondeterminism and conditional semantics.

WDF2-B/C already rejected universal unique-nearest-alternative assumptions.

---

# 165. Import-export / iteration remains open

Compare:

```text
A □→ (B □→ C)
```

with:

```text
(A AND B) □→ C
```

WDF2-F showed they are not generally identical.

A full conditional-logic audit is still missing.

---

# 166. Nonmonotonic consequence structure remains open

Counterfactual inference shares structural features with nonmonotonic reasoning:

```text
adding information/antecedent conjunct can retract consequence
```

But it does not follow that one standard nonmonotonic logic is the correct foundation.

Need compare:

```text
cautious monotony
cut
rational monotony
preferential consequence
conditional logics
causal-model consequence
```

without preselection.

---

# 167. Exact next round

The next canonical round is therefore:

# **WDF2-K — Counterfactual Consequence / Inference / Detachment / Iteration**

WDF2-K should systematically test:

```text
modus ponens / factual detachment
modus tollens
transitivity
contraposition
strengthening / weakening
SDA as an inference rule
substitution of equivalents
conditional excluded middle
import-export
nested/iterated counterfactuals
cautious monotony / cut / rational monotony
would vs might inference
probabilistic counterfactual inference
model-class-relative soundness
semantic truth vs accepted/suppositional inference
```

It must not preselect Lewis conditional logic, Stalnaker logic, Pearl/SCM inference, preferential/nonmonotonic logic or interventionist axiomatization as universally correct.

Only WDF2-K residuals may determine WDF2-L.

---

# 168. Production disposition

No production changes are admitted.

Do **not** add:

```text
AntecedentAlternativeTree
BooleanCounterfactualAST
RouteWeight
SDAEvaluator
NegationRouteGenerator
TruthmakerSubmodelEngine
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

Counterfactual Foundations remain open.

---

# 169. Closeout

```text
WDF2-J: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D/E/F/G/H/I reopen: NO
Production refactor: NO

SameTruthConditions != SameAntecedentAlternativeStructure
ObservedAlternativeSensitiveReading != ProofOfOneUniqueLexicalSemantics
DisjunctiveTruthSet != DisjunctiveRouteStructure
ClosestWithinUnion != ClosestWithinEachAlternative
ExclusiveDisjunctionRoutes != InclusiveDisjunctionRoutes
DisjunctiveFact != DisjunctiveChoiceSet
AlternativeFamily != MutuallyExclusiveEventPartition
AntecedentAlternativeSet != ProbabilityDistributionOverAlternatives
RouteWeightingRule != AntecedentMeaning
IndividuallyAdmissibleConjuncts != JointlyAdmissibleConjunction
BooleanConjunction != TemporalSequentialComposition
NegatedTruthCondition != OneCounterfactualFailureRoute
NotA != OneUniquePreventionIntervention
DeMorganTruthConditionalEquivalence != CounterfactualAlternativeEquivalence
BooleanDistributivity != AutomaticCounterfactualDecompositionEquivalence
LogicalCompositionTree != CounterfactualSurgeryPlan
TruthmakingAlternative != CausalRealizationRoute
SDAValidity is antecedent-structure/query-role sensitive
GeneralSAInvalid != NoValidAntecedentStrengtheningCases
LogicalRedundancy != CounterfactualContentRedundancy
TautologicalTruthCondition != CounterfactualNoOp under every antecedent semantics
RouteUncertainty != WithinRouteStochasticity
CounterfactualQueryAlternativeStructure != NecessarilyLexicalAlternativeStructure
BooleanNormalization != CounterfactualContentNormalization
BooleanEquivalence != AlternativeEquivalence != SurgeryEquivalence != QueryEquivalence
DuplicateSyntax != TwoIndependentCounterfactualRoutes

Exact next round:
WDF2-K — Counterfactual Consequence / Inference / Detachment / Iteration
```

Compressed result:

> **WDF2-J establishes that complex counterfactual antecedents require at least two separable semantic projections: ordinary truth conditions and an alternative/realization structure. Disjunction is the decisive case. A bare Boolean union preserves which worlds satisfy `A∨B` but can erase whether A or B is the route by which the antecedent is realized. Alternative, inquisitive and truthmaker approaches preserve those routes and thereby explain strong Simplification of Disjunctive Antecedents readings, while global closest-within-union readings can legitimately behave differently. SDA therefore cannot be a foundation-wide untyped axiom. The deeper structural constraint is a trilemma: unrestricted substitution of logical equivalents plus universal SDA would derive unrestricted Strengthening of the Antecedent via `A ≡ (A∧B)∨(A∧¬B)`, yet SA fails systematically when the added conjunct changes mechanisms, preservation, surgeries or route structure. Classical Boolean equivalence must therefore remain a truth-condition relation without becoming automatic counterfactual-content equivalence. Conjunction maps to joint constraints or WDF2-F compound surgery and requires compatibility; negation typically denotes a family of failure/prevention routes rather than one unique intervention; exclusive disjunction introduces exclusion constraints; and inclusive alternatives may overlap, so alternative families are not probability partitions. Semantic route identity, route weighting and within-route stochasticity must remain separate. Empirical De-Morgan effects further show that truth-conditionally equivalent antecedents can contribute different alternative structure, while 2026 SDA acquisition work leaves the semantic-vs-exhaustification source of that structure open. The surviving foundation is therefore typed and layered: retain truth conditions, content leaves, composition/alternative structure, compatibility/exclusion, shared preservation and weighting provenance separately. With complex antecedent structure now substantially reconstructed, the largest remaining gap moves from representation to inference: which detachment, transitivity, contraposition, import-export, conditional-excluded-middle and nonmonotonic consequence principles actually survive across the plural counterfactual model classes already uncovered. WDF2 therefore advances next to Counterfactual Consequence / Inference / Detachment / Iteration.**
