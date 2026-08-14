from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage
from ordivon_world.entity_migration import EntityMigrationError, HostEntityMigrationJournal
from ordivon_world.message_delivery import HostMessageDeliveryJournal, MessageDeliveryError
from ordivon_world.resource_transfer import HostResourceTransferJournal, ResourceTransferError
from tests.test_entity_migration import DurableDestination as EntityDestination
from tests.test_entity_migration import bundle as entity_bundle
from tests.test_message_delivery import InboxDestination
from tests.test_message_delivery import bundle as message_bundle
from tests.test_resource_transfer import DurableDestination as ResourceDestination
from tests.test_resource_transfer import ProvenNotCommittedDestination
from tests.test_resource_transfer import bundle as resource_bundle


class AM3MorphologyRelationContinuityTests(unittest.TestCase):
    """World relation truth must survive replacement of the acting controller.

    The old/fresh Host owner ids stand in for distinct cognition/morphology
    instances.  World trajectory identity, not process/loop identity, decides what
    may happen after response loss.
    """

    @staticmethod
    def _create_task(
        kernel: HostKernel,
        *,
        task_id: str,
        scenario: str,
    ) -> None:
        token = task_id.removeprefix("task:")
        kernel.create_task(
            event_id=f"event:{token}:create",
            kind=EventKind.TASK_CREATED,
            task_id=task_id,
            goal_id=f"goal:{token}",
            payload={"scenario": scenario},
            frontier=(f"node:{token}",),
        )

    def test_resource_unknown_survives_controller_replacement_and_reconciles_once(self) -> None:
        destination = ResourceDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(100_000).__next__
            with HostStorage(directory) as storage:
                first = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-a")
                self._create_task(first, task_id="task:am3-resource", scenario="AM3 resource")
                journal = HostResourceTransferJournal(HostExtensionPort(storage, first))
                journal.prepare("task:am3-resource", resource_bundle())
                self.assertEqual(journal.deliver("task:am3-resource", destination).status, "unknown")
                self.assertEqual(destination.materializations, 1)
            with HostStorage(directory) as storage:
                replacement = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-b")
                journal = HostResourceTransferJournal(HostExtensionPort(storage, replacement))
                with self.assertRaises(ResourceTransferError):
                    journal.deliver("task:am3-resource", destination)
                recovered = journal.reconcile("task:am3-resource", destination)
                self.assertEqual(recovered.status, "materialized")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(destination.materializations, 1)

    def test_message_unknown_survives_controller_replacement_and_reconciles_once(self) -> None:
        destination = InboxDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(110_000).__next__
            with HostStorage(directory) as storage:
                first = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-a")
                self._create_task(first, task_id="task:am3-message", scenario="AM3 message")
                journal = HostMessageDeliveryJournal(HostExtensionPort(storage, first))
                journal.prepare("task:am3-message", message_bundle())
                self.assertEqual(journal.deliver("task:am3-message", destination).status, "unknown")
                self.assertEqual(destination.deliveries, 1)
            with HostStorage(directory) as storage:
                replacement = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-b")
                journal = HostMessageDeliveryJournal(HostExtensionPort(storage, replacement))
                with self.assertRaises(MessageDeliveryError):
                    journal.deliver("task:am3-message", destination)
                recovered = journal.reconcile("task:am3-message", destination)
                self.assertEqual(recovered.status, "delivered")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(destination.deliveries, 1)
                self.assertEqual(destination.knowledge, {})

    def test_entity_unknown_survives_controller_replacement_without_second_body(self) -> None:
        destination = EntityDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(120_000).__next__
            with HostStorage(directory) as storage:
                first = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-a")
                self._create_task(first, task_id="task:am3-entity", scenario="AM3 entity")
                journal = HostEntityMigrationJournal(HostExtensionPort(storage, first))
                journal.prepare("task:am3-entity", entity_bundle())
                self.assertEqual(journal.materialize("task:am3-entity", destination).status, "unknown")
                self.assertEqual(destination.materializations, 1)
            with HostStorage(directory) as storage:
                replacement = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-b")
                journal = HostEntityMigrationJournal(HostExtensionPort(storage, replacement))
                with self.assertRaises(EntityMigrationError):
                    journal.materialize("task:am3-entity", destination)
                recovered = journal.reconcile("task:am3-entity", destination)
                self.assertEqual(recovered.status, "materialized")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(destination.materializations, 1)

    def test_exact_not_committed_proof_releases_unknown_across_replacement(self) -> None:
        destination = ProvenNotCommittedDestination()
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(130_000).__next__
            with HostStorage(directory) as storage:
                first = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-a")
                self._create_task(first, task_id="task:am3-release", scenario="AM3 release")
                journal = HostResourceTransferJournal(HostExtensionPort(storage, first))
                journal.prepare("task:am3-release", resource_bundle())
                self.assertEqual(journal.deliver("task:am3-release", destination).status, "unknown")
                self.assertEqual(destination.materializations, 1)
            with HostStorage(directory) as storage:
                replacement = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-b")
                journal = HostResourceTransferJournal(HostExtensionPort(storage, replacement))
                released = journal.reconcile("task:am3-release", destination)
                self.assertEqual(released.status, "prepared")
                self.assertTrue(released.reconciled)
                self.assertTrue(destination.proof_issued)
                completed = journal.deliver("task:am3-release", destination)
                self.assertEqual(completed.status, "materialized")
                self.assertEqual(destination.materializations, 2)


if __name__ == "__main__":
    unittest.main()
