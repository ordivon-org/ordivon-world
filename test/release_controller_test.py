from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts" / "ordivon_edge_release.py"
SPEC = importlib.util.spec_from_file_location("ordivon_edge_release", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load release controller")
release_controller = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release_controller
SPEC.loader.exec_module(release_controller)


class ReleaseControllerTests(unittest.TestCase):
    def test_expected_policy_matches_local_configuration(self) -> None:
        version, retention = release_controller.expected_policy()
        self.assertRegex(version, r"^p1\.6\.[a-f0-9]{16}$")
        self.assertGreater(retention["artifacts"], retention["idempotency"])

    def test_deployments_are_sorted_by_created_time(self) -> None:
        payload = [
            {"id": "new", "created_on": "2026-07-27T02:00:00Z"},
            {"id": "old", "created_on": "2026-07-27T01:00:00Z"},
        ]
        with mock.patch.object(release_controller, "run_json", return_value=payload):
            result = release_controller.deployments({})
        self.assertEqual([item["id"] for item in result], ["old", "new"])

    def test_wait_for_version_propagation_requires_consecutive_matches(self) -> None:
        responses = [
            (200, {"CF-Ray": "old"}, {"worker_version": {"id": "old"}}),
            (200, {"CF-Ray": "one"}, {"worker_version": {"id": "candidate"}}),
            (200, {"CF-Ray": "two"}, {"worker_version": {"id": "candidate"}}),
            (200, {"CF-Ray": "three"}, {"worker_version": {"id": "candidate"}}),
        ]
        calls: list[dict[str, object]] = []

        def signed(*args: object, **kwargs: object):
            calls.append(dict(kwargs))
            return responses.pop(0)

        with mock.patch.object(release_controller, "signed_request", side_effect=signed):
            result = release_controller.wait_for_version_propagation(
                release_controller.EdgeConfig(
                    endpoint="https://edge.invalid",
                    key_id="runtime-v1",
                    secret=b"x" * 32,
                ),
                "candidate",
                use_override=True,
                consecutive_required=3,
                sleep=lambda _: None,
                monotonic=lambda: 0.0,
            )

        self.assertEqual(result["attempts"], 4)
        self.assertEqual(result["observations"][-1]["cf_ray"], "three")
        self.assertTrue(all(call["version_override"] == "candidate" for call in calls))

    def test_upload_failure_writes_failure_receipt(self) -> None:
        reports: list[tuple[str, dict[str, object]]] = []

        def capture_receipt(prefix: str, report: dict[str, object]) -> pathlib.Path:
            reports.append((prefix, dict(report)))
            return pathlib.Path("/tmp/release-failed.json")

        args = argparse.Namespace(message="test upload failure")
        edge_config = release_controller.EdgeConfig(
            endpoint="https://edge.invalid",
            key_id="runtime-v1",
            secret=b"x" * 32,
        )
        versions_payload = [
            {
                "id": "old-version",
                "number": 1,
                "metadata": {"created_on": "2026-07-27T00:00:00Z"},
            }
        ]
        deployment_payload = [
            {
                "id": "deployment-old",
                "created_on": "2026-07-27T00:00:00Z",
                "versions": [
                    {"version_id": "old-version", "percentage": 100}
                ],
            }
        ]

        with (
            mock.patch.object(release_controller, "cloudflare_environment", return_value={}),
            mock.patch.object(release_controller, "load_edge_config", return_value=edge_config),
            mock.patch.object(
                release_controller,
                "verify_release_source",
                return_value="a" * 40,
            ),
            mock.patch.object(release_controller, "run"),
            mock.patch.object(
                release_controller,
                "versions",
                return_value=versions_payload,
            ),
            mock.patch.object(
                release_controller,
                "deployments",
                return_value=deployment_payload,
            ),
            mock.patch.object(
                release_controller,
                "wrangler",
                side_effect=release_controller.ReleaseError("upload rejected"),
            ),
            mock.patch.object(
                release_controller,
                "write_receipt",
                side_effect=capture_receipt,
            ),
        ):
            with self.assertRaises(release_controller.ReleaseError) as raised:
                release_controller.release(args)

        self.assertIn("/tmp/release-failed.json", str(raised.exception))
        self.assertEqual(len(reports), 1)
        prefix, report = reports[0]
        self.assertEqual(prefix, "release-failed")
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["failed_stage"], "upload_pending")
        self.assertEqual(report["previous_version"], "old-version")
        self.assertIsNone(report["candidate_version"])
        self.assertNotIn("restored_previous_version", report)


if __name__ == "__main__":
    unittest.main()
