# Research Node control v0

`ordivon_edge_node_control.ts` is the component-owned management surface for
Security's research-local Node composition. It directly uses
`LocalDisposableNodeAdapter`; it does not implement a second Edge lifecycle.
`ResearchNodeControlSession` and the JSONL process are supervisor/control, while
the adapter is the narrow research conformance/reference Provider.

## Transport

The process reads one JSON request per stdin line and writes one JSON response
per stdout line. It is a long-lived session:

```bash
pnpm node-control -- --root /private/edge-provider-root
```

Actions:

- `declare` — bind one immutable Node identity and digest-pinned entrypoint;
- `snapshot` — return the Security binding snapshot and native inspection;
- `execute` — run prepare, start, freeze, reset, destroy, reconstruct, or verify;
- `reconcile` — query the original component operation identity;
- `residual` — classify disposable body and retained evidence state.

## Why it is long-lived

Edge lease tokens are deliberately absent from journals and Receipts. A manager
restart invalidates them. The JSONL session therefore keeps one short-lived
lease token in memory across start, execution, and evidence capture. A one-shot
CLI would either be unable to complete that lifecycle or would need to persist
a bearer credential.

Completed Security operation receipts are persisted under the private control
root. Reusing the same operation ID replays the receipt. Binding an operation ID
to a different operation fails closed.

## Reset and reconstruction

The local provider cannot snapshot a running namespace. Control-level reset
therefore destroys the disposable body, advances a provider epoch, recreates a
fresh provider root, and re-admits the same deterministic Node identity.

Reconstruction uses a separate fresh root, verifies the declared source,
policy, capability, and resource inputs, emits the native reconstruction
Receipt, destroys the temporary body, and removes the root. It does not restore
memory or a long-running process.

## Residual evidence

After destruction:

- absent `nodes/<node-id>` body: `clean`;
- retained management identity and lifecycle journal: `expected_retained`;
- retained generation-scoped evidence: `expected_retained`.

The control surface does not claim WORM evidence or protection from a
compromised management host.

## Boundary

The session supports only the credential-free research authority and the local
unshare provider. It does not expose Cloudflare bindings, production
credentials, arbitrary commands, package installation, route selection, or
Link attachment. Runtime may supervise this trusted process, but does not
thereby own its Node/body lifecycle.

This session is not an independent Sandbox abstraction or a general container
service. The current code has no standalone Sandbox type. local-unshare remains
a narrow conformance/reference Provider and must not expand into image
management, writable workspaces, daemon supervision, or scheduling.
