# Agent instructions

## Scope

Ordivon Link is the Task-to-connectivity and evidence-continuity overlay above
mature network, identity, discovery, and messaging systems. Its active research
question is how one open Task expresses and binds a logical communication
relationship, verifies the realized path and identity, preserves conditioned
evidence, and continues across path, endpoint, identity, or participant change.

The repository contains four deliberately different classes:

- **observation producers** — `link-model`, `link-probe`, `link-observer`, and
  `link-console`;
- **network-condition research laboratory** — `link-world`, its observer,
  lifecycle, actor view, loopback fixture, and Security port;
- **reference transport experiment** — `link-wire` and
  `link-transport-quic`;
- **private operator tooling** — WireGuard namespace and Surfshark scripts.

`link-world` is a research hypothesis, not a proven permanent Agent-native core.
See `docs/research-route.md` and `docs/component-map.md`.

## Candidate vocabulary and ownership

- **Connectivity Requirement** describes the logical relationship, identity,
  trust/data boundary, locality, availability, and evidence one Attempt or
  Effect requires.
- **Path / Identity Observation** records versioned, expiring, method-bound facts
  about reachability, route class, egress, endpoint identity, application
  capability, and uncertainty.
- **Connectivity Binding** relates exact Task/Attempt/Effect references to
  logical source and target, path, endpoint, transport, identity generation,
  policy, and supporting observations.
- **Path-conditioned provenance** records the network and identity conditions
  under which an Artifact, Observation, or Claim was produced.
- **Invalidation** identifies which claims, permissions, or pending work become
  stale after path, endpoint, identity, observation, or policy change.
- **Relationship continuity** reconciles or explicitly hands off work without
  deleting the parent Task.

These are research candidates, not frozen schemas.

Host or the semantic Kernel owns Goal, Task, Attempt, Effect, Dispatch,
Artifact, Claim, verification, participant responsibility, and work continuity.
Edge owns external execution placement. Runtime owns trusted-local execution.
Classical network and identity systems own routes, endpoints, transports,
certificates, packets, and native lifecycle. Security or the domain system owns
consequence policy and final validity.

## Route constraints

1. Preserve useful observations, reduced history, and explicit private
   operations.
2. Next integration evidence is a versioned, expiring, secret-free Observation
   consumed by Host Context without moving Context ownership into Link.
3. Derive Connectivity Requirement fields from at least two real workloads
   before defining a schema or automatic path selector.
4. Prove path-conditioned evidence and invalidation before mutating host routes,
   DNS, VPN, or firewall automatically.
5. Prove uncertain delivery, identity rotation, endpoint replacement, and
   participant handoff under one persistent Task.
6. Retain Network World as an experiment laboratory unless multiple workloads
   prove shared identity/reset/evidence semantics above mature backends.

## Engineering rules

1. Keep `link-model ← link-probe ← link-observer ← link-console` acyclic.
2. Keep `link-wire ← link-transport-quic` independent from the observation
   slice.
3. Do not add Cloudflare Workers, Browser Rendering, R2, Queue, or external
   Fetch implementation here.
4. Do not add Ordivon Runtime Workspace, Task, Job, process, or Artifact
   lifecycle here.
5. Route and network labels describe controlled facts only, never complete path
   truth, authorization, or containment.
6. Never commit credentials, private keys, tokens, subscription links, node
   addresses, or personal egress evidence.
7. Persist only sanitized reduced observations; raw command and probe output
   stays bounded and ephemeral.
8. The console remains loopback-only and read-only unless a separate
   authenticated boundary is approved.
9. Tests must not require public network access or mutate host networking.
10. Reuse maintained TLS, QUIC, proxy, VPN, CNI, service-mesh, DNS, PKI, and
    traffic-control implementations; do not create replacements.
11. Explicit VPN mutation must be isolated to a dedicated namespace, remain
    root-only, preserve the WSL root default route, and roll back transactionally.
12. CI may syntax-check private controllers and fixture behavior only; it must
    never create namespaces, interfaces, routes, firewall rules, or public
    probes.
13. VPN key input must not place key values in command arguments, process
    listings, repository content, or normal output; mismatched pairs must leave
    existing state unchanged.
14. Reachability is never target authority, and missing routes are never proof
    of containment.
15. Any topology or fault experiment must bind a named experiment identity and
    emit independently observable events.
16. Do not describe Network World modeled effects as packet-enforced facts.
17. Do not implement automatic route, DNS, VPN, or firewall mutation before
    Task-level requirement, evidence, invalidation, and recovery semantics are
    proven.
18. Do not create a universal Agent communication identity by relabeling current
    world, node, endpoint, certificate, or route identities.
19. Do not standardize or promote Connectivity vocabulary from documentation
    alone.
20. Do not merge Edge and Link lifecycle or state; compose them only through
    explicit foreign references after real Host workloads require it.

## Required checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```
