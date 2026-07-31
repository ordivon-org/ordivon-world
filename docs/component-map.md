# Component Map

The authoritative W0 classification is
[`w0-carrier-inventory.json`](w0-carrier-inventory.json). This page is the compact
human map.

## Retained provider capability

| Component | Owner | W1 role | Disposition |
|---|---|---|---|
| signed Cloudflare Fetch | provider | external operation | retain |
| Browser Run | provider | excluded from W1 | retain |
| pending/committed request state, leases, fencing | provider | authoritative operation state | retain |
| private R2 Artifacts and Receipts | provider | result and reconciliation evidence | retain |
| release, rollback, GC, policy tooling | provider operations | none | retain |
| signed Python client | provider adapter | direct baseline | adapter-only |

## Network and inherited research carriers

| Component | Owner | W1 role | Disposition |
|---|---|---|---|
| `link-probe` and used `ProbeResult` fields | network observation | one source-native observation | adapter-only |
| reduced SQLite history and loopback console | private local operations | none | adapter-only |
| deterministic Network World and Security port | inherited research fixture | none | historical |
| disposable Node/unshare lifecycle | inherited research fixture | none | historical |
| reference wire and QUIC transport | inherited transport experiment | none | historical |
| WireGuard/Surfshark tools and protocol catalog | private operations and dated research | none | historical |
| unused `Device`, `Edge`, `Target`, `Transport`, `RouteDecision` declarations | none | none | delete-candidate |
| universal interaction field inventory | research hypothesis | none | delete-candidate |

## W1 missing capability

Only one capability remains untested:

> Can a small correlation record improve recovery and explanation after a real
> provider Receipt commits but the Host loses the response, relative to direct
> Host use of the same provider request identity and Receipt lookup?

W1 does not need a resolver, provider router, Network World, Browser/Sandbox
model, automatic recovery service, or shared schema to answer that question.
