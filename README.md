# Ordivon Edge

Ordivon Edge is the externally hosted execution layer of the Ordivon stack.

```text
Ordivon Runtime / Agent
        │ signed bounded request
        ▼
Ordivon Edge
  ├─ allowlisted external fetch
  ├─ bounded Browser Run snapshots
  ├─ private versioned R2 artifacts
  ├─ fenced execution leases and transactional receipts
  └─ versioned release, smoke, promotion, and rollback
```

## Strict boundary

Ordivon Edge owns Cloudflare Worker execution, external fetch and Browser Run policy, private R2 artifacts, execution budgets, receipts, release control, and future remote Edge-node lifecycle.

It does **not** own local route, VPN, DNS, WARP, path measurement, transport selection, QUIC relay clients, or failover; those belong to `ordivon-link`. Local Agent tasks, workspaces, process supervision, and recovery belong to `ordivon-runtime`.

## Implemented execution plane

- HMAC-SHA256 service authentication with a five-minute timestamp window;
- signed method, path, query, Request ID, timestamp, and body digest;
- one authoritative `requests/v2` state object per operation;
- queryable pending receipts and conditionally committed final receipts;
- generation-scoped execution leases and stale-executor fencing;
- Artifact cleanup when a result loses its lease or cannot commit;
- policy, capability, Worker version, and lease generation in every new Receipt;
- deterministic receipt replay and Request-ID conflict detection;
- Cloudflare-native per-key Fetch and Browser rate limits;
- structured operation logs and Worker traces;
- HTTPS-only external Fetch with bounded redirects, size, and time;
- same-origin Browser Run snapshots with PNG, rendered HTML, and manifest artifacts;
- private, generation-versioned R2 Artifact paths;
- version upload, 0% traffic smoke, version override validation, promotion, and rollback receipts;
- Workers.dev, preview URLs, and R2 public access disabled;
- machine-enforced repository boundary checks.

## Verification

```bash
pnpm install --frozen-lockfile
pnpm run ci
```

## Local client

```bash
scripts/install-edge-operations
ordivon-edge health
ordivon-edge fetch https://developers.cloudflare.com/
ordivon-edge browser-run https://example.com/ --full-page
ordivon-edge receipt <request-id> --wait
```

## Release and lifecycle

```bash
python3 scripts/ordivon_edge_release.py release
python3 scripts/ordivon_edge_release.py rollback
scripts/configure-r2-lifecycle
python3 scripts/ordivon_edge_gc.py --dry-run
```

See [`docs/reliability.md`](docs/reliability.md), [`docs/release.md`](docs/release.md), [`docs/operations.md`](docs/operations.md), [`docs/architecture.md`](docs/architecture.md), [`docs/boundary.md`](docs/boundary.md), and [`docs/security.md`](docs/security.md).
