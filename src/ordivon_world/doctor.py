from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import stat
import subprocess
from typing import Any, Callable
import urllib.error
import urllib.request

from .cloudflare import CloudflareWorldAdapter, WorldAdapterError
from .schemas import load_schema
from .version import __version__

DEFAULT_REPOSITORY = Path("/root/projects/ordivon-world")
CLOUDFLARE_CONFIG = Path("/root/.config/ordivon/secrets/cloudflare.json")
EDGE_CLIENT_CONFIG = Path("/root/.config/ordivon/secrets/edge-client.json")
MANAGED_LIFECYCLE_PREFIX = "edge-v2-"
SECONDS_PER_DAY = 86_400


@dataclass(frozen=True, slots=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


CommandRunner = Callable[[list[str]], CommandResult]


def run_command(command: list[str]) -> CommandResult:
    completed = subprocess.run(
        command,
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def check(name: str, status: str, **details: Any) -> dict[str, Any]:
    if status not in {"ok", "attention", "skipped"}:
        raise ValueError(f"invalid doctor status: {status}")
    return {"name": name, "status": status, **details}


def overall_status(checks: list[dict[str, Any]]) -> str:
    return "attention" if any(item["status"] == "attention" for item in checks) else "ok"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def repository_check(repository: Path, runner: CommandRunner) -> dict[str, Any]:
    head = runner(["git", "-C", str(repository), "rev-parse", "HEAD"])
    status = runner(["git", "-C", str(repository), "status", "--porcelain"])
    branch = runner(["git", "-C", str(repository), "branch", "--show-current"])
    if head.returncode != 0 or status.returncode != 0 or branch.returncode != 0:
        return check("repository", "attention", error="Git repository inspection failed")
    dirty_paths = [line for line in status.stdout.splitlines() if line]
    return check(
        "repository",
        "ok" if not dirty_paths else "attention",
        head=head.stdout.strip(),
        branch=branch.stdout.strip() or None,
        dirty=bool(dirty_paths),
        dirtyPaths=dirty_paths,
    )


def contract_check() -> dict[str, Any]:
    names = (
        "browser-manifest",
        "browser-request",
        "edge-capabilities",
        "edge-receipt",
        "fetch-request",
        "world-observation",
        "world-prepared-dispatch",
    )
    try:
        for name in names:
            load_schema(name)
    except Exception as error:
        return check("contracts", "attention", error=str(error))
    return check("contracts", "ok", count=len(names), draft="2020-12")


def private_config_check(path: Path, name: str) -> dict[str, Any]:
    if not path.exists():
        return check(name, "attention", path=str(path), error="missing")
    try:
        metadata = path.stat()
        mode = stat.S_IMODE(metadata.st_mode)
        value = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return check(name, "attention", path=str(path), error=str(error))
    return check(
        name,
        "ok" if mode == 0o600 else "attention",
        path=str(path),
        mode=f"{mode:04o}",
        ownerUid=metadata.st_uid,
        keys=sorted(value),
    )


def installed_tools_check(repository: Path) -> dict[str, Any]:
    paths = (
        (
            repository / "providers/cloudflare/scripts/ordivon_edge_client.py",
            Path("/usr/local/bin/ordivon-edge"),
        ),
        (
            repository / "providers/cloudflare/scripts/ordivon_edge_release.py",
            Path("/usr/local/sbin/ordivon-edge-release"),
        ),
        (
            repository / "providers/cloudflare/scripts/ordivon_edge_gc.py",
            Path("/usr/local/sbin/ordivon-edge-gc"),
        ),
        (
            repository / "modules/network-observation/scripts/ordivon-vpn",
            Path("/usr/local/sbin/ordivon-vpn"),
        ),
    )
    items: list[dict[str, Any]] = []
    current = True
    for source, installed in paths:
        item: dict[str, Any] = {
            "source": str(source),
            "installed": str(installed),
            "sourceExists": source.is_file(),
            "installedExists": installed.is_file(),
        }
        if source.is_file() and installed.is_file():
            item["sourceSha256"] = sha256_file(source)
            item["installedSha256"] = sha256_file(installed)
            item["current"] = item["sourceSha256"] == item["installedSha256"]
        else:
            item["current"] = False
        current = current and bool(item["current"])
        items.append(item)
    return check("installed-tools", "ok" if current else "attention", tools=items)


def parse_json_command(result: CommandResult, label: str) -> dict[str, Any]:
    if result.returncode != 0:
        raise RuntimeError(
            f"{label} failed with exit {result.returncode}: "
            f"{(result.stderr or result.stdout).strip()}"
        )
    value = json.loads(result.stdout)
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} returned a non-object")
    return value


def edge_status_check(repository: Path, runner: CommandRunner) -> dict[str, Any]:
    command = [
        "/usr/local/bin/ordivon-edge",
        "status",
        "--repo",
        str(repository),
        "--expected-ref",
        "HEAD",
    ]
    try:
        value = parse_json_command(runner(command), "ordivon-edge status")
        deployment = value.get("deployment")
        if not isinstance(deployment, dict):
            raise RuntimeError("deployment status is absent")
        healthy = (
            value.get("ok") is True
            and value.get("status") == "ok"
            and deployment.get("worker_inputs") == "current"
        )
        return check("cloudflare-edge", "ok" if healthy else "attention", report=value)
    except Exception as error:
        return check("cloudflare-edge", "attention", error=str(error))


def capability_check() -> dict[str, Any]:
    try:
        snapshot = CloudflareWorldAdapter.from_config().capabilities()
    except WorldAdapterError as error:
        return check("cloudflare-capabilities", "attention", error=str(error))
    return check(
        "cloudflare-capabilities",
        "ok",
        provider=snapshot.provider,
        capturedAt=snapshot.captured_at,
        conditionDigest=snapshot.condition_digest,
        observationDigest=snapshot.observation_digest,
        policyVersion=snapshot.raw["policy_version"],
        capabilities=snapshot.raw["capabilities"],
        workerVersion=snapshot.raw["worker_version"],
    )


def systemd_properties(unit: str, runner: CommandRunner) -> dict[str, str]:
    result = runner(
        [
            "systemctl",
            "show",
            unit,
            "-p",
            "LoadState",
            "-p",
            "ActiveState",
            "-p",
            "SubState",
            "-p",
            "Result",
            "-p",
            "ExecMainStatus",
        ]
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())
    properties: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            properties[key] = value
    return properties


def gc_check(runner: CommandRunner) -> dict[str, Any]:
    try:
        timer = systemd_properties("ordivon-edge-gc.timer", runner)
        service = systemd_properties("ordivon-edge-gc.service", runner)
    except Exception as error:
        return check("cloudflare-gc", "attention", error=str(error))
    timer_ok = timer.get("LoadState") == "loaded" and timer.get("ActiveState") == "active"
    service_ok = service.get("Result") in {"success", ""} and service.get("ExecMainStatus") in {
        "0",
        "",
    }
    return check(
        "cloudflare-gc",
        "ok" if timer_ok and service_ok else "attention",
        timer=timer,
        service=service,
    )


def expected_lifecycle_rules(retention: dict[str, Any]) -> list[dict[str, Any]]:
    definitions = (
        ("request-state", "requests/v2/", retention["request_state"]),
        ("receipt-mirror", "receipts/v2/", retention["receipt_mirror"]),
        ("fetch-artifacts", "fetch/v2/", retention["artifacts"]),
        ("browser-artifacts", "browser/v2/", retention["artifacts"]),
        ("cleanup-tasks", "cleanup/v2/", retention["cleanup_tasks"]),
    )
    return [
        {
            "id": f"{MANAGED_LIFECYCLE_PREFIX}{name}-{days}d",
            "enabled": True,
            "conditions": {"prefix": prefix},
            "deleteObjectsTransition": {
                "condition": {
                    "type": "Age",
                    "maxAge": int(days) * SECONDS_PER_DAY,
                }
            },
        }
        for name, prefix, days in definitions
    ]


def lifecycle_check(repository: Path) -> dict[str, Any]:
    try:
        cloudflare = load_json(CLOUDFLARE_CONFIG)
        policy = load_json(
            repository / "providers/cloudflare/config/edge-policy.json"
        )
        token = cloudflare["api_token"]
        account_id = cloudflare["account_id"]
        retention = policy["retention_days"]
        if not isinstance(token, str) or not isinstance(account_id, str):
            raise ValueError("Cloudflare credentials are incomplete")
        if not isinstance(retention, dict):
            raise ValueError("retention policy is invalid")
        path = (
            "https://api.cloudflare.com/client/v4/accounts/"
            f"{account_id}/r2/buckets/ordivon-artifacts/lifecycle"
        )
        request = urllib.request.Request(
            path,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "User-Agent": f"ordivon-world-doctor/{__version__}",
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read())
        if not isinstance(payload, dict) or payload.get("success") is not True:
            raise ValueError("Cloudflare lifecycle API returned failure")
        result = payload.get("result")
        rules = result.get("rules") if isinstance(result, dict) else None
        if not isinstance(rules, list):
            raise ValueError("Cloudflare lifecycle response has no rules")
        expected = sorted(expected_lifecycle_rules(retention), key=lambda item: item["id"])
        actual = sorted(
            [
                item
                for item in rules
                if isinstance(item, dict)
                and str(item.get("id", "")).startswith(MANAGED_LIFECYCLE_PREFIX)
            ],
            key=lambda item: str(item["id"]),
        )
        return check(
            "cloudflare-r2-lifecycle",
            "ok" if actual == expected else "attention",
            expected=expected,
            actual=actual,
        )
    except (OSError, KeyError, ValueError, json.JSONDecodeError, urllib.error.URLError) as error:
        return check("cloudflare-r2-lifecycle", "attention", error=str(error))


def network_check(repository: Path, runner: CommandRunner) -> dict[str, Any]:
    installed = Path("/usr/local/sbin/ordivon-vpn")
    source = repository / "modules/network-observation/scripts/ordivon-vpn"
    executable = installed if installed.is_file() else source
    result = runner([str(executable), "doctor"])
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        return check(
            "network-observation",
            "attention",
            exitCode=result.returncode,
            error=f"ordivon-vpn doctor returned invalid JSON: {error}",
            stderr=result.stderr.strip() or None,
        )
    if not isinstance(value, dict):
        return check(
            "network-observation",
            "attention",
            exitCode=result.returncode,
            error="ordivon-vpn doctor returned a non-object",
            stderr=result.stderr.strip() or None,
        )
    healthy = (
        result.returncode == 0
        and value.get("config_valid") is True
        and value.get("key_pair_consistent") is True
        and value.get("missing_commands") == []
    )
    return check(
        "network-observation",
        "ok" if healthy else "attention",
        exitCode=result.returncode,
        report=value,
        stderr=result.stderr.strip() or None,
    )


def collect_report(
    repository: Path,
    *,
    offline: bool = False,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    repository = repository.expanduser().resolve()
    checks = [
        repository_check(repository, runner),
        contract_check(),
    ]
    if offline:
        checks.extend(
            [
                check("installed-tools", "skipped", reason="offline"),
                check("edge-client-config", "skipped", reason="offline"),
                check("cloudflare-control-config", "skipped", reason="offline"),
                check("cloudflare-edge", "skipped", reason="offline"),
                check("cloudflare-capabilities", "skipped", reason="offline"),
                check("cloudflare-r2-lifecycle", "skipped", reason="offline"),
                check("cloudflare-gc", "skipped", reason="offline"),
                check("network-observation", "skipped", reason="offline"),
            ]
        )
    else:
        checks.extend(
            [
                installed_tools_check(repository),
                private_config_check(EDGE_CLIENT_CONFIG, "edge-client-config"),
                private_config_check(
                    CLOUDFLARE_CONFIG,
                    "cloudflare-control-config",
                ),
                edge_status_check(repository, runner),
                capability_check(),
                lifecycle_check(repository),
                gc_check(runner),
                network_check(repository, runner),
            ]
        )
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world-doctor-report",
        "version": __version__,
        "repository": str(repository),
        "status": overall_status(checks),
        "checks": checks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ordivon-world-doctor",
        description="Inspect repository, provider, retention, GC and network operational truth.",
    )
    parser.add_argument("--repo", default=str(DEFAULT_REPOSITORY))
    parser.add_argument("--offline", action="store_true")
    return parser


def entrypoint() -> None:
    args = build_parser().parse_args()
    report = collect_report(Path(args.repo), offline=args.offline)
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if report["status"] == "ok" else 1)


if __name__ == "__main__":
    entrypoint()
