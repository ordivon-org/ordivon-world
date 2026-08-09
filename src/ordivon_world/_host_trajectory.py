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
    """Private durable mechanics shared by proven cross-World trajectories.

    Trajectories default to the original one-instance-per-Task storage. A
    production trajectory may opt into `instances_field` when practice proves
    that semantic trajectory identity must be independent of Host Task identity.
    """

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
    instances_field: ClassVar[str | None] = None
    extra_instance_fields: ClassVar[tuple[str, ...]] = ()

    def __init__(self, port: HostExtensionPort) -> None:
        self.port = port

    def identities(self, task_id: str) -> tuple[str, ...]:
        current = self.port.load_namespace(task_id, "world")
        if self.instances_field is not None:
            return tuple(sorted(self._instances(current.data)))
        if not self.correlation_fields:
            return ()
        value = current.data.get(self.correlation_fields[0][0])
        return (value,) if isinstance(value, str) else ()

    def prepare(self, task_id: str, bundle: Any) -> Any:
        plan = bundle.plan
        self._verify_plan(plan)
        for slot in self.slots:
            self._verify_slot(slot, plan, getattr(bundle, slot.bundle_attr))
        current = self.port.load_namespace(task_id, "world")
        identity = self._plan_identity(plan)
        existing_entry = self._optional_entry(current.data, identity)
        if existing_entry is not None:
            existing = existing_entry.get(self.plan_digest_field)
            if existing != plan.digest:
                raise self.superseded_type(
                    f"{self.label} identity {identity} already retains different semantic meaning"
                )
            self._require_current(current.data, plan)
            return self._step(
                task_id,
                current.projection.revision,
                plan,
                str(existing_entry.get(self.state_field, "prepared")),
                self._load_receipt_from_data(current.data, plan),
                False,
            )

        objects = []
        entry_updates = self._correlation(plan)
        for slot in self.slots:
            value = getattr(bundle, slot.bundle_attr)
            stored = self.port.put_object(value, kind=slot.object_kind)
            objects.append(stored)
            entry_updates[slot.object_field] = stored.digest
        plan_object = self.port.put_object(plan.to_dict(), kind=self.plan_kind)
        objects.append(plan_object)
        entry_updates[self.plan_object_field] = plan_object.digest
        entry_updates[self.state_field] = "prepared"
        updates, remove_fields = self._mutation(
            current.data,
            plan,
            entry_updates,
            allow_missing=True,
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, "prepared", current.projection.revision + 1),
            kind=EventKind(f"{self.event_kind_prefix}-prepared"),
            updates=updates,
            remove_fields=remove_fields,
            referenced_objects=tuple(objects),
            label=self.label,
        )
        return self._step(task_id, committed.projection.revision, plan, "prepared", None, False)

    def load_bundle(self, task_id: str, identity: str | None = None) -> Any:
        current = self.port.load_namespace(task_id, "world")
        selected = self._select_identity(current.data, identity)
        entry = self._entry_by_identity(current.data, selected)
        digest = entry.get(self.plan_digest_field)
        object_digest = entry.get(self.plan_object_field)
        if not isinstance(digest, str) or not isinstance(object_digest, str):
            raise self.error_type(f"Host Task has no prepared {self.label} for {selected}")
        value = self.port.get_object(object_digest, expected_kind=self.plan_kind)
        if not isinstance(value, dict):
            raise self.error_type(f"Prepared {self.label} CAS value is not an object")
        try:
            plan = self.plan_type.from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            raise self.error_type(f"Prepared {self.label} CAS value is invalid") from error
        self._verify_plan(plan)
        if self._plan_identity(plan) != selected:
            raise self.error_type(f"Prepared {self.label} identity drifted from Host addressing")
        if plan.digest != digest:
            raise self.error_type(f"Prepared {self.label} semantic identity drifted")
        self._require_current(current.data, plan)
        values: dict[str, Any] = {}
        for slot in self.slots:
            object_key = entry.get(slot.object_field)
            if not isinstance(object_key, str):
                raise self.error_type(f"Host Task {self.label} CAS references are missing")
            slot_value = self.port.get_object(object_key, expected_kind=slot.object_kind)
            self._verify_slot(slot, plan, slot_value)
            values[slot.bundle_attr] = slot_value
        try:
            return self.bundle_type(plan=plan, **values)
        except ValueError as error:
            raise self.error_type(f"Retained {self.label} bundle is inconsistent") from error

    def execute(self, task_id: str, materialize: Any, identity: str | None = None) -> Any:
        bundle = self.load_bundle(task_id, identity)
        plan = bundle.plan
        current = self.port.load_namespace(task_id, "world")
        entry = self._entry(current.data, plan)
        receipt = self._load_receipt_from_data(current.data, plan)
        if receipt is not None:
            return self._step(
                task_id, current.projection.revision, plan, self.terminal_state, receipt, False
            )
        if entry.get(self.state_field) == "unknown":
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

    def reconcile(self, task_id: str, observe: Any, identity: str | None = None) -> Any:
        bundle = self.load_bundle(task_id, identity)
        plan = bundle.plan
        current = self.port.load_namespace(task_id, "world")
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
        current = self.port.load_namespace(task_id, "world")
        self._require_current(current.data, plan)
        entry = self._entry(current.data, plan)
        receipt = self._load_receipt_from_data(current.data, plan)
        if receipt is not None:
            return self._step(
                task_id, current.projection.revision, plan, self.terminal_state, receipt, False
            )
        if entry.get(self.state_field) == "unknown":
            return self._step(task_id, current.projection.revision, plan, "unknown", None, False)
        uncertainty = {
            "schemaVersion": 1,
            "kind": self.uncertainty_value_kind,
            self.uncertainty_identity_field: self._plan_identity(plan),
            "planDigest": plan.digest,
            "status": "unknown",
            "reason": reason,
            "nextAction": self.uncertainty_next_action,
        }
        uncertainty_object = self.port.put_object(uncertainty, kind=self.uncertainty_kind)
        updates, remove_fields = self._mutation(
            current.data,
            plan,
            {
                self.state_field: "unknown",
                self.uncertainty_object_field: uncertainty_object.digest,
            },
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, "unknown", current.projection.revision + 1),
            kind=EventKind(f"{self.event_kind_prefix}-outcome-unknown"),
            updates=updates,
            remove_fields=remove_fields,
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
        current = self.port.load_namespace(task_id, "world")
        self._require_current(current.data, plan)
        entry = self._entry(current.data, plan)
        value = receipt.to_dict()
        digest = sha256_digest(value)
        existing = entry.get(self.receipt_digest_field)
        if existing is not None:
            if existing != digest:
                raise self.superseded_type(
                    f"{self.label} identity {self._plan_identity(plan)} already retains another receipt"
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
        entry_updates = {
            self.state_field: self.terminal_state,
            self.receipt_digest_field: digest,
            self.receipt_object_field: receipt_object.digest,
        }
        entry_updates.update(
            {field: getattr(receipt, attr) for field, attr in self.terminal_fields}
        )
        updates, remove_fields = self._mutation(
            current.data,
            plan,
            entry_updates,
            remove_fields=(self.uncertainty_object_field,),
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(task_id, self.terminal_state, current.projection.revision + 1),
            kind=EventKind(f"{self.event_kind_prefix}-{self.terminal_state}"),
            updates=updates,
            remove_fields=remove_fields,
            referenced_objects=(*self._retained_objects(current.data, plan), receipt_object),
            label=self.label,
        )
        return self._step(
            task_id, committed.projection.revision, plan, self.terminal_state, receipt, reconciled
        )

    def load_receipt(self, task_id: str, identity: str | None = None) -> Any:
        bundle = self.load_bundle(task_id, identity)
        current = self.port.load_namespace(task_id, "world")
        receipt = self._load_receipt_from_data(current.data, bundle.plan)
        if receipt is None:
            raise self.error_type(f"Host Task has no retained {self.label} receipt")
        return receipt

    def _load_receipt_from_data(self, data: dict[str, Any], plan: Any) -> Any | None:
        entry = self._entry(data, plan)
        digest = entry.get(self.receipt_digest_field)
        object_digest = entry.get(self.receipt_object_field)
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
        entry = self._entry(data, plan)
        fields = (self.plan_object_field, *(slot.object_field for slot in self.slots))
        return tuple(self.port.inspect_object(str(entry[field])) for field in fields)

    def _correlation(self, plan: Any) -> dict[str, Any]:
        values = {field: getattr(plan, attr) for field, attr in self.correlation_fields}
        values[self.plan_digest_field] = plan.digest
        values.update(
            {slot.semantic_field: getattr(plan, slot.plan_digest_attr) for slot in self.slots}
        )
        return values

    def _require_current(self, data: dict[str, Any], plan: Any) -> None:
        entry = self._entry(data, plan)
        if any(entry.get(key) != value for key, value in self._correlation(plan).items()):
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

    def _plan_identity(self, plan: Any) -> str:
        value = getattr(plan, self.plan_identity_attr)
        if not isinstance(value, str) or not value:
            raise self.error_type(f"{self.label} semantic identity must be non-empty")
        return value

    def _instances(self, data: dict[str, Any]) -> dict[str, dict[str, Any]]:
        if self.instances_field is None:
            raise self.error_type(f"{self.label} does not use multi-instance Host addressing")
        raw = data.get(self.instances_field)
        if raw is None:
            legacy = self._legacy_entry(data)
            if legacy is None:
                return {}
            identity = (
                legacy.get(self.correlation_fields[0][0]) if self.correlation_fields else None
            )
            if not isinstance(identity, str) or not identity:
                raise self.error_type(f"Legacy Host Task {self.label} identity is invalid")
            return {identity: legacy}
        if not isinstance(raw, dict):
            raise self.error_type(f"Host Task {self.instances_field} must be an object")
        instances: dict[str, dict[str, Any]] = {}
        for identity, value in raw.items():
            if not isinstance(identity, str) or not isinstance(value, dict):
                raise self.error_type(f"Host Task {self.instances_field} contains invalid entry")
            instances[identity] = dict(value)
        return instances

    def _legacy_fields(self) -> tuple[str, ...]:
        fields = [
            self.state_field,
            self.plan_digest_field,
            self.plan_object_field,
            self.receipt_digest_field,
            self.receipt_object_field,
            self.uncertainty_object_field,
            *(field for field, _attr in self.correlation_fields),
            *(slot.semantic_field for slot in self.slots),
            *(slot.object_field for slot in self.slots),
            *(field for field, _attr in self.terminal_fields),
            *self.extra_instance_fields,
        ]
        return tuple(dict.fromkeys(fields))

    def _legacy_entry(self, data: dict[str, Any]) -> dict[str, Any] | None:
        if data.get(self.plan_digest_field) is None:
            return None
        return {field: data[field] for field in self._legacy_fields() if field in data}

    def _optional_entry(self, data: dict[str, Any], identity: str) -> dict[str, Any] | None:
        if self.instances_field is None:
            return data if data.get(self.plan_digest_field) is not None else None
        return self._instances(data).get(identity)

    def _entry(self, data: dict[str, Any], plan: Any) -> dict[str, Any]:
        identity = self._plan_identity(plan)
        entry = self._optional_entry(data, identity)
        if entry is None:
            raise self.error_type(f"Host Task has no retained {self.label} for {identity}")
        return entry

    def _entry_by_identity(self, data: dict[str, Any], identity: str) -> dict[str, Any]:
        if self.instances_field is None:
            return data
        entry = self._instances(data).get(identity)
        if entry is None:
            raise self.error_type(f"Host Task has no retained {self.label} for {identity}")
        return entry

    def _select_identity(self, data: dict[str, Any], identity: str | None) -> str:
        if self.instances_field is None:
            if not self.correlation_fields:
                raise self.error_type(f"{self.label} has no semantic identity field")
            retained = data.get(self.correlation_fields[0][0])
            if not isinstance(retained, str):
                raise self.error_type(f"Host Task has no prepared {self.label}")
            if identity is not None and identity != retained:
                raise self.error_type(f"Host Task has no retained {self.label} for {identity}")
            return retained
        instances = self._instances(data)
        if identity is not None:
            if identity not in instances:
                raise self.error_type(f"Host Task has no retained {self.label} for {identity}")
            return identity
        if not instances:
            raise self.error_type(f"Host Task has no prepared {self.label}")
        if len(instances) != 1:
            raise self.error_type(
                f"Host Task retains multiple {self.label} instances; semantic identity is required"
            )
        return next(iter(instances))

    def _mutation(
        self,
        data: dict[str, Any],
        plan: Any,
        updates: dict[str, Any],
        *,
        remove_fields: tuple[str, ...] = (),
        allow_missing: bool = False,
    ) -> tuple[dict[str, Any], tuple[str, ...]]:
        if self.instances_field is None:
            return updates, remove_fields
        identity = self._plan_identity(plan)
        instances = self._instances(data)
        entry = dict(instances.get(identity, {}))
        if not entry and not allow_missing:
            raise self.error_type(f"Host Task has no retained {self.label} for {identity}")
        for field in remove_fields:
            entry.pop(field, None)
        entry.update(updates)
        instances[identity] = entry
        legacy_remove = tuple(field for field in self._legacy_fields() if field in data)
        return {self.instances_field: instances}, legacy_remove

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
            **{self.step_identity_field: self._plan_identity(plan)},
            status=status,
            receipt=receipt,
            reconciled=reconciled,
        )
