from __future__ import annotations

import concurrent.futures
import itertools
import json
import os
import tempfile
import unittest
from pathlib import Path

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world.canonical import canonical_bytes, sha256_digest
from ordivon_world.entity_migration import (
    EntityMigrationBundle,
    EntityMigrationOutcomeUnknown,
    EntityMigrationReceipt,
    EntityMigrationSuperseded,
    HostEntityMigrationJournal,
)
from ordivon_world.message_delivery import (
    HostMessageDeliveryJournal,
    MessageDeliveryBundle,
    MessageDeliveryOutcomeUnknown,
    MessageDeliveryReceipt,
    MessageDeliverySuperseded,
)
from ordivon_world.resource_transfer import (
    HostResourceTransferJournal,
    ResourceTransferBundle,
    ResourceTransferOutcomeUnknown,
    ResourceTransferReceipt,
    ResourceTransferSuperseded,
)


def _bundle(kind: str, index: int):
    source = f"world-instance:w1-p5:source:{index}"
    destination = f"world-instance:w1-p5:destination:{index}"
    if kind == "resource":
        return ResourceTransferBundle.create(
            transfer_id=f"transfer:w1-p5:{index}",
            source_world_id=source,
            destination_world_id=destination,
            resource_kind="test-resource",
            source_evidence={"kind": "source-fact", "index": index},
            payload={"kind": "portable-resource", "index": index},
        )
    if kind == "entity":
        return EntityMigrationBundle.create(
            migration_id=f"migration:w1-p5:{index}",
            entity_id=f"entity:w1-p5:{index}",
            source_world_id=source,
            destination_world_id=destination,
            source_departure={"kind": "source-departure", "index": index},
            continuity_payload={"kind": "portable-continuity", "index": index},
        )
    return MessageDeliveryBundle.create(
        message_id=f"message:w1-p5:{index}",
        source_world_id=source,
        destination_world_id=destination,
        message_kind="test-message",
        provenance={"kind": "message-provenance", "index": index},
        payload={"kind": "message-payload", "index": index},
    )


class _FileDestination:
    def __init__(self, root: str | Path, kind: str, index: int, *, drop: bool = False) -> None:
        self.root = Path(root)
        self.kind = kind
        self.index = index
        self.drop = drop

    @property
    def receipt_path(self) -> Path:
        return self.root / f"{self.kind}-{self.index}.json"

    @property
    def effect_path(self) -> Path:
        return self.root / f"{self.kind}-{self.index}.effect"

    def _commit(self, plan, receipt) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        # CREATE_NEW makes duplicate semantic effects observable instead of hidden.
        fd = os.open(self.effect_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(plan.digest.encode() + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        temp = self.receipt_path.with_suffix(".tmp")
        with temp.open("xb") as handle:
            handle.write(canonical_bytes(receipt.to_dict()) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, self.receipt_path)

    def _load(self, receipt_type):
        if not self.receipt_path.exists():
            return None
        return receipt_type.from_dict(json.loads(self.receipt_path.read_text()))

    def materialize_resource(self, bundle: ResourceTransferBundle) -> ResourceTransferReceipt:
        retained = self._load(ResourceTransferReceipt)
        if retained is not None:
            return retained
        receipt = ResourceTransferReceipt(
            transfer_id=bundle.plan.transfer_id,
            plan_digest=bundle.plan.digest,
            destination_world_id=bundle.plan.destination_world_id,
            payload_digest=bundle.plan.payload_digest,
            materialization_id=f"file-resource:{self.index}",
            materialization_digest=sha256_digest({"kind": "resource", "index": self.index}),
            destination_evidence={"authority": "file-destination", "index": self.index},
        )
        self._commit(bundle.plan, receipt)
        if self.drop:
            self.drop = False
            raise ResourceTransferOutcomeUnknown(bundle.plan, RuntimeError("lost after commit"))
        return receipt

    def materialize_entity(self, bundle: EntityMigrationBundle) -> EntityMigrationReceipt:
        retained = self._load(EntityMigrationReceipt)
        if retained is not None:
            return retained
        receipt = EntityMigrationReceipt(
            migration_id=bundle.plan.migration_id,
            plan_digest=bundle.plan.digest,
            entity_id=bundle.plan.entity_id,
            destination_world_id=bundle.plan.destination_world_id,
            source_departure_digest=bundle.plan.source_departure_digest,
            materialization_id=f"file-entity:{self.index}",
            materialization_digest=sha256_digest({"kind": "entity", "index": self.index}),
            destination_evidence={"authority": "file-destination", "index": self.index},
        )
        self._commit(bundle.plan, receipt)
        if self.drop:
            self.drop = False
            raise EntityMigrationOutcomeUnknown(bundle.plan, RuntimeError("lost after commit"))
        return receipt

    def deliver_message(self, bundle: MessageDeliveryBundle) -> MessageDeliveryReceipt:
        retained = self._load(MessageDeliveryReceipt)
        if retained is not None:
            return retained
        receipt = MessageDeliveryReceipt(
            message_id=bundle.plan.message_id,
            plan_digest=bundle.plan.digest,
            destination_world_id=bundle.plan.destination_world_id,
            payload_digest=bundle.plan.payload_digest,
            delivery_id=f"file-message:{self.index}",
            delivery_digest=sha256_digest({"kind": "message", "index": self.index}),
            destination_evidence={"authority": "file-destination", "index": self.index},
        )
        self._commit(bundle.plan, receipt)
        if self.drop:
            self.drop = False
            raise MessageDeliveryOutcomeUnknown(bundle.plan, RuntimeError("lost after commit"))
        return receipt


def _run_one(
    host_root: str, destination_root: str, kind: str, index: int, drop: bool
) -> dict[str, object]:
    task_id = f"task:w1-p5:{kind}:{index}"
    bundle = _bundle(kind, index)
    destination = _FileDestination(destination_root, kind, index, drop=drop)
    with HostStorage(host_root) as storage:
        kernel = HostKernel(
            storage,
            clock_ms=itertools.count(300_000 + index * 1_000).__next__,
            owner_id=f"host:w1-p5:{kind}:{index}",
        )
        port = HostExtensionPort(storage, kernel)
        if kind == "resource":
            journal = HostResourceTransferJournal(port)
            journal.prepare(task_id, bundle)
            step = journal.deliver(
                task_id,
                type(
                    "D",
                    (),
                    {
                        "materialize": destination.materialize_resource,
                        "reconcile": lambda _self, plan: destination._load(ResourceTransferReceipt),
                    },
                )(),
            )
            conflict_type = ResourceTransferSuperseded
            changed = ResourceTransferBundle.create(
                transfer_id=bundle.plan.transfer_id,
                source_world_id=bundle.plan.source_world_id,
                destination_world_id=bundle.plan.destination_world_id,
                resource_kind=bundle.plan.resource_kind,
                source_evidence=bundle.source_evidence,
                payload={"kind": "portable-resource", "index": index, "changed": True},
            )
        elif kind == "entity":
            journal = HostEntityMigrationJournal(port)
            journal.prepare(task_id, bundle)
            step = journal.materialize(
                task_id,
                type(
                    "D",
                    (),
                    {
                        "materialize": destination.materialize_entity,
                        "reconcile": lambda _self, plan: destination._load(EntityMigrationReceipt),
                    },
                )(),
            )
            conflict_type = EntityMigrationSuperseded
            changed = EntityMigrationBundle.create(
                migration_id=bundle.plan.migration_id,
                entity_id=bundle.plan.entity_id,
                source_world_id=bundle.plan.source_world_id,
                destination_world_id=bundle.plan.destination_world_id,
                source_departure=bundle.source_departure,
                continuity_payload={"kind": "portable-continuity", "index": index, "changed": True},
            )
        else:
            journal = HostMessageDeliveryJournal(port)
            journal.prepare(task_id, bundle)
            step = journal.deliver(
                task_id,
                type(
                    "D",
                    (),
                    {
                        "deliver": destination.deliver_message,
                        "reconcile": lambda _self, plan: destination._load(MessageDeliveryReceipt),
                    },
                )(),
            )
            conflict_type = MessageDeliverySuperseded
            changed = MessageDeliveryBundle.create(
                message_id=bundle.plan.message_id,
                source_world_id=bundle.plan.source_world_id,
                destination_world_id=bundle.plan.destination_world_id,
                message_kind=bundle.plan.message_kind,
                provenance=bundle.provenance,
                payload={"kind": "message-payload", "index": index, "changed": True},
            )
        conflict = False
        try:
            journal.prepare(task_id, changed)
        except conflict_type:
            conflict = True
        snapshot = storage.read_task_event(task_id)
        return {
            "taskId": task_id,
            "kind": kind,
            "index": index,
            "drop": drop,
            "status": step.status,
            "revision": snapshot.projection.revision,
            "conflictRejected": conflict,
        }


class W1ConcurrentTrajectoryTests(unittest.TestCase):
    def test_independent_tasks_converge_without_global_world_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            host_root = root / "host"
            destination_root = root / "destinations"
            cases = [
                (kind, i, i % 3 == 0)
                for i in range(6)
                for kind in ("resource", "entity", "message")
            ]
            with HostStorage(host_root) as storage:
                kernel = HostKernel(
                    storage, clock_ms=itertools.count(100_000).__next__, owner_id="host:w1-p5:setup"
                )
                for kind, index, _drop in cases:
                    task_id = f"task:w1-p5:{kind}:{index}"
                    kernel.create_task(
                        event_id=f"event:w1-p5:{kind}:{index}:create",
                        kind=EventKind.TASK_CREATED,
                        task_id=task_id,
                        goal_id=f"goal:w1-p5:{kind}:{index}",
                        payload={"trajectory": kind, "index": index},
                        frontier=(f"node:w1-p5:{kind}:{index}",),
                    )
            with concurrent.futures.ProcessPoolExecutor(max_workers=6) as pool:
                futures = [
                    pool.submit(_run_one, str(host_root), str(destination_root), kind, index, drop)
                    for kind, index, drop in cases
                ]
                results = [future.result(timeout=20) for future in futures]
            self.assertEqual(len(results), 18)
            self.assertTrue(all(result["conflictRejected"] for result in results))
            self.assertEqual(sum(result["status"] == "unknown" for result in results), 6)
            self.assertEqual(
                sum(result["status"] in {"materialized", "delivered"} for result in results), 12
            )

            with HostStorage(host_root) as reopened:
                # Recovery time must remain monotonic across process replacement so prior
                # per-Task transition leases can expire normally.
                kernel = HostKernel(
                    reopened,
                    clock_ms=itertools.count(1_000_000).__next__,
                    owner_id="host:w1-p5:recover",
                )
                port = HostExtensionPort(reopened, kernel)
                for kind, index, drop in cases:
                    task_id = f"task:w1-p5:{kind}:{index}"
                    destination = _FileDestination(destination_root, kind, index)
                    if kind == "resource":
                        step = HostResourceTransferJournal(port).reconcile(
                            task_id,
                            type(
                                "D",
                                (),
                                {
                                    "reconcile": lambda _self, plan, d=destination: d._load(
                                        ResourceTransferReceipt
                                    )
                                },
                            )(),
                        )
                        expected = "materialized"
                    elif kind == "entity":
                        step = HostEntityMigrationJournal(port).reconcile(
                            task_id,
                            type(
                                "D",
                                (),
                                {
                                    "reconcile": lambda _self, plan, d=destination: d._load(
                                        EntityMigrationReceipt
                                    )
                                },
                            )(),
                        )
                        expected = "materialized"
                    else:
                        step = HostMessageDeliveryJournal(port).reconcile(
                            task_id,
                            type(
                                "D",
                                (),
                                {
                                    "reconcile": lambda _self, plan, d=destination: d._load(
                                        MessageDeliveryReceipt
                                    )
                                },
                            )(),
                        )
                        expected = "delivered"
                    self.assertEqual(step.status, expected)
                    snapshot = reopened.read_task_event(task_id)
                    self.assertEqual(snapshot.projection.revision, 4 if drop else 3)
                    self.assertNotIn("worldGlobalHead", snapshot.data)
                    self.assertNotIn("worldFederationRevision", snapshot.data)
                    self.assertNotIn("worldGlobalRevision", snapshot.data)
            effects = list(destination_root.glob("*.effect"))
            receipts = list(destination_root.glob("*.json"))
            self.assertEqual(len(effects), 18)
            self.assertEqual(len(receipts), 18)


if __name__ == "__main__":
    unittest.main()
