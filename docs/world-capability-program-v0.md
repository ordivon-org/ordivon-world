# World Capability Program v0

Status: completed through WCP-2, WXP-1, WXP-2, and W-A1; WCP-3 remains conditional

Date: 2026-08-02

## 1. Decision

Ordivon World will develop as two coupled but separately admitted surfaces:

1. a **World Capability Portfolio** containing useful provider and observation adapters;
2. a **World Architecture Laboratory** testing whether any reusable Task-to-world responsibility remains unowned by Host, Runtime, provider-native systems, observation sources, or domain authorities.

The program does not admit an independent World runtime, database, universal interaction object, provider broker, routing authority, or mandatory Host-to-World call path.

```text
capability growth: aggressive and local
failure experiments: aggressive and bounded
shared state and authority: conservative and evidence-gated
```

The strategic objective is to expand the external capability radius of persistent Tasks while preserving exact foreign identity, uncertainty, evidence, recovery, and replacement at lower total cost than direct integration.

## 2. Computer constraints

The program is derived from the Ordivon Computer foundations:

- classical systems remain authoritative for their physical and deterministic contracts;
- Host owns Goal, Task, Attempt, Effect, Dispatch, UNKNOWN, Verification, and completion;
- provider adapters own provider-native request, execution, Receipt, Artifact, policy, capability, and version semantics;
- observation modules own source-native observations;
- domain or Security systems own consequence authority and final validity;
- a new layer requires an unowned, non-bypassable responsibility demonstrated by a reproduced failure, a second materially different workload, measured net benefit, and a deletion test;
- durable constraints must prove net acceleration after latency, attention, maintenance, state duplication, and concentration of control are counted.

W1 already falsified one candidate: an independent correlation journal duplicated Host and provider records without preventing an additional failure. That result is a boundary, not a reason to stop acquiring external capabilities.

## 3. Frontier patterns to inherit

### 3.1 Provider-minted durable handles

MCP Tasks, A2A Tasks, OpenAI background Responses, durable workflow systems, and managed agent runtimes converge on one pattern:

```text
submit
→ receiver/provider mints an opaque durable handle
→ caller polls, streams, or receives a callback
→ caller retrieves provider-owned result and artifacts
```

World therefore stores foreign references in Host state; it does not mint a competing universal World Task ID.

### 3.2 Polling remains the recovery baseline

Push notifications and webhooks reduce latency but do not eliminate ambiguity. Callback endpoints rotate, deliveries duplicate, consumers restart, and notifications can arrive before or after local state changes.

Every callback-capable adapter must retain a provider-native inspect or result path. Push accelerates discovery; polling or provider query reconciles truth.

### 3.3 Durable process and interactive identity are different responsibilities

Current systems increasingly separate:

- long-lived or real-time Agent identity and communication;
- durable run-to-completion workflows;
- provider-native external jobs;
- isolated Sandbox or Runtime execution.

World must not absorb Host cognition or recreate a workflow engine. It selects and binds mature mechanisms through thin adapters.

### 3.4 Explicit handles beat transport sessions

Modern protocol work is moving away from implicit connection-bound state toward explicit receiver-minted handles and routing metadata. World should preserve ordinary opaque references that survive process and connection replacement rather than depend on one transport session.

### 3.5 Capability discovery is versioned evidence, not a universal ontology

A2A Agent Cards, MCP capability negotiation and extensions, provider model/tool catalogs, and cloud service descriptors expose capabilities as source-owned declarations.

World may cache a bounded capability observation with source, revision, observed time, expiry, and digest. It must not claim that all providers share one stable internal capability model.

### 3.6 Trace correlation is diagnostic, not authoritative

OpenTelemetry and agent SDK tracing increasingly cover model turns, tool calls, handoffs, and external operations. Trace context is useful for debugging and cost attribution, but a span is not a provider Receipt, Artifact, authorization decision, or proof of Effect completion.

World propagates trace context where available while retaining source-native evidence separately.

### 3.7 Identity remains a foreign authority

Managed agent platforms increasingly provide workload identity, credential exchange, gateways, and audit trails. World references the exact principal, credential provider, audience, scope, and policy revision used for an interaction. It does not build another IAM system.

## 4. Target architecture

```text
Ordivon Host
  Goal / Task / Attempt / Effect / Dispatch
  UNKNOWN / reconciliation frontier / Verification / TaskOutcome
            │
            │ local adapter call; no World service required
            ▼
Provider or Observation Adapter
  capability observation
  foreign operation handle
  provider-native status / Receipt / Artifact
  callback verification and replay protection when supported
  source-native cancellation or residual cleanup
            │
            ▼
Mature external mechanism
  HTTP API / MCP server / A2A Agent / Workflow / queue / object store
  Browser / Sandbox / device / human participant / cloud provider
```

The repository remains a carrier and experiment boundary. A deployment may contain zero, one, or several adapters without running a World daemon.

## 5. Minimum foreign-reference vocabulary

These are reference roles, not a universal persisted `WorldInteraction` object.

| Role | Meaning | Authority |
|---|---|---|
| `CapabilityRef` | exact source, adapter revision, capability revision/digest, observation time, and expiry used at dispatch | provider or observation source |
| `ForeignOperationRef` | opaque provider-issued task, response, workflow, job, session, request, or execution identifier | provider |
| `ReceiptRef` | provider-native evidence that an operation was admitted, rejected, progressed, or reached a provider-defined state | provider |
| `ArtifactRef` | content-addressed or provider-addressed output plus verification metadata | provider/object store; accepted meaning remains Host/domain-owned |
| `CallbackRef` | callback registration, expected audience, generation, authentication method, and provider handle | provider plus callback receiver |
| `ObservationRef` | source-native external observation with method, time, freshness, and digest | observation source |
| `ResidualRef` | external state that may remain after completion, cancellation, expiry, or replacement | provider/domain owner |
| `TraceRef` | diagnostic correlation only | observability system |

Host may store these as fields of Dispatch, Observation, Verification, wait state, or Task continuation. World does not synchronize them into a second database.

## 6. Adapter facets

A provider adapter implements only the facets its provider can support. No adapter is forced into a fabricated common state machine.

### 6.1 Capability facet

Answers:

- which operations are currently available;
- which input/output contract revision applies;
- which execution modes exist: immediate, pollable, streaming, callback, durable workflow, or session;
- whether inspect, result retrieval, cancellation, callback registration, Artifact export, and residual cleanup exist;
- which identity, policy, region, cost, retention, and expiry conditions apply.

Output is a source-bound `CapabilityRef`, not a global catalog entry.

### 6.2 Dispatch facet

Accepts a Host-owned Effect/Dispatch binding and provider-native input. It returns one of:

- provider-confirmed rejection;
- provider-confirmed admission plus `ForeignOperationRef`;
- locally explicit UNKNOWN when admission cannot be established.

Provider request digest and idempotency rules remain adapter-native.

### 6.3 Inspect/result facet

Queries the original `ForeignOperationRef` before redispatch. It returns provider-native status and new Receipt/Artifact references. The adapter may project a small Host-facing observation, but it must preserve the original provider payload or digest needed for audit.

### 6.4 Callback facet

When available, it provides:

- authenticated callback registration;
- callback generation or endpoint revision;
- event identity and duplicate suppression;
- out-of-order handling;
- acceptance Receipt;
- inspect/poll fallback after missing or ambiguous delivery.

A callback never directly marks the Host Task complete. Host reconciles and verifies the provider-owned result.

### 6.5 Artifact facet

Retrieves, verifies, or transfers provider-native Artifacts. Prefer remote-to-remote movement when the Host does not need to proxy bytes. Host receives a reference, digest, media/type metadata, provenance, and Verification input.

### 6.6 Cancel/close facet

Distinguishes:

- cancellation requested;
- provider cancellation accepted;
- execution actually stopped;
- external consequences already committed;
- residual resources, callbacks, credentials, sessions, or queued work still present.

Unsupported cancellation remains explicit rather than simulated.

## 7. First program workload: durable external evidence run

The first new capability class will be a Cloudflare Workflows-backed **durable external evidence run**. It is materially different from the current immediate Fetch/Browser operations while reusing existing Cloudflare operations, R2 Artifacts, release tooling, and credentials.

### 7.1 Workload

```text
Host research or deployment-verification Task
→ submit immutable evidence-run input manifest
→ Cloudflare Workflow instance is created
→ Workflow performs bounded Fetch/Browser steps
→ each step persists provider-native progress
→ outputs are written directly to private R2
→ Workflow emits one result manifest and Receipt
→ Host may restart or disconnect
→ Host inspects the original Workflow instance
→ Host retrieves only required Artifacts or references
→ independent Verification admits the result
```

The initial consumers are:

1. research-source capture for Ordivon Computer;
2. post-deployment acceptance for Ordivon Web and provider deployments.

The Workflow owns durable step execution. Host owns why the run exists, whether evidence is sufficient, and whether the parent Task completes.

### 7.2 Why Cloudflare Workflows first

- it adds a genuinely different long-running execution mode;
- it supports durable steps, retries, waits, status inspection, and external events;
- it can write Artifacts directly to the existing R2 boundary;
- it avoids building a workflow engine inside World;
- the current Cloudflare adapter, credentials, release path, and operator knowledge reduce implementation cost;
- it creates a realistic callback and remote-to-remote test surface.

Using the same cloud provider does not admit shared World semantics. The experiment must still compare direct Host-to-Workflow integration with any candidate shared mechanism.

## 8. Execution tracks

### WCP-0 — capability portfolio baseline

Deliverables:

- one machine-readable inventory of active adapters and optional facets;
- explicit owner, real consumer, capability revision, retention, cost, consequence class, and deletion trigger for each adapter;
- current Cloudflare Fetch/Browser/R2 and network observation entered as the first portfolio items;
- no runtime registry service.

Exit condition: the inventory is generated from adapter-local declarations and adds no duplicated operational state.

### WCP-1 — real consumers for current Cloudflare capability

Deliverables:

- one Computer research-source capture path;
- one Web or provider post-deployment acceptance path;
- exact Request/Receipt/Artifact references stored in Host-visible evidence;
- usage, failure, recovery, latency, Artifact, and operator-intervention measurements.

Exit condition: the existing provider performs recurring work that was previously manual, ephemeral, or unrecoverable.

### WCP-2 — direct Cloudflare Workflow adapter

Deliverables:

- provider-native Workflow submission;
- opaque Workflow instance reference;
- inspect/result/cancel support where Cloudflare exposes it;
- immutable input manifest and version binding;
- R2 result manifest and Artifact digest verification;
- Host restart recovery without a new World database.

Exit condition: one durable evidence run survives Host replacement and completes through the original foreign handle.

### WXP-1 — callback continuity experiment

Frozen arms:

- B0 polling/inspect only;
- B1 authenticated callback plus inspect fallback;
- B2 the smallest candidate callback-continuity record, only if B1 reveals an unowned failure.

Faults:

- callback delivered twice;
- callback delayed beyond local restart;
- callback delivered to a stale Host generation;
- callback lost;
- callback arrives before local registration commit;
- provider result exists while local callback acceptance is uncertain.

Measures:

- duplicate Effect or completion;
- time to discover completion;
- false completion;
- unresolved UNKNOWN duration;
- operator intervention;
- permanent state and code added.

### WXP-2 — remote-to-remote Artifact experiment

Compare:

- Host downloads and reuploads bytes;
- Workflow/provider writes directly to R2 and Host receives references;
- a candidate shared Artifact transfer responsibility only if the direct provider path cannot preserve provenance or continuation.

Measure transferred bytes through Host, latency, cost, recovery, digest integrity, provenance completeness, and state volume.

### WCP-3 — second external capability class

Select only after WCP-2 and WXP-1 produce real trajectories. Candidate classes:

1. an external programmable Sandbox with long-lived or resumable execution;
2. an A2A remote Agent with task, Artifact, streaming, and push-notification semantics;
3. a model-provider background job with webhook completion;
4. a human or institutional participant with asynchronous acceptance/refusal.

Selection criterion: highest expected Ordivon capability gain and strongest architectural contrast, not easiest API integration.

### W-A1 — architecture decision

After two materially different workloads, perform a deletion test on every proposed shared field or mechanism.

Possible outcomes:

- keep only provider and observation adapters;
- localize one reusable facet in Host or an adapter library;
- admit one thin cross-owner responsibility;
- freeze the experiment;
- delete the candidate abstraction.

A `WorldInteractionV1` schema, World service, broker, or provider marketplace remains unauthorized unless W-A1 evidence explicitly requires it.

## 9. Promotion gates

A shared World responsibility is promoted only if all are true:

1. a named realistic trajectory fails under direct Host plus mature source-native adapters;
2. the failure is not naturally owned by Host, Runtime, one provider, one observation source, Security, or the domain system;
3. a second materially different workload reproduces the same responsibility;
4. bypassing the mechanism causes duplicate Effect, false completion, lost continuation, stale authority/evidence, or materially greater unrecoverable loss;
5. the mechanism reduces total state, recovery steps, operator work, or integration cost after its permanent burden is counted;
6. each field has an observed consumer and deletion condition;
7. provider-native handles, Receipts, Artifacts, identity, policy, and status remain authoritative;
8. the mechanism can be versioned, replaced, and removed without rewriting Task identity.

## 10. Metrics

### Capability

- real Task classes newly enabled;
- recurring consumers and successful runs;
- external resources available without Host-specific code growth;
- useful Artifact and evidence production.

### Continuity

- recovery after Host/process/provider interruption;
- unsafe redispatch attempts;
- duplicate external Effects;
- false Task completion;
- time spent in UNKNOWN;
- operator interventions;
- successful provider or endpoint replacement without Task replacement.

### Evidence

- exact provider operation and capability revision binding;
- Receipt and Artifact verification rate;
- stale observation/Claim invalidation;
- callback duplicate and replay handling;
- residual external state visibility.

### Cost

- adapter code and maintenance;
- persistent state bytes;
- external latency and provider cost;
- CI/deployment time;
- Host complexity added or removed;
- participant attention and operational interruptions;
- control concentration and replacement cost.

## 11. Repository shape

The existing top-level shape remains valid:

```text
providers/
  cloudflare/
    immediate Fetch / Browser / R2 operations
    future Workflow adapter and evidence-run implementation
modules/
  network-observation/
experiments/
  w1-host-cloudflare/
  future callback and Artifact-transfer experiments
evidence/
docs/
```

Do not add `world-server/`, `world-db/`, `world-router/`, or `world-protocol/` from this design.

If adapter-local declarations become useful, place them beside the adapter and generate a read-only portfolio view. Do not introduce a writable central registry.

## 12. Explicit non-goals

- no universal provider/task status enum beyond Host's existing semantic uncertainty and completion roles;
- no forced conversion of MCP Tasks, A2A Tasks, OpenAI Responses, Workflow instances, Sandbox sessions, or human commitments into one object;
- no blind retry or automatic provider switching;
- no path, provider, participant, or identity optimization engine;
- no proxying of all external bytes through Host or World;
- no duplicate IAM, workflow, queue, Browser, Sandbox, network, or observability implementation;
- no promotion from trace correlation to execution truth;
- no generic multi-Agent society or external-world platform before a bounded consumer proves it.

## 13. Immediate order

```text
1. keep the current production Worker stable and publish the reviewed source through a separate canary decision
2. integrate current Fetch/Browser/R2 into two recurring real Ordivon consumers
3. add the adapter capability inventory as generated evidence
4. implement the direct Cloudflare Workflow evidence-run slice
5. run Host-restart recovery
6. run callback continuity with poll fallback
7. run remote-to-remote Artifact movement
8. select a second external capability class
9. perform the W-A1 deletion and promotion decision
```

No later item blocks useful earlier capability work. Any shared abstraction discovered during implementation remains experiment-local until its promotion gate is met.

## 14. Reference paradigms

The design was compared against the following current primary-source patterns:

- Model Context Protocol Tasks and explicit task handles;
- MCP Streamable HTTP and explicit routing/context headers;
- Agent2Agent Task, Artifact, streaming, and push-notification semantics;
- OpenAI background Responses, webhooks, Agents SDK handoffs, sessions, and tracing;
- Cloudflare Workflows, Agents plus Workflows, Durable Objects, Browser, and R2;
- Temporal durable execution;
- OpenTelemetry and GenAI semantic-convention practice;
- managed agent runtimes that separate harness, runtime, identity, gateway, tools, and observability.

These systems are baselines and implementation substrates. Their existence does not by itself justify another Ordivon layer.

### Primary-source reading set

| Paradigm | Primary source |
|---|---|
| durable MCP request handles | <https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks> |
| explicit MCP routing and extension evolution | <https://modelcontextprotocol.io/specification/draft/changelog> |
| A2A Tasks, Artifacts, streaming, and push | <https://a2a-protocol.org/dev/specification/> |
| OpenAI webhook completion events | <https://platform.openai.com/docs/api-reference/webhook-events> |
| minimal Agent/Handoff/Session/Trace primitives | <https://openai.github.io/openai-agents-js/> |
| Cloudflare durable multi-step execution | <https://developers.cloudflare.com/workflows/> |
| Agent identity plus Workflow execution split | <https://developers.cloudflare.com/agents/concepts/workflows/> |
| stateful coordination substrate | <https://developers.cloudflare.com/durable-objects/> |
| crash-proof workflow baseline | <https://docs.temporal.io/> |
| telemetry semantic-convention discipline | <https://opentelemetry.io/docs/specs/semconv/> |
| managed harness/runtime separation | <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html> |
| managed workload identity baseline | <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html> |

## 15. Implementation closeout

WCP-0, WCP-1, WCP-2, WXP-1, WXP-2, and W-A1 completed on 2026-08-02. The measured result is documented in [`wcp0-wxp2-results.md`](wcp0-wxp2-results.md) and the generated closeout evidence is [`../evidence/wcp0-wxp2-closeout.json`](../evidence/wcp0-wxp2-closeout.json).

The program retained adapter-local declarations, the Cloudflare Workflow capability, R2 manifests, callback wake-up with inspect fallback, and provider-to-R2 Artifact movement. It rejected every candidate shared World authority because none reduced an observed cross-owner failure after permanent state and operational cost were counted.

WCP-3 is deliberately deferred. It may begin only when a named external workload offers substantial capability gain and architectural contrast. It is not required to keep this completed program open.
