from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world.canonical import sha256_digest
from ordivon_world.entity_migration import (
    EntityMigrationBundle,
    EntityMigrationError,
    EntityMigrationOutcomeUnknown,
    EntityMigrationReceipt,
    EntityMigrationSuperseded,
    HostEntityMigrationJournal,
    PreparedEntityMigration,
)


def departure() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "station-zero-v3-entity-departure",
        "sourceWorldId": "game-run:w1:B-source",
        "entityId": "medic-reyes",
        "recordDigest": "3" * 64,
        "factId": "fact:w1:actor_life_state_changed",
        "fromLifeState": "active",
        "toLifeState": "extracted",
    }


def continuity() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.w1.identity-continuity",
        "entityId": "medic-reyes",
        "memory": {"note": "continue mission context without local Game state"},
    }


def bundle(
    *, migration_id: str = "migration:w1:medic-reyes", body: dict[str, object] | None = None
) -> EntityMigrationBundle:
    return EntityMigrationBundle.create(
        migration_id=migration_id,
        entity_id="medic-reyes",
        source_world_id="game-run:w1:B-source",
        destination_world_id="security-world:w1:B-destination",
        source_departure=departure(),
        continuity_payload=continuity() if body is None else body,
    )


class DurableDestination:
    def __init__(self) -> None:
        self.receipts: dict[str, EntityMigrationReceipt] = {}
        self.materializations = 0
        self.drop_after_commit = False
        self.override_receipt: EntityMigrationReceipt | None = None

    def materialize(self, value: EntityMigrationBundle) -> EntityMigrationReceipt:
        retained = self.receipts.get(value.plan.migration_id)
        if retained is not None:
            return retained
        self.materializations += 1
        receipt = self.override_receipt or EntityMigrationReceipt(
            migration_id=value.plan.migration_id,
            plan_digest=value.plan.digest,
            entity_id=value.plan.entity_id,
            destination_world_id=value.plan.destination_world_id,
            source_departure_digest=value.plan.source_departure_digest,
            materialization_id="process:test-destination:4242",
            materialization_digest=sha256_digest({"pid": 4242, "entityId": value.plan.entity_id}),
            destination_evidence={"authority": "test-destination-local", "bodyStarted": True},
        )
        self.receipts[value.plan.migration_id] = receipt
        if self.drop_after_commit:
            self.drop_after_commit = False
            raise EntityMigrationOutcomeUnknown(
                value.plan, RuntimeError("response lost after destination body start")
            )
        return receipt

    def reconcile(self, plan: PreparedEntityMigration) -> EntityMigrationReceipt | None:
        return self.receipts.get(plan.migration_id)


class HostEntityMigrationTests(unittest.TestCase):
    def create_task(self, storage: HostStorage, kernel: HostKernel):
        return kernel.create_task(
            event_id="event:w1-entity:create",
            kind=EventKind.TASK_CREATED,
            task_id="task:w1-entity",
            goal_id="goal:w1-entity",
            payload={"scenario": "w1-entity-migration"},
            frontier=("node:w1-entity",),
        ).projection

    def test_prepare_retains_departure_continuity_and_plan_without_changing_task_meaning(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(10_000).__next__, owner_id="host:w1-entity"
            )
            created = self.create_task(storage, kernel)
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            first = journal.prepare(created.task_id, bundle())
            second = journal.prepare(created.task_id, bundle())
            loaded = journal.load_bundle(created.task_id)
            self.assertEqual(first.status, "prepared")
            self.assertEqual(second.task_revision, first.task_revision)
            self.assertEqual(loaded, bundle())
            snapshot = storage.read_task_event(created.task_id)
            self.assertEqual(snapshot.projection.state, created.state)
            self.assertEqual(snapshot.projection.ready_frontier, created.ready_frontier)
            self.assertEqual(snapshot.data["worldEntityId"], "medic-reyes")
            self.assertNotEqual(
                snapshot.data["worldEntityMigrationPlanObjectDigest"], loaded.plan.digest
            )

    def test_response_loss_reopens_host_and_reconciles_without_second_body(self) -> None:
        destination = DurableDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(20_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(storage, clock_ms=clock, owner_id="host:w1-entity:first")
                created = self.create_task(storage, kernel)
                journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
                journal.prepare(created.task_id, bundle())
                unknown = journal.materialize(created.task_id, destination)
                self.assertEqual(unknown.status, "unknown")
                self.assertEqual(destination.materializations, 1)
            with HostStorage(directory) as reopened:
                kernel = HostKernel(reopened, clock_ms=clock, owner_id="host:w1-entity:fresh")
                journal = HostEntityMigrationJournal(HostExtensionPort(reopened, kernel))
                recovered = journal.reconcile("task:w1-entity", destination)
                self.assertEqual(recovered.status, "materialized")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(destination.materializations, 1)
                self.assertNotIn(
                    "worldEntityMigrationUncertaintyObjectDigest",
                    reopened.read_task_event("task:w1-entity").data,
                )

    def test_known_receipt_prevents_second_destination_body(self) -> None:
        destination = DurableDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(30_000).__next__, owner_id="host:w1-entity"
            )
            created = self.create_task(storage, kernel)
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            self.assertEqual(
                journal.materialize(created.task_id, destination).status, "materialized"
            )
            self.assertEqual(
                journal.materialize(created.task_id, destination).status, "materialized"
            )
            self.assertEqual(destination.materializations, 1)

    def test_same_task_cannot_change_entity_migration_or_continuity(self) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(40_000).__next__, owner_id="host:w1-entity"
            )
            created = self.create_task(storage, kernel)
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            with self.assertRaises(EntityMigrationSuperseded):
                journal.prepare(created.task_id, bundle(migration_id="migration:w1:other"))
            with self.assertRaises(EntityMigrationSuperseded):
                journal.prepare(created.task_id, bundle(body=continuity() | {"entityId": "other"}))

    def test_receipt_wrong_entity_is_rejected_before_host_commit(self) -> None:
        destination = DurableDestination()
        good = bundle()
        destination.override_receipt = EntityMigrationReceipt(
            migration_id=good.plan.migration_id,
            plan_digest=good.plan.digest,
            entity_id="other",
            destination_world_id=good.plan.destination_world_id,
            source_departure_digest=good.plan.source_departure_digest,
            materialization_id="process:wrong",
            materialization_digest="sha256:" + "4" * 64,
            destination_evidence={"authority": "test"},
        )
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(50_000).__next__, owner_id="host:w1-entity"
            )
            created = self.create_task(storage, kernel)
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, good)
            with self.assertRaises(EntityMigrationSuperseded):
                journal.materialize(created.task_id, destination)
            self.assertEqual(
                storage.read_task_event(created.task_id).data["worldEntityMigrationState"],
                "prepared",
            )

    def test_unknown_state_forbids_blind_rematerialization_after_destination_receipt_loss(
        self,
    ) -> None:
        destination = DurableDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(55_000).__next__, owner_id="host:w1-p1-entity"
            )
            created = self.create_task(storage, kernel)
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            self.assertEqual(journal.materialize(created.task_id, destination).status, "unknown")
            self.assertEqual(destination.materializations, 1)
            destination.receipts.clear()
            with self.assertRaises(EntityMigrationError):
                journal.materialize(created.task_id, destination)
            self.assertEqual(destination.materializations, 1)
            self.assertEqual(
                storage.read_task_event(created.task_id).data["worldEntityMigrationState"],
                "unknown",
            )

    def test_bundle_tamper_fails_before_destination(self) -> None:
        valid = bundle()
        with self.assertRaises(ValueError):
            EntityMigrationBundle(
                plan=valid.plan,
                source_departure=departure() | {"entityId": "other"},
                continuity_payload=valid.continuity_payload,
            )
        with self.assertRaises(ValueError):
            EntityMigrationBundle(
                plan=valid.plan,
                source_departure=valid.source_departure,
                continuity_payload=continuity() | {"localAuthority": "copied"},
            )


if __name__ == "__main__":
    unittest.main()
