from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage
from ordivon_world.resource_transfer import HostResourceTransferJournal
from ordivon_world.task_inspection import WorldTaskInspector
from tests.test_resource_transfer import DurableDestination, ProvenNotCommittedDestination, bundle


class E5ReplacementReadinessTests(unittest.TestCase):
    @staticmethod
    def _create(kernel: HostKernel, task_id: str) -> None:
        token = task_id.removeprefix("task:")
        kernel.create_task(
            event_id=f"event:{token}:create",
            kind=EventKind.TASK_CREATED,
            task_id=task_id,
            goal_id=f"goal:{token}",
            payload={"scenario": "E5 replacement readiness"},
            frontier=(f"node:{token}",),
        )

    def test_prepared_is_replaceable_but_readiness_grants_no_action(self) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(storage, clock_ms=itertools.count(400_000).__next__, owner_id="e5")
            self._create(kernel, "task:e5-prepared")
            port = HostExtensionPort(storage, kernel)
            prepared = HostResourceTransferJournal(port).prepare("task:e5-prepared", bundle())
            value = WorldTaskInspector(port).inspect_replacement_readiness(
                "task:e5-prepared", expected_revision=prepared.task_revision
            )
            self.assertTrue(value["replaceable"])
            self.assertEqual(value["reconciliationBlockers"], [])
            self.assertEqual(value["actionAuthority"], "not-granted-by-inspection")
            self.assertEqual(value["externalCurrentness"], "not-claimed")

    def test_unknown_blocks_until_original_relation_is_reconciled(self) -> None:
        destination = DurableDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(storage, clock_ms=itertools.count(410_000).__next__, owner_id="e5")
            self._create(kernel, "task:e5-unknown")
            port = HostExtensionPort(storage, kernel)
            journal = HostResourceTransferJournal(port)
            journal.prepare("task:e5-unknown", bundle())
            unknown = journal.deliver("task:e5-unknown", destination)
            blocked = WorldTaskInspector(port).inspect_replacement_readiness(
                "task:e5-unknown", expected_revision=unknown.task_revision
            )
            self.assertFalse(blocked["replaceable"])
            self.assertEqual(len(blocked["reconciliationBlockers"]), 1)
            recovered = journal.reconcile("task:e5-unknown", destination)
            clear = WorldTaskInspector(port).inspect_replacement_readiness(
                "task:e5-unknown", expected_revision=recovered.task_revision
            )
            self.assertTrue(clear["replaceable"])

    def test_not_committed_release_clears_blocker_without_granting_retry(self) -> None:
        destination = ProvenNotCommittedDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(storage, clock_ms=itertools.count(420_000).__next__, owner_id="e5")
            self._create(kernel, "task:e5-release")
            port = HostExtensionPort(storage, kernel)
            journal = HostResourceTransferJournal(port)
            journal.prepare("task:e5-release", bundle())
            unknown = journal.deliver("task:e5-release", destination)
            self.assertFalse(WorldTaskInspector(port).inspect_replacement_readiness(
                "task:e5-release", expected_revision=unknown.task_revision
            )["replaceable"])
            released = journal.reconcile("task:e5-release", destination)
            value = WorldTaskInspector(port).inspect_replacement_readiness(
                "task:e5-release", expected_revision=released.task_revision
            )
            self.assertTrue(value["replaceable"])
            self.assertEqual(value["actionAuthority"], "not-granted-by-inspection")


if __name__ == "__main__":
    unittest.main()
