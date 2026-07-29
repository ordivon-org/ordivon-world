#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "docs/charter.md",
    "docs/architecture.md",
    "docs/interaction-model.md",
    "docs/component-map.md",
    "docs/research-route.md",
    "docs/boundary.md",
    "docs/migration.md",
    "migration/sources.json",
    "providers/cloudflare/package.json",
    "providers/cloudflare/wrangler.jsonc",
    "modules/network-observation/Cargo.toml",
]

missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

for nested in [
    ROOT / "providers/cloudflare/.github",
    ROOT / "modules/network-observation/.github",
]:
    if nested.exists():
        raise SystemExit(f"nested workflow directory must be removed: {nested}")

sources = json.loads((ROOT / "migration/sources.json").read_text())
if sources.get("schemaVersion") != 1 or len(sources.get("sources", [])) != 2:
    raise SystemExit("invalid migration/sources.json")

readme = (ROOT / "README.md").read_text()
for phrase in ["World Interaction", "providers/cloudflare", "modules/network-observation"]:
    if phrase not in readme:
        raise SystemExit(f"README missing required phrase: {phrase}")

print("ordivon-world layout: ok")
