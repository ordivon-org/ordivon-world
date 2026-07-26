# Ordivon Baseline v0 security model

## Security objective

Baseline v0 aims to provide authenticated, confidential, integrity-protected relay sessions between one user's devices and one user's Edge nodes while keeping parser and resource behavior bounded.

It is not an anonymity system and makes no claim of traffic-analysis resistance.

## Threat actors

### Passive path observer

Can observe outer source and destination IP addresses, UDP port, packet timing, sizes, direction, connection duration, and QUIC-visible behavior.

### Active path attacker

Can drop, delay, reorder, replay, or inject packets and can attempt downgrade or connection disruption. TLS/QUIC must provide integrity, peer authentication, replay boundaries, and forward-secret session keys.

### Active service probe

Can send arbitrary UDP/QUIC traffic to the Edge. The server must rely on the maintained QUIC/TLS implementation for handshake parsing and must not expose a separate unauthenticated custom parser before authentication.

### Stolen device credential

Can authenticate as one device until the certificate expires or is revoked. Independent per-device credentials limit the blast radius.

### Malicious authenticated client

Can attempt to exhaust streams, DNS lookups, sockets, associations, buffers, logs, and CPU. Hard limits apply after authentication as well as before it.

### Compromised Edge

Can see destination addresses, DNS requests performed by the Edge, timing, and the bytes entering destination sockets. End-to-end application encryption such as HTTPS remains necessary. Baseline cannot protect application plaintext from a malicious Edge when the application itself is plaintext.

## Guaranteed properties when correctly implemented

- server identity authentication;
- client device authentication;
- TLS 1.3 confidentiality and integrity for protocol and application bytes between client and Edge;
- forward-secret transport session keys as supplied by TLS/QUIC;
- bounded protocol fields and stable error codes;
- separation of device credentials so one device can be revoked independently;
- no protocol-level automatic replay of application streams.

## Explicit non-properties

Baseline v0 does not hide:

- that a client communicates with a particular Edge address;
- that UDP/QUIC is in use;
- session start and end times;
- packet sizes, bursts, direction, and aggregate byte counts;
- correlation between ingress and egress traffic;
- the destination from the Edge;
- the protocol from a sufficiently capable classifier.

It includes no camouflage, browser impersonation, random padding, domain fronting, or endpoint rotation.

## China-path interpretation

The fact that `ordivon.com` and Cloudflare are reachable without Surfshark does not imply that a direct custom QUIC service under the same parent domain is reachable. The observer can distinguish at least:

- the destination IP;
- whether the DNS record is Cloudflare-proxied or direct;
- ordinary HTTP/3 behavior versus a custom ALPN;
- connection timing and traffic shape.

The Cloudflare-hosted control plane is therefore a trusted bootstrap and measurement dependency, not proof that the Baseline data plane can pass the same path.

## Credential model

- one offline or tightly controlled Ordivon trust anchor;
- one certificate per Edge identity;
- one certificate per client device;
- a device identifier derived as the first 16 bytes of SHA-256 over the authenticated leaf certificate DER;
- server-side rejection when `HELLO.device_id` does not match that certificate-derived identifier;
- private keys generated and stored on the device that uses them where practical;
- short enough certificate validity to make recovery operationally feasible;
- explicit revocation or deny-list capability before remote deployment;
- no shared global password or UUID used as the only client credential.

Certificate issuance and rotation automation are outside the current pure wire implementation and must be designed before network deployment.

## 0-RTT policy

TLS early application data is disabled. `HELLO`, `OPEN_TCP`, `OPEN_UDP`, and relay bytes cannot be sent as replayable early data in v0.

## Input and allocation safety

Implementations must:

1. validate frame length before allocating;
2. reject QUIC varints above `2^62 - 1`;
3. enforce domain, build string, error detail, and UDP payload bounds;
4. reject invalid address and response types;
5. reject unknown critical frames;
6. skip only length-delimited unknown non-critical frames;
7. treat parser errors as protocol failures, not panics;
8. release all request and association state on connection termination.

The Rust `edge-wire` crate implements the first bounded parser contract without network or filesystem access.

## Resource safety

Authentication does not remove resource limits. At minimum the server enforces:

- maximum concurrent TCP streams;
- maximum pending destination connects;
- maximum UDP associations;
- bounded DNS and connect deadlines;
- bounded control-frame length;
- bounded error text;
- effective QUIC DATAGRAM size;
- idle association expiry;
- rate limits for repeated malformed requests and authentication failures.

## Logging policy

Permitted default evidence:

- opaque session and device identifiers;
- build and protocol versions;
- route and network labels;
- handshake and connect timings;
- aggregate bytes;
- stable error codes;
- close reason;
- negotiated limits.

Not permitted by default:

- application payload;
- private keys or bearer credentials;
- full packet captures;
- cookies or HTTP bodies;
- complete browsing history;
- full destination names in public artifacts.

Detailed local diagnostics must be opt-in, bounded, and reviewed before sharing.
