# Agent instructions

## Mission

Keep only external adapters and operator tools with current consumers. World owns no duplicate production truth.

## Authority

- Host owns Task, Effect, Dispatch, UNKNOWN, Verification, and completion.
- Runtime owns local Workspace, Job, process, and terminal evidence.
- Cloudflare owns Worker execution, request state, Receipts, R2 objects, versions, and control-plane resources.
- Network tools report or explicitly alter local operator-controlled paths; they do not become a routing authority.

## A11 default

Deletion is the default for dormant code, historical experiments, generated summaries, duplicate declarations, and checks that preserve wording or project shape rather than a real failure invariant.

Retain a constraint only when its removal reproduces a current failure, irreversible loss, duplicate Effect, false completion, secret exposure, unsafe route mutation, or unrecoverable deployment.

## Required checks

```bash
cd providers/cloudflare && pnpm run ci
cd modules/network-observation && scripts/check-vpn-controller
```
