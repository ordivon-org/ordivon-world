# Architecture

## Phase 0 repository classes

The repository contains four deliberately different classes of component:

| Class | Components | Architectural treatment |
|---|---|---|
| Long-term Agent-native core | `link-world` | Own the `NetworkWorld` domain: Link-native identity, mutation, evidence, and lifecycle |
| Local-operations observation/client slice | `link-model`, `link-probe`, `link-observer`, `link-console` | Keep the acyclic local evidence and presentation chain without making it the core |
| Reference transport experiment | `link-wire`, `link-transport-quic` | Preserve the bounded Baseline v0 reference; freeze general transport expansion |
| Private operations/provider tooling | VPN and Surfshark scripts | Retain for explicit private use; do not derive public architecture from provider workflows |

See [`component-map.md`](component-map.md) for the per-component authority and dependency map.

## Long-term Agent-native core

```text
Network World manifest
  → topology and identity controller
  → transport and mediation adapters
  → programmable fault plane
  → independent observer and event root
  → freeze / reset / destruction receipt
```

`link-world` implements the manifest, deterministic controller state, bounded fault facts, independent hash-chained observer root, actor-safe projection, and lifecycle receipts. Its opt-in loopback fixture enforces service availability. It does not yet enforce link, route, DNS, latency, or loss changes in a network namespace.

This is the long-term `NetworkWorld` core and an independent vertical slice:

```text
link-world (manifest + controller + observer + fixture)

link-model ← link-probe ← link-observer ← link-console

link-wire ← link-transport-quic
```

The following layers describe the separate local-operations observation/client slice.

## Layer 1 — immutable evidence model

`link-model` defines serialized facts. It contains no network, filesystem, database, process, or route mutation.

## Layer 2 — active measurement

`link-probe` executes bounded external observations through replaceable system tools. It produces append-safe NDJSON and derived summaries. Route labels describe controlled facts; they do not claim knowledge of the full packet path.

## Layer 3 — local state reduction

`link-observer` combines bounded host observations and service probes into sanitized `LinkSnapshot` values. It persists reduced state and state-change events in SQLite. Raw route, process, DNS, PowerShell, and probe output is discarded before persistence.

## Layer 4 — local presentation

`link-console` serves a loopback-only read-only API, static UI, and SSE updates. It cannot alter VPN state, host routes, DNS, firewall, Cloudflare, or Ordivon Runtime.

## Reference transport experiment

`link-wire` defines Baseline v0 framing, limits, errors, addresses, and state transitions. `link-transport-quic` integrates that contract with Quinn and rustls for controlled interoperability tests.

```text
Local control slice                         Transport slice

link-model                                 link-wire
    ▲                                          ▲
link-probe                            link-transport-quic
    ▲
link-observer
    ▲
link-console
```

This separation prevents a Web status feature from pulling in relay code, and prevents a transport experiment from acquiring host-control authority. Phase 0 retains this bounded reference but freezes its expansion into a general transport platform. Link must reuse maintained TLS, QUIC, and proxy implementations rather than developing a general-purpose network protocol or cryptography.

## Private operations/provider tooling

The VPN namespace, key handling, Surfshark measurement, profile scanning, installation, and fixture-check scripts are private operations/provider tooling. They may exercise explicit, root-only local operations under their existing safeguards, but they are not dependencies of the Agent-native core or the observation/client crates and do not define a public VPN architecture.

Link does not implement a VPN core or container-network orchestration. Any later Network World data plane must preserve Link identity and evidence boundaries and receive a separate design; the current private scripts are not that backend.

## System boundary

```text
Ordivon Runtime ── trusted-local Agent execution, workspace, and recovery
Ordivon Link    ── Network Worlds, communication topology, path evidence, and network recovery
Ordivon Edge    ── remote bodies/Nodes, their lifecycle, and externally hosted capabilities
ordivon-web     ── public presentation and releases
```
