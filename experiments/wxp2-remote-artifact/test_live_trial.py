from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wxp2_live", ROOT / "live_trial.py")
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


class LiveTrialEvidenceTests(unittest.TestCase):
    def test_seal_replaces_prior_digest_and_is_self_verifiable(self) -> None:
        value = {
            "schema_version": 1,
            "result": "ok",
            "evidence_sha256": "stale",
        }
        sealed = M.seal_evidence(value)
        unsigned = dict(sealed)
        claimed = unsigned.pop("evidence_sha256")
        expected = hashlib.sha256(
            (json.dumps(unsigned, sort_keys=True, separators=(",", ":")) + "\n").encode()
        ).hexdigest()
        self.assertEqual(claimed, expected)
        self.assertNotEqual(claimed, "stale")


if __name__ == "__main__":
    unittest.main()
