#!/usr/bin/env python3
"""Produce verified evidence for real Ordivon World consumers."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys, time, urllib.parse
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ordivon_edge_client import ClientError, Config, load_config, make_request_id, request  # noqa: E402


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def json_call(config, method: str, path: str, *, payload=None, request_id=None):
    body = b"" if payload is None else json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    status, headers, raw = request(config, method, path, body=body, request_id=request_id)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ClientError(f"{path} returned non-JSON data") from exc
    if not isinstance(value, dict) or not 200 <= status < 300:
        raise ClientError(f"{path} returned HTTP {status}: {value}")
    return value, headers


def artifact_path(key: str) -> str:
    return "/v1/artifacts/" + "/".join(urllib.parse.quote(part, safe="") for part in key.split("/"))


def verify_artifacts(config, receipt: dict[str, Any]) -> list[dict[str, Any]]:
    items = receipt.get("artifacts")
    if not isinstance(items, list) or not items:
        items = [receipt.get("artifact")]
    verified = []
    for item in items:
        if not isinstance(item, dict):
            raise ClientError("Receipt contains an invalid Artifact reference")
        key, expected = item.get("key"), item.get("sha256")
        if not isinstance(key, str) or not isinstance(expected, str):
            raise ClientError("Artifact key or digest is invalid")
        status, headers, body = request(config, "GET", artifact_path(key), accept="application/octet-stream")
        normalized = {name.lower(): value for name, value in headers.items()}
        observed = hashlib.sha256(body).hexdigest()
        if status != 200 or observed != expected or normalized.get("x-ordivon-sha256") != expected:
            raise ClientError(f"Artifact verification failed for {key}")
        if isinstance(item.get("bytes"), int) and item["bytes"] != len(body):
            raise ClientError(f"Artifact byte count failed for {key}")
        verified.append({"key": key, "sha256": observed, "bytes": len(body), "media_type": item.get("media_type"), "verified": True})
    return verified


def operation(config, path: str, payload: dict[str, Any]):
    request_id = make_request_id()
    envelope, _ = json_call(config, "POST", path, payload=payload, request_id=request_id)
    receipt = envelope.get("receipt")
    if not isinstance(receipt, dict) or receipt.get("status") != "succeeded":
        raise ClientError(f"operation failed: {receipt}")
    return request_id, receipt, verify_artifacts(config, receipt)


def capability_ref(document: dict[str, Any]) -> dict[str, Any]:
    return {"sha256": hashlib.sha256(canonical(document)).hexdigest(), "policy_version": document.get("policy_version"), "worker_version": document.get("worker_version"), "deployment_identity": document.get("deployment_identity"), "document": document}


def seal(value: dict[str, Any]) -> dict[str, Any]:
    value["evidence_sha256"] = hashlib.sha256(canonical(value)).hexdigest()
    return value


def capture_source(config, consumer: str, url: str, browser: bool) -> dict[str, Any]:
    started = time.time()
    capabilities, _ = json_call(config, "GET", "/v1/capabilities")
    if browser:
        path, operation_id = "/v1/browser/run", "browser.run"
        payload = {"url": url, "viewport_width": 1365, "viewport_height": 768, "full_page": True, "wait_until": "domcontentloaded", "timeout_ms": 15000, "wait_after_ms": 0}
    else:
        path, operation_id = "/v1/fetch", "fetch"
        payload = {"url": url, "maximum_bytes": 524288, "timeout_ms": 15000, "accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.1"}
    request_id, receipt, artifacts = operation(config, path, payload)
    return seal({"schema_version": 1, "kind": "ordivon-world-consumer-evidence", "consumer": consumer, "workload": "research-source-capture", "source": {"url": url, "operation": operation_id}, "foreign_operation_ref": {"provider": "cloudflare", "request_id": request_id, "request_digest": receipt.get("request_digest")}, "capability_ref": capability_ref(capabilities), "receipt": receipt, "artifact_verification": artifacts, "measurements": {"elapsed_ms": round((time.time() - started) * 1000), "artifact_count": len(artifacts), "artifact_bytes": sum(item["bytes"] for item in artifacts), "operator_interventions": 0, "unsafe_redispatch_attempts": 0}})


def accept_provider(config, consumer: str) -> dict[str, Any]:
    started = time.time()
    health, _ = json_call(config, "GET", "/health")
    capabilities, _ = json_call(config, "GET", "/v1/capabilities")
    if health.get("worker_version") != capabilities.get("worker_version") or health.get("policy_version") != capabilities.get("policy_version"):
        raise ClientError("health and capabilities do not describe the same deployment")
    request_id, receipt, artifacts = operation(config, "/v1/fetch", {"url": "https://example.com/", "maximum_bytes": 65536, "timeout_ms": 10000, "accept": "text/html"})
    return seal({"schema_version": 1, "kind": "ordivon-world-consumer-evidence", "consumer": consumer, "workload": "provider-post-deployment-acceptance", "health": health, "capability_ref": capability_ref(capabilities), "foreign_operation_ref": {"provider": "cloudflare", "request_id": request_id, "request_digest": receipt.get("request_digest")}, "receipt": receipt, "artifact_verification": artifacts, "measurements": {"elapsed_ms": round((time.time() - started) * 1000), "artifact_count": len(artifacts), "artifact_bytes": sum(item["bytes"] for item in artifacts), "operator_interventions": 0, "unsafe_redispatch_attempts": 0}})


def write(path: pathlib.Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(prog="ordivon-world-evidence")
    parser.add_argument("--config", default="/root/.config/ordivon/secrets/edge-client.json")
    sub = parser.add_subparsers(dest="command", required=True)
    capture = sub.add_parser("capture-source")
    capture.add_argument("url")
    capture.add_argument("--consumer", default="ordivon-computer")
    capture.add_argument("--browser", action="store_true")
    capture.add_argument("--output", required=True)
    acceptance = sub.add_parser("accept-provider")
    acceptance.add_argument("--consumer", default="ordivon-world-release")
    acceptance.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        config = load_config(pathlib.Path(args.config).expanduser())
        value = capture_source(config, args.consumer, args.url, args.browser) if args.command == "capture-source" else accept_provider(config, args.consumer)
        write(pathlib.Path(args.output).expanduser(), value)
        print(json.dumps({"ok": True, "output": args.output, "workload": value["workload"], "evidence_sha256": value["evidence_sha256"]}, indent=2))
        return 0
    except ClientError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
