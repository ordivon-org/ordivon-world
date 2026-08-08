from __future__ import annotations

import hashlib
import hmac
import unittest

from ordivon_world.canonical import canonical_bytes, sha256_digest
from ordivon_world.message_delivery import MessageDeliveryBundle

A = "world-instance:w1-p4:A"
B = "world-instance:w1-p4:B"
C = "world-instance:w1-p4:C"
E2E = "message:e2e:w1-p4:reactor"
_SHARED_AC_KEY = b"w1-p4-test-only-a-to-c-origin-authentication-key"


def origin_statement(*, state: str = "unstable", origin: str = A) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.w1.end-to-end-origin-statement",
        "endToEndMessageId": E2E,
        "originWorldId": origin,
        "payload": {"subject": "reactor", "state": state},
        "sourceEvidenceDigest": "sha256:" + "1" * 64,
    }


def authenticate(statement: dict[str, object]) -> dict[str, object]:
    tag = hmac.new(_SHARED_AC_KEY, canonical_bytes(statement), hashlib.sha256).hexdigest()
    return {
        "scheme": "test-only-hmac-sha256",
        "keyRef": "trust:a-to-c",
        "statement": statement,
        "authenticator": "hmac-sha256:" + tag,
    }


def verify(value: dict[str, object]) -> bool:
    statement = value["statement"]
    expected = authenticate(statement)["authenticator"]
    return hmac.compare_digest(str(value["authenticator"]), str(expected))


def relayed_bundle(
    evidence: dict[str, object],
    *,
    origin_claim: str = A,
) -> MessageDeliveryBundle:
    statement = evidence["statement"]
    return MessageDeliveryBundle.create(
        message_id="message:hop:w1-p4:B-C",
        source_world_id=B,
        destination_world_id=C,
        message_kind="relayed-verifiable-foreign-claim",
        provenance={
            "schemaVersion": 1,
            "kind": "ordivon.w1.relayed-message-provenance",
            "nativeSourceWorldId": B,
            "originWorldClaim": origin_claim,
            "endToEndEvidenceDigest": sha256_digest(evidence),
        },
        payload={
            "schemaVersion": 1,
            "kind": "ordivon.w1.message-payload",
            "endToEndMessageId": statement["endToEndMessageId"],
            "claim": statement["payload"],
            "endToEndEvidence": evidence,
        },
    )


class W1RelayProvenanceTests(unittest.TestCase):
    def test_hop_native_source_and_verified_end_to_end_origin_are_separate_coordinates(
        self,
    ) -> None:
        evidence = authenticate(origin_statement())
        bundle = relayed_bundle(evidence)
        self.assertEqual(bundle.plan.source_world_id, B)
        self.assertEqual(bundle.provenance["nativeSourceWorldId"], B)
        self.assertEqual(bundle.provenance["originWorldClaim"], A)
        self.assertTrue(verify(bundle.payload["endToEndEvidence"]))
        self.assertEqual(bundle.payload["endToEndEvidence"]["statement"]["originWorldId"], A)

    def test_relay_can_lie_in_unsigned_origin_claim_without_changing_verified_origin(self) -> None:
        evidence = authenticate(origin_statement())
        bundle = relayed_bundle(evidence, origin_claim="world-instance:FAKE")
        self.assertEqual(bundle.provenance["originWorldClaim"], "world-instance:FAKE")
        self.assertTrue(verify(bundle.payload["endToEndEvidence"]))
        self.assertEqual(bundle.payload["endToEndEvidence"]["statement"]["originWorldId"], A)

    def test_relay_payload_tamper_invalidates_end_to_end_authentication(self) -> None:
        evidence = authenticate(origin_statement())
        tampered = {
            **evidence,
            "statement": {
                **evidence["statement"],
                "payload": {"subject": "reactor", "state": "stable"},
            },
        }
        self.assertFalse(verify(tampered))

    def test_relay_origin_tamper_invalidates_end_to_end_authentication(self) -> None:
        evidence = authenticate(origin_statement())
        tampered = {
            **evidence,
            "statement": {**evidence["statement"], "originWorldId": "world-instance:FAKE"},
        }
        self.assertFalse(verify(tampered))

    def test_delivery_identity_changes_if_relay_substitutes_end_to_end_evidence(self) -> None:
        valid = relayed_bundle(authenticate(origin_statement()))
        changed = relayed_bundle(authenticate(origin_statement(state="stable")))
        self.assertNotEqual(valid.plan.payload_digest, changed.plan.payload_digest)
        self.assertNotEqual(valid.plan.digest, changed.plan.digest)

    def test_end_to_end_authentication_does_not_promote_claim_to_destination_knowledge(
        self,
    ) -> None:
        evidence = authenticate(origin_statement())
        self.assertTrue(verify(evidence))
        destination_knowledge: dict[str, object] = {}
        self.assertEqual(destination_knowledge, {})
        # Verification establishes origin/content integrity, not C-local truth.
        self.assertEqual(
            evidence["statement"]["payload"], {"subject": "reactor", "state": "unstable"}
        )


if __name__ == "__main__":
    unittest.main()
