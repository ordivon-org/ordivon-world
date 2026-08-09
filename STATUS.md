# Status

## Current release line

Repository package version: `0.4.0`.

The active source boundary consists of the Host-facing Cloudflare adapter, production Resource Transfer, Message Delivery and Entity Migration contracts, Cloudflare Worker/provider operations, and private network condition tools. There is no independent World service.

## Capability status

| Capability | State | Evidence |
|---|---|---|
| Cloudflare Fetch provider | operational | provider tests, deployed health and Receipt replay |
| Cloudflare Browser Snapshot provider | operational | Worker `ba64a576-1986-4967-96d6-3d2390f7afc6`, release-controller dual smoke and deployed capability output |
| Browser Host continuity and bundle verification | live verified | one Browser POST, injected response loss, fresh-Host reconciliation, three verified Artifacts and no Task completion claim |
| private R2 Artifact reads | operational | provider and client digest, media-type, byte-count and download-contract tests |
| deterministic Host Dispatch binding | verified | Python adapter, exact identity and Host integration tests |
| response-loss fresh-Host recovery | verified | one provider POST, fresh Host Receipt lookup and preserved Task state |
| W1 cross-World evidence program | completed | P0–P5 proved Resource/Entity/Message durability, UNKNOWN recovery, Link rebinding, federation composition, untrusted-relay provenance and independent concurrency; W2 promoted Resource, Message and Entity Migration only after independent production integration |
| W2 Resource Transfer | production contract, cross-repository verified | Game retained/replayed source egress → World per-transfer durable Host journal/wire → Security transfer-specific ingress; crash-window `not_committed`, multi-transfer Task addressing and legacy flat-state recovery verified |
| W2 Message Delivery | production contract, cross-repository verified | Game visible retained Fact issuance → World per-message Host journal/wire → Security management-classified durable inbox; both UNKNOWN branches, live-commit race, broadcast semantics and legacy flat-state recovery verified |
| W2 Message endpoint/Link falsifier | first-class WorldLink not forced | pinned destination identity detected endpoint replacement; stable identity survived PID/socket rematerialization; signed discovery handled endpoint relocation without Link identity/lifecycle |
| W2 Entity Migration | production contract, cross-repository and real-KVM verified | Game retained verified extraction and fresh-process departure reread → World/Host exact continuity journal + wire → Security real KVM carrier; fresh Host retained the receipt with one destination exchange, no blind redispatch, no NIC and zero-residual cleanup under the `trusted-local-owner-originated-caller` profile |
| W5-A Agent Embodiment | research closeout; A0–A4-P1 verified, no production contract | A0–A3 prove owner-separated, action-scoped subject × cognition × Body occurrence with live Harness cognition and native Game effects. A4 proves that current Presence is scope-bound owner observation rather than durable history: the same Game Subject/Body moved `PRESENT → UNKNOWN → PRESENT` across scoped admissions, Security observation failure degraded to `UNKNOWN`, clean Body destruction produced `absent-through-body`, and the same Subject was simultaneously present through Game while absent through Security Body A. Query-shaped current evidence was sufficient; no global Presence registry was justified |
| W5-B Agent Presence | research closeout; B0–B2 verified, no production Presence contract | B0 proves current relation evidence resolves an Agent body-choice that history alone cannot; B1 proves Security as a second bounded subject-active destination while retaining Host-native Body truth; B2 shows the cross-domain minimum is a six-role proof interface (`subjectRef`, `ownerId`, `bodyRef`, `scopeDigest`, `admissionDigest`, `occurrenceDigest`) rather than a union of Game cognition/Planning and Security migration/generation semantics. No Presence registry, Embodiment manager or shared production occurrence schema is justified before a third materially different consumer |
| W5-C Discovery & Connection | active research; C0 orthogonality verified | current Game proves known peer discovery does not mint target-specific affordance; current Security proves `unreachable + exact authority` can be admitted while `active + missing capability` is rejected; current Message Delivery/Wire passes 19/19 without first-class relationship/session/`WorldLink` state. Discovery, reachability, relationship/session and authority are separate owner-native dimensions; C1 now tests which fresh evidence actually changes an Agent contact decision |
| W2 KVM migration recovery | current Security recovery law physically verified | predecessor ownership remains provenance; independently re-observed completion may repair publication; dead body-free staged/TPM-only preparation may be compensated to zero residuals and released `not_committed`; ambiguous QEMU launch evidence remains UNKNOWN and cannot authorize retry |
| W2 Host trajectory addressing | evidence-driven, intentionally asymmetric | Resource/Message/provider use per-ID maps after reproduced multi-trajectory failures; Entity Migration retains one `migrationId` per Task because no multi-migration workload has forced a map |
| live Host→Cloudflare W1 acceptance | verified locally | clean-revision private receipt under `target/acceptance/` |
| cross-language JSON Schema | verified | twenty-six packaged Draft 2020-12 Schemas; provider fixtures plus Game-produced Resource, Message and Entity departure authority documents validated across TypeScript/Python |
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
- Entity Migration materializes a continuity carrier; it still does not prove Guest-side subject activation or current Presence. W5-A A3 proves bounded action-scoped subject/cognition activation through a Game Actor; A4-P0 additionally proves that historical embodiment/materialization evidence can outlive both subject-binding currentness and physical Body currentness, so `materialized` or `active Actor` must not be read as a global Presence claim.
- No package-index publication or production support guarantee exists.

See [`docs/verification.md`](docs/verification.md).
