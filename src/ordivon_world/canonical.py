from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_digest(value: bytes | Any) -> str:
    payload = value if isinstance(value, bytes) else canonical_bytes(value)
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def sha256_hex(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
