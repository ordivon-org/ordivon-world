---
schema_version: 1
id: world.resource-ontology-r6-conversion-falsification
title: Resource Ontology R6 — Action / Effect / Outcome / Attribution / Knowledge Falsification
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
summary: Falsifies collapsed and universally linear Resource conversion chains; separates Action from owner-native Effect history, domain-owned Outcome evaluation, causal Attribution, promoted Knowledge, and resource-family-specific Consumption.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-ontology-r4-lifecycle-falsification
  - world.resource-ontology-r5-composition-falsification
  - world.resource-option-capability-model
---
# Resource Ontology R6 — Action / Effect / Outcome / Attribution / Knowledge Falsification

## 1. Question

R0–R5 established that Resource reasoning cannot be reduced to object existence, one lifecycle, or one composition graph. R6 attacks the next compression:

```text
Capability
→ Effect
→ Knowledge
```

A more careful candidate is tempting:

```text
Option
→ Action
→ Consumption
→ Effect
→ Outcome
→ Attribution
→ Knowledge
```

R6 asks whether even this longer chain is still too linear.

The deletion criterion remains strict:

> A conversion distinction survives only when deleting it changes what happened, what is currently known, which domain conclusion is justified, causal credit/blame, next admissible action, recovery, or future selection.

No R6 result is canonical production doctrine.

---

# 2. Frozen evidence boundary

Canonical World base:

```text
9e60e1b3c5d99d8dce1ec8168a99ba2fc791d2d8
```

R6 froze World plus eight sibling owners after revalidating clean worktrees and exact revisions. The selected corpus was then byte-compared against each frozen Git commit.

| Owner | Revision |
| --- | --- |
| world | `9e60e1b3c5d99d8dce1ec8168a99ba2fc791d2d8` |
| finance | `7d812d8d41d5ba6b8aa619886beddca94327b11f` |
| runtime | `c6e45d9e41d3b4d64b5b3dace01497c53e574026` |
| workstation | `85f904635e856612b78e8b13acc553b1e80d292a` |
| studio | `52f646022cc606985a63a5fd290c417fd337e80e` |
| security | `6a7a8f9b22cb4995d436da2968b135248f8f6bb3` |
| game | `0c8581c6b5eebceaf33aeb8907fa91a8b53708dc` |
| human | `f7725dfc9b391c3e9a0c509d49795994931c9d63` |
| harness | `286985c82874d293308297f66b23152c1ed53369` |


Source-integrity audit:

```text
frozen repositories                 9
selected exact source files        25
worktree bytes == frozen commit    PASS
```

The corpus includes direct execution/recovery evidence from Runtime, reconciled capital/effect/performance semantics from Finance, Game domain-value evidence, Studio render/review boundaries, Security scientific outcomes, Human capability-transfer evidence, and Harness completion/knowledge-promotion boundaries.

R6 also executed three current-system probes rather than relying only on documents.

---

# 3. Three direct R6 probes

## R6P01 — successful physical execution does not create semantic completion

Runtime Job:

```text
job-01a00588-999d-7491-8a64-cec8fa64f2c2
```

The admitted command emitted:

```text
R6_PHYSICAL_MARKER
```

and exited zero.

Runtime established physical success and durable result evidence while still projecting:

```text
semanticCompletionEvaluated = false
```

Therefore:

```text
Action admitted
+ process Effect succeeded
≠ domain Outcome proven
```

## R6P02 — an Action can exist when the intended execution fails

Runtime Job:

```text
job-01a00588-b48e-7842-8220-c3135db6d835
```

The admitted command emitted a marker and then exited `23`.

The durable Job/Attempt/result/evidence exist, but execution disposition is failed.

Therefore Action cannot be defined as “successful Effect.”

## R6P03 — current `ConsumptionOutcome` compresses materially different histories

Current World exposes a narrow ranking input:

```text
ConsumptionOutcome(
    resource_id,
    workload_id,
    observed_at,
    useful: bool,
    value: 0..1,
    evidence_refs
)
```

R6 held all Resource, demand, owner and transport facts fixed and compared:

```text
History A
  one excellent useful outcome: value=1.0
  one failed outcome

History B
  one moderate useful outcome: value=0.5
```

Current result for both:

```text
potential_score  = 0.630435
evidence_quality = 1.0
decision         = consumable-now
```

So the current prior cannot distinguish bimodal `excellent + failure` from one moderate success.

This is a real semantic compression debt, but it does **not** justify replacing `ConsumptionOutcome` with a universal Outcome database/schema in R6. Its current role remains a narrow planning prior.

---

# 4. Four frozen conversion models

## A — Collapsed Effect / Success Model

> A selected/admitted capability that executes successfully is treated as the realized Outcome; process/provider/domain success collapse into one effect/result, causal credit is implicit, consumption is associated with successful use, and only successful effects normally update Knowledge.

This is the implicit model behind phrases such as:

```text
it ran successfully
therefore it worked
therefore it was useful
therefore we learned that the resource is good
```

## B — Action–Effect Ledger

> Action and Effect are distinct. An Action is an admitted/committed attempt and owner-native Effect history may be succeeded, failed or unknown. Domain Outcome remains folded into Effect/result semantics, Attribution is implicit or optional metadata, and Knowledge is derived from retained Action/Effect history without a separate semantic promotion boundary.

B fixes physical ambiguity and recovery, but still assumes that recording what directly happened is close enough to recording domain success.

## C — Full Linear Conversion Chain

> One selected Option/feasible assignment advances through a directional chain: Action -> resource consumption -> Effect -> Outcome -> Attribution -> Knowledge. The stages are semantically distinct and may be unavailable/negative, but the episode remains fundamentally linear: Outcome is downstream of Action/Effect, Attribution is downstream of Outcome, and Knowledge is downstream of Outcome/Attribution.

C is intentionally strong. It makes Action, Effect, Outcome, Attribution and Knowledge distinct and permits negative/unavailable stages.

Its remaining assumption is structural:

```text
one episode flows downstream
from Action toward Knowledge
```

## D — Action/Effect Events + Outcome/Attribution Projections

> Selection/Decision may commit an Action: an identity-bound admitted attempt to cause or obtain a transition. Owner-native Effect events/claims record direct physical or semantic consequences and may be success, failure, no-effect or unknown. Outcome is a domain-owned evaluation projection over one or many Effects, exogenous facts, objective/observer/horizon and comparison context; it may be positive, negative, neutral or unavailable. Attribution is a separate causal/credit claim with explicit evidence and uncertainty and may remain unavailable even when Outcome is known. Knowledge is an externally/domain-promoted reusable claim that can arise from successful, failed, invalid or uncertain episodes when evidence changes future prediction/selection. Consumption is resource-family-specific Event/quantity accounting during the attempt/effect window, not a universal stage. Relations are many-to-many rather than one mandatory lifecycle.

D removes the universal lifecycle assumption.

Its root picture is:

```text
Decision / Selection
        │
        ├── may commit ──► Action Event
        │                    │
        │                    ├──► direct Effect Claims / Events
        │                    │       success / failure / no-effect / unknown
        │                    │
        │                    └──► resource-family Consumption Events / quantities
        │
Reality / exogenous events ──┴──────────────┐
                                             ▼
                                  Domain Outcome Projection
                                  objective / observer / horizon /
                                  comparison / evidence completeness
                                             │
                         ┌───────────────────┴───────────────────┐
                         ▼                                       ▼
                 Attribution Claims                       future Decisions
                 causal / credit / blame                        │
                         │                                      │
                         └──────────────┬───────────────────────┘
                                        ▼
                              Knowledge Promotion
                         reusable claim only when earned
```

---

# 5. Falsification result

| Model | Result across 40 frozen discriminators |
| --- | --- |
| A — Collapsed Effect/Success | 0 PASS / 38 FAIL / 2 AMBIG |
| B — Action–Effect Ledger | 9 PASS / 28 FAIL / 3 AMBIG |
| C — Full Linear Conversion Chain | 34 PASS / 3 FAIL / 3 AMBIG |
| D — Event/Projection model | 40 PASS / 0 FAIL / 0 AMBIG |

D was then frozen and attacked with eight new cases. It survives all eight without wording change, giving the current survivor a `48/48` falsifier surface.

This is falsifier evidence, not universal proof.

## 5.1 Complete frozen matrix

| ID | Source | Pressure | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | `R6P01` A real Runtime Job exited zero and produced the requested marker while semanticCompletionEvaluated remained false | physical success vs semantic outcome | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C02 | `R6P02` A real admitted Runtime Job produced a marker then exited 23; durable result/evidence exist while executionDisposition is failed | action vs failed effect | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C03 | `R02` Runtime resultAvailable can coexist with reconciliation-required/unknown and does not mean semantic correctness | terminal result vs certainty/correctness | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C04 | `R03` Missing Runtime Result does not prove either physical success or physical failure | effect uncertainty | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C05 | `R01` Successful process exit does not prove semantic completion or external-world success | effect vs domain outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C06 | `R06` Structured release external receipt can become terminal before generic Job lifecycle converges | nonlinear effect timing | AMBIG `A-ACCIDENTAL` | PASS `B-ACTION-EFFECT` | AMBIG `C-OVERLINEAR` | PASS `D-PROJECTION` |
| C07 | `R05` Workspace Patch prepared state can reconcile to unknown when physical files are mixed | partial/unknown effect | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C08 | `R07` Runtime cancellation controls lifecycle but cannot prove external side effects already performed by target | control action vs prior effects | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C09 | `F01` Finance A8 does not infer external financial success from submit response; independent observations are required | action/dispatch vs effect | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C10 | `F02` Venue Fill proves execution quantity/price but does not itself create a cash-ledger entry | multiple effect truth types | FAIL `A-CONFLATES` | PASS `B-ACTION-EFFECT` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C11 | `F03` Funding, interest, distributions and other bills can change capital while Agent takes no A7 action | exogenous effect/outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | FAIL `C-LINEARITY-BREAK` | PASS `D-PROJECTION` |
| C12 | `F10` Reconciled order/fill/bill/post-portfolio consequence establishes execution truth before completion but not owner-value success | effect completion vs domain outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C13 | `F04` Positive nominal owner return is not automatically positive real return | outcome depends on comparison/context | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C14 | `F05` Empty Capital Ledger is not proof of no external flow; performance can remain unavailable without coverage | outcome evidence completeness | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C15 | `F06` Only finalized effect-linked ledger entries receive causal cash credit; unresolved effects receive zero credit | attribution gate | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C16 | `F07` Effect-linked causal cash credit still does not prove Agent alpha; counterfactual value-added remains unavailable | attribution vs causal value claim | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C17 | `F08` Snapshot equity can move by mark-to-market and other non-ledger mechanisms outside exact Agent effect lineage | outcome without action lineage | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | FAIL `C-LINEARITY-BREAK` | PASS `D-PROJECTION` |
| C18 | `F09` Full diagnostic treatment used about 2.16x tokens without changing sealed selection/result | resource consumption vs outcome gain | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C19 | `G01` Two 20-Turn browser products are executable but materially distinct human experience is unproven | technical effect vs human outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C20 | `G02` Commander choices have machine-level causal leverage while strategic ownership/prediction/acceptance remain unproven | mechanical causal effect vs player outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C21 | `G03` Pressure meters reach planning/damage thresholds while anticipation/fairness remains the open player question | world effect vs experience outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C22 | `G04` Live cognition changes local behavior but improvement in player value and indispensability remain unproven | behavior effect vs product outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C23 | `G05` Reproduced player-facing implementation leak was fixed at L2 and re-probed without changing planning/World core | localized attribution | AMBIG `A-ACCIDENTAL` | AMBIG `B-PARTIAL` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C24 | `G06` Browser/E2E and simulation completion are explicitly not evidence that a feature is fun | test effect vs player value | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C25 | `S01` Exact reproducible A/V candidate is rendered/review but not approved/published because voice naturalness is human-uncertain | render effect vs production/human outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C26 | `S02` Technical success plus bounded semantic improvement does not automatically promote candidate Asset | effect vs promotion | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C27 | `S03` Studio separates render evidence from decision context used for semantic judgment | effect evidence vs outcome criteria | FAIL `A-CONFLATES` | AMBIG `B-PARTIAL` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C28 | `S04` Agent can falsify obvious issues but cannot establish human understanding/preference/trust/recall/enjoyment | machine judgment vs human outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C29 | `S05` One Output may be approved while parent Production remains review | multiple nested outcome scopes | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | AMBIG `C-OVERLINEAR` | PASS `D-PROJECTION` |
| C30 | `Q01` Security separates procedural outcome, containment outcome and scientific assessment | multiple outcome domains | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | AMBIG `C-OVERLINEAR` | PASS `D-PROJECTION` |
| C31 | `Q02` Single-use Activation remains consumed even though trial failed before Windows boot and scientific question stayed unresolved | consumption without target effect/outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C32 | `Q03` Scientifically invalid loader trial still produced methodological knowledge about projection provenance | knowledge from invalid/no scientific outcome | FAIL `A-CONFLATES` | AMBIG `B-PARTIAL` | FAIL `C-LINEARITY-BREAK` | PASS `D-PROJECTION` |
| C33 | `Q04` Runtime-backed Security P0-C proves physical lifecycle but does not prove strategic value | physical effect vs strategic outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C34 | `Q_AGENT` One model completion failed before Trial sealing; Runtime/software fact survives without a sealed domain Trial | layer result vs domain episode | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C35 | `Q05` Treating the whole Agent stack as opaque makes failures/improvements unattributable; layer isolation is required | attribution as separate claim | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C36 | `H01` Immediate assisted output is not retained Human capability | assisted effect vs retained outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C37 | `H02` Human+model system capability can be valuable without internalized Human capability | boundary-relative outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C38 | `H03` AI assistance can improve immediate performance while reducing later unassisted performance | outcome horizon reversal | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C39 | `H04` Human research rejects one augmentation score and keeps a multidimensional outcome vector | non-scalar outcome | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |
| C40 | `HA02` Harness structured CompletionProposal/procedure candidate requires external evaluation/promotion before reusable knowledge | candidate/effect vs knowledge promotion | FAIL `A-CONFLATES` | FAIL `B-NO-DOMAIN-OUTCOME` | PASS `C-LINEAR` | PASS `D-PROJECTION` |

---

# 6. A fails because execution success is not value success

A fails almost everywhere because different truth owners answer different questions.

Runtime can truthfully answer:

```text
was a Job admitted?
was an Attempt dispatched?
did the process exit?
what bytes/artifacts were retained?
is the effect known, failed, or unknown under this effect contract?
```

Runtime cannot generally answer:

```text
did the trade improve owner capital?
was the game fun?
was the film publication-worthy?
did the experiment answer the scientific question?
did the Human retain capability?
```

These are not missing Runtime fields. They are different semantic questions.

The same pattern reproduces independently across Finance, Game, Studio, Security and Human.

---

# 7. Action survives deletion

R6 provisionally defines an **Action** as:

> **An identity-bound admitted or committed attempt by an actor/system to cause or obtain a target transition under a specific authority/context.**

Action is not success.

An Action may end in:

```text
Effect succeeded
Effect failed
no relevant Effect observed
Effect outcome unknown
partial/multiple Effects
```

R6P01/R6P02 directly prove the distinction.

Finance provides a stronger external example: submitting an order is not execution success. A8 independently observes order state, fills, bills and post-effect portfolio state before reconciliation.

Therefore:

```text
Decision/Selection ≠ Action
Action ≠ Effect
```

Selection can remain local and never dispatch. Action begins only when the domain/effect boundary admits the attempt.

---

# 8. Effect survives deletion—but remains owner-native

An **Effect** is the direct consequence that an owner can truthfully establish about its own effect boundary.

Examples:

```text
Runtime:
  process exited 0
  Patch bytes equal committed after-state
  release receipt exists
  effect remains UNKNOWN

Finance venue/account:
  order observed live
  fill occurred at quantity/price
  bill changed balance
  post-effect portfolio snapshot observed

Game:
  authoritative Turn resolution changed World state

Studio:
  exact artifact bytes were rendered

Security:
  Windows boot did/did not occur
  module load did/did not occur under observed envelope
```

Effects can be plural. Finance deliberately keeps Fill, Bill, Order state and PortfolioSnapshot as different truths.

An Effect receipt/history must not be promoted into another owner's Outcome claim.

---

# 9. Effect uncertainty is first-class

R6 retains:

```text
UNKNOWN
```

rather than forcing every Action into success/failure.

Runtime already establishes this operationally:

```text
missing result
≠ success
≠ failure

resultAvailable
≠ semantic correctness

response loss / mixed mutation
→ reconcile original identity
not speculative redispatch
```

This matters at the World level because unknown Effect truth changes next admissible action and causal inference.

Unknown is therefore not merely a UI status. It is an epistemic/recovery condition attached to the exact owner-native effect claim.

---

# 10. Outcome survives deletion—but no universal Outcome schema is earned

An **Outcome** answers a different question:

> **Given one or more observed Effects plus relevant exogenous facts, what do they mean for the consuming domain's objective, observer, horizon and comparison context?**

Conceptually:

```text
Outcome = DomainEvaluation(
    effects,
    exogenous facts,
    objective,
    observer,
    horizon,
    comparison context,
    evidence completeness
)
```

This is a projection, not necessarily one persisted object.

## Finance

A perfectly reconciled trade Effect can still lead to negative owner-capital Outcome.

Even positive nominal capital return is not automatically positive real return. Inflation evidence changes the evaluation.

## Game

Twenty technically successful Turns establish executable gameplay. They do not establish delight, strategic ownership, suspense, replay desire or market value.

## Studio

A deterministic exact-byte render may remain `rendered / review` because a publication-critical human voice-quality judgment remains unresolved.

## Security

One experiment can simultaneously have:

```text
procedural outcome
containment outcome
scientific assessment
```

They are not one scalar result.

## Human

Assisted output can improve while delayed unassisted capability declines.

The correct Human outcome is horizon- and objective-dependent.

Therefore R6 rejects one universal `Outcome(value=...)` ontology.

---

# 11. Outcome is not necessarily downstream of an Agent Action

This is the first hard failure of C.

Finance explicitly observes capital changes that occur while the Agent does nothing:

```text
funding
interest
distributions
venue bills
mark-to-market
external owner flows
```

These may affect owner-capital Outcome without any A7 Agent Action lineage.

So the universal relation:

```text
Action → Effect → Outcome
```

is false as a graph of Reality.

A narrower episode can certainly have that lineage, but the domain Outcome projection must also admit exogenous Effects and facts.

This is why D models Outcome over evidence, not as the next state after Action.

---

# 12. Outcome is contextual and horizon-dependent

R6 finds several independent effect modifiers on Outcome semantics:

### Objective

```text
nominal capital gain
≠ real-capital objective satisfaction
```

### Observer

```text
Agent visual inspection
≠ fresh-player experience
≠ human listener preference
```

### Horizon

```text
immediate assisted performance rises
later unassisted performance falls
```

### Comparison

```text
positive return
≠ Agent alpha
```

unless the counterfactual benchmark is actually defined and evidenced.

Therefore an Outcome claim should always make the relevant domain evaluation boundary recoverable. R6 does not prescribe one shared field list because different domains legitimately require different dimensions.

---

# 13. Attribution survives as a separate causal claim

Observed Outcome does not answer:

> **Why did this happen, and which Action/Resource/Agent/environment deserves causal credit or blame?**

Finance provides the strongest current implementation example.

It can safely follow exact lineage:

```text
Capital Ledger entry
→ finalized reconciliation
→ ExternalEffect
→ Proposal
→ Decision
→ execution actor
```

But this only supports bounded causal cash credit.

It still refuses to call the remainder:

```text
Agent alpha
```

because mark-to-market, passive exposure and absent counterfactual evidence remain outside that causal claim.

Security reaches the same conclusion experimentally: if Provider, Harness, Host, Runtime and Security are varied together as one opaque Agent, improvements/failures become unattributable.

Game GV reaches the same conclusion operationally: a reproduced player-facing leak was localized to L2 expression and pressure stopped there; no evidence justified changing planning or World rules.

Thus:

```text
Outcome known
≠ Attribution known
```

Attribution may be:

```text
supported
partial
competing
unavailable
```

without invalidating the observed Outcome.

---

# 14. Consumption is parallel accounting, not a universal stage

R4 already rejected `consumed` as a terminal Resource state. R6 goes further.

Consumption cannot be placed universally here:

```text
Action → Consumption → Effect
```

because different resources behave differently.

Security provides a decisive case:

```text
single-use Activation consumed
→ trial failed before Windows boot
→ intended loader Effect absent
→ scientific question unresolved
```

Finance/Harness can spend:

```text
tokens
provider calls
fees
capital capacity
```

without improving Outcome.

Human work can spend:

```text
attention
time
effort
```

while assistance changes immediate output but not retained skill.

Knowledge and software are often non-rival: they may participate repeatedly without depletion.

Therefore Consumption belongs to resource-family-specific accounting:

```text
ConsumptionEvent / quantity / reservation / depletion / renewal
```

that occurs during or around an Action/Effect episode.

R7 should later investigate stock/flow/renewal/decay semantics. R6 does not invent a universal consumption ledger.

---

# 15. Knowledge is not just the final success state

The second hard failure of C is Security's invalid loader trial.

The target scientific Outcome was not established. The trial was scientifically invalid for the loader-causality question.

Yet the failure exposed a new methodological fact:

```text
Environment identity
≠ Subject projection provenance
```

That knowledge changed future experimental admission.

So:

```text
failed / invalid Outcome
```

can still yield valuable Knowledge.

But R6 does not conclude that every failure automatically becomes knowledge.

Harness P1 provides the opposite guardrail:

```text
bounded Run
→ procedure candidate
→ external evaluator
→ external promotion
→ reusable exact source
→ future explicit admission
```

A `CompletionProposal` is not semantic completion or automatic persistent learning.

Therefore R6 provisionally defines Knowledge as:

> **A reusable claim/model/procedure promoted by the appropriate semantic owner because evidence materially changes future prediction, selection, verification or recovery.**

Evidence is input to Knowledge. Evidence presence is not automatic Knowledge promotion.

---

# 16. Many-to-many replaces one-to-one conversion

C's linear chain is useful locally but cannot be the general ontology.

R6 needs at least these cardinalities:

```text
one Action → many Effects
many Actions/Effects → one Outcome
one Effect → several domain Outcome projections
one Outcome → several competing Attribution claims
one failed/invalid episode → Knowledge
no Agent Action → exogenous Effect → Outcome
```

Examples:

- one financial order can produce order-state, multiple fills, fees/bills and portfolio changes;
- one monthly owner-capital Outcome aggregates many trades, funding flows, mark-to-market and external flows;
- one Studio Output can be approved while the whole Production remains in review;
- one Security experiment has procedural, containment and scientific evaluations simultaneously;
- one Runtime release receipt can become externally terminal before the generic Job lifecycle converges.

The system therefore needs causal/evidentiary relations, not a universal one-row lifecycle.

---

# 17. Relation ledger after R6 reduction

| Concept | Placement | Verdict | Cases | Why |
| --- | --- | --- | --- | --- |
| Decision/Selection | `upstream choice of Option/feasible assignment` | **RETAIN_SEPARATE_FROM_ACTION** | C09, C18, C20 | A decision can exist without external dispatch; changing decision quality and executing it are separate truths. |
| Action | `identity-bound admitted/committed attempt to cause or obtain transition` | **REQUIRED** | C01, C02, C08, C09 | Deleting Action erases the difference between attempted/admitted work and what physically or semantically happened. |
| Effect | `owner-native direct consequence Event/Claim: success/failure/no-effect/unknown` | **REQUIRED** | C03, C05, C09, C10, C33 | Physical/semantic consequence history remains true independently from higher-domain value. |
| Outcome | `domain-owned evaluation projection over effects + exogenous context + objective/observer/horizon/comparison` | **REQUIRED_BUT_NOT_GLOBAL_SCHEMA** | C12, C19, C25, C30, C36 | Execution truth cannot answer whether capital, player experience, creative work, science or retained Human capability improved. |
| Outcome context/horizon | `parameters of domain evaluation` | **REQUIRED** | C13, C21, C28, C38 | The same effects can evaluate differently under inflation benchmark, player perception, audience, or delayed retention horizon. |
| Attribution | `separate causal/credit Claim with evidence and uncertainty` | **REQUIRED** | C15, C16, C23, C35 | Observed Outcome does not automatically identify which action/resource/agent/environment caused it. |
| Knowledge | `owner/domain-promoted reusable Claim that changes future prediction/selection` | **REQUIRED_PROMOTION_BOUNDARY** | C32, C40 | Evidence or a completion candidate does not automatically deserve durable reusable Knowledge; failures/invalid trials may still teach. |
| Consumption | `resource-family-specific Event/quantity relation during Action/Effect window` | **PARALLEL_NOT_STAGE** | C18, C31, C38 | Tokens, attention or single-use authority may be consumed even when target Effect/Outcome fails; non-rival knowledge may be reused without depletion. |
| Effect uncertainty | `owner-native unresolved/unknown effect state or claim` | **REQUIRED** | C03, C04, C07 | Unknown is not success/failure and must block unsafe inference/retry while preserving the Action identity. |
| Multiplicity | `many-to-many relation among Actions, Effects and Outcomes` | **REQUIRED** | C06, C10, C17, C29 | One action can create several effects; one long-horizon outcome can aggregate many effects; some effects/outcomes are exogenous. |
| Evidence completeness | `support condition for Effect/Outcome/Attribution claims` | **REQUIRED_CONDITION_NOT_NEW_OWNER** | C14, C27, C40 | Empty/missing observations cannot be promoted to absence or outcome truth; source/domain owners retain evidence semantics. |
| Promotion/persistence | `owner/domain decision to retain consequential Knowledge/Outcome/Attribution evidence` | **CONDITIONAL** | C26, C32, C40 | Technical success, critique or candidate completion should not automatically become selected asset, scientific conclusion or reusable procedure. |

The important compression is that only a small number of distinctions survive as root semantics.

---

# 18. Deletion and rejected-addition tests

| Mutation | Result | Cases | Why |
| --- | --- | --- | --- |
| delete Action as distinct from Effect | **FAIL** | C01, C02, C08, C09 | Cannot distinguish admitted attempt/dispatch from succeeded, failed, unknown or absent consequences. |
| delete Effect as distinct from Outcome | **FAIL** | C05, C12, C19, C25, C33 | Physical/semantic execution truth would be misused as domain-value truth. |
| delete Outcome/domain evaluation | **FAIL** | C12, C19, C25, C30, C36 | The system loses the actual consumer/domain objective and can optimize substrate success instead. |
| delete Attribution | **FAIL** | C15, C16, C23, C35 | Outcome observation alone cannot assign causal credit or blame to Action, Resource, Agent or environment. |
| delete Knowledge promotion boundary | **FAIL** | C32, C40 | Raw failure/completion evidence would automatically become durable reusable knowledge without semantic evaluation. |
| force Outcome to be downstream of an Agent Action | **REJECT_ADD** | C11, C17 | Capital and other domain outcomes can change through exogenous effects without an Agent action lineage. |
| force one Action -> one Effect -> one Outcome | **REJECT_ADD** | C06, C10, C29 | Multiplicity and nested outcomes are real; exact one-to-one lineage is not universal. |
| force Knowledge to require resolved positive Outcome + Attribution | **REJECT_ADD** | C32, C34 | Invalid/failed/uncertain episodes can produce methodological or recovery knowledge. |
| make Consumption a universal stage between Action and Effect | **REJECT_ADD** | C31, C18, C38 | Consumption is resource-family accounting; it may occur before failure, be partial, renewable, rival, or non-rival. |
| collapse Outcome into one scalar useful/value score | **REJECT_ADD** | C13, C30, C38, C39, R6P03 | Outcome can be multidimensional, horizon-dependent and distributional; current scalar prior loses failure structure. |
| allow Effect owner/receipt to assert higher-domain Outcome | **REJECT_ADD** | C05, C12, C25, C33 | Runtime/provider/render receipts do not own Finance/Game/Studio/Security/Human semantic value. |
| automatically persist every effect/review/completion as Knowledge | **REJECT_ADD** | C26, C32, C40 | Durable promotion requires consequential semantic evaluation; most critique/results remain local evidence. |

Five structures fail deletion:

```text
Action
Effect
Outcome/domain evaluation
Attribution
Knowledge promotion boundary
```

Everything else is either a condition, relation, resource-family accounting concern, or an over-generalized lifecycle addition.

---

# 19. Why B is not enough

B is operationally much better than A.

It handles:

```text
admitted Action
succeeded Effect
failed Effect
UNKNOWN Effect
reconciliation
recovery
```

This is exactly why Runtime's effect model is strong.

But it still cannot answer domain-value questions.

If World stopped at B, it could tell us that:

```text
trade filled
Turn resolved
video rendered
experiment ran
model completed
```

without asking whether:

```text
capital utility improved
player value improved
artifact quality/fitness improved
scientific question was answered
Human capability transferred
```

That would recreate the central consumer-layer failure from another direction: excellent substrate evidence with no explicit domain objective.

---

# 20. Why C is strong but still over-linear

C is not rejected because its stage distinctions are wrong. They are mostly valuable.

Its result is:

```text
34 PASS / 3 FAIL / 3 AMBIG
```

The three FAIL cases are structural:

### C11 — exogenous capital effects

Funding/interest/distributions can affect capital without an Agent Action.

### C17 — mark-to-market/non-ledger change

Owner-capital Outcome can change outside exact effect lineage.

### C32 — invalid experiment creates method Knowledge

Knowledge can be earned even when the target scientific Outcome is not established and target Attribution is not resolved.

The three AMBIG cases expose weaker pressure:

```text
Effect receipt timing can cross generic Job lifecycle order.
Output outcome and Production outcome can coexist.
One Security experiment has several outcome domains.
```

So C remains a useful **episode narrative**:

```text
selected Option
→ Action
→ Effects
→ Outcome evaluation
→ Attribution
→ Knowledge update
```

but not a universal Resource lifecycle or graph topology.

D retains the vocabulary while removing mandatory ordering/cardinality.

---

# 21. Truth ownership after R6

R6 reinforces a strict ownership rule.

## Effect owner

The owner of the physical/semantic boundary may prove what happened there.

Examples:

```text
Runtime/provider/venue/Game reducer/render pipeline
```

## Outcome owner

The domain that owns the objective/evaluation decides what those facts mean for domain value.

Examples:

```text
Finance → owner capital / continuation / benchmark-relative performance
Game    → player experience / strategy / replay value
Studio  → production fitness / craft / human response
Security→ scientific/defensive understanding under study question
Human   → retained capability / agency / well-being dimensions
```

## Attribution owner

A domain/research mechanism may assert causal lineage only to the strength supported by its design and evidence.

## Knowledge owner

The consumer/domain/research owner promotes reusable conclusions. Harness/Runtime can preserve exact evidence and admission, but do not decide semantic truth merely because they executed the episode.

Architectural law candidate:

> **Lower layers prove direct Effects. Consuming domains evaluate Outcomes. Causal Attribution and Knowledge promotion require their own evidence and owners.**

---

# 22. Outcome evidence completeness is not optional

Finance gives a precise negative example:

```text
Capital Ledger empty
```

does not prove:

```text
no external capital flow
```

unless the exact source query/coverage is complete.

Similarly:

```text
no fills in a failed/partial query
```

does not prove no fills.

Studio similarly separates render evidence from decision context; Security separates missing observation from scientific negative result; Runtime preserves UNKNOWN after ambiguous effect paths.

Therefore an Outcome/Attribution projection may need to return:

```text
unavailable / unknown / insufficient evidence
```

rather than manufacture a score.

Evidence completeness remains owner-native. R6 does not create a global EvidenceCompleteness service.

---

# 23. Fresh post-freeze falsifiers

D's wording was frozen before these eight cases were authored:

| ID | Fresh case | D |
| --- | --- | --- |
| R6Y01 | One admitted API action writes a provider object, emits a bill, and updates an audit log; one Action has several distinct Effects with different owners. | PASS `D-MULTI-EFFECT` |
| R6Y02 | A monthly capital Outcome is evaluated over hundreds of trades, funding bills, mark-to-market changes and owner flows rather than one Action. | PASS `D-MULTI-ACTION-OUTCOME` |
| R6Y03 | A venue funding payment changes capital while the Agent takes no action; Outcome observation exists without Action lineage. | PASS `D-EXOGENOUS` |
| R6Y04 | An order is correctly filled and reconciled but the position subsequently loses money; Effect succeeds while domain Outcome is negative. | PASS `D-NEGATIVE-OUTCOME` |
| R6Y05 | An external request becomes outcome-unknown, later reconciliation resolves the Effect, while the earlier ambiguity teaches a recovery rule before any value Outcome is known. | PASS `D-UNKNOWN-KNOWLEDGE` |
| R6Y06 | A rate-limit token, Human attention block or single-use Activation is consumed by an attempt that fails before its intended Effect. | PASS `D-CONSUMPTION-PARALLEL` |
| R6Y07 | A portfolio Outcome is positive and fully measured but Agent contribution remains unavailable because no evidence-backed counterfactual exists. | PASS `D-ATTRIBUTION-UNAVAILABLE` |
| R6Y08 | An invalid experiment answers none of the target scientific question but exposes a measurement/provenance flaw that is promoted into future method Knowledge. | PASS `D-FAILURE-KNOWLEDGE` |

All eight pass without changing D.

The most important pressures are:

- one Action creating several Effects;
- long-horizon Outcome aggregating hundreds of Actions/Effects;
- exogenous Effects without Agent Action;
- successful Effect plus negative Outcome;
- recovery Knowledge from an UNKNOWN episode before value Outcome exists;
- Consumption occurring before intended Effect failure;
- positive measured Outcome with unavailable Agent Attribution;
- invalid experiment producing methodological Knowledge.

---

# 24. The current `ConsumptionOutcome` production debt

R6 does not retroactively condemn the current structure.

Current `ConsumptionOutcome` has a narrow role:

```text
historical resource/workload usefulness prior
→ Resource evaluation ranking tie-breaker
```

For that narrow role it can remain useful.

What R6 disproves is the stronger interpretation:

```text
ConsumptionOutcome
= generic canonical Outcome model
```

R6P03 demonstrates two lost dimensions immediately:

```text
distribution / variance / failure structure
```

Cross-domain evidence adds more:

```text
multiple outcome dimensions
observer
horizon
comparison benchmark
exogenous effects
causal attribution
unknown/unavailable states
```

So the current class should be read as approximately:

```text
ResourceUsefulnessPriorObservation
```

semantically, even if the compatibility name is unchanged today.

Production correction requires a real consumer that needs those missing dimensions. R6 does not create a migration or schema solely to satisfy ontology aesthetics.

---

# 25. Persistence after R6

R6 does not justify a global:

```text
OutcomeRegistry
AttributionGraph
KnowledgeStore
ConversionLedger
```

Persistence follows consequence and owner truth.

Persist/reconcile when needed:

```text
exact Action identity where retry/recovery matters
owner-native Effect receipts/events
Outcome evidence when a consequential domain decision depends on it
Attribution evidence when causal credit/blame changes future action
Knowledge only after semantic promotion
resource-family Consumption accounting when stock/flow/budget continuity requires it
```

Do not persist by default:

```text
every transient critique
every model explanation
every intermediate outcome projection
every possible causal edge
every failed attempt as a promoted lesson
```

This is consistent with Studio's transient critique policy and Harness's external knowledge-promotion boundary.

---

# 26. R6 provisional root model

After R0–R6, the Resource→Effect side can now be stated more precisely:

```text
Reality
  ↓ owner-native Events + Claims
ResourceFor / ActionableResourceFor
  ↓
Transition Requirements
  ↓
Feasible Assignments / Options
  ↓ selection
Decision
  ↓ optional admission
Action
  ├── direct Effect Events / Claims
  │      success / failure / no-effect / unknown
  ├── resource-family Consumption Events / quantities
  └── evidence

Exogenous Reality Events ───────────────┐
                                         ▼
                              Domain Outcome Projection
                         objective / observer / horizon /
                         comparison / evidence completeness
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
                    Attribution                      next decisions
                    causal claim                         │
                         └───────────────┬───────────────┘
                                         ▼
                              Knowledge Promotion
                                         │
                                         ▼
                         better future Resource search,
                         composition, action and retirement
```

This is deliberately a reasoning topology, not a production schema.

---

# 27. What R6 rejects

1. No `successful execution = successful Outcome` rule.
2. No `process/provider receipt = domain completion` rule.
3. No collapse of Action into Effect.
4. No collapse of Effect into Outcome.
5. No implicit causal credit from observed Outcome.
6. No universal linear `Action → Consumption → Effect → Outcome → Attribution → Knowledge` lifecycle.
7. No requirement that every Outcome has an Agent Action ancestor.
8. No universal one-Action/one-Effect/one-Outcome cardinality.
9. No requirement that Knowledge comes only from positive resolved Outcomes.
10. No automatic Knowledge promotion from failure, critique, CompletionProposal or model reflection.
11. No universal Consumption stage/state/ledger.
12. No global scalar Outcome/value score.
13. No global Outcome schema merely because multiple domains use the word.
14. No lower effect owner asserting a higher domain's value truth.
15. No OutcomeRegistry / AttributionGraph / KnowledgeStore from R6.
16. No immediate production rewrite of `ConsumptionOutcome` merely because its name is broader than its proven semantics.

---

# 28. What R6 resolves enough for R7

R6 provisionally resolves:

### Decision / Selection

A chosen Option/assignment; may remain non-effectful.

### Action

Identity-bound admitted/committed attempt to cause or obtain a transition.

### Effect

Owner-native direct consequence Event/Claim, including failure/no-effect/UNKNOWN.

### Outcome

Domain-owned evaluation projection over Effects and exogenous facts under objective, observer, horizon, comparison and evidence context.

### Attribution

Separate causal/credit/blame claim; not implied by Outcome.

### Knowledge

Semantically promoted reusable claim/model/procedure that changes future prediction/selection/verification/recovery; may arise from success or failure.

### Consumption

Resource-family-specific stock/flow/quantity relation parallel to Action/Effect, not one universal conversion stage.

### Cardinality

Many-to-many plus exogenous inputs; a linear chain remains an optional local episode explanation, not the root ontology.

---

# 29. R7 handoff — Resource ecology dynamics

R6 now opens the next foundational question naturally:

> Once Resources participate in Actions and Effects, how are Resources created, depleted, renewed, decayed, transformed, amplified, retired and recursively produced over time?

R7 should pressure-test:

```text
stock vs flow vs capacity vs budget vs rate
rival vs non-rival vs renewable vs degradable resources
consumption vs reservation vs depletion
renewal / replenishment / reacquisition
skill/knowledge decay and relearning
capital accumulation and drawdown
compute/network quota replenishment
maintenance burden and entropy
resource-producing Actions/Effects
Knowledge → new Resource discovery/acquisition capability
Capability → more Resources/Options
negative feedback from complexity/risk/maintenance
positive feedback / compounding without assuming monotonic growth
```

Crucially, R7 must use R6's separation:

```text
Action/Effect history
≠ domain Outcome
≠ causal Attribution
```

otherwise every resource change will be incorrectly credited to the immediately preceding Action.

Do not create a universal stock-flow engine unless real owner-native domains prove a shared executable responsibility.

---

# 30. Conclusion

R6 began with a seemingly sensible improvement:

```text
Capability
→ Action
→ Consumption
→ Effect
→ Outcome
→ Attribution
→ Knowledge
```

The stage names are useful. The universal arrow chain is not.

Reality contains:

```text
successful Effect + negative Outcome
failed Effect + useful Knowledge
invalid scientific Outcome + methodological Knowledge
Outcome without Agent Action
many Effects from one Action
many Actions/Effects contributing to one Outcome
known Outcome + unknown Attribution
Consumption without intended Effect
```

The thinner foundation is therefore:

> **Action records the admitted attempt. Effect records what the effect owner can prove happened. Outcome is a domain evaluation of consequences. Attribution is a separate causal claim. Knowledge is a promoted reusable conclusion. Consumption is resource-family accounting. None of these should be collapsed merely because they often appear in one successful narrative.**

And the ownership law is:

> **Lower layers prove direct Effects; consuming domains own Outcome semantics; causal Attribution and Knowledge promotion require their own evidence.**

That is the R6 result carried into R7. It remains provisional research rather than canonical World doctrine.
