# Status

## Current release line

Repository package version: `0.1.0` development candidate.

The active source boundary consists of one Host-facing Cloudflare adapter, the Cloudflare Worker/provider operations, and private network condition tools. There is no independent World service.

## Capability status

| Capability | State | Evidence |
|---|---|---|
| Cloudflare Fetch provider | operational | provider tests, deployed health and Receipt replay |
| Cloudflare Browser Snapshot provider | operational | provider tests and deployed capability output |
| private R2 Artifact reads | operational | provider and client digest tests |
| deterministic Host Dispatch binding | implemented | Python adapter and Host integration tests |
| response-loss fresh-Host recovery | deterministic test verified | one provider POST, fresh Host Receipt lookup, preserved Task state |
| live Host→Cloudflare W1 acceptance | pending final commit-bound receipt | run after the release candidate commit is clean |
| cross-language JSON Schema | implemented | TypeScript fixtures validated by packaged Python Registry |
| W3C trace propagation | implemented as telemetry | not used as durable evidence or authority |
| World doctor | implemented | repository/offline and live machine/provider modes |
| Cloudflare GC source fix | implemented | R2 List Objects now uses `per_page` with cursor tests |
| installed GC controller repair | pending source integration | install and execute after final source commit |
| Network condition tools | operational, operator-only | static, key-pair, namespace and scheduler tests |

## Known limits

- The active provider set contains only Cloudflare. Shared provider abstractions remain intentionally narrow.
- Missing provider Receipt state remains UNKNOWN; automatic redispatch is forbidden.
- Trace Context and Dispatch headers are operational correlation only. Cloudflare Receipt and Host CAS remain authoritative.
- Browser capability is a bounded snapshot, not arbitrary Computer Use.
- Network tools do not grant Agents route, VPN or key-management authority.
- World does not yet implement RAG, SaaS, database, webhook, MQTT, OPC UA or Sandbox adapters.
- No package-index publication or production support guarantee exists.

## Completion criteria for P0–P1

P0–P1 close when all of the following are true:

1. local and CI gates pass from locked dependency graphs;
2. Cloudflare GC runs successfully with the corrected API contract;
3. `ordivon-world-doctor` reports no unresolved repository/provider/GC fault on the target machine;
4. a clean commit-bound live W1 receipt proves response loss, fresh-Host recovery, exactly one provider POST, Artifact verification and no Task completion claim;
5. source and installed controller digests agree;
6. the source repository is clean and the final commit is recorded.

See [`docs/verification.md`](docs/verification.md).
