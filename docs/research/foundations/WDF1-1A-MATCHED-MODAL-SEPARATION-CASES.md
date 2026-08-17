# WDF1-1A — Matched Modal Separation Cases

Status: complete for WDF1-1A. This sub-round does **not** select a final modal architecture. It constructs matched cases whose only purpose is to force modal coordinates apart when they can vary independently. Exact next sub-round: **WDF1-1B — Candidate Modal Architectures**.

## 0. Question

WDF1-0 separated several uses of `possible`, `reachable`, `feasible`, `accessible`, `authorized`, `epistemically possible` and `chance`, but separation by vocabulary is not enough.

WDF1-1A asks:

> Can we construct cases where one modal claim is true while another is false, under an otherwise matched target? If yes, the two claims cannot be universally identified.

The round therefore uses **independence witnesses**, not intuition alone.

## 1. Working coordinates

For one target transition/outcome `T` relative to actual condition `x`, define provisional research coordinates:

```text
N(T)   — nomologically admissible under the target world's laws/rules of physical evolution
R(T)   — reachable from the actual condition under a declared transition/input set and horizon
C_A(T) — controllably reachable by Actor A through an A-selectable policy/action set
F_A(T) — feasible for A under current resources/capacities/compatibility requirements
X_A(T) — accessible to A through a current path/interface/materialization route
U_A(T) — authorized/permitted for A under the relevant institution/owner/rule system
E_A(T) — epistemically open for A: current evidence/model has not ruled T out
P(T)   — probability/chance coordinate, if the target theory assigns one
```

These are deliberately not production fields.

Important: `R` is incomplete unless the admissible transition/input set and horizon are specified. A central goal of this sub-round is to determine whether `C_A` is reducible to a more general `R` plus Actor-relative input/policy constraints.

## 2. Case A1 — Same law, different actual state: nomologically possible but not reachable from here

Consider a deterministic transition system:

```text
state space: integers Z
law: x_{t+1} = x_t + 2
actual: x_0 = 0
```

Under the same law, state `3` is a perfectly valid state that could be an initial condition in some law-compatible history.

But from actual state `0`:

```text
0 → 2 → 4 → 6 → ...
```

state `3` is not reachable.

Therefore, under the interpretation that `nomologically possible` means `occurs in at least one law-compatible history`:

```text
N(3) = true
R_from_0(3) = false
```

### Separation earned

```text
NomologicalPossibility != ReachabilityFromActuality
```

### Deeper result

This case also shows that a law alone does not determine reachability from actuality. Reachability requires at least:

```text
law/dynamics
+ actual/initial condition
+ admissible inputs/disturbances
+ horizon/path constraints
```

Hence:

```text
Law != InitialCondition
LawCompatibility != ReachabilityFromHere
```

## 3. Case A2 — Same actual state, different horizon: reachable eventually but not before deadline

Use:

```text
x_{t+1} = x_t + 1
x_0 = 0
T = x = 10
```

Then:

```text
R_horizon=5(T)  = false
R_horizon=10(T) = true
```

No law, target or actual state changed. Only horizon changed.

### Separation earned

Reachability is intrinsically horizon-relative when time-to-target matters.

```text
Reachable(T) without horizon/regime can be underspecified.
```

This directly supports WDF0's dependence-signature discipline.

## 4. Case A3 — Natural reachability without Actor control

Consider an autonomous system:

```text
x_{t+1} = x_t - 1 for x_t > 0
x_0 = 3
Actor A has no actuator/input into x
T = x = 0
```

The target will be reached under the natural dynamics:

```text
3 → 2 → 1 → 0
```

So existential trajectory reachability is true.

But A has no action whose variation changes whether or when the target occurs.

This exposes two meanings hidden inside `can obtain`:

```text
passive eventual attainment
vs
Actor-selectable causal/control attainment
```

### Separation earned

```text
NaturalReachability != ActorControl
```

An Actor can predict or wait for a reachable outcome without possessing causal control over it.

### Implication for Capability

Current Capability uses `cause or obtain` intentionally broadly. WDF1 must not infer:

```text
Actor can obtain T
⇒ Actor causally controls T
```

## 5. Case A4 — Actor control as reachability under a typed policy/input set

Consider:

```text
x_{t+1} = x_t + u_t
x_0 = 0
T = x = 3
```

If the abstract system permits:

```text
u_t ∈ {-1, 0, +1}
```

then a suitable input sequence reaches `3`.

Now define Actor A's actual action interface:

```text
U_A = {0}
```

while Actor B has:

```text
U_B = {-1, 0, +1}
```

Then the physical/dynamical model is unchanged, but:

```text
C_A(T) = false
C_B(T) = true
```

### Compression pressure

This suggests that `control reachability` can partly be reconstructed as:

```text
Reachable(current, target | A-admissible input/policy set)
```

rather than requiring a completely separate primitive.

However, **mere existence of an A-labeled input sequence is still weaker than robust Actor control**, because real control can depend on:

- observation/feedback;
- policy selection;
- disturbances;
- uncertainty;
- timing;
- authority to issue the input;
- ability to realize the input.

Therefore WDF1-1A does not delete `C_A` yet.

## 6. Case A5 — Abstract control-reachable but resource-infeasible now

Use the same control model:

```text
x_{t+1} = x_t + u_t
x_0 = 0
T = x = 10 in one step
```

The actuator model allows:

```text
u ∈ [-10, 10]
```

so the transition is control-reachable in the abstract system.

But Actor A currently has a resource/energy/current limit:

```text
|u| ≤ 2
```

under the current battery/capital/throughput budget.

Then:

```text
C_abstract(T) = true
F_A,one-step(T) = false
```

### Separation earned

```text
ControlReachableUnderAbstractActionSet
!=
FeasibleUnderCurrentResources
```

### Important refinement

If resource limits are inserted directly into the admissible action set, feasibility can be represented as a restricted reachability problem.

This produces a central architecture candidate for WDF1-1B:

```text
Modal distinctions may sometimes be different typed constraints on one alternative/trajectory space,
without being the same truth role.
```

The distinction remains necessary because the reason for exclusion matters for action: acquire more energy/capital vs redesign dynamics vs change authority.

## 7. Case A6 — Feasible resource exists but currently inaccessible

Construct a service case:

```text
Provider P exists.
Account A has paid entitlement and sufficient quota.
Requested operation is semantically supported.
No current network route / DNS / tunnel / interface path from Actor to P exists.
```

Then the target can be resource-feasible in the sense that the needed account/quota/provider capability exists while current access is false.

```text
F_A(T) = true
X_A(T) = false
```

### Separation earned

```text
ResourceFeasible != CurrentlyAccessible
```

This is already strongly supported by current Ordivon network/capability doctrine:

```text
resource existence
!= relation usability
!= current action authority
```

## 8. Case A7 — Accessible and understood, but unauthorized/refused

HTTP provides a clean protocol-level witness.

A client can successfully reach an origin, send a syntactically meaningful request, and receive a server response indicating that the request was understood but refused.

RFC 9110 defines HTTP `403 Forbidden` precisely as the server understanding the request and refusing to fulfill it. The same standard separately defines authentication/authorization semantics and notes that valid credentials can still be inadequate to gain access.

Thus one can have:

```text
network/protocol path works
request reaches authoritative server
server understands target operation
but authorization policy refuses fulfillment
```

So:

```text
X_A(T) = true
U_A(T) = false
```

### Separation earned

```text
Accessible != Authorized
```

This is not philosophical speculation; it is encoded in a real widely deployed protocol semantics.

## 9. Case A8 — Authorized but resource/physical capability absent

Construct the matched reverse case:

```text
Institution/owner rule grants Actor A permission to request operation T.
The machine currently lacks the physical capacity/resource needed to realize T.
```

Examples in abstract form:

```text
permission to allocate 1 TB RAM
but only 16 GB physical memory exists and no backing/substitute is available;

permission to lift a payload
but the installed actuator cannot produce required force;

permission to execute a licensed operation
but required hardware/function does not exist.
```

Then:

```text
U_A(T) = true
F_A(T) = false
```

and possibly:

```text
C_A(T) = false
```

### Separation earned

```text
Authorized != Feasible
Authorized != Capability
```

Deontic/institutional permission does not manufacture physical/resource possibility.

## 10. Case A9 — Physically feasible but legally/institutionally forbidden

Take the exact same physical system and resources as A8, but now choose an action T for which the Actor has sufficient physical means while a valid rule system forbids the action.

Then:

```text
F_A(T) = true
U_A(T) = false
```

### Pairwise independence

A8 + A9 jointly show:

```text
Feasibility and Authorization are not merely different names for the same gate.
```

Either can be true while the other is false.

## 11. Case A10 — Authorization can be constitutive, not merely an extra physical barrier

Suppose two people produce physically indistinguishable signatures/commands:

```text
Person P1 is the authorized office-holder.
Person P2 is not.
```

Under the rule system, P1's act may constitute a valid institutional authorization while P2's physically similar act does not.

The modal difference is therefore not well described as a new physical force blocking P2.

### Separation earned

```text
InstitutionalAuthorization
can alter what an act counts as,
not merely whether a physically identical event can occur.
```

This preserves WDF0's firewall:

```text
Cause != Constitution
Constraint != ConstitutiveStatus
```

and prevents a generic `constraint filter` architecture from flattening all institutional modality into physical exclusion.

## 12. Case A11 — Epistemically open but objectively unreachable

Use the parity transition system from A1, but give Agent A an incomplete model:

```text
Agent believes:
  x_{t+1} may be x_t + 1 or x_t + 2
Actual rule:
  x_{t+1} = x_t + 2
Actual x_0 = 0
Target T = 3
```

Given A's evidence/model, `3` remains epistemically open.

But under actual dynamics from the actual state:

```text
R(T) = false
E_A(T) = true
```

### Separation earned

```text
EpistemicPossibility != ObjectiveReachability
```

The same pattern can occur with nomological possibility if the Agent's theory of law is wrong.

## 13. Case A12 — Objectively reachable but epistemically ruled out

Reverse the model error:

```text
Actual rule:
  x_{t+1} ∈ {x_t + 1, x_t + 2}
Agent incorrectly believes:
  x_{t+1} = x_t + 2 only
Actual x_0 = 0
Target T = 3
```

A real trajectory exists:

```text
0 → 1 → 3
```

but A's model rules it out.

Then:

```text
R(T) = true
E_A(T) = false
```

### Pairwise independence

A11 + A12 establish:

```text
EpistemicOpenness and ObjectiveReachability vary independently.
```

This is the modal extension of:

```text
WorldModel != World
```

## 14. Case A13 — Probability does not collapse to binary possibility

Consider a formal quantum measurement model with two possible outcomes and Born-rule probabilities:

```text
P(outcome 0) = 0.99
P(outcome 1) = 0.01
```

Both outcomes belong to the theory's outcome space and have non-zero assigned probability.

Thus both are possible in the model, but not equally probable.

Standard quantum theory formally assigns probabilities to measurement outcomes through the Born rule. WDF1-1A does **not** infer from this formalism that a particular metaphysics of objective chance is correct; it uses the case only to establish that a probability coordinate carries information not contained in a Boolean possibility predicate.

### Separation earned

```text
Possible != EquallyProbable
Possibility != ProbabilityValue
```

## 15. Case A14 — Epistemic uncertainty without objective stochasticity

Take a deterministic external service:

```text
Request either committed or did not commit.
Response was lost.
Current controller lacks owner-native evidence telling which actuality obtained.
```

Reality has one actual history, but the observer has two live hypotheses.

Then:

```text
E_A(committed) = true
E_A(not_committed) = true
```

while nothing in the case requires objective stochasticity.

### Separation earned

```text
MultipleEpistemicallyOpenAlternatives
!=
ObjectiveChanceProcess
```

This is exactly why current Ordivon preserves `UNKNOWN` rather than inventing probabilities.

## 16. Case A15 — Stochastic model with known distribution but unknown token outcome

Now distinguish a different case:

```text
Theory specifies a probability distribution over next outcomes.
The token outcome has not yet occurred/been observed.
```

Here two uncertainty layers can coexist:

```text
aleatory/objective-chance candidate
and
epistemic uncertainty about the future token result.
```

Even if later WDF1 rejects a primitive objective-chance interpretation, the model-level distinction remains:

```text
distributional structure
!= observer's ignorance state
```

## 17. Case A16 — Same objective modality, different observer information

Two Agents face the same actual system:

```text
A1 has current topology/rule evidence.
A2 has stale or incomplete evidence.
```

No physical/institutional/modal fact has changed, but their epistemic possibility sets differ.

```text
ObjectiveModalProfile(T) = same
E_A1(T) != E_A2(T)
```

### Separation earned

Epistemic modality is Agent/evidence-relative and cannot be part of objective modality by identity.

## 18. Case A17 — Same physical trajectory, different institutional status

Construct two worlds identical in physical microhistory for the target action but differing only in a valid institutional rule/authorization relation.

Physical motion, messages and button presses can be identical while:

```text
World W1: action is authorized/valid
World W2: action is unauthorized/invalid
```

### Result

Physical trajectory alone does not fix institutional modal/status truth unless the institutional rule system itself is included in the total Reality description.

This is not a violation of Reality objectivity. It shows:

```text
Institutional modality supervenes on a broader Reality base than bare local physical trajectory.
```

WDF1-1A does not attempt a reduction thesis beyond this.

## 19. Case A18 — Same institution, different access

Hold constant:

```text
account
permission
rule system
provider capability
operation
```

Change only network/path state:

```text
Path P1 healthy
Path P2 unavailable
```

Then:

```text
U_A(T) = same
X_A(T) differs
```

This is a clean matched Ordivon-style independence witness.

## 20. Case A19 — Same access, different authorization

Hold constant:

```text
network path
server
request syntax
resource existence
```

Change only credentials/rule decision:

```text
Credential set C1 authorized
Credential set C2 refused
```

Then access remains while authorization changes.

RFC 9110's 401/403 semantics supply concrete protocol support for exactly this distinction.

## 21. Case A20 — Same resources, different dynamics

Hold constant:

```text
Actor
energy/resource budget
action interface
target
```

Change only system dynamics:

```text
D1: x_{t+1}=x_t+u_t
D2: x_{t+1}=x_t
```

The Actor can possess the same resources and authority while control reachability changes.

### Separation earned

```text
PossessingResource != HavingCapability
```

because capability also depends on target-system dynamics/coupling.

## 22. Case A21 — Same dynamics, different Actor interface

Hold the physical system and target constant; give A and B different actuators or action channels.

Then:

```text
N(T) same
physical dynamics same
C_A(T) != C_B(T)
```

### Result

Actor-control modality is relational:

```text
Actor × Body/Interface × Target × Environment × Time
```

not an intrinsic target property.

## 23. Case A22 — Same action interface, different observation: controllable in open-loop, not robustly controllable under uncertainty

Construct a target where a precise action sequence reaches T only if an unobserved disturbance/state variable has one known value.

If Actor cannot observe that variable, there may exist an action sequence for each hidden state, but no single policy based on available observations guarantees T.

This separates:

```text
trajectory existence
open-loop reachability
feedback/policy controllability under uncertainty
```

### Result

`ControlReachable` itself is not one scalar predicate unless policy class, observation structure and robustness criterion are declared.

This will matter later for Agent capability under partial observability.

## 24. Case A23 — Same modal facts, different decision relevance

Two outcomes T1 and T2 have identical objective modal profiles, but the Agent's goal/objective treats only T1 as relevant.

Then:

```text
possible/reachable/authorized facts remain equal
Option_Q(T1) != Option_Q(T2)
```

because Option additionally depends on the decision/query/objective.

### Separation earned

```text
Optionhood != ObjectivePossibility
```

This confirms that Option remains downstream decision vocabulary, not World modality primitive.

## 25. Case A24 — Selection does not imply realization

Suppose A selects an authorized, feasible, accessible action. After dispatch, an external failure occurs.

Then:

```text
Selected = true
Realized target = false
```

Or response loss leaves realization UNKNOWN.

### Separation retained

```text
Selected != Realized
Action != Effect
```

Modal actionability does not entail actuality.

## 26. Independence matrix

Legend:

```text
+ = true in constructed case
- = false
? = intentionally unspecified / not relevant
```

| Case | N | R | C_A | F_A | X_A | U_A | E_A | Key separation |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| A1 parity from 0 → 3 | + | - | ? | ? | ? | ? | ? | N ≠ R |
| A3 passive decay | + | + | - | ? | ? | ? | + | R ≠ control |
| A5 high-force target | + | +* | +* | - | ? | ? | + | abstract control ≠ current feasibility |
| A6 route unavailable | + | +* | +* | + | - | + | + | feasible ≠ access |
| A7 HTTP 403 | + | +* | +* | + | + | - | + | access ≠ authorization |
| A8 permission, insufficient capacity | + | +* | - | - | + | + | + | authorization ≠ feasibility/capability |
| A9 feasible, forbidden | + | +* | + | + | + | - | + | feasibility ≠ authorization |
| A11 hidden parity invariant | + | - | ? | ? | ? | ? | + | epistemic openness ≠ reachability |
| A12 model falsely excludes path | + | + | ? | ? | ? | ? | - | reachability ≠ epistemic openness |

`+*` means the coordinate is true only under the deliberately stated broader/abstract transition/action set. This notation itself exposes why modal coordinates must bind their action/input sets.

## 27. Pairwise independence results actually established

WDF1-1A now has explicit witnesses for the following non-identities:

```text
NomologicalPossibility != ReachabilityFromActuality
Reachability != ActorControl
AbstractControlReachability != CurrentResourceFeasibility
ResourceFeasibility != CurrentAccess
Access != Authorization
Authorization != ResourceFeasibility
EpistemicOpenness != ObjectiveReachability
ProbabilityValue != BooleanPossibility
EpistemicUncertainty != ObjectiveChance
Optionhood != ObjectiveModality
Selection != Realization
```

Some pairs are stronger than mere non-identity: A8/A9 and A11/A12 show **two-way logical independence** under the constructed models.

## 28. First compression candidate — `Reachability` as a family parameterized by admissible transitions

Several distinctions can be represented mathematically through:

```text
Reach(T | x_actual, TransitionRelation, AllowedInputs, Horizon, Constraints)
```

Changing `AllowedInputs/Constraints` can represent:

- passive natural evolution;
- abstract control inputs;
- Actor-specific actuators;
- resource-limited inputs;
- time-bounded reachability.

This is a serious compression candidate.

But WDF1-1A finds three reasons not to reduce everything to reachability:

### 28.1 Epistemic openness

This is a relation to Agent evidence/model, not just objective transition structure.

### 28.2 Institutional authorization

Permission can be constitutive/deontic rather than a physical transition restriction.

### 28.3 Access/interface

Access is a coupling/interface relation. It can often be encoded as allowed edges/actions in an operational transition graph, but doing so may erase the explanatory difference between `path missing` and `permission denied`.

Therefore:

```text
shared mathematical representation
!= shared ontological/explanatory role
```

## 29. Second compression candidate — modal constraint intersection

For an objective target history/action H, one might write:

```text
Admissible_Q(H)
= H ∈ N
∩ D_actual
∩ C_actor
∩ F_resource
∩ X_access
∩ U_authority
```

This is attractive as an **actionability conjunction**.

However it fails as a universal ontology for three reasons:

1. some coordinates are not naturally sets over the same universe;
2. authorization can change what an act counts as rather than merely exclude a trajectory;
3. epistemic openness is an Agent/model relation and may contain objectively impossible alternatives.

Thus `intersection of filters` is retained as one architecture rival for WDF1-1B, not accepted now.

## 30. Third compression candidate — product/vector modality

Instead of one scalar possible/impossible predicate:

```text
ModalProfile_A,Q(T)
= <N, R, C, F, X, U, E, P>
```

This preserves independent coordinates and supports matched comparisons.

Problems:

- some coordinates have entailment relations under fixed definitions;
- some are not Boolean;
- `R/C/F` may be derivable from one parameterized reachability family;
- `U` includes constitutive/deontic semantics not captured by numeric gating;
- `P` may apply only after a sample/event space is declared.

Again: serious rival, not selected.

## 31. Fourth compression candidate — typed modal relations rather than a single structure

The most conservative architecture is:

```text
NomologicallyPossible(T | Laws, background)
Reachable(T | actual, transitions, horizon)
ControllableBy(A,T | actions, observations, policy, conditions)
FeasibleFor(A,T | resources, constraints, load, time)
AccessibleBy(A,T | interface/path, time)
AuthorizedFor(A,T | institution/rules, time)
EpistemicallyOpenFor(A,T | evidence/model)
Chance(T | chance model / law?)
```

No claim is made that these instantiate one common metaphysical genus beyond their all being alternative/action-related questions.

This typed pluralism has low false-unification risk but may miss real shared modal structure.

WDF1-1B must compare it against reachability/filter/product architectures.

## 32. Law vs initial/boundary condition pressure already visible in A

A1/A2 show that even under a fixed law/dynamics, changing:

```text
initial state
horizon
input set
```

changes reachability.

Therefore a model that labels every restriction on possible trajectories `law` would erase important roles.

WDF1-1A freezes only:

```text
LawRole != InitialConditionRole
LawRole != HorizonRole
```

while boundary-condition theory remains for WDF1-1C.

## 33. Constraint taxonomy pressure from cases

The matched cases expose at least these exclusion modes:

```text
nomological exclusion
state/history reachability exclusion
control-interface exclusion
resource/capacity exclusion
path/access exclusion
institutional/deontic exclusion
epistemic/model exclusion
```

They can all answer the generic question:

> Why is T not currently actionable/open?

But their remediation differs:

```text
nomological: impossible under theory / redesign target
reachability: change initial/path/time/input dynamics
control: obtain actuator/policy/feedback
resource: acquire capacity/complements
access: repair route/interface
institution: obtain/change authority/rule status
epistemic: gather evidence/revise model
```

### Deep practical result

The explanatory value of typed modality is not merely philosophical. It localizes the **kind of change required** to alter the modal status.

## 34. Modal independence is relative to the claim universe

WDF1-1A does not claim every pair is logically independent under every formalization.

For example, if `R` is defined as reachable through physically law-conforming trajectories, then:

```text
R(T) => N(T)
```

by definition.

Likewise, if `F` is defined as reachability under resource-constrained action sets, feasibility can imply a corresponding control-reachability predicate.

Therefore the real result is more precise:

> **Several modal predicates are not coextensive. Their entailment relations depend on how the alternative universe, transition relation, Actor action set, institution and epistemic model are typed.**

This is stronger and safer than claiming a universal set of independent Booleans.

## 35. `Possible` often hides a quantifier

Many modal claims can be rewritten as existential/universal quantification over a declared alternative space:

```text
Possible(T)      ≈ ∃ admissible alternative/history where T
Necessary(T)     ≈ ∀ admissible alternatives/histories, T
Reachable(T)     ≈ ∃ admissible trajectory from actual x to T
Controllable(T)  ≈ ∃ Actor policy/action sequence producing/guaranteeing T under criterion
```

This suggests the modal foundation may depend less on one magical `Possibility` property and more on:

```text
AlternativeSpace
+ Admissibility relation
+ Transition/Accessibility relation
+ Quantifier
+ Dependence scope
```

However, institutional permission and dispositional modality may not reduce cleanly to this without importing constitutive rules or causal powers into `admissibility`.

This is a key WDF1-1B question.

## 36. Counterfactual implication

The matched cases sharpen the structure required for a counterfactual:

```text
Counterfactual(Ant, Consequent)
requires at least:
  alternative-generation operation
  preserved background/laws/rules
  changed variables/relations
  reachability/admissibility criterion
  identity/continuity criterion
  comparison target
```

A8/A9 demonstrate that changing authorization and changing physical resources are different surgeries even when both change actionability.

Thus:

```text
CounterfactualAlternative != Any logically describable alternative.
```

## 37. Chance implication

A13–A15 show three different things:

```text
set of possible outcomes
probability distribution over outcomes
observer uncertainty over token actuality
```

These must remain separate.

A future chance theory must explain whether objective chance belongs to:

- law/nomology;
- disposition/propensity;
- best-system probability;
- frequency/ensemble structure;
- something else.

WDF1-1A does not choose.

## 38. External anchors used in this sub-round

- RFC 9110, HTTP Semantics: `401 Unauthorized`, `403 Forbidden`, and authoritative-access semantics provide a concrete standards-level witness that protocol reachability/understanding and authorization/refusal are distinct.
- Kalman's 1960 control-theory work is retained as historical pressure for treating controllability as a system/input-relative question rather than plain state possibility; WDF1-1A deliberately uses simple toy systems rather than importing one control-theory definition as universal World ontology.
- Standard quantum theory's Born-rule probability assignments are used only to demonstrate that a probability value carries structure beyond binary possibility; no interpretation of quantum chance is selected.

## 39. WDF1-1A anti-laws

1. `NomologicalPossibility != ReachabilityFromActuality`.
2. `ReachabilityWithoutHorizon/InputSet != FullySpecifiedReachability`.
3. `NaturalReachability != ActorControl`.
4. `AbstractControlReachability != CurrentResourceFeasibility`.
5. `ResourceFeasibility != Access`.
6. `Access != Authorization`.
7. `Authorization != Feasibility`.
8. `Authorization != Capability`.
9. `InstitutionalPermission != PhysicalForce`.
10. `EpistemicOpenness != ObjectiveReachability`.
11. `ObjectiveReachability != EpistemicOpenness`.
12. `Possible != EquallyProbable`.
13. `PossibilityPredicate != ProbabilityValue`.
14. `EpistemicAlternativeSet != ObjectiveChanceDistribution`.
15. `Optionhood != ObjectiveModality`.
16. `Selection != Realization`.
17. `SameMathematicalFilterRepresentation != SameOntologicalRole`.
18. `LawRole != InitialConditionRole`.
19. `LawRole != HorizonRole`.
20. `ActorControlClaim != MereExistenceOfATrajectory`.

## 40. Exact residual entering WDF1-1B

WDF1-1A has now proved enough non-coextensiveness to reject one untyped possibility predicate, but has not established the best common structure.

Four architectures survive:

```text
A. Nested modal filters / possible-world subsets
B. Product/vector modal profile
C. Parameterized reachability + typed constraints
D. Typed modal pluralism with only local entailments
```

Each can reconstruct some cases; none yet reconstructs all without either redundancy or flattening constitutive/epistemic distinctions.

Therefore next exact sub-round:

# WDF1-1B — Candidate Modal Architectures

It must construct and deletion-test these rivals against the A1–A24 case suite, especially:

```text
- two-way feasibility/authorization independence;
- epistemic/objective mismatch;
- passive reachability vs Actor control;
- institutional constitution rather than physical exclusion;
- stochastic probability vs possibility;
- horizon/input/policy dependence;
- counterfactual alternative preservation.
```

No law theory, causal theory or chance ontology is selected yet.
## 41. Sub-round closeout

```text
WDF1-1A matched modal separation cases: COMPLETE
Cases constructed: A1–A24
Universal scalar possibility: REJECTED
Universal linear modal ladder: REJECTED
Parameterized reachability compression: SURVIVES AS RIVAL
Filter/intersection architecture: SURVIVES AS RIVAL
Vector/product architecture: SURVIVES AS RIVAL
Typed modal pluralism: SURVIVES AS RIVAL

Next: WDF1-1B Candidate Modal Architectures
```

