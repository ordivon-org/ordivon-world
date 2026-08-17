# WDF2-I — Counterfactual Hyperintensionality / Relevance / Antecedent Individuation

Status: **complete for WDF2-I**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C/D/E/F/G/H remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-I residuals:

```text
WDF2-J — Counterfactual Antecedent Composition / Disjunction / Decomposition / Alternative Structure
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-H established that impossible antecedents cannot be handled only through their extension over ordinary possible worlds: every impossible proposition has the same empty possible-world extension, yet scientific, mathematical, institutional and explanatory reasoning distinguishes many impossible suppositions.

WDF2-I therefore asks:

> **What makes two counterfactual antecedents the same or different content for the purposes of counterfactual evaluation, and what makes one feature relevant to the consequent while another feature is merely globally similar, topically related, causally connected, syntactically present, or pragmatically salient?**

The round must answer without presupposing that counterfactual content is:

```text
sentence syntax
possible-world intension
impossible-world extension
structured proposition
truthmaker set
subject matter/topic
causal intervention
mechanism edit
premise set
```

by definition.

---

# 2. First anti-collapse law

At least the following relations must remain distinct:

```text
SyntacticIdentity
ReferentialIdentity
LogicalEquivalence
NecessaryEquivalence / IntensionalEquivalence
PossibleWorldExtensionalEquivalence
ImpossibleWorldExtensionalEquivalence
TruthmakerEquivalence
SubjectMatterEquivalence
StructuredContentEquivalence
Surgery/AlterationEquivalence
QueryLocalCounterfactualEquivalence
DecisionEquivalence
```

### Earned firewall I-ID-1

```text
SameIntension != SameCounterfactualContent by default
```

Fine's 2012 substitution puzzle and the modern hyperintensionality literature provide direct pressure against unrestricted substitution of logical/necessary equivalents inside counterfactual contexts.

---

# 3. Hyperintensionality is substitution failure at a finer grain

A concept/operator H is hyperintensional when:

```text
A and B necessarily equivalent
```

but:

```text
H(A) and H(B)
```

can differ.

The crucial point is not merely that possible-world semantics sometimes gives the wrong answer.

It is that:

```text
NecessaryEquivalence
```

can be too coarse an equivalence relation for the operator/query role.

---

# 4. Fine's counterfactual pressure

Fine's 2012 analysis explicitly argues that a counterfactual puzzle is best addressed by giving up unrestricted substitution for logical equivalents.

WDF2-I therefore treats the following as a live possibility:

```text
A <-> B logically valid
```

while:

```text
(A □→ C)
```

and:

```text
(B □→ C)
```

need not have the same evaluation under every admissible counterfactual semantics.

### Earned firewall I-SUB-1

```text
LogicalEquivalence != CounterfactualSubstitutability
```

---

# 5. Referential transparency is not universal either

Kocurek argues that if counterpossible contexts can exhibit referential opacity, closely related opacity can arise even for ordinary possible-antecedent counterfactuals.

This creates pressure against the universal principle:

```text
If a=b,
then replacing a with b anywhere inside a counterfactual preserves truth.
```

WDF2-I does not conclude that counterfactuals are always referentially opaque.

It concludes:

### Earned firewall I-REF-1

```text
Coreference != UniversalCounterfactualSubstitutability
```

Mode of presentation, supposition structure, query role and antecedent individuation can matter.

---

# PART I — THE GRANULARITY PROBLEM

# 6. Too coarse: possible-world intension

If antecedent content is only:

```text
{ possible worlds where A is true }
```

then:

```text
logically equivalent propositions
necessarily equivalent propositions
all impossible propositions
```

are collapsed at relevant levels.

This cannot represent every substitution-sensitive counterfactual phenomenon.

---

# 7. Too fine: sentence-token identity

At the opposite extreme:

```text
Content(A) = exact syntax/string of A
```

also fails.

Paraphrases, translations, unit conversions and synonymous domain descriptions can express the same intended alteration.

Examples:

```text
Increase temperature by 1°C
Increase temperature by 1 kelvin
```

for a temperature difference.

Or:

```text
set feature_enabled=false
turn feature off
```

under a known software schema.

### Earned firewall I-GRAIN-1

```text
SyntacticDifference != ContentDifference by default
```

---

# 8. Hyperintensional granularity is not one global total order

Contemporary hyperintensionality research emphasizes that different hyperintensional operators can require different degrees and kinds of fine-graining, and the notions need not form one simple total hierarchy.

For Counterfactual Foundations this implies:

```text
one universally finest proposition representation
```

is not earned.

---

# 9. Query-relative grain

A description can be equivalent for one target and non-equivalent for another.

Example:

```text
Patch P1
Patch P2
```

may be equivalent with respect to:

```text
Does crash disappear?
```

while non-equivalent with respect to:

```text
What latency does service exhibit?
```

### Earned firewall I-QGRAIN-1

```text
CounterfactualContentEquivalence can be query-relative.
```

This does not make it subjective; the query criterion is explicit.

---

# PART II — EQUIVALENCE LADDER

# 10. Syntax equivalence

```text
same token/string/tree
```

Useful for provenance, insufficient for semantic identity.

---

# 11. Reference equivalence

```text
same referent/entity
```

Can preserve many extensional claims but can fail to preserve the intended supposition route.

---

# 12. Logical equivalence

```text
A ⊢ B
B ⊢ A
```

under declared logic.

Too coarse for known counterfactual substitution phenomena.

---

# 13. Necessary/intensional equivalence

```text
A and B true at same possible worlds
```

Still too coarse for hyperintensional operators.

---

# 14. Topic/subject-matter equivalence

Two propositions can be about the same issue while making different claims about it.

Example:

```text
server is healthy
server is unhealthy
```

same topic, opposite content.

Thus:

### Earned firewall I-TOPIC-1

```text
SameSubjectMatter != SameProposition
```

---

# 15. Truthmaker equivalence

Two propositions may share the same exact truthmakers under one truthmaker semantics.

This is a strong candidate for some hyperintensional identity questions.

But truthmaker equivalence is representation/ontology dependent and need not coincide with causal/mechanism equivalence.

---

# 16. Surgery equivalence

Two descriptions can resolve to the same typed alteration:

```text
same target
same alteration kind
same temporal scope
same reference state
same model/rule/mechanism effect
```

even if syntactically different.

This is highly valuable for engineering/scientific counterfactuals.

But it cannot be universal because mathematical/logical suppositions may have no intervention-like surgery.

---

# 17. Query-local equivalence

For Q:

```text
A ≡_Q B
```

iff substituting A/B preserves the counterfactual result at Q's required resolution across the declared admissible semantics.

This is an outcome/evaluator equivalence, not necessarily a proposition identity claim.

---

# PART III — IMPOSSIBLE ANTECEDENT DIFFERENTIATION

# 18. Empty extension is not enough

Over ordinary possible worlds:

```text
2+2=5
circle squared by ruler+compass
P and not-P
water is H2O2 under an essentialist reading
```

may all have empty extension.

Yet they require different repair structures and support different relevant consequences.

---

# 19. Impossible worlds as one hyperintensional carrier

Impossible-world semantics can distinguish impossible antecedents by allowing different impossible states/worlds to verify them.

This solves the empty-extension collapse.

But it creates a granularity question:

```text
How fine are impossible worlds?
```

Berto/Jago explicitly treat this as a central hyperintensionality problem.

### Earned firewall I-IW-1

```text
ImpossibleWorldDifferentiation != CorrectGranularity by itself
```

---

# 20. Overfitting pressure

A maximally fine impossible-world semantics can distinguish every syntactic or representational variation.

That risks overfitting content identity:

```text
A
A and A
paraphrase(A)
translation(A)
```

may become needlessly distinct.

WDF2-I therefore requires coarse-graining criteria as well as fine-graining machinery.

---

# PART IV — STRUCTURED PROPOSITIONS

# 21. Structured-content family

Structured proposition approaches preserve constituent/mode-of-combination information beyond world intension.

Strengths:

```text
captures compositional structure
can distinguish logically equivalent formulations
can preserve referential/mode-of-presentation information
```

---

# 22. Structure is not automatically the right structure

Natural-language parse structure can be too fine or linguistically accidental.

Examples:

```text
active/passive paraphrase
translation across languages
different API aliases for same operation
```

can share intended counterfactual content despite distinct syntax trees.

### Earned firewall I-STRUCT-1

```text
LinguisticStructure != CounterfactualStructure by definition
```

---

# 23. Domain-normalized structure

A structured representation becomes more plausible when normalized to domain objects:

```text
entity
relation
operation
rule
mechanism
quantifier
scope
```

rather than raw syntax.

But this normalization already requires ontology/model assumptions and must remain provenance-visible.

---

# PART V — TRUTHMAKER / EXACT-STATE SEMANTICS

# 24. Exact truthmakers

Fine's truthmaker semantics uses partial states rather than complete possible worlds and distinguishes exact truthmakers from states containing irrelevant surplus material.

An exact truthmaker is intended to contain what is wholly relevant for the truth of the proposition, not arbitrary additional facts.

This is directly attractive for WDF2-I.

---

# 25. Exactness separates relevant truth-support from global similarity

Suppose:

```text
Franz is napping
```

A state containing:

```text
Franz napping + unrelated football score
```

is inexact if the score contributes nothing to the truth.

Counterfactual relevance can benefit from the same anti-surplus discipline.

---

# 26. Truthmaker exactness is not causal relevance

A fact can be part of what exactly makes a proposition true without being a cause of another target.

And a background causal mechanism can be relevant to a consequence without being part of the antecedent's exact truthmaker.

### Earned firewall I-EXACT-1

```text
ExactTruthmakingRelevance != CausalRelevance
```

---

# 27. Truthmaker ontology dependence

What counts as a state/part/fusion depends on the truthmaker framework.

WDF2-I therefore treats truthmaker semantics as a powerful rival representation, not a foundation-level proof that one ontology of states is universally fundamental.

---

# 28. 2025 task-semantics pressure

Brast-McKie's 2025 `Counterfactual Worlds` extends Fine-style truthmaker machinery using states, parthood, tasks and times; possible worlds are derived rather than primitive, and the counterfactual semantics is explicitly hyperintensional.

This provides fresh evidence that:

```text
counterfactual semantics can be built around partial/task structure instead of primitive global-world similarity.
```

WDF2-I does not infer uniqueness from this success.

---

# PART VI — SUBJECT MATTER / ABOUTNESS / TOPICS

# 29. Subject matter as an independent semantic factor

Yablo's aboutness program treats subject matter as a factor in meaning not fully determined by truth conditions.

Fine's truthmaker-content work similarly develops subject matter, common content and remainder within a hyperintensional framework.

This is highly relevant to counterfactual antecedent individuation.

---

# 30. Topic-enriched worlds

Berto's 2024 account proposes propositions represented by worlds enriched with topics, partly to retain hyperintensional distinctions without maximal overfitting.

This demonstrates a hybrid possibility:

```text
modal extension
+
subject matter/topic
```

rather than abandoning worlds entirely.

---

# 31. Topic is not sufficient for full counterfactual identity

Two antecedents can be about the same topic but request different alterations:

```text
server CPU load increases
server CPU load decreases
```

Same topic:

```text
CPU load
```

Different counterfactual content.

---

# 32. Topic can distinguish truth-conditionally equivalent content

Two necessary/equivalent claims can concern different subject matters.

Therefore topic can supply hyperintensional discrimination unavailable from possible-world extension alone.

---

# PART VII — MECHANISM / SURGERY STRUCTURE

# 33. Typed alteration as content carrier

WDF2-A through H repeatedly showed that the same surface antecedent can represent:

```text
value change
action change
policy change
mechanism change
rule change
model change
law change
semantic revision
```

Thus typed alteration structure is itself part of counterfactual content.

---

# 34. Same effect != same surgery

Two antecedents can produce identical terminal state yet differ in mechanism.

Example:

```text
restart service
replace service binary
```

both restore availability.

But downstream questions about persistence, latency, security or future failure differ.

### Earned firewall I-SURG-1

```text
SameTerminalState != SameCounterfactualAlteration
```

---

# 35. Same surgery, different wording

Conversely:

```text
disable flag F
set F=false
turn F off
```

can resolve to the same typed surgery under a fixed schema.

### Earned firewall I-SURG-2

```text
DifferentDescription != DifferentSurgery
```

---

# 36. Surgery is insufficient outside intervention-like domains

Counterlogical and mathematical suppositions can concern:

```text
proof rule
axiom
theorem
semantic interpretation
```

without a unique world-state surgery analogue.

Therefore surgery structure is one content layer, not the entire theory of antecedent content.

---

# PART VIII — PREMISE / BACKGROUND STRUCTURE

# 37. Premise semantics

Premise-based counterfactual semantics represents a supposition by adding/revising premises while preserving an appropriate background.

This naturally carries more information than a bare set of antecedent worlds.

---

# 38. Premise identity can be hyperintensional

Logically equivalent premise sets can trigger different revision behavior because they expose different components for retention/deletion.

This is a strength for counterfactual revision.

---

# 39. Premise representation can overfit too

If semantically equivalent paraphrases are stored as different premise atoms, revision can become syntax-sensitive for the wrong reason.

The premise vocabulary therefore also needs principled individuation.

---

# PART IX — RELEVANCE TAXONOMY

# 40. Relevance is not one primitive scalar

WDF2-I distinguishes at least:

```text
TopicalRelevance
TruthmakingRelevance
CausalRelevance
MechanisticRelevance
ConstitutiveRelevance
InferentialRelevance
PreservationRelevance
ExplanatoryRelevance
DecisionRelevance
Pragmatic/CommunicationRelevance
```

### Earned firewall I-REL-1

```text
Relevance != OneUniversalSimilarityWeight
```

---

# 41. Topical relevance

Feature/fact F is topically relevant when it concerns the subject matter at issue.

This does not imply causal influence.

Example:

```text
car color
car engine temperature
```

can both concern the car while only one is causally relevant to overheating.

---

# 42. Causal relevance

F can be causally relevant to target Y through modeled causal dependence/pathways.

This does not imply F is the user's topic.

A hidden cooling controller can be causally relevant even if the question is framed around engine load.

---

# 43. Constitutive relevance

A rule criterion can be relevant to whether an institutional status exists without causing the status in the ordinary physical sense.

### Earned firewall I-CREL-1

```text
ConstitutiveRelevance != CausalRelevance
```

---

# 44. Inferential relevance

A premise can be relevant to a mathematical/logical consequence despite lacking causal relation.

This matters especially for counterlogicals/countermathematicals.

---

# 45. Preservation relevance

Some facts matter because the query requires them held fixed, even if they are not part of antecedent content.

Example:

```text
same software input bytes
```

may be preservation-relevant when comparing two binaries.

---

# 46. Explanatory relevance

A factor can causally affect an outcome but be too specific, derivative or screened-off to be the appropriate explanation at the requested grain.

Thus:

```text
CausallyRelevant != ExplanatorilyRelevant at every grain
```

---

# 47. Decision relevance

Two counterfactual models can disagree on details irrelevant to the action choice.

WDF2-E already separated decision equivalence from counterfactual equivalence.

---

# PART X — RELEVANCE VS SIMILARITY

# 48. Similarity relation

Similarity compares alternatives/worlds/states along one or more dimensions.

```text
Sim(w1,w2)
```

can use:

```text
fact overlap
history overlap
law overlap
metric distance
structural distance
```

---

# 49. Relevance relation

Relevance asks whether a feature/difference bears on:

```text
antecedent realization
consequent evaluation
query role
preservation requirement
subject matter
```

### Earned firewall I-SIM-1

```text
Relevance != Similarity
```

---

# 50. Similarity without relevance

Two alternatives can be globally very similar because they match millions of irrelevant details while differing on one mechanism central to the question.

A global distance can therefore rank the wrong alternative above a less globally similar but structurally relevant one.

---

# 51. Relevance without global similarity

Two systems can be globally different but instantiate the same mechanism under study.

Example:

```text
different hardware, language and deployment
same retry protocol invariant
```

For a protocol-level counterfactual, mechanism relevance can dominate global resemblance.

---

# 52. Similarity can be downstream of relevance

A safer architecture is often:

```text
identify admissible/relevant comparison dimensions
then order alternatives within them
```

rather than:

```text
one global similarity metric first
then infer relevance from closeness
```

### Strong result

```text
RelevanceConstraints can type the similarity dimensions.
```

This does not mean relevance always uniquely determines ordering.

---

# PART XI — RELEVANCE VS ABOUTNESS

# 53. Same topic, irrelevant difference

Suppose Q is about:

```text
network reliability
```

Two differences are both topically within network state:

```text
packet payload color tag
link redundancy
```

but only redundancy may be causally/reliability relevant.

Thus:

```text
TopicalRelevance != TargetDependence
```

---

# 54. Background relevance outside explicit topic

A question about:

```text
Did patch P fix crash?
```

can require preserving:

```text
kernel version
input
resource limit
```

although those are not the linguistic topic of `patch P`.

Topic does not exhaust preservation relevance.

---

# PART XII — RELEVANCE VS MINIMALITY

# 55. Minimal change is not relevance

Changing the fewest variables can preserve an irrelevant representation while altering the wrong mechanism.

WDF2-A/C already rejected Hamming-style minimality as universal.

WDF2-I strengthens:

```text
MinimalDescriptionChange != MinimalRelevantChange
```

---

# 56. Relevant minimality can be useful locally

Once the alteration type, target, protected structure and relevant dimensions are fixed, minimality can act as a soft ordering within an admissible set.

This preserves WDF2-D's hard/soft separation.

---

# PART XIII — SAME SYNTAX, DIFFERENT CONTENT

# 57. Semantic revision

Sentence token:

```text
“Actor is licensed”
```

under K and K' can express different institutional criteria.

Same syntax, different constitutive content.

---

# 58. Software schema revision

Expression:

```text
state = ACTIVE
```

under version V and V' can refer to different state-machine semantics.

---

# 59. Model variable revision

Variable name:

```text
risk_score
```

can be redefined across model versions.

### Earned firewall I-SAME-SYNTAX-1

```text
SameSymbol != SameCounterfactualVariableAcrossModelRevision
```

---

# PART XIV — DIFFERENT SYNTAX, SAME CONTENT

# 60. Unit-normalized physical alteration

```text
increase ΔT by 1°C
increase ΔT by 1 K
```

can be same difference operation.

---

# 61. Software aliases

```text
feature=false
feature=disabled
```

can normalize to one enum/state under schema S.

---

# 62. Institutional paraphrase

Two legally defined phrases can be stipulated synonyms under one rule system.

Counterfactual content identity can survive linguistic difference.

---

# 63. Agent tool alias

Two API surface names can resolve to the same underlying operation and authority scope.

Syntax should not create false counterfactual difference.

---

# PART XV — SAME REFERENT, DIFFERENT SUPPOSITION

# 64. Coreferential description case

If two names/designators are coreferential, a supposition framed through one description can foreground a different role/identity condition than the other.

Kocurek's substitution work provides formal philosophical pressure here.

### Earned firewall I-MODE-1

```text
SameReferent != SameModeOfCounterfactualPresentation
```

---

# 65. Do not overgeneralize opacity

Many ordinary engineering counterfactuals should normalize aliases transparently.

Whether mode of presentation matters is itself typed by:

```text
query role
domain semantics
antecedent content
identity criterion
```

---

# PART XVI — PHYSICAL MATCHED CASES

# 66. Equivalent equation descriptions

A physical law can be represented in mathematically equivalent forms.

If the counterfactual changes only notation:

```text
same physical relation
```

should remain.

If it changes one parameter's causal/nomological role, it is different.

### Earned firewall I-PHYS-1

```text
AlgebraicReexpression != LawRevision
```

---

# 67. Coarse vs fine property

```text
temperature > threshold
```

and exact microstate description can be extensionally aligned in one actual case but support different counterfactual grains.

The coarser antecedent leaves more microstructure open.

---

# PART XVII — MATHEMATICAL MATCHED CASES

# 68. Necessarily false antecedents

```text
2+2=5
Fermat's Last Theorem is false
circle is squared by ruler+compass
```

all lack ordinary possible worlds under standard mathematics but concern distinct structures.

---

# 69. Inferential relevance

For:

```text
If 2+2=5, what follows about parity arithmetic?
```

arithmetical inferential relations are relevant.

For:

```text
would distant weather differ?
```

they may not be.

This relevance cannot be read from empty possible-world extension.

---

# 70. Proof-route sensitivity

Two equivalent theorems can enter a mathematical explanation through different lemmas/proof roles.

Thus:

```text
NecessaryEquivalence != SameExplanatoryRole
```

---

# PART XVIII — SOFTWARE MATCHED CASES

# 71. Same boolean effect, different mechanism

```text
set feature flag false
remove feature code entirely
```

can both yield feature absence now.

But future behavior differs under re-enable/redeploy queries.

---

# 72. Same patch semantics, different textual diff

Refactoring can produce a different diff while preserving behavior and the relevant counterfactual surgery.

Code-text distance is not counterfactual content identity.

---

# 73. Configuration key reuse

Same key name across versions may have different semantics.

WDF2-G/H correspondence and model revision remain mandatory.

---

# PART XIX — INSTITUTIONAL MATCHED CASES

# 74. Same status label, changed criteria

`member` under constitution K and K' may have different rights/obligations.

No automatic identity.

---

# 75. Different legal route, same operational access

Two legal statuses can both grant API access.

For query:

```text
Can Actor call endpoint?
```

they may be query-equivalent.

For query:

```text
What authority does Actor possess?
```

they are not equivalent.

This is a direct query-relative equivalence case.

---

# PART XX — AGENT-ERA MATCHED CASES

# 76. Provider alias vs architecture change

Two provider/model IDs can alias the same deployed model revision.

Conversely, same marketing/model name can resolve to a changed backend revision.

### Earned firewall I-AGENT-1

```text
SameProviderLabel != SameModelMechanism
```

---

# 77. Prompt paraphrase

Two prompts can encode the same task intent but differ in token form.

For semantic task outcome they may be equivalent; for token-level trajectory they are not.

---

# 78. Tool description vs authority object

Different natural-language descriptions can refer to the same exact tool operation/authority object.

The content should normalize to the authority/action semantics when that is the query grain.

---

# 79. Latent-state mode of presentation

A hidden state described as:

```text
same vector bytes
```

vs:

```text
same semantic memory
```

invokes different identity criteria.

WDF2-G grain-relative correspondence remains binding.

---

# PART XXI — CONTENT AS A MULTI-LAYER CONTRACT

# 80. No single carrier survives universally

Deletion/falsification across domains rejects:

```text
syntax only
possible-world intension only
topic only
surgery only
truthmakers only
impossible worlds only
```

as universal complete content theories for all counterfactual roles.

---

# 81. Research-level antecedent content contract

A counterfactual antecedent may require:

```text
SurfaceExpressionProvenance
Reference/EntityResolution
StructuredClaim
SubjectMatter/Topic
TypedAlterationOrFrameworkRevision when applicable
Grain/Projection
Logic/Law/Rule/Model/SemanticFramework
Identity/CorrespondenceCriterion
PreservationImplications
ModeOfPresentation when semantically active
```

This is a diagnostic bundle, not a claim that propositions metaphysically consist of these fields.

---

# 82. Content layer can be sparse

Not every query requires every field.

Example:

```text
simple hard intervention X:=1 in fixed SCM
```

may not need rich mode-of-presentation structure.

Countermathematical queries may not need Actor/action fields.

---

# PART XXII — HYPERINTENSIONAL EQUIVALENCE

# 83. No universal equality predicate earned

Instead of:

```text
SameHyperintensionalContent(A,B)
```

as one global primitive, WDF2-I supports typed relations:

```text
SameReference
SameTopic
SameStructuredClaim
SameSurgery
SameTruthmakerContent
SameFrameworkRevision
EquivalentForQuery(Q)
```

---

# 84. Equivalence proof obligations

Before collapsing A and B, state which dimensions are preserved.

Example:

```text
same surgery
same target grain
same framework
same preservation consequences
```

can justify normalization even when syntax differs.

---

# 85. Over-fine failure

If content representation distinguishes:

```text
A
A AND A
```

for every counterfactual role solely because syntax differs, it likely overfits many ordinary cases.

The contemporary granularity literature explicitly treats this as a problem.

---

# 86. Over-coarse failure

If it identifies all necessarily equivalent antecedents, Fine-style substitution pressure defeats it.

Thus the desired representation must support both:

```text
fine-graining
and
principled quotienting/coarse-graining.
```

---

# PART XXIII — RELEVANCE CONTRACT

# 87. Research diagnostic

For feature/fact/component r:

```text
Relevant(r | A,C,Q,D,F)
```

should be read as a typed question, not one universal Boolean primitive.

Possible relevance role:

```text
topic
truthmaking
causal
mechanistic
constitutive
inferential
preservation
explanatory
decision
pragmatic
```

---

# 88. Relevance can be hard or soft

Hard relevance constraints can determine:

```text
which mechanism/rule must be represented
which identity criterion is admissible
which branch variable must correspond
```

Soft relevance can rank:

```text
which additional detail is useful to report
which equivalent description is cognitively natural
```

---

# 89. Relevance cannot be defined by “whatever makes intuition right”

Circular rule:

```text
r is relevant iff including r yields the intuitive counterfactual verdict
```

is rejected.

---

# 90. Non-circular relevance sources

Relevance can be constrained by independently specified:

```text
query role
target variable/proposition
subject matter
causal/mechanistic paths
constitutive criteria
proof/inferential dependencies
preservation contract
decision objective
```

These can still underdetermine a final ranking.

---

# PART XXIV — TOPICS AND OVERFITTING

# 91. Topics as coarse-graining device

Berto's topic-enriched hyperintensional account is important because it explicitly addresses a challenge opposite to hyperintensionality itself:

```text
how not to distinguish too much.
```

Topic information can group contents that differ in representation but concern the same issue.

---

# 92. Topic equality is not enough

A topic can be very broad:

```text
software deployment
```

while two antecedents alter entirely different mechanisms.

Thus topic is a candidate coarse-graining coordinate, not a complete counterfactual semantics.

---

# PART XXV — TRUTHMAKER RELEVANCE AND EXACTNESS

# 93. Exact truthmaker advantage

Truthmaker semantics has a built-in notion of `wholly relevant to truth`, which can distinguish:

```text
exact state
```

from:

```text
exact state + irrelevant surplus
```

This is attractive for antecedent decomposition.

---

# 94. Exactness can expose alternatives inside a disjunction

A disjunction:

```text
A OR B
```

can have A-truthmakers and B-truthmakers separately rather than only the union of A-worlds and B-worlds.

This will become central in WDF2-J.

---

# 95. Exact truthmaker content is still one rival

Its state ontology and fusion/exactness criteria are substantive.

WDF2-I therefore keeps it as a strong candidate architecture rather than a frozen universal primitive.

---

# PART XXVI — DISJUNCTIVE ANTECEDENT PRESSURE EMERGES

# 96. Hyperintensionality exposes hidden antecedent alternatives

Consider:

```text
If A or B, C
```

A standard Boolean proposition may encode only:

```text
Worlds(A) union Worlds(B)
```

losing which disjunct supplied the antecedent.

But natural counterfactual reasoning often preserves the alternatives separately.

---

# 97. Simplification of Disjunctive Antecedents

A prominent principle is:

```text
(A OR B) □→ C
----------------
A □→ C
B □→ C
```

SDA has generated a long-running challenge for standard minimal-change semantics.

Recent 2026 experimental/acquisition work confirms that the phenomenon remains an active semantic issue rather than a historical footnote.

---

# 98. Classical logical equivalence collides with antecedent structure

Classical logic treats:

```text
A entails A OR B
```

and:

```text
A AND B entails A
```

as ordinary entailments.

But counterfactual inference does not simply validate every corresponding strengthening/simplification pattern.

This shows that antecedent internal structure and alternatives cannot be postponed indefinitely.

---

# 99. Causal-model pressure

Standard causal-model intervention semantics is naturally expressed for conjunctions of atomic assignments.

Briggs and later Rosella/Sprenger extend the framework to complex/disjunctive antecedents using truthmaker/alternative structure; classical logical equivalents cannot simply be substituted freely.

This is direct cross-framework evidence that Boolean antecedent composition is a distinct unresolved problem.

---

# PART XXVII — DELETION TESTS

# 100. Identify counterfactual content with possible-world intension

**FAIL**.

Logical/necessary-equivalent substitution and impossible-antecedent differentiation defeat it.

---

# 101. Identify content with syntax

**FAIL**.

Paraphrase, translation, unit normalization and API aliases generate same-content cases.

---

# 102. Identify content with referent identity

**FAIL** universally.

Mode-of-presentation/substitution cases remain.

---

# 103. Identify content with subject matter/topic

**FAIL**.

Opposite and mechanism-distinct antecedents can share topic.

---

# 104. Identify relevance with similarity

**FAIL**.

Global similarity can privilege irrelevant facts.

---

# 105. Identify relevance with causal relevance

**FAIL**.

Mathematical, constitutive and inferential relevance provide counterexamples.

---

# 106. Identify relevance with topic

**FAIL**.

Same-topic differences can be target-irrelevant.

---

# 107. Identify exact truthmaker relevance with causal relevance

**FAIL**.

Truthmaking and causation are different dependence roles.

---

# 108. Identify surgery with full antecedent content

**FAIL**.

Logical/mathematical/semantic suppositions and mode-of-presentation cases exceed action/intervention structure.

---

# 109. Treat every linguistic difference as hyperintensionally significant

**FAIL** through overfitting.

---

# 110. Treat every necessary equivalence as substitutable

**FAIL** under Fine-style counterfactual hyperintensional pressure.

---

# 111. Force one global finest grain

**FAIL**.

Different query roles and hyperintensional operators support incomparable granularity requirements.

---

# PART XXVIII — EXTERNAL RESEARCH PRESSURE

# 112. SEP hyperintensionality synthesis

The current Stanford Encyclopedia synthesis defines hyperintensionality through failures of substitution of necessarily equivalent contents and emphasizes the general granularity problem: possible-world intensions can be too coarse, while sentence-level structure can be too fine. It also notes that hyperintensional notions need not form one simple total ordering by grain.

Foundational pressure:

```text
no universal content grain is earned.
```

---

# 113. Fine 2012 substitution pressure

Fine's `A Difficulty for the Possible Worlds Analysis of Counterfactuals` argues for rejecting unrestricted substitution of logical equivalents in counterfactual reasoning.

Foundational pressure:

```text
LogicalEquivalence != CounterfactualSubstitutability.
```

---

# 114. Fine truthmaker program

Fine's `Counterfactuals Without Possible Worlds` and later truthmaker-content work replace primitive possible-world semantics with exact states/truthmakers and develop notions such as subject matter, common content and remainder.

Foundational pressure:

```text
partial/exact state structure can carry hyperintensional information hidden by complete-world extensions.
```

---

# 115. Brast-McKie 2025 task semantics

`Counterfactual Worlds` derives worlds using states, parthood, tasks and times, yielding an explicitly hyperintensional counterfactual semantics and extending it to forward/backward/backtracking temporal cases.

Foundational pressure:

```text
global possible-world similarity is not the only mature architecture for counterfactual comparison.
```

---

# 116. Berto/Jago impossible worlds

Their impossible-world program uses impossible alternatives to recover distinctions unavailable at the level of possible-world intension and explicitly recognizes the granularity problem.

Foundational pressure:

```text
finer alternatives solve empty-extension collapse but create a principled coarse-graining problem.
```

---

# 117. Berto 2024 topics

Berto proposes worlds enriched with topics as a hyperintensional proposition representation and directly addresses Williamson-style overfitting concerns.

Foundational pressure:

```text
topic/aboutness can serve as an independent hyperintensional coordinate and coarse-graining constraint.
```

---

# 118. Fine/Yablo subject matter

Yablo treats subject matter as an independent factor in meaning constrained but not determined by truth conditions; Fine develops subject matter/common-content machinery within truthmaker semantics.

Foundational pressure:

```text
truth conditions alone need not determine what a proposition is about.
```

---

# 119. Kocurek substitution of identicals

Kocurek argues that counterfactual substitution opacity is not confined to impossible antecedents if one accepts counterpossibilist opacity.

Foundational pressure:

```text
referential identity alone may underdetermine counterfactual supposition content.
```

---

# 120. Rosella/Sprenger disjunctive causal semantics

Their causal-model extension handles arbitrary Boolean antecedents by preserving truthmaker/submodel alternatives and weighting relevant submodels.

Foundational pressure:

```text
complex antecedent logical form exposes content structure not represented by atomic intervention syntax alone.
```

---

# 121. 2026 SDA acquisition work

Zani, Ciardelli and Sanfelici's 2026 work treats simplification of disjunctive antecedents as an active empirical/semantic puzzle, comparing alternative-based and exhaustification-style explanations.

Foundational pressure:

```text
disjunction's internal alternatives are likely semantically active in counterfactual antecedents.
```

---

# PART XXIX — WDF0 / WDF1 REOPEN AUDIT

# 122. WDF0

No FoundationReopenCondition fires.

WDF2-I reinforces:

```text
IdentifierEquality != OntologicalIdentity
PhysicalPattern != SemanticContent
Same_X != Same_Y without criterion
Relative != Subjective
Representation != Reality
```

Hyperintensional content is a representational/semantic interface problem; no new Reality root is required.

WDF0 remains frozen.

---

# 123. WDF1

No FoundationReopenCondition fires.

WDF1's modal claim grammar already requires alternative specification, relation/generator, dependence/background and model provenance.

WDF2-I refines how antecedent content and alternative individuation are represented without falsifying WDF1.

WDF1 remains frozen.

---

# PART XXX — RECONSTRUCTION

# 124. Antecedent content is typed and multi-resolution

The strongest surviving reconstruction is:

```text
AntecedentContent is not one bare proposition extension.
```

A research evaluator can maintain several projections:

```text
surface/syntax
reference
structured semantic content
topic/subject matter
typed surgery/framework revision
truthmaker/premise support
grain
```

and use only the projections demanded by the query role.

---

# 125. Content equivalence is scoped

Instead of one universal equivalence:

```text
A = B
```

use:

```text
Equivalent(A,B | criterion,query,domain,grain)
```

where criterion is explicit.

### Earned firewall I-EQ-1

```text
HyperintensionalEquivalence != OneContextFreeEqualityRelation
```

---

# 126. Robustness over content individuations

Sometimes two content analyses both survive:

```text
C1(A)
C2(A)
```

If they yield the same target conclusion:

```text
result is content-analysis robust.
```

If not, WDF2-E-style plural output is required.

### Earned firewall I-ROB-1

```text
ContentAnalysisUnderdetermination != SemanticFailure
```

---

# 127. Relevance is typed dependence, not aesthetic closeness

Counterfactual comparison should expose why a dimension/fact is relevant:

```text
because it is part of antecedent realization
because it constitutes target meaning
because it lies on a causal mechanism
because it is inferentially required
because query role preserves it
because it is the declared subject matter
```

This is stronger than `distance weight = 0.7` without semantic provenance.

---

# 128. Similarity remains useful downstream

Once relevant comparison dimensions are fixed, similarity can rank alternatives within them.

Therefore WDF2-I does **not** delete similarity.

It demotes similarity from:

```text
universal relevance oracle
```

to:

```text
one typed ordering instrument.
```

---

# PART XXXI — LARGEST REMAINING RESIDUAL

# 129. Why antecedent logical composition is now upstream

WDF2-I can explain why:

```text
syntax
intension
topic
surgery
```

are different content projections.

But a counterfactual antecedent is often internally structured:

```text
A and B
A or B
not A
(A or B) and C
quantified/conditional descriptions
```

The logical constructors themselves can determine which alternatives/surgeries are exposed.

---

# 130. Disjunction is the sharpest falsifier

For:

```text
If A or B, C
```

a bare Boolean possible-world union loses the distinction between A and B routes.

Yet SDA-style reasoning often treats the two disjunct alternatives separately.

Truthmaker/alternative semantics and causal-model extensions preserve them explicitly.

This is not merely another relevance problem.

It is a **composition problem inside antecedent content**.

---

# 131. Conjunction creates the dual pressure

If one validates simplification from disjunction using ordinary classical entailment principles, one risks validating unrestricted antecedent strengthening:

```text
A □→ C
therefore
A and B □→ C
```

which is famously invalid in general.

Thus ordinary Boolean algebra cannot simply be lifted wholesale into counterfactual antecedent logic.

---

# 132. Negation and decomposition remain open

For:

```text
If not A, C
```

what is altered?

```text
any A-preventing surgery?
one closest ¬A state?
a truthmaker/falsemaker of A?
a premise deletion?
```

WDF2-I does not yet decide.

---

# 133. Alternative decomposition interacts with probability

A disjunctive antecedent can expose several realization routes with different probabilities/distances/causal mechanisms.

Averaging them requires interpretation and weighting provenance.

This interacts directly with WDF2-E's probability/mixture firewall.

---

# 134. Exact next round

The next canonical round is therefore:

# **WDF2-J — Counterfactual Antecedent Composition / Disjunction / Decomposition / Alternative Structure**

WDF2-J should test:

```text
conjunction
ordinary disjunction
exclusive disjunction
negation
nested Boolean structure
Simplification of Disjunctive Antecedents
Strengthening of the Antecedent
substitution of logical equivalents
truthmaker/alternative decomposition
causal-model complex antecedents
probabilistic weighting of disjunct realizations
same-world vs route-specific alternatives
how conjunction composes typed surgeries
how negation generates alteration families
whether antecedent decomposition is semantic or pragmatic
```

It must not preselect truthmaker semantics, alternative semantics, inquisitive semantics or classical Boolean composition as universally correct.

Only WDF2-J residuals may determine WDF2-K.

---

# 135. Production disposition

No production changes are admitted.

Do **not** add:

```text
HyperintensionalContent
TopicGraph
AntecedentNormalizer
RelevanceEngine
TruthmakerState
CounterfactualContentHash
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

Counterfactual Foundations remain open.

---

# 136. Closeout

```text
WDF2-I: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C/D/E/F/G/H reopen: NO
Production refactor: NO

SameIntension != SameCounterfactualContent
LogicalEquivalence != CounterfactualSubstitutability
Coreference != UniversalCounterfactualSubstitutability
SyntacticDifference != ContentDifference
SameSubjectMatter != SameProposition
LinguisticStructure != CounterfactualStructure
ExactTruthmakingRelevance != CausalRelevance
SameTerminalState != SameCounterfactualAlteration
DifferentDescription != DifferentSurgery
Relevance != OneUniversalSimilarityWeight
ConstitutiveRelevance != CausalRelevance
Relevance != Similarity
MinimalDescriptionChange != MinimalRelevantChange
SameSymbol != SameCounterfactualVariableAcrossModelRevision
SameProviderLabel != SameModelMechanism
HyperintensionalEquivalence != OneContextFreeEqualityRelation
ContentAnalysisUnderdetermination != SemanticFailure

Exact next round:
WDF2-J — Counterfactual Antecedent Composition / Disjunction / Decomposition / Alternative Structure
```

Compressed result:

> **WDF2-I establishes that counterfactual antecedent content cannot be identified with syntax, possible-world intension, subject matter, truthmakers, impossible worlds or intervention structure alone. Counterfactual contexts exhibit genuine hyperintensional pressure: logically or necessarily equivalent antecedents need not always substitute, while syntactically different descriptions can normalize to the same domain-level surgery. The correct granularity is therefore neither maximally coarse nor maximally fine and need not form one global hierarchy. Counterfactual content is best treated at foundation stage as a multi-resolution contract exposing reference, structured claim, topic, typed alteration/framework revision, grain, model/rule/law semantics, preservation implications and—where needed—mode of presentation. Equivalence is criterion- and query-relative rather than one universal hyperintensional equality. Relevance must likewise be typed: topical, truthmaking, causal, mechanistic, constitutive, inferential, preservation, explanatory and decision relevance are distinct, and none is reducible to a single global similarity metric. Similarity remains useful only after relevant dimensions have been justified. Fine-style exact truthmaker semantics, topic/aboutness accounts, impossible worlds, structured propositions and mechanism/premise semantics each solve different parts of the problem but fail universal deletion tests. The strongest new residual appears inside antecedents themselves: disjunction, conjunction and negation expose alternative structure that bare Boolean possible-world extensions often erase. The long-standing Simplification of Disjunctive Antecedents problem, modern truthmaker/causal-model extensions, and current 2026 semantic evidence all show that logical form is not a superficial wrapper around an already individuated antecedent. WDF2 therefore advances next to antecedent composition, disjunction, decomposition and alternative structure.**
