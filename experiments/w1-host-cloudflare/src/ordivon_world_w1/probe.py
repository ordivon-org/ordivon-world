from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess

from .models import ProbeProjection


_TARGET_TOML = """schema_version = 1
[[targets]]
id = "w1-example"
url = "https://example.com/"
enabled = true
protocols = ["http_tls"]
"""


def run_link_probe(
    *,
    repository_root: str | Path,
    evidence_root: str | Path,
    network: str,
    route: str,
) -> tuple[dict[str, object], ProbeProjection]:
    root = Path(repository_root).resolve()
    evidence = Path(evidence_root).resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    target_path = evidence / "probe-target.toml"
    output_path = evidence / "probe-source.ndjson"
    target_path.write_text(_TARGET_TOML)
    os.chmod(target_path, 0o600)
    cargo = os.environ.get("ORDIVON_W1_CARGO") or shutil.which("cargo")
    if cargo is None:
        raise RuntimeError("cargo is unavailable for the source-native link-probe")
    command = [
        cargo,
        "run",
        "-q",
        "-p",
        "link-probe",
        "--",
        "run",
        "--targets",
        str(target_path),
        "--network",
        network,
        "--route",
        route,
        "--protocol",
        "http-tls",
        "--repeat",
        "1",
        "--timeout-seconds",
        "15",
        "--no-env-proxy",
        "--truncate-output",
        "--output",
        str(output_path),
    ]
    subprocess.run(
        command,
        cwd=root / "modules/network-observation",
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    lines = output_path.read_text().splitlines()
    if len(lines) != 1:
        raise RuntimeError("W1 requires exactly one source ProbeResult")
    raw = json.loads(lines[0])
    if not isinstance(raw, dict):
        raise RuntimeError("source ProbeResult is not an object")
    projection = ProbeProjection.from_source(raw)
    normalized = evidence / "probe-source.json"
    normalized.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    os.chmod(normalized, 0o600)
    return dict(raw), projection
