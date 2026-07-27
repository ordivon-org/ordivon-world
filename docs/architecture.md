# Architecture

## Platform shell

`src/index.ts` is the narrow Cloudflare Worker adapter. It reads a bounded body, authenticates the canonical request, routes the operation, and converts domain failures into stable HTTP responses.

## Authentication layer

`src/auth.ts` implements HMAC-SHA256 service authentication. The Worker secret is imported into WebCrypto and never emitted. Request IDs and timestamps are validated before any capability executes.

## Stable contracts

`src/contracts.ts` defines capabilities, operations, artifacts, fetch details, and receipts without embedding Cloudflare account identifiers or bucket names.

## Idempotency and receipts

`src/idempotency.ts` owns R2 request locks and stored receipts:

```text
signed request
  → receipt lookup
  → request-lock lookup / conditional create
  → execute once
  → persist success, failure, or rejection receipt
  → deterministic replay
```

## Fetch adapter

`src/fetch-policy.ts` validates URL, host allowlist, size, timeout, and Accept budgets. `src/external-fetch.ts` owns manual redirects, bounded response streaming, hashing, and private R2 persistence.

```text
POST /v1/fetch
  → HMAC authentication
  → Request-ID lock
  → JSON and policy validation
  → bounded HTTPS fetch
  → R2 artifact
  → R2 receipt
  → receipt envelope
```

## Artifact layer

The production Worker has one private R2 binding named `ARTIFACTS`. Artifact keys are normalized, bounded, and namespaced. No public `r2.dev` access exists. Authenticated artifact reads expose only the stored body, safe content type, length, ETag, and SHA-256.

## Next adapter

```text
Browser Run adapter
  → action allowlist
  → navigation and browser-time budget
  → screenshot / extracted result
  → R2 artifact
  → receipt
```

Browser Run cannot call back into local network selection. Link decides connectivity; Edge executes external capabilities.
