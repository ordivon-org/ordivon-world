from __future__ import annotations

import itertools
import json
from pathlib import Path
import tempfile
import unittest

from ordivon_world_w1 import (
    HashChainJournal,
    JournalCorruption,
    ProviderArtifact,
    ProviderPendingReceipt,
    ProviderReceipt,
    TrialArm,
    TrialConfig,
    dispatch_phase,
    provider_request_digest,
    resume_phase,
)
from ordivon_world_w1.models import ProviderExecution
from ordivon_world_w1.provider import provider_body_digest


PROBE = {
    "schema_version": 1,
    "probe_kind": "reachability",
    "collection_id": "reachability-test",
    "sample_index": 1,
    "target": "w1-example",
    "url": "https://example.com/",
    "network": "test-network",
    "route": "test-route",
    "protocol": "http_tls",
    "started_at": "2026-07-31T00:00:00Z",
    "dns_ms": 1.0,
    "connect_ms": 2.0,
    "tls_ms": 3.0,
    "ttfb_ms": 4.0,
    "total_ms": 5.0,
    "requested_duration_ms": None,
    "bytes_downloaded": 0,
    "speed_download_bps": 0.0,
    "connection_count": 1,
    "http_version": "1.1",
    "http_status": 200,
    "remote_ip": "203.0.113.10",
    "success": True,
    "failure_class": None,
    "termination": "completed",
    "tool_exit_code": 0,
    "error": None,
}


class FakeProvider:
    def __init__(self, *, pending_queries: int = 0, corrupt_artifact: bool = False) -> None:
        self.pending_queries = pending_queries
        self.corrupt_artifact = corrupt_artifact
        self.fetch_calls = 0
        self.receipt_calls = 0
        self.artifact_calls = 0
        self.receipts: dict[str, ProviderReceipt] = {}
        self.body = b"<html><head><title>Example Domain</title></head><body>Example Domain</body></html>"

    def fetch(self, request_id: str, payload: dict[str, object]):
        self.fetch_calls += 1
        body = self.body
        import hashlib

        artifact = ProviderArtifact(
            key=f"fetch/v2/{request_id}/g1/body",
            sha256=hashlib.sha256(body).hexdigest(),
            bytes=len(body),
            media_type="text/html; charset=utf-8",
            etag="fixture-etag",
        )
        receipt = ProviderReceipt(
            receipt_id=request_id,
            request_digest=provider_request_digest(payload),
            status="succeeded",
            started_at="2026-07-31T00:00:00Z",
            completed_at="2026-07-31T00:00:01Z",
            duration_ms=1000,
            execution=ProviderExecution(
                policy_version="p1.6.fixture",
                capability_version="fetch.v2",
                worker_version_id="worker-fixture",
                worker_version_tag="fixture",
                worker_version_timestamp="2026-07-31T00:00:00Z",
                lease_generation=1,
            ),
            artifact=artifact,
            fetch={
                "requested_url": "https://example.com/",
                "final_url": "https://example.com/",
                "http_status": 200,
                "redirect_count": 0,
            },
        )
        self.receipts[request_id] = receipt
        return receipt, False

    def receipt(self, request_id: str):
        self.receipt_calls += 1
        receipt = self.receipts[request_id]
        if self.receipt_calls <= self.pending_queries:
            return ProviderPendingReceipt(
                receipt_id=request_id,
                request_digest=receipt.request_digest,
                started_at=receipt.started_at,
                lease_expires_at="2026-07-31T00:01:00Z",
                execution=receipt.execution,
            )
        return receipt

    def artifact(self, artifact: ProviderArtifact) -> bytes:
        self.artifact_calls += 1
        return b"corrupt" if self.corrupt_artifact else self.body


class W1ExperimentTests(unittest.TestCase):
    def test_provider_digest_matches_live_idempotency_contract(self) -> None:
        payload = {
            "url": "https://example.com/",
            "maximum_bytes": 65_536,
            "timeout_ms": 10_000,
            "accept": "text/html",
        }
        self.assertEqual(
            provider_body_digest(payload),
            "a5801589a5168494958520f0dcbd05634eed7b4d7a06d261e93390b41bfea410",
        )
        self.assertEqual(
            provider_request_digest(payload),
            "8e6cebfe3a2abe4290e3e6b7517292612b8e2705d6db7533286bd19f53f1b9c4",
        )

    def test_b0_and_b1_recover_original_request_without_redispatch(self) -> None:
        for arm in (TrialArm.DIRECT, TrialArm.CORRELATION):
            with self.subTest(arm=arm.value), tempfile.TemporaryDirectory() as directory:
                provider = FakeProvider()
                config = TrialConfig(arm, f"trial-{arm.value}", Path(directory))
                dispatch = dispatch_phase(config, provider=provider, probe_source=PROBE)
                self.assertEqual(dispatch["taskState"], "waiting")
                self.assertEqual(provider.fetch_calls, 1)

                report = resume_phase(config, provider=provider, reconcile_delay_seconds=0)
                self.assertEqual(report["phase"], "completed")
                self.assertEqual(report["finalTaskState"], "completed")
                self.assertTrue(report["exactlyOnceCompletion"])
                self.assertEqual(report["providerPostAttempts"], 1)
                self.assertEqual(report["providerExecutions"], 1)
                self.assertEqual(report["duplicateExternalEffects"], 0)
                self.assertEqual(report["unsafeRedispatchAttempts"], 0)
                self.assertEqual(provider.fetch_calls, 1)
                self.assertEqual(provider.receipt_calls, 1)
                self.assertEqual(provider.artifact_calls, 1)
                self.assertEqual(config.correlation_path.exists(), arm is TrialArm.CORRELATION)
                if arm is TrialArm.CORRELATION:
                    journal = HashChainJournal(
                        config.correlation_path,
                        clock_ms=itertools.count(10_000).__next__,
                        label="test",
                    )
                    self.assertGreaterEqual(len(journal.events()), 5)
                    raw = config.correlation_path.read_text()
                    self.assertNotIn("remote_ip", raw)
                    self.assertNotIn("203.0.113.10", raw)

    def test_pending_receipt_is_polled_without_another_post(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = FakeProvider(pending_queries=2)
            config = TrialConfig(TrialArm.DIRECT, "trial-pending", Path(directory))
            dispatch_phase(config, provider=provider, probe_source=PROBE)
            report = resume_phase(
                config,
                provider=provider,
                reconcile_attempts=5,
                reconcile_delay_seconds=0,
            )
            self.assertEqual(report["phase"], "completed")
            self.assertEqual(report["providerPostAttempts"], 1)
            self.assertEqual(report["receiptQueries"], 3)
            self.assertEqual(provider.fetch_calls, 1)
            self.assertEqual(provider.receipt_calls, 3)

    def test_artifact_mismatch_blocks_false_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = FakeProvider(corrupt_artifact=True)
            config = TrialConfig(TrialArm.CORRELATION, "trial-corrupt", Path(directory))
            dispatch_phase(config, provider=provider, probe_source=PROBE)
            report = resume_phase(config, provider=provider, reconcile_delay_seconds=0)
            self.assertEqual(report["phase"], "blocked")
            self.assertEqual(report["finalTaskState"], "blocked")
            self.assertFalse(report["exactlyOnceCompletion"])
            self.assertEqual(report["providerExecutions"], 1)
            self.assertEqual(report["duplicateExternalEffects"], 0)
            events = config.trial_journal_path.read_text()
            self.assertIn('"artifactDigestAccepted":false', events)

    def test_correlation_chain_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "correlation.jsonl"
            journal = HashChainJournal(
                path,
                clock_ms=itertools.count(1_000).__next__,
                label="tamper",
            )
            journal.append("one", {"value": 1})
            journal.append("two", {"value": 2})
            path.write_text(path.read_text().replace('"value":1', '"value":9', 1))
            with self.assertRaisesRegex(JournalCorruption, "digest"):
                HashChainJournal(
                    path,
                    clock_ms=itertools.count(2_000).__next__,
                    label="tamper",
                )

    def test_event_identity_cannot_be_rebound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            journal = HashChainJournal(
                Path(directory) / "events.jsonl",
                clock_ms=itertools.count(1).__next__,
                label="identity",
            )
            first = journal.append("event", {"value": 1}, event_id="event:fixed")
            replay = journal.append("event", {"value": 1}, event_id="event:fixed")
            self.assertEqual(first, replay)
            with self.assertRaisesRegex(JournalCorruption, "different content"):
                journal.append("event", {"value": 2}, event_id="event:fixed")


if __name__ == "__main__":
    unittest.main()
