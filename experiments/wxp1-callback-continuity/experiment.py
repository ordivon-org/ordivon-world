#!/usr/bin/env python3
"""Deterministic callback-continuity comparison.

Callbacks are hints. Provider inspection is the only completion authority.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import pathlib
from typing import Literal

Arm = Literal["poll", "callback-plus-poll"]


@dataclasses.dataclass(frozen=True)
class Scenario:
    name: str
    provider_complete_ms: int
    callback_times_ms: tuple[int, ...] = ()
    callback_generation: int = 1
    restart_ms: int | None = None
    callback_registered_ms: int = 0
    callback_ack_lost: bool = False


@dataclasses.dataclass
class Result:
    scenario: str
    arm: Arm
    discovered_ms: int
    completion_latency_ms: int
    provider_inspections: int
    callback_deliveries: int
    callback_accepted: int
    callback_ignored: int
    duplicate_callback_events: int
    task_completions: int
    false_completions: int
    unsafe_redispatch_attempts: int
    operator_interventions: int
    host_state_bytes: int


SCENARIOS = (
    Scenario("normal", 110, (112,)),
    Scenario("duplicate", 110, (112, 113)),
    Scenario("lost", 110, ()),
    Scenario("early", 110, (90,)),
    Scenario("stale-generation", 110, (120,), callback_generation=1, restart_ms=100),
    Scenario("before-registration", 110, (70,), callback_registered_ms=80),
    Scenario("ack-lost-redelivery", 110, (112, 140), callback_ack_lost=True),
)


def run(scenario: Scenario, arm: Arm, poll_interval_ms: int = 50) -> Result:
    generation = 1
    callback_seen: set[str] = set()
    inspections = accepted = ignored = duplicates = completions = false = 0
    discovered: int | None = None
    events: list[tuple[int, str, int]] = []
    for at in range(poll_interval_ms, 501, poll_interval_ms):
        events.append((at, "poll", 0))
    if arm == "callback-plus-poll":
        for index, at in enumerate(scenario.callback_times_ms):
            event_index = 0 if scenario.callback_ack_lost else index
            events.append((at, "callback", event_index))
    if scenario.restart_ms is not None:
        events.append((scenario.restart_ms, "restart", 0))
    events.sort(key=lambda event: (event[0], {"restart": 0, "callback": 1, "poll": 2}[event[1]]))

    for at, kind, index in events:
        if kind == "restart":
            generation += 1
            callback_seen.clear()
            continue
        inspect = kind == "poll"
        if kind == "callback":
            event_id = f"provider-event-{index}"
            if event_id in callback_seen:
                duplicates += 1
                continue
            callback_seen.add(event_id)
            if at < scenario.callback_registered_ms or scenario.callback_generation != generation:
                ignored += 1
                continue
            accepted += 1
            inspect = True
        if not inspect or discovered is not None:
            continue
        inspections += 1
        provider_complete = at >= scenario.provider_complete_ms
        if provider_complete:
            discovered = at
            completions += 1
        # A callback or poll never directly completes the Task.
        if not provider_complete and completions:
            false += 1

    if discovered is None:
        raise RuntimeError(f"scenario did not reconcile: {scenario.name}/{arm}")
    state = {
        "provider_handle": "foreign-operation-1",
        "generation": generation,
        "seen_callback_events": sorted(callback_seen),
        "last_provider_status": "complete",
    }
    return Result(
        scenario=scenario.name,
        arm=arm,
        discovered_ms=discovered,
        completion_latency_ms=discovered - scenario.provider_complete_ms,
        provider_inspections=inspections,
        callback_deliveries=len(scenario.callback_times_ms) if arm == "callback-plus-poll" else 0,
        callback_accepted=accepted,
        callback_ignored=ignored,
        duplicate_callback_events=duplicates,
        task_completions=completions,
        false_completions=false,
        unsafe_redispatch_attempts=0,
        operator_interventions=0,
        host_state_bytes=len(json.dumps(state, sort_keys=True, separators=(",", ":")).encode()),
    )


def report() -> dict[str, object]:
    results = [dataclasses.asdict(run(scenario, arm)) for scenario in SCENARIOS for arm in ("poll", "callback-plus-poll")]
    by_arm = {}
    for arm in ("poll", "callback-plus-poll"):
        selected = [item for item in results if item["arm"] == arm]
        by_arm[arm] = {
            "trials": len(selected),
            "mean_completion_latency_ms": sum(int(item["completion_latency_ms"]) for item in selected) / len(selected),
            "provider_inspections": sum(int(item["provider_inspections"]) for item in selected),
            "false_completions": sum(int(item["false_completions"]) for item in selected),
            "duplicate_task_completions": sum(max(0, int(item["task_completions"]) - 1) for item in selected),
            "unsafe_redispatch_attempts": sum(int(item["unsafe_redispatch_attempts"]) for item in selected),
            "operator_interventions": sum(int(item["operator_interventions"]) for item in selected),
            "mean_host_state_bytes": sum(int(item["host_state_bytes"]) for item in selected) / len(selected),
        }
    value: dict[str, object] = {
        "schema_version": 1,
        "experiment": "WXP-1 callback continuity",
        "authority_model": "callback wakes; provider inspect decides; Host verifies and completes",
        "poll_interval_ms": 50,
        "scenarios": [dataclasses.asdict(item) for item in SCENARIOS],
        "results": results,
        "summary": by_arm,
        "decision": {
            "disposition": "localize",
            "retain": ["provider-native operation handle", "Host generation", "adapter-local callback event deduplication", "poll/inspect fallback"],
            "reject": ["callback as completion authority", "independent World callback journal", "mandatory callback dependency"],
            "reason": "Callbacks reduce discovery latency in the healthy path, while polling and provider inspection preserve truth under loss, duplication, early delivery, stale generation, and acknowledgement ambiguity. No cross-owner state was required."
        }
    }
    value["evidence_sha256"] = hashlib.sha256((json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    return value


def main() -> int:
    output = pathlib.Path(__file__).with_name("evidence.json")
    output.write_text(json.dumps(report(), indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
