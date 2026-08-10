---
schema_version: 1
id: world.boundaries
title: Retained Boundaries After A11 Reduction
type: decision
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - operator
  - agent
updated: 2026-08-04
summary: Decision retaining direct Host-facing provider adapters and private network tools while continuing to reject an independent World runtime or universal interaction layer.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.start
  - world.authority
---
# Retained Boundaries After A11 Reduction

## Original reduction

World previously accumulated provider, network, capability-program, control, protocol, console, experiment and generated-governance structures. Most had no active consumer and duplicated Host, Runtime, provider, network-substrate or domain responsibility.

A11 therefore retained only:

1. the Cloudflare provider implementation and its provider-local recovery controls;
2. private network operator tools whose Windows/WSL/Surfshark behavior was not captured by ordinary commands.

It deleted the proposed independent World correlation layer because Host plus direct provider and observation adapters prevented the same failures with less state.

## Current reactivation

P0–P2 does **not** reverse the absorb decision. It reactivates and strengthens the missing direct-integration seam required by the named current Fetch and Browser workloads:

```text
Host Dispatch
→ Cloudflare request
→ provider Receipt / Artifact
→ Host Observation
→ independent Verification
```

The retained Python package is an adapter and Host extension, not a World service. It adds no daemon, database, workflow engine, provider scheduler, callback authority, global World ID or universal interaction object.

The reactivated responsibility is admitted because its absence reproduced concrete failures:

- the Cloudflare provider had no production Host consumer;
- provider Receipt and Artifact facts did not enter Host continuity;
- a response-lost external action could not be recovered from a fresh Host through a repository-owned path;
- current capability conditions were not bound to Host Dispatch identity;
- provider and Python contract surfaces could drift independently.

## Retained Cloudflare responsibilities

- HMAC authentication and bounded request bodies;
- exact Request ID/input binding;
- pending state, generation-fenced leases, committed Receipts and replay;
- allowlisted Fetch and same-origin Browser Snapshot execution;
- private R2 Artifacts with digest and byte verification;
- source-input release identity, candidate deployment and rollback;
- lifecycle and deferred cleanup;
- current R2 API contract tests.

Cloudflare remains authoritative for provider state. World maps those facts but does not duplicate their lifecycle.

## Retained Host-facing responsibilities

- validate current capabilities and derive a condition digest;
- derive a deterministic provider request ID from one Host Dispatch;
- persist prepared intent before delivery;
- record transport uncertainty as UNKNOWN;
- reconstruct the original request after Host replacement;
- query, validate and map the original provider Receipt;
- map R2 Artifacts into Host `ArtifactRef` values;
- verify Browser screenshot, rendered HTML and Manifest as one generation-scoped bundle;
- preserve Task state and Ready Frontier while appending opaque extension facts;
- keep provider success separate from Host Verification and completion.

## Retained network responsibilities

- explicit `ordivon-vpn` and key-pair operations;
- isolated WireGuard namespace topology;
- Surfshark before/after measurement;
- profile validation, discovery and bounded ranking;
- focused secret, key, namespace and scheduler tests.

Network mutation remains operator-only. HP0 removed the previously reserved `network-observation` public Schema because no current producer or independent consumer used it; owner-local `ordivon-vpn`/Surfshark reports remain operational evidence rather than a speculative shared contract. Local VPN or route observations are not required state for remote Cloudflare Fetch or Browser execution because no measured failure shows that local path identity changes the semantics of the already-bound remote operation.

## Still removed

- independent World daemon or database;
- provider broker, automatic router and untriggered provider rebinding;
- capability registry beyond live provider discovery;
- callback, queue, fan-out or join orchestration;
- general MCP, RAG, Sandbox or connector platform;
- historical Rust World, Link, Edge, WCP, WXP, QUIC and wire layers;
- default replay of closed research experiments;
- duplicated Task, workflow, identity or verification models.

## Release and evidence

Release admission is based on the facts that changed:

- Worker deployment uses Worker-input digest, not repository ceremony;
- Python distribution uses exact Host/Protocol pins and packaged Schemas;
- operator controllers must match installed file digests;
- effect/recovery changes require a clean commit-bound live W1 receipt;
- CI proves portable source behavior but cannot prove live provider or machine health.

## Reactivation rule

Another deleted component may return only when a named current workload demonstrates all of the following:

1. absence causes a reproduced failure, duplicated Effect, false completion, unrecoverable uncertainty, authority confusion or material manual recovery cost;
2. Host, Runtime, the provider, operating system or domain authority cannot own the responsibility more cleanly;
3. at least two real consumers need the same retained semantics before a shared abstraction is introduced;
4. total implementation and operating cost is lower than direct adapters;
5. every retained field and service has a deletion condition.
