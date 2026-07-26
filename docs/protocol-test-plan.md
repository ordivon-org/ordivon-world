# Ordivon Baseline v0 test plan

## Test philosophy

A passing test must prove one narrow claim. A failing test must not be promoted into a deeper causal claim without controls.

The wire contract and localhost QUIC integration are implemented. Public endpoints, production credentials, and external-route claims remain outside the current phase.

## Stage 0 — pure wire and state tests

Mandatory and network-independent:

- QUIC varint boundary round trips;
- rejection above the QUIC integer limit;
- control-frame encode/decode round trips;
- negotiated limit round trips;
- domain validation;
- address encoding for domain, IPv4, and IPv6;
- unknown critical frame rejection;
- unknown non-critical frame preservation/skipping;
- TCP open and response encoding;
- UDP payload hard-cap enforcement;
- legal connection, TCP relay, and UDP association transitions;
- rejection of illegal transitions;
- no parser panic for arbitrary bounded bytes once fuzzing is added.

## Stage 1 — localhost QUIC reference implementation

No public node and no system route changes.

```text
client process
  ↔ localhost UDP/QUIC + mTLS
  ↔ server process
  ↔ local TCP echo / UDP echo targets
```

Acceptance:

1. wrong ALPN rejected;
2. missing or untrusted client certificate rejected;
3. a trusted certificate with a mismatched `HELLO.device_id` is rejected with an observable authentication error;
4. `HELLO` / `HELLO_OK` succeeds;
5. TCP strict-open relay succeeds;
6. target refusal, timeout, and DNS failure map to stable codes;
7. TCP half-close behaves correctly;
8. UDP association and message boundaries work;
9. resource limits reject excess work without affecting existing relays;
10. connection close releases all state;
11. no 0-RTT application data accepted.

## Stage 2 — local impairment

Use a controlled Linux network namespace or equivalent environment. Do not infer impairment from an uncontrolled public network.

Variables:

- latency;
- jitter;
- packet loss;
- packet reordering;
- bandwidth limit;
- MTU reduction and black-hole behavior;
- NAT idle expiry;
- abrupt server close.

Evidence:

- handshake success and duration;
- initial and smoothed RTT when available;
- TCP open success and time;
- transfer completion and throughput;
- active and idle session lifetime;
- UDP sent/received counts;
- disconnect and reconnect time;
- stable close/error reason.

## Stage 3 — public Edge path matrix

The same Edge build, certificate policy, port, and target set must be tested under named paths.

| Test ID | Local route | Destination | Protocol | Claim if successful |
|---|---|---|---|---|
| C1 | direct-no-vpn | Cloudflare-hosted control hostname | HTTP/3 | ordinary QUIC/UDP 443 reached Cloudflare during this window |
| C2 | direct-no-vpn | direct Edge, same IP as Baseline | HTTPS/TCP control | Edge IP and TCP path were reachable |
| B1 | direct-no-vpn | direct Edge | Baseline custom QUIC | custom direct QUIC handshake and authenticated session worked |
| C3 | surfshark-vpn | Cloudflare-hosted control hostname | HTTP/3 | VPN path reached Cloudflare HTTP/3 |
| C4 | surfshark-vpn | direct Edge, same IP | HTTPS/TCP control | VPN path reached Edge over TCP |
| B2 | surfshark-vpn | direct Edge | Baseline custom QUIC | known-via-VPN Baseline path worked |

`direct-no-vpn` and `surfshark-vpn` labels are controlled route facts only when the corresponding route is explicitly verified. They are not inferred from proxy environment variables.

## Interpretation matrix

| C1 | C2 | B1 | Interpretation |
|---:|---:|---:|---|
| fail | fail | fail | broad direct path failure; no protocol conclusion |
| pass | fail | fail | Cloudflare path works, direct Edge address/path does not |
| pass | pass | fail | direct TCP and Cloudflare QUIC work; Baseline UDP/custom-QUIC path is specifically suspect |
| pass | pass | pass | one direct Baseline sample succeeded; repeat before any availability claim |

A single success never proves long-term reachability. A single failure never proves UDP is categorically blocked.

## Stage 4 — repeated comparison

Minimum evidence before discussing Surfshark replacement:

- multiple time windows across at least seven days;
- both available carriers where practical;
- handshake success rate;
- P50/P95 handshake and TCP-open latency;
- transfer completion and throughput;
- active and idle session lifetime;
- reconnect behavior;
- comparison with Surfshark under the same target and time window;
- exact client/server build and configuration digest.

The replacement decision is operational:

```text
stable direct success
∧ acceptable performance
∧ acceptable recovery
∧ no critical destination regressions
```

It is not derived from the fact that the Ordivon domain itself is reachable.

## Stage 5 — security and robustness

Before persistent deployment:

- cargo fuzz or equivalent parser fuzzing;
- malformed length and truncation corpus;
- unknown frame corpus;
- certificate expiry and revocation tests;
- replay attempt tests confirming no application 0-RTT;
- concurrent stream and association exhaustion tests;
- slow-client and stalled-target tests;
- clean drain, upgrade, restart, and rollback tests;
- external source review of wire and authentication assumptions.

## Raw evidence handling

Public artifacts must redact:

- direct Edge IPs when disclosure is unnecessary;
- private DNS names;
- device certificate identities;
- credentials and key material;
- complete destination history;
- raw packet captures.

Derived aggregates and bounded protocol traces are preferred.
