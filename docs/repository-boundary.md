# Repository boundary

## Ownership test

A component belongs in Ordivon Link when its primary question is:

> What network world connects the actors, how may it change, and what connectivity facts can be independently proven?

A component belongs in Ordivon Edge when its primary question is:

> How should a remote body or Edge Node be provisioned, operated, recovered, and retired, and how should its externally hosted capabilities execute?

A component belongs in Ordivon Runtime when its primary question is:

> How should a local Agent task, process, workspace, result, or recovery lifecycle be executed and retained?

## Capability horizon

Link may construct isolated range topology, communication identity, dynamic faults, deception, and multi-Agent communication evidence. Those capabilities remain Link responsibilities even when Security defines the adversarial objective. Current code implements the local-operations profile and the first deterministic local Network World/range slice; it does not yet implement a packet-isolated multi-node data plane.

## Accepted dependencies

```text
link-console
  → link-observer
    → link-probe
      → link-model

link-transport-quic
  → link-wire

link-world
```

Cross-slice dependencies are prohibited without a concrete use case and design review. In particular:

- `link-console` must not import the QUIC relay implementation;
- `link-transport-quic` must not inspect host VPN state or persist SQLite snapshots;
- `link-probe` must not mutate routes;
- Cloudflare SDKs and R2 bindings must not enter this repository;
- Ordivon Runtime workspace/task APIs must not be reimplemented here.
- private VPN/Surfshark scripts must not become dependencies of the core or observation/client crates.

## Remote Edge terminology

Edge owns remote bodies/Edge Nodes and their lifecycle, including the identity of an Edge Sandbox Generation. Link owns the network world and any future network-side attachment facts; it does not provision or supervise the attached body.

Historical Baseline protocol documents use `Edge` for the remote endpoint of the reference relay experiment. That interoperability role does not transfer Edge Node lifecycle or Cloudflare execution into this repository, and it does not make the reference transport Link's general architecture. Cross-component attachment terminology is frozen, without a Schema or backend, in [`component-map.md`](component-map.md).
