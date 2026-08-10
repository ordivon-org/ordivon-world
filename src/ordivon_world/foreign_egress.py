from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
from typing import Any

from .canonical import sha256_digest
from .schemas import validate_contract


_WORKSTATION_AUTHORITY = "ordivon.workstation.surfpath"
_SURFPATH_OBSERVATION_KIND = "ordivon.workstation.surfshark-path-observation"
_SURFPATH_STATUS_KIND = "ordivon.workstation.surfshark-path-status"


class ForeignEgressProjectionError(ValueError):
    pass


class ForeignEgressCapabilityStale(ForeignEgressProjectionError):
    pass


def _parse_time(value: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ForeignEgressProjectionError(f"invalid observation time: {value}") from error
    if parsed.tzinfo is None:
        raise ForeignEgressProjectionError("observation time must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _format_time(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _require_digest(value: Any, field: str) -> str:
    digest = str(value)
    if not digest.startswith("sha256:") or len(digest) != 71:
        raise ForeignEgressProjectionError(f"{field} is not a sha256 digest")
    return digest


def _verify_surfpath_observation(value: dict[str, Any]) -> str:
    if int(value.get("schemaVersion", 0)) != 2:
        raise ForeignEgressProjectionError("Surfpath observation schemaVersion must be 2")
    if value.get("kind") != _SURFPATH_OBSERVATION_KIND:
        raise ForeignEgressProjectionError("document is not a Surfpath path observation")
    if value.get("truthRole") != "point-in-time-observation":
        raise ForeignEgressProjectionError("Surfpath observation truthRole is not point-in-time")
    claimed = _require_digest(value.get("observationDigest", ""), "observationDigest")
    payload = {key: item for key, item in value.items() if key != "observationDigest"}
    observed = sha256_digest(payload)
    if observed != claimed:
        raise ForeignEgressProjectionError(
            f"Surfpath observation digest mismatch: expected {claimed}, observed {observed}"
        )
    _parse_time(str(value.get("observedAt", "")))
    return claimed


def _freshness_from_status(status: dict[str, Any], observation_digest: str) -> int:
    if int(status.get("schemaVersion", 0)) != 2 or status.get("kind") != _SURFPATH_STATUS_KIND:
        raise ForeignEgressProjectionError("document is not a Surfpath schema-v2 status")
    observation = status.get("observation")
    if not isinstance(observation, dict):
        raise ForeignEgressProjectionError("Surfpath status has no observation projection")
    if observation.get("observationDigest") != observation_digest:
        raise ForeignEgressProjectionError("Surfpath status and observation identities differ")
    if int(observation.get("schemaVersion", 0)) != 2:
        raise ForeignEgressProjectionError("Surfpath status points at an obsolete observation")
    try:
        maximum = int(observation["maxAgeSeconds"])
        age = float(observation["ageSeconds"])
    except (KeyError, TypeError, ValueError) as error:
        raise ForeignEgressProjectionError("Surfpath status lacks bounded freshness evidence") from error
    if maximum <= 0:
        raise ForeignEgressProjectionError("Surfpath freshness window must be positive")
    if observation.get("fresh") is not True or observation.get("executableNow") is not True:
        raise ForeignEgressCapabilityStale(
            "Workstation does not currently project this Surfpath observation as executable"
        )
    if age < 0 or age > maximum:
        raise ForeignEgressCapabilityStale(
            f"Workstation freshness evidence is outside its action window: age={age} max={maximum}"
        )
    return maximum


def _selected_candidate(observation: dict[str, Any], path_digest: str) -> dict[str, Any]:
    path_digest = _require_digest(path_digest, "pathDigest")
    ranked = observation.get("rankedPaths")
    if not isinstance(ranked, list) or path_digest not in ranked:
        raise ForeignEgressProjectionError(
            "Agent-selected pathDigest is not a qualified path in this observation"
        )
    candidates = observation.get("candidates")
    if not isinstance(candidates, list):
        raise ForeignEgressProjectionError("Surfpath observation has no candidate set")
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        path = candidate.get("path")
        if isinstance(path, dict) and path.get("pathDigest") == path_digest:
            if candidate.get("qualified") is not True:
                raise ForeignEgressProjectionError("selected Surfpath candidate is not qualified")
            return candidate
    raise ForeignEgressProjectionError("selected pathDigest is absent from observation candidates")


def _project_relationship(
    observation: dict[str, Any], candidate: dict[str, Any]
) -> tuple[dict[str, Any], tuple[str, ...]]:
    path = candidate.get("path")
    if not isinstance(path, dict):
        raise ForeignEgressProjectionError("selected candidate has no path binding")
    ingress = path.get("ingress")
    if not isinstance(ingress, dict):
        raise ForeignEgressProjectionError("selected path has no ingress binding")

    required_targets = tuple(sorted(str(item) for item in observation.get("requiredTargets", [])))
    if not required_targets:
        raise ForeignEgressProjectionError(
            "foreign egress capability requires at least one destination-qualified target"
        )
    targets = candidate.get("targets")
    if not isinstance(targets, dict):
        raise ForeignEgressProjectionError("selected candidate has no destination evidence")
    projected_targets: list[dict[str, str]] = []
    for name in required_targets:
        target = targets.get(name)
        if not isinstance(target, dict) or target.get("ok") is not True:
            raise ForeignEgressProjectionError(
                f"selected candidate lacks successful destination evidence for {name}"
            )
        url = str(target.get("url", ""))
        selected_address = str(target.get("selectedAddress", ""))
        if not url or not selected_address:
            raise ForeignEgressProjectionError(
                f"selected candidate lacks frozen destination identity for {name}"
            )
        projected_targets.append(
            {"name": name, "url": url, "selectedAddress": selected_address}
        )

    egress_value = candidate.get("egress")
    egress: dict[str, str | None] | None = None
    if isinstance(egress_value, dict) and egress_value.get("ok") is True:
        facts = egress_value.get("facts")
        if isinstance(facts, dict):
            egress = {
                "ip": str(facts["ip"]) if facts.get("ip") else None,
                "location": str(facts["loc"]) if facts.get("loc") else None,
                "colo": str(facts["colo"]) if facts.get("colo") else None,
            }

    try:
        endpoint_port = int(path["endpointPort"])
    except (KeyError, TypeError, ValueError) as error:
        raise ForeignEgressProjectionError("selected path has no valid endpoint port") from error

    relationship: dict[str, Any] = {
        "ingress": {
            "name": str(ingress["name"]),
            "routeProfile": (
                str(ingress["routeProfile"]) if ingress.get("routeProfile") is not None else None
            ),
        },
        "transport": str(path["protocol"]),
        "node": str(path["node"]),
        "endpoint": {
            "host": str(path["endpointHost"]),
            "ip": str(path["endpointIp"]),
            "port": endpoint_port,
        },
        "providerEvidenceDigest": _require_digest(path["providerDigest"], "providerDigest"),
        "configDigest": _require_digest(path["configDigest"], "configDigest"),
        "egress": egress,
        "targets": projected_targets,
    }
    return relationship, required_targets


@dataclass(frozen=True, slots=True)
class ForeignEgressCapability:
    observation_digest: str
    path_digest: str
    catalog_digest: str
    observed_at: str
    fresh_until: str
    freshness_window_seconds: int
    relationship: dict[str, Any]
    required_targets: tuple[str, ...]
    capability_digest: str

    @classmethod
    def from_surfpath(
        cls,
        *,
        observation: dict[str, Any],
        status: dict[str, Any],
        path_digest: str,
    ) -> ForeignEgressCapability:
        observation_digest = _verify_surfpath_observation(observation)
        freshness_window = _freshness_from_status(status, observation_digest)
        candidate = _selected_candidate(observation, path_digest)
        relationship, required_targets = _project_relationship(observation, candidate)
        observed_at = _parse_time(str(observation["observedAt"]))
        fresh_until = observed_at + dt.timedelta(seconds=freshness_window)
        catalog_digest = _require_digest(observation.get("catalogDigest", ""), "catalogDigest")
        path_digest = _require_digest(path_digest, "pathDigest")
        partial = cls._document(
            observation_digest=observation_digest,
            path_digest=path_digest,
            catalog_digest=catalog_digest,
            observed_at=_format_time(observed_at),
            fresh_until=_format_time(fresh_until),
            freshness_window_seconds=freshness_window,
            relationship=relationship,
            required_targets=required_targets,
            capability_digest=None,
        )
        return cls(
            observation_digest=observation_digest,
            path_digest=path_digest,
            catalog_digest=catalog_digest,
            observed_at=_format_time(observed_at),
            fresh_until=_format_time(fresh_until),
            freshness_window_seconds=freshness_window,
            relationship=relationship,
            required_targets=required_targets,
            capability_digest=sha256_digest(partial),
        )

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ForeignEgressCapability:
        validate_contract("foreign-egress-capability", value)
        owner = value["owner"]
        instance = cls(
            observation_digest=str(owner["observationDigest"]),
            path_digest=str(owner["pathDigest"]),
            catalog_digest=str(owner["catalogDigest"]),
            observed_at=str(value["observedAt"]),
            fresh_until=str(value["freshUntil"]),
            freshness_window_seconds=int(owner["freshnessWindowSeconds"]),
            relationship=dict(value["relationship"]),
            required_targets=tuple(str(item) for item in value["requiredTargets"]),
            capability_digest=str(value["capabilityDigest"]),
        )
        expected = sha256_digest(
            cls._document(
                observation_digest=instance.observation_digest,
                path_digest=instance.path_digest,
                catalog_digest=instance.catalog_digest,
                observed_at=instance.observed_at,
                fresh_until=instance.fresh_until,
                freshness_window_seconds=instance.freshness_window_seconds,
                relationship=instance.relationship,
                required_targets=instance.required_targets,
                capability_digest=None,
            )
        )
        if instance.capability_digest != expected:
            raise ForeignEgressProjectionError(
                "foreign egress capability digest does not match its projection"
            )
        return instance

    @staticmethod
    def _document(
        *,
        observation_digest: str,
        path_digest: str,
        catalog_digest: str,
        observed_at: str,
        fresh_until: str,
        freshness_window_seconds: int,
        relationship: dict[str, Any],
        required_targets: tuple[str, ...],
        capability_digest: str | None,
    ) -> dict[str, Any]:
        value: dict[str, Any] = {
            "schemaVersion": 1,
            "kind": "ordivon.world.foreign-egress-capability",
            "truthRole": "owner-observed-capability-projection",
            "capabilityType": "foreign-egress",
            "owner": {
                "authority": _WORKSTATION_AUTHORITY,
                "observationKind": _SURFPATH_OBSERVATION_KIND,
                "observationDigest": observation_digest,
                "pathDigest": path_digest,
                "catalogDigest": catalog_digest,
                "freshnessWindowSeconds": freshness_window_seconds,
            },
            "observedAt": observed_at,
            "freshUntil": fresh_until,
            "relationship": relationship,
            "requiredTargets": list(required_targets),
            "activationAuthority": _WORKSTATION_AUTHORITY,
            "requiresOwnerRevalidation": True,
        }
        if capability_digest is not None:
            value["capabilityDigest"] = capability_digest
        return value

    def to_dict(self) -> dict[str, Any]:
        value = self._document(
            observation_digest=self.observation_digest,
            path_digest=self.path_digest,
            catalog_digest=self.catalog_digest,
            observed_at=self.observed_at,
            fresh_until=self.fresh_until,
            freshness_window_seconds=self.freshness_window_seconds,
            relationship=self.relationship,
            required_targets=self.required_targets,
            capability_digest=self.capability_digest,
        )
        validate_contract("foreign-egress-capability", value)
        return value

    def is_reference_fresh(self, at: dt.datetime) -> bool:
        if at.tzinfo is None:
            raise ForeignEgressProjectionError("freshness check time must include a timezone")
        return at.astimezone(dt.timezone.utc) <= _parse_time(self.fresh_until)

    def require_reference_fresh(self, at: dt.datetime) -> None:
        if not self.is_reference_fresh(at):
            raise ForeignEgressCapabilityStale(
                f"foreign egress capability reference expired at {self.fresh_until}; "
                "request a fresh Workstation observation before effect"
            )

    def handoff_reference(self) -> dict[str, Any]:
        value = {
            "schemaVersion": 1,
            "kind": "ordivon.world.foreign-egress-capability-reference",
            "capabilityDigest": self.capability_digest,
            "observationDigest": self.observation_digest,
            "pathDigest": self.path_digest,
            "freshUntil": self.fresh_until,
            "activationAuthority": _WORKSTATION_AUTHORITY,
            "requiresOwnerRevalidation": True,
        }
        validate_contract("foreign-egress-capability-reference", value)
        return value
