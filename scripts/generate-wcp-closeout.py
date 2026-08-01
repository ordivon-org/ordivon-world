#!/usr/bin/env python3
"""Generate and validate the WCP-0 through WXP-2 closeout summary."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence/wcp0-wxp2-closeout.json"
SOURCES = {
    "capability_portfolio": ROOT / "evidence/capability-portfolio-v0.json",
    "wcp1_research": ROOT / "evidence/wcp1/computer-research-source-post-wcp2-20260802.json",
    "wcp1_acceptance": ROOT / "evidence/wcp1/provider-acceptance-post-wcp2-20260802.json",
    "wcp2_live": ROOT / "evidence/wcp2/durable-evidence-run-live-20260802.json",
    "release_workflow_smoke": ROOT / "evidence/wcp2/release-workflow-smoke-20260802.json",
    "wxp1": ROOT / "experiments/wxp1-callback-continuity/evidence.json",
    "wxp2_deterministic": ROOT / "experiments/wxp2-remote-artifact/evidence.json",
    "wxp2_live": ROOT / "experiments/wxp2-remote-artifact/evidence-live.json",
}


class CloseoutError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def content_digest(value: dict[str, Any]) -> str:
    unsigned = dict(value)
    unsigned.pop("evidence_sha256", None)
    return hashlib.sha256(canonical(unsigned)).hexdigest()


def load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CloseoutError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CloseoutError(f"evidence is not an object: {path}")
    claimed = value.get("evidence_sha256")
    if isinstance(claimed, str) and claimed != content_digest(value):
        raise CloseoutError(f"evidence digest mismatch: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CloseoutError(message)


def build() -> dict[str, Any]:
    source = {name: load_json(path) for name, path in SOURCES.items()}
    portfolio = source["capability_portfolio"]
    research = source["wcp1_research"]
    acceptance = source["wcp1_acceptance"]
    wcp2 = source["wcp2_live"]
    release_smoke = source["release_workflow_smoke"]
    wxp1 = source["wxp1"]
    wxp2_deterministic = source["wxp2_deterministic"]
    wxp2_live = source["wxp2_live"]

    adapters = portfolio.get("adapters")
    require(portfolio.get("writable_registry") is False, "capability portfolio became writable")
    require(isinstance(adapters, list) and len(adapters) == 2, "unexpected adapter portfolio")

    worker_id = wcp2.get("deployment", {}).get("worker_version_id")
    require(isinstance(worker_id, str) and worker_id, "WCP-2 Worker version is missing")
    for name, evidence in (("research", research), ("acceptance", acceptance)):
        require(
            evidence.get("capability_ref", {}).get("worker_version", {}).get("id") == worker_id,
            f"WCP-1 {name} evidence is not bound to the WCP-2 Worker",
        )
        artifacts = evidence.get("artifact_verification")
        require(
            isinstance(artifacts, list) and artifacts and all(item.get("verified") is True for item in artifacts),
            f"WCP-1 {name} Artifact verification failed",
        )

    wcp2_measurements = wcp2.get("measurements", {})
    require(wcp2.get("fresh_process_reconciliation", {}).get("provider_status") == "complete", "WCP-2 did not complete")
    require(wcp2_measurements.get("unsafe_redispatch_attempts") == 0, "WCP-2 used unsafe redispatch")
    require(wcp2_measurements.get("duplicate_workflow_instances") == 0, "WCP-2 duplicated a Workflow")
    require(wcp2_measurements.get("false_completions") == 0, "WCP-2 falsely completed")
    require(wcp2_measurements.get("world_database_records") == 0, "WCP-2 introduced World database state")
    require(
        wcp2_measurements.get("verified_artifact_count") == wcp2_measurements.get("artifact_count"),
        "WCP-2 did not verify every Artifact",
    )

    require(release_smoke.get("worker_version_id") == worker_id, "release smoke used another Worker")
    require(release_smoke.get("smoke", {}).get("provider_status") == "complete", "release Workflow smoke failed")
    require(
        release_smoke.get("measurements", {}).get("workflow_created_during_closeout") is False,
        "closeout unexpectedly recreated the Workflow resource",
    )

    wxp1_poll = wxp1.get("summary", {}).get("poll", {})
    wxp1_callback = wxp1.get("summary", {}).get("callback-plus-poll", {})
    for arm_name, arm in (("poll", wxp1_poll), ("callback-plus-poll", wxp1_callback)):
        require(arm.get("false_completions") == 0, f"WXP-1 {arm_name} falsely completed")
        require(arm.get("duplicate_task_completions") == 0, f"WXP-1 {arm_name} duplicated completion")
        require(arm.get("unsafe_redispatch_attempts") == 0, f"WXP-1 {arm_name} used unsafe redispatch")
    require(
        wxp1_callback.get("mean_completion_latency_ms", float("inf"))
        < wxp1_poll.get("mean_completion_latency_ms", float("inf")),
        "WXP-1 callback arm did not reduce healthy discovery latency",
    )
    require(wxp1.get("decision", {}).get("disposition") == "localize", "WXP-1 disposition drifted")

    for name, evidence in (("deterministic", wxp2_deterministic), ("live", wxp2_live)):
        require(evidence.get("valid") is True, f"WXP-2 {name} trial is invalid")
        require(evidence.get("integrity", {}).get("digest_verified") is True, f"WXP-2 {name} digest failed")
        require(
            evidence.get("arms", {}).get("provider-to-r2", {}).get("copies_through_host") == 0,
            f"WXP-2 {name} copied source bytes through Host",
        )

    evidence_sources = {
        name: {
            "path": path.relative_to(ROOT).as_posix(),
            "evidence_sha256": value.get("evidence_sha256") or hashlib.sha256(canonical(value)).hexdigest(),
        }
        for (name, path), value in zip(SOURCES.items(), source.values(), strict=True)
    }
    result: dict[str, Any] = {
        "schema_version": 1,
        "kind": "ordivon-world-wcp0-wxp2-closeout",
        "status": "completed-through-wxp2",
        "production": {
            "worker_version_id": worker_id,
            "policy_version": wcp2.get("fresh_process_reconciliation", {})
            .get("workflow_output", {})
            .get("steps", [{}])[0]
            .get("execution", {})
            .get("policy_version"),
            "workflow_resource_id": wcp2.get("deployment", {}).get("workflow_resource_id"),
            "workflow_version_id": wcp2.get("deployment", {}).get("workflow_version_id"),
        },
        "results": {
            "wcp0": {
                "adapter_count": len(adapters),
                "writable_registry": False,
                "disposition": "retain adapter-local declarations and deterministic read-only projection",
            },
            "wcp1": {
                "consumer_count": 2,
                "research": {
                    "request_id": research.get("foreign_operation_ref", {}).get("request_id"),
                    "elapsed_ms": research.get("measurements", {}).get("elapsed_ms"),
                    "artifact_bytes": research.get("measurements", {}).get("artifact_bytes"),
                },
                "provider_acceptance": {
                    "request_id": acceptance.get("foreign_operation_ref", {}).get("request_id"),
                    "elapsed_ms": acceptance.get("measurements", {}).get("elapsed_ms"),
                    "artifact_bytes": acceptance.get("measurements", {}).get("artifact_bytes"),
                },
            },
            "wcp2": {
                "workflow_instance_id": wcp2.get("same_request_recovery", {})
                .get("foreign_operation_ref", {})
                .get("instance_id"),
                "measurements": wcp2_measurements,
                "release_smoke_instance_id": release_smoke.get("smoke", {}).get("instance_id"),
                "disposition": "retain provider-native Workflow and R2 manifests; repair release bootstrap",
            },
            "wxp1": {
                "poll": wxp1_poll,
                "callback_plus_poll": wxp1_callback,
                "disposition": "localize callback wake-up, generation, deduplication, and inspect fallback",
            },
            "wxp2": {
                "deterministic": wxp2_deterministic.get("measurements"),
                "live": wxp2_live.get("measurements"),
                "disposition": "retain provider-to-R2 movement and Artifact references; reject transfer service",
            },
        },
        "architecture_decision": {
            "decision_id": "W-A1",
            "disposition": "keep-adapters-localize-facets-no-shared-world-layer",
            "retain": [
                "adapter-local capability declarations",
                "Cloudflare provider-native Workflow handle and lifecycle",
                "private R2 input, result, failure, and source Artifacts",
                "Host generation and adapter-local callback deduplication",
                "provider inspect/poll as external truth reconciliation",
                "Host-independent Artifact and Task Verification",
            ],
            "delete_or_reject": [
                "writable World capability registry",
                "World service or database",
                "World Workflow engine",
                "World callback journal or completion authority",
                "World Artifact transfer service",
                "universal WorldInteraction schema or provider status enum",
                "automatic provider switching, routing, or broker authority",
                "WXP-1 B2 shared callback record",
            ],
            "reason": "WCP-2 and the callback and Artifact workloads remained recoverable through provider-native handles, adapter-local state, and Host Verification. No reproduced failure required a new cross-owner authority.",
        },
        "deferred": {
            "wcp3": "not started; select a second external capability only from a named real workload and capability gain",
            "next_architecture_review": "conditional on a materially different workload reproducing one unowned non-bypassable responsibility",
        },
        "evidence_sources": evidence_sources,
    }
    result["evidence_sha256"] = content_digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        expected = json.dumps(build(), indent=2, ensure_ascii=False) + "\n"
        if args.check:
            actual = OUTPUT.read_text(encoding="utf-8")
            if actual != expected:
                raise CloseoutError(f"generated output is stale: {OUTPUT}")
        else:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(expected, encoding="utf-8")
    except (CloseoutError, OSError) as exc:
        print(f"WCP closeout: {exc}", file=sys.stderr)
        return 1
    print("ordivon-world WCP-0 through WXP-2 closeout: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
