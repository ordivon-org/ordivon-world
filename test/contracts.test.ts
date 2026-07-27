import assert from "node:assert/strict";
import test from "node:test";

import { validateArtifactKey } from "../src/artifacts.js";
import { CAPABILITIES } from "../src/contracts.js";
import { createReceipt } from "../src/receipts.js";

test("capabilities expose only the Edge execution surface", () => {
  const ids = CAPABILITIES.capabilities.map((capability) => capability.id);
  assert.deepEqual(ids, [
    "artifact.put",
    "artifact.get",
    "artifact.delete",
    "fetch",
    "browser.run",
    "receipt"
  ]);
});

test("receipt timestamps are ordered and deterministic when an id is supplied", () => {
  const receipt = createReceipt({
    operation: "artifact.put",
    status: "succeeded",
    startedAt: new Date("2026-07-27T00:00:00.000Z"),
    completedAt: new Date("2026-07-27T00:00:01.000Z"),
    receiptId: "receipt-test"
  });
  assert.equal(receipt.receipt_id, "receipt-test");
  assert.equal(receipt.schema_version, 1);
  assert.equal(receipt.status, "succeeded");
});

test("receipt rejects reversed timestamps and unsafe error codes", () => {
  assert.throws(() =>
    createReceipt({
      operation: "fetch",
      status: "failed",
      startedAt: new Date("2026-07-27T00:00:01.000Z"),
      completedAt: new Date("2026-07-27T00:00:00.000Z"),
      errorCode: "timeout"
    })
  );
  assert.throws(() =>
    createReceipt({
      operation: "fetch",
      status: "failed",
      startedAt: new Date("2026-07-27T00:00:00.000Z"),
      completedAt: new Date("2026-07-27T00:00:01.000Z"),
      errorCode: "Unsafe Error"
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
