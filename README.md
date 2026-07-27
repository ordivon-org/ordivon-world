# Ordivon Edge

Ordivon Edge is the externally hosted execution layer of the Ordivon stack.

```text
Ordivon Runtime / Agent
        │ signed bounded request
        ▼
Ordivon Edge
  ├─ allowlisted external fetch
  ├─ private R2 artifacts
  ├─ idempotent task receipts
  ├─ bounded Browser Run snapshots
  └─ optional remote node lifecycle
```

## Strict boundary

Ordivon Edge owns Cloudflare Worker execution, external fetch and Browser Run policy, private R2 artifacts, execution budgets, receipts, and future remote Edge-node lifecycle.

It does **not** own local route, VPN, DNS, WARP, path measurement, transport selection, QUIC relay clients, or failover; those belong to `ordivon-link`. Local Agent tasks, workspaces, process supervision, and recovery belong to `ordivon-runtime`.

## Implemented P0 execution plane

- HMAC-SHA256 service authentication with a five-minute timestamp window;
- signed method, path, query, Request ID, timestamp, and body digest;
- R2-backed atomic request locks;
- deterministic receipt replay and Request-ID conflict detection;
- HTTPS-only exact/wildcard hostname allowlists;
- validated redirects, fixed GET semantics, and no caller credentials forwarded;
- bounded request, response, redirect, and time budgets;
- private response artifacts and success/failure/rejection receipts;
- authenticated health, capability, receipt, and artifact reads;
- same-origin Browser Run snapshots with PNG, rendered HTML, and manifest artifacts;
- Workers.dev, preview URLs, and R2 public access disabled;
- machine-enforced repository boundary checks.

## Verification

```bash
pnpm install --frozen-lockfile
pnpm run ci
python -m py_compile scripts/ordivon_edge_client.py
```

## Local client

```bash
scripts/install-edge-client
ordivon-edge health
ordivon-edge fetch https://developers.cloudflare.com/
ordivon-edge browser-run https://example.com/ --full-page
```

See [`docs/operations.md`](docs/operations.md), [`docs/architecture.md`](docs/architecture.md), [`docs/boundary.md`](docs/boundary.md), and [`docs/security.md`](docs/security.md).
