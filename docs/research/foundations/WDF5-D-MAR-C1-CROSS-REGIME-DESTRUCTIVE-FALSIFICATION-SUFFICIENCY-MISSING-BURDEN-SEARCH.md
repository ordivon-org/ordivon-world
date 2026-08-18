# WDF5-D — MAR-C1 Cross-Regime Destructive Falsification / Sufficiency & Missing-Burden Search

Date: 2026-08-18

Status: **WDF5-D COMPLETE / MAR-C1 JOINT SUFFICIENCY FALSIFIED / G AND A NECESSITY SURVIVE PROVISIONALLY / THIRD BURDEN REOPENED AS MEASUREMENT-ADMISSIBILITY OF EVALUATION STRUCTURE / WDF5-E ADMITTED / NO FOUNDATION FREEZE**

Canonical upstream:

```text
WDF5-A = COMPLETE
WDF5-B = COMPLETE
WDF5-C = COMPLETE

MAR-C1
= ValidMeasurementAttribution
  requires:

  G = Target-Relevant Actuality Grounding
  A = Attribution Correspondence

  under inherited WDF3 Criterion / CVE
```

WDF5-D does not improve MAR-C1 by default.

Its mandate is to destroy:

```text
G necessity
A necessity
G/A independence
G + A joint adequacy
```

and to search for a missing independent burden.

---

# 1. D headline result

D finds one exact falsifier of MAR-C1 joint sufficiency:

```text
A valid nominal-property / qualitative classification can satisfy:

G = YES
A = YES

while still being an examination / classification / diagnostic result
rather than measurement in a narrower measurement-science sense.
```

Examples:

```text
blood type = A
shape = cube
pregnancy test = positive
conformity status = pass
instructional category = level C
```

These can be:

```text
actually grounded in the target/sample
correctly attributed under an adequate bridge
semantically well defined
highly reliable
```

without thereby becoming a quantity measurement.

Thus:

```text
G + A
!= sufficient to distinguish Measurement
from Valid Property Evaluation / Examination / Classification.
```

Canonical D conclusion:

```text
MAR-C1 JointSufficiency = FALSIFIED
```

This is the first direct falsifier of C's claim that no third independent burden had been found.

---

# 2. Why this falsifier is not merely lexical

The obvious reaction would be:

```text
"BIPM simply chooses to reserve measurement for quantities;
we can define measurement more broadly and ignore the distinction."
```

D rejects that as insufficient.

The external theory space contains at least three materially different positions:

```text
P1 Narrow quantity-metrology:
   measurement applies to quantities;
   nominal properties are examined/classified.

P2 Stevens-style broad assignment:
   nominal/ordinal/etc. scales may all be called measurement scales.

P3 Cross-science property-evaluation view:
   property evaluation is broader than measurement;
   measurement is a specific kind of evaluation;
   the exact quantitative/non-quantitative boundary is itself revisable/contested.
```

Therefore the falsifier exposes a real unresolved structural question:

```text
What makes an actuality-grounded, correct property-value attribution
specifically a measurement rather than another valid evaluation?
```

That question was hidden when C absorbed all value/evaluation semantics into A.

---

# 3. Official metrology falsifier — nominal property examination

JCGM/VIM3 explicitly states:

```text
Measurement does not apply to nominal properties.
```

A nominal property has no magnitude but can have a value such as:

```text
sex
paint colour
country code
amino-acid sequence
```

VIM reference-material terminology also distinguishes:

```text
measurement of quantities
vs
examination of nominal properties
```

and notes that a nominal-property examination may have associated uncertainty that is not measurement uncertainty.

This supplies an exact G+A non-measurement case under the VIM regime.

Important:

```text
VIM is a falsifier regime, not universal WDF5 authority.
```

---

# 4. FDA qualitative-diagnostic falsifier

FDA diagnostic guidance explicitly distinguishes:

```text
quantitative test result
vs
qualitative test result
```

and notes that qualitative final results may be positive/negative even when the underlying measurement is quantitative.

Thus one pipeline can contain:

```text
underlying quantitative measurement
-> threshold / interpretation
-> qualitative diagnostic result
```

The qualitative decision can have:

```text
actual sample grounding
validated target-condition correspondence
reference-standard comparison
known sensitivity/specificity
```

without being identical to the underlying quantitative measurement.

This independently supports:

```text
ValidTargetClassification
!= MeasurementResult by identity.
```

---

# 5. Cross-science pressure — measurement is a specific kind of evaluation

Mari / Wilson / Maul provide a broader cross-science framework than VIM.

Their framework:

```text
extends measurement beyond physical quantities
includes psychosocial properties
characterizes measurement as an empirical process producing property values
```

but also explicitly says:

```text
property evaluation is broader;
measurement is a specific kind of evaluation.
```

Their analysis of nominal vs quantitative properties further notes:

```text
blood type is classificatory
nominal/ordinal/interval/ratio are better treated as evaluation structures
Stevens' broadest assignment-based definition is too broad for measurement
```

while also acknowledging that whether only quantities are called measurable can involve lexical/conventional choice.

Therefore D cannot solve the problem by simply importing:

```text
quantity only
```

as a WDF5 axiom.

The deeper residual is the **measurement-admissibility of an evaluation structure**.

---

# 6. Exact C claim falsified

C established:

```text
M4 Value / Comparison Semantics
independent root = deleted / absorbed into A.
```

D shows this compression was too strong.

A can be fully adequate for a nominal classification:

```text
actual blood sample
-> validated assay/classification bridge
-> ABO value A
```

Yet the result remains outside narrow quantity measurement.

Therefore:

```text
AttributionCorrespondence
cannot by itself decide whether the attributed value/status
belongs to a measurement-admissible evaluation structure.
```

Canonical revision:

```text
C claim "M4 fully absorbed into A for sufficiency"
= FALSIFIED
```

This does not reopen WDF0–WDF4.

It revises only the provisional WDF5 MAR-C1 research architecture.

---

# 7. What third burden is actually earned?

D does **not** establish:

```text
Measurement requires SI quantity
Measurement requires real-valued magnitude
Measurement requires ratio/interval scale
Measurement requires numeric representation
Measurement excludes every nominal-property evaluation by metaphysical law
```

Instead D establishes a weaker, structurally independent burden:

# **E — Measurement-Admissibility of Evaluation Structure**

Working form:

```text
E asks whether the target-property/result relation belongs to an
admissible measurement-evaluation kind rather than mere classification,
examination, detection, decision, or arbitrary property evaluation.
```

This burden is independent because:

```text
G can be true
A can be true
E can still fail or remain disputed.
```

Canonical shorthand:

```text
E = Evaluation-Structure / Measurement-Admissibility burden
```

Its positive content is NOT frozen in D.

---

# 8. MAR-D1 — revised provisional architecture

D replaces MAR-C1 with a provisional three-burden residual:

# **MAR-D1**

```text
ValidMeasurementAttribution(R, V:P(T) | K,CVE)
requires:

G — Target-Relevant Actuality Grounding

A — Attribution Correspondence

E — Measurement-Admissible Evaluation Structure

with K/CVE inherited from WDF3.
```

But:

```text
G = comparatively mature
A = comparatively mature
E = OPEN / UNDERDETERMINED
```

Therefore MAR-D1 is not Foundation v1.

---

# 9. D attack DF1 — valid measurement without G

D searches for accepted measurement cases lacking target-relevant actuality grounding.

Candidates:

```text
pure computation
simulation
future prediction
counterfactual estimate
mathematical measure
static source-code metric
```

Result:

```text
no convincing ValidMeasurementAttribution without some actuality grounding
was found within the intended empirical/property measurement scope.
```

Pure computation can calculate values but lacks target-world acquisition.

Simulation/prediction can produce well-formed values but do not measure the unactualized target instance.

A static formal object may be counted/evaluated by computation, but whether such operations are called measurement is a distinct formal/lexical use rather than a falsifier of empirical WDF5 measurement.

Disposition:

```text
G Necessity = SURVIVES D PROVISIONALLY
```

---

# 10. D attack DF2 — valid measurement without A

Candidates:

```text
direct physical comparison
raw calibrated readout
state introspection
simple counting
```

In each case, if the result is genuinely a valid measurement attribution, at least a thin A remains:

```text
which target property?
which result value?
why does this indication/comparison/count instantiate that value?
```

A may be trivial or identity-like, but not absent.

Disposition:

```text
A Necessity = SURVIVES D PROVISIONALLY
```

---

# 11. D attack DF3 — G+A non-measurement

This attack succeeds.

Canonical counterexamples:

```text
nominal-property examination
qualitative diagnostic classification
conformity decision
property classification
```

Thus:

```text
G+A JointAdequacy = FALSIFIED
```

This is D's exact architecture-changing result.

---

# 12. D attack DF4 — lucky correct result

No change.

```text
CorrectValueByLuck
!= ValidMeasurementAttribution
```

A defective chain can accidentally output a correct result while failing G/A/E validity.

MAR-D1 remains provenance-sensitive.

---

# 13. D attack DF5 — black-box learned sensor

Question:

```text
Does a learned model require a new "Interpretability" root burden?
```

NIST's autonomous metrology program uses physics-informed machine learning to track latent sensor drift, compensate quantum/photonic sensors, and support self-correcting calibration.

This provides a real regime where:

```text
learned model / adaptive calibration
```

participates in measurement without human-transparent closed-form mapping being a universal requirement.

D therefore distinguishes:

```text
ActualA
!= HumanInterpretabilityOfA
```

A bridge can be objectively adequate even if its internal mapping is difficult to interpret.

Interpretability affects:

```text
validation
evidence
auditability
failure localization
```

not universal measurement truth by identity.

Disposition:

```text
InterpretabilityRoot = NOT EARNED
```

---

# 14. D attack DF6 — self-calibrating adaptive Agent metric

Adaptive systems can change:

```text
sensing policy
calibration model
feature selection
metric definition
```

Potential failure:

```text
metric optimization causes the metric to cease tracking the intended target.
```

Goodhart-style RL results demonstrate a formal version of this: increasing optimization of an imperfect proxy can eventually reduce performance on the true objective.

WDF5 interpretation:

```text
G may remain strong:
  lots of real measurements/logs/data.

A may degrade:
  proxy-target correspondence no longer holds under the optimized regime.
```

Thus adaptive/Goodhart failure is naturally typed as:

```text
A/CVE failure
```

plus target-version issues in WDF3.

No fourth root is needed.

---

# 15. D attack DF7 — synthetic-world direct state introspection

A virtual-world object has realized internal state:

```text
object.hp = 73
```

An authorized state read can satisfy G.

If the target property is exactly the realized internal `hp` field and the bridge is identity-like, A holds.

Whether this is measurement or state inspection depends on E / evaluation-kind conventions.

Thus synthetic introspection does not falsify G/A.

Instead it strengthens the E residual:

```text
actuality-grounded exact attribution
can still leave the term "measurement" boundary unsettled.
```

---

# 16. D attack DF8 — historical proxy reconstruction

Historical cases use:

```text
tree rings
fossils
sediment cores
archival images
historical logs
```

G can be provided by actual traces.

A determines whether the trace is legitimately attributable as a value of the historical target or merely predicts/correlates with it.

If competing bridge models remain unresolved:

```text
AttributionStatus = UNKNOWN / model-contested
```

rather than forcing a new root burden.

Disposition:

```text
HistoricalTrace = no new root
```

---

# 17. D attack DF9 — nonprobability population sample

A nonprobability sample is genuinely actuality-grounded in actual respondents.

But an attribution to a target population may fail because the sample-to-population bridge is not adequate.

Thus:

```text
sample-level G = YES
population-level A = potentially NO / UNKNOWN
```

No new burden is required.

---

# 18. D attack DF10 — latent construct with competing models

Two psychometric models can map the same actual responses to different latent target values.

This does not eliminate A.

It shows:

```text
A may be theory-relative and underdetermined.
```

If evidence cannot discriminate:

```text
AttributionCorrespondence = UNKNOWN / competing
```

rather than:

```text
both are automatically valid measurements.
```

No new root emerges.

---

# 19. D attack DF11 — quantum/contextual measurement

Quantum theory is a major stress because the technical term `measurement` often denotes an operation/instrument whose outcome can affect the post-measurement state.

Modern quantum-instrument formalism explicitly models:

```text
measurement outcome
+
outcome-dependent post-measurement state
```

as a joint quantum-classical process.

Experimental work on weak measurement likewise makes measurement disturbance itself an explicit object of study.

D conclusion:

```text
PassiveRevelationOfPreexistingValue
!= UniversalMeasurementRequirement
```

A quantum measurement operation can satisfy G through actual system-apparatus interaction.

A can be supplied by the declared observable/POVM/instrument/context semantics when a target-value attribution is made.

If the measurement changes the state, WDF3 Criterion/CVE must specify whether the claim concerns:

```text
pre-measurement state
contextual outcome probability
measurement event outcome
post-measurement state
```

No fourth root is required.

However generalized quantum `measurement` can also function as a broader process term with discrete outcome labels not obviously equivalent to classical quantity measurement.

Therefore quantum terminology reinforces:

```text
MeasurementProcedure/Execution
!= ValidMeasurementAttribution
```

and adds pressure to E rather than falsifying G/A.

---

# 20. D attack DF12 — qualitative / ordinal borderline

Ordinal cases survive as likely measurement-capable in both physical and psychosocial regimes:

```text
hardness ordering
ordered proficiency level
pain/severity ordering under defensible scale structure
```

Therefore E cannot be:

```text
must support interval arithmetic
must support ratios
must be real-valued
```

At minimum, an ordinal structure may be measurement-capable.

Nominal classification remains the hard boundary case.

Thus:

```text
E != CardinalityRequirement
```

---

# 21. D attack DF13 — nominal classification / diagnostic test

This is the exact successful falsifier.

Pipeline:

```text
actual sample/person/object
-> valid acquisition / assay / test
-> valid correspondence
-> nominal result
```

Examples:

```text
blood type = A
pregnancy = positive
pathogen detected = yes
shape = cube
```

This can satisfy G and A.

Whether it is called measurement differs across traditions.

Therefore:

```text
E is genuinely independent from G and A.
```

But its positive criterion remains open.

---

# 22. D attack DF14 — institution-rule change across time

Suppose unemployment definition changes between v1 and v2.

Same records and same number can have different target semantics.

This is handled by:

```text
WDF3 target criterion/version
+
A bridge version
+
CVE/time
```

No new root.

Cross-version comparability remains downstream.

---

# 23. D attack DF15 — same numeric result / changed target criterion

Example:

```text
"95% availability"
```

under two different denominator/inclusion definitions.

G may be valid in both.

A is target/version-specific.

Thus:

```text
SameNumber != SameMeasurementClaim
```

No new root.

---

# 24. D attack DF16 — direct comparison without explicit model

A rod directly compared with a reference length can constitute measurement without an explicit mathematical model document.

A exists as a thin comparison correspondence.

Thus:

```text
ExplicitModel != A
```

No new root.

---

# 25. D attack DF17 — long derived-measurement chain

Long chains do not automatically destroy G.

Example:

```text
raw detector states
-> calibrated intermediate quantities
-> corrected quantities
-> derived model quantity
-> final target attribution
```

G composes if the provenance chain remains actuality-grounded and each transformation is admissible under A.

Failure can occur by:

```text
broken upstream measurement
invalid derivation
scope mismatch
version mismatch
```

but no new root is required.

---

# 26. D attack DF18 — coarse macro measurement

No change.

A macro quantity can be validly measured under a declared coarse grain even when fine-grained dynamics are hidden.

```text
G = macro-relevant actuality grounding
A = macro attribution correspondence
K/CVE = declared grain
```

No new root.

---

# 27. D attack DF19 — Goodharted metric

Goodhart pressure creates a particularly strong dynamic case.

At time t0:

```text
metric M
may have adequate A to target T.
```

After M becomes an optimization target:

```text
agents adapt
selection changes
behavior changes
M-T relation degrades
```

Then:

```text
G(M) may remain excellent
A(M,T | regime t1) may fail
```

Thus:

```text
MeasurementValidity is regime/history sensitive.
```

This is an A+CVE issue rather than a new root.

---

# 28. D attack DF20 — measurement changes / constitutes target state

Cases:

```text
quantum measurement disturbance
Hawthorne-like behavioral change
reactive surveys
adaptive diagnostics
```

These defeat the hidden assumption:

```text
measurement must passively reveal an unchanged preexisting state.
```

They do not defeat G/A.

Instead the target criterion must specify:

```text
pre-interaction property
interaction-relative property
outcome of the measurement event
post-interaction property
```

If measurement participates in constituting the target value, this is a WDF3 constitution/criterion problem plus A semantics.

No fourth root is earned.

---

# 29. G/A independence survives D

D finds no reason to collapse the two axes.

The canonical 2×2 matrix still holds at the level of broad valid property evaluation:

```text
                    A
                 NO       YES

G = NO          arbitrary prediction/simulation

G = YES         signal/   valid property evaluation
                proxy
```

What D changes is the upper-right interpretation:

```text
G=YES + A=YES
=> Valid Property Evaluation Attribution
```

not automatically:

```text
=> Valid Measurement Attribution.
```

This is the key architecture correction.

---

# 30. Reinterpretation of MAR-C1

MAR-C1 was too specifically named.

D shows its two-axis core more safely characterizes:

# **PEA-D1 — Property Evaluation Attribution Core**

```text
ValidPropertyEvaluationAttribution
requires:

G — Actuality Grounding
A — Attribution Correspondence
under K/CVE.
```

Measurement is then a subtype whose additional admissibility condition is unresolved.

This is a substantial conceptual correction.

---

# 31. Measurement vs Evaluation

Canonical after D:

```text
Evaluation
= assigning/establishing a value/status of a target property
  under a declared reference/classification/result structure.

ValidPropertyEvaluationAttribution
= G + A under K/CVE.

Measurement
= some proper or possibly context-dependent subtype of valid property evaluation,
  requiring an additional measurement-admissibility condition E.
```

E may turn out to depend on:

```text
quantitativeness
order/comparability
empirical distinguishability
scale structure
property type
measurement purpose
```

or some different condition.

D does not preselect.

---

# 32. Measurement vs Quantification after D

The owner line becomes more interesting, not less coherent.

```text
Quantification
= structured value/order/scale construction/use.

Property Evaluation
= actuality-grounded attribution of property values/statuses.

Measurement
= measurement-admissible property evaluation.
```

Possible relations:

```text
Quantification without evaluation
Evaluation without quantification
Measurement with weak/ordinal quantification
Measurement with cardinal quantification
Nominal evaluation that may or may not count as measurement by theory
```

Therefore:

```text
WDF5 OwnerLineCoherence = SURVIVES D
```

but the positive architecture now needs an explicit Evaluation layer.

---

# 33. Does D force project renaming?

No.

The admitted WDF5 route remains:

```text
Measurement / Quantification / Reference / Comparability Architecture
```

because Evaluation is currently an internal explanatory supertype discovered by destructive research.

Canonical project renaming is not earned yet.

A later round could revise the name only if Measurement becomes demonstrably non-central or owner-line boundaries split.

That has not happened.

---

# 34. Third burden status

C concluded:

```text
ThirdRootBurden = NOT FOUND.
```

D revises this to:

```text
ThirdIndependentBurden = FOUND
```

but with an important qualifier:

```text
The burden is not yet a positive root primitive.

It is an unresolved measurement-admissibility discriminator
between valid property evaluation and measurement.
```

Canonical:

```text
E = ADMITTED AS RESEARCH BURDEN
E positive architecture = UNKNOWN
```

---

# 35. MAR-D1 status

```text
MAR-D1
= G + A + E under WDF3 K/CVE
```

is only a placeholder skeleton.

Because E is undefined, MAR-D1 is not a closed theory.

Therefore:

```text
WDF5 Foundation v1 = DOES NOT EXIST
```

and Foundation freeze remains inadmissible.

---

# 36. External source synthesis

## JCGM/VIM3

Supports the narrow-regime falsifier:

```text
measurement applies to quantities
nominal properties are examined rather than measured
nominal-property uncertainty != measurement uncertainty
```

## FDA qualitative diagnostics

Supports pipeline separation:

```text
underlying quantitative measurement
can feed a qualitative final test result
```

with positive/negative outcomes treated separately from quantitative results.

## Mari / Wilson / Maul

Provides the strongest broad cross-science pressure:

```text
measurement is empirical/property-directed
measurement extends beyond classical physical metrology
property evaluation is broader than measurement
measurement is a specific kind of evaluation
nominal/ordinal/etc. structures belong to evaluation theory
```

and explicitly notes that the exact quantitative/non-quantitative measurability boundary remains conceptually nontrivial.

## NIST autonomous metrology

Shows learned/adaptive calibration can be a legitimate measurement realization without generating an interpretability root.

## Quantum-instrument literature

Shows quantum measurement is outcome-generating and state-transforming, reinforcing process/result typing and falsifying passive-revelation assumptions.

## Goodhart RL literature

Shows adaptive optimization can break proxy-target correspondence while the metric remains precisely and actuality-groundedly observed, reinforcing A/CVE failure typing.

---

# 37. Foundation reopen audit

## WDF0

No claim fails.

D strengthens:

```text
Measurement != Representation
Measurement != Evidence
Measurement != Classification by default
```

```text
FoundationReopenCondition(WDF0) = NOT FIRED
```

## WDF1

No modal/chance architecture fails.

```text
FoundationReopenCondition(WDF1) = NOT FIRED
```

## WDF2

Prediction/counterfactual remain distinct from actuality-grounded evaluation.

```text
FoundationReopenCondition(WDF2) = NOT FIRED
```

## WDF3

D relies on Criterion/CVE/version/constitution distinctions.

No exact claim is falsified.

```text
ExactWDF3ClaimFalsified = NONE
WDF3 Foundation v1 = NOT FROZEN
```

## WDF4

Quantum disturbance and reactive measurement do not identify measurement with causation.

```text
FoundationReopenCondition(WDF4) = NOT FIRED
```

---

# 38. WDF5-C internal reopen result

This is not an earlier Foundation reopen.

It is a direct falsification of provisional C architecture:

```text
C claim:
M4 local value/evaluation semantics can be fully absorbed into A
with no third independent burden.

D falsifier:
valid nominal property evaluation satisfies G+A
but does not automatically qualify as measurement.
```

Therefore:

```text
MAR-C1 = REVISED / NOT FROZEN
PEA-D1 = broader surviving core
E = newly reopened measurement-specific residual
```

---

# 39. Fresh post-D residual universe

D derives a new route set from its actual falsifier:

```text
E-R1 Measurement vs Evaluation / Classification / Examination boundary

E-R2 Measurement-admissible Value / Quantity / Order / Scale structure

E-R3 Quantum / contextual / intervention-relative measurement semantics

E-R4 Reference / Comparability / Transport architecture

E-R5 Quality / Uncertainty / Validity architecture

E-R6 Actuality-grounding provenance composition

E-R7 No-measurement-specific-core control:
     "measurement" is only a lexical/practice label over PEA-D1 + local conventions
```

---

# 40. E-R3 assessment — quantum/contextual route

Quantum is high-value stress but did not break G/A.

Its strongest contribution is to process/result typing and context-sensitive target semantics.

It is not currently the best route for resolving the exact D falsifier.

Disposition:

```text
STRONG SPECIAL-REGIME STRESS
NOT NEXT WINNER
```

---

# 41. E-R4 Reference / Comparability

Still a real downstream continent.

But it does not answer why nominal classification differs from measurement.

Disposition:

```text
STRONG DOWNSTREAM
```

---

# 42. E-R5 Quality / Uncertainty / Validity

Still important but orthogonal to the exact D falsifier.

A nominal classification can have excellent quality and uncertainty characterization while remaining a classification.

Disposition:

```text
STRONG DOWNSTREAM
```

---

# 43. E-R6 Actuality-grounding provenance

G survived D without architecture-changing falsification.

No need to deepen G before resolving E.

Disposition:

```text
DEFERRED
```

---

# 44. E-R7 lexical-control route

This is a serious control:

```text
Perhaps there is no World-native distinction between measurement and other valid property evaluations.
Perhaps communities simply reserve the word differently.
```

D does not reject this control.

Mari/Wilson/Maul explicitly note that whether only quantities are measurable may partly be an arbitrary lexical choice.

Therefore the next round must test whether a non-lexical measurement-specific discriminator exists.

This makes E-R7 a mandatory rival inside the next round.

---

# 45. E-R1 and E-R2 merge

The exact D falsifier cannot be solved by treating:

```text
Measurement vs Evaluation boundary
```

and:

```text
Value / Quantity / Order / Scale structure
```

as independent next rounds.

The major candidate explanation for the boundary is precisely evaluation structure.

Therefore they merge into one tournament.

---

# 46. WDF5-E admission

D admits:

# **WDF5-E — Measurement vs Evaluation / Classification / Examination & Measurement-Admissible Value-Structure Boundary Reconstruction**

Working question:

> Among actuality-grounded, correctly attributed property evaluations, what—if anything beyond linguistic convention—makes some evaluations measurements while others are examinations, detections, classifications, diagnoses, decisions or nominal evaluations; is quantity/magnitude necessary, is ordinal comparability sufficient, can non-quantitative psychosocial or quantum cases still count as measurement, and does a World-native Measurement-Admissibility burden E survive destructive comparison against the control that `measurement` is merely a domain-relative lexical/practice label over a more fundamental Property Evaluation Attribution architecture?

WDF5-E is research-only.

No positive E theory is preselected.

---

# 47. Mandatory WDF5-E rival positions

At minimum:

```text
E-T1 VIM quantity-only / nominal-examination boundary

E-T2 Stevens-style nominal/ordinal/interval/ratio broad measurement

E-T3 Mari/Wilson/Maul property-measurement vs broader evaluation framework

E-T4 Ordinal-or-richer measurement threshold

E-T5 Empirical-comparability / distinguishability threshold

E-T6 Pragmatic measurement-purpose account

E-T7 Property-structure realism account

E-T8 Quantum generalized-measurement challenge

E-T9 Diagnostic/examination/classification practice challenge

E-T10 Lexical/domain-relative eliminativist control
```

---

# 48. Mandatory WDF5-E cases

```text
blood type
colour class
shape class
binary pregnancy test
pathogen present/absent
binary threshold detector
ordinal hardness
ordered disease stage
reading comprehension score
Likert-style rating
count of entities
software state category
P99 latency
conformity pass/fail
quantum binary outcome
POVM outcome labels
continuous quantum observable
Agent-generated categorical metric
Agent-generated ordinal metric
classification derived from underlying quantitative measurement
same property evaluated nominally vs ordinally vs quantitatively
```

---

# 49. WDF5-D canonical results

```text
D1 G necessity survives provisionally.

D2 A necessity survives provisionally.

D3 G/A independence survives.

D4 G+A joint sufficiency for Measurement is FALSIFIED.

D5 Exact falsifier: valid nominal-property / qualitative evaluation can satisfy G+A
   while remaining examination/classification under major measurement regimes.

D6 C's complete absorption of M4 into A is falsified.

D7 PEA-D1 survives as broader core:
   ValidPropertyEvaluationAttribution = G + A under WDF3 K/CVE.

D8 Measurement requires an additional independent research burden E:
   Measurement-Admissibility of Evaluation Structure.

D9 E is not yet defined and cannot be equated with SI/numerical/cardinal quantity.

D10 Ordinal cases prevent cardinal/numeric overrestriction.

D11 Quantum/state-changing measurement does not create a fourth root;
    it reinforces process/result/context typing.

D12 Black-box learned sensors do not require interpretability as a truth root.

D13 Goodhart/adaptive metric failures are A/CVE failures, not a new root.

D14 Historical, sampled, indirect, synthetic and coarse-grained cases do not
    falsify G/A when correctly scoped.

D15 MAR-D1 = G + A + open E under WDF3 K/CVE is provisional only.

D16 WDF5 Foundation v1 remains nonexistent.

D17 WDF5-E is admitted to reconstruct the exact measurement/evaluation boundary.
```

---

# 50. Canonical frontier after WDF5-D

```text
WDF5 = ADMITTED

WDF5-A = COMPLETE
WDF5-B = COMPLETE
WDF5-C = COMPLETE
WDF5-D = COMPLETE

MAR-C1
= FALSIFIED AS JOINTLY SUFFICIENT

PEA-D1
= PROVISIONAL BROADER CORE
= ValidPropertyEvaluationAttribution
  requires G + A under WDF3 K/CVE

MAR-D1
= PROVISIONAL MEASUREMENT SKELETON
= G + A + open E under WDF3 K/CVE

G
= Target-Relevant Actuality Grounding
= survives provisionally

A
= Attribution Correspondence
= survives provisionally

E
= Measurement-Admissibility of Evaluation Structure
= INDEPENDENT RESEARCH BURDEN ADMITTED
= POSITIVE CONTENT UNKNOWN

WDF5-E
= ADMITTED
= Measurement vs Evaluation / Classification / Examination
  & Measurement-Admissible Value-Structure Boundary Reconstruction

WDF5-E execution
= NOT STARTED

WDF5 Foundation v1
= DOES NOT EXIST

WDF5-F+
= UNKNOWN / NOT ADMITTED

OwnerLineCoherence(WDF5)
= SURVIVES D

FoundationReopenCondition(WDF0) = NOT FIRED
FoundationReopenCondition(WDF1) = NOT FIRED
FoundationReopenCondition(WDF2) = NOT FIRED
ExactWDF3ClaimFalsified = NONE
FoundationReopenCondition(WDF4) = NOT FIRED

WholeWorldClosure
= NOT ESTABLISHED

Production
= UNCHANGED
```

---

# 51. Exact next action

Execute:

# **WDF5-E — Measurement vs Evaluation / Classification / Examination & Measurement-Admissible Value-Structure Boundary Reconstruction**

Do not assume quantity-only metrology wins.

Do not assume Stevens' nominal scale wins.

Do not assume broad property evaluation should all be called measurement.

The E round must decide whether a non-lexical, World-native measurement discriminator exists at all.

If none survives, WDF5 must accept that Measurement may be a subtype selected by domain/practice vocabulary over the more fundamental PEA-D1 architecture.

If one survives, reconstruct it minimally and attack it across physical, psychosocial, diagnostic, software, quantum, synthetic and Agent cases.

Do not admit WDF5-F or freeze Foundation v1 before E closes.
