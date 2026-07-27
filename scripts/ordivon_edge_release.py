#!/usr/bin/env python3
"""Versioned release and rollback controller for Ordivon Edge."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any, NoReturn

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKER_NAME = "ordivon-edge"
CLOUDFLARE_CONFIG = pathlib.Path("/root/.config/ordivon/secrets/cloudflare.json")
EDGE_CONFIG = pathlib.Path("/root/.config/ordivon/secrets/edge-client.json")
POLICY_CONFIG = ROOT / "config" / "edge-policy.json"
WRANGLER_CONFIG = ROOT / "wrangler.jsonc"
RELEASE_DIR = pathlib.Path("/root/backups/ordivon-edge/releases")


class ReleaseError(RuntimeError):
    pass


@dataclass(frozen=True)
class EdgeConfig:
    endpoint: str
    key_id: str
    secret: bytes


def fail(message: str) -> NoReturn:
    raise ReleaseError(message)


def load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseError(f"Cannot read configuration: {path}") from exc
    if not isinstance(value, dict):
        fail(f"Configuration must be a JSON object: {path}")
    return value


def cloudflare_environment() -> dict[str, str]:
    config = load_json(CLOUDFLARE_CONFIG)
    token = config.get("api_token")
    account_id = config.get("account_id")
    if not isinstance(token, str) or not token:
        fail("Cloudflare API token is missing")
    if not isinstance(account_id, str) or not account_id:
        fail("Cloudflare account ID is missing")
    environment = os.environ.copy()
    environment.update(
        {
            "CLOUDFLARE_API_TOKEN": token,
            "CLOUDFLARE_ACCOUNT_ID": account_id,
            "CI": "true",
        }
    )
    return environment


def expected_policy() -> tuple[str, dict[str, int]]:
    policy = load_json(POLICY_CONFIG)
    wrangler = load_json(WRANGLER_CONFIG)
    allowed_hosts = wrangler.get("vars", {}).get("FETCH_ALLOWED_HOSTS")
    if not isinstance(allowed_hosts, str) or not allowed_hosts:
        fail("FETCH_ALLOWED_HOSTS is missing from Wrangler configuration")
    normalized_hosts = sorted(
        host.strip().lower().rstrip(".")
        for host in allowed_hosts.split(",")
        if host.strip()
    )
    payload = json.dumps(
        {
            "policy": policy,
            "effective_fetch_allowed_hosts": normalized_hosts,
        },
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    family = policy.get("family")
    retention = policy.get("retention_days")
    if not isinstance(family, str) or not isinstance(retention, dict):
        fail("Edge policy configuration is invalid")
    version = f"{family}.{hashlib.sha256(payload).hexdigest()[:16]}"
    return version, retention


def load_edge_config() -> EdgeConfig:
    config = load_json(EDGE_CONFIG)
    endpoint = config.get("endpoint")
    key_id = config.get("key_id")
    secret_text = config.get("secret")
    if not all(isinstance(value, str) and value for value in (endpoint, key_id, secret_text)):
        fail("Edge client configuration is incomplete")
    try:
        secret = base64.urlsafe_b64decode(secret_text + "=" * (-len(secret_text) % 4))
    except ValueError as exc:
        raise ReleaseError("Edge HMAC secret is invalid") from exc
    if len(secret) < 32:
        fail("Edge HMAC secret is too short")
    return EdgeConfig(endpoint=endpoint.rstrip("/"), key_id=key_id, secret=secret)


def run(
    arguments: list[str],
    *,
    environment: dict[str, str] | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        arguments,
        cwd=ROOT,
        env=environment,
        text=True,
        check=False,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if completed.returncode != 0:
        detail = ""
        if capture:
            detail = (completed.stderr or completed.stdout or "").strip()
        raise ReleaseError(
            f"Command failed ({completed.returncode}): {' '.join(arguments)}"
            + (f"\n{detail}" if detail else "")
        )
    return completed


def run_json(arguments: list[str], environment: dict[str, str]) -> Any:
    completed = run(arguments, environment=environment, capture=True)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ReleaseError(
            f"Command returned invalid JSON: {' '.join(arguments)}"
        ) from exc


def git_output(*arguments: str) -> str:
    return run(["git", *arguments], capture=True).stdout.strip()


def verify_release_source() -> str:
    if git_output("status", "--porcelain"):
        fail("Repository is dirty; release requires a clean main branch")
    branch = git_output("branch", "--show-current")
    if branch != "main":
        fail(f"Release requires main branch, found {branch or 'detached HEAD'}")
    run(["git", "fetch", "origin", "--prune"])
    head = git_output("rev-parse", "HEAD")
    remote = git_output("rev-parse", "origin/main")
    if head != remote:
        fail("Local main does not match origin/main")
    return head


def wrangler(environment: dict[str, str], *arguments: str, capture: bool = False):
    return run(
        ["pnpm", "exec", "wrangler", *arguments],
        environment=environment,
        capture=capture,
    )


def versions(environment: dict[str, str]) -> list[dict[str, Any]]:
    value = run_json(
        [
            "pnpm",
            "exec",
            "wrangler",
            "versions",
            "list",
            "--name",
            WORKER_NAME,
            "--json",
        ],
        environment,
    )
    if not isinstance(value, list):
        fail("Wrangler versions list returned an unexpected shape")
    return sorted(
        value,
        key=lambda item: (
            item.get("number") if isinstance(item.get("number"), int) else -1,
            item.get("metadata", {}).get("created_on", "")
            if isinstance(item.get("metadata"), dict)
            else "",
        ),
    )


def deployments(environment: dict[str, str]) -> list[dict[str, Any]]:
    value = run_json(
        [
            "pnpm",
            "exec",
            "wrangler",
            "deployments",
            "list",
            "--name",
            WORKER_NAME,
            "--json",
        ],
        environment,
    )
    if not isinstance(value, list) or not value:
        fail("No active Worker deployment was found")
    return sorted(
        value,
        key=lambda item: item.get("created_on", "")
        if isinstance(item.get("created_on"), str)
        else "",
    )


def active_version(deployment_list: list[dict[str, Any]]) -> str:
    candidates = [
        version
        for version in deployment_list[-1].get("versions", [])
        if version.get("percentage") == 100
    ]
    if len(candidates) != 1 or not isinstance(candidates[0].get("version_id"), str):
        fail("Latest deployment does not have exactly one 100% active version")
    return candidates[0]["version_id"]


def deploy_versions(
    environment: dict[str, str],
    specifications: list[str],
    message: str,
) -> None:
    wrangler(
        environment,
        "versions",
        "deploy",
        *specifications,
        "--name",
        WORKER_NAME,
        "--message",
        message,
        "--yes",
    )


def canonical_target(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))


def signed_request(
    config: EdgeConfig,
    method: str,
    path: str,
    *,
    body: bytes = b"",
    request_id: str | None = None,
    version_override: str | None = None,
    timeout: float = 75.0,
) -> tuple[int, dict[str, str], Any]:
    request_id = request_id or f"req_release_{uuid.uuid4().hex}"
    url = f"{config.endpoint}{path}"
    timestamp = int(time.time())
    body_sha256 = hashlib.sha256(body).hexdigest()
    canonical = "\n".join(
        [
            "ordivon-edge-v1",
            method.upper(),
            canonical_target(url),
            request_id,
            str(timestamp),
            body_sha256,
        ]
    )
    signature = base64.urlsafe_b64encode(
        hmac.new(config.secret, canonical.encode("utf-8"), hashlib.sha256).digest()
    ).rstrip(b"=").decode("ascii")
    headers = {
        "Authorization": f"Ordivon-HMAC {config.key_id}:{signature}",
        "X-Ordivon-Request-Id": request_id,
        "X-Ordivon-Timestamp": str(timestamp),
        "Accept": "application/json",
        "User-Agent": "ordivon-edge-release/0.1",
    }
    if body:
        headers["Content-Type"] = "application/json"
    if version_override is not None:
        headers["Cloudflare-Workers-Version-Overrides"] = (
            f'{WORKER_NAME}="{version_override}"'
        )
    invocation = urllib.request.Request(
        url,
        data=body if method.upper() not in {"GET", "HEAD"} else None,
        method=method.upper(),
        headers=headers,
    )
    try:
        with urllib.request.urlopen(invocation, timeout=timeout) as response:
            status = response.status
            response_headers = dict(response.headers.items())
            raw = response.read()
    except urllib.error.HTTPError as exc:
        status = exc.code
        response_headers = dict(exc.headers.items())
        raw = exc.read()
    except urllib.error.URLError as exc:
        raise ReleaseError(f"Smoke request failed: {exc.reason}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReleaseError("Smoke request returned non-JSON data") from exc
    return status, response_headers, value


def observed_version(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    metadata = value.get("worker_version")
    if isinstance(metadata, dict) and isinstance(metadata.get("id"), str):
        return metadata["id"]
    receipt = value.get("receipt")
    execution = receipt.get("execution") if isinstance(receipt, dict) else None
    actual = execution.get("worker_version_id") if isinstance(execution, dict) else None
    return actual if isinstance(actual, str) else None


def assert_version(value: Any, version_id: str, context: str) -> None:
    if not isinstance(value, dict):
        fail(f"{context} did not return a JSON object")
    actual = observed_version(value)
    if actual != version_id:
        fail(f"{context} reached Worker version {actual!r}, expected {version_id}")


def assert_policy(value: Any, policy_version: str, context: str) -> None:
    if not isinstance(value, dict):
        fail(f"{context} did not return a JSON object")
    actual = value.get("policy_version")
    if actual != policy_version:
        fail(f"{context} reported policy {actual!r}, expected {policy_version}")


def wait_for_version_propagation(
    config: EdgeConfig,
    version_id: str,
    *,
    use_override: bool,
    timeout_seconds: float = 120.0,
    interval_seconds: float = 3.0,
    consecutive_required: int = 5,
    sleep: Any = time.sleep,
    monotonic: Any = time.monotonic,
) -> dict[str, Any]:
    if timeout_seconds <= 0 or interval_seconds <= 0 or consecutive_required < 1:
        fail("Version propagation parameters are invalid")
    deadline = monotonic() + timeout_seconds
    consecutive = 0
    observations: list[dict[str, Any]] = []
    while True:
        status, headers, health = signed_request(
            config,
            "GET",
            "/health",
            version_override=version_id if use_override else None,
        )
        actual = observed_version(health)
        normalized = {key.lower(): value for key, value in headers.items()}
        observations.append(
            {
                "status": status,
                "worker_version_id": actual,
                "cf_ray": normalized.get("cf-ray"),
            }
        )
        if status == 200 and actual == version_id:
            consecutive += 1
        else:
            consecutive = 0
        if consecutive >= consecutive_required:
            return {
                "target_version": version_id,
                "use_override": use_override,
                "consecutive_required": consecutive_required,
                "attempts": len(observations),
                "observations": observations[-20:],
            }
        if monotonic() >= deadline:
            fail(
                "Worker version propagation did not stabilize: "
                f"target={version_id}, last={actual}, attempts={len(observations)}"
            )
        sleep(interval_seconds)

def smoke_operation(
    config: EdgeConfig,
    version_id: str,
    path: str,
    body: bytes,
    request_prefix: str,
    *,
    timeout: float = 75.0,
) -> tuple[str, dict[str, Any]]:
    last_status = 0
    last_value: Any = None
    for attempt in range(1, 4):
        request_id = f"{request_prefix}_{uuid.uuid4().hex}"
        status, headers, value = signed_request(
            config,
            "POST",
            path,
            body=body,
            request_id=request_id,
            version_override=version_id,
            timeout=timeout,
        )
        last_status = status
        last_value = value
        if status != 429:
            if not isinstance(value, dict):
                fail(f"Smoke operation {path} returned a non-object response")
            return request_id, value
        if attempt < 3:
            normalized = {key.lower(): val for key, val in headers.items()}
            try:
                retry_after = int(normalized.get("retry-after", "10"))
            except ValueError:
                retry_after = 10
            time.sleep(min(max(retry_after, 1), 30))
    fail(f"Smoke operation {path} remained rate limited: HTTP {last_status}: {last_value}")


def smoke_version(
    config: EdgeConfig,
    version_id: str,
    policy_version: str,
    retention: dict[str, int],
) -> dict[str, Any]:
    status, _, health = signed_request(
        config,
        "GET",
        "/health",
        version_override=version_id,
    )
    if status != 200:
        fail(f"Version-specific health smoke returned HTTP {status}: {health}")
    assert_version(health, version_id, "health smoke")
    assert_policy(health, policy_version, "health smoke")

    status, _, capabilities = signed_request(
        config,
        "GET",
        "/v1/capabilities",
        version_override=version_id,
    )
    if status != 200:
        fail(f"Version-specific capability smoke returned HTTP {status}: {capabilities}")
    assert_version(capabilities, version_id, "capability smoke")
    assert_policy(capabilities, policy_version, "capability smoke")
    expected_retention = {
        "idempotency_days": retention["idempotency"],
        "request_state_days": retention["request_state"],
        "receipt_mirror_days": retention["receipt_mirror"],
        "artifact_days": retention["artifacts"],
        "cleanup_task_days": retention["cleanup_tasks"],
    }
    if capabilities.get("retention") != expected_retention:
        fail(
            "Capability retention does not match the release policy: "
            f"{capabilities.get('retention')!r}"
        )

    fetch_body = json.dumps(
        {
            "url": "https://example.com/",
            "maximum_bytes": 65536,
            "timeout_ms": 10000,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    fetch_id, fetch_result = smoke_operation(
        config,
        version_id,
        "/v1/fetch",
        fetch_body,
        "req_release_fetch",
    )
    fetch_status = fetch_result.get("receipt", {}).get("status")
    if fetch_status != "succeeded":
        fail(f"Version-specific fetch smoke failed: {fetch_result}")
    assert_version(fetch_result, version_id, "fetch smoke")
    fetch_receipt = fetch_result["receipt"]

    browser_body = json.dumps(
        {
            "url": "https://example.com/",
            "viewport_width": 1024,
            "viewport_height": 768,
            "full_page": False,
            "wait_until": "domcontentloaded",
            "timeout_ms": 15000,
            "wait_after_ms": 0,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    browser_id, browser_result = smoke_operation(
        config,
        version_id,
        "/v1/browser/run",
        browser_body,
        "req_release_browser",
        timeout=90.0,
    )
    browser_status = browser_result.get("receipt", {}).get("status")
    if browser_status != "succeeded":
        fail(f"Version-specific Browser smoke failed: {browser_result}")
    assert_version(browser_result, version_id, "Browser smoke")
    browser_receipt = browser_result["receipt"]

    return {
        "health": health,
        "capabilities": capabilities,
        "fetch_request_id": fetch_id,
        "fetch_receipt": fetch_receipt,
        "browser_request_id": browser_id,
        "browser_receipt": browser_receipt,
    }

def write_receipt(prefix: str, report: dict[str, Any]) -> pathlib.Path:
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    path = RELEASE_DIR / f"{prefix}-{stamp}.json"
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)
    os.chmod(path, 0o600)
    return path


def release(args: argparse.Namespace) -> int:
    environment = cloudflare_environment()
    edge = load_edge_config()
    commit = verify_release_source()
    message = args.message or f"Ordivon Edge {commit[:12]}"
    policy_version, retention = expected_policy()
    report: dict[str, Any] = {
        "status": "preflight",
        "started_at": dt.datetime.now(dt.UTC).isoformat(),
        "git_commit": commit,
        "message": message,
        "expected_policy_version": policy_version,
        "expected_retention": retention,
    }
    previous_version: str | None = None
    new_version: str | None = None
    zero_deployed = False

    try:
        run(["pnpm", "install", "--frozen-lockfile", "--offline"])
        run(["pnpm", "run", "ci"])
        report["status"] = "ci_passed"

        before_versions = {item.get("id") for item in versions(environment)}
        previous_deployments = deployments(environment)
        previous_version = active_version(previous_deployments)
        tag = f"git-{commit[:12]}-{int(time.time())}"
        report.update(
            {
                "tag": tag,
                "previous_version": previous_version,
                "status": "upload_pending",
            }
        )
        wrangler(
            environment,
            "versions",
            "upload",
            "--name",
            WORKER_NAME,
            "--tag",
            tag,
            "--message",
            message,
            "--keep-vars",
            "--strict",
        )
        after = versions(environment)
        new_versions = [
            item
            for item in after
            if item.get("id") not in before_versions
            and isinstance(item.get("id"), str)
        ]
        if len(new_versions) != 1:
            fail(f"Expected one newly uploaded version, found {len(new_versions)}")
        new_version = new_versions[0]["id"]
        report.update(
            {
                "candidate_version": new_version,
                "status": "smoke_pending",
            }
        )

        deploy_versions(
            environment,
            [f"{previous_version}@100", f"{new_version}@0"],
            f"P1.5 smoke candidate {commit[:12]}",
        )
        zero_deployed = True
        report["candidate_propagation"] = wait_for_version_propagation(
            edge,
            new_version,
            use_override=True
        )
        report["smoke"] = smoke_version(
            edge,
            new_version,
            policy_version,
            retention,
        )
        report["status"] = "smoke_passed"
        deploy_versions(
            environment,
            [f"{new_version}@100"],
            f"Promote verified Ordivon Edge {commit[:12]}",
        )
        report["promotion_propagation"] = wait_for_version_propagation(
            edge,
            new_version,
            use_override=False
        )
        status, _, health = signed_request(edge, "GET", "/health")
        if status != 200:
            fail(f"Post-promotion health returned HTTP {status}: {health}")
        assert_version(health, new_version, "post-promotion health")
        assert_policy(health, policy_version, "post-promotion health")
        report.update(
            {
                "status": "promoted",
                "completed_at": dt.datetime.now(dt.UTC).isoformat(),
                "post_promotion_health": health,
                "deployment": deployments(environment)[-1],
            }
        )
        receipt_path = write_receipt("release", report)
        print(
            json.dumps(
                {
                    "ok": True,
                    "status": report["status"],
                    "git_commit": commit,
                    "previous_version": previous_version,
                    "version_id": new_version,
                    "receipt": str(receipt_path),
                },
                indent=2,
            )
        )
        return 0
    except Exception as error:
        report.update(
            {
                "status": "failed",
                "failed_at": dt.datetime.now(dt.UTC).isoformat(),
                "failed_stage": report.get("status", "unknown"),
                "error": str(error),
                "candidate_version": new_version,
                "previous_version": previous_version,
            }
        )
        if zero_deployed and previous_version is not None:
            try:
                deploy_versions(
                    environment,
                    [f"{previous_version}@100"],
                    f"Restore previous version after failed release {commit[:12]}",
                )
                report["restored_previous_version"] = True
            except Exception as restore_error:
                report["restored_previous_version"] = False
                report["restore_error"] = str(restore_error)
        receipt_path = write_receipt("release-failed", report)
        raise ReleaseError(
            f"Release failed; receipt: {receipt_path}\n{error}"
        ) from error

def rollback(args: argparse.Namespace) -> int:
    environment = cloudflare_environment()
    edge = load_edge_config()
    deployment_list = deployments(environment)
    current = active_version(deployment_list)
    target = args.version_id
    if target is None:
        for deployment in reversed(deployment_list[:-1]):
            try:
                candidate = active_version([deployment])
            except ReleaseError:
                continue
            if candidate != current:
                target = candidate
                break
    if target is None:
        fail("No previous 100% deployment was found; provide --version-id")

    message = args.message or f"Rollback Ordivon Edge from {current} to {target}"
    wrangler(
        environment,
        "rollback",
        target,
        "--name",
        WORKER_NAME,
        "--message",
        message,
        "--yes",
    )
    time.sleep(3)
    status, _, health = signed_request(edge, "GET", "/health")
    if status != 200:
        fail(f"Rollback health returned HTTP {status}: {health}")
    assert_version(health, target, "rollback health")
    report = {
        "status": "rolled_back",
        "completed_at": dt.datetime.now(dt.UTC).isoformat(),
        "from_version": current,
        "to_version": target,
        "message": message,
        "health": health,
        "deployment": deployments(environment)[-1],
    }
    path = write_receipt("rollback", report)
    print(json.dumps({"ok": True, "receipt": str(path), **report}, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="ordivon-edge-release")
    commands = root.add_subparsers(dest="command", required=True)

    release_command = commands.add_parser("release")
    release_command.add_argument("--message")

    rollback_command = commands.add_parser("rollback")
    rollback_command.add_argument("--version-id")
    rollback_command.add_argument("--message")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "release":
            return release(args)
        if args.command == "rollback":
            return rollback(args)
        fail(f"Unknown command: {args.command}")
    except ReleaseError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
