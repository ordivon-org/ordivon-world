from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
import unittest

from ordivon_world import TransportError
from ordivon_world.cloudflare import HttpResponse

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "live_host_cloudflare_w1.py"
_SPEC = importlib.util.spec_from_file_location("ordivon_world_live_acceptance", _SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

AcceptanceError = _MODULE.AcceptanceError
DropCommittedResponseTransport = _MODULE.DropCommittedResponseTransport


class Delegate:
    def __init__(self, *, replayed: bool) -> None:
        self.replayed = replayed

    def request(
        self,
        method: str,
        path: str,
        *,
        body: bytes = b"",
        request_id: str,
        extra_headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        del method, path, body, request_id, extra_headers
        return HttpResponse(
            200,
            {},
            json.dumps(
                {
                    "receipt": {"status": "succeeded"},
                    "replayed": self.replayed,
                }
            ).encode(),
        )


class LiveAcceptanceTransportTests(unittest.TestCase):
    def test_first_execution_is_dropped_after_commit(self) -> None:
        transport = DropCommittedResponseTransport(Delegate(replayed=False))
        with self.assertRaises(TransportError):
            transport.request(
                "POST",
                "/v1/browser/run",
                request_id="request_live_first_001",
            )
        self.assertTrue(transport.dropped)
        self.assertIs(transport.committed_response_replayed, False)
        self.assertEqual(transport.post_count, 1)
        self.assertIsNotNone(transport.committed_response_digest)

    def test_replayed_receipt_is_not_accepted_as_live_execution(self) -> None:
        transport = DropCommittedResponseTransport(Delegate(replayed=True))
        with self.assertRaises(AcceptanceError):
            transport.request(
                "POST",
                "/v1/browser/run",
                request_id="request_live_replay_001",
            )
        self.assertFalse(transport.dropped)
        self.assertIsNone(transport.committed_response_replayed)
        self.assertEqual(transport.post_count, 1)

    def test_live_acceptance_never_bypasses_world_owner_boundary(self) -> None:
        tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
        direct_host_appends = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "append_preserving"
        ]
        self.assertEqual(direct_host_appends, [])


if __name__ == "__main__":
    unittest.main()
