---
schema_version: 1
id: world.start
title: Ordivon World
type: start
profile: organization
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - builder
  - operator
  - agent
updated: 2026-08-03
summary: Canonical entry to World's retained Cloudflare provider adapter and private network operator tools after removal of unused semantic and experimental layers.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.boundaries
  - world.cloudflare.capabilities
  - world.cloudflare.operations
  - world.cloudflare.reliability
  - world.cloudflare.security
  - world.cloudflare.release
  - world.network-tools
  - world.vpn-namespace
  - world.authority
---
# Ordivon World

## Purpose

Carry only the external provider adapters and private operator tools that still serve current Ordivon work and whose machine- or provider-specific recovery semantics cannot be replaced by ordinary libraries or undocumented commands.

## Start here

- [`docs/retained-boundaries.md`](docs/retained-boundaries.md) records what survived A11 reduction and why.
- [`providers/cloudflare/README.md`](providers/cloudflare/README.md) defines callable Cloudflare capabilities and authority.
- [`providers/cloudflare/docs/operations.md`](providers/cloudflare/docs/operations.md), [`reliability.md`](providers/cloudflare/docs/reliability.md), [`security.md`](providers/cloudflare/docs/security.md), and [`release.md`](providers/cloudflare/docs/release.md) define operation, uncertainty, protection, release, and rollback.
- [`modules/network-observation/README.md`](modules/network-observation/README.md) defines the retained private network tools.
- [`modules/network-observation/docs/vpn-namespace.md`](modules/network-observation/docs/vpn-namespace.md) defines their privileged operating and recovery procedure.
- [`docs/authority.md`](docs/authority.md) separates callable capability, operator procedure, machine truth, and archived experiments.

## Current boundary

World is a repository boundary, not an independent service or semantic layer. Its active scope is one Cloudflare provider adapter plus workstation-specific network operator tools. Host owns Task and commitment meaning, Runtime owns local physical execution, Cloudflare owns remote Worker and R2 state, and operators explicitly invoke private network changes.

Ordivon World carries the external adapters and private operator tools that still serve current Ordivon work. It is not an independent semantic layer.

## Active components

### Cloudflare provider

`providers/cloudflare/` supplies signed, bounded Fetch and Browser operations, private R2 Artifacts, replayable Receipts, release/rollback, and garbage collection.

Its non-replaceable role is narrow: Cloudflare owns the remote execution, Worker version, request state, Receipt, and R2 object. Host retains Task, Effect, uncertainty, Verification, and completion.

### Network operator tools

`modules/network-observation/` retains explicit VPN and Surfshark measurement tools used on this workstation. They create an isolated WireGuard namespace, validate key/profile consistency, and measure paths without silently changing the WSL root route.

Their non-replaceable role is operational rather than architectural: current generic network libraries do not contain this machine's Windows/WSL/Surfshark coordination and recovery procedure.

## Deliberately absent

The repository has no World service, database, workflow engine, callback authority, provider broker, router, universal interaction schema, capability registry, or active historical experiment framework.

Completed W0/W1/WCP/WXP experiments, negative results, imported Edge/Link prototypes, Node-control research, QUIC/wire experiments, and Network World implementations remain outside active `main`. [`docs/archive/world-negative-experiments.md`](docs/archive/world-negative-experiments.md) binds the final revision and reproduction commands; default CI does not replay closed architecture decisions.

## Why each active check remains

| Check | Failure it prevents | Why ordinary source review is insufficient | Deletion condition |
|---|---|---|---|
| Provider typecheck and unit tests | malformed request/Receipt contracts, duplicate Effects, lease and replay regressions | these failures appear only across state transitions and failure injection | delete a test when its production path or failure class is deleted |
| Policy coupling check | Worker bindings, allowlists, rate limits, and retention silently disagree | values exist in Cloudflare and local policy surfaces | delete after one generated or authoritative configuration replaces duplicates |
| Wrangler dry run | deploy bundle or binding cannot be constructed | TypeScript success does not validate Wrangler configuration | delete only if deployment itself performs an equivalent zero-effect build |
| Operation installer checks | broken shell syntax or invalid systemd units | these files are outside TypeScript tests | delete with the installer/timer |
| VPN tool checks | key/profile mismatch or unsafe topology regression | behavior crosses shell, WireGuard, namespace, and Windows state | delete when the private VPN tools are removed |
| Release candidate smoke | the uploaded Worker version cannot execute the changed capability | local tests cannot prove the deployed Cloudflare version and bindings | run only for changed capabilities; delete with remote release control |

See [`docs/retained-boundaries.md`](docs/retained-boundaries.md).
