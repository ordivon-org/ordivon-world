# Security Policy

## Supported scope

The current security boundary covers the `0.1.x` source line, its exact Host/Protocol dependency graph, the Cloudflare Worker and operator controllers, and the private network tools retained in this repository. The project is pre-1.0 and does not promise backward-compatible security fixes for historical experiments outside active `main`.

## Reporting a vulnerability

Do not open a public issue containing secrets, request signatures, private endpoint data, Artifact bytes, exploit payloads or production configuration. Report privately to the repository owner through GitHub private vulnerability reporting when enabled, or use a private channel already established with the maintainer.

Include:

- affected revision and component;
- whether the issue reaches local Host state, Cloudflare Worker/R2, systemd, network tools or release control;
- exact reproduction without live credentials;
- potential duplicated Effect, authority bypass, data exposure or recovery corruption;
- any mitigation already applied.

## Trust model

World is currently an operator-controlled integration for a trusted local Host. It is not a multi-tenant authorization service.

- Host authority must exist before an effectful provider call.
- HMAC possession authenticates the machine client to the current Cloudflare Worker; it does not establish end-user identity or business authorization.
- Cloudflare, R2 and the configured external target remain trusted dependencies.
- Network mutation commands require explicit operator action and root authority.
- A successful provider Receipt is not proof of semantic completion.

## Primary controls

- exact revision-pinned Host and Protocol dependencies;
- request/body/timestamp HMAC binding;
- deterministic request identity and provider idempotency conflict detection;
- capability-condition fencing before dispatch;
- generation-fenced provider leases and Artifacts;
- private R2 with digest-verified downloads;
- allowlisted HTTPS Fetch and same-origin bounded Browser Snapshot;
- strict local JSON Schema validation with no remote Schema retrieval;
- root-only Secrets and private receipt modes;
- no automatic redispatch from transport failure;
- no Agent authority to alter VPN routes or keys.

Provider-specific threats and controls remain in [`providers/cloudflare/docs/security.md`](providers/cloudflare/docs/security.md). Data retention and disclosure are documented in [`docs/data-and-privacy.md`](docs/data-and-privacy.md).

## Unsafe changes requiring explicit review

Treat the following as security-sensitive:

- request identity or canonicalization changes;
- HMAC, clock window, key ID or Secret handling;
- allowlist, redirect, Browser resource or size limits;
- Receipt, lease, Artifact or R2 lifecycle changes;
- a new effectful provider operation;
- automatic retry, fallback or provider replacement;
- callback or inbound event acceptance;
- exposing raw provider content to a browser or public URL;
- network route, VPN, credential or key automation;
- widening Host extension authority or treating telemetry as evidence.

## Residual risks

- A compromised shared HMAC Secret can invoke every currently allowed capability.
- An allowlisted site can return malicious or misleading content.
- External targets can change after an observation.
- R2 lifecycle and local receipts retain potentially sensitive metadata and bytes.
- Provider or network conditions can change between observation and use.
- Current Browser Snapshot cannot prove the final page identity beyond provider evidence.
- The project does not yet provide tenant isolation, user OAuth delegation, mTLS workload identity or policy-as-code authorization.
