# Capability gaps

The repository now contains a deterministic Network World, a component-owned
Security lifecycle port, local observation, controlled WireGuard egress, and a
reference QUIC transport. It is not yet a packet-isolated adversarial network
fabric.

## P0 status

| Capability | Current state |
|---|---|
| Typed Network World manifest | implemented |
| Deterministic create, inspect, freeze, reset, and destroy | implemented |
| Append-only independent observer and actor-safe projection | implemented |
| Explicit egress declaration and separately ingested evidence | implemented |
| Synthetic identity rotation, revocation, and reset | implemented |
| Versioned Security lifecycle surface | implemented as `link-world-security` |
| Response-loss reconciliation without duplicate reset/destroy | implemented |
| Fresh-root reconstruction and residual receipts | implemented |
| Live loopback service reachability | implemented |
| Packet-level partitions, latency, loss, routes, and DNS | pending |
| Persistent Edge Node network attachment | pending; P0-D design boundary |
| Production OS-account separation for observer authority | pending |

`link-world-security` exposes only snapshot, execute, reconcile, and residual
operations over the existing Link controller. It retains component-side
operation journals so a lost reset response can be proven by the exact observer
revision instead of dispatching a second reset.

The executable effect surface remains deliberately narrow. The opt-in loopback
fixture controls TCP service reachability. Link state, latency/loss, routes, and
DNS remain deterministic modeled state and events. Declared Internet denial is
not packet-containment proof.

## P1 — full-spectrum network behavior

- persistent namespace, veth, bridge, route, DNS, and `tc netem` data plane;
- dynamic topology and moving trust boundaries;
- Agent communication graph and message provenance;
- deception nodes, sinkholes, mirrors, and identity emulation;
- repeatable traffic capture and replay;
- mature transport and mediation adapters;
- multi-host range federation and controller-failure recovery.

## P2 — frontier work

- large distributed ranges;
- mobile and intermittent physical links;
- adaptive network policies competing with adaptive Agents;
- hardware-backed high-fidelity observation and impairment.

The next large step is not another manifest or controller abstraction. It is a
persistent data-plane backend that can attach an Edge-owned body without making
Link own that body's lifecycle.
