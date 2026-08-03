---
schema_version: 1
id: world.authority
title: World Content Authority
type: decision
profile: organization
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
updated: 2026-08-03
summary: Decision separating World's repository boundary, callable Cloudflare capabilities, provider operation and release contracts, private workstation procedures, machine truth, and archived experiments.
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.start
  - world.boundaries
  - world.cloudflare.capabilities
  - world.cloudflare.operations
  - world.cloudflare.reliability
  - world.cloudflare.security
  - world.cloudflare.release
  - world.network-tools
  - world.vpn-namespace
---
# World Content Authority

## Context

World contains one active Cloudflare provider, one private network-operator module, retained-boundary decisions, provider capability and operations documents, release and reliability contracts, installation procedures, tests, configuration, private receipts, and an archive of removed World, Link, Edge, WCP, WXP, QUIC, and network experiments. These sources have different authority.

## Decision

[`../README.md`](../README.md) is the repository entry. [`retained-boundaries.md`](retained-boundaries.md) owns the active repository scope and reactivation rule. [`../providers/cloudflare/README.md`](../providers/cloudflare/README.md) owns the supported provider capability surface. Its `docs/operations.md`, `reliability.md`, `security.md`, and `release.md` own operation, failure, protection, release, and rollback contracts. [`../modules/network-observation/README.md`](../modules/network-observation/README.md) and its [`vpn-namespace.md`](../modules/network-observation/docs/vpn-namespace.md) own the current private workstation tools and procedure.

Deployed Cloudflare capability output, Worker Version and Deployment state, authoritative R2 request objects, committed Receipts, Artifact metadata and bytes, effective bindings, source-input digests, exact local configuration, systemd state, WireGuard and namespace state, tests, and private operation receipts remain stronger owners for current machine and provider facts. [`archive/world-negative-experiments.md`](archive/world-negative-experiments.md) is historical reproduction authority only and cannot reactivate removed layers.

## Consequences

Only the retained capability and operations set enters strict content management. Historical experiments, negative results, and removed architecture remain available without bulk conversion. Later human-centered reconstruction may simplify operator guides and provider concepts, but it must preserve exact machine contracts, private/public separation, and explicit supersession rather than replacing executable truth with prose.

## Status

Accepted and active. Reopen when a callable capability changes, the private workstation environment changes, a mature tool replaces retained behavior, or a deleted World component is admitted under the reactivation rule.
