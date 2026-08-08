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
    HostEntityMigrationJournal,
    PreparedEntityMigration,
)
from ordivon_world.resource_transfer import (
    HostResourceTransferJournal,
    PreparedResourceTransfer,
    ResourceTransferBundle,
    ResourceTransferOutcomeUnknown,
    ResourceTransferReceipt,
)


def resource_bundle() -> ResourceTransferBundle:
    evidence = {
        "kind": "station-zero-v3-item-extracted-evidence",
        "sourceWorldId": "game-run:w1-p1:A",
        "recordDigest": "1" * 64,
        "fact": {"factId": "fact:w1-p1:item", "kind": "item_extracted", "itemId": "research-core"},
    }
    payload = {
        "schemaVersion": 1,
        "kind": "ordivon.w1.portable-resource",
        "itemId": "research-core",
    }
    return ResourceTransferBundle.create(
        transfer_id="transfer:w1-p1:resource",
        source_world_id="game-run:w1-p1:A",
        destination_world_id="security-world:w1-p1:B",
        resource_kind="station-zero-v3-item",
        source_evidence=evidence,
        payload=payload,
    )


def entity_bundle() -> EntityMigrationBundle:
    departure = {
        "schemaVersion": 1,
        "kind": "station-zero-v3-entity-departure",
        "sourceWorldId": "game-run:w1-p1:A",
        "entityId": "medic-reyes",
        "fromLifeState": "active",
        "toLifeState": "extracted",
    }
    continuity = {
        "schemaVersion": 1,
        "kind": "ordivon.w1.entity-continuity",
        "entityId": "medic-reyes",
        "portableMemory": {"source": "game-run:w1-p1:A"},
    }
    return EntityMigrationBundle.create(
        migration_id="migration:w1-p1:medic-reyes",
        entity_id="medic-reyes",
        source_world_id="game-run:w1-p1:A",
        destination_world_id="security-world:w1-p1:B",
        source_departure=departure,
        continuity_payload=continuity,
    )


def create_task(storage: HostStorage, kernel: HostKernel, task_id: str) -> None:
    token = task_id.removeprefix("task:")
    kernel.create_task(
        event_id=f"event:{token}:create",
        kind=EventKind.TASK_CREATED,
        task_id=task_id,
        goal_id=f"goal:{token}",
        payload={"scenario": "w1-p1-failure-semantics"},
        frontier=(f"node:{token}",),
    )


class LinkBindingStale(RuntimeError):
    pass


class ResourceBackend:
    def __init__(self) -> None:
        self.binding_digest = "binding:v1"
        self.receipts: dict[str, ResourceTransferReceipt] = {}
        self.native: dict[str, dict[str, str]] = {}
        self.materializations = 0
        self.present = False


class ResourceDestination:
    def __init__(
        self,
        backend: ResourceBackend,
        *,
        bound_digest: str,
        drop_after_commit: bool = False,
        reconstruct_from_native: bool = False,
    ) -> None:
        self.backend = backend
        self.bound_digest = bound_digest
        self.drop_after_commit = drop_after_commit
        self.reconstruct_from_native = reconstruct_from_native

    def _receipt(
        self,
        plan: PreparedResourceTransfer,
        *,
        accepted_binding: str,
    ) -> ResourceTransferReceipt:
        return ResourceTransferReceipt(
            transfer_id=plan.transfer_id,
            plan_digest=plan.digest,
            destination_world_id=plan.destination_world_id,
            payload_digest=plan.payload_digest,
            materialization_id=f"native-resource:{plan.payload_digest[-16:]}",
            materialization_digest=sha256_digest(
                {
                    "destinationWorldId": plan.destination_world_id,
                    "payloadDigest": plan.payload_digest,
                }
            ),
            destination_evidence={
                "authority": "test-native-resource",
                "acceptedBindingDigest": accepted_binding,
                "presentAtCommit": True,
            },
        )

    def materialize(self, value: ResourceTransferBundle) -> ResourceTransferReceipt:
        if self.bound_digest != self.backend.binding_digest:
            raise LinkBindingStale("destination Link binding changed before materialization")
        retained = self.backend.receipts.get(value.plan.transfer_id)
        if retained is not None:
            return retained
        self.backend.materializations += 1
        self.backend.present = True
        self.backend.native[value.plan.payload_digest] = {
            "transferId": value.plan.transfer_id,
            "acceptedBindingDigest": self.bound_digest,
        }
        receipt = self._receipt(value.plan, accepted_binding=self.bound_digest)
        self.backend.receipts[value.plan.transfer_id] = receipt
        if self.drop_after_commit:
            self.drop_after_commit = False
            raise ResourceTransferOutcomeUnknown(
                value.plan, RuntimeError("response lost after destination commit")
            )
        return receipt

    def reconcile(self, plan: PreparedResourceTransfer) -> ResourceTransferReceipt | None:
        retained = self.backend.receipts.get(plan.transfer_id)
        if retained is not None:
            return retained
        native = self.backend.native.get(plan.payload_digest)
        if (
            not self.reconstruct_from_native
            or native is None
            or native["transferId"] != plan.transfer_id
        ):
            return None
        receipt = self._receipt(plan, accepted_binding=native["acceptedBindingDigest"])
        self.backend.receipts[plan.transfer_id] = receipt
        return receipt


class EntityBackend:
    def __init__(self) -> None:
        self.binding_digest = "binding:v1"
        self.receipts: dict[str, EntityMigrationReceipt] = {}
        self.materializations = 0


class EntityDestination:
    def __init__(
        self,
        backend: EntityBackend,
        *,
        bound_digest: str,
        drop_after_commit: bool = False,
    ) -> None:
        self.backend = backend
        self.bound_digest = bound_digest
        self.drop_after_commit = drop_after_commit

    def materialize(self, value: EntityMigrationBundle) -> EntityMigrationReceipt:
        if self.bound_digest != self.backend.binding_digest:
            raise LinkBindingStale("destination Link binding changed before entity materialization")
        retained = self.backend.receipts.get(value.plan.migration_id)
        if retained is not None:
            return retained
        self.backend.materializations += 1
        receipt = EntityMigrationReceipt(
            migration_id=value.plan.migration_id,
            plan_digest=value.plan.digest,
            entity_id=value.plan.entity_id,
            destination_world_id=value.plan.destination_world_id,
            source_departure_digest=value.plan.source_departure_digest,
            materialization_id=f"destination-body:{self.backend.materializations}",
            materialization_digest=sha256_digest(
                {"entityId": value.plan.entity_id, "body": self.backend.materializations}
            ),
            destination_evidence={
                "authority": "test-native-entity",
                "acceptedBindingDigest": self.bound_digest,
                "bodyStartedAtCommit": True,
            },
        )
        self.backend.receipts[value.plan.migration_id] = receipt
        if self.drop_after_commit:
            self.drop_after_commit = False
            raise EntityMigrationOutcomeUnknown(
                value.plan, RuntimeError("response lost after destination body start")
            )
        return receipt

    def reconcile(self, plan: PreparedEntityMigration) -> EntityMigrationReceipt | None:
        return self.backend.receipts.get(plan.migration_id)


class W1FailureSemanticsTests(unittest.TestCase):
    def test_resource_link_rebind_changes_dispatch_condition_not_semantic_plan(self) -> None:
        backend = ResourceBackend()
        old = ResourceDestination(backend, bound_digest="binding:v1")
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(70_000).__next__, owner_id="host:w1-p1"
            )
            create_task(storage, kernel, "task:w1-p1-resource-rebind")
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare("task:w1-p1-resource-rebind", resource_bundle())
            original = journal.load_bundle("task:w1-p1-resource-rebind").plan
            backend.binding_digest = "binding:v2"
            with self.assertRaises(LinkBindingStale):
                journal.deliver("task:w1-p1-resource-rebind", old)
            self.assertEqual(backend.materializations, 0)
            self.assertEqual(
                storage.read_task_event("task:w1-p1-resource-rebind").data[
                    "worldResourceTransferState"
                ],
                "prepared",
            )
            delivered = journal.deliver(
                "task:w1-p1-resource-rebind",
                ResourceDestination(backend, bound_digest="binding:v2"),
            )
            self.assertEqual(delivered.status, "materialized")
            self.assertEqual(backend.materializations, 1)
            self.assertEqual(
                journal.load_bundle("task:w1-p1-resource-rebind").plan.digest, original.digest
            )
            self.assertEqual(
                delivered.receipt.destination_evidence["acceptedBindingDigest"], "binding:v2"
            )

    def test_resource_native_state_can_reconstruct_lost_destination_receipt_without_redispatch(
        self,
    ) -> None:
        backend = ResourceBackend()
        first = ResourceDestination(backend, bound_digest="binding:v1", drop_after_commit=True)
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(71_000).__next__, owner_id="host:w1-p1"
            )
            create_task(storage, kernel, "task:w1-p1-resource-reconstruct")
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare("task:w1-p1-resource-reconstruct", resource_bundle())
            self.assertEqual(
                journal.deliver("task:w1-p1-resource-reconstruct", first).status, "unknown"
            )
            self.assertEqual(backend.materializations, 1)
            backend.receipts.clear()
            backend.binding_digest = "binding:v2"
            recovered = journal.reconcile(
                "task:w1-p1-resource-reconstruct",
                ResourceDestination(
                    backend,
                    bound_digest="binding:v2",
                    reconstruct_from_native=True,
                ),
            )
            self.assertEqual(recovered.status, "materialized")
            self.assertTrue(recovered.reconciled)
            self.assertEqual(backend.materializations, 1)
            self.assertEqual(
                recovered.receipt.destination_evidence["acceptedBindingDigest"], "binding:v1"
            )

    def test_resource_receipt_proves_commit_history_not_current_presence(self) -> None:
        backend = ResourceBackend()
        destination = ResourceDestination(backend, bound_digest="binding:v1")
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(72_000).__next__, owner_id="host:w1-p1"
            )
            create_task(storage, kernel, "task:w1-p1-resource-drift")
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare("task:w1-p1-resource-drift", resource_bundle())
            committed = journal.deliver("task:w1-p1-resource-drift", destination)
            self.assertTrue(committed.receipt.destination_evidence["presentAtCommit"])
            backend.present = False
            retained = journal.deliver("task:w1-p1-resource-drift", destination)
            self.assertEqual(retained.status, "materialized")
            self.assertFalse(backend.present)
            self.assertEqual(retained.receipt, committed.receipt)
            self.assertEqual(backend.materializations, 1)

    def test_entity_link_replacement_after_commit_reconciles_old_receipt_without_new_body(
        self,
    ) -> None:
        backend = EntityBackend()
        first = EntityDestination(backend, bound_digest="binding:v1", drop_after_commit=True)
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(73_000).__next__, owner_id="host:w1-p1"
            )
            create_task(storage, kernel, "task:w1-p1-entity-rebind")
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            journal.prepare("task:w1-p1-entity-rebind", entity_bundle())
            original = journal.load_bundle("task:w1-p1-entity-rebind").plan
            self.assertEqual(
                journal.materialize("task:w1-p1-entity-rebind", first).status, "unknown"
            )
            backend.binding_digest = "binding:v2"
            recovered = journal.reconcile(
                "task:w1-p1-entity-rebind", EntityDestination(backend, bound_digest="binding:v2")
            )
            self.assertEqual(recovered.status, "materialized")
            self.assertEqual(backend.materializations, 1)
            self.assertEqual(
                journal.load_bundle("task:w1-p1-entity-rebind").plan.digest, original.digest
            )
            self.assertEqual(
                recovered.receipt.destination_evidence["acceptedBindingDigest"], "binding:v1"
            )

    def test_entity_receipt_loss_stays_unknown_and_cannot_authorize_rematerialization(self) -> None:
        backend = EntityBackend()
        first = EntityDestination(backend, bound_digest="binding:v1", drop_after_commit=True)
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(74_000).__next__, owner_id="host:w1-p1"
            )
            create_task(storage, kernel, "task:w1-p1-entity-lost")
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            journal.prepare("task:w1-p1-entity-lost", entity_bundle())
            self.assertEqual(journal.materialize("task:w1-p1-entity-lost", first).status, "unknown")
            backend.receipts.clear()
            recovered = journal.reconcile(
                "task:w1-p1-entity-lost", EntityDestination(backend, bound_digest="binding:v1")
            )
            self.assertEqual(recovered.status, "unknown")
            self.assertTrue(recovered.reconciled)
            self.assertEqual(backend.materializations, 1)
            with self.assertRaises(EntityMigrationError):
                journal.materialize(
                    "task:w1-p1-entity-lost", EntityDestination(backend, bound_digest="binding:v1")
                )
            self.assertEqual(backend.materializations, 1)


if __name__ == "__main__":
    unittest.main()
