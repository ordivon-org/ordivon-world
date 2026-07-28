# Repository boundary

A component belongs in Ordivon Edge when its primary question is:

> Through which remote body should an Agent exist and act, under which capability and consequence profile, and with what lifecycle and evidence?

Move it to Ordivon Link when it observes or changes local networking, chooses paths, or implements local transport clients.

Edge may define body/Sandbox semantics for disposable browsers, containers,
virtual machines, service emulators, sensors, decoys, and remote Nodes through
bounded Provider adapters. The current Cloudflare Worker remains the
operationally critical production Provider, not the whole repository.

Edge does not build a container runtime, VM orchestrator, network stack,
scheduler, or workspace runtime. local-unshare is a narrow research
conformance/reference Provider, not the seed of a general container Runtime.
OCI/runc-backed Providers remain future direction only.

Move it to Ordivon Runtime when it owns a trusted supervisor/process, local
Task, workspace, persistence, or recovery lifecycle. Runtime supervision of a
trusted Edge process does not transfer Edge body/Sandbox semantics.

Ordivon Link may consume a future generation-bound attachment handle. Link
does not own or advance the attached Sandbox lifecycle, and Phase 0 does not
implement that handle.

Forbidden Edge dependencies include:

- VPN-provider detection;
- host route or DNS inspection;
- TUN integration;
- path measurement and selection;
- local Web status for the user's workstation;
- Ordivon Runtime process supervision;
- public site presentation.
