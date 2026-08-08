from __future__ import annotations

import unittest

from ordivon_world.canonical import sha256_digest
from ordivon_world.resource_transfer import (
    ResourceTransferBundle,
    ResourceTransferOutcomeUnknown,
)
from ordivon_world.resource_wire import (
    ResourceTransferDestinationRejected,
    ResourceTransferPreDispatchError,
    ResourceTransferTransportOutcomeUnknown,
    ResourceTransferWireDestination,
    ResourceTransferWireError,
)


def bundle() -> ResourceTransferBundle:
    return ResourceTransferBundle.create(
        transfer_id="transfer:w2:wire",
        source_world_id="world-instance:w2:A",
        destination_world_id="world-instance:w2:B",
        resource_kind="test-resource",
        source_evidence={"kind": "source", "factId": "fact:w2"},
        payload={"kind": "portable-resource", "value": 7},
    )


def receipt(value: ResourceTransferBundle) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.resource-transfer-receipt",
        "transferId": value.plan.transfer_id,
        "planDigest": value.plan.digest,
        "destinationWorldId": value.plan.destination_world_id,
        "payloadDigest": value.plan.payload_digest,
        "materializationId": "resource:w2:wire",
        "materializationDigest": sha256_digest({"materialized": value.plan.payload_digest}),
        "destinationEvidence": {"authority": "wire-test"},
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


class ResourceTransferWireTests(unittest.TestCase):
    def test_materialize_serializes_exact_semantic_bundle_and_accepts_receipt(self) -> None:
        value = bundle()
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.resource-transfer-destination-response",
                "status": "materialized",
                "receipt": receipt(value),
            }
        )
        destination = ResourceTransferWireDestination(transport)
        observed = destination.materialize(value)
        self.assertEqual(observed.to_dict(), receipt(value))
        self.assertEqual(
            transport.requests,
            [
                {
                    "schemaVersion": 1,
                    "kind": "ordivon.world.resource-transfer-destination-request",
                    "operation": "materialize",
                    "plan": value.plan.to_dict(),
                    "planDigest": value.plan.digest,
                    "sourceEvidence": value.source_evidence,
                    "payload": value.payload,
                }
            ],
        )

    def test_explicit_rejection_is_safe_failure_not_unknown(self) -> None:
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.resource-transfer-destination-response",
                "status": "rejected",
                "code": "policy-rejected",
                "reason": "source World is not admitted",
            }
        )
        with self.assertRaises(ResourceTransferDestinationRejected):
            ResourceTransferWireDestination(transport).materialize(bundle())

    def test_pre_dispatch_failure_is_not_converted_to_unknown(self) -> None:
        transport = Transport(error=ResourceTransferPreDispatchError("endpoint not started"))
        with self.assertRaises(ResourceTransferPreDispatchError):
            ResourceTransferWireDestination(transport).materialize(bundle())

    def test_ambiguous_transport_failure_becomes_resource_outcome_unknown(self) -> None:
        transport = Transport(error=ResourceTransferTransportOutcomeUnknown("reply lost"))
        with self.assertRaises(ResourceTransferOutcomeUnknown):
            ResourceTransferWireDestination(transport).materialize(bundle())

    def test_malformed_post_dispatch_response_is_treated_as_unknown(self) -> None:
        transport = Transport({"schemaVersion": 1, "kind": "wrong", "status": "materialized"})
        with self.assertRaises(ResourceTransferOutcomeUnknown):
            ResourceTransferWireDestination(transport).materialize(bundle())

    def test_reconcile_missing_is_identity_bound_and_read_only(self) -> None:
        value = bundle()
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.resource-transfer-destination-response",
                "status": "missing",
                "transferId": value.plan.transfer_id,
                "planDigest": value.plan.digest,
            }
        )
        destination = ResourceTransferWireDestination(transport)
        self.assertIsNone(destination.reconcile(value.plan))
        self.assertEqual(transport.requests[0]["operation"], "reconcile")
        self.assertNotIn("payload", transport.requests[0])
        self.assertNotIn("sourceEvidence", transport.requests[0])

    def test_reconcile_not_committed_returns_identity_bound_retry_proof(self) -> None:
        value = bundle()
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.resource-transfer-destination-response",
                "status": "not_committed",
                "transferId": value.plan.transfer_id,
                "planDigest": value.plan.digest,
                "destinationWorldId": value.plan.destination_world_id,
                "payloadDigest": value.plan.payload_digest,
                "evidence": {
                    "authority": "test-destination",
                    "exactOriginalRetrySafe": True,
                },
            }
        )
        result = ResourceTransferWireDestination(transport).reconcile(value.plan)
        self.assertEqual(result.transfer_id, value.plan.transfer_id)
        self.assertEqual(result.plan_digest, value.plan.digest)
        self.assertTrue(result.evidence["exactOriginalRetrySafe"])

    def test_reconcile_invalid_response_does_not_invent_receipt(self) -> None:
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.resource-transfer-destination-response",
                "status": "materialized",
            }
        )
        with self.assertRaises(ResourceTransferWireError):
            ResourceTransferWireDestination(transport).reconcile(bundle().plan)


if __name__ == "__main__":
    unittest.main()
