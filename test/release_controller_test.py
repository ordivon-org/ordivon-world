from __future__ import annotations

import argparse
import importlib.util
import pathlib
import subprocess
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
    def test_deployment_specifications_are_bounded_and_normalized(self) -> None:
        parsed = release_controller.parse_deployment_specifications(
            ["old@99.5", "new@0.5"]
        )
        self.assertEqual(
            parsed,
            [
                {"version_id": "old", "percentage": 99.5},
                {"version_id": "new", "percentage": 0.5},
            ],
        )
        with self.assertRaises(release_controller.ReleaseError):
            release_controller.parse_deployment_specifications(["new@99"] )

    def test_nonzero_deployment_uses_cloudflare_api_without_wrangler(self) -> None:
        expected = [{"version_id": "candidate", "percentage": 100}]
        deployment = {"id": "deployment", "versions": expected}
        with (
            mock.patch.object(
                release_controller,
                "create_deployment_api",
                return_value=deployment,
            ) as create,
            mock.patch.object(release_controller.subprocess, "Popen") as popen,
        ):
            result = release_controller.deploy_versions(
                {},
                ["candidate@100"],
                "promote",
            )
        self.assertEqual(result, deployment)
        create.assert_called_once_with(expected, "promote", force=False)
        popen.assert_not_called()

    def test_deploy_timeout_is_reconciled_from_cloudflare_api(self) -> None:
        class Process:
            pid = 1234
            returncode = None

            def communicate(self, timeout=None):
                if timeout is not None:
                    raise subprocess.TimeoutExpired(
                        cmd=["wrangler"],
                        timeout=timeout,
                        output="SUCCESS deployed",
                    )
                self.returncode = -9
                return ("", None)

        expected = [
            {"version_id": "old", "percentage": 100},
            {"version_id": "new", "percentage": 0},
        ]
        deployment = {"id": "deployment", "versions": expected}
        with (
            mock.patch.object(release_controller.subprocess, "Popen", return_value=Process()),
            mock.patch.object(release_controller.os, "killpg") as killpg,
            mock.patch.object(
                release_controller,
                "wait_for_deployment",
                return_value=deployment,
            ) as reconcile,
        ):
            result = release_controller.deploy_versions(
                {},
                ["old@100", "new@0"],
                "smoke",
                command_timeout_seconds=1,
            )
        self.assertEqual(result, deployment)
        killpg.assert_called_once_with(1234, release_controller.signal.SIGKILL)
        reconcile.assert_called_once_with(expected)

    def test_expected_policy_matches_local_configuration(self) -> None:
        version, retention = release_controller.expected_policy()
        self.assertRegex(version, r"^p1\.6\.[a-f0-9]{16}$")
        self.assertGreater(retention["artifacts"], retention["idempotency"])

    def test_control_plane_json_query_retries_transient_failure(self) -> None:
        sleeps: list[float] = []
        completed = subprocess.CompletedProcess(
            args=["wrangler"],
            returncode=0,
            stdout='[{"id":"candidate"}]',
            stderr="",
        )
        with mock.patch.object(
            release_controller,
            "run",
            side_effect=[
                release_controller.ReleaseError("Cloudflare API timed out"),
                completed,
            ],
        ):
            value = release_controller.run_json(
                ["wrangler", "versions", "list"],
                {},
                attempts=2,
                sleep=sleeps.append,
            )
        self.assertEqual(value, [{"id": "candidate"}])
        self.assertEqual(sleeps, [2.0])

    def test_resumable_candidate_must_match_current_commit(self) -> None:
        versions = [
            {
                "id": "candidate",
                "annotations": {
                    "workers/tag": "git-abcdef123456-1234567890"
                },
            }
        ]
        candidate = release_controller.resumable_candidate(
            versions,
            "candidate",
            "abcdef1234567890abcdef1234567890abcdef12",
        )
        self.assertEqual(candidate["id"], "candidate")
        with self.assertRaises(release_controller.ReleaseError):
            release_controller.resumable_candidate(
                versions,
                "candidate",
                "0000000000000000000000000000000000000000",
                source_equivalent=lambda *_: False,
            )

    def test_resumable_candidate_accepts_equivalent_worker_inputs(self) -> None:
        versions = [
            {
                "id": "candidate",
                "annotations": {
                    "workers/tag": "git-abcdef123456-1234567890"
                },
            }
        ]
        comparisons: list[tuple[str, str]] = []

        def equivalent(candidate_ref: str, current_commit: str) -> bool:
            comparisons.append((candidate_ref, current_commit))
            return True

        candidate = release_controller.resumable_candidate(
            versions,
            "candidate",
            "0000000000000000000000000000000000000000",
            source_equivalent=equivalent,
        )
        self.assertEqual(candidate["id"], "candidate")
        self.assertEqual(
            comparisons,
            [("abcdef123456", "0" * 40)],
        )

    def test_release_can_resume_existing_candidate_without_upload(self) -> None:
        reports: list[tuple[str, dict[str, object]]] = []

        def capture_receipt(prefix: str, report: dict[str, object]) -> pathlib.Path:
            reports.append((prefix, dict(report)))
            return pathlib.Path("/tmp/release.json")

        commit = "a" * 40
        args = argparse.Namespace(
            message="resume candidate",
            candidate_version_id="candidate-version",
        )
        edge_config = release_controller.EdgeConfig(
            endpoint="https://edge.invalid",
            key_id="runtime-v1",
            secret=b"x" * 32,
        )
        version_payload = [
            {
                "id": "candidate-version",
                "annotations": {
                    "workers/tag": "git-aaaaaaaaaaaa-1234567890"
                },
            }
        ]
        old_deployment = [
            {
                "created_on": "2026-07-27T00:00:00Z",
                "versions": [
                    {"version_id": "old-version", "percentage": 100}
                ],
            }
        ]
        new_deployment = [
            {
                "created_on": "2026-07-27T01:00:00Z",
                "versions": [
                    {"version_id": "candidate-version", "percentage": 100}
                ],
            }
        ]
        health = {
            "policy_version": "p1.6.test",
            "worker_version": {"id": "candidate-version"},
        }

        with (
            mock.patch.object(release_controller, "cloudflare_environment", return_value={}),
            mock.patch.object(release_controller, "load_edge_config", return_value=edge_config),
            mock.patch.object(release_controller, "verify_release_source", return_value=commit),
            mock.patch.object(
                release_controller,
                "expected_policy",
                return_value=(
                    "p1.6.test",
                    {
                        "idempotency": 90,
                        "request_state": 90,
                        "receipt_mirror": 90,
                        "artifacts": 91,
                        "cleanup_tasks": 90,
                    },
                ),
            ),
            mock.patch.object(release_controller, "run"),
            mock.patch.object(release_controller, "versions", return_value=version_payload),
            mock.patch.object(
                release_controller,
                "deployments",
                side_effect=[old_deployment, new_deployment],
            ),
            mock.patch.object(release_controller, "deploy_versions") as deploy_versions,
            mock.patch.object(
                release_controller,
                "wait_for_version_propagation",
                return_value={"attempts": 1},
            ),
            mock.patch.object(release_controller, "smoke_version", return_value={}),
            mock.patch.object(
                release_controller,
                "signed_request",
                return_value=(200, {}, health),
            ),
            mock.patch.object(release_controller, "write_receipt", side_effect=capture_receipt),
            mock.patch.object(release_controller, "wrangler") as wrangler,
        ):
            result = release_controller.release(args)

        self.assertEqual(result, 0)
        self.assertEqual(deploy_versions.call_count, 2)
        wrangler.assert_not_called()
        self.assertEqual(reports[0][0], "release")
        self.assertTrue(reports[0][1]["candidate_reused"])
        self.assertEqual(
            reports[0][1]["candidate_version"],
            "candidate-version",
        )

    def test_deployments_are_sorted_by_created_time(self) -> None:
        payload = [
            {"id": "new", "created_on": "2026-07-27T02:00:00Z"},
            {"id": "old", "created_on": "2026-07-27T01:00:00Z"},
        ]
        with (
            mock.patch.object(
                release_controller,
                "load_cloudflare_credentials",
                return_value=release_controller.CloudflareCredentials(
                    api_token="test-token",
                    account_id="test-account",
                ),
            ),
            mock.patch.object(
                release_controller,
                "cloudflare_api",
                return_value={"deployments": payload},
            ),
        ):
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
