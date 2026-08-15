---
schema_version: 1
id: world.resource-ontology-r4-lifecycle-falsification
title: Resource Ontology R4 — Lifecycle / State-Space Falsification
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
summary: Tests whether Resource families share a universal lifecycle and reduces lifecycle language into native claims, historical events, demand projections and derived workflow rather than one Resource state machine.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-ontology-r0-census
  - world.resource-ontology-r1-theory-triangulation
  - world.resource-ontology-r2-definition-falsification
  - world.resource-ontology-r3-relation-model
  - world.resource-option-capability-model
  - world.resource-opportunity-flywheel
---
# Resource Ontology R4 — Lifecycle / State-Space Falsification

## 1. Question

Resource programs naturally produce a lifecycle vocabulary:

```text
latent / potential
→ discovered
→ verified
→ acquirable
→ acquired / held
→ accessible
→ qualified
→ actionable
→ option
→ selected / composed
→ consumed
→ retired
```

The chain is attractive because it compresses a difficult world into one arrow.

R4 asks whether the arrow is **true**.

The promotion criterion is strict:

> A lifecycle label earns root-state status only if deleting it changes truth, the next admissible action, recovery semantics, or a prediction across materially different Resource families.

A label does **not** become a state merely because it is convenient for UI, work queues, reporting or one provider flow.

R4 therefore separates five questions that a state machine tends to conflate:

```text
What happened?                         Event
What is currently claimed about Reality? Claim
What relation follows for this actor?   Resource projection
What can this demand do now?             Actionability / Option projection
What work should be done next?           Workflow / decision projection
```

No R4 result is canonical production doctrine.

---

# 2. Frozen evidence boundary

R4 begins at canonical World main `6ab6e3cfa09cb9c34f86af8b0748cc66b73bb636`.

Frozen source digests:
- `docs/resource-ontology-r0-census.md` → `sha256:572091ddafbd79e6c95d584a16b753ac96b6f94493bbf9721a690aa464b1b3a9`
- `docs/resource-ontology-r1-theory-triangulation.md` → `sha256:63bd83b0ba94fab4e74c4bea999ce43b39d131393a9964b101dea8a5727d9dc2`
- `docs/resource-ontology-r2-definition-falsification.md` → `sha256:97a3765d58a74cfdc1f6c3df8076b77f6acb867ae196391ed7c3145e6603cd11`
- `docs/resource-ontology-r3-relation-model.md` → `sha256:b5d7697736a458678b700835c379dd231d317ad62ae689c0c4b22b67af94e85a`
- `docs/resource-opportunity-flywheel.md` → `sha256:8ee436d6e3daca4e9c1643f7568debe8a76c843631b7234f9e3e94eb5f2542e5`
- `src/ordivon_world/resource_discovery.py` → `sha256:d78e7a0fa274847e83b737c06baedd8b7047a50312b92a9d6a33cbf3b4dca840`
- `tests/test_resource_discovery.py` → `sha256:7c5874c6bd9c9a2baf27c0b7e5bbd6a7858af7f99f6d6640581cec14945778a1`


R4 uses:

```text
40 frozen lifecycle discriminators
+ 8 fresh post-freeze tests
+ 6 executed non-linear lifecycle probes
+ 1 executed multi-workload projection probe
```

The 40 discriminators intentionally span provider resources, network resources, Studio tools, Game cognition, Security samples, Human attention/relationships, rights, cash, GPU, stale datasets, credentials, references and nested exported capabilities.

---

# 3. Four frozen lifecycle models

## A — Universal Linear Lifecycle

> Each Resource has one current lifecycle state that advances through a common ordered chain: LATENT/POTENTIAL -> DISCOVERED -> VERIFIED -> ACQUIRABLE -> HELD/ACQUIRED -> ACCESSIBLE -> QUALIFIED -> ACTIONABLE -> OPTION -> SELECTED/COMPOSED -> CONSUMED -> RETIRED. Regressions are exceptional lifecycle transitions and one state should summarize the current Resource.

A is the ordinary maturity-pipeline model.

Its strongest claim is not merely that these words are useful; it claims a Resource can be summarized by **one position on one ordered path**.

## B — Orthogonal Universal State Vector

> Each Resource has one current universal multidimensional state vector with coordinates for epistemic status, possession/authority, access, capacity, qualification/actionability, selection/consumption and freshness. There is no required linear order, but every Resource is represented by the same coordinate family.

B drops ordering and allows independent coordinates.

It is a major improvement over A but still claims all Resource families should share one universal current state vector.

## C — Milestone / Event Ledger

> Resource lifecycle is represented as an append-only set of milestones/events such as discovered, verified, acquired, accessed, qualified, selected, consumed, expired or retired. Current state is reconstructed from milestone history plus invalidations; milestones are generic across Resource families.

C recognizes history and non-monotonicity. It retains generic events/milestones and reconstructs current state.

Its risk is subtler: generic milestones such as `verified`, `accessed`, `qualified`, and `consumed` can still hide **which claim, transition, actor or demand** they apply to.

## D — Claim / Event Projection Model

> There is no universal Resource lifecycle state. Keep native events and claim-specific evidence with their own owners and time semantics; derive Candidate, Resource, ActionableResourceFor and Option as projections for actor/demand/as_of, and derive workflow queues from the next missing or decision-relevant evidence. Acquisition, access, selection, consumption, revocation and expiry are events/relations/claim changes, not steps in one Resource state machine.

D makes the strongest reduction: no universal Resource lifecycle state exists.

It keeps root truth structures narrow and projects the rest.

---

# 4. Frozen model results

| Model | Result across 40 lifecycle discriminators |
| --- | --- |
| A — Universal Linear Lifecycle | 0 PASS / 37 FAIL / 3 AMBIG |
| B — Orthogonal Universal State Vector | 15 PASS / 20 FAIL / 5 AMBIG |
| C — Milestone / Event Ledger | 23 PASS / 12 FAIL / 5 AMBIG |
| D — Claim / Event Projection Model | 40 PASS / 0 FAIL / 0 AMBIG |

The result is not a vote. The failure topology matters.

## 4.1 Complete 40-case matrix

| ID | Source | Pressure | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| L01 | `W01` Aggregator discovery does not establish owner truth | discovered vs verified | FAIL `A-ORDER` | AMBIG `B-OVERLOAD` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L02 | `W02` Required authority and possessed authority are separate | verification vs holding | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L03 | `W03` Parent entitlement may be acquired before child claim | dependency branch ordering | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L04 | `W05` Signup transport can fail while acquisition remains positive-EV | access before/after acquisition is path-specific | FAIL `A-ORDER` | PASS `B-ORTHO` | AMBIG `C-MILESTONE-AMBIG` | PASS `D-PROJECT` |
| L05 | `W07` Historical admission remains true after current presence disappears | history vs current state | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L06 | `W08` Exported capability becomes higher-layer Resource without repeating lower lifecycle | nested boundary lifecycle reset | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L07 | `N01` Hundreds of discovered transport variants are not current options | discovery vs qualification | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L08 | `N04` Client installed/executable while shared capacity absent | held/tool-present vs capacity | FAIL `A-ORDER` | PASS `B-ORTHO` | AMBIG `C-MILESTONE-AMBIG` | PASS `D-PROJECT` |
| L09 | `N09` Historical child AVAILABLE while current projection becomes UNKNOWN | non-monotonic current projection | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L10 | `N11` Stable consumer Resource survives replacement of physical members | mechanism events below identity | AMBIG `A-FORCE` | AMBIG `B-OVERLOAD` | AMBIG `C-MILESTONE-AMBIG` | PASS `D-PROJECT` |
| L11 | `N12` Installed capability exists but is intentionally excluded from ambient authority | possession vs actionability | FAIL `A-ORDER` | PASS `B-ORTHO` | AMBIG `C-MILESTONE-AMBIG` | PASS `D-PROJECT` |
| L12 | `F02` FRED Resource before current API-key authority | Resource before held authority | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L13 | `F03` Bytes acquired before research-grade evidence exists | acquired before verified-for-purpose | FAIL `A-ORDER` | AMBIG `B-OVERLOAD` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L14 | `S02` OBS retained while listener is default-off | held but not currently accessible/actionable | FAIL `A-ORDER` | PASS `B-ORTHO` | AMBIG `C-MILESTONE-AMBIG` | PASS `D-PROJECT` |
| L15 | `S05` Figma configured before OAuth consent | configured/installed before authority | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L16 | `S06` TouchDesigner Resource/option before license acquisition | pre-demand/pre-authority resource | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L17 | `G01` Catalog discovered before exact asset license identity verified | discovery granularity refinement | FAIL `A-ORDER` | AMBIG `B-OVERLOAD` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L18 | `G03` Live model consumed but player Outcome still unproven | consumption before outcome proof | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L19 | `Q03` Same bytes actionable for static analysis but not execution | simultaneous transition-specific actionability | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L20 | `Q04` Reference retained while local bytes absent | option without possession/materialization | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L21 | `Q05` libvirt available but deliberately deferred | accessible/available without selection | AMBIG `A-FORCE` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L22 | `H03` Joint Human×Agent capability does not become retained Human-alone capability | actor-boundary projection | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L23 | `H04` Human attention is a flow/capacity resource, not acquired once | flow resource | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L24 | `X02` Credential expired; renewal path is separate | expiry of one aspect, resource family persists | FAIL `A-ORDER` | AMBIG `B-OVERLOAD` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L25 | `X05` Idle GPU remains Resource with no current workload | Resource without qualification | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L26 | `X08` Relationship/reputation enables review without object possession | non-object resource | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L27 | `X12` Legal permission exists while target bytes absent | right before access/materialization | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L28 | `X13` Contractual option/right exists unexercised | Option-like resource before use | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L29 | `X19` Idle cash reserve remains Resource until selected/consumed | rival stock, optionality | AMBIG `A-FORCE` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L30 | `X24` Stale dataset valid historically but invalid for current-state claim | use-specific freshness | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L31 | `X27` Decayed skill retains bounded reacquisition advantage | decay/renewal not simple retirement | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L32 | `X28` Component useful with cheaply acquirable complement not yet held | resource before complete bundle | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L33 | `R4P01` Anonymous public Resource reaches consumable-now without AuthorityEvidence/acquisition | no universal held stage | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L34 | `R4P02` Same Resource same time consumable-now for demand X and not-fit for demand Y | qualification is demand projection | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L35 | `R4P03` Same Resource same time consumable for research and blocked-by-terms for commercial | rejected is not terminal | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L36 | `R4P04` Historical ConsumptionOutcome remains true after owner evidence stales and decision regresses | consumed not terminal; history/current split | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L37 | `R4P05` Authority remains active while transport toggles unavailable to available | held/access orthogonality | FAIL `A-ORDER` | PASS `B-ORTHO` | PASS `C-HISTORY` | PASS `D-PROJECT` |
| L38 | `R4P06` Same facts map to acquire-now or defer-acquisition when only demand threshold changes | workflow lane not resource state | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L39 | `R3F02` Mixed resource-level provenance cannot prove one capability claim | verification is claim-level | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |
| L40 | `R3Y04` Identity support remains current while transport support expires | multiple independent clocks | FAIL `A-ORDER` | FAIL `B-UNIVERSAL` | FAIL `C-PROJECTION` | PASS `D-PROJECT` |

---

# 5. A fails at the first premise: there is no universal order

A produces no clean PASS across the 40 discriminators.

The problem is not that a few Resources move backward. The problem is that several proposed stages are **not even the same kind of thing**.

## 5.1 Public resources can skip acquisition/holding entirely

Executed probe `R4P01` showed an anonymous public Resource becoming:

```text
consumable-now
```

with no `AuthorityEvidence` and no acquisition episode.

For such a Resource:

```text
VERIFIED → ACQUIRED/HELD → ACCESSIBLE
```

is not the path.

The `held` stage is absent because nothing resource-specific must be possessed.

## 5.2 Bytes can be acquired before they are verified for a research purpose

`F03` directly reverses a common ordering assumption:

```text
bytes acquired
→ later provenance / point-in-time / semantic quality established
```

So:

```text
VERIFIED before ACQUIRED
```

is not universal either.

## 5.3 Rights can exist before target materialization

`X12` and `X13` show:

```text
legal permission / contractual option
```

can be real Resources while target bytes are absent and the right is unexercised.

## 5.4 Flow resources are not acquired once

Human attention/time and provider quota are rate/capacity relations. They are available, consumed and renewed continuously.

A one-way maturity chain does not model them.

## 5.5 Nested capabilities enter a new actor boundary at a different semantic level

A Workstation capability can become a Finance Resource without Finance replaying the physical discovery/acquisition lifecycle underneath.

A universal chain leaks lower-owner mechanics across the semantic boundary.

The conclusion is stronger than “allow regression”:

> **There is no single order to regress along.**

---

# 6. B improves ordering but still over-unifies state

B replaces the arrow with a vector, for example:

```text
ResourceState = {{
  epistemic,
  held,
  access,
  capacity,
  qualification,
  freshness,
  consumption
}}
```

This correctly allows authority and transport to vary independently.

Executed `R4P05` confirms why that orthogonality matters:

```text
authority = active
transport = unavailable
        ↓
transport later available

authority remains active throughout
```

But B still fails as a **universal Resource state**.

## 6.1 Not every family has the same coordinates

What does `held` mean for:

```text
public paper
relationship / reputation
legal permission
Human attention
remote reference
exported capability
```

Forcing one value such as `N/A` does not add semantics; it only preserves a schema.

## 6.2 Qualification and Actionability are not properties of the Resource alone

Executed `R4P02` showed the same Resource at the same `as_of`:

```text
Demand X → consumable-now
Demand Y → not-fit
```

Executed `R4P03` showed:

```text
research   → consumable-now
commercial → blocked-by-terms
```

A Resource cannot have one current `qualification` or `actionable` vector coordinate that truthfully summarizes both.

The coordinate must include:

```text
actor / transition / demand / as_of
```

At that point it is no longer a Resource state. It is a **projection**.

## 6.3 One freshness coordinate is impossible

R3 already established independent clocks for identity, terms, authority, transport, capacity and historical evidence.

`R3Y04` makes the contradiction explicit:

```text
identity support = current
transport support = stale
```

No single `freshness` coordinate can represent that without hiding the claim being qualified.

## 6.4 Event history cannot be reduced to current vector state

A consumed Resource can later become non-actionable, while the consumption remains a historically true episode.

B can record a current flag, but it cannot make historical finality and current operability the same coordinate.

So B is useful as a **workload-specific projection design**, not as a universal Resource root state.

---

# 7. C preserves history but generic milestones are still too coarse

C correctly recognizes that events such as:

```text
discovered
acquired
selected
consumed
revoked
```

should not be overwritten when current conditions change.

This is why it handles `W07`, `N09`, `X02`, and `R4P04` much better than A/B.

However a generic milestone ledger still fails in four places.

## 7.1 `verified` is not one milestone

`R3F02` showed a ResourceCandidate with real owner provenance where the owner did **not** attest capability X, while an aggregator did.

A generic event:

```text
RESOURCE_VERIFIED
```

would be dangerously ambiguous.

We need propositions such as:

```text
claim(identity) verified by owner A
claim(terms) verified by owner A
claim(transition capability X) not owner-verified
```

So verification belongs to the claim, not the Resource lifecycle.

## 7.2 `qualified` cannot be one milestone

`R4P02/P03` show simultaneous incompatible qualification results for different demands.

An append-only `QUALIFIED` milestone answers the wrong question.

## 7.3 `consumed` is an episode, not a Resource terminal marker

A research paper, model API, software tool, relationship or network path can be consumed many times.

Even rival resources such as cash require amount/balance semantics rather than one terminal `CONSUMED` label.

## 7.4 Generic milestones lose actor-boundary recursion

A lower-level capability may be internally acquired/composed/operated for years before being exposed as a new semantic aspect to a higher-level actor.

The higher-level Resource relation should not inherit every lower-level milestone as its own lifecycle.

Thus C's durable-history instinct survives, but the generic Resource milestone vocabulary does not.

---

# 8. D survives by refusing to create lifecycle state

D's central move is to separate four structures.

## 8.1 Event

An Event says **something happened**.

Examples:

```text
observed catalog entry
credential issued
license accepted
authority revoked
artifact downloaded
transport probe completed
option selected
API call executed
consumption outcome observed
```

Events are historical facts when admitted by their native owners.

They do not automatically state what is true now.

## 8.2 Claim

A Claim says **a proposition about Reality is supported under a truth role**.

Conceptually:

```text
Claim(
  subject/aspect,
  predicate,
  evidence,
  native owner,
  observed/effective time,
  validity/currentness semantics
)
```

This is a reasoning structure, not an R4 production schema proposal.

Examples:

```text
provider X requires free-key
credential K is active
path P is reachable through resolver R
quota Q has 100 units remaining
asset A has CC0 license
model M supports transition family T
```

Claims can expire independently.

## 8.3 Projection

A Projection asks what follows from current claims **for a context**.

R3's surviving forms remain:

```text
Resource(actor, aspect, as_of)
ResourceFor(actor, aspect, transition, as_of)
ActionableResourceFor(actor, aspect, transition, demand, as_of)
Option(...)
```

These should generally be recomputed from native evidence rather than persisted as a global state machine.

## 8.4 Workflow / Decision projection

A workflow lane answers:

```text
What should be checked or done next?
```

Examples in current World:

```text
owner-verification-required
acquisition-verification-required
acquire-now
human-action-required
prerequisite-acquisition-required
defer-acquisition
transport-verification-required
consumable-now
```

These are useful, but they are derived from:

```text
current evidence
+ demand
+ thresholds/policy
+ verification budget
```

They are not Reality state.

---

# 9. Executed non-linear probes

R4 executed six probes against the current production evaluator under client request:

```text
world-r4-nonlinear-lifecycle-probes-20260815-01
```

All six passed as falsifiers of a linear lifecycle.

1. anonymous consumable-now without AuthorityEvidence/acquisition.
2. same resource simultaneous consumable-now and not-fit across demands.
3. same resource simultaneous consumable and blocked-by-terms across purposes.
4. historical ConsumptionOutcome survives current owner-verification regression.
5. authority remains active while transport toggles unavailable/available.
6. same candidate/owner/acquisition facts yield acquire-now or defer-acquisition solely from demand threshold.


A seventh executed probe, `world-r4-multi-workload-queue-probe-20260815-01`, held native facts constant and changed only the workload:

```text
workload A → consumable-now
workload B → not-fit
workload C → blocked-by-terms
```

This confirms that board lanes/decisions are workload projections, not Resource lifecycle states.

---

# 10. Complete lifecycle-label type audit

| Label | Classification | Plane | Verdict | Discriminators | Reason |
| --- | --- | --- | --- | --- | --- |
| `latent/potential` | DELETE_ROOT_STATE | `research-language / bounded-feasibility predicate` | **REJECT_UNIVERSAL_STATE** | L12, L16, L25, L32 | R2 already folds credible future potential into Resource; undiscovered potential is not an operationally knowable state and a separate Potential Resource state duplicates semantics. |
| `discovered` | EVENT_PLUS_EPISTEMIC_CONDITION | `observation/history` | **NOT_RESOURCE_STATE** | L01, L07, L17 | Discovery is an observation event about a Candidate claim; it does not move Reality or prove owner/transition truth. |
| `verified` | CLAIM_LOCAL_EVIDENCE_STATUS | `epistemic/owner-native claim` | **NOT_RESOURCE_STATE** | L01, L13, L17, L39, L40 | Different claims are verified independently; resource-level verification cannot summarize identity, terms, transition semantics, transport and capacity. |
| `acquirable` | RELATION_PREDICATE | `bounded enrollment/acquisition support` | **NOT_RESOURCE_STATE** | L03, L12, L16, L32 | Acquirability is a current relation/path claim and may exist before or after other dimensions; it is not a possession milestone. |
| `acquired` | EVENT | `history/effect` | **NOT_UNIVERSAL_STATE** | L03, L13, L15, L27 | Acquisition is a historical effect for some families; public, social, flow and exported-capability resources need no acquisition event. |
| `held/possessed` | RELATION_OR_STOCK_FACT | `authority/material possession/capital depending family` | **NOT_UNIVERSAL_STATE** | L11, L20, L23, L26, L27, L33, L37 | What is held differs by family; anonymous/public, relationships, rights, flow resources and remote references break one universal possession coordinate. |
| `accessible` | PATH_OR_INTERFACE_RELATION | `current access/transport/materialization` | **NOT_RESOURCE_STATE** | L04, L14, L20, L27, L37, L40 | Access is path/interface/time scoped, can toggle independently of authority, and may be unnecessary for reference/rights resources. |
| `qualified` | DEMAND_SCOPED_PROJECTION | `consumer demand` | **NOT_RESOURCE_STATE** | L07, L19, L34, L35 | The same Resource can be qualified for one demand/transition and not another at the same time. |
| `actionable` | DEMAND_TIME_PROJECTION | `consumer demand + current native joins` | **DERIVED_PROJECTION** | L11, L19, L34, L35, L37, L40 | Actionability is meaningful but belongs to ActionableResourceFor(actor,aspect,transition,demand,as_of), not a global lifecycle state. |
| `option` | DEMAND_SCOPED_SELECTABLE_RELATION | `selection/composition` | **DERIVED_PROJECTION** | L20, L21, L28, L29 | Option is a current selectable use/composition and may itself be represented by a right Resource; it is not a later maturity stage of every Resource. |
| `selected` | DECISION_EVENT | `decision/history` | **NOT_RESOURCE_STATE** | L21, L29, L38 | Selection is an episode by an actor under a demand; reusable resources remain resources after or before selection. |
| `composed` | COMPOSITION_RELATION_OR_EVENT | `Option/Capability construction` | **NOT_RESOURCE_STATE** | L03, L10, L32 | Composition concerns a bundle/transition, not one component Resource lifecycle; a component can participate in many compositions. |
| `consumed` | CONSUMPTION_EPISODE | `history/effect/outcome evidence` | **NOT_TERMINAL_STATE** | L18, L29, L36 | Consumption can repeat, may deplete or not, and historical consumption remains true when current Actionability regresses. |
| `expired/stale/revoked` | CLAIM_OR_RELATION_INVALIDATION | `claim-local time/authority` | **NOT_UNIVERSAL_STATE** | L09, L24, L30, L40 | Different claims/aspects expire independently; stale transport does not imply stale identity, and expired credential may leave account/renewal Resources. |
| `retired` | OWNER_DECISION_OR_DEPENDENCY_OUTCOME | `maintenance/selection policy` | **NOT_UNIVERSAL_TERMINAL_STATE** | L10, L11, L21, L31 | Retirement is a policy/dependency decision and can apply to one mechanism while a higher-level Resource remains; decay may be reversible. |

The 15 labels do not disappear. They are **relocated to the structure they actually describe**.

---

# 11. Label-by-label compression

## 11.1 `latent / potential` — delete as a root state

R2 already solved this.

A credible bounded future path is part of the Resource relation support. Creating:

```text
PotentialResource
```

adds a noun without adding a distinct truth boundary.

An undiscovered possible resource is also not an operational state known to Ordivon.

So `latent/potential` survives only as research language about bounded feasibility.

## 11.2 `discovered` — Event + epistemic condition

Discovery means:

```text
Ordivon observed a claim/candidate at time t
```

It changes Ordivon's knowledge, not necessarily external Reality.

A relationship may have existed for years before Ordivon discovers it. A catalog listing may be false.

Therefore:

```text
discovered != Resource state
```

## 11.3 `verified` — claim-local evidence status

There is no safe global:

```text
resource.verified = true
```

because these can differ simultaneously:

```text
identity verified
terms verified
license stale
capability unverified
transport current
quota unknown
```

R3F01/F02 make this a concrete implementation boundary, not abstract philosophy.

## 11.4 `acquirable` — relation predicate

Acquirability answers whether a bounded admissible acquisition/enrollment path exists now.

It is one possible support relation, not a stage all Resources must enter.

## 11.5 `acquired` — historical Event when acquisition exists

Credential issuance, download, purchase, account enrollment and license acquisition are real effects/events.

But public resources, social resources and higher-owner exported capabilities need no corresponding acquisition episode.

## 11.6 `held / possessed` — family-specific relation or stock fact

What is possessed can mean:

```text
bytes
credential authority
account right
capital balance
hardware
license entitlement
```

This is useful where native owners expose it, but not a universal lifecycle coordinate.

## 11.7 `accessible` — path/interface relation

Access is typically:

```text
(aspect, path/interface, actor, time)
```

and can toggle independently from Resource identity and authority.

It belongs in current Actionability joins where needed.

## 11.8 `qualified` — demand projection

Qualification has no meaning without a criterion/demand.

The same Resource can be qualified and unqualified at the same instant for different workloads.

## 11.9 `actionable` — preserve, but as a derived projection

`Actionable Resource` remains valuable vocabulary because it marks the boundary where **current conditions sufficient for a target demand** have been established.

But its precise semantics are:

```text
ActionableResourceFor(... demand, transition, as_of)
```

not:

```text
resource.state = ACTIONABLE
```

## 11.10 `option` — preserve as a selectable relation

Option remains a demand-scoped admissible use/composition available to selection.

It is not a maturity stage of every Resource.

An option/right can itself also be a Resource aspect at another level, exactly as R2 established.

## 11.11 `selected` — Decision Event

Selection is an actor choosing an Option in one decision episode.

It does not alter the persistent ontology of a reusable component Resource.

## 11.12 `composed` — composition relation / event

Composition belongs to bundles/Options/Capabilities.

A model, credential, network path or tool can participate in many simultaneous compositions.

R5 will study the algebra of those compositions; R4 rejects `COMPOSED` as a component lifecycle state.

## 11.13 `consumed` — consumption episode, not terminal state

Consumption may be:

```text
non-rival        paper read / software call
renewable        quota resets / Human attention recovers
partially rival  compute time / API quota
rival            cash spent
```

So `consumed` alone cannot say what remains.

What matters later is family-specific stock/flow/capacity accounting plus historical outcome evidence.

## 11.14 `expired / stale / revoked` — claim/relation invalidation

An expired credential can coexist with:

```text
active account Resource
renewal capability
historical credential evidence
```

A stale transport claim can coexist with current provider identity evidence.

Therefore invalidation attaches to the claim/relation/aspect that actually expired.

## 11.15 `retired` — policy/owner decision, not universal terminal Reality state

Retiring one implementation can leave a higher-level semantic Resource intact.

A decayed skill can be refreshed.

A deferred tool can later become valuable.

So retirement belongs to maintenance/selection/dependency policy unless a native owner explicitly destroys/revokes an underlying aspect.

---

# 12. Deletion and rejected-addition tests

| Mutation | Result | Discriminators | Why |
| --- | --- | --- | --- |
| add one global current lifecycle state | **REJECT_ADD** | L34, L35, L37, L40 | Concurrent demand/transition/access truths require multiple simultaneous projections; one state discards information. |
| require monotonic forward progression | **REJECT_ADD** | L09, L24, L36, L37 | Current projections can regress/toggle while historical truth remains final. |
| make discovered a Resource state | **REJECT_ADD** | L01, L07, L17 | Discovery is epistemic observation and can precede false/rejected Candidate claims. |
| make verified a Resource-wide state | **REJECT_ADD** | L13, L39, L40 | Verification is claim-local; different claims can be verified/stale concurrently. |
| make held/acquired a universal prerequisite | **REJECT_ADD** | L20, L26, L27, L33 | Anonymous, reference, social and rights-based Resources need no universal possession step. |
| make accessible a universal prerequisite for Resource | **REJECT_ADD** | L14, L20, L27 | Dormant/reference/rights Resources remain Resources without current material access. |
| make qualified/actionable global Resource state | **REJECT_ADD** | L19, L34, L35 | Qualification/actionability can differ simultaneously by demand/transition. |
| make consumed terminal | **REJECT_ADD** | L18, L29, L36 | Consumption is repeatable/non-rival for many families and historical consumption coexists with later non-actionability. |
| delete claim-local timestamps/currentness | **FAIL** | L09, L24, L30, L40 | Cannot distinguish historical truth from current validity or independently stale owner/transport/authority claims. |
| delete event/history plane | **FAIL** | L05, L18, L36 | Historical acquisition/consumption/admission must remain true after current projections change. |
| delete demand/transition context from Actionability | **FAIL** | L19, L34, L35 | Same Resource simultaneously has incompatible actionability judgments across demands/transitions. |
| persist workflow queue as Resource state | **REJECT_ADD** | L38, L01, L04 | Queue placement is derived from current missing evidence, demand policy and verification budget; it can change without Reality changing. |

The tests give R4 a minimal root structure.

Five things are especially important:

```text
claim-local time/currentness
historical event plane
demand/transition context for Actionability
actor/aspect relation semantics from R3
native truth ownership
```

None requires a Resource lifecycle enum.

---

# 13. Historical truth and current truth are different planes

Executed `R4P04` is the cleanest demonstration.

At `t0`:

```text
Resource is consumable-now
ConsumptionOutcome(useful=true) exists
```

At `t1`, owner evidence becomes stale:

```text
current decision = owner-verification-required
```

but:

```text
historical ConsumptionOutcome remains true
```

A state-machine rewrite such as:

```text
CONSUMED → UNVERIFIED
```

is semantically misleading because it sounds like the historical consumption was undone.

The correct representation is orthogonal:

```text
Event history:
  consumption at t0 = final historical fact

Current claims:
  owner terms at t1 = stale / require refresh

Current projection:
  ActionableResourceFor(..., t1) = unknown/not established
```

This same law already appears elsewhere in Ordivon around receipts, effects and current presence. R4 shows it generalizes to Resource reasoning.

---

# 14. Current state is not useless; it is just scoped

R4 does **not** argue that state is an illusion.

It argues against **one global Resource state**.

Owner-native systems can and should expose states where the ontology is real:

```text
credential.status = active / expired / revoked
transport.status = available / unavailable / unknown
provider offer eligibility = eligible / ineligible / unknown
Runtime Job Attempt = running / succeeded / failed / ...
```

These are legitimate because each has:

```text
one owner
one subject
one state machine semantics
one reconciliation boundary
```

World's mistake would be to lift all of them into:

```text
Resource.state
```

The foundation principle is therefore:

> **State machines belong where one owner can define and reconcile the state transition semantics. Cross-owner Resource reasoning should project over those states, not invent another owner above them.**

---

# 15. Workflow queues are especially dangerous to reify

Current `ResourceOpportunityBoard` exposes excellent operational lanes:

```text
ownerVerificationQueue
acquisitionVerificationQueue
acquireNowQueue
humanActionQueue
dependentAcquisitionQueue
transportVerificationQueue
consumptionQueue
feedbackQueue
deferredAcquisition
rejected
```

These are useful precisely because they answer:

```text
what next?
```

But `R4P06` proves they are not lifecycle truth.

With identical Candidate, OwnerVerification and AcquisitionAssessment facts, only changing the demand threshold produced:

```text
acquire-now
↔
defer-acquisition
```

So queue placement depends on policy/demand, not only Reality.

Likewise verification budget can determine which missing fact is investigated first without changing the Resource.

Therefore:

> **Workflow is a projection from truth + policy; never make workflow lanes ontological states.**

---

# 16. Candidate is also not lifecycle state

R2 already established:

```text
ResourceCandidate = epistemic hypothesis
```

R4 strengthens the consequence.

Candidate is not:

```text
STATE_0 before Resource
```

because a Reality aspect may already be a genuine Resource relation before Ordivon discovers it.

The Candidate exists in Ordivon's **epistemic plane**:

```text
observation
→ hypothesis
→ evidence strengthened / rejected / refined
```

while the external relation has its own Reality/history.

This separation prevents Ordivon's knowledge acquisition process from being confused with the lifecycle of the external thing.

---

# 17. R4 root decomposition

After stripping the lifecycle language, the minimal conceptual stack is:

```text
REALITY
  │
  ├─ external aspects / relations / capacities / rights / capabilities
  │
  ▼
NATIVE EVENTS + NATIVE CLAIMS
  │        │
  │        ├─ provenance / truth role
  │        ├─ subject/aspect
  │        ├─ predicate
  │        └─ time/currentness semantics
  │
  ▼
RESOURCE PROJECTION
  Resource(actor, aspect, as_of)
  ResourceFor(actor, aspect, transition, as_of)
  │
  ▼
DEMAND PROJECTION
  ActionableResourceFor(... demand, as_of)
  Option(...)
  │
  ▼
DECISION / WORKFLOW
  select / acquire / verify / defer / consume / compose
  │
  ▼
NEW EVENTS + CLAIMS
```

This is a loop, not a lifecycle line.

The system can revisit the same projection repeatedly with new evidence without rewriting history.

---

# 18. Three basic semantic primitives

R4 suggests an even stronger compression for later foundations work.

## Primitive 1 — Event

```text
Something happened.
```

Examples: observation, acquisition, revocation, transfer, use, consumption, renewal.

## Primitive 2 — Claim

```text
A native authority/evidence source supports proposition P under time/truth-role semantics.
```

Examples: permission, availability, capacity, transition support, ownership, identity.

## Primitive 3 — Projection

```text
Given a bounded context and relevant Claims/Events, proposition Q follows now.
```

Examples: Resource, Actionable Resource, Option, workflow lane.

`Resource` itself is therefore not forced to be a fourth durable object. It can remain a semantically important **projection predicate**.

This is consistent with R3's conclusion that the absence of a persisted `ResourceRelation` may be a feature.

---

# 19. Why not persist one universal orthogonal vector anyway?

A universal vector can appear harmless:

```text
{{
  discovered: true,
  verified: partial,
  authority: none,
  access: available,
  capacity: unknown,
  actionability: false
}}
```

But R4 rejects this as root ontology for three reasons.

### 19.1 `N/A` proliferation signals false universality

Rights, public resources, relationships and exported capabilities do not naturally populate the same coordinates.

### 19.2 Each coordinate already has a native owner

Duplicating them into World creates stale-copy/reconciliation problems.

### 19.3 Demand-scoped coordinates cannot have one value

Actionability/qualification can be simultaneously true and false under different demands.

The right approach is **selective projection**: join only the coordinates required for the question being asked.

---

# 20. Fresh post-freeze tests

D's wording was frozen before the following eight cases were authored.

| ID | Fresh case | D |
| --- | --- | --- |
| R4Y01 | A public web page is discovered and directly readable before any explicit acquisition event; later its server is temporarily unreachable while a cached exact copy remains available for another transition. | PASS `D-MULTI-ASPECT-PROJECTION` |
| R4Y02 | A license is revoked while previously downloaded open-compatible artifacts remain locally usable under a separate surviving license claim; one claim invalidates without collapsing all aspect history. | PASS `D-CLAIM-LOCAL-INVALIDATION` |
| R4Y03 | One dataset is simultaneously ActionableFor(historical-analysis) and non-ActionableFor(current-state-estimation) because freshness requirements differ. | PASS `D-CONCURRENT-ACTIONABILITY` |
| R4Y04 | A consumable API is used successfully, then quota becomes zero, then quota resets next month without any new Resource discovery or acquisition. | PASS `D-CAPACITY-TIME` |
| R4Y05 | A Human relationship exists before any Ordivon discovery event and becomes known later; discovery changes epistemic state, not the relationship in Reality. | PASS `D-EPISTEMIC-REALITY-SPLIT` |
| R4Y06 | A model capability is selected into two simultaneous compositions, one succeeds and one fails; the component Resource cannot have one selected/composed/consumed state summarizing both episodes. | PASS `D-MULTI-EPISODE` |
| R4Y07 | A credential object expires but an automated renewal capability immediately produces a new credential; credential-instance history changes while account-level Resource continuity remains. | PASS `D-NESTED-ASPECT-LIFECYCLE` |
| R4Y08 | The same resource is in feedbackQueue for workload A, consumptionQueue for workload B, and rejected for workload C at the same as_of because queues are workload projections. | PASS `D-QUEUE-PROJECTION` |

D survives all eight without wording change.

The strongest new pressures are:

- `R4Y03`: simultaneous Actionability for historical analysis and non-Actionability for current estimation;
- `R4Y04`: quota capacity cycles after prior successful consumption without rediscovery/acquisition;
- `R4Y05`: a relationship exists in Reality before discovery changes Ordivon's epistemic state;
- `R4Y06`: one component participates in simultaneous compositions with different outcomes;
- `R4Y07`: credential-instance expiry/renewal beneath stable account-level Resource continuity;
- `R4Y08`: queue membership can differ by workload at one `as_of`.

This remains falsifier evidence, not universal proof.

---

# 21. What survives from the old lifecycle words

R4 does not delete useful language. It reassigns responsibility:

```text
Candidate        epistemic role
Resource         actor/aspect relation projection
Actionable       demand-time projection
Option           selectable relation

Discovered       Event / epistemic history
Verified         claim-local evidence status
Acquired         Event
Held             native possession/authority/stock claim
Accessible       native path/interface claim
Selected         Decision Event
Composed         composition relation/event
Consumed         consumption episode
Expired/Stale    claim-specific invalidation
Retired          owner/policy decision
```

This is much closer to the actual structure of the world than a maturity ladder.

---

# 22. Implication for current production code

Current `resource_discovery.py` is again structurally closer to the R4 survivor than a proposed new abstraction would be.

It already has:

```text
separate evidence classes
per-evidence currentness
one demand-scoped evaluator
derived decision classes
derived opportunity-board queues
separate ConsumptionOutcome history
```

The important existing debt remains R3F01/F02: claim-level transition provenance is insufficiently bound.

R4 finds **no new reason to create a Resource lifecycle enum** while fixing that debt.

A future narrow correction should strengthen the claim/evidence join, not add lifecycle state.

---

# 23. R4 provisional lifecycle result

The surviving model is D:

> **A Resource does not have one universal lifecycle state. Resource reasoning emerges from native Events and claim-specific evidence; Resource/Actionability/Option and workflow lanes are contextual projections over that evidence.**

The strongest concise law candidate is:

> **Persist native truth and historical effects; recompute cross-owner Resource state.**

More precisely:

```text
persist/reconcile where one owner owns the state machine
project where multiple owners' truths must be joined for a question
```

That principle is broader than Resource ontology and aligns with Ordivon's existing owner-first architecture.

---

# 24. What R4 rejects

1. No universal ordered Resource lifecycle.
2. No global Resource lifecycle enum with regression edges.
3. No universal orthogonal Resource state vector merely to avoid ordering.
4. No generic `RESOURCE_VERIFIED` truth; verification is claim-specific.
5. No universal acquisition/holding prerequisite.
6. No `ACCESSIBLE` root state; access is path/interface/time scoped.
7. No global `QUALIFIED` or `ACTIONABLE` state; these are demand/transition projections.
8. No `CONSUMED` terminal state.
9. No Resource-wide `EXPIRED/STALE` state.
10. No generic milestone ledger as the authority for current Resource truth.
11. No workflow queue reification into lifecycle state.
12. No Candidate-as-state-0 interpretation.
13. No lifecycle progress score.
14. No production Resource lifecycle service/schema/registry from R4.

---

# 25. What R4 resolves enough to enter R5

R4 closes the lifecycle question provisionally:

### Root history primitive

Events preserve admitted occurrences.

### Root epistemic primitive

Claims preserve proposition-specific owner/provenance/time semantics.

### Cross-owner semantics

Resource, ResourceFor, ActionableResourceFor and Option are projections.

### Workflow

Queues/decisions are policy- and demand-scoped projections over missing/current evidence.

### Currentness

Lives on claims/relations owned by the relevant system, not on Resource as a whole.

### State machines

Remain legitimate at owner-native boundaries where one owner can define, transition and reconcile them.

### Resource lifecycle

No universal Resource state machine is currently justified.

---

# 26. R5 handoff: composition after lifecycle deletion

R5 can now study composition on a cleaner substrate.

Instead of asking:

```text
Which lifecycle state are Resource A and B in?
```

R5 can ask:

```text
For transition T at as_of t:
which ResourceFor projections are supported?
which ActionableResourceFor projections hold?
which resources substitute?
which complement?
which are prerequisites/catalysts?
which failure domains are shared?
what bundle supports Capability C?
```

The core R5 questions become:

1. substitution versus complementarity;
2. necessary versus sufficient bundles;
3. catalysts/prerequisites that enable conversion without being consumed;
4. bottlenecks and limiting capacity;
5. common-mode failure and effective redundancy;
6. rival/non-rival consumption in composition;
7. whether composition itself needs persisted shared structure or can remain demand-scoped projection;
8. how a composed Capability becomes a higher-level Resource without transferring internal authority.

R5 must preserve the R4 rule:

> Do not rebuild a global lifecycle/dependency graph through composition vocabulary.

---

# 27. Conclusion

R4 started with a familiar lifecycle:

```text
Potential
→ Discovered
→ Verified
→ Acquired
→ Accessible
→ Qualified
→ Actionable
→ Option
→ Consumed
```

The evidence does not support it as a root ontology.

After deletion, the structure is smaller:

```text
Reality
  │
  ├───────────────┐
  ▼               ▼
Events          Claims
  │               │
  └──────┬────────┘
         ▼
   Resource Projection
         │
         ▼
 Actionability / Option
         │
         ▼
 Decision / Workflow
         │
         ▼
    new Events/Claims
```

The key correction is:

> **Lifecycle was mostly a projection of our knowledge and workflow onto Reality. The foundation is not a Resource state machine; it is owner-native Events and Claims plus context-bound projections.**

That is the R4 result carried into R5. It remains provisional research, not canonical World doctrine.
