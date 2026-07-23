# Privacy boundary

Ordivon Edge is private by default.

## Data not retained

The read-only Web plane does not persist or return:

- public or private IP addresses;
- remote endpoint IP addresses;
- usernames, hostnames, account paths, or device names;
- MAC addresses;
- raw route, adapter, DNS, PowerShell, systemd, process, or probe output;
- service target URLs;
- probe stderr fragments;
- Surfshark credentials, keys, configuration files, or account details.

The observer extracts only the minimum booleans, categories, timings, and protocol labels needed to reduce state. Raw command output is dropped in memory immediately after parsing.

## Network exposure

The default bind is:

```text
127.0.0.1:8787
```

Non-loopback addresses are rejected in this phase. A reverse proxy or tunnel must connect to the loopback listener; the Edge process itself cannot bind publicly.

The repository does not create a Cloudflare Tunnel route for the Web UI. Remote exposure must add authentication, authorization, audit, and a separate review of which fields may leave the host.

## Browser controls

The server returns:

- a same-origin-only Content Security Policy;
- `frame-ancestors 'none'` and `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Cache-Control: no-store`;
- disabled camera, microphone, geolocation, and payment browser permissions;
- no external scripts, fonts, analytics, trackers, or CDNs.

## Storage

The SQLite database contains sanitized snapshots, service checks, and state-change events. It remains private host data and should be backed up with the same controls as other Ordivon state.

Automated tests reject known identity-bearing field names. Operational validation additionally scans API and event responses for IPv4 literals and forbidden fields.
