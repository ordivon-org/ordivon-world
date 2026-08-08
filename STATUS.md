# Status

## Current release line

Repository package version: `0.1.0` development candidate.

The active source boundary consists of one Host-facing Cloudflare adapter, the Cloudflare Worker/provider operations, and private network condition tools. There is no independent World service.

## Capability status

| Capability | State | Evidence |
|---|---|---|
| Cloudflare Fetch provider | operational | provider tests, deployed health and Receipt replay |
| Cloudflare Browser Snapshot provider | operational | Worker `ba64a576-1986-4967-96d6-3d2390f7afc6`, release-controller dual smoke and deployed capability output |
| Browser Host continuity and bundle verification | live verified | one Browser POST, injected response loss, fresh-Host reconciliation, three verified Artifacts and no Task completion claim |
| private R2 Artifact reads | operational | provider and client digest, media-type, byte-count and download-contract tests |
| deterministic Host Dispatch binding | verified | Python adapter, exact identity and Host integration tests |
| response-loss fresh-Host recovery | verified | one provider POST, fresh Host Receipt lookup and preserved Task state |
| W1 cross-World evidence program | completed | P0–P5 proved Resource/Entity/Message durability, UNKNOWN recovery, Link rebinding, federation composition, untrusted-relay provenance and independent concurrency; W2 promoted only Resource after production integration |
| W2 Resource Transfer | production contract, cross-repository verified | Game retained/replayed source egress → World per-transfer durable Host journal/wire → Security transfer-specific ingress; crash-window `not_committed`, multi-transfer Task addressing and legacy flat-state recovery verified |
| W2 Host trajectory addressing | verified across two production consumers | Resource uses `transferId`; provider extension uses Host `dispatchId`; partial UNKNOWN state is per trajectory; legacy flat Resource/provider state migrates on first mutation |
| live Host→Cloudflare W1 acceptance | verified locally | clean-revision private receipt under `target/acceptance/` |
| cross-language JSON Schema | verified | fourteen packaged Draft 2020-12 Schemas; provider fixtures plus Game-produced Resource Egress documents validated across TypeScript/Python |
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

## P2 Browser continuity closeout

P2 extends the same direct Host-to-Cloudflare boundary to Browser Snapshot without introducing a provider broker or World runtime. All six acceptance conditions are closed:

1. Browser Manifest is a shared TypeScript/Python machine contract;
2. succeeded Browser Receipts require screenshot, rendered HTML and primary Manifest Artifacts from one request generation;
3. Provider rejects non-PNG screenshot output before committing Browser Artifacts;
4. fresh Host recovery queries the original Browser request and performs no second POST;
5. Host verifies the three-Artifact bundle while preserving Task state and Ready Frontier;
6. the committed Worker candidate passed stable zero-traffic admission, Fetch and Browser smoke, promotion and live Browser response-loss acceptance.

The promoted Worker is `ba64a576-1986-4967-96d6-3d2390f7afc6`, with Worker-input digest prefix `854721962bd3f31a`. Private release receipt `release-20260804T085441Z.json` has SHA-256 `16d7e8766646729244abd99a75eaffd49cb83eec8d0e0aa6ea78545d3066bf7c`. The live Browser receipt is bound to source revision `deebb30216b7a831e058a6d3577e1926e8dbfa87`, has SHA-256 `6bab1e39172e390cf9cdff2444da7fd390502064a346f015189f0fc553e22356`, and proves 20 of 20 checks including one first-execution POST, committed-response loss, Host UNKNOWN, fresh-Host recovery, three Artifact verifications and no Task completion claim.

Provider capability negotiation and Effect rebinding remain conditional because P1/P2 have not demonstrated a semantically equivalent replacement-provider need. Local network observations remain outside required remote Cloudflare Dispatch state because no observed failure justifies that coupling.

## Known limits

- The active provider set contains only Cloudflare. Shared provider abstractions remain intentionally narrow.
- Missing provider Receipt state remains UNKNOWN; automatic redispatch is forbidden.
- Trace Context and Dispatch headers are operational correlation only. Cloudflare Receipt and Host CAS remain authoritative.
- Browser capability is a bounded snapshot, not arbitrary Computer Use.
- Network tools do not grant Agents route, VPN or key-management authority.
- World does not yet implement RAG, SaaS, database, webhook, MQTT, OPC UA or Sandbox adapters.
- No package-index publication or production support guarantee exists.

See [`docs/verification.md`](docs/verification.md).
