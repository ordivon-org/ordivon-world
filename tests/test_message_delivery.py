from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world.canonical import sha256_digest
from ordivon_world.message_delivery import (
    HostMessageDeliveryJournal,
    MessageDeliveryBundle,
    MessageDeliveryError,
    MessageDeliveryOutcomeUnknown,
    MessageDeliveryReceipt,
    MessageDeliverySuperseded,
    PreparedMessageDelivery,
)


def provenance() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.w1.message-provenance",
        "originWorldId": "world-instance:w1-message:A",
        "sourceEvidenceRef": "fact:w1-message:claim-1",
    }


def payload() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.w1.message-payload",
        "claim": {"subject": "reactor", "state": "unstable"},
        "sourceConfidence": "confirmed-in-source-world",
    }


def bundle(
    *, message_id: str = "message:w1:claim-1", body: dict[str, object] | None = None
) -> MessageDeliveryBundle:
    return MessageDeliveryBundle.create(
        message_id=message_id,
        source_world_id="world-instance:w1-message:A",
        destination_world_id="world-instance:w1-message:B",
        message_kind="foreign-claim",
        provenance=provenance(),
        payload=payload() if body is None else body,
    )


class InboxDestination:
    def __init__(self) -> None:
        self.receipts: dict[str, MessageDeliveryReceipt] = {}
        self.inbox: dict[str, str] = {}
        self.knowledge: dict[str, object] = {}
        self.deliveries = 0
        self.drop_after_commit = False
        self.override_receipt: MessageDeliveryReceipt | None = None

    def deliver(self, value: MessageDeliveryBundle) -> MessageDeliveryReceipt:
        retained = self.receipts.get(value.plan.message_id)
        if retained is not None:
            return retained
        self.deliveries += 1
        self.inbox[value.plan.message_id] = value.plan.payload_digest
        receipt = self.override_receipt or MessageDeliveryReceipt(
            message_id=value.plan.message_id,
            plan_digest=value.plan.digest,
            destination_world_id=value.plan.destination_world_id,
            payload_digest=value.plan.payload_digest,
            delivery_id=f"inbox:{value.plan.message_id}",
            delivery_digest=sha256_digest(
                {
                    "messageId": value.plan.message_id,
                    "sequence": self.deliveries,
                    "payloadDigest": value.plan.payload_digest,
                }
            ),
            destination_evidence={
                "authority": "test-destination-inbox",
                "acceptedSequence": self.deliveries,
                "knowledgePromoted": False,
            },
        )
        self.receipts[value.plan.message_id] = receipt
        if self.drop_after_commit:
            self.drop_after_commit = False
            raise MessageDeliveryOutcomeUnknown(
                value.plan, RuntimeError("response lost after destination inbox commit")
            )
        return receipt

    def reconcile(self, plan: PreparedMessageDelivery) -> MessageDeliveryReceipt | None:
        return self.receipts.get(plan.message_id)


class HostMessageDeliveryTests(unittest.TestCase):
    def create_task(self, storage: HostStorage, kernel: HostKernel):
        return kernel.create_task(
            event_id="event:w1-message:create",
            kind=EventKind.TASK_CREATED,
            task_id="task:w1-message",
            goal_id="goal:w1-message",
            payload={"scenario": "w1-message-delivery"},
            frontier=("node:w1-message",),
        ).projection

    def test_prepare_retains_provenance_payload_and_plan_without_changing_task_meaning(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(80_000).__next__, owner_id="host:w1-message"
            )
            created = self.create_task(storage, kernel)
            journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
            first = journal.prepare(created.task_id, bundle())
            second = journal.prepare(created.task_id, bundle())
            loaded = journal.load_bundle(created.task_id)
            self.assertEqual(first.status, "prepared")
            self.assertEqual(second.task_revision, first.task_revision)
            self.assertEqual(loaded, bundle())
            snapshot = storage.read_task_event(created.task_id)
            self.assertEqual(snapshot.projection.state, created.state)
            self.assertEqual(snapshot.projection.ready_frontier, created.ready_frontier)
            self.assertEqual(snapshot.data["worldMessageDeliveryState"], "prepared")
            self.assertNotEqual(
                snapshot.data["worldMessagePayloadObjectDigest"], loaded.plan.payload_digest
            )

    def test_response_loss_reopens_host_and_reconciles_delivery_without_second_send(self) -> None:
        destination = InboxDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(81_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(storage, clock_ms=clock, owner_id="host:w1-message:first")
                created = self.create_task(storage, kernel)
                journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
                journal.prepare(created.task_id, bundle())
                self.assertEqual(journal.deliver(created.task_id, destination).status, "unknown")
                self.assertEqual(destination.deliveries, 1)
            with HostStorage(directory) as reopened:
                kernel = HostKernel(reopened, clock_ms=clock, owner_id="host:w1-message:fresh")
                journal = HostMessageDeliveryJournal(HostExtensionPort(reopened, kernel))
                recovered = journal.reconcile("task:w1-message", destination)
                self.assertEqual(recovered.status, "delivered")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(destination.deliveries, 1)
                snapshot = reopened.read_task_event("task:w1-message")
                self.assertEqual(snapshot.data["worldMessageDeliveryState"], "delivered")
                self.assertEqual(snapshot.event_kind, EventKind("world.message-delivery-delivered"))

    def test_delivery_does_not_promote_foreign_claim_to_destination_knowledge(self) -> None:
        destination = InboxDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(82_000).__next__, owner_id="host:w1-message"
            )
            created = self.create_task(storage, kernel)
            journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            delivered = journal.deliver(created.task_id, destination)
            self.assertEqual(delivered.status, "delivered")
            self.assertIn(bundle().plan.message_id, destination.inbox)
            self.assertEqual(destination.knowledge, {})
            self.assertFalse(delivered.receipt.destination_evidence["knowledgePromoted"])

    def test_known_delivery_receipt_prevents_second_send(self) -> None:
        destination = InboxDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(83_000).__next__, owner_id="host:w1-message"
            )
            created = self.create_task(storage, kernel)
            journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            self.assertEqual(journal.deliver(created.task_id, destination).status, "delivered")
            self.assertEqual(journal.deliver(created.task_id, destination).status, "delivered")
            self.assertEqual(destination.deliveries, 1)

    def test_same_message_identity_cannot_change_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(84_000).__next__, owner_id="host:w1-message"
            )
            created = self.create_task(storage, kernel)
            journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            with self.assertRaises(MessageDeliverySuperseded):
                journal.prepare(
                    created.task_id, bundle(body=payload() | {"sourceConfidence": "changed"})
                )

    def test_wrong_payload_receipt_is_rejected_before_host_delivery_finality(self) -> None:
        destination = InboxDestination()
        good = bundle()
        destination.override_receipt = MessageDeliveryReceipt(
            message_id=good.plan.message_id,
            plan_digest=good.plan.digest,
            destination_world_id=good.plan.destination_world_id,
            payload_digest="sha256:" + "0" * 64,
            delivery_id="inbox:wrong",
            delivery_digest="sha256:" + "2" * 64,
            destination_evidence={"authority": "test"},
        )
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(85_000).__next__, owner_id="host:w1-message"
            )
            created = self.create_task(storage, kernel)
            journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, good)
            with self.assertRaises(MessageDeliverySuperseded):
                journal.deliver(created.task_id, destination)
            self.assertEqual(
                storage.read_task_event(created.task_id).data["worldMessageDeliveryState"],
                "prepared",
            )

    def test_unknown_message_delivery_forbids_blind_redelivery_after_receipt_loss(self) -> None:
        destination = InboxDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(86_000).__next__, owner_id="host:w1-message"
            )
            created = self.create_task(storage, kernel)
            journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            self.assertEqual(journal.deliver(created.task_id, destination).status, "unknown")
            destination.receipts.clear()
            with self.assertRaises(MessageDeliveryError):
                journal.deliver(created.task_id, destination)
            self.assertEqual(destination.deliveries, 1)
            self.assertEqual(journal.reconcile(created.task_id, destination).status, "unknown")

    def test_bundle_tamper_fails_before_destination(self) -> None:
        valid = bundle()
        with self.assertRaises(ValueError):
            MessageDeliveryBundle(
                plan=valid.plan,
                provenance=provenance() | {"originWorldId": "world-instance:fake"},
                payload=valid.payload,
            )
        with self.assertRaises(ValueError):
            MessageDeliveryBundle(
                plan=valid.plan,
                provenance=valid.provenance,
                payload=payload() | {"claim": {"subject": "reactor", "state": "stable"}},
            )


if __name__ == "__main__":
    unittest.main()
