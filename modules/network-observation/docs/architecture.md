# Architecture

## Target semantic overlay

```text
Host Goal / Task / Attempt / Effect
  → Connectivity Requirement
  → Path and Identity Observations and candidates
  → immutable Connectivity Binding
  → mature network, identity, discovery, or messaging mechanism
  → path-conditioned Observation / Artifact / failure / delivery evidence
  → invalidation, reconciliation, handoff, and continued Task
```

Link does not own the complete chain. Host and the semantic Kernel own open-work
and Effect history. Classical network and identity systems own physical
mechanisms. Link's candidate responsibility is the exact Task-conditioned
relation, evidence, and recovery boundary between them.

## Current implementation classes

### 1. Observation chain

```text
link-model ← link-probe ← link-observer ← link-console
```

This slice defines bounded facts, collects path and service evidence, reduces
local state, persists sanitized history, and presents it read-only. It is the
closest current substrate for Host-consumable path Observations.

### 2. Network-condition research laboratory

`link-world` defines deterministic manifests, identities, modeled mutations,
independent events, actor projections, lifecycle, and a narrow loopback fixture.
It can exercise evidence and reset hypotheses but does not implement a Task-level
Connectivity Binding or packet-enforced production data plane.

### 3. Reference transport

```text
link-wire ← link-transport-quic
```

This is a bounded interoperability experiment using maintained QUIC and TLS
libraries. It is not Link's general architecture.

### 4. Private operator tools

The WireGuard namespace and Surfshark scripts provide explicit private
operations and measurement. They do not define public Link semantics and are not
dependencies of the crate graph.

## Missing semantic layers

Current code has no implementation of:

- Task-derived Connectivity Requirement;
- logical relation identity distinct from path and endpoint;
- immutable Host-visible Connectivity Binding;
- path-conditioned Artifact or Claim provenance;
- dependency-driven invalidation after path/identity change;
- delivery/reply reconciliation and participant handoff;
- demonstrated value of Network World above mature network mechanisms.

## Evidence model

A useful observation should eventually preserve:

```text
source / target / method / protocol / path label / endpoint identity
policy revision / timestamp / freshness / uncertainty / result
```

Route labels and modeled world state remain controlled facts, not complete packet
truth, authorization, or containment proof.

## World experiment boundary

Network World may remain valuable for Security and capability experiments. Its
long-term admission requires two workloads that need the same world identity,
reset, observation, invalidation, and replay semantics above maintained
namespace, CNI, service-mesh, SDN, or traffic-control backends.
