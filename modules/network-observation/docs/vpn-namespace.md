---
schema_version: 1
id: world.vpn-namespace
title: Isolated VPN namespace
type: operations
profile: engineering
lifecycle: active
source_role: canonical
visibility: private
owners:
  - ordivon-world
  - workstation-operator
audience:
  - operator
  - builder
  - agent
updated: 2026-08-03
summary: Canonical operating and recovery procedure for an explicit WireGuard namespace that preserves the WSL root route and records bounded private evidence.
evidence_status: verified
readiness: READY
applies_to:
  - modules/network-observation
related:
  - world.network-tools
  - world.boundaries
  - world.authority
---
# Isolated VPN namespace

## Scope

Provide a selected-command WireGuard path inside `ordivon-vpn` while Runtime, MCP, Cloudflare Tunnel, and ordinary WSL traffic remain on the root namespace and route.

## Normal operation

Install the tools and canonical key pair, run `doctor`, explicitly bring up one named profile, inspect status, execute only selected commands inside the namespace, and bring the namespace down after use. Profile measurement and scanning remain separate explicit operations.

## Failure detection

Detect active Windows Surfshark, WireGuard, or OpenVPN tunnels; key or profile mismatch; missing dependencies; namespace, interface, or route divergence; partial setup; invalid private-file permissions; mislabeled samples; unsafe endpoint data; and interrupted scans.

## Recovery

`up` is transactional and cleans partial state. `down` is idempotent and is the primary recovery action after interruption. The namespace service is installed but never enabled automatically. Raw evidence remains under private backup paths and never contains exported secret keys.

## Verification

Use `ordivon-vpn doctor`, status inspection, root-route comparison, selected-command Cloudflare trace, key-pair and rendered-profile validation, bounded handshake probes, private evidence review, focused tests, shell syntax checks, systemd unit validation, and secret scanning. [`../README.md`](../README.md) defines the command contract, [`../../../docs/retained-boundaries.md`](../../../docs/retained-boundaries.md) defines retention, and [`../../../docs/authority.md`](../../../docs/authority.md) records authority.

These tools provide an explicit WireGuard path for selected commands without replacing the WSL root route used by Ordivon Runtime, MCP, and Cloudflare Tunnel.

```text
WSL root namespace
├─ Runtime / MCP / cloudflared
└─ WireGuard encrypted UDP socket
   └─ moved interface inside `ordivon-vpn`
      └─ explicitly selected commands
```

## Why this code remains

Generic `wg` and `ip netns` commands do not preserve the complete local invariant:

- reject an active Windows Surfshark, WireGuard, or OpenVPN tunnel;
- derive every rendered profile from one canonical local key pair;
- create WireGuard in the root namespace before moving the interface, preserving the encrypted socket path;
- avoid veth, NAT, IP forwarding, firewall, and root-route mutation;
- clean all partial state after failure;
- record bounded private evidence for later diagnosis.

Deleting these scripts would return operation to an undocumented sequence of privileged commands with materially higher recovery risk.

## Install and keys

```bash
sudo scripts/install-ordivon-vpn
sudo ordivon-vpn-keypair
ordivon-vpn doctor jp-tok
```

Keys and rendered profiles remain outside Git under `/root/.config/ordivon/secrets/surfshark/`. The installer validates permissions and key-pair consistency before atomically replacing local state.

## Operate

```bash
sudo ordivon-vpn up jp-tok
ordivon-vpn status
sudo ordivon-vpn exec curl -fsS https://www.cloudflare.com/cdn-cgi/trace
sudo ordivon-vpn down
```

`up` is transactional. `down` is idempotent and is the recovery action after an interrupted operation. The optional `ordivon-vpn@.service` is installed but never enabled automatically.

## Measure Windows Surfshark

```bash
sudo surfshark-measure before
# Connect Surfshark in Windows and wait for the adapter to become active.
sudo surfshark-measure after
sudo surfshark-measure compare
```

The command rejects mislabeled samples and stores raw local evidence only under `/root/backups/ordivon-link/surfshark-measure`.

## Discover profiles

```bash
sudo surfshark-profile-scan validate
sudo surfshark-profile-scan scan
surfshark-profile-scan rank
```

Discovery uses bounded parallel handshake workers; throughput benchmarking is serial to avoid self-contention. Interrupted scans resume from their private output directory. The tool reports local fingerprints rather than keys or endpoint addresses and never changes the default route or selects a profile automatically.

## Deletion condition

Delete the module when the workstation no longer uses Surfshark/WireGuard profiles or when a maintained tool demonstrably provides the same Windows-state checks, namespace topology, atomic key/profile handling, recovery, and evidence behavior.
