# Ordivon Network Operator Tools

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
