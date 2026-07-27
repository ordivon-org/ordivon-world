# Operations

## Production endpoint

The first production surface is the HMAC-authenticated custom domain:

```text
https://edge.ordivon.com
```

Workers.dev and preview URLs remain disabled.

## Client configuration

The local client reads a root-only file:

```text
/root/.config/ordivon/secrets/edge-client.json
```

Schema:

```json
{
  "endpoint": "https://edge.ordivon.com",
  "key_id": "runtime-v1",
  "secret": "base64url-encoded-32-byte-secret"
}
```

The same secret is installed as the Worker secret `EDGE_HMAC_SECRET`. It must never enter Git, logs, receipts, or command output.

## Signed request contract

Each request carries:

```text
Authorization: Ordivon-HMAC <key-id>:<base64url-hmac-sha256>
X-Ordivon-Request-Id: <bounded-id>
X-Ordivon-Timestamp: <unix-seconds>
```

The canonical payload is:

```text
ordivon-edge-v1
<METHOD>
<PATH-AND-QUERY>
<REQUEST-ID>
<TIMESTAMP>
<SHA256-BODY>
```

Requests outside a five-minute clock window are rejected. Reusing a Request ID with the same signed content replays the stored receipt; reusing it with different content returns `409 idempotency_conflict`.

## Client commands

```bash
ordivon-edge health
ordivon-edge status --repo /root/projects/ordivon-edge --expected-ref HEAD
ordivon-edge capabilities
ordivon-edge fetch https://developers.cloudflare.com/ --maximum-bytes 262144
ordivon-edge receipt <receipt-id>
ordivon-edge artifact-get fetch/v2/<receipt-id>/g<generation>/body \
  --sha256 <sha256-from-receipt> \
  --output /tmp/result.bin
```

## Fetch boundary

P0 fetch allows only:

- HTTPS;
- port 443;
- hostnames in `FETCH_ALLOWED_HOSTS`;
- three validated redirects;
- request bodies up to 8 KiB;
- response bodies up to 1 MiB;
- execution time up to 15 seconds;
- fixed GET semantics with no caller-provided cookies or authorization headers.

Every accepted request conditionally creates an authoritative R2 `requests/v2` Pending state. Successes, failures, and policy rejections commit a final Receipt into that same state object and write a best-effort Receipt mirror.


## Browser Run P1

The P1 endpoint is:

```text
POST /v1/browser/run
```

The client invocation is:

```bash
ordivon-edge browser-run https://example.com/ \
  --viewport-width 1365 \
  --viewport-height 768 \
  --wait-until domcontentloaded \
  --timeout-ms 15000
```

A successful run creates three private artifacts:

```text
browser/v2/<request-id>/g<generation>/screenshot.png
browser/v2/<request-id>/g<generation>/content.html
browser/v2/<request-id>/g<generation>/manifest.json
```

The manifest is the receipt's primary `artifact`; all three references appear in `artifacts`. Download each object with `ordivon-edge artifact-get`.

P1 intentionally supports only one action: navigate to an allowlisted HTTPS URL and capture a snapshot. It does not accept scripts, cookies, credentials, arbitrary headers, clicks, form input, selectors, or file downloads. Browser subresources are restricted to the requested hostname.


## P1.5 operation state

New operations persist an authoritative state under `requests/v2/`. Receipt queries can return HTTP `202` while the execution lease is pending. Use:

```bash
ordivon-edge receipt <request-id> --wait
```

New Artifact paths include the lease generation. Consumers must use the keys returned by the Receipt rather than constructing paths.

## Execution budgets

Cloudflare Rate Limit bindings apply per HMAC key ID:

```text
Browser Run: 1 new execution / 10 seconds
Fetch:       30 new executions / 60 seconds
```

Receipt replay occurs before budget consumption. A rate-limited first execution produces a failed Receipt and a `Retry-After` response header.

## R2 lifecycle

Apply the managed lifecycle rules through the Cloudflare R2 Lifecycle API with:

```bash
scripts/configure-r2-lifecycle
```

Retention is defined once in `config/edge-policy.json`. Request states, Receipt mirrors, cleanup tombstones, and Request-ID idempotency are retained for 90 days. Fetch and Browser Artifacts are retained for 91 days so a replayable Receipt does not outlive its result. Legacy v1 evidence is not modified.

When immediate Artifact cleanup is deferred, inspect or execute the bounded GC controller:

```bash
python3 scripts/ordivon_edge_gc.py --dry-run
python3 scripts/ordivon_edge_gc.py
```

GC accepts only generation-matching `fetch/v2` and `browser/v2` keys from `cleanup/v2` tombstones.


## Local operational installation

Install the client, release controller, GC controller, and daily GC timer:

```bash
scripts/install-edge-operations
```

The timer runs after WSL boot and approximately once every 24 hours with randomized delay:

```bash
systemctl status ordivon-edge-gc.timer
systemctl list-timers ordivon-edge-gc.timer
```

The service is root-only, uses a `0077` umask, and processes at most 100 cleanup tombstones per run.


## Client transport and Artifact integrity

The client retries transient transport failures up to three times. A POST retry preserves the original Request ID and request body, so the Edge state machine returns a first execution, Pending state, or deterministic Receipt replay rather than creating a second operation. HTTP policy failures are not retried automatically.

Artifact downloads fail closed unless `X-Ordivon-Sha256` is present and matches the downloaded bytes. `--sha256` additionally verifies the digest carried by the operation Receipt. The client writes through a same-directory temporary file, fsyncs it, atomically renames it, and applies mode `0600`.

## Effective policy version

`config/edge-policy.json` is the single source for execution bounds, lease durations, expected rate limits, and retention. The Worker combines that document with the effective `FETCH_ALLOWED_HOSTS` binding and reports a fingerprint such as `p1.6.<digest>`. An expired Pending request cannot be taken over when that fingerprint changed. `pnpm check:policy` rejects drift between the policy document and Wrangler configuration.


The lifecycle controller preserves non-Ordivon rules, replaces all rules whose IDs begin with `edge-v2-`, then rereads the API and requires an exact match. It does not depend on Wrangler or the local Node dependency tree.
