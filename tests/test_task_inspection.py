from __future__ import annotations

import itertools
import json
import tempfile
import unittest
from pathlib import Path

from ordivon_host import (
    ExternalContinuityHost,
    HostExtensionPort,
    HostKernel,
    HostStorage,
    WorkingCheckpoint,
)

from ordivon_world import (
    CapabilitySnapshot,
    CloudflareWorldAdapter,
    HostEntityMigrationJournal,
    HostMessageDeliveryJournal,
    HostResourceTransferJournal,
    HostWorldExtension,
    WorldTaskInspectionSuperseded,
    WorldTaskInspector,
)
from tests.test_entity_migration import DurableDestination as EntityDestination
from tests.test_entity_migration import bundle as entity_bundle
from tests.test_host_world import ProviderBackend, ProviderTransport, capability_document
from tests.test_message_delivery import InboxDestination
from tests.test_message_delivery import bundle as message_bundle
from tests.test_resource_transfer import ProvenNotCommittedDestination
from tests.test_resource_transfer import bundle as resource_bundle


class WorldTaskInspectionTests(unittest.TestCase):
    def test_mixed_commitments_survive_host_checkpoint_without_body_dump(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            task_id = "task:w5e:inspection:mixed"
            clock = itertools.count(2_000_000).__next__
            checkpoint = WorkingCheckpoint(
                task_id=task_id,
                objective="Recover bounded World owner commitments.",
                frontier="Inspect World owner state.",
                established=(),
                unresolved=(),
                rejected=(),
                constraints=("External truth remains owner-authored.",),
                next_actions=("Inspect World owner state.",),
                runtime=None,
            )
            backend = ProviderBackend()
            transport = ProviderTransport(backend)
            capability = CapabilitySnapshot.from_document(
                capability_document(), "2026-08-09T00:00:00Z"
            )
            adapter = CloudflareWorldAdapter(transport)
            prepared = adapter.prepare_fetch(
                dispatch_id="dispatch:w5e:inspection:mixed",
                effect_id="effect:w5e:inspection:mixed",
                url="https://developers.cloudflare.com/",
                capability=capability,
            )
            transport.prepared = prepared

            with HostStorage(directory) as storage:
                host = ExternalContinuityHost(
                    storage,
                    clock_ms=clock,
                    owner_id="host:w5e:inspection:first",
                )
                host.adopt(
                    task_id=task_id,
                    goal_id="goal:w5e:inspection:mixed",
                    initial_checkpoint=checkpoint,
                )
                port = HostExtensionPort(
                    storage,
                    HostKernel(
                        storage,
                        clock_ms=clock,
                        owner_id="world:w5e:inspection:first",
                    ),
                )

                world = HostWorldExtension(port)
                world.prepare(task_id, prepared)
                unknown = world.deliver(task_id, adapter, check_conditions=False)
                self.assertEqual(unknown.status, "unknown")
                self.assertEqual(backend.posts, 1)

                resource = HostResourceTransferJournal(port)
                secret_resource_payload = {
                    "schemaVersion": 1,
                    "kind": "ordivon.w5e.secret-resource-body",
                    "itemId": "payload-secret-resource-marker",
                    "category": "objective",
                }
                resource_value = resource_bundle(
                    transfer_id="transfer:w5e:inspection:resource",
                    body=secret_resource_payload,
                )
                resource_step = resource.prepare(task_id, resource_value)
                self.assertEqual(resource_step.status, "prepared")

                message = HostMessageDeliveryJournal(port)
                message_value = message_bundle()
                message.prepare(task_id, message_value)
                delivered = message.deliver(task_id, InboxDestination())
                self.assertEqual(delivered.status, "delivered")

                entity = HostEntityMigrationJournal(port)
                entity_value = entity_bundle()
                entity.prepare(task_id, entity_value)
                materialized = entity.materialize(task_id, EntityDestination())
                self.assertEqual(materialized.status, "materialized")

                later = WorkingCheckpoint(
                    task_id=task_id,
                    objective=checkpoint.objective,
                    frontier="Fresh Agent inspects World owner state after Host checkpoint.",
                    established=("Host meaning advanced after World effects.",),
                    unresolved=(
                        "Outstanding World commitments still require owner recovery.",
                    ),
                    rejected=(),
                    constraints=("Do not copy external truth into this checkpoint.",),
                    next_actions=("Inspect World owner state.",),
                    runtime=None,
                )
                committed = host.checkpoint(
                    task_id=task_id,
                    expected_revision=materialized.task_revision,
                    checkpoint=later,
                    disposition="continue",
                )

            with HostStorage(directory) as reopened:
                port = HostExtensionPort(
                    reopened,
                    HostKernel(
                        reopened,
                        clock_ms=itertools.count(2_100_000).__next__,
                        owner_id="world:w5e:inspection:fresh",
                    ),
                )
                inspection = WorldTaskInspector(port).inspect_task(
                    task_id,
                    expected_revision=committed.projection.revision,
                )
                self.assertEqual(
                    inspection["kind"], "ordivon.world.task-commitment-inspection"
                )
                self.assertEqual(inspection["ownerNamespace"], "world")
                self.assertEqual(
                    inspection["taskRevision"], committed.projection.revision
                )
                self.assertFalse(inspection["worldState"]["legacy"])
                self.assertLess(
                    inspection["worldState"]["revision"], inspection["taskRevision"]
                )
                commitments = {
                    (value["family"], value["identity"]): value
                    for value in inspection["commitments"]
                }

                provider = commitments[
                    ("provider-dispatch", prepared.dispatch.dispatch_id)
                ]
                self.assertEqual(provider["state"], "unknown")
                self.assertEqual(provider["commitmentClass"], "outstanding")
                self.assertEqual(
                    provider["nextOwnerOperation"], "reconcile-original-request"
                )
                self.assertEqual(
                    provider["providerRequestId"], prepared.provider_request_id
                )
                self.assertEqual(provider["effectId"], prepared.dispatch.effect_id)

                resource_projection = commitments[
                    ("resource-transfer", resource_value.plan.transfer_id)
                ]
                self.assertEqual(resource_projection["state"], "prepared")
                self.assertEqual(
                    resource_projection["commitmentClass"], "outstanding"
                )
                self.assertEqual(
                    resource_projection["nextOwnerOperation"],
                    "materialize-prepared-transfer",
                )
                self.assertEqual(
                    resource_projection["destinationWorldId"],
                    resource_value.plan.destination_world_id,
                )

                message_projection = commitments[
                    ("message-delivery", message_value.plan.message_id)
                ]
                self.assertEqual(message_projection["state"], "delivered")
                self.assertEqual(
                    message_projection["commitmentClass"], "historical-terminal"
                )
                self.assertIsNone(message_projection["nextOwnerOperation"])

                entity_projection = commitments[
                    ("entity-migration", entity_value.plan.migration_id)
                ]
                self.assertEqual(entity_projection["state"], "materialized")
                self.assertEqual(
                    entity_projection["commitmentClass"], "historical-terminal"
                )
                self.assertIsNone(entity_projection["nextOwnerOperation"])
                self.assertEqual(
                    entity_projection["entityId"], entity_value.plan.entity_id
                )

                encoded = json.dumps(inspection, sort_keys=True).lower()
                for forbidden in (
                    '"payload"',
                    '"provenance"',
                    '"continuitypayload"',
                    "payload-secret-resource-marker",
                    "reactor",
                    "continue mission context",
                ):
                    self.assertNotIn(forbidden, encoded)
                for value in inspection["commitments"]:
                    self.assertEqual(
                        value["authority"], "not-granted-by-inspection"
                    )
                    self.assertEqual(value["externalCurrentness"], "not-claimed")

                with self.assertRaises(WorldTaskInspectionSuperseded):
                    WorldTaskInspector(port).inspect_task(
                        task_id,
                        expected_revision=committed.projection.revision - 1,
                    )

    def test_not_committed_projection_authorizes_only_exact_original_retry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            task_id = "task:w5e:inspection:not-committed"
            checkpoint = WorkingCheckpoint(
                task_id=task_id,
                objective="Project exact retry evidence without granting new authority.",
                frontier="Inspect released Resource commitment.",
                established=(),
                unresolved=(),
                rejected=(),
                constraints=("Only exact original retry is admissible.",),
                next_actions=("Inspect World owner state.",),
                runtime=None,
            )
            with HostStorage(directory) as storage:
                clock = itertools.count(3_000_000).__next__
                host = ExternalContinuityHost(
                    storage,
                    clock_ms=clock,
                    owner_id="host:w5e:inspection:not-committed",
                )
                host.adopt(
                    task_id=task_id,
                    goal_id="goal:w5e:inspection:not-committed",
                    initial_checkpoint=checkpoint,
                )
                port = HostExtensionPort(
                    storage,
                    HostKernel(
                        storage,
                        clock_ms=clock,
                        owner_id="world:w5e:inspection:not-committed",
                    ),
                )
                journal = HostResourceTransferJournal(port)
                value = resource_bundle(
                    transfer_id="transfer:w5e:inspection:not-committed"
                )
                journal.prepare(task_id, value)
                destination = ProvenNotCommittedDestination()
                unknown = journal.deliver(task_id, destination)
                self.assertEqual(unknown.status, "unknown")
                released = journal.reconcile(task_id, destination)
                self.assertEqual(released.status, "prepared")

                inspection = WorldTaskInspector(port).inspect_task(
                    task_id,
                    expected_revision=released.task_revision,
                )
                projection = next(
                    item
                    for item in inspection["commitments"]
                    if item["family"] == "resource-transfer"
                )
                self.assertEqual(projection["state"], "prepared")
                self.assertEqual(projection["commitmentClass"], "outstanding")
                self.assertEqual(
                    projection["nextOwnerOperation"],
                    "retry-exact-original-transfer",
                )
                self.assertIn("notCommittedDigest", projection["evidence"])
                self.assertEqual(
                    projection["authority"], "not-granted-by-inspection"
                )

    def test_provider_pending_remains_outstanding_reconciliation_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            task_id = "task:w5e:inspection:provider-pending"
            checkpoint = WorkingCheckpoint(
                task_id=task_id,
                objective="Keep pending Provider currentness unresolved.",
                frontier="Inspect Provider commitment.",
                established=(),
                unresolved=("Provider is still pending.",),
                rejected=(),
                constraints=("Pending is not terminal evidence.",),
                next_actions=("Reconcile the original Provider request.",),
                runtime=None,
            )
            capability = CapabilitySnapshot.from_document(
                capability_document(), "2026-08-09T00:00:00Z"
            )
            backend = ProviderBackend()
            transport = ProviderTransport(backend)
            adapter = CloudflareWorldAdapter(transport)
            prepared = adapter.prepare_fetch(
                dispatch_id="dispatch:w5e:inspection:provider-pending",
                effect_id="effect:w5e:inspection:provider-pending",
                url="https://developers.cloudflare.com/",
                capability=capability,
            )
            with HostStorage(directory) as storage:
                clock = itertools.count(3_100_000).__next__
                host = ExternalContinuityHost(
                    storage,
                    clock_ms=clock,
                    owner_id="host:w5e:inspection:provider-pending",
                )
                host.adopt(
                    task_id=task_id,
                    goal_id="goal:w5e:inspection:provider-pending",
                    initial_checkpoint=checkpoint,
                )
                port = HostExtensionPort(
                    storage,
                    HostKernel(
                        storage,
                        clock_ms=clock,
                        owner_id="world:w5e:inspection:provider-pending",
                    ),
                )
                world = HostWorldExtension(port)
                world.prepare(task_id, prepared)
                current = port.load_namespace(task_id, "world")
                projected_data = json.loads(json.dumps(current.data))
                projected_data["worldDispatches"][prepared.dispatch.dispatch_id][
                    "worldOutcomeState"
                ] = "pending"
                projection = world.project_owner_commitments(
                    task_id,
                    projected_data,
                    legacy=False,
                )[0]
                self.assertEqual(projection["state"], "pending")
                self.assertEqual(projection["commitmentClass"], "outstanding")
                self.assertEqual(
                    projection["nextOwnerOperation"], "reconcile-original-request"
                )

    def test_aggregator_does_not_decode_trajectory_storage_fields(self) -> None:
        source = (
            Path(__file__).resolve().parents[1]
            / "src"
            / "ordivon_world"
            / "task_inspection.py"
        ).read_text(encoding="utf-8")
        self.assertIn("project_owner_commitments", source)
        for forbidden in (
            "state_field",
            "plan_digest_field",
            "plan_object_field",
            "receipt_digest_field",
            "uncertainty_object_field",
            "terminal_fields",
            "extra_instance_fields",
            "._instances(",
            "._legacy_entry(",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
