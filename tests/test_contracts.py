from __future__ import annotations

import unittest

from ordivon_world.canonical import sha256_digest
from ordivon_world import (
    ContractError,
    EntityDepartureAuthority,
    EntityDepartureReceipt,
    EntityMigrationBundle,
    EntityMigrationNotCommitted,
    EntityMigrationReceipt,
    MessageDeliveryBundle,
    MessageDeliveryNotCommitted,
    MessageDeliveryReceipt,
    MessageIssuanceAuthority,
    MessageIssuanceReceipt,
    ResourceEgressAuthority,
    ResourceEgressReceipt,
    ResourceTransferBundle,
    ResourceTransferNotCommitted,
    ResourceTransferReceipt,
    load_schema,
    validate_contract,
)


def execution(capability: str) -> dict[str, object]:
    return {
        "policy_version": "p1.6.test",
        "capability_version": capability,
        "worker_version_id": "worker-test",
        "worker_version_tag": "git-111111111111-src-2222222222222222-1",
        "worker_version_timestamp": "2026-08-04T00:00:00Z",
        "lease_generation": 1,
    }


def artifact(key: str, media_type: str) -> dict[str, object]:
    return {
        "key": key,
        "sha256": "a" * 64,
        "bytes": 12,
        "media_type": media_type,
    }


def resource_bundle(transfer_id: str) -> ResourceTransferBundle:
    payload = {"kind": "resource", "value": transfer_id}
    evidence = {"kind": "source", "transferId": transfer_id}
    egress = ResourceEgressReceipt(
        transfer_id=transfer_id,
        source_world_id="world:w2:A",
        destination_world_id="world:w2:B",
        resource_kind="contract-test",
        payload_digest=sha256_digest(payload),
        source_occurrence_id=f"resource-occurrence:{transfer_id}",
        source_occurrence_digest=sha256_digest(evidence),
        authority=ResourceEgressAuthority(
            authority_id="source-authority:w2:A",
            mechanism="contract-test.v1",
            evidence=evidence,
        ),
    )
    return ResourceTransferBundle.create(source_egress=egress, payload=payload)


def entity_bundle(migration_id: str) -> EntityMigrationBundle:
    continuity = {"kind": "continuity", "entityId": "entity:w2:contract", "contextRef": "ctx:1"}
    departure = EntityDepartureReceipt(
        migration_id=migration_id,
        entity_id="entity:w2:contract",
        source_world_id="world:w2:A",
        destination_world_id="security-world:w2:B",
        source_occurrence_id=f"entity-departure:{migration_id}",
        source_occurrence_digest=sha256_digest({"factId": f"fact:{migration_id}"}),
        authority=EntityDepartureAuthority(
            authority_id="source-authority:w2:A",
            mechanism="contract-test-departure.v1",
            evidence={"migrationId": migration_id},
        ),
    )
    return EntityMigrationBundle.create_departed(
        source_departure=departure,
        continuity_payload=continuity,
    )


def message_bundle(message_id: str) -> MessageDeliveryBundle:
    provenance = {"kind": "message-provenance", "messageId": message_id}
    payload = {"kind": "message-payload", "value": message_id}
    issuance = MessageIssuanceReceipt(
        message_id=message_id,
        source_world_id="world:w2:A",
        destination_world_id="world:w2:B",
        message_kind="contract-test-message",
        provenance_digest=sha256_digest(provenance),
        payload_digest=sha256_digest(payload),
        source_occurrence_id=f"message-source:{message_id}",
        source_occurrence_digest=sha256_digest({"factId": f"fact:{message_id}"}),
        authority=MessageIssuanceAuthority(
            authority_id="source-authority:w2:A",
            mechanism="contract-test-message.v1",
            evidence={"messageId": message_id},
        ),
    )
    return MessageDeliveryBundle.create_issued(
        source_issuance=issuance,
        provenance=provenance,
        payload=payload,
    )


class ContractTests(unittest.TestCase):
    def test_all_published_contracts_are_valid_draft_2020_12(self) -> None:
        names = (
            "browser-manifest",
            "browser-request",
            "edge-capabilities",
            "edge-receipt",
            "entity-departure-receipt",
            "entity-migration-destination-request",
            "entity-migration-destination-response",
            "entity-migration-not-committed",
            "entity-migration-plan",
            "entity-migration-receipt",
            "fetch-request",
            "message-delivery-destination-request",
            "message-delivery-destination-response",
            "message-delivery-not-committed",
            "message-delivery-plan",
            "message-delivery-receipt",
            "message-issuance-receipt",
            "network-observation",
            "resource-egress-receipt",
            "resource-transfer-destination-request",
            "resource-transfer-destination-response",
            "resource-transfer-not-committed",
            "resource-transfer-plan",
            "resource-transfer-receipt",
            "world-observation",
            "world-prepared-dispatch",
        )
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(
                    load_schema(name)["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )

    def test_public_resource_models_validate_against_published_contracts(self) -> None:
        bundle = resource_bundle("transfer:w2:contract")
        validate_contract("resource-egress-receipt", bundle.source_egress)
        validate_contract("resource-transfer-plan", bundle.plan.to_dict())
        receipt = ResourceTransferReceipt(
            transfer_id=bundle.plan.transfer_id,
            plan_digest=bundle.plan.digest,
            destination_world_id=bundle.plan.destination_world_id,
            payload_digest=bundle.plan.payload_digest,
            materialization_id="resource:w2:contract",
            materialization_digest="sha256:" + "2" * 64,
            destination_evidence={"authority": "contract-test"},
        )
        validate_contract("resource-transfer-receipt", receipt.to_dict())
        proof = ResourceTransferNotCommitted(
            transfer_id=bundle.plan.transfer_id,
            plan_digest=bundle.plan.digest,
            destination_world_id=bundle.plan.destination_world_id,
            payload_digest=bundle.plan.payload_digest,
            evidence={"authority": "contract-test", "exactOriginalRetrySafe": True},
        )
        validate_contract("resource-transfer-not-committed", proof.to_dict())

    def test_public_entity_models_validate_against_published_contracts(self) -> None:
        bundle = entity_bundle("migration:w2:contract")
        departure = EntityDepartureReceipt.from_dict(bundle.source_departure)
        validate_contract("entity-departure-receipt", departure.to_dict())
        validate_contract("entity-migration-plan", bundle.plan.to_dict())
        receipt = EntityMigrationReceipt(
            migration_id=bundle.plan.migration_id,
            plan_digest=bundle.plan.digest,
            entity_id=bundle.plan.entity_id,
            destination_world_id=bundle.plan.destination_world_id,
            source_departure_digest=bundle.plan.source_departure_digest,
            materialization_id="entity-body:w2:contract",
            materialization_digest="sha256:" + "6" * 64,
            destination_evidence={
                "authority": "security-kvm",
                "continuityPayloadDigest": bundle.plan.continuity_payload_digest,
            },
        )
        validate_contract("entity-migration-receipt", receipt.to_dict())
        proof = EntityMigrationNotCommitted(
            migration_id=bundle.plan.migration_id,
            plan_digest=bundle.plan.digest,
            entity_id=bundle.plan.entity_id,
            destination_world_id=bundle.plan.destination_world_id,
            source_departure_digest=bundle.plan.source_departure_digest,
            continuity_payload_digest=bundle.plan.continuity_payload_digest,
            evidence={
                "authority": "security-kvm",
                "exactOriginalRetrySafe": True,
                "nativeSubstrateChecked": True,
            },
        )
        validate_contract("entity-migration-not-committed", proof.to_dict())
        validate_contract(
            "entity-migration-destination-request",
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.entity-migration-destination-request",
                "operation": "materialize",
                "plan": bundle.plan.to_dict(),
                "planDigest": bundle.plan.digest,
                "sourceDeparture": bundle.source_departure,
                "continuityPayload": bundle.continuity_payload,
            },
        )

    def test_entity_reconcile_contract_forbids_departure_and_continuity_payload(self) -> None:
        bundle = entity_bundle("migration:w2:reconcile")
        for forbidden_field, value in (
            ("sourceDeparture", bundle.source_departure),
            ("continuityPayload", bundle.continuity_payload),
        ):
            with self.subTest(forbidden_field=forbidden_field), self.assertRaises(ContractError):
                validate_contract(
                    "entity-migration-destination-request",
                    {
                        "schemaVersion": 1,
                        "kind": "ordivon.world.entity-migration-destination-request",
                        "operation": "reconcile",
                        "plan": bundle.plan.to_dict(),
                        "planDigest": bundle.plan.digest,
                        forbidden_field: value,
                    },
                )

    def test_entity_not_committed_contract_requires_native_substrate_check(self) -> None:
        bundle = entity_bundle("migration:w2:unsafe-proof")
        with self.assertRaises(ContractError):
            validate_contract(
                "entity-migration-destination-response",
                {
                    "schemaVersion": 1,
                    "kind": "ordivon.world.entity-migration-destination-response",
                    "status": "not_committed",
                    "migrationId": bundle.plan.migration_id,
                    "planDigest": bundle.plan.digest,
                    "entityId": bundle.plan.entity_id,
                    "destinationWorldId": bundle.plan.destination_world_id,
                    "sourceDepartureDigest": bundle.plan.source_departure_digest,
                    "continuityPayloadDigest": bundle.plan.continuity_payload_digest,
                    "evidence": {
                        "authority": "unsafe-destination",
                        "exactOriginalRetrySafe": True,
                        "nativeSubstrateChecked": False,
                    },
                },
            )

    def test_public_message_models_validate_against_published_contracts(self) -> None:
        bundle = message_bundle("message:w2:contract")
        self.assertIsNotNone(bundle.plan.source_issuance)
        validate_contract("message-issuance-receipt", bundle.plan.source_issuance.to_dict())
        validate_contract("message-delivery-plan", bundle.plan.to_dict())
        receipt = MessageDeliveryReceipt(
            message_id=bundle.plan.message_id,
            plan_digest=bundle.plan.digest,
            destination_world_id=bundle.plan.destination_world_id,
            payload_digest=bundle.plan.payload_digest,
            delivery_id="message-admission:w2:contract",
            delivery_digest="sha256:" + "4" * 64,
            destination_evidence={"authority": "contract-test", "classification": "management"},
        )
        validate_contract("message-delivery-receipt", receipt.to_dict())
        proof = MessageDeliveryNotCommitted(
            message_id=bundle.plan.message_id,
            plan_digest=bundle.plan.digest,
            destination_world_id=bundle.plan.destination_world_id,
            payload_digest=bundle.plan.payload_digest,
            evidence={"authority": "contract-test", "exactOriginalRetrySafe": True},
        )
        validate_contract("message-delivery-not-committed", proof.to_dict())
        validate_contract(
            "message-delivery-destination-request",
            {
                "schemaVersion": 1,
                "kind": "ordivon.world.message-delivery-destination-request",
                "operation": "deliver",
                "plan": bundle.plan.to_dict(),
                "planDigest": bundle.plan.digest,
                "provenance": bundle.provenance,
                "payload": bundle.payload,
            },
        )

    def test_message_reconcile_contract_forbids_delivery_payload_fields(self) -> None:
        bundle = message_bundle("message:w2:reconcile")
        with self.assertRaises(ContractError):
            validate_contract(
                "message-delivery-destination-request",
                {
                    "schemaVersion": 1,
                    "kind": "ordivon.world.message-delivery-destination-request",
                    "operation": "reconcile",
                    "plan": bundle.plan.to_dict(),
                    "planDigest": bundle.plan.digest,
                    "payload": bundle.payload,
                },
            )

    def test_resource_reconcile_contract_forbids_materialize_payload_fields(self) -> None:
        bundle = resource_bundle("transfer:w2:reconcile")
        with self.assertRaises(ContractError):
            validate_contract(
                "resource-transfer-destination-request",
                {
                    "schemaVersion": 1,
                    "kind": "ordivon.world.resource-transfer-destination-request",
                    "operation": "reconcile",
                    "plan": bundle.plan.to_dict(),
                    "planDigest": bundle.plan.digest,
                    "payload": bundle.payload,
                },
            )

    def test_not_committed_wire_contract_requires_explicit_retry_safety(self) -> None:
        bundle = resource_bundle("transfer:w2:not-committed")
        with self.assertRaises(ContractError):
            validate_contract(
                "resource-transfer-destination-response",
                {
                    "schemaVersion": 1,
                    "kind": "ordivon.world.resource-transfer-destination-response",
                    "status": "not_committed",
                    "transferId": bundle.plan.transfer_id,
                    "planDigest": bundle.plan.digest,
                    "destinationWorldId": bundle.plan.destination_world_id,
                    "payloadDigest": bundle.plan.payload_digest,
                    "evidence": {
                        "authority": "contract-test",
                        "exactOriginalRetrySafe": False,
                    },
                },
            )

    def test_fetch_contract_rejects_unowned_options(self) -> None:
        with self.assertRaises(ContractError):
            validate_contract(
                "fetch-request",
                {
                    "url": "https://example.com/",
                    "maximum_bytes": 1024,
                    "timeout_ms": 1000,
                    "accept": "*/*",
                    "authorization": "forbidden",
                },
            )

    def test_succeeded_fetch_requires_fetch_evidence(self) -> None:
        body = artifact("fetch/v2/request_fetch_test/g1/body", "text/plain")
        value = {
            "schema_version": 1,
            "receipt_id": "request_fetch_test",
            "request_digest": "b" * 64,
            "operation": "fetch",
            "status": "succeeded",
            "started_at": "2026-08-04T00:00:00Z",
            "completed_at": "2026-08-04T00:00:01Z",
            "duration_ms": 1000,
            "execution": execution("fetch.v2"),
            "artifact": body,
            "artifacts": [body],
        }
        with self.assertRaises(ContractError):
            validate_contract("edge-receipt", value)

    def test_failed_receipt_forbids_artifact_evidence(self) -> None:
        body = artifact("fetch/v2/request_failed_test/g1/body", "text/plain")
        value = {
            "schema_version": 1,
            "receipt_id": "request_failed_test",
            "request_digest": "c" * 64,
            "operation": "fetch",
            "status": "failed",
            "started_at": "2026-08-04T00:00:00Z",
            "completed_at": "2026-08-04T00:00:01Z",
            "duration_ms": 1000,
            "execution": execution("fetch.v2"),
            "error_code": "timeout",
            "artifact": body,
            "artifacts": [body],
        }
        with self.assertRaises(ContractError):
            validate_contract("edge-receipt", value)

    def test_succeeded_browser_requires_three_artifacts(self) -> None:
        screenshot = artifact(
            "browser/v2/request_browser_test/g1/screenshot.png",
            "image/png",
        )
        value = {
            "schema_version": 1,
            "receipt_id": "request_browser_test",
            "request_digest": "d" * 64,
            "operation": "browser.run",
            "status": "succeeded",
            "started_at": "2026-08-04T00:00:00Z",
            "completed_at": "2026-08-04T00:00:01Z",
            "duration_ms": 1000,
            "execution": execution("browser.snapshot.v2"),
            "artifact": screenshot,
            "artifacts": [screenshot],
            "browser": {
                "requested_url": "https://example.com/",
                "final_url_observed": False,
                "page_title": "Example",
                "page_status": 200,
                "browser_ms": 10,
                "viewport": {"width": 1280, "height": 720},
                "full_page": False,
            },
        }
        with self.assertRaises(ContractError):
            validate_contract("edge-receipt", value)


if __name__ == "__main__":
    unittest.main()
