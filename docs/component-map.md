# Phase 0 component map

This map classifies the current repository without moving directories. `keep`
means active code aligned with the durable boundary; `reference` means a
bounded experiment retained for interoperability; `ops` means private
operational/provider tooling; `freeze` means no new general abstraction or
implementation in Phase 0.

## Crates

| Component | Class and authority | Allowed dependency direction | Phase 0 |
|---|---|---|---|
| `link-world` | Long-term Agent-native core. Authoritative for its native Network World manifest and Link World ID, modeled state and mutations, independent event evidence, actor projection, and lifecycle receipts. It does not prove packet isolation for modeled-only effects. | Independent of the other workspace crates. Future adapters consume its native surface without replacing its identity or event authority. | `keep` |
| `link-model` | Local-operations observation/client model. Authoritative only for the serialized local observation, target, route-decision, snapshot, and event types it defines; not for Network World lifecycle or target authority. | Leaf of the observation chain; `link-probe` may depend on it. | `keep` |
| `link-probe` | Local-operations evidence producer. Its bounded results are observations under named conditions, not complete path truth, authorization, or containment proof. | `link-probe → link-model`; `link-observer` may depend on it. | `keep` |
| `link-observer` | Local-operations reducer and sanitized SQLite history. Authoritative for its reduced recorded observations, not raw command output, Network World state, or host/network control. | `link-observer → link-probe → link-model`; `link-console` may depend on it. | `keep` |
| `link-console` | Local-operations read-only presentation. It has no mutation, route, VPN, Runtime, or Network World authority. | `link-console → link-observer → link-probe → link-model`; no dependency on transport or world slices. | `keep` |
| `link-wire` | Bounded Baseline v0 reference wire contract and state machines. It is authoritative only for this experiment's framing contract, not a general Link protocol. | Leaf of the reference transport slice; only `link-transport-quic` depends on it. | `reference` |
| `link-transport-quic` | Quinn/rustls localhost reference adapter for Baseline v0. It has no host-observation, route-control, Network World, or production Edge Node authority. | `link-transport-quic → link-wire`; no cross-dependency with world or observation slices. | `reference` |

General transport expansion is `freeze`: do not turn the reference crates into
a protocol framework or add new in-house transport, TLS, proxy, or
cryptographic machinery. Production choices reuse maintained TLS, QUIC, and
proxy implementations.

## Private operations/provider scripts

These scripts are explicit operator tools, not crate dependencies or public
architecture:

| Script | Operational scope and authority | Allowed dependency direction | Phase 0 |
|---|---|---|---|
| `scripts/ordivon-vpn` | Root-only isolated WireGuard namespace control for explicitly selected commands; no authority over the Network World core or WSL root default route. | May consume private rendered profiles and maintained host tools; no crate may depend on it. | `ops` |
| `scripts/ordivon-vpn-keypair` | Private Surfshark/WireGuard key-pair validation and transactional profile rendering; it defines no public identity system. | Produces private inputs for `ordivon-vpn` and the scanner; no crate dependency. | `ops` |
| `scripts/surfshark-measure` | Provider-specific local route-state and egress measurement. Its outputs are bounded operational evidence, not public architecture or universal path truth. | Invoked directly by an operator; no crate dependency. | `ops` |
| `scripts/surfshark-profile-scan` | Provider-specific profile validation, discovery, and ranking using isolated WireGuard test topology. | Consumes private profiles and maintained host tools; no crate dependency. | `ops` |
| `scripts/install-ordivon-vpn` | Installs the private controller, provider tools, and existing service unit onto an explicitly managed host. | Copies the four operational tools and service unit; no crate dependency. | `ops` |
| `scripts/check-vpn-controller` | Static/synthetic check entry point for the VPN/provider script set. It grants no runtime or network authority. | Validates the operational scripts and invokes their fixture tests. | `ops` |
| `scripts/test-vpn-keypair` | Temporary-fixture validation of key matching, rendering, and fail-closed behavior. | Tests `ordivon-vpn-keypair` and non-mutating controller checks only. | `ops` |
| `scripts/test-surfshark-profile-scan` | Temporary-fixture validation of scanner parsing, redaction, and result handling. | Tests `surfshark-profile-scan`; it is not a production dependency. | `ops` |

The script set orchestrates a maintained VPN implementation; it is not a VPN
core. It must not grow into general-purpose VPN software or container-network
orchestration.

## NetworkAttachment v0 terminology freeze

Before any `NetworkAttachment` v0 design, only the following ownership terms
are frozen:

| Term | Phase 0 meaning and owner |
|---|---|
| **Security World ID** | Security-owned identity for its orchestrated world/context. Link may carry it as a foreign reference but does not mint or replace it. |
| **Link World ID** | Link-owned, component-native identity of a Network World. The current implementation is the content-addressed `nw1-...` identity derived from the normalized manifest. |
| **Edge Node** | Edge-owned remote body/Node. Link may reason about its network presence but does not own its provisioning or lifecycle. |
| **Edge Sandbox Generation** | Edge-owned identity for one lifecycle generation of an Edge sandbox/body. It is not a Link World revision or Link communication-identity generation. |
| **NetworkAttachment** | Future Link-owned network-side binding/evidence concept relating an Edge-owned subject generation to a Link World. No attachment contract or backend exists in Phase 0. |
| **component-native identity** | Each component remains authoritative for its own identities, revisions, and lifecycle. Cross-component orchestration references those identities instead of replacing them with one global ID. |

This is a naming and ownership freeze only. It defines no fields, serialized
Schema, API, cardinality, lifecycle state machine, persistence format, or
data-plane backend, and it does not increase the implemented P0-D capability.

## Layout decision

No directory is moved in Phase 0. The documented authority and dependency
boundaries provide the required separation; moving unchanged files would add
review and history churn without changing behavior or ownership. A later move
requires a concrete dependency, release, or ownership need.

Link does not develop a general-purpose network protocol, VPN core,
cryptography, or container-network orchestration. The bounded Baseline
reference and private WireGuard tooling remain exceptions only in the roles
listed above and continue to reuse maintained implementations.
