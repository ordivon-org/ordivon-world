---
schema_version: 1
id: world.resource-ontology-r5-composition-falsification
title: Resource Ontology R5 — Composition / Substitution / Bottleneck Falsification
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - researcher
  - agent
updated: 2026-08-15
summary: Falsifies additive bags, global dependency graphs and fixed typed bundle ontologies; reduces cross-resource composition to transition-specific requirements, current assignments and native constraints, with substitution, complementarity, modifiers, bottlenecks and redundancy derived from feasible assignment structure.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-ontology-r0-census
  - world.resource-ontology-r1-theory-triangulation
  - world.resource-ontology-r2-definition-falsification
  - world.resource-ontology-r3-relation-model
  - world.resource-ontology-r4-lifecycle-falsification
  - world.resource-option-capability-model
---
# Resource Ontology R5 — Composition / Substitution / Bottleneck Falsification

## 1. Question

R0–R4 progressively removed object-centric Resource semantics and a universal Resource lifecycle. R5 now asks the next foundational question:

> When one target transition depends on several Resources, what is the minimum structure needed to establish that those Resources can jointly support a Capability or Option?

The dangerous shortcut is familiar:

```text
Resources
  ↓
Dependency Graph
  ↓
Bundle
  ↓
Capability
```

That graph tends to accumulate apparently obvious edge types:

```text
requires
substitutes
complements
catalyzes
depends-on
redundant-with
bottleneck-for
```

R5 does not assume these are primitive relations.

The promotion criterion remains deletion-based:

> A composition concept is foundational only when deleting it changes transition feasibility, next admissible action, capacity/bottleneck prediction, redundancy/failure prediction, or recovery.

No R5 result is canonical production doctrine.

---

# 2. Frozen evidence boundary

R5 begins from canonical World main:

```text
300e3feef2be31ed3c8f72dfcb7383b1fd50979a
```

The cross-owner corpus was frozen before modeling. Every selected sibling worktree was clean, each HEAD matched the recorded revision, and every selected source file was byte-compared against `git show <revision>:<path>` before use.

Frozen repositories:

| Owner | Revision |
| --- | --- |
| world | `300e3feef2be31ed3c8f72dfcb7383b1fd50979a` |
| finance | `d9fdbfcbf2d578135587813cb9c8c14b640fbb40` |
| runtime | `c6e45d9e41d3b4d64b5b3dace01497c53e574026` |
| workstation | `85f904635e856612b78e8b13acc553b1e80d292a` |
| studio | `52f646022cc606985a63a5fd290c417fd337e80e` |
| security | `6a7a8f9b22cb4995d436da2968b135248f8f6bb3` |
| game | `0c8581c6b5eebceaf33aeb8907fa91a8b53708dc` |
| human | `f7725dfc9b391c3e9a0c509d49795994931c9d63` |
| harness | `286985c82874d293308297f66b23152c1ed53369` |


The discriminators cover World, Finance, Runtime, Workstation, Studio, Security, Game, Human and Harness.

R5 also executed four production-adjacent probes against the current World evaluator:

```text
world-r5-current-composition-gap-probes-20260815-01
```

---

# 3. The first real implementation gap

Current `resource_discovery` evaluates one candidate at a time.

R5 constructed:

```text
Demand requires: x + y

Resource A supports x
Resource B supports y
```

Current result:

```text
A → not-fit, demandFit=0.5
B → not-fit, demandFit=0.5
consumptionQueue = []
```

So the current evaluator cannot infer:

```text
A + B jointly satisfy x + y
```

This is a **real composition gap**.

But the control matters. A lower owner exported one composite semantic capability:

```text
Resource C supports x + y
```

and current World returned:

```text
consumable-now
```

Therefore R5 does **not** conclude that World should become a universal composer.

The actual boundary question is:

> When should a lower owner compose its internal resources and export one semantic Capability, and when must World join several cross-owner ResourceFor projections because no owner below can truthfully own the whole requirement?

---

# 4. Four frozen composition models

## A — Flat Additive Bag

> A Capability is the union/sum of individual Resource capability labels and values. More resources are non-decreasing; resources advertising the same capability are substitutes; composition needs no explicit requirement, assignment, compatibility, capacity, authority or disturbance structure.

A is the strongest form of “more resources = more capability.”

It also represents common informal reasoning such as:

```text
same capability label → substitute
more providers → redundancy
more tools/context → better system
```

## B — Universal Dependency Graph

> All Resources are nodes in one persistent cross-domain graph with stable typed edges such as requires, substitutes, complements, catalyzes and depends-on. Capability follows by graph reachability after current node-state filtering; the same edge semantics apply across actors, transitions, demands and owners.

B acknowledges structure and typed relations, but makes them global and persistent.

Its appeal is obvious: one graph appears able to answer everything.

Its risk is that transition-, purpose-, time-, load- and disturbance-scoped relations become stale global ontology.

## C — Transition-Scoped Typed Bundle / Hypergraph

> For each target transition, construct a transition-scoped typed bundle/hyperedge over ResourceFor projections. Resources receive explicit roles such as prerequisite, component, complement, substitute, catalyst and redundancy member; current authority/capacity/failure-domain constraints qualify the bundle. A supported bundle establishes an Option/Capability.

C is a strong competitor.

It fixes the biggest problem in B by scoping composition to a transition and allowing multiple resources to participate jointly.

R5 intentionally does not weaken C. It is capable of representing almost the full evidence corpus.

Its open question is whether fixed roles such as:

```text
prerequisite
component
complement
substitute
catalyst
redundancy-member
```

are themselves primitives, or merely readable names for patterns in a more basic satisfiability structure.

## D — Requirement–Assignment–Constraint Projection

> For actor A, target transition T, demand/load D and as_of t, composition is established only when there exists an assignment of supported ResourceFor/ActionableResourceFor projections to transition-specific requirements such that all material native constraints hold. Requirements state what T needs; assignments state which current resources satisfy them; constraints preserve compatibility, authority/currentness, capacity/load units, temporal/admission ordering, effect/recovery conditions and disturbance-relative independence. Substitution, complementarity, prerequisite, conversion modifiers, bottlenecks and redundancy are derived relations over feasible assignments rather than global Resource edge types. Composition is persisted only when a native owner/effect/recovery boundary requires exact bundle identity.

D is the minimum candidate.

Conceptually:

```text
Transition T
  ↓ defines
Requirements R1..Rn
  ↓
current ResourceFor / ActionableResourceFor candidates
  ↓ assignment
A : Requirements → Resources / native capabilities
  ↓ constrained by
compatibility
authority/currentness
capacity/load
temporal/admission order
effect/recovery conditions
disturbance-relative independence
  ↓
Feasible Assignment Set
  ↓
Options / supportable Capability
```

---

# 5. Frozen model results

| Model | Result across 40 discriminators |
| --- | --- |
| A — Flat Additive Bag | 0 PASS / 36 FAIL / 4 AMBIG |
| B — Universal Dependency Graph | 6 PASS / 28 FAIL / 6 AMBIG |
| C — Transition-Scoped Typed Bundle | 32 PASS / 0 FAIL / 8 AMBIG |
| D — Requirement–Assignment–Constraint | 40 PASS / 0 FAIL / 0 AMBIG |

C's result is deliberately important:

```text
32 PASS / 0 FAIL / 8 AMBIG
```

R5 does not reject C as false. It asks whether D can explain the same evidence with less ontology.

## 5.1 Complete 40-case matrix

| ID | Source | Pressure | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | `R5P01` Two separate resources x and y cannot satisfy current conjunctive demand x+y in per-resource evaluator | cross-resource conjunction | FAIL `A-FLAT` | PASS `B-GRAPH` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C02 | `R5P02` Lower owner exported composite x+y capability is consumable without World understanding internal composition | boundary export | AMBIG `A-ACCIDENTAL` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C03 | `R5P03` Two resources advertise x but one transport is unavailable | nominal substitute vs actionable substitute | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C04 | `R5P04` Same x resource is usable for research but blocked for commercial purpose | purpose-scoped substitution | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C05 | `N1` native-a/native-b may be connector redundant while converging on one physical WAN | failure-domain independence | FAIL `A-FLAT` | AMBIG `B-OVERLOAD` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C06 | `N2` WireGuard can fail while OpenVPN remains qualified on same ingress/location | disturbance-specific substitution | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C07 | `N3` Two admitted roots survive injected failure of the other | effective redundancy under tested root fault | AMBIG `A-ACCIDENTAL` | PASS `B-GRAPH` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C08 | `N4` Snowflake mechanism reaches broker but shared volunteer capacity is zero | capacity blocks composition | FAIL `A-FLAT` | AMBIG `B-OVERLOAD` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C09 | `N5` Same Snowflake resource is unavailable under one parent and available under another | parent-context composition | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C10 | `N6` Child relation binds exact ancestor capability and old child invalidates after parent generation replacement | versioned prerequisite | FAIL `A-FLAT` | PASS `B-GRAPH` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C11 | `N7` Ambient succeeds on OKX while native-a/native-b fail; scoped paths succeed on other consumers | transition-specific egress substitute | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C12 | `N8` Nominally redundant connectors fail together through half-dead shared lower substrate | common-mode failure | FAIL `A-FLAT` | AMBIG `B-OVERLOAD` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C13 | `F1` Finance executor composes site/API semantics with Workstation-exported scoped egress but does not own VPN mechanics | cross-owner requirement assignment | FAIL `A-FLAT` | AMBIG `B-OVERLOAD` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C14 | `F2` Risk policy wants to reduce exposure but participation/liquidity capacity prevents executable de-risking | bottleneck capacity | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C15 | `F3` Full diagnostic context costs ~2.16x tokens without changing sealed selection/result | non-monotonic additive value | FAIL `A-FLAT` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C16 | `F4` GVA evidence/rules plus Harness exact route admission jointly establish model/provider use | authority-aware composition | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C17 | `F5` Finance decision kernel composes belief structure and survival constraints; either alone is insufficient | multiple semantic requirements | FAIL `A-FLAT` | PASS `B-GRAPH` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C18 | `R1` Runtime Host Dependencies are explicit partial prerequisites, not complete environment closure | declared prerequisite incompleteness | FAIL `A-FLAT` | AMBIG `B-OVERLOAD` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C19 | `R2` Delayed dlopen consumes changed dependency after pre-spawn validation | temporal dependency continuity | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C20 | `R3` Target private mount namespace can consume different bytes than host-path witness | view-specific compatibility | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C21 | `R4` Runtime self-release binds exact commit+manifest+authority+deployer+Job because effect identity/recovery requires it | persist bundle only at effect boundary | AMBIG `A-ACCIDENTAL` | PASS `B-GRAPH` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C22 | `S1` REAPER complements rather than replaces FFmpeg/Resolve through distinct editable audio project state | complement not substitute | FAIL `A-FLAT` | PASS `B-GRAPH` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C23 | `S2` ImageMagick and FFmpeg tie on speed while ImageMagick survives through lower semantic friction | conversion modifier | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C24 | `S3` Blender versus Python spatial projection overlap on output but Blender uniquely supplies editable 3D scene/camera/render state | partial substitution | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C25 | `S4` OBS+Godot+Blender fallback does not automatically equal TouchDesigner live node/sensor world | bundle semantic non-equivalence | FAIL `A-FLAT` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C26 | `S5` Inkscape fallback relation changes when Figma is pending/available and when local vector mutation is required | context-dependent substitute set | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C27 | `Q1` Security composes Runtime execution, Harness cognition/tools, Security admission and provider mechanics without one gateway owner | cross-owner layered composition | FAIL `A-FLAT` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C28 | `Q2` Three evidence modes from one LLVM provider family are diverse evidence but not independent provider failure domains | evidence diversity vs redundancy | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C29 | `Q3` Independent ASan replay initially fails because reproducer changed decision-relevant semantics | semantic compatibility | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C30 | `Q4` Guardian runtime budget shorter than instrumentation envelope invalidates experiment before durable Guest result | limiting envelope bottleneck | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C31 | `G1` Fixture/policy Agents substitute for live models only when hypothesis does not require richer cognition | hypothesis-scoped substitution | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C32 | `G2` Game cognition can be policy/model/human/hierarchy; role and admission shape determine composition | heterogeneous component role | FAIL `A-FLAT` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C33 | `G3` Action admission binds exact Subject × Cognition × Actor × Intent at one planning/world revision | action-scoped composition identity | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C34 | `G4` Studio asset/output composes into Game presentation while Game retains gameplay-rule authority | cross-owner semantic composition | FAIL `A-FLAT` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C35 | `H1` Human+model capability depends on model, interface, context, tools/access and Human direction/verification | joint-system composition | FAIL `A-FLAT` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C36 | `H2` Joint-system output does not imply retained Human capability after assistant removal | boundary-relative capability | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C37 | `H3` Founder personal attention can be the limiting resource even when legal ownership and other assets exist | attention bottleneck | FAIL `A-FLAT` | AMBIG `B-OVERLOAD` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C38 | `H4` Human allocation distinguishes durability/control value from representation/retrievability and attention cost | conversion modifier vs destination | FAIL `A-FLAT` | FAIL `B-GLOBAL` | AMBIG `C-OVERCOMMIT` | PASS `D-RAC` |
| C39 | `HA1` Harness ToolProgram reduces model calls 7→2 with same five physical Tool calls | coordination catalyst/modifier | AMBIG `A-ACCIDENTAL` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |
| C40 | `HA2` Installed mechanism, Run-admitted composition and exact turn action surface are distinct | admission-scoped composition | FAIL `A-FLAT` | FAIL `B-GLOBAL` | PASS `C-BUNDLE` | PASS `D-RAC` |

---

# 6. Why A fails: capability is not additive inventory

A fails 36 of 40 discriminators.

## 6.1 Partial resources do not automatically compose

The executed `R5P01` probe is sufficient:

```text
A supports x
B supports y
Demand requires x+y
```

A Resource bag contains all nominal labels needed, yet current World correctly has no evidence that A and B are compatible, jointly admissible, jointly executable, capacity-sufficient or recoverable as one transition.

A union of labels is not a proof of composition.

## 6.2 Same label does not imply substitution

Executed `R5P03`:

```text
Resource 1 supports x, current transport available
Resource 2 supports x, current transport unavailable
```

Only one is a current substitute.

Executed `R5P04`:

```text
same resource + same x
research   → consumable-now
commercial → blocked-by-terms
```

Substitution therefore cannot be inferred from capability vocabulary alone.

## 6.3 More providers do not imply redundancy

Workstation's `native-a/native-b` can be connector/transport alternatives while sharing one lower WAN or one half-dead VPN capture substrate.

Conversely, protocol diversity sometimes matters: one observed WireGuard path failed while OpenVPN TCP/UDP remained qualified.

The relevant relation is:

```text
substitutable for transition T
AND
independent against disturbance class D
```

not:

```text
provider count >= 2
```

## 6.4 More context/tools can reduce conversion efficiency

Finance QB3b used roughly 2.16x provider tokens under the full diagnostic treatment without changing the sealed selection or result.

Harness ToolProgram achieved the opposite kind of improvement:

```text
7 model calls / 5 Tool calls
→
2 model calls / same 5 Tool calls
```

No new physical Tool capability was added. Composition changed coordination cost.

So composition value is not monotonic in resource count.

---

# 7. Why B fails: a global dependency graph puts context into the wrong owner

B is structurally richer than A but still fails 28 cases.

## 7.1 Substitution edges are not stable

The same Workstation path can substitute for one destination and fail another.

PAL P2 observed:

```text
OKX:
  ambient succeeds
  native-a/native-b fail

DeepSeek/OpenAlex:
  native-a/native-b succeed and can be materially faster
```

There is no context-free edge:

```text
native-a SUBSTITUTE ambient
```

The relation needs at least target transition/demand/currentness.

## 7.2 Dependency edges are often version- and time-scoped

Workstation child observations bind the exact ancestor capability generation. Replacing the parent generation invalidates the old child relation even when logical location/protocol stays similar.

Runtime P2/P3 go further: a declared Host Dependency can change after pre-spawn verification, and delayed `dlopen()` can consume changed bytes.

So a graph edge:

```text
A REQUIRES B
```

is insufficient without identity, time/view and effect-boundary semantics.

## 7.3 Some dependencies cannot be completely discovered

Runtime explicitly refuses to claim complete dynamic environment closure.

That is not a missing graph crawler. It is a proof boundary: loaders, drivers, network, services and namespaces can influence execution without being inferable as one complete static dependency graph.

A universal graph creates pressure to turn unknown ambient context into false completeness.

## 7.4 Cross-owner composition does not create a cross-owner state owner

Security's CA5 audit is explicit:

```text
Runtime   → physical execution/recovery
Harness   → cognition/tool composition
Security  → adversarial effect admission
Provider  → provider mechanics
```

A global World dependency graph would tend to become a fifth owner of relations whose semantic truth remains elsewhere.

R4 already rejected that architecture pattern for state; R5 finds the same pattern in composition.

---

# 8. C is strong—but fixed role ontology is not yet earned

C handles most evidence correctly.

It can represent:

```text
A+B required jointly
A/B alternatives
capacity constraints
exact prerequisites
failure domains
current authority
```

So why not stop at C?

Because the familiar role names can change under context.

## 8.1 Substitute can become complement

At one load, CPU and GPU may each independently satisfy an execution requirement.

At a larger load, GPU memory plus host RAM can become jointly necessary.

The pair changed from:

```text
substitutes
```

to:

```text
complements
```

without either Resource changing identity.

## 8.2 A prerequisite can be irrelevant on another path

A signed entitlement may be mandatory for one provider path and irrelevant for an offline fallback.

So `PREREQUISITE` is a property of a requirement/path/admission relation, not the Resource itself.

## 8.3 A catalyst can become a hard requirement

A cache may only reduce cost for a small workload, but at larger volume the uncached path may exceed the economic or token budget and become inadmissible.

The same mechanism moved from:

```text
conversion modifier
```

to effectively:

```text
necessary requirement satisfaction
```

Fixed role names are therefore useful **views**, not necessarily primitives.

## 8.4 Bottleneck is not a role assigned in advance

Liquidity, quota, Human attention, runtime envelope or network throughput becomes the bottleneck only relative to requested load and the surrounding assignment set.

The bottleneck can move after one capacity change.

So C's typed hypergraph is expressive, but R5 has not found a reason to store those role labels as the root ontology.

---

# 9. D's basic structure

D reduces composition to four questions.

## 9.1 Requirement

A Requirement says:

> What must be true or available for target transition T under this domain's semantics?

Examples:

```text
Finance order dispatch:
  current venue/site semantics
  current trading authority
  current egress path to exact production origin
  survival/admission permission

Repository repair:
  source read
  digest-bound mutation
  check
  diff
  reread

Game Agent action:
  exact Subject
  exact Cognition
  exact Actor
  exact Intent
  current Planning/World binding
```

Requirements belong to the owner/domain that understands the target transition.

World should not invent domain semantics from Resource metadata.

## 9.2 Assignment

An Assignment answers:

> Which current ResourceFor/ActionableResourceFor projection satisfies this Requirement?

One Requirement may have:

```text
zero assignments   → transition infeasible / more work required
one assignment     → single current path
many assignments   → optionality; possible substitution
```

The assignment is contextual.

## 9.3 Constraint

Constraints preserve the facts that make a set of assignments jointly valid:

```text
semantic compatibility
authority/currentness
capacity/load units
temporal/admission ordering
exact identity/version/view
effect/recovery contract
failure-domain/disturbance independence
```

These truths remain owner-native where possible.

## 9.4 Projection

A feasible composition is then a projection:

```text
Feasible(T, demand, load, as_of)
iff
∃ assignment A
  such that every hard requirement is satisfied
  and every material constraint holds
```

A selectable feasible assignment becomes an Option.

A reliably supportable class of such transitions supports a Capability claim at the appropriate owner/system boundary.

---

# 10. Relation ledger after reduction

| Concept | R5 placement | Verdict | Discriminators | Why |
| --- | --- | --- | --- | --- |
| Requirement | `transition/domain-authored semantic condition` | **REQUIRED** | C01, C17, C35, C40 | Without explicit requirements, partial resources cannot be composed and lower-owner exports cannot be distinguished from unmet conjunctions. |
| Assignment | `projection from ResourceFor/ActionableResourceFor to one requirement` | **REQUIRED** | C03, C09, C13, C31 | The same Resource can satisfy one transition/purpose and fail another; satisfaction is contextual mapping, not a global edge. |
| Compatibility | `constraint over assignments/effect boundary` | **REQUIRED** | C20, C25, C29, C33 | Nominal capabilities can fail when view, semantics, revision or action binding differ. |
| Authority/currentness | `native constraints consumed by projection` | **REQUIRED_CONSTRAINT_NOT_COMPOSITION_OWNER** | C04, C10, C16, C40 | Composition cannot launder authority; current native admission facts qualify assignments. |
| Capacity/load | `native quantity/rate/budget constraints with units` | **REQUIRED_WHEN_BINDING** | C08, C14, C30, C37 | Capability existence and executable quantity diverge; bottlenecks emerge only relative to requested load. |
| Substitution | `derived relation between alternative feasible assignments for same requirement/context` | **DERIVED_NOT_GLOBAL_EDGE** | C03, C06, C11, C24, C31 | Substitution changes with transition, purpose, current access, semantic ceiling and disturbance. |
| Complementarity | `derived joint-feasibility or interaction relation among assignments` | **DERIVED_NOT_GLOBAL_EDGE** | C17, C22, C25, C35 | Resources complement when joint assignment satisfies requirements or creates a transition neither supplies alone; not an intrinsic pair label. |
| Prerequisite | `hard temporal/admission requirement/constraint` | **DERIVED_CONSTRAINT** | C10, C18, C19, C40 | Prerequisite describes ordering/admission for one transition; it is not a universal resource type and may be version/time scoped. |
| Conversion modifier / catalyst | `derived effect on cost, latency, reliability, attention or conversion rate without necessarily changing feasible set` | **SURVIVES_AS_MODIFIER_RELATION** | C15, C23, C38, C39 | Some resources/mechanisms improve conversion efficiency while adding no new physical transition; deleting this distinction misclassifies real gains. |
| Bottleneck | `derived binding constraint / least slack under requested load` | **DERIVED_NOT_RESOURCE_TYPE** | C08, C14, C30, C37 | Bottleneck can move as load/capacity changes and may be quota, liquidity, time, attention or control envelope. |
| Failure-domain independence | `native evidence + disturbance-scoped relation over alternative assignments` | **REQUIRED_FOR_REDUNDANCY_CLAIM** | C05, C06, C07, C12, C28 | Alternative count or provider labels cannot establish survival under a disturbance. |
| Redundancy | `derived set of >=2 feasible substitutes with sufficient independence against declared disturbance` | **DERIVED** | C05, C07, C12, C28 | Redundancy is not resource count; it requires substitutability, actionability and independence under the target disturbance. |
| Bundle identity | `owner-native effect/recovery boundary only when exact members materially define action/effect` | **CONDITIONAL_PERSISTENCE** | C21, C33, C40 | Exact bundle persistence is justified for replay/recovery/action identity, not for every planning composition. |

This is the central R5 compression.

The familiar vocabulary survives, but mostly as **derived relations**.

---

# 11. Substitution is assignment equivalence, not Resource identity

R5's current definition candidate is:

```text
Resources A and B are substitutes
for requirement R
under context C
iff
A and B are distinct feasible assignments to R
and replacing A with B preserves the relevant transition constraints.
```

This immediately explains why substitution is not transitive or permanent.

For example:

```text
A substitutes B for OpenAlex
A does not substitute B for OKX
```

or:

```text
A substitutes B at low load
A does not substitute B at high load
```

or:

```text
A substitutes B under ordinary provider failure
A and B fail together under shared identity-provider outage
```

Therefore no global `substituteEdge(A,B)` is justified.

---

# 12. Complementarity is joint feasibility / interaction

A and B are complements when their joint assignment changes transition feasibility or material transition properties relative to the relevant alternatives.

Two common forms are enough for R5:

### Requirement complementarity

```text
Requirement R1 needs A
Requirement R2 needs B
T requires R1 AND R2
```

Example: Finance belief structure + survival gate.

### Interaction complementarity

A+B jointly provide a property not available from either assignment alone.

Example: REAPER's editable multitrack project-state world complements FFmpeg/Resolve workflows rather than merely duplicating them.

R5 does not yet need a global complement edge or superadditivity score.

---

# 13. Prerequisite is temporal/admission structure

`Prerequisite` survives only as a readable description of a hard constraint such as:

```text
before action admission,
claim/resource/effect P must already be established.
```

Examples:

- exact Workstation parent capability before child binding;
- Runtime-declared Host Dependency before dispatch and through the relevant continuity window;
- exact Harness Run/Turn admission before a Tool action exists;
- provider entitlement before one online path.

This is why a prerequisite can be absent on another path without contradiction.

---

# 14. Conversion modifier / catalyst survives—but narrowly

R5 finds one concept that should **not** be deleted entirely.

Some Resources/mechanisms alter:

```text
cost
latency
reliability
Human attention
model-call count
token use
conversion rate
```

without necessarily changing the current feasible transition set.

Examples:

- ImageMagick retained value through lower semantic friction despite tied resize speed;
- Harness ToolProgram reduced model calls while keeping the same five physical Tool calls;
- Human knowledge representation/retrievability changes attention cost without automatically changing semantic knowledge destination;
- verbose diagnostic context can be a **negative** modifier when it adds token cost without better outcome.

R5 therefore retains:

```text
ConversionModifier(resource/mechanism, transition, context)
```

as a **derived relation**.

`Catalyst` can remain informal shorthand, but no universal `CatalystResource` class is earned.

---

# 15. Bottleneck is the currently binding constraint

R5 rejects:

```text
resource.is_bottleneck = true
```

A bottleneck is derived relative to a requested load and feasible composition.

Examples:

### Workstation Snowflake

Local client/broker mechanics exist, but shared volunteer capacity can be zero.

Capacity is the binding constraint.

### Finance de-risking

Policy knows desired exposure should fall, but liquidity participation can prevent the resize.

Liquidity capacity is binding.

### Security D3

Guardian runtime was 90s while instrumentation envelope was 120s.

The outer control budget invalidated the experiment before durable Guest result.

### Human founder

Legal ownership, knowledge and business assets can all exist while personal attention remains the limiting throughput resource.

So the useful question is:

> Which current constraint has the least relevant slack / highest marginal effect on feasible throughput for this transition/load?

R5 does not create one unitless bottleneck score across money, time, throughput, tokens and attention.

---

# 16. Capacity must preserve native units

R5 strengthens R0/R1's stock/flow warning.

Capacity can mean:

```text
requests / minute
bytes / second
tokens / run
concurrent Jobs
capital available
liquidity participation
Human minutes
GPU memory
quota units
```

These cannot be normalized into one scalar without a workload-specific conversion model.

Composition therefore asks only for the quantity constraints materially required by the target transition.

A Resource can satisfy a semantic requirement while failing the requested load.

This distinction is essential for redundancy too: an independent fallback with only 10% of required throughput is not full redundancy for that load.

---

# 17. Redundancy is a derived composition property

R5 gives effective redundancy a sharper structure:

```text
RedundantFor(requirement R, disturbance D, load L, as_of t)
requires
  >= 2 distinct feasible assignments
  + each is Actionable for R/L/t
  + assignments are sufficiently substitutable for R
  + failure evidence supports independence under D
```

This rejects several common shortcuts:

```text
2 endpoints        != redundancy
2 providers        != redundancy
2 protocols        != redundancy
2 evidence modes   != redundancy
```

Workstation provides both sides of the discriminator:

- native connector identities can share a lower failure domain;
- independently admitted roots survived injected failure of the other under the tested root-fault class;
- protocol diversity protected against one observed protocol-level failure;
- the same alternatives may still share a physical WAN.

Security CA2 likewise shows three evidence modes in one LLVM provider family are not three independent provider failure domains.

Redundancy is therefore disturbance-specific proof, not inventory count.

---

# 18. Lower-owner composition versus World composition

`R5P02` gives the default preference:

```text
lower owner can truthfully compose
+ owns effect/recovery semantics
+ can export one stable semantic capability
→ higher owner consumes exported Capability as Resource
```

Examples already established across Ordivon:

```text
Workstation egress capability → Finance Resource
Runtime contained execution → Harness/domain Resource
Harness cognition/tool composition → Game/Security/Finance Resource
Studio editable media capability → Game production Resource
```

World should **not** reopen internals merely because it can enumerate them.

Cross-owner composition is justified only when no lower owner truthfully owns all requirements.

Finance order readiness is a good example: Finance owns venue/risk semantics while Workstation owns transport and an account/provider owns authority. No single lower owner can truthfully export the complete decision-ready capability without stealing another owner's semantics.

That is where requirement assignment is useful.

---

# 19. Persist composition only where identity/recovery needs it

R4's persistence law survives R5.

Planning composition is usually recomputable:

```text
requirements
+ current claims
+ current assignments
→ current feasible Options
```

Persisting every assignment would create a stale dependency graph.

But some compositions **must** bind exact members because changing them changes the action/effect.

Runtime self-release is an example: exact Workspace commit, manifest, deployment authority, deployer and Job jointly define the structured effect identity/recovery contract.

Game action admission similarly binds exact Subject × Cognition × Actor × Intent × planning/world revision.

Harness ToolProgram retains exact outer action and per-step evidence for recovery.

Therefore the persistence rule is:

> **Persist exact composition identity only at an owner-native admission/effect/recovery boundary where member changes materially change the action. Recompute planning composition elsewhere.**

---

# 20. C versus D: the deletion result

C remains expressive. D is preferred provisionally because the typed role ontology can be reconstructed from requirement-assignment structure.

Examples:

```text
Substitute
= alternative feasible assignments to same requirement

Complement
= assignments whose joint satisfaction/interaction is required

Prerequisite
= hard temporal/admission constraint

Conversion modifier
= assignment/mechanism changes cost/rate/reliability without necessarily changing feasibility

Bottleneck
= currently binding capacity/constraint for requested load

Redundancy
= multiple feasible substitutes + disturbance-relative independence
```

So R5 does not need these as six primitive edge classes.

The words remain useful for explanation and local domain projections.

---

# 21. Deletion / rejected-addition tests

| Mutation | Result | Discriminators | Why |
| --- | --- | --- | --- |
| delete transition-specific requirements | **FAIL** | C01, C17, C35 | Cannot distinguish partial capability inventory from a sufficient composition proof. |
| delete assignment relation and use capability labels globally | **FAIL** | C03, C04, C11, C31 | Same nominal capability has different admissibility/fitness across contexts. |
| delete compatibility/semantic binding constraints | **FAIL** | C20, C25, C29, C33 | Nominally matching components can compose into the wrong bytes, semantics, revision or action binding. |
| delete capacity/load constraints | **FAIL** | C08, C14, C30, C37 | Feasible capability claims become false under zero shared capacity, liquidity freeze, runtime envelope or attention bottleneck. |
| delete disturbance/failure-domain evidence from redundancy | **FAIL** | C05, C07, C12, C28 | Correlated alternatives are misclassified as resilient redundancy. |
| add global substitute edges | **REJECT_ADD** | C04, C06, C11, C24, C31 | Substitution is transition/purpose/as_of/disturbance scoped. |
| add global complement edges | **REJECT_ADD** | C17, C22, C25, C35 | Complementarity follows from joint requirement satisfaction/interaction and changes with target transition. |
| promote prerequisite to universal Resource type | **REJECT_ADD** | C10, C18, C19, C40 | Prerequisite is a temporal/admission constraint and may refer to authority, bytes, parent capability or prior observation. |
| promote catalyst to universal Resource class | **REJECT_ADD** | C15, C23, C38, C39 | The useful invariant is conversion modification; the same resource can be necessary in one transition and merely efficiency-improving in another. |
| promote bottleneck to fixed Resource property/type | **REJECT_ADD** | C08, C14, C30, C37 | Binding constraint changes with requested load, capacities and surrounding assignments. |
| persist every feasible composition as global bundle/dependency graph | **REJECT_ADD** | C02, C13, C27, C34 | Lower owners already export semantic capabilities and cross-owner planning compositions often need no durable shared identity. |
| treat adding resources as non-decreasing capability/value | **REJECT_ADD** | C15, C23, C25, C39 | Extra context/tools can add cost/friction without new capability; modifiers can be positive, zero or negative. |

Five structures survive deletion:

```text
transition-specific requirements
assignment mapping
compatibility / semantic binding
capacity/load constraints when material
disturbance/failure evidence for redundancy
```

Authority/currentness and temporal/effect constraints are also necessary where the transition requires them, but those truths remain native claims rather than becoming a Composition owner.

---

# 22. R5 relation algebra candidate

Without proposing a production DSL, the current reasoning form can be written compactly.

Let:

```text
T = target transition
R(T) = transition-specific hard requirements
A = assignment from each requirement to one or more current ResourceFor projections
C(A,T,D,t) = material constraints for demand/load D at time t
```

Then:

```text
Feasible(A,T,D,t)
  iff
  all hard requirements are satisfied by A
  and all material constraints hold
```

The feasible assignment set is:

```text
F(T,D,t) = { A | Feasible(A,T,D,t) }
```

Then:

```text
Option
≈ selectable member of F(T,D,t)
```

and a Capability claim requires evidence that the actor/system can reliably support the relevant transition class, not merely that one assignment once appeared feasible.

Derived relations operate over `F`, not over global Resource identity.

---

# 23. Fresh post-freeze falsifiers

D's wording was frozen before the following eight cases were authored.

| ID | Fresh case | D |
| --- | --- | --- |
| R5Y01 | Two API providers satisfy the same semantic requirement, but both depend on the same upstream identity provider; they are substitutes for ordinary provider failure but not for identity-provider outage. | PASS `D-DISTURBANCE` |
| R5Y02 | One GPU and one CPU can each execute a small model, but a larger batch requires GPU memory plus host RAM simultaneously; substitution at low load becomes complementarity at high load. | PASS `D-LOAD-CHANGES-RELATION` |
| R5Y03 | A cache does not change the set of tasks the system can perform but reduces repeated provider cost enough to make a workload economically admissible. | PASS `D-CONVERSION-MODIFIER` |
| R5Y04 | A signed entitlement is a hard prerequisite for one provider call, while the same entitlement is irrelevant to an offline fallback path. | PASS `D-PATH-SCOPED-PREREQ` |
| R5Y05 | Three resources are all individually current, but two cannot be composed because their licenses forbid the target redistribution while the third can pair with either for internal analysis. | PASS `D-COMPAT-AUTHORITY` |
| R5Y06 | A durable effect records exact input bundle identity for replay, while a planning-only alternative bundle is recomputed after current capacity changes. | PASS `D-CONDITIONAL-PERSISTENCE` |
| R5Y07 | Two independent routes are both feasible substitutes, but one has only 10% of required throughput; it contributes partial capacity but is not full redundancy for the requested load. | PASS `D-CAPACITY-REDUNDANCY` |
| R5Y08 | A Human reviewer is not required for low-consequence drafts but becomes a hard admission requirement for a high-consequence publication using the same model/tool resources. | PASS `D-CONSEQUENCE-REQUIREMENT` |

D survives all eight without wording change.

The strongest fresh pressures are:

- disturbance-specific substitution under a shared upstream identity provider;
- substitution becoming complementarity as load changes;
- a cache acting as conversion modifier without changing nominal capability;
- one entitlement being prerequisite on one path and irrelevant on another;
- license compatibility blocking otherwise current resources;
- durable effect bundle identity coexisting with recomputed planning bundles;
- partial independent capacity failing full redundancy for requested load;
- Human review becoming a hard requirement only when consequence changes.

This remains falsifier evidence, not universal proof.

---

# 24. Current production implications

R5 finds one genuine current limitation:

```text
current resource_discovery evaluator
= per-candidate demand fit
```

It cannot express conjunctive multi-resource requirement satisfaction.

However R5 does **not** yet authorize a production composition engine.

Why not?

1. Lower owners already successfully export composed semantic capabilities.
2. Harness already owns bounded mechanical Tool composition.
3. Runtime already owns exact effect bundle identity where recovery demands it.
4. Security/Game/Finance retain domain-specific action semantics.
5. One reproduced World evaluator gap is insufficient evidence for a global graph/service.

The smallest future production experiment, if demanded by a real consumer, should therefore be a **demand-scoped composition projection** over explicit requirements and existing evidence—not a registry.

---

# 25. Carried R3 debt remains separate

R3F01/R3F02 established that `ResourceCandidate.capabilities` can satisfy demand fit without claim-level owner evidence for that semantic capability.

R5 makes that debt more important, not less:

```text
an Assignment is only as valid as the ResourceFor claim it assigns.
```

A future composition projection must not combine unverified capability labels into a synthetic Capability.

So the implementation order is logically:

```text
claim-level transition evidence boundary
before
production cross-resource composition
```

R5 does not silently fix either in this research round.

---

# 26. R5 provisional root model

The surviving candidate is D:

```text
Reality / owner-native Claims + Events
          │
          ▼
ResourceFor / ActionableResourceFor projections
          │
          ▼
Target Transition Requirements
          │
          ▼
Requirement ← Assignment → Resource
          │
          ▼
Native Constraints
  compatibility
  authority/currentness
  capacity/load
  temporal/admission
  effect/recovery
  disturbance independence
          │
          ▼
Feasible Assignment Set
          │
     ┌────┴────┐
     ▼         ▼
   Option   Capability evidence
```

Then the familiar concepts are derived views over that structure.

---

# 27. What R5 rejects

1. No Flat Additive Resource Bag as capability model.
2. No global `same capability label => substitute` rule.
3. No provider/endpoint count as redundancy proof.
4. No universal persistent Resource dependency graph.
5. No global substitute/complement/prerequisite/catalyst/bottleneck edge ontology.
6. No universal `CatalystResource` class; preserve conversion modifier relation instead.
7. No fixed `BottleneckResource`; derive the binding constraint under requested load.
8. No one scalar capacity across incompatible native units.
9. No automatic promotion of a planning composition into durable bundle identity.
10. No World-owned composer when a lower owner can truthfully export the composed semantic capability.
11. No laundering of authority/currentness/failure-domain truth through composition.
12. No production Composition Registry/DependencyGraph/CapabilityManager from R5.
13. No composition from unverified candidate capability labels.

---

# 28. What R5 resolves enough for R6

R5 provisionally resolves the composition boundary:

### Composition primitive

Not `Bundle` or `Graph`, but:

```text
Requirement + Assignment + Constraint + Projection
```

### Substitution

Alternative feasible assignments for the same requirement/context.

### Complementarity

Joint requirement satisfaction or interaction that changes feasibility/material transition properties.

### Prerequisite

Hard temporal/admission constraint, not Resource type.

### Conversion modifier / catalyst

Derived relation that changes conversion cost/rate/reliability/attention, possibly without changing feasible set.

### Bottleneck

Current binding constraint for target transition/load.

### Redundancy

Multiple feasible substitutes with sufficient disturbance-relative independence and capacity.

### Persistence

Only where exact composition identity is part of an owner-native admission/effect/recovery contract.

### Higher-level Resource recursion

A lower owner's composed Capability remains consumable as a higher-level Resource without transferring internal composition or authority.

---

# 29. R6 handoff: conversion chain / action-effect-outcome

R5 now makes the next unresolved boundary much sharper.

Even after a feasible composition exists:

```text
Capability / Option
```

we still need to distinguish:

```text
selection
Action
Effect
Outcome
Attribution
Knowledge
```

R0 already suspected the current chain is compressed:

```text
Capability → Effect → Knowledge
```

R6 should now attack:

```text
Capability
→ selected feasible assignment
→ Action / admitted effect request
→ Effect / physical or semantic consequence
→ Outcome / domain value
→ Attribution
→ Knowledge
```

Questions for R6:

1. Is `Action` distinct from `Effect` across all material domains?
2. When is an Effect exact/historical while Outcome remains unknown?
3. Can one Action produce multiple Effects or one Outcome require multiple Actions?
4. Where does consumption belong for rival/non-rival Resources?
5. How does attribution distinguish composition failure from resource failure, execution failure, environment change and domain-value failure?
6. Which evidence owner may promote Effect to Outcome?
7. How does null/negative Outcome become Knowledge without rewriting historical Effect truth?

R6 must preserve the R5 rule that a feasible composition proves only **ability/action possibility**, not success or value.

---

# 30. Conclusion

R5 began with an intuitive picture:

```text
Resource A ─┐
Resource B ─┼─ dependency/composition graph → Capability
Resource C ─┘
```

The evidence supports a thinner foundation:

```text
What does transition T require?
        ↓
Which current Resources can satisfy each requirement?
        ↓
Can those assignments coexist under current native constraints and requested load?
        ↓
Which feasible assignments are selectable?
```

That is enough to recover substitution, complementarity, prerequisites, modifiers, bottlenecks and redundancy **without making them universal Resource edge types**.

The key law candidate is:

> **Composition is not a property of a bag of Resources. It is a context-bound proof that current Resources can be assigned to a transition's requirements under material native constraints.**

And the architectural consequence is:

> **Compose below the boundary when one owner can truthfully own the whole capability; project across owners only when the requirement itself crosses ownership boundaries.**

That is the R5 result carried into R6. It remains provisional research, not canonical World doctrine.
