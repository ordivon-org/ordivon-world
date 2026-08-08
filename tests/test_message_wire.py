from __future__ import annotations

import unittest

from ordivon_world.canonical import sha256_digest
from ordivon_world.message_delivery import (
    MessageDeliveryBundle,
    MessageDeliveryOutcomeUnknown,
    MessageIssuanceAuthority,
    MessageIssuanceReceipt,
)
from ordivon_world.message_wire import (
    MessageDeliveryDestinationRejected,
    MessageDeliveryPreDispatchError,
    MessageDeliveryTransportOutcomeUnknown,
    MessageDeliveryWireDestination,
    MessageDeliveryWireError,
)


def bundle() -> MessageDeliveryBundle:
    provenance = {"kind": "message-provenance", "factId": "fact:w2"}
    payload = {"kind": "message-payload", "claim": "unstable"}
    issuance = MessageIssuanceReceipt(
        message_id="message:w2:wire",
        source_world_id="world-instance:w2:A",
        destination_world_id="world-instance:w2:B",
        message_kind="test-message",
        provenance_digest=sha256_digest(provenance),
        payload_digest=sha256_digest(payload),
        source_occurrence_id="message-source:w2:wire",
        source_occurrence_digest=sha256_digest({"factId": "fact:w2"}),
        authority=MessageIssuanceAuthority(
            authority_id="source-authority:w2:A",
            mechanism="test-message-issuance.v1",
            evidence={"factId": "fact:w2"},
        ),
    )
    return MessageDeliveryBundle.create_issued(
        source_issuance=issuance,
        provenance=provenance,
        payload=payload,
    )


def receipt(value: MessageDeliveryBundle) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.message-delivery-receipt",
        "messageId": value.plan.message_id,
        "planDigest": value.plan.digest,
        "destinationWorldId": value.plan.destination_world_id,
        "payloadDigest": value.plan.payload_digest,
        "deliveryId": "message-admission:w2:wire",
        "deliveryDigest": sha256_digest({"messageId": value.plan.message_id}),
        "destinationEvidence": {"authority": "wire-test", "classification": "management"},
    }


class Transport:
    def __init__(self, response=None, error: BaseException | None = None) -> None:
        self.response = response
        self.error = error
        self.requests: list[dict[str, object]] = []

    def exchange(self, request):
        self.requests.append(request)
        if self.error is not None:
            raise self.error
        return self.response


class MessageDeliveryWireTests(unittest.TestCase):
    def test_deliver_serializes_source_issued_bundle_and_accepts_receipt(self) -> None:
        value = bundle()
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.message-delivery-destination-response",
                "status": "delivered",
                "receipt": receipt(value),
            }
        )
        observed = MessageDeliveryWireDestination(transport).deliver(value)
        self.assertEqual(observed.to_dict(), receipt(value))
        request = transport.requests[0]
        self.assertEqual(request["operation"], "deliver")
        self.assertEqual(request["plan"]["sourceIssuance"], value.plan.source_issuance.to_dict())
        self.assertEqual(request["provenance"], value.provenance)
        self.assertEqual(request["payload"], value.payload)

    def test_legacy_unissued_bundle_is_rejected_before_transport(self) -> None:
        legacy = MessageDeliveryBundle.create(
            message_id="message:w2:legacy",
            source_world_id="world:A",
            destination_world_id="world:B",
            message_kind="legacy",
            provenance={"p": 1},
            payload={"v": 1},
        )
        transport = Transport()
        with self.assertRaises(MessageDeliveryWireError):
            MessageDeliveryWireDestination(transport).deliver(legacy)
        self.assertEqual(transport.requests, [])

    def test_rejection_is_safe_failure_not_unknown(self) -> None:
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.message-delivery-destination-response",
                "status": "rejected",
                "code": "policy-rejected",
                "reason": "source not admitted",
            }
        )
        with self.assertRaises(MessageDeliveryDestinationRejected):
            MessageDeliveryWireDestination(transport).deliver(bundle())

    def test_pre_dispatch_failure_is_not_unknown(self) -> None:
        transport = Transport(error=MessageDeliveryPreDispatchError("endpoint absent"))
        with self.assertRaises(MessageDeliveryPreDispatchError):
            MessageDeliveryWireDestination(transport).deliver(bundle())

    def test_ambiguous_transport_failure_becomes_message_unknown(self) -> None:
        transport = Transport(error=MessageDeliveryTransportOutcomeUnknown("ACK lost"))
        with self.assertRaises(MessageDeliveryOutcomeUnknown):
            MessageDeliveryWireDestination(transport).deliver(bundle())

    def test_reconcile_not_committed_returns_retry_proof_without_payload(self) -> None:
        value = bundle()
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.message-delivery-destination-response",
                "status": "not_committed",
                "messageId": value.plan.message_id,
                "planDigest": value.plan.digest,
                "destinationWorldId": value.plan.destination_world_id,
                "payloadDigest": value.plan.payload_digest,
                "evidence": {"authority": "test-destination", "exactOriginalRetrySafe": True},
            }
        )
        proof = MessageDeliveryWireDestination(transport).reconcile(value.plan)
        self.assertEqual(proof.message_id, value.plan.message_id)
        self.assertTrue(proof.evidence["exactOriginalRetrySafe"])
        request = transport.requests[0]
        self.assertEqual(request["operation"], "reconcile")
        self.assertNotIn("payload", request)
        self.assertNotIn("provenance", request)

    def test_invalid_reconcile_response_does_not_invent_receipt(self) -> None:
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.message-delivery-destination-response",
                "status": "delivered",
            }
        )
        with self.assertRaises(MessageDeliveryWireError):
            MessageDeliveryWireDestination(transport).reconcile(bundle().plan)


if __name__ == "__main__":
    unittest.main()
