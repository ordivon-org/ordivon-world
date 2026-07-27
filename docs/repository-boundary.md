# Repository boundary

## Ownership test

A component belongs in Ordivon Link when its primary question is:

> Which local or remote network path is available, suitable, selected, connected, or recoverable?

A component belongs in Ordivon Edge when its primary question is:

> Which externally hosted capability should execute a bounded network-side task and return a receipt or artifact?

A component belongs in Ordivon Runtime when its primary question is:

> How should a local Agent task, process, workspace, result, or recovery lifecycle be executed and retained?

## Accepted dependencies

```text
link-console
  → link-observer
    → link-probe
      → link-model

link-transport-quic
  → link-wire
```

Cross-slice dependencies are prohibited without a concrete use case and design review. In particular:

- `link-console` must not import the QUIC relay implementation;
- `link-transport-quic` must not inspect host VPN state or persist SQLite snapshots;
- `link-probe` must not mutate routes;
- Cloudflare SDKs and R2 bindings must not enter this repository;
- Ordivon Runtime workspace/task APIs must not be reimplemented here.

## Remote Edge terminology

The protocol model may use `Edge` to mean a remote relay endpoint. That role name does not transfer Cloudflare execution ownership into this repository. Production node lifecycle belongs to `ordivon-edge`; Link owns the local client, measurement, route policy, and reference interoperability tests.
