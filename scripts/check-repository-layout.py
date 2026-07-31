#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
    "docs/w0-carrier-inventory.json",
    "docs/w0-carrier-inventory.md",
    "docs/w1-experiment-contract.md",
    "docs/w1-results.md",
    "evidence/w1/w1-live-20260731c.json",
    "scripts/check-w1-evidence.py",
    "experiments/w1-host-cloudflare/pyproject.toml",
    "experiments/w1-host-cloudflare/uv.lock",
    "experiments/w1-host-cloudflare/README.md",
    "experiments/w1-host-cloudflare/src/ordivon_world_w1/experiment.py",
    "experiments/w1-host-cloudflare/tests/test_w1.py",
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
for phrase in [
    "W1 did not earn an independent production World layer",
    "providers/cloudflare",
    "modules/network-observation",
    "docs/w1-results.md",
    "evidence/w1/w1-live-20260731c.json",
    "W2 conditional",
]:
    if phrase not in readme:
        raise SystemExit(f"README missing required phrase: {phrase}")

inventory_path = ROOT / "docs/w0-carrier-inventory.json"
inventory = json.loads(inventory_path.read_text())
if inventory.get("schemaVersion") != 1:
    raise SystemExit("unsupported W0 inventory schema")
if inventory.get("kind") != "ordivon-world-w0-carrier-inventory":
    raise SystemExit("invalid W0 inventory identity")
if not re.fullmatch(r"[0-9a-f]{40}", inventory.get("sourceRevision", "")):
    raise SystemExit("W0 inventory sourceRevision must be a full Git SHA")

allowed = {"retain", "adapter-only", "historical", "delete-candidate"}
if set(inventory.get("allowedDispositions", [])) != allowed:
    raise SystemExit("W0 inventory disposition vocabulary drifted")

carriers = inventory.get("carriers")
if not isinstance(carriers, list) or not carriers:
    raise SystemExit("W0 inventory carriers must be non-empty")
identifiers = [carrier.get("id") for carrier in carriers]
if len(identifiers) != len(set(identifiers)):
    raise SystemExit("W0 inventory carrier ids must be unique")
seen_dispositions: set[str] = set()
for carrier in carriers:
    disposition = carrier.get("disposition")
    if disposition not in allowed:
        raise SystemExit(f"invalid W0 disposition: {carrier.get('id')} -> {disposition}")
    seen_dispositions.add(disposition)
    paths = carrier.get("paths")
    if not isinstance(paths, list) or not paths:
        raise SystemExit(f"W0 carrier has no paths: {carrier.get('id')}")
    for path in paths:
        candidate = ROOT / path
        if not candidate.exists():
            raise SystemExit(f"W0 carrier path does not exist: {carrier.get('id')} -> {path}")
    role = carrier.get("w1Role")
    if role != "none" and disposition not in {"retain", "adapter-only"}:
        raise SystemExit(f"W1 cannot consume {disposition} carrier: {carrier.get('id')}")
if seen_dispositions != allowed:
    raise SystemExit("W0 inventory must exercise every disposition")

live = inventory.get("liveReadOnlyBaseline", {})
provider = live.get("provider", {})
observation = live.get("pathObservation", {})
if provider.get("status") != "ok":
    raise SystemExit("W0 live provider baseline was not healthy")
if provider.get("fetchCapability") != "fetch.v2" or provider.get("receiptCapability") != "receipt.v2":
    raise SystemExit("W0 live provider capability baseline is incomplete")
if observation.get("target") != "w1-example" or observation.get("success") is not True:
    raise SystemExit("W0 live path-observation baseline is incomplete")

selection = inventory.get("w1Selection", {})
expected_selection = {
    "provider": "cloudflare",
    "providerOperation": "fetch",
    "target": "https://example.com/",
    "pathObservationProducer": "link-probe",
    "primaryBaseline": "direct-host-to-provider",
    "faultPoint": "after-provider-receipt-commit-before-host-admission",
    "pathChangeInW1": False,
    "providerRebindingInW1": False,
}
if selection != expected_selection:
    raise SystemExit("W1 selection is not frozen to the audited Fetch trajectory")

by_id = {carrier["id"]: carrier for carrier in carriers}
for required_id, expected_disposition in {
    "cloudflare-fetch-provider": "retain",
    "cloudflare-request-reliability": "retain",
    "cloudflare-direct-client": "adapter-only",
    "network-probe-observations": "adapter-only",
    "deterministic-network-world": "historical",
    "cloudflare-node-lifecycle-research": "historical",
    "unused-link-model-entities": "delete-candidate",
    "universal-world-interaction-schema": "delete-candidate",
}.items():
    carrier = by_id.get(required_id)
    if carrier is None or carrier.get("disposition") != expected_disposition:
        raise SystemExit(f"required W0 disposition missing: {required_id}")

contract = (ROOT / "docs/w1-experiment-contract.md").read_text()
for phrase in [
    "after-provider-receipt-commit-before-host-admission",
    "B0 — direct integration",
    "B1 — minimum World correlation",
    "query GET /v1/receipts/<request-id> before any redispatch",
    "No universal World ID is introduced",
    "Browser Run",
    "Every B1 field receives",
]:
    if phrase not in contract:
        raise SystemExit(f"W1 contract missing frozen requirement: {phrase}")

print("ordivon-world layout and W0 contract: ok")
