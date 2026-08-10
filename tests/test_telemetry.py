from __future__ import annotations

import unittest

from ordivon_world.telemetry import TraceContext


class TraceContextTests(unittest.TestCase):
    def test_valid_context_projects_standard_headers(self) -> None:
        context = TraceContext(
            "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01",
            "ordivon=world",
        )
        self.assertEqual(context.headers()["traceparent"], context.traceparent)
        self.assertEqual(context.headers()["tracestate"], "ordivon=world")

    def test_zero_trace_identity_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TraceContext(
                "00-00000000000000000000000000000000-0123456789abcdef-01"
            )


if __name__ == "__main__":
    unittest.main()
