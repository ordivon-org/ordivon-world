#!/usr/bin/env python3
"""Remote-to-remote Artifact transfer comparison."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from typing import Any


def compare(
    *,
    source_bytes: int,
    source_sha256: str,
    provider_artifact_sha256: str,
    submission_bytes: int,
    provider_response_bytes: int,
    status_response_bytes: int,
    result_manifest_bytes: int,
) -> dict[str, Any]:
    if source_bytes <= 0:
        raise ValueError("source_bytes must be positive")
    digest_verified = source_sha256 == provider_artifact_sha256
    host_proxy_bytes = source_bytes * 2
    remote_reference_bytes = (
        submission_bytes
        + provider_response_bytes
        + status_response_bytes
        + result_manifest_bytes
    )
    result: dict[str, Any] = {
        "schema_version": 1,
        "experiment": "WXP-2 remote-to-remote Artifact movement",
        "arms": {
            "host-proxy": {
                "description": "Host downloads source bytes and uploads the same bytes to object storage.",
                "host_transit_bytes": host_proxy_bytes,
                "source_bytes": source_bytes,
                "copies_through_host": 2,
            },
            "provider-to-r2": {
                "description": "Cloudflare Workflow fetches and writes to R2; Host receives provider handles, status, and manifest references.",
                "host_transit_bytes": remote_reference_bytes,
                "source_bytes": source_bytes,
                "copies_through_host": 0,
            },
        },
        "integrity": {
            "direct_source_sha256": source_sha256,
            "provider_artifact_sha256": provider_artifact_sha256,
            "digest_verified": digest_verified,
        },
        "measurements": {
            "host_bytes_avoided": host_proxy_bytes - remote_reference_bytes,
            "host_transit_reduction_ratio": 1 - remote_reference_bytes / host_proxy_bytes,
        },
        "decision": {
            "disposition": "keep-provider-native",
            "retain": [
                "provider-native Workflow handle",
                "R2 ArtifactRef with digest and byte length",
                "Host-independent Verification",
            ],
            "reject": [
                "mandatory Host byte proxy",
                "independent World Artifact transfer service",
                "universal transfer state machine",
            ],
            "reason": "Direct provider-to-R2 movement preserves digest and provenance while removing source bytes from the Host path. Existing Workflow, R2, ArtifactRef, and Host Verification responsibilities are sufficient.",
        },
    }
    result["valid"] = digest_verified and remote_reference_bytes < host_proxy_bytes
    result["evidence_sha256"] = hashlib.sha256(
        (json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path(__file__).with_name("evidence.json"))
    args = parser.parse_args()
    if args.input is None:
        fixture = b"ordivon-world-remote-artifact-fixture\n" * 32768
        digest = hashlib.sha256(fixture).hexdigest()
        values = {
            "source_bytes": len(fixture),
            "source_sha256": digest,
            "provider_artifact_sha256": digest,
            "submission_bytes": 512,
            "provider_response_bytes": 640,
            "status_response_bytes": 2048,
            "result_manifest_bytes": 1536,
        }
    else:
        values = json.loads(args.input.read_text(encoding="utf-8"))
    result = compare(**values)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
