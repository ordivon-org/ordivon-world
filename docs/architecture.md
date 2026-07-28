# Architecture

## Network World slice

```text
Network World manifest
  → topology and identity controller
  → transport and mediation adapters
  → programmable fault plane
  → independent observer and event root
  → freeze / reset / destruction receipt
```

`link-world` implements the manifest, deterministic controller state, bounded fault facts, independent hash-chained observer root, actor-safe projection, and lifecycle receipts. Its opt-in loopback fixture enforces service availability. It does not yet enforce link, route, DNS, latency, or loss changes in a network namespace.

It is an independent vertical slice:

```text
link-world (manifest + controller + observer + fixture)

link-model ← link-probe ← link-observer ← link-console

link-wire ← link-transport-quic
```

The following layers describe the separate local operations slice.

## Layer 1 — immutable evidence model

`link-model` defines serialized facts. It contains no network, filesystem, database, process, or route mutation.

## Layer 2 — active measurement

`link-probe` executes bounded external observations through replaceable system tools. It produces append-safe NDJSON and derived summaries. Route labels describe controlled facts; they do not claim knowledge of the full packet path.

## Layer 3 — local state reduction

`link-observer` combines bounded host observations and service probes into sanitized `LinkSnapshot` values. It persists reduced state and state-change events in SQLite. Raw route, process, DNS, PowerShell, and probe output is discarded before persistence.

## Layer 4 — local presentation

`link-console` serves a loopback-only read-only API, static UI, and SSE updates. It cannot alter VPN state, host routes, DNS, firewall, Cloudflare, or Ordivon Runtime.

## Independent transport slice

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

This separation prevents a Web status feature from pulling in relay code, and prevents a transport experiment from acquiring host-control authority.

## System boundary

```text
Ordivon Runtime ── local Agent execution and recovery
Ordivon Link    ── local network observation, selection, connection, recovery
Ordivon Edge    ── externally hosted fetch, browser, artifact, and node capabilities
ordivon-web     ── public presentation and releases
```
