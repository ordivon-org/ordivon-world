# Architecture

## Target semantic overlay

```text
Host Goal / Task / Attempt / Effect
  → Placement Requirement
  → Provider Capability Observation and candidate
  → immutable Placement Binding
  → provider-native body and execution
  → Receipt / Artifact / Observation / residual evidence
  → reconciliation, verification, and continued Task
```

Edge does not own the complete chain. Host and the semantic Kernel own open-work
and Effect history. Providers own physical bodies and native lifecycle. Edge's
candidate responsibility is the exact semantic binding and continuity boundary
between them.

## Current implementation classes

### 1. Cloudflare production provider

`src/index.ts` and its imported modules implement bounded external Fetch and
Browser Run, private R2 Artifacts, request authentication, transaction state,
Receipts, policy, cleanup, observability, and version identity.

```text
signed request
→ authoritative pending state
→ generation-scoped execution
→ Artifact persistence
→ conditional committed Receipt
→ deterministic replay or reconciliation
```

This is operational production capability and the strongest current evidence
for Edge's remote-effect reliability role.

### 2. Provider-neutral body/lifecycle research substrate

`src/node-contracts.ts`, `src/node-lifecycle.ts`,
`src/local-node-adapter.ts`, and the research control session model one narrow
body experiment: deterministic identity input, lifecycle, leases, evidence,
reconstruction, and residual classification.

This substrate remains valuable for experiments. It is not the implemented
Task-level Placement model and does not establish permanent Agent presence.

### 3. Operations

The client, release, GC, lifecycle configuration, and checks operate the
Cloudflare provider. They do not define the future semantic model.

## Missing semantic layers

Current code has no implementation of:

- Task-derived Placement Requirement;
- provider capability candidate comparison;
- immutable Host-visible Placement Binding;
- cross-provider semantic reconstruction;
- multi-body branch/join provenance;
- persistent presence justified by a real workload.

## Idempotency and uncertainty

The production request state machine is retained as a key mechanism:

```text
pending
  → committed
```

Generation fencing, conditional writes, ambiguous-write reread, queryable
pending state, replay, and cleanup prevent transport ambiguity from becoming
invented world history. Future Host integration should bind this physical state
to exact Effect and Dispatch references rather than replace it.

## Artifact boundary

Temporary body state is not Task state. Results become durable Task inputs only
when exported with content identity and exact execution provenance. Future
research should add semantic references without weakening the provider's
private R2, bounded Artifact, digest, and retention guarantees.
