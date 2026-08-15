---
schema_version: 1
id: world.resource-ontology-r8-evidence-resource-falsification
title: Resource Ontology R8 — Evidence Resource Falsification
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
summary: Falsifies carrier-centric and universal evidence-record interpretations; retains claim-support as the minimal Evidence semantic relation and decision-scoped ActionableEvidenceFor projection for transportability, currentness, independence, coverage, target evidence, negative evidence and value-of-information.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-ontology-r3-relation-model
  - world.resource-ontology-r6-conversion-falsification
  - world.resource-ontology-r7-ecology-dynamics-falsification
---
# Resource Ontology R8 — Evidence Resource Falsification

## 1. Question

R0–R7 established that Resources, lifecycle, composition, conversion and ecology all become misleading when World turns contextual relations into one universal record.

R8 asks the branch that every earlier round depended on but had not isolated:

> **What exactly makes something an Evidence Resource, and when is that Evidence actionable for a new claim, target or decision?**

The tempting shortcuts are familiar:

```text
file exists                         → evidence
official source                     → true
more citations                      → stronger evidence
fresh observation                   → applicable everywhere
direct target evidence              → only valid evidence
machine/Agent evidence              → Human Outcome evidence
failed experiment                   → useless
high confidence                     → act
Evidence                            → Knowledge
```

R8 attacks each shortcut directly.

The target is not an Evidence database. The target is the smallest semantics that changes prediction, inference, action, recovery or promotion.

---

# 2. Frozen boundary

R8 opened on canonical World:

```text
b03b40f0adf15df37f284bd0ef9cd9f48ed35bda
```

Frozen owner revisions:

| Owner | Revision |
|---|---|
| world | `b03b40f0adf15df37f284bd0ef9cd9f48ed35bda` |
| finance | `1499b0b48c83cc1a16ec6c68504f77a88433b96d` |
| runtime | `c6e45d9e41d3b4d64b5b3dace01497c53e574026` |
| workstation | `85f904635e856612b78e8b13acc553b1e80d292a` |
| studio | `52f646022cc606985a63a5fd290c417fd337e80e` |
| security | `6a7a8f9b22cb4995d436da2968b135248f8f6bb3` |
| game | `0c8581c6b5eebceaf33aeb8907fa91a8b53708dc` |
| human | `f7725dfc9b391c3e9a0c509d49795994931c9d63` |
| harness | `286985c82874d293308297f66b23152c1ed53369` |


The falsifier corpus binds:

```text
33 exact selected source files
66 exact source needles
60 frozen cross-domain discriminators
12 post-freeze falsifiers (10 synthetic/adversarial + 2 independent concurrent Finance FR3 cases)
4 current-system probes
5 external foundational theory families
```

Every selected local source file is digest-bound to its frozen repository Commit. R8 does not reinterpret a later sibling-repository HEAD as historical evidence.

---

# 3. R8 starts from an existing Ordivon Evidence Ecology

A separate pre-R8 evidence-ecology investigation had already produced one useful candidate chain:

```text
external Reality
→ observation / case / research
→ Evidence Resource
→ source/target relation + mechanism/effect-modifier qualification
→ Actionable Evidence
→ Prior / Hypothesis / Option
→ local probe / action
→ outcome attribution
→ Knowledge Capital
```

It also established two warnings:

```text
Evidence abundance ≠ Knowledge
Epistemic redundancy ≠ citation count
```

R8 does not copy that chain into production. It uses R0–R7 deletion tests to determine which pieces are semantics, which are downstream projections, and which are merely useful research language.

---

# 4. Foundational theory triangulation

R8 uses external theory to attack Ordivon assumptions, not to import a ready-made ontology.

| ID | Theory family | Source | Imported relation | What R8 does **not** import | Ordivon falsifier |
|---|---|---|---|---|---|
| T1 | decision analysis / value of information | Ronald A. Howard, Information Value Theory (1966) — DOI `10.1109/TSSC.1966.300074` | information amount is not decision value; information value is decision/preference/uncertainty dependent | does not define Ordivon evidence ontology or a universal action threshold | R8P03 same posterior produces different action and EVPI under different consequence structures |
| T2 | causal transportability | Elias Bareinboim & Judea Pearl, Transportability of Causal Effects: Completeness Results — DOI `10.1609/aaai.v26i1.8232` | source causal evidence may be reused in a target only relative to modeled source-target differences and available target information | formal causal transport does not automatically govern aesthetic preference, software receipts or noncausal claims | Game/Human cases where external evidence creates transfer hypotheses but target-specific residuals remain |
| T3 | trial generalizability / target population | Dahabreh et al., Extending inferences from a randomized trial to a new target population — DOI `10.1002/sim.8426` | effect modifiers and selective participation can make source and target effects differ; target covariates can support transport | does not imply every Ordivon target needs a direct experiment or person-level re-estimation | Human M0 heterogeneous individual effects + Evidence Transport contraction |
| T4 | dependent evidence synthesis | Hedges, Tipton & Johnson, Robust variance estimation in meta-regression with dependent effect size estimates — DOI `10.1002/jrsm.5`; erratum `10.1002/jrsm.17` | multiple effect sizes sharing participants/investigator/lab can violate independence; raw effect count is not independent evidence count | statistical RVE is not a universal Ordivon evidence combiner | Finance effectiveIndependentTrials and Workstation failure-domain independence cases |
| T5 | transport sensitivity | Dahabreh et al., Global Sensitivity Analysis for Studies Extending Inferences From a Randomized Trial to a Target Population (2026) — DOI `10.1002/sim.70083` | transport conclusions depend on assumptions whose violations can be sensitivity-tested rather than hidden | does not imply one global sensitivity parameter for heterogeneous Ordivon domains | preserve transport residuals/moderators and contradiction rather than collapse to confidence |

The cross-theory convergence is narrow but strong:

```text
information amount        ≠ decision value
source evidence           ≠ target effect
many observed effects     ≠ many independent evidence lineages
transport assumptions     must be explicit / sensitivity-bearing
```

Pearl/Bareinboim and Dahabreh formalize transport in causal settings; Hedges/Tipton demonstrate dependence in evidence synthesis; Howard separates communication information from decision value. These theories do **not** imply that all Ordivon evidence should become causal graphs, meta-analytic effect sizes, or numeric VOI records.

---

# 5. Four frozen Evidence models

## A — Artifact / Source Evidence

> An Evidence Resource is fundamentally a retrievable, integrity/provenance-bound source artifact, observation, receipt, trace or review packet. If the artifact exists and its source identity is trustworthy, it is the evidence; claim meaning, transport and decision use are interpretations performed later.

This is the natural evidence-store model:

```text
Evidence = source/blob/receipt/trace + provenance
```

It is operationally useful and necessary for exact recovery.

R8 tests whether it is semantically sufficient.

## B — Claim-Support Relation

> Evidence is a provenance/method/time-bound relation between an identifiable observation/artifact and one explicit claim, with support/contradiction/bounding/unknown semantics scoped to the declared context and time. Evidence is not the carrier alone and does not automatically become Knowledge.

B moves the semantic center from the artifact to:

```text
Evidence item / observation
        ── supports / contradicts / bounds / leaves unresolved ──► Claim
```

with provenance, method/context and time attached to the support assertion.

## C — Universal Transfer Contract

> Every actionable Evidence Resource is represented through one universal contract containing source, target, claim, mechanism, moderators/effect modifiers, method/design, uncertainty, independence/common-mode risks, freshness/applicability, permitted action class, falsifier and decision information value. The contract is the primary shared evidence object.

C is intentionally strong. It places source, target, mechanism, moderators, uncertainty, independence, freshness, action class, falsifier and VOI into one universal transferable-evidence object.

## D — Evidence Resource + Decision-Scoped Epistemic Projection

> An Evidence Resource is an identifiable provenance-bound observation/artifact/trace whose owner-native semantics support, contradict, bound or leave unresolved at least one explicit claim. Carrier identity, claim support and Knowledge are separate. ActionableEvidenceFor(claim,target,decision,as_of) is a derived projection that joins claim support with source-to-target transport/applicability, claim-specific currentness, retrievability/authority, set-level independence/common-mode structure, and decision consequence/reversibility/value-of-information. Native owners retain evidence and claim truth; consumers/domains own belief and Knowledge promotion. No universal confidence score is required.

D decomposes the problem:

```text
Evidence root semantics
    = carrier/observation identity
    + provenance/method/time
    + explicit Claim support

ActionableEvidenceFor
    = query-time projection over
      Claim × Target × Decision × as_of
      + applicability/currentness
      + transport
      + retrievability/authority
      + set-level independence/common-mode
      + coverage/contradiction
      + decision consequence / VOI
```

D does not make World the owner of belief or Knowledge.

---

# 6. Falsification result

| Model | 60 frozen discriminators |
|---|---|
| A — Artifact / Source Evidence | 12 PASS / 37 FAIL / 11 AMBIG |
| B — Claim-Support Relation | 41 PASS / 0 FAIL / 19 AMBIG |
| C — Universal Transfer Contract | 60 PASS / 0 FAIL / 0 AMBIG |
| D — Evidence Resource + Decision-Scoped Projection | 60 PASS / 0 FAIL / 0 AMBIG |

R8 deliberately strengthened B after anti-strawman review.

Before correction:

```text
41 PASS / 8 FAIL / 11 AMBIG
```

After correction:

```text
41 PASS / 0 FAIL / 19 AMBIG
```

The eight former FAILs were not failures of claim-support semantics. They were questions about transport, target population, Human experience or decision/VOI. Calling them Evidence-definition failures would collapse `Evidence` and `ActionableEvidenceFor`.

C and D both pass all 60 frozen cases and all twelve post-freeze cases.

Therefore R8 does **not** claim that C is false.

The selection pressure is deletion/minimality:

> **C stores downstream context inside every Evidence object; D keeps B-like Claim Support as the Evidence root and derives downstream context only when a target decision asks for it.**

---

# 7. Complete frozen discriminator matrix

| ID | Evidence case | Pressure | A | B | C | D |
|---|---|---|---|---|---|---|
| C01 | `W01` One evidence object/owner claim may support one transition witness while providing no support for an unrelated capability claim | claim binding | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C02 | `R8P01` Current World marks cap:x consumable-now even though owner evidence attests only resource/terms/interface and cap:x comes only from aggregator/candidate labeling | claim-level provenance gap | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C03 | `W03` A foreign claim can be successfully delivered to a destination without becoming destination Knowledge | evidence vs knowledge | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C04 | `W04` End-to-end authenticated provenance still does not promote the foreign claim to destination Knowledge | authentication vs semantic authority | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C05 | `W05` Provider observation time and World availability time are separate facts for the same observation | observation vs availability time | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C06 | `W06` A historical transfer receipt can be Evidence for past admission without proving current native bytes/presence | historical support vs current truth | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C07 | `W07` Information amount/source count is not equivalent to decision value of information | amount vs value | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C08 | `W08` Failed, invalid or uncertain episodes can yield reusable Knowledge only after external/domain promotion | negative evidence promotion | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C09 | `W09` Missing observations cannot be promoted to absence or Outcome truth without owner-native completeness semantics | absence vs evidence of absence | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C10 | `R8P02` Candidate diversityPotential changes planner ranking without failure-domain independence evidence; source explicitly calls it a heuristic | heuristic vs epistemic redundancy | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C11 | `F01` Finance UNKNOWN means evidence missing/unavailable/insufficient and must not be converted into evidence that a carrier is bad | unknown vs negative evidence | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C12 | `F02` Finance STALE preserves prior evidence while denying current applicability | staleness | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C13 | `F03` Venue contract mechanics require observation time/evidence/revalidation rather than eternal law | claim-specific freshness | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C14 | `F04` Finance append-only identity observations prevent later transition knowledge from leaking backward into earlier known_at queries | knowledge time | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C15 | `F05` Finance FR2 falsification fixture is not primary-source authority despite containing source navigation hints | fixture vs primary evidence | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C16 | `F06` Production Finance identity ingestion must preserve actual issuer/regulator/venue bytes and bind normalized rows to them | carrier + normalized claim binding | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C17 | `F07` An empty Capital Ledger is not evidence that no external owner flow occurred | coverage and absence | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C18 | `F08` Missing/partial/failed flow coverage keeps performance unavailable rather than assuming zero flow | completeness gate | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C19 | `F09` Observed owner-conditioned favorable capital consequence still does not prove Agent alpha without counterfactual/attribution evidence | effect vs causal claim | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C20 | `F10` A context treatment earns default status through stable replicated sealed benefit, not rationale or one favorable carrier | replication burden | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C21 | `F11` Finance explicitly counts effective independent trials rather than raw rows/results | independence | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C22 | `F12` A sealed replication can remain single-carrier evidence rather than a general law | scope/generalization | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C23 | `G01` Game uses external products/research as falsifier generators, not imported Station Zero requirements | external transport | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C24 | `G02` External evidence expands failure coverage while local reproduction decides whether implementation pressure exists | transport + local probe | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C25 | `G03` Live-Agent trajectories can differ substantially from fixture trajectories without that difference establishing player value | proxy/effect vs value | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C26 | `G04` Game can prove live cognition operational/behavioral while keeping player-value claim explicitly UNPROVEN | claim lattice | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C27 | `G05` Agent/model review can pre-falsify copy/hidden-information defects but cannot be relabeled as delight/preference/replay evidence | proxy boundary | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C28 | `G06` A clear repeated usability failure can justify a reversible local fix without first obtaining a large population sample | action threshold by consequence | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C29 | `G07` Owner/developer observation is not a clean fresh-player substitute because implementation knowledge is a target/source difference | effect modifier/target mismatch | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C30 | `G08` Large simulation volume does not substitute for experience judgment | volume vs target evidence | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C31 | `S01` Studio review-video creates disposable review evidence for one artifact iteration | evidence carrier lifecycle | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C32 | `S02` A review packet is not automatically an Asset, Output, Claim, Receipt or durable research result | evidence vs promotion/persistence | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C33 | `S03` Technical QC/perception sampling support structural observations but not beauty, truthfulness, persuasion or suspense | claim scope | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C34 | `S04` Human/expert calibration is conditional on a residual human-response claim, not a universal ritual | target-native residual evidence | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C35 | `S05` Vendor documentation establishes control surfaces but does not establish equipment retention value | source authority is claim-specific | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C36 | `S06` Equipment graduation requires real execution; vendor capability claims alone are insufficient | potential vs observed target effect | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C37 | `S07` A Blender process can exit zero while the domain artifact contract fails, so process-success evidence is insufficient for domain success | lower evidence vs higher claim | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C38 | `S08` Machine evidence can prove exact media/QC facts while the same exact Blob still requires human audition for naturalness/publication worthiness | mixed evidence roles | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C39 | `Q01` Security state/hypothesis evidence improved local diagnostics but did not establish transferable capability | local effect vs transfer | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C40 | `Q02` Four failed one-seed model trials support a do-not-promote decision while remaining informative about trace/information behavior | failed trial as evidence | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C41 | `Q03` One synthetic compromised-member scenario is insufficient evidence for a multi-Agent organization ontology | synthetic evidence scope | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C42 | `Q04` One trial per provider/memory mode is explicitly diagnostic only, not a general capability ranking | sample scope | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C43 | `Q05` In adversarial Security evidence, a signal should be treated as shaped until corroborated by an independent observation | independence/adversarial source | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C44 | `Q06` A phase transition makes prior route intelligence stale while preserving it as historical evidence | context-specific staleness | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C45 | `Q07` A cached exact Security result survives outage while a new unique job is unavailable | historical evidence vs current capability | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C46 | `Q08` Credential/service revocation does not retroactively invalidate an already delivered exact result | historical finality | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C47 | `H01` Human evidence is sufficient only when design, measurement, population, timing and uncertainty support the stated claim | design-to-claim | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C48 | `H02` Prestige, sample size, accuracy, significance or model complexity alone do not grant causal/normative authority | anti-score | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C49 | `H03` No single Human study design dominates every question; design must match claim | method heterogeneity | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C50 | `H04` Population observations may describe a distribution, predict under the DGP, or provide a prior for intervention effect—different claims | claim type | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C51 | `H05` More repeated personal observations help only when identification/design assumptions support the inference | data volume vs identification | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C52 | `H06` Synthetic Human M0 demonstrates an observational association with the opposite sign from the true average causal effect | measurement/design failure | FAIL `A-CLAIM-RELATION-LOSS` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C53 | `H07` A positive population-average effect does not determine an individual target effect; one synthetic target benefits and one is harmed | population-to-target transport | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C54 | `H08` Mature external Human evidence is the default prior; direct Ordivon experiments are reserved for decision-relevant transport residuals | direct evidence not monopoly | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C55 | `H09` Availability of a measurement does not by itself justify collecting direct target evidence | VOI/admission | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C56 | `H10` Human contraction selects transport analysis rather than universal N-of-1 replication | graded evidence acquisition | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C57 | `HA01` An externally promoted reusable source can exist without being selected into a Harness Run | evidence/source presence vs use | PASS `A-CARRIER-SUFFICIENT` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C58 | `HA02` Harness procedural candidates with unresolved unknowns or no independent evidence are rejected by the external evaluator | promotion burden | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-SET-OR-DECISION-AMBIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C59 | `HA03` CompletionProposal with evidence refs remains a candidate for domain verification rather than automatic persistent learning | candidate vs knowledge | AMBIG `A-CARRIER-ONLY-PARTIAL` | PASS `B-CLAIM-SUPPORT-SUFFICIENT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |
| C60 | `R8P03` The same posterior evidence supports a reversible outer probe but not an irreversible core change; EVPI also differs by stakes | decision-scoped threshold/VOI | FAIL `A-CLAIM-RELATION-LOSS` | AMBIG `B-DOWNSTREAM-RELATION-OUTSIDE-ROOT` | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-LAYERED-EVIDENCE-PROJECTION` |

---

# 8. Why A fails: provenance-bound bytes are a carrier, not the whole Evidence semantics

A source artifact can be perfectly exact and still fail to answer the intended claim.

Examples:

```text
Runtime receipt
  proves one physical execution/effect fact
  does not prove domain Outcome

Studio technical QC
  proves codec/color/dimensions/exact bytes
  does not prove beauty/naturalness/publication worthiness

Game live-Agent trace
  proves behavior differs
  does not prove player value

vendor documentation
  proves a documented control surface
  does not prove local equipment retention value
```

The Evidence carrier matters because it allows exact provenance, replay and reinspection.

But deleting Claim identity causes immediate semantic collapse.

Therefore:

```text
EvidenceCarrier
≠ EvidenceClaimSupport
```

---

# 9. B survives as the minimal Evidence semantic relation

After anti-strawman correction, B has no hard falsifier in the frozen corpus.

The minimum relation is:

```text
EvidenceSupport(
    evidence_item / observation,
    source/provenance,
    method/context/time,
    explicit_claim,
    relation = support | contradict | bound | unresolved
)
```

This is conceptual structure, not a proposed schema.

The key point is directionality:

```text
one item → several claims, with different support status
several items → one claim, with different dependence/quality
```

Evidence is therefore claim-relative in the same sense that R3 made Resource relation actor/transition-relative.

---

# 10. Claim binding is not optional

R8P01 reproduces the strongest R3 evidence debt against current production World.

The probe constructed:

```text
owner evidence:
  resource existence / terms / interface only

aggregator/candidate label:
  cap:x

consumer demand:
  requires cap:x
```

Current result:

```text
decision        consumable-now
demandFit       1.0
evidenceQuality 0.9
```

Probe Job:

```text
job-01a005b4-ee75-7ec1-9dd8-5298b99093a0
```

Nothing in the owner-native evidence attested `cap:x`.

This confirms:

> **Resource-level owner provenance does not establish claim-level transition semantics.**

A claim-support relation must preserve **which evidence supports which capability/transition claim**.

---

# 11. Current `evidenceQuality` is not epistemic quality

Current `ResourceEvaluation.evidence_quality` is computed from the presence/currentness of:

```text
OwnerVerification
candidate owner provenance
AuthorityEvidence
AcquisitionAssessment
TransportEvidence
historical ConsumptionOutcome
```

It does not evaluate:

```text
whether evidence supports the specific capability claim
transportability to a target
source/method dependence
common-mode bias
coverage/sensitivity
causal identification
contradiction structure
Human preference authority
decision value
```

R8 therefore classifies it as:

```text
planner evidence-completeness/currentness heuristic
```

not:

```text
universal epistemic confidence
```

No immediate rename/API change is performed because foundations research should not manufacture compatibility churn without a consumer need.

---

# 12. Provenance is necessary but not sufficient

Current World already proves two important anti-laws:

```text
delivery of a foreign claim
≠ destination Knowledge

authenticated end-to-end origin
≠ destination semantic authority
```

R8P04 re-ran the current implementation tests and all three passed:

```text
delivery does not promote foreign claim to Knowledge
end-to-end authentication does not promote claim to Knowledge
provider observation time remains separate from World availability time
```

Probe Job:

```text
job-01a005ba-3f5c-7a41-83f9-241c2c3b6180
```

Thus provenance answers:

```text
who/what produced this observation?
what exact bytes/event are we talking about?
```

It does not answer:

```text
is the source authorized for this claim?
is the claim true?
does it transport to this target?
should this decision act on it?
```

---

# 13. Source authority is claim-specific

Studio Equipment World gives a clean example.

Official vendor documentation can be authoritative for:

```text
available scripting API
supported command/control surface
package identity
protocol/interface description
```

But vendor documentation alone does not prove:

```text
our installation works
our network path works
our artifact contract succeeds
this tool reduces friction
this tool deserves retention
```

That requires Ordivon-native execution/production evidence.

Likewise an exchange may author venue contract mechanics but cannot author Owner portfolio utility; Runtime can author process/effect evidence but not Game player value.

There is no universal “trusted source” field that grants all claims.

---

# 14. Evidence can be positive, negative, limiting or unresolved

Finance's four-state semantic evidence is especially useful:

```text
PASS     current evidence supports the required proposition
FAIL     current evidence contradicts it
UNKNOWN  evidence missing/unavailable/insufficient
STALE    prior evidence exists, current applicability expired/changed
```

R8 does not promote these exact four labels to every domain.

It retains the deeper distinction:

```text
support
contradict
bound / narrow
unresolved
```

because `UNKNOWN` is not negative evidence and `STALE` is not historical falsification.

Security adds another case: four failed trials can support a **do-not-promote** conclusion and still provide useful methodological/trace evidence.

Failure is an outcome of a bounded observation process, not absence of Evidence.

---

# 15. Absence is a special inference, not an empty list

R6 already established:

```text
empty/missing observations
≠ absence / Outcome truth
```

Finance makes this executable:

```text
empty Capital Ledger
≠ proof of no external capital flow
```

Only an exact-period, complete evidence-backed query/coverage result may support the zero-flow inference.

This gives R8 a general law:

> **Evidence of absence requires an observation process whose relevant coverage/sensitivity/completeness is itself supported.**

A null scan, empty query, no log entry or zero result count does not self-authorize a negative claim.

---

# 16. Observation process is part of inferential support

Two identical values can imply different things under different data-generating processes.

Human M0 gives an explicit synthetic falsifier:

```text
naive observational difference
has the opposite sign
from the true population-average causal effect
```

The bytes are not corrupt.

The inferential failure is the selection/identification process.

Similarly Studio found a Blender process that exited zero while domain postconditions failed.

Therefore evidence support may need method/process facts such as:

```text
what was measured
what was observable
selection/sampling
coverage
randomization / intervention
comparison baseline
failure detection
postconditions
```

but only when the claim depends on them.

---

# 17. Evidence has multiple clocks

Finance FR2 and World observation-time semantics converge on a bitemporal lesson.

A fact can have:

```text
effective time       when the source-world regime applies
observed time        when source/provider observed it
available/known time when Ordivon could use it
applicability time   whether it still bears on the current claim
```

A later correction or transition must not leak backward into an earlier `known_at` decision.

Likewise:

```text
historically correct evidence
can become STALE for a current claim
without becoming historically false
```

R8 therefore rejects one universal:

```text
Evidence.current = true/false
```

Currentness belongs to the claim/target/use relation.

---

# 18. Transportability is downstream of Evidence existence

Game demonstrates the distinction unusually cleanly:

```text
external product/research failure
→ valid external Evidence
→ transfer hypothesis
→ Station Zero reproduction probe
→ local pressure only if relevant failure reproduces
```

External evidence remains Evidence even if Station Zero does not share the failure.

Therefore:

```text
source Evidence truth
≠ target applicability
```

Transport is a relation between source evidence/claim and a target context.

This is why the root Evidence object should not be rewritten when a new target appears.

---

# 19. Transport requires differences that matter, not a universal similarity score

Useful transport questions are:

```text
What is the source claim?
What target claim/decision are we considering?
What mechanism is expected to persist?
Which source-target differences can modify that mechanism/effect?
What evidence supports those moderator assumptions?
What local observation would falsify the transfer?
```

Human Evidence Transport uses exactly this logic:

```text
external Human evidence
→ mechanism / moderator boundary
→ Ordivon structural analysis
→ natural dogfood
→ residual experiment only if still decision-relevant
```

The target is not “similar enough” in one scalar sense.

Only claim-relevant differences matter.

---

# 20. Direct target-native evidence is a calibration anchor, not an epistemic monopoly

R8 rejects both extremes:

```text
external evidence always transports
```

and:

```text
no action until direct local evidence exists
```

Human research demonstrates why.

Mature external evidence can strongly constrain general Human mechanisms. Re-running the same mechanism on one ordinary local person may have very low information gain.

Direct target evidence becomes high-value when:

```text
known moderators differ
support/task structure materially differs
natural target observations contradict the transported prior
population preference / target Human response is the actual claim
consequence is high enough that residual uncertainty matters
```

Game GV7 is exactly such a residual: Agent review can falsify literal legibility defects, but delight/replay/preference requires appropriately scoped fresh-player evidence.

---

# 21. Machine / Agent / synthetic evidence has real but bounded authority

R8 explicitly rejects the view that proxy evidence is “fake.”

Agent/machine evidence can strongly establish:

```text
literal UI token leakage
structural hierarchy/copy defects
mechanical consequence
reproducibility
hidden-information violations
artifact integrity/QC
simulation behavior
falsifier coverage
```

What it cannot inherit automatically is the authority for:

```text
Human delight
preference
suspense
attachment
retention
market appeal
publication-worthiness
```

Game and Studio both already enforce this boundary.

The correct classification is:

> **proxy/falsifier sensor with claim-bounded authority.**

---

# 22. Evidence independence is a set relation

A citation, paper or observation cannot be called “independent” in isolation.

Relevant common modes include:

```text
same underlying participants/data
same experiment/trial
same lab/investigator/provider/model
same measurement instrument
same source API
same causal assumption
same network/root/failure domain
same training corpus / generated synthetic world
```

Finance's `effectiveIndependentTrials` and Workstation's explicit independence dimensions already embody this pattern.

External meta-analysis theory independently agrees: correlated effect estimates sharing participants or study clusters violate naïve independence assumptions.

Therefore:

```text
10 citations from one study
may be one epistemic lineage
```

while:

```text
2 genuinely independent methods
may add more redundancy
```

No `sourceCount` is an epistemic redundancy score.

---

# 23. Epistemic redundancy is relative to a falsifier/bias class

R5's redundancy law transfers cleanly to evidence:

```text
redundancy
≠ cardinality
```

Candidate R8 definition:

> **An Evidence Set has epistemic redundancy for a bounded claim/falsifier when at least two evidence lineages can bear on that claim and are sufficiently independent with respect to the bias/failure mechanism that would defeat one lineage.**

This is deliberately disturbance-relative.

Two different publishers copying the same source are not redundancy against source fabrication.

Two different models trained on heavily overlapping data may not be redundancy against shared dataset bias.

Two independent measurement modalities may be valuable against an instrument-specific failure.

No global independence graph is required to preserve this law.

---

# 24. Contradiction is information

A universal score tends to turn:

```text
+0.8 evidence
-0.8 evidence
```

into:

```text
0.0 confidence
```

R8 rejects that compression by default.

Contradictory evidence may reveal:

```text
heterogeneous treatment effects
population/target mismatch
regime change
measurement failure
confounding
shared assumption failure
adversarial shaping
```

Human M0's population/individual heterogeneity and Security phase changes are examples where disagreement is the useful signal.

The structure of contradiction should survive until the consumer can explain or deliberately tolerate it.

---

# 25. Evidence amount is not Evidence value

World R1 already imported the Shannon/Howard distinction:

```text
information amount
!=
decision value of information
```

R8 generalizes this to Evidence Resources.

Raw measures such as:

```text
bytes
citations
papers
trials
model runs
tokens
confidence numbers
```

cannot determine evidence value without the decision context.

The useful question is:

> **Could resolving this uncertainty change a currently available consequential decision enough to justify the information-acquisition cost?**

---

# 26. R8P03 — same Evidence, different action and VOI

R8 used one simple decision-analysis falsifier.

Same prior and evidence:

```text
prior = 0.5
likelihood ratio = 3
posterior = 0.75
```

Two actions:

```text
reversible outer probe
  true benefit = +1
  false cost   = -0.1
  action EV    = +0.725
  decision     = ACT
  EVPI         = 0.025

irreversible core change
  true benefit = +1
  false cost   = -5
  action EV    = -0.5
  decision     = DO NOT ACT
  EVPI         = 0.75
```

Probe Job:

```text
job-01a005b5-460b-7253-a86f-1d56b6f6fde5
```

Nothing about the Evidence changed.

The action threshold and value of further information changed because the **decision** changed.

Therefore no universal Evidence confidence threshold can authorize all actions.

---

# 27. Evidence acquisition is itself an Option

R8 refines the evidence-ecology loop:

```text
current evidence set
→ unresolved decision-relevant uncertainty
→ evidence acquisition Options
→ expected information value / burden / delay / downside
→ choose probe / external source / direct target test / no further evidence
→ observation
→ update projection
```

A useful qualitative rule is:

```text
acquire more evidence when
expected decision improvement / option preservation
materially exceeds
cost + delay + burden + risk of measurement itself
```

This can be quantified locally when a domain has defensible utilities/probabilities.

R8 does not define one global VOI scalar or threshold.

---

# 28. Reversibility changes evidence burden

Evidence Ecology and R8P03 converge on a graded policy:

### Cheap / reversible / outer-layer action

Transported external evidence may be enough to justify a local falsifier experiment.

Example:

```text
external UI legibility risk
→ inspect actual Station Zero UI
→ cheap L2 copy treatment if reproduced
```

### Consequential but recoverable domain change

Require stronger owner-native evidence, independent corroboration or local dogfood where material.

### Deep / costly / hard-to-reverse / asymmetric-downside change

Residual uncertainty and transport failures matter more; additional independent or target-native evidence may have high VOI.

This is an action policy, not a property stored inside Evidence identity.

---

# 29. Failed experiments remain Evidence Resources

Security and Harness both make this unavoidable.

A failed experiment can establish:

```text
the treatment did not meet objective under tested conditions
one mechanism did not generalize
an assumption was invalid
an observation interface is insufficient
an external effect is UNKNOWN
an evaluator/promotion gate correctly rejected a candidate
```

R6 already allows Knowledge to arise from failed/invalid/uncertain episodes after semantic promotion.

R8 therefore rejects:

```text
positive result = evidence
negative/failed result = waste
```

The correct question remains:

```text
what bounded Claim does this trial actually support, contradict or narrow?
```

---

# 30. Evidence is not Knowledge

Current World and Harness independently enforce:

```text
foreign claim delivered
→ Evidence / observation may exist
→ no automatic destination Knowledge

CompletionProposal
→ candidate + evidence refs + unknowns
→ external/domain evaluation
→ optional external promotion
→ reusable canonical source
```

Thus:

```text
Evidence
→ candidate inference / hypothesis / decision input
```

is not the same as:

```text
Evidence
→ canonical reusable Knowledge
```

Knowledge is an owner/domain promotion decision under R6.

World must not become a global BeliefStore merely because evidence crosses projects.

---

# 31. C and D tie on expressivity

C passes every frozen and fresh case.

That is important.

A universal record containing:

```text
source
target
claim
mechanism
moderators
method
uncertainty
independence
freshness
permitted action
falsifier
VOI
```

can describe almost anything if enough fields are optional and extensible.

But deletion asks whether those coordinates must be **Evidence identity/state**.

Direct local cases immediately show they need not be.

A Runtime receipt does not need a population moderator field.

A source-code digest observation does not need a decision VOI field.

A Studio QC record need not know every future Human target population.

An evidence item can remain unchanged while a new decision gives it new value.

Therefore C is expressive but over-packed.

---

# 32. D is C decomposed, not C denied

R8's provisional survivor is structurally:

```text
                 Evidence Carrier / Observation
                            │
                            ▼
               provenance + method + time
                            │
                            ▼
                    Claim Support
                  / contradict / bound
                            │
            ┌───────────────┼─────────────────┐
            ▼               ▼                 ▼
       source→target    currentness        retrievability
       transport        applicability      authority
            │               │                 │
            └───────────────┼─────────────────┘
                            ▼
                  Evidence Set projection
                    independence
                    common modes
                    contradictions
                    coverage gaps
                            │
                            ▼
          Claim × Target × Decision × as_of
                            │
                            ▼
                 ActionableEvidenceFor
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
          act / probe               acquire more evidence
                                             │
                                             ▼
                                            VOI
                            │
                            ▼
                       R6 outcomes
                            │
                            ▼
                 optional Knowledge promotion
```

No global Evidence record owns every box.

---

# 33. Evidence Resource definition candidate

R8's current minimal Evidence-specific definition is:

> **Relative to an actor/system boundary, an Evidence Resource is an identifiable observation, artifact, trace, receipt, representation or retained result with sufficient provenance/method/time support for at least one explicit claim such that the actor can intentionally enroll that claim-support relation in prediction, falsification, selection, verification, recovery or decision. The Evidence Resource need not currently be retrievable, target-applicable, independent of other evidence, sufficient for an action, or promoted to Knowledge; those are downstream relations/projections.**

This remains subordinate to the general R2 Resource definition and is not canonical doctrine yet.

A compact conceptual decomposition is:

```text
EvidenceResource
= Evidence Carrier / Observation Identity
× Source / Provenance
× Method / Observation Context where inference requires it
× Temporal coordinates where relevant
× Explicit Claim-Support Relation
```

Not:

```text
EvidenceResource
= source + target + decision + confidence + VOI + Knowledge
```

---

# 34. ActionableEvidenceFor candidate

The current downstream query is conceptually:

```text
ActionableEvidenceFor(
    actor,
    claim,
    target,
    decision,
    as_of
)
```

It may need to project:

```text
which evidence items support/contradict/bound the claim
which are retrievable/authorized
which are current/applicable
which transport to the target and why
which share common failure/bias lineages
whether negative/absence claims have sufficient coverage
which contradictions remain unresolved
which residual observations could change the decision
```

The output should remain structured.

A single confidence number would erase the reasons that determine the next action.

---

# 35. Independence belongs to Evidence Set, not Evidence item

This is one of R8's strongest deletion results.

Conceptually:

```text
EvidenceItem A
EvidenceItem B
```

are not “independent=true” globally.

Instead ask:

```text
IndependentFor(
    {A,B},
    claim/falsifier,
    bias_or_failure_class
)
```

Examples:

```text
same data, different paper        → not independent vs sampling bias
same provider, different endpoint → maybe independent vs endpoint failure, not provider failure
two models, shared training data  → uncertain vs shared-data bias
machine QC + human audition       → more independent for perception-vs-structure distinction
```

This mirrors R5's redundancy/failure-domain law exactly.

---

# 36. Freshness belongs to claims, not bytes

R8Y04 attacks one global expiry policy.

The same repository may contain:

```text
mathematical identity / stable specification claim
  half-life: potentially very long

provider endpoint reachability
  half-life: minutes

license entitlement
  half-life: until explicit expiry/revocation/currentness evidence

Human preference study
  applicability: population/context-dependent
```

The evidence bytes do not “decay.”

What changes is:

```text
current support/applicability for a named claim/target
```

R7's ecology currentness law therefore carries directly into R8.

---

# 37. Retrievability is Actionability, not historical truth

A cached receipt may be temporarily unavailable to one Agent.

That does not make the historical claim false.

Likewise a reusable Harness source may exist but is not selected into a Run.

Thus:

```text
Evidence support exists
≠ evidence currently materialized/retrievable
≠ evidence currently selected
```

When a current decision requires exact bytes, retrievability becomes an ActionableEvidenceFor condition.

---

# 38. Evidence contradictions should generate Options

Instead of compressing conflict immediately, R8 treats contradiction as a search surface.

Possible next actions:

```text
inspect source/method mismatch
look for moderator/effect modifier
acquire independent evidence
run a targeted local probe
narrow the Claim
split population/context/regime
leave UNKNOWN and preserve option value
```

This turns Evidence into a Resource in the original World sense: it expands or changes the Option set.

---

# 39. R8 relation ledger

| Concept | R8 disposition | Cases | Why |
|---|---|---|---|
| Evidence carrier/artifact identity | **KEEP_SEPARATE** | C15, C16, C31, C45 | Bytes/receipt/trace identity is necessary for exact provenance and replay but does not by itself state which higher claim is supported. |
| Source/provenance identity | **REQUIRED_FOR_SUPPORT** | C01, C04, C16, C35 | Who/what produced the observation constrains which claims it may author; authentication does not grant semantic authority beyond source scope. |
| Claim identity | **REQUIRED_SEMANTIC_COORDINATE** | C01, C25, C33, C47 | The same evidence can strongly support one proposition and be irrelevant to another. |
| Support relation/polarity | **REQUIRED_SEMANTIC_RELATION** | C11, C17, C40, C52 | Evidence can support, contradict, bound, or leave unresolved; missing/failed observations are not one universal negative value. |
| Observation/measurement process | **REQUIRED_WHEN_INFERENCE_DEPENDS_ON_COVERAGE** | C09, C17, C37, C51 | Absence and causal interpretation depend on what the observation process could have detected and how it was produced. |
| Observed/effective/available/known time | **CLAIM_LOCAL_TEMPORAL_COORDINATES** | C05, C12, C14, C44 | Evidence occurrence, target applicability and knowledge availability can move on different clocks; historical truth must not be rewritten. |
| Currentness/applicability | **CLAIM-TARGET-SPECIFIC_PROJECTION** | C12, C13, C44, C45 | Evidence bytes can remain while applicability to a current claim expires. |
| Source→target transport | **DOWNSTREAM_RELATION_NOT_EVIDENCE_IDENTITY** | C23, C29, C53, C54 | Source evidence remains valid in its source context even when target transport is weak or unknown. |
| Mechanism/moderator/effect modifier | **TRANSPORT_SUPPORT_WHEN_RELEVANT** | C29, C53, C54 | Differences matter only when they can modify the claim/effect under transfer; they are not mandatory fields on every direct local receipt. |
| Independence/common-mode | **EVIDENCE-SET_RELATION** | C20, C21, C43, C58 | Independence is not a property of one citation; it is relative to shared data, method, source, laboratory/model and failure/bias mechanism. |
| Epistemic redundancy | **DERIVED_SET_PROPERTY** | C20, C21, C43 | Multiple evidence items add resilience/information only to the degree they are substitutable and sufficiently independent for the relevant falsifier. |
| Evidence completeness/coverage | **OWNER-NATIVE_SUPPORT_CONDITION** | C09, C17, C18 | An empty result can imply absence only when the owner proves the query/measurement coverage needed for that inference. |
| Contradictory evidence | **PRESERVE_AS_STRUCTURE_NOT_AVERAGE_AWAY** | C40, C52, C53 | Conflict can reveal heterogeneity, confounding or boundary failure; a scalar average may destroy the reason for disagreement. |
| Negative/failed evidence | **FIRST_CLASS_BOUNDED_EVIDENCE** | C08, C11, C40 | A failure/null/invalid episode can falsify or narrow a claim and later support Knowledge, provided its observation/design semantics are explicit. |
| Retrievability/materialization | **ACTIONABILITY_CONDITION_NOT_SUPPORT_IDENTITY** | C31, C45, C57 | Evidence can remain semantically valid while temporarily unavailable to a current consumer; exact reuse still needs retrievable bytes/reference. |
| Authority/access to evidence | **ACTIONABILITY_CONDITION** | C16, C35, C57 | Possessing authority to retrieve or use evidence is separate from whether the evidence supports the claim. |
| Uncertainty | **CLAIM/METHOD_NATIVE_NOT_GLOBAL_SCORE** | C11, C18, C47, C58 | UNKNOWN/intervals/unresolved unknowns must remain explicit; one confidence scalar is not universal across heterogeneous claims. |
| Decision relevance | **DOWNSTREAM_PROJECTION** | C07, C28, C55, C60 | Evidence value depends on which decision is available, its consequences and whether the claim can change action. |
| Value of information | **DECISION-SCOPED_ACQUISITION_SIGNAL** | C07, C55, C60 | The same uncertainty can have tiny or large information value depending on stakes, reversibility and current best action. |
| Knowledge promotion | **SEPARATE_DOMAIN/OWNER_DECISION** | C03, C04, C08, C59 | Delivery, authentication, critique or CompletionProposal does not automatically produce reusable canonical Knowledge. |
| Direct target-native evidence | **CALIBRATION/RESIDUAL_ANCHOR_NOT_MONOPOLY** | C28, C34, C54, C56 | Target-native evidence is indispensable for target-specific residuals but mature external evidence can be the default prior when transport is strong. |
| Synthetic/Agent/machine evidence | **CLAIM-BOUNDED_PROXY/FALSIFIER** | C27, C30, C33, C41 | Synthetic or machine evidence can falsify structural defects or exercise mechanisms without inheriting Human preference/market/long-horizon authority. |
| Source prestige/count/volume | **NOT_EVIDENCE_VALUE** | C21, C30, C48, C51 | Volume can be dependent, mismeasured or irrelevant; design, claim fit, independence and decision impact dominate raw count. |
| Historical evidence | **PRESERVE_WITHOUT_CURRENT_PROMOTION** | C06, C12, C14, C46 | Later staleness, revocation or corrections do not erase what was historically observed/known. |

The major compression is visible in the disposition column:

```text
Evidence root:
  carrier identity
  provenance/source
  explicit Claim identity
  support relation
  method/time when required for that support

Downstream projections:
  transport
  target applicability/currentness
  retrievability/authority
  independence/redundancy
  decision relevance / VOI
  Knowledge promotion
```

---

# 40. Deletion and rejected-addition tests

| Mutation | Result | Cases | Why |
|---|---|---|---|
| delete explicit Claim identity from Evidence support | **FAIL** | C01, C25, C33, C47 | The same bytes/receipt can support a mechanical fact while leaving player value, causality or another transition unsupported. |
| delete provenance/source identity | **FAIL** | C01, C04, C16, C35 | Authentication/authority is claim-specific and normalized/candidate labels cannot self-authenticate semantic truth. |
| delete observation/design process | **FAIL** | C09, C17, C37, C52 | No-observation cannot become absence and correlation cannot become causal evidence without knowing what the process measured. |
| delete temporal coordinates and keep one Evidence.current bit | **FAIL** | C05, C12, C14, C44 | Observed, available, effective, known and applicability time can differ while historical truth persists. |
| delete source→target transport relation | **FAIL** | C23, C29, C53, C54 | External/population evidence can remain valid yet fail to justify a target-specific claim or action. |
| delete set-level independence/common-mode reasoning | **FAIL** | C20, C21, C43, C58 | Replications/citations sharing data/method/source can create false redundancy. |
| delete coverage/completeness semantics | **FAIL** | C09, C17, C18 | Empty query/ledger/result cannot prove absence unless the owner proves the observation was complete enough. |
| delete negative/failed evidence from the Evidence Resource family | **FAIL** | C08, C11, C40 | Failures can falsify/narrow claims and create methodological/recovery knowledge without a positive Outcome. |
| delete Evidence→Knowledge promotion boundary | **FAIL** | C03, C04, C08, C59 | Transported/authenticated/candidate evidence would automatically become durable semantic belief. |
| delete decision context from evidence acquisition/action threshold | **FAIL** | C28, C55, C60 | The same posterior evidence rationally supports a reversible probe but not a costly irreversible change. |
| force every Evidence Resource to carry one universal Transfer Contract with target, moderators, independence, action class and VOI | **REJECT_ADD** | C05, C16, C31, C45 | Direct owner-local observations do not need all downstream coordinates; the fields become nullable/duplicated decision state rather than Evidence identity. |
| force one global confidence/evidence-quality scalar | **REJECT_ADD** | C10, C11, C47, C60 | Completeness, claim support, transport, independence and action value are different relations; averaging them destroys failure reasons. |
| use citation/source/result count as epistemic redundancy | **REJECT_ADD** | C20, C21, C30, C43 | Dependence/common-mode can make many observations one effective evidence lineage. |
| require direct target-native evidence before any action | **REJECT_ADD** | C23, C28, C54, C56 | Strong transported evidence can justify cheap reversible probes; direct evidence is residual/calibrating where target differences matter. |
| allow external/synthetic/Agent evidence to assert Human preference or market Outcome directly | **REJECT_ADD** | C25, C27, C30, C41 | Proxy evidence has bounded structural authority and does not own target Human experience. |
| treat failed/null/invalid experiments as zero-value evidence | **REJECT_ADD** | C08, C40, C52 | They can reveal design failure, falsify a promotion, expose confounding or support recovery/methodological Knowledge. |
| average contradictory evidence into one score before checking heterogeneity/design/transport | **REJECT_ADD** | C40, C52, C53 | Contradiction may be the evidence of a moderator or identification failure that the average erases. |
| treat human presence itself as approval authority | **REJECT_ADD** | C34, C38 | Human judgment must be bound to the exact claim/artifact and remains scoped to the decision it can actually observe. |
| persist a global EvidenceGraph/BeliefStore because cross-domain evidence relations exist | **REJECT_ADD** | C03, C16, C23, C59 | Native owners already own source/claim truth and consumers own belief/Knowledge; current failures need narrow joins, not a second semantic authority. |

The strongest retained distinctions are not new object types. They are relation boundaries.

---

# 41. Fresh post-freeze falsifiers

The models were frozen before these twelve cases were added.

| ID | Post-freeze falsifier | C | D |
|---|---|---|---|
| R8Y01 | Ten papers/report URLs derived from one underlying dataset are not ten independent evidence lineages for a claim. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-INDEPENDENCE-SET` |
| R8Y02 | A direct target-native anecdote can calibrate or falsify transport but does not automatically dominate a larger well-designed external evidence base for a general mechanism. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-TARGET-CALIBRATION` |
| R8Y03 | A null security scan is evidence of absence only when coverage/sensitivity and the relevant target surface are established; otherwise it is UNKNOWN/limited evidence. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-COVERAGE-NEGATIVE` |
| R8Y04 | A stable mathematical/specification claim may remain applicable for years while an endpoint-health observation can become stale within minutes; Evidence has no universal freshness clock. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-CLAIM-CLOCK` |
| R8Y05 | An exact historical receipt may be temporarily inaccessible to one consumer while its prior claim support remains historically valid; retrievability changes Actionability, not past truth. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-RETRIEVABILITY` |
| R8Y06 | Two genuinely independent methods that converge on one bounded claim can add more epistemic redundancy than a hundred repeated measurements sharing one systematic bias. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-INDEPENDENCE-NOT-COUNT` |
| R8Y07 | A machine/Agent review that exposes a literal implementation token in player UI is enough to justify a reversible copy-layer fix but not a claim about market appeal. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-CLAIM-ACTION-SCOPE` |
| R8Y08 | A transported prior and a fresh target observation can disagree; both Evidence Resources remain, while the target projection must expose the contradiction/moderator instead of deleting one source. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-CONTRADICTION-PRESERVED` |
| R8Y09 | A source correction can supersede current support without rewriting what an earlier decision maker could know at the historical known_at time. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-BITEMPORAL-EVIDENCE` |
| R8Y10 | The same posterior evidence can rationally trigger a low-cost reversible probe and block a high-downside irreversible core rewrite; the latter also has higher value for additional information. | PASS `C-UNIVERSAL-CONTRACT-CAN-EXPRESS` | PASS `D-DECISION-VOI` |

Both C and D survive all twelve.

Current expressivity surface:

```text
C = 72 / 72
D = 72 / 72
```

The tie is deliberate. D's provisional preference comes from lower ontological commitment and clearer truth ownership.

---

# 42. Post-freeze concurrent Finance FR3 falsifier

After R8 froze A/B/C/D and the 60-case matrix, Finance independently advanced from frozen `1499b0b...` to:

```text
3d714710e330954b2f0f98510ceaf700847b02b6
finance: separate carrier observation and admission
```

FR3 was not used to author the R8 models. Its new `Carrier Semantics` independently decomposes:

```text
market/carry observation
→ evidence completeness
→ hard semantic carrier gates
→ research-stage admission
→ optional triage ranking
```

It explicitly states that a provider/egress failure yields `fundingHistory=UNKNOWN`, not a low-carry/weak-carrier claim; `QUALIFIED` cannot be reinterpreted as capital/trade permission; and `triageScore` exists only when all score inputs are observed. When fresh network collection failed, FR3 reused same-day canonical observations for deterministic semantic replay rather than treating network instability as financial evidence.

This is a strong out-of-sample convergence on R8's separation:

```text
Observation / Evidence
≠ Evidence completeness
≠ semantic admission
≠ ranking
≠ capital/execution authority
```

R8Y11/R8Y12 add these two post-freeze cases. C and D both pass them without wording changes.

---

# 43. Current production debts

## 42.1 Claim-level provenance — reproduced

R3F01/R3F02 and R8P01 all show the same truth-role error:

```text
Resource-level owner provenance
+ unbound candidate capability label
→ current evaluator may treat capability as verified demand fit
```

This is a real correctness debt.

R8 still does not choose a production schema because the smallest correct representation could be:

```text
owner-verified capability claims
claim-level transition evidence
consumer semantic proof
provider-native capability export
```

R9 cross-domain dogfood should reproduce the actual consumer responsibility before World installs a shared structure, unless the debt is separately scoped as a narrow existing-law correctness fix.

## 42.2 `evidenceQuality` semantic overread risk

`ResourceEvaluation.evidence_quality` is useful for its current planner role but is not epistemic quality.

Do not reuse it as:

```text
confidence
truth probability
transportability
independence
scientific evidence strength
```

## 42.3 `diversityPotential` is intentionally only a heuristic

R8P02 proves that changing only:

```text
diversityPotential 0 → 1
```

changes potential score:

```text
0.650000 → 0.816667
```

with no new independence evidence.

This is not a newly discovered implementation contradiction because the source explicitly calls the field a discovery/ranking heuristic.

It is a hard boundary against interpreting Resource ranking as epistemic redundancy.

---

# 44. Why R8 does not implement an EvidenceGraph

The failures reproduced in R8 are narrow:

```text
claim-level provenance is missing in one generic evaluator join
transport needs explicit target reasoning
independence is evidence-set/failure-class relative
VOI is decision-scoped
Knowledge belongs to consumers/domains
```

A global graph would add:

```text
second source authority
belief ownership ambiguity
universal currentness semantics
mandatory relation persistence
cross-domain schema coupling
```

without proving that any real consumer needs one shared storage/control surface.

Therefore R8 introduces **no**:

```text
EvidenceManager
EvidenceGraph
ClaimRegistry
BeliefStore
ConfidenceService
EvidenceScore
EvidenceDatabase
GlobalVOIEngine
```

---

# 45. The old Transfer Contract survives as an ephemeral projection template

Evidence Ecology's candidate Transfer Contract was useful:

```text
source
target
shared mechanism
differences/effect modifiers
claim
evidence basis
independence/common-mode risks
permitted action class
falsifier
freshness/expiry
```

R8 does **not** discard it.

It changes its status:

```text
Universal persisted Evidence object        REJECT
Decision-scoped transport assessment       RETAIN
```

Use it when a real source→target transfer question exists.

Do not require every direct local receipt or exact hash observation to carry fields for a hypothetical future target.

---

# 46. Evidence thresholds become action classes, not one score

A practical Ordivon policy after R8 is qualitative and reversible:

```text
External/theoretical evidence
    can justify cheap falsifier generation

Independent machine/Agent evidence
    can justify bounded structural fixes it directly observes

Repeated owner-native evidence
    can justify consequential domain changes within its authority

Appropriately scoped Human/target-native evidence
    is required for target Human preference/value claims

Deep irreversible/high-downside changes
    justify more independent/target evidence when residual uncertainty has high VOI
```

This does not mean “more evidence is always better.”

Measurement burden, delay, privacy, opportunity cost and experimental side effects are themselves Resource costs.

---

# 47. Evidence acquisition stopping rule

R8's current stopping rule is:

> **Stop acquiring evidence when the remaining uncertainty is unlikely to change the available decision enough to justify the marginal acquisition burden, or when no feasible evidence can resolve the uncertainty on a useful timescale.**

Conversely, continue when:

```text
there are competing actions
residual uncertainty can flip the choice
consequences are material
an affordable evidence Option can resolve it
```

This is the decision-theoretic content of VOI without forcing every domain into the same utility units.

---

# 48. Evidence can itself create new Resources and Options

R7 showed recursive Resource creation requires Attribution.

R8 specifies the epistemic branch:

```text
new Evidence
→ narrows uncertainty / exposes contradiction / validates mechanism
→ changes acquisition or selection
→ unlocks or rejects Options
→ may create Knowledge after promotion
→ may improve future Resource discovery
```

But causal attribution still matters.

If new Resources appear after a research round, R8 does not automatically credit the evidence unless comparison/mechanism evidence supports the connection.

---

# 49. Evidence ecology is therefore not a library problem

A large corpus can have low action value when:

```text
all sources copy one underlying dataset
claims do not match the decision
currentness expired
transport is weak
measurement cannot identify the claim
all evidence shares one failure mode
no available action changes
```

A small corpus can be highly valuable when:

```text
claim is explicit
mechanism is relevant
independent evidence attacks decisive falsifiers
one cheap probe can resolve a live decision
```

The scarce variable is often **evidence conversion**, not evidence volume.

---

# 50. R8 minimum topology

```text
Reality / source system
        │
        ▼
Observation / Artifact / Receipt / Trace
        │
        ├── exact identity / bytes
        ├── provenance / source authority
        ├── method / observation process
        └── temporal coordinates
        │
        ▼
Claim Support Relation
 support / contradict / bound / unresolved
        │
        ▼
Evidence Resource
        │
        ├──────── source→target applicability / transport ────────┐
        ├──────── currentness / retrievability / authority ──────┤
        ├──────── Evidence Set independence / contradiction ─────┤
        └──────── coverage / unresolved gaps ────────────────────┤
                                                                  ▼
                                              Claim × Target × Decision × as_of
                                                                  │
                                                                  ▼
                                                    ActionableEvidenceFor
                                                     / evidence acquisition
                                                                  │
                                                                  ▼
                                                       Action / Probe / Abstain
                                                                  │
                                                                  ▼
                                                   R6 Effect / Outcome / Attribution
                                                                  │
                                                                  ▼
                                                optional domain Knowledge promotion
```

This topology intentionally has no global Belief node owned by World.

---

# 51. What R8 rejects

1. Evidence = file/blob/receipt alone.
2. Official/authenticated source = authority for every claim.
3. Resource-level provenance = claim-level semantic support.
4. Citation/source/result count = independent evidence count.
5. Information amount = decision value.
6. One universal evidence-quality/confidence score.
7. One universal Evidence currentness clock.
8. Empty result = evidence of absence without coverage semantics.
9. UNKNOWN = negative evidence.
10. STALE = historically false evidence.
11. Failed/null/invalid experiment = zero-value evidence.
12. Machine/Agent/synthetic evidence = Human preference/market Outcome evidence.
13. Direct target-native evidence = only legitimate evidence.
14. External evidence = imported target requirement.
15. Human presence = approval authority.
16. Contradictory evidence should be averaged away before checking heterogeneity/transport/design.
17. Every Evidence Resource must carry a Universal Transfer Contract.
18. Evidence delivery/authentication = Knowledge promotion.
19. CompletionProposal/model reflection = automatic learning.
20. Global EvidenceGraph/ClaimRegistry/BeliefStore/ConfidenceService from R8.
21. Immediate broad production schema to fix R8P01.
22. A universal numeric VOI or evidence threshold across domains.

---

# 52. What R8 resolves enough for R9

### Evidence carrier and Evidence semantics are separate

Exact bytes/receipts/traces preserve source identity. Claim support gives them semantic evidentiary role.

### Evidence is claim-relative

One item may strongly support one claim and say nothing about another.

### Provenance is required but bounded

Source identity constrains semantic authority; authentication does not create target/domain truth.

### Negative and failed evidence is first-class

When observation/design semantics are known, it can falsify, narrow or create later Knowledge.

### Historical evidence survives current staleness

Applicability/currentness changes do not rewrite what was observed or known.

### Transportability is downstream

Source Evidence can remain valid while target applicability is weak/unknown.

### Direct target evidence is residual/calibrating, not monopolistic

External evidence can justify reversible probes; target-specific claims require target-appropriate evidence.

### Independence is an Evidence Set relation

It is relative to a shared bias/failure class, not source count.

### Decision value is downstream

The same Evidence can support different actions/VOI under different consequence structures.

### Evidence is not Knowledge

Knowledge requires explicit domain/owner promotion.

### C is expressive but too thick as a universal object

The full Transfer Contract survives as an ephemeral decision/transport assessment, not Evidence identity.

---

# 53. R9 handoff — cross-domain Resource dogfood

R0–R8 have now produced a coherent provisional stack:

```text
R2/R3   Resource / ResourceFor
R4      Events + Claims, not universal lifecycle
R5      Requirements + Assignments + Constraints
R6      Action / Effect / Outcome / Attribution / Knowledge
R7      owner-native dynamics + Ecology Projection
R8      Claim-Support Evidence + ActionableEvidenceFor projection
```

R9 must stop extending theory in isolation.

Its task is to consume the stack in several materially different real owners and ask:

```text
Which distinctions actually improve current decisions?
Which distinctions never get queried?
Where do real consumers reproduce the same missing join?
Does R8P01 claim-level provenance fail in more than the generic World evaluator?
Does any domain actually need a shared quantitative capacity surface from R7P01?
Does composition require a shared cross-owner seam from R5?
Can Evidence transport/actionability remain ephemeral projections?
What can be deleted before R10 doctrine compression?
```

Minimum R9 dogfood should include materially different domains such as:

```text
Finance    current instrument/evidence/capital decision
Game       external evidence → consumer failure → smallest treatment
Studio     machine evidence → residual Human claim
Security   negative/adversarial evidence → promotion/recovery decision
Human      external prior → transport residual → experiment admission
```

R9 should prefer existing real work over synthetic framework tests.

No R10 promotion should occur until at least several owners converge on the same surviving distinctions.

---

# 54. Conclusion

R8 started with the intuitive question:

```text
What counts as good evidence?
```

That question was too compressed.

The stable decomposition is:

```text
What exact observation/artifact exists?
Who produced it, how and when?
Which explicit Claim does it support, contradict, bound or leave unresolved?
Does that support transport to this target now?
What common-mode dependencies exist in the Evidence Set?
What contradictions or coverage gaps remain?
Can the current actor retrieve/use it?
Could more evidence change the available decision enough to justify its cost?
Has any conclusion earned domain Knowledge promotion?
```

The resulting law is:

> **Evidence is not a pile of sources and not a confidence number. Its root semantic unit is a provenance-bound claim-support relation. Target applicability, independence, currentness, evidence sufficiency and value-of-information are downstream relations of a particular claim and decision.**

And the acquisition law is:

> **Use the least specialized evidence that can resolve the live decision. Transport strong external evidence where the mechanism survives, spend scarce target-native evidence on real residuals, and raise the evidence burden as reversibility falls or downside rises.**

C and D both survive the full 72-case expressivity surface. D is provisionally preferred because it preserves the same explanatory power with a thinner semantic waist and without creating a second global evidence/belief authority.
