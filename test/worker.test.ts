import assert from "node:assert/strict";
import test from "node:test";

import type { EdgeReceiptEnvelope } from "../src/contracts.js";
import { handleRequest } from "../src/index.js";
import { MemoryR2, makeEnv, signedRequest } from "./helpers.js";

test("unsigned requests are rejected before route handling", async () => {
  const response = await handleRequest(
    new Request("https://edge.invalid/health"),
    makeEnv()
  );
  assert.equal(response.status, 401);
  assert.match(response.headers.get("www-authenticate") ?? "", /Ordivon-HMAC/);
});

test("signed health and capabilities are minimal and non-cacheable", async () => {
  const environment = makeEnv();
  const health = await handleRequest(
    signedRequest("https://edge.invalid/health"),
    environment
  );
  assert.equal(health.status, 200);
  assert.equal(health.headers.get("cache-control"), "no-store");
  assert.deepEqual(await health.json(), {
    schema_version: 1,
    service: "ordivon-edge",
    status: "ok"
  });

  const capabilities = await handleRequest(
    signedRequest("https://edge.invalid/v1/capabilities", {
      requestId: "request_caps_001"
    }),
    environment
  );
  const body = await capabilities.text();
  assert.equal(capabilities.status, 200);
  assert.doesNotMatch(body, /account_id|bucket_name|ordivon-artifacts/i);
});

test("bounded fetch persists an artifact and receipt, then replays without refetching", async () => {
  const memory = new MemoryR2();
  const environment = makeEnv(memory);
  const requestId = "request_fetch_001";
  const signedAt = Math.floor(Date.now() / 1000);
  const requestBody = JSON.stringify({
    url: "https://allowed.example.org/data",
    maximum_bytes: 1024,
    timeout_ms: 2000
  });
  let fetchCount = 0;
  const fetcher = async () => {
    fetchCount += 1;
    return new Response("edge-result", {
      status: 200,
      headers: { "content-type": "text/plain; charset=utf-8" }
    });
  };

  const first = await handleRequest(
    signedRequest("https://edge.invalid/v1/fetch", {
      method: "POST",
      body: requestBody,
      requestId,
      timestamp: signedAt
    }),
    environment,
    { fetcher }
  );
  assert.equal(first.status, 200);
  const firstEnvelope = (await first.json()) as EdgeReceiptEnvelope;
  assert.equal(firstEnvelope.replayed, false);
  assert.equal(firstEnvelope.receipt.status, "succeeded");
  assert.equal(firstEnvelope.receipt.artifact?.key, `fetch/v1/${requestId}.body`);
  assert.equal(fetchCount, 1);
  assert.ok(memory.objects.has(`receipts/v1/${requestId}.json`));
  assert.ok(memory.objects.has(`fetch/v1/${requestId}.body`));

  const second = await handleRequest(
    signedRequest("https://edge.invalid/v1/fetch", {
      method: "POST",
      body: requestBody,
      requestId,
      timestamp: signedAt + 1
    }),
    environment,
    { fetcher }
  );
  const secondEnvelope = (await second.json()) as EdgeReceiptEnvelope;
  assert.equal(secondEnvelope.replayed, true);
  assert.equal(second.headers.get("x-ordivon-replayed"), "true");
  assert.equal(fetchCount, 1);
});

test("one request ID cannot be rebound to different content", async () => {
  const environment = makeEnv();
  const requestId = "request_conflict_001";
  const fetcher = async () => new Response("ok");
  const firstBody = JSON.stringify({ url: "https://allowed.example.org/one" });
  const secondBody = JSON.stringify({ url: "https://allowed.example.org/two" });

  const first = await handleRequest(
    signedRequest("https://edge.invalid/v1/fetch", {
      method: "POST",
      body: firstBody,
      requestId
    }),
    environment,
    { fetcher }
  );
  assert.equal(first.status, 200);

  const conflict = await handleRequest(
    signedRequest("https://edge.invalid/v1/fetch", {
      method: "POST",
      body: secondBody,
      requestId
    }),
    environment,
    { fetcher }
  );
  assert.equal(conflict.status, 409);
  assert.equal((await conflict.json() as { error: string }).error, "idempotency_conflict");
});

test("redirect destinations are revalidated before a second fetch", async () => {
  const environment = makeEnv();
  const requestId = "request_redirect_001";
  const calls: string[] = [];
  const fetcher = async (input: RequestInfo | URL) => {
    const url = input.toString();
    calls.push(url);
    if (calls.length === 1) {
      return new Response(null, {
        status: 302,
        headers: { location: "https://redirect.example.org/final" }
      });
    }
    return new Response("redirected");
  };
  const response = await handleRequest(
    signedRequest("https://edge.invalid/v1/fetch", {
      method: "POST",
      body: JSON.stringify({ url: "https://allowed.example.org/start" }),
      requestId
    }),
    environment,
    { fetcher }
  );
  assert.equal(response.status, 200);
  assert.deepEqual(calls, [
    "https://allowed.example.org/start",
    "https://redirect.example.org/final"
  ]);
});

test("rejected fetches receive persistent receipts", async () => {
  const memory = new MemoryR2();
  const environment = makeEnv(memory);
  const requestId = "request_reject_001";
  const body = JSON.stringify({ url: "https://forbidden.example.org/data" });
  const response = await handleRequest(
    signedRequest("https://edge.invalid/v1/fetch", {
      method: "POST",
      body,
      requestId
    }),
    environment
  );
  assert.equal(response.status, 403);
  const envelope = (await response.json()) as EdgeReceiptEnvelope;
  assert.equal(envelope.receipt.status, "rejected");
  assert.equal(envelope.receipt.error_code, "host_not_allowed");
  assert.ok(memory.objects.has(`receipts/v1/${requestId}.json`));
});

test("authenticated clients can retrieve persisted artifacts", async () => {
  const memory = new MemoryR2();
  const environment = makeEnv(memory);
  await environment.ARTIFACTS.put("fetch/v1/request_artifact_001.body", "artifact-body", {
    httpMetadata: { contentType: "text/plain" },
    customMetadata: { sha256: "b".repeat(64) }
  });
  const response = await handleRequest(
    signedRequest(
      "https://edge.invalid/v1/artifacts/fetch/v1/request_artifact_001.body",
      { requestId: "request_get_001" }
    ),
    environment
  );
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "artifact-body");
  assert.equal(response.headers.get("content-type"), "application/octet-stream");
  assert.equal(response.headers.get("content-disposition"), "attachment; filename=artifact.bin");
  assert.equal(response.headers.get("cache-control"), "no-store, no-transform");
  assert.equal(response.headers.get("x-ordivon-media-type"), "text/plain");
  assert.equal(response.headers.get("x-ordivon-sha256"), "b".repeat(64));
});
