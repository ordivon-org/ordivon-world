# Security boundary

## Authentication

Every route is protected by HMAC-SHA256 request signing. The signature binds:

- protocol version;
- HTTP method;
- path and query;
- bounded Request ID;
- Unix timestamp;
- SHA-256 of the complete request body.

Requests outside a five-minute window, signed with a different key ID, or carrying an invalid body signature are rejected. The shared key is a 32-byte random Worker secret and never appears in Git or Worker variables.

## Replay and idempotency

R2 stores one authoritative `requests/v2` state object per Request ID. Creation uses an `If-None-Match: *` equivalent condition; takeover and final commit use the current object ETag. A Request ID can have only one request digest:

- same ID and committed digest: return the stored Receipt without re-execution;
- same ID and different digest: `409 idempotency_conflict`;
- active Pending state: `409 request_in_progress`;
- expired Pending state with the same policy: generation-incrementing conditional takeover;
- expired Pending state under a different policy: require a new Request ID.

R2 strong consistency makes each state transition globally visible after the write completes. The idempotency contract is retained for 90 days.

## External fetch

Fetch is intentionally constrained:

- HTTPS and port 443 only;
- no URL credentials;
- no IP literals, localhost, private naming suffixes, or onion names;
- exact hostname allowlist; wildcard entries are rejected;
- redirects handled manually and revalidated at every hop;
- at most three redirects;
- no caller cookies, authorization headers, or arbitrary outbound headers;
- request body at most 8 KiB;
- response body at most 1 MiB;
- timeout between one and fifteen seconds;
- response bodies never returned inline from the execution endpoint.

The fetched body is stored in private R2 and referenced by SHA-256, byte length, media type, and ETag. Artifact reads are always served as `application/octet-stream` with `Content-Disposition: attachment` and `Cache-Control: no-store, no-transform`; the original media type is exposed only as `X-Ordivon-Media-Type`. This preserves exact bytes and prevents HTML execution or Cloudflare JavaScript Detection injection.


## Browser Run P1

Browser Run is constrained to a single snapshot operation:

- the top-level URL passes the same HTTPS and hostname allowlist as Fetch;
- browser network requests are restricted to the requested hostname;
- viewport is bounded to 320–1920 by 240–1080;
- navigation timeout is bounded to 1–30 seconds;
- post-load wait is bounded to 0–3 seconds;
- screenshot output is bounded to 4 MiB;
- rendered HTML is bounded to 1 MiB;
- Browser Run response envelopes are bounded to 8 MiB;
- browser cache is disabled;
- media, fonts, prefetch, WebSockets, event sources, manifests, pings, and reporting requests are blocked;
- caller-provided scripts, styles, cookies, HTTP credentials, headers, selectors, clicks, and form input are not accepted.

The Worker stores the screenshot, rendered HTML, and a manifest as private R2 artifacts. The Receipt records browser milliseconds reported by Cloudflare, page status, title, viewport, and full-page mode.

## Public surface

- `GET /health` — authenticated;
- `GET /v1/capabilities` — authenticated;
- `POST /v1/fetch` — authenticated and receipt-backed;
- `POST /v1/browser/run` — authenticated, allowlisted, same-origin, and receipt-backed;
- `GET /v1/receipts/:id` — authenticated;
- `GET /v1/artifacts/:key` — authenticated;
- all other paths return 404;
- unsupported methods return 405;
- responses deny caching, framing, referrers, MIME sniffing, and cross-origin resource embedding;
- Workers.dev and preview URLs are disabled;
- R2 public access remains disabled.

Arbitrary browser interaction remains disabled until a separate action contract and per-action authorization model are implemented.


## P1.5 execution confidentiality

Final Receipts explicitly whitelist execution metadata fields. Private lease tokens and R2 state ETags never enter Receipt JSON, public responses, or structured operation logs.

Every new Receipt records the policy version, capability version, Worker version ID/tag/timestamp, and lease generation. An expired pending request cannot be taken over after a policy or capability version change; callers must use a new Request ID.

Rate Limit bindings fail closed when the budget service is unavailable. Replays return an already committed Receipt without invoking the budget or external capability again.


## Client-side Artifact verification

The local client treats the R2 SHA-256 metadata as mandatory. It compares the downloaded bytes against `X-Ordivon-Sha256` and, when supplied, against the Receipt digest before replacing the destination. Failed verification leaves any existing destination unchanged. Successful files are atomically installed with mode `0600`.
