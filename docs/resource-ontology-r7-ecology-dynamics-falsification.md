---
schema_version: 1
id: world.resource-ontology-r7-ecology-dynamics-falsification
title: Resource Ontology R7 — Resource Ecology Dynamics Falsification
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
summary: Falsifies universal Resource balance/vector/lifecycle models and retains owner-native dynamic claims plus demand-scoped ecology projection for reservation, capacity, currentness, renewal, decay, replication, maintenance, non-rival reuse and recursive feedback.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-ontology-r6-conversion-falsification
  - world.resource-option-capability-model
---
# Resource Ontology R7 — Resource Ecology Dynamics Falsification

## 1. Question

R0–R6 progressively removed several false universal structures:

```text
Resource is not just an owned/useful object.
Resource does not have one universal lifecycle.
Capability is not an additive bag of Resources.
Composition is not one universal dependency graph.
Action/Effect/Outcome/Knowledge are not one success pipeline.
```

R7 asks the next question:

> **Once Resources participate in real work, what actually changes over time?**

The tempting answer is an inventory system:

```text
Resource balance
+ acquisition / replenishment
- reservation / consumption / decay
= next balance
```

That picture is correct for some resources. R7 tests whether it is the root model.

R7 specifically pressure-tests:

```text
stock
flow / rate
capacity
budget
reservation
release
consumption / depletion
renewal / replenishment
reacquisition
expiry / revocation
currentness / availability
decay / relearning
replica / materialization
maintenance burden
non-rival reuse
recursive resource creation
positive and negative feedback
```

The same deletion law remains active:

> Keep a dynamic distinction only if deleting it changes a prediction, current Option, admission/recovery decision, causal claim, owner responsibility, or future selection.

R7 does not begin by designing a Resource ledger.

---

# 2. Frozen evidence boundary

Canonical World base at R7 admission:

```text
50abd7e9d84a4f02604e3fd59a3500f6f26064c1
```

The frozen owner revisions were:

| Owner | Revision |
| --- | --- |
| world | `50abd7e9d84a4f02604e3fd59a3500f6f26064c1` |
| finance | `7d812d8d41d5ba6b8aa619886beddca94327b11f` |
| runtime | `c6e45d9e41d3b4d64b5b3dace01497c53e574026` |
| workstation | `85f904635e856612b78e8b13acc553b1e80d292a` |
| studio | `52f646022cc606985a63a5fd290c417fd337e80e` |
| security | `6a7a8f9b22cb4995d436da2968b135248f8f6bb3` |
| game | `0c8581c6b5eebceaf33aeb8907fa91a8b53708dc` |
| human | `f7725dfc9b391c3e9a0c509d49795994931c9d63` |
| harness | `286985c82874d293308297f66b23152c1ed53369` |


R7 bound **22 selected source files** and **49 exact source needles** to this frozen corpus.

A concurrent Finance change occurred *after* the four R7 models and 50-case matrix were frozen. It did not modify any selected frozen Finance source file. R7 therefore retained the original frozen corpus and used the new Finance work only as post-freeze falsifier evidence.

Concurrent Finance evidence:

```text
1499b0b48c83cc1a16ec6c68504f77a88433b96d
finance: add temporal financial resource identity
```

That chronology matters. The new Finance model was not used to author D.

---

# 3. Two direct R7 implementation probes

## R7P01 — current World is quantitatively blind to quota magnitude

Current `OwnerVerification` contains:

```text
quota_class: str
```

R7 constructed the same Resource, demand, owner identity and transport evidence twice. The only changed owner fact was:

```text
remaining-1-request
```

versus:

```text
remaining-100-requests
```

Current `ResourceEvaluation` was exactly identical:

```text
decision         = consumable-now
demandFit        = 1.0
evidenceQuality  = 0.9
potentialScore   = 0.617391
```

No current output field records the 100× capacity difference.

Therefore current World has a real **quantitative dynamics projection gap**.

This does not prove that every Resource needs a quantity field. It proves only that a consumer requiring quantitative quota/capacity cannot obtain that truth from the current generic projection.

Probe Job:

```text
job-01a00599-e094-7ca2-9a59-0d54b57d987b
```

## R7P02 — Runtime reservation and release are real relations, not a narrative

A real Runtime Job held the sole execution slot in one Workspace:

```text
holder Job:
job-01a0059a-43e4-75c3-8e66-f255b4111b62
```

A second exact request received:

```text
CONCURRENCY_LIMIT
active = 1
limit = 1
holderJobIds = [exact holder]
commitState = not_started
```

After the original holder reached terminal convergence, the **same rejected `clientRequestId`** was submitted again and admitted successfully:

```text
admitted Job:
job-01a0059a-bd33-7882-9d21-a4a2c351a276
```

This proves:

```text
Reservation exists
→ available capacity changes
→ another Option is infeasible

terminal convergence
→ Reservation releases
→ available capacity changes again
→ the previously blocked Option becomes feasible
```

The historical holder Job did not disappear and the rejected request was not retroactively committed.

So:

```text
reservation history
≠ current reserved quantity
≠ consumption/depletion
```

---

# 4. Four frozen ecology models

## A — Universal Stock Account

> Every Resource has one scalar balance in a resource-specific unit. Admission/reservation/consumption subtracts balance; release, renewal, replenishment or reacquisition adds balance; decay is balance loss. Dynamic Resource reasoning is fundamentally accounting over that one stock.

This is the strongest version of the intuitive “resources are inventory” model.

It predicts that every important dynamic can ultimately be explained as a balance moving up or down.

## B — Universal Stock–Flow–Capacity Vector

> Every Resource is projected into one common time-indexed vector containing quantity, inflow, outflow, reserved, available, capacity/rate, decay and replenishment in native units. Resource change is represented by updates to that vector; identity/currentness/authority facts may qualify the vector but are not separate dynamic topologies.

B tries to rescue A by adding a full vector rather than one balance.

The danger is ontology-by-nullable-field: every Resource receives dimensions that may have no meaningful owner-native interpretation.

## C — Single Family-Specific Lifecycle

> Every Resource belongs to exactly one canonical dynamics family (for example stock, flow, capacity, entitlement, availability, reusable reference, skill or replicated artifact). Each family has its own owner-native lifecycle/state rules; cross-family composition is allowed, but one Resource identity has one dynamics family and one family lifecycle.

C accepts heterogeneous resources and gives each family its own dynamics.

After an anti-strawman audit, R7 deliberately strengthened C. Former hard failures that could be absorbed by hybrid family state or cross-family transitions were moved to PASS/AMBIG.

Before correction:

```text
36 PASS / 7 FAIL / 7 AMBIG
```

After correction:

```text
39 PASS / 0 FAIL / 11 AMBIG
```

C is therefore **expressive, not falsified**.

Its remaining problem is whether the canonical family taxonomy itself earns explanatory or executable value.

## D — Owner-Native Dynamic Claims + Ecology Projection

> Resource identity remains independent from one global dynamics type. Native owners expose only transition-relevant dynamic Claims/Events—quantity, stock, rate, capacity, reservation/release, quota window, availability/currentness, expiry/revocation, replica/materialization, decay/maintenance, renewal/reacquisition or non-rival reuse—using native units, clocks and identities. World forms demand/actor/transition/as_of ecology projections from those claims. A Resource may participate in several dynamic aspects at once. Renewal/reacquisition need not invert prior history; reservation is distinct from consumption/depletion; recursive creation and negative feedback require R6 evidence/Attribution rather than temporal adjacency.

D says the dynamic root is not a Resource state machine at all.

Instead:

```text
Resource identity
    │
    ├── owner-native quantity / stock Claims, where real
    ├── owner-native rate / capacity Claims, where real
    ├── Reservation / Release Events, where real
    ├── currentness / availability Claims
    ├── authority / expiry / revocation Claims
    ├── replica / materialization Claims
    ├── decay / maintenance evidence
    ├── renewal / reacquisition Events/Claims
    └── reusable/non-rival evidence
                 │
                 ▼
        demand / actor / transition / as_of
                 │
                 ▼
          Ecology Projection
                 │
        current Options / capacity /
        bottlenecks / maintenance /
        renewal or acquisition pressure
```

A Resource can participate in several dynamic aspects at once without being assigned a new hybrid class.

---

# 5. Falsification result

| Model | 50 frozen discriminators |
| --- | --- |
| A — Universal Stock Account | 16 PASS / 24 FAIL / 10 AMBIG |
| B — Universal Stock–Flow–Capacity Vector | 19 PASS / 21 FAIL / 10 AMBIG |
| C — Single Family-Specific Lifecycle | 39 PASS / 0 FAIL / 11 AMBIG |
| D — Owner-Native Dynamic Claims + Ecology Projection | 50 PASS / 0 FAIL / 0 AMBIG |

After D wording was frozen, ten additional falsifiers passed without changing D.

Current D surface:

```text
60 / 60
```

This remains falsifier evidence, not universal proof.

## 5.1 Complete frozen matrix

| ID | Source | Pressure | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | `R7P02` A live Runtime Job holds the sole Workspace execution slot and a second exact request is rejected not_started with the exact holder identity | reservation blocks option | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C02 | `R02` Runtime terminal convergence releases the durable concurrency reservation atomically | reservation release | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C03 | `R03` An identity-uncertain Runtime Attempt retains its reservation while the recorded unit/process/cgroup may still own work | uncertainty holds capacity | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C04 | `R04` A policy change applies to new Runtime admission while exact replay preserves the old Job and old effective limits | policy window vs historical commitment | FAIL `A-NOT-STOCK` | AMBIG `B-OVERPROJECTS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C05 | `R05` Windows Attempt acquires an Attempt-scoped SystemRequired Power Request only while physical work is active | ephemeral lease | AMBIG `A-PARTIAL-STOCK` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C06 | `R06` Terminal replay does not restart the launcher and therefore does not reacquire the Power Request | history vs renewed lease | AMBIG `A-PARTIAL-STOCK` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C07 | `R07` Runtime cache reclamation is driven by high/low capacity watermarks and only eligible bytes are reclaimed | stock pressure plus policy | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C08 | `R08` Global package-manager caches are measured but not interpreted/deleted by Runtime because another owner controls their lifecycle | ownership of stock dynamics | FAIL `A-NOT-STOCK` | AMBIG `B-OVERPROJECTS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C09 | `R09` Workspace closure removes Workspace-scoped disposable caches while shared trusted-local package caches survive | different lifecycles under one execution | AMBIG `A-PARTIAL-STOCK` | AMBIG `B-OVERPROJECTS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C10 | `R10` Timeout/output/memory/process/CPU budgets constrain physical consumption but are explicitly not scheduling/priority/approval semantics | budget vs resource state | AMBIG `A-PARTIAL-STOCK` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C11 | `F01` Finance consumes daily authority budget at ExternalEffect reservation before venue submission | reservation before effect | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C12 | `F02` Finance counts every daily reservation regardless of eventual venue outcome instead of guessing failure/UNKNOWN returned the budget | reserved vs consumed/released | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C13 | `F03` A later reconciliation may establish evidence-backed release/accounting semantics without rewriting the original reservation event | release after evidence | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C14 | `F04` Remote Finance ledger owns daily reservation truth so deleting/restarting local state cannot reset available budget | durable windowed capacity | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C15 | `F05` All executor replicas in one authority domain must share the same durable daily ledger or capacity splits falsely | shared capacity owner | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C16 | `F06` Exact replay returns historical admission without consuming daily budget twice | idempotent accounting | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C17 | `F07` Owner capital contributions/withdrawals change capital stock but are removed from investment performance | stock flow vs outcome | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C18 | `F08` Portfolio equity changes through mark-to-market and other non-ledger mechanisms without a cash-flow event | valuation stock without flow | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C19 | `F09` Finance measures drawdown/minimum equity but explicitly refuses one universal drawdown threshold | state measure vs policy | AMBIG `A-PARTIAL-STOCK` | AMBIG `B-OVERPROJECTS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C20 | `N01` Workstation revalidation accepts only an exact saved path/observation identity; using the path does not deplete it | currentness not depletion | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C21 | `N02` Successful Workstation qualification creates a fresh observation before readmission | refresh claim not refill stock | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C22 | `N03` Anchor admission refuses silent replacement of a different active selection | generation/selection identity | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C23 | `N04` A catalog of 98 public candidates is not 98 currently executable roots | candidate cardinality vs current capacity | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C24 | `N05` Provider/mechanism diversity does not form a current independent pair when one root is unavailable | availability and independence | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C25 | `N06` Negative current root observations are retained rather than retried until they become green | historical negative truth | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C26 | `N07` Stopped/replaced network relations invalidate exact bindings; readmission never resurrects the old generation | reacquisition is new relation identity | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C27 | `N08` The same Snowflake Resource is available in one parent relation and unavailable in another at the same time | relation-scoped dynamics | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C28 | `S01` Studio Asset digest existed while selected bytes had not yet been moved into durable storage before Workspace close | identity vs materialized stock | AMBIG `A-PARTIAL-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C29 | `S02` Studio materialize creates the missing working copy once; exact replay returns existing without creating a second semantic master | materialization vs identity | AMBIG `A-PARTIAL-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C30 | `S03` After destructive local-CAS loss, an independently verified R2 replica restores the same exact Blob identity | replication/reacquisition | AMBIG `A-PARTIAL-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C31 | `S04` A materialized review MP4 is a recoverable working copy, not a separate master Resource merely because another byte copy exists | copy count vs resource identity | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C32 | `S05` Studio tool retention weighs maintenance/failure surface and can keep powerful tools specialist/on-demand rather than maximizing utilization | maintenance and idle optionality | FAIL `A-NOT-STOCK` | AMBIG `B-OVERPROJECTS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C33 | `S06` A future Resolve version requires compatibility re-probe before reusing the old profile | compatibility decay/currentness | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C34 | `Q01` A Security single-run Activation remains consumed after an invalid trial and must be replaced for rerun | rival single-use authority | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C35 | `Q02` Security retains exact sample bytes unchanged while disposable execution environments/activations are consumed separately | reusable bytes vs consumable authority | AMBIG `A-PARTIAL-STOCK` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C36 | `Q03` A cached exact Security result remains usable historical truth during outage | non-rival retained result | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C37 | `Q04` The same outage blocks a new unique Security job while cached exact result remains available | historical result vs current capability | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C38 | `Q05` Persistent artifact/service can remain while usable controller authority disappears after credential revocation | object persistence vs authority decay | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C39 | `H01` Human attention/time is measured as a policy cost and interruption count consumes synchronization attention | flow/capacity resource | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C40 | `H02` Human capability can decay through non-use, changing environments, illness, automation or obsolete knowledge | degradable capability | PASS `A-STOCK-FIT` | PASS `B-VECTOR-FIT` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C41 | `H03` Relearning rate after interruption is evidence about retained Human capability | decay is not deletion | PASS `A-STOCK-FIT` | AMBIG `B-OVERPROJECTS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C42 | `H04` Tools can increase joint-system capability while reducing practice of internal Human skill | positive and negative coupled feedback | AMBIG `A-PARTIAL-STOCK` | AMBIG `B-OVERPROJECTS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C43 | `H05` Human capability can produce resources, reputation, autonomy and further learning opportunities | recursive resource creation | FAIL `A-NOT-STOCK` | AMBIG `B-OVERPROJECTS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C44 | `HA01` One externally promoted exact Harness procedure is reused across two independent Runs without being depleted by first use | non-rival reusable resource | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C45 | `HA02` Harness reusable source presence does not mean selection into a Run | resource presence vs current use | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C46 | `HA03` Each ToolProgram inner step consumes one existing Tool-call budget unit while procedural knowledge remains intact | consumed budget vs non-rival knowledge | FAIL `A-NOT-STOCK` | AMBIG `B-OVERPROJECTS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C47 | `HA04` ToolProgram reduces model calls from seven to two while preserving the same five physical Tool calls | conversion modifier changes one flow only | FAIL `A-NOT-STOCK` | AMBIG `B-OVERPROJECTS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C48 | `R7P01` Current World produces identical ResourceEvaluation when owner quota text changes from remaining-1-request to remaining-100-requests | production quantitative blind spot | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C49 | `WQ01` Current World stores quota only as opaque quota_class text and has no quantity/reserved/replenishment projection in ResourceEvaluation | representation gap | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | PASS `C-FAMILY-FIT` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |
| C50 | `R6C` R6 already established resource-family-specific consumption accounting rather than one universal consumption stage | prior boundary constraint | FAIL `A-NOT-STOCK` | FAIL `B-VECTOR-TOPOLOGY-LOSS` | AMBIG `C-FAMILY-BOUNDARY-AMBIG` | PASS `D-NATIVE-DYNAMIC-PROJECTION` |

---

# 6. Why A fails: many Resources do not behave like inventory

A is useful for:

```text
cash
storage bytes
single-use activations
some quotas
some reserved capacity
```

But R7 repeatedly finds dynamics that are not balance depletion.

## Network paths

A Workstation path can become unusable because:

```text
owner observation stales
root fails
parent relation changes
generation is replaced
qualification is no longer current
```

Using the path did not consume it.

## Authority

A credential can be revoked while:

```text
artifact remains
service remains
historical result remains
account-level Resource may remain
```

Calling this “balance became zero” loses which aspect disappeared.

## Knowledge

A promoted procedure can be used in two independent Harness Runs without the first Run depleting it.

## Human skill

Skill can decay through non-use and later relearn faster than from zero. A scalar quantity may summarize one measurement but does not explain the mechanism.

## Studio artifact identity

A local CAS copy can disappear while an independent R2 replica preserves recoverability of the same exact Blob identity.

Therefore A mistakes several different questions for one:

```text
How much exists?
Is it currently available?
Is authority still valid?
Is a copy materialized here?
Can it be restored?
Is it selected?
Has skill decayed?
```

---

# 7. Why B does not rescue the universal model

B adds enough fields to make most quantitative cases representable:

```text
quantity
inflow
outflow
reserved
available
capacity
rate
decay
replenishment
```

But the cost is that the vector becomes a generic bag of optional coordinates.

R7's failures are not primarily missing arithmetic.

They are often **topology and truth-role failures**:

```text
same Resource available in parent A, unavailable in parent B
old generation invalid, fresh readmission creates new relation identity
local materialization absent, remote exact replica present
cached historical result available, new unique work unavailable
physical artifact persists, authority revoked
Reusable source present but not selected
```

A larger numeric vector does not naturally encode which owner, relation, generation, materialization, or truth role the number belongs to.

B can keep adding qualifiers until it becomes D expressed as nullable fields. At that point the universal vector is no longer doing explanatory work.

---

# 8. C is strong—and that is exactly why R7 does not reject it

C says:

```text
cash → Stock family
attention → Flow/Capacity family
API quota → RenewableQuota family
credential → Entitlement family
network path → Availability family
artifact → ReplicatedArtifact family
skill → Skill family
knowledge → ReusableReference family
```

This is coherent.

When a hard case appears, C can add:

```text
EntitlementWithQuota
RelationalAvailability
ReplicatedArtifactWithCompatibility
SkillWithFatigueAndRelearning
ValuatedCapital
```

or a cross-family transition.

That means C is rarely false.

It also means the key deletion question becomes:

> What prediction changes because World knows the canonical family name, rather than simply joining the owner-native dynamic Claims needed by the current transition?

Current evidence does not answer that in C's favor.

R7 therefore does **not** say “resource families are wrong.”

It says:

> **Family labels are useful explanatory shorthand, but a universal family registry/lifecycle hierarchy is not yet earned.**

A domain owner can still have a native `capital`, `quota`, `skill`, `artifact`, or `entitlement` model where that vocabulary is real domain truth.

---

# 9. Reservation survives deletion

Reservation is one of R7's strongest retained distinctions.

It answers:

> **Which capacity has been precommitted such that another Option must currently behave as unavailable?**

Runtime proves it mechanically:

```text
Job admitted
→ SQLite reservation committed
→ physical dispatch later
→ terminal/recovery convergence
→ reservation released atomically
```

Finance independently proves the same abstract relation with different semantics:

```text
ExternalEffect reservation
→ daily authority budget consumed
→ venue result later
→ UNKNOWN does not imply release
→ later reconciliation may authorize accounting/release
```

These are not one shared implementation.

The shared semantic fact is narrower:

```text
Reservation
≠ Consumption
≠ Effect
≠ Outcome
```

Reservation exists because committed optionality itself can be scarce.

---

# 10. Release does not erase history

A dangerous inventory intuition is:

```text
reserve 1
release 1
therefore nothing happened
```

R7 rejects that.

After Runtime release:

```text
historical Job/Attempt/reservation remains true
current reserved capacity returns
```

After Finance reconciliation-backed release:

```text
historical ExternalEffect reservation remains true
current daily authority availability may change
```

Thus release is a later owner-native Event/transition affecting current projection.

It is not mutation of the earlier event into “never reserved.”

This matches R4's event/history law and R6's effect/outcome separation.

---

# 11. Consumption and depletion remain resource-family-specific

R7 now has decisive positive and negative examples.

## Rival / depleting

```text
single-use Security Activation
cash spent
Tool-call budget unit
some finite quotas
```

## Reservable but not necessarily consumed immediately

```text
Runtime concurrency slot
Finance daily authority budget
```

## Renewable

```text
windowed API quota
periodic capacity budget
```

## Reusable / non-rival

```text
promoted Harness procedure
cached exact result
software
public data source
knowledge claim
```

## Replicable

```text
Studio Blob
local CAS + remote R2 replica
```

So R7 retains R6's rule:

```text
ConsumptionEvent / quantity / reservation / depletion / renewal
```

only where the owner can define those terms truthfully.

No universal `consumed=true` state is reintroduced.

---

# 12. Capacity is not Resource count

R7 repeatedly reproduces:

```text
cardinality ≠ capacity
```

Workstation's catalog can contain 98 candidates while current strong-root availability remains much smaller.

Two provider mechanisms are not a current independent pair if one root is unavailable.

Runtime's one Workspace execution slot is actual capacity because admission enforces and reports it.

Finance daily authority capacity is actual capacity because reservation history is shared across replicas.

This gives a stronger R7 capacity rule:

> **Capacity is an owner-native quantitative or bounded claim about how much/how often/how concurrently a named transition can currently be supported under declared load/context—not a count of Resources that look relevant.**

Native units stay native:

```text
Jobs
requests / minute
USD
bytes
model calls
tokens
seconds
Human attention time
liquidity participation
```

No universal unit conversion is justified.

---

# 13. Currentness and availability are dynamics without depletion

Some of the most important Resource dynamics have no conservation law.

A network route may be:

```text
available at t0
unavailable at t1
available again after fresh qualification at t2
```

No path inventory was consumed and replenished.

A Resolve compatibility profile may be valid for one version and require re-probe after upgrade.

A Security cached result may remain usable while new unique execution becomes unavailable during outage.

A Finance identity regime may change at an economic/reference transition even though the economic object continues.

Therefore:

```text
Actionability(t)
```

can change because a relation/claim changed, not because a Resource quantity moved.

This is why R7 keeps currentness/availability as relational dynamic Claims rather than forcing them into stock arithmetic.

---

# 14. Renewal, replenishment and reacquisition are not synonyms

R7 distinguishes three broad mechanisms.

## Replenishment

A quantitative capacity becomes available again under the same owner-native accounting regime.

Example:

```text
renewable quota window resets
```

## Renewal

Authority/contract/current evidence advances to a new validity period or generation.

Example:

```text
credential/license/token renewal
```

## Reacquisition / readmission

A useful relation or materialization is obtained again, possibly with a new identity/generation.

Examples:

```text
Workstation fresh observation + anchor admission
Studio R2 restore to local CAS
```

The important law is:

> **Restoring current usability does not require reversing history to a previous state.**

Workstation explicitly says readmission never resurrects an old generation binding.

Studio restoration recreates local materialization of the same exact Blob identity; it does not pretend the destructive local loss never happened.

---

# 15. Replica count is not Resource count

Studio gives R7 a clean identity example.

The same selected Blob can exist as:

```text
canonical semantic Asset reference
local content-addressed Blob
remote R2 exact replica
review working copy
```

These copies have different recovery roles.

But the materialized review MP4 is explicitly:

```text
not a separate master
```

So increasing physical copies can increase:

```text
durability
failure-domain diversity
recovery options
```

without increasing semantic Resource cardinality one-for-one.

R7 therefore keeps:

```text
Resource identity
Replica/materialization relations
```

separate.

This also generalizes to datasets, software artifacts, model files and evidence blobs.

---

# 16. Expiry and revocation do not delete everything below them

Security gives a strong layered counterexample:

```text
persistent artifact present
service active
credential revoked
usable controller authority absent
```

Likewise a cached exact result may survive service outage or later revocation while a new unique job is unavailable.

Therefore:

```text
credential/authority validity
physical artifact existence
historical result truth
current execution capability
```

must not share one lifecycle state.

Expiry/revocation is an invalidation of a specific authority/claim/relation.

It is not universal Resource deletion.

---

# 17. Decay is not one generic subtraction process

Human and Studio provide two very different forms of decay.

## Human skill

Capability can decay through:

```text
non-use
changing environment
illness
automation
obsolete knowledge
```

Yet `relearning rate after interruption` can show retained substrate.

Thus:

```text
performance drop
≠ skill deleted
```

## Tool/compatibility knowledge

A Resolve compatibility result can become insufficient after a version change.

The binary/tool may still exist. The old observation remains historical truth. What decays is applicability/currentness of the compatibility claim.

Therefore no universal:

```text
resource_quantity -= decay_rate * dt
```

is earned.

Different owners may legitimately use very different decay models.

---

# 18. Maintenance burden creates negative ecology feedback

Resource acquisition is not monotonic value creation.

Studio Equipment World explicitly retains:

```text
capability gain
friction reduction
quality / editable-master ceiling
cost / maintenance / failure surface
```

A powerful tool may remain specialist/on-demand because always-on integration costs more than its ordinary value.

Runtime similarly preserves owner boundaries around caches and historical data because automatic deletion/management itself has recovery and authority costs.

Security adds attack-surface pressure.

Human adds skill-practice displacement.

Thus Resource ecology requires signed feedback:

```text
new Resource
  → + Capability / Option / resilience
  → - maintenance / complexity / attack surface / attention
```

No law says the net is positive.

---

# 19. Human evidence gives both positive and negative feedback loops

Human's current capability model explicitly contains:

```text
Capability
→ resources, reputation, autonomy, further learning opportunities
```

This supports cumulative-advantage loops:

```text
Capability
→ better Resource acquisition
→ more Options
→ more learning/effects
→ more Capability
```

But Human also states:

```text
Tools can increase system capability
while reducing practice of internal skill.
```

So another loop is possible:

```text
external capability ↑
→ internal practice ↓
→ independent skill ↓
→ dependence on external Resource ↑
```

These are not contradictions.

They show that feedback must be:

```text
signed
objective-specific
horizon-specific
actor-boundary-specific
```

and, because of R6:

```text
causally attributed before being promoted as a loop law.
```

---

# 20. Non-rival knowledge changes ecology without depletion

Harness P1 provides an especially clean case:

```text
promoted exact procedure
→ Run A explicit admission/use
→ Run B explicit admission/use
```

The source does not become “half as available” after Run A.

Its dynamic constraints are instead:

```text
is the canonical source still present?
is provenance exact?
is it selected for this Run?
is it still applicable/current?
does the current Run admit it?
```

This is a different ecology from money or a single-use Activation.

Harness P2 then shows that a reusable procedure can change **other** resource flows:

```text
baseline:  7 model calls / 5 Tool calls
treatment: 2 model calls / 5 Tool calls
```

The procedure itself is not depleted. It is a conversion modifier that changes model-call/token cost while preserving physical Tool effects.

---

# 21. Recursive Resource creation needs Attribution

It is tempting to write:

```text
Knowledge → Resources
Capability → Resources
capital → compute/data
Security capability → access to more resources
```

R7 retains these as candidate causal loops, but R6 changes the proof rule.

Temporal order is insufficient.

A credible recursive-creation claim needs evidence that the upstream Resource/Capability materially changed:

```text
discovery
acquisition
qualification
conversion cost
reachable Options
recovery
```

relative to a relevant comparison.

Otherwise:

```text
Knowledge existed
then more Resources appeared
```

could simply be exogenous reality.

The resource flywheel is therefore a **causal hypothesis/evidence structure**, not an automatic accounting identity.

---

# 22. Concurrent Finance FR2 independently attacks the universal balance model

After R7 froze D, Finance independently completed FR2 at:

```text
1499b0b48c83cc1a16ec6c68504f77a88433b96d
```

FR2's winner is:

```text
temporal relation intervals + identity events
```

It requires two separate clocks:

```text
effective time
observed_at / knowledge time
```

and permits bounded transition windows whose correct result is:

```text
UNKNOWN
```

rather than an invented exact instant.

It also keeps one economic object across several reference/identity regimes.

An `IdentityEvent` can invalidate:

```text
reference assumptions
historical comparability
carrier history
hypothesis-carrier assumptions
```

without meaning that the underlying economic object was consumed or that one scalar stock went to zero.

FR2 independently converges on the same structural lesson as R4/R7:

> **Temporal dynamics often belong to relation/claim/event history with explicit knowledge time, not to mutation of one current Resource record.**

This is particularly strong because FR2 was not part of D's frozen authoring corpus.

---

# 23. “Five useful stocks” survives—but only as macro reasoning language

Existing World research says:

```text
For reasoning—not as a new database schema—
Resource Capital
Authority Capital
Option Capital
Capability Capital
Knowledge Capital
```

R7 does not reject this.

These are useful aggregate metaphors for system position:

```text
Do we know/hold more potentially useful reality?
Do we possess more usable authority?
Do we have more current alternatives?
Can the system reliably do more?
Do we know more about what works and why?
```

But they are **not** literal per-Resource bank accounts.

For example:

```text
Knowledge Capital can rise
without a source document being consumed.

Option Capital can fall
because one network path becomes unavailable,
without Resource Capital being destroyed.

Authority Capital can fall
when a credential is revoked,
while physical artifact stock remains unchanged.
```

Therefore macro stock language and micro Resource dynamics occupy different abstraction levels.

---

# 24. R7 dynamic relation ledger

| Dynamic concept | R7 disposition | Cases | Why |
| --- | --- | --- | --- |
| Resource identity | **KEEP_SEPARATE_FROM_DYNAMIC_AMOUNT** | C28, C30, C31, C38 | Local materialization, replica count or current authority can change while the underlying bounded Resource aspect remains identifiable. |
| Stock/quantity | **OPTIONAL_OWNER_NATIVE_DIMENSION** | C07, C17, C18 | Bytes/capital can have meaningful quantities, but many Resources do not have a useful scalar stock. |
| Flow/rate | **OPTIONAL_OWNER_NATIVE_DIMENSION** | C17, C18, C39, C47 | Cash flows, attention use and call rates matter without becoming the identity of the Resource. |
| Capacity | **OPTIONAL_OWNER_NATIVE_DIMENSION** | C01, C15, C23, C39 | Capacity limits simultaneous/repeated transitions and may be shared across consumers; count of resources is not capacity. |
| Reservation | **REQUIRED_WHEN_OWNER_PRECOMMITS_CAPACITY** | C01, C03, C11, C12 | Reserved capacity blocks Options before actual Effect/consumption and can remain held under uncertainty. |
| Release | **SEPARATE_EVENT_OR_OWNER_TRANSITION** | C02, C13 | Release restores available capacity only after owner-native terminal/reconciliation evidence; it does not erase the reservation history. |
| Consumption/depletion | **FAMILY_SPECIFIC_NOT_UNIVERSAL** | C34, C35, C44, C46 | Single-use authority depletes, Tool-call budget consumes, sample/procedure knowledge may be reused without depletion. |
| Renewal/replenishment | **OWNER_NATIVE_MECHANISM_NOT_INVERSE_LIFECYCLE** | C04, C14, C21, C26 | New policy/window/fresh observation/readmission may restore Actionability without reversing historical events or reusing old generation identity. |
| Currentness/availability | **RELATIONAL_DYNAMIC_CLAIM** | C20, C21, C24, C27, C33, C37 | Use need not deplete a Resource; Actionability can instead change because current evidence, parent relation, compatibility or provider availability changes. |
| Expiry/revocation | **CLAIM_OR_AUTHORITY_INVALIDATION** | C37, C38 | Authority/capability may disappear while historical results or physical artifacts persist. |
| Replica/materialization | **SEPARATE_FROM_RESOURCE_IDENTITY** | C28, C29, C30, C31 | Copies and current materializations affect durability/recovery, not necessarily semantic Resource cardinality. |
| Decay | **FAMILY_SPECIFIC_EVIDENCE** | C33, C40, C41 | Compatibility and skill can decay through different mechanisms and clocks; decay is not generic quantity subtraction. |
| Maintenance burden | **SEPARATE_NEGATIVE_FEEDBACK_DIMENSION** | C08, C32 | More retained Resources can increase maintenance/failure/ownership burden even when current capability count rises. |
| Recursive creation | **REQUIRES_EFFECT_OUTCOME_ATTRIBUTION** | C43 | Capability may create future resources/opportunities, but R6 forbids inferring causality from temporal adjacency alone. |
| Conversion modifier | **DYNAMIC_RELATION_NOT_RESOURCE_STOCK** | C47 | A procedure can reduce model-call flow while leaving physical Tool-call flow unchanged. |
| Non-rival reuse | **REQUIRED_COUNTEREXAMPLE_TO_DEPLETION** | C36, C44, C45 | Historical results/procedures can be reused without being diminished by use; selection remains separate. |
| Policy threshold | **NOT_RESOURCE_DYNAMICS_BY_DEFAULT** | C04, C19 | Changing admission/drawdown policy can change decisions without changing the underlying Resource stock. |
| Feedback | **SIGNED_AND_ATTRIBUTED** | C42, C43 | Resource/capability loops may be positive or negative; assistance can increase joint capability while decreasing internal practice. |

The key reduction is that most concepts are **optional owner-native coordinates**, not mandatory Resource fields.

---

# 25. Deletion and rejected-addition tests

| Mutation | Result | Cases | Why |
| --- | --- | --- | --- |
| delete Reservation as distinct from Consumption | **FAIL** | C01, C11, C12 | Capacity can be blocked before physical/financial Effect and remain held when outcome is UNKNOWN. |
| delete Release as a separate owner-native event/transition | **FAIL** | C02, C13 | Available capacity changes after terminal/reconciliation without rewriting historical reservation/Effect truth. |
| delete currentness/availability dynamics and model all loss as depletion | **FAIL** | C20, C24, C27, C33, C37 | Paths, compatibility and provider access can become unusable without being consumed. |
| delete replica/materialization distinction | **FAIL** | C28, C30, C31 | Local bytes can disappear while exact Resource identity remains recoverable from another replica. |
| delete non-rival reuse | **FAIL** | C36, C44 | Exact results/procedures remain reusable after use; a depletion-only model predicts false scarcity. |
| delete decay/relearning distinction and treat absent performance as deletion | **FAIL** | C40, C41 | Human skill can degrade and later relearn faster; retained substrate is not binary possession. |
| delete maintenance/negative feedback | **FAIL** | C32, C42 | More tools/assistance can add capability while increasing maintenance or reducing internal practice. |
| force every Resource into one scalar balance | **REJECT_ADD** | C20, C27, C38, C44 | Availability relations, authority and non-rival knowledge are distorted as inventory. |
| force every Resource to materialize a universal stock-flow-capacity vector | **REJECT_ADD** | C27, C31, C45, C50 | Meaningless nullable dimensions add ontology without changing owner-native predictions and still lose relation identity. |
| force exactly one canonical dynamics family per Resource | **REJECT_ADD** | C18, C27, C38, C42, C47 | One Resource/aspect can participate simultaneously in valuation, availability, authority, skill and modifier relations depending on transition/boundary. |
| treat renewal/reacquisition as reversal to a prior state | **REJECT_ADD** | C21, C26 | Fresh observation/readmission can create a new generation/claim while old historical failure remains true. |
| credit recursive resource growth to the immediately preceding Action without Attribution | **REJECT_ADD** | C43 | R6 requires causal evidence; exogenous changes and shared causes remain possible. |
| maximize utilization as ecology objective | **REJECT_ADD** | C32, C44 | Idle/on-demand tools and reusable knowledge can retain option value; utilization can increase wear, cost or deskilling. |
| interpret candidate/resource count as available capacity | **REJECT_ADD** | C23, C24 | Catalog cardinality and provider diversity do not prove current actionable capacity or independence. |

Seven distinctions fail deletion in the current corpus:

```text
Reservation
Release
currentness/availability dynamics
replica/materialization distinction
non-rival reuse
decay/relearning distinction
maintenance/negative feedback
```

None implies one global state machine.

---

# 26. Fresh post-freeze falsifiers

D wording was frozen before these cases were added:

| ID | Post-freeze case | D |
| --- | --- | --- |
| R7Y01 | A public dataset is copied locally: local materialization bytes increase while the public source Resource is not depleted. | PASS `D-REPLICA-NONRIVAL` |
| R7Y02 | A quota reservation receives exact not-committed proof and releases; the same ambiguous reservation without proof remains held. | PASS `D-RESERVATION-EVIDENCE` |
| R7Y03 | Credential renewal rotates a token generation while the account-level Resource and historical expired credential evidence persist. | PASS `D-RENEWAL-NOT-REVERSAL` |
| R7Y04 | Human fatigue temporarily reduces available capability while retained skill evidence is unchanged; rest restores availability without relearning the skill from zero. | PASS `D-MULTI-ASPECT-CAPABILITY` |
| R7Y05 | Deleting a reconstructible build cache lowers local byte stock but leaves task Capability unchanged until rebuild latency becomes a binding constraint. | PASS `D-STOCK-NOT-CAPABILITY` |
| R7Y06 | Adding a powerful tool creates a new Option but also adds maintenance/attack-surface burden, so ecology value need not move monotonically with Resource count. | PASS `D-SIGNED-FEEDBACK` |
| R7Y07 | Promoted Knowledge changes a later discovery strategy; only a measured discovery/acquisition difference can support the claim that Knowledge created new Resources/Options. | PASS `D-ATTRIBUTED-RECURSION` |
| R7Y08 | A renewable API window resets available calls at a clock boundary while yesterday’s consumption history remains true and current provider eligibility can independently expire. | PASS `D-MULTI-CLOCK` |
| R7Y09 | A concurrently completed Finance FR2 requires both effective time and observed_at/knowledge time, with bounded transition windows returning UNKNOWN rather than mutating one current Resource row. | PASS `D-MULTI-CLOCK-CLAIMS` |
| R7Y10 | Finance FR2 keeps one economic object across multiple temporal identity/reference regimes; IdentityEvent can invalidate comparability without meaning the object stock was depleted or replaced. | PASS `D-IDENTITY-RELATION-DYNAMICS` |

All ten pass without modifying D.

The final two are especially important because they came from a concurrent real Finance implementation rather than R7-authored synthetic cases.

Current D falsifier surface:

```text
50 frozen
+ 10 post-freeze
= 60 / 60
```

---

# 27. The minimum R7 ecology model

R7's current minimal topology is:

```text
Reality
  │
  ├── Resource identity / Aspect identity
  │
  ├── owner-native dynamic Claims
  │      quantity / stock
  │      rate / throughput
  │      capacity / quota
  │      currentness / availability
  │      authority / expiry / revocation
  │      materialization / replica
  │      compatibility / decay / maintenance
  │
  ├── owner-native Events
  │      reserve
  │      release
  │      consume / deplete
  │      replenish
  │      renew
  │      reacquire / readmit
  │      invalidate
  │      replicate / restore
  │
  └── promoted Knowledge / Capability exports
                   │
                   ▼
Actor + Transition + Demand + as_of + load
                   │
                   ▼
           Ecology Projection
      ┌────────────┼─────────────┐
      ▼            ▼             ▼
 current Options  capacity     bottlenecks
 reservations     renewal      maintenance
 currentness      substitutes  recovery
      │
      ▼
Decision / Action
      │
      ▼
R6 Effect / Outcome / Attribution
      │
      ▼
Knowledge / Capability / Resource changes
      │
      └── evidence-backed positive or negative feedback
```

There is deliberately no universal `ResourceState` node in the center.

---

# 28. Persistence rule after R7

Persist dynamic truth where its native owner needs continuity, recovery or point-in-time reconstruction.

Examples already justified:

```text
Runtime reservation rows
Finance authority reservation ledger
Finance temporal identity intervals/events
Studio exact Blob replicas
Security exact activation/authority evidence
Harness promoted external reusable source
```

Recompute/project when persistence adds no independent owner truth:

```text
current cross-owner Option set
current bottleneck ranking
current ecology summary
substitution under one demand
maintenance priority
aggregate “Resource Capital” score
```

R7 does not justify:

```text
GlobalResourceLedger
ResourceBalanceTable
ResourceFamilyRegistry
UniversalStockFlowEngine
GlobalReservationService
RenewalScheduler
ResourceMarketplace
```

---

# 29. Current production gap: quantitative dynamics

R7P01 is a real gap:

```text
quota 1 remaining
quota 100 remaining
→ same current ResourceEvaluation
```

A real future consumer may therefore need a shared projection such as:

```text
capacity for transition X
under owner Y
for load L
at as_of T
```

But R7 explicitly avoids choosing its production schema.

Why?

Because the correct representation may be:

```text
Finance-owned authority capacity
Runtime-owned concurrency projection
Workstation-owned path throughput
provider-owned rate-limit evidence
```

with World only joining them when one cross-owner decision actually needs the result.

The current gap earns **research pressure**, not a universal quantity table.

---

# 30. Resource ecology and the old flywheel

The earlier high-level loop was:

```text
Resources
→ Options
→ Capability
→ Effect
→ Knowledge
→ more Resources and Options
```

R4–R7 make it more accurate:

```text
Reality
  ↓ observe / discover
Resource identities + owner-native Claims/Events
  ↓ demand-scoped Actionability / Requirements / Assignments
Options / feasible compositions
  ↓ selection + admission
Actions
  ↓
Effects + resource-family accounting
  ↓ domain evaluation
Outcomes
  ↓ causal evidence
Attribution
  ↓ semantic promotion
Knowledge / improved Capability
  ↓
changed discovery / acquisition / maintenance / retirement decisions
  ↓
possibly more useful Resources and Options
```

And now there is a missing branch that the old flywheel hid:

```text
                   ┌── positive feedback
Knowledge/Capability
                   └── negative feedback
                       maintenance / complexity /
                       cost / attack surface /
                       deskilling / correlated dependence
```

So the Resource ecology is not a growth engine.

It is an **adaptive system with stocks where real, flows where real, relations where real, and feedback of either sign.**

---

# 31. What R7 rejects

1. No universal scalar Resource balance.
2. No assumption that every use depletes a Resource.
3. No assumption that every restoration is replenishment of a prior stock.
4. No universal Stock–Flow–Capacity vector for every Resource.
5. No canonical one-family-per-Resource registry/lifecycle from R7.
6. No collapse of Reservation into Consumption.
7. No release-by-guess after failed/UNKNOWN Effect.
8. No interpretation of Resource/catalog count as current capacity.
9. No interpretation of replica/copy count as semantic Resource count.
10. No interpretation of currentness loss as depletion.
11. No interpretation of expiry/revocation as deletion of every lower artifact/result.
12. No universal decay equation.
13. No assumption that reacquisition/readmission resurrects old generation identity.
14. No assumption that reusable Knowledge is depleted by use.
15. No automatic causal credit for recursive Resource growth.
16. No monotonic `more Resources = more value` law.
17. No maximize-utilization objective.
18. No global scalar conversion between bytes, USD, tokens, Jobs, requests, time, attention or skill.
19. No GlobalResourceLedger / ResourceFamilyRegistry / universal renewal scheduler.
20. No immediate production fix for R7P01 until a real consumer earns the shared representation.

---

# 32. What R7 resolves enough for R8

R7 provisionally retains these laws.

### Resource identity is not dynamic quantity

A Resource/aspect can remain identifiable while quantity, materialization, currentness or authority changes.

### Quantity/capacity/rate are optional owner-native Claims

Use them where they materially constrain the target transition, in native units.

### Reservation is first-class when capacity is precommitted

It changes current Options before final Effect and may remain held under uncertainty.

### Release is a later Event/transition

It changes current availability without erasing reservation history.

### Consumption/depletion is family-specific

Some resources deplete; some renew; some are non-rival; some only change applicability/currentness.

### Renewal/replenishment/reacquisition are different mechanisms

None is automatically the inverse of the prior event.

### Currentness/availability is relational

A Resource may be usable in one relation and unusable in another simultaneously.

### Replicas/materializations are relations to Resource identity

They matter to durability/recovery without automatically multiplying semantic Resources.

### Decay and maintenance are mechanism-specific

Skill, compatibility, evidence and infrastructure decay through different clocks/processes.

### Feedback has sign

Resources/Capability can create new Resources/Options, but also maintenance, complexity, attack surface or deskilling.

### Recursive creation needs R6 Attribution

Do not infer a flywheel from temporal adjacency.

---

# 33. R8 handoff — Evidence Resource branch

R7 now makes R8 much sharper.

Evidence is a particularly important Resource family because it combines several unusual dynamics:

```text
usually non-rival
replicable
can become stale without bytes disappearing
may have source/claim-specific currentness clocks
can be superseded without historical falsification
can increase decision value through combination
can become less useful through correlation/redundancy
may create Knowledge after promotion
can alter future Resource discovery/acquisition
```

R8 should therefore ask:

```text
What exactly is an Evidence Resource?
When does evidence existence differ from evidence actionability?
How does source identity differ from claim support?
How do freshness, applicability and transportability decay?
When do multiple pieces create epistemic redundancy versus correlated repetition?
How do negative results and failed experiments remain useful Resources?
When does evidence become Knowledge, and when must it remain only evidence?
How should evidence value-of-information affect action under reversibility/cost/risk?
Can direct target-native evidence calibrate external/synthetic evidence without becoming an epistemic monopoly?
```

R8 must preserve R7's rule:

```text
Evidence bytes/count
≠ evidence capacity/value
```

and R6's rule:

```text
Evidence
≠ automatic Knowledge
```

No EvidenceGraph or universal score is authorized before R8 falsification.

---

# 34. Conclusion

The intuitive Resource Ecology starts as accounting:

```text
get resources
spend resources
renew resources
accumulate more resources
```

R7 finds a thinner and more general structure.

Some resources really are stocks.
Some are flows.
Some constrain capacity.
Some are reservations.
Some are temporary authority.
Some are relationships whose currentness changes.
Some are replicas of one identity.
Some decay without disappearing.
Some are non-rival and reusable.
Some create new Options while simultaneously adding maintenance or dependency.

The root law is therefore:

> **Do not ask every Resource for a balance. Ask the native owner which dynamic facts materially constrain the named transition now, preserve those facts in their native units and clocks, and derive the current ecology only at the consuming boundary.**

And the feedback law is:

> **Resource growth, Capability growth and Knowledge growth are not automatically virtuous or causal. Preserve signed costs and require evidence-backed Attribution before promoting a recursive flywheel claim.**

D currently survives 60/60 frozen and post-freeze falsifiers, including an independently completed concurrent Finance temporal-identity model. It remains provisional research, not canonical World doctrine.
