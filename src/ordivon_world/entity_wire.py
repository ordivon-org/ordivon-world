from __future__ import annotations

from typing import Any, Protocol

from .entity_migration import (
    EntityDepartureReceipt,
    EntityMigrationBundle,
    EntityMigrationError,
    EntityMigrationNotCommitted,
    EntityMigrationOutcomeUnknown,
    EntityMigrationReceipt,
    PreparedEntityMigration,
)
from .schemas import ContractError, validate_contract

_REQUEST_KIND = "ordivon.world.entity-migration-destination-request"
_RESPONSE_KIND = "ordivon.world.entity-migration-destination-response"


class EntityMigrationWireError(EntityMigrationError):
    pass


class EntityMigrationDestinationRejected(EntityMigrationWireError):
    def __init__(self, code: str, reason: str) -> None:
        self.code = code
        self.reason = reason
        super().__init__(f"entity migration destination rejected request [{code}]: {reason}")


class EntityMigrationTransportError(EntityMigrationWireError):
    pass


class EntityMigrationPreDispatchError(EntityMigrationTransportError):
    """The transport proves the destination operation never started."""


class EntityMigrationTransportOutcomeUnknown(EntityMigrationTransportError):
    """The transport may have dispatched but cannot return an authoritative response."""


class EntityMigrationWireTransport(Protocol):
    def exchange(self, request: dict[str, Any]) -> dict[str, Any]: ...


class EntityMigrationWireDestination:
    def __init__(self, transport: EntityMigrationWireTransport) -> None:
        self.transport = transport

    def materialize(self, bundle: EntityMigrationBundle) -> EntityMigrationReceipt:
        self._require_source_departure(bundle)
        request = {
            "schemaVersion": 1,
            "kind": _REQUEST_KIND,
            "operation": "materialize",
            "plan": bundle.plan.to_dict(),
            "planDigest": bundle.plan.digest,
            "sourceDeparture": bundle.source_departure,
            "continuityPayload": bundle.continuity_payload,
        }
        self._validate_request(request)
        try:
            response = self.transport.exchange(request)
        except EntityMigrationTransportOutcomeUnknown as error:
            raise EntityMigrationOutcomeUnknown(bundle.plan, error) from error
        except EntityMigrationPreDispatchError:
            raise
        try:
            self._validate_response_envelope(response)
            status = response.get("status")
            if status == "unknown":
                reason = response.get("reason")
                raise EntityMigrationOutcomeUnknown(
                    bundle.plan,
                    EntityMigrationWireError(
                        str(reason) if isinstance(reason, str) and reason else "destination unknown"
                    ),
                )
            if status == "rejected":
                raise self._rejected(response)
            if status != "materialized":
                raise EntityMigrationWireError(
                    "entity migration materialize response status is unsupported"
                )
            return self._receipt(response)
        except (EntityMigrationDestinationRejected, EntityMigrationOutcomeUnknown):
            raise
        except (KeyError, TypeError, ValueError, EntityMigrationWireError) as error:
            raise EntityMigrationOutcomeUnknown(bundle.plan, error) from error

    def reconcile(
        self,
        plan: PreparedEntityMigration,
    ) -> EntityMigrationReceipt | EntityMigrationNotCommitted | None:
        request = {
            "schemaVersion": 1,
            "kind": _REQUEST_KIND,
            "operation": "reconcile",
            "plan": plan.to_dict(),
            "planDigest": plan.digest,
        }
        self._validate_request(request)
        response = self.transport.exchange(request)
        self._validate_response_envelope(response)
        status = response.get("status")
        if status == "unknown":
            if (
                response.get("migrationId") != plan.migration_id
                or response.get("planDigest") != plan.digest
            ):
                raise EntityMigrationWireError("unknown reconciliation response identity drifted")
            return None
        if status == "not_committed":
            evidence = response.get("evidence")
            if not isinstance(evidence, dict):
                raise EntityMigrationWireError("not-committed response omitted evidence")
            try:
                return EntityMigrationNotCommitted(
                    migration_id=str(response["migrationId"]),
                    plan_digest=str(response["planDigest"]),
                    entity_id=str(response["entityId"]),
                    destination_world_id=str(response["destinationWorldId"]),
                    source_departure_digest=str(response["sourceDepartureDigest"]),
                    continuity_payload_digest=str(response["continuityPayloadDigest"]),
                    evidence=dict(evidence),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise EntityMigrationWireError("not-committed response is invalid") from error
        if status == "rejected":
            raise self._rejected(response)
        if status != "materialized":
            raise EntityMigrationWireError("entity migration reconciliation status is unsupported")
        return self._receipt(response)

    @staticmethod
    def _require_source_departure(bundle: EntityMigrationBundle) -> None:
        value = bundle.source_departure
        if not isinstance(value, dict):
            raise EntityMigrationWireError(
                "production Entity Migration requires a source departure receipt"
            )
        try:
            departure = EntityDepartureReceipt.from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            raise EntityMigrationWireError(
                "production Entity Migration requires a valid source departure receipt"
            ) from error
        plan = bundle.plan
        if (
            departure.migration_id != plan.migration_id
            or departure.entity_id != plan.entity_id
            or departure.source_world_id != plan.source_world_id
            or departure.destination_world_id != plan.destination_world_id
            or departure.digest != plan.source_departure_digest
        ):
            raise EntityMigrationWireError(
                "source departure receipt differs from Entity Migration plan"
            )

    @staticmethod
    def _receipt(response: dict[str, Any]) -> EntityMigrationReceipt:
        value = response.get("receipt")
        if not isinstance(value, dict):
            raise EntityMigrationWireError("materialized response omitted Entity Migration receipt")
        try:
            return EntityMigrationReceipt.from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            raise EntityMigrationWireError("Entity Migration receipt is invalid") from error

    @staticmethod
    def _validate_request(request: dict[str, Any]) -> None:
        try:
            validate_contract("entity-migration-destination-request", request)
        except ContractError as error:
            raise EntityMigrationWireError(
                "entity migration destination request violates the published wire contract"
            ) from error

    @staticmethod
    def _validate_response_envelope(response: dict[str, Any]) -> None:
        if not isinstance(response, dict):
            raise EntityMigrationWireError(
                "entity migration destination response must be an object"
            )
        try:
            validate_contract("entity-migration-destination-response", response)
        except ContractError as error:
            raise EntityMigrationWireError(
                "entity migration destination response violates the published wire contract"
            ) from error

    @staticmethod
    def _rejected(response: dict[str, Any]) -> EntityMigrationDestinationRejected:
        code = response.get("code")
        reason = response.get("reason")
        if not isinstance(code, str) or not code or not isinstance(reason, str) or not reason:
            raise EntityMigrationWireError("entity migration destination rejection is malformed")
        return EntityMigrationDestinationRejected(code, reason)
