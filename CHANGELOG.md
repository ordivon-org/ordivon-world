# Changelog

All notable changes are recorded here. The project follows a pre-1.0 compatibility policy described in [`docs/compatibility.md`](docs/compatibility.md).

## Unreleased

### Added

- Python `ordivon-world` package pinned to the public Host and Protocol graph;
- Host-facing Cloudflare adapter with deterministic Dispatch-to-request identity;
- Host CAS/Journal persistence for prepared Dispatches, UNKNOWN outcomes and mapped Observations;
- response-loss reconciliation through the original Cloudflare Receipt without redispatch;
- packaged Draft 2020-12 contracts and a local Schema Registry;
- cross-language TypeScript Capability/Receipt fixture validation;
- W3C Trace Context propagation as non-authoritative telemetry;
- repository and live-system `ordivon-world-doctor`;
- wheel, dependency, documentation and local acceptance gates;
- clean-commit live Host→Cloudflare W1 acceptance scenario.

### Fixed

- Cloudflare R2 cleanup enumeration now uses the current `per_page` List Objects parameter instead of the unsupported `limit` parameter;
- GC pagination tests now verify `prefix`, `per_page` and `cursor` behavior;
- relative Schema references resolve exclusively from packaged local resources.

### Changed

- World is now described as a recoverable external capability adapter and condition-observation boundary rather than only a repository containing provider and workstation tools;
- the reactivated Host-facing seam remains an absorbed direct integration, not an independent World runtime or universal interaction layer.
