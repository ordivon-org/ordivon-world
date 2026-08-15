#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
LOCK = ROOT / "uv.lock"
HOST_REVISION = "ebaf6ef90d87e7bc524e8f30d71521b371d17f2e"
PROTOCOL_REVISION = "420dc356cb664d75db0f34f356156baebe5843db"
HOST_URL = "https://github.com/zycxfyh/ordivon-host.git"
PROTOCOL_URL = "https://github.com/zycxfyh/ordivon-computing.git"


class DependencyError(RuntimeError):
    pass


def main() -> int:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    dependencies = project["dependencies"]
    if not isinstance(dependencies, list):
        raise DependencyError("project dependencies are not a list")
    expected_host = f"ordivon-host @ git+{HOST_URL}@{HOST_REVISION}"
    if dependencies.count(expected_host) != 1:
        raise DependencyError("pyproject does not contain the exact Host revision once")
    if sum(str(item).startswith("ordivon-host") for item in dependencies) != 1:
        raise DependencyError("pyproject contains another Host dependency declaration")
    if sum(str(item).startswith("jsonschema") for item in dependencies) != 1:
        raise DependencyError("pyproject must declare one jsonschema dependency")

    lock = LOCK.read_text(encoding="utf-8")
    host_source = (
        f'git = "{HOST_URL}?rev={HOST_REVISION}#{HOST_REVISION}"'
    )
    protocol_source = (
        f'git = "{PROTOCOL_URL}?subdirectory=packages%2Fordivon-protocol'
        f'&rev={PROTOCOL_REVISION}#{PROTOCOL_REVISION}"'
    )
    if lock.count(host_source) != 1:
        raise DependencyError("uv.lock Host source differs from the public pin")
    if lock.count(protocol_source) != 1:
        raise DependencyError("uv.lock Protocol source differs from Host's public graph")
    if "requirements-audit.txt" not in {
        path.name for path in ROOT.glob("requirements-audit.txt")
    }:
        raise DependencyError("requirements-audit.txt is absent")

    print(
        json.dumps(
            {
                "ok": True,
                "hostRevision": HOST_REVISION,
                "protocolRevision": PROTOCOL_REVISION,
                "python": project["requires-python"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
