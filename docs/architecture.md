# Architecture

## Boundary

Ordivon Edge / Link owns observation, selection, deployment, verification, failover, and recovery. Mature TLS, QUIC, certificate validation, and proxy implementations remain replaceable dependencies.

```text
Target registry + network label + route label
                       │
                       ▼
                   edge-probe
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
 reachability       transfer     connection lifetime
       │               │                │
       └───────────────┴────────────────┘
                       ▼
              ProbeResult NDJSON
                       │
               ┌───────┴────────┐
               ▼                ▼
          compare JSON      report Markdown
```

The wire-level TLS and QUIC behavior is delegated to the system `curl` build. Ordivon owns the target declaration, collection semantics, observation schema, failure classification, aggregation, and future path decision logic.

## Minimum domain model

- `Device`: a client under the user's control.
- `Edge`: a future overseas execution or transport endpoint.
- `Target`: a real service whose reachability matters.
- `Transport`: a replaceable data-plane implementation and protocol.
- `ProbeResult`: one immutable observation from one target, network, route, protocol, probe kind, and collection round.
- `RouteDecision`: a future explainable selection result; modeled but not executed in P1.

## Probe kinds

### Reachability

Issues an HTTP HEAD request and measures DNS, connect, TLS/QUIC, TTFB, response status, and completion without downloading the response body. Any HTTP response status from 100 through 599 proves an HTTP response was reached; it does not imply application authorization or business success.

### Transfer

Downloads a declared object to `/dev/null` and requires a completed response with non-zero bytes. It records bytes and average download throughput. It is not a full congestion-control benchmark.

### Connection lifetime

Uses a sufficiently large object plus a configured rate limit to keep one response-body connection active. Reaching at least 95% of the requested duration with one connection and non-zero bytes is success. Curl deadline exit 28 is expected when the requested duration is reached.

This test does not cover idle timeout, bidirectional streams, path migration, or recovery after interface changes.

## Timing and transfer fields

All timings are milliseconds:

- `dns_ms`: name resolution;
- `connect_ms`: transport connection after DNS;
- `tls_ms`: TLS handshake after transport connect;
- `ttfb_ms`: cumulative start-to-first-byte time;
- `total_ms`: cumulative completion or deadline time.

Additional fields include downloaded bytes, average bytes per second, connection count, HTTP version, requested duration, collection identity, and sample index. Values may be absent when a failure occurs before a phase completes.

## Failure model

The intentionally small taxonomy is:

- `configuration`;
- `dns`;
- `tcp_connect`;
- `tls_handshake`;
- `quic_handshake`;
- `http`;
- `transfer`;
- `connection_lifetime`;
- `timeout`;
- `tool`;
- `unknown`.

It classifies the observed failure surface and does not claim a deeper root cause without additional evidence.

## Trust boundary

P1 does not handle secrets or mutate networking. Future credentials must remain outside Git. Raw evidence can reveal IP addresses, timestamps, route labels, and service availability, so baseline artifacts remain ignored by default.

The project is for lawful administration of user-controlled personal infrastructure. It does not provide public proxy access, multi-user subscriptions, traffic resale, credential interception, or unreviewed cryptographic mechanisms.
