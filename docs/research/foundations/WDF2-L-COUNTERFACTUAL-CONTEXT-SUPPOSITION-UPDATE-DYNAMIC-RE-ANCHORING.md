# WDF2-L — Counterfactual Context / Supposition / Update / Dynamic Re-Anchoring

Status: **complete for WDF2-L**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D/E/F/G/H/I/J/K remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-L residuals:

```text
WDF2-M — Counterfactual Normality / Typicality / Defaults / Norms
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-K established that counterfactual inference is frame-indexed and that many apparent rule failures are really frame transformations: anchor shift, route shift, realization mismatch, intervention augmentation, vacuity, content-equivalence failure or quantifier-order change.

WDF2-L asks the upstream dynamic question:

> **What happens to the interpretive/informational context when an agent or discourse participant counterfactually supposes A, and how does that transformation govern later nested suppositions without collapsing counterfactual supposition into observation, belief revision, physical-world update or intervention?**

The round compares:

```text
static truth conditions + pragmatic context shift
dynamic/update semantics
premise/background revision
Ramsey-test / belief-revision accounts
belief update accounts
contextualist hybrids
inquisitive/information-state update
causal intervention/backtracking
multi-agent/common-ground dynamics
```

No family is preselected as universal.

---

# 2. First anti-collapse law — context is not one object

At least the following must remain distinguishable:

```text
Reality / WorldState
ModelState
InformationState
BeliefState / CredalState
PremiseBackground
CommonGround / PublicDiscourseState
ModalDomain / ContextRestriction
Similarity/RelevanceOrdering
Normality/DefaultStructure
DiscourseSalience
SemanticAssignment / ReferenceContext
SuppositionalLocalContext
QueryRole / Perspective
```

### Earned firewall L-CONTEXT-1

```text
Context != WorldState != ModelState != BeliefState != CommonGround
```

The word `context` is therefore insufficient without a typed projection.

---

# 3. Dynamic-semantics pressure

Dynamic semantics treats meanings as transformations of information/context states rather than only static truth conditions.

For counterfactuals, Veltman's 2005 `Making Counterfactual Assumptions` explicitly supplies an update semantics and gives a dynamic twist to premise semantics.

This establishes a serious rival architecture:

```text
meaning of a counterfactual antecedent/conditional
can include a context-change potential
```

rather than merely a function from a fixed world to a truth value.

---

# 4. But dynamicity is not forced by order effects alone

von Fintel and Gillies use dynamic context interaction to explain Sobel/reverse-Sobel order effects.

Moss develops a pragmatic account preserving more static/classical counterfactual truth conditions.

Karen Lewis develops a contextualist account centered on conversational relevance and argues that both pure dynamic and pure pragmatic approaches face difficulties.

### Earned firewall L-EVID-1

```text
SequenceOrderEffect != ProofOfSemanticDynamicity
```

Observed discourse dynamics underdetermine whether the dynamics live in truth conditions, pragmatics, contextual restriction, or a hybrid.

---

# PART I — SUPPOSITION AS A DISTINCT OPERATION

# 5. Minimal suppositional transform

Research schematically:

```text
S --Suppose_cf(A)--> S_A
```

where `S` is not Reality itself but a typed evaluation/information context.

---

# 6. Supposing A is not asserting A

A counterfactual speaker can say:

```text
Suppose the server had failed yesterday...
```

without asserting or believing that the server failed.

### Earned firewall L-SUPP-1

```text
CounterfactualSupposition != AssertionOfAntecedent
```

---

# 7. Supposing A is not observing A

Observation normally provides evidence about actuality.

Counterfactual supposition intentionally allows nonactual or impossible antecedents.

### Earned firewall L-SUPP-2

```text
CounterfactualSupposition != ObservationUpdate
```

---

# 8. Supposing A is not intervention by definition

The supposition may be realized by:

```text
forward intervention
backtracking/background change
premise revision
rule revision
law revision
impossible-domain extension
```

depending on WDF2-A→H typing.

### Earned firewall L-SUPP-3

```text
CounterfactualSupposition != Intervention
```

---

# 9. Supposing A is not categorical belief revision

The evaluator can temporarily entertain A while retaining the categorical belief that `not A` actually occurred.

### Earned firewall L-SUPP-4

```text
SuppositionAcceptance(A) != CategoricalBelief(A)
```

---

# PART II — COUNTERFACTUAL SUPPOSITION CAN WITHDRAW CERTAINTIES

# 10. 2026 dynamic-supposition result

Berto and Rafiee Rad's 2026 `Dynamics of Counterfactual Supposition I` develops a qualitative dynamic logic of counterfactual supposition using belief-dynamics techniques.

A crucial result emphasized in the paper is that counterfactual supposition, unlike their indicative-mood supposition, can make the supposing agent lose certainties.

---

# 11. Foundational consequence

A state can contain:

```text
certainty P
```

while:

```text
Suppose_cf(NOT P)
```

must locally suspend/replace P rather than preserve every certainty.

### Earned firewall L-CERT-1

```text
CounterfactualSupposition != MonotonicExpansionOfBeliefs
```

---

# 12. Supposition success is scoped

Within the counterfactual local state one can require:

```text
A accepted-as-supposed
```

without requiring:

```text
A becomes categorically believed outside the scope.
```

### Earned firewall L-SUCCESS-1

```text
SuppositionalSuccess != GlobalBeliefSuccess
```

---

# PART III — RAMSEY TEST PRESSURE

# 13. Classical Ramsey-test intuition

Gärdenfors formulates the familiar idea:

```text
Accept “if A, C” in belief state K
iff
minimal revision of K needed to accept A also accepts C.
```

This makes counterfactual acceptance intimately related to hypothetical belief change.

---

# 14. The relationship is not a simple identity

Gärdenfors's work also generated famous incompatibility/triviality pressures when conditionals, revision and closure principles are combined too strongly.

Later work reconstructs variants rather than showing that every Ramsey-test approach is impossible.

### Earned firewall L-RT-1

```text
RamseyTestConnection != CounterfactualSuppositionIsOrdinaryAGMRevision
```

---

# 15. Modern recovery

Berto/Rafiee Rad prove a Ramsey Test for their dynamic logic:

```text
one believes A > C
iff
one comes to believe C upon counterfactually supposing A
```

within their formal system.

This is evidence that a dynamic supposition architecture can recover Ramsey-style structure without identifying every supposition with categorical revision.

---

# PART IV — REVISION VS UPDATE

# 16. AGM-style revision

The classic revision problem is broadly:

```text
current beliefs concern one static world
new information conflicts with some beliefs
revise minimally to accept new information
```

---

# 17. KM-style update

Katsuno/Mendelzon distinguish `update` from revision by targeting cases in which the world itself may have changed.

This traditional distinction remains useful as a falsifier.

---

# 18. Counterfactual supposition is neither by default

A counterfactual supposition need not claim:

```text
A is newly learned about the actual static world
```

or:

```text
the actual world changed so that A became true.
```

It may instead create a hypothetical local evaluation branch.

### Earned firewall L-RU-1

```text
BeliefRevision != BeliefUpdate != CounterfactualSupposition
```

---

# 19. Formal resemblance does not prove semantic identity

A counterfactual dynamic can satisfy axioms borrowed from belief-update theory while still representing hypothetical reasoning rather than physical-world change.

### Earned firewall L-RU-2

```text
SharedUpdatePostulates != SameUpdateInterpretation
```

---

# PART V — PREMISE/BACKGROUND DYNAMICS

# 20. Premise semantics view

A counterfactual can be treated as temporarily adding the antecedent while revising a background premise set enough to restore an appropriate coherent supposition.

The crucial object is then not merely a world but a selected/revised premise base.

---

# 21. Premise background is not belief state

Some premises can be methodological/modeling assumptions rather than things an agent categorically believes.

### Earned firewall L-PREM-1

```text
PremiseBackground != CategoricalBeliefSet
```

---

# 22. Background retention is selective

Supposing A can require abandoning:

```text
facts incompatible with A
rules explicitly revised by A
model assumptions falsified by A
```

while retaining other structure.

This is the dynamic version of WDF2-A/F preservation typing.

---

# 23. Dynamic preservation

Research transformation:

```text
P_{i+1}
=
RevalidatePreservation(P_i, Supposition_i, Context_i)
```

Supposition therefore changes not only a candidate world but also the list of facts/rules that count as live background.

---

# PART VI — INFORMATION STATE

# 24. Information-state update

A context can be represented as a set/family of live possibilities compatible with currently accepted information.

Ordinary informative assertion often removes incompatible possibilities.

---

# 25. Counterfactual expansion pressure

If A conflicts with all currently live possibilities, counterfactual supposition cannot merely intersect the information state with A.

That would produce the empty set.

It must permit some form of:

```text
revision
expansion beyond current live domain
alternative generation
background relaxation
```

### Earned firewall L-INFO-1

```text
CounterfactualUpdate != SimpleInformationFiltering
```

---

# 26. Information loss can be rational

Because the antecedent may conflict with current certainty/background, the local counterfactual state can contain less categorical information than the original state.

This matches the Berto/Rafiee Rad pressure.

---

# PART VII — COMMON GROUND

# 27. Public discourse state

Speaker and hearer can mutually recognize:

```text
we are now considering A counterfactually
```

without adding A as an actual-world commitment to common ground.

---

# 28. Public supposition vs public assertion

### Earned firewall L-CG-1

```text
PubliclySharedSupposition(A) != CommonGroundCommitmentThatAIsActual
```

---

# 29. Private belief can diverge

Two agents can share the same public counterfactual supposition while retaining different private beliefs, causal models or background assumptions.

### Earned firewall L-CG-2

```text
SharedSupposition != SharedPrivateEvaluationState
```

---

# PART VIII — CONTEXT RESTRICTION / MODAL DOMAIN

# 30. Dynamic strict accounts

von Fintel/Gillies-style approaches allow counterfactual discourse to modify the contextually relevant modal domain/restriction.

This can explain why the order of Sobel-style statements affects later felicity/interpretation.

---

# 31. Domain expansion

A more specific counterfactual can introduce possibilities not previously in the active context restriction.

A later broader antecedent can then be interpreted against the expanded domain.

---

# 32. Static alternative

Moss-style pragmatic accounts preserve static semantic values and explain the order effect through norms of assertion/epistemic responsibility rather than semantic domain update.

### Earned firewall L-DYN-1

```text
ContextChangeInDiscourse != SemanticValueMustBeDynamic
```

---

# 33. Contextualist hybrid

Karen Lewis's work shows another possible architecture where conversational relevance/context affects the semantic evaluation of counterfactuals while discourse effects can be partly pragmatic.

This blocks a simple binary:

```text
dynamic semantics OR pragmatics
```

---

# PART IX — RELEVANCE / SALIENCE UPDATE

# 34. Supposition can make new differences relevant

Before A is entertained, feature F can be irrelevant.

After A, F can become central because A opens a mechanism/path where F matters.

### Earned firewall L-REL-1

```text
RelevanceBeforeSupposition != RelevanceAfterSupposition by default
```

---

# 35. Salience is not relevance

A discourse move can make an alternative salient without making it causally/constitutively relevant.

### Earned firewall L-SAL-1

```text
SalienceUpdate != RelevanceUpdate
```

---

# 36. Relevance can change semantic selection

If a counterfactual evaluator uses contextually relevant dimensions to order alternatives, updating relevance changes later selection without changing Reality or the causal model.

---

# PART X — NORMALITY / DEFAULT UPDATE

# 37. Supposition can challenge defaults

Supposing an abnormal event can locally require treating that event as given while leaving uncertain which other defaults survive.

Example:

```text
Suppose the normally reliable server failed...
```

The local context should not reject the supposition merely because failure is abnormal.

---

# 38. Given abnormality vs normalized branch

Once A is supposed, two different policies are possible:

```text
continue to treat A as abnormal but fixed
```

or:

```text
renormalize relative to the A-worlds so A is no longer a ranking penalty inside the local branch
```

### Earned firewall L-NORM-1

```text
SupposeAbnormalA != OneUniqueNormalityUpdate
```

---

# 39. This component remains under-grounded

WDF2-A→L repeatedly use:

```text
normality
default
typicality
expectation
```

as optional structures, but no round has yet separated their descriptive, statistical, causal, normative and conventional senses.

This becomes the largest residual.

---

# PART XI — LOCAL CONTEXTS AND NESTING

# 40. Nested counterfactual

```text
A □→ (B □→ C)
```

requires an answer to:

```text
What is the context in which B is interpreted?
```

---

# 41. Inherit policy

```text
S_A = Suppose(A,S)
Evaluate B in S_A
```

A's local assumptions/background remain live unless B revises them.

---

# 42. Reset policy

```text
Evaluate B again from original S
```

The inner conditional does not inherit A's contextual effects.

---

# 43. Selective inheritance

Possible hybrid:

```text
inherit A's branch/model facts
reset discourse salience
recompute normality
retain identity mapping
```

or other typed projections.

---

# 44. Branch policy

A local supposition can create a branch-specific context object:

```text
S
 └─ A -> S_A
       └─ B -> S_AB
```

without modifying the base context S.

---

# 45. Cross-world import policy

The inner query can import a value from another branch rather than continue the same local context.

WDF2-F/G remain binding.

---

# 46. Strong firewall

```text
NestedContextInheritance != OneUniversalPolicy
```

---

# PART XII — DYNAMIC RE-ANCHORING

# 47. Reality anchor vs suppositional anchor

After supposing A, subsequent evaluation can be anchored to:

```text
actual world/history
A-branch state
revised premise base
contextually selected A-domain
cross-world imported state
```

These are distinct.

---

# 48. Anchor is not common ground

A semantic evaluation can re-anchor to A-worlds while the discourse common ground still records that A is contrary to fact.

### Earned firewall L-ANCHOR-1

```text
EvaluationAnchor != PublicActualityCommitment
```

---

# 49. Re-anchoring can explain inference drift

WDF2-K transitivity/import-export failures can now be restated dynamically:

```text
second premise is evaluated after a different context transform than the intermediate state generated by the first premise.
```

---

# PART XIII — UPDATE COMPOSITION

# 50. Sequential update

Define schematically:

```text
U_B(U_A(S))
```

---

# 51. Noncommutativity

Sobel/reverse-Sobel phenomena and premise/context revision give strong pressure that:

```text
U_B(U_A(S)) != U_A(U_B(S))
```

in general.

### Earned firewall L-COMP-1

```text
CounterfactualContextUpdates are not universally commutative.
```

---

# 52. Joint supposition differs

```text
U_{A AND B}(S)
```

need not equal:

```text
U_B(U_A(S))
```

because joint A∧B can realize a different surgery/premise combination than sequential supposition.

### Earned firewall L-COMP-2

```text
SequentialSupposition != JointSupposition by default
```

---

# 53. Idempotence is typed

In some update systems:

```text
U_A(U_A(S)) = U_A(S)
```

once A is already accepted in the local state.

But repeated mention can alter:

```text
salience
normality framing
route emphasis
discourse commitment
```

without changing A's truth-condition component.

### Earned firewall L-IDEM-1

```text
TruthConditionalIdempotence != FullContextIdempotence
```

---

# 54. Associativity is not automatic

Grouping sequential suppositions can alter scope and which context components are inherited.

Therefore:

```text
U_C(U_B(U_A(S)))
```

requires explicit scope/stack semantics.

---

# PART XIV — SCOPE AND ROLLBACK

# 55. Temporary local supposition

A counterfactual thought experiment is often bracketed:

```text
enter supposition A
reason locally
exit supposition
```

The base categorical beliefs need not become A-beliefs.

---

# 56. Semantic rollback

At scope exit:

```text
BaseBeliefState_after
can equal
BaseBeliefState_before
```

while the agent has learned a higher-order conditional/result.

### Earned firewall L-ROLL-1

```text
ExitSupposition != ForgetCounterfactualResult
```

---

# 57. Discourse residue

Even if local assumptions are rolled back, the discourse can retain:

```text
newly salient alternatives
agreed terminology
identified mechanism
counterfactual conclusion
```

### Earned firewall L-ROLL-2

```text
LocalAssumptionRollback != TotalContextRollback
```

---

# PART XV — STATIC VS DYNAMIC REPRESENTATIONAL EQUIVALENCE

# 58. Same verdict, different mechanism

A static similarity semantics plus pragmatic context model and a dynamic update semantics can agree on all tested counterfactual verdicts in some domain.

---

# 59. Semantic mechanism remains underdetermined

### Earned firewall L-EQUIV-1

```text
VerdictEquivalence != DynamicMechanismEquivalence
```

Data sufficient to predict answers may not identify where context change is represented.

---

# 60. Query-local quotienting

If the research target needs only verdicts under a restricted domain, static/dynamic differences can be abstracted away locally.

But foundation claims about update architecture require stronger evidence.

---

# PART XVI — OBSERVATION, REVISION, UPDATE, SUPPOSITION, INTERVENTION MATRIX

# 61. Observation

Typical role:

```text
learn evidence about actuality
filter/reweight factual hypotheses
```

---

# 62. Belief revision

Typical role:

```text
change categorical beliefs about one static target world
```

---

# 63. Belief update

Typical role:

```text
change beliefs when the target world may itself have evolved/changed
```

---

# 64. Counterfactual supposition

Typical role:

```text
temporarily construct/revise a hypothetical evaluation state
without categorical actuality commitment
```

---

# 65. Intervention

Typical role:

```text
modify a causal/mechanistic model or branch realization
```

---

# 66. Premise revision

Typical role:

```text
alter the background assumptions used for hypothetical evaluation
```

---

# 67. Accommodation

Typical role:

```text
adjust discourse/common-ground/relevance structures needed to interpret an utterance
```

---

# 68. Matrix firewall

```text
Observation
!= Revision
!= WorldUpdate
!= Supposition
!= Intervention
!= PremiseRevision
!= Accommodation
```

They can compose, but composition is not identity.

---

# PART XVII — AGENT-ERA PRESSURE

# 69. LLM context window is not semantic context

An Agent/LLM can have:

```text
token context window
hidden state
retrieved memory
public conversation state
world model
counterfactual local branch
```

These must not be collapsed.

### Earned firewall L-AGENT-1

```text
ModelContextWindow != CounterfactualSemanticContext
```

---

# 70. Same prompt, different discourse history

The same textual counterfactual prompt can rationally produce different interpretations after different prior discussions because:

```text
referents
preservation assumptions
salient mechanisms
query role
```

have changed.

This is not automatically model inconsistency.

---

# 71. Hypothetical tool output

Suppose:

```text
“If tool T had returned r...”
```

This must not write r into factual memory as an observed tool result.

### Earned firewall L-AGENT-2

```text
HypotheticalToolResult != ObservedToolResult
```

---

# 72. Counterfactual sandboxing

Agent systems therefore benefit conceptually from separating:

```text
actual evidence state
counterfactual local reasoning state
```

but WDF2-L does not admit production implementation.

---

# 73. Same action token, different local context

An Agent can reason:

```text
if I had called T after failure F...
```

and:

```text
if I had called T before F...
```

with the same action token but different context/anchor.

---

# PART XVIII — MULTI-AGENT / MULTI-SPEAKER CONTEXT

# 74. Shared factual model, different context

Two agents can agree on:

```text
causal graph
factual observations
antecedent A
```

and still disagree on A□→C because they differ in:

```text
preservation assumptions
normality
relevance
supposition update policy
```

---

# 75. Different verdict does not imply factual disagreement

### Earned firewall L-MA-1

```text
CounterfactualDisagreement != FactualModelDisagreement by default
```

---

# 76. Public alignment can be partial

Agents may negotiate:

```text
“hold the policy fixed”
“do not backtrack”
“treat either tool route separately”
```

thereby aligning selected context dimensions without sharing all private state.

---

# 77. Context synchronization is typed

Possible alignment dimensions:

```text
AnchorAgreement
PremiseAgreement
RouteAgreement
NormalityAgreement
GeneratorAgreement
RelevanceAgreement
```

No single `same context` Boolean is sufficient.

---

# PART XIX — CONTEXT-UPDATE UNDERDETERMINATION

# 78. Multiple admissible update policies

For the same A and base state S, several update policies can survive:

```text
U1 = premise revision
U2 = dynamic modal-domain expansion
U3 = causal backtracking
U4 = interventionist realization
```

for different query roles or even under unresolved semantics.

---

# 79. WDF2-E robustness lifts again

Let:

```text
U in AdmissibleContextUpdates(A,S,Q)
```

Then a context-robust consequence can require:

```text
for all U, C holds after U(A,S)
```

### Earned firewall L-ROB-1

```text
ContextUpdateRobust != GeneratorRobust != CompletionRobust
```

---

# 80. Do not average context-update policies by default

Different update policies are semantic/model alternatives, not automatically probabilistic events.

WDF2-E mixture firewall remains binding.

---

# PART XX — CONTEXT SUCCESS / CONSISTENCY

# 81. Ordinary antecedent

A successful supposition state should normally make A locally accepted/realized at the declared content grain.

---

# 82. Impossible antecedent

WDF2-H allows:

```text
vacuous strict semantics
impossible-world/domain extension
NoAdmissibleAlternative
ModelRevisionRequired
```

Therefore `success` cannot universally mean ordinary classical consistency.

---

# 83. Local consistency vs base consistency

The base state can remain categorically consistent while a paraconsistent/impossible local context is entertained.

### Earned firewall L-CONS-1

```text
SuppositionalLocalConsistency != BaseBeliefConsistency
```

---

# PART XXI — CONTEXTUAL PARAMETERS MAY CHANGE AT DIFFERENT SPEEDS

# 84. Information state

Can update immediately on assertion/observation.

---

# 85. Relevance/salience

Can change after one discourse move.

---

# 86. Normality/default structure

May be more persistent or may locally renormalize under a supposition.

---

# 87. Model/generator commitments

May require explicit revision rather than ordinary discourse accommodation.

---

# 88. Identity/semantic scheme

Usually stable unless antecedent explicitly revises it.

### Earned firewall L-RATE-1

```text
ContextUpdate != UniformReplacementOfAllContextDimensions
```

---

# PART XXII — SOBEL / REVERSE-SOBEL RECONSTRUCTION

# 89. Ordinary Sobel sequence

A broad counterfactual can be followed by a more specific exception:

```text
If A, C.
But if A and B, not C.
```

often felicitously.

---

# 90. Reverse sequence

Specific exception first, then broad claim, often sounds degraded:

```text
If A and B, not C.
# But if A, C.
```

---

# 91. Dynamic explanation

First utterance expands/changes the relevant A-domain so later broad claim must reckon with A∧B cases.

---

# 92. Pragmatic explanation

Later broad utterance can be semantically consistent but conversationally irresponsible given a salient exception the speaker cannot rule out.

---

# 93. Contextualist explanation

Conversational relevance/salience affects which worlds count as relevant for semantic evaluation.

### Strong result

```text
One behavioral datum supports several context architectures.
```

---

# PART XXIII — TEMPORAL RE-ANCHORING

# 94. Historical scope

Supposition can set an anchor time:

```text
If A had happened at t...
```

then later B can be interpreted relative to:

```text
state at t
post-A state at t+1
actual present
```

---

# 95. Temporal context is not causal order by itself

```text
B mentioned later
```

does not mean B is causally downstream.

### Earned firewall L-TIME-1

```text
DiscourseOrder != TemporalOrder != CausalOrder
```

---

# PART XXIV — STATIC TRUTH VS DYNAMIC ACCEPTANCE

# 96. A counterfactual can have one static truth value

while its assertability/acceptability changes as context changes.

---

# 97. Dynamic semantics can encode change compositionally

instead of attributing it to pragmatics.

---

# 98. Foundation position

WDF2-L does not collapse:

```text
Truth
Acceptability
Felicity
ContextChangePotential
```

### Earned firewall L-TAC-1

```text
CounterfactualTruth != CounterfactualFelicity != ContextUpdateEffect
```

---

# PART XXV — DELETION TESTS

# 99. Treat context as one opaque bag

**FAIL**.

Belief, common ground, relevance, normality, modal domain and anchor change independently.

---

# 100. Treat supposition as assertion

**FAIL**.

Counterfactual antecedents need not be actuality commitments.

---

# 101. Treat supposition as observation

**FAIL**.

Nonactual/impossible antecedents are central.

---

# 102. Treat supposition as intervention

**FAIL** through backtracking, premise, rule and model-revision cases.

---

# 103. Treat supposition as AGM revision universally

**FAIL**.

Temporary/local supposition, public discourse and physical-world update require different roles.

---

# 104. Treat supposition as KM world update universally

**FAIL**.

Counterfactual local branches do not assert actual-world change.

---

# 105. Simple information intersection

**FAIL** when antecedent contradicts current certainties/live worlds.

---

# 106. Preserve all certainties

**FAIL** under counterfactual supposition of their negations; 2026 dynamic-supposition work directly pressures this.

---

# 107. Semantic dynamicity from reverse Sobel alone

**FAIL** because static/pragmatic and hybrid accounts exist.

---

# 108. Static semantics always sufficient

**FAIL** as a universal claim because mature update-semantics architectures capture context transformation compositionally and may explain additional patterns.

---

# 109. One nested inheritance policy

**FAIL** across continuation/reset/selective/cross-world readings.

---

# 110. Universal commutativity

**FAIL** due sequence/order effects and background revision.

---

# 111. Universal full-context idempotence

**FAIL** because repeated suppositions can alter salience/context even if truth-conditional content is stable.

---

# 112. Full rollback

**FAIL** because local assumptions can disappear while learned conditional results/discourse salience remain.

---

# 113. Same public supposition implies same private state

**FAIL** in multi-agent discourse.

---

# 114. Average context-update policies

**FAIL** without probability interpretation.

---

# PART XXVI — STRONG RESULTS

# 115. Strong result — counterfactual supposition is a scoped hypothetical state transition

The strongest general form is not:

```text
believe A
```

or:

```text
do A
```

but:

```text
construct/update a local evaluation state in which A is admitted according to typed realization semantics.
```

---

# 116. Strong result — context dynamics is multi-channel

A supposition can transform:

```text
information
premises
modal domain
relevance
normality
anchor
```

without changing all channels.

---

# 117. Strong result — dynamic semantics vs pragmatics is an architectural underdetermination

The same order-sensitive discourse evidence can often be represented at several levels.

The correct foundation therefore records **where** an update is claimed to occur.

---

# 118. Strong result — nested counterfactuals require context inheritance semantics

WDF2-F's anchor scope is now extended:

```text
AnchorScope
+
ContextInheritancePolicy
```

The inner counterfactual cannot be interpreted from syntax alone.

---

# 119. Strong result — temporary local acceptance and categorical belief are orthogonal

An agent can be certain `not A` categorically and still reason coherently in a local A-supposition.

This is not irrational inconsistency.

---

# 120. Strong result — robustness acquires a context-update axis

A conclusion can be:

```text
model robust
but context-policy sensitive
```

or vice versa.

---

# PART XXVII — EXTERNAL RESEARCH PRESSURE

# 121. Veltman 2005

`Making Counterfactual Assumptions` explicitly constructs an update semantics for counterfactuals by dynamically reconstructing premise semantics.

Foundational pressure:

```text
counterfactual meaning can be modeled as context transformation.
```

---

# 122. von Fintel 2001 / Gillies 2007

Dynamic-context / scorekeeping approaches explain Sobel-style ordering phenomena by allowing counterfactual discourse to alter the contextually relevant modal restriction.

Foundational pressure:

```text
sequence effects can arise from counterfactual context change.
```

---

# 123. Moss 2010/2012

Moss argues that reverse-Sobel judgments can be explained pragmatically without abandoning standard counterfactual semantics.

Foundational pressure:

```text
order effects do not uniquely identify semantic update.
```

---

# 124. Karen Lewis 2018

`Counterfactual Discourse in Context` argues that both dynamic-semantic and purely pragmatic approaches have shortcomings and develops a contextualist account emphasizing conversational relevance.

Foundational pressure:

```text
context-to-semantics and discourse-to-context relations can be split across semantic/pragmatic layers.
```

---

# 125. Gärdenfors 1986

The Ramsey test connects conditional acceptance to minimal hypothetical belief revision while exposing compatibility/triviality pressures for overly strong belief-revision formulations.

Foundational pressure:

```text
belief-change structure is deeply relevant but not a free identity theorem for counterfactual semantics.
```

---

# 126. AGM 1985

The AGM tradition supplies a mature theory of contraction/revision under rationality postulates.

Foundational pressure:

```text
background belief change has algebraic structure that can be compared with supposition dynamics.
```

---

# 127. Katsuno/Mendelzon

Their revision/update distinction separates incorporating information about a static world from accommodating world change.

Foundational pressure:

```text
not every state transition called “update” represents the same kind of change.
```

---

# 128. Berto/Rafiee Rad 2026

`Dynamics of Counterfactual Supposition I`, published online as an accepted manuscript in July 2026, gives a dynamic logic of qualitative counterfactual supposition, recaptures belief-update-style axioms, proves a Ramsey Test, and highlights that counterfactual supposition can make an agent lose certainties.

Foundational pressure:

```text
counterfactual supposition is a first-class dynamic operation distinct from simple monotonic hypothetical addition.
```

---

# PART XXVIII — WDF0 / WDF1 REOPEN AUDIT

# 129. WDF0

No FoundationReopenCondition fires.

WDF2-L reinforces:

```text
Reality != Belief != Model != Representation
Relative != Subjective
WithinModelUpdate != StructuralModelRevision
Action != Authority
```

Context dynamics belongs to epistemic/representational access and typed relations, not a new Reality root.

WDF0 remains frozen.

---

# 130. WDF1

No FoundationReopenCondition fires.

WDF1 already requires explicit:

```text
anchor
dependence/background
alternative generator
operator
model provenance
```

WDF2-L adds a dynamic account of how those parameters can change under nested supposition without falsifying the modal grammar.

WDF1 remains frozen.

---

# PART XXIX — RECONSTRUCTION

# 131. Suppositional context contract

Research-only:

```text
SuppositionContext =
  ActualityCommitments
  LocalHypotheticalCommitments
  PremiseBackground
  InformationState
  ModalRestriction
  Relevance/SalienceState
  Normality/DefaultState
  Anchor/Time
  Model/GeneratorCommitments
  Identity/ReferenceState
  Public/PrivateScope
  QueryRole
```

Not every query requires every field.

---

# 132. Supposition transition

Research-only:

```text
Suppose(A,S,Policy)
  -> S'
```

with possible effects:

```text
add local A commitment
withdraw incompatible local background
expand modal domain
change relevance/salience
re-anchor
migrate preservation
retain base actuality commitment
```

---

# 133. Transition result statuses

```text
LocalContextConstructed
ContextExpanded
PremiseRevisionRequired
ModelRevisionRequired
AlternativeDomainExtensionRequired
NoAdmissibleSupposition
MultipleAdmissibleUpdatePolicies
```

---

# 134. Nested transition

```text
S0 --A--> S1 --B--> S2
```

requires explicit:

```text
which projections of S1 B inherits
which projections reset to S0
which are recalculated
```

---

# 135. Robust result

For admissible update policies U:

```text
ContextRobust(C)
:= for all U, C holds in U(A,S)
```

This is an additional WDF2-E robustness axis.

---

# PART XXX — LARGEST REMAINING RESIDUAL

# 136. Why normality/default structure becomes upstream

WDF2-L can now separate:

```text
information
belief
premise background
relevance
context restriction
supposition scope
```

But nearly every serious update architecture still needs a principle for questions such as:

```text
Which incompatible beliefs should be withdrawn first?
Which A-realizations are normal enough to remain relevant?
Which abnormalities should be held fixed after A is supposed?
Which exception should defeat a default?
Which alternative is ordinary/typical vs deviant?
```

---

# 137. “Normality” has been used without foundation

Across WDF2-A→L the term has appeared as:

```text
normality ordering
usual/default background
typical behavior
prescriptive/normative expectations
causal normality
contextual relevance prior
```

These are not obviously the same structure.

---

# 138. Statistical vs normative pressure

A behavior can be:

```text
statistically rare but normatively required
statistically common but prohibited
causally default but institutionally deviant
```

Therefore:

```text
Typical != Permitted != Expected != Default
```

must be tested directly.

---

# 139. Partial ordering pressure

Halpern's extended causal models explicitly allow normality orderings to be partial rather than total.

This is important because two deviations can be incomparable rather than artificially ranked.

---

# 140. Context dependence pressure

Normality can depend on:

```text
domain
institution
historical period
query role
causal model
social/normative context
```

without becoming subjective whim.

---

# 141. Counterfactual selection pressure

Fazelpour's work asks why norms should influence counterfactual selection at all rather than simply assuming that they do.

This is precisely the grounding question WDF2 has postponed.

---

# 142. Bridge-to-causation pressure

Normality/defaults become especially important once WDF2 eventually enters:

```text
actual causation
prevention
omission
responsibility
```

Halpern/Hitchcock-style causal models formally use normality/typicality to rank witnesses and causal judgments.

Counterfactual Foundations therefore should type this structure before using it downstream.

---

# 143. Exact next round

The next canonical round is therefore:

# **WDF2-M — Counterfactual Normality / Typicality / Defaults / Norms**

WDF2-M should separate and stress-test:

```text
statistical typicality
frequency
expectation / prediction
causal/mechanistic default
model default
conventional default
institutional norm
moral/legal norm
baseline/reference value
normality ordering
plausibility ordering
similarity ordering
salience
relevance
```

and ask:

```text
which of these should constrain counterfactual alternative selection?
how are partial/incomparable orderings represented?
when does supposing an abnormal A renormalize the local context?
can norms affect selection without becoming causes?
how do descriptive and prescriptive normality interact?
how robust are conclusions across admissible normality structures?
```

It must not preselect Halpern/Hitchcock normality orderings, probabilistic typicality, social norms, Lewisian similarity or KLM plausibility as one universal primitive.

Only WDF2-M residuals may determine WDF2-N.

---

# 144. Production disposition

No production changes are admitted.

Do **not** add:

```text
SuppositionContext
ContextStack
CounterfactualSandbox
ContextUpdatePolicy
DynamicAnchor
CommonGroundState
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

Counterfactual Foundations remain open.

---

# 145. Closeout

```text
WDF2-L: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D/E/F/G/H/I/J/K reopen: NO
Production refactor: NO

Context != WorldState != ModelState != BeliefState != CommonGround
SequenceOrderEffect != ProofOfSemanticDynamicity
CounterfactualSupposition != Assertion
CounterfactualSupposition != ObservationUpdate
CounterfactualSupposition != Intervention
SuppositionAcceptance != CategoricalBelief
CounterfactualSupposition != MonotonicExpansionOfBeliefs
SuppositionalSuccess != GlobalBeliefSuccess
RamseyTestConnection != OrdinaryAGMRevisionIdentity
BeliefRevision != BeliefUpdate != CounterfactualSupposition
SharedUpdatePostulates != SameUpdateInterpretation
PremiseBackground != CategoricalBeliefSet
CounterfactualUpdate != SimpleInformationFiltering
PublicSupposition != ActualityCommonGroundCommitment
SharedSupposition != SharedPrivateEvaluationState
ContextChangeInDiscourse != SemanticValueMustBeDynamic
RelevanceBeforeSupposition != RelevanceAfterSupposition
SalienceUpdate != RelevanceUpdate
SupposeAbnormalA != OneUniqueNormalityUpdate
NestedContextInheritance != OneUniversalPolicy
EvaluationAnchor != PublicActualityCommitment
CounterfactualContextUpdates are not universally commutative
SequentialSupposition != JointSupposition
TruthConditionalIdempotence != FullContextIdempotence
ExitSupposition != ForgetCounterfactualResult
LocalAssumptionRollback != TotalContextRollback
VerdictEquivalence != DynamicMechanismEquivalence
Observation != Revision != WorldUpdate != Supposition != Intervention != PremiseRevision != Accommodation
ModelContextWindow != CounterfactualSemanticContext
HypotheticalToolResult != ObservedToolResult
CounterfactualDisagreement != FactualModelDisagreement
ContextUpdateRobust != GeneratorRobust != CompletionRobust
SuppositionalLocalConsistency != BaseBeliefConsistency
ContextUpdate != UniformReplacementOfAllContextDimensions
DiscourseOrder != TemporalOrder != CausalOrder
CounterfactualTruth != CounterfactualFelicity != ContextUpdateEffect

Exact next round:
WDF2-M — Counterfactual Normality / Typicality / Defaults / Norms
```

Compressed result:

> **WDF2-L establishes that counterfactual supposition is best treated at foundation stage as a scoped hypothetical state transition, not as assertion, observation, categorical belief revision, physical-world update or intervention by definition. The relevant “context” is itself typed: information state, categorical beliefs, premise background, common ground, modal restriction, relevance/salience, normality/default ordering, semantic reference, model/generator commitments and local anchor can change independently. Veltman's update semantics and von Fintel/Gillies scorekeeping show mature dynamic architectures in which counterfactual discourse transforms context, while Moss and Karen Lewis show that Sobel/reverse-Sobel order effects do not uniquely force semantic dynamicity; static/pragmatic and hybrid contextualist explanations remain live. Gärdenfors's Ramsey Test and modern Berto/Rafiee Rad dynamics show a deep link between counterfactual acceptance and hypothetical belief change, but counterfactual supposition is not ordinary AGM revision: it can be temporary, locally successful without global belief change, and—according to the 2026 dynamic logic—can make an agent lose certainties. Nested counterfactuals therefore require an explicit context-inheritance policy: inner suppositions may inherit, reset, selectively inherit or cross-world-import from outer contexts. Sequential suppositions are not generally commutative and need not equal joint conjunction; local assumption rollback does not erase learned counterfactual conclusions or discourse salience. Multi-agent systems add another separation between public supposition and private evaluation state, and robustness must now quantify over admissible context-update policies as another uncertainty axis. The largest remaining gap is the structure repeatedly used to decide what is retained, ordinary, deviant or preferred during these updates: normality/default/typicality. WDF2 has not yet distinguished statistical frequency, predictive expectation, causal default, conventional baseline, institutional/legal/moral norm or plausibility ordering. That unresolved structure now becomes the next foundation round.**
