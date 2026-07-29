# Deterministic Network World v1


> **Research-status note:** `link-world` is a deterministic network-condition laboratory under the revised Link route, not a proven permanent Agent-native network core or production data plane. See [`research-route.md`](research-route.md).
`link-world` is the first executable range-profile slice. It is independent from the local observation chain and the QUIC transport chain.

## Manifest and identity

The v1 manifest covers:

- nodes and loopback fixture services;
- links, subnets, and trust zones;
- communication identities;
- routes;
- declared external boundaries;
- initial fault and mutation state.

Validation rejects unknown fields, duplicate or unsafe identifiers, dangling references, non-loopback fixture addresses, oversized collections, and loss above 100%.

Before hashing or persistence, manifest collections are sorted by identifier, node services are sorted by identifier, and initial mutations are sorted by their canonical JSON encoding. The SHA-256 of that normalized JSON has two representations:

- `nw1-<hex>` is the stable world identity;
- `sha256:<hex>` is the manifest revision.

Equivalent ordering produces the same identity. Any semantic manifest change produces a different identity. No credentials, node addresses, tokens, or real-target evidence belong in a manifest.

Runtime revision starts at zero. Each successful mutation, egress-evidence record, freeze, reset, and destroy advances it once. Reset reconstructs initial mutation state, restores identity generation 1 and revocation state, clears observed egress evidence, and advances rather than rewinds the runtime revision.

## Authority and evaluated-actor boundary

The controller requires independent, non-nested roots:

```text
artifacts/worlds/<world-id>/             authoritative manifest and current state
artifacts/world-observer/<world-id>/     append-only event chain
```

On Unix these directories and files are created with owner-only permissions. Every event includes sequence, runtime revision, previous hash, and its own SHA-256 hash. The complete chain is verified before inspection or append. The fixture appends a reduced service-connection event without retaining peer addresses or raw traffic. Destroy removes authoritative state but retains the observer chain and destruction event.

`link-world-actor` is the separate range-facing executable. It returns only the versioned current-state projection; it exposes no lifecycle operation, observer path, event rewrite operation, or egress evidence. Lifecycle, mutation, evidence ingestion, and authoritative event inspection remain in the `link-world` controller executable. OS ownership or a separate service account must enforce the process boundary in a deployed range—the Rust interface alone is not a substitute for host access control.

## Modeled and enforced effects

| Effect | v1 behavior |
|---|---|
| Service reachability | Deterministic state and events; enforced by binding or withdrawing the opt-in loopback fixture listener |
| Link partition/up | Deterministic modeled state and events |
| Latency/loss | Deterministic metadata and events; loss is bounded to 0–10000 basis points |
| Route enabled/disabled | Deterministic modeled state and events |
| DNS override/clear | Deterministic modeled state and events |
| Identity rotation/revocation | Deterministic generation and revocation state and events |
| External boundary | Declared allow/deny policy, separate from recorded observation evidence |

The fixture is a foreground test aid, not process lifecycle management. It accepts only manifest-declared loopback addresses and uses the operating system TCP implementation. It does not create namespaces, routes, firewall rules, or traffic-control rules.

The example world begins with both inter-node links partitioned and declares public Internet egress denied. Those are controlled declarations, not proof of packet containment. Missing routes and an empty evidence list are never interpreted as containment.

`record-egress` ingests a result produced by an independent measurement. Its method and detail fields accept only bounded public labels, preventing raw command output, addresses, or free-form evidence from entering persistent state. It does not perform a probe and must not be described as measured evidence unless its named method actually ran outside this command.

## CLI walkthrough

Validate and create the three-service example:

```bash
cargo run -p link-world -- validate \
  config/worlds/disconnected-three-service.toml

cargo run -p link-world -- create \
  config/worlds/disconnected-three-service.toml
```

Copy the returned `world_id` into the following commands:

```bash
WORLD_ID=nw1-<manifest-hash>

cargo run -p link-world -- inspect "$WORLD_ID"
cargo run -p link-world --bin link-world-actor -- "$WORLD_ID"

# Optional foreground fixture on 127.0.0.1:38101-38103.
cargo run -p link-world -- fixture "$WORLD_ID"

# Withdraw and restore one live fixture service.
cargo run -p link-world -- mutate "$WORLD_ID" service worker-rpc --reachable false
cargo run -p link-world -- mutate "$WORLD_ID" service worker-rpc --reachable true

# Change modeled topology and impairment facts.
cargo run -p link-world -- mutate "$WORLD_ID" link gateway-worker --partitioned false
cargo run -p link-world -- mutate "$WORLD_ID" impairment gateway-worker \
  --latency-ms 80 --loss-basis-points 250

cargo run -p link-world -- freeze "$WORLD_ID"
cargo run -p link-world -- events "$WORLD_ID"
cargo run -p link-world -- reset "$WORLD_ID"
cargo run -p link-world -- destroy "$WORLD_ID"

# The authority is gone; the observer event file remains.
cargo run -p link-world -- events "$WORLD_ID"
```

All successful control commands emit schema-versioned JSON. Errors are nonzero exits. Tests cover order-independent identity, lifecycle revision rules, live loopback service withdrawal/restoration, freeze/reset/destroy, retained destruction history, actor-view separation, and tamper detection.
