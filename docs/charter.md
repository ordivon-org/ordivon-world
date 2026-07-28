# Ordivon Link Charter

Status: active working definition

Ordivon Link is the programmable network and communication fabric for observing, constructing, perturbing, and controlling the connectivity of distributed Agents and systems.

The current local observation, probe, VPN namespace, and Baseline QUIC implementation is one operational slice. It does not define the project's eventual capability ceiling.

## Responsibility

Link owns network-world identity, topology, paths, communication identities, transport adapters, controlled faults, partitions, discovery, independent network observation, egress facts, and recovery evidence.

It supports three profiles:

- local operations: workstation diagnosis, measurement, and explicit per-command egress;
- range: isolated multi-node networks with deterministic lifecycle and programmable faults;
- adversarial: dynamic topology, deception, competing communication policies, and independent observation.

## Capability and consequence

The evaluated Agent may have broad internal communication and adaptation capabilities. Link separately constrains and proves which external networks and targets are reachable. Reachability is not authorization, and absence of an obvious route is not proof of containment.

## Boundary

Link does not decide campaign objectives, attack or defense strategy, Agent cognition, local Job lifecycle, or remote Node provisioning. Security owns campaigns and verdicts; Host owns cognition and Tasks; Runtime owns trusted-local execution; Edge owns remote bodies and their lifecycle.

The cross-project source charter is maintained in `ordivon-computing/research/charters/LINK-CHARTER-002.md`.
