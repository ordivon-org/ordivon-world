# WDF5-C — Measurement Attribution / Actuality Grounding / Bridge Minimal-Architecture Reconstruction

Date: 2026-08-18

Status: **WDF5-C COMPLETE / MTR-B1 COMPRESSED / TWO-AXIS MINIMAL ARCHITECTURE ESTABLISHED PROVISIONALLY / WDF5-D ADMITTED / NO FOUNDATION FREEZE**

Canonical upstream:

```text
WDF5 = ADMITTED
WDF5-A = COMPLETE
WDF5-B = COMPLETE
WDF5 Foundation v1 = DOES NOT EXIST
```

B-stage residual:

```text
MTR-B1

M1 Target Attribution
M2 Target-Relevant Empirical Grounding Chain
M3 Attribution / Interpretation Bridge
M4 Value / Comparison Semantics
M5 inherited WDF3 Criterion / CVE
```

C does not preserve these five labels by default.

Its mandate is deletion, absorption and missing-burden search.

---

# 1. C objective

The central question is:

> Can the B-stage residual be compressed into a smaller World-native architecture that distinguishes valid measurement attribution from prediction, proxying, estimation, scoring, classification, arbitrary computation and mere causal/informational dependence across physical, psychometric, software, institutional, synthetic and Agent regimes?

C uses:

```text
delete-one tests
absorption tests
2×2 independence tests
process/result/validity typing
cross-regime hard cases
truth-vs-evidence tests
actuality-vs-prediction tests
```

---

# 2. Terminology correction: Empirical Grounding is too physical/epistemic

B used:

```text
Target-Relevant Empirical Grounding Chain
```

C finds this label too narrow for the World project.

A valid measurement can be grounded in:

```text
physical sensor interaction
digital execution state
software logs
institutional records
virtual-world state
historical traces
sampled population records
upstream valid measurements
```

The common requirement is not specifically laboratory observation.

It is **contact with / dependence on the actuality of the target-relevant realized state, history, population, event or substrate**.

C therefore renames M2:

```text
Target-Relevant Actuality Grounding
```

or, where instance language is appropriate:

```text
Actuality / Instance Grounding
```

Canonical shorthand:

```text
AG = Actuality Grounding
```

This is intended to cover physical, digital, institutional and synthetic regimes without identifying actuality with physical causation.

---

# 3. C deletion test — delete M1 Target Attribution

Suppose M1 is removed while M2–M4 remain.

Counterexamples:

```text
sensor voltage with excellent grounding
arbitrary benchmark score with known scale semantics
well-calibrated indication with no declared measurand
system log counter with exact provenance
```

Without a target attribution, none says:

```text
V is a value/status of attribute A of target T.
```

Thus raw data/value production becomes measurement by default.

So the semantic content of M1 cannot disappear.

However, C asks a second question:

> Must Target Attribution survive as an independent burden?

Answer:

```text
NO.
```

Any genuine Attribution/Interpretation Bridge already needs a codomain/interpretation of the form:

```text
empirical/actual basis
-> value/status V as A(T)
```

A bridge with no target attribute is not a measurement attribution bridge at all.

Therefore:

```text
M1 semantic content = NECESSARY
M1 independent burden = ABSORBED INTO M3
```

---

# 4. C deletion test — delete M4 Value / Comparison Semantics

Suppose M4 is removed.

A bridge claims to map empirical basis E to result token r, but says nothing about:

```text
what r means
whether two results are equal/different
whether order is meaningful
whether ratio/difference is meaningful
what reference/version applies
whether the result is value, interval, rank or category
```

Then arbitrary encoding and measurement are not distinguishable.

So M4's semantic content cannot disappear.

But again C asks whether it is independent.

A legitimate Attribution Bridge must specify what it means for its output to count as **the attributed value/status of A(T)**.

That interpretation necessarily includes the result structure actually claimed.

Therefore:

```text
M4 semantic content = NECESSARY
M4 independent burden = ABSORBED INTO M3
```

The surviving bridge is richer than B's M3:

```text
Attribution Correspondence
```

which includes:

```text
target attribution
result/value interpretation
allowed comparison semantics
proxy-vs-target distinction
```

Canonical shorthand:

```text
AC = Attribution Correspondence
```

---

# 5. Important limitation of M4 absorption

Absorbing M4 into AC does **not** imply that:

```text
Reference
Scale
Unit
Comparability
```

are unimportant.

It means they are not an independent root condition for every valid measurement attribution.

Local result semantics can exist without global cross-system comparability.

Therefore:

```text
Local Result Interpretation
is part of AC.

Cross-system Reference/Comparability
remains a downstream architecture.
```

This distinction prevents WDF5 from making global metrological traceability constitutive of all measurement.

---

# 6. C absorption test — can AG be absorbed into AC?

Candidate compression:

```text
ValidMeasurementAttribution
= one sufficiently rich Attribution Correspondence
```

where the bridge is simply defined to include empirical grounding.

This is syntactically possible.

C therefore requires an independence test.

---

# 7. AG × AC independence matrix

Construct four quadrants.

## Q1 — AG = NO, AC = NO

Examples:

```text
random number
arbitrary ID
fictional score with no target mapping
```

Disposition:

```text
Neither measurement nor valid target attribution.
```

## Q2 — AG = YES, AC = NO

Examples:

```text
raw sensor signal affected by target but interpreted as wrong quantity
highly correlated proxy
click count used as engagement without adequate bridge
zip code used as individual income measurement
biomarker causally associated with disease but not valid as disease severity measure
```

The output is actuality-grounded and target-relevant in some sense, yet the claimed measurement attribution fails.

Disposition:

```text
Actuality-grounded observation/proxy/signal
!= ValidMeasurementAttribution
```

## Q3 — AG = NO, AC = YES or apparently YES

Examples:

```text
weather forecast for tomorrow
simulation output for a future target instance
model-predicted patient biomarker next week
counterfactual quantity under unperformed intervention
```

The model/interpretation from input state to target value may be scientifically warranted, but there is no actuality grounding in the target instance/conditions being claimed as measured.

Disposition:

```text
Prediction / simulation / counterfactual estimation
!= measurement of that unactualized target instance
```

## Q4 — AG = YES, AC = YES

Examples:

```text
calibrated physical measurement
valid psychometric attribution under adequate construct bridge
software latency result grounded in realized requests under correct metric semantics
institutional statistic grounded in actual records under declared rule definition
indirect derived quantity grounded through valid upstream measurements
```

Disposition:

```text
Candidate ValidMeasurementAttribution
```

### Independence result

```text
AG != AC
```

They can vary independently.

Absorbing AG into AC would conceal the prediction-vs-measurement distinction and the proxy-vs-measurement distinction inside one opaque predicate.

Therefore:

```text
M2/AG = RETAINED AS INDEPENDENT AXIS
M3 = RECONSTRUCTED AS AC
```

---

# 8. Prediction test — strongest AG falsifier

A prediction can be:

```text
precisely specified
well modeled
numerically calibrated
highly accurate historically
semantically clear
```

but still not measure the future target instance before that instance is realized/observed.

Thus:

```text
ValidInterpretationBridge
+ HistoricalEvidence
!= TargetInstanceMeasurement
```

The missing relation is:

```text
Actuality Grounding to the target-relevant realized state/history.
```

This is why AG remains independent.

---

# 9. Prediction edge case — measuring a current expectation

The same numerical output can change type when the declared target changes.

Example:

```text
"Tomorrow's actual temperature will be 30 °C"
```

is prediction.

But:

```text
"The current model-implied expected temperature for tomorrow is 30 °C"
```

can be an evaluation/estimate of a **current model property** if that is the declared target.

Therefore:

```text
Prediction vs Measurement
is target-criterion sensitive.
```

WDF3 Criterion/CVE remains essential.

---

# 10. Proxy test — strongest AC falsifier

A proxy may satisfy:

```text
actuality grounding
correlation
causal relation
predictive accuracy
stability
reliability
```

and still fail as measurement of the intended target.

Examples:

```text
clicks -> engagement
readmission -> healthcare quality
skin conductance -> fear
benchmark score -> general capability
zip code -> personal income
```

Therefore:

```text
AG alone != measurement
```

and:

```text
TargetRelevantInformation alone != AC
```

AC must establish why the empirical/result state is legitimately interpretable **as a value/status of the declared target attribute**, not only as information about it.

---

# 11. AC is not epistemic evidence by identity

C avoids defining AC as:

```text
we have good evidence that the bridge is valid
```

because evidence and truth can come apart.

Instead:

```text
AC = actual adequacy/correspondence of the attribution relation under scope.
```

Evidence, calibration, validation, robustness and replication are ways Agents test/justify AC.

Thus:

```text
AttributionCorrespondence
!= EvidenceForAttributionCorrespondence
```

This preserves WDF0/WDF3 firewalls.

---

# 12. Lucky-correctness test

Suppose a broken instrument outputs exactly the true target value by accident.

Then:

```text
ResultTruth = TRUE
```

but its target-relevant grounding/bridge is defective.

Therefore:

```text
CorrectValueByLuck
!= ValidMeasurementAttribution
```

This proves that measurement validity is not reducible to final proposition truth.

A valid measurement relation is provenance/structure sensitive.

---

# 13. Weak-evidence / true-measurement test

Suppose a new procedure objectively has adequate AG and AC, but the scientific community has little validation evidence yet.

Then it is possible that:

```text
ValidMeasurementAttribution = TRUE
EpistemicConfidence = LOW
```

Thus:

```text
MeasurementTruth != CurrentEvidenceStrength
```

WDF5 should separately model truth and epistemic validation.

---

# 14. Strong-evidence / invalid-attribution test

Conversely, a community may possess apparently strong but misleading evidence supporting a proxy relation that is actually invalid.

Then:

```text
EpistemicConfidence = HIGH
ValidMeasurementAttribution = FALSE
```

Therefore validation evidence is not the truthmaker.

---

# 15. Actuality Grounding is not direct physical causation

AG must support indirect measurements.

BIPM/JCGM measurement practice allows measured values to be calculated from input quantities in measurement models.

Cross-science measurement theory likewise distinguishes direct and indirect methods and emphasizes that indirect measurement is ultimately grounded in empirical/direct measurement components.

WDF5 therefore defines AG compositionally.

```text
AG may be direct:
  target instance/state -> acquisition record

AG may be indirect:
  target-relevant actual states/records
  -> upstream valid measurements
  -> admissible derivation chain
  -> result basis
```

No direct target-device edge is universally required.

---

# 16. AG composition rule — provisional

Let:

```text
Grounded(E, X | K)
```

mean that empirical/actual basis E is admissibly grounded in realized target-relevant X under criterion K.

For derived measurement:

```text
Grounded(E1, X1)
Grounded(E2, X2)
...
ValidBridge((X1,X2,...), A(T))
```

may support a derived attribution of A(T).

Examples:

```text
density from measured mass and volume
resistance from voltage and current
software availability from realized event logs
population statistic from sampled records
```

AG is therefore a provenance/actuality relation, not a single sensor edge.

---

# 17. Pure-computation test

Case A:

```text
f(3,7) = 21
```

with arbitrary constants.

This is computation, not measurement.

Case B:

```text
Y = f(X1,...,Xn)
```

where Xi are valid actual-world measurements and f is an adequate attribution bridge to target Y.

This can produce an indirect measurement result.

Therefore:

```text
Computation != Measurement
```

but:

```text
Computation + AG + AC
can participate in ValidMeasurementAttribution.
```

---

# 18. Synthetic / virtual reality test

A simulated or rule-created world provides an important stress against the word "empirical".

Suppose a game/simulation contains an actual realized object O with internal state variable x.

An authorized state read of x can be actuality-grounded relative to that virtual regime.

Therefore:

```text
ActualityGrounding
!= PhysicalMatterContact
```

and:

```text
Virtual/Simulated Actuality
can support measurement under its regime/CVE.
```

This is one reason C prefers AG over "Empirical Grounding" as the canonical World-level term.

---

# 19. Software metric test

Consider:

```text
P99 latency = 300 ms
```

AG requires actual realized request/event records relevant to the stated population/window/version.

AC requires correct interpretation of:

```text
request inclusion
clock semantics
retry/exclusion rules
aggregation
percentile definition
version/topology
```

A value computed exactly from logs can fail AC if the named target is "user-perceived latency" but the metric captures only internal server processing time.

Thus:

```text
ExactComputation + AG
!= ValidMeasurementAttribution
```

without AC.

---

# 20. Cross-version software metric test

Version v1:

```text
Availability = successful responses / all external requests
```

Version v2:

```text
Availability = successful terminal attempts / all terminal attempts
```

Each can support a valid local measurement attribution under its own criterion.

But:

```text
SameMetricName(v1,v2)
!= SameTargetDefinition
!= AutomaticComparability
```

This shows:

```text
local measurement validity
!= cross-version comparability.
```

Cross-version bridge semantics is downstream of the two-axis core.

---

# 21. Psychometric latent-construct test

Target:

```text
memory capacity of participant P under task family K
```

AG:

```text
actual responses/reaction times of P under the relevant task conditions
```

AC:

```text
adequate construct/model/calibration relation
showing why the observable pattern supports attribution of value V
as memory capacity rather than reading speed, motivation, motor speed, etc.
```

Reliability can strengthen quality/evidence but cannot replace AC.

Thus the two-axis architecture survives latent-target stress.

---

# 22. Institution-constituted target test

Target:

```text
unemployment rate for jurisdiction J in month t
```

WDF3 supplies the institution-relative target criterion:

```text
who counts as employed/unemployed
population scope
time window
classification rules
```

AG:

```text
actual survey/administrative records sampled from the relevant population
```

AC:

```text
sampling/classification/weighting bridge
from records to the attributed population statistic
```

The target is partly constituted by rules but measurement remains objectively assessable under the declared rule regime.

Thus:

```text
RuleConstitutedTarget
!= MeasurementProcedure
```

and the two-axis architecture survives.

---

# 23. Population/sample test

A potential attack on AG is that population quantities are often inferred from samples rather than all target instances.

C response:

AG need not mean exhaustive access.

It requires target-relevant actuality anchoring through an admissible sample/record chain.

AC then bears the sampling/inference bridge from observed sample to population attribution.

Thus:

```text
PartialActualityGrounding
can support population measurement
under adequate sampling bridge + CVE.
```

AG strength/coverage becomes a quality/validity issue, not an all-or-none physical contact condition.

---

# 24. Historical trace / retrodiction test

Past targets cannot be directly re-observed now.

But actual traces/records may remain.

Example:

```text
tree rings
archival instrument records
satellite images
ledger records
fossil/geochemical proxies
```

AG can be historical:

```text
present record R is itself an actual trace causally/structurally related to past state H.
```

AC determines whether R can legitimately be attributed as a value of H or only used as a predictor/proxy.

Thus retrodiction does not automatically collapse into measurement; the bridge decides the classification.

---

# 25. Agent-created target test

An Agent creates a new operational target:

```text
"interaction friction score v3"
```

WDF3 must determine target criterion/version semantics.

AG requires actual relevant interaction records.

AC requires a non-circular bridge showing how score components count as the target attribute under the declared definition.

Agent authorship is irrelevant to truth by identity.

```text
AgentCreated != Subjective
AgentCreated != Valid
```

---

# 26. Adaptive measurement test

An Agent changes its sensing policy after previous results.

Potential problem:

```text
measurement procedure depends on prior measurements
```

This does not invalidate the architecture.

Each attribution must expose:

```text
selection policy
actuality-grounded observations
bridge/version
CVE/time
```

Adaptive selection can introduce sampling bias or change the target population, but that is an AC/CVE validity issue rather than a new measurement primitive.

---

# 27. Coarse-grained measurement test

A coarse sensor reports macrostate M while hiding microstate variation.

If the declared target is the macrostate under coarse grain G:

```text
AG = valid at macro-relevant realized states
AC = adequate under G
```

Then:

```text
ValidMeasurementAttribution(M | G) = possible
```

Even though it is inadequate for a microstate query.

Thus:

```text
CoarseMeasurement != FalseMeasurement
```

and:

```text
Validity is CVE/query relative.
```

This strengthens WDF3 rather than reopening it.

---

# 28. Invalid-but-intended measurement procedure test

A laboratory procedure is sincerely designed and recognized as a measurement procedure, but its calibration model is wrong.

Then:

```text
MeasurementProcedure = YES
MeasurementExecution = YES
MeasurementResultAttribution = YES
ValidMeasurementAttribution = NO
```

This confirms B's typing and prevents `measurement process` from being equated with valid measurement truth.

---

# 29. Procedure intention is not thin-core truth

A historical photograph not originally taken for measurement can later be used to extract glacier extent.

At the time of later analysis, a valid attribution may be built from the actual image record plus an adequate bridge.

Therefore:

```text
OriginalDataCollectionIntentToMeasure
!= UniversalNecessityForValidMeasurementAttribution
```

Intent/design remains a property of measurement practice/procedure, not the core truth relation.

---

# 30. AC structure after absorption

C reconstructs M3 as:

```text
Attribution Correspondence AC(E, V:A(T) | K,CVE)
```

where AC asserts that under criterion K and validity envelope CVE:

```text
1. E is interpreted with an admissible bridge B;
2. B maps/relates E to V as a value/status of A(T);
3. V's local identity/order/difference/reference semantics needed by the claim are defined;
4. the relation is target-attributive, not merely predictive/correlative/proxy;
5. relevant transformations/corrections/inference are semantically valid for this attribution.
```

AC may be:

```text
identity-like/direct
comparison-based
calibration-based
model-based
statistical
rule-defined
multi-stage
```

No one realization is universal.

---

# 31. AG structure after reconstruction

```text
Actuality Grounding AG(E, T | K,CVE)
```

asserts that E depends through an admissible provenance/acquisition chain on realized target-relevant state/history/population/records sufficient for the measurement claim.

AG may be:

```text
direct physical interaction
actual digital-state read
observed behavioral response
sampled record
historical trace
upstream valid measurement chain
```

AG is not:

```text
generic past evidence
model training data
mere theoretical plausibility
counterfactual simulation
unrealized future-state prediction
```

unless the declared target is itself a current model/statistical property.

---

# 32. Two-axis minimal architecture — MAR-C1

C therefore compresses MTR-B1 into:

# **MAR-C1 — Measurement Attribution Relation**

```text
ValidMeasurementAttribution(R, V:A(T) | K,CVE)
requires jointly:

G — Actuality Grounding
    Target-relevant realized-state/history/record grounding
    for the target claim.

A — Attribution Correspondence
    An adequate bridge interpreting the grounded basis as
    the declared value/status V of attribute A(T), including
    the local result semantics required by the claim.

with:

K / CVE
= inherited WDF3 Criterion / Validity Envelope discipline.
```

Canonical compression:

```text
M1 -> absorbed into A
M2 -> reconstructed as G
M3 -> reconstructed as A
M4 -> absorbed into A
M5 -> inherited WDF3
```

So the WDF5-specific thin core now has **two independent axes**, not four/five independent primitives.

---

# 33. Why G and A are not primitives of Reality by default

C does not claim:

```text
ActualityGrounding
AttributionCorrespondence
```

are new fundamental ontic relations.

They are Foundation-level semantic burdens for identifying valid measurement attribution across regimes.

They may themselves reduce differently in:

```text
physics
psychology
software
institutions
synthetic worlds
```

The Foundation claim is structural:

```text
a measurement attribution fails if either actuality grounding
or target-value attribution correspondence fails.
```

---

# 34. Measurement vs Quantification after C

C sharpens the relationship.

```text
Quantification
= construction/use of structured values/orders/scales/indices.

MeasurementAttribution
= actuality-grounded attribution of an admissible value/status
  to a target attribute through adequate correspondence.
```

Thus:

```text
Quantification can supply the result-space side of A.
```

But:

```text
Quantification alone lacks G and may lack target attribution.
```

Therefore owner-line coherence continues to survive.

---

# 35. Measurement vs classification after C

A potential collapse remains:

```text
if A can output any status/category,
why isn't every valid classification a measurement?
```

C does not fully close this question.

It establishes only:

```text
nominal/classification result semantics
are not automatically measurement-value semantics.
```

The exact boundary depends on the admissible structure of `V` and the claim made about property/quantity/construct.

This becomes a downstream residual for Quantification / Value Semantics.

Therefore:

```text
Measurement != Classification
```

remains preserved, but its deepest formal boundary is **not yet frozen**.

---

# 36. Measurement vs estimation after C

An estimate may or may not be a measurement attribution.

```text
Estimate of future state
-> no target actuality grounding -> prediction

Estimate of current population parameter from actual sample
-> may have G + A -> measurement-compatible

Estimate of latent construct from actual responses
-> may have G + A -> measurement-compatible
```

Therefore:

```text
Estimation is an inferential method class,
not a measurement truth type.
```

---

# 37. Measurement vs observation after C

Observation can satisfy G without A.

Example:

```text
"the pointer moved"
```

is actuality-grounded observation.

Without interpreting the pointer position as a value of a target attribute, it is not yet a measurement attribution.

Thus:

```text
Observation ~= possible G-provider
Observation != ValidMeasurementAttribution
```

---

# 38. Measurement vs sensing after C

Sensing can satisfy direct G.

But sensor outputs can be:

```text
uncalibrated
cross-sensitive
wrongly mapped
wrong-target
```

so A may fail.

Therefore:

```text
Sensing = realization mechanism for G
not measurement validity by identity.
```

---

# 39. Measurement vs evidence after C

A valid measurement attribution may become evidence for another claim.

But:

```text
measurement truth = G + A under K/CVE
```

whereas:

```text
evidential support
```

is a downstream relation between information and propositions/hypotheses.

Thus WDF0 separation survives exactly.

---

# 40. Measurement vs causal validation after C

G may be realized by causal interaction, but does not reduce to causation.

A may use causal theory, but a causal relation can be proxy-like or irrelevant to the target value attribution.

Therefore:

```text
Cause != ActualityGrounding by identity
Cause != AttributionCorrespondence by identity
```

No WDF4 reopen condition fires.

---

# 41. Quality architecture remains outside MAR-C1

C preserves:

```text
accuracy
trueness
precision
uncertainty
reliability
robustness
resolution
selectivity
traceability
fitness for purpose
```

as dimensions describing:

```text
strength
error profile
uncertainty
transportability
reproducibility
fitness
```

of G/A/procedure/result under scope.

They are not added to MAR-C1 as mandatory root slots.

---

# 42. Validity typing after C

C recommends:

```text
ProcedureValidity
= procedure is fit to generate candidate measurement attributions under conditions

AttributionValidity
= G + A hold for the specific result claim under K/CVE

QualityAdequacy
= uncertainty/accuracy/reliability/etc. are sufficient for intended use

EvidenceAdequacy
= available evidence justifies confidence in those validity/quality claims
```

These are distinct.

A result can be:

```text
valid but too uncertain for use
valid with weak current evidence
invalid despite strong misleading evidence
correct by luck but invalid as measurement
```

---

# 43. Reference/comparability typing after C

C distinguishes:

```text
LocalResultSemantics
= inside A
```

from:

```text
CrossResultComparability
CrossProcedureComparability
CrossVersionComparability
TraceabilityNetwork
```

which are transport/composition relations among measurement systems/results.

Thus WDF5's Reference/Comparability route remains real but is no longer confused with the minimal local validity relation.

---

# 44. Cross-regime comparison matrix

```text
Regime         G realization                    A realization

Physical       instrument/actual interaction    calibration/model/comparison
Chemical       sample/assay records              method/model/reference relation
Biological     biomarker/behavioral data         biological/construct bridge
Psychometric   actual task responses             latent-construct model/validation bridge
Software       logs/traces/state reads            metric semantics/aggregation bridge
Institutional  survey/admin records              rule/sampling/classification bridge
Synthetic      realized virtual state             rule-world value interpretation
Agent          observations/adaptive records      target/model/version bridge
```

No regime requires a new third root axis so far.

---

# 45. Missing-burden search

C actively searches for a case satisfying G + A but still clearly not measurement because of a missing independent burden.

Candidates tested:

```text
intention
instrument
standard
uncertainty
reliability
public reproducibility
community recognition
theory consensus
numeric representation
physical causation
explicit model
```

Each can be removed in at least some plausible valid measurement cases.

No third universal root burden is currently earned.

Therefore:

```text
ThirdRootBurden = NOT FOUND IN C
```

---

# 46. Potential challenge — is G + A sufficient?

C is not yet willing to freeze:

```text
G + A = sufficient universal definition of ValidMeasurementAttribution
```

because several difficult classes remain:

```text
nominal/classification boundary
historical proxy reconstruction
highly theory-mediated latent variables
self-referential/adaptive Agent metrics
changing target definitions
quantum/contextual measurement terminology
cross-level emergent quantities
```

Thus MAR-C1 is a strong minimal architecture candidate, not Foundation v1.

---

# 47. External pressure alignment

C's two-axis result is independently compatible with multiple external traditions without copying any one.

BIPM/JCGM:

```text
measurement = experimentally obtaining values reasonably attributable to a quantity
```

with broad allowance for models/calculations and distinct measurand/result/model semantics.

This independently pressures both:

```text
actual-world acquisition
+ attribution to a target quantity.
```

Mari/Wilson/Maul's cross-science framework explicitly characterizes measurement as an empirical and informational process and argues that indirect measurement retains empirical grounding through direct measurement components.

This independently supports G/A separation.

Van Fraassen emphasizes theory-dependent empirical grounding criteria connecting quantities and measurement procedures.

Bach's psychometric analysis independently pressures A: observable variables need a valid bridge to latent constructs.

Ohnesorge's historical work prevents A from requiring a universally shared mature theory before measurement practice can exist.

No source is treated as canonical ontology.

---

# 48. WDF3 stress audit

C relies heavily on:

```text
Criterion
CVE
identity/category
scoped objectivity
constitution vs attribution
representation vs Reality
```

No exact WDF3 claim is falsified.

Instead, C achieves a substantial compression precisely by **reusing** WDF3 rather than duplicating it.

For example:

```text
TargetCriterion
TargetVersion
Regime-relative objectivity
```

remain WDF3 responsibilities.

WDF5 contributes:

```text
G + A measurement-attribution relation
```

This is positive independent support for the WDF3/WDF5 ownership boundary.

```text
ExactWDF3ClaimFalsified = NONE
WDF3 Foundation v1 = NOT FROZEN
```

---

# 49. Foundation reopen audit

## WDF0

C strengthens:

```text
Reality != Representation != Evidence != Model
```

because G/A truth is separated from epistemic evidence.

```text
FoundationReopenCondition(WDF0) = NOT FIRED
```

## WDF1

No modal/chance claim fails.

```text
FoundationReopenCondition(WDF1) = NOT FIRED
```

## WDF2

Prediction/counterfactual cases remain separable from measurement actuality grounding.

No counterfactual architecture claim fails.

```text
FoundationReopenCondition(WDF2) = NOT FIRED
```

## WDF3

No exact claim fails.

```text
ExactWDF3ClaimFalsified = NONE
```

## WDF4

Causal relations are neither sufficient nor universally necessary for G/A identity.

```text
FoundationReopenCondition(WDF4) = NOT FIRED
```

---

# 50. C-stage architecture summary

B began with:

```text
M1 Target Attribution
M2 Empirical Grounding
M3 Attribution Bridge
M4 Value Semantics
M5 WDF3 Criterion/CVE
```

C ends with:

```text
MAR-C1

G = Target-Relevant Actuality Grounding
A = Attribution Correspondence
K/CVE = inherited WDF3
```

Compression:

```text
M1 -> A
M2 -> G
M3 -> A
M4 -> A
M5 -> WDF3 inherited
```

So:

```text
Independent WDF5 root-burden count
provisionally drops from 4 to 2.
```

---

# 51. C residual universe — freshly derived

C does not inherit B's route ordering.

New residual families:

```text
D-R1 MAR-C1 cross-regime destructive falsification
     and sufficiency attack

D-R2 Measurement Value / Quantification /
     Classification boundary architecture

D-R3 Reference / Comparability / Transport architecture

D-R4 Measurement validity / failure / quality architecture

D-R5 Actuality-grounding composition / provenance architecture

D-R6 Target constitution / version-change interface

D-R7 No-further-foundation control:
     MAR-C1 + domain-local quality/reference theory is enough
```

---

# 52. D-R2 assessment — Value / Quantification / Classification

This residual is materially stronger after C because M4 was absorbed rather than independently frozen.

Open questions:

```text
what result structures qualify as measurement values?
when is ordinal evaluation measurement?
when is binary status detection/classification rather than measurement?
how do score/index/metric scales become measurement-capable?
```

High information, but MAR-C1 itself has not yet faced independent cross-regime sufficiency falsification.

Disposition:

```text
VERY STRONG DOWNSTREAM
```

---

# 53. D-R3 assessment — Reference / Comparability / Transport

Open questions:

```text
same target across instruments
same metric across versions
cross-lab comparison
population norm transport
institutional definition changes
traceability vs local comparability
```

This is important but clearly downstream of local valid attribution.

Disposition:

```text
STRONG DOWNSTREAM
```

---

# 54. D-R4 assessment — Validity / Failure / Quality

C's typing now makes this much cleaner:

```text
ProcedureValidity
AttributionValidity
QualityAdequacy
EvidenceAdequacy
```

This is high-value, but it should consume a stable attribution architecture rather than substitute for testing MAR-C1.

Disposition:

```text
VERY STRONG DOWNSTREAM
```

---

# 55. D-R5 assessment — Actuality-grounding composition

Indirect measurement, sampling, historical traces and synthetic regimes make AG composition nontrivial.

However C already has a provisional compositional rule sufficient for further stress.

Disposition:

```text
STRONG SUB-ARCHITECTURE
```

---

# 56. D-R6 assessment — Target constitution / version change

Deep but still strongly shared with WDF3.

It is best used as an external stress family unless MAR-C1 fails there.

Disposition:

```text
HIGH INFORMATION / OWNERSHIP-SENSITIVE
```

---

# 57. D-R7 control assessment

Could WDF5 stop at MAR-C1 and delegate all other details to local sciences/domains?

Not yet justified.

MAR-C1 has not faced a sufficiently independent destructive attack designed specifically to find:

```text
G + A cases that are not measurement
valid measurement cases lacking G
valid measurement cases lacking A
regime-specific hidden third burdens
```

Thus no-further-research control is premature.

---

# 58. D-R1 wins

The highest information-gain move after positive compression is not immediately adding downstream architecture.

It is trying to destroy MAR-C1 itself.

Therefore:

```text
D-R1 = WINNER
```

---

# 59. WDF5-D admission

C therefore admits:

# **WDF5-D — MAR-C1 Cross-Regime Destructive Falsification / Sufficiency & Missing-Burden Search**

Working question:

> Does the two-axis MAR-C1 architecture — Target-Relevant Actuality Grounding + Attribution Correspondence under inherited WDF3 Criterion/CVE — actually survive adversarial cases across physical, psychometric, biological, software, institutional, synthetic and Agent regimes; can valid measurement exist without either axis; can non-measurement satisfy both; is a third independent burden required; and does the architecture preserve prediction/proxy/classification/estimation boundaries without overfitting familiar scientific measurement practices?

WDF5-D is admitted for destructive research only.

No Foundation freeze occurs in C.

---

# 60. Mandatory WDF5-D falsifiers

At minimum:

```text
DF1 G absent / apparent valid measurement
DF2 A absent / apparent valid measurement
DF3 G + A present / obvious non-measurement
DF4 lucky correct result
DF5 black-box learned sensor with unknown bridge
DF6 self-calibrating adaptive Agent metric
DF7 synthetic-world direct state introspection
DF8 historical proxy reconstruction
DF9 population parameter from nonprobability sample
DF10 latent construct with competing models
DF11 quantum/contextual measurement terminology
DF12 purely qualitative/ordinal borderline case
DF13 nominal classification / diagnostic test
DF14 institution-rule change across time
DF15 same numeric result / changed target criterion
DF16 direct physical comparison without explicit model
DF17 derived quantity with long upstream measurement chain
DF18 coarse-grained macro quantity hiding fine dynamics
DF19 adversarial Goodharted metric
DF20 measurement that changes/constitutes target state
```

D must search for a **specific falsifier** of G, A, their independence or their joint adequacy.

---

# 61. WDF5-C canonical results

```text
C1 "Empirical Grounding" is renamed/reconstructed as
   Target-Relevant Actuality Grounding (G).

C2 M1 Target Attribution is not independently retained;
   its semantic content is absorbed into Attribution Correspondence.

C3 M4 Value/Comparison Semantics is not independently retained;
   local result semantics are absorbed into Attribution Correspondence.

C4 M2/G cannot be absorbed into Attribution Correspondence without
   collapsing prediction into measurement.

C5 Proxy cases prove G without A is possible.

C6 Prediction cases prove A-like interpretation without G is possible.

C7 Therefore G != A and both are independent axes.

C8 CorrectValueByLuck != ValidMeasurementAttribution.

C9 MeasurementTruth != CurrentEvidenceStrength.

C10 AG is not direct physical causation and may compose through
    upstream valid measurements/actual records.

C11 Virtual/digital/institutional realized states can supply AG;
    actuality is regime-relative, not physical-only.

C12 MAR-C1 is established provisionally:

    ValidMeasurementAttribution
    = G + A under inherited WDF3 Criterion/CVE.

C13 No third universal root burden is found in C.

C14 Quality/reference/comparability remain important downstream layers,
    not independent MAR-C1 root conditions.

C15 Measurement/Quantification owner-line coherence survives C.

C16 MAR-C1 is NOT frozen as Foundation v1.

C17 WDF5-D is admitted as independent destructive falsification of MAR-C1.
```

---

# 62. Canonical frontier after WDF5-C

```text
WDF5 = ADMITTED
WDF5-A = COMPLETE
WDF5-B = COMPLETE
WDF5-C = COMPLETE

MAR-C1
= PROVISIONAL TWO-AXIS MINIMAL ARCHITECTURE
= Actuality Grounding + Attribution Correspondence
  under inherited WDF3 Criterion/CVE

WDF5-D
= ADMITTED
= MAR-C1 Cross-Regime Destructive Falsification /
  Sufficiency & Missing-Burden Search

WDF5-D execution
= NOT STARTED

WDF5 Foundation v1
= DOES NOT EXIST

WDF5-E+
= UNKNOWN / NOT ADMITTED

OwnerLineCoherence(WDF5)
= SURVIVES C

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

# 63. Exact next action

Execute:

# **WDF5-D — MAR-C1 Cross-Regime Destructive Falsification / Sufficiency & Missing-Burden Search**

Do not improve MAR-C1 unless a falsifier requires it.

First attempt to destroy:

```text
G necessity
A necessity
G/A independence
G+A joint adequacy
```

Search especially for:

```text
valid measurement without target actuality grounding
valid measurement without attribution correspondence
obvious non-measurement satisfying both
third-burden cases
```

Do not admit WDF5-E or freeze WDF5 Foundation v1 before D closes.
