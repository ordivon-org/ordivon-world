# W1 Frozen Experiment Contract

Status: implementation-ready after W0

## Research question

Does a minimal World correlation record prevent a real lost-response continuity
failure better than direct Host-to-Cloudflare integration, after the provider's
native request identity, Receipt lookup, and Artifact verification are already
used correctly?

A provider retry mechanism winning is a valid result. W1 exists to test the
World boundary, not to justify it.

## Frozen workload

One Host research Task must:

> Fetch the public Example Domain document, retain the returned bytes as a
> provider Artifact, independently verify the Artifact digest and a bounded
> content predicate, then complete the original Task exactly once.

The exact provider request is:

```json
{
  "url": "https://example.com/",
  "maximum_bytes": 65536,
  "timeout_ms": 10000,
  "accept": "text/html"
}
```

The target is already allowlisted and used by provider release smoke tests.
Browser Run is excluded.

## Frozen trajectory

```text
Host Goal / Task / Attempt / Effect
→ one explicit link-probe HTTP/TLS observation for example.com
→ canonical Fetch payload and stable provider request ID
→ POST /v1/fetch
→ provider writes Artifact and commits authoritative Receipt
→ fault injector discards the response before Host admission
→ original caller exits; a fresh Host process continues
→ query GET /v1/receipts/<request-id> before any redispatch
→ retrieve the exact Artifact key carried by the Receipt
→ verify provider SHA-256 metadata, Receipt digest, and content predicate
→ Host records verification and completes the same Task exactly once
```

The single injected fault is
`after-provider-receipt-commit-before-host-admission`. W1 does not change the
path, provider, target, capability, policy, or identity after the fault. Those
variables belong to later conditional experiments.

## Compared arms

### B0 — direct integration

Host invokes the existing signed provider client with a stable Request ID. On
response loss, the fresh process queries the provider Receipt, downloads and
verifies the Artifact, and continues using ordinary Host state. No World-owned
record exists.

### B1 — minimum World correlation

The same provider and Host behavior runs through an experiment-local correlation
record. The record may reference but never copy authoritative Host or provider
state. It contains only:

- experiment and arm identity;
- foreign Host Goal, Task, Attempt, Effect, and Dispatch references and current
  digests or revisions;
- exact path-observation reference and canonical digest;
- provider endpoint label, operation, Request ID, and canonical request digest;
- Receipt and Artifact references returned by the provider;
- fault, reconciliation, verification, and continuation events;
- the final architectural disposition.

This record is evidence for W1, not a stable World schema or production service.

### B2 — optional mature orchestration comparator

A durable Activity comparator may be added only if the existing Runtime/Temporal
experiment environment can express the same provider call naturally without
new permanent World code. It is secondary; B0 and B1 are mandatory.

## Identity and authority

| Fact | Authority |
|---|---|
| Goal, Task, Attempt, Effect, Dispatch, completion | Host |
| path probe command and raw `ProbeResult` | network observation module |
| provider Request ID, pending/committed state, lease generation | Cloudflare provider |
| Receipt, Artifact key, Artifact digest, provider policy/capability/Worker versions | Cloudflare provider |
| Artifact acceptance and Task completion | Host verifier |
| arm assignment, fault injection, measurements, disposition | W1 experiment |

No universal World ID is introduced. Correlation uses separate identities and
content digests.

## Path-observation projection

W1 records a digest over one canonical projection of the source-native probe:

- probe kind;
- collection and sample identity;
- public target label;
- network and route labels;
- protocol;
- start time;
- DNS, connect, TLS, TTFB, and total duration when available;
- HTTP status, success, failure class, and termination.

Raw target URL, remote IP, stderr, host identity, credentials, and unrelated
local-health fields are excluded from the World correlation record. Freshness is
measured from `started_at`; W1 records the observation but does not implement
automatic path selection.

## Fault and recovery rules

1. The fault injector may drop only the caller-visible response after proving
   the provider has committed the final Receipt.
2. The fresh process must query the original Request ID before any new POST.
3. A `pending` Receipt remains unresolved; it is not success or failure.
4. A committed Receipt with matching request digest is authoritative for the
   provider operation.
5. A different request digest is a conflict and cannot reuse the Request ID.
6. Artifact bytes must match both provider metadata and the digest carried by
   the Receipt.
7. Provider success does not complete the Host Task until independent acceptance
   passes.
8. The same Host Task and Effect may receive only one accepted completion.

## Measurements

Each arm reports:

- provider executions and POST attempts;
- duplicate external Effects;
- false success and false failure;
- unsafe redispatch attempts;
- Receipt queries and Artifact downloads;
- recovery latency from fresh-process start to verified continuation;
- operator interventions;
- permanent code and state-object count;
- temporary experiment code and evidence size;
- whether an observation became stale or misleading before completion;
- exact first admissible continuation after restart.

## Acceptance thresholds

Both mandatory arms must:

- execute the provider operation exactly once;
- recover from the injected lost response without blind redispatch;
- verify the exact Artifact independently;
- complete one original Host Task exactly once;
- expose enough evidence to explain the recovery from a fresh process.

B1 earns retention only if it prevents a reproduced error, reduces operator or
recovery cost, or preserves a necessary correlation that B0 cannot express
without equivalent ad hoc state. Merely centralizing references is not a win.

## Closeout matrix

| Result | Decision |
|---|---|
| B0 is equally correct and simpler | absorb semantics into Host plus provider/observation adapters; retain no independent World layer |
| B1 prevents a measured continuity or provenance failure with small stable state | retain the minimum proven World responsibility |
| only provider reliability and probes matter | retain those modules and freeze/delete unified World abstractions |
| one missing capability/rebinding failure appears | open or activate W2 with that exact failure; do not generalize from expectation |

Every B1 field receives `retain`, `move-to-host`, `move-to-provider-adapter`, or
`delete` at closeout.

## Non-goals

No Browser Run, provider broker, route selection, provider replacement, Network
World, custom transport, VPN control, body lifecycle, callback, fan-out/join,
remote-to-remote transfer, general schema, daemon, database, or Protocol change.
