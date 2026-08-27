from __future__ import annotations

from pathlib import Path
import unittest

from ordivon_world.doctor import (
    CommandResult,
    contract_check,
    lifecycle_check,
    overall_status,
    repository_check,
    systemd_properties,
)


class DoctorTests(unittest.TestCase):
    def test_contract_check_covers_all_published_schemas(self) -> None:
        result = contract_check()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["count"], 25)
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

    def test_lifecycle_check_preserves_provider_projection_on_nonzero_exit(self) -> None:
        def runner(command: list[str]) -> CommandResult:
            self.assertEqual(command[-1], "--check")
            return CommandResult(
                1,
                '{"ok":false,"bucket":"ordivon-artifacts","expected":[],"actual":[]}\n',
                "policy drift\n",
            )

        result = lifecycle_check(runner)
        self.assertEqual(result["status"], "attention")
        self.assertEqual(result["exitCode"], 1)
        self.assertFalse(result["report"]["ok"])
        self.assertEqual(result["stderr"], "policy drift")


if __name__ == "__main__":
    unittest.main()
