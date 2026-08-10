from __future__ import annotations

from ordivon_world.browser import BrowserBundleError
from ordivon_world.cloudflare import (
    CapabilitySnapshot,
    CloudflareWorldAdapter,
    PreparedWorldDispatch,
    TransportError,
    WorldProviderError,
)
from ordivon_world.host import HostWorldExtension

import itertools
import json
import tempfile
import unittest

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage


from ordivon_world.canonical import sha256_hex
from ordivon_world.cloudflare import HttpResponse

_PNG = b"\x89PNG\r\n\x1a\n" + b"browser-screenshot"
_HTML = b"<!doctype html><title>Browser Bundle</title><p>rendered</p>"


def capability_document() -> dict[str, object]:
    return {
        "schema_version": 1,
        "service": "ordivon-edge",
        "policy_version": "p1.6.browser-test",
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
            "id": "browser-worker-test",
            "tag": "git-111111111111-src-2222222222222222-1",
            "timestamp": "2026-08-04T00:00:00Z",
        },
        "deployment_identity": {
            "source_commit": "111111111111",
            "worker_release_digest": "2222222222222222",
        },
    }


class BrowserBackend:
    def __init__(self) -> None:
        self.receipts: dict[str, dict[str, object]] = {}
        self.artifacts: dict[str, bytes] = {}
        self.media_types: dict[str, str] = {}
        self.posts = 0
        self.drop_after_commit = False
        self.manifest_browser_override: dict[str, object] | None = None
        self.media_type_override: dict[str, str] = {}


class BrowserTransport:
    def __init__(self, backend: BrowserBackend) -> None:
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
        if method == "POST" and path == "/v1/browser/run":
            assert self.prepared is not None
            self.backend.posts += 1
            receipt = self._commit_browser(self.prepared)
            if self.backend.drop_after_commit:
                self.backend.drop_after_commit = False
                raise TransportError("response lost after Browser provider commit")
            return HttpResponse(
                200,
                {},
                json.dumps({"receipt": receipt, "replayed": self.backend.posts > 1}).encode(),
            )
        if method == "GET" and path.startswith("/v1/receipts/"):
            value = self.backend.receipts.get(path.rsplit("/", 1)[-1])
            if value is None:
                return HttpResponse(404, {}, b'{"error":"receipt_not_found"}')
            return HttpResponse(200, {}, json.dumps(value).encode())
        if method == "GET" and path.startswith("/v1/artifacts/"):
            key = path.removeprefix("/v1/artifacts/")
            value = self.backend.artifacts.get(key)
            if value is None:
                return HttpResponse(404, {}, b"")
            media_type = self.backend.media_type_override.get(
                key,
                self.backend.media_types[key],
            )
            return HttpResponse(
                200,
                {
                    "content-type": "application/octet-stream",
                    "content-length": str(len(value)),
                    "etag": '"browser-test-etag"',
                    "x-ordivon-media-type": media_type,
                    "x-ordivon-sha256": sha256_hex(value),
                },
                value,
            )
        raise AssertionError((method, path, request_id, extra_headers, body))

    def _commit_browser(
        self,
        prepared: PreparedWorldDispatch,
    ) -> dict[str, object]:
        request_id = prepared.provider_request_id
        base = f"browser/v2/{request_id}/g1"
        browser: dict[str, object] = {
            "requested_url": prepared.request["url"],
            "final_url_observed": False,
            "page_title": "Browser Bundle",
            "page_status": 200,
            "browser_ms": 321,
            "viewport": {
                "width": prepared.request["viewport_width"],
                "height": prepared.request["viewport_height"],
            },
            "full_page": prepared.request["full_page"],
        }
        execution = {
            "policy_version": "p1.6.browser-test",
            "capability_version": "browser.snapshot.v2",
            "worker_version_id": "browser-worker-test",
            "worker_version_tag": "git-111111111111-src-2222222222222222-1",
            "worker_version_timestamp": "2026-08-04T00:00:00Z",
            "lease_generation": 1,
        }
        screenshot = self._store(
            f"{base}/screenshot.png",
            _PNG,
            "image/png",
        )
        content = self._store(
            f"{base}/content.html",
            _HTML,
            "text/html; charset=utf-8",
        )
        manifest_browser = self.backend.manifest_browser_override or browser
        manifest_document = {
            "schema_version": 2,
            "receipt_id": request_id,
            "execution": execution,
            "browser": manifest_browser,
            "artifacts": [screenshot, content],
        }
        manifest_body = json.dumps(
            manifest_document,
            separators=(",", ":"),
        ).encode()
        manifest = self._store(
            f"{base}/manifest.json",
            manifest_body,
            "application/json; charset=utf-8",
        )
        receipt: dict[str, object] = {
            "schema_version": 1,
            "receipt_id": request_id,
            "request_digest": prepared.provider_request_digest,
            "operation": "browser.run",
            "status": "succeeded",
            "started_at": "2026-08-04T00:00:00Z",
            "completed_at": "2026-08-04T00:00:01Z",
            "duration_ms": 1000,
            "execution": execution,
            "artifact": manifest,
            "artifacts": [screenshot, content, manifest],
            "browser": browser,
        }
        self.backend.receipts[request_id] = receipt
        return receipt

    def _store(
        self,
        key: str,
        body: bytes,
        media_type: str,
    ) -> dict[str, object]:
        self.backend.artifacts[key] = body
        self.backend.media_types[key] = media_type
        return {
            "key": key,
            "sha256": sha256_hex(body),
            "bytes": len(body),
            "media_type": media_type,
            "etag": '"browser-test-etag"',
        }


class BrowserBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.backend = BrowserBackend()
        self.transport = BrowserTransport(self.backend)
        self.adapter = CloudflareWorldAdapter(self.transport)
        self.capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-04T00:00:00Z",
        )

    def prepare(self) -> PreparedWorldDispatch:
        prepared = self.adapter.prepare_browser(
            dispatch_id="dispatch:world:browser-test:r1",
            effect_id="effect:world:browser-test:r1",
            url="https://developers.cloudflare.com/",
            capability=self.capability,
            viewport_width=1280,
            viewport_height=720,
        )
        self.transport.prepared = prepared
        return prepared

    def test_bundle_verifies_receipt_manifest_and_all_artifacts(self) -> None:
        observation = self.adapter.deliver(self.prepare(), check_conditions=False)
        bundle = self.adapter.read_browser_bundle(observation)
        self.assertEqual(bundle.receipt_id, observation.receipt["receipt_id"])
        self.assertEqual(bundle.screenshot.body, _PNG)
        self.assertEqual(bundle.content.body, _HTML)
        self.assertEqual(len(bundle.artifacts), 3)
        self.assertEqual(bundle.browser["page_title"], "Browser Bundle")

    def test_receipt_content_identity_drift_fails_closed(self) -> None:
        observation = self.adapter.deliver(self.prepare(), check_conditions=False)
        screenshot = observation.receipt["artifacts"][0]
        assert isinstance(screenshot, dict)
        original_digest = screenshot["sha256"]
        original_bytes = screenshot["bytes"]

        screenshot["bytes"] = int(original_bytes) + 1
        with self.assertRaisesRegex(BrowserBundleError, "byte count differs"):
            self.adapter.read_browser_bundle(observation)

        screenshot["bytes"] = original_bytes
        screenshot["sha256"] = "0" * 64
        with self.assertRaisesRegex(BrowserBundleError, "Host digest differs"):
            self.adapter.read_browser_bundle(observation)

        screenshot["sha256"] = original_digest
        bundle = self.adapter.read_browser_bundle(observation)
        self.assertEqual(bundle.screenshot.body, _PNG)

    def test_manifest_semantic_drift_fails_after_digest_verification(self) -> None:
        self.backend.manifest_browser_override = {
            "requested_url": "https://developers.cloudflare.com/",
            "final_url_observed": False,
            "page_title": "Tampered title",
            "page_status": 200,
            "browser_ms": 321,
            "viewport": {"width": 1280, "height": 720},
            "full_page": False,
        }
        observation = self.adapter.deliver(self.prepare(), check_conditions=False)
        with self.assertRaises(BrowserBundleError):
            self.adapter.read_browser_bundle(observation)

    def test_download_media_type_drift_fails_closed(self) -> None:
        observation = self.adapter.deliver(self.prepare(), check_conditions=False)
        screenshot_key = str(observation.receipt["artifacts"][0]["key"])
        self.backend.media_type_override[screenshot_key] = "application/octet-stream"
        with self.assertRaises(WorldProviderError):
            self.adapter.read_browser_bundle(observation)

    def test_fresh_host_recovers_browser_bundle_without_second_post(self) -> None:
        prepared = self.prepare()
        self.backend.drop_after_commit = True
        with tempfile.TemporaryDirectory() as directory:
            clock = itertools.count(20_000).__next__
            with HostStorage(directory) as storage:
                kernel = HostKernel(
                    storage,
                    clock_ms=clock,
                    owner_id="host:browser-test:first",
                )
                created = kernel.create_task(
                    event_id="event:browser-test:create",
                    kind=EventKind.TASK_CREATED,
                    task_id="task:browser-test",
                    goal_id="goal:browser-test",
                    payload={"scenario": "browser-response-loss"},
                    frontier=("node:browser-test",),
                ).projection
                extension = HostWorldExtension(HostExtensionPort(storage, kernel))
                extension.prepare(created.task_id, prepared)
                unknown = extension.deliver(
                    created.task_id,
                    self.adapter,
                    check_conditions=False,
                )
                self.assertEqual(unknown.status, "unknown")
                self.assertEqual(self.backend.posts, 1)

            fresh_transport = BrowserTransport(self.backend)
            fresh_adapter = CloudflareWorldAdapter(fresh_transport)
            with HostStorage(directory) as reopened:
                kernel = HostKernel(
                    reopened,
                    clock_ms=clock,
                    owner_id="host:browser-test:fresh",
                )
                extension = HostWorldExtension(HostExtensionPort(reopened, kernel))
                restored = extension.load_prepared("task:browser-test")
                fresh_transport.prepared = restored
                recovered = extension.reconcile("task:browser-test", fresh_adapter)
                self.assertEqual(recovered.status, "succeeded")
                self.assertTrue(recovered.reconciled)
                assert recovered.observation is not None
                bundle = fresh_adapter.read_browser_bundle(recovered.observation)
                self.assertEqual(bundle.screenshot.body, _PNG)
                self.assertEqual(self.backend.posts, 1)
                final = reopened.read_task_event("task:browser-test")
                self.assertEqual(final.projection.state, created.state)
                self.assertEqual(
                    final.projection.ready_frontier,
                    created.ready_frontier,
                )


if __name__ == "__main__":
    unittest.main()
