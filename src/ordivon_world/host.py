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
    """Persist World adapter facts through Host's opaque extension boundary.

    The extension owns only its schemas and provider correlation. Host continues
    to own Task state, revision fencing, Ready Frontier, authority and completion.
    """

    def __init__(self, port: HostExtensionPort) -> None:
        self.port = port

    def prepare(
        self,
        task_id: str,
        prepared: PreparedWorldDispatch,
    ) -> HostWorldStep:
        current = self.port.load(task_id)
        existing = current.data.get("worldPreparedDispatchDigest")
        prepared_object = self.port.put_object(
            prepared.to_dict(),
            kind=_PREPARED_KIND,
        )
        if existing is not None:
            if existing != prepared_object.digest:
                raise HostWorldSuperseded(
                    "Host Task already retains a different World Dispatch"
                )
            return self._step(
                task_id,
                current.projection.revision,
                prepared,
                status=str(current.data.get("worldOutcomeState", "prepared")),
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
            updates={
                "worldPreparedDispatchDigest": prepared_object.digest,
                "worldDispatchId": prepared.dispatch.dispatch_id,
                "worldProviderRequestId": prepared.provider_request_id,
                "worldOutcomeState": "prepared",
            },
            referenced_objects=(prepared_object,),
            label="World",
        )
        return self._step(
            task_id,
            committed.projection.revision,
            prepared,
            status="prepared",
        )

    def load_prepared(self, task_id: str) -> PreparedWorldDispatch:
        current = self.port.load(task_id)
        digest = current.data.get("worldPreparedDispatchDigest")
        if not isinstance(digest, str):
            raise HostWorldError("Host Task has no prepared World Dispatch")
        value = self.port.get_object(digest, expected_kind=_PREPARED_KIND)
        if not isinstance(value, dict):
            raise HostWorldError("prepared World Dispatch CAS value is not an object")
        try:
            prepared = PreparedWorldDispatch.from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            raise HostWorldError("prepared World Dispatch CAS value is invalid") from error
        self._require_current(current.data, prepared)
        return prepared

    def deliver(
        self,
        task_id: str,
        adapter: CloudflareWorldAdapter,
        *,
        check_conditions: bool = True,
    ) -> HostWorldStep:
        prepared = self.load_prepared(task_id)
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
    ) -> HostWorldStep:
        prepared = self.load_prepared(task_id)
        result = adapter.reconcile(prepared)
        return self.record_reconciliation(task_id, prepared, result)

    def record_unknown(
        self,
        task_id: str,
        prepared: PreparedWorldDispatch,
        *,
        reason: str,
    ) -> HostWorldStep:
        current = self.port.load(task_id)
        self._require_current(current.data, prepared)
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
        prepared_object = self.port.inspect_object(
            str(current.data["worldPreparedDispatchDigest"])
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
            updates={
                "worldOutcomeState": "unknown",
                "worldUncertaintyDigest": uncertainty_object.digest,
            },
            remove_fields=("worldObservationDigest",),
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
            current = self.port.load(task_id)
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
            current = self.port.load(task_id)
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
        current = self.port.load(task_id)
        self._require_current(current.data, prepared)
        if observation.envelope.dispatch_id != prepared.dispatch.dispatch_id:
            raise HostWorldSuperseded(
                "World Observation belongs to another Host Dispatch"
            )
        observation_object = self.port.put_object(
            observation.to_dict(),
            kind=_OBSERVATION_KIND,
        )
        existing = current.data.get("worldObservationDigest")
        if existing is not None:
            if existing != observation_object.digest:
                raise HostWorldSuperseded(
                    "Host Task already retains a different World Observation"
                )
            return self._step(
                task_id,
                current.projection.revision,
                prepared,
                status=observation.envelope.status,
                observation=observation,
                reconciled=observation.reconciled,
            )
        prepared_object = self.port.inspect_object(
            str(current.data["worldPreparedDispatchDigest"])
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
            updates={
                "worldOutcomeState": observation.envelope.status,
                "worldObservationDigest": observation_object.digest,
                "worldObservationPayloadDigest": (
                    observation.envelope.payload_digest
                ),
                "worldObservationReconciled": observation.reconciled,
            },
            remove_fields=("worldUncertaintyDigest",),
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

    @staticmethod
    def _require_current(
        data: dict[str, Any],
        prepared: PreparedWorldDispatch,
    ) -> None:
        if (
            data.get("worldDispatchId") != prepared.dispatch.dispatch_id
            or data.get("worldProviderRequestId")
            != prepared.provider_request_id
        ):
            raise HostWorldSuperseded(
                "Host Task World Dispatch correlation changed"
            )

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
