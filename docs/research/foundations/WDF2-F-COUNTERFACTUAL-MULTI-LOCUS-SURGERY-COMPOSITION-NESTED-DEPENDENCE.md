# WDF2-F — Counterfactual Multi-Locus Surgery / Composition / Nested Dependence

Status: **complete for WDF2-F**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D/E remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-F residuals:

```text
WDF2-G — Counterfactual Cross-World Coherence / Consistency / Compatibility
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-A through WDF2-E established that a counterfactual query requires typed alteration, preservation, correspondence, generator admissibility, and explicit handling of underdetermination.

Until now, most falsifiers were deliberately close to one-locus alterations.

Real counterfactuals often alter several loci:

```text
value + action
policy + future action sequence
mechanism + parameter
rule + credential
model + variable domain
provider + prompt + memory + tool availability
network structure + node state
law/mechanism + boundary condition
```

WDF2-F asks:

> **How do several counterfactual surgeries compose, and when is composition itself undefined, order-sensitive, cross-world, or structurally revisionary?**

The round tests:

```text
simultaneous vs sequential surgery
commutativity
associativity
idempotence
overwrite/conflict
precedence
preservation recomputation
policy adaptation
structural-state change
nested counterfactuals
cross-world substitution
probability/coupling composition
identity across sequential transformations
model revision mid-chain
```

---

# 2. Initial anti-collapse laws

WDF2-F immediately rejects:

```text
MultipleAlterations != UnorderedSetOfAssignments
SequentialSurgery != SimultaneousSurgery
NestedCounterfactual != SequentialIntervention by definition
CrossWorldSubstitution != SameWorldCompoundIntervention
PolicyChange != FixedFutureActionSequence
StructuralChange != OrdinaryValueChange
```

These are not stylistic distinctions.

They determine what the altered scenario is.

---

# 3. Surgery as a partial frame transformation

WDF2-A treated an alteration as a typed component of a counterfactual frame.

WDF2-F now requires a stronger diagnostic view.

Let a research frame be:

```text
F =
  Anchor
  + Model/DomainRepresentation
  + AlterationContext
  + PreservationProfile
  + Identity/Correspondence
  + QueryRole
  + TruthRole
  + GeneratorContext
```

A surgery is not merely:

```text
Δ : value -> value
```

but schematically:

```text
Δ : F ⇀ F'
```

where the arrow is **partial**.

It can fail because:

```text
target no longer exists
alteration contradicts protected structure
identity map is unavailable
new model language is required
second surgery presupposes a structure removed by the first
```

### Earned firewall F-PARTIAL-1

```text
SurgeryApplicability is not guaranteed by syntax.
```

---

# 4. Why the result is a frame, not only a world state

After changing:

```text
program version
institutional rule
causal mechanism
network structure
provider/model
```

the next counterfactual step may require different:

```text
preservation profile
variable meanings
identity mapping
available actions
policy semantics
causal graph
probability coupling
```

Therefore surgery output must conceptually update the **interpretive frame**, not merely mutate a state vector.

### Earned firewall F-FRAME-1

```text
PostSurgeryFrame != PreSurgeryFrame + NewStateValues only
```

---

# PART I — SIMULTANEOUS COMPOUND SURGERY

# 5. Independent hard assignments in a fixed SCM

Consider a fixed acyclic SCM with distinct endogenous variables X and Z.

A compound hard intervention:

```text
do(X=x, Z=z)
```

replaces the equations for X and Z simultaneously.

Under this narrow regime, there is a strong normalization intuition:

```text
do(X=x); do(Z=z)
```

and:

```text
do(Z=z); do(X=x)
```

can produce the same surgically modified fixed model when:

```text
X != Z
both are ordinary hard equation replacements
neither surgery changes the variable/model vocabulary
neither assignment is defined in terms of the other's post-surgery natural value
the same exogenous/background coupling is used
```

This is a **conditional commutativity result**, not a universal surgery law.

---

# 6. Conditional commutativity law

For distinct fixed-model hard interventions:

```text
Δ_X=x ∘ Δ_Z=z
≈
Δ_Z=z ∘ Δ_X=x
```

under declared fixed-model conditions.

### Earned firewall F-COMM-1

```text
SomeHardInterventionsCommute
!= CounterfactualSurgeriesCommuteUniversally
```

---

# 7. Same-locus identical hard intervention

Sequentially applying:

```text
X := x
X := x
```

under one fixed-model hard-intervention semantics adds no further structural change.

So a local idempotence property can hold:

```text
Δ_X=x ∘ Δ_X=x = Δ_X=x
```

provided the second operation has the same semantics and no time-indexed meaning.

### Caveat

If the two assignments occur at different times:

```text
X_t := x
X_{t+1} := x
```

this is not the same-locus same-time operation and idempotence does not follow.

---

# 8. Same-locus conflicting simultaneous assignments

A compound request:

```text
X := x
AND
X := x'
```

with:

```text
x != x'
```

at the same semantic locus/time cannot be resolved by pretending the intervention set is an unordered set.

Possible outcomes are:

```text
InvalidCompoundSurgery
```

or a richer semantics that distinguishes layers/times/conditions.

### Earned firewall F-CONFLICT-1

```text
Conflict != Tie
```

A contradictory compound surgery is not a pair of equally good alternatives.

---

# 9. Sequential overwrite is different from simultaneous conflict

A declared sequence:

```text
X := x;
then X := x'
```

can have a last-write / later-surgery interpretation under some hard-update semantics.

That does **not** license resolving simultaneous:

```text
{X:=x, X:=x'}
```

by arbitrary precedence.

### Earned firewall F-SEQ-1

```text
SequentialOverwrite != SimultaneousConflictResolution
```

---

# PART II — NATURAL-VALUE-DEPENDENT AND POLICY SURGERIES

# 10. Shift intervention matched case

Suppose:

```text
X natural value = x_nat
```

and surgery is:

```text
X := x_nat + δ
```

Now manipulate several variables.

The second shift can mean at least two things:

```text
A. shift relative to each variable's factual/natural value
B. shift relative to the response after prior shifts
```

These are not equivalent.

Research on shift interventions explicitly distinguishes:

```text
shift interventions on the treated
```

from recursively defined:

```text
shift interventions as policies
```

when multiple variables are manipulated.

This is direct external evidence that multi-variable intervention semantics depend on **which natural value the surgery references**.

---

# 11. Reference-state typing

Every surgery that depends on a natural/current value needs a reference state:

```text
FactualReference
PrecedingCounterfactualReference
CurrentBranchReference
PopulationPolicyReference
```

### Earned firewall F-REF-1

```text
FunctionOfNaturalValue
```

is incomplete until the relevant natural-value anchor is declared.

---

# 12. Policy intervention is adaptive composition

A policy π is not generally a fixed sequence:

```text
[a1,a2,a3,...]
```

It is a rule such as:

```text
a_t = π(h_t)
```

where history h_t depends on earlier counterfactual outcomes.

Changing policy therefore changes future actions **recursively**.

Research on policy interventions in treatment-outcome sequences emphasizes precisely this point: future treatments are determined by policy and may adapt to previous outcomes, so changing policy is not reducible to pre-fixing one treatment sequence.

### Earned firewall F-POLICY-1

```text
PolicyIntervention != InterventionOnOneRealizedActionSequence
```

---

# 13. Sequential policy composition

Suppose:

```text
π1 used during interval I1
π2 used during interval I2
```

The result depends on state/history produced by π1 before π2 begins.

Thus:

```text
π2 ∘ π1
```

is semantically sequential.

Changing order can change:

```text
state distribution
available actions
future policy inputs
absorbing states
resource inventory
```

No general commutativity is earned.

---

# PART III — MECHANISM VS VALUE SURGERY

# 14. Mechanism then value

Suppose X is generated by mechanism:

```text
X := f(PA_X,U_X)
```

Two surgeries:

```text
ΔM: f -> f'
ΔV: X := x
```

Sequence A:

```text
ΔM;
ΔV
```

can yield a final model where X is hard-clamped, making f' irrelevant for X under that intervention.

---

# 15. Value then mechanism

Sequence B:

```text
ΔV;
ΔM
```

requires semantics for whether ΔM modifies:

```text
the dormant natural mechanism
or
the currently overridden assignment mechanism
```

Different intervention formalisms may answer differently.

### Strong result

The pair is not automatically commutative because the second surgery can target a structure replaced by the first.

### Earned firewall F-TARGET-1

```text
SurgeryTargetIdentity must survive prior surgery.
```

---

# 16. Mechanism replacement can invalidate preservation

Suppose the original frame says:

```text
preserve mechanism f
```

and ΔM explicitly replaces f.

The old preservation profile is no longer globally valid.

It must be transformed/revalidated.

### Earned firewall F-PRES-1

```text
PreservationProfileAfterSurgery
!= PreservationProfileBeforeSurgery by default
```

---

# PART IV — RULE / CONSTITUTION SURGERY

# 17. Credential then rule change

Anchor rule:

```text
K: credential C confers authorization A
```

Sequence:

```text
1. give Actor C
2. replace K with K' where C no longer confers A
```

Final authorization may be false.

---

# 18. Rule change then credential

Sequence:

```text
1. replace K with K'
2. give Actor C
```

can produce the same final result in this simple case.

But if K' changes what counts as credential C itself, then the second surgery's target meaning changes.

### Earned firewall F-CONST-1

```text
ConstitutiveRuleChange can change the semantics of later alteration targets.
```

This is stronger than ordinary state dependence.

---

# 19. Status identity after rule reform

Suppose under K:

```text
status S = licensed operator
```

and under K':

```text
S no longer exists
new status S' has different rights/duties
```

A later surgery:

```text
set S=true
```

is not simply false; it may be **ill-typed after K'**.

Correct result can be:

```text
TargetNoLongerDefined
```

or:

```text
CrossModelCorrespondenceRequired
```

rather than a value assignment.

---

# PART V — SOFTWARE / RUNTIME COMPOSITION

# 20. Config then code patch

Program version V:

```text
config c controls behavior b
```

Sequence:

```text
c := off
then patch V -> V' where c is removed
```

The second surgery can eliminate the locus affected by the first.

---

# 21. Code patch then config

If V' no longer defines c, then:

```text
patch first;
then c := off
```

is ill-typed.

### Falsifier

Any universal composition rule that merely merges key/value updates cannot represent this case honestly.

---

# 22. Dependency-version case

Change:

```text
application code
+
dependency version
```

The application patch may have been authored against the old dependency API.

Thus the combined surgery can be invalid even though each surgery is individually valid against the factual system.

### Earned firewall F-COMPAT-1

```text
IndividuallyAdmissible(Δ1)
∧ IndividuallyAdmissible(Δ2)
```

does not imply:

```text
JointlyComposable(Δ1,Δ2)
```

---

# PART VI — NETWORK / RELATIONAL STRUCTURE CHANGE

# 23. Network intervention

Changing a network edge:

```text
remove tie i-j
```

is a structural intervention on a relation, not merely changing a node attribute.

Research on network interventions explicitly treats creation/severance of ties as a distinct structural intervention family.

This matters because later node-level effects can depend on the new topology.

---

# 24. Node state then edge removal

If node-level surgery depends on neighborhood aggregate:

```text
X_i := g(neighbors(i))
```

then performing:

```text
X_i update
then remove edge
```

can differ from:

```text
remove edge
then recompute/update X_i
```

because the parent/relation set changed.

No general commutativity.

---

# 25. Structural relation deletion can invalidate identity paths

If Actor or system identity is tracked partly through relational role:

```text
member-of
controller-of
connected-to
```

a structural intervention can invalidate correspondence criteria used by later steps.

Composition therefore needs identity revalidation as well as target revalidation.

---

# PART VII — PATH-DEPENDENT STRUCTURE

# 26. Fixed graph over time is not universal

Longitudinal counterfactual reasoning often assumes one causal graph replicated through time.

Path-dependent structural equation models were introduced specifically because interventions can alter later state transitions and thereby change the qualitative causal structure encountered downstream.

This is direct pressure against:

```text
OneStaticGraph + SequenceOfValueInterventions
```

as a universal temporal counterfactual architecture.

---

# 27. Frame evolution

A sequential counterfactual can therefore require:

```text
F0 --Δ1--> F1 --Δ2--> F2 ...
```

where:

```text
ModelStructure(F0) != ModelStructure(F1)
```

and later surgeries must be interpreted against the current frame, not the factual frame by default.

### Earned firewall F-EVOLVE-1

```text
SequentialCounterfactualEvaluation != RepeatedEvaluationAgainstOriginalModel
```

unless explicitly defined that way.

---

# PART VIII — COMPOSITION ALGEBRA: WHICH LAWS SURVIVE?

# 28. Identity/no-op

A well-defined no-op surgery can satisfy:

```text
Id ∘ Δ = Δ
Δ ∘ Id = Δ
```

when no-op truly leaves the frame unchanged.

This is a safe local algebraic property.

---

# 29. Idempotence

Idempotence is **typed and conditional**.

Examples where it can hold:

```text
same-time hard assignment X:=x repeated
same rule replacement K:=K' repeated
```

if the second operation is semantically identical.

Examples where it fails:

```text
increment X by +1 twice
apply policy for one more time interval
remove one available resource unit twice
time-indexed treatment
```

### Earned firewall F-IDEM-1

```text
Idempotence is operation-specific, not a universal intervention axiom.
```

---

# 30. Commutativity

Potentially holds for:

```text
disjoint hard assignments in stable fixed model
```

Potentially fails for:

```text
policy/history-dependent alterations
mechanism + value changes
rule + status changes
network + neighbor-dependent changes
model revision + variable assignment
```

Thus:

```text
Commute(Δ1,Δ2 | F)
```

must be a typed relation, not assumed globally.

---

# 31. Associativity

Pure function composition is associative when all transformations are defined:

```text
Δ3 ∘ (Δ2 ∘ Δ1)
=
(Δ3 ∘ Δ2) ∘ Δ1
```

But counterfactual syntax can introduce different re-anchoring/re-preservation boundaries.

For example:

```text
[Δ1 then Δ2] under one compound frame,
then Δ3
```

can differ semantically from:

```text
Δ1,
then evaluate a new nested counterfactual [Δ2 then Δ3]
```

because the inner counterfactual may recompute relevance/background or change anchor scope.

### Earned firewall F-ASSOC-1

```text
TransformCompositionAssociativity
!= NestedCounterfactualAssociativity
```

---

# 32. Monotonicity fails

Adding another surgery does not generally preserve previous counterfactual consequence.

```text
Δ1 -> C
```

but:

```text
Δ1 + Δ2 -> not-C
```

is normal.

Therefore multi-surgery counterfactual consequence is not monotonic in antecedent additions.

This is consistent with earlier counterfactual nonmonotonicity pressure.

---

# PART IX — STATIC VS DYNAMIC PRESERVATION

# 33. Static preservation fails under structural change

Suppose initial preservation says:

```text
keep program semantics V fixed
```

and the compound antecedent includes:

```text
V -> V'
```

The preservation rule must be revised.

Likewise:

```text
preserve institutional rule K
```

cannot survive a rule-reform surgery that targets K.

---

# 34. Preservation transition

WDF2-F therefore introduces a research operation:

```text
RevalidatePreservation(P_i, Δ_i, F_i) -> P_{i+1}
```

Possible outcomes:

```text
unchanged
updated
partially invalidated
requires query reinterpretation
inconsistent
```

This is not a Reality primitive.

It captures the fact that `what is held fixed` is itself scoped to the current altered structure.

---

# 35. Protected structure classes

Preservation should distinguish:

```text
protected because query role requires it
protected because domain semantics requires it
protected only by default
protected only until explicitly targeted
```

A later surgery can legitimately override the last two categories under explicit query semantics.

---

# 36. No hidden precedence hierarchy

WDF2-F rejects a universal order such as:

```text
law > rule > mechanism > policy > value
```

for conflict resolution.

These layers are not one metaphysical stack, and cross-domain mappings differ.

If two surgeries conflict, resolution must come from:

```text
explicit temporal order
query role
operation semantics
model/domain constraints
```

or remain invalid/underdetermined.

---

# PART X — NESTED COUNTERFACTUALS

# 37. Surface nesting

A query can have form:

```text
If A had occurred, then if B occurred, would C?
```

This is not automatically identical to:

```text
If A and B had occurred, would C?
```

because the inner conditional may be evaluated relative to an A-altered anchor/background rather than the factual anchor.

---

# 38. Nested anchor scope

At least three interpretations exist.

## Sequential same-branch continuation

```text
F0 --A--> F1 --B--> F2
```

The B surgery is interpreted against F1.

## Re-evaluated nested supposition

The inner counterfactual can recompute relevant alternatives around an A-world/result rather than simply mutate one selected A-world.

## Cross-world import

A value generated under one branch can be imported into another branch.

This is the strongest and most assumption-heavy form.

### Earned firewall F-NEST-1

```text
NestedCounterfactual has an AnchorScope parameter.
```

---

# 39. Dynamic treatment-regime pressure

Complex nested potential outcomes arise in dynamic treatment regimes and path-specific effects.

The potential-outcome calculus literature explicitly notes that standard do-calculus is not sufficient for arbitrary complex nested counterfactuals and develops additional machinery for them.

This supports treating nesting as real additional structure rather than syntactic sugar.

---

# PART XI — CROSS-WORLD SUBSTITUTION

# 40. Mediation archetype

A familiar nested quantity has form:

```text
Y_{a, M_{a'}}
```

Interpretation:

```text
evaluate outcome under treatment a
while mediator is set to the value it would have taken under a'
```

This combines material from two counterfactual branches.

It is not the same as an ordinary single-world compound intervention:

```text
do(A=a, M=m)
```

because m is branch-generated:

```text
m = M_{a'}
```

---

# 41. Earned firewall F-XW-1

```text
CrossWorldValueImport
!= SameWorldJointIntervention
```

The imported value requires:

```text
cross-branch subject correspondence
variable identity
coupling/structural assumptions
nested evaluation semantics
```

---

# 42. Cross-world assumptions are substantive

Natural/path-specific effects can require assumptions linking variables across incompatible treatment worlds.

Interventionist mediation research explicitly develops alternative formulations through separable treatment components that avoid direct reference to nested cross-world counterfactuals, while showing close relations under stronger structural-model assumptions except in recanting-witness settings.

WDF2-F therefore does not ban cross-world quantities.

It requires them to be explicitly typed as stronger objects than single-world interventions.

---

# 43. Recanting witness pressure

A treatment-induced variable can lie on pathways that need incompatible treatment assignments for a desired path-specific decomposition.

This creates recanting-witness problems.

The foundational lesson is:

```text
one factual/counterfactual variable token cannot always coherently satisfy two branch-specific parentage requirements at once.
```

### Earned firewall F-RECANT-1

```text
PathSpecificComposition can fail because branch requirements are mutually incompatible.
```

This failure should not be disguised as ordinary estimation noise.

---

# 44. Cross-world import is not necessarily physical intervention

A nested counterfactual quantity can be mathematically meaningful under a structural model even when no physical intervention can literally set a mediator to “the value it would have had under another world.”

Therefore:

```text
CrossWorldCounterfactualQuantity
!= PhysicallyExecutableIntervention
```

WDF2-D's actionability firewall remains binding.

---

# PART XII — INTERVENTIONIST ALTERNATIVES TO CROSS-WORLD NESTING

# 45. Separable components

An interventionist approach can replace one treatment A with components:

```text
A_Y
A_M
```

intended to affect different mechanisms/pathways.

Then one can ask single-world interventions on the components rather than directly importing M_{a'} into an a-world.

This can improve manipulation clarity.

---

# 46. But decomposition itself needs grounding

The treatment decomposition:

```text
A -> (A_Y,A_M)
```

is additional model/domain structure.

It cannot be assumed merely to avoid cross-world language.

### Earned firewall F-SEP-1

```text
AvoidingNestedCounterfactualSyntax
!= EliminatingStructuralAssumptions
```

The assumptions move to component separability and mechanism structure.

---

# PART XIII — PROBABILITY AND COUPLING UNDER SEQUENTIAL SURGERY

# 47. Shared randomness across a chain

For individualized counterfactual trajectories, one must decide how latent/noise variables correspond through multiple surgeries.

Possible policies:

```text
same exogenous background across entire branch
stepwise resampling
shared seed only while mechanism identity persists
branch-specific coupling after mechanism change
```

These are not equivalent.

---

# 48. Mechanism change can invalidate same-noise coupling

If provider/model changes:

```text
M -> M'
```

then a latent noise variable U_M may have no natural one-to-one counterpart in M'.

Therefore a sequence:

```text
change prompt
then change provider
```

can invalidate a coupling that was meaningful for the prompt-only counterfactual.

### Earned firewall F-COUPLE-1

```text
CouplingValidity must be re-audited after mechanism/model surgery.
```

---

# 49. Counterfactual influence over long trajectories

Recent MDP work shows that counterfactual trajectories may lose dependence on the factual trajectory over time and become effectively interventional.

WDF2-F interprets this as a composition problem too:

```text
sequential transitions can erode the correspondence constraint that made the first step individualized.
```

Thus identity/coupling obligations must persist across a chain, not only at the initial surgery.

---

# 50. Policy intervention and stochastic adaptation

Under changed policy π', future actions are functions/distributions of counterfactual history.

The probability law over trajectories is therefore generated recursively.

A fixed list of per-time action interventions can fail to represent the policy counterfactual because it removes feedback.

---

# PART XIV — MODEL REVISION MID-CHAIN

# 51. Model revision as surgery boundary

Sequence:

```text
Δ1 changes model structure M -> M'
Δ2 was authored against M
```

Before applying Δ2, one needs a mapping:

```text
Map_{M->M'}(target(Δ2))
```

Possible outcomes:

```text
unique mapped target
multiple candidates
no target
changed target type
```

---

# 52. Cross-model surgery transport

A surgery can be transported across model revision only if correspondence is sufficient.

### Earned firewall F-TRANSPORT-1

```text
SurgeryValidInM
!= SurgeryTransportableToM'
```

This mirrors causal transportability structurally but is not itself the same statistical problem.

---

# 53. Coarse/fine model composition

Suppose M_micro is abstracted to M_macro.

A micro intervention may not correspond to one unique macro intervention, and a macro intervention may have many micro realizations.

Compositional-abstraction research explicitly studies transformations between interventional causal models and treats compositionality of model transformations as a nontrivial formal desideratum.

This independently supports the need for explicit cross-model composition mappings.

---

# 54. Model revision can be triggered by the first surgery

Path-dependent systems can enter a structural state not represented by the factual model.

Then the first counterfactual step may force:

```text
ModelRevisionRequired
```

before the second surgery is even interpretable.

Sequential counterfactual evaluation must allow this branch outcome.

---

# PART XV — MULTI-AGENT / MULTI-ACTOR COMPOSITION

# 55. One Actor action changes others' future policies

In multi-agent systems:

```text
Agent A changes action
-> environment changes
-> Agent B observes new state
-> B changes action
-> later A reacts
```

This is not captured by holding every other agent's factual action sequence fixed unless that is explicitly the query.

---

# 56. Propagation channel typing

Recent multi-agent counterfactual effect-decomposition work separates effects propagating through later agents' actions from effects propagating through environment state transitions.

WDF2-F uses the structural lesson:

```text
AgentBehaviorPropagation
!= EnvironmentTransitionPropagation
```

even if both contribute to one total outcome difference.

---

# 57. Policy-fixed vs action-fixed others

A multi-agent counterfactual must distinguish:

```text
hold other agents' realized factual actions fixed
```

from:

```text
hold their policies fixed and let their actions adapt to the altered history
```

These produce different branches.

### Earned firewall F-MA-1

```text
OtherAgentsPolicyFixed != OtherAgentsActionsFixed
```

---

# PART XVI — COMPOUND SURGERY VALIDITY

# 58. Pairwise compatibility is not enough

Three surgeries can have:

```text
Δ1 compatible with Δ2
Δ2 compatible with Δ3
Δ1 compatible with Δ3
```

while the triple is inconsistent due to a higher-order constraint.

Example:

```text
three configuration changes each individually valid pairwise
but together exceed a resource/invariant constraint
```

Therefore:

```text
PairwiseComposable
!= JointlyComposable
```

---

# 59. Compound-admissibility object

A research compound surgery needs:

```text
AlterationSet / Sequence
Target loci
Temporal/order relation
Reference-state policy
Conflict rules
Preservation transition rule
Correspondence transition rule
Coupling transition rule
Model revision/transport rule
```

No production object is authorized.

---

# 60. Explicit ordering forms

At least:

```text
Parallel/Simultaneous
TotalSequence
PartialOrder
ConditionalPolicy
NestedBranch
CrossWorldImport
```

are semantically distinct composition forms.

### Earned firewall F-ORDER-1

```text
CompoundAntecedent != OneUniversalOrderedList
```

Some surgeries are intentionally simultaneous; some only partially ordered; some adaptive.

---

# PART XVII — ROBUSTNESS LIFTED THROUGH COMPOSITION

# 61. Composition-plan family

WDF2-E quantified over admissible generators.

WDF2-F adds possible admissible composition plans:

```text
P ∈ Plans(F,Q)
```

where P determines:

```text
order
reference-state semantics
preservation transitions
cross-world imports
```

---

# 62. Robust consequence now has another axis

Schematic strong result:

```text
∀G ∈ A
∀P ∈ Plans_G
∀a ∈ Alt_{G,P}
  C(a)
```

is stronger than robustness over generators alone.

### Earned firewall F-ROB-1

```text
GeneratorRobust != CompositionRobust
```

A conclusion can be invariant across models but sensitive to surgery order.

---

# 63. Do not average surgery orders

If two composition plans are semantically admissible but represent qualitatively different sequences, averaging their outputs by default repeats WDF2-E's model-mixture error.

Preserve the plan family unless a justified decision/epistemic weighting exists.

---

# PART XVIII — MATCHED COMPOSITION MATRIX

# 64. Compact matrix

| Pair | Same components? | Main varied coordinate | Result |
|---|---:|---|---|
| hard X, hard Z | yes | order | can commute under fixed-model/disjoint conditions |
| X shift, Z shift | yes | factual vs recursive natural-value reference | can differ |
| action token, policy | superficially | alteration grain | not equivalent |
| mechanism + value | yes | order / target replacement | can fail to commute |
| credential + rule | yes | constitutive semantics | order may change target meaning |
| config + code patch | yes | target survival | later surgery may become ill-typed |
| node state + network edge | yes | structural relation | order can change parent set |
| prompt + provider | yes | mechanism/coupling | same-noise correspondence can fail |
| policy + future actions | same intention | adaptive vs fixed sequence | not equivalent |
| nested A then B vs A&B | similar surface | anchor scope | not generally equivalent |
| Y_{a,M_{a'}} vs do(a,m) | target-like | cross-world import | fundamentally different object |
| rule reform + new status | yes | model vocabulary | may require model revision |

---

# PART XIX — DELETION TESTS

# 65. Treat all compound alterations as an unordered set

**FAIL**.

Policy, mechanism, rule, network and model-change cases are order-sensitive.

---

# 66. Require all surgeries to be sequential

**FAIL**.

Some joint hard interventions are naturally simultaneous; forcing an arbitrary order adds semantics not present in the query.

---

# 67. Assume commutativity

**FAIL**.

Mechanism/value, rule/status, policy/history and network/state falsifiers defeat it.

---

# 68. Assume noncommutativity always

**FAIL**.

Disjoint hard interventions in a stable fixed model can normalize to the same compound surgery.

---

# 69. Assume global idempotence

**FAIL**.

Incremental, time-indexed and policy-duration surgeries are not idempotent.

---

# 70. Keep preservation static across the chain

**FAIL**.

Structural/mechanism/rule/model changes invalidate old preservation commitments.

---

# 71. Keep identity mapping static

**FAIL**.

Constitutive/model changes can remove or redefine the subject/target.

---

# 72. Keep coupling static

**FAIL**.

Mechanism/provider/model changes can destroy meaningful shared-noise correspondence.

---

# 73. Reduce policy change to fixed action sequence

**FAIL**.

Adaptive policy behavior depends on counterfactual history.

---

# 74. Treat nested counterfactual as conjunction of antecedents

**FAIL**.

Nested anchor scope and cross-world import can differ.

---

# 75. Treat cross-world mediation quantity as ordinary do-intervention

**FAIL**.

Y_{a,M_{a'}} imports a branch-specific mediator value.

---

# 76. Ban all cross-world quantities because they are not direct interventions

**FAIL** as research grammar.

They can be well-defined under stronger structural assumptions and are central to mediation/path-specific questions.

---

# 77. Require a point composition plan

**FAIL**.

WDF2-E underdetermination can apply to surgery order/reference/coupling as well as generator choice.

---

# PART XX — CONDITIONAL SURGERY LAWS

# 78. Surviving local laws

WDF2-F does not yield one universal algebra.

It yields conditional laws of the form:

```text
If surgery family = fixed-model hard assignment
and targets disjoint
and reference states independent
and model/correspondence stable
then commutativity may hold.
```

Likewise:

```text
If operation = exact same hard assignment at same locus/time
then idempotence may hold.
```

This is a major methodological result.

### Earned firewall F-LAW-1

```text
CounterfactualCompositionLaws are typed and conditional.
```

---

# 79. Why no universal algebra is a positive result

A universal algebra would have to collapse:

```text
state assignment
mechanism surgery
policy transformation
constitutive reform
model revision
cross-world substitution
```

into one operation family.

WDF2-A already rejected that collapse.

WDF2-F confirms composition inherits the same typing.

---

# PART XXI — STRUCTURAL RECONSTRUCTION

# 80. Counterfactual transformation trace

The minimal research reconstruction is now closer to:

```text
F0
 --Δ1 / provenance1-->
F1
 --Δ2 / provenance2-->
F2
 ...
```

with each transition recording:

```text
surgery type
order relation
reference-state rule
preservation transition
identity/correspondence transition
coupling transition
model transition
```

---

# 81. Parallel surgery branch

For simultaneous alterations:

```text
Compound(F,{Δ1,Δ2,...})
```

must first test joint compatibility rather than serializing silently.

---

# 82. Nested branch

For nested semantics:

```text
Evaluate(F0,A)
-> family of A-frames
then evaluate B relative to declared anchor scope
```

This may produce multiple branches even before stochasticity.

---

# 83. Cross-world stitching branch

For objects such as:

```text
Y_{a,M_{a'}}
```

an explicit stitch operation is conceptually needed:

```text
Generate M under branch a'
Correspond mediator token/value
Import into branch a
Evaluate Y
```

The stitch carries stronger coherence assumptions than ordinary sequential surgery.

---

# PART XXII — STRONGEST NEW RESULT: COMPOSITION IS A PARTIAL, TYPED OPERATION

# 84. Not every surgery pair has a composition

The most important result can be written:

```text
Compose(Δ2,Δ1 | F)
```

is a **partial typed relation/operator**.

Possible outputs:

```text
one composed transition
several admissible compositions
simultaneous compound surgery
nested branch family
cross-world stitched query
Conflict
TargetUndefined
CorrespondenceRequired
ModelRevisionRequired
```

### Strong firewall F-COMP-1

```text
CounterfactualComposition != TotalFunction
```

---

# 85. This blocks a common engineering metaphor

A tempting implementation analogy is:

```text
counterfactual = patch stack
```

WDF2-F rejects that as universal foundation.

Some counterfactuals resemble patches.
Others alter the patch language itself, the object identity, the future policy, or import values across branches.

---

# PART XXIII — STRONGEST NEW RESULT: PRESERVATION IS DYNAMIC

# 86. Duality becomes temporal

WDF2-A/B established:

```text
Alteration ↔ Preservation
```

WDF2-F strengthens this:

```text
At each transition i:
  Δ_i constrains P_i
  and produces a frame requiring P_{i+1} revalidation.
```

Thus preservation is not one global static set attached to the original query.

---

# 87. Dynamic invariance

A sequential query can preserve:

```text
mechanism f through step 1
```

then explicitly alter f at step 2,
then preserve f' through later steps.

This is coherent.

A static preservation list cannot represent it.

---

# PART XXIV — STRONGEST NEW RESULT: CROSS-WORLD STITCHING IS A DISTINCT OPERATION

# 88. Why nested mediation matters beyond causation research

The structure:

```text
value generated in branch B
used as intervention input in branch A
```

can appear outside biological mediation too.

Examples:

```text
Use the credential Actor would have earned under policy P'
inside the world where institution rule K is unchanged.

Use the model state that provider M' would have produced
inside a continuation executed by provider M.
```

These are structurally cross-world objects.

They require explicit coherence conditions.

---

# 89. This creates the next residual

WDF2-F can type cross-world stitching, but does not yet answer:

```text
When are values/entities from two incompatible branches jointly coherent?
Which cross-world equalities are licensed?
When can a branch-generated value be imported without contradiction?
What consistency axioms follow from one shared structural model?
What happens when several individually coherent nested quantities are jointly inconsistent?
How should impossible or model-revised branches participate?
```

This is now the largest unresolved foundation problem.

---

# PART XXV — EXTERNAL RESEARCH PRESSURE

# 90. Multiple shift interventions

Sani, Lee and Shpitser distinguish shifts defined relative to natural factual values from recursively policy-defined shifts under multiple manipulated variables.

Foundational pressure:

```text
same local transformation formula
+ different reference-state semantics
= different compound intervention
```

---

# 91. Policy interventions

Hızlı and collaborators model treatment policies jointly with outcomes and emphasize that interventions on a policy differ from fixing future treatment sequences because treatments can depend stochastically on previous treatment effectiveness/history.

Foundational pressure:

```text
adaptive policy composition is recursive.
```

---

# 92. Nested/path-specific counterfactuals

Malinsky, Shpitser and Richardson develop a potential-outcomes calculus because complex nested counterfactuals/path-specific effects and dynamic treatment regimes exceed what ordinary do-calculus alone expresses.

Foundational pressure:

```text
NestedCounterfactual != OrdinaryDoQuery syntax sugar
```

---

# 93. Interventionist mediation

Robins, Richardson and Shpitser develop mediation via separable treatment components, avoiding direct nested cross-world counterfactuals while showing close relationships under structural-model assumptions and highlighting recanting-witness boundaries.

Foundational pressure:

```text
cross-world semantics and interventionist decompositions are distinct architectures with different assumptions.
```

---

# 94. Path-dependent structure

Srinivasan, Lee, Bhattacharya and Shpitser introduce path-dependent structural equation models specifically because interventions can alter later structural states and causal relationships.

Foundational pressure:

```text
PreserveOneStaticCausalStructureThroughSequence
```

is not universal.

---

# 95. Network interventions

Sherman and Shpitser study interventions that create/sever network ties rather than changing ordinary variables.

Foundational pressure:

```text
relation/topology surgery is a genuine structural alteration family.
```

---

# 96. Multi-agent propagation

Triantafyllou and collaborators decompose counterfactual effects in multi-agent sequential decision making into propagation through future agents' actions and through state transitions.

Foundational pressure:

```text
hold other agents' policies fixed
```

is different from:

```text
hold their realized actions fixed.
```

---

# 97. Compositional intervention learning

Yu and collaborators explicitly study sequential compositions of intervention labels and impose structural assumptions on how intervention effects compose.

Foundational pressure:

```text
Generalization to unseen intervention combinations requires composition assumptions;
composition is not free.
```

---

# 98. Interventional model abstraction

Rischel and Weichwald formalize compositional transformations between interventional causal models and abstraction errors.

Foundational pressure:

```text
model transformation composition itself needs explicit mappings and error/accountability structure.
```

---

# PART XXVI — WDF0 / WDF1 REOPEN AUDIT

# 99. WDF0

No FoundationReopenCondition fires.

WDF2-F reinforces:

```text
WithinModelUpdate != StructuralModelRevision
IdentifierEquality != OntologicalIdentity
ParticularModelStructure != Reality
Cause != Constitution
PhysicalToken != InstitutionalStatus
```

The need for cross-model correspondence and constitutive-rule retyping is exactly what WDF0's anti-collapse discipline predicted.

WDF0 remains frozen.

---

# 100. WDF1

No FoundationReopenCondition fires.

WDF1's typed modal grammar never required one static alternative generator or one fixed domain through a nested query.

WDF2-F extends the open counterfactual interface without falsifying:

```text
ActionOccurrence != Intervention
CurrentAlternativeDomain != CompleteRealityModalDomain
ModelModalProjection != RealityModalTruth
```

WDF1 remains frozen.

---

# PART XXVII — RESIDUAL RANKING

# 101. Residuals after WDF2-F

```text
1. Cross-world coherence / consistency / compatibility               CRITICAL
2. Nested-branch identity and counterpart coherence                  CRITICAL
3. Cross-world coupling constraints and impossible combinations      CRITICAL
4. Multi-model / model-revision coherence across nested chains        CRITICAL
5. Mediation/path-specific counterfactual consistency                 HIGH/CRITICAL
6. Robust quantification over generator × composition-plan families   HIGH/CRITICAL
7. Counterfactual modal logic for nested would/might                  HIGH
8. Temporal/history persistence and backtracking across long chains   HIGH
9. Prevention/omission/preemption bridge to causal architecture       HIGH
10. Law/chance/powers grounding under structural composition          HIGH
```

The first residual is now upstream.

WDF2-F can say **how** branches/surgeries are composed and when targets/preservation must be revalidated.

It cannot yet say which cross-branch combinations are jointly coherent.

---

# 102. Why coherence is now the next problem

Consider:

```text
M_{a'}
```

and:

```text
Y_{a,M_{a'}}
```

The syntax tells us to import one branch-generated value into another branch.

But the deeper questions are:

```text
Does M refer to the same variable/entity across both branches?
Can the imported value coexist with the receiving branch's structural equations?
Which exogenous background is shared?
Which structural equations are allowed to differ?
Can two cross-world statements be jointly true even if each is individually satisfiable?
What consistency follows from recursive structural substitution?
```

These are not merely composition-order questions.

They are **coherence constraints over families of counterfactual worlds/branches**.

---

# 103. Exact next round

The next canonical round is therefore:

# **WDF2-G — Counterfactual Cross-World Coherence / Consistency / Compatibility**

WDF2-G should test:

```text
consistency axioms such as factual consistency/composition under typed conditions
joint satisfiability of nested counterfactual assignments
cross-world equality/correspondence assumptions
shared-exogenous-background constraints
branch-specific mechanism changes
recanting-witness / incompatible path assignments
counterfactual contradiction vs model-revision failure
cross-model nested correspondence
impossible-world participation in nested queries
robustness over multiple coherent cross-world completions
```

It must not assume the strongest NPSEM-style cross-world independence/identity conditions by default.

Only WDF2-G residuals may determine WDF2-H.

---

# 104. Production disposition

No production changes are admitted.

Do **not** add:

```text
SurgeryStack
CounterfactualTransaction
NestedCounterfactual AST
CrossWorldValueRef
CompositionPlanner
PreservationRevalidator
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

Counterfactual Foundations are not frozen yet.

---

# 105. Closeout

```text
WDF2-F: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D/E reopen: NO
Production refactor: NO

MultipleAlterations != UnorderedSetOfAssignments
SequentialSurgery != SimultaneousSurgery
SomeHardInterventionsCommute != SurgeriesCommuteUniversally
SequentialOverwrite != SimultaneousConflictResolution
PolicyIntervention != FixedActionSequence
PostSurgeryPreservation != PreSurgeryPreservation by default
IndividuallyAdmissibleSurgeries != JointlyComposableSurgeries
NestedCounterfactual != CompoundAntecedent by definition
CrossWorldValueImport != SameWorldJointIntervention
CounterfactualComposition != TotalFunction
GeneratorRobust != CompositionRobust

Exact next round:
WDF2-G — Counterfactual Cross-World Coherence / Consistency / Compatibility
```

Compressed result:

> **WDF2-F finds that counterfactual composition is a partial, typed transformation problem rather than a universal patch algebra. Under narrow fixed-model conditions, disjoint hard interventions can commute and identical assignments can be idempotent; these local laws fail as soon as surgeries depend on natural values, policies, mechanisms, constitutive rules, network structure, model revision or adaptive history. Sequential surgery therefore evolves the counterfactual frame itself: preservation, target identity, correspondence and coupling may need revalidation after every structural step. Policy changes are recursive generators of future actions, not fixed action sequences; path-dependent systems can enter new causal structures; individually admissible alterations need not be jointly composable. Nested counterfactuals introduce a further distinction between sequential same-branch continuation and genuine cross-world substitution such as Y_{a,M_{a'}}, where a value generated in one branch is imported into another. That operation is stronger than an ordinary joint intervention and can fail through incompatible branch requirements such as recanting-witness structures. WDF2 can now type these composition forms, but the largest remaining gap is cross-world coherence itself: which branch-generated values, identities, mechanisms and background assignments are jointly compatible, and which consistency laws are genuinely earned rather than assumed.**
