from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ._host_trajectory import _HostTrajectoryJournal, _PayloadSlot
from .canonical import sha256_digest

_PLAN_KIND = "world-resource-transfer-plan"
_SOURCE_EVIDENCE_KIND = "world-resource-source-evidence"
_PAYLOAD_KIND = "world-resource-portable-payload"
_RECEIPT_KIND = "world-resource-destination-receipt"
_UNCERTAINTY_KIND = "world-resource-transfer-uncertainty"


class ResourceTransferError(RuntimeError):
    pass


class ResourceTransferSuperseded(ResourceTransferError):
    pass


@dataclass(frozen=True, slots=True)
class PreparedResourceTransfer:
    """One exact cross-World resource-transfer intent.

    The plan deliberately owns no source-domain or destination-domain state. It
    binds one source evidence object and one portable payload object retained in
    Host CAS to one destination World identity.
    """

    transfer_id: str
    source_world_id: str
    destination_world_id: str
    resource_kind: str
    source_evidence_digest: str
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
            ("source evidence digest", self.source_evidence_digest),
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
            "sourceEvidenceDigest": self.source_evidence_digest,
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
            source_evidence_digest=str(value["sourceEvidenceDigest"]),
            payload_digest=str(value["payloadDigest"]),
        )


@dataclass(frozen=True, slots=True)
class ResourceTransferBundle:
    plan: PreparedResourceTransfer
    source_evidence: Any
    payload: Any

    def __post_init__(self) -> None:
        if sha256_digest(self.source_evidence) != self.plan.source_evidence_digest:
            raise ValueError("Resource transfer source evidence digest mismatch")
        if sha256_digest(self.payload) != self.plan.payload_digest:
            raise ValueError("Resource transfer payload digest mismatch")

    @classmethod
    def create(
        cls,
        *,
        transfer_id: str,
        source_world_id: str,
        destination_world_id: str,
        resource_kind: str,
        source_evidence: Any,
        payload: Any,
    ) -> ResourceTransferBundle:
        return cls(
            plan=PreparedResourceTransfer(
                transfer_id=transfer_id,
                source_world_id=source_world_id,
                destination_world_id=destination_world_id,
                resource_kind=resource_kind,
                source_evidence_digest=sha256_digest(source_evidence),
                payload_digest=sha256_digest(payload),
            ),
            source_evidence=source_evidence,
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


class ResourceTransferOutcomeUnknown(ResourceTransferError):
    def __init__(self, plan: PreparedResourceTransfer, cause: BaseException) -> None:
        self.plan = plan
        self.cause = cause
        super().__init__(
            f"resource transfer outcome is unknown for {plan.transfer_id}; reconcile before redispatch: {cause}"
        )


class ResourceTransferDestination(Protocol):
    def materialize(self, bundle: ResourceTransferBundle) -> ResourceTransferReceipt: ...

    def reconcile(self, plan: PreparedResourceTransfer) -> ResourceTransferReceipt | None: ...


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
            "worldResourceSourceEvidenceDigest",
            "worldResourceSourceEvidenceObjectDigest",
            _SOURCE_EVIDENCE_KIND,
            "source_evidence",
            "source_evidence_digest",
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
    materialization_fields = (
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
        return super().reconcile(task_id, destination.reconcile)
