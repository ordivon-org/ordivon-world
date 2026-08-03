---
schema_version: 1
id: world.network-tools
title: Ordivon Network Operator Tools
type: reference
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
summary: Canonical reference for workstation-specific WireGuard namespace, key installation, Surfshark measurement, profile scanning, explicit invocation, and deletion conditions.
evidence_status: verified
readiness: READY
applies_to:
  - modules/network-observation
related:
  - world.vpn-namespace
  - world.boundaries
  - world.authority
---
# Ordivon Network Operator Tools

## Scope

Define the retained private commands used to inspect and explicitly control selected VPN paths on the current Windows and WSL workstation without changing the WSL root route automatically.

## Contract

`ordivon-vpn` creates and removes the isolated namespace; `ordivon-vpn-keypair` validates and atomically installs the canonical key and rendered profiles; Surfshark tools capture bounded before-and-after evidence and validate or rank profiles. Every action is explicit, privileged where required, and leaves private recovery evidence.

## Errors

Fail on active nested Windows VPN state, key and profile inconsistency, unsafe namespace topology, partial setup, invalid permissions, mislabeled measurements, interrupted or conflicting scan state, or any attempt to mutate the default route implicitly.

## Compatibility

The tools apply only to the current Windows, WSL, Surfshark, WireGuard, systemd, and private evidence layout. Delete or replace them when that environment disappears or a maintained tool provides the same state checks, namespace ordering, atomic key handling, recovery, and evidence behavior.

This module contains explicit private tools used to inspect and control VPN paths on the current Windows/WSL workstation.

## Retained commands

- `ordivon-vpn` — create an isolated WireGuard namespace without changing the WSL root route;
- `ordivon-vpn-keypair` — validate and atomically install the canonical key pair and rendered profiles;
- `surfshark-measure` — compare Windows/WSL route state before and after Surfshark connection;
- `surfshark-profile-scan` — validate, probe, resume, and rank profiles;
- `install-ordivon-vpn` — install commands and the namespace service.

These tools remain because generic WireGuard and network utilities do not encode the current Windows service state, nested-VPN rejection, key/profile consistency, namespace birth ordering, evidence locations, and recovery procedure.

They are not a World routing layer and never select or mutate the default path automatically.

See `docs/vpn-namespace.md`.
