# Architecture

## Target architecture

```text
Edge Node contract
  → provider adapter and lifecycle controller
  → profile-scoped capability and resource lease
  → remote execution and observation
  → identity-bound Artifact and Receipt export
  → freeze / snapshot / restore / destruction evidence
```

The implemented Cloudflare layers below are the production profile of that broader architecture.

## Provider-neutral Node layer

`src/node-contracts.ts` defines deterministic Node identity, provider/source,
profile-scoped capability and policy, resources, Campaign/World membership,
leases, observations, evidence, and reconstruction without importing a platform
SDK. `src/node-lifecycle.ts` defines idempotent lifecycle uncertainty,
reconciliation, and durable snapshots.

`src/local-node-adapter.ts` implements the research-local provider with a
minimal Linux user-namespace body, a sealed read-only rootfs, a durable local
management journal, monotonic lease fencing, and atomic evidence export. Its
management, experiment, observation, and evidence-export roots are inaccessible
from the evaluated chroot, while remaining under one trusted local provider
account. It is not imported by `src/index.ts`; `config/edge-node-policy.json` is
also separate from the production Worker policy and fingerprint. See
[`node-contract.md`](node-contract.md).

## Platform shell

`src/index.ts` is the narrow Cloudflare Worker adapter. It reads a bounded body, authenticates the canonical request, routes the operation, and converts domain failures into stable HTTP responses.

## Authentication layer

`src/auth.ts` implements HMAC-SHA256 service authentication. The Worker secret is imported into WebCrypto and never emitted. Request IDs and timestamps are validated before any capability executes.

## Stable contracts

`src/contracts.ts` defines capabilities, operations, artifacts, fetch details, and receipts without embedding Cloudflare account identifiers or bucket names.

## Idempotency and receipts

`src/idempotency.ts` owns the authoritative R2 request state and Receipt replay:

```text
signed request
  → requests/v2 lookup / conditional Pending create
  → execute under a generation lease
  → ETag-fenced final Receipt commit
  → best-effort receipts/v2 mirror
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

## Browser Run adapter

`src/browser-policy.ts` accepts only bounded navigation fields and generates a same-origin Browser Run policy. `src/browser-run.ts` invokes the Cloudflare Browser binding's `snapshot` Quick Action, validates and bounds its response, then writes three R2 objects.

```text
POST /v1/browser/run
  → HMAC authentication
  → Request-ID lock
  → URL, viewport, wait, and timeout policy
  → same-origin Browser Run snapshot
  → PNG + rendered HTML + manifest
  → R2 receipt
```

Arbitrary actions remain outside P1. Browser Run cannot call back into local network selection. Link decides connectivity; Edge executes external capabilities.


## P1.5 execution coordinator

`src/idempotency.ts` now implements a single-object request state machine rather than a separately written lock and Receipt. `src/execution.ts` derives bounded lease durations and execution metadata. `src/version.ts` is the explicit policy and capability version registry.

```text
HMAC request
  → requests/v2 pending state
  → rate-limit budget
  → capability adapter
  → generation-scoped Artifacts
  → ETag-fenced committed state
  → best-effort receipt mirror
```

`src/observability.ts` emits bounded structured events that carry execution identity but omit target URLs, request bodies, credentials, lease tokens, and R2 ETags.


## Policy source

`config/edge-policy.json` is consumed by Worker policy adapters, release validation, CI drift checks, and R2 lifecycle configuration. `src/policy.ts` derives the effective policy fingerprint using the actual hostname allowlist binding. This removes the previous manual coupling between policy constants, Wrangler variables, lifecycle rules, and stale-lease fencing.
