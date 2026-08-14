# AM6 — Internal Sub-Agent vs Persistent World Entity

Status: executable boundary result.

AM6 tests whether a multi-agent cognition pattern should automatically become a World Entity topology. The result is no.

An internal critic/planner/verifier may produce information that crosses World as a Message. That creates Message provenance/delivery evidence only; it does not create `worldEntityId`, Entity continuity, Presence, capability, or destination knowledge.

A persistent actor crossing World requires the Entity trajectory explicitly: stable entity identity, source departure, continuity payload, destination materialization and destination-native evidence. Message portability is insufficient to satisfy those requirements.

`tests/test_am6_entity_threshold.py` verifies three cases:

1. helper output crosses World as Message without creating Entity state;
2. persistent actor migration retains exact entity identity/departure/continuity/materialization evidence;
3. a delivered helper Message cannot be loaded as an Entity migration.

Targeted result: 3/3 pass. Full World suite after AM3–AM6: 151 tests pass; Ruff passes.

Decision: internal multi-agent topology remains Harness cognition morphology until independent durable identity + continuity + independently addressable World relation/authority are required. Only then does it cross the World/domain Entity threshold.
