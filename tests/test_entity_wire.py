from __future__ import annotations

import unittest

from ordivon_world.canonical import sha256_digest
from ordivon_world.entity_migration import (
    EntityDepartureAuthority,
    EntityDepartureReceipt,
    EntityMigrationBundle,
    EntityMigrationOutcomeUnknown,
)
from ordivon_world.entity_wire import (
    EntityMigrationDestinationRejected,
    EntityMigrationPreDispatchError,
    EntityMigrationTransportOutcomeUnknown,
    EntityMigrationWireDestination,
    EntityMigrationWireError,
)


def bundle() -> EntityMigrationBundle:
    continuity = {"kind": "continuity", "entityId": "entity:w2:test", "memoryRef": "m1"}
    departure = EntityDepartureReceipt(
        migration_id="migration:w2:wire",
        entity_id="entity:w2:test",
        source_world_id="world:w2:A",
        destination_world_id="security-world:w2:B",
        source_occurrence_id="entity-departure:w2:wire",
        source_occurrence_digest=sha256_digest({"factId": "fact:w2:departure"}),
        authority=EntityDepartureAuthority(
            authority_id="source-authority:w2:A",
            mechanism="verified-departure.v1",
            evidence={"factId": "fact:w2:departure"},
        ),
    )
    return EntityMigrationBundle.create_departed(
        source_departure=departure,
        continuity_payload=continuity,
    )


def receipt(value: EntityMigrationBundle) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.entity-migration-receipt",
        "migrationId": value.plan.migration_id,
        "planDigest": value.plan.digest,
        "entityId": value.plan.entity_id,
        "destinationWorldId": value.plan.destination_world_id,
        "sourceDepartureDigest": value.plan.source_departure_digest,
        "materializationId": "entity-body:w2:wire",
        "materializationDigest": sha256_digest({"body": value.plan.migration_id}),
        "destinationEvidence": {
            "authority": "security-kvm",
            "continuityPayloadDigest": value.plan.continuity_payload_digest,
        },
    }


class Transport:
    def __init__(self, response=None, error: BaseException | None = None) -> None:
        self.response = response
        self.error = error
        self.requests: list[dict[str, object]] = []

    def exchange(self, request):
        self.requests.append(request)
        if self.error is not None:
            raise self.error
        return self.response


class EntityMigrationWireTests(unittest.TestCase):
    def test_materialize_serializes_exact_departure_and_continuity(self) -> None:
        value = bundle()
        transport = Transport(
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.entity-migration-destination-response",
                "status": "materialized",
                "receipt": receipt(value),
            }
        )
        observed = EntityMigrationWireDestination(transport).materialize(value)
        self.assertEqual(observed.to_dict(), receipt(value))
        request = transport.requests[0]
        self.assertEqual(request["sourceDeparture"], value.source_departure)
        self.assertEqual(request["continuityPayload"], value.continuity_payload)

    def test_legacy_untyped_departure_is_rejected_before_transport(self) -> None:
        legacy = EntityMigrationBundle.create(
            migration_id="migration:w2:legacy",
            entity_id="e",
            source_world_id="A",
            destination_world_id="B",
            source_departure={"kind": "legacy"},
            continuity_payload={"v": 1},
        )
        transport = Transport()
        with self.assertRaises(EntityMigrationWireError):
            EntityMigrationWireDestination(transport).materialize(legacy)
        self.assertEqual(transport.requests, [])

    def test_transport_unknown_and_destination_unknown_both_preserve_unknown(self) -> None:
        value = bundle()
        with self.assertRaises(EntityMigrationOutcomeUnknown):
            EntityMigrationWireDestination(
                Transport(error=EntityMigrationTransportOutcomeUnknown("lost"))
            ).materialize(value)
        response = {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-migration-destination-response",
            "status": "unknown",
            "migrationId": value.plan.migration_id,
            "planDigest": value.plan.digest,
            "reason": "unresolved-native-materialization",
        }
        with self.assertRaises(EntityMigrationOutcomeUnknown):
            EntityMigrationWireDestination(Transport(response)).materialize(value)

    def test_pre_dispatch_failure_is_not_converted_to_unknown(self) -> None:
        with self.assertRaises(EntityMigrationPreDispatchError):
            EntityMigrationWireDestination(
                Transport(error=EntityMigrationPreDispatchError("absent"))
            ).materialize(bundle())

    def test_reconcile_not_committed_requires_native_retry_proof_and_omits_payload(self) -> None:
        value = bundle()
        response = {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-migration-destination-response",
            "status": "not_committed",
            "migrationId": value.plan.migration_id,
            "planDigest": value.plan.digest,
            "entityId": value.plan.entity_id,
            "destinationWorldId": value.plan.destination_world_id,
            "sourceDepartureDigest": value.plan.source_departure_digest,
            "continuityPayloadDigest": value.plan.continuity_payload_digest,
            "evidence": {
                "authority": "security-kvm",
                "exactOriginalRetrySafe": True,
                "nativeSubstrateChecked": True,
            },
        }
        transport = Transport(response)
        proof = EntityMigrationWireDestination(transport).reconcile(value.plan)
        self.assertEqual(proof.migration_id, value.plan.migration_id)
        self.assertTrue(proof.evidence["nativeSubstrateChecked"])
        request = transport.requests[0]
        self.assertNotIn("sourceDeparture", request)
        self.assertNotIn("continuityPayload", request)

    def test_reconcile_unknown_is_identity_bound_and_returns_none(self) -> None:
        value = bundle()
        response = {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-migration-destination-response",
            "status": "unknown",
            "migrationId": value.plan.migration_id,
            "planDigest": value.plan.digest,
            "reason": "native unresolved",
        }
        self.assertIsNone(EntityMigrationWireDestination(Transport(response)).reconcile(value.plan))

    def test_explicit_rejection_is_safe_failure(self) -> None:
        response = {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-migration-destination-response",
            "status": "rejected",
            "code": "policy-rejected",
            "reason": "source denied",
        }
        with self.assertRaises(EntityMigrationDestinationRejected):
            EntityMigrationWireDestination(Transport(response)).materialize(bundle())


if __name__ == "__main__":
    unittest.main()
