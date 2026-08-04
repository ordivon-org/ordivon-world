import {
  capabilitiesDocument,
  type EdgePendingReceipt
} from "../src/contracts.js";
import { createReceipt } from "../src/receipts.js";

const execution = {
  policy_version: "p1.6.fixture",
  capability_version: "fetch.v2",
  worker_version_id: "fixture-worker-version",
  worker_version_tag: "git-111111111111-src-2222222222222222-1",
  worker_version_timestamp: "2026-08-04T00:00:00.000Z",
  lease_generation: 1
};

const fetchArtifact = {
  key: "fetch/v2/world_fixture_fetch/g1/body",
  sha256: "a".repeat(64),
  bytes: 12,
  media_type: "text/plain",
  etag: '"fixture-fetch-etag"'
};

const browserArtifact = {
  key: "browser/v2/world_fixture_browser/g1/screenshot.png",
  sha256: "c".repeat(64),
  bytes: 32,
  media_type: "image/png",
  etag: '"fixture-browser-etag"'
};

const capabilities = {
  ...capabilitiesDocument("p1.6.fixture"),
  worker_version: {
    id: "fixture-worker-version",
    tag: "git-111111111111-src-2222222222222222-1",
    timestamp: "2026-08-04T00:00:00.000Z"
  },
  deployment_identity: {
    source_commit: "111111111111",
    worker_release_digest: "2222222222222222"
  }
};

const fetchReceipt = createReceipt({
  operation: "fetch",
  status: "succeeded",
  requestDigest: "b".repeat(64),
  receiptId: "world_fixture_fetch",
  startedAt: new Date("2026-08-04T00:00:00.000Z"),
  completedAt: new Date("2026-08-04T00:00:01.000Z"),
  execution,
  artifact: fetchArtifact,
  artifacts: [fetchArtifact],
  fetch: {
    requested_url: "https://developers.cloudflare.com/",
    final_url: "https://developers.cloudflare.com/",
    http_status: 200,
    redirect_count: 0
  }
});

const browserReceipt = createReceipt({
  operation: "browser.run",
  status: "succeeded",
  requestDigest: "d".repeat(64),
  receiptId: "world_fixture_browser",
  startedAt: new Date("2026-08-04T00:00:00.000Z"),
  completedAt: new Date("2026-08-04T00:00:02.000Z"),
  execution: {
    ...execution,
    capability_version: "browser.snapshot.v2"
  },
  artifact: browserArtifact,
  artifacts: [browserArtifact],
  browser: {
    requested_url: "https://developers.cloudflare.com/",
    final_url_observed: true,
    final_url: "https://developers.cloudflare.com/",
    page_title: "Cloudflare Developers",
    page_status: 200,
    browser_ms: 1500,
    viewport: { width: 1365, height: 768 },
    full_page: false
  }
});

const pendingReceipt: EdgePendingReceipt = {
  schema_version: 1,
  receipt_id: "world_fixture_pending",
  request_digest: "e".repeat(64),
  operation: "fetch",
  status: "pending",
  started_at: "2026-08-04T00:00:00.000Z",
  lease_expires_at: "2026-08-04T00:01:00.000Z",
  execution
};

const rejectedReceipt = createReceipt({
  operation: "fetch",
  status: "rejected",
  requestDigest: "f".repeat(64),
  receiptId: "world_fixture_rejected",
  startedAt: new Date("2026-08-04T00:00:00.000Z"),
  completedAt: new Date("2026-08-04T00:00:00.010Z"),
  execution,
  errorCode: "host_not_allowed"
});

process.stdout.write(
  JSON.stringify({
    capabilities,
    fetchReceipt,
    browserReceipt,
    pendingReceipt,
    rejectedReceipt
  })
);
