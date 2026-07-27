#!/usr/bin/env python3
"""Apply Ordivon Edge R2 lifecycle rules through the Cloudflare API."""

from __future__ import annotations

import json
import os
import pathlib
import urllib.error
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUCKET = "ordivon-artifacts"
CLOUDFLARE_CONFIG = pathlib.Path("/root/.config/ordivon/secrets/cloudflare.json")
POLICY_CONFIG = ROOT / "config" / "edge-policy.json"
MANAGED_PREFIX = "edge-v2-"
SECONDS_PER_DAY = 86400


class LifecycleError(RuntimeError):
    pass


def load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LifecycleError(f"Cannot read configuration: {path}") from exc
    if not isinstance(value, dict):
        raise LifecycleError(f"Configuration must be an object: {path}")
    return value


def api_request(method: str, path: str, token: str, body: dict[str, Any] | None = None) -> Any:
    encoded = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4{path}",
        data=encoded,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "ordivon-edge-lifecycle/0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read())
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        raise LifecycleError(f"Cloudflare lifecycle request failed: {method} {path}") from exc
    if not isinstance(payload, dict) or payload.get("success") is not True:
        raise LifecycleError(f"Cloudflare lifecycle request returned failure: {payload}")
    return payload.get("result")


def managed_rules(retention: dict[str, int]) -> list[dict[str, Any]]:
    definitions = [
        ("request-state", "requests/v2/", retention["request_state"]),
        ("receipt-mirror", "receipts/v2/", retention["receipt_mirror"]),
        ("fetch-artifacts", "fetch/v2/", retention["artifacts"]),
        ("browser-artifacts", "browser/v2/", retention["artifacts"]),
        ("cleanup-tasks", "cleanup/v2/", retention["cleanup_tasks"]),
    ]
    return [
        {
            "id": f"{MANAGED_PREFIX}{name}-{days}d",
            "enabled": True,
            "conditions": {"prefix": prefix},
            "deleteObjectsTransition": {
                "condition": {"type": "Age", "maxAge": days * SECONDS_PER_DAY}
            },
        }
        for name, prefix, days in definitions
    ]


def main() -> int:
    cloudflare = load_json(CLOUDFLARE_CONFIG)
    policy = load_json(POLICY_CONFIG)
    token = cloudflare.get("api_token")
    account_id = cloudflare.get("account_id")
    retention = policy.get("retention_days")
    if not isinstance(token, str) or not isinstance(account_id, str):
        raise LifecycleError("Cloudflare credentials are incomplete")
    if not isinstance(retention, dict):
        raise LifecycleError("Retention policy is missing")
    path = f"/accounts/{account_id}/r2/buckets/{BUCKET}/lifecycle"
    current = api_request("GET", path, token)
    rules = current.get("rules") if isinstance(current, dict) else None
    if not isinstance(rules, list):
        raise LifecycleError("Cloudflare lifecycle response has no rules")
    preserved = [
        rule
        for rule in rules
        if isinstance(rule, dict) and not str(rule.get("id", "")).startswith(MANAGED_PREFIX)
    ]
    expected_managed = managed_rules(retention)
    api_request("PUT", path, token, {"rules": [*preserved, *expected_managed]})
    verified = api_request("GET", path, token)
    verified_rules = verified.get("rules") if isinstance(verified, dict) else None
    if not isinstance(verified_rules, list):
        raise LifecycleError("Updated lifecycle response has no rules")
    actual_managed = sorted(
        (rule for rule in verified_rules if str(rule.get("id", "")).startswith(MANAGED_PREFIX)),
        key=lambda rule: str(rule.get("id")),
    )
    if actual_managed != sorted(expected_managed, key=lambda rule: str(rule.get("id"))):
        raise LifecycleError("Lifecycle verification did not match the policy")
    print(json.dumps({"ok": True, "bucket": BUCKET, "rules": verified_rules}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
