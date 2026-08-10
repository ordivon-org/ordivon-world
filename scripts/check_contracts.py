#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any

from ordivon_world import load_schema, validate_contract

ROOT = Path(__file__).resolve().parent.parent
PROVIDER = ROOT / "providers" / "cloudflare"
POLICY = PROVIDER / "config" / "edge-policy.json"
EMITTER = PROVIDER / "scripts" / "emit-contract-fixtures.ts"
CONTRACTS = (
    "browser-manifest",
    "browser-request",
    "edge-capabilities",
    "edge-receipt",
    "fetch-request",
    "world-observation",
    "world-prepared-dispatch",
)


class ContractCheckError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractCheckError(f"JSON document must be an object: {path}")
    return value


def expect(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise ContractCheckError(
            f"{label} differs: schema={actual!r}, policy={expected!r}"
        )


def check_policy_coupling() -> None:
    policy = load_json(POLICY)
    fetch = policy["fetch"]
    browser = policy["browser"]
    fetch_schema = load_schema("fetch-request")["properties"]
    browser_schema = load_schema("browser-request")["properties"]

    expect(fetch_schema["url"]["maxLength"], fetch["max_url_bytes"], "fetch URL bound")
    expect(
        fetch_schema["maximum_bytes"]["maximum"],
        fetch["max_response_bytes"],
        "fetch response bound",
    )
    expect(
        fetch_schema["timeout_ms"]["minimum"],
        fetch["min_timeout_ms"],
        "fetch timeout minimum",
    )
    expect(
        fetch_schema["timeout_ms"]["maximum"],
        fetch["max_timeout_ms"],
        "fetch timeout maximum",
    )
    expect(
        fetch_schema["accept"]["maxLength"],
        fetch["max_accept_bytes"],
        "fetch accept bound",
    )
    expect(
        browser_schema["viewport_width"]["minimum"],
        browser["viewport"]["min_width"],
        "browser viewport width minimum",
    )
    expect(
        browser_schema["viewport_width"]["maximum"],
        browser["viewport"]["max_width"],
        "browser viewport width maximum",
    )
    expect(
        browser_schema["viewport_height"]["minimum"],
        browser["viewport"]["min_height"],
        "browser viewport height minimum",
    )
    expect(
        browser_schema["viewport_height"]["maximum"],
        browser["viewport"]["max_height"],
        "browser viewport height maximum",
    )
    expect(
        browser_schema["timeout_ms"]["minimum"],
        browser["timeout"]["min_ms"],
        "browser timeout minimum",
    )
    expect(
        browser_schema["timeout_ms"]["maximum"],
        browser["timeout"]["max_ms"],
        "browser timeout maximum",
    )
    expect(
        browser_schema["wait_after_ms"]["minimum"],
        browser["wait_after"]["min_ms"],
        "browser wait minimum",
    )
    expect(
        browser_schema["wait_after_ms"]["maximum"],
        browser["wait_after"]["max_ms"],
        "browser wait maximum",
    )
    expect(
        browser_schema["wait_until"]["enum"],
        browser["wait_until"],
        "browser lifecycle events",
    )


def provider_fixtures() -> dict[str, Any]:
    typecheck = subprocess.run(
        [
            "pnpm",
            "exec",
            "tsc",
            "--project",
            "scripts/tsconfig.contracts.json",
            "--noEmit",
        ],
        cwd=PROVIDER,
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if typecheck.returncode != 0:
        raise ContractCheckError(
            "TypeScript contract fixture typecheck failed: "
            + (typecheck.stderr or typecheck.stdout).strip()
        )
    completed = subprocess.run(
        ["pnpm", "exec", "tsx", str(EMITTER)],
        cwd=PROVIDER,
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise ContractCheckError(
            "TypeScript contract fixture generation failed: "
            + (completed.stderr or completed.stdout).strip()
        )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise ContractCheckError("TypeScript contract fixtures are not an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-provider-fixtures",
        action="store_true",
        help="validate packaged schemas and policy only",
    )
    args = parser.parse_args()

    for name in CONTRACTS:
        load_schema(name)
    check_policy_coupling()
    fixture_count = 0
    if not args.skip_provider_fixtures:
        fixtures = provider_fixtures()
        validate_contract("edge-capabilities", fixtures.get("capabilities"))
        validate_contract("browser-manifest", fixtures.get("browserManifest"))
        for name in (
            "fetchReceipt",
            "browserReceipt",
            "pendingReceipt",
            "rejectedReceipt",
        ):
            validate_contract("edge-receipt", fixtures.get(name))
        fixture_count = 6
    print(
        json.dumps(
            {
                "ok": True,
                "schemas": len(CONTRACTS),
                "providerFixtures": fixture_count,
                "policyCoupling": True,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
