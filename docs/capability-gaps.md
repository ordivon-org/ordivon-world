# Capability gaps

The current repository is a mature narrow Cloudflare production slice, but it is not yet a distributed external presence and execution fabric.

## P0 — required before heterogeneous Edge claims

1. A provider-neutral Edge Node contract covering identity, class, provider, source or image, capabilities, policy, resources, and lifecycle state.
2. Provision, admit, start, freeze, snapshot, restore, retire, and destroy semantics.
3. Separate production, research, and adversarial profiles with independent credentials and authority.
4. At least one disposable container or virtual-machine adapter beyond Cloudflare Worker.
5. Management-plane separation from evaluated Nodes and authoritative evidence storage.
6. A one-way identity-bound evidence export contract.
7. Node lease and reconciliation for uncertain creation, execution, loss, and destruction.
8. Reconstruction receipts proving which declared inputs recreate a destroyed Node.

## P1 — distributed presence

- browser, container, VM, service-emulator, sensor, and decoy Node classes;
- campaign membership and multi-Node coordination identity;
- checkpoint and restore plus partial-world recovery;
- controlled dependency and Tool installation in research profiles;
- heterogeneous cloud and user-owned provider adapters;
- resource accounting and failure-domain placement.

## P2 — frontier work

- multi-region and cross-provider placement;
- accelerator and specialized hardware bodies;
- long-lived migratable Agent bodies;
- physical or IoT interfaces in isolated facilities.

The first implementation target should be one disposable local container or VM profile sharing the same identity and receipt concepts as the production Cloudflare profile.
