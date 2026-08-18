# WDF5-G — Reference / Comparability / Cross-Scale Transport / Traceability Architecture

Date: 2026-08-18

Status: **WDF5-G COMPLETE / CROSS-EVALUATION TRANSPORT ARCHITECTURE RECONSTRUCTED / COMPARABILITY-COMPATIBILITY-EQUALITY SEPARATED / REFERENCE ROLES TYPED / TRACEABILITY DEMOTED FROM CORRECTNESS TO SPECIAL TRANSPORT-PROVENANCE MECHANISM / BRIDGE TRANSITIVITY REJECTED BY DEFAULT / WDF5-H ADMITTED / NO FOUNDATION FREEZE**

Canonical upstream:

```text
PEA-E1
= ValidPropertyEvaluationAttribution
= G + A under WDF3 Criterion / CVE

QES-F1
= PS / VS / RE / A_structure / Gamma / Meaningfulness
```

F established:

```text
RepresentationTransform != EvaluationStructureRevision
InvertibleMap != SemanticEquivalence
Convertibility != Comparability
```

G asks what additional architecture is required before two locally valid evaluations/results may support a cross-evaluation claim.

---

# 1. G headline result

Local validity does not imply cross-result comparability.

Two evaluations can each be valid under their own target criterion, value structure, representation and CVE while lacking any justified relation that licenses a comparison between them.

Canonical:

```text
LocalValidity(E1)
+ LocalValidity(E2)
!= CrossEvaluationComparability(E1,E2)
```

The missing burden is **semantic transport**.

G reconstructs comparability around a claim-relative common comparison frame and valid semantic transports into that frame.

---

# 2. Shortcut falsification summary

All of the following fail as universal sufficient conditions:

```text
SameNumber
SameUnit
SameName
SameScaleRange
SameDisplayFormat
InvertibleMap
CommonReference
Traceability
SameTargetName
SameBenchmarkName
```

Each can coexist with incompatible target criteria or evaluation semantics.

Therefore:

```text
Comparability
= additional relational achievement
not local-result metadata identity.
```

---

# 3. Same unit falsifier

VIM provides a direct hard case.

The same unit name/symbol may be used for quantities that are not of the same kind.

For example:

```text
J/K
```

can denote both heat capacity and entropy.

Thus:

```text
SameUnit
!= SameQuantityKind
!= AutomaticComparability
```

A shared unit is only semantically useful after the target property kind and relevant structure are aligned.

---

# 4. Same kind need not mean same target instance

VIM metrological comparability explicitly allows results for different measurands to be comparable when the quantities are of the same kind and traceable to the same reference.

Example:

```text
Earth–Moon distance
Paris–London distance
```

can be comparable as lengths.

Therefore:

```text
Comparability
!= SameTargetInstance
```

This is important for World architecture.

Comparability is often about placing different target instances in a shared value/comparison structure.

---

# 5. Compatibility is much stronger than comparability

VIM separately defines metrological compatibility for results concerning a specified measurand, with agreement judged relative to the uncertainty of their difference.

Thus:

```text
Comparability
!= Compatibility
```

and:

```text
Compatibility
requires a stronger target/sameness hypothesis
plus an agreement criterion.
```

A set of comparable results can be mutually incompatible.

Example:

```text
same measurand
same reference system
results differ far beyond declared uncertainties
```

The results are still comparable, but they disagree.

---

# 6. Compatibility is not equality

Two results can be compatible without being numerically or semantically identical.

Compatibility expresses:

```text
sufficient agreement under a declared tolerance/uncertainty criterion
```

not:

```text
literal identity of value.
```

Therefore:

```text
Compatibility != Equality
```

and:

```text
Equality != Interchangeability
```

because two numerically equal values can arise under different targets or evaluation definitions.

---

# 7. G cross-evaluation relation taxonomy

G reconstructs a typed hierarchy.

## R1 Encoding Convertibility

A map exists between RE encodings.

```text
RE1 -> RE2
```

This is syntactic/representational.

## R2 Value Transformability

A map exists between VS representations/value spaces with declared structural meaning.

```text
VS1 -> VS2
```

This can still fail target semantics.

## R3 Semantic Transportability

A bridge preserves the claim-relevant target/evaluation meaning under K/CVE.

## R4 Comparability

A declared cross-result relation can be meaningfully evaluated after semantic transport into a common comparison frame.

## R5 Compatibility

Comparable results concerning a sufficiently aligned target hypothesis satisfy a declared agreement criterion, often uncertainty-aware.

## R6 Equivalence / Interchangeability

Substituting one result/system for another preserves the declared downstream claims/decisions under a specified CVE.

## R7 Equality

The transported semantic values are equal in the relevant comparison frame.

Canonical:

```text
Convertibility
< SemanticTransportability
< Comparability
```

but compatibility/equivalence/equality are different stronger/specialized relations rather than one simple linear ladder.

---

# 8. Comparison is relation-specific

There is no single undifferentiated `comparable` predicate.

Two evaluations can be comparable for:

```text
order
sign
rank
difference
ratio
distance
membership
trend
equivalence
decision substitution
```

while not comparable for other relations.

Example:

Two ordinal scales connected by a monotone transform may support:

```text
order comparison
```

but not:

```text
difference comparison
ratio comparison
```

Canonical:

```text
Comparability_R
```

where R is the relation/claim being transported.

---

# 9. Common Comparison Frame

G introduces:

# **CF — Common Comparison Frame**

A CF is a value/semantic frame in which the declared cross-evaluation relation is well-defined.

It may be:

```text
one party's VS
an external reference scale
a shared latent scale
a unit/reference system
a common coordinate-free structure
a common population/reference distribution
a temporary bridge frame constructed for the comparison
```

A universal global frame is not required.

---

# 10. Semantic Transport Bridges

For local evaluations:

```text
E1 with VS1
E2 with VS2
```

comparability requires, provisionally:

```text
T1 : VS1 -> CF
T2 : VS2 -> CF
```

where each `Ti` is a **semantic transport bridge**, not merely a mathematical map.

A valid transport must preserve the target/evaluation structure needed by the comparison claim.

Thus:

```text
MathematicalMap
!= SemanticTransportBridge
```

---

# 11. CRT-G1 — Cross-Evaluation Reference & Transport Architecture

G proposes:

# **CRT-G1**

A cross-evaluation claim `C_R(E1,E2)` is candidate-valid only if:

```text
C1 Relation Declaration
   The exact cross-evaluation relation R is declared.

C2 Target / Kind / Criterion Alignment
   The targets/properties are sufficiently aligned for R,
   or an explicit target-semantic bridge is supplied.

C3 Common Comparison Frame
   A frame CF exists in which R is semantically defined.

C4 Valid Semantic Transport
   Each local VS is transported into CF by bridges preserving
   the claim-relevant evaluation structure.

C5 Reference Context
   Any reference that constitutes, anchors, validates or transfers
   the semantics is identified with version/time/population scope.

C6 Transport CVE
   The bridge is valid for the relevant regime, population,
   procedure, version, conditions and time.
```

Uncertainty/quality enters when R itself requires agreement, confidence or fitness claims.

CRT-G1 is provisional research architecture, not frozen Foundation.

---

# 12. Target alignment is relation-dependent

The required alignment differs by claim.

For comparing lengths of different objects:

```text
same quantity kind / compatible value structure
```

may suffice.

For checking repeat measurement agreement:

```text
same measurand / stable target hypothesis
```

is required.

For comparing two institutional indices:

```text
same name
```

is not enough; target constitution and aggregation rules may differ.

Therefore:

```text
TargetAlignment_R
```

is claim-relative.

---

# 13. Same target, different units

Different units do not prevent comparability.

If the target/evaluation structure is shared and a valid unit conversion preserves the relevant semantics:

```text
metres <-> feet
Celsius-like representation <-> Fahrenheit-like representation
```

may support transport.

Therefore:

```text
SameUnit != NecessaryForComparability
```

The important condition is semantic transportability, not label identity.

---

# 14. Nonlinear admissible transformations

Suppose two ordinal representations are linked by a strictly monotone nonlinear map.

Then:

```text
order claims
```

can remain comparable.

But differences/ratios may not.

Thus:

```text
NonlinearTransform
```

is neither automatically valid nor invalid.

Validity is relation-specific:

```text
TransformValidFor_R
```

and depends on QES-F1 Gamma/Meaningfulness.

---

# 15. Same number, different target

```text
3 °C
rank 3
risk tier 3
3 radians
ID 3
```

share a representation token but not a comparison frame.

Therefore:

```text
SameNumber
!= Comparability
```

unless explicit target/value semantics establish a valid relation.

---

# 16. Same metric name, changed definition

Software/Agent metrics provide a canonical version-drift case.

Example:

```text
Availability v1
= successful external requests / all external requests

Availability v2
= successful terminal attempts / all terminal attempts
```

Both may be locally valid.

But:

```text
SameName
!= SameEvaluationStructure
```

and a cross-version time series requires an explicit bridge or should preserve a discontinuity.

Canonical:

```text
MetricVersionChange
may break comparability without breaking local validity.
```

---

# 17. Same 0–100 range, changed weights

Composite indices provide another canonical falsifier.

If:

```text
Index_v1 = 0.5 A + 0.5 B
Index_v2 = 0.2 A + 0.8 B
```

both normalized to 0–100,

then:

```text
SameRange
SameName
SameNumericType
```

still do not establish semantic equivalence.

Weight changes are EvaluationStructureRevision, not representation conversion.

---

# 18. Reference roles are typed

G finds that `Reference` is overloaded.

Canonical research typing:

## Ref-C — Constitutive Reference

The reference participates in defining the value semantics.

Examples:

```text
percentile reference population
benchmark version
institutional baseline
index base period
```

## Ref-A — Anchoring Reference

Places local values into a common frame.

Examples:

```text
measurement unit realization
calibration standard
anchor test
common scale
```

## Ref-V — Validation Reference

Used to assess trueness, criterion validity or quality.

It need not define the scale.

## Ref-T — Transfer Reference

An object/material/procedure used to transport a relation between procedures/systems.

Its transfer behavior may itself require validation.

Canonical:

```text
ConstitutiveReference
!= AnchoringReference
!= ValidationReference
!= TransferReference
```

One artifact can play more than one role, but the roles are not identical.

---

# 19. Percentile reference-population case

A percentile is not semantically complete without its reference population/distribution.

```text
90th percentile in population P1
90th percentile in population P2
```

need not represent the same raw magnitude or same latent position under a shared target model.

Thus:

```text
ReferencePopulation
= ConstitutiveReference for percentile semantics
```

and:

```text
SamePercentileNumber
!= CrossPopulationComparability
```

A bridge requires population/construct assumptions or a common latent/raw frame.

---

# 20. Psychometric linking vs equating

Psychometric practice supplies a strong cross-domain analogue.

A link between score scales can exist without warranting score interchangeability.

ETS equating literature treats equating as the stronger operation intended to make scores from different forms have the same meaning over time and to support interchangeability.

Population invariance is a fundamental requirement for equating/linking claims of this strength.

Therefore:

```text
ScoreLinkExists
!= ScoresInterchangeable
```

and:

```text
CommonScale
!= Equivalence
```

This independently confirms CRT-G1's distinction between mathematical/estimated linking and semantic transport validity.

---

# 21. Population invariance stress

Suppose linking function:

```text
L_AB
```

works for population P1 but differs materially for P2.

Then:

```text
BridgeValidityCVE = P1
```

not universal.

Thus:

```text
TransportBridgeValidity
is population/CVE-relative.
```

A single global conversion table can hide local non-invariance.

---

# 22. Cross-lab physical calibration

Physical metrology supplies a mature special case.

Locally valid results from labs L1 and L2 can be placed in a common metrological frame through calibration chains to a common reference for quantities of the same kind.

This can establish metrological comparability.

But it does not establish:

```text
same measurand
agreement
absence of mistake
fitness of uncertainty for purpose
```

Therefore:

```text
TraceabilityToSameReference
can support comparability
without guaranteeing compatibility/correctness.
```

---

# 23. Traceability reconstructed

VIM metrological traceability is a property of a result whereby it can be related to a reference through a documented unbroken chain of calibrations, with each link contributing to uncertainty.

G generalizes the structural lesson without universalizing laboratory metrology.

Canonical:

```text
Traceability
= special transport-provenance relation
```

It records how a local result/frame is related through a chain to a reference.

It is **not**:

```text
Correctness
Validity
FitnessForPurpose
TargetIdentity
Compatibility
```

by itself.

---

# 24. Traceable wrong-target result

Suppose an instrument is perfectly calibrated and traceable to a reference but is used to infer the wrong target property.

Then:

```text
Traceability = YES
A = NO
```

for the intended target attribution.

Thus:

```text
Traceability
cannot repair a broken Attribution Correspondence.
```

PEA-E1 survives.

---

# 25. Local comparability without global traceability

A global public reference is not universally required.

Two local systems can be compared through a direct validated bridge:

```text
VS1 <-> VS2
```

within a narrow CVE.

Examples:

```text
pairwise instrument comparison
local experimental scale linking
direct coordinate transformation
within-study psychometric linking
```

Thus:

```text
GlobalReference
!= UniversalNecessaryConditionForComparability
```

A global reference improves transport network reach and reproducibility, but is not ontologically mandatory for every comparison.

---

# 26. Reference material commutability falsifier

A common transfer material/reference can fail as a transport device if its behavior across two procedures differs from its behavior for routine samples.

Metrology formalizes this as **commutability** of a reference material.

Therefore:

```text
CommonReferenceMaterial
!= ValidCrossProcedureTransport
```

The transfer role itself needs validation.

This is one of G's strongest falsifiers of `common reference => comparable`.

---

# 27. Method-defined / constituted references

Some value systems depend on procedures or definitions that partly constitute the target/evaluation semantics.

Examples:

```text
operational chemical quantity defined by a reference procedure
benchmark score defined by benchmark version/protocol
institutional index defined by rules
percentile defined by reference population
```

Here:

```text
Reference
```

is not merely an external calibration anchor.

It can be part of the target/evaluation definition.

Thus:

```text
ReferenceRole must be typed before transport claims are evaluated.
```

---

# 28. Vector coordinate transport

Two vector evaluations can use different coordinate bases.

A valid basis transformation may alter every displayed component while preserving the underlying vector relation.

Thus:

```text
ComponentwiseNumericEquality
!= VectorEquivalence
```

and:

```text
CoordinateTransform
can support semantic transport
when the underlying vector structure is shared.
```

Comparability claims should be expressed in coordinate-invariant or correctly transported terms.

---

# 29. Cyclic reference-origin transport

Angles/phases can use different zero origins.

A constant phase shift may be a representation/reference transformation.

Absolute displayed angles differ, while:

```text
relative phase
cyclic neighborhood
angular difference modulo cycle
```

can remain invariant.

Thus:

```text
ReferenceOriginChange
!= EvaluationRevision by default
```

but only if cyclic structure and orientation conventions are aligned.

---

# 30. Distribution-valued comparison

Comparing distributions requires declaration of the relation:

```text
same mean?
stochastic dominance?
distance/divergence?
quantile relation?
support overlap?
full distribution equality?
```

Therefore:

```text
DistributionComparable
```

is meaningless without `R`.

This reinforces:

```text
Comparability_R
```

rather than a generic yes/no flag.

---

# 31. Institutional cross-jurisdiction index

Suppose two jurisdictions publish an index from 0–100 with the same public label.

Their definitions may differ in:

```text
population
components
weights
thresholds
missing-data policy
time window
legal categories
```

Thus:

```text
SameName + SameRange
!= CrossJurisdictionComparability
```

A valid bridge may be impossible without reconstructing both constituted targets.

In some cases the correct result is:

```text
PARTIALLY COMPARABLE
```

for selected subcomponents only.

---

# 32. Agent-created metrics across Agents

Two Agents can independently create metrics called `confidence`, `risk` or `priority`.

Even if both output 0–1:

```text
same range
same name
same numeric type
```

provides almost no semantic alignment.

Cross-Agent comparison requires:

```text
target criterion alignment
value-structure alignment
bridge/version semantics
CVE compatibility
```

Therefore:

```text
AgentMetricNameEquality
!= MetricComparability
```

---

# 33. Adaptive metric drift

An Agent may change the metric definition over time.

If the change is semantic:

```text
M_v1 -> M_v2
```

then a time series across the boundary is not automatically continuous.

Canonical:

```text
MetricContinuityClaim
requires VersionBridge
```

or the discontinuity must be preserved explicitly.

---

# 34. Bridge composition is not automatically transitive

Suppose:

```text
T_AB : A -> B
T_BC : B -> C
```

are each locally valid.

It does not follow automatically that:

```text
T_AC = T_BC ∘ T_AB
```

is globally valid.

Failure modes include:

```text
non-overlapping CVEs
different reference populations
intermediate scale drift
lossy coarsening
procedure-specific bias
uncertainty accumulation
version mismatch
non-commutable transfer references
```

Thus:

```text
PairwiseTransportValidity
!= GlobalTransitiveComparability
```

This is independently mirrored by psychometric scale-linking drift and population-invariance concerns.

---

# 35. Transport path dependence

If two independent bridge paths from A to C yield materially different transported semantics:

```text
A -> B -> C
A -> D -> C
```

then the transport network exhibits path inconsistency.

Canonical:

```text
PathIndependence
= validation property
not automatic law.
```

A mature reference/transport network should test loop closure where relevant.

---

# 36. Global reference as network convenience, not ontology

A global standard/reference can:

```text
reduce pairwise bridge burden
improve reproducibility
create shared conventions
support large transport networks
```

but does not by itself make every target/value relation correct.

Therefore:

```text
GlobalReference
= powerful coordination/transport architecture
!= universal truthmaker.
```

---

# 37. Comparability as existence of a valid common relation

G's core reconstruction is:

```text
Comparable_R(E1,E2 | K,CVE)
```

iff there exists a suitable common comparison frame CF and semantic transports T1,T2 such that relation R is meaningful and claim-relevant semantics are preserved under the declared scope.

This does not require:

```text
same encoding
same unit
same numeric range
same target instance
same instrument
same laboratory
same reference path
```

unless the specific relation/CVE requires them.

---

# 38. Comparability may be partial

Two evaluations need not be wholly comparable or wholly incomparable.

Example:

Two multidimensional indices may align on:

```text
component A
component B
```

but not on the aggregate score.

Two ordinal scales may support order comparison but not difference comparison.

Thus:

```text
PartialComparability
= first-class possibility
```

and must preserve which relations are transportable.

---

# 39. Directional transport vs symmetric comparability

A semantic transport map can be directional or lossy:

```text
fine scale -> coarse category
```

may exist while reverse reconstruction does not.

Therefore:

```text
Transportability(T1->T2)
!= SymmetricEquivalence
```

A specific comparison relation may still be symmetric once both values are embedded in a suitable frame, but the bridge itself need not be invertible.

---

# 40. Invertibility revisited

F established:

```text
InvertibleMap != SemanticEquivalence
```

G strengthens it.

An invertible map between numeric ranges can be semantically invalid if:

```text
target criteria differ
weights differ
population references differ
latent constructs differ
regime versions differ
```

Conversely a non-invertible coarsening may still support limited comparison claims.

Thus:

```text
Invertibility
= mathematical property
not semantic transport criterion.
```

---

# 41. Compatibility architecture

G does not fully solve uncertainty/quality, but it types compatibility for the next stage.

Candidate:

```text
Compatible_R(E1,E2)
requires:

1. relevant comparability already established;
2. a sufficiently aligned target/sameness hypothesis;
3. an agreement/tolerance relation;
4. uncertainty/error/covariance structure adequate to evaluate that relation.
```

Thus compatibility consumes future Quality/Uncertainty architecture.

It is not a root of generic comparability.

---

# 42. Traceability network architecture

A traceability network can be modeled as:

```text
local result/frame
-> calibrated bridge
-> intermediate standards/procedures
-> reference
```

with each edge carrying:

```text
scope
version/time
uncertainty contribution
procedure identity
```

But G insists:

```text
TraceabilityPathExists
!= SemanticTransportValidity by itself
```

if the target/property semantics are mismatched.

Traceability is a specialized provenance/anchoring mechanism inside CRT-G1.

---

# 43. Reference-time/version dependence

References themselves can change.

Examples:

```text
new benchmark version
new reference population
revised standard realization
updated anchor items
new institutional base period
```

Therefore:

```text
ReferenceIdentity
requires version/time semantics.
```

A claim of comparability must specify which reference state was used.

This aligns with VIM's explicit requirement that reference information include relevant time in a traceability hierarchy.

---

# 44. PEA-E1 stress audit

G does not falsify the local property-evaluation core.

Instead it shows:

```text
PEA local validity
```

is insufficient for cross-evaluation relations.

No valid local evaluation case is found without G/A.

Therefore:

```text
PEA-E1 = SURVIVES G
```

---

# 45. QES-F1 stress audit

G strongly confirms F's distinctions:

```text
PS != VS != RE
RepresentationTransform != EvaluationRevision
Meaningfulness is relation/claim relative
```

Cross-scale comparability failures are often exactly failures to respect these distinctions.

No exact QES-F1 claim is falsified.

Therefore:

```text
QES-F1 = SURVIVES G
```

---

# 46. CRT-G1 result

Canonical provisional architecture:

```text
CRT-G1

CrossEvaluationClaim_R(E1,E2)
requires:

R
= declared relation to compare

TA_R
= target/kind/criterion alignment appropriate to R

CF
= common comparison frame

T1,T2
= valid semantic transports from local VS into CF

RefContext
= typed constitutive/anchoring/validation/transfer references
  with version/time/population where relevant

TCVE
= transport validity envelope
```

Optional/specialized mechanisms:

```text
traceability chain
calibration hierarchy
anchor test
reference material
common population design
bridge study
```

are realizations of this general architecture, not universal primitives.

---

# 47. G canonical firewalls

```text
LocalValidity != Comparability
SameUnit != Comparability
SameNumber != Comparability
SameName != Comparability
SameRange != Comparability
CommonReference != ValidTransport
Traceability != Correctness
Traceability != Compatibility
Convertibility != Comparability
Invertibility != SemanticEquivalence
Comparability != Compatibility
Compatibility != Equality
Equality != Interchangeability
SameTargetInstance != NecessaryForComparability
SameTargetName != SameTargetCriterion
PairwiseComparability != GlobalTransitivity
ReferenceTransform != EvaluationRevision
```

---

# 48. External source pressure synthesis

External literature is pressure/evidence, not canonical ontology.

## JCGM/BIPM VIM3

Provides mature special-case separations:

```text
metrological comparability
= same quantity kind + traceability to same reference

metrological compatibility
= specified measurand + uncertainty-aware agreement

traceability
= documented unbroken calibration chain to a reference
```

and explicitly notes that traceability does not guarantee uncertainty fitness or absence of mistakes.

VIM also shows same unit names/symbols may occur for different quantity kinds, falsifying same-unit shortcuts.

## VIM reference-material commutability

Shows that even a common calibrator/reference material must behave appropriately across procedures to support transfer.

This independently supports:

```text
CommonReference != ValidTransportBridge
```

## ETS score linking/equating

Equating is intended to preserve score meaning/interchangeability across forms; population invariance is a central requirement.

This independently supports:

```text
LinkExists != Interchangeability
CommonScale != SemanticEquivalence
BridgeValidity = population/CVE-sensitive
```

---

# 49. Foundation reopen audit

## WDF0

G strengthens:

```text
representation identity
!= semantic identity
!= target identity
```

```text
FoundationReopenCondition(WDF0) = NOT FIRED
```

## WDF1

No modal/chance claim fails.

```text
FoundationReopenCondition(WDF1) = NOT FIRED
```

## WDF2

No counterfactual architecture claim fails.

```text
FoundationReopenCondition(WDF2) = NOT FIRED
```

## WDF3

G relies heavily on criterion/version/target identity/CVE.

No exact WDF3 claim is falsified.

```text
ExactWDF3ClaimFalsified = NONE
WDF3 Foundation v1 = NOT FROZEN
```

## WDF4

No causal architecture claim fails.

```text
FoundationReopenCondition(WDF4) = NOT FIRED
```

---

# 50. Owner-line effect after G

The deep owner-native architecture now has three strong structural cores:

```text
PEA-E1
Property Evaluation Attribution

QES-F1
Evaluation / Value Structure

CRT-G1
Reference / Comparability / Transport
```

Measurement and Quantification remain derived families/practice labels over this deeper architecture.

This substantially increases pressure for a later canonical rebase.

However:

```text
CanonicalProjectRename = NOT ADMITTED
ProjectSplit = NOT EARNED
```

because Quality/Uncertainty/Validity remains a large unresolved owner responsibility.

---

# 51. Fresh post-G residual universe

Derived freshly:

```text
H-R1 Quality / Uncertainty / Error / Validity / Decision-Adequacy Architecture

H-R2 PEA + QES + CRT integrated destructive closure stress

H-R3 Epistemic Accountability / measurement-practice architecture

H-R4 Owner-line rebase / canonical naming / split control

H-R5 No-new-round control
```

---

# 52. H-R2 closure stress assessment

The three structural cores are now compact and mutually reinforcing.

However compatibility already exposed direct dependence on uncertainty/error/quality semantics.

Freezing before that layer is reconstructed would leave a major owner-native burden unresolved.

Disposition:

```text
HIGH VALUE
DEFER UNTIL QUALITY/UNCERTAINTY
```

---

# 53. H-R3 Epistemic Accountability assessment

EA remains important for auditability and justification.

But many of its concrete dimensions overlap with validation evidence, uncertainty characterization, robustness and quality control.

A Quality/Validity round should precede a dedicated practice round.

Disposition:

```text
HIGH VALUE
DOWNSTREAM / PARTIALLY ABSORBABLE
```

---

# 54. H-R4 naming/rebase assessment

Naming pressure is now strong:

```text
Measurement = derived
Quantification = derived
```

while deeper owner-native cores are PEA/QES/CRT.

Still, canonical rebase should wait until the final major structural owner burden—Quality/Uncertainty/Validity—is reconstructed.

Disposition:

```text
REQUIRED LATER
NOT NEXT RESEARCH OBJECT
```

---

# 55. H-R5 no-new-round control

Rejected.

Major unresolved distinctions remain:

```text
error vs uncertainty
accuracy vs trueness vs precision
reliability vs validity
quality vs truth
fitness for purpose
uncertainty-aware compatibility
robustness/selectivity/resolution
quality under transport
decision adequacy
```

These are not reducible to PEA/QES/CRT alone.

---

# 56. H-R1 wins

Canonical comparison:

```text
H-R1
= Quality / Uncertainty / Error / Validity / Decision-Adequacy
= WINNER
```

Reasons:

```text
CurrentCoverageDeficit = VERY HIGH
OwnerNativeCentrality = VERY HIGH
DirectDependencyOnG = YES
CompatibilityPrerequisite = YES
CrossRegimeBreadth = VERY HIGH
PrerequisiteReadiness = VERY HIGH
ClosureImportance = VERY HIGH
ExpectedArchitectureYield = VERY HIGH
```

---

# 57. WDF5-H admission

G admits:

# **WDF5-H — Quality / Uncertainty / Error / Validity / Decision-Adequacy Architecture**

Working question:

> How should truth/validity of a property evaluation be separated from uncertainty, error, accuracy, trueness, precision, reliability, robustness, selectivity, resolution and fitness for purpose; what is the minimal quality architecture for point-, interval-, distribution-, categorical-, psychometric-, software-, institutional- and Agent evaluations; when does uncertainty describe epistemic state versus modeled result dispersion versus target indeterminacy; how should compatibility and decision adequacy consume quality information; and which quality claims transport across reference/comparability bridges without becoming universal truth conditions for Property Evaluation Attribution?

WDF5-H is admitted for research only.

No WDF5-I is admitted in advance.

---

# 58. Mandatory WDF5-H attacks

At minimum:

```text
HH1 valid-but-imprecise result
HH2 precise-but-biased result
HH3 reliable-but-invalid psychometric score
HH4 accurate-by-luck result
HH5 low-uncertainty wrong-target result
HH6 high-uncertainty valid result
HH7 uncertainty omitted but actual relation valid
HH8 uncertainty well-characterized around invalid proxy
HH9 categorical/diagnostic uncertainty
HH10 interval/distribution-valued result quality
HH11 software metric sampling error vs semantic invalidity
HH12 cross-version quality transport
HH13 cross-lab uncertainty compatibility
HH14 correlated measurement uncertainty
HH15 robustness vs validity
HH16 sensitivity/selectivity tradeoff
HH17 resolution vs accuracy
HH18 decision threshold / fitness-for-purpose
HH19 Agent confidence vs measurement uncertainty
HH20 model uncertainty vs data uncertainty
HH21 ontic indeterminacy vs epistemic uncertainty
HH22 unknown unknown / model misspecification
HH23 quality improvement that does not improve target validity
HH24 reference traceability with inadequate uncertainty
```

Do not presuppose:

```text
low uncertainty => validity
precision => accuracy
reliability => validity
traceability => quality fitness
uncertainty => randomness only
all uncertainty is numeric probability
quality is one scalar score
```

---

# 59. WDF5-G canonical results

```text
G1 LocalValidity != Comparability.

G2 SameUnit/Number/Name/Range are not sufficient for comparability.

G3 Comparability != SameTargetInstance; different targets of the same relevant kind can be comparable.

G4 Comparability != Compatibility.

G5 Compatibility != Equality; Equality != Interchangeability.

G6 Cross-evaluation relations are claim-specific: Comparability_R.

G7 Common Comparison Frame CF is introduced.

G8 Semantic transport bridges T1,T2 are required to place local evaluations into CF.

G9 CRT-G1 provisional architecture is established: relation declaration, target/criterion alignment, common comparison frame, valid semantic transport, typed reference context, transport CVE.

G10 Same target can remain comparable across different units through valid transport.

G11 Nonlinear transforms are relation-specific; order may transport while differences/ratios do not.

G12 Reference roles are typed as constitutive, anchoring, validation and transfer roles.

G13 Reference population can constitute percentile/value semantics.

G14 Score linking != score interchangeability; equating requires stronger invariance/meaning conditions.

G15 Traceability is reconstructed as a special transport-provenance relation, not correctness/validity/compatibility by identity.

G16 Global reference is not universally necessary for local comparability.

G17 Common reference material does not automatically guarantee cross-procedure transport; commutability matters.

G18 Vector, cyclic and distribution-valued transport require structure-specific comparison frames.

G19 Institutional/Agent metric same-name/range comparisons fail without target/evaluation bridges.

G20 Pairwise bridge validity is not automatically transitive; CVE/reference/scale drift can break composition.

G21 Path independence/loop closure is a validation property, not a law.

G22 Partial comparability and directional transport are first-class cases.

G23 Invertibility remains insufficient for semantic equivalence.

G24 Compatibility consumes future uncertainty/quality architecture.

G25 PEA-E1 survives G.

G26 QES-F1 survives G.

G27 OwnerLineCoherence(WDF5) survives G; naming/rebase pressure strengthens but no rename/split is admitted.

G28 WDF5-H is admitted as Quality / Uncertainty / Error / Validity / Decision-Adequacy Architecture.
```

---

# 60. Canonical frontier after WDF5-G

```text
WDF5 = ADMITTED

WDF5-A = COMPLETE
WDF5-B = COMPLETE
WDF5-C = COMPLETE
WDF5-D = COMPLETE
WDF5-E = COMPLETE
WDF5-F = COMPLETE
WDF5-G = COMPLETE

PEA-E1
= STRONG PROVISIONAL SURVIVOR
= G + A under WDF3 K/CVE

QES-F1
= PROVISIONAL EVALUATION-STRUCTURE ARCHITECTURE
= PS / VS / RE / A_structure / Gamma / Meaningfulness

CRT-G1
= PROVISIONAL CROSS-EVALUATION TRANSPORT ARCHITECTURE
= R / TargetAlignment_R / CF / T1,T2 / RefContext / TCVE

Measurement
= DERIVED / FAMILY / PRACTICE LABEL

Quantification
= DERIVED STRUCTURED-EVALUATION FAMILY

Traceability
= SPECIAL TRANSPORT-PROVENANCE MECHANISM

WDF5-H
= ADMITTED
= Quality / Uncertainty / Error / Validity / Decision-Adequacy Architecture

WDF5-H execution
= NOT STARTED

WDF5 Foundation v1
= DOES NOT EXIST

WDF5-I+
= UNKNOWN / NOT ADMITTED

OwnerLineCoherence(WDF5)
= SURVIVES G

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

# 61. Exact next action

Execute:

# **WDF5-H — Quality / Uncertainty / Error / Validity / Decision-Adequacy Architecture**

Begin by separating:

```text
truth / attribution validity
error
uncertainty
accuracy / trueness / precision
reliability
robustness
fitness for purpose
```

and attack all shortcuts from low uncertainty/reliability/traceability to validity.

Keep PEA-E1, QES-F1 and CRT-G1 provisional; reopen them only on concrete H falsifiers.

Do not admit WDF5-I or freeze WDF5 Foundation v1 before H closes.
