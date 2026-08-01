# Ordivon World

Ordivon World is Ordivon's Task-to-World Interaction Continuity boundary: the place where we study how an open Task discovers, invokes, observes, reconciles, and conditionally rebinds external interactions. It also carries the production provider and observation modules used by current work.

It contains two real but independently owned capabilities:

- `providers/cloudflare/` — signed Fetch and Browser operations, private R2 Artifacts, authoritative request state, Receipts, response-loss reconciliation, release, rollback, policy, and operations;
- `modules/network-observation/` — source-native path, DNS, HTTP/TLS, QUIC, transfer, and lifetime observations plus private local tooling and historical research fixtures.

The former `ordivon-edge` and `ordivon-link` histories are preserved here. Their unification created a useful research question, but **W1 did not earn an independent production World layer**.

## W1 result

A real Host Task executed the same Cloudflare Fetch through two arms:

```text
B0 direct
Host Dispatch + provider Request ID
→ provider commits Receipt and Artifact
→ response is deliberately lost
→ fresh Host process queries original Receipt
→ exact Artifact verification
→ exactly-once Task completion

B1 correlation
same complete path
+ separate hash-chained World correlation journal
```

Both arms executed the provider operation once, queried the original Receipt before any retry, produced no duplicate Effect or unsafe redispatch, verified the same Artifact independently, completed the original Host Task exactly once, and required zero operator intervention.

B1 reduced no Host state or recovery step. It added six correlation events, 4,535 bytes per Trial, and a 169-line journal implementation. The decision is therefore:

```text
Do not retain a World correlation layer.

Host owns Task meaning, UNKNOWN, reconciliation, verification, and completion.
Provider adapters own native request/Receipt/Artifact semantics.
Observation adapters supply source-native facts through Host StateRefs.
```

See [`docs/w1-results.md`](docs/w1-results.md) and the validated evidence in [`evidence/w1/w1-live-20260731c.json`](evidence/w1/w1-live-20260731c.json).

## Current repository role

The repository retains the unified World problem definition while serving as:

1. the home of the production Cloudflare provider;
2. the home of private network-observation tools;
3. the preserved history of the Edge and Link prototypes;
4. an experiment repository for future external-interaction failures.

It is **not** a mandatory Host→Runtime→World pipeline, universal World schema, provider broker, network controller, proxy, VPN, service mesh, Sandbox, Browser implementation, workflow engine, or second authority store.

## Ownership after W1

| Fact | Authority |
|---|---|
| Goal, Task, Attempt, Effect, Dispatch, UNKNOWN, Verification, TaskOutcome | Ordivon Host |
| local Workspace, process, Job, cancellation, terminal evidence | Ordivon Runtime |
| provider Request ID, idempotency digest, pending/committed state, Receipt, Artifact, policy and Worker identity | provider and provider adapter |
| raw path, endpoint, protocol, latency, and failure observation | source-native observation module |
| consequence authorization and domain validity | domain or Security system |
| experiment arm, fault schedule, measurements, disposition | bounded experiment only |

No universal World ID or synchronized World database exists.

## Repository layout

```text
providers/cloudflare/                 production Fetch/Browser/R2 provider
modules/network-observation/          observations, private tools, research fixtures
experiments/w1-host-cloudflare/       reproducible W1 comparison, not product code
evidence/w1/                          validated closeout evidence
docs/                                 W0/W1 contracts, results, boundaries, history
migration/                            exact source and retirement provenance
scripts/check-repository-layout.py
scripts/check-w1-evidence.py
```

Historical names remain where renaming would break local operations or falsify old receipts. They do not restore separate Edge or Link architectural ownership.

## Verification

```bash
python3 scripts/check-repository-layout.py
python3 scripts/check-w1-evidence.py

cd experiments/w1-host-cloudflare
uv sync --frozen
uv run python -m unittest discover -s tests -v

cd ../../providers/cloudflare
pnpm install --frozen-lockfile
pnpm run ci

cd ../../modules/network-observation
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```

## Capability program

The post-W1 development design is [`docs/world-capability-program-v0.md`](docs/world-capability-program-v0.md). World now advances through a capability portfolio plus a failure-driven architecture laboratory. The first new capability class is a direct Cloudflare Workflows-backed durable evidence run; it does not introduce a World service or shared authority.

## Research route

- **W0 complete:** classified 16 inherited carrier groups without admitting an inherited schema.
- **W1 complete:** direct Host integration matched the correlation arm with less state; semantics were absorbed into Host and adapters.
- **W2 conditional:** remains inactive until a real capability mismatch, contract drift, callback discontinuity, participant handoff, remote-to-remote Artifact continuity, or valid Effect-rebinding failure is reproduced.

Future work starts from a named failure. The existence of provider, network, Node, transport, or World fixture code is not sufficient evidence for another shared layer.
