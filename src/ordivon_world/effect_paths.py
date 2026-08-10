from __future__ import annotations

import copy
from dataclasses import dataclass
import datetime as dt
from typing import Any

from .canonical import sha256_digest
from .foreign_egress import ForeignEgressCapability
from .schemas import validate_contract


class EffectPathProjectionError(ValueError):
    pass


def _parse_time(value: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise EffectPathProjectionError(f"invalid observation time: {value}") from error
    if parsed.tzinfo is None:
        raise EffectPathProjectionError("observation time must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _require_digest(value: Any, field: str) -> str:
    text = str(value)
    if len(text) != 71 or not text.startswith("sha256:"):
        raise EffectPathProjectionError(f"{field} must be a sha256 digest")
    try:
        int(text[7:], 16)
    except ValueError as error:
        raise EffectPathProjectionError(f"{field} must be a sha256 digest") from error
    return text


def _without_digest(value: dict[str, Any], field: str) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != field}


@dataclass(frozen=True, slots=True)
class EffectPathCandidate:
    source_kind: str
    effect_kind: str
    target: str
    owner_authority: str
    activation_authority: str
    request_control: str
    owner_observation_digest: str
    owner_observed_at: str
    owner_valid_until: str | None
    usability_evidence_digest: str
    usability_observed_at: str
    source_projection: dict[str, Any]
    candidate_digest: str

    @classmethod
    def from_foreign_egress_http_get(
        cls,
        capability: ForeignEgressCapability,
        *,
        target: str,
        effect_observed_at: str,
        effect_evidence_digest: str,
        http_status: int,
    ) -> EffectPathCandidate:
        value = capability.to_dict()
        targets = value["relationship"]["targets"]
        if not any(item.get("url") == target for item in targets):
            raise EffectPathProjectionError(
                "requested HTTP target is not present in the foreign-egress capability"
            )
        if http_status <= 0:
            raise EffectPathProjectionError("HTTP effect evidence has no completed status")
        effect_time = _parse_time(effect_observed_at)
        observed_time = _parse_time(capability.observed_at)
        fresh_until = _parse_time(capability.fresh_until)
        if effect_time < observed_time or effect_time > fresh_until:
            raise EffectPathProjectionError(
                "foreign-egress effect evidence was not observed inside the owner freshness window"
            )
        evidence_digest = _require_digest(effect_evidence_digest, "effectEvidenceDigest")
        source_projection = {
            "capability": value,
            "effectEvidence": {
                "observedAt": effect_observed_at,
                "evidenceDigest": evidence_digest,
                "httpStatus": http_status,
            },
        }
        return cls._create(
            source_kind="ordivon.world.foreign-egress-capability",
            effect_kind="http.get",
            target=target,
            owner_authority=str(value["owner"]["authority"]),
            activation_authority=str(value["activationAuthority"]),
            request_control="consumer-request-owner-revalidated",
            owner_observation_digest=str(value["owner"]["observationDigest"]),
            owner_observed_at=str(value["observedAt"]),
            owner_valid_until=str(value["freshUntil"]),
            usability_evidence_digest=evidence_digest,
            usability_observed_at=effect_observed_at,
            source_projection=source_projection,
        )

    @classmethod
    def from_cloudflare_fixed_http_get(
        cls,
        *,
        owner_observation: dict[str, Any],
        effect_observation: dict[str, Any],
    ) -> EffectPathCandidate:
        if owner_observation.get("kind") != "ordivon.world.wx3-cloudflare-owner-observation":
            raise EffectPathProjectionError("unexpected Cloudflare owner observation kind")
        observation_digest = _require_digest(
            owner_observation.get("observationDigest"), "observationDigest"
        )
        expected_observation_digest = sha256_digest(
            _without_digest(owner_observation, "observationDigest")
        )
        if observation_digest != expected_observation_digest:
            raise EffectPathProjectionError("Cloudflare owner observation digest mismatch")
        resources = owner_observation.get("resources")
        if not isinstance(resources, dict) or not all(
            isinstance(resources.get(name), dict) and resources[name].get("exists") is True
            for name in ("dns", "route", "worker")
        ):
            raise EffectPathProjectionError(
                "Cloudflare owner observation does not show all connector resources present"
            )
        identity = owner_observation.get("resourceIdentity")
        if not isinstance(identity, dict):
            raise EffectPathProjectionError("Cloudflare owner observation has no resource identity")
        route = resources["route"]
        if route.get("script") != identity.get("script"):
            raise EffectPathProjectionError("Cloudflare route is not bound to the observed Worker")
        host = str(identity.get("host", ""))
        pattern = str(route.get("pattern", ""))
        if not host or not pattern.startswith(host):
            raise EffectPathProjectionError("Cloudflare route is not bound to the observed host")

        if effect_observation.get("kind") != "ordivon.world.wx3-cloudflare-openai-observation":
            raise EffectPathProjectionError("unexpected Cloudflare effect observation kind")
        effect = effect_observation.get("effect")
        if not isinstance(effect, dict):
            raise EffectPathProjectionError("Cloudflare effect observation has no effect body")
        target = str(owner_observation.get("fixedTarget", ""))
        if (
            effect_observation.get("localHttpStatus") != 200
            or effect.get("kind") != "ordivon.world.request-scoped-openai-connector-effect"
            or effect.get("fixedUpstream") != target
            or effect.get("upstreamCompleted") is not True
            or not isinstance(effect.get("upstreamStatus"), int)
            or effect["upstreamStatus"] <= 0
        ):
            raise EffectPathProjectionError(
                "Cloudflare owner resources exist but no successful fixed-target effect is proven"
            )
        owner_time = _parse_time(str(owner_observation.get("observedAt", "")))
        effect_time_text = str(effect.get("observedAt", ""))
        effect_time = _parse_time(effect_time_text)
        if effect_time < owner_time:
            raise EffectPathProjectionError(
                "Cloudflare effect evidence predates its owner observation"
            )
        if effect_observation.get("host") != identity.get("host"):
            raise EffectPathProjectionError("Cloudflare effect host differs from owner observation")
        if effect_observation.get("script") != identity.get("script"):
            raise EffectPathProjectionError("Cloudflare effect Worker differs from owner observation")
        effect_digest = sha256_digest(effect_observation)
        source_projection = {
            "ownerObservation": copy.deepcopy(owner_observation),
            "effectObservation": copy.deepcopy(effect_observation),
        }
        authority = str(owner_observation.get("authority", ""))
        if not authority:
            raise EffectPathProjectionError("Cloudflare owner observation has no authority")
        return cls._create(
            source_kind="ordivon.world.cloudflare-fixed-target-connector-evidence",
            effect_kind="http.get",
            target=target,
            owner_authority=authority,
            activation_authority=authority,
            request_control="owner-fixed-request",
            owner_observation_digest=observation_digest,
            owner_observed_at=str(owner_observation["observedAt"]),
            owner_valid_until=None,
            usability_evidence_digest=effect_digest,
            usability_observed_at=effect_time_text,
            source_projection=source_projection,
        )

    @classmethod
    def _create(
        cls,
        *,
        source_kind: str,
        effect_kind: str,
        target: str,
        owner_authority: str,
        activation_authority: str,
        request_control: str,
        owner_observation_digest: str,
        owner_observed_at: str,
        owner_valid_until: str | None,
        usability_evidence_digest: str,
        usability_observed_at: str,
        source_projection: dict[str, Any],
    ) -> EffectPathCandidate:
        partial = cls._document(
            source_kind=source_kind,
            effect_kind=effect_kind,
            target=target,
            owner_authority=owner_authority,
            activation_authority=activation_authority,
            request_control=request_control,
            owner_observation_digest=owner_observation_digest,
            owner_observed_at=owner_observed_at,
            owner_valid_until=owner_valid_until,
            usability_evidence_digest=usability_evidence_digest,
            usability_observed_at=usability_observed_at,
            source_projection=source_projection,
            candidate_digest=None,
        )
        return cls(
            source_kind=source_kind,
            effect_kind=effect_kind,
            target=target,
            owner_authority=owner_authority,
            activation_authority=activation_authority,
            request_control=request_control,
            owner_observation_digest=owner_observation_digest,
            owner_observed_at=owner_observed_at,
            owner_valid_until=owner_valid_until,
            usability_evidence_digest=usability_evidence_digest,
            usability_observed_at=usability_observed_at,
            source_projection=copy.deepcopy(source_projection),
            candidate_digest=sha256_digest(partial),
        )

    @staticmethod
    def _document(
        *,
        source_kind: str,
        effect_kind: str,
        target: str,
        owner_authority: str,
        activation_authority: str,
        request_control: str,
        owner_observation_digest: str,
        owner_observed_at: str,
        owner_valid_until: str | None,
        usability_evidence_digest: str,
        usability_observed_at: str,
        source_projection: dict[str, Any],
        candidate_digest: str | None,
    ) -> dict[str, Any]:
        value: dict[str, Any] = {
            "sourceKind": source_kind,
            "effect": {"kind": effect_kind, "target": target},
            "ownerAuthority": owner_authority,
            "activationAuthority": activation_authority,
            "requestControl": request_control,
            "ownerObservation": {
                "digest": owner_observation_digest,
                "observedAt": owner_observed_at,
                "validUntil": owner_valid_until,
            },
            "usabilityEvidence": {
                "digest": usability_evidence_digest,
                "observedAt": usability_observed_at,
                "result": "succeeded",
            },
            "currentActionAuthority": False,
            "requiresOwnerRevalidation": True,
            "sourceProjection": copy.deepcopy(source_projection),
        }
        if candidate_digest is not None:
            value["candidateDigest"] = candidate_digest
        return value

    def _require_digest_current(self) -> None:
        expected = sha256_digest(
            self._document(
                source_kind=self.source_kind,
                effect_kind=self.effect_kind,
                target=self.target,
                owner_authority=self.owner_authority,
                activation_authority=self.activation_authority,
                request_control=self.request_control,
                owner_observation_digest=self.owner_observation_digest,
                owner_observed_at=self.owner_observed_at,
                owner_valid_until=self.owner_valid_until,
                usability_evidence_digest=self.usability_evidence_digest,
                usability_observed_at=self.usability_observed_at,
                source_projection=self.source_projection,
                candidate_digest=None,
            )
        )
        if expected != self.candidate_digest:
            raise EffectPathProjectionError(
                "effect-path candidate digest does not match its current projection"
            )

    def to_dict(self) -> dict[str, Any]:
        self._require_digest_current()
        return self._document(
            source_kind=self.source_kind,
            effect_kind=self.effect_kind,
            target=self.target,
            owner_authority=self.owner_authority,
            activation_authority=self.activation_authority,
            request_control=self.request_control,
            owner_observation_digest=self.owner_observation_digest,
            owner_observed_at=self.owner_observed_at,
            owner_valid_until=self.owner_valid_until,
            usability_evidence_digest=self.usability_evidence_digest,
            usability_observed_at=self.usability_observed_at,
            source_projection=self.source_projection,
            candidate_digest=self.candidate_digest,
        )


@dataclass(frozen=True, slots=True)
class EffectPathQuery:
    effect_kind: str
    target: str
    candidates: tuple[EffectPathCandidate, ...]
    query_digest: str

    @classmethod
    def for_http_get(
        cls,
        *,
        target: str,
        candidates: tuple[EffectPathCandidate, ...],
    ) -> EffectPathQuery:
        if not candidates:
            raise EffectPathProjectionError("effect-path query requires at least one candidate")
        digests: set[str] = set()
        for candidate in candidates:
            candidate._require_digest_current()
            if candidate.effect_kind != "http.get" or candidate.target != target:
                raise EffectPathProjectionError(
                    "effect-path candidate does not match the requested HTTP GET"
                )
            if candidate.candidate_digest in digests:
                raise EffectPathProjectionError("duplicate effect-path candidate")
            digests.add(candidate.candidate_digest)
        ordered = tuple(sorted(candidates, key=lambda item: item.candidate_digest))
        partial = cls._document(
            effect_kind="http.get",
            target=target,
            candidates=ordered,
            query_digest=None,
        )
        return cls(
            effect_kind="http.get",
            target=target,
            candidates=ordered,
            query_digest=sha256_digest(partial),
        )

    @staticmethod
    def _document(
        *,
        effect_kind: str,
        target: str,
        candidates: tuple[EffectPathCandidate, ...],
        query_digest: str | None,
    ) -> dict[str, Any]:
        value: dict[str, Any] = {
            "schemaVersion": 1,
            "kind": "ordivon.world.effect-path-query",
            "truthRole": "informational-agent-choice-projection",
            "effect": {"kind": effect_kind, "target": target},
            "selectionAuthority": "agent",
            "candidates": [candidate.to_dict() for candidate in candidates],
            "constraints": [
                "query-does-not-rank-or-select",
                "query-does-not-grant-action-authority",
                "candidate-success-evidence-is-historical-until-owner-revalidated",
            ],
        }
        if query_digest is not None:
            value["queryDigest"] = query_digest
        return value

    def to_dict(self) -> dict[str, Any]:
        expected = sha256_digest(
            self._document(
                effect_kind=self.effect_kind,
                target=self.target,
                candidates=self.candidates,
                query_digest=None,
            )
        )
        if expected != self.query_digest:
            raise EffectPathProjectionError(
                "effect-path query digest does not match its current projection"
            )
        value = self._document(
            effect_kind=self.effect_kind,
            target=self.target,
            candidates=self.candidates,
            query_digest=self.query_digest,
        )
        validate_contract("effect-path-query", value)
        return value

    def require_candidate(self, candidate_digest: str) -> EffectPathCandidate:
        matches = [
            candidate
            for candidate in self.candidates
            if candidate.candidate_digest == candidate_digest
        ]
        if len(matches) != 1:
            raise EffectPathProjectionError(
                "Agent must select one exact candidateDigest from the current query"
            )
        return matches[0]
