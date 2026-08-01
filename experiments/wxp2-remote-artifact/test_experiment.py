from __future__ import annotations
import importlib.util, pathlib, sys, unittest

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wxp2", ROOT / "experiment.py")
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


class RemoteArtifactTests(unittest.TestCase):
    def test_provider_to_r2_removes_source_bytes_from_host_path(self) -> None:
        digest = "a" * 64
        result = M.compare(
            source_bytes=1_000_000,
            source_sha256=digest,
            provider_artifact_sha256=digest,
            submission_bytes=500,
            provider_response_bytes=700,
            status_response_bytes=2500,
            result_manifest_bytes=1800,
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["arms"]["host-proxy"]["host_transit_bytes"], 2_000_000)
        self.assertEqual(result["arms"]["provider-to-r2"]["copies_through_host"], 0)
        self.assertGreater(result["measurements"]["host_transit_reduction_ratio"], 0.99)

    def test_digest_mismatch_fails_the_experiment(self) -> None:
        result = M.compare(
            source_bytes=100,
            source_sha256="a" * 64,
            provider_artifact_sha256="b" * 64,
            submission_bytes=10,
            provider_response_bytes=10,
            status_response_bytes=10,
            result_manifest_bytes=10,
        )
        self.assertFalse(result["valid"])
        self.assertFalse(result["integrity"]["digest_verified"])


if __name__ == "__main__":
    unittest.main()
