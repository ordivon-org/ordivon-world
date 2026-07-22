# Architecture

## Boundary

Ordivon Edge / Link owns observation, selection, deployment, verification, failover, and recovery. Mature TLS, QUIC, certificate validation, and proxy implementations remain replaceable dependencies.

```text
Target registry + route label + network label
                     │
                     ▼
                 edge-probe
          ┌──────────┴──────────┐
          │                     │
   HTTP/1.1 + TLS        HTTP/3-only + QUIC
          │                     │
          └──────────┬──────────┘
                     ▼
              ProbeResult NDJSON
                     │
             ┌───────┴────────┐
             ▼                ▼
        compare JSON      report Markdown
```

The initial probe adapter delegates wire-level TLS and QUIC behavior to the system `curl` build. This deliberately avoids an immature in-repository TLS or QUIC implementation while preserving a stable Ordivon observation schema.

## Minimum domain model

- `Device`: a client under the user's control.
- `Edge`: a future overseas execution or transport endpoint.
- `Target`: a real service whose reachability matters.
- `Transport`: a replaceable data-plane implementation and protocol.
- `ProbeResult`: one immutable observation from one target, network, route, and protocol.
- `RouteDecision`: a future explainable selection result; modeled now but not executed in Phase 1.

## Timing semantics

All timing values are milliseconds:

- `dns_ms`: name-resolution phase;
- `connect_ms`: transport-connect phase after DNS;
- `tls_ms`: TLS handshake phase after transport connect;
- `ttfb_ms`: cumulative time from start to first response byte;
- `total_ms`: cumulative time from start to completion.

Values may be absent when a failure happens before a phase completes.

## Failure model

The initial taxonomy is intentionally small:

- `configuration`;
- `dns`;
- `tcp_connect`;
- `tls_handshake`;
- `quic_handshake`;
- `http`;
- `timeout`;
- `tool`;
- `unknown`.

This taxonomy classifies the observed failure surface. It does not claim root cause beyond the available evidence.

## Threat and trust boundary

Phase 1 does not handle secrets and does not mutate network configuration. Future node credentials must live outside Git. Probe output can reveal timing, route labels, IP addresses, and service availability; raw personal baselines remain ignored by default and should be published only after review and redaction.

The project is for lawful administration of user-controlled personal infrastructure. It does not provide public proxy access, multi-user subscriptions, traffic resale, credential interception, or unreviewed cryptographic mechanisms.
