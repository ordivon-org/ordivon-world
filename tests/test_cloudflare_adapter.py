from __future__ import annotations

import json
import unittest

from ordivon_world import (
    CapabilitySnapshot,
    CloudflareWorldAdapter,
    PreparedWorldDispatch,
    TraceContext,
    TransportError,
    WorldBindingStale,
    WorldOutcomeUnknown,
    WorldProviderError,
)
from ordivon_world.canonical import sha256_hex
from ordivon_world.cloudflare import HttpResponse


def capability_document(*, policy: str = "p1.6.test") -> dict[str, object]:
    return {
        "schema_version": 1,
        "service": "ordivon-edge",
        "policy_version": policy,
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
                "reason": "private artifacts",
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
            "id": "worker-version-test",
            "tag": "git-111111111111-src-2222222222222222-1",
            "timestamp": "2026-08-04T00:00:00Z",
        },
        "deployment_identity": {
            "source_commit": "111111111111",
            "worker_release_digest": "2222222222222222",
        },
    }


def receipt(prepared: PreparedWorldDispatch, body: bytes = b"world-result") -> dict[str, object]:
    digest = sha256_hex(body)
    artifact = {
        "key": f"fetch/v2/{prepared.provider_request_id}/g1/body",
        "sha256": digest,
        "bytes": len(body),
        "media_type": "text/plain",
        "etag": '"etag"',
    }
    return {
        "schema_version": 1,
        "receipt_id": prepared.provider_request_id,
        "request_digest": prepared.provider_request_digest,
        "operation": prepared.operation,
        "status": "succeeded",
        "started_at": "2026-08-04T00:00:00Z",
        "completed_at": "2026-08-04T00:00:01Z",
        "duration_ms": 1000,
        "execution": {
            "policy_version": "p1.6.test",
            "capability_version": prepared.capability_version,
            "worker_version_id": "worker-version-test",
            "worker_version_tag": "git-111111111111-src-2222222222222222-1",
            "worker_version_timestamp": "2026-08-04T00:00:00Z",
            "lease_generation": 1,
        },
        "artifact": artifact,
        "artifacts": [artifact],
        "fetch": {
            "requested_url": prepared.request["url"],
            "final_url": prepared.request["url"],
            "http_status": 200,
            "redirect_count": 0,
        },
    }


class FakeCloudflareTransport:
    def __init__(self) -> None:
        self.capabilities_document = capability_document()
        self.receipts: dict[str, dict[str, object]] = {}
        self.artifacts: dict[str, bytes] = {}
        self.posts = 0
        self.drop_after_commit = False
        self.post_headers: dict[str, str] | None = None
        self.receipt_request_digest_override: str | None = None

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
            return HttpResponse(200, {}, json.dumps(self.capabilities_document).encode())
        if method == "POST" and path == "/v1/fetch":
            self.posts += 1
            self.post_headers = dict(extra_headers or {})
            prepared = PreparedWorldDispatch.from_dict(self.prepared_value)
            value = receipt(prepared)
            if self.receipt_request_digest_override is not None:
                value["request_digest"] = self.receipt_request_digest_override
            self.receipts[request_id] = value
            artifact = value["artifact"]
            assert isinstance(artifact, dict)
            self.artifacts[str(artifact["key"])] = b"world-result"
            if self.drop_after_commit:
                self.drop_after_commit = False
                raise TransportError("response dropped after provider commit")
            return HttpResponse(
                200,
                {},
                json.dumps({"receipt": value, "replayed": self.posts > 1}).encode(),
            )
        if method == "GET" and path.startswith("/v1/receipts/"):
            key = path.rsplit("/", 1)[-1]
            value = self.receipts.get(key)
            if value is None:
                return HttpResponse(404, {}, b'{"error":"receipt_not_found"}')
            return HttpResponse(200, {}, json.dumps(value).encode())
        if method == "GET" and path.startswith("/v1/artifacts/"):
            key = path.removeprefix("/v1/artifacts/")
            value = self.artifacts.get(key)
            if value is None:
                return HttpResponse(404, {}, b"")
            return HttpResponse(
                200,
                {"x-ordivon-sha256": sha256_hex(value)},
                value,
            )
        raise AssertionError((method, path, request_id, extra_headers, body))

    prepared_value: dict[str, object]


class CloudflareWorldAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.transport = FakeCloudflareTransport()
        self.adapter = CloudflareWorldAdapter(self.transport)
        self.capability = CapabilitySnapshot.from_document(
            capability_document(),
            "2026-08-04T00:00:00Z",
        )

    def prepare(self) -> PreparedWorldDispatch:
        prepared = self.adapter.prepare_fetch(
            dispatch_id="dispatch:world:test:fetch:r1",
            effect_id="effect:world:test:fetch:r1",
            url="https://developers.cloudflare.com/",
            capability=self.capability,
            trace_context=TraceContext(
                "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"
            ),
        )
        self.transport.prepared_value = prepared.to_dict()
        return prepared

    def test_prepare_is_deterministic_and_round_trips(self) -> None:
        first = self.prepare()
        second = self.adapter.prepare_fetch(
            dispatch_id=first.dispatch.dispatch_id,
            effect_id=first.dispatch.effect_id,
            url="https://developers.cloudflare.com/",
            capability=self.capability,
            trace_context=first.trace_context,
        )
        self.assertEqual(first.provider_request_id, second.provider_request_id)
        self.assertEqual(first.provider_request_digest, second.provider_request_digest)
        self.assertEqual(PreparedWorldDispatch.from_dict(first.to_dict()), first)
        self.assertEqual(first.dispatch.idempotency_key, first.provider_request_id)
        self.assertEqual(
            first.dispatch.required_state_refs[0].digest,
            self.capability.condition_digest,
        )

    def test_deliver_maps_receipt_and_artifact_to_host_observation(self) -> None:
        prepared = self.prepare()
        observed = self.adapter.deliver(prepared)
        self.assertEqual(observed.envelope.dispatch_id, prepared.dispatch.dispatch_id)
        self.assertEqual(observed.envelope.status, "succeeded")
        self.assertFalse(observed.reconciled)
        self.assertEqual(len(observed.envelope.evidence_refs), 1)
        body = self.adapter.read_artifact(observed.envelope.evidence_refs[0])
        self.assertEqual(body, b"world-result")
        assert self.transport.post_headers is not None
        self.assertEqual(
            self.transport.post_headers["traceparent"],
            prepared.trace_context.traceparent if prepared.trace_context else None,
        )
        self.assertEqual(
            self.transport.post_headers["x-ordivon-dispatch-id"],
            prepared.dispatch.dispatch_id,
        )

    def test_browser_preparation_uses_browser_capability_and_contract(self) -> None:
        prepared = self.adapter.prepare_browser(
            dispatch_id="dispatch:world:test:browser:r1",
            effect_id="effect:world:test:browser:r1",
            url="https://developers.cloudflare.com/",
            capability=self.capability,
        )
        self.assertEqual(prepared.operation, "browser.run")
        self.assertEqual(prepared.path, "/v1/browser/run")
        self.assertEqual(prepared.capability_version, "browser.snapshot.v2")
        self.assertEqual(prepared.request["wait_until"], "domcontentloaded")
        self.assertEqual(
            PreparedWorldDispatch.from_dict(prepared.to_dict()),
            prepared,
        )

    def test_receipt_request_identity_drift_fails_closed(self) -> None:
        prepared = self.prepare()
        self.transport.receipt_request_digest_override = "f" * 64
        with self.assertRaises(WorldProviderError):
            self.adapter.deliver(prepared)
        self.assertEqual(self.transport.posts, 1)

    def test_response_loss_is_reconciled_by_fresh_adapter_without_redispatch(self) -> None:
        prepared = self.prepare()
        durable = prepared.to_dict()
        self.transport.drop_after_commit = True
        with self.assertRaises(WorldOutcomeUnknown):
            self.adapter.deliver(prepared)
        self.assertEqual(self.transport.posts, 1)

        fresh = CloudflareWorldAdapter(self.transport)
        restored = PreparedWorldDispatch.from_dict(durable)
        result = fresh.reconcile(restored)
        self.assertTrue(result.found)
        self.assertFalse(result.pending)
        self.assertIsNotNone(result.observation)
        assert result.observation is not None
        self.assertTrue(result.observation.reconciled)
        self.assertEqual(self.transport.posts, 1)

    def test_condition_drift_fails_before_external_dispatch(self) -> None:
        prepared = self.prepare()
        self.transport.capabilities_document = capability_document(policy="p1.7.changed")
        with self.assertRaises(WorldBindingStale):
            self.adapter.deliver(prepared)
        self.assertEqual(self.transport.posts, 0)

    def test_reconcile_missing_does_not_dispatch(self) -> None:
        prepared = self.prepare()
        result = self.adapter.reconcile(prepared)
        self.assertFalse(result.found)
        self.assertIsNone(result.observation)
        self.assertEqual(self.transport.posts, 0)


if __name__ == "__main__":
    unittest.main()
