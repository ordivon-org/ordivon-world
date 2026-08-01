from __future__ import annotations
import hashlib, importlib.util, json, pathlib, sys, unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("evidence", SCRIPTS / "ordivon_world_evidence.py")
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class FakeRequester:
    def __init__(self):
        self.body = b"example"
        self.sha = hashlib.sha256(self.body).hexdigest()
        self.version = {"id": "worker-1", "tag": "test", "timestamp": "2026-08-02T00:00:00Z"}

    def __call__(self, config, method, path, **kwargs):
        if path == "/health":
            value = {"status": "ok", "policy_version": "p1", "worker_version": self.version}
        elif path == "/v1/capabilities":
            value = {"policy_version": "p1", "worker_version": self.version, "capabilities": [{"id": "fetch", "state": "ready"}]}
        elif path == "/v1/fetch":
            value = {"receipt": {"status": "succeeded", "request_digest": "digest-1", "artifacts": [{"key": "fetch/v2/request/g1/body", "sha256": self.sha, "bytes": len(self.body), "media_type": "text/plain"}]}}
        elif path.startswith("/v1/artifacts/"):
            return 200, {"X-Ordivon-Sha256": self.sha}, self.body
        else:
            raise AssertionError(path)
        return 200, {}, json.dumps(value).encode()


class EvidenceConsumerTest(unittest.TestCase):
    def setUp(self):
        self.config = M.Config("https://edge.example", "runtime-v1", b"x" * 32)

    def test_operation_preserves_receipt_and_verifies_artifact(self):
        fake = FakeRequester()
        original = M.request
        M.request = fake
        try:
            request_id, receipt, artifacts = M.operation(self.config, "/v1/fetch", {"url": "https://example.com"})
        finally:
            M.request = original
        self.assertTrue(request_id.startswith("req_"))
        self.assertEqual(receipt["request_digest"], "digest-1")
        self.assertTrue(artifacts[0]["verified"])

    def test_capability_reference_is_content_bound(self):
        document = {"policy_version": "p1", "worker_version": {"id": "v1"}}
        reference = M.capability_ref(document)
        self.assertEqual(reference["sha256"], hashlib.sha256(M.canonical(document)).hexdigest())

    def test_artifact_mismatch_fails_closed(self):
        fake = FakeRequester()
        fake.sha = "0" * 64
        original = M.request
        M.request = fake
        try:
            with self.assertRaises(M.ClientError):
                M.verify_artifacts(self.config, {"artifacts": [{"key": "fetch/v2/request/g1/body", "sha256": "1" * 64, "bytes": 7}]})
        finally:
            M.request = original


if __name__ == "__main__":
    unittest.main()
