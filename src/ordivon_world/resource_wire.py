from __future__ import annotations

from typing import Any, Protocol

from .resource_transfer import (
    PreparedResourceTransfer,
    ResourceTransferBundle,
    ResourceTransferError,
    ResourceTransferNotCommitted,
    ResourceTransferOutcomeUnknown,
    ResourceTransferReceipt,
)

_REQUEST_KIND = "ordivon.world.resource-transfer-destination-request"
_RESPONSE_KIND = "ordivon.world.resource-transfer-destination-response"


class ResourceTransferWireError(ResourceTransferError):
    pass


class ResourceTransferDestinationRejected(ResourceTransferWireError):
    def __init__(self, code: str, reason: str) -> None:
        self.code = code
        self.reason = reason
        super().__init__(f"resource destination rejected request [{code}]: {reason}")


class ResourceTransferTransportError(ResourceTransferWireError):
    pass


class ResourceTransferPreDispatchError(ResourceTransferTransportError):
    """The transport proves the destination operation never started."""


class ResourceTransferTransportOutcomeUnknown(ResourceTransferTransportError):
    """The transport may have dispatched but cannot return an authoritative response."""


class ResourceTransferWireTransport(Protocol):
    def exchange(self, request: dict[str, Any]) -> dict[str, Any]: ...


class ResourceTransferWireDestination:
    """Map Resource Transfer semantics onto a versioned destination JSON contract.

    The transport is injected so World does not own destination process
    supervision. A transport must classify pre-dispatch failure separately from
    ambiguous post-dispatch delivery failure.
    """

    def __init__(self, transport: ResourceTransferWireTransport) -> None:
        self.transport = transport

    def materialize(self, bundle: ResourceTransferBundle) -> ResourceTransferReceipt:
        request = {
            "schemaVersion": 1,
            "kind": _REQUEST_KIND,
            "operation": "materialize",
            "plan": bundle.plan.to_dict(),
            "planDigest": bundle.plan.digest,
            "sourceEvidence": bundle.source_evidence,
            "payload": bundle.payload,
        }
        try:
            response = self.transport.exchange(request)
        except ResourceTransferTransportOutcomeUnknown as error:
            raise ResourceTransferOutcomeUnknown(bundle.plan, error) from error
        except ResourceTransferPreDispatchError:
            raise
        try:
            return self._receipt_from_materialize_response(response)
        except ResourceTransferDestinationRejected:
            raise
        except (KeyError, TypeError, ValueError, ResourceTransferWireError) as error:
            raise ResourceTransferOutcomeUnknown(bundle.plan, error) from error

    def reconcile(
        self,
        plan: PreparedResourceTransfer,
    ) -> ResourceTransferReceipt | ResourceTransferNotCommitted | None:
        request = {
            "schemaVersion": 1,
            "kind": _REQUEST_KIND,
            "operation": "reconcile",
            "plan": plan.to_dict(),
            "planDigest": plan.digest,
        }
        response = self.transport.exchange(request)
        self._validate_response_envelope(response)
        status = response.get("status")
        if status == "missing":
            if (
                response.get("transferId") != plan.transfer_id
                or response.get("planDigest") != plan.digest
            ):
                raise ResourceTransferWireError("missing reconciliation response identity drifted")
            return None
        if status == "not_committed":
            evidence = response.get("evidence")
            if not isinstance(evidence, dict):
                raise ResourceTransferWireError(
                    "not-committed reconciliation response omitted evidence"
                )
            try:
                return ResourceTransferNotCommitted(
                    transfer_id=str(response["transferId"]),
                    plan_digest=str(response["planDigest"]),
                    destination_world_id=str(response["destinationWorldId"]),
                    payload_digest=str(response["payloadDigest"]),
                    evidence=dict(evidence),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise ResourceTransferWireError(
                    "not-committed reconciliation response is invalid"
                ) from error
        if status == "rejected":
            raise self._rejected(response)
        if status != "materialized":
            raise ResourceTransferWireError(
                "resource reconciliation response status is unsupported"
            )
        receipt_value = response.get("receipt")
        if not isinstance(receipt_value, dict):
            raise ResourceTransferWireError("materialized reconciliation response omitted receipt")
        try:
            return ResourceTransferReceipt.from_dict(receipt_value)
        except (KeyError, TypeError, ValueError) as error:
            raise ResourceTransferWireError("resource reconciliation receipt is invalid") from error

    @classmethod
    def _receipt_from_materialize_response(
        cls,
        response: dict[str, Any],
    ) -> ResourceTransferReceipt:
        cls._validate_response_envelope(response)
        status = response.get("status")
        if status == "rejected":
            raise cls._rejected(response)
        if status != "materialized":
            raise ResourceTransferWireError("resource materialize response status is unsupported")
        receipt_value = response.get("receipt")
        if not isinstance(receipt_value, dict):
            raise ResourceTransferWireError(
                "materialized response omitted Resource Transfer receipt"
            )
        try:
            return ResourceTransferReceipt.from_dict(receipt_value)
        except (KeyError, TypeError, ValueError) as error:
            raise ResourceTransferWireError(
                "materialized Resource Transfer receipt is invalid"
            ) from error

    @staticmethod
    def _validate_response_envelope(response: dict[str, Any]) -> None:
        if not isinstance(response, dict):
            raise ResourceTransferWireError("resource destination response must be an object")
        if response.get("schemaVersion") != 1 or response.get("kind") != _RESPONSE_KIND:
            raise ResourceTransferWireError("resource destination response schema is unsupported")

    @staticmethod
    def _rejected(response: dict[str, Any]) -> ResourceTransferDestinationRejected:
        code = response.get("code")
        reason = response.get("reason")
        if not isinstance(code, str) or not code or not isinstance(reason, str) or not reason:
            raise ResourceTransferWireError("resource destination rejection is malformed")
        return ResourceTransferDestinationRejected(code, reason)
