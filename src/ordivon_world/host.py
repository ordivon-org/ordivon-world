from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ordivon_host import EventKind, HostExtensionPort

from .cloudflare import (
    CloudflareWorldAdapter,
    PreparedWorldDispatch,
    ReconciliationResult,
    WorldObservation,
    WorldOutcomeUnknown,
)

_PREPARED_KIND = "world-prepared-dispatch"
_OBSERVATION_KIND = "world-cloudflare-observation"
_UNCERTAINTY_KIND = "world-outcome-uncertainty"


class HostWorldError(RuntimeError):
    pass


class HostWorldSuperseded(HostWorldError):
    pass


@dataclass(frozen=True, slots=True)
class HostWorldStep:
    task_id: str
    task_revision: int
    dispatch_id: str
    provider_request_id: str
    status: str
    observation: WorldObservation | None = None
    reconciled: bool = False


class HostWorldExtension:
    """Persist provider trajectory facts through Host's opaque extension boundary.

    Provider Dispatch identity is independent of Host Task identity. New state is
    stored under ``worldDispatches[dispatchId]``. Pre-P5 flat Task extensions are
    read as one virtual entry and migrate atomically on the first later mutation.

    Host continues to own Task state, revision fencing, Ready Frontier, authority
    and completion; this extension owns only provider correlation and evidence.
    """

    instances_field = "worldDispatches"
    _legacy_fields = (
        "worldPreparedDispatchDigest",
        "worldDispatchId",
        "worldProviderRequestId",
        "worldOutcomeState",
        "worldUncertaintyDigest",
        "worldObservationDigest",
        "worldObservationPayloadDigest",
        "worldObservationReconciled",
    )

    def __init__(self, port: HostExtensionPort) -> None:
        self.port = port

    def dispatch_ids(self, task_id: str) -> tuple[str, ...]:
        current = self.port.load_namespace(task_id, "world")
        return tuple(sorted(self._instances(current.data)))

    def project_owner_commitments(
        self,
        task_id: str,
        data: dict[str, Any],
        *,
        legacy: bool,
    ) -> list[dict[str, Any]]:
        """Project bounded Provider commitment facts from World-owned state."""
        result: list[dict[str, Any]] = []
        for dispatch_id, entry in sorted(self._instances(data).items()):
            digest = entry.get("worldPreparedDispatchDigest")
            if not isinstance(digest, str):
                raise HostWorldError(
                    f"Host Task has no prepared World Dispatch for {dispatch_id}"
                )
            value = self.port.get_object(digest, expected_kind=_PREPARED_KIND)
            if not isinstance(value, dict):
                raise HostWorldError("prepared World Dispatch CAS value is not an object")
            try:
                prepared = PreparedWorldDispatch.from_dict(value)
            except (KeyError, TypeError, ValueError) as error:
                raise HostWorldError("prepared World Dispatch CAS value is invalid") from error
            if prepared.dispatch.dispatch_id != dispatch_id:
                raise HostWorldError(
                    "prepared World Dispatch identity drifted from Host addressing"
                )
            self._require_current(data, prepared)

            state = entry.get("worldOutcomeState", "prepared")
            if not isinstance(state, str) or not state:
                raise HostWorldError("World provider dispatch state is invalid")
            evidence: dict[str, str] = {
                "providerRequestDigest": prepared.provider_request_digest,
            }
            temporal_evidence: dict[str, Any] | None = None
            observation_digest = entry.get("worldObservationDigest")
            if isinstance(observation_digest, str):
                evidence["observationDigest"] = observation_digest
                observation_value = self.port.get_object(
                    observation_digest,
                    expected_kind=_OBSERVATION_KIND,
                )
                if not isinstance(observation_value, dict):
                    raise HostWorldError("World Observation CAS value is not an object")
                try:
                    stored_observation = WorldObservation.from_dict(observation_value)
                except (KeyError, TypeError, ValueError) as error:
                    raise HostWorldError("World Observation CAS value is invalid") from error
                temporal_evidence = {
                    "providerStartedAt": stored_observation.receipt["started_at"],
                    "providerCompletedAt": stored_observation.receipt.get("completed_at"),
                    "availableAt": stored_observation.available_at,
                    "providerTimeSource": "cloudflare-receipt",
                    "availabilityTimeSource": "world.cloudflare",
                }
            uncertainty_digest = entry.get("worldUncertaintyDigest")
            if isinstance(uncertainty_digest, str):
                evidence["uncertaintyObjectDigest"] = uncertainty_digest

            if legacy:
                next_operation: str | None = "recover-legacy-world-state"
            elif state == "prepared":
                next_operation = "deliver-prepared-dispatch"
            elif state in {"unknown", "pending"}:
                next_operation = "reconcile-original-request"
            else:
                next_operation = None

            commitment: dict[str, Any] = {
                "family": "provider-dispatch",
                "identity": dispatch_id,
                "effectId": prepared.dispatch.effect_id,
                "providerRequestId": prepared.provider_request_id,
                "state": state,
                "commitmentClass": (
                    "outstanding"
                    if state in {"prepared", "unknown", "pending"}
                    else "historical-terminal"
                ),
                "evidence": evidence,
                "nextOwnerOperation": next_operation,
                "authority": "not-granted-by-inspection",
                "externalCurrentness": "not-claimed",
            }
            if temporal_evidence is not None:
                commitment["temporalEvidence"] = temporal_evidence
            result.append(commitment)
        return result

    def prepare(
        self,
        task_id: str,
        prepared: PreparedWorldDispatch,
    ) -> HostWorldStep:
        current = self.port.load_namespace(task_id, "world")
        prepared_object = self.port.put_object(
            prepared.to_dict(),
            kind=_PREPARED_KIND,
        )
        dispatch_id = prepared.dispatch.dispatch_id
        existing_entry = self._optional_entry(current.data, dispatch_id)
        if existing_entry is not None:
            existing = existing_entry.get("worldPreparedDispatchDigest")
            if existing != prepared_object.digest:
                raise HostWorldSuperseded(
                    f"World Dispatch identity {dispatch_id} already retains different semantic meaning"
                )
            self._require_current(current.data, prepared)
            return self._step(
                task_id,
                current.projection.revision,
                prepared,
                status=str(existing_entry.get("worldOutcomeState", "prepared")),
            )
        updates, remove_fields = self._mutation(
            current.data,
            prepared,
            {
                "worldPreparedDispatchDigest": prepared_object.digest,
                "worldDispatchId": dispatch_id,
                "worldProviderRequestId": prepared.provider_request_id,
                "worldOutcomeState": "prepared",
            },
            allow_missing=True,
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(
                task_id,
                "prepared",
                current.projection.revision + 1,
            ),
            kind=EventKind("world.dispatch-prepared"),
            updates=updates,
            remove_fields=remove_fields,
            referenced_objects=(prepared_object,),
            label="World",
        )
        return self._step(
            task_id,
            committed.projection.revision,
            prepared,
            status="prepared",
        )

    def load_prepared(
        self,
        task_id: str,
        dispatch_id: str | None = None,
    ) -> PreparedWorldDispatch:
        current = self.port.load_namespace(task_id, "world")
        selected = self._select_dispatch(current.data, dispatch_id)
        entry = self._entry_by_id(current.data, selected)
        digest = entry.get("worldPreparedDispatchDigest")
        if not isinstance(digest, str):
            raise HostWorldError(f"Host Task has no prepared World Dispatch for {selected}")
        value = self.port.get_object(digest, expected_kind=_PREPARED_KIND)
        if not isinstance(value, dict):
            raise HostWorldError("prepared World Dispatch CAS value is not an object")
        try:
            prepared = PreparedWorldDispatch.from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            raise HostWorldError("prepared World Dispatch CAS value is invalid") from error
        if prepared.dispatch.dispatch_id != selected:
            raise HostWorldError("prepared World Dispatch identity drifted from Host addressing")
        self._require_current(current.data, prepared)
        return prepared

    def deliver(
        self,
        task_id: str,
        adapter: CloudflareWorldAdapter,
        *,
        check_conditions: bool = True,
        dispatch_id: str | None = None,
    ) -> HostWorldStep:
        prepared = self.load_prepared(task_id, dispatch_id)
        try:
            observation = adapter.deliver(
                prepared,
                check_conditions=check_conditions,
            )
        except WorldOutcomeUnknown as error:
            if error.prepared != prepared:
                raise HostWorldSuperseded(
                    "unknown provider result belongs to another World Dispatch"
                ) from error
            return self.record_unknown(task_id, prepared, reason=str(error))
        return self.record_observation(task_id, prepared, observation)

    def reconcile(
        self,
        task_id: str,
        adapter: CloudflareWorldAdapter,
        *,
        dispatch_id: str | None = None,
    ) -> HostWorldStep:
        prepared = self.load_prepared(task_id, dispatch_id)
        result = adapter.reconcile(prepared)
        return self.record_reconciliation(task_id, prepared, result)

    def record_unknown(
        self,
        task_id: str,
        prepared: PreparedWorldDispatch,
        *,
        reason: str,
    ) -> HostWorldStep:
        current = self.port.load_namespace(task_id, "world")
        self._require_current(current.data, prepared)
        entry = self._entry(current.data, prepared)
        if entry.get("worldOutcomeState") == "unknown":
            return self._step(
                task_id,
                current.projection.revision,
                prepared,
                status="unknown",
            )
        uncertainty = {
            "schemaVersion": 1,
            "kind": "ordivon.world-outcome-uncertainty",
            "dispatchId": prepared.dispatch.dispatch_id,
            "provider": "cloudflare",
            "providerRequestId": prepared.provider_request_id,
            "providerRequestDigest": prepared.provider_request_digest,
            "status": "unknown",
            "reason": reason,
            "nextAction": "reconcile-original-request",
        }
        uncertainty_object = self.port.put_object(
            uncertainty,
            kind=_UNCERTAINTY_KIND,
        )
        prepared_object = self.port.inspect_object(str(entry["worldPreparedDispatchDigest"]))
        updates, remove_fields = self._mutation(
            current.data,
            prepared,
            {
                "worldOutcomeState": "unknown",
                "worldUncertaintyDigest": uncertainty_object.digest,
            },
            remove_entry_fields=("worldObservationDigest",),
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(
                task_id,
                "unknown",
                current.projection.revision + 1,
            ),
            kind=EventKind("world.outcome-unknown"),
            updates=updates,
            remove_fields=remove_fields,
            referenced_objects=(prepared_object, uncertainty_object),
            label="World",
        )
        return self._step(
            task_id,
            committed.projection.revision,
            prepared,
            status="unknown",
        )

    def record_reconciliation(
        self,
        task_id: str,
        prepared: PreparedWorldDispatch,
        result: ReconciliationResult,
    ) -> HostWorldStep:
        if not result.found:
            current = self.port.load_namespace(task_id, "world")
            self._require_current(current.data, prepared)
            return self._step(
                task_id,
                current.projection.revision,
                prepared,
                status="unknown",
                reconciled=True,
            )
        if result.observation is None:
            raise HostWorldError("found reconciliation result omitted its Observation")
        if result.pending:
            current = self.port.load_namespace(task_id, "world")
            self._require_current(current.data, prepared)
            return self._step(
                task_id,
                current.projection.revision,
                prepared,
                status="pending",
                observation=result.observation,
                reconciled=True,
            )
        return self.record_observation(
            task_id,
            prepared,
            result.observation,
        )

    def record_observation(
        self,
        task_id: str,
        prepared: PreparedWorldDispatch,
        observation: WorldObservation,
    ) -> HostWorldStep:
        current = self.port.load_namespace(task_id, "world")
        self._require_current(current.data, prepared)
        entry = self._entry(current.data, prepared)
        if observation.envelope.dispatch_id != prepared.dispatch.dispatch_id:
            raise HostWorldSuperseded("World Observation belongs to another Host Dispatch")
        observation_document = observation.to_dict()
        existing = entry.get("worldObservationDigest")
        if existing is not None:
            existing_value = self.port.get_object(
                str(existing),
                expected_kind=_OBSERVATION_KIND,
            )
            if not isinstance(existing_value, dict):
                raise HostWorldError("retained World Observation CAS value is not an object")
            try:
                retained_observation = WorldObservation.from_dict(existing_value)
            except (KeyError, TypeError, ValueError) as error:
                raise HostWorldError("retained World Observation CAS value is invalid") from error
            if (
                retained_observation.envelope != observation.envelope
                or retained_observation.receipt != observation.receipt
            ):
                raise HostWorldSuperseded(
                    f"World Dispatch {prepared.dispatch.dispatch_id} already retains a different Observation"
                )
            return self._step(
                task_id,
                current.projection.revision,
                prepared,
                status=retained_observation.envelope.status,
                observation=retained_observation,
                reconciled=retained_observation.reconciled,
            )
        observation_object = self.port.put_object(
            observation_document,
            kind=_OBSERVATION_KIND,
        )
        prepared_object = self.port.inspect_object(str(entry["worldPreparedDispatchDigest"]))
        updates, remove_fields = self._mutation(
            current.data,
            prepared,
            {
                "worldOutcomeState": observation.envelope.status,
                "worldObservationDigest": observation_object.digest,
                "worldObservationPayloadDigest": observation.envelope.payload_digest,
                "worldObservationReconciled": observation.reconciled,
            },
            remove_entry_fields=("worldUncertaintyDigest",),
        )
        committed = self.port.append_preserving(
            task_id=task_id,
            expected_revision=current.projection.revision,
            event_id=self._event_id(
                task_id,
                "observed",
                current.projection.revision + 1,
            ),
            kind=EventKind("world.dispatch-observed"),
            updates=updates,
            remove_fields=remove_fields,
            referenced_objects=(prepared_object, observation_object),
            label="World",
        )
        return self._step(
            task_id,
            committed.projection.revision,
            prepared,
            status=observation.envelope.status,
            observation=observation,
            reconciled=observation.reconciled,
        )

    def _legacy_entry(self, data: dict[str, Any]) -> dict[str, Any] | None:
        if data.get("worldPreparedDispatchDigest") is None:
            return None
        return {field: data[field] for field in self._legacy_fields if field in data}

    def _instances(self, data: dict[str, Any]) -> dict[str, dict[str, Any]]:
        raw = data.get(self.instances_field)
        if raw is None:
            legacy = self._legacy_entry(data)
            if legacy is None:
                return {}
            dispatch_id = legacy.get("worldDispatchId")
            if not isinstance(dispatch_id, str) or not dispatch_id:
                raise HostWorldError("Legacy Host Task World Dispatch identity is invalid")
            return {dispatch_id: legacy}
        if not isinstance(raw, dict):
            raise HostWorldError(f"Host Task {self.instances_field} must be an object")
        instances: dict[str, dict[str, Any]] = {}
        for dispatch_id, value in raw.items():
            if not isinstance(dispatch_id, str) or not isinstance(value, dict):
                raise HostWorldError(f"Host Task {self.instances_field} contains invalid entry")
            instances[dispatch_id] = dict(value)
        return instances

    def _optional_entry(
        self,
        data: dict[str, Any],
        dispatch_id: str,
    ) -> dict[str, Any] | None:
        return self._instances(data).get(dispatch_id)

    def _entry(
        self,
        data: dict[str, Any],
        prepared: PreparedWorldDispatch,
    ) -> dict[str, Any]:
        dispatch_id = prepared.dispatch.dispatch_id
        entry = self._optional_entry(data, dispatch_id)
        if entry is None:
            raise HostWorldError(f"Host Task has no retained World Dispatch for {dispatch_id}")
        return entry

    def _entry_by_id(
        self,
        data: dict[str, Any],
        dispatch_id: str,
    ) -> dict[str, Any]:
        entry = self._optional_entry(data, dispatch_id)
        if entry is None:
            raise HostWorldError(f"Host Task has no retained World Dispatch for {dispatch_id}")
        return entry

    def _select_dispatch(
        self,
        data: dict[str, Any],
        dispatch_id: str | None,
    ) -> str:
        instances = self._instances(data)
        if dispatch_id is not None:
            if dispatch_id not in instances:
                raise HostWorldError(f"Host Task has no retained World Dispatch for {dispatch_id}")
            return dispatch_id
        if not instances:
            raise HostWorldError("Host Task has no prepared World Dispatch")
        if len(instances) != 1:
            raise HostWorldError(
                "Host Task retains multiple World Dispatches; dispatch identity is required"
            )
        return next(iter(instances))

    def _mutation(
        self,
        data: dict[str, Any],
        prepared: PreparedWorldDispatch,
        updates: dict[str, Any],
        *,
        remove_entry_fields: tuple[str, ...] = (),
        allow_missing: bool = False,
    ) -> tuple[dict[str, Any], tuple[str, ...]]:
        dispatch_id = prepared.dispatch.dispatch_id
        instances = self._instances(data)
        entry = dict(instances.get(dispatch_id, {}))
        if not entry and not allow_missing:
            raise HostWorldError(f"Host Task has no retained World Dispatch for {dispatch_id}")
        for field in remove_entry_fields:
            entry.pop(field, None)
        entry.update(updates)
        instances[dispatch_id] = entry
        legacy_remove = tuple(field for field in self._legacy_fields if field in data)
        return {self.instances_field: instances}, legacy_remove

    def _require_current(
        self,
        data: dict[str, Any],
        prepared: PreparedWorldDispatch,
    ) -> None:
        entry = self._entry(data, prepared)
        if (
            entry.get("worldDispatchId") != prepared.dispatch.dispatch_id
            or entry.get("worldProviderRequestId") != prepared.provider_request_id
        ):
            raise HostWorldSuperseded("Host Task World Dispatch correlation changed")

    @staticmethod
    def _event_id(task_id: str, stage: str, revision: int) -> str:
        token = task_id.removeprefix("task:").replace(":", "-")
        return f"event:world:{token}:{stage}:r{revision}"

    @staticmethod
    def _step(
        task_id: str,
        revision: int,
        prepared: PreparedWorldDispatch,
        *,
        status: str,
        observation: WorldObservation | None = None,
        reconciled: bool = False,
    ) -> HostWorldStep:
        return HostWorldStep(
            task_id=task_id,
            task_revision=revision,
            dispatch_id=prepared.dispatch.dispatch_id,
            provider_request_id=prepared.provider_request_id,
            status=status,
            observation=observation,
            reconciled=reconciled,
        )
