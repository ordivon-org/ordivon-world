# World Latest Foundations → Engineering Delta Audit — 2026-08-18

Status: **CLOSED — NO NEW PRODUCT SUBSYSTEM ADMITTED; NARROW DOCUMENTATION CONSUMPTION ONLY**

Scope: current World product at `7f4b7ca3d463d61be6799be89dd10be2a973c4d3` against the latest frozen World research families:

- WDF4 — Causal Reality Architecture;
- WDF5 — Property Evaluation Architecture;
- TSAF0 — Temporal Structure Architecture.

This audit asks whether those research results expose a current World engineering defect. Foundation admission alone is not an implementation requirement.

## Decision matrix

| Research family | Current production pressure | Disposition |
|---|---|---|
| WDF4 Causal Reality | World transports/retains owner-native occurrence, admission, provenance and receipt evidence but does not expose a generic causal-attribution API or infer cause from sequence/correlation | **NO CODE CHANGE REQUIRED** |
| WDF5 Property Evaluation | Provider observations and Browser Artifact bundles are integrity/evidence objects; current contracts explicitly refuse to equate structural/digest validity with truth, freshness or target validity | **NO GENERIC MEASUREMENT LAYER; DOCUMENT FUTURE ADMISSION RULE** |
| TSAF0 Temporal Structure | Provider start/completion, World `availableAt`, Host admission and claim-specific currentness already remain separate; historical receipts do not establish current Presence | **EXISTING PRODUCT SATISFIES CURRENT LOAD-BEARING DISTINCTIONS** |

## WDF4 — Causal Reality Architecture

### What the research adds

WDF4 separates causal relation, causal query, grounding/evidence, actual contribution, composition and validity envelope. Temporal order, correlation, provenance, successful execution and source admission are not automatically causal truth.

### Current World product

Current World production already keeps narrower owner facts separate:

- source occurrence/admission is established by the source owner;
- destination materialization/admission is established by the destination owner;
- Host owns durable work/uncertainty continuity;
- Runtime owns physical execution facts;
- World preserves typed trajectory bindings and reconciliation without translating those facts into a universal causal model.

Resource Transfer, Message Delivery and Entity Migration therefore do **not** claim that the retained source occurrence is the complete cause of every destination state, or that temporal succession establishes causal attribution.

### Engineering verdict

No current consumer requires a generic causal query, actual-cause object, causal graph, causal manager or causal schema in `ordivon-world`.

**Reopen engineering consumption only when a real World interface must answer a causal claim rather than merely preserve owner-native occurrence/admission/effect evidence.** At that point the interface must declare the causal target/query, admissible contrast/intervention or contribution semantics, grounding evidence and validity scope rather than deriving causation from receipt order.

## WDF5 — Property Evaluation Architecture

### What the research adds

WDF5 distinguishes sensing/detection, scoring/prediction, quantification, measurement attribution, empirical grounding, interpretation/value semantics, comparability and quality/uncertainty/validity.

A digest-valid observation can still be the wrong proxy for a target. Reliability or precise uncertainty does not itself establish target validity. Numeric representation alone is not measurement.

### Current World product

The current product already refuses the dangerous collapse:

- `BrowserArtifactBundle` verifies bytes, manifest/receipt alignment and bundle integrity, **not page truth or Task satisfaction**;
- `WorldObservation` maps provider evidence and does not claim freshness/currentness/truth;
- `WorldTaskInspector` is a bounded projection with `actionAuthority=not-granted-by-inspection` and `externalCurrentness=not-claimed`;
- provider-native schemas remain local rather than being normalized into one universal observation/measurement ontology.

### Engineering verdict

No current World surface advertises generic measurement-of-a-declared-property semantics. Therefore adding `Measurement`, `Quality`, `Uncertainty`, `Calibration`, `Comparator` or `Metric` managers now would be ontology-to-schema translation without a consumer.

If a future World adapter **does** claim that an output measures/evaluates property `A(T)`, admission must be explicit about:

1. target/property identity;
2. target-relevant empirical grounding chain;
3. attribution/interpretation bridge;
4. value/comparison semantics required by the claim;
5. quality/uncertainty/validity scope needed by the actual consumer.

Provider score/telemetry output must not silently gain measurement authority merely because it is numeric or precise.

## TSAF0 — Temporal Structure Architecture

### What the research adds

TSAF0 reinforces that occurrence, ordering, duration/interval, availability/observation, history and current validity are different temporal roles and may be owned by different systems.

### Current World product

Current production already has a concrete three-coordinate falsifier against time collapse:

```text
provider started_at / completed_at
!= WorldObservation.availableAt
!= Host recordedAt
```

and explicitly states:

```text
availableAt
!= source occurrence time
!= freshness
!= currentness
!= action authority
```

Historical transfer/message/entity receipts remain historical completion evidence and do not establish current destination Presence. Current actionability requires owner-native re-observation/reconciliation at the relevant evidence boundary.

### Engineering verdict

Current World already satisfies the load-bearing TSAF0 distinctions needed by its production workloads. No generic Time/Timeline/TemporalGraph service or universal currentness clock is admitted.

## Engineering consequences

The latest Foundations therefore **tighten interpretation rather than expand the product**:

- occurrence/admission/provenance evidence must not be promoted to causal truth;
- integrity/observation/score output must not be promoted to measurement validity without an explicit target-attribution contract;
- temporal coordinates stay owner-native and role-specific;
- currentness remains claim/evidence-specific;
- new shared Causal/Measurement/Temporal machinery requires a real consumer and a reproduced failure of the narrower owner-native representation.

## Non-admissions

This audit does not admit:

- `WorldCausalGraph` / `CausalManager`;
- `WorldMeasurement` / global Metric registry;
- universal uncertainty/quality schema;
- `WorldTimeline` / generic temporal ontology;
- WDF6 or TSAF1;
- a rewrite of existing production contracts into Foundation vocabulary.

## Reopen

Reopen only when a current World consumer demonstrates at least one concrete failure:

1. it must answer a causal claim and current occurrence/admission evidence is insufficient;
2. it must make a measurement/property-evaluation claim and current observation evidence lacks required attribution/validity semantics;
3. a real temporal decision cannot be represented with owner-native event/availability/currentness coordinates without ambiguity;
4. two materially different consumers need the same new cross-provider semantic contract.
