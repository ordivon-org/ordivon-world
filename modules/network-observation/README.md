# Ordivon Link


> **Migration note:** this is the inherited network-observation and research module of Ordivon World. Its Link terminology is retained where required for operational compatibility and historical evidence; it no longer defines a separate top-level project.
Ordivon Link is the Task-to-connectivity and evidence-continuity overlay of the
Ordivon stack. It lets open Tasks express logical communication needs, bind them
to mature network and identity mechanisms, verify the realized relation,
preserve path-conditioned evidence, and continue when paths, endpoints,
identities, or participants change.

Link does **not** build a network stack, VPN core, proxy, CNI implementation,
service mesh, SDN controller, DNS, PKI, QUIC stack, or traffic shaper. Those
classical systems remain authoritative for byte transport and network
configuration.

```text
Host Goal / Task / Attempt / Effect
                │
                ▼
 connectivity requirement and exact binding
                │
                ▼
 mature DNS / route / VPN / proxy / mesh / transport / identity substrate
                │
                ▼
 path, endpoint, identity, policy, delivery and failure evidence
                │
                ▼
 invalidation, reconciliation, handoff, continued Task
```

## Foundational split

```text
logical relationship
  who needs to interact with whom, why, and under which authority

communication identity
  which service, workload, Agent participant, device, or person is present

physical path
  which endpoint, route, transport, tunnel, relay, region, or intermediary
  carried the interaction
```

Relation, identity, and path are not interchangeable. Reachability does not
prove authority. Endpoint replacement does not prove participant continuity.
Transparent failover does not guarantee evidence equivalence.

## Current repository truth

The repository currently contains four different classes of result:

1. **Observation producers** — local route, DNS, VPN, WARP, service, HTTP/TLS,
   HTTP/3/QUIC, transfer, and connection-lifetime probes plus reduced history.
2. **Private operator tooling** — explicit per-command WireGuard namespaces and
   Surfshark-specific measurement and profile scanning.
3. **Reference transport experiment** — bounded Baseline v0 framing and a
   Quinn/rustls localhost implementation.
4. **Network-condition research substrate** — deterministic Network World
   identity, modeled topology/mutations, observer chain, actor view, lifecycle,
   Security port, and a narrow loopback fixture.

The fourth class is a research laboratory, not a proven permanent Agent-native
Network World core. Current code does not implement Task-level Connectivity
Requirements, Connectivity Bindings, path-conditioned Artifact provenance,
path-change invalidation, participant continuity, automatic selection, or Host
recovery across path and identity changes.

See [`docs/component-map.md`](docs/component-map.md) and
[`docs/research-route.md`](docs/research-route.md).

## Active route

```text
L0 preserve observations and explicit private operations
→ L1 publish versioned, expiring observations for Host Context
→ L2 derive Connectivity Requirement from two real workloads
→ L3 prove path-conditioned evidence and invalidation
→ L4 prove uncertain-delivery, identity, path, and participant recovery
→ L5 revisit Network World/data-plane abstractions only if workloads require them
```

The cross-project research source is
[`LINK-CHARTER-003`](https://github.com/zycxfyh/ordivon-computing/blob/main/research/charters/LINK-CHARTER-003.md).

## Provisional research vocabulary

- **Connectivity Requirement** — what logical relation, identity assurance,
  trust/data boundary, locality, availability, and evidence one Attempt or
  Effect needs.
- **Path / Identity Observation** — versioned, expiring, method-bound facts about
  reachability, route class, egress, endpoint identity, application capability,
  and uncertainty.
- **Connectivity Binding** — the exact relation from Task/Attempt/Effect
  references to logical source and target, selected path/transport, endpoint,
  identity generation, policy, and supporting observations.
- **Path-conditioned provenance** — the network and identity conditions under
  which an Artifact, Observation, or Claim was produced.
- **Invalidation** — which prior claims, permissions, or pending communications
  become stale when path, endpoint, identity, or policy changes.
- **Relationship continuity** — recovery or explicit handoff without deleting
  the parent Task when communication changes.

These are research candidates, not frozen public schemas.

## Strict boundary

Link may own Task-conditioned connectivity requirements, observations,
bindings, path-conditioned provenance, invalidation, and communication
reconciliation.

Link references but does not redefine Goal, Task, Attempt, Effect, Dispatch,
Artifact, Claim, Verification, participant responsibility, or organization.
Host and the semantic Kernel own open work. Edge owns external execution
placement. Runtime owns trusted-local execution. Classical network and identity
systems own their native mechanisms. Security or the domain system owns final
consequence and validity.

Forbidden expansions include:

- a self-developed VPN, proxy, CNI, service mesh, network protocol,
  cryptography, transport, DNS, identity, or traffic-control platform;
- automatic host route, DNS, or VPN mutation before a Task-level requirement and
  recovery model is empirically established;
- treating the current Network World as a production data plane or settled
  universal Agent abstraction;
- moving Task, body, provider, or campaign lifecycle into Link.

## Workspace

| Class | Component | Current role |
|---|---|---|
| Observations | `link-model`, `link-probe`, `link-observer`, `link-console` | collect, reduce, store, and present bounded path/service facts |
| Network-condition research | `link-world` | deterministic modeled world, identity, events, lifecycle, actor view, and loopback fixture |
| Reference transport | `link-wire`, `link-transport-quic` | bounded Baseline v0 interoperability experiment |
| Private operations | VPN and Surfshark scripts | explicit isolated egress and provider-specific measurement |

The slices remain independent:

```text
link-model ← link-probe ← link-observer ← link-console
link-wire ← link-transport-quic
link-world
```

## Deterministic Network World experiment

```bash
cargo run -p link-world -- validate \
  config/worlds/disconnected-three-service.toml
cargo run -p link-world -- create \
  config/worlds/disconnected-three-service.toml
```

It provides deterministic state, events, and loopback service reachability. It
does not enforce packet-level route, DNS, partition, latency, or loss and is not
the current production architecture.

## Local console

```bash
cargo run -p link-console -- \
  --bind 127.0.0.1:8787 \
  --database artifacts/runtime/link.db \
  --targets config/targets/web.toml \
  --interval-seconds 30
```

## Isolated VPN execution

```bash
sudo scripts/install-ordivon-vpn
sudo ordivon-vpn-keypair
ordivon-vpn doctor jp-tok
sudo ordivon-vpn up jp-tok
sudo ordivon-vpn exec curl -fsS https://www.cloudflare.com/cdn-cgi/trace
sudo ordivon-vpn down
```

The private controller remains an operator tool, not Link's public architecture.

## Verification

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```
