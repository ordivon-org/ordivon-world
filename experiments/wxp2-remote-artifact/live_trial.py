#!/usr/bin/env python3
"""Run the live WXP-2 direct-host vs Cloudflare Workflow-to-R2 comparison."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import sys
import time
import urllib.request
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
WORLD_ROOT = HERE.parents[1]
CLIENT_PATH = WORLD_ROOT / "providers/cloudflare/scripts/ordivon_edge_client.py"
EXPERIMENT_PATH = HERE / "experiment.py"


def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


client = load("ordivon_edge_client_wxp2", CLIENT_PATH)
experiment = load("wxp2_experiment", EXPERIMENT_PATH)


def seal_evidence(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("evidence_sha256", None)
    value["evidence_sha256"] = hashlib.sha256(
        (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    return value


def parse_json(status: int, body: bytes, context: str) -> dict[str, Any]:
    try:
        value = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{context} returned non-JSON data") from exc
    if not isinstance(value, dict) or not 200 <= status < 300:
        raise RuntimeError(f"{context} failed: HTTP {status}: {value}")
    return value


def direct_source(url: str, accept: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"Accept": accept, "User-Agent": "ordivon-world-wxp2/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def run(config_path: pathlib.Path, url: str, timeout: float, interval: float) -> dict[str, Any]:
    config = client.load_config(config_path)
    accept = "text/plain, text/markdown;q=0.9, */*;q=0.1"
    source_started = time.monotonic()
    source = direct_source(url, accept)
    source_elapsed_ms = round((time.monotonic() - source_started) * 1000)
    source_sha256 = hashlib.sha256(source).hexdigest()

    manifest = {
        "schema_version": 1,
        "consumer": "ordivon-world-wxp2",
        "workload": "remote-to-remote-artifact",
        "steps": [
            {
                "id": "source",
                "operation": "fetch",
                "input": {
                    "url": url,
                    "maximum_bytes": max(len(source) + 4096, 65536),
                    "timeout_ms": 15000,
                    "accept": accept,
                },
            }
        ],
    }
    body = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    request_id = client.make_request_id()
    started = time.monotonic()
    status, _, raw = client.request(
        config,
        "POST",
        "/v1/evidence-runs",
        body=body,
        request_id=request_id,
    )
    submission = parse_json(status, raw, "evidence submission")
    host_response_bytes = len(raw)
    ref = submission.get("foreign_operation_ref")
    instance_id = ref.get("instance_id") if isinstance(ref, dict) else None
    if not isinstance(instance_id, str):
        raise RuntimeError("evidence submission returned no Workflow instance ID")

    deadline = time.monotonic() + timeout
    status_observations = 0
    final: dict[str, Any] | None = None
    while time.monotonic() < deadline:
        code, _, status_raw = client.request(config, "GET", f"/v1/evidence-runs/{instance_id}")
        host_response_bytes += len(status_raw)
        status_observations += 1
        value = parse_json(code, status_raw, "evidence status")
        provider = value.get("provider_status")
        provider_state = provider.get("status") if isinstance(provider, dict) else None
        if provider_state in {"complete", "errored", "terminated"}:
            final = value
            break
        time.sleep(interval)
    if final is None:
        raise RuntimeError("evidence run did not reach a terminal state")
    provider = final.get("provider_status")
    if not isinstance(provider, dict) or provider.get("status") != "complete":
        raise RuntimeError(f"evidence run did not complete: {provider}")
    output = provider.get("output")
    if not isinstance(output, dict):
        raise RuntimeError("completed Workflow returned no output")
    artifacts = output.get("artifacts")
    if not isinstance(artifacts, list):
        raise RuntimeError("Workflow output returned no Artifact references")
    source_artifact = next(
        (
            item
            for item in artifacts
            if isinstance(item, dict) and str(item.get("key", "")).startswith("fetch/v2/")
        ),
        None,
    )
    if not isinstance(source_artifact, dict):
        raise RuntimeError("Workflow output returned no source Artifact")
    result_manifest = output.get("result_manifest")
    if not isinstance(result_manifest, dict):
        raise RuntimeError("Workflow output returned no result manifest")

    comparison = experiment.compare(
        source_bytes=len(source),
        source_sha256=source_sha256,
        provider_artifact_sha256=str(source_artifact.get("sha256", "")),
        submission_bytes=len(body),
        provider_response_bytes=len(raw),
        status_response_bytes=host_response_bytes - len(raw),
        result_manifest_bytes=int(result_manifest.get("bytes", 0)),
    )
    comparison["live"] = {
        "url": url,
        "request_id": request_id,
        "workflow_instance_id": instance_id,
        "status_observations": status_observations,
        "workflow_elapsed_ms": round((time.monotonic() - started) * 1000),
        "direct_source_elapsed_ms": source_elapsed_ms,
        "source_artifact": source_artifact,
        "result_manifest": result_manifest,
        "provider_status": provider.get("status"),
        "operator_interventions": 0,
    }
    return seal_evidence(comparison)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--config", type=pathlib.Path, default=pathlib.Path("/root/.config/ordivon/secrets/edge-client.json"))
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    value = run(args.config, args.url, args.timeout, args.interval)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0 if value.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
