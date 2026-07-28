# Ordivon Edge

Ordivon Edge is the distributed external presence and execution fabric of the
Ordivon stack. Phase 0 contains a mature Cloudflare Worker production provider,
provider-neutral Node contracts and lifecycle, a trusted research control
session, and a narrow local-unshare conformance/reference provider.

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

Cloudflare production remains the repository's operationally critical
production plane. It is no longer accurate to describe it as the only
implemented part of this repository.

## Phase 0 repository shape

- **Agent-native core** — Node identity/lifecycle, leases, evidence, and
  reconstruction contracts;
- **supervisor/control** — `ResearchNodeControlSession` and the long-lived JSONL
  session;
- **providers** — Cloudflare Worker production and local-unshare
  research/conformance;
- **ops** — the Cloudflare client, release, GC, and lifecycle scripts.

See [`docs/component-map.md`](docs/component-map.md) for the key files,
authority, and Phase 0 disposition of each area.

## Frozen terminology

- A **Node** is the long-lived semantic identity of an Agent presence.
- A **Sandbox** is an isolated instance of a Node on one Provider, including
  its generation.
- An **Execution** is one bounded action inside a Sandbox.

The current code does not contain an independent `Sandbox` type. The existing
Node identity input, provider body, lifecycle record, and generation fields
cover parts of the model, but must not be presented as a completed Sandbox
abstraction.

## Project horizon

Edge is not limited to Cloudflare Fetch and Browser Run. Its full subject is the identity, lifecycle, capability, evidence, and recovery of remote Agent bodies across browsers, containers, virtual machines, service emulators, sensors, decoys, and user-controlled infrastructure.

Production, research, and adversarial-range profiles are distinct. A range body may be internally powerful while its external consequence scope remains independently constrained and observed.

That horizon is realized through bounded Provider adapters, not by building a
container runtime, VM orchestrator, network stack, scheduler, or workspace
runtime in Edge. OCI/runc-backed providers are a future direction only; Phase 0
does not implement them.

See [`docs/charter.md`](docs/charter.md) and [`docs/capability-gaps.md`](docs/capability-gaps.md).

The provider-neutral identity/lifecycle contract and the rootless disposable
research conformance profile are documented in
[`docs/node-contract.md`](docs/node-contract.md). The local provider is a
separate library adapter and does not add Worker routes, bindings, or release
behavior. Its scope is frozen as a narrow reference implementation; it is not
the seed of a self-developed container Runtime.

A component-owned long-lived JSONL control session exposes the research Node to
Ordivon Security without persisting lease tokens or copying Edge lifecycle
state. See [`docs/research-node-control-v0.md`](docs/research-node-control-v0.md).

## Strict boundary

Ordivon Edge owns Node identity and authoritative lifecycle, body/Sandbox
semantics, leases, execution evidence, reconstruction, and Provider contracts.
It also owns the Cloudflare Worker production execution plane: external Fetch
and Browser Run policy, private R2 Artifacts, budgets, receipts, and release
control.

Ordivon Runtime supervises trusted supervisor/control processes and owns local
Agent Tasks, workspaces, process supervision, and recovery. It does not own
Edge body/Sandbox lifecycle. Ordivon Link owns connectivity, but may only
consume a future generation-bound attachment handle; it does not own or advance
Node or Sandbox lifecycle. That handle is not implemented in Phase 0.

Edge does **not** own local route, VPN, DNS, WARP, path measurement, transport
selection, QUIC relay clients, or failover. It also does not implement a
container runtime, VM orchestrator, network stack, scheduler, or workspace
runtime.

## Cloudflare production execution plane

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

## Research Node control

```bash
corepack enable
pnpm node-control -- --root /private/edge-provider-root
```

The process accepts bounded JSONL `declare`, `snapshot`, `execute`, `reconcile`,
and `residual` requests. It is not a production HTTP API and must remain under
the trusted research management boundary. It supervises the narrow local
conformance provider; it does not establish a general Sandbox service or a
second Runtime.

## Verification

The repository pins `pnpm@10.33.2`; local and CI entry points use the same major
version and build-script policy.

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

See [`docs/component-map.md`](docs/component-map.md), [`docs/charter.md`](docs/charter.md), [`docs/capability-gaps.md`](docs/capability-gaps.md), [`docs/reliability.md`](docs/reliability.md), [`docs/release.md`](docs/release.md), [`docs/operations.md`](docs/operations.md), [`docs/architecture.md`](docs/architecture.md), [`docs/boundary.md`](docs/boundary.md), and [`docs/security.md`](docs/security.md).
