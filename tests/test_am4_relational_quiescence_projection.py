from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage
from ordivon_world.resource_transfer import HostResourceTransferJournal
from ordivon_world.task_inspection import WorldTaskInspector
from tests.test_resource_transfer import DurableDestination, ProvenNotCommittedDestination, bundle


def morphology_replacement_projection(inspection: dict[str, object]) -> dict[str, object]:
    """Research-only derived projection; it grants no action authority."""

    commitments = inspection["commitments"]
    assert isinstance(commitments, list)
    blockers: list[dict[str, object]] = []
    for commitment in commitments:
        assert isinstance(commitment, dict)
        operation = commitment.get("nextOwnerOperation")
        if isinstance(operation, str) and operation.startswith("reconcile-"):
            blockers.append(
                {
                    "family": commitment["family"],
                    "identity": commitment["identity"],
                    "state": commitment["state"],
                    "nextOwnerOperation": operation,
                }
            )
    return {
        "safeToReplaceCognitionController": not blockers,
        "reconciliationBlockers": blockers,
        "actionAuthority": "not-granted-by-derived-projection",
    }


class AM4RelationalQuiescenceProjectionTests(unittest.TestCase):
    @staticmethod
    def _create(kernel: HostKernel, task_id: str) -> None:
        token = task_id.removeprefix("task:")
        kernel.create_task(
            event_id=f"event:{token}:create",
            kind=EventKind.TASK_CREATED,
            task_id=task_id,
            goal_id=f"goal:{token}",
            payload={"scenario": "AM4 relational quiescence"},
            frontier=(f"node:{token}",),
        )

    @staticmethod
    def _projection(port: HostExtensionPort, task_id: str, revision: int) -> dict[str, object]:
        inspection = WorldTaskInspector(port).inspect_task(task_id, expected_revision=revision)
        return morphology_replacement_projection(inspection)

    def test_pre_dispatch_prepared_commitment_is_replaceable_but_grants_no_action(self) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            clock = itertools.count(200_000).__next__
            kernel = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-a")
            self._create(kernel, "task:am4-prepared")
            port = HostExtensionPort(storage, kernel)
            step = HostResourceTransferJournal(port).prepare("task:am4-prepared", bundle())
            projection = self._projection(port, "task:am4-prepared", step.task_revision)
            self.assertTrue(projection["safeToReplaceCognitionController"])
            self.assertEqual(projection["reconciliationBlockers"], [])
            self.assertEqual(projection["actionAuthority"], "not-granted-by-derived-projection")

    def test_unknown_is_a_replacement_blocker_until_original_relation_is_reconciled(self) -> None:
        destination = DurableDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            clock = itertools.count(210_000).__next__
            kernel = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-a")
            self._create(kernel, "task:am4-unknown")
            port = HostExtensionPort(storage, kernel)
            journal = HostResourceTransferJournal(port)
            prepared = journal.prepare("task:am4-unknown", bundle())
            unknown = journal.deliver("task:am4-unknown", destination)
            self.assertGreater(unknown.task_revision, prepared.task_revision)
            blocked = self._projection(port, "task:am4-unknown", unknown.task_revision)
            self.assertFalse(blocked["safeToReplaceCognitionController"])
            self.assertEqual(len(blocked["reconciliationBlockers"]), 1)
            recovered = journal.reconcile("task:am4-unknown", destination)
            clear = self._projection(port, "task:am4-unknown", recovered.task_revision)
            self.assertTrue(clear["safeToReplaceCognitionController"])

    def test_not_committed_release_removes_ambiguity_without_granting_retry(self) -> None:
        destination = ProvenNotCommittedDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            clock = itertools.count(220_000).__next__
            kernel = HostKernel(storage, clock_ms=clock, owner_id="morphology:loop-a")
            self._create(kernel, "task:am4-not-committed")
            port = HostExtensionPort(storage, kernel)
            journal = HostResourceTransferJournal(port)
            journal.prepare("task:am4-not-committed", bundle())
            unknown = journal.deliver("task:am4-not-committed", destination)
            self.assertFalse(
                self._projection(port, "task:am4-not-committed", unknown.task_revision)[
                    "safeToReplaceCognitionController"
                ]
            )
            released = journal.reconcile("task:am4-not-committed", destination)
            projection = self._projection(port, "task:am4-not-committed", released.task_revision)
            self.assertTrue(projection["safeToReplaceCognitionController"])
            self.assertEqual(projection["actionAuthority"], "not-granted-by-derived-projection")


if __name__ == "__main__":
    unittest.main()
