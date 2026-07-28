# Agent instructions

## Scope

Ordivon Link owns programmable network worlds, communication topology, path and transport evidence, controlled faults, selection, containment facts, and network recovery. The repository currently contains a deterministic local Network World slice in addition to the local-operations observation/client slice, a bounded reference transport experiment, and private operations/provider tooling. `link-world` is the long-term Agent-native core; the other slices do not define that core's architecture. Keep remote Node lifecycle, Cloudflare execution, Agent cognition, and trusted-local process execution outside this repository.

## Engineering rules

1. Keep `link-model ← link-probe ← link-observer ← link-console` acyclic.
2. Keep `link-wire ← link-transport-quic` independent from the observation slice.
3. Do not add Cloudflare Workers, Browser Rendering, R2, Queue, or external fetch implementation here.
4. Do not add Ordivon Runtime workspace, task, process, or artifact lifecycle here.
5. Route and network labels describe controlled facts only.
6. Never commit credentials, private keys, tokens, subscription links, node addresses, or personal egress evidence.
7. Persist only sanitized reduced observations; raw command and probe output stays bounded and ephemeral.
8. The console remains loopback-only and read-only unless a separate authenticated boundary is approved.
9. Tests must not require public network access or mutate host networking.
10. Reuse maintained TLS, QUIC, proxy, and VPN implementations; do not create a general-purpose network protocol, VPN core, cryptographic primitives, or container-network orchestration.
11. Explicit VPN mutation must be isolated to a dedicated namespace, remain root-only, preserve the WSL root default route, and roll back transactionally.
12. CI may syntax-check the VPN controller and exercise key-pair rendering only against temporary fixtures, but must never create namespaces, interfaces, routes, firewall rules, or public probes.
13. VPN key input must not place key values in command arguments, process listings, repository content, or normal output; mismatched pairs must leave existing state unchanged.
14. Capability inside an owned range and consequence outside it are separate; do not reduce the project definition to workstation diagnosis.
15. Any future topology or fault mutation must bind a named Network World identity and emit independently observable events.
16. Reachability is never treated as target authority, and missing routes are never sufficient proof of containment.

## Required checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```
