# Component Map Under the Revised Link Route

This map separates operational capability from long-term research claims. No
code is moved by this documentation change.

## Crates

| Component | Current authority | Revised classification | Disposition |
|---|---|---|---|
| `link-model` | serialized local targets, probes, routes, snapshots, and events | observation vocabulary | retain; evolve only from real Host consumption |
| `link-probe` | bounded reachability, transfer, and lifetime observations | path evidence producer | retain; add method/freshness semantics before broader use |
| `link-observer` | reduced local state and sanitized history | observation reducer | retain; no Task or network-control authority |
| `link-console` | loopback read-only presentation | operator presentation | retain independently of semantic route |
| `link-world` | deterministic manifest, world state, modeled mutations, events, lifecycle, actor view, fixture | network-condition research laboratory | keep for experiments; do not call permanent core |
| `link-wire` | bounded Baseline v0 framing and state machines | reference protocol experiment | freeze general expansion |
| `link-transport-quic` | localhost Quinn/rustls integration | reference transport adapter | freeze; reuse maintained transport |

## Private operations

| Component | Current authority | Revised classification | Disposition |
|---|---|---|---|
| `ordivon-vpn` and key/profile tools | explicit root-only isolated WireGuard egress | private provider/operator tools | retain for user needs; no crate dependency |
| Surfshark measurement and scanning | provider-specific path evidence | private measurement tools | retain; never define public architecture |
| install and check scripts | local deployment and fixture validation | operations | retain independently of Link research outcome |

## Not yet implemented

| Candidate | Evidence status |
|---|---|
| Connectivity Requirement | research only |
| Path/Identity Observation contract for Host Context | partial raw ingredients only |
| Host-visible Connectivity Binding | absent |
| path-conditioned Artifact/Claim provenance | absent |
| dependency-driven invalidation | absent |
| uncertain-delivery reconciliation | absent |
| participant continuity and handoff | absent |
| durable Network World above mature backends | unproven hypothesis |

## Ownership summary

- Classical network systems own byte movement and native configuration.
- Link may own the exact Task-conditioned relation/path/identity binding and its
  evidence/invalidation semantics.
- Host owns why the relation exists and how Task state advances.
- Edge owns where external execution occurs.

The current Network World remains useful because it can falsify or refine these
boundaries. Its existence does not settle them.
