# Capability gaps

The repository now contains a mature narrow Cloudflare production profile, a
provider-neutral Node contract, a real research-local unshare body, and a
component-owned Security control session. It is not yet a heterogeneous or
long-lived distributed execution fabric.

## P0 status

| Capability | Current state |
|---|---|
| Provider-neutral Node identity, membership, policy, capability, and resource contract | implemented |
| Provision, admit, start, freeze, retire, and destroy semantics | implemented |
| Snapshot and restore contract | defined; local provider execution pending |
| Production, research, and adversarial-range authority profiles | separated; adversarial provider pending |
| Disposable provider beyond Cloudflare Worker | implemented as local unshare/chroot |
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

## P1 — distributed presence

- OCI images or verified source archives and writable overlays;
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

The next large step is not another lifecycle type. It is a persistent provider
whose network namespace can be attached by Ordivon Link without transferring
Node ownership to Link.
