from __future__ import annotations

from pathlib import Path
import unittest

from ordivon_world.doctor import (
    CommandResult,
    contract_check,
    expected_lifecycle_rules,
    network_check,
    overall_status,
    repository_check,
    systemd_properties,
)


class DoctorTests(unittest.TestCase):
    def test_contract_check_covers_all_published_schemas(self) -> None:
        result = contract_check()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["count"], 8)
        self.assertEqual(result["draft"], "2020-12")

    def test_overall_status_surfaces_attention(self) -> None:
        self.assertEqual(
            overall_status(
                [
                    {"name": "a", "status": "ok"},
                    {"name": "b", "status": "attention"},
                ]
            ),
            "attention",
        )

    def test_repository_check_reports_dirty_paths(self) -> None:
        responses = iter(
            [
                CommandResult(0, "a" * 40 + "\n", ""),
                CommandResult(0, " M README.md\n", ""),
                CommandResult(0, "main\n", ""),
            ]
        )

        def runner(command: list[str]) -> CommandResult:
            self.assertEqual(command[0], "git")
            return next(responses)

        result = repository_check(Path("/repo"), runner)
        self.assertEqual(result["status"], "attention")
        self.assertEqual(result["head"], "a" * 40)
        self.assertEqual(result["dirtyPaths"], [" M README.md"])

    def test_systemd_properties_are_parsed_without_inventing_state(self) -> None:
        def runner(command: list[str]) -> CommandResult:
            self.assertEqual(command[:2], ["systemctl", "show"])
            return CommandResult(
                0,
                "LoadState=loaded\nActiveState=inactive\nResult=success\nExecMainStatus=0\n",
                "",
            )

        value = systemd_properties("ordivon-edge-gc.service", runner)
        self.assertEqual(value["Result"], "success")
        self.assertEqual(value["ActiveState"], "inactive")

    def test_network_check_preserves_structured_report_on_nonzero_exit(self) -> None:
        def runner(command: list[str]) -> CommandResult:
            self.assertEqual(command[-1], "doctor")
            return CommandResult(
                1,
                '{"config_valid":false,"key_pair_consistent":true,"missing_commands":[]}\n',
                "profile needs attention\n",
            )

        result = network_check(Path("/repo"), runner)
        self.assertEqual(result["status"], "attention")
        self.assertEqual(result["exitCode"], 1)
        self.assertFalse(result["report"]["config_valid"])
        self.assertEqual(result["stderr"], "profile needs attention")

    def test_expected_lifecycle_rules_match_retention_contract(self) -> None:
        rules = expected_lifecycle_rules(
            {
                "request_state": 90,
                "receipt_mirror": 90,
                "artifacts": 91,
                "cleanup_tasks": 90,
            }
        )
        self.assertEqual(len(rules), 5)
        self.assertEqual(rules[0]["id"], "edge-v2-request-state-90d")
        self.assertEqual(
            rules[2]["deleteObjectsTransition"]["condition"]["maxAge"],
            91 * 86_400,
        )


if __name__ == "__main__":
    unittest.main()
