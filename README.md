# Ordivon Link

Ordivon Link is the local network observation, transport, path-selection, and recovery layer of the Ordivon stack.

It owns facts and decisions about the path between a user-controlled device and user-controlled or third-party network endpoints:

```text
Observe local path
→ Probe named targets
→ Reduce evidence
→ Select a route
→ Connect through a replaceable transport
→ Verify
→ Fail over
→ Recover
```

## Strict boundary

Ordivon Link owns:

- local route, DNS, interface, VPN, WARP, and service observations;
- HTTP/TLS and HTTP/3/QUIC measurement evidence;
- explainable route-selection inputs and future failover policy;
- local read-only status history and console;
- replaceable transport adapters;
- the Ordivon Baseline v0 wire contract and QUIC reference adapter.

Ordivon Link does **not** own:

- Cloudflare Workers, Browser Rendering, R2 artifacts, or external fetch execution — those belong to `ordivon-edge`;
- local Agent jobs, workspaces, process supervision, or task artifacts — those belong to `ordivon-runtime`;
- public project presentation — that belongs to `ordivon-web`;
- public proxy subscriptions, multi-user accounts, traffic resale, or new cryptography.

## Workspace

| Crate | Responsibility |
|---|---|
| `link-model` | Stable observation, target, transport, route, snapshot, and event models |
| `link-probe` | Reachability, transfer, connection-lifetime collection, comparison, and reports |
| `link-observer` | Local WSL/Windows/VPN/DNS/service observation and sanitized SQLite history |
| `link-console` | Loopback-only read-only Web console and status API |
| `link-wire` | Pure bounded Baseline v0 wire contract and state machines |
| `link-transport-quic` | Quinn/rustls localhost reference client/server for Baseline v0 |

The dependency graph is deliberately split into three independent vertical slices:

```text
link-model ← link-probe ← link-observer ← link-console

link-wire ← link-transport-quic

configuration + evidence ← operational commands
```

The observation/control slice does not depend on the Baseline wire implementation. The wire/transport slice does not depend on host observation, SQLite, or the Web console.

## Verification

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```

## Local console

```bash
cargo run -p link-console -- \
  --bind 127.0.0.1:8787 \
  --database artifacts/runtime/link.db \
  --targets config/targets/web.toml \
  --interval-seconds 30
```

The console remains loopback-only and read-only. It does not mutate VPN, routes, DNS, firewall, Tunnel, or Ordivon Runtime state.

## Probe example

```bash
cargo run -p link-probe -- run \
  --network wsl-current \
  --route direct-process \
  --protocol all \
  --repeat 3 \
  --no-env-proxy \
  --output artifacts/baseline/reachability.ndjson
```

See [`docs/repository-boundary.md`](docs/repository-boundary.md), [`docs/current-state.md`](docs/current-state.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/operations.md`](docs/operations.md).
