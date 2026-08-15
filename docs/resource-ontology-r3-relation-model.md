---
schema_version: 1
id: world.resource-ontology-r3-relation-model
title: Resource Ontology R3 — Minimal Relation Model Falsification
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
summary: Falsifies competing Resource relation models and separates Resource identity, proof obligations, Actionability joins and portfolio relations without creating a Resource schema or registry.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-ontology-r0-census
  - world.resource-ontology-r1-theory-triangulation
  - world.resource-ontology-r2-definition-falsification
  - world.resource-option-capability-model
  - world.resource-opportunity-flywheel
---
# Resource Ontology R3 — Minimal Relation Model Falsification

## 1. Question

R2 produced a provisional Resource definition, E `Evidenced Enrollable Potential`, with six conceptual requirements:

```text
actor/system-relative
identifiable Reality aspect
evidence
transition mechanism
bounded feasibility
intentional/admissible enrollability
```

R3 asks the more dangerous engineering question:

> Which of those are actually **Resource relation semantics**, which are merely **proof obligations**, which belong only to **Actionable Resource / Option / valuation**, and which facts must remain owned by their native systems rather than copied into World?

R3 explicitly refuses the easy transformation:

```text
six concepts
→ six fields
→ ResourceRelation schema
→ global registry
```

That would confuse a reasoning model with a storage model.

R3 instead freezes competing relation models, attacks them with cross-domain cases, audits the existing `resource_discovery` implementation, and uses coordinate deletion tests.

No R3 result is canonical production doctrine.

---

# 2. Evidence boundary

R3 starts from canonical World main `f6337ab6ca1a30127e1ae2b8882fcbe18c785425`.

Frozen source digests:

- `docs/resource-ontology-r0-census.md` → `sha256:572091ddafbd79e6c95d584a16b753ac96b6f94493bbf9721a690aa464b1b3a9`
- `docs/resource-ontology-r1-theory-triangulation.md` → `sha256:63bd83b0ba94fab4e74c4bea999ce43b39d131393a9964b101dea8a5727d9dc2`
- `docs/resource-ontology-r2-definition-falsification.md` → `sha256:97a3765d58a74cfdc1f6c3df8076b77f6acb867ae196391ed7c3145e6603cd11`
- `src/ordivon_world/resource_discovery.py` → `sha256:d78e7a0fa274847e83b737c06baedd8b7047a50312b92a9d6a33cbf3b4dca840`


R3 uses 40 relation-discriminator cases drawn from the frozen R0/R2 corpus plus one directly executed implementation falsifier (`R3F01`). The test set emphasizes identity/provenance, nested boundaries, deferred authority, currentness, non-object resources, transition-specific authority, representation/materialization, capacity, liabilities and portfolio relations.

---

# 3. Four frozen relation models

## A — Universal Relation Tuple

> A Resource relation is one universal tuple containing actor/system boundary, aspect identity, owner, provenance, transition/interface, authority/admissibility, acquisition path, access/transport, capacity, currentness/expiry, cost/risk, dependencies, failure domain and substitutability. The tuple is the Resource relation; missing coordinates are materially incomplete.

A is the intuitive schema-first response: put every potentially useful coordinate on one `ResourceRelation` record.

Its falsifier is not implementation complexity alone. Its semantic claim is that those coordinates jointly constitute Resource relation identity/completeness.

## B — Actor-Aspect Pair

> A Resource relation is established by an actor/system boundary plus an identifiable Reality aspect with evidence that the aspect exists. Transition mechanism, direction, admissibility, feasibility and current qualification are all downstream.

B takes R2's actor-relative result seriously but removes transition/enrollment structure from Resource itself.

Its risk is over-breadth: anything real for an actor can become Resource if existence evidence is enough.

## C — Supported Enrollment Relation

> Relative to a declared actor/system scope and an identifiable Reality aspect, Resource(actor, aspect, as_of) is supported when there exists at least one transition witness and an evidence envelope whose native claims jointly establish a bounded, admissible path by which the actor can intentionally enroll that aspect as a means, input or enabling relation for that transition family. The coarse Resource projection is existential over transition witnesses; ResourceFor retains the transition family when precision is required. Owner, authority, access, capacity, cost, failure domain and substitutability are not universal Resource-tuple fields; they remain claim-native support or downstream joins.

C separates **relation semantics** from **supporting truth**.

Its coarse form is:

```text
Resource(actor, aspect, as_of)
iff
∃ transition_family:
    SupportedEnrollment(actor, aspect, transition_family, as_of)
```

and the precise form is:

```text
ResourceFor(actor, aspect, transition_family, as_of)
```

A supported enrollment is not a new persisted entity. It is a claim/projection justified by an evidence envelope whose native facts establish a bounded admissible path for intentional enrollment.

## D — Demand-Only Projection

> No workload-independent Resource relation exists. Resource status is only a demand-scoped projection from discovered candidate facts plus current owner/authority/access/fit evidence for one active ConsumerDemand.

D takes the current `evaluate_resource(candidate, demand, ...)` shape to its logical extreme: no workload-independent Resource relation exists at all.

Its pressure is R2's dormant/gated/general-purpose evidence.

---

# 4. Relation-model results

| Model | Result across 40 discriminators |
| --- | --- |
| A — Universal Relation Tuple | 0 PASS / 34 FAIL / 6 AMBIG |
| B — Actor-Aspect Pair | 28 PASS / 9 FAIL / 3 AMBIG |
| C — Supported Enrollment Relation | 40 PASS / 0 FAIL / 0 AMBIG |
| D — Demand-Only Projection | 20 PASS / 18 FAIL / 2 AMBIG |

The counts are not a score. The failure *shape* matters.

## 4.1 Complete 40-case relation matrix

| ID | Source | Pressure | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| R01 | `W01` Discovery source versus owner truth | identity/provenance | AMBIG `A-UNIVERSAL` | PASS `B-PAIR` | PASS `C-SER` | AMBIG `D-IDENTITY` |
| R02 | `W02` Required authority versus possessed authority | authority stage separation | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R03 | `W03` Parent entitlement unlocks children | deferred prerequisite/enrollment | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R04 | `W05` Signup transport versus resource value | stage/path-scoped access | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R05 | `W07` Historical admission versus current presence | historical evidence/currentness | FAIL `A-LAYER` | AMBIG `B-TIME` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R06 | `W08` Capability becomes a higher-layer resource | nested system boundary | AMBIG `A-UNIVERSAL` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R07 | `N02` Two logical alternatives share a failure domain | portfolio independence | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R08 | `N04` Executable Snowflake client but no shared capacity | capacity vs relation | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R09 | `N05` Same mechanism changes actionability under parent relation | relation/path context | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | PASS `D-DEMAND` |
| R10 | `N09` Historical child resource invalidated by parent change | dependency currentness | FAIL `A-LAYER` | AMBIG `B-TIME` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R11 | `N11` Stable consumer resource over replaceable physical members | semantic identity over mechanism | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R12 | `N12` Installed capability excluded from ambient authority | possession vs authority | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R13 | `F02` High-value FRED but current key absent | deferred authority | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R14 | `F03` Source bytes versus research-grade evidence | truth role/provenance | AMBIG `A-UNIVERSAL` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R15 | `S02` OBS retained while listener default-off | dormant resource | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R16 | `S05` Figma configured but OAuth consent absent | resource vs actionability | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R17 | `S06` TouchDesigner option before license acquisition | pre-demand/deferred resource | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R18 | `G01` CC0 catalog requires exact asset identity/license | aspect identity granularity | AMBIG `A-UNIVERSAL` | PASS `B-PAIR` | PASS `C-SER` | AMBIG `D-IDENTITY` |
| R19 | `G03` Live cognition changes actions but not proven player value | transition vs Outcome | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R20 | `Q02` Provider claim does not become Security truth | claim-native truth role | AMBIG `A-UNIVERSAL` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R21 | `Q03` Sample can support static analysis while execution remains unauthorized | transition-specific authority | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | PASS `D-DEMAND` |
| R22 | `Q04` Reference can preserve option without local bytes | representation/materialization | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R23 | `Q06` Remote entitlement and remote capability are different | authority carrier vs capability | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R24 | `H01` Generic Resource role was deleted in Human | over-broad ontology | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | PASS `D-DEMAND` |
| R25 | `H02` Same tool changes role with the question | actor/question relation | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | PASS `D-DEMAND` |
| R26 | `H03` Joint-system capability does not become retained Human capability | nested actor boundary | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R27 | `H04` Human attention is scarce conversion capacity | flow/non-object resource | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | PASS `D-DEMAND` |
| R28 | `X08` Reputation/relationship enables review without being an owned object | social relation resource | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R29 | `X09` Technical debt shrinks safe options | direction/liability | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | PASS `D-DEMAND` |
| R30 | `X12` Legal permission exists while bytes are absent | institutional relation | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R31 | `X18` Hostile botnet capability is controlled by adversary | resource-for-whom | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | PASS `D-DEMAND` |
| R32 | `X24` Stale dataset valid historically but not for current-state claim | claim-specific currentness | FAIL `A-LAYER` | AMBIG `B-TIME` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R33 | `X28` Component useful only with cheaply acquirable complement | bounded complement path | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R34 | `X30` Formal option expires before prerequisites can be satisfied | temporal bounded feasibility | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R35 | `X05` Healthy idle GPU with no current workload | workload-independent resource | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R36 | `X13` Unexercised contractual option/right | non-object option resource | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R37 | `X19` Idle unrestricted cash reserve | rival stock with optionality | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R38 | `X26` Encrypted backup with irretrievably lost key | identified aspect without feasible path | FAIL `A-LAYER` | FAIL `B-NOWITNESS` | PASS `C-SER` | PASS `D-DEMAND` |
| R39 | `X27` Decayed skill with bounded cheaper refresh | latent reacquisition resource | FAIL `A-LAYER` | PASS `B-PAIR` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |
| R40 | `R3F01` Aggregator-only capability claim currently reaches consumable-now when owner only confirms terms/interface | transition-witness provenance gap | AMBIG `A-UNIVERSAL` | FAIL `B-NOWITNESS` | PASS `C-SER` | FAIL `D-NO-PREDEMAND` |

---

# 5. Why A fails: one tuple collapses independent truth layers

A tries to make these all Resource-relation coordinates:

```text
actor
aspect
owner
provenance
transition/interface
authority
acquisition path
access
capacity
currentness
cost/risk
dependencies
failure domain
substitutability
```

But R0–R2 repeatedly show that these coordinates change independently.

Examples:

### Authority changes without Resource identity changing

`F02`, `S05`, `S06` remain legitimate deferred Resources while current consuming authority is absent.

If authority is part of the Resource tuple's required identity, then:

```text
same FRED API + no key
same FRED API + active key
```

become two different Resource relations, when the important difference is Actionability.

### Transport changes without Resource identity changing

`W05`, `S02`, `Q04` show current materialization/reachability can disappear while the Resource relation or future option remains meaningful.

### Failure domain changes portfolio truth, not Resource identity

`N02` and `N11` show that a path can remain the same Resource while evidence about shared physical failure domain changes redundancy.

### Substitutability changes marginal value, not identity

A new substitute can make Inkscape or one VPN path low-value without erasing the underlying Resource.

### One currentness field is false compression

Owner terms, possessed authority, transport, shared capacity, current presence and historical admission each have independent clocks/truth roles.

Therefore A's failure is conceptual:

> **It turns a join of independent claims into the identity of the thing being reasoned about.**

That is exactly the kind of schema bureaucracy R3 was intended to prevent.

---

# 6. Why B is too thin: actor + aspect cannot establish direction

B gets two important things right:

```text
resource-for-whom
exact aspect identity
```

It therefore handles nested boundary cases and many non-object Resources better than object-centric ontology.

But without a transition/enrollment witness it cannot reliably distinguish:

```text
Resource
Hazard
Liability
Target
Background Reality
```

Examples:

- `X18` hostile botnet is real relative to Ordivon but is a hazard, not an Ordivon Resource.
- `X09` technical debt is real and causally important but directionally shrinks feasible safe action.
- `Q03` the same malware bytes support static analysis but not authorized execution.
- `X30` an option/right that cannot be exercised before expiry has identity but no bounded enrollment path.
- `R3F01` an aggregator can name a capability without supplying authoritative evidence that the aspect actually supports that transition.

So transition/enrollment evidence is not merely downstream Actionability.

R3's correction to B is subtle:

> The transition family need not fragment coarse Resource **identity**, but at least one transition witness is required to establish the Resource relation at all.

---

# 7. Why D is too late: Resource cannot begin at active demand

D matches a useful current production pattern: `ResourceEvaluation` is demand-scoped and recomputed from current evidence.

But if *Resource existence itself* begins only with active `ConsumerDemand`, R2's strongest cases disappear:

```text
idle GPU
cash reserve
unexercised right
TouchDesigner before current project
FRED before current key
reference-preserved sample
relationship/reputation
bounded reacquisition advantage from decayed skill
```

These can be real Resources while no current workload selects them.

Therefore current demand belongs at:

```text
Actionable Resource / Option
```

not the root Resource relation.

D remains a good **evaluation surface**, not a complete ontology.

---

# 8. C's compression: two semantic coordinates + two proof obligations

C survives the 40 discriminator set because it does **not** turn R2's six conceptual requirements into six identity fields.

## 8.1 Semantic coordinates

### Actor/System Scope

Answers:

```text
Resource for whom / which bounded system?
```

This is required by `X18`, `H02`, nested Finance/Workstation cases and Human×Agent cases.

But the scope need not be duplicated on every persisted object. If a caller is already explicitly scoped to `Finance`, that scope can be context rather than a field.

### Aspect Identity

Answers:

```text
What exact aspect of Reality are we talking about?
```

The aspect may be:

```text
object
relation
entitlement/right
capability export
information/evidence representation
capacity slice
Human availability/attention
social relationship
software component
network path
```

R3 therefore deliberately does not create a universal `resource_type` ontology.

## 8.2 Proof obligations

### Transition Witness

At least one transition family must be evidenced in which the aspect can act as a means/input/enabler.

This prevents Resource from becoming a synonym for Reality.

However the transition family is not necessarily part of **coarse Resource identity**.

Instead:

```text
Resource(actor, aspect)
= existential projection over supported transition witnesses
```

while:

```text
ResourceFor(actor, aspect, transition_family)
```

retains precision when authority, semantics or use differs by transition.

This solves `Q03` cleanly:

```text
malware bytes
→ ResourceFor(static-analysis) = supported
→ ActionableFor(execution) = false
→ coarse Resource(actor, bytes) = true
```

because at least one admissible enrollment witness exists.

### Evidence Envelope

The Resource relation is not self-authenticating.

The evidence envelope carries/refers to the native claims needed to establish:

```text
aspect identity
transition witness
bounded feasibility
admissibility/directionality
```

Evidence is **support**, not Resource identity.

This is how R3 preserves owner-native truth without making World own every fact.

---

# 9. Bounded feasibility and admissibility are predicates, not universal fields

R2 retained both as conceptual coordinates. R3 compresses them further.

They are required conditions on the **supporting evidence** for a transition witness:

```text
SupportedEnrollment
requires
  credible bounded path
  + relevant admissibility/direction
```

but not one universal:

```text
resource.acquisition_path
resource.legal_permission
```

field.

Why?

Different Resources establish feasibility differently:

```text
public paper
→ direct read access

FRED
→ bounded account/key acquisition

component with complement
→ cheap prerequisite acquisition

decayed Human skill
→ bounded refresh path

exported Workstation capability
→ native capability surface

relationship/reputation
→ social/institutional access path
```

Trying to normalize all these into one path schema would create more ontology than prediction.

Likewise admissibility may come from:

```text
provider terms
license
operator grant
contractual right
Human consent
system-owner policy
```

World should consume those claims, not own one universal permission system.

---

# 10. Candidate coordinate ledger

The complete R3 placement audit is:

| Coordinate | R3 placement | Verdict | Discriminators | Reason |
| --- | --- | --- | --- | --- |
| actor/system scope | `resource-relation-context` | **REQUIRED_SEMANTIC** | R06, R25, R26, R31 | Necessary for resource-for-whom; may be supplied by an explicitly scoped caller rather than duplicated in every record. |
| aspect identity | `resource-relation-identity` | **REQUIRED_SEMANTIC** | R01, R18, R22, R23 | Must identify the Reality aspect/relation/capability/representation being discussed; not restricted to owned objects. |
| transition witness/family | `support-witness` | **REQUIRED_PROOF_NOT_COARSE_IDENTITY** | R09, R21, R24, R29, R40 | At least one witnessed enrollment transition is necessary to avoid vacuity; coarse Resource(actor,aspect) can existentially project over it, while ResourceFor retains it when precision matters. |
| evidence/provenance envelope | `support-evidence` | **REQUIRED_PROOF_NOT_IDENTITY** | R01, R14, R18, R20, R40 | Evidence establishes the relation but should not become the Resource identity. Truth-role/provenance of the transition witness must be preserved. |
| bounded enrollment/acquisition feasibility | `support-predicate` | **REQUIRED_PROOF_NOT_FIELD** | R03, R13, R17, R33, R34, R38, R39 | Needed to separate realistic deferred resources from unreachable theoretical utility; represented by native evidence/path claims, not one universal path field. |
| admissibility/directionality | `support-predicate/native-authority` | **REQUIRED_PROOF_NOT_FIELD** | R21, R29, R30, R31 | Must be established from relevant native purpose/authority facts; not reducible to technical feasibility and not copied into a global Resource authority field. |
| owner | `claim-native-source` | **DELETE_UNIVERSAL_COORDINATE** | R20, R27, R28, R30 | Different claims can have different native owners; some resources are relational/social and have no single provider-style owner. |
| possessed consuming authority | `actionable-resource` | **DOWNSTREAM** | R02, R12, R13, R16, R21 | Current authority determines Actionability for a transition; requiring it for Resource existence collapses Resource into Actionable Resource. |
| access/transport/materialization | `actionable-resource` | **DOWNSTREAM** | R04, R15, R22, R30 | Current access is use/path scoped and not required for a deferred or reference-preserved Resource. |
| capacity/quota | `actionable-resource-or-option` | **DOWNSTREAM** | R08, R27, R37 | Capacity answers how much/how often, not whether the underlying Resource relation exists. |
| currentness/expiry | `evidence-claim-validity` | **CLAIM_LOCAL_NOT_RESOURCE_FIELD** | R04, R05, R10, R32, R34 | Owner terms, authority, transport, presence, historical evidence and option expiry have different clocks; projection is as-of evidence, not one Resource current bit. |
| cost/risk/value | `acquisition-selection-valuation` | **DOWNSTREAM** | R13, R17, R37 | Affects whether/when to acquire or select, not Resource identity. |
| dependencies/complements | `support-or-composition` | **CONTEXTUAL_NOT_UNIVERSAL** | R03, R10, R33, R34 | A prerequisite can establish bounded enrollment feasibility before actionability; other dependencies belong to Option/Capability composition. |
| failure domain | `redundancy-portfolio` | **DOWNSTREAM** | R07, R11 | Relevant to effective redundancy/resilience, not Resource existence. |
| substitutability | `redundancy-portfolio` | **DOWNSTREAM** | R07, R17 | Substitute arrival can change marginal value without changing Resource identity. |

The important compression is:

```text
Resource relation semantics:
  actor/system scope
  aspect identity

Resource relation proof:
  transition witness
  evidence envelope
    └─ bounded feasibility + admissibility/directionality

Actionable Resource joins:
  only the current facts this demand needs

Portfolio/valuation:
  failure domain
  substitutability
  cost/risk
  marginal option/capacity value
```

---

# 11. Coordinate deletion tests

| Mutation | Result | Discriminators | Why |
| --- | --- | --- | --- |
| delete actor/system scope | **FAIL** | R31, R25, R26 | Cannot distinguish resource-for-Ordivon from resource-for-adversary or different actor boundaries. |
| delete exact aspect identity | **FAIL** | R01, R18, R22 | Catalog/provider labels transfer claims across heterogeneous underlying aspects. |
| delete transition witness entirely | **FAIL** | R21, R29, R40 | Existing things, liabilities and aggregator claims become indistinguishable from enrollable Resources. |
| make transition witness part of coarse Resource identity | **REJECT_ADD** | R21, R19, R35 | One aspect fragments into many Resource identities even though transition precision is only needed for ResourceFor/Actionability. |
| delete evidence/provenance support | **FAIL** | R14, R20, R40 | Claims become self-authenticating and aggregator capability labels can mint semantic ResourceFor truth. |
| copy one universal owner into Resource relation | **REJECT_ADD** | R27, R28, R30 | Attention, relationships/rights and multi-source resources do not have one provider-style owner; ownership belongs to individual claims. |
| require current possessed authority in Resource relation | **REJECT_ADD** | R13, R16, R17 | Deferred/gated Resources disappear and Resource collapses toward Actionable Resource. |
| require current access/materialization | **REJECT_ADD** | R15, R22, R30 | Dormant/reference/rights-based Resources disappear. |
| store one Resource currentness/expiry field | **REJECT_ADD** | R04, R05, R32, R34 | Distinct supporting claims have different validity clocks and historical truth roles. |
| store failure domain/substitutability in Resource identity | **REJECT_ADD** | R07, R11 | Portfolio context changes without changing the underlying Resource relation. |
| remove bounded feasibility/admissibility from support predicate | **FAIL** | R29, R31, R34, R38 | Liabilities, hostile capabilities, expired rights and unreachable aspects can be promoted merely because a mechanism can be imagined. |

These tests give R3 a stronger answer than “keep 15 coordinates”.

## 11.1 Required semantically, but not necessarily persisted

```text
actor/system scope
aspect identity
```

## 11.2 Required as proof obligations

```text
transition witness
provenance/evidence support
bounded feasibility
admissibility/directionality
```

## 11.3 Explicitly downstream

```text
possessed consuming authority
current access/transport/materialization
capacity/quota
cost/risk/value
failure domain
substitutability
```

## 11.4 Contextual rather than universal

```text
owner
dependencies/complements
```

## 11.5 Currentness belongs to the claim

There is no surviving justification for:

```text
Resource.current = true/false
```

as one universal field.

---

# 12. Currentness: project as-of, qualify evidence independently

The current production code already gives strong supporting evidence here:

```text
OwnerVerification.is_current(...)
AuthorityEvidence.is_active(...)
TransportEvidence.is_current(...)
AcquisitionAssessment.is_current(...)
```

Each truth family has its own clock.

R3 therefore proposes the research semantics:

```text
Resource(actor, aspect, as_of)
```

is a projection supported by whatever evidence remains sufficient **for the Resource relation** at `as_of`.

`ActionableResourceFor(..., as_of)` may require additional evidence with much shorter freshness horizons.

Example:

```text
API identity / existence evidence      still valid
owner terms                            still valid
transport evidence                     stale

Resource                               supported
ActionableFor(network call now)         UNKNOWN / requires refresh
```

Historical evidence is not deleted:

```text
Resource(..., t0) supported
```

can remain historically true even if:

```text
Resource(..., t1)
```

is currently unknown or unsupported.

This does not require a global freshness service; each evidence owner retains its own validity semantics.

---

# 13. Truth ownership map

R3's strongest architectural conclusion is that **Resource is a projection across owners, not a new owner of their truths.**

| Truth | Native owner / source role | World role |
| --- | --- | --- |
| actor/system scope | consuming owner/caller | use as explicit evaluation context |
| aspect identity | provider/domain/source/native subsystem | preserve exact identity + provenance |
| transition/capability witness | provider/domain/native capability owner and/or semantic consumer evidence | compose evidence; never treat discovery label as owner truth |
| terms/license/purpose | provider/legal/operator/Human authority | consume claim |
| possessed authority | account/operator/secret/entitlement authority | consume current proof |
| transport/path/resolver | Workstation/network owner | consume current proof |
| capacity/quota | provider/Runtime/Workstation/domain owner | consume current proof when binding |
| currentness | each claim owner | evaluate per evidence type |
| domain Outcome | consuming domain | consume for learning/selection, never promote automatically |
| failure domain | owner of physical/logical substrate | consume only for the disturbance being reasoned about |

World's responsibility is the **join semantics** and the preservation of truth boundaries.

It is not a resource data warehouse.

---

# 14. Nested boundaries

C handles capability-as-resource recursion without special ontology.

## Workstation → Finance

```text
Workstation
  owns: physical routes, path members, current egress capability truth
  exports: stable semantic egress capability

Finance
  actor/system scope = Finance
  aspect = exported Workstation egress capability
  transition witness = bounded network egress family
  support = Workstation-native capability evidence
```

Finance does **not** copy:

```text
VPN node list
resolver implementation
physical route truth
member generation
```

into its Resource identity.

If Workstation replaces an underlying member while preserving the exported semantic capability, `N11` says Finance's Resource relation should remain stable.

## Runtime → domain

Same structure:

```text
Runtime contained-execution Capability
→ aspect consumed as domain Resource
```

Runtime continues to own job/execution/recovery semantics.

## Agent cognition → Game/Finance/Security

The model/API capability can be a Resource to the domain without implying that its output becomes domain Outcome truth.

## Human×Agent

`H03` is explained by actor scope:

```text
model capability may be Resource for Human×Agent joint system
```

while:

```text
same output != retained Resource/Capability of Human-alone boundary
```

No special “AI resource” ontology is required.

---

# 15. Non-object Resources

A flat asset ontology struggles with R3's non-object cases. C does not require objecthood.

## Rights and permissions

A contractual option or legal permission is itself an identifiable **institutional relation/aspect of Reality**.

It can be enrolled as an enabling relation even when target bytes are absent.

## Relationships and reputation

A trusted relationship can be an evidenced social relation that enables introductions/review.

It need not be “owned” like a file.

## Human attention/time

One hour of available attention is a bounded availability/capacity aspect. The Resource relation can exist; the exact amount needed by a workload belongs to Actionability/capacity reasoning.

## Knowledge/evidence

An exact report, negative experiment, verified claim or retained representation can be enrolled to reduce uncertainty or change selection.

Truth ownership remains with the relevant evidence/domain owner.

## Exported capability

The semantic capability surface itself is the aspect. Internal mechanism is not required at the consuming boundary.

The unifying concept is therefore not “asset”. It is:

> **identifiable aspect of Reality capable of supported enrollment for this actor/system.**

---

# 16. Dependencies are not one relation coordinate

R3 finds two very different dependency roles.

### Enrollment-feasibility dependency

`W03`, `X28`, `X30`:

```text
Resource exists because a bounded prerequisite path is evidenced,
but it is not Actionable yet.
```

The prerequisite belongs inside evidence supporting bounded enrollability.

### Composition dependency

Other dependencies matter only when constructing an Option/Capability:

```text
model + compute + credential + network
```

A universal `resource.dependencies[]` field would conflate these roles and drift toward a global dependency graph.

R3 therefore keeps dependency semantics contextual.

R5 can later study composition/catalysis formally.

---

# 17. Failure domain and substitutability move out of Resource relation

`N02` is decisive.

Two paths can both remain valid Resources while sharing one physical failure domain.

Therefore:

```text
Resource identity
≠ independent redundancy
```

Failure-domain evidence answers a later question:

```text
Against disturbance class D,
are Options A and B independently substitutable?
```

Similarly, substitutability is portfolio/demand-relative.

Adding a substitute changes marginal value without rewriting Resource identity.

This confirms the R2 rejection of Option-set identity and prevents R3 from rebuilding a global graph through the back door.

---

# 18. Fresh post-freeze tests for C

C's wording above was frozen before these eight additional tests were authored.

| ID | Fresh case | C |
| --- | --- | --- |
| R3Y01 | One API license permits personal research but forbids commercial output; the same aspect has one supported transition family and one unsupported family. | PASS `C-TRANSITION-SCOPED` |
| R3Y02 | A resource relation needs identity evidence from a provider, transport evidence from Workstation, and permission evidence from an account authority; no single system owns all support. | PASS `C-MULTI-OWNER-EVIDENCE` |
| R3Y03 | A stable Workstation egress capability changes its internal path member while preserving its exported semantic capability identity consumed by Finance. | PASS `C-NESTED-BOUNDARY` |
| R3Y04 | Identity evidence remains valid but transport evidence expires; Resource remains supportable while current Actionability becomes unknown until transport refresh. | PASS `C-CLAIM-CURRENTNESS` |
| R3Y05 | A jointly maintained open-source tool has no meaningful single owner field; repo identity, license, package provenance and local compatibility come from different authorities. | PASS `C-NO-UNIVERSAL-OWNER` |
| R3Y06 | A complement is not currently held, but owner-native evidence shows a low-cost bounded acquisition path; the component is a Resource but not yet Actionable for a composition requiring the complement. | PASS `C-DEFERRED-COMPLEMENT` |
| R3Y07 | A source aggregator claims capability X, but current owner evidence proves only identity/terms/interface and does not attest X; ResourceFor(X) is not established even if the aspect may be a Resource for another transition. | PASS `C-WITNESS-PROVENANCE` |
| R3Y08 | The same malware bytes are a ResourceFor(static-analysis) under current authority and not ActionableFor(execution); coarse Resource(actor,aspect) remains true because at least one supported transition witness exists. | PASS `C-EXISTENTIAL-PROJECTION` |

C survives all eight without wording change.

The strongest are:

- `R3Y01`: transition-specific permission requires `ResourceFor`, not fragmented object identity;
- `R3Y02`: one relation can be supported by evidence from multiple native owners;
- `R3Y04`: stale transport can invalidate Actionability without erasing Resource identity/existence evidence;
- `R3Y05`: no universal provider-style owner exists for all resources;
- `R3Y07`: capability witness provenance must be independently supported;
- `R3Y08`: coarse Resource is existential over precise supported transition relations.

This remains falsifier evidence, not universal proof.

---

# 19. Existing implementation audit: much of the architecture is already right

Current `resource_discovery.py` already avoids a monolithic Resource object.

It separates:

```text
ResourceCandidate
DiscoveryEvidence
OwnerVerification
AcquisitionAssessment
AuthorityEvidence
TransportEvidence
ConsumerDemand
ConsumptionOutcome
ResourceEvaluation
```

That separation is structurally aligned with R3:

- discovery provenance is separate from owner truth;
- required authority is separate from possessed authority;
- acquisition decision is separate from authority possession;
- transport has its own path/resolver/time;
- currentness is evidence-type-specific;
- evaluation is demand-scoped;
- outcomes do not rewrite owner/authority truth.

This is evidence that **the absence of a persisted ResourceRelation object may be a feature, not a missing abstraction.**

R3 therefore finds no justification for creating one.

---

# 20. Existing implementation falsifiers R3F01 / R3F02

R3 uncovered a concrete truth-boundary debt in the existing evaluator and reproduced it in two distinct provenance shapes.

## R3F01 — aggregator-only capability semantics

The first executed falsifier constructed:

```text
ResourceCandidate
  provenance = aggregator only
  capabilities = [claimed-x]

OwnerVerification
  proves provider identity / terms / interface
  does NOT attest claimed-x capability semantics

TransportEvidence
  current available

ConsumerDemand
  requires claimed-x
```

Current `evaluate_resource(...)` returned:

```text
decision = consumable-now
demandFit = 1.0
```

Execution client request:

```text
world-r3-capability-provenance-falsifier-20260815-02
```

So an aggregator-authored capability label can currently satisfy demand fit after unrelated owner terms/interface verification.

## R3F02 — mixed resource-level provenance still does not prove the claim

The second executed falsifier made the case harder:

```text
ResourceCandidate.provenance
  ├─ owner evidence: proves resource exists
  └─ aggregator evidence: claims capability X

ResourceCandidate.capabilities = [claimed-x]

OwnerVerification
  proves provider terms / interface
  does NOT attest claimed-x
```

Current `evaluate_resource(...)` again returned:

```text
decision = consumable-now
demandFit = 1.0
```

Execution client request:

```text
world-r3-capability-provenance-falsifier-20260815-03
```

This proves a stronger point:

> **Resource-level provenance is insufficient to establish claim-level transition semantics.**

Merely having *some* owner provenance on a `ResourceCandidate` cannot upgrade an unrelated capability claim into owner-native truth.

That violates the deeper truth boundary already stated elsewhere in World:

```text
aggregator discovery != owner-native fact
```

R3's interpretation is narrow:

> **Transition-witness provenance is not optional, and evidence support must preserve which native claim supports which transition witness.**

`ResourceCandidate.capabilities` is suitable as a discovery hint, but a specific `ResourceFor(capability/transition)` or current `consumable-now` judgment must not treat an unbound candidate label as independently verified semantic capability truth.

R3 deliberately does **not** fix production code in this round. The finding is recorded as concrete implementation debt because the current foundations constraint forbids turning research into production mutation before the relation result is frozen and scoped.

This is also evidence against creating a larger Resource schema: the bug is not “missing fields”; it is **wrong truth-role propagation across an existing join**.

---

# 21. R3 provisional relation model

The surviving research model is C.

## Coarse projection

```text
Resource(actor_scope, aspect_identity, as_of)
```

is supported iff there exists at least one transition family with sufficient evidence for a bounded admissible intentional enrollment path.

## Precise projection

```text
ResourceFor(
  actor_scope,
  aspect_identity,
  transition_family,
  as_of
)
```

is used when transition-specific authority/semantics matter.

## Support envelope

Not a universal schema. Conceptually it preserves references to claims proving:

```text
identity
transition witness
bounded feasibility
admissibility / directionality
```

Each underlying claim keeps its own owner and currentness semantics.

## Actionability

```text
ActionableResourceFor(resource_for, demand, as_of)
```

joins only the facts materially required for that demand, potentially including:

```text
current owner/purpose terms
possessed authority
access / transport / materialization
capacity / quota
semantic interface / fit
required prerequisite state
```

There is no requirement that every Resource have every one of those facts.

## Option

An Option remains a demand-scoped admissible use/composition available to selection.

This preserves:

```text
Resource != Actionable Resource != Option != Capability
```

without creating four global registries.

---

# 22. The R2 six-coordinate model after R3 compression

R2 said:

```text
Actor/System-relative
× Identifiable Reality Aspect
× Evidence
× Enrollable Direction
× Transition Mechanism
× Bounded Feasibility
```

R3 now says these are not six peers.

They compress into:

```text
RELATION SEMANTICS
├─ Actor/System Scope
└─ Aspect Identity

PROOF OBLIGATION
├─ Transition Witness
└─ Evidence Envelope
   ├─ bounded feasibility
   └─ admissible intentional direction
```

This is a meaningful reduction in ontology.

The concepts survive; the field count does not.

---

# 23. What R3 rejects

R3 adds the following rejections:

1. **No universal `ResourceRelation` tuple with owner/authority/access/capacity/currentness/cost/dependencies/failure-domain/substitutability fields.**
2. **No object-only Resource ontology.** Rights, relationships, knowledge, attention and exported capabilities are valid aspects of Reality.
3. **No owner field as a universal Resource coordinate.** Ownership/truth authority is claim-specific.
4. **No transition-less actor/aspect definition.** It becomes too broad and loses directionality.
5. **No transition family in coarse Resource identity by default.** Keep it in `ResourceFor` when precision matters.
6. **No current possessed authority/access requirement for Resource existence.** Those belong to Actionability.
7. **No Resource-wide currentness bit or expiry.** Currentness is claim/evidence-specific.
8. **No failure-domain/substitutability fields in Resource identity.** Those are portfolio relations.
9. **No universal dependency graph.** Enrollment prerequisites and composition dependencies are different relations.
10. **No production Resource registry/schema/service from R3.** The existing evidence-join architecture is closer to the surviving model than a monolithic abstraction would be.
11. **No treating candidate capability labels as semantic owner truth.** `R3F01` proves this is unsafe.

---

# 24. What R3 resolves enough for R4

R3 provisionally resolves:

### Resource relation identity

```text
actor/system scope
+
aspect identity
```

with scope potentially carried by caller context rather than copied into records.

### Resource relation establishment

Requires at least one supported transition witness with evidence for bounded admissible enrollability.

### Transition precision

Use existential coarse `Resource` and transition-specific `ResourceFor` rather than fragmenting every aspect into independent object identities.

### Truth ownership

World composes native claims; it does not become provider/legal/network/domain truth owner.

### Currentness

Evidence-specific and projection-as-of, never one universal Resource clock.

### Actionability

A separate demand-time join of only materially required current facts.

### Portfolio relations

Failure domain, substitutability, redundancy and marginal value remain downstream.

### Implementation direction

No new Resource schema is earned. One concrete evaluator provenance debt is recorded for later correction.

---

# 25. Still unresolved

R3 intentionally leaves these for later rounds:

1. **R4 lifecycle/state-space:** whether discovery/verification/acquisition/actionability states can be compressed without a universal rigid state machine.
2. **Capacity families:** stock/flow/budget/rate semantics for capital, compute, attention, quota and time.
3. **Composition:** prerequisites, catalysts, complements, substitution and bundles belong to R5.
4. **Resource creation/decay:** learning, renewal, skill decay, capital regeneration and network effects belong to R7.
5. **Evidence threshold:** R3 establishes proof roles but no universal confidence score.
6. **Transition vocabulary:** R3 does not authorize a global taxonomy of transition families/capabilities.
7. **Implementation debt R3F01:** needs a narrow owner-boundary correction plan after research boundary allows it; avoid solving it with a global capability registry.
8. **Outcome/Attribution:** remains R6.

---

# 26. R4 handoff

R4 should not start by enumerating states such as:

```text
DISCOVERED
VERIFIED
ACQUIRED
ACCESSIBLE
QUALIFIED
ACTIONABLE
...
```

Instead ask:

> Across different Resource families, which state distinctions actually change the truth or next admissible action, and which are merely evidence/workflow lanes?

R3 supplies the boundary:

```text
Candidate = epistemic hypothesis
Resource = supported actor/aspect enrollment relation
Actionable Resource = current demand-time qualification
Option = selectable use/composition
```

R4 should attack whether additional lifecycle labels are needed at all.

It must preserve:

- evidence-specific currentness;
- owner-native truth;
- no global Resource registry;
- no universal state machine unless multiple materially different Resource families require the same state semantics.

---

# 27. R3 conclusion

R3's main result is a **reduction**, not an expansion.

R2's provisional Resource definition survives, but its six conceptual coordinates do not become six stored properties.

The current best relation model is:

```text
                     native evidence claims
                    /      |       |      \
                   v       v       v       v
Actor Scope + Aspect Identity + Transition Witness
              \                    /
               \ bounded + admissible
                \ enrollment proof
                         |
                         v
                 ResourceFor(...)
                         |
                existential projection
                         v
                  Resource(...)
                         |
         demand + current native joins
                         v
               Actionable Resource
                         |
                 use/composition
                         v
                       Option
```

The crucial architectural law candidate is:

> **Resource is not a record of all facts about a thing. It is a supported relation projection across truth owners.**

That is the only R3 result strong enough to carry into R4, and it remains provisional until later dogfood/promotion.
