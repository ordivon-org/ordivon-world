# WDF0-E — Scale / Composition / Part–Whole / Organization / Emergence / Coarse-Graining

Status: complete for WDF0-E. No positive World ontology is frozen. WDF0-F final reconstruction is the next admitted sub-round. WDF1 remains UNKNOWN.

## 0. Question

WDF0-D showed that scale, boundary, state, system and model claims have explicit dependence signatures rather than belonging cleanly to a simple objective/subjective split. WDF0-E now asks:

> When does a collection of lower-level things count as a whole, what kinds of part–whole relations exist, when is a macro description genuinely explanatory rather than arbitrary compression, and what—if anything—does `emergence` add?

The round treats `part`, `component`, `member`, `constituent`, `participant`, `substrate`, `dependency`, `level`, `macro`, `micro`, `organization` and `emergence` as suspicious overloaded terms until separated.

## 1. First firewall — there is no single `part-of`

WDF0-E rejects an untyped universal `partOf(x,y)` as too weak for World Foundations.

At minimum, the following relations differ:

### 1.1 Mereological part

```text
Part_K(x, whole)
```

A broad whole–part claim under a composition criterion K.

This only says that x is counted within the whole under K. It does not yet say x has a function, is indispensable, physically contained, causally active or permanently attached.

### 1.2 Constituent

A constituent helps make up the material/structural composition of a target at a specified time or regime.

Examples:

- molecule in a fluid sample;
- cell in a tissue;
- file/object in a repository snapshot.

Constituency can change while higher-level identity persists.

### 1.3 Component

A component is a part whose organization/activity is relevant to some mechanism, function or system behavior.

Mechanistic explanation explicitly requires component parts/activities plus their spatial-temporal organization; a mere bag of parts is not yet a mechanism.

Thus:

```text
Component != ArbitraryPart
```

### 1.4 Member

Membership is a group/social/institutional relation.

Examples:

- employee in company;
- citizen in polity;
- node enrolled in a cluster membership set.

A member need not be a spatial or material part of the whole in the same sense as a heart is part of an organism.

### 1.5 Participant

A participant takes part in a process/interaction without being a constituent part of that process in the same sense as a component is part of a mechanism.

Examples:

- trader participates in a market;
- enzyme participates in a reaction cycle;
- Agent participates in a workflow.

### 1.6 Substrate / realizer

A substrate physically/computationally realizes or supports a pattern, process, representation or function.

Examples:

- neurons realize a memory representation;
- hardware realizes a VM/service;
- paper/digital storage realizes a legal record.

The higher-level role can sometimes survive substrate replacement.

### 1.7 Dependency

A dependency is something whose availability/state constrains the target but need not be a part/member/constituent.

Examples:

- DNS dependency of a service;
- oxygen dependency of combustion;
- supplier dependency of a firm;
- law/jurisdiction dependency of a legal status.

Hence:

```text
DependsOn != PartOf
```

## 2. Typed composition replaces universal wholehood

A `whole` is not admitted as an observer-free universal primitive.

Provisional grammar:

```text
Whole_K(P, R, H, Boundary, Scale, Time)
```

where:

- P = candidate parts/participants/members/constituents;
- R = relations/organization among them;
- H = relevant history/lineage/formation conditions;
- K = wholehood criterion;
- Boundary/Scale/Time are explicit dependencies.

Different K produce different legitimate wholes.

Examples:

```text
Whole_material
Whole_mechanistic
Whole_organismic
Whole_task
Whole_legal
Whole_economic
Whole_computational
```

The aim is not to create these as production classes. They show that `whole` is a typed claim.

## 3. Aggregation != Composition != Organization

### 3.1 Aggregation

An aggregation is a collection/grouping under some selection rule.

```text
Aggregate = members selected/grouped together
```

No strong internal organization is implied.

Ten rocks in a box can form an aggregate.

### 3.2 Composition

Composition asserts that selected parts jointly constitute a whole under K.

```text
Compose_K(parts, relations, context) -> whole-status claim
```

Composition is stronger than aggregation because the part–whole relation matters.

### 3.3 Organization

Organization requires structured relations, differentiation, coordination, constraint or dependency among parts such that rearranging relations while preserving the same parts changes the relevant whole behavior/status.

A useful deletion test:

```text
same parts
+ different organization
=> different system behavior/status
```

If true, organization carries explanatory information not contained in the unordered multiset of parts.

### 3.4 Network

A network is a relational topology among nodes/entities/events.

It need not constitute one bounded whole.

A trade network, road network or dependency graph can span many systems/organizations.

Thus:

```text
Network != Organization != Whole
```

### 3.5 Closure

Closure is a stronger organization property under a specified relation.

Biological closure-of-constraints work provides one concrete form: constraints mutually depend on and contribute to maintaining each other while channeling open thermodynamic processes at relevant timescales.

Closure does not mean isolation from environment.

```text
Closure != ClosedSystem
```

A biologically organized whole can be materially/energetically open.

## 4. Organization can create a new valid unit without creating new fundamental substance

Major evolutionary transitions provide a strong real-world falsifier.

Evolutionary research describes transitions where lower-level entities that were previously capable of independent replication become integrated into a higher-level individual; recurrent markers include cooperation, division of labor, communication, mutual dependence and reduced within-group conflict.

This shows:

```text
CollectionOfCells
!=
MulticellularIndividual
```

The transformation is not merely adding more cells. It changes relations among lower-level units, dependence, reproduction and the level at which fitness/selection can be coherently assigned.

Therefore:

```text
NewWholeStatus can emerge through reorganization of old components.
```

But:

```text
NewWholeStatus != NewFundamentalSubstance
```

No ontological magic is required.

## 5. Component replacement and multiple realization

Cross-domain cases repeatedly show that wholes can persist across component replacement:

- cells/material in organisms;
- employees/directors in organizations;
- machines/processes in distributed services;
- neurons participating in memory engrams;
- hardware underlying migrated VMs/Agents.

This yields:

```text
WholeIdentity_K != ExactComponentSetEquality
```

and:

```text
Role/Function/Organization can be multiply realized.
```

However, multiple realization does **not** imply substrate irrelevance.

Different realizers can differ in:

- energy/resource cost;
- latency;
- reliability;
- capacity;
- failure mode;
- jurisdiction;
- security properties;
- embodied affordances.

Thus:

```text
SameMacroRole != SameRealizationProperties
```

## 6. `Level` is not one axis

WDF0-E falsifies the idea of one universal hierarchy:

```text
micro < meso < macro
```

as if every claim could be placed on one ladder.

At least these axes differ:

### 6.1 Spatial scale

nanometer, cell, organism, city, planet.

### 6.2 Temporal scale

microseconds, seconds, development, generations, institutional centuries.

### 6.3 Mereological depth

part → whole → super-whole under one composition relation.

### 6.4 Mechanistic level

component activity → mechanism behavior → contextual function.

Mechanistic levels are defined by constitutive organization, not simply size.

### 6.5 Organizational / institutional hierarchy

employee → team → division → corporation, or court → appellate system, etc.

This is a role/authority relation, not necessarily physical composition.

### 6.6 Network scale / community resolution

local node neighborhood → module/community → network-level structure.

### 6.7 Representational resolution / coarse-graining

fine-grained model → macro variable / reduced model.

### 6.8 Causal abstraction level

different variable sets used to state stable intervention relations.

Therefore:

```text
HigherLevel_A != HigherLevel_B
```

unless the level axis is specified.

`Level` becomes another Dependence-Signature coordinate, not a universal noun.

## 7. Coarse-graining — model operation, Reality test

A generic coarse-graining can be written:

```text
G : micro/configuration space -> macro/equivalence classes
```

Many detailed configurations are mapped to the same macro state.

The crucial WDF0-E distinction is:

```text
The mapping G is selected/constructed by a modeler or modeling procedure.
Reality does not automatically supply one unique coarse-graining.
```

But this does **not** imply the macro pattern is arbitrary.

Reality determines whether the proposed macro classes exhibit:

- stable persistence;
- predictive sufficiency;
- causal/interventional regularity;
- control relevance;
- robustness across micro variation;
- transfer across contexts;
- valid constitutive/institutional status;
- reliable measurement.

Hence:

```text
MacroVariableProposal = model-relative
MacroVariableValidity = Reality-constrained given its Dependence Signature
```

This is one of WDF0-E's main results.

## 8. Objective macro variables as robust equivalence classes

D proposed objectivity as invariance/reproducibility under irrelevant transformations after legitimate dependencies are fixed.

E extends that idea:

```text
MacroVariable_K
= equivalence class over micro/configuration states
  where K declares which differences are irrelevant for question Q.
```

A macro variable earns stronger objective standing when members of the same class remain equivalent under relevant prediction/intervention/control tests.

For example:

- thermodynamic variables ignore molecular identities while preserving selected bulk predictions;
- phase labels ignore many micro configurations while tracking robust collective order;
- service identity ignores machine/process replacement while preserving an interface/continuity criterion;
- legal company identity ignores member turnover while preserving institutional criteria.

The equivalence relation is question/criterion dependent; its empirical/operational robustness is not simply invented.

## 9. Coarse-graining can improve explanatory power

Hoel, Albantakis and Tononi showed in model systems that a coarse-grained macro description can have higher effective information than the fixed micro description under their causal-effectiveness measure. Their result is not proof that all macro levels have independent metaphysical causation; it is proof against the default claim that maximal micro detail always yields the best causal representation.

More recent work continues to study causal emergence and explicitly notes that results can depend strongly on the coarse-graining method.

WDF0-E therefore retains only the cautious conclusion:

```text
MoreMicroDetail != MoreCausal/DecisionInformation by default.
```

and:

```text
MacroCausalAdvantage is measure-, variable- and coarse-graining-dependent.
```

## 10. Information loss is not automatically explanatory loss

Coarse-graining deliberately removes distinctions.

A good coarse-graining removes distinctions irrelevant to Q while preserving or improving relevant regularity.

Define provisionally:

```text
Loss_G = discarded micro distinctions
Value_G,Q = retained predictive/causal/control/constitutive relevance for Q
```

Then:

```text
Loss_G > 0
```

does not imply:

```text
ModelQuality_Q decreases.
```

Indeed, noisy/degenerate micro detail can hide stable macro structure.

The real danger is **wrong invariance**: collapsing microstates whose differences become relevant under transfer, intervention, failure or changed goals.

## 11. Emergence — reject the universal magic word

WDF0-E rejects `Emergence` as one undifferentiated primitive.

At least five distinct uses must separate.

### 11.1 Epistemic / descriptive emergence

A macro pattern is surprising, difficult to derive, or only apparent after coarse-graining.

This is primarily about the modeler/description.

```text
HardToDerive != NewOnticPower
```

### 11.2 Dynamical / pattern emergence

Collective interaction generates stable patterns/order/attractors not usefully attributable to isolated components alone.

Examples include vortices, waves, synchronization and phase order.

The macro pattern is physically realized but does not require new fundamental laws.

### 11.3 Organizational emergence

Previously independent/loosely coupled parts become organized into a unit with division of labor, mutual dependence, closure or coordinated function.

Major transitions in individuality are strong biological cases.

### 11.4 Causal emergence

A macro causal model outperforms a micro causal model under a specified measure/intervention/coarse-graining.

This is a **model-comparison claim**, not automatically an ontological declaration.

### 11.5 Constitutive / institutional emergence

Relations/rules among lower-level participants constitute a higher-level status/whole:

- legal corporation;
- contract;
- market organization;
- authority structure.

This is governed by constitutive/deontic relations, not new physical force.

### 11.6 Strong ontological emergence

The claim that genuinely novel fundamental causal powers/laws appear that are not in any suitable sense grounded in lower-level reality is **not admitted** by WDF0-E. None of the current Ordivon falsifiers require it.

Hence:

```text
Emergent_P must always specify P-type.
```

Bare `emergent` is rejected as explanatory completion.

## 12. Part–whole and cause–constitution must remain separate

Mechanistic work makes an important distinction: relationships among components can be causal, while the relationship between organized components and the mechanism-as-whole is often constitutive rather than another causal arrow between two independent things.

This matters for double-counting.

Suppose:

```text
heart activity + vascular organization constitute organism-level circulation
```

It is usually misleading to model:

```text
organism-circulation -> heart
```

as if the whole and its constituting parts were independent simultaneous causes.

WDF0-E retains:

```text
InterlevelConstitution != IntralevelCausation
```

This extends C's `Cause != Constitute` firewall into multiscale reasoning.

## 13. Downward causation is too ambiguous

`Downward causation` is often used for several different phenomena.

WDF0-E separates:

### 13.1 Mechanistically mediated contextual effect

A macro context changes boundary conditions, inputs or interactions of components through ordinary causal pathways.

Example:

- network congestion changes component packet behavior;
- organismal hormonal state changes cell activity;
- firm policy changes employee actions via communication/incentives.

No mysterious macro force is required.

### 13.2 Downward constraint

Whole-level organization restricts the accessible behavior of components because of structural/organizational relations.

Example:

- cell architecture constrains biochemical pathways;
- protocol/state machine constrains legal transitions of component roles;
- institutional rules constrain member action possibilities.

### 13.3 Selection / retention effect

Higher-level persistence/reproduction conditions favor some lower-level variants/behaviors over others across time.

Major evolutionary transitions provide biological examples of lower-level conflict being suppressed as a higher-level individual becomes integrated.

### 13.4 Constitutive determination

A whole-level status determines what lower-level role something counts as under the organization/rule system.

Example:

- the same person counts as director because of company governance status.

This is constitutive, not causal.

Therefore:

```text
DownwardCausation != OneRelation
```

WDF0 currently prefers explicit mechanisms/constraints/constitution over the bare phrase.

## 14. Craver–Bechtel pressure on top-down causes

Craver and Bechtel argue that many apparent top-down causal claims can be reconstructed as mechanistically mediated effects combining constitutive relations across levels with causal relations among components/contexts, avoiding mysterious direct interlevel causes.

WDF0 does not freeze their account as universal truth, but adopts the methodological discipline:

> Before positing a new top-down causal primitive, reconstruct the physical/organizational mediation and the constitutive relation first.

This is a strong anti-double-counting rule.

## 15. Multi-level causation without double-counting

A higher-level variable may still be a better causal/control variable for Q even if physically realized by lower-level processes.

To avoid double-counting:

```text
1. state the intervention target/level;
2. state the realization/constitution mapping;
3. state whether the macro and micro variables are alternative descriptions of overlapping events;
4. do not sum them as independent causes unless independent interventions justify that factorization.
```

Thus:

```text
MacroCausalUsefulness
!=
IndependentExtraForce
```

## 16. Nested wholes are real but not necessarily a tree

Reality contains nested organization:

```text
organelle -> cell -> tissue -> organism
process -> service -> application -> organization
person -> team -> firm -> market/institution
```

But this tempts a false universal tree.

A single entity can participate in overlapping wholes under different relations:

- a Human is part of an organismic whole, member of a company, citizen of a polity, participant in a market and component of a task system;
- one server can support several services;
- one legal entity can belong to multiple contractual networks;
- one gene product can participate in multiple mechanisms.

Therefore:

```text
CompositionStructure != UniversalTree
```

A better research representation is a typed multiplex/hypergraph of part/member/participant/dependency/realization relations.

## 17. Overlap does not imply contradiction

Two wholes can share components if their wholehood criteria differ or if the relevant composition relation permits overlap.

The question is not:

> Which is the one true whole?

but:

```text
Whole_K1(...)
Whole_K2(...)
```

with dependency signatures.

Contradiction occurs only when two claims assert mutually exclusive relations under the same K/scope/time.

## 18. Hierarchy != nesting != authority

Another overloaded term is `hierarchy`.

Separate:

```text
mereological hierarchy
organizational reporting hierarchy
control hierarchy
causal abstraction hierarchy
classification hierarchy
scale hierarchy
authority hierarchy
```

A manager can be `above` an employee in authority while both are material peers as humans. A service may be above a process in logical abstraction but realized by many processes. A macro variable may be coarser without having authority over micro variables.

Therefore:

```text
Above/Below requires typed relation.
```

## 19. Organization has at least five dimensions

`Organization` is still too broad. E finds at least:

### 19.1 Structural organization

who/what is connected to whom, topology/geometry.

### 19.2 Functional organization

differentiated roles coordinated toward/within a system activity.

### 19.3 Dynamical organization

feedback, synchronization, attractors, recurrent interaction patterns.

### 19.4 Constraint organization

mutually maintained constraints restricting component/process possibility spaces.

### 19.5 Institutional organization

roles, rules, rights, authority, membership and constitutive status.

These can coexist but must not collapse.

## 20. A whole can be real in more than one sense

WDF0-E therefore rejects the question:

> Is the corporation / organism / market / service a real entity: yes or no?

A better audit is:

```text
What Whole_K claims are true?
What persistence criterion applies?
What organization supports them?
What scale/boundary is used?
What causal/constitutive relations are valid?
What realization substrate matters?
```

For a corporation:

- legal whole: strong;
- organizational whole: often strong;
- material whole: weak/non-contiguous;
- organismic whole: false;
- task-system whole: context-dependent.

This is not relativism. It is typed wholehood.

## 21. Scale validity criteria

A scale/grain is not justified because it is convenient alone.

WDF0-E proposes a **Scale Validity Ledger**. A candidate macro level may earn standing through one or more of:

```text
Predictive sufficiency
Interventional stability
Control relevance
Robust invariance under micro variation
Mechanistic/constitutive relevance
Historical/persistence continuity
Institutional validity
Measurement reproducibility
Transfer/generalization
Compression efficiency under bounded loss
```

No single criterion is universal.

A scale can be useful for control but poor for mechanistic explanation; another can be institutionally authoritative but physically coarse.

## 22. Scale optimality is query-relative

There is no universal best scale.

```text
BestScale(Q, Action, Horizon, Tolerance, Cost)
```

may differ for:

- explanation;
- prediction;
- intervention;
- diagnosis;
- control;
- accounting;
- legal adjudication;
- Agent planning.

This directly connects to ActionableWorldModel from D.

## 23. Coarse-graining and action

An Agent should prefer the cheapest model grain that preserves decision-relevant differences.

Provisional rule:

```text
Choose G such that:
  distinctions discarded by G
  do not change the preferred action/outcome estimate
  beyond tolerance within the claimed regime.
```

But the model must retain a reopen condition for when discarded variables become relevant.

Thus:

```text
CoarseModel
+ ReopenCondition
```

can be superior to maximal-detail modeling.

## 24. Emergence and surprise are different

A phenomenon can be surprising because the modeler omitted a known mechanism; this is not ontological emergence.

Similarly, a macro regularity may be easy to derive but still constitute a valid higher-level organization.

Therefore:

```text
Surprise != Emergence
DifficultyOfPrediction != EmergentOntology
```

This prevents `emergence` from becoming a synonym for ignorance.

## 25. Emergence and novelty are different

Novelty can refer to:

- first historical occurrence;
- new pattern;
- new capability;
- new role/status;
- new variable useful to a model;
- new causal regime;
- new fundamental law.

These are radically different.

Thus:

```text
Novel != Emergent by default.
```

## 26. Emergence and irreducibility are different

A macro property can be:

- derivable in principle but computationally hard;
- multiply realizable;
- robust under micro variation;
- causally useful at a macro scale;
- constitutionally dependent on micro organization.

None automatically entails metaphysical irreducibility.

Therefore:

```text
MacroValidity != FundamentalIrreducibility
```

## 27. Cross-domain wholehood falsifiers

### 27.1 Pile of stones

Strong aggregate, weak organization.

Shows:

```text
Collection != OrganizedWhole
```

### 27.2 Clock/mechanism

Components + spatial/temporal organization are required for mechanism behavior.

Shows:

```text
SameComponentsDifferentOrganization -> DifferentMechanism
```

### 27.3 Cell

Open thermodynamic processes + maintained constraints/boundary/organization.

Shows:

```text
Whole can be materially open yet organizationally integrated.
```

### 27.4 Multicellular organism

Evolutionarily integrated cells with division of labor and reduced independent fitness.

Shows:

```text
CooperativeGroup != NewIndividual
```

until integration criteria change.

### 27.5 Corporation

Legal/institutional + organizational whole, despite spatial dispersion/member replacement.

Shows:

```text
Wholehood need not require spatial contiguity.
```

### 27.6 Market

Strong process/network/institution; weaker bounded-whole claim depending on venue/jurisdiction/question.

Shows:

```text
Network/Process != AutomaticallyOneWhole
```

### 27.7 Distributed service

Logical service identity can survive process/machine replacement; dependency graph may cross owner boundaries.

Shows:

```text
ServiceWhole != MachineAggregate
```

### 27.8 Agent task system

Human + model + tools + external bodies can form a temporary functional/task whole without merging organism/legal/ownership identity.

Shows:

```text
FunctionalWhole != IdentityFusion
```

## 28. New candidate — Integration Signature

Dependence Signature tells us what a claim depends on. E needs a complementary grammar for why selected parts warrant a whole claim.

Provisional **Integration Signature**:

```text
Int_K(W) = {
  Boundary/closure,
  Interaction density/structure,
  Coordination,
  Mutual dependence,
  Division of labor,
  Shared persistence/history,
  Joint control/feedback,
  Reproduction/selection,
  Constitutive rule/status,
  Functional/mechanistic contribution
}
```

This is deliberately a menu, not a universal checklist.

Different whole types use different subsets.

Examples:

- organism: boundary + mutual dependence + self-maintenance + reproduction/history;
- mechanism: functional contribution + organization + causal coordination;
- company: constitutive rule/status + membership/authority + organizational continuity;
- distributed service: interface/behavior continuity + dependency/coordination + operational boundary;
- task system: temporary coordination + shared outcome + control coupling.

`Int_K` may become a powerful way to prevent `system` and `whole` from becoming empty nouns.

## 29. New candidate — Realization Map

For macro role/property M, track:

```text
Realize(M, substrate/configuration, time, conditions)
```

This separates:

```text
MacroIdentity
from
CurrentRealizerIdentity
```

and permits multiple realization without declaring substrate irrelevant.

A valid realization claim should expose which substrate differences are ignored at the macro level and which reopen the model.

## 30. New candidate — Scale/Composition Signature

WDF0-E compresses many overloaded level claims into:

```text
ScaleCompositionSignature(C) = {
  Grain/Resolution,
  SpatialScale,
  TemporalScale,
  CompositionCriterion,
  WholeType,
  OrganizationType,
  BoundaryCriterion,
  RealizationMapping,
  CoarseGrainingMapping,
  Query/Use
}
```

Again this is research grammar, not production schema.

## 31. Major WDF0-E result — Reality can support multiple jointly valid levels without one universal hierarchy

The safest current formulation is:

```text
Reality supports structures/patterns/relations at multiple scales.
Models select decompositions and variables.
A level earns objective/scoped validity when its invariants and relations survive the relevant Reality tests.
```

Therefore:

```text
ManyLevelsCanBeTrue
```

without:

```text
AllLevelsAreEquallyGood
```

and without:

```text
OneLevelMustBeTheOnlyRealLevel
```

This is the multiscale counterpart of D's `Relative != Subjective`.

## 32. Major WDF0-E result — macro objectivity is constrained equivalence, not absolute level privilege

A macro class is initially proposed by grouping fine-grained configurations.

It becomes strongly justified when distinctions inside the class are irrelevant under a declared test family while distinctions across classes matter.

Provisional form:

```text
x ~_{K,Q} y
iff
x and y are interchangeable for Q under admissible tests K
within tolerance/regime.
```

Then macro states are equivalence classes under `~_{K,Q}`.

Reality constrains whether this equivalence is stable.

This gives a non-mystical account of why a macro state can be objective while remaining scale/question dependent.

## 33. Major WDF0-E result — composition itself is constitutive, not another causal process

When parts organized in R constitute whole W:

```text
parts + organization R
constitute W
```

This should not automatically be rewritten as:

```text
parts cause W
```

because W may be the same realized event/system described at a different constitutive level.

Causation can occur **within** and **around** the organized whole, while composition explains what the whole consists in.

This distinction is essential to avoid multiscale causal double-counting.

## 34. Major WDF0-E result — organization is transformation-sensitive relation structure

A strong candidate definition is:

```text
Organization_K(P,R)
```

where the whole's K-relevant behavior/status changes under some transformations of R even when the component multiset P is held fixed.

This means organization is not a mystical property added on top of parts; it is the explanatory relevance of how parts are related/coordinated/constrained.

It also allows organization to be physical, biological, computational or institutional depending on R and K.

## 35. What E now falsifies

### E-F1 — one universal part-of relation

Rejected.

### E-F2 — collection/aggregation is sufficient for wholehood

Rejected.

### E-F3 — every network is a system/whole

Rejected.

### E-F4 — wholehood requires spatial contiguity

Rejected by organizations, distributed services and institutions.

### E-F5 — whole identity requires fixed component membership

Rejected.

### E-F6 — all levels form one universal micro→macro ladder

Rejected.

### E-F7 — coarse-graining is merely subjective information loss

Rejected. Mapping is model-selected, but validity is Reality-constrained.

### E-F8 — more micro detail is always more explanatory/causal/useful

Rejected as a default.

### E-F9 — macro causal usefulness implies a new independent force

Rejected.

### E-F10 — downward causation names one primitive relation

Rejected.

### E-F11 — emergence is one universal phenomenon

Rejected.

### E-F12 — emergent = surprising/hard to derive

Rejected.

### E-F13 — macro validity entails metaphysical irreducibility

Rejected.

### E-F14 — multiple realization means substrate does not matter

Rejected.

### E-F15 — nested systems necessarily form a tree

Rejected.

### E-F16 — higher/lower without typed axis is meaningful enough for foundations

Rejected.

## 36. WDF0-E anti-laws

1. `Part != Component`.
2. `Part != Member`.
3. `Part != Participant`.
4. `Dependency != Part`.
5. `Substrate != Role/WholeIdentity`.
6. `Aggregate != Composition`.
7. `Composition != Organization`.
8. `Network != Whole`.
9. `Closure != ClosedSystem`.
10. `CollectionOfUnits != NewIndividual`.
11. `WholeIdentity != ExactComponentSetEquality`.
12. `SameMacroRole != SameRealizationProperties`.
13. `Level != OneUniversalAxis`.
14. `Macro != MerelyLarge`.
15. `Micro != FundamentallyPrivileged by default`.
16. `CoarseGrainingMap != RealityGivenUniquePartition`.
17. `ModelSelectedMacro != SubjectiveMacro`.
18. `MoreDetail != MoreExplanatoryPower`.
19. `InformationLoss != ExplanatoryLoss`.
20. `Emergence != Surprise`.
21. `Emergence != Novelty`.
22. `Emergence != OnePrimitive`.
23. `MacroValidity != FundamentalIrreducibility`.
24. `InterlevelConstitution != IntralevelCausation`.
25. `MacroCausalUsefulness != IndependentExtraForce`.
26. `DownwardCausation != OneRelation`.
27. `CompositionStructure != UniversalTree`.
28. `Hierarchy != Authority != Scale != MereologicalDepth`.
29. `FunctionalWhole != IdentityFusion`.
30. `MultipleRealization != SubstrateIrrelevance`.
31. `ManyValidLevels != AllLevelsEquallyValid`.
32. `ManyValidLevels != NoRealityConstraint`.

## 37. External pressure retained in E

Primary/near-primary sources used:

- Montévil & Mossio, *Biological organisation as closure of constraints* (Journal of Theoretical Biology, 2015): process/constraint distinction, mutual maintenance and organizational boundary.
- West, Fisher, Gardner & Kiers, *Major evolutionary transitions in individuality* (PNAS, 2015): transition from cooperative groups to integrated higher-level individuals via division of labor, mutual dependence, communication and reduced conflict.
- Michod, *Evolution of individuality during the transition from unicellular to multicellular life* (PNAS, 2007): reorganization of fitness and transformation of groups into higher-level evolutionary individuals.
- Hoel, Albantakis & Tononi, *Quantifying causal emergence shows that macro can beat micro* (PNAS, 2013): macro coarse-grained causal models can exceed micro models under effective information in selected architectures.
- Zhang et al., *Dynamical reversibility and a new theory of causal emergence based on SVD* (npj Complexity, 2025): explicitly highlights coarse-graining dependence as a central challenge for causal-emergence claims.
- Craver, *Constitutive Explanatory Relevance* (2007) and Craver & Bechtel, *Top-down Causation Without Top-down Causes* (2007): component/whole constitutive relevance and caution against mysterious interlevel causal duplication.
- recent network-flow coarse-graining work provides additional evidence that coarse-grained variables can be optimized to preserve task-relevant flow/dynamic structure across complex networks.

## 38. Exact residual entering WDF0-F

After A–E, the major open problem is no longer lack of concepts. It is compression and reconstruction.

WDF0 now has:

- anti-collapse laws;
- typed persistence/invariance;
- typed boundary/environment;
- dependence signatures;
- physical/spatial realization requirements;
- cause/constraint/constitution separation;
- observation/evidence/model separation;
- multiscale composition/organization grammar;
- emergence taxonomy;
- scoped partial world models and structural revision.

The danger is now the opposite: **foundation bloat**.

WDF0-F must answer:

```text
What is the smallest durable World grammar that can generate these distinctions?
Which concepts are root distinctions and which are derived?
What exact coverage remains missing?
Which anti-laws are strong enough to freeze?
What Deep Route should be admitted next from the largest irreducible residual?
```

Therefore the next exact round is:

# WDF0-F — Reconstruction / Compression / Coverage Ledger / Reopen Conditions

WDF0-F must not simply summarize A–E. It must attempt destructive compression, remove redundant concepts, expose contradictions and decide whether WDF0 can close.

## 39. WDF0-E closeout

WDF0-E closes with the following durable research state:

```text
1. Part–whole relations are typed; part/component/member/participant/substrate/dependency cannot collapse.
2. Aggregation, composition, organization, network and closure are distinct.
3. Wholehood is a typed claim supported by an Integration Signature, not a universal yes/no property.
4. Component replacement and multiple realization are compatible with macro identity, while substrate differences remain causally/actionably relevant.
5. `Level` is multidimensional; no single universal micro→macro hierarchy survives.
6. Coarse-graining is model-selected but its macro equivalence classes can be objectively Reality-constrained through robustness, prediction, intervention, control and constitutive tests.
7. More micro detail is not automatically more causal, explanatory or decision-relevant.
8. `Emergence` must split into descriptive, dynamical/pattern, organizational, causal and constitutive/institutional forms; strong ontological emergence is not currently required.
9. Interlevel constitution must not be double-counted as an extra causal force; downward causation should be decomposed into mediated causal effects, constraints, selection and constitution.
10. Reality can support multiple jointly valid levels without all levels being equally valid or one level being uniquely real.
11. Typed multiplex composition is a better candidate than a universal hierarchy tree.
12. WDF0 now has enough structure that the next problem is compression, not expansion.
```

No production refactor is justified by E. WDF0-F is admitted; WDF1 remains UNKNOWN.
