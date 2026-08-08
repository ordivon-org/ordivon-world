from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world import (
    ResourceEgressAuthority,
    ResourceEgressReceipt,
    ResourceTransferBundle,
    ResourceTransferNotCommitted,
    ResourceTransferReceipt,
)
from ordivon_world.canonical import sha256_digest
from ordivon_world.resource_transfer import (
    HostResourceTransferJournal,
    ResourceTransferError,
    ResourceTransferOutcomeUnknown,
)


def bundle(index: int) -> ResourceTransferBundle:
    payload = {"kind": "portable-resource", "index": index}
    occurrence = {"factId": f"fact:w2-p4:{index}"}
    egress = ResourceEgressReceipt(
        transfer_id=f"transfer:w2-p4:{index}",
        source_world_id=f"world:w2-p4:source:{index}",
        destination_world_id="world:w2-p4:destination",
        resource_kind="test-resource",
        payload_digest=sha256_digest(payload),
        source_occurrence_id=f"resource-occurrence:w2-p4:{index}",
        source_occurrence_digest=sha256_digest(occurrence),
        authority=ResourceEgressAuthority(
            authority_id=f"source-authority:w2-p4:{index}",
            mechanism="test-source-egress.v1",
            evidence=occurrence,
        ),
    )
    return ResourceTransferBundle.create(source_egress=egress, payload=payload)


class PartialDestination:
    def __init__(self, unknown_transfer_id: str) -> None:
        self.unknown_transfer_id = unknown_transfer_id
        self.first_unknown = True
        self.receipts: dict[str, ResourceTransferReceipt] = {}
        self.materialize_calls: list[str] = []

    def materialize(self, value: ResourceTransferBundle) -> ResourceTransferReceipt:
        self.materialize_calls.append(value.plan.transfer_id)
        retained = self.receipts.get(value.plan.transfer_id)
        if retained is not None:
            return retained
        if value.plan.transfer_id == self.unknown_transfer_id and self.first_unknown:
            self.first_unknown = False
            raise ResourceTransferOutcomeUnknown(
                value.plan,
                RuntimeError("destination failed before semantic admission"),
            )
        receipt = ResourceTransferReceipt(
            transfer_id=value.plan.transfer_id,
            plan_digest=value.plan.digest,
            destination_world_id=value.plan.destination_world_id,
            payload_digest=value.plan.payload_digest,
            materialization_id=f"resource:{value.plan.transfer_id}",
            materialization_digest=sha256_digest(
                {"transferId": value.plan.transfer_id, "admitted": True}
            ),
            destination_evidence={"authority": "w2-p4-destination"},
        )
        self.receipts[value.plan.transfer_id] = receipt
        return receipt

    def reconcile(self, plan):
        retained = self.receipts.get(plan.transfer_id)
        if retained is not None:
            return retained
        if plan.transfer_id == self.unknown_transfer_id:
            return ResourceTransferNotCommitted(
                transfer_id=plan.transfer_id,
                plan_digest=plan.digest,
                destination_world_id=plan.destination_world_id,
                payload_digest=plan.payload_digest,
                evidence={
                    "authority": "w2-p4-destination",
                    "exactOriginalRetrySafe": True,
                },
            )
        return None


class W2MultiResourceTaskTests(unittest.TestCase):
    def test_one_task_retains_independent_resource_trajectories_and_partial_recovery(self) -> None:
        first = bundle(1)
        second = bundle(2)
        destination = PartialDestination(second.plan.transfer_id)
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=itertools.count(1_600_000).__next__,
                owner_id="host:w2-p4",
            )
            created = kernel.create_task(
                event_id="event:w2-p4:create",
                kind=EventKind.TASK_CREATED,
                task_id="task:w2-p4",
                goal_id="goal:w2-p4",
                payload={"goal": "move two independent resources"},
                frontier=("node:w2-p4",),
            ).projection
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))

            journal.prepare(created.task_id, first)
            first_done = journal.deliver(created.task_id, destination)
            journal.prepare(created.task_id, second)
            second_unknown = journal.deliver(
                created.task_id,
                destination,
                transfer_id=second.plan.transfer_id,
            )
            self.assertEqual(first_done.status, "materialized")
            self.assertEqual(second_unknown.status, "unknown")
            self.assertEqual(
                journal.transfer_ids(created.task_id),
                tuple(sorted((first.plan.transfer_id, second.plan.transfer_id))),
            )

            with self.assertRaises(ResourceTransferError):
                journal.load_bundle(created.task_id)
            with self.assertRaises(ResourceTransferError):
                journal.deliver(created.task_id, destination)

            snapshot = storage.read_task_event(created.task_id)
            entries = snapshot.data["worldResourceTransfers"]
            self.assertEqual(
                entries[first.plan.transfer_id]["worldResourceTransferState"],
                "materialized",
            )
            self.assertEqual(
                entries[second.plan.transfer_id]["worldResourceTransferState"],
                "unknown",
            )
            first_receipt_before = journal.load_receipt(created.task_id, first.plan.transfer_id)

            second_released = journal.reconcile(
                created.task_id,
                destination,
                transfer_id=second.plan.transfer_id,
            )
            self.assertEqual(second_released.status, "prepared")
            snapshot = storage.read_task_event(created.task_id)
            entries = snapshot.data["worldResourceTransfers"]
            self.assertEqual(
                entries[first.plan.transfer_id]["worldResourceTransferState"],
                "materialized",
            )
            self.assertEqual(
                entries[second.plan.transfer_id]["worldResourceTransferState"],
                "prepared",
            )
            self.assertIn(
                "worldResourceTransferNotCommittedDigest",
                entries[second.plan.transfer_id],
            )
            self.assertNotIn(
                "worldResourceTransferNotCommittedDigest",
                entries[first.plan.transfer_id],
            )

            second_done = journal.deliver(
                created.task_id,
                destination,
                transfer_id=second.plan.transfer_id,
            )
            self.assertEqual(second_done.status, "materialized")
            self.assertEqual(
                journal.load_receipt(created.task_id, first.plan.transfer_id),
                first_receipt_before,
            )
            self.assertEqual(
                journal.load_receipt(created.task_id, second.plan.transfer_id),
                second_done.receipt,
            )
            snapshot = storage.read_task_event(created.task_id)
            self.assertEqual(snapshot.projection.state, created.state)
            self.assertEqual(snapshot.projection.ready_frontier, created.ready_frontier)
            self.assertEqual(
                [
                    first.plan.transfer_id,
                    second.plan.transfer_id,
                    second.plan.transfer_id,
                ],
                destination.materialize_calls,
            )


if __name__ == "__main__":
    unittest.main()
