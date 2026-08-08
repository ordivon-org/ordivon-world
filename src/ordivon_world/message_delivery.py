from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ._host_trajectory import _HostTrajectoryJournal, _PayloadSlot
from .canonical import sha256_digest

_PLAN_KIND = "world-message-delivery-plan"
_PROVENANCE_KIND = "world-message-source-provenance"
_PAYLOAD_KIND = "world-message-payload"
_RECEIPT_KIND = "world-message-delivery-receipt"
_UNCERTAINTY_KIND = "world-message-delivery-uncertainty"


class MessageDeliveryError(RuntimeError):
    pass


class MessageDeliverySuperseded(MessageDeliveryError):
    pass


@dataclass(frozen=True, slots=True)
class PreparedMessageDelivery:
    """One exact informational delivery intent between two World instances.

    Link binding, transport endpoint and destination knowledge are deliberately
    absent. The message carries provenance and payload; destination truth or
    knowledge promotion requires a separate native-domain decision.
    """

    message_id: str
    source_world_id: str
    destination_world_id: str
    message_kind: str
    provenance_digest: str
    payload_digest: str

    def __post_init__(self) -> None:
        if not self.message_id.startswith("message:"):
            raise ValueError("Message delivery identity must start with message:")
        for label, value in (
            ("source World identity", self.source_world_id),
            ("destination World identity", self.destination_world_id),
            ("message kind", self.message_kind),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        for label, value in (
            ("message provenance digest", self.provenance_digest),
            ("message payload digest", self.payload_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.prepared-message-delivery",
            "messageId": self.message_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "messageKind": self.message_kind,
            "provenanceDigest": self.provenance_digest,
            "payloadDigest": self.payload_digest,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PreparedMessageDelivery:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.prepared-message-delivery"
        ):
            raise ValueError("Prepared message delivery schema is unsupported")
        return cls(
            message_id=str(value["messageId"]),
            source_world_id=str(value["sourceWorldId"]),
            destination_world_id=str(value["destinationWorldId"]),
            message_kind=str(value["messageKind"]),
            provenance_digest=str(value["provenanceDigest"]),
            payload_digest=str(value["payloadDigest"]),
        )


@dataclass(frozen=True, slots=True)
class MessageDeliveryBundle:
    plan: PreparedMessageDelivery
    provenance: Any
    payload: Any

    def __post_init__(self) -> None:
        if sha256_digest(self.provenance) != self.plan.provenance_digest:
            raise ValueError("Message provenance digest mismatch")
        if sha256_digest(self.payload) != self.plan.payload_digest:
            raise ValueError("Message payload digest mismatch")

    @classmethod
    def create(
        cls,
        *,
        message_id: str,
        source_world_id: str,
        destination_world_id: str,
        message_kind: str,
        provenance: Any,
        payload: Any,
    ) -> MessageDeliveryBundle:
        return cls(
            plan=PreparedMessageDelivery(
                message_id=message_id,
                source_world_id=source_world_id,
                destination_world_id=destination_world_id,
                message_kind=message_kind,
                provenance_digest=sha256_digest(provenance),
                payload_digest=sha256_digest(payload),
            ),
            provenance=provenance,
            payload=payload,
        )


@dataclass(frozen=True, slots=True)
class MessageDeliveryReceipt:
    message_id: str
    plan_digest: str
    destination_world_id: str
    payload_digest: str
    delivery_id: str
    delivery_digest: str
    destination_evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.message_id.startswith("message:"):
            raise ValueError("Message delivery receipt identity must start with message:")
        for label, value in (
            ("plan digest", self.plan_digest),
            ("payload digest", self.payload_digest),
            ("delivery digest", self.delivery_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")
        if not self.destination_world_id or not self.delivery_id:
            raise ValueError("Message delivery destination identities must be non-empty")
        if not isinstance(self.destination_evidence, dict):
            raise ValueError("Message delivery destination evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.message-delivery-receipt",
            "messageId": self.message_id,
            "planDigest": self.plan_digest,
            "destinationWorldId": self.destination_world_id,
            "payloadDigest": self.payload_digest,
            "deliveryId": self.delivery_id,
            "deliveryDigest": self.delivery_digest,
            "destinationEvidence": self.destination_evidence,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> MessageDeliveryReceipt:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.message-delivery-receipt"
        ):
            raise ValueError("Message delivery receipt schema is unsupported")
        evidence = value.get("destinationEvidence")
        if not isinstance(evidence, dict):
            raise ValueError("Message delivery destination evidence must be an object")
        return cls(
            message_id=str(value["messageId"]),
            plan_digest=str(value["planDigest"]),
            destination_world_id=str(value["destinationWorldId"]),
            payload_digest=str(value["payloadDigest"]),
            delivery_id=str(value["deliveryId"]),
            delivery_digest=str(value["deliveryDigest"]),
            destination_evidence=dict(evidence),
        )


class MessageDeliveryOutcomeUnknown(MessageDeliveryError):
    def __init__(self, plan: PreparedMessageDelivery, cause: BaseException) -> None:
        self.plan = plan
        self.cause = cause
        super().__init__(
            f"message delivery outcome is unknown for {plan.message_id}; reconcile before redelivery: {cause}"
        )


class MessageDeliveryDestination(Protocol):
    def deliver(self, bundle: MessageDeliveryBundle) -> MessageDeliveryReceipt: ...

    def reconcile(self, plan: PreparedMessageDelivery) -> MessageDeliveryReceipt | None: ...


@dataclass(frozen=True, slots=True)
class HostMessageDeliveryStep:
    task_id: str
    task_revision: int
    message_id: str
    status: str
    receipt: MessageDeliveryReceipt | None = None
    reconciled: bool = False


class HostMessageDeliveryJournal(_HostTrajectoryJournal):
    """Durable informational delivery journal backed by Host's opaque extension port."""

    label = "World message delivery"
    event_token = "world-message"
    event_kind_prefix = "world.message-delivery"
    state_field = "worldMessageDeliveryState"
    plan_digest_field = "worldMessageDeliveryPlanDigest"
    plan_object_field = "worldMessageDeliveryPlanObjectDigest"
    receipt_digest_field = "worldMessageDeliveryReceiptDigest"
    receipt_object_field = "worldMessageDeliveryReceiptObjectDigest"
    uncertainty_object_field = "worldMessageDeliveryUncertaintyObjectDigest"
    plan_kind = _PLAN_KIND
    receipt_kind = _RECEIPT_KIND
    uncertainty_kind = _UNCERTAINTY_KIND
    uncertainty_value_kind = "ordivon.world.message-delivery-uncertainty"
    uncertainty_identity_field = "messageId"
    uncertainty_next_action = "reconcile-original-message"
    plan_identity_attr = "message_id"
    step_identity_field = "message_id"
    plan_type = PreparedMessageDelivery
    bundle_type = MessageDeliveryBundle
    receipt_type = MessageDeliveryReceipt
    step_type = HostMessageDeliveryStep
    outcome_unknown_type = MessageDeliveryOutcomeUnknown
    error_type = MessageDeliveryError
    superseded_type = MessageDeliverySuperseded
    slots = (
        _PayloadSlot(
            "worldMessageProvenanceDigest",
            "worldMessageProvenanceObjectDigest",
            _PROVENANCE_KIND,
            "provenance",
            "provenance_digest",
        ),
        _PayloadSlot(
            "worldMessagePayloadDigest",
            "worldMessagePayloadObjectDigest",
            _PAYLOAD_KIND,
            "payload",
            "payload_digest",
        ),
    )
    correlation_fields = (("worldMessageId", "message_id"),)
    receipt_bindings = (
        ("message identity", "message_id", "message_id"),
        ("plan identity", "plan_digest", "digest"),
        ("destination World", "destination_world_id", "destination_world_id"),
        ("payload identity", "payload_digest", "payload_digest"),
    )
    terminal_state = "delivered"
    terminal_fields = (
        ("worldMessageDestinationDeliveryId", "delivery_id"),
        ("worldMessageDestinationDeliveryDigest", "delivery_digest"),
    )

    def deliver(
        self,
        task_id: str,
        destination: MessageDeliveryDestination,
    ) -> HostMessageDeliveryStep:
        return self.execute(task_id, destination.deliver)

    def reconcile(
        self,
        task_id: str,
        destination: MessageDeliveryDestination,
    ) -> HostMessageDeliveryStep:
        return super().reconcile(task_id, destination.reconcile)
