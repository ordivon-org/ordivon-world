# Ordivon Edge

Ordivon Edge is the distributed external presence and execution fabric of the Ordivon stack. The current repository implements its Cloudflare production profile.

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

## Project horizon

Edge is not limited to Cloudflare Fetch and Browser Run. Its full subject is the identity, lifecycle, capability, evidence, and recovery of remote Agent bodies across browsers, containers, virtual machines, service emulators, sensors, decoys, and user-controlled infrastructure.

Production, research, and adversarial-range profiles are distinct. A range body may be internally powerful while its external consequence scope remains independently constrained and observed.

See [`docs/charter.md`](docs/charter.md) and [`docs/capability-gaps.md`](docs/capability-gaps.md).

The provider-neutral identity/lifecycle contract and the rootless disposable
research profile are documented in
[`docs/node-contract.md`](docs/node-contract.md). The local provider is a
separate library adapter and does not add Worker routes, bindings, or release
behavior.

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
- policy fingerprint, capability, Worker version, and lease generation in every new Receipt;
- deterministic receipt replay with an explicit 90-day idempotency window;
- Cloudflare-native per-key Fetch and Browser rate limits;
- structured operation logs and Worker traces;
- HTTPS-only external Fetch with bounded redirects, size, and time;
- same-origin Browser Run snapshots with PNG, rendered HTML, and manifest artifacts;
- private, generation-versioned R2 Artifact paths retained longer than replayable Receipts;
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
ordivon-edge status --repo /root/projects/ordivon-edge --expected-ref HEAD
ordivon-edge fetch https://developers.cloudflare.com/
ordivon-edge browser-run https://example.com/ --full-page
ordivon-edge receipt <request-id> --wait
ordivon-edge artifact-get <artifact-key> --sha256 <receipt-sha256> --output ./artifact.bin
```

## Release and lifecycle

```bash
python3 scripts/ordivon_edge_release.py release
python3 scripts/ordivon_edge_release.py rollback
scripts/configure-r2-lifecycle
python3 scripts/ordivon_edge_gc.py --dry-run
```

See [`docs/charter.md`](docs/charter.md), [`docs/capability-gaps.md`](docs/capability-gaps.md), [`docs/reliability.md`](docs/reliability.md), [`docs/release.md`](docs/release.md), [`docs/operations.md`](docs/operations.md), [`docs/architecture.md`](docs/architecture.md), [`docs/boundary.md`](docs/boundary.md), and [`docs/security.md`](docs/security.md).
