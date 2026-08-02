# Agent instructions

This directory contains private network operator tools, not a network abstraction or default data plane.

Retain only behavior used on the current workstation:

- isolated WireGuard namespace creation and teardown;
- canonical key/profile validation;
- nested Windows VPN rejection;
- Surfshark path measurement and profile ranking;
- atomic local evidence and recovery.

Do not add automatic route selection, failover, generic protocol layers, topology models, dashboards, databases, or background services without a named current workload.

Run `scripts/check-vpn-controller` after changes.
