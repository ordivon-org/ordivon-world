from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage
from ordivon_world.entity_migration import EntityMigrationError, HostEntityMigrationJournal
from ordivon_world.message_delivery import HostMessageDeliveryJournal
from tests.test_entity_migration import DurableDestination as EntityDestination
from tests.test_entity_migration import bundle as entity_bundle
from tests.test_message_delivery import InboxDestination, bundle as message_bundle


class AM6EntityThresholdTests(unittest.TestCase):
    """Distinguish cognition/message helpers from independently persistent Entities."""

    @staticmethod
    def _create(kernel: HostKernel, task_id: str) -> None:
        token = task_id.removeprefix("task:")
        kernel.create_task(
            event_id=f"event:{token}:create",
            kind=EventKind.TASK_CREATED,
            task_id=task_id,
            goal_id=f"goal:{token}",
            payload={"scenario": "AM6 entity threshold"},
            frontier=(f"node:{token}",),
        )

    def test_internal_helper_output_can_cross_world_as_message_without_becoming_entity(self) -> None:
        destination = InboxDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(storage, clock_ms=itertools.count(300_000).__next__, owner_id="am6")
            self._create(kernel, "task:am6-helper")
            journal = HostMessageDeliveryJournal(HostExtensionPort(storage, kernel))
            value = message_bundle(message_id="message:am6:critic-output")
            journal.prepare("task:am6-helper", value)
            delivered = journal.deliver("task:am6-helper", destination)
            self.assertEqual(delivered.status, "delivered")
            self.assertEqual(destination.knowledge, {})
            snapshot = storage.read_task_event("task:am6-helper")
            self.assertIn("worldMessageDeliveries", snapshot.data)
            self.assertNotIn("worldEntityMigrationState", snapshot.data)
            self.assertNotIn("worldEntityId", snapshot.data)

    def test_persistent_actor_cross_world_requires_explicit_entity_identity_and_continuity(self) -> None:
        destination = EntityDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(storage, clock_ms=itertools.count(310_000).__next__, owner_id="am6")
            self._create(kernel, "task:am6-entity")
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            value = entity_bundle(migration_id="migration:am6:medic-reyes")
            prepared = journal.prepare("task:am6-entity", value)
            self.assertEqual(prepared.status, "prepared")
            materialized = journal.materialize("task:am6-entity", destination)
            self.assertEqual(materialized.status, "materialized")
            self.assertEqual(materialized.receipt.entity_id, value.plan.entity_id)
            self.assertEqual(
                materialized.receipt.source_departure_digest,
                value.plan.source_departure_digest,
            )
            snapshot = storage.read_task_event("task:am6-entity")
            self.assertEqual(snapshot.data["worldEntityId"], value.plan.entity_id)
            self.assertIn("worldEntityContinuityPayloadDigest", snapshot.data)
            self.assertNotEqual(
                snapshot.data["worldEntityContinuityPayloadObjectDigest"],
                snapshot.data["worldEntityContinuityPayloadDigest"],
            )

    def test_message_delivery_does_not_satisfy_entity_continuity_requirements(self) -> None:
        """A helper's information can be portable without giving the helper Presence."""
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(storage, clock_ms=itertools.count(320_000).__next__, owner_id="am6")
            self._create(kernel, "task:am6-both")
            port = HostExtensionPort(storage, kernel)
            message = HostMessageDeliveryJournal(port)
            message.prepare("task:am6-both", message_bundle(message_id="message:am6:planner"))
            message.deliver("task:am6-both", InboxDestination())
            snapshot = storage.read_task_event("task:am6-both")
            self.assertNotIn("worldEntityId", snapshot.data)
            with self.assertRaises(EntityMigrationError):
                HostEntityMigrationJournal(port).load_bundle("task:am6-both")


if __name__ == "__main__":
    unittest.main()
