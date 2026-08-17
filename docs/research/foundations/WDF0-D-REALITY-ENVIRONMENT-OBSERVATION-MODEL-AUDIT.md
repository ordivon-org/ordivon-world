# WDF0-D — Reality / Environment / Observation / Representation / WorldModel Audit

Status: complete for WDF0-D. No positive World ontology is frozen. WDF0-E scale/composition/emergence audit is the next admitted sub-round. WDF1 remains UNKNOWN.

## 0. Question

WDF0-C produced a ten-coordinate question grammar but left a dangerous ambiguity: some coordinates may describe Reality itself, some a selected system/environment relation, some an observer/model, and some a constitutive social/institutional relation.

WDF0-D asks:

> Which distinctions are about Reality, which are about a target-system/environment decomposition, which are about measurement/observation/modeling, and which only exist in relations among these layers?

The round rejects a simple `objective vs subjective` binary and instead audits dependency structure.

## 1. Starting firewall

The following chain must not collapse:

```text
Reality
  != Target specification
  != Measurement interaction
  != Indication / Signal
  != Data / Record
  != Observation
  != Evidence
  != Representation
  != Belief
  != Model
  != Simulation
  != Prediction
  != Action
```

Several arrows can be causal, inferential, constitutive or representational rather than identity relations.

## 2. Reality — provisional research role

WDF0-D does not define metaphysical Reality exhaustively. It retains a weaker but durable commitment:

```text
Reality = that which a claim, model, observation or action is answerable to,
and which is not exhausted by the current observer's representation of it.
```

This formulation deliberately avoids equating Reality with `mind-independent physical matter`, because institutional, semantic and social facts can depend on other minds/rules/collectives while remaining independent of whether the current Ordivon Agent models them correctly.

Therefore:

```text
Model-independent-from-this-observer
!=
independent-of-all-agents/institutions.
```

A company can be institution-dependent yet model-transcendent relative to one Agent. A legal status may cease if the institution/rule ceases, but it does not cease merely because an observing Agent has the wrong belief.

## 3. `World` is too overloaded to be a current foundation primitive

Current Ordivon uses at least three meanings:

1. **Reality-totality sense** — `the world` as everything actual.
2. **Domain/environment sense** — `the game world`, `social world`, `external world`.
3. **Engineering World project sense** — the boundary between Host-owned work semantics and independently authoritative environments.

These are not interchangeable.

WDF0-D therefore does **not** define a universal `World` object.

For research, use:

```text
Reality        — upstream referent
Target         — what a question/model is about
System_K       — a target individuated under criterion K
Environment_K  — relevant external/coupled Reality relative to System_K
WorldModel_A,Q — an Agent/modeler's scoped representation for question Q
```

`World` remains the programme/domain label until later reconstruction determines whether it has a sharper foundation role.

## 4. System and Environment are relational decompositions

A system/environment split requires at least a criterion and scope:

```text
System_K(S, BoundaryCriterion, Scale, Time)
Environment_K(S)
```

Environment is therefore not `the rest of Reality` in an undifferentiated set-complement sense. It is the part of Reality outside/across the chosen boundary that is relevantly coupled to the target for the question at hand.

Examples:

- organismal environment can differ from legal/social environment;
- process environment can differ from host-machine environment;
- an Agent's sensor-accessible environment can be smaller than the external reality affecting it;
- a firm's competitive environment differs from its physical room surroundings.

Markov-blanket work is useful pressure here: it defines internal/external separation statistically through conditional independence, admits nested boundaries, and explicitly notes that such boundaries need not coincide with ordinary biophysical boundaries.

Hence:

```text
Environment_S != Reality
Environment_S != Observable_S
Observable_S != Observed_S
```

## 5. Measurement is not a transparent read of Reality

The International Vocabulary of Metrology (VIM) is unusually valuable because it makes several hidden modeling assumptions explicit:

- measurement is an experimental process for obtaining values reasonably attributable to a quantity;
- measurement presupposes a description of the quantity appropriate to intended use, a procedure, a calibrated measuring system and measurement conditions;
- the measurand is the quantity intended to be measured;
- the measuring system and conditions can themselves change the target phenomenon, so the actually measured quantity may differ from the defined measurand;
- a measurement result includes values attributed to the measurand plus relevant information, normally including uncertainty;
- a measurement model is a mathematical relation among quantities known to be involved in the measurement.

World implication:

```text
TargetReality
  ↓ specification
Measurand / target property
  ↓ measurement interaction
Indication / sensor signal
  ↓ calibration + correction + model
Measurement result
```

This destroys the naive chain:

```text
SensorOutput = RealityValue
```

### 5.1 Observation can be intervention

Measurement may perturb the target. Therefore:

```text
Observe(X) can causally change X.
```

This is not restricted to quantum measurement. A voltmeter can load a circuit; a biological assay can change a specimen; active sensing moves cameras, bodies or probes.

Therefore World must distinguish:

```text
pre-observation target condition
measurement/observation interaction
post-observation target condition
```

when perturbation matters.

### 5.2 Target specification precedes measurement result

The VIM requirement that a measurand be specified shows that `what exactly was measured?` is not answered by raw sensor output alone.

Hence:

```text
Indication != Measurand
MeasurementResult != UnmediatedReality
```

but also:

```text
MeasurementResult != MereSubjectiveOpinion
```

A well-specified result is a constrained, traceable epistemic relation to Reality.

## 6. Signal, data, observation and evidence separate

### 6.1 Signal / indication

A signal is a physically or digitally realized carrier/variation that can participate in sensing or communication. An instrument indication is an instrument-produced value.

It can exist without anyone currently interpreting it correctly.

### 6.2 Data / record

Data is an encoded retained representation of an indication, event, state, content or other source.

A record can preserve:

- signal sample;
- timestamp;
- metadata;
- provenance;
- transformed/calibrated value.

But:

```text
Record != OriginalOccurrence
```

### 6.3 Observation

For WDF0, `Observation` is retained as an acquisition/result role:

```text
Observation_A(X, Path, Conditions, Time)
```

It says some observer/system gained bounded information about a target through a path under conditions.

It does **not** imply:

- total access to X;
- truth of every interpretation;
- currentness outside the observation scope;
- absence of perturbation;
- absence when observation fails.

### 6.4 Evidence

Evidence is not an intrinsic substance inside a datum.

Provisional form:

```text
Evidence(Datum, Claim, Method/Background, Scope)
```

The same datum can support one claim, be irrelevant to another, or undermine a third.

Therefore:

```text
Data != Evidence
Evidence != Truth
NoEvidence != Falsehood
```

This matches existing Runtime/World/Human/Finance anti-collapse laws.

## 7. Representation

A representation is a structure/token/state that stands for, tracks, depicts, encodes or otherwise maps to some target under an interpretation/mapping relation.

WDF0-D refuses to make `representation` a universal natural kind. A map, measurement record, memory, equation, database row, legal document and neural code can all be representational in materially different ways.

Minimum grammar:

```text
Representation(R, Target, Mapping/Interpretation, Scope)
```

A representation may preserve selected structure while deleting other structure.

Thus:

```text
RepresentationFidelity_Q
```

is always relative to a question/property family Q.

A road map can be excellent for navigation and terrible for geology without being `false in general`.

## 8. Belief

Belief is an epistemic state of an Agent/system about claims/models, not a World fact merely because it is held.

```text
Belief_A(C, confidence/context)
```

A belief can concern:

- current state;
- hidden cause;
- causal law;
- identity;
- institution;
- future outcome;
- another Agent's belief.

POMDPs formalize one important special case by distinguishing hidden environment state, observations and a belief state used for action under partial observability.

The firewall is:

```text
BeliefState_A != EnvironmentReality
```

and even:

```text
PerfectBeliefWithinModel
!=
CorrectModelClass
```

An Agent can have a perfectly concentrated posterior inside the wrong ontology.

## 9. Model

NASA engineering vocabulary defines a model as a description or representation of a system, entity, phenomenon or process, and a simulation as an imitation of characteristics using a computational model. WDF0 retains this distinction while generalizing beyond software.

Provisional model grammar:

```text
Model M
= Representation
+ selected variables/categories
+ relations/structure
+ dynamics/rules where needed
+ boundary/scale assumptions
+ parameterization
+ scope/purpose
```

A model therefore is not merely stored knowledge; it is an organized representational structure that supports some combination of:

- description;
- compression;
- prediction;
- explanation;
- counterfactual reasoning;
- simulation;
- control/action selection.

### 9.1 Model validity is scoped

Use:

```text
Adequate(M, Target, Question, Regime, Tolerance)
```

not:

```text
ModelIsSimplyTrue
```

This does not deny truth. It prevents local adequacy from being silently promoted to complete ontology.

## 10. Simulation

Simulation is the **execution/evolution of a model**, not the target reality itself.

```text
SimulationRun(M, initial/input conditions)
  -> simulated trajectory/output
```

Therefore:

```text
SimulationState != TargetState
SimulationEvent != TargetEvent
```

unless the simulation itself is the target system under study.

This exception matters: a game simulation, economic simulation market or digital twin execution can itself become part of Reality and causally influence people/systems. In that case there are two roles:

```text
simulation-as-representation-of-X
simulation-as-real-computational-process-Y
```

They must remain separate.

## 11. Prediction

Prediction is a claim generated by a model/inference procedure about an unobserved, future, counterfactual or withheld target condition.

```text
Prediction(M, Conditions, Claim, Horizon)
```

It can be:

- accurate for wrong structural reasons;
- inaccurate despite locally correct structure because inputs/conditions were wrong;
- calibrated without being causally explanatory;
- useful for decision without being globally descriptive.

Hence:

```text
PredictiveSuccess != OntologicalTruth
PredictiveFailure != TotalModelFailure
```

The error location must be diagnosed.

## 12. Explanation

C exposed cause/constraint/constitution as separate. D adds that explanation is a relation between a question and an explanatory structure, not another object in Reality.

Possible explanatory modes include:

```text
causal/mechanistic
constitutive
constraint/modal
historical/genealogical
functional/organizational
statistical
geometric/structural
```

A valid answer to `why?` therefore depends on what contrast/question is being asked.

## 13. Dependence Signature — central WDF0-D result

The objective/subjective binary is too coarse.

For a claim C, define a provisional **Dependence Signature**:

```text
Dep(C) ⊆ {
  Target,
  RelationPartner,
  Time,
  History,
  ReferenceFrame,
  Scale,
  BoundaryCriterion,
  System,
  Actor,
  Goal/Outcome,
  Institution/RuleSystem,
  Observer/Sensor,
  MeasurementProcedure,
  Model/Representation
}
```

This is a research grammar, not a production schema.

A claim is not made subjective merely because Dep(C) is non-empty. Almost all meaningful claims have dependencies.

### 13.1 Examples

```text
velocity(body)
Dep = {body, time, reference frame}
```

Frame-relative yet objectively testable when the frame is fixed.

```text
capability(actor, outcome)
Dep = {actor, outcome/goal class, environment conditions, time, authority/access}
```

Actor-relative without being imaginary.

```text
legalPerson(company)
Dep = {organization, jurisdiction/rule system, time}
```

Institution-relative without being observer-opinion-relative.

```text
observedOnline(server)
Dep = {server, observer/path, procedure, time}
```

Observation-relative and path-relative.

```text
temperature(system)
Dep = {system boundary, equilibrium/coarse-graining assumptions, time, scale, measurement definition}
```

Macro/model-conditioned while tracking physical reality.

## 14. Relativity is not subjectivity

This becomes a durable anti-collapse:

```text
RelativeTo(K) != SubjectiveOpinion
```

Examples:

- position/velocity can be reference-frame relative;
- pressure/temperature can be system/scale/model-definition dependent;
- ecological state can be scale/boundary dependent;
- capability can be actor/environment relative;
- authority can be institution/domain relative;
- evidence can be claim/method relative.

These statements can still be wrong or right given their dependency coordinates.

## 15. Objectivity is not context-freedom

A stronger candidate notion emerges:

```text
Objectivity(C | Dep(C))
= C is constrained by Reality and invariant/reproducible
  under changes that should be irrelevant once its legitimate dependencies are fixed.
```

This is deliberately provisional.

Examples:

- different calibrated instruments should converge within uncertainty for the same specified measurand/conditions;
- observers using the same legal record/rules should agree about incorporation status, barring interpretive dispute;
- route reachability may disagree across network paths because path is a legitimate dependency rather than evidence of subjectivity.

Thus:

```text
Objective != ContextFree
ContextSpecified != Arbitrary
```

This may become a major World principle if it survives WDF0-E/F.

## 16. Observer dependence has multiple meanings

WDF0-D separates at least four:

### 16.1 Epistemic observer dependence

What is observed/known depends on observer, sensor and path.

### 16.2 Frame dependence

Some numerical descriptions depend on coordinate/reference frame without depending on anyone's beliefs.

### 16.3 Intervention dependence

Measurement/observation procedure can causally perturb the target.

### 16.4 Constitutive social dependence

Some facts depend on rule-governed collective/institutional activity.

These must not collapse into `observer-created reality`.

## 17. Observer-free falsifier

Consider a star evolving before any observer exists.

The following can remain meaningful without an observer:

- physical occurrence/change;
- spatial relations;
- physical quantities/flows;
- causal/mechanistic structure;
- constraints/laws;
- historical trajectory.

The following do not exist in the same role without an observer/modeling system:

- observation;
- evidence-for-a-claim;
- belief;
- model;
- prediction.

Therefore:

```text
EpistemicLayer != ConstituentRequiredForAllReality
```

Agent-centric ontology is rejected again.

But this does not imply every Reality property is intrinsic/context-free. Reference frames, scales and relational structures can remain relevant without sentient observers.

## 18. C-coordinate provenance audit

### 18.1 Standing / persistence

**Mixed relational Reality claim.**

Real continuities/transformations exist, but `same under K` requires a persistence criterion/sortal/claim purpose.

```text
Reality supplies continuity/history;
claim supplies K.
```

### 18.2 Occurrence / change / history

**Primarily Reality-facing**, but event segmentation can be projection-relative.

A process can occur without observers; deciding where one event ends and another begins can depend on scale/criterion.

### 18.3 Relation / structure / organization

**Reality-facing but typed.**

Some relations are physical, causal or constitutive; some structures are analyst-selected. `Structure` alone does not tell us which.

### 18.4 Boundary / scale / environment

**Strongly relational/decomposition-relative.**

Some boundaries are physically realized, but the statement `this is the relevant system boundary` requires criterion/scale/question.

### 18.5 Spatial / physical realization

**Reality-facing with representation layers.**

Spatial/physical relationships can be real while coordinates are frame/model-dependent.

### 18.6 Dynamic state projection

**Mostly model/decomposition-relative.**

Target reality has conditions/configurations, but `state vector S` and sufficient variables are selected under a model and purpose.

### 18.7 Modal structure

**Mixed.**

Physical possibility may depend on physical laws/conditions; reachability depends on dynamics/start; feasibility depends on resources; accessibility on coupling; authorization on institutions.

### 18.8 Causal/mechanistic structure

**Candidate Reality-facing relation with model-selected variables/scales.**

Causal dependencies need not be created by models, but causal variables/interventions are representations at a chosen level.

### 18.9 Constitutive / semantic / deontic structure

**Relational/institution-dependent Reality.**

A status can be objectively true relative to a real rule-governed institution while not existing independently of that institution.

### 18.10 Epistemic / representational position

**Observer/model-relative by definition.**

Observation, evidence, belief and models are real processes/objects in one sense but their epistemic role is relational to targets/claims/agents.

## 19. Model multiplicity — same evidence, different models

Structural-identifiability research provides a precise technical falsifier against `data uniquely determines model`.

Distinct parameter values or model structures can produce the same observable input-output behavior. Even with ideal noise-free observations, some parameters can remain structurally unidentifiable.

World implication:

```text
SameObservations
can be compatible with
DifferentLatentModels
```

Therefore:

```text
FitToObservedData != UniqueWorldModel
```

This is not merely a practical-noise problem.

## 20. Model equivalence is question-relative

Two models may be equivalent for one query and divergent for another.

Examples:

- Newtonian and relativistic approximations can agree within one low-speed tolerance but diverge elsewhere;
- two financial models can price a local instrument similarly while disagreeing about tail states;
- two network models can predict reachability while disagreeing about shared failure domains;
- two causal models can predict observational distributions similarly while disagreeing under intervention.

Provisional notation:

```text
Equivalent_Q,R(M1, M2)
```

where Q is question class and R is regime/tolerance.

Hence:

```text
ModelEquivalence != ModelIdentity
LocalEquivalence != GlobalEquivalence
```

## 21. Useful but structurally wrong models

A model can be useful when it compresses the right regularity inside a bounded regime even if its deeper ontology is wrong or incomplete.

This yields another firewall:

```text
OperationalAdequacy != OntologicalAdequacy
```

Possible dimensions of model adequacy:

```text
DescriptiveFit
PredictiveCalibration
Causal/InterventionalValidity
Structural/MechanisticValidity
TransferValidity
DecisionUtility
ComputationalCost
```

No one dimension automatically implies the others.

This matters for Agent world models: a cheap heuristic model can be rational for a decision while remaining explicitly provisional.

## 22. WorldModel — Agent-facing reconstruction

WDF0-D now rejects the image:

```text
WorldModel = one complete internal copy of World state
```

A more robust provisional form is:

```text
WorldModel_A
= a set of scoped representations/models
  + beliefs/uncertainties
  + dependency assumptions
  + evidence links
  + model-selection/use conditions
  + revision conditions
```

Different submodels can cover:

- physical dynamics;
- network reachability;
- Human behavior;
- legal authority;
- finance;
- tool capability;
- causal mechanisms.

They need not share one universal state vector.

## 23. Actionable partial world model

For an Agent decision Q, the necessary model may be only a bounded projection:

```text
ActionableWorldModel(A,Q)
≈ target/boundary scope
 + relevant current-state belief
 + relevant dynamics/mechanisms
 + available actions/affordances
 + constraints/resources/authority
 + outcome model
 + uncertainty/evidence
 + currentness horizon
 + model-revision triggers
```

The word `partial` is not a defect. It is often the only computationally and epistemically defensible form.

The crucial rule is:

```text
PartialModel must know/represent its own scope and reopen conditions.
```

Otherwise partiality becomes hidden false completeness.

## 24. Within-model update vs model revision

C introduced this split; D sharpens it.

### Within-model update

```text
same variables/categories/relations
new evidence
→ update state / parameters / probabilities
```

### Structural model revision

```text
prediction/evidence failure
→ question boundary/scale/category/relation/mechanism
→ add, split, merge, remove or replace model structure
```

Recent Agent work such as WorldEvolver independently explores test-time revision from prediction–observation mismatch, although its particular mechanism revises memory/context rather than establishing a universal ontology-revision solution.

WDF0 retains the broader requirement:

```text
GeneralWorldLearning
requires the possibility of structural revision.
```

## 25. Surprise taxonomy for model revision

Not every prediction failure should reopen ontology.

WDF0-D proposes a diagnostic ladder:

```text
L0 observation fault
  sensor/path/calibration/provenance problem

L1 state error
  model family is adequate; current hidden state was wrong

L2 parameter error
  variables/relations are adequate; parameterization wrong

L3 dynamics/mechanism error
  transition/causal law wrong

L4 boundary/scale error
  target decomposition wrong

L5 missing variable/relation/action
  model structure incomplete

L6 category/ontology error
  current conceptual kinds collapse distinct realities or omit a required family
```

This hierarchy is provisional but gives Ordivon a disciplined way to avoid both extremes:

- never revising foundational concepts;
- reopening ontology after every noisy mismatch.

## 26. Reality gap, observation gap and model gap

Agent failure can now be decomposed:

```text
RealityGap:
  Reality contains relevant structure/effect not present in model.

ObservationGap:
  relevant Reality exists but current sensor/path did not expose it.

InterpretationGap:
  signal/data exists but mapping/meaning is wrong.

ModelGap:
  observation is available but model cannot represent/explain it correctly.

ActionGap:
  model is adequate but Agent lacks option/capability/authority.
```

These gaps are orthogonal enough to matter. Solving one does not imply solving another.

## 27. Environment and affordance/capability

An affordance/capability cannot be located cleanly `inside the environment` or `inside the Agent`.

Provisional relational form:

```text
Affordance/Capability(A, Environment, OutcomeClass, Conditions, Time)
```

The environment contributes structure/resources; the Actor contributes body/skill/control; institutions may contribute permission/authority.

Thus:

```text
EnvironmentProperty alone != Affordance
ActorProperty alone != Capability
```

This is one of the clearest cases where a World concept belongs primarily to the relation between Reality and Agent.

## 28. Institutional objectivity

Institutional facts provide a decisive test against `objective = independent of all social construction`.

Suppose a company is legally incorporated under a valid jurisdiction.

Its status depends on:

- rule system;
- authorized acts/records;
- organizational facts;
- time/jurisdiction.

But it is not made false by a particular observer's ignorance.

Therefore WDF0 distinguishes:

```text
Agent-independent-given-institution
from
Institution-independent.
```

Institutional facts can be **relationally objective** while socially constituted.

This keeps Finance/Human institutional reality inside World without pretending it is either physical substance or subjective metadata.

## 29. Measurement objectivity as a prototype

Metrology offers a useful prototype for WDF0's `objective with dependencies` idea.

A measurement claim can explicitly bind:

```text
measurand definition
procedure
instrument/calibration
conditions
uncertainty
traceability
```

The result becomes more objective not by deleting these dependencies, but by specifying, controlling and exposing them.

This suggests a general World principle:

```text
Objectivity often increases through explicit dependency disclosure,
not through pretending dependencies do not exist.
```

## 30. WDF0-D revised layered architecture

The current best research architecture is no longer one flat ontology:

```text
REALITY
│
├─ physical / causal / constitutive / historical structures
│
├─ selected Target / System_K
│      └─ Environment_K / Boundary / Scale / Frame
│
├─ Measurement / Interaction
│      └─ Signal / Indication / Data
│
├─ Observation / Evidence
│
├─ Representation / Belief / Model
│      └─ Simulation / Prediction / Explanation
│
└─ Agent coupling
       └─ Affordance / Resource / Capability / Authority / Action
```

The layers are not ontologically isolated. Measurement and models are themselves physical/social Reality processes. The diagram separates **roles**, not universes.

A camera is physically real while its image is also a representation. A legal registry is physically/digitally real while its entries can also constitute institutional status. One thing can occupy multiple truth roles without role collapse.

## 31. Role multiplicity

This produces another important principle:

```text
SameToken can occupy multiple roles simultaneously.
```

Example: a signed contract PDF can be:

- a physical/digital byte object;
- a record;
- a representation of terms;
- evidence of agreement;
- a constitutive legal instrument under some system;
- an input to an Agent model.

These are not six duplicate objects. They are six relations/truth roles involving one token.

This may become a major compression device for World Foundations.

## 32. C grammar after D provenance audit

| C coordinate | WDF0-D provenance |
|---|---|
| standing/persistence | mixed Reality + typed criterion relation |
| occurrence/change/history | primarily Reality-facing; segmentation can be model-relative |
| relation/structure/organization | Reality-facing when instantiated; type/scale selection can be model-relative |
| boundary/scale/environment | relational/decomposition-relative; sometimes physically/institutionally realized |
| spatial/physical realization | Reality-facing; coordinate descriptions frame-relative |
| state/dynamic projection | mainly model-relative representation of target configuration/dynamics |
| modal structure | typed relational mixture: physical/dynamic/resource/actor/institution |
| causal/mechanistic | candidate Reality relation expressed through model-selected variables/scales |
| constitutive/semantic/deontic | institution/rule/context-relative but can be objectively true |
| epistemic/representational | observer/model-relative truth role |

This table is one of WDF0-D's main deliverables.

## 33. What D now falsifies

### D-F1 — Reality = Environment

Rejected. Environment is system/criterion/coupling relative.

### D-F2 — Observable = Real

Rejected. Reality can exceed current observability.

### D-F3 — Observation = passive copy

Rejected. Measurement can perturb targets and always occurs through path/procedure/conditions.

### D-F4 — Data = Evidence

Rejected. Evidence is a support relation to claims under methods/background.

### D-F5 — Evidence = Truth

Rejected.

### D-F6 — State vector = target Reality

Rejected as a universal identification.

### D-F7 — Model = simulation

Rejected. A simulation executes/evolves a model.

### D-F8 — Prediction = model

Rejected. Prediction is one model-generated claim/output role.

### D-F9 — Relative = subjective

Rejected.

### D-F10 — Objective = context-free

Rejected.

### D-F11 — Same observations uniquely determine latent model

Rejected by structural non-identifiability/model multiplicity.

### D-F12 — WorldModel = monolithic internal copy of World

Rejected.

### D-F13 — fixed-schema Bayesian/state update = general world learning

Rejected.

### D-F14 — useful model = ontologically correct model

Rejected.

## 34. WDF0-D anti-laws

1. `Reality != Environment_S`.
2. `Environment_S != Observable_S`.
3. `Observable_S != Observed_S`.
4. `Target != MeasurandSpecification`.
5. `Measurand != Indication`.
6. `Indication != MeasurementResult`.
7. `Observation != PassiveCopy`.
8. `Data != Evidence`.
9. `Evidence != Truth`.
10. `NoEvidence != Falsehood`.
11. `Representation != Target`.
12. `Belief != Reality`.
13. `Model != Reality`.
14. `Model != Simulation`.
15. `SimulationRun != TargetTrajectory`.
16. `Prediction != Model`.
17. `PredictiveSuccess != OntologicalTruth`.
18. `PredictiveFailure != TotalModelFailure`.
19. `Relative != Subjective`.
20. `Objective != ContextFree`.
21. `DependencySpecified != Arbitrary`.
22. `StateVector != Reality`.
23. `SameObservations != UniqueLatentModel`.
24. `LocalModelEquivalence != GlobalModelEquivalence`.
25. `OperationalAdequacy != OntologicalAdequacy`.
26. `WorldModel != World`.
27. `PartialWorldModel != DefectiveWorldModel` by default.
28. `WithinModelUpdate != StructuralModelRevision`.
29. `Affordance != EnvironmentPropertyAlone`.
30. `Capability != ActorPropertyAlone`.
31. `InstitutionRelative != ObserverOpinionRelative`.
32. `SameTokenRoleA != SameTokenRoleB` while one token may instantiate both roles.

## 35. External pressure retained in D

Primary/authoritative sources used:

- JCGM/BIPM, *International Vocabulary of Metrology (VIM), JCGM 200:2012*: measurement, measurand, measurement result, indication and measurement model; especially explicit procedure/conditions, uncertainty and measurement perturbation.
- Kaelbling, Littman & Cassandra, *Planning and Acting in Partially Observable Stochastic Domains*: hidden environment state / observations / belief-state action under partial observability.
- Kirchhoff, Parr, Palacios, Friston & Kiverstein, *The Markov blankets of life* (2018): statistical system/environment boundaries, nested scales, non-coextensiveness with biophysical boundary.
- NASA-STD-7009 / NASA software-engineering vocabulary: model as description/representation; simulation as computational imitation using a model; scoped credibility/validation practice.
- structural-identifiability literature: observational behavior can fail to uniquely determine latent parameter/model structure even with idealized data.
- 2026 self-evolving world-model Agent work: prediction-observation mismatch is increasingly used to revise deployment-time model context/memory, illustrating current pressure toward revisable rather than static world models.

## 36. Exact residual entering WDF0-E

D cleans the Reality/model boundary but creates the next unavoidable problem:

> If system, boundary, state, persistence, causal variables and even valid explanations can depend on scale/decomposition, what makes one level or composition real/useful rather than arbitrary?

C already showed:

- vortex/phase exist at selected scales;
- cell/organism boundaries are organized and nested;
- ecosystems can have macro regimes/hysteresis;
- corporations/markets/institutions survive component replacement;
- distributed services have logical identity above processes/machines;
- coarse-graining can alter explanatory/causal usefulness.

D now shows these are not merely observer subjectivity; they are dependence-signature questions.

Therefore the next exact sub-round is:

# WDF0-E — Scale / Composition / Part–Whole / Organization / Emergence / Coarse-Graining

It must ask:

```text
What is a part?
What composes a whole?
When does aggregation become organization?
What makes a macro variable valid?
When is emergence merely epistemic compression?
When is it explanatory / causal / constitutive?
How can multiple scales be jointly true without double-counting causes/entities?
```

## 37. WDF0-D closeout

WDF0-D closes with the following durable research state:

```text
1. Reality is not exhausted by any observer/model, but Reality may include relational and institution-dependent facts.
2. `World` remains overloaded and is not admitted as a universal ontology object.
3. Environment is a typed system-relative coupling projection, not total Reality.
4. Measurement is a procedure-bound interaction that can perturb its target; indication/result/reality must be separated.
5. Data, observation, evidence, representation, belief, model, simulation and prediction are distinct truth roles.
6. Relative does not mean subjective; objective does not mean context-free.
7. Dependence Signature is introduced as the candidate grammar for declaring frame/scale/boundary/actor/institution/observer/model dependencies.
8. C's ten coordinates have mixed provenance; only some are straightforward Reality-facing claims.
9. Same evidence can support multiple latent models; model adequacy is multidimensional and scoped.
10. Agent world models are best treated as revisable portfolios of scoped partial models, beliefs, evidence and reopen conditions rather than one monolithic global state copy.
11. General world learning requires both within-model update and structural model revision.
```

No production refactor follows automatically. WDF0-E is admitted; WDF1 remains UNKNOWN.
