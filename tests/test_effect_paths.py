from __future__ import annotations

import copy
import unittest

from ordivon_world import (
    EffectPathCandidate,
    EffectPathProjectionError,
    EffectPathQuery,
    ForeignEgressCapability,
)
from ordivon_world.canonical import sha256_digest

TARGET = "https://api.openai.com/v1/models"
RUNTIME_EFFECT_DIGEST = "sha256:71edc8e5c5aa77ba6d15a910f6a06ed524888869a2d7a69ddebd4abd1a0e24c2"


def surfpath_capability() -> ForeignEgressCapability:
    return ForeignEgressCapability.from_dict(
        {
            "schemaVersion": 1,
            "kind": "ordivon.world.foreign-egress-capability",
            "truthRole": "owner-observed-capability-projection",
            "capabilityType": "foreign-egress",
            "owner": {
                "authority": "ordivon.workstation.surfpath",
                "observationKind": "ordivon.workstation.surfshark-path-observation",
                "observationDigest": "sha256:327472b0046df888da2e573c6a59e9c8334d72212298f38885313e28dee77e4d",
                "pathDigest": "sha256:ad19ae221df2a3028e8a16b554cf152194c6f383ab7a9a3f8c45d82adee6f5eb",
                "catalogDigest": "sha256:1782aa5050bde036324487a755c86efb253563b783bb23085c70dd23a0ab3a1c",
                "freshnessWindowSeconds": 180,
            },
            "observedAt": "2026-08-10T04:37:13.650844Z",
            "freshUntil": "2026-08-10T04:40:13.650844Z",
            "relationship": {
                "ingress": {"name": "native-a", "routeProfile": "A"},
                "transport": "openvpn-udp",
                "node": "jp-tok",
                "endpoint": {
                    "host": "jp-tok.prod.surfshark.com",
                    "ip": "172.216.10.36",
                    "port": 1194,
                },
                "providerEvidenceDigest": "sha256:3cf5263c630168cbd1a67e68afa129df1f69feae82b3880b247d63e4edd2c694",
                "configDigest": "sha256:32805d1325c6ac9364c9370a48c314dc5701547ac1de1246f6a8f9a0c0bae648",
                "egress": {"ip": "172.216.10.37", "location": "JP", "colo": "NRT"},
                "targets": [
                    {
                        "name": "openai",
                        "url": TARGET,
                        "selectedAddress": "162.159.140.245",
                    }
                ],
            },
            "requiredTargets": ["openai"],
            "activationAuthority": "ordivon.workstation.surfpath",
            "requiresOwnerRevalidation": True,
            "capabilityDigest": "sha256:4c070368181602b2cf88d39ca18c48f23ca5a7b6fa8571fbb625f20506e998f8",
        }
    )


def cloudflare_owner_observation(*, present: bool = True) -> dict[str, object]:
    value: dict[str, object] = {
        "schemaVersion": 1,
        "kind": "ordivon.world.wx3-cloudflare-owner-observation",
        "truthRole": "point-in-time-owner-observation",
        "observedAt": "2026-08-10T06:27:48.312312Z",
        "authority": "cloudflare.account-api",
        "fixedTarget": TARGET,
        "resourceIdentity": {
            "script": "world-wx3-openai-1786343238-456cd1",
            "host": "wx3-openai-1786343238-456cd1.ordivon.com",
            "dnsId": "e6f11518f18dd86ae50f5d3d957d5176",
            "routeId": "520b4f58324d41c5aa9edf36406560ca",
        },
        "resources": {
            "dns": {
                "queryCompleted": True,
                "httpStatus": 200 if present else 404,
                "exists": present,
                "name": "wx3-openai-1786343238-456cd1.ordivon.com",
                "proxied": True,
                "type": "A",
            },
            "route": {
                "queryCompleted": True,
                "httpStatus": 200 if present else 404,
                "exists": present,
                "pattern": "wx3-openai-1786343238-456cd1.ordivon.com/*",
                "script": "world-wx3-openai-1786343238-456cd1",
            },
            "worker": {
                "queryCompleted": True,
                "httpStatus": 200 if present else 404,
                "exists": present,
            },
        },
    }
    value["observationDigest"] = sha256_digest(value)
    return value


def cloudflare_success_effect() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.wx3-cloudflare-openai-observation",
        "localHttpStatus": 200,
        "localElapsedMs": 20885.034,
        "host": "wx3-openai-1786343238-456cd1.ordivon.com",
        "script": "world-wx3-openai-1786343238-456cd1",
        "fixedUpstream": TARGET,
        "effect": {
            "schemaVersion": 1,
            "kind": "ordivon.world.request-scoped-openai-connector-effect",
            "connector": "cloudflare-worker-https",
            "fixedUpstream": TARGET,
            "observedAt": "2026-08-10T06:28:28.824Z",
            "connectorEdgeColo": "LHR",
            "connectorIngressCountry": "GB",
            "upstreamCompleted": True,
            "upstreamStatus": 401,
            "bodyBytes": 151,
            "bodySha256": "sha256:020cefc21c2f2477bc862fb750a476414029d287454ca6a67d0b1d19d82d219d",
            "elapsedMs": 19778,
        },
    }


def cloudflare_failed_effect() -> dict[str, object]:
    value = cloudflare_success_effect()
    value["localHttpStatus"] = 522
    value["effect"] = {
        "cloudflare_error": True,
        "status": 522,
        "error_name": "connection_timeout",
    }
    return value


def surfpath_candidate() -> EffectPathCandidate:
    return EffectPathCandidate.from_foreign_egress_http_get(
        surfpath_capability(),
        target=TARGET,
        effect_observed_at="2026-08-10T04:39:17.993Z",
        effect_evidence_digest=RUNTIME_EFFECT_DIGEST,
        http_status=401,
    )


def cloudflare_candidate() -> EffectPathCandidate:
    return EffectPathCandidate.from_cloudflare_fixed_http_get(
        owner_observation=cloudflare_owner_observation(),
        effect_observation=cloudflare_success_effect(),
    )


class EffectPathQueryTests(unittest.TestCase):
    def test_two_provider_query_preserves_differences_without_ranking(self) -> None:
        query = EffectPathQuery.for_http_get(
            target=TARGET,
            candidates=(surfpath_candidate(), cloudflare_candidate()),
        )
        value = query.to_dict()
        self.assertEqual(value["selectionAuthority"], "agent")
        self.assertNotIn("recommendedCandidateDigest", value)
        self.assertNotIn("selectedCandidateDigest", value)
        self.assertEqual(len(value["candidates"]), 2)
        by_source = {item["sourceKind"]: item for item in value["candidates"]}
        surfpath = by_source["ordivon.world.foreign-egress-capability"]
        cloudflare = by_source["ordivon.world.cloudflare-fixed-target-connector-evidence"]
        self.assertEqual(surfpath["ownerObservation"]["validUntil"], "2026-08-10T04:40:13.650844Z")
        self.assertIsNone(cloudflare["ownerObservation"]["validUntil"])
        self.assertEqual(surfpath["requestControl"], "consumer-request-owner-revalidated")
        self.assertEqual(cloudflare["requestControl"], "owner-fixed-request")
        self.assertFalse(surfpath["currentActionAuthority"])
        self.assertFalse(cloudflare["currentActionAuthority"])
        self.assertTrue(surfpath["requiresOwnerRevalidation"])
        self.assertTrue(cloudflare["requiresOwnerRevalidation"])

    def test_query_order_is_deterministic_but_not_a_rank(self) -> None:
        first = EffectPathQuery.for_http_get(
            target=TARGET,
            candidates=(surfpath_candidate(), cloudflare_candidate()),
        )
        second = EffectPathQuery.for_http_get(
            target=TARGET,
            candidates=(cloudflare_candidate(), surfpath_candidate()),
        )
        self.assertEqual(first.query_digest, second.query_digest)
        self.assertEqual(first.to_dict(), second.to_dict())

    def test_agent_must_select_one_exact_candidate_digest(self) -> None:
        candidate = surfpath_candidate()
        query = EffectPathQuery.for_http_get(target=TARGET, candidates=(candidate,))
        self.assertEqual(query.require_candidate(candidate.candidate_digest), candidate)
        with self.assertRaisesRegex(EffectPathProjectionError, "exact candidateDigest"):
            query.require_candidate("sha256:" + "9" * 64)

    def test_cloudflare_resource_presence_is_not_usability(self) -> None:
        with self.assertRaisesRegex(EffectPathProjectionError, "no successful fixed-target effect"):
            EffectPathCandidate.from_cloudflare_fixed_http_get(
                owner_observation=cloudflare_owner_observation(),
                effect_observation=cloudflare_failed_effect(),
            )

    def test_historical_cloudflare_effect_is_not_current_after_owner_resources_disappear(self) -> None:
        with self.assertRaisesRegex(EffectPathProjectionError, "resources present"):
            EffectPathCandidate.from_cloudflare_fixed_http_get(
                owner_observation=cloudflare_owner_observation(present=False),
                effect_observation=cloudflare_success_effect(),
            )

    def test_foreign_egress_effect_must_fall_inside_owner_freshness_window(self) -> None:
        with self.assertRaisesRegex(EffectPathProjectionError, "freshness window"):
            EffectPathCandidate.from_foreign_egress_http_get(
                surfpath_capability(),
                target=TARGET,
                effect_observed_at="2026-08-10T04:41:00Z",
                effect_evidence_digest=RUNTIME_EFFECT_DIGEST,
                http_status=401,
            )

    def test_candidate_nested_semantic_mutation_fails_closed(self) -> None:
        candidate = cloudflare_candidate()
        candidate.source_projection["ownerObservation"]["fixedTarget"] = "https://example.com/"
        with self.assertRaisesRegex(EffectPathProjectionError, "candidate digest"):
            candidate.to_dict()

    def test_cloudflare_input_alias_is_not_retained(self) -> None:
        owner = cloudflare_owner_observation()
        effect = cloudflare_success_effect()
        candidate = EffectPathCandidate.from_cloudflare_fixed_http_get(
            owner_observation=owner,
            effect_observation=effect,
        )
        owner["resourceIdentity"]["host"] = "mutated.invalid"
        effect["host"] = "mutated.invalid"
        value = candidate.to_dict()
        self.assertNotEqual(
            value["sourceProjection"]["ownerObservation"]["resourceIdentity"]["host"],
            "mutated.invalid",
        )

    def test_query_rejects_candidate_for_different_effect(self) -> None:
        candidate = copy.deepcopy(cloudflare_candidate())
        object.__setattr__(candidate, "target", "https://example.com/")
        with self.assertRaises(EffectPathProjectionError):
            EffectPathQuery.for_http_get(target=TARGET, candidates=(candidate,))


if __name__ == "__main__":
    unittest.main()
