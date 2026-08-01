# WCP-0 through WXP-2 Results

Status: completed and production-validated

Date: 2026-08-02

Implementation merge: `bac8c24f61a96bc1c6d717566d1670b4732ffc79`

Authoritative closeout summary: [`../evidence/wcp0-wxp2-closeout.json`](../evidence/wcp0-wxp2-closeout.json)

## Decision

The World Capability Program produced useful external capability without earning an independent World authority layer.

The retained composition is:

```text
Host
  Task / Effect / Dispatch / UNKNOWN
  reconciliation / Verification / completion

Cloudflare provider adapter
  Fetch / Browser / Workflow submission and inspect
  provider request identity, policy, status, Receipt, and Artifact metadata

Cloudflare Workflows and R2
  durable provider execution
  immutable submission, input, result, failure, and source Artifacts

network observation adapter
  source-native observations

World repository
  adapter carrier, capability projection, experiments, and evidence
```

The final W-A1 disposition is:

```text
keep adapters
localize callback and Artifact facets
retain provider-native Workflow and R2 authority
admit no shared World service, database, workflow engine, callback journal,
transfer service, universal interaction schema, broker, or router
```

## WCP-0 — capability portfolio

Two adapter-local declarations now generate one deterministic read-only portfolio:

- `providers/cloudflare/capability.json`;
- `modules/network-observation/capability.json`;
- generated `docs/capability-portfolio.md`;
- generated `evidence/capability-portfolio-v0.json`.

The generated portfolio declares `writable_registry: false`. It records each adapter's owner, authority, real consumers, consequence class, cost model, retention source, facets, capability revisions, and deletion trigger without copying provider operational state.

Disposition:

- retain adapter-local declarations;
- retain deterministic read-only projection;
- reject a writable registry or capability service.

## WCP-1 — real consumers

### Research-source capture

The `ordivon-computer` consumer captured the current Cloudflare Workflows documentation through the production provider and independently verified the returned Artifact.

| Measure | Result |
|---|---:|
| Request ID | `req_a9ec828123a74022bec7057dc7c3729e` |
| Worker version | `749dc76c-16cc-4d20-b209-e5df67d70143` |
| elapsed | 8,129 ms |
| Artifacts | 1 |
| verified Artifact bytes | 129,314 |
| operator interventions | 0 |
| unsafe redispatch attempts | 0 |

Evidence: [`../evidence/wcp1/computer-research-source-post-wcp2-20260802.json`](../evidence/wcp1/computer-research-source-post-wcp2-20260802.json).

### Provider post-deployment acceptance

The release consumer bound health, capabilities, policy, Worker version, one Fetch Receipt, and one independently verified Artifact.

| Measure | Result |
|---|---:|
| Request ID | `req_e26904d959714e7b94706207a00ba017` |
| Worker version | `749dc76c-16cc-4d20-b209-e5df67d70143` |
| elapsed | 7,410 ms |
| Artifacts | 1 |
| verified Artifact bytes | 559 |
| operator interventions | 0 |
| unsafe redispatch attempts | 0 |

Evidence: [`../evidence/wcp1/provider-acceptance-post-wcp2-20260802.json`](../evidence/wcp1/provider-acceptance-post-wcp2-20260802.json).

### Installed consumer defect

The source consumer initially worked only from the repository because its installed executable could not import `ordivon_edge_client`. The installer now places the single shared implementation at:

```text
/usr/local/lib/ordivon-world/ordivon_edge_client.py
```

The executable remains `/usr/local/bin/ordivon-world-evidence`. No protocol implementation was duplicated.

## WCP-2 — durable evidence run

The Cloudflare adapter now exposes `evidence.run.v1` with one to eight bounded `fetch` or `browser.run` steps.

Provider routes:

```text
POST /v1/evidence-runs
GET  /v1/evidence-runs/{instance-id}
POST /v1/evidence-runs/{instance-id}/terminate
```

The provider preserves one opaque Workflow instance handle and writes immutable R2 manifests:

```text
evidence-runs/v1/<instance>/submission.json
evidence-runs/v1/<instance>/input.json
evidence-runs/v1/<instance>/result.json
evidence-runs/v1/<instance>/failure.json
```

### Production bootstrap failure retained

The first live submission used Request ID:

```text
req_wcp2_live_20260802_001
```

It failed with `evidence_run_unavailable` because the Worker code and Workflow binding had been deployed but the Cloudflare Workflow control-plane resource did not yet exist. No Workflow instance was created, no new Effect was dispatched, and the same Request ID remained available for reconciliation.

The provider resource was then created once:

| Field | Value |
|---|---|
| Workflow | `ordivon-evidence-run` |
| resource ID | `3818c7af-2ebd-4d10-8f1f-47f61ea96df8` |
| version ID | `d7e343e7-3b8c-4fa5-9d60-f9228297226f` |
| script | `ordivon-edge` |
| class | `EvidenceRunWorkflow` |
| success/error retention | 3 days |

The original Request ID was resubmitted. It created exactly one provider instance:

```text
evidence-req_wcp2_live_20260802_001
```

### Host-process replacement result

A fresh process retained only `foreign_operation_ref.instance_id`, queried the original provider instance, and recovered a complete result.

| Measure | Result |
|---|---:|
| Workflow status | `complete` |
| durable steps | 2 |
| Artifacts | 5 |
| independently verified Artifacts | 5 |
| verified Artifact bytes | 165,048 |
| unsafe redispatch attempts | 0 |
| duplicate Workflow instances | 0 |
| false completions | 0 |
| World database records | 0 |
| Task-recovery operator interventions | 0 |
| provider release bootstrap interventions | 1 |

Result manifest:

```text
evidence-runs/v1/evidence-req_wcp2_live_20260802_001/result.json
SHA-256 012ca251c91578b599d087d86e469b779a1a3e1073f26a1ec2fface81ed0aec8
```

Evidence: [`../evidence/wcp2/durable-evidence-run-live-20260802.json`](../evidence/wcp2/durable-evidence-run-live-20260802.json).

### Release-chain correction

The release controller now performs the narrow required sequence:

```text
candidate Worker at 0%
→ list Workflow resources
→ validate existing script/class, or bootstrap once when absent
→ run a real evidence.run candidate smoke
→ inspect the original Workflow handle to completion
→ verify the step's Worker version
→ promote the candidate
```

An existing Workflow is not rewritten during later releases. The closeout smoke observed `running → complete` on instance `evidence-req_release_evidence_c6617788cfea486fbc092d520dc07af3`, used the production Worker version, and created no new Workflow resource.

Evidence: [`../evidence/wcp2/release-workflow-smoke-20260802.json`](../evidence/wcp2/release-workflow-smoke-20260802.json).

## WXP-1 — callback continuity

The comparison tested polling alone against callback wake-up plus provider inspect fallback across seven scenarios:

- normal delivery;
- duplicate delivery;
- lost callback;
- early callback;
- stale Host generation;
- callback before registration;
- acknowledgement loss and redelivery.

| Measure | Poll | Callback + poll |
|---|---:|---:|
| trials | 7 | 7 |
| mean completion-discovery latency | 40.00 ms | 23.71 ms |
| provider inspections | 21 | 22 |
| mean Host state | 116.00 bytes | 134.14 bytes |
| false completions | 0 | 0 |
| duplicate Task completions | 0 | 0 |
| unsafe redispatch attempts | 0 | 0 |
| operator interventions | 0 | 0 |

Callback delivery improved the healthy discovery path but did not become execution truth. Lost, early, duplicate, stale-generation, and ambiguous callbacks remained recoverable through the original provider handle and inspect path.

Disposition:

- retain Host generation;
- retain adapter-local callback event deduplication;
- retain provider inspect/poll fallback;
- reject callback completion authority;
- reject an independent World callback journal;
- do not admit B2.

Evidence: [`../experiments/wxp1-callback-continuity/evidence.json`](../experiments/wxp1-callback-continuity/evidence.json).

## WXP-2 — remote-to-remote Artifact movement

The experiment compared:

```text
Host proxy
source → Host → object storage

provider-native
Cloudflare Workflow → R2
Host receives status, ArtifactRef, digest, and result-manifest reference
```

### Deterministic large-Artifact comparison

| Measure | Result |
|---|---:|
| Host bytes avoided | 2,485,632 |
| Host transit reduction | 99.81% |
| source-byte copies through Host | 0 |
| digest verified | yes |

### Live small-Artifact comparison

The live source was a 5,696-byte immutable GitHub file.

| Measure | Host proxy | Provider → R2 |
|---|---:|---:|
| Host transit bytes | 11,392 | 6,460 |
| source-byte copies through Host | 2 | 0 |

Additional live results:

- Host bytes avoided: 4,932;
- Host transit reduction: 43.29%;
- Workflow status observations: 2;
- Workflow elapsed: 11,005 ms;
- source and Provider Artifact SHA-256 matched;
- operator interventions: 0.

The deterministic 99.81% result is not extrapolated to every payload. Fixed submission, status, and manifest bytes dominate small files; the relative benefit increases with Artifact size.

Disposition:

- retain provider-to-R2 transfer;
- retain ArtifactRef, digest, byte length, provenance, and independent Verification;
- reject mandatory Host byte proxying;
- reject an independent World transfer service or universal transfer state machine.

Evidence: [`../experiments/wxp2-remote-artifact/evidence-live.json`](../experiments/wxp2-remote-artifact/evidence-live.json).

## W-A1 deletion and promotion decision

The completed workloads are materially different:

1. callback discovery and recovery under notification faults;
2. durable provider execution and Host replacement;
3. remote-to-remote Artifact movement and integrity verification.

None reproduced one unowned, non-bypassable responsibility that required a shared World authority.

### Retain

- adapter-local capability declarations;
- provider-native Workflow handle and lifecycle;
- private R2 manifests and source Artifacts;
- Host generation and adapter-local callback deduplication;
- provider inspect as external state reconciliation;
- Host-independent Artifact and Task Verification.

### Delete or reject

- writable World capability registry;
- World service or database;
- World Workflow engine;
- World callback journal or completion authority;
- World Artifact transfer service;
- universal `WorldInteraction` schema or provider status enum;
- provider broker, automatic switching, or routing authority;
- WXP-1 B2 shared callback record.

### WCP-3 disposition

WCP-3 is not started. A second external capability class must be selected from a named real workload and expected capability gain, not to satisfy a roadmap sequence. It does not block this closeout.

## Production state

| Field | Value |
|---|---|
| production Worker version | `749dc76c-16cc-4d20-b209-e5df67d70143` |
| implementation source | `bac8c24f61a96bc1c6d717566d1670b4732ffc79` |
| policy | `p1.6.0276f25929e23c23` |
| Workflow resource | `3818c7af-2ebd-4d10-8f1f-47f61ea96df8` |
| production traffic | 100% |

The closeout changes repair release and installation tooling only; they do not alter the deployed Worker bundle.

## Verification

```bash
python3 scripts/check-repository-layout.py
python3 scripts/check-w1-evidence.py
python3 scripts/generate-capability-portfolio.py --check
python3 scripts/generate-wcp-closeout.py --check

python3 experiments/wxp1-callback-continuity/experiment.py
python3 -m unittest -v experiments/wxp1-callback-continuity/test_experiment.py

python3 experiments/wxp2-remote-artifact/experiment.py
python3 -m unittest discover -s experiments/wxp2-remote-artifact -p 'test_*.py' -v

cd providers/cloudflare
pnpm run ci

cd ../../modules/network-observation
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```

## Final boundary

World gained a durable provider execution mode, real consumers, callback and Artifact experiments, and a production release correction. It did not gain a new center of control.

That is the intended result of the program: expand the capability radius of persistent Tasks while deleting every abstraction that did not prove ownership, necessity, and net acceleration.
