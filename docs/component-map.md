# Component Map After W1

The W0 source inventory remains in [`w0-carrier-inventory.json`](w0-carrier-inventory.json). W1 resolved the only active boundary question.

## Production and operational carriers

| Component | Authority | Disposition after W1 |
|---|---|---|
| signed Cloudflare Fetch and Browser Run | provider | retain |
| pending/committed request state, lease, fencing | provider | retain |
| private R2 Artifact and deterministic Receipt | provider | retain |
| release, rollback, GC, policy tooling | provider operations | retain |
| signed Python provider client | provider adapter | retain as adapter |
| `link-probe` and used `ProbeResult` fields | observation module | retain as source-native adapter input |
| reduced local history and loopback console | private local operations | retain while useful |

## Historical or deletion-tested carriers

| Component | Disposition |
|---|---|
| W1 correlation journal | historical experiment; do not promote |
| deterministic Network World and Security port | historical fixture |
| disposable Node/unshare lifecycle | historical fixture |
| reference wire and QUIC transport | historical experiment |
| WireGuard/Surfshark and transport catalog | private or dated research |
| unused `Device`, `Edge`, `Target`, `Transport`, `RouteDecision` declarations | delete-candidate |
| universal World Interaction field inventory | delete-candidate |

## Surviving cross-component path

```text
Host Dispatch
  ├─ StateRef → source-native probe digest
  └─ idempotency_key → provider Request ID

provider Receipt / Artifact
  → Host Observation
  → Host Verification
  → Host TaskOutcome
```

No separate World authority is required for this path.
