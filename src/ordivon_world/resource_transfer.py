from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ordivon_host import EventKind

from ._host_trajectory import _HostTrajectoryJournal, _PayloadSlot
from .canonical import sha256_digest
from .resource_egress import ResourceEgressReceipt

_PLAN_KIND = "world-resource-transfer-plan"
_SOURCE_EGRESS_KIND = "world-resource-source-egress"
_PAYLOAD_KIND = "world-resource-portable-payload"
_RECEIPT_KIND = "world-resource-destination-receipt"
_UNCERTAINTY_KIND = "world-resource-transfer-uncertainty"
_NOT_COMMITTED_KIND = "world-resource-transfer-not-committed"


class ResourceTransferError(RuntimeError):
    pass


class ResourceTransferSuperseded(ResourceTransferError):
    pass


@dataclass(frozen=True, slots=True)
class PreparedResourceTransfer:
    """One exact cross-World resource-transfer intent.

    The plan deliberately owns no source-domain or destination-domain state. It
    binds one source-World egress receipt and one portable payload retained in
    Host CAS to one destination World identity.
    """

    transfer_id: str
    source_world_id: str
    destination_world_id: str
    resource_kind: str
    source_egress_digest: str
    payload_digest: str

    def __post_init__(self) -> None:
        if not self.transfer_id.startswith("transfer:"):
            raise ValueError("Resource transfer identity must start with transfer:")
        for label, value in (
            ("source World identity", self.source_world_id),
            ("destination World identity", self.destination_world_id),
            ("resource kind", self.resource_kind),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        for label, value in (
            ("source egress digest", self.source_egress_digest),
            ("payload digest", self.payload_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.prepared-resource-transfer",
            "transferId": self.transfer_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "resourceKind": self.resource_kind,
            "sourceEgressDigest": self.source_egress_digest,
            "payloadDigest": self.payload_digest,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PreparedResourceTransfer:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.prepared-resource-transfer"
        ):
            raise ValueError("Prepared resource transfer schema is unsupported")
        return cls(
            transfer_id=str(value["transferId"]),
            source_world_id=str(value["sourceWorldId"]),
            destination_world_id=str(value["destinationWorldId"]),
            resource_kind=str(value["resourceKind"]),
            source_egress_digest=str(value["sourceEgressDigest"]),
            payload_digest=str(value["payloadDigest"]),
        )


@dataclass(frozen=True, slots=True)
class ResourceTransferBundle:
    plan: PreparedResourceTransfer
    source_egress: dict[str, Any]
    payload: Any

    def __post_init__(self) -> None:
        try:
            egress = ResourceEgressReceipt.from_dict(self.source_egress)
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Resource transfer source egress receipt is invalid") from error
        if egress.digest != self.plan.source_egress_digest:
            raise ValueError("Resource transfer source egress digest mismatch")
        if sha256_digest(self.payload) != self.plan.payload_digest:
            raise ValueError("Resource transfer payload digest mismatch")
        if (
            egress.transfer_id != self.plan.transfer_id
            or egress.source_world_id != self.plan.source_world_id
            or egress.destination_world_id != self.plan.destination_world_id
            or egress.resource_kind != self.plan.resource_kind
            or egress.payload_digest != self.plan.payload_digest
        ):
            raise ValueError(
                "Resource Egress receipt does not bind the exact Resource Transfer plan"
            )

    @property
    def egress_receipt(self) -> ResourceEgressReceipt:
        return ResourceEgressReceipt.from_dict(self.source_egress)

    @classmethod
    def create(
        cls,
        *,
        source_egress: ResourceEgressReceipt,
        payload: Any,
    ) -> ResourceTransferBundle:
        payload_digest = sha256_digest(payload)
        if source_egress.payload_digest != payload_digest:
            raise ValueError(
                "Resource Egress receipt payload identity differs from portable payload"
            )
        return cls(
            plan=PreparedResourceTransfer(
                transfer_id=source_egress.transfer_id,
                source_world_id=source_egress.source_world_id,
                destination_world_id=source_egress.destination_world_id,
                resource_kind=source_egress.resource_kind,
                source_egress_digest=source_egress.digest,
                payload_digest=payload_digest,
            ),
            source_egress=source_egress.to_dict(),
            payload=payload,
        )


@dataclass(frozen=True, slots=True)
class ResourceTransferReceipt:
    transfer_id: str
    plan_digest: str
    destination_world_id: str
    payload_digest: str
    materialization_id: str
    materialization_digest: str
    destination_evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.transfer_id.startswith("transfer:"):
            raise ValueError("Resource transfer receipt identity must start with transfer:")
        for label, value in (
            ("plan digest", self.plan_digest),
            ("payload digest", self.payload_digest),
            ("materialization digest", self.materialization_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")
        if not self.destination_world_id or not self.materialization_id:
            raise ValueError("Resource transfer receipt destination identities must be non-empty")
        if not isinstance(self.destination_evidence, dict):
            raise ValueError("Resource transfer destination evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-transfer-receipt",
            "transferId": self.transfer_id,
            "planDigest": self.plan_digest,
            "destinationWorldId": self.destination_world_id,
            "payloadDigest": self.payload_digest,
            "materializationId": self.materialization_id,
            "materializationDigest": self.materialization_digest,
            "destinationEvidence": self.destination_evidence,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ResourceTransferReceipt:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.resource-transfer-receipt"
        ):
            raise ValueError("Resource transfer receipt schema is unsupported")
        evidence = value.get("destinationEvidence")
        if not isinstance(evidence, dict):
            raise ValueError("Resource transfer destination evidence must be an object")
        return cls(
            transfer_id=str(value["transferId"]),
            plan_digest=str(value["planDigest"]),
            destination_world_id=str(value["destinationWorldId"]),
            payload_digest=str(value["payloadDigest"]),
            materialization_id=str(value["materializationId"]),
            materialization_digest=str(value["materializationDigest"]),
            destination_evidence=dict(evidence),
        )


@dataclass(frozen=True, slots=True)
class ResourceTransferNotCommitted:
    transfer_id: str
    plan_digest: str
    destination_world_id: str
    payload_digest: str
    evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.transfer_id.startswith("transfer:"):
            raise ValueError("Resource not-committed identity must start with transfer:")
        for label, value in (
            ("plan digest", self.plan_digest),
            ("payload digest", self.payload_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")
        if not self.destination_world_id:
            raise ValueError("Resource not-committed destination World must be non-empty")
        if not isinstance(self.evidence, dict):
            raise ValueError("Resource not-committed evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-transfer-not-committed",
            "transferId": self.transfer_id,
            "planDigest": self.plan_digest,
            "destinationWorldId": self.destination_world_id,
            "payloadDigest": self.payload_digest,
            "evidence": self.evidence,
        }


class ResourceTransferOutcomeUnknown(ResourceTransferError):
    def __init__(self, plan: PreparedResourceTransfer, cause: BaseException) -> None:
        self.plan = plan
        self.cause = cause
        super().__init__(
            f"resource transfer outcome is unknown for {plan.transfer_id}; reconcile before redispatch: {cause}"
        )


class ResourceTransferDestination(Protocol):
    def materialize(self, bundle: ResourceTransferBundle) -> ResourceTransferReceipt: ...

    def reconcile(
        self,
        plan: PreparedResourceTransfer,
    ) -> ResourceTransferReceipt | ResourceTransferNotCommitted | None: ...


@dataclass(frozen=True, slots=True)
class HostResourceTransferStep:
    task_id: str
    task_revision: int
    transfer_id: str
    status: str
    receipt: ResourceTransferReceipt | None = None
    reconciled: bool = False


class HostResourceTransferJournal(_HostTrajectoryJournal):
    """Durable resource transfer journal backed by Host's opaque extension port."""

    label = "World resource transfer"
    event_token = "world-resource"
    event_kind_prefix = "world.resource-transfer"
    state_field = "worldResourceTransferState"
    plan_digest_field = "worldResourceTransferPlanDigest"
    plan_object_field = "worldResourceTransferPlanObjectDigest"
    receipt_digest_field = "worldResourceTransferReceiptDigest"
    receipt_object_field = "worldResourceTransferReceiptObjectDigest"
    uncertainty_object_field = "worldResourceTransferUncertaintyObjectDigest"
    plan_kind = _PLAN_KIND
    receipt_kind = _RECEIPT_KIND
    uncertainty_kind = _UNCERTAINTY_KIND
    uncertainty_value_kind = "ordivon.world.resource-transfer-uncertainty"
    uncertainty_identity_field = "transferId"
    uncertainty_next_action = "reconcile-original-transfer"
    plan_identity_attr = "transfer_id"
    step_identity_field = "transfer_id"
    plan_type = PreparedResourceTransfer
    bundle_type = ResourceTransferBundle
    receipt_type = ResourceTransferReceipt
    step_type = HostResourceTransferStep
    outcome_unknown_type = ResourceTransferOutcomeUnknown
    error_type = ResourceTransferError
    superseded_type = ResourceTransferSuperseded
    slots = (
        _PayloadSlot(
            "worldResourceSourceEgressDigest",
            "worldResourceSourceEgressObjectDigest",
            _SOURCE_EGRESS_KIND,
            "source_egress",
            "source_egress_digest",
        ),
        _PayloadSlot(
            "worldResourcePayloadDigest",
            "worldResourcePayloadObjectDigest",
            _PAYLOAD_KIND,
            "payload",
            "payload_digest",
        ),
    )
    correlation_fields = (("worldResourceTransferId", "transfer_id"),)
    receipt_bindings = (
        ("transfer identity", "transfer_id", "transfer_id"),
        ("plan identity", "plan_digest", "digest"),
        ("destination World", "destination_world_id", "destination_world_id"),
        ("payload identity", "payload_digest", "payload_digest"),
    )
    terminal_state = "materialized"
    terminal_fields = (
        ("worldResourceMaterializationId", "materialization_id"),
        ("worldResourceMaterializationDigest", "materialization_digest"),
    )

    def deliver(
        self,
        task_id: str,
        destination: ResourceTransferDestination,
    ) -> HostResourceTransferStep:
        return self.execute(task_id, destination.materialize)

    def reconcile(
        self,
        task_id: str,
        destination: ResourceTransferDestination,
    ) -> HostResourceTransferStep:
        bundle = self.load_bundle(task_id)
        plan = bundle.plan
        current = self.port.load(task_id)
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
        if isinstance(result, ResourceTransferNotCommitted):
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
        plan: PreparedResourceTransfer,
        proof: ResourceTransferNotCommitted,
    ) -> HostResourceTransferStep:
        self._validate_not_committed(plan, proof)
        current = self.port.load(task_id)
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
        if current.data.get(self.state_field) == "prepared":
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                "prepared",
                None,
                True,
            )
        if current.data.get(self.state_field) != "unknown":
            raise ResourceTransferError(
                "not-committed proof can only release an unknown Resource Transfer"
            )
        proof_value = proof.to_dict()
        proof_digest = sha256_digest(proof_value)
        proof_object = self.port.put_object(proof_value, kind=_NOT_COMMITTED_KIND)
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, "not-committed", current.projection.revision + 1),
            kind=EventKind("world.resource-transfer-not-committed"),
            updates={
                self.state_field: "prepared",
                "worldResourceTransferNotCommittedDigest": proof_digest,
                "worldResourceTransferNotCommittedObjectDigest": proof_object.digest,
            },
            remove_fields=(self.uncertainty_object_field,),
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
        plan: PreparedResourceTransfer,
        proof: ResourceTransferNotCommitted,
    ) -> None:
        if proof.transfer_id != plan.transfer_id:
            raise ResourceTransferSuperseded(
                "not-committed proof belongs to another Resource Transfer"
            )
        if proof.plan_digest != plan.digest:
            raise ResourceTransferSuperseded(
                "not-committed proof binds another Resource Transfer plan"
            )
        if proof.destination_world_id != plan.destination_world_id:
            raise ResourceTransferSuperseded(
                "not-committed proof belongs to another destination World"
            )
        if proof.payload_digest != plan.payload_digest:
            raise ResourceTransferSuperseded("not-committed proof binds another Resource payload")
        if proof.evidence.get("exactOriginalRetrySafe") is not True:
            raise ResourceTransferError(
                "not-committed evidence does not authorize exact original retry"
            )
