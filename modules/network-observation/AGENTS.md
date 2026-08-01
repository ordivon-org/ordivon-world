# Agent instructions

## Scope

This directory is the source-native network observation module carried by Ordivon World. Legacy `link-*` crate and command names remain for compatibility and evidence; they do not restore an independent Link authority.

The active default workspace is `link-model`, `link-probe`, `link-observer`, and `link-console`. It collects, sanitizes, stores, and presents bounded observations. `link-world`, `link-wire`, and `link-transport-quic` are historical experiments excluded from the default workspace. VPN and Surfshark scripts are explicit private operator tools, not automatic World control.

## Owned facts

The module owns source-native, method-bound observations such as probe kind, target label, protocol, timing, reachability, transfer, connection lifetime, reduced route state, failure class, collection identity, and observation time.

It does not own Task requirements, connectivity binding, participant identity, authority, containment, routing decisions, provider selection, Effect recovery, or Task completion. Host consumes observations through bounded references or projections.

## Rules

1. Keep the active dependency direction `link-model ← link-probe ← link-observer ← link-console`.
2. Use argument-vector process execution; never interpolate probe input into a shell.
3. Bound target count, identifiers, URLs, process lifetime, stdout, stderr, samples, and stored history.
4. Persist only sanitized reduced observations; raw output remains bounded and ephemeral.
5. Reachability is not authority, a route label is not complete path truth, and missing observation is not proof of absence or containment.
6. The console remains loopback-only, read-only, and protected by strict response headers.
7. Tests must not require public network access or mutate host networking.
8. VPN mutation remains root-only, explicit, isolated, recoverable, and outside default CI.
9. Reuse maintained networking, TLS, QUIC, VPN, proxy, CNI, mesh, DNS, PKI, and traffic-control implementations.
10. Do not promote historical Network World, wire, transport, or identity types without a new reproduced workload failure.

## Required checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```
