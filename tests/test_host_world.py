from __future__ import annotations

import itertools
import json
import tempfile
import unittest

from ordivon_host import (
    EventKind,
    ExternalContinuityHost,
    HostExtensionPort,
    HostKernel,
    HostStorage,
    WorkingCheckpoint,
)

from ordivon_world import (
    CapabilitySnapshot,
    CloudflareWorldAdapter,
    HostWorldError,
    HostWorldExtension,
    PreparedWorldDispatch,
    TransportError,
    WorldOutcomeUnknown,
)
from ordivon_world.canonical import sha256_hex
from ordivon_world.cloudflare import HttpResponse


def capability_document() -> dict[str, object]:
    return {
        "schema_version": 1,
        "service": "ordivon-edge",
        "policy_version": "p1.6.test",
        "retention": {
            "idempotency_days": 90,
            "request_state_days": 90,
            "receipt_mirror_days": 90,
            "artifact_days": 91,
            "cleanup_task_days": 90,
        },
        "capabilities": [
            {
                "id": "artifact.get",
                "version": "artifact.get.v1",
                "state": "ready",
                "reason": "private artifact reads",
            },
            {
                "id": "fetch",
                "version": "fetch.v2",
                "state": "ready",
                "reason": "bounded fetch",
            },
            {
                "id": "browser.run",
                "version": "browser.snapshot.v2",
                "state": "ready",
                "reason": "bounded browser snapshot",
            },
            {
                "id": "receipt",
                "version": "receipt.v2",
                "state": "ready",
                "reason": "durable receipts",
            },
        ],
        "worker_version": {
            "id": "worker-test",
            "tag": "git-111111111111-src-2222222222222222-1",
            "timestamp": "2026-08-04T00:00:00Z",
        },
        "deployment_identity": {
            "source_commit": "111111111111",
            "worker_release_digest": "2222222222222222",
        },
    }


class ProviderBackend:
    def __init__(self) -> None:
        self.receipts: dict[str, dict[str, object]] = {}
        self.posts = 0
        self.drop_after_commit = True


class ProviderTransport:
    def __init__(self, backend: ProviderBackend) -> None:
        self.backend = backend
        self.prepared: PreparedWorldDispatch | None = None

    def request(
        self,
        method: str,
        path: str,
        *,
        body: bytes = b"",
        request_id: str,
        extra_headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        if method == "GET" and path == "/v1/capabilities":
            return HttpResponse(200, {}, json.dumps(capability_document()).encode())
        if method == "POST" and path == "/v1/fetch":
            assert self.prepared is not None
            self.backend.posts += 1
            artifact_body = b"host-world-result"
            artifact = {
                "key": f"fetch/v2/{request_id}/g1/body",
                "sha256": sha256_hex(artifact_body),
                "bytes": len(artifact_body),
                "media_type": "text/plain",
                "etag": '"etag"',
            }
            receipt = {
                "schema_version": 1,
                "receipt_id": request_id,
                "request_digest": self.prepared.provider_request_digest,
                "operation": "fetch",
                "status": "succeeded",
                "started_at": "2026-08-04T00:00:00Z",
                "completed_at": "2026-08-04T00:00:01Z",
                "duration_ms": 1000,
                "execution": {
                    "policy_version": "p1.6.test",
                    "capability_version": "fetch.v2",
                    "worker_version_id": "worker-test",
                    "worker_version_tag": "git-111111111111-src-2222222222222222-1",
                    "worker_version_timestamp": "2026-08-04T00:00:00Z",
                    "lease_generation": 1,
                },
                "artifact": artifact,
                "artifacts": [artifact],
                "fetch": {
                    "requested_url": self.prepared.request["url"],
                    "final_url": self.prepared.request["url"],
                    "http_status": 200,
                    "redirect_count": 0,
                },
            }
            self.backend.receipts[request_id] = receipt
            if self.backend.drop_after_commit:
                self.backend.drop_after_commit = False
                raise TransportError("response lost after commit")
            return HttpResponse(
                200,
                {},
                json.dumps({"receipt": receipt, "replayed": True}).encode(),
            )
        if method == "GET" and path.startswith("/v1/receipts/"):
            value = self.backend.receipts.get(path.rsplit("/", 1)[-1])
            if value is None:
                return HttpResponse(404, {}, b'{"error":"receipt_not_found"}')
            return HttpResponse(200, {}, json.dumps(value).encode())
        raise AssertionError((method, path, body, request_id, extra_headers))


class HostWorldExtensionTests(unittest.TestCase):
    def test_fresh_host_recovers_provider_commit_without_redispatch(self) -> None:
        capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-04T00:00:00Z",
        )
        backend = ProviderBackend()
        first_transport = ProviderTransport(backend)
        first_adapter = CloudflareWorldAdapter(first_transport)
        prepared = first_adapter.prepare_fetch(
            dispatch_id="dispatch:world:host-test:r1",
            effect_id="effect:world:host-test:r1",
            url="https://developers.cloudflare.com/",
            capability=capability,
        )
        first_transport.prepared = prepared

        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(10_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(
                    storage,
                    clock_ms=clock,
                    owner_id="host:world-test:first",
                )
                created = kernel.create_task(
                    event_id="event:world-host-test:create",
                    kind=EventKind.TASK_CREATED,
                    task_id="task:world-host-test",
                    goal_id="goal:world-host-test",
                    payload={"scenario": "response-loss"},
                    frontier=("node:world-host-test",),
                ).projection
                extension = HostWorldExtension(HostExtensionPort(storage, kernel))
                prepared_step = extension.prepare(created.task_id, prepared)
                unknown = extension.deliver(
                    created.task_id,
                    first_adapter,
                    check_conditions=False,
                )
                self.assertEqual(prepared_step.status, "prepared")
                self.assertEqual(unknown.status, "unknown")
                self.assertEqual(backend.posts, 1)
                snapshot = storage.read_task_event(created.task_id)
                self.assertEqual(snapshot.projection.state, created.state)
                self.assertEqual(
                    snapshot.projection.ready_frontier,
                    created.ready_frontier,
                )
                self.assertEqual(snapshot.event_kind, EventKind("world.outcome-unknown"))
                entry = snapshot.data["worldDispatches"][prepared.dispatch.dispatch_id]
                self.assertEqual(entry["worldOutcomeState"], "unknown")

            fresh_transport = ProviderTransport(backend)
            with HostStorage(directory) as reopened:
                fresh_kernel = HostKernel(
                    reopened,
                    clock_ms=clock,
                    owner_id="host:world-test:fresh",
                )
                fresh_extension = HostWorldExtension(HostExtensionPort(reopened, fresh_kernel))
                restored = fresh_extension.load_prepared("task:world-host-test")
                fresh_transport.prepared = restored
                recovered = fresh_extension.reconcile(
                    "task:world-host-test",
                    CloudflareWorldAdapter(fresh_transport),
                )
                self.assertEqual(recovered.status, "succeeded")
                self.assertTrue(recovered.reconciled)
                self.assertIsNotNone(recovered.observation)
                self.assertEqual(backend.posts, 1)
                snapshot = reopened.read_task_event("task:world-host-test")
                self.assertEqual(
                    snapshot.event_kind,
                    EventKind("world.dispatch-observed"),
                )
                entry = snapshot.data["worldDispatches"][prepared.dispatch.dispatch_id]
                self.assertEqual(entry["worldOutcomeState"], "succeeded")
                self.assertNotIn("worldUncertaintyDigest", entry)
                self.assertEqual(snapshot.projection.state, created.state)
                self.assertEqual(
                    snapshot.projection.ready_frontier,
                    created.ready_frontier,
                )

    def test_provider_unknown_survives_later_host_core_checkpoint(self) -> None:
        capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-09T00:00:00Z",
        )
        backend = ProviderBackend()
        first_transport = ProviderTransport(backend)
        first_adapter = CloudflareWorldAdapter(first_transport)
        prepared = first_adapter.prepare_fetch(
            dispatch_id="dispatch:world:e0-core-checkpoint",
            effect_id="effect:world:e0-core-checkpoint",
            url="https://example.invalid/e0-core-checkpoint",
            capability=capability,
        )
        first_transport.prepared = prepared

        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(15_000).__next__
            checkpoint = WorkingCheckpoint(
                task_id="task:world:e0-core-checkpoint",
                objective="Preserve World owner state across Host semantic checkpoints.",
                frontier="Reconcile the exact unknown Provider request.",
                established=(),
                unresolved=("Provider outcome is not yet known.",),
                rejected=(),
                constraints=("Do not redispatch the Provider request.",),
                next_actions=("Reconcile the original Provider request.",),
                runtime=None,
            )
            with HostStorage(directory) as storage:
                host = ExternalContinuityHost(
                    storage,
                    clock_ms=clock,
                    owner_id="host:world-e0:first",
                )
                adopted = host.adopt(
                    task_id=checkpoint.task_id,
                    goal_id="goal:world:e0-core-checkpoint",
                    initial_checkpoint=checkpoint,
                )
                extension = HostWorldExtension(
                    HostExtensionPort(
                        storage,
                        HostKernel(
                            storage,
                            clock_ms=clock,
                            owner_id="world:e0:first",
                        ),
                    )
                )
                extension.prepare(checkpoint.task_id, prepared)
                unknown = extension.deliver(
                    checkpoint.task_id,
                    first_adapter,
                    check_conditions=False,
                )
                self.assertEqual(unknown.status, "unknown")
                self.assertEqual(backend.posts, 1)
                later = WorkingCheckpoint(
                    task_id=checkpoint.task_id,
                    objective=checkpoint.objective,
                    frontier="Fresh controller must recover World owner state.",
                    established=("Host semantic work advanced after World UNKNOWN.",),
                    unresolved=("World owner reconciliation remains outstanding.",),
                    rejected=(),
                    constraints=checkpoint.constraints,
                    next_actions=checkpoint.next_actions,
                    runtime=None,
                )
                core = host.checkpoint(
                    task_id=checkpoint.task_id,
                    expected_revision=unknown.task_revision,
                    checkpoint=later,
                    disposition="continue",
                )
                self.assertGreater(core.projection.revision, adopted.projection.revision)
                current = storage.read_task_event(checkpoint.task_id)
                self.assertEqual(current.event_kind, EventKind.TASK_CONTEXT_CHECKPOINTED)
                self.assertNotIn("worldDispatches", current.data)

            fresh_transport = ProviderTransport(backend)
            with HostStorage(directory) as reopened:
                fresh_extension = HostWorldExtension(
                    HostExtensionPort(
                        reopened,
                        HostKernel(
                            reopened,
                            clock_ms=clock,
                            owner_id="world:e0:fresh",
                        ),
                    )
                )
                restored = fresh_extension.load_prepared(checkpoint.task_id)
                self.assertEqual(restored, prepared)
                fresh_transport.prepared = restored
                recovered = fresh_extension.reconcile(
                    checkpoint.task_id,
                    CloudflareWorldAdapter(fresh_transport),
                )
                self.assertEqual(recovered.status, "succeeded")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(backend.posts, 1)
                world = fresh_extension.port.load_namespace(checkpoint.task_id, "world")
                entry = world.data["worldDispatches"][prepared.dispatch.dispatch_id]
                self.assertEqual(entry["worldOutcomeState"], "succeeded")
                self.assertNotIn("worldUncertaintyDigest", entry)
                self.assertEqual(world.projection.revision, recovered.task_revision)

    def test_one_task_supports_sequential_provider_dispatches_and_requires_identity_when_ambiguous(
        self,
    ) -> None:
        capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-08T00:00:00Z",
        )
        backend = ProviderBackend()
        backend.drop_after_commit = False
        transport = ProviderTransport(backend)
        adapter = CloudflareWorldAdapter(transport)
        first = adapter.prepare_fetch(
            dispatch_id="dispatch:world:w2-p5:1",
            effect_id="effect:world:w2-p5:1",
            url="https://example.invalid/w2-p5/1",
            capability=capability,
        )
        second = adapter.prepare_fetch(
            dispatch_id="dispatch:world:w2-p5:2",
            effect_id="effect:world:w2-p5:2",
            url="https://example.invalid/w2-p5/2",
            capability=capability,
        )
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=itertools.count(20_000).__next__,
                owner_id="host:w2-p5",
            )
            created = kernel.create_task(
                event_id="event:w2-p5:create",
                kind=EventKind.TASK_CREATED,
                task_id="task:w2-p5",
                goal_id="goal:w2-p5",
                payload={"goal": "perform two sequential provider fetches"},
                frontier=("node:w2-p5",),
            ).projection
            extension = HostWorldExtension(HostExtensionPort(storage, kernel))
            extension.prepare(created.task_id, first)
            transport.prepared = first
            first_done = extension.deliver(
                created.task_id,
                adapter,
                check_conditions=False,
                dispatch_id=first.dispatch.dispatch_id,
            )
            extension.prepare(created.task_id, second)
            transport.prepared = second
            second_done = extension.deliver(
                created.task_id,
                adapter,
                check_conditions=False,
                dispatch_id=second.dispatch.dispatch_id,
            )
            self.assertEqual(first_done.status, "succeeded")
            self.assertEqual(second_done.status, "succeeded")
            self.assertEqual(backend.posts, 2)
            self.assertEqual(
                extension.dispatch_ids(created.task_id),
                tuple(sorted((first.dispatch.dispatch_id, second.dispatch.dispatch_id))),
            )
            with self.assertRaisesRegex(HostWorldError, "dispatch identity is required"):
                extension.load_prepared(created.task_id)
            with self.assertRaisesRegex(HostWorldError, "dispatch identity is required"):
                extension.deliver(created.task_id, adapter, check_conditions=False)
            snapshot = storage.read_task_event(created.task_id)
            entries = snapshot.data["worldDispatches"]
            self.assertEqual(entries[first.dispatch.dispatch_id]["worldOutcomeState"], "succeeded")
            self.assertEqual(entries[second.dispatch.dispatch_id]["worldOutcomeState"], "succeeded")
            self.assertEqual(snapshot.projection.state, created.state)
            self.assertEqual(snapshot.projection.ready_frontier, created.ready_frontier)

    def test_second_provider_unknown_reconciles_independently_after_host_restart(self) -> None:
        capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-08T00:00:00Z",
        )
        backend = ProviderBackend()
        backend.drop_after_commit = False
        transport = ProviderTransport(backend)
        adapter = CloudflareWorldAdapter(transport)
        first = adapter.prepare_fetch(
            dispatch_id="dispatch:world:w2-p5:partial:1",
            effect_id="effect:world:w2-p5:partial:1",
            url="https://example.invalid/w2-p5/partial/1",
            capability=capability,
        )
        second = adapter.prepare_fetch(
            dispatch_id="dispatch:world:w2-p5:partial:2",
            effect_id="effect:world:w2-p5:partial:2",
            url="https://example.invalid/w2-p5/partial/2",
            capability=capability,
        )
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(30_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(
                    storage,
                    clock_ms=clock,
                    owner_id="host:w2-p5:first",
                )
                created = kernel.create_task(
                    event_id="event:w2-p5:partial:create",
                    kind=EventKind.TASK_CREATED,
                    task_id="task:w2-p5:partial",
                    goal_id="goal:w2-p5:partial",
                    payload={"goal": "two provider fetches with second response loss"},
                    frontier=("node:w2-p5:partial",),
                ).projection
                extension = HostWorldExtension(HostExtensionPort(storage, kernel))
                extension.prepare(created.task_id, first)
                transport.prepared = first
                first_done = extension.deliver(
                    created.task_id,
                    adapter,
                    check_conditions=False,
                    dispatch_id=first.dispatch.dispatch_id,
                )
                backend.drop_after_commit = True
                extension.prepare(created.task_id, second)
                transport.prepared = second
                second_unknown = extension.deliver(
                    created.task_id,
                    adapter,
                    check_conditions=False,
                    dispatch_id=second.dispatch.dispatch_id,
                )
                self.assertEqual(first_done.status, "succeeded")
                self.assertEqual(second_unknown.status, "unknown")
                self.assertEqual(backend.posts, 2)
                snapshot = storage.read_task_event(created.task_id)
                entries = snapshot.data["worldDispatches"]
                self.assertEqual(
                    entries[first.dispatch.dispatch_id]["worldOutcomeState"], "succeeded"
                )
                self.assertEqual(
                    entries[second.dispatch.dispatch_id]["worldOutcomeState"], "unknown"
                )
                first_observation_digest = entries[first.dispatch.dispatch_id][
                    "worldObservationDigest"
                ]

            fresh_transport = ProviderTransport(backend)
            with HostStorage(directory) as reopened:
                fresh_kernel = HostKernel(
                    reopened,
                    clock_ms=clock,
                    owner_id="host:w2-p5:fresh",
                )
                fresh_extension = HostWorldExtension(HostExtensionPort(reopened, fresh_kernel))
                restored = fresh_extension.load_prepared(
                    "task:w2-p5:partial",
                    second.dispatch.dispatch_id,
                )
                fresh_transport.prepared = restored
                recovered = fresh_extension.reconcile(
                    "task:w2-p5:partial",
                    CloudflareWorldAdapter(fresh_transport),
                    dispatch_id=second.dispatch.dispatch_id,
                )
                self.assertEqual(recovered.status, "succeeded")
                self.assertTrue(recovered.reconciled)
                self.assertEqual(backend.posts, 2)
                snapshot = reopened.read_task_event("task:w2-p5:partial")
                entries = snapshot.data["worldDispatches"]
                self.assertEqual(
                    entries[first.dispatch.dispatch_id]["worldOutcomeState"], "succeeded"
                )
                self.assertEqual(
                    entries[first.dispatch.dispatch_id]["worldObservationDigest"],
                    first_observation_digest,
                )
                self.assertEqual(
                    entries[second.dispatch.dispatch_id]["worldOutcomeState"], "succeeded"
                )
                self.assertNotIn("worldUncertaintyDigest", entries[second.dispatch.dispatch_id])
                self.assertEqual(snapshot.projection.state, created.state)
                self.assertEqual(snapshot.projection.ready_frontier, created.ready_frontier)

    def test_pre_p5_flat_unknown_reconciles_without_redispatch_and_migrates(self) -> None:
        capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-08T00:00:00Z",
        )
        backend = ProviderBackend()
        transport = ProviderTransport(backend)
        adapter = CloudflareWorldAdapter(transport)
        prepared = adapter.prepare_fetch(
            dispatch_id="dispatch:world:w2-p5:legacy-unknown",
            effect_id="effect:world:w2-p5:legacy-unknown",
            url="https://example.invalid/w2-p5/legacy-unknown",
            capability=capability,
        )
        transport.prepared = prepared
        with self.assertRaises(WorldOutcomeUnknown):
            adapter.deliver(prepared, check_conditions=False)
        self.assertEqual(backend.posts, 1)

        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=itertools.count(35_000).__next__,
                owner_id="host:w2-p5:legacy-unknown",
            )
            created = kernel.create_task(
                event_id="event:w2-p5:legacy-unknown:create",
                kind=EventKind.TASK_CREATED,
                task_id="task:w2-p5:legacy-unknown",
                goal_id="goal:w2-p5:legacy-unknown",
                payload={"scenario": "pre-p5-flat-provider-unknown"},
                frontier=("node:w2-p5:legacy-unknown",),
            ).projection
            port = HostExtensionPort(storage, kernel)
            prepared_object = port.put_object(
                prepared.to_dict(),
                kind="world-prepared-dispatch",
            )
            uncertainty = {
                "schemaVersion": 1,
                "kind": "ordivon.world-outcome-uncertainty",
                "dispatchId": prepared.dispatch.dispatch_id,
                "provider": "cloudflare",
                "providerRequestId": prepared.provider_request_id,
                "providerRequestDigest": prepared.provider_request_digest,
                "status": "unknown",
                "reason": "legacy response loss",
                "nextAction": "reconcile-original-request",
            }
            uncertainty_object = port.put_object(
                uncertainty,
                kind="world-outcome-uncertainty",
            )
            port.append_preserving(
                task_id=created.task_id,
                expected_revision=created.revision,
                event_id="event:w2-p5:legacy-unknown:flat",
                kind=EventKind("world.outcome-unknown"),
                updates={
                    "worldPreparedDispatchDigest": prepared_object.digest,
                    "worldDispatchId": prepared.dispatch.dispatch_id,
                    "worldProviderRequestId": prepared.provider_request_id,
                    "worldOutcomeState": "unknown",
                    "worldUncertaintyDigest": uncertainty_object.digest,
                },
                referenced_objects=(prepared_object, uncertainty_object),
                label="World",
            )
            extension = HostWorldExtension(port)
            self.assertEqual(extension.load_prepared(created.task_id), prepared)
            recovered = extension.reconcile(created.task_id, adapter)
            self.assertEqual(recovered.status, "succeeded")
            self.assertTrue(recovered.reconciled)
            self.assertEqual(backend.posts, 1)
            snapshot = storage.read_task_event(created.task_id)
            entry = snapshot.data["worldDispatches"][prepared.dispatch.dispatch_id]
            self.assertEqual(entry["worldOutcomeState"], "succeeded")
            self.assertNotIn("worldUncertaintyDigest", entry)
            self.assertIn("worldObservationDigest", entry)
            self.assertNotIn("worldPreparedDispatchDigest", snapshot.data)
            self.assertNotIn("worldDispatchId", snapshot.data)
            self.assertNotIn("worldOutcomeState", snapshot.data)
            self.assertEqual(snapshot.projection.state, created.state)
            self.assertEqual(snapshot.projection.ready_frontier, created.ready_frontier)

    def test_pre_p5_flat_provider_dispatch_is_readable_and_migrates_with_second_dispatch(
        self,
    ) -> None:
        capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-08T00:00:00Z",
        )
        backend = ProviderBackend()
        backend.drop_after_commit = False
        transport = ProviderTransport(backend)
        adapter = CloudflareWorldAdapter(transport)
        first = adapter.prepare_fetch(
            dispatch_id="dispatch:world:w2-p5:legacy:1",
            effect_id="effect:world:w2-p5:legacy:1",
            url="https://example.invalid/w2-p5/legacy/1",
            capability=capability,
        )
        second = adapter.prepare_fetch(
            dispatch_id="dispatch:world:w2-p5:legacy:2",
            effect_id="effect:world:w2-p5:legacy:2",
            url="https://example.invalid/w2-p5/legacy/2",
            capability=capability,
        )
        with tempfile.TemporaryDirectory() as directory, HostStorage(directory) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=itertools.count(40_000).__next__,
                owner_id="host:w2-p5:legacy",
            )
            created = kernel.create_task(
                event_id="event:w2-p5:legacy:create",
                kind=EventKind.TASK_CREATED,
                task_id="task:w2-p5:legacy",
                goal_id="goal:w2-p5:legacy",
                payload={"scenario": "pre-p5-flat-provider"},
                frontier=("node:w2-p5:legacy",),
            ).projection
            port = HostExtensionPort(storage, kernel)
            prepared_object = port.put_object(first.to_dict(), kind="world-prepared-dispatch")
            port.append_preserving(
                task_id=created.task_id,
                expected_revision=created.revision,
                event_id="event:w2-p5:legacy:flat",
                kind=EventKind("world.dispatch-prepared"),
                updates={
                    "worldPreparedDispatchDigest": prepared_object.digest,
                    "worldDispatchId": first.dispatch.dispatch_id,
                    "worldProviderRequestId": first.provider_request_id,
                    "worldOutcomeState": "prepared",
                },
                referenced_objects=(prepared_object,),
                label="World",
            )
            extension = HostWorldExtension(port)
            self.assertEqual(extension.load_prepared(created.task_id), first)
            self.assertEqual(extension.dispatch_ids(created.task_id), (first.dispatch.dispatch_id,))
            extension.prepare(created.task_id, second)
            snapshot = storage.read_task_event(created.task_id)
            entries = snapshot.data["worldDispatches"]
            self.assertEqual(
                set(entries), {first.dispatch.dispatch_id, second.dispatch.dispatch_id}
            )
            self.assertEqual(
                entries[first.dispatch.dispatch_id]["worldPreparedDispatchDigest"],
                prepared_object.digest,
            )
            self.assertNotIn("worldPreparedDispatchDigest", snapshot.data)
            self.assertNotIn("worldDispatchId", snapshot.data)
            self.assertNotIn("worldProviderRequestId", snapshot.data)
            self.assertEqual(
                extension.load_prepared(created.task_id, first.dispatch.dispatch_id),
                first,
            )
            self.assertEqual(
                extension.load_prepared(created.task_id, second.dispatch.dispatch_id),
                second,
            )


if __name__ == "__main__":
    unittest.main()
