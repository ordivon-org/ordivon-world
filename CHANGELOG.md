# Changelog

All notable changes are recorded here. The project follows a pre-1.0 compatibility policy described in [`docs/compatibility.md`](docs/compatibility.md).

## Unreleased

### Added

- Python `ordivon-world` package pinned to the public Host and Protocol graph;
- Host-facing Cloudflare adapter with deterministic Dispatch-to-request identity;
- Host CAS/Journal persistence for prepared Dispatches, UNKNOWN outcomes and mapped Observations;
- response-loss reconciliation through the original Cloudflare Receipt without redispatch;
- packaged Draft 2020-12 contracts and a local Schema Registry;
- cross-language TypeScript Capability and multi-state Receipt fixture validation;
- W3C Trace Context propagation as non-authoritative telemetry;
- repository and live-system `ordivon-world-doctor`;
- wheel, dependency, documentation and local acceptance gates;
- clean-commit live Host→Cloudflare W1 acceptance scenario;
- Browser Manifest machine contract and three-Artifact bundle reader;
- Browser response-loss and fresh-Host continuity tests;
- Fetch/Browser dual-mode clean-revision acceptance runner;
- pinned GitHub CI, CodeQL, secret scanning and dependency automation.

### Fixed

- Cloudflare R2 cleanup enumeration now uses the current `per_page` List Objects parameter instead of the unsupported `limit` parameter;
- GC pagination tests now verify `prefix`, `per_page` and `cursor` behavior;
- the installed GC controller now completes successfully and remains scheduled by the active timer;
- relative Schema references resolve exclusively from packaged local resources;
- contract fixture type checking no longer changes the Worker release-input digest;
- Browser non-PNG output now fails before Artifact commit;
- Receipt construction and JSON Schema reject succeeded operations without their required evidence and reject evidence on failed or pending outcomes.

### Changed

- World is now described as a recoverable external capability adapter and condition-observation boundary rather than only a repository containing provider and workstation tools;
- the reactivated Host-facing seam remains an absorbed direct integration, not an independent World runtime or universal interaction layer;
- Worker source provenance and test-only TypeScript compilation scopes are kept separate.

### Verified

- the portable P0–P1 matrix covers Python, Worker, provider-controller, network, dependency audit, contract, documentation and isolated wheel installation gates;
- live doctor reports current installation, Worker inputs, R2 lifecycle, GC and network prerequisites as healthy;
- live W1 proves one external POST, injected response loss, Host UNKNOWN, fresh-Host reconciliation by the original request ID, digest-verified Artifact recovery, independent Verification and no Task completion claim.
