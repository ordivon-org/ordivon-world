from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ._host_trajectory import _HostTrajectoryJournal, _PayloadSlot
from .canonical import sha256_digest

_PLAN_KIND = "world-entity-migration-plan"
_DEPARTURE_KIND = "world-entity-source-departure"
_CONTINUITY_KIND = "world-entity-continuity-payload"
_RECEIPT_KIND = "world-entity-destination-receipt"
_UNCERTAINTY_KIND = "world-entity-migration-uncertainty"


class EntityMigrationError(RuntimeError):
    pass


class EntityMigrationSuperseded(EntityMigrationError):
    pass


@dataclass(frozen=True, slots=True)
class PreparedEntityMigration:
    """One exact entity-continuity intent between two World instances.

    The plan binds identity and portable continuity material. It deliberately
    does not model destination-local Presence, position, capability, authority,
    inventory or lifecycle state.
    """

    migration_id: str
    entity_id: str
    source_world_id: str
    destination_world_id: str
    source_departure_digest: str
    continuity_payload_digest: str

    def __post_init__(self) -> None:
        if not self.migration_id.startswith("migration:"):
            raise ValueError("Entity migration identity must start with migration:")
        for label, value in (
            ("entity identity", self.entity_id),
            ("source World identity", self.source_world_id),
            ("destination World identity", self.destination_world_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        for label, value in (
            ("source departure digest", self.source_departure_digest),
            ("continuity payload digest", self.continuity_payload_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.prepared-entity-migration",
            "migrationId": self.migration_id,
            "entityId": self.entity_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "sourceDepartureDigest": self.source_departure_digest,
            "continuityPayloadDigest": self.continuity_payload_digest,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PreparedEntityMigration:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.prepared-entity-migration"
        ):
            raise ValueError("Prepared entity migration schema is unsupported")
        return cls(
            migration_id=str(value["migrationId"]),
            entity_id=str(value["entityId"]),
            source_world_id=str(value["sourceWorldId"]),
            destination_world_id=str(value["destinationWorldId"]),
            source_departure_digest=str(value["sourceDepartureDigest"]),
            continuity_payload_digest=str(value["continuityPayloadDigest"]),
        )


@dataclass(frozen=True, slots=True)
class EntityMigrationBundle:
    plan: PreparedEntityMigration
    source_departure: Any
    continuity_payload: Any

    def __post_init__(self) -> None:
        if sha256_digest(self.source_departure) != self.plan.source_departure_digest:
            raise ValueError("Entity migration source departure digest mismatch")
        if sha256_digest(self.continuity_payload) != self.plan.continuity_payload_digest:
            raise ValueError("Entity migration continuity payload digest mismatch")

    @classmethod
    def create(
        cls,
        *,
        migration_id: str,
        entity_id: str,
        source_world_id: str,
        destination_world_id: str,
        source_departure: Any,
        continuity_payload: Any,
    ) -> EntityMigrationBundle:
        return cls(
            plan=PreparedEntityMigration(
                migration_id=migration_id,
                entity_id=entity_id,
                source_world_id=source_world_id,
                destination_world_id=destination_world_id,
                source_departure_digest=sha256_digest(source_departure),
                continuity_payload_digest=sha256_digest(continuity_payload),
            ),
            source_departure=source_departure,
            continuity_payload=continuity_payload,
        )


@dataclass(frozen=True, slots=True)
class EntityMigrationReceipt:
    migration_id: str
    plan_digest: str
    entity_id: str
    destination_world_id: str
    source_departure_digest: str
    materialization_id: str
    materialization_digest: str
    destination_evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.migration_id.startswith("migration:"):
            raise ValueError("Entity migration receipt identity must start with migration:")
        for label, value in (
            ("plan digest", self.plan_digest),
            ("source departure digest", self.source_departure_digest),
            ("materialization digest", self.materialization_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")
        for label, value in (
            ("entity identity", self.entity_id),
            ("destination World identity", self.destination_world_id),
            ("materialization identity", self.materialization_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        if not isinstance(self.destination_evidence, dict):
            raise ValueError("Entity migration destination evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-migration-receipt",
            "migrationId": self.migration_id,
            "planDigest": self.plan_digest,
            "entityId": self.entity_id,
            "destinationWorldId": self.destination_world_id,
            "sourceDepartureDigest": self.source_departure_digest,
            "materializationId": self.materialization_id,
            "materializationDigest": self.materialization_digest,
            "destinationEvidence": self.destination_evidence,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> EntityMigrationReceipt:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.entity-migration-receipt"
        ):
            raise ValueError("Entity migration receipt schema is unsupported")
        evidence = value.get("destinationEvidence")
        if not isinstance(evidence, dict):
            raise ValueError("Entity migration destination evidence must be an object")
        return cls(
            migration_id=str(value["migrationId"]),
            plan_digest=str(value["planDigest"]),
            entity_id=str(value["entityId"]),
            destination_world_id=str(value["destinationWorldId"]),
            source_departure_digest=str(value["sourceDepartureDigest"]),
            materialization_id=str(value["materializationId"]),
            materialization_digest=str(value["materializationDigest"]),
            destination_evidence=dict(evidence),
        )


class EntityMigrationOutcomeUnknown(EntityMigrationError):
    def __init__(self, plan: PreparedEntityMigration, cause: BaseException) -> None:
        self.plan = plan
        self.cause = cause
        super().__init__(
            f"entity migration outcome is unknown for {plan.migration_id}; reconcile before rematerialization: {cause}"
        )


class EntityMigrationDestination(Protocol):
    def materialize(self, bundle: EntityMigrationBundle) -> EntityMigrationReceipt: ...

    def reconcile(self, plan: PreparedEntityMigration) -> EntityMigrationReceipt | None: ...


@dataclass(frozen=True, slots=True)
class HostEntityMigrationStep:
    task_id: str
    task_revision: int
    migration_id: str
    status: str
    receipt: EntityMigrationReceipt | None = None
    reconciled: bool = False


class HostEntityMigrationJournal(_HostTrajectoryJournal):
    """Durable entity migration journal backed by Host's opaque extension port."""

    label = "World entity migration"
    event_token = "world-entity"
    event_kind_prefix = "world.entity-migration"
    state_field = "worldEntityMigrationState"
    plan_digest_field = "worldEntityMigrationPlanDigest"
    plan_object_field = "worldEntityMigrationPlanObjectDigest"
    receipt_digest_field = "worldEntityMigrationReceiptDigest"
    receipt_object_field = "worldEntityMigrationReceiptObjectDigest"
    uncertainty_object_field = "worldEntityMigrationUncertaintyObjectDigest"
    plan_kind = _PLAN_KIND
    receipt_kind = _RECEIPT_KIND
    uncertainty_kind = _UNCERTAINTY_KIND
    uncertainty_value_kind = "ordivon.world.entity-migration-uncertainty"
    uncertainty_identity_field = "migrationId"
    uncertainty_next_action = "reconcile-original-migration"
    plan_identity_attr = "migration_id"
    step_identity_field = "migration_id"
    plan_type = PreparedEntityMigration
    bundle_type = EntityMigrationBundle
    receipt_type = EntityMigrationReceipt
    step_type = HostEntityMigrationStep
    outcome_unknown_type = EntityMigrationOutcomeUnknown
    error_type = EntityMigrationError
    superseded_type = EntityMigrationSuperseded
    slots = (
        _PayloadSlot(
            "worldEntitySourceDepartureDigest",
            "worldEntitySourceDepartureObjectDigest",
            _DEPARTURE_KIND,
            "source_departure",
            "source_departure_digest",
        ),
        _PayloadSlot(
            "worldEntityContinuityPayloadDigest",
            "worldEntityContinuityPayloadObjectDigest",
            _CONTINUITY_KIND,
            "continuity_payload",
            "continuity_payload_digest",
        ),
    )
    correlation_fields = (
        ("worldEntityMigrationId", "migration_id"),
        ("worldEntityId", "entity_id"),
    )
    receipt_bindings = (
        ("migration identity", "migration_id", "migration_id"),
        ("plan identity", "plan_digest", "digest"),
        ("entity identity", "entity_id", "entity_id"),
        ("destination World", "destination_world_id", "destination_world_id"),
        ("source departure identity", "source_departure_digest", "source_departure_digest"),
    )
    terminal_state = "materialized"
    terminal_fields = (
        ("worldEntityMaterializationId", "materialization_id"),
        ("worldEntityMaterializationDigest", "materialization_digest"),
    )

    def materialize(
        self,
        task_id: str,
        destination: EntityMigrationDestination,
    ) -> HostEntityMigrationStep:
        return self.execute(task_id, destination.materialize)

    def reconcile(
        self,
        task_id: str,
        destination: EntityMigrationDestination,
    ) -> HostEntityMigrationStep:
        return super().reconcile(task_id, destination.reconcile)
