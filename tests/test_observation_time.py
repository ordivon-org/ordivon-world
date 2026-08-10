from __future__ import annotations

import itertools
import tempfile
import time
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world import (
    CapabilitySnapshot,
    CloudflareWorldAdapter,
    HostWorldExtension,
    WorldObservation,
    WorldTaskInspector,
)
from tests.test_cloudflare_adapter import (
    FakeCloudflareTransport,
    capability_document,
)


class ObservationAvailabilityTests(unittest.TestCase):
    def adapter_and_prepared(self) -> tuple[FakeCloudflareTransport, CloudflareWorldAdapter, object]:
        transport = FakeCloudflareTransport()
        adapter = CloudflareWorldAdapter(transport)
        capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-10T06:00:00Z",
        )
        prepared = adapter.prepare_fetch(
            dispatch_id="dispatch:world:p2-time:fetch:r1",
            effect_id="effect:world:p2-time:fetch:r1",
            url="https://developers.cloudflare.com/",
            capability=capability,
        )
        transport.prepared_value = prepared.to_dict()
        return transport, adapter, prepared

    def test_world_observation_retains_provider_time_and_world_availability_separately(self) -> None:
        _transport, adapter, prepared = self.adapter_and_prepared()
        observation = adapter.deliver(prepared, check_conditions=False)
        value = observation.to_dict()
        self.assertEqual(value["receipt"]["completed_at"], "2026-08-04T00:00:01Z")
        self.assertIsNotNone(observation.available_at)
        self.assertEqual(value["availableAt"], observation.available_at)
        self.assertNotEqual(value["availableAt"], value["receipt"]["completed_at"])

    def test_legacy_observation_without_available_at_remains_readable(self) -> None:
        _transport, adapter, prepared = self.adapter_and_prepared()
        value = adapter.deliver(prepared, check_conditions=False).to_dict()
        value.pop("availableAt")
        restored = WorldObservation.from_dict(value)
        self.assertIsNone(restored.available_at)
        self.assertEqual(restored.receipt["completed_at"], "2026-08-04T00:00:01Z")

    def test_agent_inspection_projects_temporal_evidence_without_promoting_currentness(self) -> None:
        transport, adapter, prepared = self.adapter_and_prepared()
        transport.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(5_000_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(storage, clock_ms=clock, owner_id="host:world:p2-time")
                created = kernel.create_task(
                    event_id="event:world:p2-time:created",
                    kind=EventKind.TASK_CREATED,
                    task_id="task:world:p2-time",
                    goal_id="goal:world:p2-time",
                    payload={"scenario": "temporal-evidence"},
                    frontier=("node:world:p2-time",),
                ).projection
                port = HostExtensionPort(storage, kernel)
                world = HostWorldExtension(port)
                world.prepare(created.task_id, prepared)
                unknown = world.deliver(created.task_id, adapter, check_conditions=False)
                self.assertEqual(unknown.status, "unknown")
                recovered = world.reconcile(created.task_id, CloudflareWorldAdapter(transport))
                self.assertIsNotNone(recovered.observation)
                assert recovered.observation is not None
                inspection = WorldTaskInspector(port).inspect_task(
                    created.task_id,
                    expected_revision=recovered.task_revision,
                )

            provider = next(
                item
                for item in inspection["commitments"]
                if item["family"] == "provider-dispatch"
            )
            temporal = provider["temporalEvidence"]
            self.assertEqual(temporal["providerStartedAt"], "2026-08-04T00:00:00Z")
            self.assertEqual(temporal["providerCompletedAt"], "2026-08-04T00:00:01Z")
            self.assertEqual(temporal["availableAt"], recovered.observation.available_at)
            self.assertEqual(temporal["providerTimeSource"], "cloudflare-receipt")
            self.assertEqual(temporal["availabilityTimeSource"], "world.cloudflare")
            self.assertEqual(provider["authority"], "not-granted-by-inspection")
            self.assertEqual(provider["externalCurrentness"], "not-claimed")

    def test_repeated_reconciliation_preserves_first_availability_and_revision(self) -> None:
        transport, adapter, prepared = self.adapter_and_prepared()
        transport.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(6_000_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(storage, clock_ms=clock, owner_id="host:world:p2-repeat")
                created = kernel.create_task(
                    event_id="event:world:p2-repeat:created",
                    kind=EventKind.TASK_CREATED,
                    task_id="task:world:p2-repeat",
                    goal_id="goal:world:p2-repeat",
                    payload={"scenario": "repeat-reconcile"},
                    frontier=("node:world:p2-repeat",),
                ).projection
                world = HostWorldExtension(HostExtensionPort(storage, kernel))
                world.prepare(created.task_id, prepared)
                unknown = world.deliver(created.task_id, adapter, check_conditions=False)
                self.assertEqual(unknown.status, "unknown")
                fresh = CloudflareWorldAdapter(transport)
                first = world.reconcile(created.task_id, fresh)
                self.assertIsNotNone(first.observation)
                assert first.observation is not None
                first_available_at = first.observation.available_at
                first_revision = first.task_revision
                time.sleep(0.002)
                second = world.reconcile(created.task_id, fresh)
                self.assertIsNotNone(second.observation)
                assert second.observation is not None
                self.assertEqual(second.task_revision, first_revision)
                self.assertEqual(second.observation.available_at, first_available_at)
                self.assertEqual(transport.posts, 1)


if __name__ == "__main__":
    unittest.main()
