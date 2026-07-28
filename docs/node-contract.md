# Provider-neutral Edge Node contract

Status: implemented contract plus one narrow research conformance/reference
provider

The contract is split deliberately:

- `src/node-contracts.ts` contains platform-neutral identity, profile,
  capability, resource, membership, lifecycle, lease, observation, evidence,
  and reconstruction types;
- `src/node-lifecycle.ts` contains the deterministic lifecycle state machine;
- `src/local-node-adapter.ts` owns one disposable, one-shot Linux namespace
  reference body provider;
- `config/edge-node-policy.json` owns profile and local-provider bounds.

The Cloudflare Worker continues to use `config/edge-policy.json` and
`src/policy.ts`. Research policy is not part of the production policy
fingerprint, Worker bundle, routes, bindings, or release controller.

## Scope

The local-unshare adapter is an Edge research-profile conformance/reference
provider, not a second Runtime and not a general container provider. It can
create, admit, make eligible, execute once under a bounded lease, capture
evidence, retire, and destroy one digest-pinned body. Its scope is frozen at
exercising lifecycle, fencing, evidence, reconstruction, and isolation
contracts. It does not schedule Tasks, manage workspaces, install tools,
supervise arbitrary host processes, recover Runtime work, select connectivity,
or orchestrate other providers.

The implemented source format is intentionally only a digest-pinned Bash
fixture. OCI unpacking, arbitrary source archives, writable overlays, package
installation, generic process commands, and cloud orchestration are not
implemented. OCI/runc-backed Providers are future direction only, not Phase 0
work or permission to expand this adapter into a self-developed container
Runtime.

## Terminology

A Node is the long-lived semantic identity of an Agent presence. A Sandbox is
one isolated instance of that Node on a Provider, including its generation. An
Execution is one bounded action inside a Sandbox.

The current contract has no independent Sandbox type. `EdgeNodeIdentity` still
binds generation in its identity input, while the local adapter couples a body,
lifecycle record, and lease generations. Those are current implementation
facts, not a completed standalone Sandbox abstraction.

## Identity

`edgeNodeIdentity` hashes canonical UTF-8 JSON containing:

- Node class and provider;
- source or image descriptor;
- profile-scoped capability and consequence descriptor;
- policy revision and resource profile;
- Campaign ID, World ID, and membership generation;
- Node generation.

Canonical object keys use code-unit ordering rather than locale-sensitive
sorting. Non-JSON values, non-finite numbers, duplicate or non-canonical plane
sets, invalid digests, and invalid budgets are rejected. The returned identity
contains a normalized deep copy, so later mutation of the caller's input does
not change the identity record.

The resulting ID is `edge-` plus the first 32 characters of the full SHA-256.
Evidence and reconstruction Receipts bind the complete identity digest.
Strings are byte-exact; Unicode lookalikes are not normalized or treated as
equal.

## Profiles and credentials

`config/edge-node-policy.json` declares three non-interchangeable authorities:

| Profile | Provider | Credential mode | Consequence scope | Status |
| --- | --- | --- | --- | --- |
| production | Cloudflare Worker | externally profile-scoped | production allowlist | existing, outside this adapter |
| research | local `unshare` | none | range-local only | implemented |
| adversarial-range | deferred | externally profile-scoped | range-local only | deferred |

The local adapter accepts only the configured research authority with
`credential_mode: "none"`. Its child environment is constructed from an
allowlist and never inherits the parent environment. No API accepts Cloudflare
bindings, tokens, or production policy authority.

These checks are not a credential vault. The trusted management process must
still run in a research credential domain. A compromise of that management
process can use its host permissions; profile labels cannot prevent that.

## Planes and trust

```text
local provider root
├── management/<node-id>/       identity, lifecycle journal, lease fence
├── nodes/<node-id>/rootfs/     disposable experiment body
├── observation/<node-id>/gN/   committed execution Receipt and observations
└── evidence/<node-id>/gN/      committed evidence Receipt and artifacts
```

Only `nodes/<node-id>/rootfs` enters the evaluated body. The management,
observation, and evidence roots are absent from its chroot. Top-level and
per-Node symbolic-link traversal fails closed.

The four planes are separate relative to the evaluated workload, not separate
OS accounts or independent services. They share the trusted provider process
and filesystem owner. Read-only modes discourage accidental mutation;
SHA-256 verification detects later mutation. They do not make evidence
immutable against a compromised host administrator.

## Lifecycle, idempotency, and restart

The provider-neutral state machine defines:

```text
declare → provision → admit → start → freeze
                                  ├→ evidence capture → retire → destroy
                                  └→ snapshot → restore → admit
```

Operation IDs are bounded and globally bound to one operation. Repeating a
completed or uncertain operation ID replays its outcome. Rebinding the ID to a
different operation is rejected.

Provision and destroy are journaled as uncertain before their filesystem
effect. No other operation can dispatch until reconciliation:

- provision accepts existence only when a sealed rootfs manifest, source
  digest, Node ID, and full identity digest all verify;
- an absent or invalid provision body reconciles to `declared` and only the
  matching Node body staging root is removed;
- destroy considers any residual matching Node body present and reconciles to
  `retired`; complete absence reconciles to `destroyed`.

Identity, lifecycle outcomes, uncertainty, and the highest lease generation use
atomic replacement and file/directory `fsync`. On restart, `declare` reloads
and validates the journal. An identity-only journal is safely recoverable as
`declared`; state without identity fails closed. Lease tokens are deliberately
not persisted, so every manager restart invalidates outstanding leases.

Operations are serialized per Node within one adapter instance. The current
profile assumes a single authoritative management process. Cross-process
locking or distributed consensus is deferred and two adapter processes must
not manage the same provider root concurrently.

`start` makes this one-shot body eligible for execution; it does not start a
long-lived daemon. `freeze` is consequently a lifecycle admission gate between
runs, not `SIGSTOP`. Provider-neutral snapshot/restore states exist, but the
local adapter rejects them because namespace/chroot isolation provides no
coherent memory checkpoint. Evidence capture is the implemented alternative.

## Leases and execution

Lease generations increase monotonically and issuing a new generation fences
all prior in-memory tokens. Tokens are required for execution and evidence
export but are absent from journals and Receipts. Expiry, authority, profile,
Node ID, lease ID, and current generation are checked together.

The live executor:

- creates new user, mount, PID, network, IPC, and UTS namespaces;
- uses private mount propagation;
- bind-mounts only the prepared rootfs and remounts it read-only;
- chroots before executing the digest-pinned entrypoint;
- exposes no `/proc`, `/dev`, host root, workspace, management, observation, or
  evidence path;
- starts with an empty network namespace and a replacement environment;
- copies only the configured trusted Bash executable and its resolved dynamic
  dependencies into a freshly created staging root;
- rejects rootfs symbolic links, dependency collisions, oversized entrypoints,
  oversized rootfs output, and unsealed or subsequently modified bodies.

Wall time, total stdout/stderr bytes, action count, entrypoint size, rootfs
bytes, and virtual address space are enforced. The executor applies
`RLIMIT_NPROC`, but namespace-root semantics vary by kernel; a hard process and
CPU ceiling requires cgroup delegation and remains deferred. Killing the
`unshare` namespace leader also kills its PID-namespace descendants.

Linux user namespaces may be disabled by the host. The live provider fails
closed in that case. Default tests use an injected deterministic executor;
the opt-in test exercises the complete live adapter on a supporting host.

## Observation and evidence

One action is committed to `observation/<node-id>/gN` through a staging
directory and atomic rename. stdout, stderr, exit status, their descriptors, and
the execution Receipt are generation-scoped. A failed executor receives a
bounded failed Receipt without raw host diagnostics.

Evidence export:

1. verifies observation size and SHA-256;
2. constructs safe artifact names from validated observation IDs;
3. binds Node ID, full identity digest, lease generation, observation IDs, and
   artifact metadata into an evidence-manifest root;
4. writes and `fsync`s a staging generation;
5. atomically renames it to the committed generation;
6. persists the lifecycle capture.

Duplicate export returns the already committed Receipt only after recomputing
the root and revalidating every artifact. Conflicting or tampered evidence fails
closed. A restart after evidence rename but before lifecycle journal update
detects the valid committed generation and completes the capture transition.

Atomic rename and `fsync` are subject to the guarantees of the backing local
filesystem. This profile does not claim WORM storage or protection from a
compromised management host.

## Reconstruction

A reconstruction Receipt requires exactly one digest-matching source, policy,
capability, and resource input, each marked required. Names and kinds must be
unique. A snapshot input is rejected unless the lifecycle has a coherent
snapshot, which the local adapter cannot currently create.

The input root also binds Node ID, full identity digest, Campaign, World, Node
generation, and membership generation. Ordivon Runtime or Host must still
supply those digest-matching inputs to a new provision request; the Receipt
does not recreate a Task or workspace.

## Exact validation commands

```bash
pnpm install --frozen-lockfile
pnpm run ci
```

Focused provider-neutral tests:

```bash
node --import tsx --test test/node-lifecycle.test.ts
node scripts/check-node-policy.mjs
```

Opt-in end-to-end live isolation test:

```bash
ORDIVON_EDGE_LIVE_TEST=1 node --import tsx test/node-lifecycle.test.ts
```

## Integration points

- **Security** supplies Campaign/World identity, consequence approval, and
  policy revisions; it does not receive lease tokens or lifecycle authority.
- **Link** may later consume an explicit generation-bound attachment handle for
  approved range-local connectivity. It does not own or advance Sandbox
  lifecycle. This implementation contains neither that handle nor route, DNS,
  VPN, path-selection, or transport client code.
- **Host** chooses a body and consumes verified observations and Receipts; the
  evaluated Agent cannot mutate authoritative lifecycle state or the evidence
  root through the body.
- **Runtime** schedules trusted-local Tasks, supervises trusted
  supervisor/control processes, and supplies reconstruction inputs. Edge does
  not own Runtime Tasks, workspaces, or recovery; Runtime supervision of an
  Edge process does not transfer body/Sandbox semantics or lifecycle authority.
- **Cloudflare production** remains in `src/index.ts`, the original production
  policy, R2 transaction state, and `scripts/ordivon_edge_release.py`.

Direction beyond Phase 0 includes externally supplied OCI/runc-backed
Providers, checkpoint/restore, multi-Node World recovery, independently
administered evidence storage, adversarial-range Providers, and Link-managed
range connectivity. None is implemented here. In particular, the
local-unshare reference provider must not acquire generic image management,
writable workspaces, daemon supervision, scheduling, or container-Runtime
responsibilities.


## Security control session

`src/research-node-control.ts` and
`scripts/ordivon_edge_node_control.ts` expose the local provider through a
bounded long-lived JSONL session. The session binds one immutable identity,
keeps non-persistent lease tokens in memory, persists completed Security
operation Receipts, and provides reset, fresh-root reconstruction, and residual
classification without changing production Worker routes or policy.

The session does not solve cross-process authority. One trusted process still
owns a provider root, and two sessions must not manage the same root
concurrently. See [`research-node-control-v0.md`](research-node-control-v0.md).
