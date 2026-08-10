#!/usr/bin/env python3
from __future__ import annotations

import argparse
from email.parser import BytesParser
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

EXPECTED_VERSION = "0.4.0"
HOST_REVISION = "95cd5479e71281baed5a1d1c34cbfaadffe2a22f"
EXPECTED_SCHEMA_NAMES = (
    "browser-manifest",
    "browser-request",
    "edge-capabilities",
    "edge-receipt",
    "entity-departure-receipt",
    "entity-migration-destination-request",
    "entity-migration-destination-response",
    "entity-migration-not-committed",
    "entity-migration-plan",
    "entity-migration-receipt",
    "fetch-request",
    "message-delivery-destination-request",
    "message-delivery-destination-response",
    "message-delivery-not-committed",
    "message-delivery-plan",
    "message-delivery-receipt",
    "message-issuance-receipt",
    "resource-egress-receipt",
    "resource-transfer-destination-request",
    "resource-transfer-destination-response",
    "resource-transfer-not-committed",
    "resource-transfer-plan",
    "resource-transfer-receipt",
    "world-observation",
    "world-prepared-dispatch",
)


class WheelError(RuntimeError):
    pass


def command(arguments: list[str], *, cwd: Path | None = None) -> str:
    completed = subprocess.run(
        arguments,
        cwd=cwd,
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise WheelError(
            f"command failed ({completed.returncode}): {' '.join(arguments)}\n"
            + (completed.stderr or completed.stdout).strip()
        )
    return completed.stdout


def find_wheel(path: Path) -> Path:
    if path.is_file() and path.suffix == ".whl":
        return path.resolve()
    wheels = sorted(path.glob("*.whl"))
    if len(wheels) != 1:
        raise WheelError(f"expected exactly one wheel, found {len(wheels)}")
    return wheels[0].resolve()


def inspect_wheel(wheel: Path) -> dict[str, object]:
    with zipfile.ZipFile(wheel) as archive:
        metadata_names = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        entry_names = [name for name in archive.namelist() if name.endswith(".dist-info/entry_points.txt")]
        if len(metadata_names) != 1 or len(entry_names) != 1:
            raise WheelError("wheel has no unique metadata or entry-point document")
        metadata = BytesParser().parsebytes(archive.read(metadata_names[0]))
        entries = archive.read(entry_names[0]).decode("utf-8")
        schema_names = tuple(
            sorted(
                Path(name).name.removesuffix(".schema.json")
                for name in archive.namelist()
                if "/contracts/" in name and name.endswith(".schema.json")
            )
        )
    if metadata["Name"] != "ordivon-world":
        raise WheelError("wheel project name differs")
    if metadata["Version"] != EXPECTED_VERSION:
        raise WheelError("wheel version differs")
    python_range = metadata["Requires-Python"]
    normalized_range = tuple(
        sorted(part.strip() for part in python_range.split(",") if part.strip())
    )
    if normalized_range != ("<3.13", ">=3.12"):
        raise WheelError("wheel Python range differs")
    requirements = metadata.get_all("Requires-Dist") or []
    if not any(HOST_REVISION in item for item in requirements):
        raise WheelError("wheel Host dependency is not revision-pinned")
    if not any(item.lower().startswith("jsonschema") for item in requirements):
        raise WheelError("wheel jsonschema dependency is absent")
    if "ordivon-world-doctor = ordivon_world.doctor:entrypoint" not in entries:
        raise WheelError("wheel doctor entry point is absent")
    if schema_names != EXPECTED_SCHEMA_NAMES:
        raise WheelError("wheel contract schema set differs from the current public contract set")
    return {
        "name": metadata["Name"],
        "version": metadata["Version"],
        "schemas": len(schema_names),
    }


def install_and_import(wheel: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ordivon-world-wheel-") as directory:
        root = Path(directory)
        environment = root / ".venv"
        command(["uv", "venv", "--python", "3.12", str(environment)])
        python = environment / "bin" / "python"
        command(["uv", "pip", "install", "--python", str(python), str(wheel)])
        program = (
            "import json; "
            "from ordivon_world import (EntityMigrationBundle, MessageDeliveryBundle, ResourceTransferBundle, load_schema); "
            f"names={EXPECTED_SCHEMA_NAMES!r}; "
            "[load_schema(name) for name in names]; "
            "print(json.dumps({'api':['EntityMigrationBundle','MessageDeliveryBundle','ResourceTransferBundle'],"
            "'schemas':len(names)}))"
        )
        output = command([str(python), "-I", "-c", program], cwd=root)
        value = json.loads(output)
        if value != {
            "api": ["EntityMigrationBundle", "MessageDeliveryBundle", "ResourceTransferBundle"],
            "schemas": len(EXPECTED_SCHEMA_NAMES),
        }:
            raise WheelError("isolated wheel import returned an unexpected result")
        command([str(environment / "bin" / "ordivon-world-doctor"), "--help"], cwd=root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    wheel = find_wheel(Path(args.path))
    metadata = inspect_wheel(wheel)
    install_and_import(wheel)
    print(
        json.dumps(
            {
                "ok": True,
                "wheel": wheel.name,
                **metadata,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
