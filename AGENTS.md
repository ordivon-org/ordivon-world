# Agent instructions

## Mission

Ordivon World is the Task-to-World Interaction Continuity boundary. It studies how an open Task discovers, invokes, observes, reconciles, and—only when evidence requires it—rebinds one external interaction across changing targets, paths, identities, providers, participants, and result channels.

W1 proved that the current Cloudflare Fetch response-loss trajectory does not require an independent World correlation layer. Preserve the unified problem definition, but do not create a World service, database, universal ID, broker, router, or second authority store without a reproduced cross-owner failure.

## Current carriers

- `providers/cloudflare/` is a production provider adapter with provider-native request, execution, Receipt, Artifact, policy, release, rollback, and cleanup semantics.
- `modules/network-observation/` is a source-native observation adapter and private local-operations module.
- `experiments/` and `evidence/` preserve bounded architecture tests and negative results.
- inherited Edge/Link Node, Network World, wire, QUIC, VPN, and transport material is historical or private; it is outside the default production workspace unless explicitly reactivated.

## Authority after W1

1. Host owns Goal, Task, Attempt, Effect, Dispatch, UNKNOWN, recovery frontier, Verification, Artifact acceptance, and completion.
2. Runtime owns trusted-local Workspace, Job, process, cancellation, and terminal evidence.
3. Provider adapters own provider-native endpoint, request digest, idempotency, pending/committed state, Receipt, Artifact, policy, capability, and provider version.
4. Observation adapters own source-native observations and expose bounded references or projections.
5. Security or the domain system owns consequence authority and final validity.
6. World owns no duplicate production truth today; it retains the shared question, experiment boundary, and concrete modules.

## Engineering constraints

1. Reconcile uncertain external work by its original provider identity before redispatch.
2. Never replace provider-native request or Receipt semantics with a generic World digest or state machine.
3. Never synchronize Host Task truth, provider request truth, and raw observation truth into a World database.
4. Bind exact path, endpoint, identity, provider, policy, capability, build, and time revisions only where a consumer uses them.
5. Do not automate route, DNS, VPN, firewall, provider, or participant changes before a concrete failure proves the need.
6. Historical carriers may be deleted, archived, or left unbuilt; default CI must not preserve them merely because they once existed.
7. Every proposed shared responsibility needs a direct baseline, reproduced failure when deleted, a second materially different consumer, explicit ownership, measured net benefit, and a closeout disposition.
8. Preserve invalid and null experiments exactly. Checks prove only their named property and must not override deletion judgment.

## Conditional reactivation

Open a narrow W2 or successor experiment only after reproducing a capability mismatch, contract drift, callback discontinuity, participant handoff failure, remote-to-remote Artifact continuity failure, or still-open Effect rebinding failure that Host plus source-native adapters cannot own cleanly.

A provider marketplace, universal broker, automatic routing, or blind retry is never implied.

## Required checks

```bash
python3 scripts/check-repository-layout.py
python3 scripts/check-w1-evidence.py
cd experiments/w1-host-cloudflare && uv sync --frozen && uv run python -m unittest discover -s tests -v
cd providers/cloudflare && pnpm run ci
cd modules/network-observation && cargo fmt --all -- --check
cd modules/network-observation && cargo clippy --workspace --all-targets -- -D warnings
cd modules/network-observation && cargo test --workspace --all-targets
```
