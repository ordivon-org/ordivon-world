import assert from "node:assert/strict";
import test from "node:test";

import { validateArtifactKey } from "../src/artifacts.js";
import { CAPABILITIES } from "../src/contracts.js";
import { validateExternalUrl, validateFetchRequest } from "../src/fetch-policy.js";
import { createReceipt } from "../src/receipts.js";

const DIGEST = "a".repeat(64);

test("capabilities expose only the Edge execution surface", () => {
  const states = new Map(
    CAPABILITIES.capabilities.map((capability) => [capability.id, capability.state])
  );
  assert.equal(states.get("fetch"), "ready");
  assert.equal(states.get("artifact.get"), "ready");
  assert.equal(states.get("browser.run"), "planned");
});

test("receipt timestamps and request digests are explicit", () => {
  const receipt = createReceipt({
    operation: "artifact.put",
    status: "succeeded",
    requestDigest: DIGEST,
    startedAt: new Date("2026-07-27T00:00:00.000Z"),
    completedAt: new Date("2026-07-27T00:00:01.000Z"),
    receiptId: "receipt-test"
  });
  assert.equal(receipt.receipt_id, "receipt-test");
  assert.equal(receipt.request_digest, DIGEST);
  assert.equal(receipt.duration_ms, 1_000);
});

test("receipt rejects invalid outcome combinations", () => {
  assert.throws(() =>
    createReceipt({
      operation: "fetch",
      status: "failed",
      requestDigest: DIGEST,
      receiptId: "receipt-test",
      startedAt: new Date("2026-07-27T00:00:01.000Z"),
      completedAt: new Date("2026-07-27T00:00:00.000Z"),
      errorCode: "timeout"
    })
  );
  assert.throws(() =>
    createReceipt({
      operation: "fetch",
      status: "succeeded",
      requestDigest: DIGEST,
      receiptId: "receipt-test",
      startedAt: new Date("2026-07-27T00:00:00.000Z"),
      completedAt: new Date("2026-07-27T00:00:01.000Z"),
      errorCode: "unexpected"
    })
  );
});

test("artifact keys are normalized and namespaced", () => {
  assert.equal(
    validateArtifactKey("artifacts/2026/receipt-test.json"),
    "artifacts/2026/receipt-test.json"
  );
  for (const key of [
    "/artifacts/a",
    "unknown/a",
    "artifacts/../secret",
    "artifacts\\secret",
    "artifacts/"
  ]) {
    assert.throws(() => validateArtifactKey(key));
  }
});

test("fetch policy is HTTPS-only, allowlisted, and bounded", () => {
  const environment = { FETCH_ALLOWED_HOSTS: "allowed.example.org,*.trusted.example.org" };
  assert.equal(
    validateExternalUrl("https://allowed.example.org/path#fragment", environment).toString(),
    "https://allowed.example.org/path"
  );
  assert.equal(
    validateExternalUrl("https://api.trusted.example.org/path", environment).hostname,
    "api.trusted.example.org"
  );
  for (const url of [
    "http://allowed.example.org/",
    "https://127.0.0.1/",
    "https://localhost/",
    "https://not-allowed.example.org/",
    "https://allowed.example.org:8443/"
  ]) {
    assert.throws(() => validateExternalUrl(url, environment));
  }

  const request = validateFetchRequest(
    { url: "https://allowed.example.org/data", maximum_bytes: 1024, timeout_ms: 2000 },
    environment
  );
  assert.equal(request.maximumBytes, 1024);
  assert.equal(request.timeoutMs, 2000);
});
