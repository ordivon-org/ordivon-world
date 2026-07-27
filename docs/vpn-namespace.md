# Isolated VPN namespace

Ordivon Link can provide an explicit, local-only WireGuard execution path without changing the WSL root namespace default route.

```text
WSL root namespace
├─ Ordivon Runtime
├─ Ordivon MCP / cloudflared
└─ veth + NAT
   └─ ordivon-vpn namespace
      └─ WireGuard
         └─ explicitly selected commands only
```

## Security boundary

- WireGuard configuration files remain outside Git under `/root/.config/ordivon/secrets/surfshark/rendered`.
- Every configuration must be a regular `0600` file and must contain a real locally retained private key.
- The controller never prints keys, peer public keys, endpoint hostnames, or endpoint addresses.
- Runtime, MCP, and Cloudflare Tunnel remain in the root namespace.
- No automatic failover or route selection is enabled.
- Only one `ordivon-vpn` namespace is active at a time.

## Install

```bash
sudo scripts/install-ordivon-vpn
ordivon-vpn doctor jp-tok
```

## Operate

```bash
sudo ordivon-vpn up jp-tok
ordivon-vpn status
sudo ordivon-vpn exec curl -fsS https://www.cloudflare.com/cdn-cgi/trace
sudo ordivon-vpn exec git clone https://github.com/example/example.git
sudo ordivon-vpn down
```

The `exec` subcommand replaces itself with `ip netns exec`; command exit status is preserved.

A manual systemd instance is also available:

```bash
sudo systemctl start ordivon-vpn@jp-tok.service
sudo systemctl stop ordivon-vpn@jp-tok.service
```

The unit is installed but not enabled automatically.

## Recovery

`up` is transactional. Any failure before verified WireGuard handshake and HTTPS egress removes the namespace, veth, nftables tables, resolver file, temporary stripped configuration, and restores the previous IPv4 forwarding value.

`down` is idempotent and may be used after an interrupted invocation:

```bash
sudo ordivon-vpn down
```

Raw configuration, endpoint, route, and public-egress evidence must not be committed.
