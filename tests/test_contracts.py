from __future__ import annotations

import unittest

from ordivon_world import ContractError, load_schema, validate_contract


def execution(capability: str) -> dict[str, object]:
    return {
        "policy_version": "p1.6.test",
        "capability_version": capability,
        "worker_version_id": "worker-test",
        "worker_version_tag": "git-111111111111-src-2222222222222222-1",
        "worker_version_timestamp": "2026-08-04T00:00:00Z",
        "lease_generation": 1,
    }


def artifact(key: str, media_type: str) -> dict[str, object]:
    return {
        "key": key,
        "sha256": "a" * 64,
        "bytes": 12,
        "media_type": media_type,
    }


class ContractTests(unittest.TestCase):
    def test_all_published_contracts_are_valid_draft_2020_12(self) -> None:
        names = (
            "browser-manifest",
            "browser-request",
            "edge-capabilities",
            "edge-receipt",
            "fetch-request",
            "network-observation",
            "world-observation",
            "world-prepared-dispatch",
        )
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(
                    load_schema(name)["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )

    def test_fetch_contract_rejects_unowned_options(self) -> None:
        with self.assertRaises(ContractError):
            validate_contract(
                "fetch-request",
                {
                    "url": "https://example.com/",
                    "maximum_bytes": 1024,
                    "timeout_ms": 1000,
                    "accept": "*/*",
                    "authorization": "forbidden",
                },
            )

    def test_succeeded_fetch_requires_fetch_evidence(self) -> None:
        body = artifact("fetch/v2/request_fetch_test/g1/body", "text/plain")
        value = {
            "schema_version": 1,
            "receipt_id": "request_fetch_test",
            "request_digest": "b" * 64,
            "operation": "fetch",
            "status": "succeeded",
            "started_at": "2026-08-04T00:00:00Z",
            "completed_at": "2026-08-04T00:00:01Z",
            "duration_ms": 1000,
            "execution": execution("fetch.v2"),
            "artifact": body,
            "artifacts": [body],
        }
        with self.assertRaises(ContractError):
            validate_contract("edge-receipt", value)

    def test_failed_receipt_forbids_artifact_evidence(self) -> None:
        body = artifact("fetch/v2/request_failed_test/g1/body", "text/plain")
        value = {
            "schema_version": 1,
            "receipt_id": "request_failed_test",
            "request_digest": "c" * 64,
            "operation": "fetch",
            "status": "failed",
            "started_at": "2026-08-04T00:00:00Z",
            "completed_at": "2026-08-04T00:00:01Z",
            "duration_ms": 1000,
            "execution": execution("fetch.v2"),
            "error_code": "timeout",
            "artifact": body,
            "artifacts": [body],
        }
        with self.assertRaises(ContractError):
            validate_contract("edge-receipt", value)

    def test_succeeded_browser_requires_three_artifacts(self) -> None:
        screenshot = artifact(
            "browser/v2/request_browser_test/g1/screenshot.png",
            "image/png",
        )
        value = {
            "schema_version": 1,
            "receipt_id": "request_browser_test",
            "request_digest": "d" * 64,
            "operation": "browser.run",
            "status": "succeeded",
            "started_at": "2026-08-04T00:00:00Z",
            "completed_at": "2026-08-04T00:00:01Z",
            "duration_ms": 1000,
            "execution": execution("browser.snapshot.v2"),
            "artifact": screenshot,
            "artifacts": [screenshot],
            "browser": {
                "requested_url": "https://example.com/",
                "final_url_observed": False,
                "page_title": "Example",
                "page_status": 200,
                "browser_ms": 10,
                "viewport": {"width": 1280, "height": 720},
                "full_page": False,
            },
        }
        with self.assertRaises(ContractError):
            validate_contract("edge-receipt", value)


if __name__ == "__main__":
    unittest.main()
