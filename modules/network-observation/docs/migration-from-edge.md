# Migration from the Edge / Link incubator

This repository preserves the Git history of the original `ordivon-edge` network incubator.

The split maps code as follows:

| Incubator path | Ordivon Link path | Reason |
|---|---|---|
| `edge-model` | `link-model` | Local network and route domain models |
| `edge-probe` | `link-probe` | Path evidence collection |
| `edge-runtime` | `link-observer` | Local observation and state reduction, not Agent execution |
| `edge-server` | `link-console` | Local read-only status surface |
| `edge-wire` | `link-wire` | Link-to-Edge transport contract |
| `edge-transport-quic` | `link-transport-quic` | Replaceable Link transport reference |

The original pre-split state is retained at branch `archive/edge-link-incubator`.

Cloudflare Workers, Browser Rendering, R2 artifact handling, bounded external fetch, and external task receipts continue in the separate `ordivon-edge` repository.
