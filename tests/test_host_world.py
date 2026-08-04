from __future__ import annotations

import itertools
import json
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world import (
    CapabilitySnapshot,
    CloudflareWorldAdapter,
    HostWorldExtension,
    PreparedWorldDispatch,
    TransportError,
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

            fresh_transport = ProviderTransport(backend)
            with HostStorage(directory) as reopened:
                fresh_kernel = HostKernel(
                    reopened,
                    clock_ms=clock,
                    owner_id="host:world-test:fresh",
                )
                fresh_extension = HostWorldExtension(
                    HostExtensionPort(reopened, fresh_kernel)
                )
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
                self.assertEqual(snapshot.data["worldOutcomeState"], "succeeded")
                self.assertNotIn("worldUncertaintyDigest", snapshot.data)
                self.assertEqual(snapshot.projection.state, created.state)
                self.assertEqual(
                    snapshot.projection.ready_frontier,
                    created.ready_frontier,
                )


if __name__ == "__main__":
    unittest.main()
