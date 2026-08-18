# Canonical Registry and Provenance

## Registry semantics

A canonical World research registry entry must distinguish at least:

1. canonical identity / code;
2. project or subarchitecture;
3. truth role;
4. Foundation standing;
5. closure scope;
6. historical research order;
7. canonical artifact pointer;
8. reopen condition;
9. provenance / durable Git reachability.

Do not derive ontology priority, global owner priority, or a roadmap from a WDF/TSA number.

## Canonical registry

| Identity | Project | Truth role | Standing | Canonical evidence |
|---|---|---|---|---|
| WDF0 | World / Reality | root research grammar | FROZEN Foundation v1 | [`../foundations/WDF0-CLOSEOUT.md`](../foundations/WDF0-CLOSEOUT.md) |
| WDF1 | World / Reality | modal root stratum | FROZEN Foundation v1 | [`../foundations/WDF1-CLOSEOUT.md`](../foundations/WDF1-CLOSEOUT.md) |
| WDF2-A→N | Counterfactual Architecture | deep research history | complete; not frozen Foundation | WDF2 detailed artifacts under [`../foundations/`](../foundations/) |
| WDF3-A→L | Categorial Reality Architecture | deep research history | complete; not frozen Foundation | [`../foundations/WDF3-A-WDF3-L-CATEGORIAL-REALITY-ARCHITECTURE-CLOSEOUT-AND-DOMAIN-COVERAGE-HANDOFF-20260818.md`](../foundations/WDF3-A-WDF3-L-CATEGORIAL-REALITY-ARCHITECTURE-CLOSEOUT-AND-DOMAIN-COVERAGE-HANDOFF-20260818.md) |
| WDF4 | Causal Reality Architecture | local subarchitecture Foundation | FROZEN Foundation v1 | WDF4 A→F closeout |
| WDF5 | Property Evaluation Architecture | local subarchitecture Foundation | FROZEN Foundation v1 | WDF5 A→I closeout |
| TSAF0 | Temporal Structure Architecture | local subarchitecture Foundation | FROZEN Foundation v1 | TSAF0 A→E closeout |

## Git durability repair baseline — 2026-08-18

Before this materialization, canonical research history ended at:

`8efea81cca235d4d4c0c0f7b6bbc42cd5b277edf` — `world: close TSAF0 and audit registry integration`.

Physical verification established:

- source repo: `/root/projects/ordivon-world`;
- then-current `main`: `6f98e381f6c58c0ff1a56cf7036c607d9ac0d4c6`;
- research tip was a **clean linear descendant** of `main`;
- `main..research = 74` commits; `research..main = 0`;
- no named ref contained the research tip before repair;
- canonical WDF0/WDF1/WDF2 research worktrees were clean;
- several older experimental World worktrees retained dirty/untracked state and were therefore not disposed during repair.

The canonical research ancestry was pinned, without rewriting commits, to:

`refs/heads/research/world-reality-canonical-20260818`

at the exact pre-materialization tip `8efea81cca235d4d4c0c0f7b6bbc42cd5b277edf` before any integration or cleanup was considered.

The first materialization commit is `774ffb864e4d2f4a723cbd81daf5af2cfb7679f3` (`docs(world): materialize canonical research root`), whose parent is exactly `8efea81cca235d4d4c0c0f7b6bbc42cd5b277edf`.

This directory is a compression/navigation layer added **on top of that original ancestry**. Detailed WDF/TSA evidence remains preserved unchanged under [`../foundations/`](../foundations/).
