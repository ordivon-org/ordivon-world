#!/usr/bin/env python3
"""Signed single-user client for Ordivon Edge."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any

DEFAULT_CONFIG = pathlib.Path("/root/.config/ordivon/secrets/edge-client.json")
USER_AGENT = "ordivon-edge-client/0.1"


class ClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class Config:
    endpoint: str
    key_id: str
    secret: bytes


def load_config(path: pathlib.Path) -> Config:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ClientError(f"Edge client configuration does not exist: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise ClientError(f"Cannot read Edge client configuration: {path}") from exc

    endpoint = raw.get("endpoint")
    key_id = raw.get("key_id")
    secret_text = raw.get("secret")
    if not all(isinstance(value, str) and value for value in (endpoint, key_id, secret_text)):
        raise ClientError("Edge client configuration is incomplete")
    try:
        secret = base64.urlsafe_b64decode(secret_text + "=" * (-len(secret_text) % 4))
    except ValueError as exc:
        raise ClientError("Edge client secret is not valid base64url") from exc
    if len(secret) < 32:
        raise ClientError("Edge client secret is too short")
    return Config(endpoint=endpoint.rstrip("/"), key_id=key_id, secret=secret)


def make_request_id() -> str:
    return f"req_{uuid.uuid4().hex}"


def canonical_target(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))


def signed_headers(
    config: Config,
    method: str,
    url: str,
    body: bytes,
    request_id: str,
    timestamp: int | None = None,
) -> dict[str, str]:
    timestamp = int(time.time()) if timestamp is None else timestamp
    body_digest = hashlib.sha256(body).hexdigest()
    canonical = "\n".join(
        [
            "ordivon-edge-v1",
            method.upper(),
            canonical_target(url),
            request_id,
            str(timestamp),
            body_digest,
        ]
    )
    signature = base64.urlsafe_b64encode(
        hmac.new(config.secret, canonical.encode("utf-8"), hashlib.sha256).digest()
    ).rstrip(b"=").decode("ascii")
    return {
        "Authorization": f"Ordivon-HMAC {config.key_id}:{signature}",
        "X-Ordivon-Request-Id": request_id,
        "X-Ordivon-Timestamp": str(timestamp),
        "User-Agent": USER_AGENT,
    }


def request(
    config: Config,
    method: str,
    path: str,
    *,
    body: bytes = b"",
    request_id: str | None = None,
    accept: str = "application/json",
) -> tuple[int, dict[str, str], bytes]:
    request_id = request_id or make_request_id()
    url = f"{config.endpoint}{path}"
    headers = signed_headers(config, method, url, body, request_id)
    headers["Accept"] = accept
    if body:
        headers["Content-Type"] = "application/json"
    invocation = urllib.request.Request(
        url,
        data=body if method.upper() not in {"GET", "HEAD"} else None,
        method=method.upper(),
        headers=headers,
    )
    try:
        with urllib.request.urlopen(invocation, timeout=30) as response:
            return response.status, dict(response.headers.items()), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items()), exc.read()
    except urllib.error.URLError as exc:
        raise ClientError(f"Edge request failed: {exc.reason}") from exc


def print_json_bytes(body: bytes) -> None:
    try:
        value = json.loads(body)
    except json.JSONDecodeError:
        raise ClientError("Edge returned a non-JSON response")
    print(json.dumps(value, indent=2, ensure_ascii=False))


def command_json(config: Config, path: str) -> int:
    status, _, body = request(config, "GET", path)
    print_json_bytes(body)
    return 0 if 200 <= status < 300 else 1


def command_fetch(config: Config, args: argparse.Namespace) -> int:
    payload: dict[str, Any] = {
        "url": args.url,
        "maximum_bytes": args.maximum_bytes,
        "timeout_ms": args.timeout_ms,
    }
    if args.accept:
        payload["accept"] = args.accept
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    status, _, response = request(
        config,
        "POST",
        "/v1/fetch",
        body=body,
        request_id=args.request_id,
    )
    print_json_bytes(response)
    return 0 if 200 <= status < 300 else 1


def command_artifact_get(config: Config, args: argparse.Namespace) -> int:
    encoded = "/".join(urllib.parse.quote(segment, safe="") for segment in args.key.split("/"))
    status, headers, body = request(
        config,
        "GET",
        f"/v1/artifacts/{encoded}",
        accept="application/octet-stream",
    )
    if not 200 <= status < 300:
        print_json_bytes(body)
        return 1
    destination = pathlib.Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(body)
    receipt = {
        "saved": str(destination),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "edge_sha256": headers.get("X-Ordivon-Sha256")
        or headers.get("x-ordivon-sha256"),
        "content_type": headers.get("Content-Type")
        or headers.get("content-type"),
    }
    print(json.dumps(receipt, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="ordivon-edge")
    root.add_argument(
        "--config",
        default=os.environ.get("ORDIVON_EDGE_CONFIG", str(DEFAULT_CONFIG)),
    )
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("health")
    commands.add_parser("capabilities")

    fetch = commands.add_parser("fetch")
    fetch.add_argument("url")
    fetch.add_argument("--maximum-bytes", type=int, default=262_144)
    fetch.add_argument("--timeout-ms", type=int, default=10_000)
    fetch.add_argument("--accept")
    fetch.add_argument("--request-id", default=make_request_id())

    receipt = commands.add_parser("receipt")
    receipt.add_argument("receipt_id")

    artifact = commands.add_parser("artifact-get")
    artifact.add_argument("key")
    artifact.add_argument("--output", required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        config = load_config(pathlib.Path(args.config).expanduser())
        if args.command == "health":
            return command_json(config, "/health")
        if args.command == "capabilities":
            return command_json(config, "/v1/capabilities")
        if args.command == "fetch":
            return command_fetch(config, args)
        if args.command == "receipt":
            return command_json(config, f"/v1/receipts/{args.receipt_id}")
        if args.command == "artifact-get":
            return command_artifact_get(config, args)
        raise ClientError(f"Unknown command: {args.command}")
    except ClientError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
