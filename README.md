# Ordivon Link

Ordivon Link is the programmable network and communication fabric of the Ordivon stack. The current repository contains the long-term Agent-native Network World core, a local-operations observation/client slice, a bounded reference transport experiment, and private operations/provider tooling.

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

## Project horizon

Link is not limited to one workstation, VPN, or relay. Its full subject is the network world through which distributed Agents discover, communicate, fail, reorganize, and compete. Future range profiles may construct isolated multi-node topologies, inject faults and partitions, expose synthetic identities, and provide independent network evidence.

The evaluated Agent's internal communication capability and the experiment's external consequence boundary are separate concerns. Link may support broad range-local behavior while independently proving which external paths exist.

See [`docs/charter.md`](docs/charter.md) and [`docs/capability-gaps.md`](docs/capability-gaps.md).

## Repository shape

The Phase 0 boundary separates four kinds of code:

1. **Long-term Agent-native core:** `link-world` owns the `NetworkWorld` domain, Link-native world identity, modeled mutations, independent evidence, and lifecycle. The implemented slice is deterministic and local; only its loopback service fixture has an executable effect plane today.
2. **Local-operations observation/client slice:** `link-model`, `link-probe`, `link-observer`, and `link-console` observe and present workstation, path, and service facts. They are useful clients of Link capabilities, not the definition of the Network World core.
3. **Reference transport experiment:** `link-wire` and `link-transport-quic` preserve the bounded Baseline v0 interoperability experiment. Phase 0 freezes expansion into a general transport platform; production work must reuse maintained TLS, QUIC, and proxy implementations.
4. **Private operations/provider tooling:** the VPN and Surfshark scripts support explicit private operations and provider-specific evidence. They do not define Link's public architecture or a reusable VPN core.

See [`docs/component-map.md`](docs/component-map.md) for component authority, dependency direction, and Phase 0 disposition.

## Strict boundary

Ordivon Link owns:

- `NetworkWorld` identity, modeled topology and mutations, independent network evidence, and lifecycle receipts;
- local route, DNS, interface, VPN, WARP, and service observations;
- HTTP/TLS and HTTP/3/QUIC measurement evidence;
- explainable route-selection inputs and future failover policy;
- local read-only status history and console;
- replaceable transport adapters;
- explicit root-only isolated VPN namespaces for selected commands, without changing the WSL root default route;
- the Ordivon Baseline v0 wire contract and QUIC reference adapter.

Ordivon Link does **not** own:

- Cloudflare Workers, Browser Rendering, R2 artifacts, or external fetch execution — those belong to `ordivon-edge`;
- local Agent jobs, workspaces, process supervision, or task artifacts — those belong to `ordivon-runtime`;
- public project presentation — that belongs to `ordivon-web`;
- public proxy subscriptions, multi-user accounts, or traffic resale;
- a self-developed general-purpose network protocol, VPN core, cryptography, or container-network orchestration.

## Workspace

| Category | Component | Responsibility |
|---|---|---|
| Agent-native core | `link-world` | Independent Network World v1 manifest, identity, lifecycle, mutation, event chain, actor view, and loopback fixture |
| Local operations | `link-model` | Stable observation, target, transport, route, snapshot, and event models |
| Local operations | `link-probe` | Reachability, transfer, connection-lifetime collection, comparison, and reports |
| Local operations | `link-observer` | Local WSL/Windows/VPN/DNS/service observation and sanitized SQLite history |
| Local operations | `link-console` | Loopback-only read-only Web console and status API |
| Reference transport | `link-wire` | Pure bounded Baseline v0 wire contract and state machines |
| Reference transport | `link-transport-quic` | Quinn/rustls localhost reference client/server for Baseline v0 |
| Private operations | `scripts/` VPN and Surfshark tools | Explicit isolated egress, provider-specific measurement, installation, and fixture checks |

The dependency graph keeps the core, local observation, and reference transport slices independent; private operations scripts remain outside the crate graph:

```text
link-model ← link-probe ← link-observer ← link-console

link-wire ← link-transport-quic

link-world

configuration + evidence ← operational commands
```

The observation/client slice does not depend on the Baseline wire implementation. The wire/transport experiment does not depend on host observation, SQLite, the Web console, or `link-world`.

## Deterministic Network World

The first range slice constructs typed world state without coupling it to host observation or the transport core:

```bash
cargo run -p link-world -- validate \
  config/worlds/disconnected-three-service.toml

cargo run -p link-world -- create \
  config/worlds/disconnected-three-service.toml
```

Use the returned `world_id` with `inspect`, `mutate`, `freeze`, `reset`, `events`, and `destroy`. A separate read-only `link-world-actor` binary exposes evaluated-actor inspection without lifecycle or observer controls. The optional `fixture` command enforces service reachability for the three loopback TCP services; topology, route, DNS, and impairment mutations are modeled in this slice. See [`docs/network-world.md`](docs/network-world.md).

## Security lifecycle port

`link-world-security` exposes a component-owned JSON surface for Security
snapshot, lifecycle execution, reconciliation, residual checks, and fresh-root
reconstruction. It preserves Link's native World identity and observer chain;
it does not move Link state into Security.

```bash
cargo run -p link-world --bin link-world-security -- \
  --manifest config/worlds/disconnected-three-service.toml \
  --authority-root /private/link/authority \
  --observer-root /private/link/observer \
  --actor-root /private/link/actor \
  --operation-root /private/link/operations \
  --reconstruction-root /private/link/reconstruction \
  snapshot
```

See [`docs/security-port-v0.md`](docs/security-port-v0.md).

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

## Isolated VPN execution

The separate `ordivon-vpn` controller creates a root-only network namespace for explicitly selected commands. WireGuard is born in the WSL root namespace and then moved into the isolated namespace, so encrypted UDP uses the existing root network path while cleartext routes remain isolated. The controller is not called by the console and does not move Runtime, MCP, or Cloudflare Tunnel. It also refuses startup when a rendered profile does not match the canonical installed Surfshark key pair.

```bash
sudo scripts/install-ordivon-vpn
sudo ordivon-vpn-keypair
ordivon-vpn doctor jp-tok
sudo ordivon-vpn up jp-tok
sudo ordivon-vpn exec curl -fsS https://www.cloudflare.com/cdn-cgi/trace
sudo ordivon-vpn down
```

Windows Surfshark must be disconnected before starting the isolated namespace. For route-state evidence, use `surfshark-measure before`, `after`, and `compare`.

See [`docs/vpn-namespace.md`](docs/vpn-namespace.md).

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

See [`docs/charter.md`](docs/charter.md), [`docs/capability-gaps.md`](docs/capability-gaps.md), [`docs/component-map.md`](docs/component-map.md), [`docs/repository-boundary.md`](docs/repository-boundary.md), [`docs/current-state.md`](docs/current-state.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/operations.md`](docs/operations.md).
