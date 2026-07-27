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
ordivon-edge capabilities
ordivon-edge fetch https://developers.cloudflare.com/ --maximum-bytes 262144
ordivon-edge receipt <receipt-id>
ordivon-edge artifact-get fetch/v1/<receipt-id>.body --output /tmp/result.bin
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

Every accepted request acquires an R2 idempotency lock. Successes, failures, and policy rejections produce private Receipt objects.
