from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ordivon_host import EventKind

from ._host_trajectory import _HostTrajectoryJournal, _PayloadSlot
from .canonical import sha256_digest

_PLAN_KIND = "world-message-delivery-plan"
_PROVENANCE_KIND = "world-message-source-provenance"
_PAYLOAD_KIND = "world-message-payload"
_RECEIPT_KIND = "world-message-delivery-receipt"
_UNCERTAINTY_KIND = "world-message-delivery-uncertainty"
_NOT_COMMITTED_KIND = "world-message-delivery-not-committed"


class MessageDeliveryError(RuntimeError):
    pass


class MessageDeliverySuperseded(MessageDeliveryError):
    pass


@dataclass(frozen=True, slots=True)
class MessageIssuanceAuthority:
    authority_id: str
    mechanism: str
    evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.authority_id or not self.mechanism:
            raise ValueError("Message issuance authority identity and mechanism must be non-empty")
        if not isinstance(self.evidence, dict):
            raise ValueError("Message issuance authority evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "authorityId": self.authority_id,
            "mechanism": self.mechanism,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> MessageIssuanceAuthority:
        evidence = value.get("evidence")
        if not isinstance(evidence, dict):
            raise ValueError("Message issuance authority evidence must be an object")
        return cls(
            authority_id=str(value["authorityId"]),
            mechanism=str(value["mechanism"]),
            evidence=dict(evidence),
        )


@dataclass(frozen=True, slots=True)
class MessageIssuanceReceipt:
    message_id: str
    source_world_id: str
    destination_world_id: str
    message_kind: str
    provenance_digest: str
    payload_digest: str
    source_occurrence_id: str
    source_occurrence_digest: str
    authority: MessageIssuanceAuthority

    def __post_init__(self) -> None:
        if not self.message_id.startswith("message:"):
            raise ValueError("Message issuance identity must start with message:")
        for label, value in (
            ("source World identity", self.source_world_id),
            ("destination World identity", self.destination_world_id),
            ("message kind", self.message_kind),
            ("source occurrence identity", self.source_occurrence_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        for label, value in (
            ("message provenance digest", self.provenance_digest),
            ("message payload digest", self.payload_digest),
            ("source occurrence digest", self.source_occurrence_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.message-issuance-receipt",
            "messageId": self.message_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "messageKind": self.message_kind,
            "provenanceDigest": self.provenance_digest,
            "payloadDigest": self.payload_digest,
            "sourceOccurrenceId": self.source_occurrence_id,
            "sourceOccurrenceDigest": self.source_occurrence_digest,
            "authority": self.authority.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> MessageIssuanceReceipt:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.message-issuance-receipt"
        ):
            raise ValueError("Message issuance receipt schema is unsupported")
        authority = value.get("authority")
        if not isinstance(authority, dict):
            raise ValueError("Message issuance authority is missing")
        return cls(
            message_id=str(value["messageId"]),
            source_world_id=str(value["sourceWorldId"]),
            destination_world_id=str(value["destinationWorldId"]),
            message_kind=str(value["messageKind"]),
            provenance_digest=str(value["provenanceDigest"]),
            payload_digest=str(value["payloadDigest"]),
            source_occurrence_id=str(value["sourceOccurrenceId"]),
            source_occurrence_digest=str(value["sourceOccurrenceDigest"]),
            authority=MessageIssuanceAuthority.from_dict(authority),
        )


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
    source_issuance: MessageIssuanceReceipt | None = None

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
        if self.source_issuance is not None:
            issue = self.source_issuance
            if (
                issue.message_id != self.message_id
                or issue.source_world_id != self.source_world_id
                or issue.destination_world_id != self.destination_world_id
                or issue.message_kind != self.message_kind
                or issue.provenance_digest != self.provenance_digest
                or issue.payload_digest != self.payload_digest
            ):
                raise ValueError("Message issuance receipt differs from delivery plan")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        value = {
            "schemaVersion": 1,
            "kind": "ordivon.world.prepared-message-delivery",
            "messageId": self.message_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "messageKind": self.message_kind,
            "provenanceDigest": self.provenance_digest,
            "payloadDigest": self.payload_digest,
        }
        if self.source_issuance is not None:
            value["sourceIssuance"] = self.source_issuance.to_dict()
        return value

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PreparedMessageDelivery:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.prepared-message-delivery"
        ):
            raise ValueError("Prepared message delivery schema is unsupported")
        source_issuance = value.get("sourceIssuance")
        if source_issuance is not None and not isinstance(source_issuance, dict):
            raise ValueError("Prepared message source issuance must be an object")
        return cls(
            message_id=str(value["messageId"]),
            source_world_id=str(value["sourceWorldId"]),
            destination_world_id=str(value["destinationWorldId"]),
            message_kind=str(value["messageKind"]),
            provenance_digest=str(value["provenanceDigest"]),
            payload_digest=str(value["payloadDigest"]),
            source_issuance=(
                None
                if source_issuance is None
                else MessageIssuanceReceipt.from_dict(source_issuance)
            ),
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

    @classmethod
    def create_issued(
        cls,
        *,
        source_issuance: MessageIssuanceReceipt,
        provenance: Any,
        payload: Any,
    ) -> MessageDeliveryBundle:
        if sha256_digest(provenance) != source_issuance.provenance_digest:
            raise ValueError("Message provenance differs from source issuance")
        if sha256_digest(payload) != source_issuance.payload_digest:
            raise ValueError("Message payload differs from source issuance")
        return cls(
            plan=PreparedMessageDelivery(
                message_id=source_issuance.message_id,
                source_world_id=source_issuance.source_world_id,
                destination_world_id=source_issuance.destination_world_id,
                message_kind=source_issuance.message_kind,
                provenance_digest=source_issuance.provenance_digest,
                payload_digest=source_issuance.payload_digest,
                source_issuance=source_issuance,
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


@dataclass(frozen=True, slots=True)
class MessageDeliveryNotCommitted:
    message_id: str
    plan_digest: str
    destination_world_id: str
    payload_digest: str
    evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.message_id.startswith("message:"):
            raise ValueError("Message not-committed identity must start with message:")
        for label, value in (
            ("plan digest", self.plan_digest),
            ("payload digest", self.payload_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")
        if not self.destination_world_id:
            raise ValueError("Message not-committed destination World must be non-empty")
        if not isinstance(self.evidence, dict):
            raise ValueError("Message not-committed evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.message-delivery-not-committed",
            "messageId": self.message_id,
            "planDigest": self.plan_digest,
            "destinationWorldId": self.destination_world_id,
            "payloadDigest": self.payload_digest,
            "evidence": self.evidence,
        }


class MessageDeliveryOutcomeUnknown(MessageDeliveryError):
    def __init__(self, plan: PreparedMessageDelivery, cause: BaseException) -> None:
        self.plan = plan
        self.cause = cause
        super().__init__(
            f"message delivery outcome is unknown for {plan.message_id}; reconcile before redelivery: {cause}"
        )


class MessageDeliveryDestination(Protocol):
    def deliver(self, bundle: MessageDeliveryBundle) -> MessageDeliveryReceipt: ...

    def reconcile(
        self, plan: PreparedMessageDelivery
    ) -> MessageDeliveryReceipt | MessageDeliveryNotCommitted | None: ...


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
    owner_family = "message-delivery"
    owner_initial_operation = "deliver-prepared-message"
    owner_retry_operation = "retry-exact-original-message"
    instances_field = "worldMessageDeliveries"
    extra_instance_fields = (
        "worldMessageDeliveryNotCommittedDigest",
        "worldMessageDeliveryNotCommittedObjectDigest",
    )
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

    def message_ids(self, task_id: str) -> tuple[str, ...]:
        return self.identities(task_id)

    def load_bundle(
        self,
        task_id: str,
        message_id: str | None = None,
    ) -> MessageDeliveryBundle:
        return super().load_bundle(task_id, message_id)

    def load_receipt(
        self,
        task_id: str,
        message_id: str | None = None,
    ) -> MessageDeliveryReceipt:
        return super().load_receipt(task_id, message_id)

    def deliver(
        self,
        task_id: str,
        destination: MessageDeliveryDestination,
        *,
        message_id: str | None = None,
    ) -> HostMessageDeliveryStep:
        return self.execute(task_id, destination.deliver, message_id)

    def reconcile(
        self,
        task_id: str,
        destination: MessageDeliveryDestination,
        *,
        message_id: str | None = None,
    ) -> HostMessageDeliveryStep:
        bundle = self.load_bundle(task_id, message_id)
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
        if isinstance(result, MessageDeliveryNotCommitted):
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
        plan: PreparedMessageDelivery,
        proof: MessageDeliveryNotCommitted,
    ) -> HostMessageDeliveryStep:
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
            raise MessageDeliveryError(
                "not-committed proof can only release an unknown Message Delivery"
            )
        proof_value = proof.to_dict()
        proof_digest = sha256_digest(proof_value)
        proof_object = self.port.put_object(proof_value, kind=_NOT_COMMITTED_KIND)
        updates, remove_fields = self._mutation(
            current.data,
            plan,
            {
                self.state_field: "prepared",
                "worldMessageDeliveryNotCommittedDigest": proof_digest,
                "worldMessageDeliveryNotCommittedObjectDigest": proof_object.digest,
            },
            remove_fields=(self.uncertainty_object_field,),
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, "not-committed", current.projection.revision + 1),
            kind=EventKind("world.message-delivery-not-committed"),
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
        plan: PreparedMessageDelivery,
        proof: MessageDeliveryNotCommitted,
    ) -> None:
        if proof.message_id != plan.message_id:
            raise MessageDeliverySuperseded(
                "not-committed proof belongs to another Message Delivery"
            )
        if proof.plan_digest != plan.digest:
            raise MessageDeliverySuperseded(
                "not-committed proof binds another Message Delivery plan"
            )
        if proof.destination_world_id != plan.destination_world_id:
            raise MessageDeliverySuperseded(
                "not-committed proof belongs to another destination World"
            )
        if proof.payload_digest != plan.payload_digest:
            raise MessageDeliverySuperseded("not-committed proof binds another Message payload")
        if proof.evidence.get("exactOriginalRetrySafe") is not True:
            raise MessageDeliveryError(
                "not-committed evidence does not authorize exact original retry"
            )
