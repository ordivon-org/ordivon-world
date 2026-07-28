# Capability gaps

The repository now contains a mature narrow Cloudflare production profile, a
provider-neutral Node contract, a narrow research-local unshare
conformance/reference body, and a component-owned Security control session. It
is not yet a heterogeneous or long-lived distributed execution fabric.

## P0 status

| Capability | Current state |
|---|---|
| Provider-neutral Node identity, membership, policy, capability, and resource contract | implemented |
| Provision, admit, start, freeze, retire, and destroy semantics | implemented |
| Snapshot and restore contract | defined; local provider execution pending |
| Production, research, and adversarial-range authority profiles | separated; adversarial provider pending |
| Disposable provider beyond Cloudflare Worker | narrow lifecycle/isolation conformance reference implemented as local unshare/chroot; not a general container Provider |
| Management, experiment, observation, and evidence plane separation | implemented relative to evaluated body; same host account remains trusted |
| Identity-bound one-way evidence export | implemented |
| Lease generation and uncertain provision/destroy reconciliation | implemented |
| Reconstruction receipts | implemented |
| Stable Security control surface | implemented as long-lived JSONL session |
| Exact package-manager toolchain | pinned to pnpm 10.33.2 |
| Cross-process single-authority locking | pending |
| Persistent Link-managed network attachment | pending; P0-D design boundary |
| Hard cgroup CPU/process enforcement | pending |
| Long-running body freeze/resume | pending |

The JSONL control session remains long-lived intentionally. Lease tokens are
held only in memory and are invalidated on manager restart. Turning it into a
one-shot CLI would require persisting bearer authority or weakening the lease
boundary.

The current body remains one digest-pinned Bash fixture executed once inside a
fresh namespace/chroot. It is sufficient for lifecycle and evidence
composition, not for long-horizon Agent execution.

## Direction beyond Phase 0

The following items are architectural direction, not authorized Phase 0
implementation work:

- external OCI/runc-backed Providers or verified source Providers;
- persistent container or microVM bodies;
- browser, VM, service-emulator, sensor, and decoy Node classes;
- checkpoint/restore plus partial-world recovery;
- controlled dependency and Tool installation in research profiles;
- heterogeneous cloud and user-owned provider adapters;
- resource accounting and failure-domain placement;
- WORM or independently administered evidence storage.

## P2 — frontier work

- multi-region and cross-provider placement;
- accelerator and specialized hardware bodies;
- long-lived migratable Agent bodies;
- physical or IoT interfaces in isolated facilities.

A future persistent Provider may expose a generation-bound attachment handle
that Ordivon Link consumes without acquiring Sandbox lifecycle authority. That
handle and Provider are not implemented in Phase 0.

The local-unshare reference provider must not be expanded to reach these
directions. Edge will not grow it into a container runtime, VM orchestrator,
network stack, scheduler, or workspace runtime.
