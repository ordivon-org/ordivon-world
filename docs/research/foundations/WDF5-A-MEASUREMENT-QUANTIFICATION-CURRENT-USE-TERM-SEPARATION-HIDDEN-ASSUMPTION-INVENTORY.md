# WDF5-A — Measurement / Quantification Current-Use / Term Separation / Hidden-Assumption Inventory

Date: 2026-08-18

Status: **WDF5-A COMPLETE / NO FOUNDATION FREEZE / WDF5-B NOT YET ADMITTED**

Canonical upstream:

```text
WDF0 = FROZEN
WDF1 = FROZEN
WDF2-A→N = completed research history
WDF2-O = NOT ADMITTED
WDF3-A→L = completed research history
WDF3 Foundation v1 = NOT FROZEN
WDF3-M = UNKNOWN / NOT ADMITTED
WDF4-A→F = completed research history
WDF4 Foundation v1 = FROZEN
WDF4-G = NOT ADMITTED

WDF5 = ADMITTED ROUTE
WDF5 Foundation v1 = DOES NOT EXIST
```

WDF5-A does not choose a positive measurement theory.

Its purpose is to make the current-use vocabulary explicit, separate false friends, expose hidden assumptions, and test whether `Measurement / Quantification / Reference / Comparability` remains one coherent World owner line after cross-regime attack.

---

# 1. Search discipline

WDF5-A treats every familiar measurement word as overloaded until separated.

Primary regimes:

```text
physical metrology
chemical/material measurement
biological/medical measurement
psychometrics / latent constructs
software/digital metrics
institutional/economic statistics
synthetic/virtual worlds
Agent-generated sensing/metrics
```

External pressure interfaces:

```text
Time
Law
Chance
Ontic Indeterminacy
Dynamics
Thermodynamics
Regime / possibility-space transformation
Gauge / symmetry / representation redundancy
```

Core firewalls inherited from prior WDFs:

```text
Reality != Observation != Evidence != Representation != Model
Relative != Subjective
Cause != Constraint != Constitution
Probability != ObjectiveChance
CausalValidity != MeasurementValidity
```

---

# 2. First result — Measurement and Quantification are not synonyms

A current-use inventory immediately exposes two distinct truth roles.

## Quantification

Broadly concerns assigning or using structured values, orderings, counts, scores, coordinates, indices or other formal magnitude-like representations.

Examples:

```text
counting requests
ranking preferences
assigning severity 0–5
constructing an index
benchmark scoring
mapping categories to numbers
estimating a parameter
```

Quantification can occur without a valid claim that the output measures a Reality attribute.

## Measurement

Adds a target-directed validity burden:

```text
what target is claimed?
what attribute/quantity/construct is claimed?
what procedure/model/interaction connects output to target?
what reference/scale/comparison semantics apply?
what uncertainty/resolution/validity envelope applies?
```

Therefore:

```text
Quantification != Measurement
```

and:

```text
NumberProduced != TargetMeasured
```

### Minimal counterexamples

```text
A random ID number quantifies/encodes but measures nothing.
A benchmark score can be numerically precise while failing to measure intended capability.
An arbitrary 1/2/3 category code is not measurement merely because it is numerical.
A valid ordinal quantity can support measurement without ratio-scale arithmetic.
```

### Owner-line judgment

The distinction does **not** force a project split.

Measurement and Quantification remain one owner line because the central World question is precisely when formal value structure becomes a valid Reality-targeting measurement claim.

```text
OwnerLineCoherence(WDF5) = PROVISIONALLY SURVIVES
```

---

# 3. Measurement != Observation

Observation is broader.

One can observe:

```text
color
shape
presence
behavior
text output
instrument indication
```

without producing a measurement claim.

Measurement requires additional target/reference/validity structure.

Therefore:

```text
Observation may provide input to Measurement.
Measurement may contain Observation.
Observation != Measurement.
```

---

# 4. Detection != Measurement

Detection answers a threshold/presence question such as:

```text
Is phenomenon X present above threshold θ?
```

It need not estimate the target quantity with measurement-scale semantics.

A detector can validly indicate presence while being unable to quantify magnitude accurately.

Therefore:

```text
Detection != Quantification
Detection != Measurement
```

A detection threshold may itself depend on error probabilities, procedure and background noise.

---

# 5. Sensing != Measurement

A sensor is a physical/digital interaction point affected by the phenomenon or substrate.

But:

```text
sensor response
```

can be:

```text
uncalibrated
drifting
nonselective
underspecified relative to target
wrongly interpreted
```

Therefore:

```text
Sensing != Measurement
SensorOutput != MeasurementResult
```

Sensing is a realization/interaction role; measurement is a truth/validity claim about target attribution.

---

# 6. Indication != Measured Value != Measurement Result

This separation is hard.

## Indication

Instrument/system output at a particular stage.

Examples:

```text
pointer position
display number
code pattern
sensor voltage
raw ADC value
```

## Measured value

A value attributed to the measured quantity after applying the procedure/model/correction as appropriate.

## Measurement result

The result-level object/claim, which may include:

```text
one or more attributed values
uncertainty
coverage information
reference/conditions
other relevant information
```

Therefore:

```text
Indication != MeasuredValue != MeasurementResult
```

A model/correction can validly infer the intended measurand from an instrument interaction that perturbs or differs from the intended target condition.

---

# 7. Data != Measurement Result

`Data` is too broad to function as a measurement primitive.

Data can include:

```text
raw indication
metadata
text
image
log
sample identifier
model output
calibration record
```

A measurement result is a semantically typed outcome of a measurement claim.

Thus:

```text
Data != MeasurementResult
```

and:

```text
MoreData != BetterMeasurement by default.
```

---

# 8. Target != Measurand != Carrier/System

WDF5 uses `Target` as the broadest cross-regime term.

Physical metrology uses `measurand` for the quantity intended to be measured.

But the bearer/system and target quantity are not identical.

Example:

```text
steel rod = carrier/system
length at 20 °C = measurand
```

The actual interaction may occur at another temperature and require correction.

Therefore:

```text
TargetSystem != TargetAttribute
TargetAttribute != ActualInstrumentInteractionQuantity
```

This becomes critical for latent constructs and institution-defined targets.

---

# 9. Property != Attribute != Quantity != Construct

These words cannot be globally collapsed.

## Property

Broad Reality role: some feature/status/relation predicated of a target.

## Attribute

Often a target-relevant feature selected for description or measurement; may be qualitative or quantitative.

## Quantity

A property/attribute with magnitude-like structure suitable for a defined value/comparison system.

## Construct

A theory-mediated target concept, often not directly observable and requiring a validity bridge from observables.

Examples:

```text
length = physical quantity
hardness = conventional/ordinal quantity family
memory = latent psychological construct
service availability = operationally defined system attribute
unemployment = institutionally defined statistical target
```

Hard firewall:

```text
Construct != MereProxy
Quantity != AnyNumberedAttribute
Property != Quantity by default
```

---

# 10. Nominal property != Ordinal quantity != Cardinal quantity

Current metrology itself distinguishes non-quantitative nominal properties from ordinal quantities.

An ordinal quantity supports order but not necessarily meaningful differences/ratios.

Therefore:

```text
NumericLabel != Quantity
OrdinalScale != IntervalScale != RatioScale
```

WDF5 must not assume:

```text
if x has a number, arithmetic over x is empirically meaningful.
```

---

# 11. Scale != Unit != Reference != Standard

## Scale

A structured space/rule relating values or order positions.

May be:

```text
ratio
interval
ordinal
conventional/reference scale
index scale
latent score scale
```

## Unit

A selected reference quantity used to express quantities of a kind.

Not every valid quantity/measurement regime requires an SI-like unit.

## Reference

A basis for comparison or anchoring.

Can be:

```text
unit realization
reference procedure
reference material
conventional value
historical baseline
versioned benchmark definition
```

## Standard

Dangerously overloaded.

It can mean:

```text
measurement standard / etalon
normative technical standard/specification
benchmark convention
institutional standard
```

Therefore:

```text
Scale != Unit != Reference != Standard
```

and:

```text
Reference != Truth
Standard != Law
```

---

# 12. Calibration != Verification != Validation

This is a central false-friend cluster.

## Calibration

Establishes a relation between reference/standard values and indications/results under specified conditions, including associated uncertainty.

Calibration answers roughly:

```text
How does this measuring system's indication relate to a reference structure?
```

## Verification

Checks whether specified requirements are fulfilled.

## Validation

Checks whether the specified requirements are adequate for intended use.

Therefore:

```text
Calibration != Verification != Validation
```

and:

```text
Calibrated != ValidForTarget
Verified != ValidForUse
```

A perfectly calibrated instrument can be used to measure the wrong target or under the wrong validity envelope.

---

# 13. Traceability != Correctness != Validity

Metrological traceability connects a result to a reference through a documented calibration chain, with uncertainty propagated/contributed along that chain.

But traceability does not prove:

```text
the target was correctly specified
the uncertainty is fit for purpose
the measurement procedure is valid for the intended use
no mistake occurred
```

Thus:

```text
Traceability != Correctness
Traceability != FitnessForPurpose
Traceability != MeasurementValidity
```

Traceability is one kind of provenance/reference bridge.

WDF5 must not universalize physical traceability chains to every regime.

---

# 14. Comparability != Compatibility != Equality

## Comparability

Two results can be meaningfully compared because they share an adequate reference/scale semantics.

## Compatibility

A stronger relation in a specified statistical/uncertainty sense: results for the same target/measurand are sufficiently consistent given uncertainty.

Thus:

```text
Comparable != Compatible
Compatible != Equal
SameUnit != AutomaticallyComparable
```

Cross-version software metrics and changing institutional definitions provide non-metrological analogues where comparability requires explicit bridge/version semantics.

---

# 15. Accuracy != Trueness != Precision

Current metrology treats these as non-identical.

## Precision

Consistency/agreement among replicate indications/values under specified conditions.

## Trueness

Agreement of an aggregate/mean behavior with a reference value; linked to systematic error rather than random spread.

## Accuracy

A broader closeness-to-target notion involving both systematic and random aspects but not itself simply one numerical quantity.

Therefore:

```text
Precision != Accuracy
Trueness != Precision
Accuracy != Validity
```

A highly precise instrument can be systematically wrong.

A highly accurate physical measurement can still be irrelevant to a different intended construct.

---

# 16. Reliability != Validity

Reliability is domain-dependent but generally concerns repeatability/consistency/stability of a score/procedure under declared conditions.

Validity asks whether the interpretation/result actually supports the intended target claim/use.

Psychometric hard case:

```text
A task produces extremely stable scores
but tracks reading speed instead of memory capacity.
```

Then:

```text
Reliability = HIGH
Validity(memory) = LOW
```

Therefore:

```text
Reliability != Validity
```

This is one of WDF5-A's strongest cross-regime anti-collapse results.

---

# 17. Error != Uncertainty != Noise != Mistake

## Noise

Unwanted/random/background variation in signals/data/conditions.

## Measurement error

Difference between measured value and a reference value under an error-account semantics.

## Uncertainty

A representation of dispersion/range/epistemic attribution associated with values assigned to the measurand/target based on available information.

Can include contributions from:

```text
instrument
calibration/reference
model
sampling
systematic effects
corrections
target definition
```

## Mistake

A procedural/implementation/human/software error, not a normal uncertainty component merely by occurrence.

Therefore:

```text
Noise != Error != Uncertainty != Mistake
```

and:

```text
Uncertainty != RandomnessOnly
```

---

# 18. Unique true value is not a universal WDF5 assumption

Even mature metrology distinguishes multiple approaches.

Under one traditional error framing a unique true value may be presupposed.

Under uncertainty-oriented framing, incomplete target definition can leave a set of values consistent with the quantity definition.

Some frameworks can work primarily with compatibility/reference relations rather than a unique accessible true value.

Therefore WDF5-A rejects:

```text
EveryMeasurableTargetHasExactlyOneTrueScalarValue
```

as a universal foundation axiom.

This does not imply:

```text
TrueValueNeverExists.
```

It means true-value ontology must be theory/target/regime scoped.

---

# 19. Resolution != Sensitivity != Selectivity != Detection Limit

These device/procedure properties separate.

## Resolution

Smallest target-side change that yields a perceptible/distinguishable indication change under conditions.

## Sensitivity

How much indication changes relative to target quantity change.

## Selectivity

Ability to obtain a target measurement without confounding/disturbance from other measurands/quantities.

## Detection limit

A threshold concept tied to false-positive/false-negative risk under a procedure.

Therefore:

```text
HigherSensitivity != BetterResolution always
Resolution != Accuracy
DetectionLimit != Sensitivity
Selectivity != Validity
```

---

# 20. Sampling != Measurement

Sampling determines which entities/times/regions/events enter the data-generating process.

A measurement may be perfect conditional on a sample while the sample is nonrepresentative for the claim population.

Thus:

```text
MeasurementValidity(target instance)
!= SamplingValidity(population claim)
```

This is critical in:

```text
epidemiology
survey statistics
observability
Agent telemetry
adaptive sensing
```

---

# 21. Estimation != Measurement

Estimation is an inference operation over data/model/priors/assumptions.

Measurement may require estimation.

But estimation can concern:

```text
future state
latent parameter
counterfactual quantity
unobserved population statistic
```

without itself being a measurement event.

Therefore:

```text
Estimation != Measurement
```

A measured value can be an estimate; that does not make all estimates measurements.

---

# 22. Inference != Measurement

Inference transforms/supports claims from premises/data/models.

Measurement provides a typed target-attribution result that may be consumed by inference.

Therefore:

```text
MeasurementResult -> may feed Inference
Inference -> may produce estimates about unmeasured targets
```

but:

```text
Inference != Measurement
```

---

# 23. Evidence != Measurement

Measurement results can be evidence.

Evidence can also be:

```text
witness report
proof
trace
historical record
qualitative observation
model comparison
```

Therefore:

```text
Measurement != Evidence
```

and:

```text
ValidMeasurement
!= StrongEvidenceForEveryClaim
```

This preserves WDF0/WDF3 separation.

---

# 24. Model != Measurement but model-mediated measurement is normal

Measurement can involve substantial modeling:

```text
correction model
calibration curve
measurement function
latent-variable model
sensor fusion model
instrument response model
```

Therefore:

```text
ModelMediatedMeasurement
!= LessRealMeasurement by default
```

But:

```text
ModelFit != MeasurementValidity
```

A model can fit observed data while its target mapping is wrong.

---

# 25. Proxy != Target

Proxy measurement claims are especially dangerous.

Examples:

```text
clicks as engagement
benchmark score as intelligence/capability
hospital readmission as quality
GDP as welfare
skin conductance as fear
```

A proxy may be causally/structurally correlated with a target without measuring the target under the intended interpretation.

Thus:

```text
Proxy != Target
Correlation != MeasurementBridge
```

WDF4 causal validity does not automatically solve proxy validity.

---

# 26. Index != Score != Metric != Benchmark

These are representation/aggregation artifacts unless target validity is separately earned.

## Score

A procedure-specific output, often from test items/events.

## Index

An aggregate/composite construction over selected components and weights.

## Metric

Extremely overloaded: mathematical distance, software observable, performance statistic, business KPI, evaluation measure.

## Benchmark

A reference test/task/dataset/protocol plus scoring semantics.

Therefore:

```text
Score != Measurement
Index != Measurement
Metric != Measurement
Benchmark != Measurement
```

by naming alone.

Each can become part of a legitimate measurement architecture if target/bridge/reference/validity are established.

---

# 27. Threshold != Classification != Measurement

A threshold maps a quantitative/score space into a decision/category.

Classification maps observations/features into labels.

These can depend on measurement results but are not themselves necessarily measurement.

```text
MeasuredValue -> threshold -> classification
```

is one possible pipeline.

Therefore:

```text
ThresholdDecision != MeasurementResult
ClassificationAccuracy != MeasurementValidity
```

---

# 28. Operational definition != target exhaustion

Operationalism creates a classic hidden-assumption risk:

```text
Target X is whatever Procedure P outputs.
```

This can make validity circular.

A useful operational definition may specify one method for producing/identifying a target claim without exhausting the target's Reality identity.

Thus:

```text
OperationalDefinition != TargetIdentity by default
```

and:

```text
ProcedureSuccess != ConstructValidity automatically.
```

---

# 29. Physical metrology is a mature regime, not WDF5 universal ontology

BIPM/JCGM provides especially sharp separations for:

```text
measurement
measurand
result
measured value
true value
uncertainty
calibration
traceability
comparability
compatibility
accuracy
trueness
precision
resolution
sensitivity
selectivity
detection limit
```

WDF5 adopts these as falsifier-quality distinctions where cross-regime truth supports them.

WDF5 does **not** freeze:

```text
MeasurementRequiresPhysicalInstrument
MeasurementRequiresSIUnit
MeasurementRequiresCalibrationHierarchy
MeasurementRequiresUniqueTrueScalar
```

as universal truths.

Current JCGM work is still actively revising uncertainty concepts for VIM4 and maintaining the GUM suite, reinforcing that even mature metrology remains conceptually revisable.

---

# 30. Psychometric stress — latent target is not directly observable

Psychometric/experimental psychology provides a decisive cross-regime stress.

Latent targets such as:

```text
memory
attention
confidence
```

are inferred/estimated through observable task variables.

This requires at least:

```text
construct specification
observable/task mapping
calibration/validation evidence
reliability analysis
model assumptions
CVE/population/task scope
```

Therefore:

```text
ObservableScore != LatentConstruct
ReliableScore != ValidConstructMeasurement
```

This regime preserves the WDF5 owner line while falsifying a narrow physical-instrument ontology.

---

# 31. Software metric stress — computable is not measurable

Example:

```text
P99 latency = 300 ms
```

This output is defined only relative to:

```text
request population
sampling window
clock
retry/exclusion semantics
aggregation implementation
version/topology
instrumentation
```

Even if computation is exact, target semantics can be wrong.

Therefore:

```text
ExactComputation != ValidMeasurement
```

and:

```text
SameMetricName != SameTargetDefinition across versions.
```

---

# 32. Institutional quantity stress — constructed does not mean arbitrary

Examples:

```text
unemployment rate
crime count
inflation index
GDP
school performance index
```

These targets can depend on institutional definitions/classification rules.

Thus:

```text
TargetConstitution may be rule-relative.
```

But once rules/CVE are fixed, claims can still be objectively right or wrong.

Therefore:

```text
ConstructedTarget != SubjectiveTarget
InstitutionRelative != Arbitrary
```

WDF5 must keep separate:

```text
TargetConstitution
MeasurementProcedure
ResultValidity
EvidenceUse
```

---

# 33. Synthetic-world / Agent measurement stress

Agents can create:

```text
new metrics
new target categories
adaptive sensing policies
cross-sensor fusion
learned estimators
new rule-world quantities
```

This creates additional failure modes:

```text
target drift
metric gaming
self-induced observation effects
adaptive sampling bias
reference mismatch
model-mediated proxy substitution
versioned target definition
```

But no `AgentMeasurement` primitive is needed.

The generic burden remains:

```text
What exactly is the target?
What makes the output about that target?
Under what reference/CVE?
With what uncertainty/comparability status?
```

---

# 34. Dynamic-target stress

Measurements often target systems that change during acquisition.

Needed separations:

```text
TargetTime
AcquisitionWindow
InstrumentResponseTime
SamplingRate
AggregationWindow
ResultTimeReference
```

Therefore:

```text
MeasurementOfDynamicTarget
!= MeasurementOfStaticSnapshot by default
```

Higher resolution or faster sampling is not automatically better if response/noise/target semantics change.

This creates a mandatory interface with future Time/Dynamics research without reopening them now.

---

# 35. Thermodynamic/coarse-graining stress

A coarse-grained measurement can systematically hide:

```text
microscopic transitions
dissipation
entropy production
rare events
```

Yet coarse-grained variables can still be objectively valid at their own CVE.

Thus:

```text
CoarseMeasurement != FalseMeasurement
```

but:

```text
CoarseMeasurementValidity(Q1)
!= AdequacyForFineGrainedClaim(Q2)
```

This directly reuses WDF3 effective-reality discipline.

---

# 36. Chance and uncertainty firewall

Measurement uncertainty may use probability distributions.

That does not imply the target Reality is objectively stochastic.

Therefore:

```text
MeasurementUncertainty
!= ObjectiveChance
```

Likewise an objectively stochastic target can be measured with additional measurement uncertainty.

Thus two uncertainty layers may coexist:

```text
TargetStochasticity
MeasurementUncertainty
```

without identity.

---

# 37. Ontic indeterminacy firewall

A broad/set-valued measurement result can arise because of:

```text
instrument uncertainty
sampling
model uncertainty
target-definition incompleteness
```

without implying ontic indeterminacy.

Conversely, a genuinely indeterminate target would require measurement semantics capable of representing indeterminacy rather than forcing a unique value.

Therefore:

```text
MeasurementUncertainty
!= OnticIndeterminacy
```

---

# 38. Gauge / representation firewall

Formal coordinates/representations may contain redundancy.

Therefore:

```text
NumericalCoordinate
!= DirectlyMeasurableRealityProperty by default
```

A quantity may be:

```text
gauge-invariant
relational
reference-frame dependent but objective
representation-dependent and nonphysical
```

Measurement validity requires theory/CVE grounding of the target role.

No universal `all formal variables are observables` assumption is allowed.

---

# 39. Hidden-assumption inventory — canonical A attack results

## HA1 — every measurable target has one unique true scalar value

```text
FALSIFIED as universal assumption.
```

## HA2 — measurement merely reveals a pre-existing property

```text
FALSIFIED as universal assumption.
```

Institutional/constructed targets and model-mediated measurands require target-constitution discipline.

## HA3 — indication = measured value = result

```text
FALSIFIED.
```

## HA4 — precision = accuracy = validity

```text
FALSIFIED.
```

## HA5 — reliability = validity

```text
FALSIFIED.
```

## HA6 — calibration = validation

```text
FALSIFIED.
```

## HA7 — traceability = correctness

```text
FALSIFIED.
```

## HA8 — all measurement requires SI-style units

```text
FALSIFIED as universal assumption.
```

## HA9 — all valid quantification is measurement

```text
FALSIFIED.
```

## HA10 — every number-producing procedure is measurement

```text
FALSIFIED.
```

## HA11 — target criteria are independent of measurement models

```text
FALSIFIED as universal assumption.
```

Some target specification/model interaction is constitutive to the claim.

## HA12 — uncertainty is random noise only

```text
FALSIFIED.
```

## HA13 — error and uncertainty are interchangeable

```text
FALSIFIED.
```

## HA14 — more resolution always means better measurement

```text
FALSIFIED.
```

## HA15 — measurement is purely epistemic

```text
REJECTED as complete characterization.
```

Measurement has epistemic use but also Reality interaction/reference/attribution semantics.

## HA16 — observation is measurement

```text
FALSIFIED.
```

## HA17 — sensing is measurement

```text
FALSIFIED.
```

## HA18 — causal interaction is sufficient for measurement

```text
FALSIFIED.
```

Random perturbation/interaction need not carry valid target information.

## HA19 — numerical representation is sufficient for measurement

```text
FALSIFIED.
```

## HA20 — one physical-metrology architecture applies unchanged across all regimes

```text
FALSIFIED.
```

## HA21 — model-mediated measurement is less real by definition

```text
FALSIFIED.
```

## HA22 — Agent-generated targets/metrics are subjective by definition

```text
FALSIFIED.
```

Scoped objectivity remains possible.

---

# 40. Additional hidden assumptions exposed by WDF5-A

## HA23 — reference = truth

```text
FALSIFIED.
```

References may be conventional/practical anchors.

## HA24 — standard = physical etalon = normative specification

```text
FALSIFIED by term overload.
```

## HA25 — comparability = compatibility

```text
FALSIFIED.
```

## HA26 — repeatability/reproducibility/reliability are one relation

```text
REJECTED by scope/condition dependence.
```

## HA27 — detection = measurement

```text
FALSIFIED.
```

## HA28 — proxy = target

```text
FALSIFIED.
```

## HA29 — benchmark score = capability measurement

```text
FALSIFIED as automatic inference.
```

## HA30 — operational definition exhausts target identity

```text
REJECTED.
```

## HA31 — measurement always requires a dedicated instrument

```text
REJECTED as universal assumption.
```

Model/calculation/comparison/counting can participate in measurement claims.

## HA32 — measurement is non-invasive

```text
FALSIFIED.
```

Instrument interaction can perturb the carrier/system.

## HA33 — measurement is one-step

```text
FALSIFIED.
```

Measurement commonly includes chains of sensing, transformation, calibration/model correction and attribution.

## HA34 — uncertainty is always adequately represented by one scalar

```text
NOT ESTABLISHED.
```

Structured/multidimensional/versioned uncertainty may be required.

## HA35 — target is static during measurement

```text
FALSIFIED.
```

## HA36 — same metric name across versions means same measurand/target

```text
FALSIFIED.
```

---

# 41. Current-use false-friend matrix

```text
Observation      -> noticing/recording phenomenon; not sufficient
Detection        -> presence/threshold decision; not sufficient
Sensing          -> direct interaction/transduction role; not sufficient
Indication       -> measuring-system output; not result by identity
Data             -> broad recorded representation; not measurement result by identity
Quantification   -> structured value/order assignment; broader than measurement
Measurement      -> target-valid attribution under declared structure
Estimation       -> inferential value assignment; may support measurement
Inference        -> reasoning relation; broader than measurement
Evidence         -> support relation; broader/different
Calibration      -> reference↔indication/result relation under conditions
Verification     -> requirement fulfillment
Validation       -> adequacy for intended use
Traceability     -> reference-provenance chain/bridge
Comparability    -> meaningful common-reference comparison
Compatibility    -> consistency under declared uncertainty criterion
Reliability      -> consistency/stability under conditions
Validity         -> intended-target/use support
Error            -> measured-reference discrepancy under semantics
Uncertainty      -> attributed-result uncertainty structure
Noise            -> unwanted variation/source
Resolution       -> distinguishable target-side change
Sensitivity      -> output response per target change
Selectivity      -> resistance to confounding quantities
Proxy            -> target surrogate candidate, not target identity
Score            -> procedure output
Index            -> composite representation
Metric           -> overloaded formal/performance quantity
Benchmark        -> test/reference protocol
Classification   -> label assignment/decision
OperationalDef   -> procedural semantics, not target exhaustion
```

---

# 42. A provisional measurement-situation inventory — research grammar only

WDF5-A does not freeze a positive Foundation, but the term inventory repeatedly requires the following slots for research bookkeeping:

```text
Target
TargetCriterion
AttributeRole
ReferenceStructure
Procedure/Interaction
MeasurementModel
Indication/Data
Result
UncertaintyStructure
ValidityEnvelope
Provenance/TraceabilityBridge
Comparison/CompatibilityClaim
```

This is only a **research inventory**.

Do not infer production schema or metaphysical primitives.

The next round must try to delete/compress these slots rather than preserve them by naming inertia.

---

# 43. Measurement / Quantification owner-line status after A

A was explicitly allowed to split the owner line if current-use analysis demonstrated incoherence.

It did not.

Instead:

```text
Quantification
= formal value/order/scale construction family

Measurement
= Reality-targeting validity family that often consumes quantification
```

Their nonidentity is itself one of the most important WDF5 distinctions.

Shared owner question:

```text
When does a structured value/ordering/result legitimately count as
measurement/quantification of a Reality target under explicit criteria,
reference/comparison semantics and uncertainty/validity conditions?
```

Therefore:

```text
WDF5 Owner Line = RETAINED
Project split = NOT EARNED
```

---

# 44. Candidate rival theories exposed for future destructive comparison

WDF5-A does not rank these yet.

At minimum:

```text
R1 Representational measurement theory
R2 Operationalist / conventionalist accounts
R3 Realist true-value / quantity accounts
R4 Uncertainty-oriented metrology
R5 Model-based measurement accounts
R6 Information-theoretic accounts
R7 Causal interaction / detection accounts
R8 Structural / relational quantity accounts
R9 Construct-validity / psychometric accounts
R10 Typed plural / thin common architecture
R11 Eliminativist/decomposition control:
    no generic measurement relation beyond domain-local practices
```

No winner is admitted in A.

---

# 45. Strongest residual tensions after A

## Residual 1 — What is the minimal truth condition for Measurement?

Current-use distinctions tell us what Measurement is not, but not yet the minimal positive condition.

## Residual 2 — Measurement vs Quantification composition

Does every measurement require a quantitative/ordinal value structure, or can some valid measurement be non-quantitative in a stronger sense?

## Residual 3 — Target constitution

When is the target discovered, selected, operationally specified, institutionally constituted, model-induced or merely proxied?

## Residual 4 — Reference architecture

What is common among:

```text
physical standards
reference procedures
conventional scales
population norms
benchmark definitions
institutional baselines
versioned digital references
```

without creating one fake universal `Standard` primitive?

## Residual 5 — Uncertainty architecture

Need to compare:

```text
instrumental
sampling
model
reference/calibration
definitional
stochastic
version/regime
unknown-unknown / inadequacy
```

without collapsing error/chance/ignorance.

## Residual 6 — Validity

Need to separate:

```text
measurement validity
construct validity
procedure validation
model validity
causal validity
fit-for-purpose
```

## Residual 7 — Cross-regime comparability

How can results remain comparable across:

```text
instruments
labs
populations
versions
metric definitions
models
institutions
Agent-generated targets
```

## Residual 8 — Dynamic/change-sensitive measurement

Time/sample/response/CVE must become explicit.

---

# 46. Foundation reopen audits

## WDF0

WDF5-A repeatedly relies on:

```text
Reality != Observation != Evidence != Representation
Relative != Subjective
Model != Reality
```

No contradiction.

```text
FoundationReopenCondition(WDF0) = NOT FIRED
```

## WDF1

Measurement uncertainty and objective chance remain separate.

No typed-modal claim fails.

```text
FoundationReopenCondition(WDF1) = NOT FIRED
```

## WDF2

Comparison/reference and alternative calibration choices do not falsify counterfactual architecture.

```text
FoundationReopenCondition(WDF2) = NOT FIRED
```

## WDF3

WDF5-A provides major independent pressure on:

```text
Criterion
CVE
Representation/Reality
Identity/equivalence
Effective Reality
Approximation
Naturalness/objective carving
Relation vs Evidence
```

No exact claim is falsified.

```text
ExactWDF3ClaimFalsified = NONE
WDF3 Foundation v1 = NOT FROZEN
```

## WDF4

Measurement validity is not causal validity.

No WDF4 RC1–RC8 fires.

```text
FoundationReopenCondition(WDF4) = NOT FIRED
```

---

# 47. External anchors used in A

These sources are falsifier/terminology anchors, not universal ontological authority.

## JCGM/BIPM VIM3 and current JCGM work

Used for mature distinctions among:

```text
measurement
measurand
measurement result
measured value
true value
accuracy
trueness
precision
uncertainty
calibration
traceability
comparability
compatibility
sensor
detector
indication
resolution
sensitivity
selectivity
detection limit
```

JCGM is actively maintaining the GUM and preparing VIM4, including continued revision of the concept of measurement uncertainty.

## Dominik R. Bach (2024), Psychometrics in experimental psychology: A case for calibration

Used as cross-regime pressure that latent constructs are not directly accessible and require validity/calibration bridges from observable variables.

## Philosophy-of-measurement literature

Representational, operationalist, realist, information-theoretic and model-based traditions are retained as rival families rather than collapsed.

---

# 48. WDF5-A final results

```text
A1 Quantification != Measurement.
A2 Observation != Detection != Sensing != Measurement.
A3 Indication != MeasuredValue != MeasurementResult.
A4 Data != MeasurementResult.
A5 TargetSystem != TargetAttribute != ActualInteractionQuantity.
A6 Property != Attribute != Quantity != Construct.
A7 NumericLabel != Quantity; scale type controls meaningful operations.
A8 Scale != Unit != Reference != Standard.
A9 Calibration != Verification != Validation.
A10 Traceability != Correctness != Validity.
A11 Comparability != Compatibility != Equality.
A12 Accuracy != Trueness != Precision != Reliability != Validity.
A13 Noise != Error != Uncertainty != Mistake.
A14 UniqueTrueScalarValue is not a universal measurement assumption.
A15 Resolution != Sensitivity != Selectivity != DetectionLimit.
A16 Sampling != Measurement.
A17 Estimation != Measurement.
A18 Inference != Measurement.
A19 Evidence != Measurement.
A20 ModelMediatedMeasurement can be fully real/valid.
A21 Proxy != Target.
A22 Score/Index/Metric/Benchmark do not become measurement by naming.
A23 Threshold/Classification != MeasurementResult.
A24 OperationalDefinition != TargetIdentity by default.
A25 Physical metrology is a mature regime, not universal WDF5 ontology.
A26 Reliability != Validity survives psychometric stress.
A27 ExactComputation != ValidMeasurement survives software stress.
A28 ConstructedTarget != Subjective/UnrealTarget survives institutional stress.
A29 No AgentMeasurement primitive is needed.
A30 MeasurementUncertainty != ObjectiveChance != OnticIndeterminacy.
A31 FormalCoordinate != DirectlyMeasurableRealityProperty by default.
A32 Measurement/Quantification owner line survives provisionally.
A33 No positive Foundation architecture is frozen.
```

---

# 49. Canonical frontier after WDF5-A

```text
WDF0 = FROZEN
WDF1 = FROZEN
WDF2-A→N = completed research history
WDF2-O = NOT ADMITTED
WDF3-A→L = completed research history
WDF3 Foundation v1 = NOT FROZEN
WDF3-M = UNKNOWN / NOT ADMITTED
WDF4-A→F = completed research history
WDF4 Foundation v1 = FROZEN
WDF4-G = NOT ADMITTED

WDF5 = ADMITTED
WDF5-A = COMPLETE
WDF5 Foundation v1 = DOES NOT EXIST
WDF5-B = UNKNOWN / NOT ADMITTED

OwnerLineCoherence(WDF5) = PROVISIONALLY SURVIVES
FoundationReopenCondition(WDF0) = NOT FIRED
FoundationReopenCondition(WDF1) = NOT FIRED
FoundationReopenCondition(WDF2) = NOT FIRED
ExactWDF3ClaimFalsified = NONE
FoundationReopenCondition(WDF4) = NOT FIRED

WholeWorldClosure = NOT ESTABLISHED
Production = UNCHANGED
```

---

# 50. Next-route rule after A

WDF5-A is complete, but it does **not** automatically admit WDF5-B.

The next research move must first decide which residual has the strongest destructive information value.

Candidate shapes include:

```text
B1 matched measurement/non-measurement boundary falsification
B2 rival measurement-theory tournament
B3 target/attribute/quantity/construct ontology
B4 reference/scale/comparability architecture
B5 error/uncertainty/validity architecture
B6 cross-regime measurement composition stress
```

Do not inherit this list as roadmap.

A fresh residual/falsifier comparison must decide whether one of these earns WDF5-B and what B actually is.

No production engineering change is admitted.
