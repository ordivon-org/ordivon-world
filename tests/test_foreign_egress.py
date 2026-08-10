from __future__ import annotations

import datetime as dt
import json
import unittest

from ordivon_world import (
    ForeignEgressCapability,
    ForeignEgressCapabilityStale,
    ForeignEgressProjectionError,
)
from ordivon_world.canonical import sha256_digest


PATH_DIGEST = "sha256:" + "1" * 64
OTHER_PATH_DIGEST = "sha256:" + "2" * 64
CATALOG_DIGEST = "sha256:" + "3" * 64
PROVIDER_DIGEST = "sha256:" + "4" * 64
CONFIG_DIGEST = "sha256:" + "5" * 64
PROVIDER_BINARY_DIGEST = "sha256:" + "6" * 64


def surfpath_observation() -> dict[str, object]:
    value: dict[str, object] = {
        "schemaVersion": 2,
        "kind": "ordivon.workstation.surfshark-path-observation",
        "truthRole": "point-in-time-observation",
        "observedAt": "2026-08-10T04:00:00Z",
        "catalogDigest": CATALOG_DIGEST,
        "protocols": ["openvpn-udp"],
        "requiredTargets": ["openai"],
        "candidates": [
            {
                "path": {
                    "protocol": "openvpn-udp",
                    "ingress": {
                        "name": "native-b",
                        "routePreference": 10202,
                        "routeProfile": "B",
                        "routeTable": 202,
                        "routeUser": "cloudflared-direct-b",
                    },
                    "node": "jp-tok",
                    "configDigest": CONFIG_DIGEST,
                    "endpointHost": "jp-tok.prod.surfshark.com",
                    "endpointIp": "154.47.23.57",
                    "endpointPort": 1194,
                    "providerDigest": PROVIDER_DIGEST,
                    "providerBinaryDigest": PROVIDER_BINARY_DIGEST,
                    "pathDigest": PATH_DIGEST,
                },
                "connection": {"ok": True, "kind": "openvpn-initialization", "elapsedMs": 3000.0},
                "egress": {
                    "ok": True,
                    "selectedAddress": "104.16.123.96",
                    "facts": {"ip": "154.47.23.58", "loc": "JP", "colo": "NRT"},
                    "attempts": [],
                },
                "targets": {
                    "openai": {
                        "ok": True,
                        "url": "https://api.openai.com/v1/models",
                        "selectedAddress": "172.66.0.243",
                        "attempts": [],
                    }
                },
                "qualified": True,
                "score": 101000,
                "effectiveLatencyMs": 4500.0,
            }
        ],
        "rankedPaths": [PATH_DIGEST],
        "recommendedPathDigest": OTHER_PATH_DIGEST,
    }
    value["observationDigest"] = sha256_digest(value)
    return value


def surfpath_status(observation: dict[str, object]) -> dict[str, object]:
    return {
        "schemaVersion": 2,
        "kind": "ordivon.workstation.surfshark-path-status",
        "providers": {},
        "catalog": {},
        "ingresses": [],
        "observation": {
            "exists": True,
            "schemaVersion": 2,
            "observationDigest": observation["observationDigest"],
            "recommendedPathDigest": observation["recommendedPathDigest"],
            "qualifiedPaths": 1,
            "ageSeconds": 5.0,
            "maxAgeSeconds": 180,
            "fresh": True,
            "executableNow": True,
        },
    }


class ForeignEgressCapabilityTests(unittest.TestCase):
    def project(self) -> ForeignEgressCapability:
        observation = surfpath_observation()
        return ForeignEgressCapability.from_surfpath(
            observation=observation, status=surfpath_status(observation), path_digest=PATH_DIGEST
        )

    def test_projection_preserves_semantic_path_and_strips_provider_mechanics(self) -> None:
        value = self.project().to_dict()
        self.assertEqual(value["owner"]["pathDigest"], PATH_DIGEST)
        self.assertEqual(
            value["relationship"]["ingress"], {"name": "native-b", "routeProfile": "B"}
        )
        self.assertEqual(value["relationship"]["transport"], "openvpn-udp")
        self.assertEqual(value["relationship"]["node"], "jp-tok")
        self.assertEqual(value["relationship"]["egress"]["location"], "JP")
        self.assertEqual(value["requiredTargets"], ["openai"])
        self.assertTrue(value["requiresOwnerRevalidation"])
        self.assertEqual(value["activationAuthority"], "ordivon.workstation.surfpath")
        serialized = json.dumps(value, sort_keys=True)
        for forbidden in (
            "routeTable",
            "routeUser",
            "providerBinaryDigest",
            "authAuthorityPath",
            "configPath",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_agent_selection_is_explicit_not_recommended_path(self) -> None:
        capability = self.project()
        self.assertEqual(capability.path_digest, PATH_DIGEST)
        self.assertEqual(capability.to_dict()["owner"]["pathDigest"], PATH_DIGEST)

    def test_status_must_project_current_executability(self) -> None:
        observation = surfpath_observation()
        status = surfpath_status(observation)
        status["observation"]["fresh"] = False
        status["observation"]["executableNow"] = False
        with self.assertRaises(ForeignEgressCapabilityStale):
            ForeignEgressCapability.from_surfpath(
                observation=observation, status=status, path_digest=PATH_DIGEST
            )

    def test_observation_digest_is_verified(self) -> None:
        observation = surfpath_observation()
        status = surfpath_status(observation)
        observation["catalogDigest"] = "sha256:" + "9" * 64
        with self.assertRaisesRegex(ForeignEgressProjectionError, "digest mismatch"):
            ForeignEgressCapability.from_surfpath(
                observation=observation, status=status, path_digest=PATH_DIGEST
            )

    def test_unqualified_path_cannot_be_projected(self) -> None:
        observation = surfpath_observation()
        observation["rankedPaths"] = []
        observation["observationDigest"] = sha256_digest(
            {key: value for key, value in observation.items() if key != "observationDigest"}
        )
        status = surfpath_status(observation)
        with self.assertRaisesRegex(ForeignEgressProjectionError, "not a qualified path"):
            ForeignEgressCapability.from_surfpath(
                observation=observation, status=status, path_digest=PATH_DIGEST
            )

    def test_reference_expiry_never_becomes_effect_authority(self) -> None:
        capability = self.project()
        within = dt.datetime(2026, 8, 10, 4, 2, 59, tzinfo=dt.timezone.utc)
        expired = dt.datetime(2026, 8, 10, 4, 3, 1, tzinfo=dt.timezone.utc)
        self.assertTrue(capability.is_reference_fresh(within))
        capability.require_reference_fresh(within)
        with self.assertRaises(ForeignEgressCapabilityStale):
            capability.require_reference_fresh(expired)
        reference = capability.handoff_reference()
        self.assertTrue(reference["requiresOwnerRevalidation"])
        self.assertEqual(reference["capabilityDigest"], capability.capability_digest)
        self.assertEqual(reference["observationDigest"], capability.observation_digest)
        self.assertEqual(reference["pathDigest"], capability.path_digest)
        self.assertNotIn("relationship", reference)
        self.assertNotIn("providerEvidenceDigest", json.dumps(reference, sort_keys=True))

    def test_round_trip_revalidates_projection_digest(self) -> None:
        capability = self.project()
        restored = ForeignEgressCapability.from_dict(capability.to_dict())
        self.assertEqual(restored, capability)
        tampered = capability.to_dict()
        tampered["relationship"]["node"] = "sg-sin"
        with self.assertRaisesRegex(ForeignEgressProjectionError, "digest does not match"):
            ForeignEgressCapability.from_dict(tampered)


if __name__ == "__main__":
    unittest.main()
