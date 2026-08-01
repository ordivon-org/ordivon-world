from __future__ import annotations
import importlib.util, pathlib, sys, unittest

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wxp1", ROOT / "experiment.py")
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


class CallbackContinuityTests(unittest.TestCase):
    def test_all_faults_reconcile_without_false_or_duplicate_completion(self) -> None:
        for scenario in M.SCENARIOS:
            for arm in ("poll", "callback-plus-poll"):
                result = M.run(scenario, arm)
                self.assertEqual(result.task_completions, 1)
                self.assertEqual(result.false_completions, 0)
                self.assertEqual(result.unsafe_redispatch_attempts, 0)
                self.assertEqual(result.operator_interventions, 0)

    def test_callback_improves_healthy_discovery_only(self) -> None:
        scenario = next(item for item in M.SCENARIOS if item.name == "normal")
        polling = M.run(scenario, "poll")
        callback = M.run(scenario, "callback-plus-poll")
        self.assertLess(callback.completion_latency_ms, polling.completion_latency_ms)

    def test_lost_and_stale_callbacks_fall_back_to_inspection(self) -> None:
        for name in ("lost", "stale-generation", "before-registration"):
            scenario = next(item for item in M.SCENARIOS if item.name == name)
            result = M.run(scenario, "callback-plus-poll")
            self.assertGreaterEqual(result.discovered_ms, scenario.provider_complete_ms)
            self.assertGreater(result.provider_inspections, 0)


if __name__ == "__main__":
    unittest.main()
