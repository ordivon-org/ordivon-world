# Isolated VPN namespace

Ordivon Link can provide an explicit, local-only WireGuard execution path without changing the WSL root namespace default route.

```text
WSL root namespace
├─ Ordivon Runtime
├─ Ordivon MCP / cloudflared
└─ WireGuard encrypted UDP socket
   └─ moved wg0 interface in ordivon-vpn namespace
      └─ explicitly selected commands only
```

## Security boundary

- WireGuard configuration files remain outside Git under `/root/.config/ordivon/secrets/surfshark/rendered`.
- Every configuration must be a regular `0600` file and must contain a real locally retained private key. `doctor` also derives its public key and requires it to match the canonical `ordivon-manual` key pair before `up` is admitted.
- The controller never prints keys, peer public keys, endpoint hostnames, or endpoint addresses.
- Runtime, MCP, and Cloudflare Tunnel remain in the root namespace.
- No automatic failover or route selection is enabled.
- Windows Surfshark must be disconnected before `up`; the controller rejects nested VPN startup.
- The WireGuard interface is created in the WSL root namespace and then moved; its encrypted UDP socket remains in the root namespace while cleartext routes exist only inside `ordivon-vpn`.
- The controller does not create a veth pair, enable IP forwarding, add NAT, or modify Docker/host firewall rules.
- Only one `ordivon-vpn` namespace is active at a time.

## Install

```bash
sudo scripts/install-ordivon-vpn
```

Install or replace the Surfshark key pair interactively:

```bash
sudo ordivon-vpn-keypair
```

Paste the Surfshark public key at the first prompt. Paste the matching private key at the second prompt; input is hidden. The script validates that both keys form one WireGuard pair, backs up the previous local state, renders every downloaded profile, and never prints either key. A mismatch changes nothing.

Then validate a profile:

```bash
ordivon-vpn doctor jp-tok
```

`doctor` reports whether Windows Surfshark is currently active. Disconnect it before starting the namespace.

## Operate

```bash
sudo ordivon-vpn up jp-tok
ordivon-vpn status
sudo ordivon-vpn exec curl -fsS https://www.cloudflare.com/cdn-cgi/trace
sudo ordivon-vpn exec git clone https://github.com/example/example.git
sudo ordivon-vpn down
```

The `exec` subcommand replaces itself with `ip netns exec`; command exit status is preserved. The namespace contains only loopback and the moved WireGuard interface.

A manual systemd instance is also available:

```bash
sudo systemctl start ordivon-vpn@jp-tok.service
sudo systemctl stop ordivon-vpn@jp-tok.service
```

The unit is installed but not enabled automatically.

## Recovery

`up` is transactional. Any failure before verified WireGuard handshake and HTTPS egress removes the namespace, any not-yet-moved WireGuard interface, resolver file, state, and temporary stripped configuration.

`down` is idempotent and may be used after an interrupted invocation:

```bash
sudo ordivon-vpn down
```

Raw configuration, endpoint, route, and public-egress evidence must not be committed.

## Surfshark before/after measurement

Capture a VPN-disconnected baseline, a connected sample, and a reduced comparison without storing key values:

```bash
sudo surfshark-measure before
# Connect Surfshark in Windows and wait 15–20 seconds.
sudo surfshark-measure after
sudo surfshark-measure compare
```

`before` is rejected while the Windows WireGuard service or adapter is active; `after` is rejected until both are active. Raw local evidence remains root-only under `/root/backups/ordivon-link/surfshark-measure`.

## Surfshark profile discovery and ranking

The profile scanner is a separate measurement utility, not part of the always-on VPN controller. It sequentially creates the same birth-namespace WireGuard topology for each rendered profile, records whether endpoint UDP returns, and benchmarks only profiles that complete a WireGuard handshake.

Validate the complete local profile inventory without changing network state:

```bash
sudo surfshark-profile-scan validate
```

Disconnect Windows Surfshark, wait for the adapter to go down, and run the full discovery pass:

```bash
sudo surfshark-profile-scan scan
```

Defaults:

- all rendered profiles, sorted deterministically;
- one profile at a time;
- 12-second handshake deadline;
- HTTPS timing plus a 1 MiB download only after a successful handshake;
- no root-route, NAT, forwarding, or firewall changes.

Each profile result is written atomically under `/root/backups/ordivon-link/surfshark-profile-scan/<timestamp>/profiles`. An interrupted run can continue without repeating completed profiles:

```bash
sudo surfshark-profile-scan scan --resume /root/backups/ordivon-link/surfshark-profile-scan/<timestamp>
```

Reduced outputs include `summary.json`, `results.jsonl`, `results.csv`, and `ranking.csv`. Endpoint names and addresses are represented only by local fingerprints; keys are never printed or persisted in results. Show the current ranking with:

```bash
surfshark-profile-scan rank
```

The first pass is discovery evidence, not a permanent latency claim. Re-run leading profiles at different times before making an automatic selection policy.
