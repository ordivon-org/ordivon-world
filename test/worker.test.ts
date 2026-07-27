import assert from "node:assert/strict";
import test from "node:test";

import { handleRequest } from "../src/index.js";

test("health is minimal and non-cacheable", async () => {
  const response = await handleRequest(new Request("https://edge.invalid/health"));
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("cache-control"), "no-store");
  assert.deepEqual(await response.json(), {
    schema_version: 1,
    service: "ordivon-edge",
    status: "ok"
  });
});

test("capabilities are read-only and do not expose account or bucket identity", async () => {
  const response = await handleRequest(
    new Request("https://edge.invalid/v1/capabilities")
  );
  assert.equal(response.status, 200);
  const body = await response.text();
  assert.doesNotMatch(body, /account_id|bucket_name|ordivon-artifacts/i);
});

test("known routes reject mutation methods", async () => {
  const response = await handleRequest(
    new Request("https://edge.invalid/health", { method: "POST" })
  );
  assert.equal(response.status, 405);
  assert.equal(response.headers.get("allow"), "GET");
});

test("unknown routes fail closed", async () => {
  const response = await handleRequest(
    new Request("https://edge.invalid/v1/fetch")
  );
  assert.equal(response.status, 404);
});
