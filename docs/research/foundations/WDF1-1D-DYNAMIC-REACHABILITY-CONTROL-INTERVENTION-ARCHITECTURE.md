# WDF1-1D — Dynamic Reachability / Control / Intervention Architecture

Status: complete for WDF1-1D. No universal causal theory is selected. TARA survives and is strengthened by a policy/strategy layer. `Capability` is **not retained as a World root primitive**: it can be reconstructed as a supported, scoped projection over typed control/attainment relations, Actor interfaces, resources, authority/access, observation structure, horizon and success criterion. However, the compressed term remains useful operationally. `Intervention` is also not promoted as a universal primitive; it is reconstructed as a typed **mechanism-replacement / alternative-generation operation relative to a causal model and target query**, with an important separation from ordinary endogenous action. Exact next sub-round: **WDF1-1E — Objective Modality / Epistemic Openness / Probability / Chance Separation**.

## 0. Question

WDF1-1A proved:

```text
there exists a trajectory to T
!=
Actor A can control T.
```

WDF1-1B then suggested that dynamic/control modalities can be represented within TARA using typed transition relations and strategy operators. WDF1-1C isolated law/actuality/boundary roles so that control can condition on a declared nomological/dynamical model without claiming that the law metaphysics is solved.

WDF1-1D now asks:

> What is the minimum structure needed to say that an Actor can intentionally bring about, obtain, maintain, avoid, recover or influence an outcome — and when does an Actor action count as a causal intervention rather than merely another endogenous event?

This question sits directly underneath current Ordivon Capability doctrine.

## 1. Starting grammar

Let a controlled/open system be represented provisionally by:

```text
Nomological/dynamical base Θ
Actual anchor/history a
State/configuration representation X   [model-relative]
Actor A
Action/input interface U_A
Observation/interface O_A
Environment/disturbance/adversary E
Resource/capacity constraints R_A
Access/coupling conditions X_Access
Institutional authority/permission I_A
Policy/strategy class Π_A
Horizon H
Target/safety/outcome criterion K
```

No item above is assumed to be a universal production schema.

A generic policy-mediated trajectory family is:

```text
Traj_Θ(a | π_A, e, background)
```

for policy `π_A ∈ Π_A` and environment/disturbance/opponent realization `e`.

The central WDF1-1D task is to type the quantifiers and criteria over this family.

## 2. Natural reachability

A target T is naturally reachable from actuality if at least one admissible trajectory under the declared dynamics/background reaches T:

```text
NaturalReachable(T | a, Θ, H)
≈ ∃ trajectory τ from a, τ reaches T within H.
```

No Actor control is implied.

Examples:

- a decaying system eventually reaches zero;
- a scheduled external event occurs regardless of Actor choice;
- gravity causes an already released object to reach the ground.

### Hard separation

```text
NaturalReachability != ActorCapability
```

Mere eventual attainment does not establish that A possesses a control relation to the outcome.

## 3. Passive attainment

An Actor can sometimes `obtain` an outcome simply by waiting, observing or being present while an external process produces it.

Define:

```text
PassiveAttainment_A(T)
```

when T occurs in a way usable/receivable by A without an A-selectable action being a relevant difference-maker for occurrence.

Examples include:

- waiting for a scheduled public release;
- receiving a broadcast that arrives automatically;
- watching an autonomous process terminate.

### Result

```text
PassiveAttainment != Control
PassiveAttainment != Production
```

This matters because current Capability wording says `cause or obtain`; WDF1-1D finds that `obtain` is too broad unless its mode is typed.

## 4. Selectable enrollment / mediated attainment

Many real Ordivon cases are neither direct production nor passive waiting.

Example pattern:

```text
Actor selects request / enrollment action
→ external provider accepts request
→ provider-owned mechanism produces effect
→ Actor receives/uses result
```

The Actor does not own or control the provider's internal mechanism, but the outcome depends on the Actor's selectable enrollment relation.

Define:

```text
MediatedAttainment_A(T | Provider/Mechanism M)
```

when:

1. A has a selectable action/policy that invokes/enrolls M;
2. M has the relevant provider-owned capability/effect relation;
3. access, authority and resource conditions hold;
4. target T is obtained under the declared success criterion.

### Strong result

```text
CapabilityToObtain
can be compositional/delegated
without CapabilityToProduce internally.
```

This is a better reconstruction of API/tool/provider use than treating the Agent as the producer of every downstream effect.

## 5. Open-loop controllability / attainability

An open-loop control claim can be written:

```text
∃ action sequence u_0:H
such that trajectory reaches T.
```

The sequence is chosen without updating it in response to later observations.

This is stronger than natural reachability because the trajectory is generated/selected through an Actor-available input sequence.

But it remains weak under uncertainty.

### Separation

```text
OpenLoopAttainability
!=
FeedbackControl
```

because the successful sequence may depend on an unknown state/disturbance value that the Actor cannot know in advance.

## 6. Feedback/policy control

A feedback policy maps available information/history to actions:

```text
π_A : observation/history → action
```

Then:

```text
FeedbackReachable_A(T)
≈ ∃ π_A ∈ Π_A such that the closed-loop trajectory meets T
under the declared environment criterion.
```

The policy domain is not automatically the true state.

This distinction becomes essential under partial observability.

## 7. Partial observability

Smallwood & Sondik's classical POMDP formulation explicitly treats the controlled process's internal state as not directly observable; the controller receives outputs probabilistically related to the hidden state and chooses policy based on the resulting information/belief state.

WDF1 lesson:

```text
Policy(x_true)
```

is generally illegitimate if Actor A does not observe `x_true`.

The admissible policy must instead be based on:

```text
observations
observation history
belief/information state
memory
```

### Hard anti-law

```text
FullStateControllability != ActorControllabilityUnderPartialObservation
```

A control sequence can exist in state space while no realizable policy can choose it from the Actor's information.

## 8. Observability and controllability are different roles

An Actor may:

- observe a variable without being able to affect it;
- affect a variable without measuring its exact state;
- need both sensing and actuation for closed-loop control;
- exploit external feedback channels without owning either mechanism internally.

Therefore:

```text
Observability != Controllability
SensorAccess != ActuatorAccess
```

This directly reinforces Ordivon's Sense / Connect / Act separation.

## 9. Classical controllability is system/input-relative, not Actor-intrinsic

Kalman's foundational 1960 control work made controllability a property of a declared dynamical system together with its input structure, rather than a free-floating quality of a state or controller.

WDF1 generalization:

```text
ControllableBy_A(T)
```

must inherit at least:

```text
system boundary
dynamics/nomological model
Actor input interface
target class
horizon
```

and, for realistic Agents:

```text
observation structure
policy class
resources/access/authority
environment model
```

### Result

```text
Controllability != IntrinsicActorTrait
```

This aligns with the existing relational Capability doctrine but pushes the decomposition deeper.

## 10. Controllability vs stabilizability

Full controllability can be stronger than the operational requirement.

An Actor may not be able to reach every system state but may still be able to stabilize a desired equilibrium/region.

Thus:

```text
CanStabilize(T)
!=
CanReachEveryState
```

For World foundations, `control` should not be identified with one textbook controllability criterion.

## 11. Reach target vs remain safe

Control tasks split at least into:

```text
reachability / liveness:
  eventually enter target T

invariance / safety:
  remain inside safe set S for all relevant times
```

Ames et al.'s control-barrier-function work formalizes safety through forward invariance of a set and uses control constraints to guarantee that invariance while separately optimizing performance.

This provides a direct falsifier against:

```text
Capability = ability to reach a target only
```

### Anti-law

```text
Reachability != Viability/Safety
```

## 12. Viability

Viability theory asks whether there exists an evolution/control keeping the system within a declared constraint/safe set over time. The viability kernel identifies states from which such a viable evolution exists.

A generic Actor-relative form is:

```text
Viable_A(S | a, Θ, H)
≈ ∃ policy π_A such that
   for all relevant t ≤ H,
   trajectory remains in S
   under the declared environment criterion.
```

### Result

```text
CanReachGoal
and
CanStaySafe
```

are orthogonal capability questions.

A policy may reach a target only by leaving a safety region; another may remain safe forever without reaching the target.

## 13. Recoverability

A further relation is:

```text
Recoverable_A(FailureRegion → Safe/TargetRegion)
```

meaning A has a policy that can return the system from a failure/degraded region to a required safe/operational region under bounded conditions.

This is important for Ordivon because recovery is often more valuable than one-shot success.

### Anti-law

```text
NominalCapability != RecoveryCapability
```

## 14. Robust control

Under disturbances/adversarial environment choices, control strength depends on quantifier order.

Weak attainability:

```text
∃ π_A ∃ e : T
```

means some Actor policy and some favorable environment realization reach T.

Robust/guaranteed control:

```text
∃ π_A ∀ e ∈ E_admissible : T
```

means one Actor policy succeeds against all declared disturbances/opponents.

These are radically different.

### Hard anti-law

```text
PossibleUnderFavorableEnvironment
!=
RobustlyControllable
```

## 15. Strategic / multi-Agent control

Alternating-time temporal logic gives a formal counterpart to this quantifier structure by allowing selective quantification over paths compatible with a coalition's strategy while the rest of the system/environment retains choices.

For coalition `C`:

```text
∃ strategy_C
∀ strategies_not-C
  target property holds
```

This is not reducible to simple graph reachability.

### Result

```text
MultiAgentCapability
is strategy- and opponent-model-relative.
```

The Actor boundary/coalition definition itself matters.

## 16. Stochastic/probabilistic control

Another criterion is neither existential nor worst-case universal:

```text
∃ π_A : P_μ(T | π_A) ≥ p
```

or:

```text
π_A maximizes E[U(outcome)]
```

This introduces a measure/chance/model layer.

WDF1-1D does not decide whether `μ` is objective chance or model probability.

### Separation

```text
RobustGuarantee
!=
HighProbabilitySuccess
!=
HighExpectedUtility
```

A policy with 99% success is not a guarantee; a policy with highest expected utility may accept low-probability catastrophic outcomes unless the objective forbids them.

## 17. Control objective is not one scalar notion

At least these success semantics must remain typed:

```text
existential attainability
finite-horizon reachability
stabilization
tracking
safety / invariance
viability
recovery
robust guarantee
probabilistic threshold
expected utility / cost optimization
multi-objective tradeoff
```

### Anti-law

```text
ControlSuccess != OneUniversalPredicate
```

## 18. Policy class matters

A system can be controllable under a rich policy class but not under a restricted one.

Examples:

```text
continuous feedback vs discrete actions
memoryless vs history-dependent
centralized vs decentralized
full-state vs observation-based
bounded-compute vs unrestricted
safe-policy-only vs unrestricted
```

Therefore:

```text
Capability_A(T)
```

without a policy/action-class dependence can overstate real ability.

## 19. Computation is itself a control resource/constraint

For an Agent, a policy that exists mathematically but cannot be computed before the action deadline may not be operationally realizable.

Thus:

```text
ExistenceOfPolicy
!=
ActionablePolicyForActorNow
```

when computation/time/memory constraints are material.

This belongs under resource/feasibility rather than nomological possibility.

## 20. Access as control coupling

WDF1-1B suspected that Access can be reduced to typed coupling/reachability.

D refines this into two main forms:

```text
SensorCoupling_A:
  can A obtain the observations required by policy π?

ActuatorCoupling_A:
  can A realize/dispatch the actions assumed by policy π?
```

plus external service/tool coupling.

### Provisional disposition

```text
Access does not require an independent modal root.
```

It is a typed coupling condition on observation/action/enrollment paths, while the word remains useful for failure localization.

## 21. Resource/capacity feasibility as policy-set restriction

Resources do not create a new modality primitive.

They restrict which policies/actions are currently realizable:

```text
Π_A^effective
= Π_A
  ∩ ResourceFeasible
  ∩ CapacityFeasible
  ∩ AccessRealizable
  ∩ current technical compatibility
```

This is a useful derived intersection.

But blocker provenance remains typed.

### Result

```text
Feasibility can often be reconstructed as admissibility over a policy/action set.
```

without turning all constraints into one ontology.

## 22. Authority/permission enters differently

Institutional authorization can also restrict the policy/action set used for **admitted actionability**:

```text
Π_A^admitted
= Π_A^effective ∩ AuthorizedActions_A
```

but WDF1-1B/C established that authorization may first require constitutive status evaluation.

Therefore:

```text
Constitutive/Deontic Evaluation
→ admissible policy projection
```

not:

```text
physical inability by default.
```

## 23. Physical ability vs admitted ability

This yields a clean split:

```text
PhysicallyControllable_A(T)
```

vs

```text
AdmissiblyControllable_A(T)
```

where the latter also respects institutional/safety/resource policies.

### Hard anti-law

```text
PhysicalControlAbility != Authorized/AdmittedControlAbility
```

This directly preserves the existing Ordivon firewall:

```text
PhysicalAbility != Capability != Authority
```

while providing a deeper derivation.

## 24. Delegated control

Suppose A can issue a request to provider P, while P independently controls the downstream mechanism.

Then the composed attainment relation can look like:

```text
A controls/selects enrollment/request q
P owns capability CP(T | q)
Authority/access/admission connect q to P
→ A can obtain T through P
```

A does not thereby gain P's internal actuator set or authority.

### Result

```text
DelegatedCapability
!=
TransferredMechanismOwnership
!=
TransferredAuthority
```

This is especially important for Agent-first tool use.

## 25. Capability can be composed without identity fusion

For Human-Agent/tool systems or Agent-provider systems:

```text
JointCapability(A ⊕ Tool, T)
```

can exceed the independent capability of either component.

The capability claim belongs to the declared system boundary.

Therefore:

```text
JointSystemCapability
!=
ComponentIntrinsicCapability
```

and component replacement can preserve joint role if the relevant control/enrollment relations are preserved.

## 26. Capability expression vs production remains separate

Current conditions can enlarge `Π_A^effective` or improve observation/access without changing retained Actor state.

That is capability **expression**.

Capability production instead changes later policy/model/body/interface state such that future ability persists after the immediate support is removed.

### Anti-law

```text
CurrentControlSuccess
!=
RetainedCapabilityProduction
```

WDF1-1D retains this existing doctrine unchanged.

## 27. What is an ordinary endogenous action?

Consider a causal/dynamic model with an action variable:

```text
A_t = π(O_≤t)
```

The Agent's action is generated by the policy and observations inside the modeled system.

This is an **endogenous action occurrence**.

It can causally influence downstream variables, but its occurrence does not by itself perform a model surgery on the action-generating mechanism.

### Hard anti-law

```text
EndogenousAction != InterventionOperator
```

## 28. Pearl-style intervention as structural replacement

In structural causal modeling, an intervention such as:

```text
do(X=x)
```

is represented by replacing the structural equation/mechanism that normally determines X with the constant assignment `X=x`, while leaving the other structural equations intact.

The intervention is therefore not merely `observe X=x` and not merely `X happens to equal x`.

### Hard anti-laws

```text
Observe(X=x) != do(X=x)
EndogenousOccurrence(X=x) != do(X=x)
```

This is one of the most important WDF1-1D separations.

## 29. Policy intervention

A richer operation can replace the normal action mechanism not with a constant but with a policy:

```text
A_t := π'(O_≤t)
```

Conceptually:

```text
intervene on action-generation rule
```

rather than one token action value.

This is relevant to:

- policy evaluation;
- institution rule change;
- controller replacement;
- Agent behavior experiments.

### Result

```text
ValueIntervention != Policy/MechanismIntervention
```

## 30. Mechanism intervention

One can intervene on the structural function itself:

```text
f_X := f'_X
```

rather than setting one value of X.

This changes a **mechanism/policy/dynamics relation** across multiple contexts.

### Anti-law

```text
MechanismChange != VariableValueChange
```

This distinction will matter later for institutional and software changes.

## 31. Intervention is model-relative

A `do(X=x)` operation is defined relative to:

```text
chosen variable X
chosen structural equations
chosen model boundary
chosen invariant mechanisms
```

Changing the variable decomposition can change what the same physical manipulation corresponds to formally.

Therefore:

```text
SCMIntervention != ModelFreeRealityPrimitive
```

It is a typed alternative generator/evaluation operator over a causal model.

## 32. Physical intervention vs formal intervention

A real experiment/manipulation may be represented by a formal intervention only if the physical procedure approximately satisfies the model's intervention assumptions.

Examples of failure:

- manipulation changes X and directly changes Y through another path;
- manipulation also changes confounders/background;
- intervention changes the downstream mechanism one intended to hold fixed;
- measurement procedure alters the system in an unmodeled way.

### Anti-law

```text
PhysicalManipulation != ValidFormalIntervention by default
```

## 33. Intervention need not be anthropocentric

Interventionist causal formalisms can use hypothetical or natural intervention variables/operations; the concept does not require a human hand.

For Ordivon this means an automated Agent, process or natural shock can realize an intervention-like contrast if the structural conditions are satisfied.

But:

```text
NonhumanOccurrence != Intervention automatically.
```

Isolation/surgery semantics still matter.

## 34. Control does not imply intervention

A feedback controller can successfully steer a system while acting through the normal endogenous action channel:

```text
A_t = π(O_t)
```

The controller is part of the system's ordinary closed-loop dynamics.

Thus:

```text
ControlAction != InterventionOperator
```

unless the causal query specifically compares a surgery/replacement of an action variable/mechanism.

## 35. Intervention does not imply control of target

A model may permit a clean intervention on X:

```text
do(X=x)
```

while Y is unaffected or only weakly affected.

Therefore:

```text
Intervenable(X)
!=
CanControl(Y)
```

A variable can be manipulable without being a useful handle for the target.

## 36. Causal effect vs control ability

A causal-effect question asks something like:

```text
How would Y change under intervention on X?
```

A control question asks:

```text
Does there exist an admissible policy over available handles that achieves criterion K?
```

The latter can combine multiple causal channels, observations, feedback and constraints.

Therefore:

```text
CausalEffect(X→Y)
!=
Capability_A(Y)
```

A causal relationship can exist where A has no access/control over X; A can control Y through another channel without needing X.

## 37. Successful control does not imply mechanism knowledge

A controller may be learned, empirical, adaptive or black-box and still achieve stable control under a domain/regime.

Operational control success therefore does not by itself establish:

```text
complete causal mechanism
correct ontology
transport outside the tested regime
```

### Anti-law

```text
ControlSuccess != MechanisticExplanation
```

This preserves WDF0's operational-adequacy vs ontological-adequacy firewall.

## 38. Mechanism knowledge can improve control without being identical to it

Mechanistic understanding can improve:

- transfer;
- diagnosis;
- intervention localization;
- robustness;
- extrapolation;
- failure recovery.

But it is evidence/structure supporting control claims, not the same semantic relation as `can control`.

## 39. Causal variables are handles/interfaces, not automatically Reality primitives

SCM and interventionist formalisms gain power by choosing variables on which interventions and counterfactuals can be defined.

WDF0-D/E already established that variables/scales are model-selected.

WDF1-1D therefore retains:

```text
GoodCausalHandle != FundamentalRealityVariable
```

A coarse variable may be an excellent intervention/control interface while being multiply realized.

## 40. Control abstraction across scale

Suppose many microstates realize the same macro control variable M.

If interventions/policies on M produce stable target behavior across admissible realizers, M can be a valid causal/control abstraction.

But if micro-realization differences change the response, the abstraction can fail under intervention/transfer.

### Result

```text
ControlAbstractionValidity
is intervention/regime/realization-relative.
```

This links WDF1-1D back to WDF0-E macro validity.

## 41. Safety/viability exposes a crucial difference from causal effect

Knowing that increasing input X raises Y is insufficient to know whether a policy can keep the entire system inside a safe set while achieving a target.

Control-barrier-function results show that safety is naturally a set-invariance problem with explicit constraints on allowable control inputs, distinct from mere causal effect estimation.

Therefore:

```text
CausalEffectKnowledge
!=
SafeControllerExistence
```

## 42. Open systems require explicit environment quantification

For a closed deterministic model, one action sequence may determine a trajectory.

For an open system, the environment contributes:

```text
disturbances
other agents
provider decisions
network failures
market movements
unmodeled events
```

Capability claims therefore require an environment quantifier/assumption.

Examples:

```text
best-case capability: ∃π ∃e
expected capability: ∃π E_e[utility]
chance-constrained capability: ∃π P_e(success)≥p
robust capability: ∃π ∀e
```

### Hard anti-law

```text
CapabilityWithoutEnvironmentQuantifier
can be underspecified.
```

## 43. Environment model vs Reality

The `e` alternatives used in a controller are model-selected.

Actual Reality can produce an out-of-model disturbance.

Therefore:

```text
RobustToModeledDisturbances
!=
RobustToAllReality
```

A capability claim must bind its disturbance/environment class and reopen condition.

## 44. Control horizon matters

An Actor can be able to reach a target eventually but not before deadline H.

Or a system can be kept safe for 10 minutes but not indefinitely.

Therefore:

```text
Capability_H1 != Capability_H2
```

without contradiction.

Horizon remains a Dependence Signature coordinate.

## 45. Success tolerance matters

A controller can place a state within ε of target but not exactly at target; or guarantee safety only with a bounded violation probability.

Thus the target criterion must declare:

```text
exact vs approximate
probability threshold
safety margin
tracking tolerance
cost bound
```

### Anti-law

```text
Capability != ToleranceFreeBoolean by default
```

## 46. Currentness matters

Actuator failure, permission revocation, resource depletion, path loss or state drift can invalidate a previously established control relation.

Therefore:

```text
HistoricalCapabilityEvidence
!=
CurrentCapability
```

The existing Ordivon currentness doctrine remains foundationally justified.

## 47. Evidence strength matters

A single successful episode supports only a bounded existence claim under observed conditions.

Stronger claims require stronger tests:

```text
repeatability
varied initial conditions
support removal
adversarial/disturbance testing
partial-observation testing
transfer
recovery
intervention tests
```

### Result

```text
ObservedSuccess
!=
RobustCapability
```

## 48. Capability reconstruction

WDF1-1D can now reconstruct Capability without a root primitive.

For Actor/system boundary A, target criterion K and conditions Γ:

```text
CapabilityClaim(A,K | Γ)
= supported claim that there exists an A-admissible
  policy/enrollment/control relation satisfying the declared
  success operator over the declared environment/horizon,
  given current observation/action coupling,
  resources/capacity, access and authority,
  with explicit evidence/currentness.
```

A more formal research skeleton:

```text
Cap_{A,K}(
  Θ,
  a,
  O_A,
  U_A,
  Π_A,
  E,
  Res_A,
  Access_A,
  Authority_A,
  H,
  SuccessOperator,
  Evidence
)
```

This is intentionally a **projection formula**, not a production object.

## 49. Capability types become query operators

Instead of one hidden essence, different capability claims correspond to different operators:

```text
AttainableCapability:
  ∃π ∃e  Reach(T)

GuaranteedControlCapability:
  ∃π ∀e  Reach(T)

ProbabilisticCapability_p:
  ∃π  P(Reach(T)) ≥ p

SafetyCapability:
  ∃π ∀t  x_t ∈ Safe

RecoveryCapability:
  ∃π  Return(Failure→Safe)

DelegatedAttainmentCapability:
  ∃ enrollment/request policy + provider capability chain

AuthorizedCapability:
  above + deontic/authority admission
```

Thus `Capability` is a family of scoped modal/control projections.

## 50. Does Capability fully reduce?

### Ontologically/root-wise: YES, provisionally

No WDF1-1D falsifier requires a separate primitive `Capability` property beyond:

```text
Actor/system boundary
alternative/dynamical structure
observation/action coupling
policy/strategy quantification
resources/access/authority
success criterion
horizon/environment
supporting evidence/currentness
```

### Semantically/operationally: NO deletion

The term remains highly useful because consumers need a compressed answer:

> Can this declared system boundary achieve/maintain/obtain K under Γ?

Therefore:

```text
CapabilityRootPrimitive: REJECT
CapabilityDerivedProjection: RETAIN STRONGLY
```

## 51. `Ability` and `power` remain unresolved metaphysically

The reduction above is a World research/operational reconstruction.

It does not settle whether physical objects possess irreducible dispositional powers in the metaphysical sense.

Thus:

```text
ActorCapabilityProjection
!=
DispositionalPowersMetaphysics
```

The powers/disposition law/causation rival remains open for later WDF1.

## 52. Intervention reconstruction in TARA

TARA can now specialize an intervention as an **alternative generator over a causal model**:

```text
Intervene(M, SurgerySpec S)
→ M^S
```

where `S` may replace:

```text
variable assignment
policy/mechanism
structural function
edge/coupling
institutional rule representation
```

and the query states which other mechanisms/background relations are intended to remain invariant.

### Result

```text
Intervention
= typed model-relative alternative-generation operation
```

not a universal physical primitive.

## 53. Intervention validity is query-relative

A manipulation can be a valid intervention for one causal query and invalid for another if it creates a direct side path or changes a mechanism that the second query intended to hold fixed.

Therefore:

```text
ValidIntervention(S | X,Y,M)
```

must bind target variables/query/model.

### Anti-law

```text
Intervention != ContextFreeActionType
```

## 54. Intervention and control form a bridge but not identity

They connect in two directions:

```text
causal intervention models
→ identify useful control handles

control policies/experiments
→ generate interventions/evidence for causal relations
```

But:

```text
Control != Intervention
Intervention != Control
```

This firewall survives strongly.

## 55. Action chain refinement

WDF0/Runtime had:

```text
Intent != Action != Realization != Effect != Observation
```

WDF1-1D adds:

```text
ActionOccurrence
!= ControlRelation
!= InterventionOperation
!= CausalAttribution
```

One admitted action can fail; one successful effect can be caused by multiple factors; one intervention is a counterfactual/model surgery relation; one capability is a supported modal projection.

## 56. Ordivon provider/tool example

A generic external-tool capability can now be decomposed:

```text
Agent policy chooses request q
+ current Connector/Access path realizes q
+ authority permits q
+ provider admits q
+ provider-owned mechanism executes q
+ effect owner reconciles result
→ Agent can obtain target effect class T under Γ
```

Important non-collapses:

```text
AgentCanObtain(T)
!= AgentOwnsProducingMechanism(T)

AgentCanRequest(T)
!= ProviderWillSucceed(T)

ProviderEffect
!= DomainOutcome

EffectReceipt
!= CausalAttributionOfValue
```

This is a direct foundational reconstruction of current World engineering semantics.

## 57. Control failure taxonomy

Given `CapabilityClaim=false/UNKNOWN`, WDF1-1D distinguishes:

```text
NOMIC/DYNAMIC GAP
  no admissible trajectory/model relation

INITIAL/STATE GAP
  target unreachable from current anchor

OBSERVATION GAP
  policy needs information Actor cannot obtain

ACTUATION GAP
  Actor lacks an input/control interface

POLICY GAP
  no admissible policy known/exists in declared class

ROBUSTNESS GAP
  only favorable-environment trajectories work

RESOURCE GAP
  energy/capital/time/compute/capacity insufficient

ACCESS GAP
  sensor/actuator/provider path unavailable

AUTHORITY GAP
  action exists physically but is not admitted/authorized

PROVIDER/MEDIATION GAP
  delegated mechanism unavailable/refuses/fails

EVIDENCE GAP
  capability may exist but support/currentness is insufficient
```

This is a research taxonomy, not a production state machine.

## 58. Capability acquisition becomes change of the determining structure

A capability can be created/enlarged by changing different coordinates:

```text
learn better policy
add sensor
add actuator
increase compute/resource
open access path
obtain permission
contract external provider
change system dynamics/design
reduce disturbance set
change target/tolerance/horizon
improve evidence without changing Reality capability
```

The last case is crucial:

```text
CapabilityRealityChange
!= CapabilityKnowledgeChange
```

## 59. Capability loss similarly decomposes

Loss can arise through:

```text
resource exhaustion
hardware failure
path loss
authority revocation
provider change
environment regime shift
policy/model staleness
body/interface change
state drift into uncontrollable region
```

No single `capability state machine` is implied.

## 60. Control and current state can be non-monotonic

An Actor can have capability in one region of state space and lose it after crossing a boundary/invariant/viability limit.

Thus capability can be:

```text
state-dependent
history-dependent
resource-dependent
regime-dependent
```

### Anti-law

```text
CapabilityOnceEstablished != CapabilityForever
```

## 61. Control authority can be delegated separately from causal ability

An institution can authorize A to issue commands to a system whose physical control mechanism is owned by B.

Thus:

```text
AuthorityToCommand
!= PhysicalActuationOwnership
```

Yet the composite system can give A an admitted control capability via B.

This again argues for relational/compositional capability rather than possession metaphors.

## 62. Causal intervention on institutions requires care

Changing an institutional rule may:

1. constitute new permissions/statuses;
2. causally alter subsequent behavior through incentives/enforcement/information;
3. change the causal model's action space itself.

Therefore a `do(rule=r')` representation can be operationally useful, but the real change is not merely a physical variable assignment.

### Anti-law

```text
InstitutionRuleChange != PurePhysicalVariableIntervention
```

The causal model must preserve the constitutive layer rather than erase it.

## 63. Multi-level interventions require realization consistency

If a macro variable is realized by lower-level configurations, intervening on the macro variable typically requires changing some realizer consistently.

One cannot demand:

```text
change macro M
while holding all realizing micro facts fixed
```

when that is constitutively impossible.

### Result

```text
InterventionOnMacro
must respect RealizationMap.
```

This preserves WDF0-E's anti-double-counting/realization discipline.

## 64. Causal handle quality is graded

A variable/action can be a better control handle when its intervention relation is:

```text
stable across backgrounds
specific to target
low side-effect
observable/actuable
resource-efficient
robust
reversible/recoverable
```

These are dimensions of useful control/interface quality, not proof of fundamental ontology.

## 65. Control does not require free will metaphysics

The architecture only needs Actor-indexed selectable/policy alternatives within the model/system boundary.

It does not require resolving libertarian free will or metaphysical indeterminism.

An Agent/controller can be physically deterministic while its policy still defines a meaningful control relation in the model/system.

### Anti-law

```text
ControlTheoryActorChoice
!=
MetaphysicalFreeWillCommitment
```

## 66. TARA refinement after D

TARA now has a more precise action/control branch:

```text
AlternativeDomain:
  trajectories / policies / strategy outcomes

Relation/Generator:
  dynamics + input/coupling + environment transitions

Operator:
  ∃path
  ∃action-sequence
  ∃policy
  ∃policy∀disturbance
  ∃strategy∀opponents
  probability threshold
  invariance/viability criterion

Background/Dependence:
  Θ, actual anchor, horizon, observations,
  policy class, resources, access, authority,
  disturbance class, target/tolerance
```

Intervention is added as a distinct alternative generator:

```text
Model surgery / mechanism replacement
```

rather than merged with ordinary policy execution.

## 67. Strongest result 1 — Capability is quantifier structure over a relation, not a possession

The deep reconstruction is:

```text
Capability
≈ supported truth of an Actor-indexed modal/control formula
under declared scope.
```

For example:

```text
∃π_A ∀e : K(Traj_Θ(a,π_A,e))
```

plus resource/access/authority/evidence conditions.

This explains why a global `CapabilityScore` was always structurally suspect.

## 68. Strongest result 2 — control strength is quantifier-sensitive

The difference between:

```text
∃π∃e
∃π P_e≥p
∃π∀e
```

is not cosmetic.

It changes the semantic claim from favorable-case attainability to probabilistic competence to robust guarantee.

Thus capability confidence/strength cannot be represented merely by attaching one confidence number to an untyped capability label.

## 69. Strongest result 3 — sensing belongs inside capability when policy depends on it

Under partial observability:

```text
Actuator exists
```

is not enough.

A realizable feedback policy depends on the information actually exposed through A's sensing/interface path.

Hence:

```text
Capability can depend on Body/Sensor relation
without Sensor becoming Capability itself.
```

This reconnects World Sense and Act at a deeper control level while preserving their separation.

## 70. Strongest result 4 — viability/recovery are first-class capability questions

Ordivon should conceptually value:

```text
Can remain inside acceptable region?
Can recover after perturbation/failure?
```

alongside:

```text
Can reach target once?
```

This follows from control/viability foundations, not an engineering preference.

## 71. Strongest result 5 — intervention is an epistemic/causal modeling operation plus possible physical realization

The cleanest current reconstruction is:

```text
formal intervention:
  typed surgery on a causal model's determining relation

physical experimental intervention:
  real manipulation judged to satisfy the formal isolation/invariance assumptions sufficiently for a causal query
```

Neither is identical to generic Agent action.

## 72. WDF1-1D hard anti-laws

1. `NaturalReachability != ActorCapability`.
2. `PassiveAttainment != Control`.
3. `CapabilityToObtain != CapabilityToProduce`.
4. `DelegatedCapability != MechanismOwnership`.
5. `OpenLoopAttainability != FeedbackControl`.
6. `FullStateControllability != ControlUnderPartialObservation`.
7. `Observability != Controllability`.
8. `SensorAccess != ActuatorAccess`.
9. `Controllability != IntrinsicActorTrait`.
10. `FullControllability != Stabilizability`.
11. `Reachability != Viability/Safety`.
12. `NominalCapability != RecoveryCapability`.
13. `FavorableCaseAttainability != RobustControl`.
14. `RobustGuarantee != HighProbabilitySuccess`.
15. `HighProbabilitySuccess != HighExpectedUtility`.
16. `ControlSuccess != OneUniversalPredicate`.
17. `ExistenceOfPolicy != ActionablePolicyNow`.
18. `Access != IndependentModalRoot` provisionally; access is typed coupling/reachability.
19. `PhysicalControlAbility != AuthorizedControlAbility`.
20. `JointCapability != ComponentIntrinsicCapability`.
21. `CurrentControlSuccess != RetainedCapabilityProduction`.
22. `EndogenousAction != InterventionOperator`.
23. `Observe(X=x) != do(X=x)`.
24. `EndogenousOccurrence(X=x) != do(X=x)`.
25. `ValueIntervention != Policy/MechanismIntervention`.
26. `MechanismChange != VariableValueChange`.
27. `SCMIntervention != ModelFreeRealityPrimitive`.
28. `PhysicalManipulation != ValidFormalIntervention by default`.
29. `ControlAction != InterventionOperator`.
30. `Intervenable(X) != CanControl(Y)`.
31. `CausalEffect != ActorCapability`.
32. `ControlSuccess != MechanisticExplanation`.
33. `GoodCausalHandle != FundamentalRealityVariable`.
34. `CausalEffectKnowledge != SafeControllerExistence`.
35. `RobustToModeledDisturbances != RobustToAllReality`.
36. `Capability != ToleranceFreeBoolean by default`.
37. `HistoricalCapabilityEvidence != CurrentCapability`.
38. `ObservedSuccess != RobustCapability`.
39. `ActorCapabilityProjection != DispositionalPowersMetaphysics`.
40. `Intervention != ContextFreeActionType`.
41. `InstitutionRuleChange != PurePhysicalVariableIntervention`.
42. `InterventionOnMacro must respect RealizationMap`.
43. `ControlTheoryActorChoice != MetaphysicalFreeWillCommitment`.

## 73. External evidence retained in D

Primary/authoritative pressure:

- R. E. Kalman, *On the General Theory of Control Systems* (1960): foundational system/input-relative controllability and observability framework.
- Richard D. Smallwood & Edward J. Sondik, *The Optimal Control of Partially Observable Markov Processes over a Finite Horizon* (Operations Research, 1973): controller acts under hidden internal state using probabilistically related observations/information state.
- Jean-Pierre Aubin's viability theory and Aubin/Frankowska viability work: viability kernels/controlled invariance distinguish maintaining admissible/safe evolution from simple target reachability.
- Aaron D. Ames, Xiangru Xu, Jessy W. Grizzle & Paulo Tabuada, *Control Barrier Function Based Quadratic Programs for Safety Critical Systems* (IEEE TAC, 2017): safety expressed through forward invariance and control-input constraints, separable from performance objectives.
- Rajeev Alur, Thomas Henzinger & Orna Kupferman, *Alternating-Time Temporal Logic* (Berkeley technical report / JACM): coalition/strategy-selective path quantification separates strategic ability from ordinary path possibility.
- Judea Pearl, structural causal model work / *Causality*: intervention `do(x)` is modeled by replacing the structural equation for X while leaving the remaining structural model intact.
- James Woodward's interventionist work is retained as philosophical pressure that causal intervention should be understood through appropriately isolated manipulations/difference-making rather than generic human action; WDF1 does not adopt interventionism as the universal metaphysics of causation.

## 74. What D does not solve

WDF1-1D intentionally leaves open:

```text
objective chance vs model probability
probability semantics under stochastic control
causal truthmakers behind SCM invariance
actual/token causation
preemption and omission
mechanism vs difference-making priority
law metaphysics
physical powers/dispositions
counterfactual similarity/background selection
```

These are not hidden by the control reconstruction.

## 75. Exact residual entering WDF1-1E

D can express stochastic/probabilistic capability only by injecting a measure/model:

```text
∃π : μ(success | π) ≥ p
```

But WDF1 still does not know what `μ` means ontologically.

Likewise an Agent's uncertainty over hidden state or response-loss alternatives is epistemic and can coexist with deterministic Reality.

The next sharp residual is therefore:

# WDF1-1E — Objective Modality / Epistemic Openness / Probability / Chance Separation

It must attack:

```text
1. epistemic possibility vs objective possibility;
2. probability as degree of belief vs model frequency vs objective chance;
3. stochastic transition law vs uncertainty about hidden state/model;
4. zero probability vs impossibility;
5. propensity/disposition vs best-system chance rivals;
6. calibration/frequency evidence vs token chance;
7. partial-observation belief state vs Reality state;
8. how chance enters TARA as measure/operator without becoming one generic uncertainty primitive;
9. whether expected/probabilistic capability claims require objective chance or can be model-relative;
10. what reopen conditions apply when probability model class is wrong.
```

No law/causal theory is selected before E.

## 76. WDF1-1D closeout

```text
WDF1-1D1 natural/open-loop/feedback/robust/viable separation  COMPLETE
WDF1-1D2 Actor actions/observations/policies/resources         COMPLETE
WDF1-1D3 action vs intervention                               COMPLETE
WDF1-1D4 resource/access/authority integration                COMPLETE
WDF1-1D5 multi-Agent/strategic control                        COMPLETE
WDF1-1D6 Capability destructive reconstruction                COMPLETE

Capability root primitive: REJECTED
Capability derived scoped projection: STRONGLY RETAINED
Access independent modal root: PROVISIONALLY REJECTED
Intervention universal primitive: REJECTED
Intervention typed causal-model surgery/operator: RETAINED
TARA: SURVIVES AND STRENGTHENED

Next:
WDF1-1E Objective Modality / Epistemic Openness / Probability / Chance Separation
```
