#!/usr/bin/env python3
"""Generate a deterministic read-only capability portfolio."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = (
    ROOT / "providers/cloudflare/capability.json",
    ROOT / "modules/network-observation/capability.json",
)
JSON_OUT = ROOT / "evidence/capability-portfolio-v0.json"
MD_OUT = ROOT / "docs/capability-portfolio.md"
TOP_KEYS = {
    "schema_version", "adapter_id", "adapter_revision", "owner", "authority",
    "real_consumers", "consequence_class", "cost_model", "retention_source",
    "deletion_trigger", "facets", "capabilities"
}
CAP_KEYS = {"id", "contract", "execution_mode", "state"}
STATES = {"ready", "implementing", "planned", "disabled"}


class PortfolioError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def load(path: pathlib.Path) -> tuple[dict[str, Any], str]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PortfolioError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict) or set(value) != TOP_KEYS:
        raise PortfolioError(f"invalid top-level keys: {path}")
    if value["schema_version"] != 1:
        raise PortfolioError(f"unsupported schema: {path}")
    for key in ("adapter_id", "adapter_revision", "owner", "consequence_class", "retention_source", "deletion_trigger"):
        if not isinstance(value[key], str) or not value[key]:
            raise PortfolioError(f"invalid {key}: {path}")
    for key in ("authority", "real_consumers", "facets", "capabilities"):
        if not isinstance(value[key], list) or not value[key]:
            raise PortfolioError(f"invalid {key}: {path}")
    if not isinstance(value["cost_model"], dict) or set(value["cost_model"]) != {"fixed", "variable"}:
        raise PortfolioError(f"invalid cost_model: {path}")
    seen: set[str] = set()
    for item in value["capabilities"]:
        if not isinstance(item, dict) or set(item) != CAP_KEYS:
            raise PortfolioError(f"invalid capability: {path}")
        if item["state"] not in STATES or item["id"] in seen:
            raise PortfolioError(f"invalid or duplicate capability: {path}")
        seen.add(item["id"])
    normalized = json.loads(canonical(value))
    return normalized, hashlib.sha256(canonical(normalized)).hexdigest()


def build() -> tuple[str, str]:
    adapters: list[dict[str, Any]] = []
    for path in SOURCES:
        item, digest = load(path)
        adapters.append({**item, "declaration_path": path.relative_to(ROOT).as_posix(), "declaration_sha256": digest})
    adapters.sort(key=lambda item: item["adapter_id"])
    portfolio = {
        "schema_version": 1,
        "kind": "ordivon-world-capability-portfolio",
        "authority": "read-only projection of adapter-local declarations",
        "writable_registry": False,
        "adapters": adapters,
    }
    lines = [
        "# World Capability Portfolio", "",
        "Generated from adapter-local declarations. This is a read-only view, not a registry or operational authority.", "",
        "| Adapter | Owner | Facets | Capabilities | Consumers | Deletion trigger |",
        "|---|---|---|---|---|---|",
    ]
    for item in adapters:
        caps = ", ".join(f"`{cap['id']}` ({cap['state']})" for cap in item["capabilities"])
        lines.append("| " + " | ".join([
            f"`{item['adapter_id']}` `{item['adapter_revision']}`",
            item["owner"],
            ", ".join(f"`{facet}`" for facet in item["facets"]),
            caps,
            "; ".join(item["real_consumers"]),
            item["deletion_trigger"],
        ]) + " |")
    lines += ["", "## Admission rule", "", "A capability remains local unless two materially different workloads reproduce one unowned, non-bypassable responsibility with lower total cost.", ""]
    return json.dumps(portfolio, indent=2, ensure_ascii=False) + "\n", "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        expected_json, expected_md = build()
        if args.check:
            if JSON_OUT.read_text(encoding="utf-8") != expected_json or MD_OUT.read_text(encoding="utf-8") != expected_md:
                raise PortfolioError("generated outputs are stale")
        else:
            JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
            JSON_OUT.write_text(expected_json, encoding="utf-8")
            MD_OUT.write_text(expected_md, encoding="utf-8")
    except (PortfolioError, OSError) as exc:
        print(f"capability portfolio: {exc}", file=sys.stderr)
        return 1
    print("ordivon-world capability portfolio: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
