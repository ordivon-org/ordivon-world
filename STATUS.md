# Status

## Current release line

Repository package version: `0.1.0` development candidate.

The active source boundary consists of one Host-facing Cloudflare adapter, the Cloudflare Worker/provider operations, and private network condition tools. There is no independent World service.

## Capability status

| Capability | State | Evidence |
|---|---|---|
| Cloudflare Fetch provider | operational | provider tests, deployed health and Receipt replay |
| Cloudflare Browser Snapshot provider | operational; P2 Worker candidate pending deployment | provider tests, Manifest contract and deployed capability output |
| Browser Host continuity and bundle verification | implemented; live acceptance pending | fresh-Host response-loss tests plus Receipt/Manifest/three-Artifact integrity checks |
| private R2 Artifact reads | operational | provider and client digest, media-type, byte-count and download-contract tests |
| deterministic Host Dispatch binding | verified | Python adapter, exact identity and Host integration tests |
| response-loss fresh-Host recovery | verified | one provider POST, fresh Host Receipt lookup and preserved Task state |
| live Host→Cloudflare W1 acceptance | verified locally | clean-revision private receipt under `target/acceptance/` |
| cross-language JSON Schema | verified | TypeScript capabilities plus Fetch, Browser, pending and rejected Receipts validated by the packaged Python Registry |
| W3C trace propagation | implemented as telemetry | not used as durable evidence or authority |
| World doctor | operational | repository-only and live machine/provider modes; live aggregate status is `ok` |
| Cloudflare GC source contract | operational | R2 List Objects uses `per_page` and cursor with focused tests |
| installed GC controller | operational | source/installed digests match; oneshot exits with `Result=success` and status 0 |
| Network condition tools | operational, operator-only | static, key-pair, namespace, scheduler and live doctor checks |
| GitHub CI, CodeQL and dependency automation | configured | remote execution begins after the local commits are pushed |

## P0–P1 closeout

P0–P1 is closed for a source revision only when the following evidence is regenerated for that exact clean revision:

1. the locked portable gate passes, including Python, Worker, provider-controller, network, dependency-audit and wheel checks;
2. Cloudflare GC succeeds through the corrected API contract;
3. `ordivon-world-doctor` reports no unresolved repository, installation, provider, lifecycle, GC or network fault on the target machine;
4. a live W1 receipt proves response loss, fresh-Host recovery, exactly one provider POST, Artifact verification and no Task completion claim;
5. source and installed controller digests agree;
6. the source repository remains clean after private receipts are written to ignored storage.

The current local `main` follows this closeout path. Remote CI execution and public publication are separate release actions and are not implied until the commits are pushed.

## P2 Browser continuity candidate

P2 extends the same direct Host-to-Cloudflare boundary to Browser Snapshot without introducing a provider broker or World runtime. The candidate is complete at the portable-test level when:

1. Browser Manifest is a shared TypeScript/Python machine contract;
2. succeeded Browser Receipts require screenshot, rendered HTML and primary Manifest Artifacts from one request generation;
3. Provider rejects non-PNG screenshot output before committing Browser Artifacts;
4. fresh Host recovery queries the original Browser request and performs no second POST;
5. Host verifies the three-Artifact bundle while preserving Task state and Ready Frontier;
6. a clean committed Worker candidate is deployed through the release controller and a live Browser response-loss receipt passes.

Items 1–5 are implemented in the current candidate. Item 6 remains pending until the candidate is committed and deployed. Provider capability negotiation and Effect rebinding remain conditional because P1/P2 have not demonstrated a semantically equivalent replacement-provider need. Local network observations are not bound as required state for remote Cloudflare execution because no observed failure justifies that coupling.

## Known limits

- The active provider set contains only Cloudflare. Shared provider abstractions remain intentionally narrow.
- Missing provider Receipt state remains UNKNOWN; automatic redispatch is forbidden.
- Trace Context and Dispatch headers are operational correlation only. Cloudflare Receipt and Host CAS remain authoritative.
- Browser capability is a bounded snapshot, not arbitrary Computer Use.
- Network tools do not grant Agents route, VPN or key-management authority.
- World does not yet implement RAG, SaaS, database, webhook, MQTT, OPC UA or Sandbox adapters.
- No package-index publication or production support guarantee exists.

See [`docs/verification.md`](docs/verification.md).
