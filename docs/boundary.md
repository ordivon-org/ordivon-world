# Repository boundary

A component belongs in Ordivon Edge when its primary question is:

> Through which remote body should an Agent exist and act, under which capability and consequence profile, and with what lifecycle and evidence?

Move it to Ordivon Link when it observes or changes local networking, chooses paths, or implements local transport clients.

Edge may own disposable browsers, containers, virtual machines, service emulators, sensors, decoys, and remote Nodes. The current Cloudflare Worker is the production profile, not the repository ceiling.

Move it to Ordivon Runtime when it owns local process, task, workspace, persistence, or recovery lifecycle.

Forbidden Edge dependencies include:

- VPN-provider detection;
- host route or DNS inspection;
- TUN integration;
- path measurement and selection;
- local Web status for the user's workstation;
- Ordivon Runtime process supervision;
- public site presentation.
