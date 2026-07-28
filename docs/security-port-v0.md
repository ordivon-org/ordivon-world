# Security lifecycle port v0

`link-world-security` is the component-owned management surface used by
Ordivon Security. It wraps the existing Network World controller rather than
creating a second Link state machine.

## Interface

Global inputs identify independent private roots and one immutable manifest:

```text
--manifest
--authority-root
--observer-root
--actor-root
--operation-root
--reconstruction-root
```

Commands:

```text
snapshot
execute <prepare|start|freeze|reset|destroy|reconstruct|verify> <operation-id>
reconcile <operation> <operation-id>
residual
```

All successful commands emit one JSON object. Errors use a nonzero exit.

## Binding

The Security binding preserves both identity layers:

- Security owns Campaign ID and Security World ID;
- Link owns the content-addressed `nw1-...` World ID;
- manifest revision is the native component revision;
- the binding root digest is the manifest revision;
- metadata explicitly states which effects are modeled and which loopback
  effect is executable.

## Unknown outcomes

Before a native operation, the port writes a private component operation
journal. Completed receipts replay idempotently. A prepared operation is never
blindly re-dispatched.

For reset, reconciliation requires the Link observer head to be an exact Reset
event at `pre_runtime_revision + 1`. This prevents a lost response from causing
a second revision-changing reset. Destroy reconciliation requires the verified
observer chain to end in Destroyed.

## Residual evidence

After destruction the port distinguishes:

- absent authority state: `clean`;
- retained observer history ending in Destroyed: `expected_retained`;
- retained actor destruction tombstone: `expected_retained`;
- released loopback fixture listeners: `clean`;
- retained component operation journal: `expected_retained`.

Missing or unverifiable observer evidence never becomes clean.

## Reconstruction

Reconstruction creates a fresh isolated root, recreates the same manifest,
compares the content-addressed identity, destroys the reconstructed World, and
removes the fresh root. A destroyed World is never recreated under its original
observer root.

## Boundary

The port does not supervise the foreground fixture process. Ordivon Runtime
owns that process, while Security combines Runtime process evidence with Link
World and observer evidence.
