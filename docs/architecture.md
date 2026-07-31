# Architecture After W1

## Retained composition

```text
Host Task / Effect / Dispatch
        │
        ├─ required StateRef ──▶ source-native observation adapter
        │                         raw ProbeResult remains source-owned
        │
        └─ idempotency key ───▶ provider adapter
                                  signed request
                                  provider request digest
                                  pending / committed state
                                  Receipt / Artifact
        │
        ▼
Host UNKNOWN → reconcile original Request ID → Observation
        ▼
independent Verification → TaskOutcome
```

This composition completed the W1 response-loss trajectory without a World service, database, universal ID, binding object, or duplicated state machine.

## Authorities

### Host

Owns the semantic lifecycle: Goal, Task, Attempt, Effect, Dispatch, required source references, UNKNOWN, reconciliation frontier, Verification, Artifact acceptance, and completion.

### Provider and adapter

Own native endpoint, signed body, idempotency algorithm, Request ID, lease, policy, capability, Worker identity, pending/committed request state, Receipt, Artifact key, and Artifact metadata.

### Observation module and adapter

Own raw source observation. The adapter may quantize or project fields into Host-compatible evidence, but it does not convert source state into a universal World schema.

### Experiment

Owns arm assignment, fault injection, measurements, and disposition only. Experiment logs are not production authority.

## W1 rejected architecture

The B1 candidate journal repeated six transitions:

```text
interaction prepared
provider Receipt committed
caller response dropped
provider Receipt reconciled
Host verification recorded
Task outcome recorded
```

Each transition already belonged to Host, provider, or the experiment. The separate chain added 4,535 bytes and no recovery capability. It remains historical evidence only.

## Retained modules

- `providers/cloudflare/` remains a real production capability provider.
- `modules/network-observation/` remains a source-native observation/private-operations module.
- inherited Network World, Node, wire, QUIC, VPN, and Security ports remain historical or private surfaces.
- `experiments/w1-host-cloudflare/` remains reproducible research code.

## Conditional future architecture

W2 may test capability negotiation and Effect rebinding only after an observed mismatch or drift failure. No current code implements a broker, router, automatic resolver, or rebinding authority.
