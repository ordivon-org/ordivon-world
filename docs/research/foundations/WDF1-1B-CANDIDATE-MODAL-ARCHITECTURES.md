# WDF1-1B — Candidate Modal Architectures

Status: complete for WDF1-1B. No final World-level modal ontology is frozen. The four architectures admitted by WDF1-1A are formalized and deletion-tested against the A1–A24 separation suite. Three are demoted to local/projection roles. A fifth reconstructed candidate — **Typed Alternative-Relation Architecture (TARA)** — survives as the smallest common meta-architecture so far, but remains provisional until WDF1-1C–F attack law/background, control, epistemic/objective and counterfactual interfaces. Exact next sub-round: **WDF1-1C — Law / Initial Condition / Boundary Condition / Constraint Separation**.

## 0. Question

WDF1-1A proved that the following cannot be universally collapsed:

```text
nomological possibility
reachability from actuality
Actor control
resource feasibility
access
authorization
epistemic openness
probability/chance
selection/realization
```

The remaining question is architectural:

> Are these merely unrelated predicates, different coordinates of one vector, nested restrictions of one possible-world set, or different operators over a more general alternative structure?

WDF1-1B compares the four survivors from A and attempts destructive reconstruction.

## 1. Requirements for a successful architecture

A candidate must reconstruct at least:

### Q1 — objective/epistemic divergence

```text
E_A(T)=true while R(T)=false
R(T)=true while E_A(T)=false
```

### Q2 — feasibility/authorization two-way independence

```text
F_A(T)=true,  U_A(T)=false
F_A(T)=false, U_A(T)=true
```

### Q3 — passive reachability vs strategic control

```text
there exists a path to T
!=
Actor A has a policy/strategy ensuring/causing T under the declared criterion
```

### Q4 — constitutive authorization

The architecture must represent the fact that a rule/status can change what an act **counts as**, not merely remove one physical trajectory from a set.

### Q5 — probability beyond Boolean possibility

A possible outcome can carry a nontrivial probability/chance value.

### Q6 — dependence binding

Horizon, actual state, input/action set, policy class, observation structure, institution/rules, evidence/model and event space must be explicit when relevant.

### Q7 — local entailment without universal collapse

The architecture should allow results such as:

```text
Reachable_under_law_conforming_transitions(T)
=> NomologicallyPossible(T)
```

without requiring:

```text
Authorized(T) => PhysicallyPossible(T)
```

or another false universal implication.

### Q8 — counterfactual compatibility

A later counterfactual theory must be able to state:

```text
which alternatives are generated
what changes
what remains invariant
which relation/operator evaluates the consequent
```

### Q9 — explanatory localization

If a target is not actionable, the architecture should preserve whether the blocker is:

```text
law/dynamics
initial condition/horizon
control interface
resource/capacity
access/path
authority/rule
evidence/model
```

A mathematically unified representation that erases this distinction fails Ordivon's action-localization requirement.

## 2. Rival A — Universal Nested Modal Filters

### 2.1 Basic form

The strongest version assumes one universe of alternatives `Ω` and a chain of increasingly restrictive subsets:

```text
Ω
⊇ Ω_nomological
⊇ Ω_reachable
⊇ Ω_controllable
⊇ Ω_feasible
⊇ Ω_accessible
⊇ Ω_authorized
⊇ Ω_selected
```

Then `T is M-possible` means some alternative in the corresponding set satisfies T.

This is attractive because actionability often does look like accumulating requirements.

### 2.2 Strengths

- compact;
- naturally models conjunction of restrictions;
- easy to compute in finite planning/search spaces;
- captures many local pipelines such as:

```text
candidate actions
→ physically executable
→ within budget
→ interface currently reachable
→ policy-admissible
```

- supports set inclusion and monotonic pruning.

### 2.3 A8/A9 falsifier — authorization and feasibility are not nested

WDF1-1A constructed:

```text
A8: authorized but infeasible
A9: feasible but unauthorized
```

Therefore no universal order:

```text
Ω_authorized ⊆ Ω_feasible
```

or:

```text
Ω_feasible ⊆ Ω_authorized
```

survives.

One can replace the chain with a lattice/intersection of independent filters, but that abandons the defining claim of universal nesting.

### 2.4 A11/A12 falsifier — epistemic alternatives are not an objective subset chain

An Agent can consider an objectively impossible alternative live, or falsely rule out an objectively possible alternative.

Thus:

```text
Ω_epistemic(A)
```

is not in general a subset or superset of:

```text
Ω_objective
```

It is a different Agent/model/evidence-relative relation.

### 2.5 A10/A17 falsifier — constitutive modality is not merely physical exclusion

If the exact same local physical act counts as a valid authorization in one rule/status context and invalid in another, a pure filter model can represent the output extensionally but misses the explanatory relation:

```text
rule/status + act
constitutes valid institutional act
```

The problem is not inability to encode the extension. Any sufficiently rich set representation can encode almost anything. The failure is **role flattening**.

### 2.6 Deletion test

Delete universal nesting and retain only:

```text
independent typed filters/intersections where the query earns them.
```

Nothing important from A1–A24 is lost.

### 2.7 Disposition

```text
UNIVERSAL NESTED FILTER ARCHITECTURE: REJECTED.
LOCAL CONJUNCTIVE FILTER PIPELINES: RETAINED.
```

Nested filtering is an implementation/planning pattern, not the World-level modal foundation.

## 3. Rival B — Product / Vector ModalProfile

### 3.1 Basic form

For target T and Actor A:

```text
ModalProfile_A,Q(T)
= <N, R, C, F, X, U, E, P>
```

where components represent nomological possibility, reachability, control, feasibility, access, authorization, epistemic openness and probability/chance.

### 3.2 Strengths

- faithfully preserves A1–A24 independence;
- easy to inspect and compare;
- naturally supports UNKNOWN/stale values;
- useful as a diagnostic projection;
- makes hidden modal dependencies visible.

### 3.3 Weakness B1 — it promotes derived coordinates to apparent peers

A1–A5 already suggest:

```text
R, C, F
```

can partly be reconstructed from one transition/reachability structure under different input/constraint sets.

A flat vector silently treats them as primitive independent axes.

### 3.4 Weakness B2 — no semantics for why one coordinate has its value

A vector says:

```text
F=false
```

but does not itself represent whether the failure comes from:

- energy;
- capital;
- required complement;
- timing;
- compatibility.

Likewise:

```text
U=false
```

does not explain which rule/status relation constitutes the refusal.

### 3.5 Weakness B3 — cross-coordinate entailments are external knowledge

The vector alone does not encode that under a declared law-conforming transition relation:

```text
R => N
```

or that some feasibility definition entails a corresponding restricted control reachability claim.

One must add external rules until the vector starts becoming a structured relation system.

### 3.6 Weakness B4 — probability is not naturally one scalar peer

`P` requires:

```text
sample/event space
sigma algebra or event algebra where applicable
probability/chance assignment
conditions/model
```

A single `P` coordinate without those objects is underspecified.

### 3.7 Deletion test

Delete the vector as foundation and recompute it from typed relations/operators when useful.

A1–A24 distinctions remain expressible.

### 3.8 Disposition

```text
VECTOR AS FOUNDATION: REJECTED.
VECTOR AS DIAGNOSTIC/PROJECTION: RETAINED.
```

This mirrors WDF0's result for `State`: useful projection does not imply root ontology.

## 4. Rival C — Parameterized Reachability + Typed Constraints

### 4.1 Basic form

Use one general transition structure:

```text
Reach(
  anchor,
  target
  | transition relation,
    allowed inputs/actions,
    policy class,
    observation structure,
    disturbances,
    horizon,
    constraints
)
```

Then derive:

```text
natural reachability
Actor control reachability
resource-constrained reachability
access-limited reachability
```

by changing parameters.

### 4.2 External pressure: dynamic logic

Propositional Dynamic Logic associates modalities with programs/actions and interprets program execution through relations among states. This is strong evidence that one useful modal pattern is not `possible simpliciter`, but:

```text
possible/reachable after execution relation α
```

The modal operator is indexed by a transition-generating object.

### 4.3 External pressure: strategic/alternating-time logic

Alternating-time temporal logic goes further: ordinary path existence and the ability of a coalition/Agent to enforce temporal outcomes are distinct because strategic quantification ranges only over paths compatible with a strategy while other players/environment retain choices.

This strongly supports WDF1-1A's distinction:

```text
∃ path to T
!=
∃ strategy_A such that ∀ relevant environment continuations, T
```

Control is therefore naturally more structured than path existence.

### 4.4 Strengths

- high compression for dynamic/action modality;
- makes actual state, horizon and action/input set explicit;
- naturally represents passive vs controlled reachability;
- can absorb resource/capacity limitations as restrictions on allowed actions/transitions;
- supports planning, model checking and control;
- gives counterfactuals an operational alternative generator when the antecedent corresponds to a changed input/policy/system relation.

### 4.5 Weakness C1 — epistemic modality is not objective transition reachability

One could create an `epistemic accessibility relation` among world descriptions, but this relation is not generated by physical dynamics. At that point `reachability` has been generalized to mean any accessibility relation.

The generalization may be useful, but the word `reachability` becomes misleading.

### 4.6 Weakness C2 — deontic/institutional modality can be constitutive

Permission/authorization can be represented extensionally by restricting an action set:

```text
AllowedActions_A^institution
```

This is excellent for operational planning.

But it does not by itself represent why an act is valid/authorized, especially where:

```text
rule + role + act
constitutes status/action-kind
```

rather than merely blocks an otherwise identical physical transition.

### 4.7 Weakness C3 — nomological possibility can exceed state-transition reachability

If lawhood is global/all-at-once, variational, boundary-based or otherwise not fundamentally a local update rule, representing nomological possibility as graph reachability can already bias WDF1 toward dynamical law theories.

This is prohibited by WDF1-0.

### 4.8 Weakness C4 — chance requires measure, not only graph connectivity

A stochastic transition system can attach probabilities to edges/paths, but connectivity alone does not encode them.

### 4.9 Deletion test

Delete `Reachability` as universal modal genus but retain:

```text
transition/accessibility relations indexed by type
```

plus query-specific quantifiers/strategy operators.

Everything valuable survives while physical-dynamical bias decreases.

### 4.10 Disposition

```text
PARAMETERIZED REACHABILITY AS UNIVERSAL MODALITY: REJECTED.
PARAMETERIZED TRANSITION/ACCESSIBILITY RELATIONS: STRONGLY RETAINED.
```

This is the strongest surviving structural contribution among A–D.

## 5. Rival D — Typed Modal Pluralism

### 5.1 Basic form

Keep independent relations:

```text
NomologicallyPossible(...)
Reachable(...)
ControllableBy(...)
FeasibleFor(...)
AccessibleBy(...)
AuthorizedFor(...)
EpistemicallyOpenFor(...)
Chance(...)
```

and add only local laws where earned.

### 5.2 Strengths

- passes all A1–A24 cases by construction;
- preserves explanatory provenance;
- avoids physicalizing institutions;
- avoids treating Agent belief as Reality;
- prevents false total orders.

### 5.3 Weakness D1 — under-compression

It misses obvious shared structure:

```text
possible/necessary
reachable/unreachable
known/open
permitted/forbidden
```

all reason over alternatives under some typed relation or evaluation.

Historical modal logic provides strong mathematical evidence that many such operators can share a relational semantics without sharing one ontological relation.

### 5.4 Weakness D2 — duplicated machinery

If every modal family independently reinvents:

```text
alternative set
accessibility relation
existential/universal quantification
scope
context
```

then pluralism preserves nouns at the cost of repeated structure.

### 5.5 Weakness D3 — weak composition theory

Agent actionability requires combining several relations without collapsing them. Bare pluralism says they differ but does not explain composition.

### 5.6 Deletion test

Delete independent bespoke modal machinery while retaining typed relation identity and local semantics.

The distinctions survive under a common higher-order frame.

### 5.7 Disposition

```text
UNCONSTRAINED/BARE MODAL PLURALISM: REJECTED.
TYPED SEMANTIC PLURALITY: RETAINED.
```

The remaining problem is to share structure without declaring shared ontology.

## 6. Reconstruction pressure from Kripke-style relational semantics

Kripke's modal semantics is a decisive architectural clue, not because WDF1 must adopt possible-world metaphysics, but because it demonstrates a general mathematical form:

```text
Frame = <W, R>
```

where modal truth at one point is evaluated relative to alternatives accessible through `R`.

Different frame conditions yield different modal logics.

More importantly for WDF1, multimodal extensions can use different accessibility relations:

```text
R_1, R_2, ..., R_n
```

over a shared or related domain without identifying the modalities.

This gives a clean meta-lesson:

```text
Shared relational form != shared accessibility relation
Shared accessibility syntax != shared ontology
```

## 7. Dynamic logic adds typed transition generators

Dynamic logic replaces one undifferentiated modal relation with program/action-indexed modalities.

Conceptually:

```text
<α> φ
```

asks whether some execution of program/action relation `α` can lead to a state satisfying `φ`, while box-style forms quantify over all relevant executions.

This directly motivates:

```text
Modal operator
+ typed relation/generator
+ quantifier
```

as a more fundamental architecture than one scalar `Possible`.

## 8. ATL adds strategic quantification

Alternating-time temporal logic shows a second extension is required for agency:

```text
path quantification
```

is not enough.

A coalition's ability is evaluated through strategy-controlled sets of paths in the presence of other agents/environment choices.

This suggests a generic modal claim may require an **operator**, not merely an accessibility edge:

```text
∃ path
∀ path
∃ strategy_A ∀ environment continuation
probability ≥ p
permitted by rule system
compatible with Agent evidence
```

The quantificational shape itself is part of the modality.

## 9. Epistemic logic adds observer-relative alternative sets

Formal epistemic models treat an Agent's knowledge/uncertainty through alternatives compatible with its information/local state.

Fagin/Halpern/Vardi and later runs-and-systems work repeatedly show that properties of knowledge depend on system assumptions such as determinism, memory and environment effects.

For WDF1 this supports:

```text
E_A(T)
```

as an Agent/information-indexed alternative relation rather than an objective physical modal subset.

The architecture can reuse relational machinery without collapsing:

```text
R_epistemic(A)
```

into:

```text
R_physical
```

## 10. Deontic logic provides a historical warning against alethic collapse

Von Wright's 1951 work helped establish deontic logic as a distinct modal family for obligation/permission/prohibition rather than simply physical possibility.

Later deontic systems vary on whether operators apply primarily to propositions/states or actions, and agency-oriented deontic logic explicitly distinguishes `what ought to be` from `what an Agent ought to do`.

WDF1 therefore retains:

```text
permission/authorization modality
```

as type-specific even if it can sometimes be encoded through possible-world/action accessibility structures.

## 11. Fifth reconstructed candidate — Typed Alternative-Relation Architecture (TARA)

The four rivals suggest a smaller common structure.

WDF1-1B introduces, provisionally:

# **TARA — Typed Alternative-Relation Architecture**

This is a research grammar, not a production schema and not a possible-world metaphysics.

### 11.1 Core form

A modal claim is evaluated relative to a typed alternative structure:

```text
ModalClaim_τ(
  anchor,
  target/proposition,
  AlternativeDomain_τ,
  RelationOrGenerator_τ,
  Operator_τ,
  Background/Dependence_τ
)
```

Compressed notation:

```text
M_τ[Q, R, B](φ | a)
```

where:

```text
τ = modal type
Q = quantifier/operator
R = typed accessibility/transition/evaluation relation
B = declared background/dependence structure
φ = target condition/claim
a = actual/epistemic/institutional anchor where relevant
```

### 11.2 AlternativeDomain is typed

It need not always be `possible worlds`.

Depending on the question it can be:

```text
complete histories
physical configurations
state trajectories
program executions
Actor policies
resource assignments
actions
institutional status alternatives
world descriptions compatible with evidence
measurement outcomes
```

The architecture therefore avoids turning one representational ontology into Reality ontology.

### 11.3 Relation/generator is typed

Examples:

```text
R_nom     — law/admissibility relation or admissible-history condition
R_dyn     — system transition relation from actuality
R_prog(α) — program/action execution relation
R_ctrl(A) — Actor/coalition strategy-compatible outcome relation
R_res(A)  — resource/capacity-constrained transition relation
R_access  — path/interface coupling relation
R_epi(A)  — evidence/information compatibility relation
R_deon(I) — institution/rule/permission evaluation/accessibility relation
```

No equality among these is presumed.

### 11.4 Operator is typed

Examples:

```text
∃ alternative      — possibility/existence
∀ alternatives     — necessity/guarantee
∃ path             — reachability
∃ policy           — some Actor policy can attain target
∃ policy ∀ disturbances/opponents — robust/strategic control
RuleStatus(action) — permitted/forbidden/obligatory/authorized
μ(event)=p          — probability/chance assignment
compatible-with-evidence — epistemic openness
```

This is why one common `Possible` predicate is too weak.

## 12. TARA reconstruction of A1–A24

### A1 — law-compatible but unreachable from actual state

```text
R_nom admits histories containing state 3.
R_dyn from actual 0 under +2 dynamics does not reach 3.
```

Same target, different typed relation.

### A3 — passive reachability without control

```text
∃ path under R_dyn reaches T.
No Actor-indexed strategy operator over R_ctrl(A) gives A difference-making control.
```

### A5 — abstract control but resource infeasibility

```text
R_ctrl^abstract(A) admits target policy.
R_res^current(A) removes required action magnitudes/budget.
```

The architecture shares transition machinery but keeps exclusion provenance.

### A6 — feasible but inaccessible

Resource assignment/owner relation supports target, while current interface/path relation has no execution path.

### A7/A9 — accessible/feasible but unauthorized

```text
R_access succeeds.
R_deon/rule evaluation rejects authorization.
```

No false nesting required.

### A8 — authorized but infeasible

Rule evaluation grants status, while resource/physical transition relation lacks a realization path.

### A10/A17 — constitutive authorization

TARA does **not** force deontic status to be represented only as edge deletion.

The deontic relation may include a constitutive evaluator:

```text
K_I(role, act, context)
→ institutional act/status
```

and permission/authorization is then evaluated over that institutional status/action space.

This is a crucial extension beyond naive Kripke/filter semantics.

### A11/A12 — epistemic/objective mismatch

```text
R_epi(A)
```

can include alternatives excluded by `R_nom/R_dyn`, or omit alternatives admitted by them, because it is evidence/model-relative.

### A13–A15 — probability and uncertainty

TARA separates:

```text
Support/EventDomain
Relation/admissibility
Measure μ
Agent evidence relation
```

so probability does not collapse to possibility and epistemic uncertainty does not collapse to chance.

## 13. TARA does not mean all modalities are the same thing

This firewall is essential:

```text
Same Meta-Architecture
!= Same Modal Relation
!= Same Ontology
!= Same Truthmaker
```

A deontic permission relation and physical transition relation can both be represented using alternative structures while being constituted by very different Reality facts.

The analogy is similar to:

```text
graph representation of a road network
and
graph representation of a social network
```

The shared graph formalism does not imply roads and friendships are one relation type.

## 14. What exactly is shared under TARA?

Only this minimal structure:

```text
1. a target/modal question;
2. a declared domain of alternatives;
3. a typed relation/generator/evaluator connecting or classifying alternatives;
4. an operator/quantifier/measure over those alternatives;
5. explicit background/dependence conditions;
6. an anchor such as actuality, Actor information state, institution or current system state where relevant.
```

This is weaker than a universal metaphysics of possible worlds.

## 15. Possible and Necessary become operator forms, not root properties

Under TARA:

```text
Possible_τ(φ | a)
≈ ∃ τ-admissible/accessibile alternative satisfying φ

Necessary_τ(φ | a)
≈ ∀ relevant τ-admissible/accessibile alternatives, φ
```

The crucial word is `τ`.

Thus:

```text
physically possible
epistemically possible
institutionally permitted
```

can share quantificational form while differing in relation/domain/background.

## 16. Reachability becomes a path-structured special case

For transition modalities:

```text
Reachable_R(a, T, H)
≈ ∃ R-path from anchor a to target T within horizon H.
```

This is a derived operator over transition structure.

### Result

`Reachability` does not need to be a universal modal primitive.

It is a particularly important **path modality**.

## 17. Control becomes a strategy-structured special case

For agency:

```text
CanForce_A(T)
≈ ∃ policy/strategy π_A
   such that ∀ admitted opponent/disturbance/environment continuations,
   target criterion T holds.
```

Other weaker notions can use:

```text
∃ policy ∃ continuation
```

or probability thresholds.

Thus `Control` is not reducible to one fixed Boolean relation without declaring:

```text
policy class
observation structure
environment/opponent choices
success criterion
horizon
robustness/probability threshold
```

## 18. Feasibility becomes composition over typed constraints, not one modality

Resource feasibility can be reconstructed as a query over a transition/assignment alternative space with constraints such as:

```text
quantity
capacity
compatibility
time
required complements
```

But WDF1-1B retains the **reason labels** for failed feasibility because different blockers imply different actions.

Thus:

```text
Feasible(T)
```

is a derived conjunction/query result, while the underlying constraint families remain typed.

## 19. Access becomes coupling/interface reachability

Access is a strong candidate for reduction to a special relation:

```text
R_access(A, target, interface/path, time)
```

It asks whether the Actor's current embodiment/tool/network/interface is coupled to the target sufficiently to attempt the relevant operation.

### Provisional result

```text
Access likely does not require an independent root modal category.
```

It survives as a typed coupling/reachability relation because its failure provenance remains action-relevant.

This is not yet frozen; WDF1-1D can still attack it.

## 20. Authorization requires both constitutive and modal structure

Authorization cannot safely be reduced to:

```text
edge exists / edge absent
```

A stronger reconstruction is:

```text
Reality facts
+ institution/rule system
+ Actor role/status
+ action/context
→ constitutive institutional act/status
→ deontic evaluation: permitted / forbidden / authorized / obligatory / invalid
```

Then planning can project that result back into an allowed-action relation.

Thus there are two levels:

```text
ConstitutiveStatusLayer
→ DeonticModalProjection
```

This is exactly parallel to WDF0's principle that one thing can occupy multiple roles without role collapse.

## 21. Epistemic openness is a modal projection over model/evidence compatibility

For Agent A:

```text
Alt_epi(A)
= world/model alternatives compatible with A's current evidence/awareness/model assumptions.
```

Then:

```text
EpistemicallyPossible_A(φ)
≈ ∃ compatible alternative where φ.
```

But WDF1 must preserve open-world structural revision:

```text
Current epistemic alternative set
!= all possibilities the Agent could ever learn to represent.
```

This is an important limitation of ordinary fixed-language possible-world epistemic models and will matter when WDF1 returns to structural model revision.

## 22. Probability/chance is a measure layer, not another accessibility Boolean

For a declared event space:

```text
Ω_τ
F_τ
μ_τ
```

one can evaluate:

```text
μ_τ(event) = p.
```

This structure can coexist with modal support:

```text
Support(μ)
```

but cannot be reconstructed from Boolean support alone.

Therefore:

```text
Probability/ChanceLayer
is orthogonal to bare accessibility.
```

The ontology of `μ` — objective chance, best-system probability, propensity, epistemic credence, model probability — remains unresolved.

## 23. Why TARA is not just Vector Profile in disguise

Vector architecture stores answers:

```text
<N,R,C,F,X,U,E,P>
```

TARA stores/reconstructs the **structures and operators that generate those answers**.

The profile can then be computed as a view:

```text
TARA structures
→ evaluate selected modal queries
→ ModalProfile projection
```

Thus:

```text
TARA -> VectorProjection
```

but not vice versa without reconstructing hidden structure.

## 24. Why TARA is not Nested Filters in disguise

TARA permits local composition:

```text
R_actionable
= intersection/composition of selected typed relations
```

when the query requires it.

But there is no universal subset order among:

```text
R_nom
R_epi
R_deon
R_access
R_resource
```

Thus nested filters become a derived local optimization.

## 25. Why TARA is not Reachability in disguise

Transition/path relations are only one relation family.

TARA also admits:

```text
evidence compatibility
constitutive rule/status mappings
deontic evaluation
probability measures
```

without relabeling all of them `reachability`.

## 26. Why TARA is not bare pluralism

TARA compresses shared machinery:

```text
alternative domain
anchor
relation/generator/evaluator
operator/quantifier/measure
background/dependence
```

while preserving type-specific semantics.

That is exactly the middle position WDF1-1B was searching for.

## 27. Architecture scorecard

Scale: 0 = fails badly, 1 = weak, 2 = adequate with caveats, 3 = strong.

| Criterion | Nested filters | Vector | Param. reachability | Typed pluralism | TARA |
|---|---:|---:|---:|---:|---:|
| A1–A24 independence | 1 | 3 | 2 | 3 | 3 |
| Compression | 3 | 1 | 3 | 0 | 3 |
| Dynamic/control semantics | 2 | 0 | 3 | 2 | 3 |
| Epistemic/objective separation | 0 | 3 | 1 | 3 | 3 |
| Constitutive authorization | 1 | 2 | 1 | 3 | 3 |
| Probability structure | 1 | 1 | 2 with stochastic extension | 3 | 3 |
| Local entailment/composition | 3 | 1 | 3 | 1 | 3 |
| Explanatory provenance | 1 | 1 | 2 | 3 | 3 |
| Low ontology bias | 1 | 2 | 1–2 | 3 | 3 |
| Counterfactual extensibility | 2 | 1 | 3 for action cases | 2 | 3 |

This table is heuristic research scoring, not empirical measurement.

## 28. Deletion test on TARA itself

WDF1-1B now attempts to remove each proposed TARA component.

### Remove AlternativeDomain

Then `possible/necessary`, probability support and epistemic compatibility lack a declared universe of alternatives.

**Fails.**

### Remove typed Relation/Generator/Evaluator

Then physical dynamics, epistemic compatibility and deontic rules collapse into one undifferentiated accessibility relation.

**Fails A7–A12/A17.**

### Remove Operator/Quantifier

Then path existence, universal guarantee, strategic control and probability threshold collapse.

**Fails A3/A22/A13.**

### Remove Background/Dependence

Then horizon, actual state, policy class, evidence and institution become hidden assumptions.

**Fails A2 and WDF0 Dependence discipline.**

### Remove Anchor

Some purely global necessity claims may not need a distinguished actual anchor, but reachability, epistemic state and current actionability do.

Therefore anchor is **optional by modal type**, not universal mandatory data.

### Result

The currently irreducible meta-structure is closer to:

```text
AlternativeDomain
+ typed Relation/Generator/Evaluator
+ typed Operator/Measure
+ Background/Dependence
(+ Anchor when the modal question is anchor-relative)
```

## 29. New distinction — Alternative Space vs Alternative Generator

WDF1-1B finds these must separate.

An alternative space can be defined extensionally:

```text
Ω = set/class of alternatives
```

while a generator defines how alternatives are produced/reached/constructed:

```text
G(anchor, action, intervention, rule change, model variation)
→ alternatives
```

For counterfactual and Agent reasoning, the generator matters because arbitrary logically describable alternatives are often not the intended comparison set.

Thus:

```text
AlternativeSpace != AlternativeGenerationRule
```

This becomes a key bridge to counterfactual theory.

## 30. New distinction — Admissibility vs Accessibility

Another compression trap:

```text
admissible
```

can mean an alternative belongs to the relevant modal base, while:

```text
accessible from anchor
```

means there is a declared relation/path from the anchor to it.

A state can be nomologically admissible yet inaccessible/reachable from the actual state.

Therefore:

```text
Admissible_τ(x)
!=
Accessible_τ(anchor,x)
```

This restates A1 at the architecture level.

## 31. New distinction — Evaluation vs Generation

Institutional authorization gives the cleanest witness.

The rule system may evaluate an already physically realized/possible act:

```text
Evaluate_I(act, role, context)
→ authorized / unauthorized / valid / invalid
```

without generating the physical act.

Hence TARA must allow:

```text
Generator relation
```

and:

```text
Evaluator/constitutive relation
```

as distinct subroles.

This may later matter for value/normative systems beyond permission.

## 32. New distinction — Possibility support vs weight

For probability/chance:

```text
Support(μ)
```

answers which events/outcomes receive positive or otherwise admitted probability mass/density support under the formalism.

```text
μ(E)
```

answers how weight is distributed.

Thus:

```text
Support != Weight
```

and even `probability zero` requires care in continuous spaces, where individual outcomes may have zero measure without being excluded from the support.

WDF1-1B therefore refuses a naive rule:

```text
P(E)=0 => impossible
```

without specifying the probability/chance formalism.

## 33. Entailments under TARA are type-conditional

Instead of universal ladders, WDF1 should state conditional entailments.

Example:

```text
IF R_dyn contains only law-admissible transitions
AND target T is reached by an R_dyn path,
THEN T is nomologically possible under that model.
```

This is:

```text
R_dyn-path(T) => N_model(T)
```

under explicit assumptions.

Likewise:

```text
IF Feasible_A(T)
means there exists an A-policy satisfying current resource constraints,
THEN Feasible_A(T) => ControlReachable_A(T)
```

under that definition.

No implication is exported beyond its typed premises.

## 34. Modal composition becomes relation/operator composition

Actionability can now be represented without pretending all modal roles are one kind.

Conceptually:

```text
Target T
  must pass/evaluate through:

physical/nomological admissibility
+ current-state reachability
+ Actor policy/control relation
+ resource constraint evaluation
+ access/coupling relation
+ institutional status/evaluation
+ evidence/currentness admission for decision
```

The result may be a conjunction for one decision, but the underlying structures remain separately typed.

This is a more rigorous version of current Ordivon Resource/Option doctrine.

## 35. Modal failure provenance becomes a first-class research requirement

Given:

```text
Actionable(T)=false
```

TARA requires preserving the failed relation/operator:

```text
N failure     — theory/law conflict
R failure     — current trajectory/horizon conflict
C failure     — Actor policy/control conflict
F failure     — resource/capacity/compatibility conflict
X failure     — path/interface conflict
U failure     — authority/rule/status conflict
E failure     — evidence/model uncertainty or exclusion
```

The modal architecture therefore supports remediation localization without creating one production `ModalFailure` object.

## 36. TARA and WDF0 Dependence Signature

TARA can be understood as specializing WDF0's Dependence discipline.

A modal claim should bind relevant coordinates such as:

```text
actual anchor
laws/background
initial/boundary conditions
transition/generator
horizon
action/input/policy set
Actor/coalition
resources/load
interface/path
institution/rules/role
evidence/model/awareness
event space/probability measure
```

Thus modal truth is often:

```text
M_τ(φ | DependenceSignature)
```

not context-free `possible(φ)`.

## 37. TARA and Reality/model separation

A critical firewall:

```text
AlternativeStructureInModel
!=
Reality's complete modal structure
```

A model can:

- omit physically possible alternatives;
- include impossible alternatives;
- use wrong transition relations;
- use wrong rule/status representation;
- assign wrong probabilities.

Therefore WDF1 must distinguish:

```text
ObjectiveModalClaim
from
ModelModalProjection
```

just as WDF0 distinguished Reality from State/Model.

## 38. Open-world problem — fixed alternative sets can be incomplete

Standard modal models normally start with a defined language/state/world set.

But Ordivon explicitly needs structural model revision.

An Agent may later discover:

```text
new action type
new entity
new mechanism
new rule
new sensor
new variable
new outcome category
```

that was absent from its previous alternative domain.

Hence:

```text
CurrentAlternativeDomain_A
!=
AllRealityPossibilities
```

This is an important reopen pressure on any possible-world-style formalism used operationally.

TARA handles this only meta-theoretically by allowing the alternative domain itself to be revised. A complete formal theory of domain expansion is not yet provided.

## 39. Why metaphysical possibility remains unresolved

TARA can represent a `τ=metaphysical` relation/operator if WDF1 later earns one.

But WDF1-1B has no case requiring a distinct metaphysical modal relation beyond:

- logical consistency;
- nomological/physical possibility;
- constitutive identity/essence questions.

Therefore:

```text
MetaphysicalPossibility remains OPEN, not promoted.
```

The architecture must not bake it in as mandatory.

## 40. Strongest conclusion of B

The best current compression is not:

```text
one set of possible worlds
```

nor:

```text
one reachability graph
```

nor:

```text
one vector of modal booleans
```

nor:

```text
completely unrelated modal predicates.
```

It is provisionally:

```text
A family of typed alternative structures
sharing a small meta-grammar:

Alternative Domain
+ Typed Relation / Generator / Evaluator
+ Typed Operator / Quantifier / Measure
+ Explicit Background / Dependence
+ Anchor when relevant
```

This gives common structure without common ontology.

## 41. WDF1-1B anti-laws

1. `UniversalNestedModalChain != ModalArchitecture`.
2. `ModalVector != ModalSemantics`.
3. `Reachability != UniversalModality`.
4. `TypedPlurality != NoSharedStructure`.
5. `SharedRelationalForm != SharedOntology`.
6. `PossibleWorldRepresentation != PossibleWorldMetaphysics`.
7. `Admissible != AccessibleFromActuality`.
8. `AlternativeSpace != AlternativeGenerator`.
9. `Generation != Evaluation`.
10. `PhysicalTransitionRelation != EpistemicAccessibilityRelation`.
11. `PhysicalTransitionRelation != DeonticConstitutiveRelation`.
12. `PathExistence != StrategicControl`.
13. `StrategicControl != ResourceFeasibility` by default.
14. `AuthorizationProjection != PhysicalTrajectoryFilter` by default.
15. `ProbabilityWeight != PossibilitySupport`.
16. `ProbabilityZero != Impossible` without formal context.
17. `CurrentModelAlternativeDomain != CompleteRealityPossibilitySpace`.
18. `SameMathematicalAccessibilityPattern != SameTruthmaker`.
19. `LocalModalEntailment != UniversalModalLadder`.
20. `ActionabilityConjunction != OneConstraintOntology`.

## 42. Architecture dispositions

### Rival A — Nested filters

```text
Universal: REJECT
Local actionability/planning filter: RETAIN
```

### Rival B — Vector profile

```text
Foundation: REJECT
Diagnostic/projection: RETAIN
```

### Rival C — Parameterized reachability

```text
Universal modality: REJECT
Dynamic/control/access subkernel: STRONGLY RETAIN
```

### Rival D — Typed pluralism

```text
Bare/no-shared-structure version: REJECT
Semantic type plurality: RETAIN
```

### Reconstructed Rival E — TARA

```text
Typed Alternative-Relation Architecture:
PROVISIONAL WINNER FOR WDF1-1B
NOT FROZEN UNTIL WDF1-1C–F
```

## 43. External evidence retained in B

Primary/authoritative pressure used:

- Saul Kripke, 1963 modal-semantic work: relational frames/accessibility as a general semantics for modal operators.
- Fischer & Ladner, *Propositional Dynamic Logic of Regular Programs* (1979): program-indexed modal transition relations and program execution semantics.
- Alur, Henzinger & Kupferman, *Alternating-Time Temporal Logic* (JACM 2002): selective/strategic path quantification, separating path possibility from coalition ability.
- Kalman 1960 control-system work: controllability depends on system/input structure rather than bare state possibility.
- Fagin, Halpern, Moses & Vardi work on epistemic models/runs-and-systems: Agent knowledge/possibility depends on information/system assumptions and can be modeled separately from objective system transitions.
- G. H. von Wright, *Deontic Logic* (Mind 1951): deontic modality as a distinct formal family around obligation/permission/prohibition.

These sources show reusable mathematical architecture across modal families, but none establishes that all modalities share one metaphysical accessibility relation.

## 44. Exact residual entering WDF1-1C

TARA now exposes a sharper unresolved than A did:

> For objective/physical modality, what determines `AlternativeDomain` and `R_nom`?

Current candidates include:

```text
laws of nature
initial conditions
boundary conditions
conservation relations
symmetries
global/variational constraints
material structure
contingent environmental conditions
```

WDF1 cannot evaluate Best-System, governing-law, powers or law-as-constraint theories while these roles remain mixed.

For example:

```text
x_{t+1}=x_t+2
```

might be called a law in a toy model, while:

```text
x_0=0
```

is an initial condition, and:

```text
x(T)=10
```

could be a boundary/target condition.

All three restrict histories, but not in the same explanatory/nomic role.

Therefore next exact sub-round:

# WDF1-1C — Law / Initial Condition / Boundary Condition / Constraint Separation

It must test:

```text
1. whether `restricts possible histories` is sufficient for lawhood;
2. local evolution laws vs global/all-at-once laws;
3. initial/boundary conditions vs laws;
4. conservation/symmetry constraints vs contingent constraints;
5. physical constraint vs resource/environment constraint;
6. law-relative reachability under deterministic/stochastic systems;
7. whether TARA's R_nom can be defined without already choosing a law metaphysics.
```

No law theory is selected in B.

## 45. WDF1-1B closeout

```text
WDF1-1B1 nested modal filters              COMPLETE — universal form rejected
WDF1-1B2 product/vector profile            COMPLETE — projection only
WDF1-1B3 parameterized reachability        COMPLETE — dynamic subkernel retained
WDF1-1B4 typed pluralism                   COMPLETE — type plurality retained
WDF1-1B5 destructive reconstruction        COMPLETE

Provisional reconstructed architecture:
TARA — Typed Alternative-Relation Architecture

TARA status: CANDIDATE, NOT FROZEN

Next:
WDF1-1C Law / Initial / Boundary / Constraint Separation
```
