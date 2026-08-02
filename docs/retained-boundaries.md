# Retained Boundaries After A11 Reduction

Date: 2026-08-02

## Decision

World remains a repository boundary for two concrete capabilities, not a runtime layer:

1. the Cloudflare provider adapter;
2. private network operator tools.

Everything else is restored from Git only when a named workload reopens it.

## Cloudflare provider

### Retained

- HMAC request authentication and bounded request bodies;
- exact Request ID/input binding;
- pending state, fenced leases, committed Receipts, replay, and reconciliation;
- allowlisted Fetch and same-origin Browser execution;
- private R2 Artifacts with digest and byte verification;
- source-input digest release identity, candidate deployment, rollback, and GC;
- policy/binding/lifecycle checks where configuration is duplicated by Cloudflare contracts.

### Non-replaceable effect

Removing these mechanisms can duplicate an external Effect after response loss, accept a stale executor, expose private Artifact bytes, publish an unbuildable Worker, or make rollback ambiguous. Cloudflare primitives remain authoritative; the adapter only binds them to Ordivon's signed request and Receipt contract.

### Removed

- `evidence.run` and the Cloudflare Workflow resource: no persistent Computer, Host, Harness, Web, service, timer, or automation consumed it;
- capability portfolio and generated closeout machinery;
- historical local Node/research-control implementation;
- lexical boundary checks;
- W0/W1/WCP/WXP replay in default CI.

## Network operator tools

### Retained

- `ordivon-vpn` and key-pair installer;
- isolated namespace systemd unit;
- Surfshark before/after measurement;
- profile validation, discovery, and bounded ranking;
- their focused tests and secret scan.

### Non-replaceable effect

The tools encode this workstation's WSL/Windows/VPN interaction, reject nested VPN startup, preserve the root route, validate a canonical WireGuard identity, and leave recovery evidence. Replacing them with generic `wg` commands would lose these machine-specific invariants.

### Removed

- unused Rust observation, console, model, protocol, QUIC, wire, and Network World crates;
- protocol and architecture documents with no active executable consumer;
- generated capability declaration.

## Release validation

Release admission is based on Worker input digest, not repository ceremony. A branch, detached commit, or unrelated documentation change is acceptable. Dirty Worker inputs remain forbidden because they cannot be reconstructed.

A release is a no-op when the active Worker already carries the same Worker-input digest. When code changes, health and capability identity are always checked; Fetch and Browser smokes run only when their own path or shared runtime code changed. One matching deployed observation is sufficient; repeated identical health probes do not prove additional correctness.

## Reactivation rule

A deleted component may return only when a named current workload demonstrates:

- a responsibility not owned by Host, Runtime, Provider, network substrate, or domain authority;
- failure when the component is absent;
- net acceleration after permanent maintenance and operator cost;
- a deletion condition.
