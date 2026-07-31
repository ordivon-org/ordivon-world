# W0 Carrier Inventory and Disposition

Status: frozen at `1ad5085772656df85e14d1bcedd56f9e44e98f0d`

This inventory records the actual starting point for World W1. It does not
rename inherited modules, introduce a World schema, or authorize implementation.
The machine-readable source is [`w0-carrier-inventory.json`](w0-carrier-inventory.json).

## Baseline evidence

The audited revision passed:

- repository layout validation;
- the complete Cloudflare provider CI: typecheck, 40 Node tests passed, one
  environment-dependent test skipped, 19 Python tests passed, policy and
  boundary checks, operational checks, and Wrangler dry-run build;
- network-module formatting and Clippy with warnings denied;
- 82 network-module tests covering observations, bounded process execution,
  QUIC reference behavior, Network World lifecycle, Security-port recovery,
  concurrency, tamper detection, and local presentation.

A read-only live check on 31 July 2026 also observed `edge.ordivon.com` healthy,
with `fetch.v2` and `receipt.v2` ready, a 90-day request-state/Receipt contract,
a 91-day Artifact contract, and a successful HTTP/TLS observation of the W1
target. This is dated baseline evidence, not a permanent deployment assumption;
each W1 Trial must bind the policy, capability, Worker, and observation versions
actually used.

The inventory therefore classifies working code. A `historical` disposition does
not mean broken; it means the surface is not admitted into the active World
boundary.

## Disposition meanings

| Disposition | Meaning |
|---|---|
| `retain` | Real provider or operational capability that remains useful independently of W1. |
| `adapter-only` | Existing source-native capability W1 may call or project, without adopting its internal schema. |
| `historical` | Working fixture, private tool, compatibility surface, or dated research retained without active architectural expansion. |
| `delete-candidate` | No current consumer or no demonstrated failure-preventing value; eligible for later removal after consumer verification. |

## What W1 is allowed to use

W1 admits exactly three inherited surfaces:

1. Cloudflare `fetch` as the external capability;
2. the Cloudflare request-state, Receipt, and Artifact machinery as
   provider-owned evidence;
3. one explicit `link-probe` HTTP/TLS result as a source-native path/target
   observation.

The provider-specific Python client is the direct-integration baseline. W1 may
reference its request and Receipt semantics but must not promote its CLI or
response objects into a shared World API.

## What W1 must not absorb

The following are explicitly outside W1:

- Browser Run and screenshot semantics;
- disposable Node, unshare, body, Sandbox, or reconstruction lifecycles;
- deterministic `NetworkWorldManifest`, `WorldState`, and Security-port state;
- custom wire, QUIC relay, VPN, Surfshark, route control, or protocol selection;
- the local observer SQLite database and console;
- a provider catalog, broker, automatic resolver, or universal interaction ID;
- the complete field inventory in `interaction-model.md`.

These exclusions prevent the existence of inherited code from deciding the new
architecture before the experiment.

## Principal classifications

| Carrier | Disposition | W1 use | Reason |
|---|---|---|---|
| Cloudflare Fetch and HTTPS policy | retain | provider | Smallest complete real external action. |
| Pending/committed state, fencing, Receipt, Artifact, cleanup | retain | provider evidence | Already resolves provider-local transport ambiguity. World must not copy it. |
| Cloudflare Browser Run | retain | none | Valuable provider capability, but rendering adds unrelated variables to W1. |
| Cloudflare release, rollback, policy, and lifecycle tooling | retain | none | Provider operations remain provider-owned. |
| Signed Python provider client | adapter-only | direct baseline | Already invokes, polls, and verifies the provider without a World layer. |
| `link-probe` and used `ProbeResult` fields | adapter-only | observation | Supplies an exact, time-bound path/target observation. |
| `link-observer` and loopback console | adapter-only | none | Useful local operations, but not required for one explicit W1 sample. |
| disposable Node and research control | historical | none | Large inherited body/lifecycle experiment with no W1 requirement. |
| deterministic Network World and Security port | historical | none | Valid fixture, not a production or universal World model. |
| custom wire and QUIC reference implementation | historical | none | W1 uses mature HTTPS. |
| VPN, Surfshark, and transport research | historical | none | Private operations and dated research, not automatic World control. |
| `Device`, `Edge`, `Target`, `Transport`, `RouteDecision` | delete-candidate | none | Declared but unused by current code. |
| universal World Interaction field inventory | delete-candidate | none | Hypothesis ledger only; fields survive only through measured failures. |

## Cleanup decisions deferred until after W1

W0 deliberately performs no mass rename or deletion. After W1, one cleanup may:

- delete the five unused `link-model` declarations after checking external crate
  consumers;
- remove stale future-tense claims that assign separate Edge or Link ownership;
- archive or delete body/Network World acceptance ports when Security no longer
  consumes their historical path;
- keep operational command names where renaming would break local deployment or
  falsify existing receipts.

The architecture follows retained responsibility, not vocabulary cleanup.
