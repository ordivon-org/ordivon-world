from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world.canonical import sha256_digest
from ordivon_world.message_delivery import (
    HostMessageDeliveryJournal,
    MessageDeliveryBundle,
    MessageDeliveryOutcomeUnknown,
    MessageDeliveryReceipt,
)

END_TO_END = "message:e2e:w1-p3:reactor-claim"
WORLD_A = "world-instance:w1-p3:A"
WORLD_B = "world-instance:w1-p3:B"
WORLD_C = "world-instance:w1-p3:C"


def claim_payload() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.w1.message-payload",
        "endToEndMessageId": END_TO_END,
        "claim": {"subject": "reactor", "state": "unstable"},
        "sourceConfidence": "confirmed-in-A",
    }


def first_hop() -> MessageDeliveryBundle:
    return MessageDeliveryBundle.create(
        message_id="message:hop:w1-p3:A-B",
        source_world_id=WORLD_A,
        destination_world_id=WORLD_B,
        message_kind="foreign-claim-hop",
        provenance={
            "schemaVersion": 1,
            "kind": "ordivon.w1.message-provenance",
            "endToEndMessageId": END_TO_END,
            "originWorldId": WORLD_A,
            "sourceEvidenceRef": "fact:A:reactor-unstable",
        },
        payload=claim_payload(),
    )


def second_hop(upstream: MessageDeliveryReceipt) -> MessageDeliveryBundle:
    return MessageDeliveryBundle.create(
        message_id="message:hop:w1-p3:B-C",
        source_world_id=WORLD_B,
        destination_world_id=WORLD_C,
        message_kind="relayed-foreign-claim-hop",
        provenance={
            "schemaVersion": 1,
            "kind": "ordivon.w1.relayed-message-provenance",
            "endToEndMessageId": END_TO_END,
            "originWorldClaim": WORLD_A,
            "nativeSourceWorldId": WORLD_B,
            "upstreamReceiptDigest": sha256_digest(upstream.to_dict()),
        },
        payload=claim_payload(),
    )


class DurableInbox:
    def __init__(self, world_id: str) -> None:
        self.world_id = world_id
        self.receipts: dict[str, MessageDeliveryReceipt] = {}
        self.deliveries = 0
        self.available = True
        self.drop_after_commit = False

    def deliver(self, bundle: MessageDeliveryBundle) -> MessageDeliveryReceipt:
        if not self.available:
            raise ConnectionError(f"{self.world_id} is unavailable")
        retained = self.receipts.get(bundle.plan.message_id)
        if retained is not None:
            return retained
        self.deliveries += 1
        receipt = MessageDeliveryReceipt(
            message_id=bundle.plan.message_id,
            plan_digest=bundle.plan.digest,
            destination_world_id=bundle.plan.destination_world_id,
            payload_digest=bundle.plan.payload_digest,
            delivery_id=f"inbox:{self.world_id}:{self.deliveries}",
            delivery_digest=sha256_digest(
                {
                    "messageId": bundle.plan.message_id,
                    "worldId": self.world_id,
                    "sequence": self.deliveries,
                }
            ),
            destination_evidence={
                "authority": f"inbox:{self.world_id}",
                "nativeSourceWorldId": bundle.plan.source_world_id,
                "knowledgePromoted": False,
            },
        )
        self.receipts[bundle.plan.message_id] = receipt
        if self.drop_after_commit:
            self.drop_after_commit = False
            raise MessageDeliveryOutcomeUnknown(
                bundle.plan, RuntimeError("response lost after relay-hop commit")
            )
        return receipt

    def reconcile(self, plan):
        return self.receipts.get(plan.message_id)


def create_task(kernel: HostKernel, task_id: str) -> None:
    token = task_id.removeprefix("task:")
    kernel.create_task(
        event_id=f"event:{token}:create",
        kind=EventKind.TASK_CREATED,
        task_id=task_id,
        goal_id=f"goal:{token}",
        payload={"trajectory": "w1-p3-durable-federation"},
        frontier=(f"node:{token}",),
    )


class W1DurableFederationTests(unittest.TestCase):
    def test_each_hop_has_independent_semantic_identity_receipt_and_native_source(self) -> None:
        b = DurableInbox(WORLD_B)
        c = DurableInbox(WORLD_C)
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(90_000).__next__, owner_id="host:w1-p3"
            )
            create_task(kernel, "task:w1-p3-ab")
            create_task(kernel, "task:w1-p3-bc")
            port = HostExtensionPort(storage, kernel)
            ab = HostMessageDeliveryJournal(port)
            bc = HostMessageDeliveryJournal(port)
            ab.prepare("task:w1-p3-ab", first_hop())
            up = ab.deliver("task:w1-p3-ab", b).receipt
            downstream = second_hop(up)
            bc.prepare("task:w1-p3-bc", downstream)
            down = bc.deliver("task:w1-p3-bc", c).receipt
            self.assertNotEqual(up.message_id, down.message_id)
            self.assertEqual(
                first_hop().payload["endToEndMessageId"], downstream.payload["endToEndMessageId"]
            )
            self.assertEqual(down.destination_evidence["nativeSourceWorldId"], WORLD_B)
            self.assertNotEqual(down.destination_evidence["nativeSourceWorldId"], WORLD_A)
            self.assertEqual(
                downstream.provenance["upstreamReceiptDigest"], sha256_digest(up.to_dict())
            )
            self.assertFalse(down.destination_evidence["knowledgePromoted"])

    def test_downstream_failure_does_not_rollback_upstream_delivery(self) -> None:
        b = DurableInbox(WORLD_B)
        c = DurableInbox(WORLD_C)
        c.available = False
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(91_000).__next__, owner_id="host:w1-p3"
            )
            create_task(kernel, "task:w1-p3-ab")
            create_task(kernel, "task:w1-p3-bc")
            port = HostExtensionPort(storage, kernel)
            ab = HostMessageDeliveryJournal(port)
            bc = HostMessageDeliveryJournal(port)
            ab.prepare("task:w1-p3-ab", first_hop())
            up = ab.deliver("task:w1-p3-ab", b)
            bc.prepare("task:w1-p3-bc", second_hop(up.receipt))
            with self.assertRaises(ConnectionError):
                bc.deliver("task:w1-p3-bc", c)
            self.assertEqual(
                storage.read_task_event("task:w1-p3-ab").data["worldMessageDeliveryState"],
                "delivered",
            )
            self.assertEqual(
                storage.read_task_event("task:w1-p3-bc").data["worldMessageDeliveryState"],
                "prepared",
            )
            self.assertEqual(b.deliveries, 1)
            self.assertEqual(c.deliveries, 0)

    def test_partial_federation_converges_forward_after_host_restart_without_global_head(
        self,
    ) -> None:
        b = DurableInbox(WORLD_B)
        c = DurableInbox(WORLD_C)
        c.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(92_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(storage, clock_ms=clock, owner_id="host:w1-p3:first")
                create_task(kernel, "task:w1-p3-ab")
                create_task(kernel, "task:w1-p3-bc")
                port = HostExtensionPort(storage, kernel)
                ab = HostMessageDeliveryJournal(port)
                bc = HostMessageDeliveryJournal(port)
                ab.prepare("task:w1-p3-ab", first_hop())
                up = ab.deliver("task:w1-p3-ab", b).receipt
                bc.prepare("task:w1-p3-bc", second_hop(up))
                self.assertEqual(bc.deliver("task:w1-p3-bc", c).status, "unknown")
                self.assertEqual(b.deliveries, 1)
                self.assertEqual(c.deliveries, 1)
            with HostStorage(directory) as reopened:
                kernel = HostKernel(reopened, clock_ms=clock, owner_id="host:w1-p3:fresh")
                port = HostExtensionPort(reopened, kernel)
                ab = HostMessageDeliveryJournal(port)
                bc = HostMessageDeliveryJournal(port)
                up = ab.load_receipt("task:w1-p3-ab")
                recovered = bc.reconcile("task:w1-p3-bc", c)
                self.assertEqual(recovered.status, "delivered")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(b.deliveries, 1)
                self.assertEqual(c.deliveries, 1)
                self.assertEqual(
                    bc.load_bundle("task:w1-p3-bc").provenance["upstreamReceiptDigest"],
                    sha256_digest(up.to_dict()),
                )
                for task_id in ("task:w1-p3-ab", "task:w1-p3-bc"):
                    data = reopened.read_task_event(task_id).data
                    self.assertNotIn("worldFederationRevision", data)
                    self.assertNotIn("worldGlobalHead", data)

    def test_relay_origin_is_provenance_claim_not_native_c_authority(self) -> None:
        b = DurableInbox(WORLD_B)
        c = DurableInbox(WORLD_C)
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(93_000).__next__, owner_id="host:w1-p3"
            )
            create_task(kernel, "task:w1-p3-ab")
            create_task(kernel, "task:w1-p3-bc")
            port = HostExtensionPort(storage, kernel)
            ab = HostMessageDeliveryJournal(port)
            bc = HostMessageDeliveryJournal(port)
            ab.prepare("task:w1-p3-ab", first_hop())
            up = ab.deliver("task:w1-p3-ab", b).receipt
            relayed = second_hop(up)
            forged_origin = MessageDeliveryBundle.create(
                message_id=relayed.plan.message_id,
                source_world_id=relayed.plan.source_world_id,
                destination_world_id=relayed.plan.destination_world_id,
                message_kind=relayed.plan.message_kind,
                provenance={**relayed.provenance, "originWorldClaim": "world-instance:FAKE"},
                payload=relayed.payload,
            )
            bc.prepare("task:w1-p3-bc", forged_origin)
            receipt = bc.deliver("task:w1-p3-bc", c).receipt
            self.assertEqual(receipt.destination_evidence["nativeSourceWorldId"], WORLD_B)
            self.assertEqual(forged_origin.provenance["originWorldClaim"], "world-instance:FAKE")
            self.assertFalse(receipt.destination_evidence["knowledgePromoted"])


if __name__ == "__main__":
    unittest.main()
