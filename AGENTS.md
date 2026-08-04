# Agent instructions

## Mission

Keep World as the narrow recoverable boundary between Host-owned work and provider-owned external reality. Add only adapters, condition observers and operator controls with a named current consumer and a reproduced failure trajectory.

## Authority

- Host owns Task, Effect, Dispatch, revision fencing, UNKNOWN, Verification and completion.
- Harness owns the model/Tool loop and Run evidence.
- Runtime owns local Workspace, Job, process and terminal evidence.
- World owns provider binding, capability conditions, reconciliation and evidence mapping.
- Cloudflare owns Worker execution, request state, Receipts, R2 objects, versions and control-plane resources.
- Network tools report or explicitly alter local operator-controlled paths; they are not a routing authority.

## Non-negotiable recovery rules

- Persist `PreparedWorldDispatch` before external delivery.
- Derive one deterministic provider request ID from the Host Dispatch and request.
- Treat transport uncertainty as UNKNOWN.
- Query the original Receipt before any replacement action.
- Never infer Task completion from provider success.
- Keep telemetry correlation separate from durable evidence.
- Fail closed on capability-condition, Receipt identity, request digest or Artifact digest drift.

## A11 default

Deletion remains the default for dormant providers, generic registries, automatic routers, workflow layers, duplicated provider state and checks that preserve wording rather than a failure invariant.

A shared abstraction requires two materially different workloads, two real consumers and a failure that direct Host plus provider adapters cannot solve cleanly.

## Required checks

```bash
uv sync --locked
cd providers/cloudflare && pnpm install --frozen-lockfile && cd ../..
scripts/local-acceptance
```

For live-effect changes, also run the clean-commit W1 acceptance and `ordivon-world-doctor` described in [`docs/operations.md`](docs/operations.md).
