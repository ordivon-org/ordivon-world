from __future__ import annotations

import itertools
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world.canonical import sha256_digest
from ordivon_world.resource_egress import ResourceEgressAuthority, ResourceEgressReceipt
from ordivon_world.resource_transfer import (
    HostResourceTransferJournal,
    PreparedResourceTransfer,
    ResourceTransferBundle,
    ResourceTransferError,
    ResourceTransferNotCommitted,
    ResourceTransferOutcomeUnknown,
    ResourceTransferReceipt,
    ResourceTransferSuperseded,
)


def payload() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.w1.portable-resource",
        "resourceType": "station-zero-v3-item",
        "itemId": "research-core",
        "category": "objective",
    }


def source_egress(
    *,
    transfer_id: str = "transfer:w1:research-core",
    body: dict[str, object] | None = None,
) -> ResourceEgressReceipt:
    resource = payload() if body is None else body
    occurrence = {
        "sourceWorldId": "game-run:w1:A",
        "recordDigest": "sha256:" + "1" * 64,
        "factId": "fact:batch:w1:0001:item_extracted",
    }
    return ResourceEgressReceipt(
        transfer_id=transfer_id,
        source_world_id="game-run:w1:A",
        destination_world_id="security-world:w1:B",
        resource_kind="station-zero-v3-item",
        payload_digest=sha256_digest(resource),
        source_occurrence_id="resource-occurrence:w1:research-core",
        source_occurrence_digest=sha256_digest(occurrence),
        authority=ResourceEgressAuthority(
            authority_id="ordivon.game.station-zero-v3:game-run:w1:A",
            mechanism="test-retained-source-egress.v1",
            evidence=occurrence,
        ),
    )


def bundle(
    *, transfer_id: str = "transfer:w1:research-core", body: dict[str, object] | None = None
) -> ResourceTransferBundle:
    resource = payload() if body is None else body
    return ResourceTransferBundle.create(
        source_egress=source_egress(transfer_id=transfer_id, body=resource),
        payload=resource,
    )


class DurableDestination:
    def __init__(self) -> None:
        self.receipts: dict[str, ResourceTransferReceipt] = {}
        self.materializations = 0
        self.drop_after_commit = False
        self.override_receipt: ResourceTransferReceipt | None = None

    def materialize(self, value: ResourceTransferBundle) -> ResourceTransferReceipt:
        retained = self.receipts.get(value.plan.transfer_id)
        if retained is not None:
            return retained
        self.materializations += 1
        receipt = self.override_receipt or ResourceTransferReceipt(
            transfer_id=value.plan.transfer_id,
            plan_digest=value.plan.digest,
            destination_world_id=value.plan.destination_world_id,
            payload_digest=value.plan.payload_digest,
            materialization_id=f"security-resource:{value.plan.payload_digest[-16:]}",
            materialization_digest=sha256_digest(
                {
                    "destinationWorldId": value.plan.destination_world_id,
                    "payloadDigest": value.plan.payload_digest,
                }
            ),
            destination_evidence={
                "authority": "test-destination-local",
                "present": True,
            },
        )
        self.receipts[value.plan.transfer_id] = receipt
        if self.drop_after_commit:
            self.drop_after_commit = False
            raise ResourceTransferOutcomeUnknown(
                value.plan, RuntimeError("response lost after destination commit")
            )
        return receipt

    def reconcile(self, plan: PreparedResourceTransfer) -> ResourceTransferReceipt | None:
        return self.receipts.get(plan.transfer_id)


class ProvenNotCommittedDestination:
    def __init__(self) -> None:
        self.materializations = 0
        self.proof_issued = False

    def materialize(self, value: ResourceTransferBundle) -> ResourceTransferReceipt:
        self.materializations += 1
        if self.materializations == 1:
            raise ResourceTransferOutcomeUnknown(
                value.plan, RuntimeError("destination died before semantic commit")
            )
        return ResourceTransferReceipt(
            transfer_id=value.plan.transfer_id,
            plan_digest=value.plan.digest,
            destination_world_id=value.plan.destination_world_id,
            payload_digest=value.plan.payload_digest,
            materialization_id="security-resource:retry-safe",
            materialization_digest=sha256_digest(
                {"payloadDigest": value.plan.payload_digest, "attempt": 2}
            ),
            destination_evidence={"authority": "test-destination"},
        )

    def reconcile(self, plan: PreparedResourceTransfer) -> ResourceTransferNotCommitted:
        self.proof_issued = True
        return ResourceTransferNotCommitted(
            transfer_id=plan.transfer_id,
            plan_digest=plan.digest,
            destination_world_id=plan.destination_world_id,
            payload_digest=plan.payload_digest,
            evidence={
                "authority": "test-destination",
                "exactOriginalRetrySafe": True,
            },
        )


class HostResourceTransferTests(unittest.TestCase):
    def create_task(
        self, storage: HostStorage, kernel: HostKernel, task_id: str = "task:w1-resource"
    ):
        return kernel.create_task(
            event_id=f"event:{task_id.removeprefix('task:')}:create",
            kind=EventKind.TASK_CREATED,
            task_id=task_id,
            goal_id=f"goal:{task_id.removeprefix('task:')}",
            payload={"scenario": "w1-resource-transfer"},
            frontier=(f"node:{task_id.removeprefix('task:')}",),
        ).projection

    def test_prepare_retains_source_payload_and_plan_without_changing_task_meaning(self) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(10_000).__next__, owner_id="host:w1:first"
            )
            created = self.create_task(storage, kernel)
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            first = journal.prepare(created.task_id, bundle())
            second = journal.prepare(created.task_id, bundle())
            loaded = journal.load_bundle(created.task_id)
            self.assertEqual(first.status, "prepared")
            self.assertEqual(second.task_revision, first.task_revision)
            self.assertEqual(loaded, bundle())
            snapshot = storage.read_task_event(created.task_id)
            self.assertEqual(snapshot.projection.state, created.state)
            self.assertEqual(snapshot.projection.ready_frontier, created.ready_frontier)
            self.assertEqual(snapshot.event_kind, EventKind("world.resource-transfer-prepared"))
            self.assertEqual(
                next(iter(snapshot.data["worldResourceTransfers"].values()))[
                    "worldResourcePayloadDigest"
                ],
                loaded.plan.payload_digest,
            )
            self.assertNotEqual(
                next(iter(snapshot.data["worldResourceTransfers"].values()))[
                    "worldResourcePayloadObjectDigest"
                ],
                loaded.plan.payload_digest,
            )
            self.assertEqual(
                next(iter(snapshot.data["worldResourceTransfers"].values()))[
                    "worldResourceTransferPlanDigest"
                ],
                loaded.plan.digest,
            )
            self.assertNotEqual(
                next(iter(snapshot.data["worldResourceTransfers"].values()))[
                    "worldResourceTransferPlanObjectDigest"
                ],
                loaded.plan.digest,
            )

    def test_response_loss_reopens_host_and_reconciles_original_destination_commit(self) -> None:
        destination = DurableDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(20_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(storage, clock_ms=clock, owner_id="host:w1:first")
                created = self.create_task(storage, kernel)
                journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
                journal.prepare(created.task_id, bundle())
                unknown = journal.deliver(created.task_id, destination)
                self.assertEqual(unknown.status, "unknown")
                self.assertEqual(destination.materializations, 1)
            with HostStorage(directory) as reopened:
                kernel = HostKernel(reopened, clock_ms=clock, owner_id="host:w1:fresh")
                journal = HostResourceTransferJournal(HostExtensionPort(reopened, kernel))
                recovered = journal.reconcile("task:w1-resource", destination)
                self.assertEqual(recovered.status, "materialized")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(destination.materializations, 1)
                self.assertEqual(journal.load_receipt("task:w1-resource"), recovered.receipt)
                snapshot = reopened.read_task_event("task:w1-resource")
                self.assertNotIn(
                    "worldResourceTransferUncertaintyObjectDigest",
                    next(iter(snapshot.data["worldResourceTransfers"].values())),
                )

    def test_known_receipt_prevents_second_destination_materialization(self) -> None:
        destination = DurableDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(30_000).__next__, owner_id="host:w1"
            )
            created = self.create_task(storage, kernel)
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            first = journal.deliver(created.task_id, destination)
            second = journal.deliver(created.task_id, destination)
            self.assertEqual(first.status, "materialized")
            self.assertEqual(second.status, "materialized")
            self.assertEqual(destination.materializations, 1)

    def test_distinct_transfer_identity_is_independent_but_same_identity_cannot_change_payload(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(40_000).__next__, owner_id="host:w1"
            )
            created = self.create_task(storage, kernel)
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            first = bundle()
            second = bundle(transfer_id="transfer:w1:other")
            journal.prepare(created.task_id, first)
            journal.prepare(created.task_id, second)
            self.assertEqual(
                journal.transfer_ids(created.task_id),
                tuple(sorted((first.plan.transfer_id, second.plan.transfer_id))),
            )
            changed = payload() | {"category": "changed"}
            with self.assertRaises(ResourceTransferSuperseded):
                journal.prepare(created.task_id, bundle(body=changed))

    def test_receipt_binding_drift_is_rejected_before_host_commit(self) -> None:
        destination = DurableDestination()
        good = bundle()
        destination.override_receipt = ResourceTransferReceipt(
            transfer_id=good.plan.transfer_id,
            plan_digest=good.plan.digest,
            destination_world_id=good.plan.destination_world_id,
            payload_digest="sha256:" + "0" * 64,
            materialization_id="security-resource:wrong",
            materialization_digest="sha256:" + "2" * 64,
            destination_evidence={"authority": "test"},
        )
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(50_000).__next__, owner_id="host:w1"
            )
            created = self.create_task(storage, kernel)
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, good)
            with self.assertRaises(ResourceTransferSuperseded):
                journal.deliver(created.task_id, destination)
            snapshot = storage.read_task_event(created.task_id)
            self.assertEqual(
                next(iter(snapshot.data["worldResourceTransfers"].values()))[
                    "worldResourceTransferState"
                ],
                "prepared",
            )
            self.assertNotIn(
                "worldResourceTransferReceiptDigest",
                next(iter(snapshot.data["worldResourceTransfers"].values())),
            )

    def test_reconcile_missing_never_materializes_or_redispatches(self) -> None:
        destination = DurableDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(60_000).__next__, owner_id="host:w1"
            )
            created = self.create_task(storage, kernel)
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            step = journal.reconcile(created.task_id, destination)
            self.assertEqual(step.status, "unknown")
            self.assertTrue(step.reconciled)
            self.assertEqual(destination.materializations, 0)

    def test_unknown_state_forbids_blind_redispatch_even_if_destination_receipt_is_lost(
        self,
    ) -> None:
        destination = DurableDestination()
        destination.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage, clock_ms=itertools.count(65_000).__next__, owner_id="host:w1-p1-resource"
            )
            created = self.create_task(storage, kernel)
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            self.assertEqual(journal.deliver(created.task_id, destination).status, "unknown")
            self.assertEqual(destination.materializations, 1)
            destination.receipts.clear()
            with self.assertRaises(ResourceTransferError):
                journal.deliver(created.task_id, destination)
            self.assertEqual(destination.materializations, 1)
            self.assertEqual(
                next(
                    iter(
                        storage.read_task_event(created.task_id)
                        .data["worldResourceTransfers"]
                        .values()
                    )
                )["worldResourceTransferState"],
                "unknown",
            )

    def test_not_committed_proof_releases_unknown_for_exact_original_retry(self) -> None:
        destination = ProvenNotCommittedDestination()
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=itertools.count(66_000).__next__,
                owner_id="host:w2-not-committed",
            )
            created = self.create_task(storage, kernel)
            journal = HostResourceTransferJournal(HostExtensionPort(storage, kernel))
            journal.prepare(created.task_id, bundle())
            self.assertEqual(journal.deliver(created.task_id, destination).status, "unknown")
            released = journal.reconcile(created.task_id, destination)
            self.assertEqual(released.status, "prepared")
            self.assertTrue(released.reconciled)
            self.assertTrue(destination.proof_issued)
            snapshot = storage.read_task_event(created.task_id)
            self.assertEqual(
                next(iter(snapshot.data["worldResourceTransfers"].values()))[
                    "worldResourceTransferState"
                ],
                "prepared",
            )
            self.assertIn(
                "worldResourceTransferNotCommittedDigest",
                next(iter(snapshot.data["worldResourceTransfers"].values())),
            )
            self.assertNotIn(
                "worldResourceTransferUncertaintyObjectDigest",
                next(iter(snapshot.data["worldResourceTransfers"].values())),
            )
            completed = journal.deliver(created.task_id, destination)
            self.assertEqual(completed.status, "materialized")
            self.assertEqual(destination.materializations, 2)

    def test_bundle_rejects_tampered_source_egress_or_payload(self) -> None:
        valid = bundle()
        with self.assertRaises(ValueError):
            ResourceTransferBundle(
                plan=valid.plan,
                source_egress={
                    **valid.source_egress,
                    "sourceOccurrenceId": "resource-occurrence:tampered",
                },
                payload=valid.payload,
            )
        with self.assertRaises(ValueError):
            ResourceTransferBundle(
                plan=valid.plan,
                source_egress=valid.source_egress,
                payload=payload() | {"itemId": "medkit"},
            )


if __name__ == "__main__":
    unittest.main()
