# WDF2-C — Counterfactual Alternative Generation / Selection Architectures

Status: **complete for WDF2-C**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A and WDF2-B remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-C residuals:

```text
WDF2-D — Counterfactual Generator Grounding / Admissibility / Query-Role Separation
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-A established that a counterfactual is not generic possibility or generic intervention. WDF2-B then showed that a valid counterfactual frame requires at least:

```text
Anchor
+ typed Alteration
+ compatible PreservationProfile
+ Identity/Correspondence
+ AlternativeGeneration/Selection
+ ModalForce
+ TruthRole/ModelProvenance
+ Probability/Coupling when relevant
```

and further showed that these coordinates are constrained rather than independent.

WDF2-C asks the next irreducible question:

> **Once alteration, preservation and correspondence are sufficiently typed, how are the alternatives relevant to `would`, `might`, diagnostic, causal, probabilistic or counterpossible evaluation generated, ordered, selected, tied, weighted or left plural?**

The round compares the major candidate architectures against the WDF2-B falsifier suite.

It does **not** assume that all named traditions are direct rivals. Indeed, one of the strongest findings of this round is that several supposedly competing accounts occupy different architectural layers and therefore cannot be fairly compared as if each were a complete replacement for the others.

---

# 2. WDF2-B inherited falsifier suite

A candidate architecture is tested against at least the following requirements.

```text
F1  typed alteration locus
F2  explicit preservation semantics
F3  alteration/preservation compatibility
F4  domain-scoped identity/correspondence
F5  plural alternatives / ties / nondeterminism
F6  query-sensitive relevance
F7  backtracking policy
F8  probability / coupling separation
F9  structural model revision boundary
F10 impossible antecedent typing
F11 causal-stress compatibility
F12 model/Reality truth-role firewall
F13 institutional rule/constitution change
F14 mechanism/policy vs token-value distinction
F15 grain/representation sensitivity without model=Reality collapse
```

The central scoring vocabulary is:

```text
NATIVE
  the architecture has an explicit primitive/construction that handles the requirement.

PARAMETERIZABLE
  the architecture can represent the requirement if additional ordering/context/model parameters are supplied.

EXTENSION
  a recognized extension of the core architecture can handle it, but the canonical/basic form does not.

EXTERNAL
  the requirement must be settled by another theory or modeling choice outside the architecture.

FAIL-AS-UNIVERSAL
  the basic architecture imposes a condition contradicted by WDF2-B if treated as a universal foundation.
```

`FAIL-AS-UNIVERSAL` does not mean the architecture is useless. It means the architecture cannot be elevated unchanged into the universal World counterfactual foundation.

---

# 3. First decisive result — the candidate list is heterogeneous

WDF1/WDF2-A initially listed families such as:

```text
Stalnaker selection
Lewis similarity/orderings
premise semantics
SCM/Pearl
backtracking
nondeterministic causal models
law/chance-relative accounts
powers/dispositions
impossible worlds
plural/domain-specific accounts
```

WDF2-C finds that these are not all answers to the same question.

They occupy at least five architectural roles.

## 3.1 Selection / evaluation architectures

Primarily answer:

```text
Given an anchor and antecedent, which alternatives count for evaluation?
```

Examples:

```text
Stalnaker selection function
Lewis sphere / comparative similarity
premise / ordering semantics
```

## 3.2 Structural alteration / generation architectures

Primarily answer:

```text
How does the antecedent modify a structured model and what solutions follow?
```

Examples:

```text
SCM forward intervention
SCM backtracking
nondeterministic structural models
```

## 3.3 Reality-facing grounding families

Primarily answer:

```text
What in Reality makes certain alternatives, invariances or manifestations privileged?
```

Examples:

```text
law / nomological structure
objective chance candidate
powers / dispositions
causal mechanisms
```

These are not selection algorithms by themselves.

## 3.4 Alternative-domain extensions

Primarily answer:

```text
What kinds of alternatives may be admitted at all?
```

Example:

```text
impossible-world / nonvacuist extension
```

This does not by itself settle ordinary similarity or structural surgery.

## 3.5 Meta-architectures

Primarily answer:

```text
How are multiple domain/query-specific generators coordinated without pretending they are one ontology?
```

Example:

```text
typed plural / domain-relative architecture
```

### Earned firewall C-LAYER-1

```text
SelectionSemantics
!= AlterationGenerator
!= RealityGrounding
!= AlternativeDomainExtension
!= MetaRouter
```

A theory may instantiate more than one role, but shared vocabulary must not erase the distinction.

This is one of the strongest WDF2-C results.

---

# PART I — STALNAKER SELECTION-FUNCTION FAMILY

# 4. Core form

The canonical selection-function intuition can be represented schematically as:

```text
f(w, A) -> one selected A-alternative

A □→ C at w
iff
C holds at f(w,A)
```

with centering/selection constraints depending on the system.

Its attraction is obvious:

```text
antecedent-indexed
compact
compositional
clean `would` truth condition
```

The architecture directly answers a selection question.

---

# 5. Strength — explicit antecedent-indexed relevance

The function:

```text
f(anchor, antecedent)
```

makes it explicit that a counterfactual is not bare existential possibility.

It naturally captures:

```text
CounterfactualAlternative != Any A-alternative
```

and creates a clear interface for contextual relevance.

WDF2 therefore does **not** reject selection-function semantics.

---

# 6. WDF2-B pressure — uniqueness

Canonical Stalnaker semantics selects one antecedent-world.

But WDF2-B produced independent sources of plurality:

```text
tied minimal repairs
nondeterministic transition
probability over alternative outcomes
multiple admissible institutional implementations
```

Therefore:

```text
one selected world
```

cannot be a universal fact inferred from the counterfactual query itself.

A model can still stipulate a selection function that breaks ties, but then the tie-breaking rule is **additional semantic structure**.

### Disposition

```text
Unique selection as universal foundation: FAIL-AS-UNIVERSAL
Selection function as typed/query-local evaluator: RETAIN
Set-valued/generalized selection: OPEN EXTENSION
```

---

# 7. WDF2-B pressure — hidden grounding of f

The function notation is mathematically compact but ontologically and scientifically silent about why:

```text
f(w,A)=w1
```

rather than:

```text
f(w,A)=w2
```

when both satisfy A.

The answer may depend on:

```text
laws
causal structure
normality
institutional constitution
program semantics
query target
historical continuity
similarity priorities
```

Thus the selection function can **store** the answer without **grounding** it.

### Falsifier C-SF1

A candidate that treats arbitrary `f` as explanatory completion merely relocates hidden assumptions into the function.

```text
SelectionFunctionExistence != SelectionGrounding
```

---

# 8. Structural alteration pressure

Nothing in bare selection-function form distinguishes:

```text
value change
mechanism replacement
rule change
model revision
```

unless these distinctions are encoded in:

```text
antecedent representation
world structure
selection function
```

Therefore F1/F3/F13/F14 are mostly **EXTERNAL/PARAMETERIZABLE**.

The architecture can express the results after a rich world representation is supplied, but does not itself solve WDF2-A/B alteration typing.

---

# 9. Counterpossible pressure

In ordinary merely-possible-world semantics, an antecedent with no admissible A-world creates vacuity or undefined-selection pressure depending on the exact system.

Impossible-world extensions can repair nonvacuous counterpossibles, but that is an extension to the alternative domain rather than a virtue of the basic selection function alone.

Disposition:

```text
F10 impossible antecedents: EXTENSION
```

---

# 10. Formal expressivity note — not an ontological falsifier

A 2026 result by Kocurek, Walsh and Weiss proves a strong non-axiomatizability result for an enriched first-order version of Stalnaker's proposition-taking selection-function semantics.

WDF2-C treats this carefully:

```text
formal first-order axiomatization limitation
!= semantic inadequacy
!= metaphysical falsification
```

It is relevant to future formal/logic engineering but does not decide whether selection functions capture a legitimate counterfactual role.

---

# 11. Stalnaker-family score

```text
F1 typed alteration                 EXTERNAL
F2 preservation                     PARAMETERIZABLE via f/world structure
F3 alteration-preservation compat   EXTERNAL
F4 correspondence                   EXTERNAL
F5 plurality/ties                   FAIL-AS-UNIVERSAL in singleton form
F6 query relevance                  PARAMETERIZABLE
F7 backtracking                     PARAMETERIZABLE / EXTERNAL
F8 probability/coupling             EXTERNAL
F9 model revision                   EXTERNAL
F10 counterpossible                 EXTENSION
F11 causal stress                   WEAK without extra structure
F12 model/Reality firewall          COMPATIBLE
F13 institutional constitution      EXTERNAL
F14 mechanism vs value              EXTERNAL
F15 grain sensitivity               EXTERNAL/PARAMETERIZABLE
```

### Verdict

**Strong evaluator interface; weak standalone grounding/generation theory.**

Not selected as universal foundation.

---

# PART II — LEWIS ORDERING / SPHERE FAMILY

# 12. Core form

Lewis-style architectures replace single selection with comparative closeness or nested spheres around an anchor.

Schematic form:

```text
≤_w orders alternatives by closeness/relevance to anchor w

A □→ C
is evaluated over the closest/relevantly best A-alternatives
```

Unlike canonical Stalnaker uniqueness, Lewisian ordering naturally permits several equally close A-worlds.

This immediately handles one WDF2-B pressure better.

---

# 13. Strength — plurality and ties

WDF2-B S-family requires alternatives to remain plural in cases of:

```text
equal repair cost
nondeterminism
multiple implementation realizations
```

An ordering/sphere architecture can retain:

```text
Best_A(w) = {w1,w2,...}
```

rather than forcing a unique representative.

Thus:

```text
F5 plurality/ties: NATIVE/STRONG
```

relative to the singleton Stalnaker form.

---

# 14. Strength — law/fact priorities can be represented

Lewis's own work makes similarity priorities explicit, including pressure involving:

```text
law violations / small miracles
large fact divergence
historical match
```

This is important because WDF2-B rejected simple edit distance.

An ordering architecture can encode lexicographic or partial priorities over **types of difference**.

But representation is not grounding.

---

# 15. Central weakness — similarity is a loaded compression

WDF2-B showed that `minimal change` is downstream of:

```text
alteration type
preservation profile
grain
correspondence
query target
```

A global closeness relation can encode all of those dimensions, but then:

```text
≤_w
```

becomes a compressed repository for precisely the hidden assumptions WDF2 is trying to expose.

### Falsifier C-L1

```text
SimilarityOrdering != ExplanationOfWhyDifferencesMatter
```

unless the ordering is grounded independently.

---

# 16. Query sensitivity pressure

WDF2-B S5 showed:

```text
same antecedent
+ availability query
```

can require different relevant similarity dimensions from:

```text
same antecedent
+ compliance query
```

A single target-independent global ordering must either:

1. prove that the query-sensitive results emerge anyway;
2. index ordering by query/target;
3. admit layered/order families.

Thus:

```text
GlobalSimilarityMetric: NOT EARNED
Query-indexed ordering: viable extension
```

---

# 17. Backtracking pressure

Lewisian similarity traditions can encode different attitudes toward historical divergence and miracle size.

However WDF2-B and formal SCM backtracking work show that backtracking is not merely one numerical weight; it can correspond to preserving a different **kind of structure**:

```text
forward/interventional:
  background U fixed
  local mechanism changed

backtracking:
  mechanisms F fixed
  background U changes
```

Ordering semantics can rank the resulting worlds, but it does not by itself identify which alteration regime the query intended.

Therefore F7 is **PARAMETERIZABLE**, not solved at root.

---

# 18. Structural and institutional pressure

Possible-world ordering is representation-general, which is both strength and weakness.

It can compare worlds where:

```text
software code differs
rules differ
laws differ
institutions differ
```

but only if world descriptions and identity/correspondence conditions have already been supplied.

It does not natively distinguish:

```text
change the Actor credential
vs
change the rule constituting authorization
```

unless similarity dimensions are typed accordingly.

---

# 19. Counterpossible pressure

Standard Lewis/Stalnaker possible-world treatments are classically associated with vacuity when no possible A-world exists.

Impossible-world extensions can preserve the ordering idea while enlarging the domain.

This is important because it demonstrates:

```text
ordering architecture
```

and:

```text
possible-only domain
```

are separable choices.

---

# 20. Lewis-family score

```text
F1 typed alteration                 EXTERNAL
F2 preservation                     PARAMETERIZABLE via ordering priorities
F3 compatibility                    EXTERNAL
F4 correspondence                   EXTERNAL / counterpart theory possible
F5 plurality/ties                   NATIVE
F6 query relevance                  PARAMETERIZABLE; global form pressured
F7 backtracking                     PARAMETERIZABLE
F8 probability/coupling             EXTERNAL
F9 model revision                   EXTERNAL
F10 counterpossible                 EXTENSION
F11 causal stress                   EXPRESSIVE but not sufficient for preemption alone
F12 model/Reality firewall          COMPATIBLE
F13 institutional constitution      EXTERNAL
F14 mechanism vs value              EXTERNAL
F15 grain sensitivity               PARAMETERIZABLE but representation-dependent
```

### Verdict

**Strong general relevance-ordering language; weak independent grounding of relevance.**

Retained as a major candidate component, not universal World ontology.

---

# PART III — PREMISE / BACKGROUND / COTENABILITY FAMILY

# 21. Core form

Premise semantics evaluates a counterfactual by combining the antecedent with a structured subset/revision of factual premises.

Schematic form:

```text
FactualPremises(w)
+ antecedent A
-> admissible/maximal consistent revised premise sets
-> consequences C
```

Kratzer-style work emphasizes how facts are divided, lumped and retained rather than positing primitive overall world similarity.

This directly targets WDF2-B's preservation problem.

---

# 22. Strength — preservation becomes explicit material

Compared with a global distance relation, premise semantics forces attention to:

```text
which factual premises survive the supposition?
which conflict with A?
which are grouped together?
which are protected?
```

Thus F2 is unusually strong.

```text
F2 preservation: NATIVE
```

at the semantic level.

---

# 23. Strength — indeterminacy can be structural rather than erroneous

If several maximal admissible premise sets survive, counterfactual evaluation can remain indeterminate/plural.

This fits WDF2-B's rejection of mandatory unique nearest alternatives.

It also provides a natural location for:

```text
ceteris paribus
normal background
contextual relevance
```

without pretending they are a numerical metric.

---

# 24. Central weakness — premise individuation/lumping is itself a grounding problem

The architecture replaces:

```text
Which world is closest?
```

with:

```text
Which facts/premises belong together and which may be dropped independently?
```

This is an improvement when premise structure is independently motivated, but otherwise it can simply move arbitrariness into:

```text
premise granularity
lumping
priority
admissibility constraints
```

### Falsifier C-P1

```text
PremiseRevision != IndependentGroundingOfPremiseStructure
```

The problem is relocated, not necessarily solved.

---

# 25. Important bridge — premise semantics and causal structure need not be rivals

Causal premise semantics demonstrates that premise-style semantics can incorporate Pearl-style causal networks, intervention and backtracking structure.

This yields a major WDF2-C methodological result:

```text
Different semantic architectures can be partially intertranslatable/composable.
```

Therefore expressive success alone cannot identify the correct foundational role.

Two theories may reproduce many of the same truth conditions while placing explanatory commitments in different places:

```text
ordering
premise set
causal graph
selection function
```

### Earned firewall C-EQ-1

```text
FormalExpressiveEquivalence
!= GroundingEquivalence
!= OntologicalEquivalence
```

This prevents WDF2 from declaring a winner merely because one formalism can encode another.

---

# 26. Structural revision pressure

Premise semantics can revise premises more flexibly than a fixed SCM can alter variables, but it still needs a language in which the new antecedent is expressible.

A genuinely novel institutional status or model category may require:

```text
language / ontology expansion
```

rather than ordinary premise revision.

Thus F9 is better exposed but not solved.

---

# 27. Premise-family score

```text
F1 typed alteration                 PARAMETERIZABLE via premise types
F2 preservation                     NATIVE
F3 compatibility                    PARAMETERIZABLE / can be explicit
F4 correspondence                   EXTERNAL
F5 plurality/ties                   NATIVE
F6 query relevance                  NATIVE/PARAMETERIZABLE via premise context
F7 backtracking                     EXTENSION / causal premise semantics
F8 probability/coupling             EXTERNAL/EXTENSION
F9 model revision                   PARTIAL; language revision external
F10 counterpossible                 DEPENDS on background logic/domain
F11 causal stress                   EXTENSION with causal premise structure
F12 model/Reality firewall          COMPATIBLE
F13 institutional constitution      STRONG if rules are typed premises
F14 mechanism vs value              PARAMETERIZABLE
F15 grain sensitivity               EXPLICIT but premise-grain grounded externally
```

### Verdict

**Strong preservation/revision architecture; central residual is what licenses premise structure and lumping.**

Retained.

---

# PART IV — SCM FORWARD / INTERVENTIONAL STRUCTURAL ARCHITECTURE

# 28. Core form

A standard structural causal model supplies:

```text
M = (U,V,F)
```

with structural functions assigning endogenous variables from parents/background variables.

A forward intervention:

```text
do(X=x)
```

replaces the equation/mechanism for X while preserving the remaining declared mechanisms and factual exogenous background.

Counterfactual evaluation then follows the familiar pattern:

```text
abduction
-> action / structural surgery
-> prediction
```

This is much more than a generic selection metric.

It supplies a **typed structural generator**.

---

# 29. Strength — alteration and preservation are mechanically explicit

Within the declared model:

```text
altered equation(s) are named
unchanged equation(s) are named
background coupling is named
solution propagation is defined
```

This directly satisfies WDF2-B's strongest demand better than possible-world similarity alone.

```text
F1 typed alteration: NATIVE for supported intervention kinds
F2 preservation: NATIVE
F3 compatibility: NATIVE within model surgery rules
```

---

# 30. Strength — observation / intervention / counterfactual separation

Structural semantics explicitly distinguishes:

```text
P(Y | X=x)
P(Y | do(X=x))
P(Y_x | evidence)
```

This strongly preserves WDF1/WDF2 probability firewalls.

It also gives a principled coupling in deterministic SCMs by sharing exogenous background across factual and counterfactual submodels.

---

# 31. Core limitation — fixed model and variable choice

The strength of SCMs comes from committing to:

```text
variables
causal parents
equations
exogenous background
```

But WDF0 requires structural revisability.

Therefore:

```text
SCM counterfactual truth is conditional on model adequacy.
```

It cannot by itself decide whether:

```text
an omitted variable should exist
a rule should be represented as a variable or mechanism
a new institutional status requires ontology revision
a changed physical law is an intervention or a new model
```

### Falsifier C-SCM1

```text
FixedModelCounterfactual != GeneralCounterfactualArchitecture
```

unless a meta-level model-revision theory is added.

---

# 32. Core limitation — `do(X=x)` is not all alteration

Standard perfect interventions are excellent for direct value-setting surgery.

But WDF2-B distinguishes:

```text
one-token value set
soft intervention
mechanism replacement
policy replacement
rule/constitution change
model/boundary change
law change
```

Some can be encoded through expanded SCMs, stochastic/soft interventions or meta-variables.

But a universal strategy of:

```text
turn every structural change into an ordinary node assignment
```

risks destroying the distinction between object-level state and model-level structure.

### Falsifier C-SCM2

```text
RepresentableAsVariableAssignment
!= SameAlterationType
```

---

# 33. Identity/correspondence strength and limit

Within one SCM, factual and counterfactual copies of variables have a strong correspondence supplied by the model structure and shared variable meaning.

This is useful for token-level queries.

But when the model itself changes:

```text
M -> M'
```

a mapping between variables/entities is required.

That mapping is not supplied automatically by standard within-model counterfactual semantics.

Thus:

```text
F4 correspondence: NATIVE within fixed model; EXTERNAL across model revision
```

---

# 34. Uniqueness pressure

Traditional deterministic acyclic SCM semantics often yields a unique counterfactual solution for a given exogenous context and intervention.

WDF2-B showed this cannot be universalized.

The 2025 nondeterministic causal-model program explicitly removes both:

```text
unique child assignment for each parent assignment
unique counterfactual world per intervention
```

Therefore deterministic uniqueness is a **domain/model assumption**, not a definition of counterfactuality.

---

# 35. Backtracking pressure

Forward SCM counterfactuals preserve background and alter local mechanism/equation structure.

But WDF2-B B-family showed legitimate queries where one instead wants:

```text
mechanisms fixed
upstream/background conditions changed
```

This is exactly what modern backtracking SCM semantics formalizes.

Therefore:

```text
SCM != one unique counterfactual semantics
```

The model language can support different generator policies.

### Earned firewall C-SCM3

```text
CausalModelStructure != CounterfactualGeneratorPolicy
```

The same structural model can support forward and backtracking queries with different truth conditions.

---

# 36. Counterpossible and law-change pressure

Standard SCMs operate inside a declared causal model.

Antecedents inconsistent with:

```text
variable domain
model ontology
higher-order structural constraints
logical/mathematical possibility
```

are not automatically meaningful counterfactuals.

Thus impossible/counterlegal cases require:

```text
model alteration
meta-model
expanded domain
or another semantic layer
```

F10 is not natively universal.

---

# 37. Forward SCM score

```text
F1 typed alteration                 NATIVE within intervention vocabulary
F2 preservation                     NATIVE
F3 compatibility                    NATIVE within fixed model
F4 correspondence                   NATIVE within model / external across M->M'
F5 plurality/ties                   FAIL-AS-UNIVERSAL in deterministic form; EXTENSION
F6 query relevance                  model/query-target parameterized
F7 backtracking                     FAIL in forward-only form; EXTENSION
F8 probability/coupling             STRONG in deterministic probabilistic SCM; assumptions explicit
F9 model revision                   EXTERNAL
F10 counterpossible                 EXTERNAL/EXTENSION
F11 causal stress                   STRONG
F12 model/Reality firewall          COMPATIBLE if provenance retained
F13 institutional constitution      PARTIAL; depends on modeling level
F14 mechanism vs value              STRONGER than generic possible-world form
F15 grain sensitivity               EXTERNAL model-selection/abstraction problem
```

### Verdict

**Best current structural generator for many scientific/engineering causal counterfactuals; not a universal counterfactual metaphysics.**

Retained as a major typed generator.

---

# PART V — SCM BACKTRACKING ARCHITECTURE

# 38. Core form

Backtracking SCM semantics keeps the causal laws/functions fixed while allowing background/exogenous conditions to differ between factual and counterfactual scenarios.

Schematic contrast:

```text
Forward/interventional:
  U* = U
  F* differs locally

Backtracking:
  F* = F
  U* may differ from U
```

A backtracking coupling/conditional chooses or weights alternative background states consistent with the antecedent.

---

# 39. Strength — WDF2-B B-family is native

Diagnostic questions such as:

```text
If the server had been healthy, what earlier conditions would have needed to differ?
```

are directly natural.

The architecture preserves:

```text
causal mechanisms
```

and explains antecedent differences upstream.

This is not an edge-case patch. It is a different generator policy.

---

# 40. Central residual — backtracking relocates selection into background coupling

Once U may differ, the theory needs something like:

```text
P_B(U* | U)
```

or another closeness/relevance relation over background conditions.

Thus the selection problem returns in a new location:

```text
Which upstream differences are admissible/preferred?
```

### Falsifier C-BT1

```text
BacktrackingSemantics != GroundingOfBacktrackingSimilarity
```

The architecture clarifies **what is held fixed**, but still needs a principle for **which changed background is relevant**.

---

# 41. Query-role complementarity

The backtracking literature explicitly argues that forward and backtracking semantics can be suited to different reasoning tasks rather than one simply replacing the other.

This matches WDF2-B exactly:

```text
consequence under local action/intervention
!=
diagnostic upstream accommodation
```

This is strong evidence for a later **query-role architecture**.

---

# 42. Backtracking SCM score

```text
F1 typed alteration                 NATIVE for background-change form
F2 preservation                     NATIVE: mechanisms fixed
F3 compatibility                    NATIVE within model
F4 correspondence                   NATIVE within fixed variable model
F5 plurality/ties                   NATIVE if P_B/set-valued coupling allows
F6 query relevance                  PARAMETERIZABLE in backtracking coupling
F7 backtracking                     NATIVE
F8 probability/coupling             NATIVE but grounding of coupling remains
F9 model revision                   EXTERNAL
F10 counterpossible                 EXTERNAL
F11 causal stress                   COMPLEMENTARY; not replacement for forward causal queries
F12 model/Reality firewall          COMPATIBLE
F13 institutional constitution      PARTIAL
F14 mechanism vs value              CLEAR distinction from forward surgery
F15 grain sensitivity               EXTERNAL
```

### Verdict

**Strong diagnostic generator, complementary to forward SCM; central residual is grounding the backtracking coupling/relevance relation.**

Retained.

---

# PART VI — NONDETERMINISTIC / STOCHASTIC STRUCTURAL ARCHITECTURES

# 43. Why this is a separate candidate

WDF2-B showed that deterministic SCM semantics contains two assumptions that are not foundation-safe:

```text
unique child value for each parent assignment
unique counterfactual solution per intervention/context
```

Recent nondeterministic causal models explicitly remove these assumptions through multivalued mechanisms and altered counterfactual semantics.

This is not a minor numerical generalization. It changes the shape of the counterfactual alternative set.

---

# 44. Strength — plurality becomes structural rather than epistemic

In a nondeterministic causal model:

```text
same declared parent state
```

can admit multiple child outcomes.

Therefore plurality need not represent ignorance about one hidden deterministic world.

This is especially relevant to domains such as:

```text
stochastic physical processes
randomized mechanisms
black-box probabilistic services
LLM/provider output distributions
```

where forcing all randomness into hidden deterministic response variables can add unrealistic structure.

---

# 45. Strong contemporary pressure — LLMs/providers

Recent work explicitly models probabilistic LLMs as nondeterministic causal models and argues that different counterfactual-generation methods impose different application-specific biases such as counterfactual stability.

This matches WDF2-B's Agent/provider cases:

```text
same factual output
+ changed prompt
```

does not uniquely determine which counterfactual sample should correspond unless one adds a coupling/stability criterion.

### Earned firewall C-ND1

```text
ApplicationUsefulCoupling
!= UniversalCounterfactualSemantics
```

A Gumbel/shared-randomness style coupling can be extremely useful while still being a purpose-specific choice.

---

# 46. Strength — actual-solution preservation can replace hidden deterministic seed sharing

Nondeterministic causal semantics can preserve actual mechanism behavior where parent configurations remain factual without positing a globally shared hidden deterministic response table.

This provides a different answer to the correspondence/coupling problem.

But it is still a substantive semantic commitment, not pure logic.

---

# 47. Limit — fixed structural vocabulary remains

Nondeterminism does not solve:

```text
rule-change semantics
model revision
new institutional status
law-changing antecedent
identity across different model vocabularies
```

It generalizes the solution set **within a model family**.

Therefore WDF2 must not mistake:

```text
plural structural solutions
```

for a complete open-world counterfactual theory.

---

# 48. Nondeterministic structural score

```text
F1 typed alteration                 NATIVE within causal model
F2 preservation                     NATIVE
F3 compatibility                    NATIVE
F4 correspondence                   STRONG within model
F5 plurality/ties                   NATIVE
F6 query relevance                  PARAMETERIZABLE
F7 backtracking                     separate extension/policy
F8 probability/coupling             STRONG; multiple semantics possible
F9 model revision                   EXTERNAL
F10 counterpossible                 EXTERNAL
F11 causal stress                   STRONG potential
F12 model/Reality firewall          COMPATIBLE
F13 institutional constitution      PARTIAL
F14 mechanism vs value              STRONG
F15 grain sensitivity               EXTERNAL
```

### Verdict

**Best current pressure against deterministic-uniqueness universalization; retained as a structural generator family, not universal ontology.**

---

# PART VII — LAW / CHANCE-RELATIVE GENERATION

# 49. Architectural role correction

A law-relative account can say roughly:

```text
hold laws fixed
vary local facts/background
```

or use law/chance structure to constrain admissible histories.

This is valuable especially in physical/scientific counterfactuals.

But WDF2-C finds that `law/chance-relative` is not one complete selector architecture.

It is better classified as a **grounding source** for:

```text
preservation
admissibility
ordering priorities
probability weight
```

---

# 50. Strength — objective physical relevance

If a law theory is independently supplied, it can explain why some histories are not merely less similar but **nomologically excluded**.

Likewise a chance theory can assign objective weight among physically admissible continuations.

This is stronger Reality-facing grounding than arbitrary world similarity.

---

# 51. Fatal universalization pressure — law-changing counterfactuals

WDF2-B K/P physical cases include:

```text
If the law/mechanism had been different ...
```

A semantics defined by:

```text
always hold actual laws fixed
```

cannot evaluate those cases without a meta-law or higher-order comparison principle.

Therefore:

```text
LawHeldFixed
```

is a query-dependent preservation policy, not a universal definition.

---

# 52. WDF1 circularity remains

WDF1 already isolated:

```text
law -> counterfactual support
counterfactual support -> criterion/evidence for law
```

WDF2-C finds no new reduction that breaks this circle.

Law grounding is therefore important but still an open Reality-facing interface.

---

# 53. Cross-domain pressure

Software, institutions and Agent policy counterfactuals have structures analogous to invariance/rules, but:

```text
program semantics
institutional rule
physical law
```

are not automatically one ontology.

A law-relative architecture cannot gain universality by calling all stable rules `laws`.

### Earned firewall C-LAW1

```text
PhysicalNomologicalLaw
!= SoftwareSemantics
!= InstitutionalConstitutiveRule
```

although each can ground a domain-specific preservation relation.

---

# 54. Law/chance disposition

```text
As universal selector: REJECTED
As Reality-facing physical grounding provider: RETAINED / OPEN
As chance weighting provider: RETAINED / OPEN pending ObjectiveChance foundations
```

---

# PART VIII — POWERS / DISPOSITIONAL GROUNDING

# 55. Architectural role correction

Powers/dispositional approaches can ground claims such as:

```text
fragile object would break if struck under appropriate conditions
```

by appealing to what the object/system is disposed/powered to do.

But this is not itself a full algorithm for selecting alternatives.

WDF2-C therefore reclassifies the family as primarily **Reality-facing grounding**.

---

# 56. Strength — avoids pure similarity conventionalism

A dispositional account promises to explain why certain manifestations are relevant because of properties/capacities of the system, not merely because a possible world happens to score highly on a similarity metric.

This can provide genuine grounding pressure.

---

# 57. Classic pressure — finks, masks, antidotes

Simple conditional reduction:

```text
x has disposition D
iff
if stimulus S then manifestation M
```

fails under familiar cases where:

```text
the stimulus removes the disposition
another factor masks manifestation
an antidote interferes with normal operation
```

Therefore the disposition itself cannot be naively reduced to one unqualified counterfactual.

And conversely, using dispositions to select counterfactual backgrounds can become circular if the disposition is defined through those same counterfactuals.

---

# 58. Cross-domain pressure

`powers` language may fit physical/biological causal capacities better than:

```text
software version change
institutional charter revision
semantic convention
model ontology expansion
```

Trying to call all of these `powers` risks destructive metaphorization.

Thus cross-domain universality is not earned.

---

# 59. Powers disposition

```text
As universal selector: REJECTED
As possible Reality-facing grounding family for some domains: RETAINED / OPEN
Simple counterfactual reduction of dispositions: REJECTED
```

---

# PART IX — IMPOSSIBLE-WORLD / NONVACUIST EXTENSION

# 60. Architectural role correction

Impossible-world semantics primarily expands:

```text
AlternativeDomain
```

so that counterfactuals with impossible antecedents can receive nontrivial evaluation.

It does not by itself determine ordinary physical/software/institutional alteration semantics.

Thus it is best classified as a **domain extension**, not a replacement for SCM/order/premise semantics.

---

# 61. Strength — WDF2-B K-family survives

Nonvacuist semantics allows:

```text
A impossible
A □→ C true
A □→ D false
```

rather than forcing all counterpossibles to be trivially true.

This is exactly why WDF2-B refused to delete impossible antecedents.

---

# 62. Strength — hyperintensional separation

Impossible worlds can distinguish antecedents that are necessarily equivalent in ordinary possible-world semantics while still differing in inferential/content structure.

This is important for:

```text
logical suppositions
mathematical reasoning
semantic/conventional changes
essence-style questions
```

---

# 63. Central residual — impossible alternatives still need relevance structure

Once impossible worlds are admitted, the hard question becomes:

```text
which impossible worlds are relevant?
how are they ordered?
what impossibilities may be preserved?
which logical consequences remain operative?
```

Impossible-world accounts therefore reintroduce selection/order/accessibility structure.

They extend the domain; they do not delete the selection problem.

### Earned firewall C-IW1

```text
AlternativeDomainExpansion != AlternativeSelectionSolution
```

---

# 64. Impossible-world disposition

```text
Counterpossible coverage: STRONG
Ordinary alteration typing: EXTERNAL
Preservation grounding: PARAMETERIZABLE
Selection grounding: OPEN
Universal use for possible antecedents: NOT REQUIRED
```

Retained as a typed extension.

---

# PART X — PLURAL / DOMAIN-RELATIVE META-ARCHITECTURE

# 65. Why pluralism now becomes a serious candidate

WDF2-C finds no single candidate that natively solves all of:

```text
structural surgery
background preservation
query relevance
nondeterminism
probability coupling
impossible antecedents
model revision
institutional constitution
Reality grounding
```

The failures are not random. They align with domain/query roles.

This motivates a meta-architecture in which different counterfactual generators are typed rather than collapsed.

---

# 66. Weak pluralism is unacceptable

The statement:

```text
use whichever semantics feels appropriate
```

is not a foundation.

It merely renames hidden assumptions as `context`.

Therefore WDF2 rejects unconstrained pluralism.

### Falsifier C-PL1

A plural architecture must answer:

```text
what licenses choosing generator G for query Q?
```

without circularly saying:

```text
because G gives the right answer.
```

---

# 67. Strong typed pluralism

A serious plural architecture would need at least:

```text
CounterfactualFrame F
QueryRole Q
Domain/Model D
TruthRole T
CandidateGenerator family {G_i}
Admissibility relation Admit(G_i | F,Q,D,T)
Generator provenance/evidence
Result shape
```

where result shape can be:

```text
singleton alternative
minimal/tied set
ordered alternatives/spheres
maximal premise sets
structural solution set
probability measure/distribution
impossible-world extension
failure: no admissible correspondence/model
```

This does **not** say Reality contains a meta-router.

It is a research architecture for making commitments explicit.

---

# 68. Major discovery — generator result shape must be typed

WDF2-B showed that alternative generation may yield qualitatively different outputs.

Therefore a universal API of:

```text
getNearestWorld() -> World
```

is too narrow even at the research level.

A semantics-neutral generator result needs to permit at least:

```text
Singleton(a)
Set({a_i})
OrderedSet(≤,{a_i})
PremiseFamily({Γ_i})
StructuralSolutions({s_i})
Measure(Ω,μ)
DomainExtendedAlternatives(...)
NoAdmissibleAlternative(reason)
ModelRevisionRequired(reason)
```

Again, this is conceptual structure, not a production schema.

---

# 69. Major discovery — selection and evaluation must be separated

Suppose the generator returns multiple alternatives.

Then `would`, `might`, probability and robustness can use different operators over the same result:

```text
would C:
  C across all selected/best alternatives under declared semantics

might C:
  C in at least some relevant alternative under declared semantics

probability of C:
  μ(C) under a declared measure/coupling

robustly would C:
  C over a wider perturbation family
```

Therefore:

```text
AlternativeGeneration != ModalForceEvaluation
```

This preserves WDF1's operator/measure separation.

---

# 70. Major discovery — candidate theories can compose

Examples:

```text
SCM generator
+ Lewis-style ordering over admissible structural solutions

SCM backtracking
+ probability coupling over exogenous alternatives

premise semantics
+ causal-network constraints

possible-world ordering
+ impossible-world extension

law-grounded admissibility
+ chance measure
```

This means a one-dimensional `theory tournament` is structurally wrong.

The correct comparison asks:

```text
Which architectural role is being supplied?
What assumptions does it add?
Can it compose without double-counting or contradiction?
```

### Earned firewall C-COMP1

```text
CounterfactualTheoryName != OneAtomicArchitecture
```

A mature counterfactual system may be a typed composition of components historically associated with different schools.

---

# 71. Composite candidate — Typed Counterfactual Generation Contract

WDF2-C does **not** freeze a universal counterfactual semantics.

But deletion tests support a minimal meta-contract:

```text
Given:
  Frame F
  QueryRole Q
  Domain/Model D
  TruthRole T

A generator/selector G must expose:
  alteration semantics it assumes
  preservation semantics it assumes
  correspondence semantics it assumes
  alternative-domain commitments
  result shape
  ordering/measure/coupling if any
  grounding/provenance
  failure/revision conditions
```

The contract does not specify **which G wins**.

It specifies what must be visible before the output can be interpreted.

### Disposition

```text
Universal one-generator semantics: NOT EARNED
Typed generator/selector contract: EARNED AS RESEARCH META-ARCHITECTURE
Reality ontology status: NONE
Production schema status: NOT ADMITTED
```

---

# PART XI — CROSS-CANDIDATE SCORECARD

# 72. Compact score matrix

Legend:

```text
N  native
P  parameterizable
E  extension
X  external
F  fail-as-universal in basic form
```

| Architecture | F1 Alteration | F2 Preserve | F4 Correspond | F5 Plural | F6 Query relevance | F7 Backtrack | F8 Coupling | F9 Revision | F10 Impossible | F11 Causal stress |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Stalnaker singleton selection | X | P | X | F | P | P/X | X | X | E | X/weak |
| Lewis ordering/spheres | X | P | X | N | P | P | X | X | E | P |
| Premise semantics | P | N | X | N | N/P | E | X/E | P/X | E | E |
| SCM forward deterministic | N | N | N/X | F | P | F/E | N | X | X | N |
| SCM backtracking | N | N | N/X | N/P | P | N | N/P | X | X | P |
| Nondeterministic structural | N | N | N/X | N | P | E | N/P | X | X | N/P |
| Law/chance grounding | X/P | N for physical cases | X | P | X/P | P | chance-specific | X | counterlegal pressure | P |
| Powers/dispositions | X/P | P | X | P | P | P | X | X | X | P |
| Impossible-world extension | X | P | P/X | N/P | P | P | X | X/P | N | P |
| Typed plural meta-architecture | routes | routes | routes | N | N if admissibility grounded | routes | routes | routes | routes | routes |

The table makes the central result visible:

> **No single candidate has `N` across the matrix, and several rows are not even the same architectural species.**

---

# 73. Why expressive coverage cannot choose the winner

A highly expressive formalism can encode:

```text
selection function
ordering
causal model
premise set
rule system
```

as data.

If `can encode all cases` were sufficient, a general-purpose programming language would win every ontology debate.

Therefore WDF2-C rejects:

```text
MaximumExpressivity -> FoundationalAdequacy
```

The relevant criteria are instead:

```text
explicit assumptions
independent grounding
cross-domain falsification
truth-role preservation
minimal hidden imports
revisability
```

---

# 74. Why predictive success cannot choose the winner

Two architectures can agree on observed/current cases while disagreeing on untested counterfactuals.

This is especially severe for token counterfactual coupling:

```text
same observational distribution
same interventional marginals
```

can coexist with different joint potential-outcome structures.

Thus:

```text
ObservedFit != CounterfactualIdentification
```

and:

```text
CounterfactualPredictiveAgreementOnKnownCases
!= SameCounterfactualSemantics
```

---

# PART XII — THEORY-SPECIFIC FALSIFIERS DERIVED FOR LATER USE

# 75. Stalnaker-specific falsifiers

```text
SF1 tied minima without principled tie-break
SF2 objective/model nondeterminism
SF3 query-dependent selection with same A
SF4 impossible antecedent without domain extension
SF5 structural rule change where selected-world notation hides surgery
```

---

# 76. Lewis-specific falsifiers

```text
LF1 same coarse distance, different alteration type
LF2 target changes relevance dimensions
LF3 grain change reverses distance
LF4 law-breaking vs rule-breaking vs semantic change
LF5 no independently grounded priority ordering
```

---

# 77. Premise-specific falsifiers

```text
PF1 equivalent truth result under different premise lumping
PF2 premise granularity arbitrary relative to target
PF3 new ontology/category not expressible as premise revision
PF4 causal direction hidden in premise choice
PF5 inconsistent/counterpossible premise handling
```

---

# 78. Forward-SCM falsifiers

```text
SCF1 mechanism/rule/model change not representable as honest within-model do
SCF2 changed variable ontology
SCF3 diagnostic/backtracking query
SCF4 nondeterministic process with no realistic hidden response variable
SCF5 counterlegal/counterpossible query
```

---

# 79. Backtracking-SCM falsifiers

```text
BTF1 two equally plausible upstream accommodations
BTF2 query needs actual intervention rather than explanation
BTF3 background similarity/coupling unsupported
BTF4 model revision
BTF5 institution rule change beyond exogenous-state alteration
```

---

# 80. Nondeterministic-structural falsifiers

```text
NDF1 model ontology changes
NDF2 mechanism identity changes across providers
NDF3 query demands purpose-specific coupling not implied by model
NDF4 counterpossible antecedent
NDF5 cross-grain causal abstraction failure
```

---

# 81. Impossible-world falsifiers

```text
IWF1 ordinary possible antecedent where impossible worlds add no value
IWF2 two impossible worlds with no relevance ordering
IWF3 logical vs nomological impossibility conflated
IWF4 impossible-world semantics destroys desired ordinary validities
IWF5 identity/correspondence at impossible worlds underdetermined
```

---

# PART XIII — LARGEST RESIDUAL: GENERATOR GROUNDING / ADMISSIBILITY

# 82. The selection problem has not disappeared

Each architecture relocates the hardest question.

```text
Stalnaker:
  why f(w,A)=w1?

Lewis:
  why w1 ≤_w w2?

Premise semantics:
  why preserve Γ1 but drop Γ2?

SCM forward:
  why is this causal model/surgery the right representation?

SCM backtracking:
  why this P_B(U*|U) / upstream closeness?

Nondeterministic causal model:
  why this counterfactual coupling/preservation rule?

Law account:
  why these are the laws / why law is preserved?

Powers account:
  why this disposition/background/manifestation relation?

Impossible worlds:
  why these impossible alternatives are relevant?

Pluralism:
  why route query Q to generator G?
```

This common residual is **generator grounding/admissibility**.

---

# 83. `Context` is not an acceptable primitive answer

One tempting response is:

```text
context chooses the relevant semantics
```

But unless `context` is decomposed, this merely hides:

```text
query goal
truth role
domain mechanism
speaker interest
causal question
normative question
model fidelity
evidence
```

inside a generic word.

### Earned firewall C-CTX1

```text
ContextSensitivity != ArbitraryContextParameter
```

A valid World foundation must say **which context coordinate legitimately changes which counterfactual role**.

---

# 84. Preliminary sources of generator admissibility

WDF2-C does not solve the grounding problem, but identifies candidate sources that WDF2-D must separate and falsify.

## 84.1 Query role

Examples:

```text
prediction
planning
diagnosis
causal attribution
responsibility
explanation
robustness analysis
scientific intervention
policy comparison
counterpossible reasoning
```

Different roles can legitimately preserve different structures.

## 84.2 Domain semantics

Examples:

```text
physical dynamics
program execution semantics
institutional constitutive rules
Agent policy/provider semantics
```

## 84.3 Reality-facing grounding

Examples:

```text
law candidate
causal mechanism
power/disposition
objective chance candidate
```

## 84.4 Model adequacy / representation

A generator may be invalid if the model lacks the required variable, mechanism, status or grain.

## 84.5 Evidence / identification

A semantic quantity may exist but not be identified by available observations/experiments.

## 84.6 Normality / normative relevance

Omission/responsibility queries can require legitimate default/duty structure, which must not contaminate purely physical truth claims.

---

# 85. Generator admissibility must be typed by truth role

A generator can be suitable for:

```text
model-exploratory claim
```

but insufficient for:

```text
Reality-facing causal claim
```

Likewise a human-language similarity judgment may be adequate for:

```text
conversational counterfactual interpretation
```

but not for:

```text
physical intervention effect identification
```

Thus the admissibility relation must preserve WDF0/WDF1 truth-role separation.

---

# 86. Generator admissibility is not empirical identification

Even after choosing a correct semantic generator:

```text
G defines Y_x
```

we may lack enough evidence to estimate:

```text
P(Y_x | evidence)
```

Conversely, a statistical estimator can be numerically precise under an unjustified counterfactual model.

### Earned firewall C-ID1

```text
GeneratorSemantics
!= IdentificationAssumptions
!= EstimationProcedure
```

This will matter later for Finance, Human and Agent-evaluation consumers.

---

# PART XIV — WDF0 / WDF1 REOPEN AUDIT

# 87. WDF0

No FoundationReopenCondition fires.

WDF2-C strengthens:

```text
Reality != Model
SharedFormalStructure != SharedOntology
Cause != Constraint != Constitution
WithinModelUpdate != StructuralModelRevision
IdentifierEquality != OntologicalIdentity
InstitutionRelative != Subjective
```

The discovery that rival counterfactual theories occupy different architectural levels fits WDF0's meta-foundational discipline rather than falsifying it.

Disposition:

```text
WDF0 remains FROZEN.
```

---

# 88. WDF1

No FoundationReopenCondition fires.

WDF1's TMCG requires typed alternative/generator/evaluator/operator/provenance structure but never claimed a unique generator.

WDF2-C actually validates why WDF1 demoted TARA from Reality ontology to claim grammar.

The fact that:

```text
generator result may be singleton/set/order/measure/structural solutions
```

still fits the WDF1 open typed-generator role.

Disposition:

```text
WDF1 remains FROZEN.
```

---

# PART XV — PRODUCTION DISPOSITION

# 89. No engineering consumption

WDF2-C does not authorize:

```text
CounterfactualEngine
SimilarityService
WorldSelector
SCM service
PremiseRevision service
ImpossibleWorld registry
GeneratorRouter
```

in production World.

Current production remains:

```text
Bind -> Observe -> Act -> Reconcile
```

and is not required to instantiate a general counterfactual semantics.

Engineering consumption still requires:

```text
frozen relevant foundation
+
concrete reproduced consumer need
```

---

# PART XVI — RESIDUAL RANKING

# 90. Residuals after WDF2-C

```text
1. Generator grounding / admissibility / query role           CRITICAL
2. Structural-surgery composition across multiple loci       CRITICAL
3. Probability / coupling / nondeterministic evaluation      CRITICAL
4. Model revision and cross-model correspondence              CRITICAL
5. Similarity/premise relevance grounding                     HIGH/CRITICAL
6. Counterpossible domain/order grounding                     HIGH
7. Would/might/robust modal-force logic                        HIGH
8. Backtracking/forward hybrid semantics                       HIGH
9. Prevention/omission/preemption bridge to causation          HIGH
10. Law/chance/powers Reality-grounding comparison             HIGH, interface-coupled
```

The first residual is now clearly upstream:

> **Before composing several surgeries or assigning probabilities, World must know what makes a particular counterfactual generator admissible for a particular query and truth role.**

Without that step, pluralism becomes arbitrary and every candidate can hide its assumptions behind `context`, `similarity`, `model`, `premises` or `background`.

---

# 91. Exact next round

The next canonical round is therefore:

# **WDF2-D — Counterfactual Generator Grounding / Admissibility / Query-Role Separation**

WDF2-D should attack at least:

```text
prediction vs diagnosis
planning vs causal attribution
physical consequence vs responsibility
forward intervention vs backtracking explanation
model exploration vs Reality-facing claim
software semantics vs institutional constitution vs physical law
human pragmatic relevance vs objective mechanism relevance
semantic definition vs empirical identification
```

It should attempt to derive a non-circular admissibility test of the form:

```text
When is generator G licensed for query Q over domain/model D with truth role T?
```

without using:

```text
because G yields the intuitive/right answer
```

as the criterion.

Only WDF2-D residuals may determine WDF2-E.

---

# 92. Research sources / pressure references

Primary and high-quality research pressure used in WDF2-C includes:

- Robert Stalnaker, `A Theory of Conditionals` — canonical selection-function family.
- David Lewis, `Counterfactuals`, `Counterfactual Dependence and Time's Arrow`, and `Ordering Semantics and Premise Semantics for Counterfactuals` — comparative similarity/sphere family and background-ordering issues.
- Angelika Kratzer, `Partition and Revision: The Semantics of Counterfactuals`, `Constraining Premise Sets for Counterfactuals`, and later premise-semantics work — premise/background/lumping architecture.
- Stefan Kaufmann, `Causal Premise Semantics` — explicit bridge between premise semantics, causal networks, intervention and backtracking.
- Judea Pearl, `Structural Counterfactuals: A Brief Introduction` — structural counterfactual generation and abduction-action-prediction semantics.
- Alexander Balke & Judea Pearl, `Counterfactual Probabilities: Computational Methods, Bounds and Applications` — mechanism assumptions, probabilities of counterfactuals and partial identification.
- Julius von Kügelgen, Abdirisak Mohamed & Sander Beckers, `Backtracking Counterfactuals` — formal SCM distinction between forward/interventional and backtracking semantics.
- Sander Beckers, `Nondeterministic Causal Models` (CLeaR/PMLR 2025) — explicit removal of deterministic and unique-counterfactual-world assumptions.
- Sander Beckers, `Causal Counterfactuals Reconsidered` (2025 preprint) — stochastic/probabilistic counterfactual semantics without universal deterministic response-variable commitments.
- Sander Beckers, `Large Language Models as Nondeterministic Causal Models` (2025 preprint) — application-specific coupling/stability choices for probabilistic LLM counterfactuals.
- Francesco Berto, Mark Jago, Rohan French, Graham Priest & David Ripley, impossible-world / counterpossible work — nonvacuist alternative-domain extension and ordering pressure.
- Alexander Bird, `Dispositions and Antidotes`, plus the broader fink/mask literature — pressure against simple counterfactual reduction of dispositions.
- Alexander Kocurek, James Walsh & Yale Weiss, `Stalnaker's logical problem of conditionals is unsolvable` (2026 preprint) — formal limitation of an enriched first-order proposition-taking selection-function logic; treated as a formal expressivity/axiomatization result, not a metaphysical falsifier.

No source is treated as authority for a universal Ordivon World ontology.

---

# 93. Closeout

```text
WDF2-C: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B reopen: NO
Production refactor: NO

SelectionSemantics != AlterationGenerator
SelectionSemantics != RealityGrounding
AlternativeDomainExtension != SelectionSolution
FormalExpressiveEquivalence != GroundingEquivalence
CausalModelStructure != CounterfactualGeneratorPolicy
UniqueNearestAlternative as universal foundation: REJECTED
GlobalSimilarityMetric as universal foundation: NOT EARNED
Unconstrained pluralism: REJECTED
Typed generator/selector contract: EARNED AS RESEARCH META-ARCHITECTURE

Exact next round:
WDF2-D — Counterfactual Generator Grounding / Admissibility / Query-Role Separation
```

Compressed result:

> **WDF2-C does not find one winning universal counterfactual semantics. More importantly, it finds that the apparent competitors are architecturally heterogeneous. Stalnaker and Lewis mainly specify selection; premise semantics specifies background revision; forward, backtracking and nondeterministic SCMs specify structured generators; law/chance and powers offer candidate Reality-facing grounding; impossible worlds extend the alternative domain; pluralism is a meta-level routing proposal. These components can sometimes compose or emulate one another, so expressive equivalence cannot settle foundational adequacy. The common unresolved question survives every family in a different location: what makes this generator, ordering, premise set, surgery, coupling or impossible alternative the legitimate one for this query? WDF2 therefore advances not to a premature winner, but to generator grounding and admissibility.**
