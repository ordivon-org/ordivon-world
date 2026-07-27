# Repository boundary

A component belongs in Ordivon Edge when its primary question is:

> Which externally hosted capability should execute a bounded task and return a receipt or artifact?

Move it to Ordivon Link when it observes or changes local networking, chooses paths, or implements local transport clients.

Move it to Ordivon Runtime when it owns local process, task, workspace, persistence, or recovery lifecycle.

Forbidden Edge dependencies include:

- VPN-provider detection;
- host route or DNS inspection;
- TUN integration;
- path measurement and selection;
- local Web status for the user's workstation;
- Ordivon Runtime process supervision;
- public site presentation.
