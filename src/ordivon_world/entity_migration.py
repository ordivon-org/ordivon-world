from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ordivon_host import EventKind

from ._host_trajectory import _HostTrajectoryJournal, _PayloadSlot
from .canonical import sha256_digest

_PLAN_KIND = "world-entity-migration-plan"
_DEPARTURE_KIND = "world-entity-source-departure"
_CONTINUITY_KIND = "world-entity-continuity-payload"
_RECEIPT_KIND = "world-entity-destination-receipt"
_UNCERTAINTY_KIND = "world-entity-migration-uncertainty"
_NOT_COMMITTED_KIND = "world-entity-migration-not-committed"


class EntityMigrationError(RuntimeError):
    pass


class EntityMigrationSuperseded(EntityMigrationError):
    pass


@dataclass(frozen=True, slots=True)
class EntityDepartureAuthority:
    authority_id: str
    mechanism: str
    evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.authority_id or not self.mechanism:
            raise ValueError("Entity Departure authority identity and mechanism must be non-empty")
        if not isinstance(self.evidence, dict):
            raise ValueError("Entity Departure authority evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "authorityId": self.authority_id,
            "mechanism": self.mechanism,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> EntityDepartureAuthority:
        evidence = value.get("evidence")
        if not isinstance(evidence, dict):
            raise ValueError("Entity Departure authority evidence must be an object")
        return cls(
            authority_id=str(value["authorityId"]),
            mechanism=str(value["mechanism"]),
            evidence=dict(evidence),
        )


@dataclass(frozen=True, slots=True)
class EntityDepartureReceipt:
    migration_id: str
    entity_id: str
    source_world_id: str
    destination_world_id: str
    source_occurrence_id: str
    source_occurrence_digest: str
    authority: EntityDepartureAuthority

    def __post_init__(self) -> None:
        if not self.migration_id.startswith("migration:"):
            raise ValueError("Entity Departure migration identity must start with migration:")
        for label, value in (
            ("entity identity", self.entity_id),
            ("source World identity", self.source_world_id),
            ("destination World identity", self.destination_world_id),
            ("source occurrence identity", self.source_occurrence_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        if (
            not isinstance(self.source_occurrence_digest, str)
            or not self.source_occurrence_digest.startswith("sha256:")
            or len(self.source_occurrence_digest) != 71
        ):
            raise ValueError("Entity Departure source occurrence digest must be a sha256: digest")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-departure-receipt",
            "migrationId": self.migration_id,
            "entityId": self.entity_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "sourceOccurrenceId": self.source_occurrence_id,
            "sourceOccurrenceDigest": self.source_occurrence_digest,
            "authority": self.authority.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> EntityDepartureReceipt:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.entity-departure-receipt"
        ):
            raise ValueError("Entity Departure receipt schema is unsupported")
        authority = value.get("authority")
        if not isinstance(authority, dict):
            raise ValueError("Entity Departure authority is missing")
        return cls(
            migration_id=str(value["migrationId"]),
            entity_id=str(value["entityId"]),
            source_world_id=str(value["sourceWorldId"]),
            destination_world_id=str(value["destinationWorldId"]),
            source_occurrence_id=str(value["sourceOccurrenceId"]),
            source_occurrence_digest=str(value["sourceOccurrenceDigest"]),
            authority=EntityDepartureAuthority.from_dict(authority),
        )


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
        """Legacy/untyped constructor retained for recovery of W1 durable state."""
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

    @classmethod
    def create_departed(
        cls,
        *,
        source_departure: EntityDepartureReceipt,
        continuity_payload: Any,
    ) -> EntityMigrationBundle:
        departure_value = source_departure.to_dict()
        return cls(
            plan=PreparedEntityMigration(
                migration_id=source_departure.migration_id,
                entity_id=source_departure.entity_id,
                source_world_id=source_departure.source_world_id,
                destination_world_id=source_departure.destination_world_id,
                source_departure_digest=source_departure.digest,
                continuity_payload_digest=sha256_digest(continuity_payload),
            ),
            source_departure=departure_value,
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


@dataclass(frozen=True, slots=True)
class EntityMigrationNotCommitted:
    migration_id: str
    plan_digest: str
    entity_id: str
    destination_world_id: str
    source_departure_digest: str
    continuity_payload_digest: str
    evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.migration_id.startswith("migration:"):
            raise ValueError("Entity not-committed identity must start with migration:")
        for label, value in (
            ("plan digest", self.plan_digest),
            ("source departure digest", self.source_departure_digest),
            ("continuity payload digest", self.continuity_payload_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")
        if not self.entity_id or not self.destination_world_id:
            raise ValueError("Entity not-committed identities must be non-empty")
        if not isinstance(self.evidence, dict):
            raise ValueError("Entity not-committed evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-migration-not-committed",
            "migrationId": self.migration_id,
            "planDigest": self.plan_digest,
            "entityId": self.entity_id,
            "destinationWorldId": self.destination_world_id,
            "sourceDepartureDigest": self.source_departure_digest,
            "continuityPayloadDigest": self.continuity_payload_digest,
            "evidence": self.evidence,
        }


class EntityMigrationOutcomeUnknown(EntityMigrationError):
    def __init__(self, plan: PreparedEntityMigration, cause: BaseException) -> None:
        self.plan = plan
        self.cause = cause
        super().__init__(
            f"entity migration outcome is unknown for {plan.migration_id}; reconcile before rematerialization: {cause}"
        )


class EntityMigrationDestination(Protocol):
    def materialize(self, bundle: EntityMigrationBundle) -> EntityMigrationReceipt: ...

    def reconcile(
        self, plan: PreparedEntityMigration
    ) -> EntityMigrationReceipt | EntityMigrationNotCommitted | None: ...


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
    extra_instance_fields = (
        "worldEntityMigrationNotCommittedDigest",
        "worldEntityMigrationNotCommittedObjectDigest",
    )
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
        bundle = self.load_bundle(task_id)
        plan = bundle.plan
        current = self.port.load_namespace(task_id, "world")
        retained = self._load_receipt_from_data(current.data, plan)
        if retained is not None:
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                self.terminal_state,
                retained,
                True,
            )
        result = destination.reconcile(plan)
        if isinstance(result, EntityMigrationNotCommitted):
            return self.record_not_committed(task_id, plan, result)
        if result is None:
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                "unknown",
                None,
                True,
            )
        return self.record_receipt(task_id, plan, result, reconciled=True)

    def record_not_committed(
        self,
        task_id: str,
        plan: PreparedEntityMigration,
        proof: EntityMigrationNotCommitted,
    ) -> HostEntityMigrationStep:
        self._validate_not_committed(plan, proof)
        current = self.port.load_namespace(task_id, "world")
        self._require_current(current.data, plan)
        retained = self._load_receipt_from_data(current.data, plan)
        if retained is not None:
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                self.terminal_state,
                retained,
                True,
            )
        entry = self._entry(current.data, plan)
        if entry.get(self.state_field) == "prepared":
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                "prepared",
                None,
                True,
            )
        if entry.get(self.state_field) != "unknown":
            raise EntityMigrationError(
                "not-committed proof can only release an unknown Entity Migration"
            )
        proof_value = proof.to_dict()
        proof_digest = sha256_digest(proof_value)
        proof_object = self.port.put_object(proof_value, kind=_NOT_COMMITTED_KIND)
        updates, remove_fields = self._mutation(
            current.data,
            plan,
            {
                self.state_field: "prepared",
                "worldEntityMigrationNotCommittedDigest": proof_digest,
                "worldEntityMigrationNotCommittedObjectDigest": proof_object.digest,
            },
            remove_fields=(self.uncertainty_object_field,),
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, "not-committed", current.projection.revision + 1),
            kind=EventKind("world.entity-migration-not-committed"),
            updates=updates,
            remove_fields=remove_fields,
            referenced_objects=(*self._retained_objects(current.data, plan), proof_object),
            label=self.label,
        )
        return self._step(
            task_id,
            committed.projection.revision,
            plan,
            "prepared",
            None,
            True,
        )

    @staticmethod
    def _validate_not_committed(
        plan: PreparedEntityMigration,
        proof: EntityMigrationNotCommitted,
    ) -> None:
        if proof.migration_id != plan.migration_id:
            raise EntityMigrationSuperseded(
                "not-committed proof belongs to another Entity Migration"
            )
        if proof.plan_digest != plan.digest:
            raise EntityMigrationSuperseded(
                "not-committed proof binds another Entity Migration plan"
            )
        if proof.entity_id != plan.entity_id:
            raise EntityMigrationSuperseded("not-committed proof belongs to another Entity")
        if proof.destination_world_id != plan.destination_world_id:
            raise EntityMigrationSuperseded(
                "not-committed proof belongs to another destination World"
            )
        if proof.source_departure_digest != plan.source_departure_digest:
            raise EntityMigrationSuperseded("not-committed proof binds another source departure")
        if proof.continuity_payload_digest != plan.continuity_payload_digest:
            raise EntityMigrationSuperseded("not-committed proof binds another continuity payload")
        if proof.evidence.get("exactOriginalRetrySafe") is not True:
            raise EntityMigrationError(
                "not-committed evidence does not authorize exact original retry"
            )
        if proof.evidence.get("nativeSubstrateChecked") is not True:
            raise EntityMigrationError(
                "not-committed evidence did not check destination native materialization"
            )
