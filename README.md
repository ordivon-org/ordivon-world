# Ordivon World

Ordivon World is Ordivon's Task-to-World Interaction Continuity boundary: the place where we study how an open Task discovers, invokes, observes, reconciles, and conditionally rebinds external interactions. It also carries the production provider and observation modules used by current work.

It contains two real but independently owned capabilities:

- `providers/cloudflare/` — signed Fetch and Browser operations, durable Cloudflare Workflow evidence runs, private R2 Artifacts and manifests, authoritative request state, Receipts, release, rollback, policy, and operations;
- `modules/network-observation/` — source-native path, DNS, HTTP/TLS, QUIC, transfer, and lifetime observations plus private local tooling and historical research fixtures.

The former `ordivon-edge` and `ordivon-link` histories are preserved here. Their unification created a useful research question, but **W1 did not earn an independent production World layer**. The completed World Capability Program did not reverse that decision.

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

B1 reduced no Host state or recovery step. It added six correlation events, 4,535 bytes per Trial, and a 169-line journal implementation. The decision was:

```text
Do not retain a World correlation layer.

Host owns Task meaning, UNKNOWN, reconciliation, verification, and completion.
Provider adapters own native request/Receipt/Artifact semantics.
Observation adapters supply source-native facts through Host StateRefs.
```

See [`docs/w1-results.md`](docs/w1-results.md) and [`evidence/w1/w1-live-20260731c.json`](evidence/w1/w1-live-20260731c.json).

## Capability Program result

WCP-0 through WXP-2 completed on 2026-08-02:

- adapter-local capability declarations generate one read-only portfolio;
- two real consumers capture research sources and accept provider deployments;
- `evidence.run.v1` uses Cloudflare Workflows and R2 for durable bounded Fetch/Browser runs;
- one live run survived Host-process replacement through the original Workflow handle;
- callback faults remained recoverable through generation, adapter-local deduplication, and provider inspect fallback;
- provider-to-R2 Artifact movement preserved digest and provenance without proxying source bytes through Host;
- W-A1 deleted every candidate shared World authority.

The live WCP-2 trajectory completed two durable steps, independently verified all five Artifacts and 165,048 bytes, and produced zero unsafe redispatches, duplicate Workflow instances, false completions, World database records, or Task-recovery interventions.

Final disposition:

```text
retain adapters and provider-native authority
localize callback and Artifact facets
admit no World service, database, Workflow engine, callback journal,
Artifact transfer service, universal interaction schema, broker, or router
```

See [`docs/wcp0-wxp2-results.md`](docs/wcp0-wxp2-results.md) and [`evidence/wcp0-wxp2-closeout.json`](evidence/wcp0-wxp2-closeout.json).

## Current repository role

The repository retains the unified World problem definition while serving as:

1. the home of the production Cloudflare provider;
2. the home of private network-observation tools;
3. the home of adapter-local capability declarations and generated evidence;
4. an experiment repository for external-interaction failures;
5. the preserved history of the Edge and Link prototypes.

It is **not** a mandatory Host→Runtime→World pipeline, universal World schema, provider broker, network controller, proxy, VPN, service mesh, Sandbox, Browser implementation, Workflow engine, callback authority, Artifact transfer service, or second authority store.

## Ownership

| Fact | Authority |
|---|---|
| Goal, Task, Attempt, Effect, Dispatch, UNKNOWN, Verification, TaskOutcome | Ordivon Host |
| local Workspace, process, Job, cancellation, terminal evidence | Ordivon Runtime |
| provider Request ID, Workflow instance, idempotency digest, state, Receipt, Artifact, policy and Worker identity | provider and provider adapter |
| raw path, endpoint, protocol, latency, and failure observation | source-native observation module |
| consequence authorization and domain validity | domain or Security system |
| experiment arm, fault schedule, measurements, disposition | bounded experiment only |

No universal World ID or synchronized World database exists.

## Repository layout

```text
providers/cloudflare/                    production Fetch/Browser/Workflow/R2 adapter
modules/network-observation/             observations, private tools, research fixtures
experiments/w1-host-cloudflare/          W1 direct-versus-correlation comparison
experiments/wxp1-callback-continuity/    callback continuity comparison
experiments/wxp2-remote-artifact/        remote-to-remote Artifact comparison
evidence/w1/                             W1 live evidence
evidence/wcp1/                           real consumer evidence
evidence/wcp2/                           durable Workflow and release evidence
evidence/wcp0-wxp2-closeout.json         generated W-A1 closeout summary
docs/                                    contracts, results, boundaries, route, history
migration/                               exact source and retirement provenance
scripts/check-repository-layout.py
scripts/check-w1-evidence.py
scripts/generate-capability-portfolio.py
scripts/generate-wcp-closeout.py
```

Historical names remain where renaming would break local operations or falsify old receipts. They do not restore separate Edge or Link architectural ownership.

## Verification

```bash
python3 scripts/check-repository-layout.py
python3 scripts/check-w1-evidence.py
python3 scripts/generate-capability-portfolio.py --check
python3 scripts/generate-wcp-closeout.py --check

cd experiments/w1-host-cloudflare
uv sync --frozen
uv run python -m unittest discover -s tests -v

cd ../wxp1-callback-continuity
python3 experiment.py
python3 -m unittest -v test_experiment.py

cd ../wxp2-remote-artifact
python3 experiment.py
python3 -m unittest discover -s . -p 'test_*.py' -v

cd ../../providers/cloudflare
pnpm install --frozen-lockfile
pnpm run ci

cd ../../modules/network-observation
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```

## Research route

- **W0 complete:** classified inherited carriers without admitting an inherited schema.
- **W1 complete:** direct Host integration matched the correlation arm with less state.
- **Capability Program v0 complete through WXP-2:** durable Workflow, callback, and Artifact workloads retained source-native responsibilities and rejected a shared World layer.
- **W2 conditional:** inactive until a materially different workload reproduces one exact unowned responsibility.
- **WCP-3 deferred:** select a second capability only from a named real workload and substantial capability gain.

Future work starts from a named failure or capability need. The existence of provider, network, Node, transport, or historical World code is not sufficient evidence for another layer.
