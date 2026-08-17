# WDF2-D — Counterfactual Generator Grounding / Admissibility / Query-Role Separation

Status: **complete for WDF2-D**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A/B/C remain closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from WDF2-D residuals:

```text
WDF2-E — Counterfactual Underdetermination / Generator Disagreement / Robust Consequence
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-C discovered that the apparent rival counterfactual theories are not one-dimensional competitors.

They occupy different roles:

```text
selection / evaluation
structural alteration / generation
Reality-facing grounding
alternative-domain extension
meta-routing
```

The common residual was therefore not:

```text
Which named theory wins?
```

but:

> **What non-circular facts license generator G for query Q over domain/model D and truth role T?**

WDF2-D attacks that question.

The round must distinguish legitimate query sensitivity from arbitrary contextual tuning.

It must also preserve the WDF0/WDF1 firewalls:

```text
Reality != Model
Cause != Constraint != Constitution
ActionOccurrence != Intervention
PhysicalAbility != Authority
ProbabilityMeasure != ProbabilityInterpretation
ModelCounterfactual != RealityCounterfactualTruth
```

---

# 2. Initial danger — “context chooses” is not an answer

A common escape after WDF2-C is:

```text
Different contexts use different counterfactual semantics.
```

This is too weak.

`Context` can hide:

```text
speaker interest
question target
prediction task
planning task
diagnostic task
causal-attribution task
responsibility task
physical mechanism
institutional rule
program semantics
normality/default
model limitations
evidence limitations
```

These are not interchangeable.

Therefore:

```text
ContextSensitivity != OpaqueContextParameter
```

and:

```text
PragmaticInterest != TruthMaker
```

A user can choose which question to ask. Their interest does not thereby alter physical laws, program execution semantics, institutional constitutive rules or causal mechanisms.

---

# 3. First major result — admissibility is layered

WDF2-D falsifies the idea that there is one Boolean gate:

```text
AdmissibleCounterfactual(G,Q) -> yes/no
```

At least four distinct gates are required.

## 3.1 Semantic generator admissibility

Does G actually implement the intended kind of counterfactual contrast?

```text
SemAdmit(G | Frame, QueryRole, DomainSemantics, TruthRole)
```

This concerns:

```text
alteration locus
preservation profile
backtracking/forward direction
identity/correspondence
result shape
alternative-domain commitments
```

---

## 3.2 Representational adequacy

Can model M faithfully express the structures that the query and generator require?

```text
RepAdeq(M | Frame, Domain, QueryRole)
```

This concerns:

```text
missing variables
wrong grain
missing institutional status
missing mechanism
wrong policy representation
model-boundary error
```

A generator can be semantically appropriate while the current model is inadequate.

---

## 3.3 Epistemic / identification warrant

Do available evidence and assumptions identify or sufficiently support the claimed counterfactual quantity?

```text
Warrant(Result | Evidence, Model, Assumptions, TruthRole)
```

This concerns:

```text
identification
partial identification
sensitivity
parameter uncertainty
causal-model uncertainty
factual-unit coupling uncertainty
```

A semantic counterfactual can be well-defined but empirically unidentified.

---

## 3.4 Action / normative admissibility when relevant

If the counterfactual is being used for recourse, planning, responsibility or blame, additional gates become relevant.

```text
ActAdmit(Action | Actor, Ability, Authority, Access, Resource, Timing)

NormAdmit(Attribution | Rule, Duty, Default, Knowledge, Agency, Jurisdiction)
```

These must not be imported into purely physical consequence queries.

---

# 4. Earned firewall D-GATE-1

```text
GeneratorSemantics
!= ModelAdequacy
!= EmpiricalIdentification
!= Actionability
!= NormativeAttribution
```

This is the strongest structural result of WDF2-D.

A single word such as `valid`, `feasible`, `realistic` or `reasonable` must not collapse these gates.

---

# 5. Why this separation is not merely terminological

The literature supplies direct pressure.

Algorithmic-recourse work shows that a nearest feature-space counterfactual can describe where a prediction changes while failing to specify an intervention that the person can actually execute; causal recourse therefore shifts from nearest counterfactual states toward interventions and explicitly notes that reliable recourse cannot generally be guaranteed under imperfect causal knowledge.

Likewise, counterfactual MDP work shows that a formally generated counterfactual trajectory can gradually lose dependence on the factual episode and become effectively interventional rather than individualized.

Thus:

```text
DesiredOutcomeState != ActionableIntervention
FormalCounterfactualSample != AdequatelyIndividualizedCounterfactual
```

The distinction is structural, not stylistic.

---

# PART I — QUERY ROLE AS SEMANTIC CONTRACT

# 6. Query role is not mere user purpose

WDF2-D introduces `QueryRole` only under a strict interpretation.

It is **not**:

```text
whatever the user wants
```

It is a typed specification of what dependency relation the query is asking the counterfactual engine to expose.

A query role constrains:

```text
what may be altered
what should normally be preserved
which direction of accommodation is intended
which result shape is appropriate
which extra constraints may legitimately enter
```

### Earned firewall D-ROLE-1

```text
QueryRole != SubjectivePreference
```

A query role is closer to the semantic type of the question.

---

# 7. Minimal role family surviving deletion tests

WDF2-D does not claim the following family is eternally exhaustive.

It claims that deleting these distinctions destroys matched cases.

```text
ConsequenceUnderSpecifiedAlteration
DiagnosticAccommodation
Planning / Recourse
PolicyComparison
IndividualizedCounterfactualEvaluation
ActualCause / CausalAttribution
Explanation
Responsibility / Blame
Robustness / Sensitivity
ModelExploration / StructuralRevision
Counterpossible / CounterconventionalReasoning
```

Several can compose.

For example:

```text
policy comparison
+ individualized counterfactual evaluation
+ robustness
```

is coherent.

The family is a role grammar, not a Reality ontology.

---

# PART II — CONSEQUENCE VS DIAGNOSIS

# 8. Q-family — same antecedent, opposite accommodation direction

## Q1 — server health consequence

Anchor:

```text
deployment failed at t1
server unhealthy at t2
request r arrives at t3
```

Question:

```text
If the server had been healthy at t2, would r have succeeded?
```

### Role A — consequence under specified alteration

Interpretation:

```text
set/ensure health at t2
preserve upstream factual history as much as declared
propagate downstream
```

A local/forward generator can be admissible.

### Role B — diagnostic accommodation

Interpretation:

```text
assuming normal server mechanisms remain intact,
what earlier circumstances must have differed so health at t2 occurred?
```

A backtracking generator can be admissible.

These are different questions despite nearly identical surface language.

---

# 9. Admissibility principle Q-F1

```text
Forward generator is licensed when the antecedent is treated as a specified alteration whose consequences are the target.

Backtracking generator is licensed when the antecedent state is treated as a constraint to be naturally accommodated by changing upstream/background conditions while preserving the relevant mechanisms.
```

The distinction is grounded in **semantic role**, not in which answer feels intuitive.

Modern backtracking SCM work supports exactly this mechanical contrast: intervention-style semantics holds exogenous background fixed while altering local causal mechanisms; backtracking semantics holds causal laws/mechanisms fixed while allowing upstream/background states to differ.

---

# 10. Failure case — circular role selection

Rejected rule:

```text
Use backtracking when backtracking gives the plausible answer.
```

This is circular.

Accepted direction:

```text
The query asks for upstream accommodation under preserved mechanism.
Therefore a generator that preserves mechanism and varies upstream conditions is role-compatible.
```

The conclusion is testable before seeing the final answer.

---

# PART III — EXPLANATION VS RECOURSE / PLANNING

# 11. R-family — same desired output, different semantics

Anchor:

```text
classifier rejects applicant
feature vector x
causal domain model M
```

Question family:

```text
What would have to be different for approval?
```

This surface question is dangerously ambiguous.

---

# 12. R1 — contrastive/model explanation

A nearest state:

```text
x' such that classifier(x') = approve
```

can answer:

```text
Where is the decision boundary contrast?
```

This may be legitimate as a **model-explanatory** query.

It need not imply that x' is reachable by the Actor.

---

# 13. R2 — recourse/planning

Planning asks:

```text
Which available action/intervention can the Actor perform so that downstream consequences yield the desired result?
```

Now the generator must constrain alternatives by:

```text
Actor control
physical ability
authority
access
resource cost
time
causal downstream effects
institutional admissibility
```

Nearest feature perturbation is not enough.

Algorithmic-recourse research explicitly makes this distinction: counterfactual explanations can identify a desired state without telling an individual how to reach it; causal recourse instead targets minimal interventions/actions.

---

# 14. Earned firewall D-ACT-1

```text
CounterfactualExplanation != ActionRecommendation
DesiredState != ReachableState
ReachableState != ActorControllableState
ActorControllableState != AuthorizedAction
```

This imports WDF1 modal firewalls directly into counterfactual admissibility.

---

# 15. R3 — imperfect causal knowledge

Suppose the causal graph is known but structural equations are not.

A recourse generator can be semantically well-typed:

```text
intervene on actionable variables
```

but the exact individual outcome may not be guaranteed.

Research on recourse under imperfect causal knowledge shows precisely this: without the true structural equations, guaranteed individual recourse can fail, motivating probabilistic or subpopulation-level intervention criteria.

Therefore:

```text
SemAdmit(recoursive intervention generator) = possible
```

while:

```text
Warrant(guaranteed success) = insufficient
```

This is a direct empirical witness for D-GATE-1.

---

# PART IV — TOKEN ACTION VS POLICY CHANGE

# 16. P-family — planning granularity

Anchor:

```text
policy π
state trajectory τ
π(s_t)=a_t
```

Questions:

```text
P1: What if action a_t had been a'_t?
P2: What if the policy had been π'?
```

The first is a token-action counterfactual.
The second changes an action-generating mechanism over multiple states.

Policy-intervention research explicitly models the second as distinct from changing one fixed treatment/action sequence.

---

# 17. Admissibility consequence

A one-step intervention generator can be semantically valid for P1 and invalid for P2.

For P2, a generator must preserve the fact that later actions are generated under π', not continue factual π after the first changed action unless that is explicitly the query.

### Earned firewall D-POLICY-1

```text
ActionTokenChange != PolicyChange
```

and:

```text
GeneratorAdmissibility is alteration-grain sensitive.
```

---

# 18. Individualized policy counterfactuals

Off-policy counterfactual work uses factual episodes to construct alternative trajectories under changed policies.

Recent work shows an important failure mode: as a counterfactual trajectory diverges, the factual episode may cease to constrain the result, so the object becomes closer to a generic interventional rollout.

This demonstrates that `individualized` is a semantic obligation, not a decorative label.

A generator for an individualized query must expose its factual-counterfactual coupling and whether that coupling remains informative along the horizon.

---

# 19. Earned firewall D-IND-1

```text
InterventionalPolicyOutcome
!= IndividualizedCounterfactualPolicyOutcome
```

Even when both concern the same policy π'.

---

# PART V — CAUSAL ATTRIBUTION VS EXPLANATION

# 20. C-family — counterfactual dependence is not yet actual cause

Anchor:

```text
candidate event C occurred
effect E occurred
```

A simple dependence query asks:

```text
Had C not occurred, would E still have occurred?
```

But WDF2-B preemption/overdetermination cases already showed that this is insufficient for actual causation.

Actual-causation approaches use additional contingencies, structural simplification, normality or related machinery.

Therefore a generator admitted for:

```text
simple counterfactual dependence
```

is not automatically admitted as a complete generator for:

```text
actual causal attribution
```

---

# 21. Function-first pressure

Recent nondeterministic-causation work explicitly argues for developing actual-causation criteria from the function actual-cause information serves in communicating/learning causal structure rather than merely fitting case intuitions.

WDF2-D takes the methodological lesson, not the specific definition:

```text
QueryRole can provide independent design constraints.
```

That is better than:

```text
choose the definition matching intuition.
```

But function/purpose still cannot overwrite domain truth.

---

# 22. Explanation is another role

A causal explanation can depend on:

```text
actual cause
background uncertainty
contrast class
explanatory target
information available to the explainee
```

A model can therefore support:

```text
cause C of E
```

without C being the most useful explanation in a specific epistemic context.

### Earned firewall D-EXP-1

```text
Cause != Explanation
```

WDF0 already kept Reality separate from representation/epistemic access; WDF2-D now shows the same discipline is required inside counterfactual practice.

---

# PART VI — PHYSICAL CONSEQUENCE VS RESPONSIBILITY / BLAME

# 23. N-family — same physical counterfactual, different normative overlay

Anchor:

```text
operator omitted patch
system failed
```

Physical question:

```text
If patch had been applied, would failure have occurred?
```

Responsibility question:

```text
How responsible/blameworthy is the operator for the failure?
```

The latter can depend on:

```text
duty
role
knowledge
authority
available alternatives
foreseeability
normality
jurisdiction
```

These are not physical truth-makers for the failure mechanism itself.

---

# 24. Normality pressure

Halpern/Hitchcock-style work explicitly models default/normality orderings as affecting actual-causation judgments and distinguishes descriptive/prescriptive normality.

Responsibility/blame work further introduces epistemic state and graded responsibility.

WDF2-D therefore rejects both extremes:

```text
normality never matters
```

and:

```text
normality is part of every counterfactual truth condition
```

Instead:

```text
Normality/Norm can be role-admissible for causal attribution, responsibility or explanation when the target relation itself includes those concepts.
```

It is not automatically admissible for a purely physical consequence-under-intervention query.

---

# 25. Earned firewall D-NORM-1

```text
PhysicalCounterfactualTruth
!= ActualCauseRanking
!= Responsibility
!= Blame
```

and:

```text
NormativeBackground may constrain normative/attributional roles without becoming physical law.
```

---

# PART VII — MODEL EXPLORATION VS REALITY-FACING CLAIM

# 26. M-family — same formal counterfactual, different truth role

Suppose model M says:

```text
If X:=x' then Y=y'.
```

This can support at least two claim types.

## M1 — model-exploratory

```text
Within M, under surgery Δ, Y evaluates to y'.
```

The generator can be admissible if Δ is well-formed in M.

## M2 — Reality-facing causal claim

```text
In Reality, if we were to perform Δ, Y would be y'.
```

This requires more:

```text
M adequately represents the relevant mechanism
Δ corresponds to a realizable/meaningful alteration
model parameters/structure have sufficient evidence
transport/currentness conditions are satisfied
```

---

# 27. Earned firewall D-TRUTH-1

```text
SemAdmitWithinModel
!= WarrantForRealityClaim
```

A counterfactual result can be mathematically exact and epistemically weak.

Conversely, uncertainty in evidence does not make the semantic quantity meaningless.

---

# 28. Model misspecification as admissibility pressure

Actual-causation/modeling literature explicitly emphasizes that variable choice and structural equations can change causal conclusions.

Counterfactual-fairness and causal-sensitivity work likewise shows that counterfactual claims can be highly sensitive to unmeasured confounding/model assumptions.

Therefore `model adequacy` cannot be hidden inside the generator.

It is a separate warrant boundary.

---

# PART VIII — DOMAIN SEMANTICS AS CONSTRAINT, NOT UNIVERSAL ONTOLOGY

# 29. Physical domain

Candidate grounding can include:

```text
physical laws
causal mechanisms
boundary conditions
initial conditions
objective chance candidate
```

A consequence-under-action query normally preserves the relevant physical dynamics unless the alteration explicitly targets them.

But a counterlegal query can alter the law/mechanism itself.

Therefore:

```text
PreservePhysicalLaw by default within ordinary physical intervention role
```

is legitimate domain semantics.

```text
AlwaysPreserveActualLaw for every physical counterfactual
```

is not.

---

# 30. Software domain

Candidate authoritative structure can include:

```text
program version
language/runtime semantics
input contract
configuration
external service contract
```

Query roles differ:

```text
input what-if -> preserve program semantics
bug diagnosis -> backtrack to input/state/config/code cause candidates
patch planning -> change implementation/mechanism
language-version counterfactual -> change runtime semantics
```

Calling all of these `interventions on variables` without level typing loses the domain meaning.

---

# 31. Institutional domain

Candidate authoritative structure can include:

```text
constitutive rule set
authorization rules
legal/institutional status
procedural rules
```

A factual-status counterfactual can preserve current rules.
A rule-reform counterfactual must alter those rules.

Responsibility/legal attribution can additionally invoke normative and epistemic structures.

### Earned firewall D-DOM-1

```text
PhysicalLaw
!= ProgramSemantics
!= InstitutionalConstitutiveRule
```

but all three can serve analogous **preservation-grounding roles** in different domains.

Shared role != shared ontology.

---

# 32. Agent/provider domain

Relevant structure can include:

```text
prompt/context
model/provider/version
sampling mechanism
agent policy
memory/tool state
execution environment
```

Queries include:

```text
force one output token/action
change prompt
change policy
change model/provider
change tool availability
change memory
```

The appropriate generator depends on which layer the antecedent targets.

A shared seed or latent noise coupling may be meaningful within one mechanism and meaningless across provider changes.

---

# PART IX — QUERY-ROLE CONTRACT

# 33. Minimal contract

WDF2-D derives the following research-level contract.

For a query role Q, define obligations:

```text
RoleContract(Q) =
  RequiredAlterationKinds
  ProtectedStructureKinds
  PermittedAccommodationDirections
  RequiredCorrespondence
  RequiredResultShape
  PermittedExtraStructures
  ForbiddenImports
```

A generator G is semantically role-compatible only if it satisfies these obligations.

---

# 34. Consequence-under-specified-alteration contract

```text
Required:
  explicit alteration Δ
  downstream propagation

Normally protected:
  declared non-target mechanisms/background according to domain

Forbidden:
  silently changing upstream causes merely to make Δ natural
  importing responsibility/duty into physical result
```

---

# 35. Diagnostic-accommodation contract

```text
Required:
  target state/antecedent treated as a constraint
  search over upstream/background differences

Normally protected:
  relevant mechanisms/laws/rules unless query targets them

Forbidden:
  local output override that bypasses the diagnostic mechanism
```

---

# 36. Planning / recourse contract

```text
Required:
  actor/action set
  causal consequences of actions
  goal/outcome criterion
  temporal/resource constraints

Additional admissibility:
  ability
  authority
  access
  resource
  timing

Forbidden:
  treating arbitrary feature perturbations as executable actions
```

---

# 37. Policy-comparison contract

```text
Required:
  policy-level alteration
  future actions generated by altered policy
  distribution/trajectory evaluation

Forbidden:
  one-token override masquerading as policy replacement
```

---

# 38. Individualized-counterfactual contract

```text
Required:
  factual-unit/episode anchor
  declared factual-counterfactual coupling
  correspondence over time

Forbidden:
  silently degrading to population/interventional distribution while retaining individualized language
```

---

# 39. Actual-cause / attribution contract

```text
Required:
  actual occurrence of candidate/event target as relevant
  counterfactual contingency/pathway expressivity
  preemption/overdetermination support

Possible extra structure:
  normality/default, depending on theory/claim

Forbidden:
  equating simple but-for failure with non-causation universally
```

---

# 40. Responsibility / blame contract

```text
Required:
  causal/attributional substrate
  agent/role relation
  normative/institutional criteria
  available alternatives
  epistemic state when blame is claimed

Forbidden:
  deriving blame from physical counterfactual dependence alone
```

---

# 41. Model-exploration contract

```text
Required:
  explicit model truth role
  model alteration/revision provenance

Permitted:
  antecedents not yet Reality-grounded

Forbidden:
  promotion to Reality-facing truth without adequacy/evidence gate
```

---

# 42. Counterpossible contract

```text
Required:
  type/source of impossibility
  alternative-domain semantics
  what logic/rules remain operative

Forbidden:
  treating all impossible antecedents identically
```

---

# PART X — SEMANTIC ADMISSIBILITY TEST

# 43. Candidate formula

WDF2-D proposes a research diagnostic, not a production predicate:

```text
SemAdmit(G | F,Q,D,T) iff
  RoleFit(G,Q)
  ∧ AlterationFit(G,F.Alteration)
  ∧ PreservationFit(G,F.Preservation,D,Q)
  ∧ Compatibility(G,F)
  ∧ CorrespondenceFit(G,F.IdentityCriterion)
  ∧ DomainSemanticsFit(G,D)
  ∧ ResultShapeFit(G,Q)
  ∧ TruthRoleFit(G,T)
  ∧ ExplicitProvenance(G)
  ∧ NoForbiddenImport(G,Q,T)
```

This does not say these predicates are fundamental Reality entities.

It is a falsifiable research grammar.

---

# 44. Why evidence is excluded from SemAdmit

A tempting formula is:

```text
SemAdmit(..., Evidence)
```

WDF2-D rejects this as the default architecture.

Reason:

A counterfactual quantity can be semantically coherent even when evidence does not identify it.

Likewise abundant data cannot make a semantically wrong generator correct.

Therefore evidence belongs to a later gate:

```text
Warrant(...)
```

not inside semantic admissibility.

### Earned firewall D-EPI-1

```text
SemanticAdmissibility != EpistemicWarrant
```

---

# 45. Why actionability is excluded from generic SemAdmit

A physical counterfactual such as:

```text
If the Moon disappeared, what would tides do?
```

can be meaningful even though no Actor can perform that alteration.

Therefore:

```text
Actionability
```

cannot be a universal counterfactual requirement.

It becomes mandatory only for roles such as:

```text
planning
recourse
control
recommendation
```

### Earned firewall D-ACT-2

```text
CounterfactualMeaningfulness != ActorActionability
```

---

# 46. Why normativity is excluded from generic SemAdmit

Likewise:

```text
If operator had applied patch, would failure occur?
```

does not require a duty claim.

But:

```text
Was operator blameworthy for not applying patch?
```

does.

Normativity is role-gated.

---

# PART XI — REPRESENTATIONAL ADEQUACY

# 47. RepAdeq test

A generator can pass SemAdmit and still fail because the model cannot express the query faithfully.

Minimal diagnostics:

```text
TargetRepresented?
AlterationLocusRepresentedAtCorrectLevel?
PreservedStructureRepresented?
Identity/CorrespondenceRepresented?
RelevantConfounders/DependenciesRepresented?
ResultGrainMatchesQuery?
Rule/Mechanism/Policy distinction preserved?
```

If not:

```text
ModelRevisionRequired
```

is preferable to a false precise answer.

---

# 48. Model adequacy is role-relative but not arbitrary

A coarse model can be adequate for:

```text
population average effect
```

and inadequate for:

```text
individual token counterfactual
```

because the latter needs finer correspondence/coupling structure.

Similarly a service-level model can answer availability but not legal authorization if it lacks constitutive rules.

Thus:

```text
RepAdeq(M,Q1) != RepAdeq(M,Q2)
```

without implying that adequacy is subjective.

---

# PART XII — EPISTEMIC WARRANT / IDENTIFICATION

# 49. Identification ladder

After semantic and representational gates, a result can occupy:

```text
point identified
set/bound identified
sensitivity-characterized
model-dependent estimate
prior-dependent estimate
unsupported / not identified
```

These are epistemic statuses, not different counterfactual meanings.

---

# 50. Current research pressure

Counterfactual causal models can be observationally and interventionally equivalent while disagreeing on individual counterfactuals.

Recent work on counterfactual-equivalent models, fairness identifiability and robust counterfactual MDPs makes this pressure explicit.

The 2025 robust-MDP line emphasizes that many causal models may match the same observational/interventional MDP while yielding different counterfactual distributions, motivating bounds across compatible models rather than arbitrarily fixing one.

The 2026 nondeterministic robust-policy extension goes further by separating latent confounding from irreducible stochasticity and optimizing policies under counterfactual sensitivity.

This strongly supports keeping:

```text
generator/model choice uncertainty
```

visible rather than forcing point counterfactuals.

---

# 51. Earned firewall D-ID-1

```text
ObservationalEquivalence
!= InterventionalEquivalence
!= CounterfactualEquivalence
```

and even:

```text
Observational + Interventional Equivalence
!= IndividualCounterfactualEquivalence
```

in general.

---

# PART XIII — PRAGMATIC RELEVANCE

# 52. Pragmatics has a legitimate but bounded role

WDF2-D does not eliminate pragmatics.

Speaker/task interest can legitimately select:

```text
target variable
contrast class
reporting horizon
resolution/grain
which already-admissible consequence matters
```

But pragmatic interest cannot by itself license:

```text
violating domain law
changing institutional rules silently
reclassifying a model projection as Reality truth
calling inaccessible actions feasible
```

---

# 53. Earned firewall D-PRAG-1

```text
PragmaticRelevance can select among semantically admissible questions/outputs.
PragmaticRelevance cannot create Reality-grounding ex nihilo.
```

---

# PART XIV — HARD VS SOFT ADMISSIBILITY

# 54. Another major result — not every criterion is a tie-break weight

Some admissibility conditions are hard failures:

```text
wrong alteration locus
contradictory preservation
invalid identity mapping
model cannot represent target
truth-role collapse
unauthorized action when role requires authorized action
```

Others can rank otherwise admissible alternatives:

```text
cost
minimality
normality
typicality
similarity
robustness preference
communication usefulness
```

### Earned firewall D-HARD-1

```text
HardAdmissibilityConstraint != SoftRelevanceOrdering
```

This directly constrains future similarity/selection architectures.

A huge similarity score cannot repair a semantically invalid generator.

---

# 55. Example — unauthorized action

For a pure physical question:

```text
If command c executed, what would system do?
```

a model can answer even if Actor lacks authorization.

For a planning question:

```text
What can Actor do now to achieve outcome O?
```

the same command must be excluded from the Actor's admissible plan if authorization is required and unavailable.

Thus authority is neither universally relevant nor merely a soft cost.

Its role is query-typed.

---

# PART XV — MULTIPLE GENERATORS CAN REMAIN ADMISSIBLE

# 56. The attempted admissibility criterion does not guarantee uniqueness

This is WDF2-D's most important residual.

Suppose:

```text
Q = individualized diagnostic question
D = stochastic system
T = model-relative explanatory claim
```

Two different generators can both satisfy:

```text
RoleFit
AlterationFit
PreservationFit
CorrespondenceFit
DomainFit
TruthRoleFit
```

while differing in:

```text
factual-counterfactual coupling
background prior
normality ordering
grain
model structure
```

if available domain/evidence does not resolve those choices.

Therefore:

```text
SemAdmit(G1)=true
SemAdmit(G2)=true
```

can coexist with:

```text
Result(G1) != Result(G2)
```

---

# 57. This is not a failure of the admissibility architecture

Forcing one generator would reintroduce arbitrary hidden assumptions.

The correct output may be:

```text
multiple admissible generators
counterfactual disagreement
partial/bounded result
robust invariant result
```

rather than:

```text
choose one secretly
```

This directly motivates the next round.

---

# 58. Under-determination can arise at several levels

```text
U1 generator-family underdetermination
U2 model-structure underdetermination
U3 parameter underdetermination
U4 factual-counterfactual coupling underdetermination
U5 alternative-ordering underdetermination
U6 identity/correspondence underdetermination
U7 normality/normative-order underdetermination
```

These must not all be called `uncertainty` without typing.

---

# 59. Earned firewall D-UNDER-1

```text
MultipleAdmissibleGenerators != SemanticFailure
```

and:

```text
CounterfactualUnderdetermination != OrdinaryStatisticalNoise
```

It can reflect genuinely unresolved structural commitments.

---

# PART XVI — MATCHED CASE MATRIX

# 60. Query-role discriminator matrix

| Surface family | Role A | Role B | Required generator difference |
|---|---|---|---|
| “If server were healthy” | downstream consequence | upstream diagnosis | forward/local vs backtracking |
| “What would make approval occur?” | model contrast | recourse | feature state vs actionable intervention |
| “If action differed” | token action | policy replacement | one-step surgery vs policy generator change |
| “What if policy π'?” | population intervention | individualized episode CF | marginal rollout vs factual-coupled trajectory |
| “Did C cause E?” | dependence test | actual causation | simple removal vs contingency/path structure |
| “Why E?” | causal attribution | explanation | Reality relation vs epistemic/contrastive role |
| “If patch applied?” | physical consequence | responsibility | physical generator vs causal+normative overlay |
| “If X:=x' then Y?” | within-model | Reality-facing | semantic result vs adequacy/warrant gate |
| “If rule changed” | institutional reform | credential-state change | rule surgery vs state alteration |
| impossible A | logical/math | counterconventional | domain-extension type and preserved logic differ |

No single default generator survives all rows.

---

# PART XVII — NON-CIRCULARITY TESTS

# 61. Rejected criterion — intuition fit

```text
Admit G iff G gives the intuitive answer.
```

**FAIL**.

It uses the verdict as the criterion.

---

# 62. Rejected criterion — predictive accuracy

```text
Admit G iff its model predicts observed data well.
```

**FAIL**.

Observed/predictive equivalence can coexist with counterfactual disagreement.

---

# 63. Rejected criterion — minimal change

```text
Admit G iff it changes least.
```

**FAIL**.

WDF2-B/C already showed that change metric/grain and protected structure must be grounded first.

---

# 64. Rejected criterion — actionability everywhere

```text
Admit only counterfactuals an Actor can perform.
```

**FAIL**.

Scientific, explanatory and counterlegal counterfactuals can be meaningful without actor control.

---

# 65. Rejected criterion — one authoritative domain model

```text
Admit G iff current model M supports it.
```

**FAIL** as universal rule.

The model may be incomplete; WDF0 requires structural revision to remain possible.

---

# 66. Rejected criterion — linguistic form

```text
“If A had...” -> one fixed generator family
```

**FAIL**.

Surface language underdetermines role.

---

# 67. Surviving criterion family

The strongest surviving non-circular route is constraint-based:

```text
1. Parse the semantic role of the query.
2. Type the alteration and intended invariants.
3. Use domain semantics to rule out incompatible generators.
4. Require explicit identity/correspondence and result shape.
5. Keep truth role explicit.
6. Separately audit model adequacy.
7. Separately audit evidence/identification.
8. Add actor/normative constraints only for roles that require them.
9. If several generators remain admissible, preserve the disagreement.
```

This can be applied before observing the desired answer.

---

# PART XVIII — ROLE ROUTING IS NOT A PRODUCTION ROUTER

# 68. Research meta-architecture only

The previous section may look like software architecture.

It is not authorization to implement:

```text
CounterfactualRouter
GeneratorRegistry
QueryRole enum
AdmissibilityEngine
```

The structure is currently a research grammar used to test foundations.

Production consumption still requires concrete consumer pressure.

---

# PART XIX — CROSS-DOMAIN DELETION TESTS

# 69. Delete QueryRole

**FAIL**.

Forward consequence and backtracking diagnosis collapse.
Explanation and recourse collapse.
Physical consequence and responsibility collapse.

---

# 70. Treat QueryRole as arbitrary user preference

**FAIL**.

It cannot explain hard structural obligations.

---

# 71. Delete DomainSemantics

**FAIL**.

Program semantics, physical dynamics and institutional rules become indistinguishable arbitrary invariants.

---

# 72. Delete TruthRole

**FAIL**.

Within-model and Reality-facing counterfactuals collapse.

---

# 73. Delete ModelAdequacy gate

**FAIL**.

A mathematically valid fixed-model answer can masquerade as a valid answer to an unrepresentable query.

---

# 74. Delete Identification/Warrant gate

**FAIL**.

Semantically coherent but empirically unidentified token counterfactuals become falsely precise.

---

# 75. Require Actionability universally

**FAIL**.

Non-agentive scientific/counterlegal counterfactuals disappear.

---

# 76. Delete Actionability for planning

**FAIL**.

Nearest states masquerade as recommendations.

---

# 77. Delete normative gate for responsibility

**FAIL**.

Physical causation becomes blame.

---

# 78. Require unique generator after admissibility

**FAIL**.

Model/coupling/order underdetermination remains even after all known hard constraints are respected.

---

# PART XX — WDF0 / WDF1 REOPEN AUDIT

# 79. WDF0

No FoundationReopenCondition fires.

WDF2-D strongly reinforces:

```text
Reality != Model
Observable != Real
Cause != Constitution
PhysicalAbility != Authority
WithinModelUpdate != StructuralModelRevision
Relative != Subjective
```

The new layered-gate architecture is a direct consequence of these separations.

WDF0 remains frozen.

---

# 80. WDF1

No FoundationReopenCondition fires.

WDF1 already required:

```text
typed modal truth role
typed generator/evaluator
explicit dependence/background
anchor
measure interpretation
model/evidence provenance
```

WDF2-D gives the counterfactual-specific elaboration of why these fields cannot be collapsed.

It does not falsify TMCG.

WDF1 remains frozen.

---

# PART XXI — FOUNDATION RECONSTRUCTION AFTER WDF2-D

# 81. Counterfactual claim architecture now has three layers

## Layer A — semantic frame

```text
Anchor
Alteration
Target
Preservation
Correspondence
QueryRole
TruthRole
```

## Layer B — generator semantics

```text
GeneratorFamily
AlternativeDomain
ResultShape
Ordering/Coupling
BacktrackingPolicy
```

## Layer C — warrant/use gates

```text
ModelAdequacy
Identification/Evidence
Actionability when relevant
Normative/Institutional admissibility when relevant
```

None is a Reality ontology.

---

# 82. Refined admissibility architecture

```text
FrameWellTyped(F,Q)

SemanticallyAdmissibleGenerators =
  { G |
      RoleFit(G,Q)
      ∧ SurgeryFit(G,F)
      ∧ PreservationFit(G,F,D)
      ∧ CorrespondenceFit(G,F)
      ∧ DomainFit(G,D)
      ∧ TruthRoleFit(G,T)
  }

For each G:
  RepAdeq(M,G,Q,D)?
  Warrant(Result_G,Evidence,Assumptions,T)?
  ActAdmit(...)?       when Q requires action
  NormAdmit(...)?      when Q requires normative attribution
```

Crucially:

```text
|SemanticallyAdmissibleGenerators| may be > 1.
```

That is not an implementation bug.

---

# 83. QueryRole should constrain, not fully determine, G

Another deletion test shows:

```text
QueryRole -> exactly one generator
```

is too strong.

For example, individualized prediction in a stochastic system may admit several couplings consistent with the same role and domain semantics.

Thus role removes invalid generators but may not uniquely identify one.

### Earned firewall D-ROLE-2

```text
QueryRoleConstrainsGenerator
!= QueryRoleUniquelyDeterminesGenerator
```

---

# 84. DomainSemantics should constrain, not freeze, models

Likewise:

```text
DomainSemantics -> one final model
```

is too strong.

Multiple models can respect known domain laws/rules and observations.

Therefore domain semantics gives hard constraints and candidate grounding without eliminating model uncertainty.

---

# PART XXII — CURRENT EXTERNAL RESEARCH PRESSURE

# 85. Backtracking and forward roles

Von Kügelgen, Mohamed and Beckers formalize interventionist and backtracking counterfactuals within SCMs as distinct modes: the former changes local causal laws/mechanisms under shared exogenous conditions; the latter preserves the causal laws and alters upstream/exogenous conditions.

This is direct pressure for Q-role separation.

---

# 86. Recourse and actionability

Karimi, Schölkopf and Valera argue that nearest counterfactual explanations identify a target state but need not provide a way to reach that state, motivating recourse through interventions.

Karimi et al. further show that imperfect causal knowledge prevents guaranteed recourse in general and motivates probabilistic/subpopulation alternatives.

This is direct pressure for separating semantic counterfactual contrast, action admissibility and epistemic warrant.

---

# 87. Individualized vs interventional trajectory

Kazemi et al. show that in MDP counterfactual inference a generated trajectory can drift far enough from the observed path that the factual observation no longer influences it, making the result effectively interventional rather than individualized.

This is direct pressure for an explicit correspondence/coupling obligation in individualized roles.

---

# 88. Policy-level intervention

Causal policy-intervention work models changing the treatment policy itself rather than merely changing a fixed future treatment sequence.

This supports WDF2-B/C/D's policy-vs-token alteration firewall.

---

# 89. Actual causation and functional role

Beckers' 2025 nondeterministic actual-causation work explicitly develops a causation definition from the function actual-cause information can fulfill in causal discovery/communication rather than relying only on example intuitions.

WDF2-D adopts the methodological pressure:

```text
role-based independent constraints are possible
```

without adopting that specific actual-causation definition.

---

# 90. Normality, responsibility and modeling

Halpern/Hitchcock work shows that normality/defaults can alter actual-causation judgments, while responsibility/blame extensions add graded responsibility and epistemic state.

Their model-appropriateness work also emphasizes that variable/model choice changes causal conclusions.

This supports two WDF2-D separations:

```text
physical counterfactual != normative attribution
semantic generator != model adequacy
```

---

# 91. Counterfactual model multiplicity

Recent robust counterfactual MDP research explicitly treats multiple causal models that agree on observational/interventional behavior but yield different counterfactual distributions.

The August 2026 nondeterministic extension additionally optimizes robust policies while separating latent confounding from irreducible stochasticity.

This is the strongest current external pressure for the WDF2-D residual:

```text
multiple admissible generators/models may remain
```

and robust/bounded conclusions may be preferable to arbitrary point selection.

---

# PART XXIII — RESIDUAL RANKING

# 92. Residuals after WDF2-D

```text
1. Multiple admissible generators / counterfactual disagreement      CRITICAL
2. Robust consequences invariant across admissible generators        CRITICAL
3. Structural-surgery composition across multiple loci               CRITICAL
4. Model revision + cross-model identity/correspondence               CRITICAL
5. Probabilistic coupling / nondeterministic identification           CRITICAL
6. Ordering/normality underdetermination                              HIGH/CRITICAL
7. Would/might/robust modal-force logic                               HIGH
8. Nested/sequential counterfactual composition                       HIGH
9. Prevention/omission/preemption bridge to causal architecture       HIGH
10. Law/chance/powers Reality-grounding comparison                    HIGH
```

The new first residual is upstream of several others.

WDF2-D can rule out semantically invalid generators, but it cannot guarantee a unique surviving generator.

When several survive, the system must determine how to represent disagreement without:

```text
arbitrary tie-breaking
false averaging
truth-role collapse
confusing model uncertainty with stochasticity
```

---

# 93. Exact next round

The next canonical round is therefore:

# **WDF2-E — Counterfactual Underdetermination / Generator Disagreement / Robust Consequence**

WDF2-E should ask:

```text
What kinds of counterfactual disagreement exist?
When do several admissible generators count as equivalent?
Which conclusions are invariant across them?
When should World return a set/bound/interval rather than one verdict?
Can generator disagreement be ordered by evidence without collapsing semantics into epistemology?
How should model uncertainty, coupling uncertainty, nondeterminism and ordinary probability remain separate?
What does “robustly would” mean across admissible generator families?
When does disagreement force model revision rather than mere uncertainty reporting?
```

Only WDF2-E residuals may determine WDF2-F.

---

# 94. Production disposition

No production changes are admitted.

Do **not** add:

```text
QueryRole enum
CounterfactualAdmissibilityEngine
GeneratorRouter
ModelAdequacy service
CounterfactualUncertainty aggregator
```

Current production World remains narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

and the research foundation is not yet frozen as a complete Counterfactual Foundation v1.

---

# 95. Closeout

```text
WDF2-D: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A/B/C reopen: NO
Production refactor: NO

GeneratorSemantics != ModelAdequacy
GeneratorSemantics != EmpiricalIdentification
GeneratorSemantics != Actionability
GeneratorSemantics != NormativeAttribution
QueryRole != SubjectivePreference
QueryRoleConstrainsGenerator != QueryRoleUniquelyDeterminesGenerator
DesiredState != ActionableIntervention
InterventionalOutcome != IndividualizedCounterfactualOutcome
PhysicalCounterfactual != Responsibility/Blame
SemAdmitWithinModel != WarrantForRealityClaim
HardAdmissibilityConstraint != SoftRelevanceOrdering
MultipleAdmissibleGenerators != SemanticFailure

Exact next round:
WDF2-E — Counterfactual Underdetermination / Generator Disagreement / Robust Consequence
```

Compressed result:

> **WDF2-D succeeds in making generator admissibility substantially less circular, but it does so by refusing to collapse distinct questions. A counterfactual generator is first judged against the semantic role of the query, the typed alteration/preservation frame, domain semantics, correspondence and truth role. Model adequacy is a separate gate; evidence and identification are another; actionability and normative constraints enter only for roles that require them. This explains why forward intervention, backtracking diagnosis, recourse, policy comparison, individualized counterfactuals, causal attribution and responsibility may legitimately require different generators without making counterfactual truth arbitrary. The decisive residual is that these constraints still need not select one unique generator. Several generators or causal models can remain independently admissible while yielding different counterfactual answers. WDF2 must therefore next study underdetermination itself: how to classify disagreement, preserve robust invariants, return bounds or plural results, and avoid silently turning unresolved structural assumptions into false precision.**
