from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Literal

from .canonical import sha256_digest

AuthorityClass = Literal[
    "anonymous-public",
    "free-key",
    "account",
    "student",
    "identity",
    "payment",
    "operator-grant",
]
SourceKind = Literal["aggregator", "index", "owner"]
TermsStatus = Literal["allowed", "conditional", "unknown", "forbidden"]
TransportStatus = Literal["available", "unavailable", "unknown"]
AuthorityStatus = Literal["active", "missing", "expired", "revoked", "unknown"]
EligibilityStatus = Literal["eligible", "ineligible", "unknown"]
AcquisitionMode = Literal[
    "agent-self-service",
    "human-login",
    "human-verification",
    "human-payment",
    "human-contract",
    "operator-grant",
]
Decision = Literal[
    "owner-verification-required",
    "acquisition-verification-required",
    "not-fit",
    "not-eligible",
    "blocked-by-terms",
    "authority-required",  # legacy projection; new evaluations use acquisition decisions below
    "acquire-now",
    "human-action-required",
    "prerequisite-acquisition-required",
    "defer-acquisition",
    "transport-verification-required",
    "transport-unavailable",
    "consumable-now",
]

_AUTHORITY_FRICTION: dict[str, int] = {
    "anonymous-public": 0,
    "free-key": 1,
    "account": 2,
    "student": 2,
    "identity": 3,
    "payment": 4,
    "operator-grant": 4,
}


def _utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include an explicit timezone")
    return parsed.astimezone(timezone.utc)


def _nonempty(label: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty")
    return value


def _tuple_strings(label: str, values: Iterable[str]) -> tuple[str, ...]:
    result = tuple(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))
    if any(not value for value in result):
        raise ValueError(f"{label} values must be non-empty")
    return result


def _unit_interval(label: str, value: float) -> float:
    result = float(value)
    if not 0.0 <= result <= 1.0:
        raise ValueError(f"{label} must be within [0, 1]")
    return result


@dataclass(frozen=True, slots=True)
class DiscoveryEvidence:
    """Evidence that a resource candidate was observed somewhere.

    Aggregators and indexes can create candidates, but only source_kind=owner may
    establish owner-native facts. This distinction is intentionally structural.
    """

    source_id: str
    source_kind: SourceKind
    observed_at: str
    locator: str
    evidence_refs: tuple[str, ...] = ()
    source_digest: str | None = None

    def __post_init__(self) -> None:
        _nonempty("source identity", self.source_id)
        _nonempty("source locator", self.locator)
        _utc(self.observed_at)
        if self.source_kind not in {"aggregator", "index", "owner"}:
            raise ValueError("unsupported discovery source kind")
        if self.source_digest is not None and not self.source_digest.startswith("sha256:"):
            raise ValueError("source digest must be sha256: when present")
        object.__setattr__(self, "evidence_refs", _tuple_strings("evidence refs", self.evidence_refs))

    def to_dict(self) -> dict[str, Any]:
        return {
            "sourceId": self.source_id,
            "sourceKind": self.source_kind,
            "observedAt": self.observed_at,
            "locator": self.locator,
            "sourceDigest": self.source_digest,
            "evidenceRefs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class ResourceCandidate:
    """A cheap-to-create candidate, not permission or a proven capability.

    ``diversity_potential`` is only a discovery/ranking heuristic for expected
    marginal diversity. It is not evidence that two resources are independent
    under any concrete failure domain. Independence remains an owner-native,
    current relation fact (for example a Workstation physical-access observation).
    """

    resource_id: str
    name: str
    capabilities: tuple[str, ...]
    provenance: tuple[DiscoveryEvidence, ...]
    owner_hint: str | None = None
    interfaces: tuple[str, ...] = ()
    reuse_potential: float = 0.5
    diversity_potential: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _nonempty("resource identity", self.resource_id)
        _nonempty("resource name", self.name)
        object.__setattr__(self, "capabilities", _tuple_strings("capabilities", self.capabilities))
        object.__setattr__(self, "interfaces", _tuple_strings("interfaces", self.interfaces))
        if not self.provenance:
            raise ValueError("resource candidates require discovery provenance")
        if not all(isinstance(item, DiscoveryEvidence) for item in self.provenance):
            raise ValueError("resource provenance must contain DiscoveryEvidence")
        object.__setattr__(self, "reuse_potential", _unit_interval("reuse potential", self.reuse_potential))
        object.__setattr__(self, "diversity_potential", _unit_interval("diversity potential", self.diversity_potential))
        if not isinstance(self.metadata, dict):
            raise ValueError("resource candidate metadata must be an object")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    @property
    def owner_evidence_present(self) -> bool:
        return any(item.source_kind == "owner" for item in self.provenance)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-candidate",
            "resourceId": self.resource_id,
            "name": self.name,
            "ownerHint": self.owner_hint,
            "capabilities": list(self.capabilities),
            "interfaces": list(self.interfaces),
            "reusePotential": self.reuse_potential,
            "diversityPotential": self.diversity_potential,
            "provenance": [item.to_dict() for item in self.provenance],
            "metadata": self.metadata,
        }


@dataclass(frozen=True, slots=True)
class OwnerVerification:
    """Current owner-native facts for exactly one candidate identity."""

    resource_id: str
    owner_id: str
    official_locator: str
    verified_at: str
    authority_class: AuthorityClass
    terms_status: TermsStatus
    allowed_purposes: tuple[str, ...]
    license_class: str
    cost_class: str
    quota_class: str
    machine_interfaces: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for label, value in (
            ("resource identity", self.resource_id),
            ("owner identity", self.owner_id),
            ("official locator", self.official_locator),
            ("license class", self.license_class),
            ("cost class", self.cost_class),
            ("quota class", self.quota_class),
        ):
            _nonempty(label, value)
        _utc(self.verified_at)
        if self.authority_class not in _AUTHORITY_FRICTION:
            raise ValueError("unsupported authority class")
        if self.terms_status not in {"allowed", "conditional", "unknown", "forbidden"}:
            raise ValueError("unsupported terms status")
        object.__setattr__(self, "allowed_purposes", _tuple_strings("allowed purposes", self.allowed_purposes))
        object.__setattr__(self, "machine_interfaces", _tuple_strings("machine interfaces", self.machine_interfaces))
        object.__setattr__(self, "evidence_refs", _tuple_strings("evidence refs", self.evidence_refs))
        object.__setattr__(self, "notes", _tuple_strings("notes", self.notes))
        if not self.evidence_refs:
            raise ValueError("owner verification requires owner evidence")

    @property
    def authority_friction(self) -> int:
        return _AUTHORITY_FRICTION[self.authority_class]

    def is_current(self, *, as_of: str, max_age_seconds: int) -> bool:
        if max_age_seconds < 0:
            raise ValueError("max owner-verification age must be non-negative")
        age = (_utc(as_of) - _utc(self.verified_at)).total_seconds()
        return 0 <= age <= max_age_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-owner-verification",
            "resourceId": self.resource_id,
            "ownerId": self.owner_id,
            "officialLocator": self.official_locator,
            "verifiedAt": self.verified_at,
            "authorityClass": self.authority_class,
            "termsStatus": self.terms_status,
            "allowedPurposes": list(self.allowed_purposes),
            "licenseClass": self.license_class,
            "costClass": self.cost_class,
            "quotaClass": self.quota_class,
            "machineInterfaces": list(self.machine_interfaces),
            "evidenceRefs": list(self.evidence_refs),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class TransportEvidence:
    """Workstation-owned current reachability attached without becoming World truth."""

    resource_id: str
    observed_at: str
    path_id: str
    resolver_id: str
    status: TransportStatus
    evidence_refs: tuple[str, ...]
    latency_ms: float | None = None

    def __post_init__(self) -> None:
        for label, value in (
            ("resource identity", self.resource_id),
            ("path identity", self.path_id),
            ("resolver identity", self.resolver_id),
        ):
            _nonempty(label, value)
        _utc(self.observed_at)
        if self.status not in {"available", "unavailable", "unknown"}:
            raise ValueError("unsupported transport status")
        object.__setattr__(self, "evidence_refs", _tuple_strings("evidence refs", self.evidence_refs))
        if self.latency_ms is not None and float(self.latency_ms) < 0:
            raise ValueError("transport latency must be non-negative")

    def is_current(self, *, as_of: str, max_age_seconds: int) -> bool:
        if max_age_seconds < 0:
            raise ValueError("max transport age must be non-negative")
        age = (_utc(as_of) - _utc(self.observed_at)).total_seconds()
        return 0 <= age <= max_age_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "resourceId": self.resource_id,
            "observedAt": self.observed_at,
            "pathId": self.path_id,
            "resolverId": self.resolver_id,
            "status": self.status,
            "latencyMs": self.latency_ms,
            "evidenceRefs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class AuthorityEvidence:
    """Evidence that Ordivon actually possesses a resource-specific authority.

    OwnerVerification states what the provider requires. This object states what
    we currently possess. It never carries a secret value: ``authority_id`` is a
    non-secret handle such as a secret reference, account id, or entitlement id.
    """

    resource_id: str
    observed_at: str
    authority_class: AuthorityClass
    authority_id: str
    status: AuthorityStatus
    evidence_refs: tuple[str, ...]
    expires_at: str | None = None

    def __post_init__(self) -> None:
        _nonempty("resource identity", self.resource_id)
        _nonempty("authority identity", self.authority_id)
        _utc(self.observed_at)
        if self.authority_class not in _AUTHORITY_FRICTION:
            raise ValueError("unsupported authority class")
        if self.status not in {"active", "missing", "expired", "revoked", "unknown"}:
            raise ValueError("unsupported authority status")
        if self.expires_at is not None:
            _utc(self.expires_at)
        object.__setattr__(self, "evidence_refs", _tuple_strings("evidence refs", self.evidence_refs))
        if not self.evidence_refs:
            raise ValueError("authority evidence requires evidence refs")

    def is_active(self, *, as_of: str, max_age_seconds: int) -> bool:
        if max_age_seconds < 0:
            raise ValueError("max authority-evidence age must be non-negative")
        age = (_utc(as_of) - _utc(self.observed_at)).total_seconds()
        if not 0 <= age <= max_age_seconds or self.status != "active":
            return False
        return self.expires_at is None or _utc(self.expires_at) > _utc(as_of)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-authority-evidence",
            "resourceId": self.resource_id,
            "observedAt": self.observed_at,
            "authorityClass": self.authority_class,
            "authorityId": self.authority_id,
            "status": self.status,
            "expiresAt": self.expires_at,
            "evidenceRefs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class AcquisitionAssessment:
    """Current estimate of whether acquiring missing authority is worth doing.

    Account/key/student/payment friction is modeled as cost, never as moral veto.
    Values are normalized so the assumptions remain inspectable and falsifiable.
    """

    resource_id: str
    observed_at: str
    eligibility: EligibilityStatus
    acquisition_mode: AcquisitionMode
    expected_benefit: float
    option_value: float
    acquisition_cost: float
    maintenance_cost: float
    payment_exposure: float
    lock_in_cost: float
    expiry_pressure: float
    evidence_refs: tuple[str, ...]
    human_actions: tuple[str, ...] = ()
    prerequisite_resources: tuple[str, ...] = ()
    nominal_value: str | None = None
    expires_at: str | None = None

    def __post_init__(self) -> None:
        _nonempty("resource identity", self.resource_id)
        _utc(self.observed_at)
        if self.eligibility not in {"eligible", "ineligible", "unknown"}:
            raise ValueError("unsupported acquisition eligibility")
        if self.acquisition_mode not in {
            "agent-self-service", "human-login", "human-verification", "human-payment",
            "human-contract", "operator-grant",
        }:
            raise ValueError("unsupported acquisition mode")
        for label in (
            "expected_benefit", "option_value", "acquisition_cost", "maintenance_cost",
            "payment_exposure", "lock_in_cost", "expiry_pressure",
        ):
            object.__setattr__(self, label, _unit_interval(label.replace("_", " "), getattr(self, label)))
        object.__setattr__(self, "evidence_refs", _tuple_strings("evidence refs", self.evidence_refs))
        object.__setattr__(self, "human_actions", _tuple_strings("human actions", self.human_actions))
        object.__setattr__(self, "prerequisite_resources", _tuple_strings("prerequisite resources", self.prerequisite_resources))
        if self.resource_id in set(self.prerequisite_resources):
            raise ValueError("resource cannot depend on its own acquisition")
        if not self.evidence_refs:
            raise ValueError("acquisition assessments require evidence refs")
        if self.expires_at is not None:
            _utc(self.expires_at)
        if self.nominal_value is not None:
            _nonempty("nominal value", self.nominal_value)

    @property
    def requires_human_action(self) -> bool:
        return self.acquisition_mode != "agent-self-service"

    @property
    def gross_opportunity_value(self) -> float:
        return 0.65 * self.expected_benefit + 0.35 * self.option_value

    @property
    def burden(self) -> float:
        return (
            0.25 * self.acquisition_cost
            + 0.20 * self.maintenance_cost
            + 0.25 * self.payment_exposure
            + 0.15 * self.lock_in_cost
            + 0.15 * self.expiry_pressure
        )

    @property
    def net_opportunity_value(self) -> float:
        return self.gross_opportunity_value - self.burden

    def is_current(self, *, as_of: str, max_age_seconds: int) -> bool:
        if max_age_seconds < 0:
            raise ValueError("max acquisition-assessment age must be non-negative")
        age = (_utc(as_of) - _utc(self.observed_at)).total_seconds()
        if not 0 <= age <= max_age_seconds:
            return False
        return self.expires_at is None or _utc(self.expires_at) > _utc(as_of)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-acquisition-assessment",
            "resourceId": self.resource_id,
            "observedAt": self.observed_at,
            "eligibility": self.eligibility,
            "acquisitionMode": self.acquisition_mode,
            "expectedBenefit": self.expected_benefit,
            "optionValue": self.option_value,
            "acquisitionCost": self.acquisition_cost,
            "maintenanceCost": self.maintenance_cost,
            "paymentExposure": self.payment_exposure,
            "lockInCost": self.lock_in_cost,
            "expiryPressure": self.expiry_pressure,
            "grossOpportunityValue": round(self.gross_opportunity_value, 6),
            "burden": round(self.burden, 6),
            "netOpportunityValue": round(self.net_opportunity_value, 6),
            "requiresHumanAction": self.requires_human_action,
            "humanActions": list(self.human_actions),
            "prerequisiteResources": list(self.prerequisite_resources),
            "nominalValue": self.nominal_value,
            "expiresAt": self.expires_at,
            "evidenceRefs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class ConsumerDemand:
    workload_id: str
    purpose: str
    required_capabilities: tuple[str, ...]
    preferred_capabilities: tuple[str, ...] = ()
    # Kept for compatibility/reporting. It is NOT an acquisition veto.
    authority_budget: AuthorityClass = "anonymous-public"
    owner_max_age_seconds: int = 30 * 24 * 60 * 60
    authority_max_age_seconds: int = 24 * 60 * 60
    acquisition_max_age_seconds: int = 7 * 24 * 60 * 60
    transport_max_age_seconds: int = 5 * 60
    acquisition_threshold: float = 0.15
    reuse_weight: float = 0.25
    diversity_weight: float = 0.15

    def __post_init__(self) -> None:
        _nonempty("workload identity", self.workload_id)
        _nonempty("purpose", self.purpose)
        object.__setattr__(self, "required_capabilities", _tuple_strings("required capabilities", self.required_capabilities))
        object.__setattr__(self, "preferred_capabilities", _tuple_strings("preferred capabilities", self.preferred_capabilities))
        if self.authority_budget not in _AUTHORITY_FRICTION:
            raise ValueError("unsupported authority budget")
        if min(self.owner_max_age_seconds, self.authority_max_age_seconds, self.acquisition_max_age_seconds, self.transport_max_age_seconds) < 0:
            raise ValueError("currentness budgets must be non-negative")
        threshold = float(self.acquisition_threshold)
        if not -1.0 <= threshold <= 1.0:
            raise ValueError("acquisition threshold must be within [-1, 1]")
        object.__setattr__(self, "acquisition_threshold", threshold)
        object.__setattr__(self, "reuse_weight", _unit_interval("reuse weight", self.reuse_weight))
        object.__setattr__(self, "diversity_weight", _unit_interval("diversity weight", self.diversity_weight))

    @property
    def authority_friction_budget(self) -> int:
        """Legacy projection only; acquisition is no longer hard-gated by this value."""
        return _AUTHORITY_FRICTION[self.authority_budget]


@dataclass(frozen=True, slots=True)
class ConsumptionOutcome:
    resource_id: str
    workload_id: str
    observed_at: str
    useful: bool
    value: float
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _nonempty("resource identity", self.resource_id)
        _nonempty("workload identity", self.workload_id)
        _utc(self.observed_at)
        object.__setattr__(self, "value", _unit_interval("outcome value", self.value))
        object.__setattr__(self, "evidence_refs", _tuple_strings("evidence refs", self.evidence_refs))
        if not self.evidence_refs:
            raise ValueError("consumption outcomes require evidence")


@dataclass(frozen=True, slots=True)
class ResourceEvaluation:
    """Demand-scoped planning projection, not a durable capability grant.

    ``consumable-now`` means the supplied owner/authority/transport evidence is
    sufficient for this demand at ``as_of``. It does not mean that a collection
    of evaluations forms redundant capability: substitutability and relevant
    failure-domain independence must be established separately by their owners.
    """

    resource_id: str
    decision: Decision
    hard_reasons: tuple[str, ...]
    demand_fit: float
    preferred_fit: float
    evidence_quality: float
    reuse_potential: float
    diversity_potential: float
    outcome_prior: float
    authority_friction: int
    authority_present: bool
    acquisition_net_value: float | None
    acquisition_mode: AcquisitionMode | None
    potential_score: float

    def __post_init__(self) -> None:
        if self.decision not in {
            "owner-verification-required", "acquisition-verification-required", "not-fit",
            "not-eligible", "blocked-by-terms", "authority-required", "acquire-now",
            "human-action-required", "prerequisite-acquisition-required", "defer-acquisition", "transport-verification-required",
            "transport-unavailable", "consumable-now",
        }:
            raise ValueError("unsupported resource decision")

    @property
    def benefit_vector(self) -> tuple[float, float, float, float, float]:
        return (
            self.demand_fit,
            self.preferred_fit,
            self.evidence_quality,
            self.reuse_potential,
            self.diversity_potential,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-evaluation",
            "resourceId": self.resource_id,
            "decision": self.decision,
            "hardReasons": list(self.hard_reasons),
            "demandFit": self.demand_fit,
            "preferredFit": self.preferred_fit,
            "evidenceQuality": self.evidence_quality,
            "reusePotential": self.reuse_potential,
            "diversityPotential": self.diversity_potential,
            "outcomePrior": self.outcome_prior,
            "authorityFriction": self.authority_friction,
            "authorityPresent": self.authority_present,
            "acquisitionNetValue": self.acquisition_net_value,
            "acquisitionMode": self.acquisition_mode,
            "potentialScore": self.potential_score,
        }


def evaluate_resource(
    candidate: ResourceCandidate,
    demand: ConsumerDemand,
    *,
    as_of: str,
    owner: OwnerVerification | None = None,
    authority: AuthorityEvidence | None = None,
    acquisition: AcquisitionAssessment | None = None,
    prerequisite_authorities: Iterable[AuthorityEvidence] = (),
    transport: TransportEvidence | None = None,
    outcomes: Iterable[ConsumptionOutcome] = (),
) -> ResourceEvaluation:
    """Evaluate one candidate without conflating required and possessed authority.

    Provider requirements are owner truth. Acquisition is a value/cost decision.
    AuthorityEvidence proves what is actually possessed. Only then does transport
    become relevant for non-anonymous resources.
    """

    _utc(as_of)
    required = set(demand.required_capabilities)
    offered = set(candidate.capabilities)
    missing = sorted(required - offered)
    required_fit = 1.0 if not required else len(required & offered) / len(required)
    preferred = set(demand.preferred_capabilities)
    preferred_fit = 0.0 if not preferred else len(preferred & offered) / len(preferred)

    relevant_outcomes = [
        item for item in outcomes
        if item.resource_id == candidate.resource_id and item.workload_id == demand.workload_id
    ]
    outcome_prior = (
        sum(item.value if item.useful else 0.0 for item in relevant_outcomes) / len(relevant_outcomes)
        if relevant_outcomes else 0.5
    )

    decision: Decision
    reasons: list[str] = []
    authority_friction = 5
    owner_current = False
    authority_present = False
    acquisition_current = False
    acquisition_net_value: float | None = None
    acquisition_mode: AcquisitionMode | None = None
    transport_current = False

    if missing:
        decision = "not-fit"
        reasons.append("missing-required-capabilities:" + ",".join(missing))
    elif owner is None or owner.resource_id != candidate.resource_id:
        decision = "owner-verification-required"
        reasons.append("candidate-has-no-matching-owner-verification")
    else:
        authority_friction = owner.authority_friction
        owner_current = owner.is_current(as_of=as_of, max_age_seconds=demand.owner_max_age_seconds)
        if not owner_current:
            decision = "owner-verification-required"
            reasons.append("owner-verification-stale")
        elif owner.terms_status == "forbidden" or demand.purpose not in set(owner.allowed_purposes):
            decision = "blocked-by-terms"
            reasons.append("consumer-purpose-not-owner-admitted")
        elif owner.terms_status == "unknown":
            decision = "owner-verification-required"
            reasons.append("owner-terms-unknown")
        else:
            if owner.authority_class == "anonymous-public":
                authority_present = True
            elif (
                authority is not None
                and authority.resource_id == candidate.resource_id
                and authority.authority_class == owner.authority_class
                and authority.is_active(as_of=as_of, max_age_seconds=demand.authority_max_age_seconds)
            ):
                authority_present = True
            else:
                if authority is not None and authority.resource_id == candidate.resource_id:
                    reasons.append("authority-evidence-not-active-or-not-matching-owner-requirement")
                if acquisition is None or acquisition.resource_id != candidate.resource_id:
                    decision = "acquisition-verification-required"
                    reasons.append("missing-current-acquisition-assessment")
                else:
                    acquisition_current = acquisition.is_current(
                        as_of=as_of, max_age_seconds=demand.acquisition_max_age_seconds
                    )
                    acquisition_mode = acquisition.acquisition_mode
                    acquisition_net_value = acquisition.net_opportunity_value
                    prerequisite_map = {row.resource_id: row for row in prerequisite_authorities}
                    missing_prerequisites = [
                        resource_id for resource_id in acquisition.prerequisite_resources
                        if resource_id not in prerequisite_map
                        or not prerequisite_map[resource_id].is_active(
                            as_of=as_of, max_age_seconds=demand.authority_max_age_seconds
                        )
                    ]
                    if not acquisition_current:
                        decision = "acquisition-verification-required"
                        reasons.append("acquisition-assessment-stale")
                    elif missing_prerequisites:
                        decision = "prerequisite-acquisition-required"
                        reasons.append("missing-prerequisite-authority:" + ",".join(missing_prerequisites))
                    elif acquisition.eligibility == "ineligible":
                        decision = "not-eligible"
                        reasons.append("current-owner-eligibility-not-satisfied")
                    elif acquisition_net_value < demand.acquisition_threshold:
                        decision = "defer-acquisition"
                        reasons.append(
                            f"net-opportunity-{acquisition_net_value:.3f}-below-threshold-{demand.acquisition_threshold:.3f}"
                        )
                    elif acquisition.eligibility == "unknown":
                        if acquisition.requires_human_action:
                            decision = "human-action-required"
                            reasons.append("positive-net-value-eligibility-resolved-in-human-acquisition-flow")
                        else:
                            decision = "acquisition-verification-required"
                            reasons.append("acquisition-eligibility-unknown")
                    elif acquisition.requires_human_action:
                        decision = "human-action-required"
                        reasons.append("positive-net-value-requires-human-action")
                    else:
                        decision = "acquire-now"
                        reasons.append("positive-net-value-agent-acquisition")

            if authority_present:
                if transport is None or transport.resource_id != candidate.resource_id:
                    decision = "transport-verification-required"
                    reasons.append("no-matching-transport-evidence")
                else:
                    transport_current = transport.is_current(
                        as_of=as_of, max_age_seconds=demand.transport_max_age_seconds
                    )
                    if not transport_current or transport.status == "unknown":
                        decision = "transport-verification-required"
                        reasons.append("transport-evidence-stale-or-unknown")
                    elif transport.status == "unavailable":
                        decision = "transport-unavailable"
                        reasons.append("current-scoped-transport-unavailable")
                    else:
                        decision = "consumable-now"

    evidence_quality = 0.0
    if owner is not None and owner.resource_id == candidate.resource_id:
        evidence_quality += 0.45 if owner_current else 0.2
    if candidate.owner_evidence_present:
        evidence_quality += 0.1
    if authority is not None and authority.resource_id == candidate.resource_id:
        evidence_quality += 0.1 if authority_present else 0.03
    if acquisition is not None and acquisition.resource_id == candidate.resource_id:
        evidence_quality += 0.1 if acquisition_current else 0.03
    if transport is not None and transport.resource_id == candidate.resource_id:
        evidence_quality += 0.35 if transport_current and transport.status == "available" else 0.1
    if relevant_outcomes:
        evidence_quality += 0.1
    evidence_quality = min(1.0, evidence_quality)

    if authority_present:
        acquisition_term = 1.0
    elif acquisition_net_value is not None:
        acquisition_term = max(0.0, min(1.0, (acquisition_net_value + 1.0) / 2.0))
    else:
        acquisition_term = 0.5
    potential_score = (
        0.30 * required_fit
        + 0.10 * preferred_fit
        + 0.15 * evidence_quality
        + demand.reuse_weight * candidate.reuse_potential
        + demand.diversity_weight * candidate.diversity_potential
        + 0.10 * outcome_prior
        + 0.10 * acquisition_term
    )
    normalizer = 0.75 + demand.reuse_weight + demand.diversity_weight
    potential_score = min(1.0, potential_score / normalizer)

    return ResourceEvaluation(
        resource_id=candidate.resource_id,
        decision=decision,
        hard_reasons=tuple(reasons),
        demand_fit=round(required_fit, 6),
        preferred_fit=round(preferred_fit, 6),
        evidence_quality=round(evidence_quality, 6),
        reuse_potential=candidate.reuse_potential,
        diversity_potential=candidate.diversity_potential,
        outcome_prior=round(outcome_prior, 6),
        authority_friction=authority_friction,
        authority_present=authority_present,
        acquisition_net_value=None if acquisition_net_value is None else round(acquisition_net_value, 6),
        acquisition_mode=acquisition_mode,
        potential_score=round(potential_score, 6),
    )


def pareto_frontier(evaluations: Iterable[ResourceEvaluation]) -> tuple[ResourceEvaluation, ...]:
    """Return non-dominated consumable candidates on benefit dimensions only.

    Authority friction is not a moral penalty. Once authority is actually held,
    the frontier should not demote a useful resource merely because acquisition
    once required an account, student verification, or payment verification.
    """

    rows = [row for row in evaluations if row.decision == "consumable-now"]

    def dominates(left: ResourceEvaluation, right: ResourceEvaluation) -> bool:
        benefit_ge = all(a >= b for a, b in zip(left.benefit_vector, right.benefit_vector, strict=True))
        strict = any(a > b for a, b in zip(left.benefit_vector, right.benefit_vector, strict=True))
        return benefit_ge and strict

    frontier = [row for row in rows if not any(dominates(other, row) for other in rows if other is not row)]
    return tuple(sorted(frontier, key=lambda row: (-row.potential_score, row.resource_id)))


def rank_resource_evaluations(evaluations: Iterable[ResourceEvaluation]) -> tuple[ResourceEvaluation, ...]:
    decision_order = {
        "consumable-now": 0,
        "acquire-now": 1,
        "human-action-required": 2,
        "prerequisite-acquisition-required": 3,
        "transport-verification-required": 4,
        "acquisition-verification-required": 5,
        "owner-verification-required": 6,
        "authority-required": 6,
        "defer-acquisition": 7,
        "transport-unavailable": 8,
        "not-eligible": 9,
        "not-fit": 10,
        "blocked-by-terms": 11,
    }
    return tuple(sorted(
        evaluations,
        key=lambda row: (decision_order[row.decision], -row.potential_score, row.resource_id),
    ))


@dataclass(frozen=True, slots=True)
class ResourceOpportunityBoard:
    """Demand-scoped work queue for discovery, acquisition, transport and use."""

    workload_id: str
    as_of: str
    candidate_count: int
    evaluations: tuple[ResourceEvaluation, ...]
    frontier: tuple[ResourceEvaluation, ...]
    owner_verification_queue: tuple[ResourceEvaluation, ...]
    acquisition_verification_queue: tuple[ResourceEvaluation, ...]
    acquire_now_queue: tuple[ResourceEvaluation, ...]
    human_action_queue: tuple[ResourceEvaluation, ...]
    dependent_acquisition_queue: tuple[ResourceEvaluation, ...]
    transport_verification_queue: tuple[ResourceEvaluation, ...]
    authority_queue: tuple[ResourceEvaluation, ...]
    consumption_queue: tuple[ResourceEvaluation, ...]
    feedback_queue: tuple[ResourceEvaluation, ...]
    deferred_acquisition: tuple[ResourceEvaluation, ...]
    rejected: tuple[ResourceEvaluation, ...]

    def to_dict(self) -> dict[str, Any]:
        def ids(rows: tuple[ResourceEvaluation, ...]) -> list[str]:
            return [row.resource_id for row in rows]
        return {
            "schemaVersion": 2,
            "kind": "ordivon.world.resource-opportunity-board",
            "workloadId": self.workload_id,
            "asOf": self.as_of,
            "candidateCount": self.candidate_count,
            "frontier": ids(self.frontier),
            "ownerVerificationQueue": ids(self.owner_verification_queue),
            "acquisitionVerificationQueue": ids(self.acquisition_verification_queue),
            "acquireNowQueue": ids(self.acquire_now_queue),
            "humanActionQueue": ids(self.human_action_queue),
            "dependentAcquisitionQueue": ids(self.dependent_acquisition_queue),
            "transportVerificationQueue": ids(self.transport_verification_queue),
            "authorityQueue": ids(self.authority_queue),
            "consumptionQueue": ids(self.consumption_queue),
            "feedbackQueue": ids(self.feedback_queue),
            "deferredAcquisition": ids(self.deferred_acquisition),
            "rejected": ids(self.rejected),
            "evaluations": [row.to_dict() for row in self.evaluations],
        }


def build_opportunity_board(
    candidates: Iterable[ResourceCandidate],
    demand: ConsumerDemand,
    *,
    as_of: str,
    owners: Iterable[OwnerVerification] = (),
    authorities: Iterable[AuthorityEvidence] = (),
    acquisitions: Iterable[AcquisitionAssessment] = (),
    transports: Iterable[TransportEvidence] = (),
    outcomes: Iterable[ConsumptionOutcome] = (),
    verification_budget: int = 12,
) -> ResourceOpportunityBoard:
    """Turn a broad universe into bounded verification plus active acquisition.

    Broad discovery stays cheap. Verification work is budgeted. Positive-EV
    legitimate acquisition is surfaced explicitly rather than hidden behind an
    authority queue or suppressed by an anonymous-only preference.
    """

    if verification_budget < 0:
        raise ValueError("verification budget must be non-negative")
    _utc(as_of)
    candidate_rows = tuple(candidates)
    owner_map = {row.resource_id: row for row in owners}
    authority_map = {row.resource_id: row for row in authorities}
    acquisition_map = {row.resource_id: row for row in acquisitions}
    transport_map = {row.resource_id: row for row in transports}
    outcome_rows = tuple(outcomes)
    evaluated = tuple(
        evaluate_resource(
            candidate, demand, as_of=as_of,
            owner=owner_map.get(candidate.resource_id),
            authority=authority_map.get(candidate.resource_id),
            acquisition=acquisition_map.get(candidate.resource_id),
            prerequisite_authorities=tuple(authority_map.values()),
            transport=transport_map.get(candidate.resource_id),
            outcomes=outcome_rows,
        )
        for candidate in candidate_rows
    )
    ranked = rank_resource_evaluations(evaluated)

    def bucket(decision: Decision) -> tuple[ResourceEvaluation, ...]:
        return tuple(row for row in ranked if row.decision == decision)

    owner_queue = bucket("owner-verification-required")[:verification_budget]
    remaining = max(0, verification_budget - len(owner_queue))
    acquisition_verification = bucket("acquisition-verification-required")[:remaining]
    remaining = max(0, remaining - len(acquisition_verification))
    transport_queue = bucket("transport-verification-required")[:remaining]
    acquire_now = bucket("acquire-now")
    human_action = bucket("human-action-required")
    dependent = bucket("prerequisite-acquisition-required")
    consumable = bucket("consumable-now")
    frontier = pareto_frontier(consumable)
    outcome_keys = {(row.resource_id, row.workload_id) for row in outcome_rows}
    feedback = tuple(
        row for row in consumable
        if (row.resource_id, demand.workload_id) not in outcome_keys
    )
    deferred = bucket("defer-acquisition")
    rejected = tuple(
        row for row in ranked
        if row.decision in {"not-fit", "not-eligible", "blocked-by-terms", "transport-unavailable"}
    )
    return ResourceOpportunityBoard(
        workload_id=demand.workload_id,
        as_of=as_of,
        candidate_count=len(candidate_rows),
        evaluations=ranked,
        frontier=frontier,
        owner_verification_queue=owner_queue,
        acquisition_verification_queue=acquisition_verification,
        acquire_now_queue=acquire_now,
        human_action_queue=human_action,
        dependent_acquisition_queue=dependent,
        transport_verification_queue=transport_queue,
        authority_queue=acquire_now + human_action,
        consumption_queue=consumable,
        feedback_queue=feedback,
        deferred_acquisition=deferred,
        rejected=rejected,
    )
