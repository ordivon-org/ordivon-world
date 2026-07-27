# Ordivon Edge

Ordivon Edge is the externally hosted execution layer of the Ordivon stack.

It runs bounded network-side capabilities close to public infrastructure and returns explicit receipts or artifacts:

```text
Ordivon Runtime / Agent
        │ authenticated request
        ▼
Ordivon Edge
  ├─ bounded external fetch
  ├─ Browser Run
  ├─ R2 artifact storage
  ├─ task receipts
  └─ optional remote node lifecycle
```

## Strict boundary

Ordivon Edge owns:

- Cloudflare Worker request handling;
- external fetch and Browser Run policy;
- private R2 artifact storage;
- execution budgets, receipts, and externally hosted capability status;
- future lifecycle management for user-controlled remote Edge nodes.

It does **not** own:

- local route, VPN, DNS, WARP, path measurement, transport selection, QUIC relay clients, or failover — those belong to `ordivon-link`;
- local Agent tasks, workspaces, process supervision, or recovery — those belong to `ordivon-runtime`;
- public project presentation — that belongs to `ordivon-web`.

## Current phase

The repository contains the clean Cloudflare Worker foundation:

- exact health and capability routes;
- fail-closed HTTP behavior and restrictive response headers;
- R2 binding to the private `ordivon-artifacts` bucket;
- artifact-key validation;
- Receipt schema v1;
- build-time boundary checks preventing Link/network code from returning;
- no public Worker route, mutation endpoint, external fetch, or Browser Run exposure yet.

## Commands

```bash
pnpm install
pnpm run ci
```

`wrangler.jsonc` deliberately sets `workers_dev=false` and `preview_urls=false`. Deployment must not create an unauthenticated public surface by accident.

See [`docs/boundary.md`](docs/boundary.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/security.md`](docs/security.md).
