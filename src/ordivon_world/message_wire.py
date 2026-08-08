from __future__ import annotations

from typing import Any, Protocol

from .message_delivery import (
    MessageDeliveryBundle,
    MessageDeliveryError,
    MessageDeliveryNotCommitted,
    MessageDeliveryOutcomeUnknown,
    MessageDeliveryReceipt,
    PreparedMessageDelivery,
)
from .schemas import ContractError, validate_contract

_REQUEST_KIND = "ordivon.world.message-delivery-destination-request"
_RESPONSE_KIND = "ordivon.world.message-delivery-destination-response"


class MessageDeliveryWireError(MessageDeliveryError):
    pass


class MessageDeliveryDestinationRejected(MessageDeliveryWireError):
    def __init__(self, code: str, reason: str) -> None:
        self.code = code
        self.reason = reason
        super().__init__(f"message destination rejected request [{code}]: {reason}")


class MessageDeliveryTransportError(MessageDeliveryWireError):
    pass


class MessageDeliveryPreDispatchError(MessageDeliveryTransportError):
    """The transport proves the destination operation never started."""


class MessageDeliveryTransportOutcomeUnknown(MessageDeliveryTransportError):
    """The transport may have dispatched but cannot return an authoritative response."""


class MessageDeliveryWireTransport(Protocol):
    def exchange(self, request: dict[str, Any]) -> dict[str, Any]: ...


class MessageDeliveryWireDestination:
    """Map source-issued Message semantics onto the destination JSON contract."""

    def __init__(self, transport: MessageDeliveryWireTransport) -> None:
        self.transport = transport

    def deliver(self, bundle: MessageDeliveryBundle) -> MessageDeliveryReceipt:
        if bundle.plan.source_issuance is None:
            raise MessageDeliveryWireError(
                "production Message delivery requires a source issuance receipt"
            )
        request = {
            "schemaVersion": 1,
            "kind": _REQUEST_KIND,
            "operation": "deliver",
            "plan": bundle.plan.to_dict(),
            "planDigest": bundle.plan.digest,
            "provenance": bundle.provenance,
            "payload": bundle.payload,
        }
        self._validate_request(request)
        try:
            response = self.transport.exchange(request)
        except MessageDeliveryTransportOutcomeUnknown as error:
            raise MessageDeliveryOutcomeUnknown(bundle.plan, error) from error
        except MessageDeliveryPreDispatchError:
            raise
        try:
            return self._receipt_from_deliver_response(response)
        except MessageDeliveryDestinationRejected:
            raise
        except (KeyError, TypeError, ValueError, MessageDeliveryWireError) as error:
            raise MessageDeliveryOutcomeUnknown(bundle.plan, error) from error

    def reconcile(
        self,
        plan: PreparedMessageDelivery,
    ) -> MessageDeliveryReceipt | MessageDeliveryNotCommitted | None:
        if plan.source_issuance is None:
            raise MessageDeliveryWireError(
                "production Message reconciliation requires a source issuance receipt"
            )
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
        if status == "missing":
            if (
                response.get("messageId") != plan.message_id
                or response.get("planDigest") != plan.digest
            ):
                raise MessageDeliveryWireError("missing reconciliation response identity drifted")
            return None
        if status == "not_committed":
            evidence = response.get("evidence")
            if not isinstance(evidence, dict):
                raise MessageDeliveryWireError(
                    "not-committed reconciliation response omitted evidence"
                )
            try:
                return MessageDeliveryNotCommitted(
                    message_id=str(response["messageId"]),
                    plan_digest=str(response["planDigest"]),
                    destination_world_id=str(response["destinationWorldId"]),
                    payload_digest=str(response["payloadDigest"]),
                    evidence=dict(evidence),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise MessageDeliveryWireError(
                    "not-committed reconciliation response is invalid"
                ) from error
        if status == "rejected":
            raise self._rejected(response)
        if status != "delivered":
            raise MessageDeliveryWireError("message reconciliation response status is unsupported")
        receipt_value = response.get("receipt")
        if not isinstance(receipt_value, dict):
            raise MessageDeliveryWireError("delivered reconciliation response omitted receipt")
        try:
            return MessageDeliveryReceipt.from_dict(receipt_value)
        except (KeyError, TypeError, ValueError) as error:
            raise MessageDeliveryWireError("message reconciliation receipt is invalid") from error

    @classmethod
    def _receipt_from_deliver_response(cls, response: dict[str, Any]) -> MessageDeliveryReceipt:
        cls._validate_response_envelope(response)
        status = response.get("status")
        if status == "rejected":
            raise cls._rejected(response)
        if status != "delivered":
            raise MessageDeliveryWireError("message deliver response status is unsupported")
        receipt_value = response.get("receipt")
        if not isinstance(receipt_value, dict):
            raise MessageDeliveryWireError("delivered response omitted Message Delivery receipt")
        try:
            return MessageDeliveryReceipt.from_dict(receipt_value)
        except (KeyError, TypeError, ValueError) as error:
            raise MessageDeliveryWireError(
                "delivered Message Delivery receipt is invalid"
            ) from error

    @staticmethod
    def _validate_request(request: dict[str, Any]) -> None:
        try:
            validate_contract("message-delivery-destination-request", request)
        except ContractError as error:
            raise MessageDeliveryWireError(
                "message destination request violates the published wire contract"
            ) from error

    @staticmethod
    def _validate_response_envelope(response: dict[str, Any]) -> None:
        if not isinstance(response, dict):
            raise MessageDeliveryWireError("message destination response must be an object")
        try:
            validate_contract("message-delivery-destination-response", response)
        except ContractError as error:
            raise MessageDeliveryWireError(
                "message destination response violates the published wire contract"
            ) from error

    @staticmethod
    def _rejected(response: dict[str, Any]) -> MessageDeliveryDestinationRejected:
        code = response.get("code")
        reason = response.get("reason")
        if not isinstance(code, str) or not code or not isinstance(reason, str) or not reason:
            raise MessageDeliveryWireError("message destination rejection is malformed")
        return MessageDeliveryDestinationRejected(code, reason)
