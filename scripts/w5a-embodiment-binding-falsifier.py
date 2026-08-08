#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from ordivon_world.canonical import sha256_digest
from ordivon_world.entity_migration import EntityDepartureReceipt, EntityMigrationBundle
from ordivon_world.entity_wire import EntityMigrationWireDestination
from ordivon_world.schemas import validate_contract


class ExperimentalEmbodimentBindingError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ExperimentalContinuitySubjectReceipt:
    """W5-A fixture receipt from the owner of one continuity subject.

    This is deliberately NOT a production World contract. World does not mint or
    interpret subject identity. The fixture models a separate authority stating
    that one exact continuity payload belongs to one opaque subject and is bound
    to one exact source departure trajectory.
    """

    subject_ref: str
    migration_id: str
    entity_id: str
    source_world_id: str
    destination_world_id: str
    source_departure_digest: str
    continuity_payload_digest: str
    authority_id: str
    mechanism: str
    evidence: dict[str, Any]

    def __post_init__(self) -> None:
        for label, value in (
            ("continuity subject reference", self.subject_ref),
            ("migration identity", self.migration_id),
            ("entity identity", self.entity_id),
            ("source World identity", self.source_world_id),
            ("destination World identity", self.destination_world_id),
            ("authority identity", self.authority_id),
            ("authority mechanism", self.mechanism),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ExperimentalEmbodimentBindingError(f"{label} must be non-empty")
        for label, value in (
            ("source departure digest", self.source_departure_digest),
            ("continuity payload digest", self.continuity_payload_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ExperimentalEmbodimentBindingError(f"{label} must be sha256:<64 hex>")
        if not isinstance(self.evidence, dict):
            raise ExperimentalEmbodimentBindingError("continuity authority evidence must be an object")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.w5a-experimental-continuity-subject-receipt",
            "subjectRef": self.subject_ref,
            "migrationId": self.migration_id,
            "entityId": self.entity_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "sourceDepartureDigest": self.source_departure_digest,
            "continuityPayloadDigest": self.continuity_payload_digest,
            "authority": {
                "authorityId": self.authority_id,
                "mechanism": self.mechanism,
                "evidence": self.evidence,
            },
        }


def bind_candidate(
    *,
    departure: EntityDepartureReceipt,
    continuity_payload: Any,
    subject_receipt: ExperimentalContinuitySubjectReceipt,
) -> EntityMigrationBundle:
    """Bind two owner-specific receipts without making World an identity authority."""

    expected = {
        "migration identity": (subject_receipt.migration_id, departure.migration_id),
        "entity identity": (subject_receipt.entity_id, departure.entity_id),
        "source World": (subject_receipt.source_world_id, departure.source_world_id),
        "destination World": (
            subject_receipt.destination_world_id,
            departure.destination_world_id,
        ),
        "source departure": (
            subject_receipt.source_departure_digest,
            departure.digest,
        ),
        "continuity payload": (
            subject_receipt.continuity_payload_digest,
            sha256_digest(continuity_payload),
        ),
    }
    for label, (observed, wanted) in expected.items():
        if observed != wanted:
            raise ExperimentalEmbodimentBindingError(
                f"continuity subject receipt {label} differs from owner-bound trajectory"
            )
    return EntityMigrationBundle.create_departed(
        source_departure=departure,
        continuity_payload=continuity_payload,
    )


def published_request(bundle: EntityMigrationBundle) -> dict[str, Any]:
    request = {
        "schemaVersion": 1,
        "kind": "ordivon.world.entity-migration-destination-request",
        "operation": "materialize",
        "plan": bundle.plan.to_dict(),
        "planDigest": bundle.plan.digest,
        "sourceDeparture": bundle.source_departure,
        "continuityPayload": bundle.continuity_payload,
    }
    validate_contract("entity-migration-destination-request", request)
    EntityMigrationWireDestination._require_source_departure(bundle)
    return request


def _expect_rejected(label: str, operation) -> dict[str, Any]:
    try:
        operation()
    except ExperimentalEmbodimentBindingError as error:
        return {"case": label, "rejected": True, "reason": str(error)}
    raise RuntimeError(f"W5-A negative case unexpectedly passed: {label}")


def run(
    departure_path: Path,
    *,
    game_revision: str | None = None,
    world_revision: str | None = None,
) -> dict[str, Any]:
    raw = json.loads(departure_path.read_text(encoding="utf-8"))
    departure_value = raw.get("receipt", raw)
    if not isinstance(departure_value, dict):
        raise RuntimeError("departure input must contain an Entity Departure receipt")
    validate_contract("entity-departure-receipt", departure_value)
    departure = EntityDepartureReceipt.from_dict(departure_value)

    alpha_payload = {
        "schemaVersion": 1,
        "kind": "ordivon.agent-continuity-envelope",
        "entityId": departure.entity_id,
        "identityRef": "agent-identity:alpha",
        "cognitionRef": "agent-context:alpha",
        "sourceLocalAuthorityCopied": False,
    }
    mallory_payload = {
        "schemaVersion": 1,
        "kind": "ordivon.agent-continuity-envelope",
        "entityId": departure.entity_id,
        "identityRef": "agent-identity:mallory",
        "cognitionRef": "agent-context:mallory",
        "sourceLocalAuthorityCopied": False,
    }

    # Baseline falsifier: current production contracts accept either opaque payload
    # with the same genuine source departure. Integrity exists, ownership does not.
    baseline_alpha = EntityMigrationBundle.create_departed(
        source_departure=departure,
        continuity_payload=alpha_payload,
    )
    baseline_mallory = EntityMigrationBundle.create_departed(
        source_departure=departure,
        continuity_payload=mallory_payload,
    )
    published_request(baseline_alpha)
    published_request(baseline_mallory)

    subject = ExperimentalContinuitySubjectReceipt(
        subject_ref="continuity-subject:alpha",
        migration_id=departure.migration_id,
        entity_id=departure.entity_id,
        source_world_id=departure.source_world_id,
        destination_world_id=departure.destination_world_id,
        source_departure_digest=departure.digest,
        continuity_payload_digest=sha256_digest(alpha_payload),
        authority_id="continuity-owner:w5a-fixture:alpha",
        mechanism="w5a-fixture-continuity-owner.v1",
        evidence={
            "subjectIdentityOwnedOutsideWorld": True,
            "continuitySemanticsOwnedOutsideWorld": True,
            "worldAuthorityTranslation": False,
        },
    )
    bound = bind_candidate(
        departure=departure,
        continuity_payload=alpha_payload,
        subject_receipt=subject,
    )
    published_request(bound)

    wrong_destination = ExperimentalContinuitySubjectReceipt(
        subject_ref=subject.subject_ref,
        migration_id=subject.migration_id,
        entity_id=subject.entity_id,
        source_world_id=subject.source_world_id,
        destination_world_id="security-world:w5a:other",
        source_departure_digest=subject.source_departure_digest,
        continuity_payload_digest=subject.continuity_payload_digest,
        authority_id=subject.authority_id,
        mechanism=subject.mechanism,
        evidence=subject.evidence,
    )
    wrong_entity = ExperimentalContinuitySubjectReceipt(
        subject_ref=subject.subject_ref,
        migration_id=subject.migration_id,
        entity_id="another-entity",
        source_world_id=subject.source_world_id,
        destination_world_id=subject.destination_world_id,
        source_departure_digest=subject.source_departure_digest,
        continuity_payload_digest=subject.continuity_payload_digest,
        authority_id=subject.authority_id,
        mechanism=subject.mechanism,
        evidence=subject.evidence,
    )

    negative = [
        _expect_rejected(
            "payload-substitution",
            lambda: bind_candidate(
                departure=departure,
                continuity_payload=mallory_payload,
                subject_receipt=subject,
            ),
        ),
        _expect_rejected(
            "destination-substitution",
            lambda: bind_candidate(
                departure=departure,
                continuity_payload=alpha_payload,
                subject_receipt=wrong_destination,
            ),
        ),
        _expect_rejected(
            "entity-substitution",
            lambda: bind_candidate(
                departure=departure,
                continuity_payload=alpha_payload,
                subject_receipt=wrong_entity,
            ),
        ),
    ]

    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5a-embodiment-binding-falsifier",
        "status": "passed",
        "revisions": {
            "game": game_revision,
            "world": world_revision,
        },
        "source": {
            "migrationId": departure.migration_id,
            "entityId": departure.entity_id,
            "sourceWorldId": departure.source_world_id,
            "destinationWorldId": departure.destination_world_id,
            "sourceDepartureDigest": departure.digest,
            "sourceAuthorityId": departure.authority.authority_id,
            "sourceAuthorityMechanism": departure.authority.mechanism,
        },
        "baseline": {
            "sameRealDepartureAcceptedWithConflictingContinuity": True,
            "sameMigrationId": baseline_alpha.plan.migration_id
            == baseline_mallory.plan.migration_id,
            "sameEntityId": baseline_alpha.plan.entity_id == baseline_mallory.plan.entity_id,
            "sameSourceDepartureDigest": baseline_alpha.plan.source_departure_digest
            == baseline_mallory.plan.source_departure_digest,
            "differentContinuityPayloadDigest": baseline_alpha.plan.continuity_payload_digest
            != baseline_mallory.plan.continuity_payload_digest,
            "sourceDepartureBindsContinuityPayload": False,
            "sourceDepartureBindsContinuitySubject": False,
        },
        "candidate": {
            "subjectRef": subject.subject_ref,
            "subjectReceiptDigest": subject.digest,
            "boundPlanDigest": bound.plan.digest,
            "worldMintsSubjectIdentity": False,
            "worldInterpretsContinuitySemantics": False,
            "worldTranslatesAuthority": False,
            "negativeCases": negative,
        },
        "disposition": {
            "carrierMaterializationIsEmbodiment": False,
            "continuityIntegrityIsContinuityOwnership": False,
            "twoOwnerBindingRemovesPayloadSubstitution": True,
            "activeEmbodimentStillUnproven": True,
            "currentPresenceStillUnproven": True,
            "productionContractPromotion": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="W5-A Agent embodiment ownership falsifier")
    parser.add_argument("--departure", type=Path, required=True)
    parser.add_argument("--game-revision")
    parser.add_argument("--world-revision")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(
        args.departure,
        game_revision=args.game_revision,
        world_revision=args.world_revision,
    )
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
