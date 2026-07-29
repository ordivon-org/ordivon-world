# Component Map Under the Revised Edge Route

This map separates current operational value from long-term research claims.
No code is moved by this documentation change.

| Component | Current authority | Revised classification | Disposition |
|---|---|---|---|
| `src/index.ts` and Cloudflare capability modules | bounded signed Fetch/Browser execution and stable HTTP behavior | production provider adapter | retain and harden |
| `src/idempotency.ts`, `src/execution.ts`, `src/receipts.ts`, `src/artifacts.ts`, `src/cleanup.ts` | provider request state, fencing, Receipt, Artifact, cleanup | remote-effect reliability mechanisms | retain; later bind to Host Effect/Dispatch |
| `src/auth.ts`, `src/policy.ts`, provider policies | production authentication, limits, capability and policy revision | provider-specific authority and consequence implementation | retain; do not treat as universal policy model |
| `src/node-contracts.ts`, `src/node-lifecycle.ts` | deterministic Node/body experiment identity and lifecycle | body/lifecycle research hypothesis | keep stable for experiments; do not call permanent core |
| `src/local-node-adapter.ts`, `src/node-policy.ts` | narrow local `unshare` conformance body | classical isolation reference provider | freeze scope; no generic Sandbox growth |
| `src/research-node-control.ts` and JSONL script | trusted control of one research body and operation reconciliation | Security integration/conformance surface | retain while consumed; not a general Edge service |
| client, release, GC, lifecycle scripts | Cloudflare operations | production operations | retain independently of research route |
| tests and boundary checks | exact current contracts | conformance and regression evidence | update terminology; preserve behavior |

## Not yet implemented

| Candidate | Evidence status |
|---|---|
| Placement Requirement | research only |
| Provider Capability Observation and candidate comparison | research only |
| Host-visible Placement Binding | absent |
| cross-provider Task continuation | absent |
| multi-body branch/join provenance | absent |
| persistent Agent presence distinct from Task/service/provider identity | unproven hypothesis |

## Ownership summary

- Provider owns physical body and native lifecycle.
- Edge may own the exact Task-to-provider execution binding and remote continuity
  evidence.
- Host owns why work occurs and how Task state advances.
- Link owns how bodies and targets connect.

The current body/lifecycle experiment remains useful because it can falsify or
refine these boundaries. Its existence does not settle them.
