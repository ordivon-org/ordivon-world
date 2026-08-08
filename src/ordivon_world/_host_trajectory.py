from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from ordivon_host import EventKind, HostExtensionPort

from .canonical import sha256_digest


@dataclass(frozen=True, slots=True)
class _PayloadSlot:
    semantic_field: str
    object_field: str
    object_kind: str
    bundle_attr: str
    plan_digest_attr: str


class _HostTrajectoryJournal:
    """Private durable mechanics proven by two cross-World trajectories."""

    label: ClassVar[str]
    event_token: ClassVar[str]
    event_kind_prefix: ClassVar[str]
    state_field: ClassVar[str]
    plan_digest_field: ClassVar[str]
    plan_object_field: ClassVar[str]
    receipt_digest_field: ClassVar[str]
    receipt_object_field: ClassVar[str]
    uncertainty_object_field: ClassVar[str]
    plan_kind: ClassVar[str]
    receipt_kind: ClassVar[str]
    uncertainty_kind: ClassVar[str]
    uncertainty_value_kind: ClassVar[str]
    uncertainty_identity_field: ClassVar[str]
    uncertainty_next_action: ClassVar[str]
    plan_identity_attr: ClassVar[str]
    step_identity_field: ClassVar[str]
    plan_type: ClassVar[type]
    bundle_type: ClassVar[type]
    receipt_type: ClassVar[type]
    step_type: ClassVar[type]
    outcome_unknown_type: ClassVar[type[Exception]]
    error_type: ClassVar[type[Exception]]
    superseded_type: ClassVar[type[Exception]]
    slots: ClassVar[tuple[_PayloadSlot, ...]]
    correlation_fields: ClassVar[tuple[tuple[str, str], ...]]
    receipt_bindings: ClassVar[tuple[tuple[str, str, str], ...]]
    terminal_state: ClassVar[str]
    terminal_fields: ClassVar[tuple[tuple[str, str], ...]]

    def __init__(self, port: HostExtensionPort) -> None:
        self.port = port

    def prepare(self, task_id: str, bundle: Any) -> Any:
        plan = bundle.plan
        self._verify_plan(plan)
        for slot in self.slots:
            self._verify_slot(slot, plan, getattr(bundle, slot.bundle_attr))
        current = self.port.load(task_id)
        existing = current.data.get(self.plan_digest_field)
        if existing is not None:
            if existing != plan.digest:
                raise self.superseded_type(f"Host Task already retains a different {self.label}")
            self._require_current(current.data, plan)
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                str(current.data.get(self.state_field, "prepared")),
                self._load_receipt_from_data(current.data, plan),
                False,
            )

        objects = []
        updates = self._correlation(plan)
        for slot in self.slots:
            value = getattr(bundle, slot.bundle_attr)
            stored = self.port.put_object(value, kind=slot.object_kind)
            objects.append(stored)
            updates[slot.object_field] = stored.digest
        plan_object = self.port.put_object(plan.to_dict(), kind=self.plan_kind)
        objects.append(plan_object)
        updates[self.plan_object_field] = plan_object.digest
        updates[self.state_field] = "prepared"
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, "prepared", current.projection.revision + 1),
            kind=EventKind(f"{self.event_kind_prefix}-prepared"),
            updates=updates,
            referenced_objects=tuple(objects),
            label=self.label,
        )
        return self._step(task_id, committed.projection.revision, plan, "prepared", None, False)

    def load_bundle(self, task_id: str) -> Any:
        current = self.port.load(task_id)
        digest = current.data.get(self.plan_digest_field)
        object_digest = current.data.get(self.plan_object_field)
        if not isinstance(digest, str) or not isinstance(object_digest, str):
            raise self.error_type(f"Host Task has no prepared {self.label}")
        value = self.port.get_object(object_digest, expected_kind=self.plan_kind)
        if not isinstance(value, dict):
            raise self.error_type(f"Prepared {self.label} CAS value is not an object")
        try:
            plan = self.plan_type.from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            raise self.error_type(f"Prepared {self.label} CAS value is invalid") from error
        self._verify_plan(plan)
        if plan.digest != digest:
            raise self.error_type(f"Prepared {self.label} semantic identity drifted")
        self._require_current(current.data, plan)
        values: dict[str, Any] = {}
        for slot in self.slots:
            object_key = current.data.get(slot.object_field)
            if not isinstance(object_key, str):
                raise self.error_type(f"Host Task {self.label} CAS references are missing")
            value = self.port.get_object(object_key, expected_kind=slot.object_kind)
            self._verify_slot(slot, plan, value)
            values[slot.bundle_attr] = value
        try:
            return self.bundle_type(plan=plan, **values)
        except ValueError as error:
            raise self.error_type(f"Retained {self.label} bundle is inconsistent") from error

    def execute(self, task_id: str, materialize: Any) -> Any:
        bundle = self.load_bundle(task_id)
        plan = bundle.plan
        current = self.port.load(task_id)
        receipt = self._load_receipt_from_data(current.data, plan)
        if receipt is not None:
            return self._step(
                task_id, current.projection.revision, plan, self.terminal_state, receipt, False
            )
        if current.data.get(self.state_field) == "unknown":
            raise self.error_type(
                f"{self.label} outcome is unknown; reconcile the original operation before any new execution"
            )
        try:
            receipt = materialize(bundle)
        except self.outcome_unknown_type as error:
            if error.plan.digest != plan.digest:
                raise self.superseded_type(
                    f"Unknown {self.label} outcome belongs to another trajectory"
                ) from error
            return self.record_unknown(task_id, plan, reason=str(error))
        return self.record_receipt(task_id, plan, receipt)

    def reconcile(self, task_id: str, observe: Any) -> Any:
        bundle = self.load_bundle(task_id)
        plan = bundle.plan
        current = self.port.load(task_id)
        receipt = self._load_receipt_from_data(current.data, plan)
        if receipt is not None:
            return self._step(
                task_id, current.projection.revision, plan, self.terminal_state, receipt, True
            )
        receipt = observe(plan)
        if receipt is None:
            return self._step(task_id, current.projection.revision, plan, "unknown", None, True)
        return self.record_receipt(task_id, plan, receipt, reconciled=True)

    def record_unknown(self, task_id: str, plan: Any, *, reason: str) -> Any:
        current = self.port.load(task_id)
        self._require_current(current.data, plan)
        receipt = self._load_receipt_from_data(current.data, plan)
        if receipt is not None:
            return self._step(
                task_id, current.projection.revision, plan, self.terminal_state, receipt, False
            )
        if current.data.get(self.state_field) == "unknown":
            return self._step(task_id, current.projection.revision, plan, "unknown", None, False)
        uncertainty = {
            "schemaVersion": 1,
            "kind": self.uncertainty_value_kind,
            self.uncertainty_identity_field: getattr(plan, self.plan_identity_attr),
            "planDigest": plan.digest,
            "status": "unknown",
            "reason": reason,
            "nextAction": self.uncertainty_next_action,
        }
        uncertainty_object = self.port.put_object(uncertainty, kind=self.uncertainty_kind)
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, "unknown", current.projection.revision + 1),
            kind=EventKind(f"{self.event_kind_prefix}-outcome-unknown"),
            updates={
                self.state_field: "unknown",
                self.uncertainty_object_field: uncertainty_object.digest,
            },
            referenced_objects=(*self._retained_objects(current.data, plan), uncertainty_object),
            label=self.label,
        )
        return self._step(task_id, committed.projection.revision, plan, "unknown", None, False)

    def record_receipt(
        self,
        task_id: str,
        plan: Any,
        receipt: Any,
        *,
        reconciled: bool = False,
    ) -> Any:
        self._validate_receipt(plan, receipt)
        current = self.port.load(task_id)
        self._require_current(current.data, plan)
        value = receipt.to_dict()
        digest = sha256_digest(value)
        existing = current.data.get(self.receipt_digest_field)
        if existing is not None:
            if existing != digest:
                raise self.superseded_type(
                    f"Host Task already retains a different {self.label} receipt"
                )
            retained = self._load_receipt_from_data(current.data, plan)
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                self.terminal_state,
                retained,
                reconciled,
            )
        receipt_object = self.port.put_object(value, kind=self.receipt_kind)
        updates = {
            self.state_field: self.terminal_state,
            self.receipt_digest_field: digest,
            self.receipt_object_field: receipt_object.digest,
        }
        updates.update({field: getattr(receipt, attr) for field, attr in self.terminal_fields})
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, self.terminal_state, current.projection.revision + 1),
            kind=EventKind(f"{self.event_kind_prefix}-{self.terminal_state}"),
            updates=updates,
            remove_fields=(self.uncertainty_object_field,),
            referenced_objects=(*self._retained_objects(current.data, plan), receipt_object),
            label=self.label,
        )
        return self._step(
            task_id, committed.projection.revision, plan, self.terminal_state, receipt, reconciled
        )

    def load_receipt(self, task_id: str) -> Any:
        bundle = self.load_bundle(task_id)
        current = self.port.load(task_id)
        receipt = self._load_receipt_from_data(current.data, bundle.plan)
        if receipt is None:
            raise self.error_type(f"Host Task has no retained {self.label} receipt")
        return receipt

    def _load_receipt_from_data(self, data: dict[str, Any], plan: Any) -> Any | None:
        digest = data.get(self.receipt_digest_field)
        object_digest = data.get(self.receipt_object_field)
        if digest is None and object_digest is None:
            return None
        if not isinstance(digest, str) or not isinstance(object_digest, str):
            raise self.error_type(f"{self.label} receipt digests are invalid")
        value = self.port.get_object(object_digest, expected_kind=self.receipt_kind)
        if not isinstance(value, dict):
            raise self.error_type(f"{self.label} receipt CAS value is not an object")
        try:
            receipt = self.receipt_type.from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            raise self.error_type(f"{self.label} receipt CAS value is invalid") from error
        self._validate_receipt(plan, receipt)
        if sha256_digest(receipt.to_dict()) != digest:
            raise self.error_type(f"{self.label} receipt semantic identity drifted")
        return receipt

    def _retained_objects(self, data: dict[str, Any], plan: Any) -> tuple[Any, ...]:
        self._require_current(data, plan)
        fields = (self.plan_object_field, *(slot.object_field for slot in self.slots))
        return tuple(self.port.inspect_object(str(data[field])) for field in fields)

    def _correlation(self, plan: Any) -> dict[str, Any]:
        values = {field: getattr(plan, attr) for field, attr in self.correlation_fields}
        values[self.plan_digest_field] = plan.digest
        values.update(
            {slot.semantic_field: getattr(plan, slot.plan_digest_attr) for slot in self.slots}
        )
        return values

    def _require_current(self, data: dict[str, Any], plan: Any) -> None:
        if any(data.get(key) != value for key, value in self._correlation(plan).items()):
            raise self.superseded_type(f"Host Task {self.label} correlation changed")

    def _validate_receipt(self, plan: Any, receipt: Any) -> None:
        for label, receipt_attr, plan_attr in self.receipt_bindings:
            if getattr(receipt, receipt_attr) != getattr(plan, plan_attr):
                raise self.superseded_type(f"Destination receipt {label} drifted")

    def _verify_plan(self, plan: Any) -> None:
        if sha256_digest(plan.to_dict()) != plan.digest:
            raise self.error_type(f"{self.label} plan digest differs from its semantic content")

    def _verify_slot(self, slot: _PayloadSlot, plan: Any, value: Any) -> None:
        if sha256_digest(value) != getattr(plan, slot.plan_digest_attr):
            raise self.error_type(f"{self.label} retained payload digest mismatch")

    def _event_id(self, task_id: str, stage: str, revision: int) -> str:
        token = task_id.removeprefix("task:").replace(":", "-")
        return f"event:{self.event_token}:{token}:{stage}:r{revision}"

    def _step(
        self,
        task_id: str,
        revision: int,
        plan: Any,
        status: str,
        receipt: Any | None,
        reconciled: bool,
    ) -> Any:
        return self.step_type(
            task_id=task_id,
            task_revision=revision,
            **{self.step_identity_field: getattr(plan, self.plan_identity_attr)},
            status=status,
            receipt=receipt,
            reconciled=reconciled,
        )
