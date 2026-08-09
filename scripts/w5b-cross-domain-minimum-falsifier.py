#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from ordivon_world.canonical import sha256_digest

CORE_FIELDS = (
    "subjectRef",
    "ownerId",
    "bodyRef",
    "scopeDigest",
    "admissionDigest",
    "occurrenceDigest",
)


def _digest(value: Any) -> str:
    return sha256_digest(value)


def game_projection(evidence: dict[str, Any]) -> dict[str, Any]:
    cognition = evidence["cognitions"][0]
    world = evidence["worldInput"]
    scope = {
        "kind": "game-action-scope",
        "runId": world["runId"],
        "planningId": world["planningId"],
        "worldRevision": world["worldRevision"],
        "worldDigest": world["worldDigest"],
        "intentDigest": cognition["intentDigest"],
    }
    admission = {
        "worldBindingDigest": cognition["worldBindingDigest"],
        "destinationAdmissionDigest": cognition["destinationAdmissionDigest"],
        "destinationPlanDigest": cognition["destinationPlanDigest"],
    }
    occurrence = {
        "nativeEffect": cognition["nativeEffect"],
        "freshGameVerification": cognition["freshGameVerification"],
    }
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5b-experimental-bounded-occurrence-proof",
        "domain": "game",
        "subjectRef": cognition["subjectRef"],
        "ownerId": "ordivon.game.station-zero-v3",
        "bodyRef": f"game-actor:{world['runId']}:{world['actorId']}",
        "scopeDigest": _digest(scope),
        "admissionDigest": _digest(admission),
        "occurrenceDigest": _digest(occurrence),
        "ownerNative": {
            "scope": scope,
            "admission": admission,
            "occurrence": occurrence,
            "cognitionRunId": cognition["harnessRunId"],
            "planningId": world["planningId"],
            "intentDigest": cognition["intentDigest"],
        },
    }


def security_projection(evidence: dict[str, Any]) -> dict[str, Any]:
    result = evidence["physicalAcceptance"]["result"]
    materialization = result["materialization"]
    activation = result["activation"]
    binding = activation["binding"]
    scope = {
        "kind": "security-kvm-activation-scope",
        "destinationWorldId": binding["destinationWorldId"],
        "migrationId": binding["migrationId"],
        "materializationId": binding["materializationId"],
        "generation": binding["generation"],
        "activationId": binding["activationId"],
    }
    admission = {
        "activationBindingDigest": activation["bindingDigest"],
        "planDigest": binding["planDigest"],
        "continuityPayloadDigest": binding["continuityPayloadDigest"],
    }
    occurrence = {
        "guestResultDigest": activation["guestResultDigest"],
        "fixtureResultDigest": activation["fixtureResultDigest"],
        "bodyCurrentBeforeAction": materialization["bodyCurrentBeforeAction"],
        "bodyCurrentAfterResult": activation["bodyCurrentAfterResult"],
    }
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5b-experimental-bounded-occurrence-proof",
        "domain": "security",
        "subjectRef": binding["subjectRef"],
        "ownerId": "ordivon.security.windows-kvm",
        "bodyRef": f"security-kvm:{binding['materializationId']}",
        "scopeDigest": _digest(scope),
        "admissionDigest": _digest(admission),
        "occurrenceDigest": _digest(occurrence),
        "ownerNative": {
            "scope": scope,
            "admission": admission,
            "occurrence": occurrence,
            "migrationId": binding["migrationId"],
            "generation": binding["generation"],
            "activationId": binding["activationId"],
        },
    }


def verify_against_owner_witness(
    claim: dict[str, Any], witness: dict[str, Any], required_fields: tuple[str, ...] = CORE_FIELDS
) -> bool:
    return all(claim.get(field) == witness.get(field) for field in required_fields)


def substituted(value: dict[str, Any], field: str) -> dict[str, Any]:
    changed = copy.deepcopy(value)
    replacements = {
        "subjectRef": "continuity-subject:mallory",
        "ownerId": "ordivon.foreign-owner",
        "bodyRef": "body:substituted",
        "scopeDigest": "sha256:" + "1" * 64,
        "admissionDigest": "sha256:" + "2" * 64,
        "occurrenceDigest": "sha256:" + "3" * 64,
    }
    changed[field] = replacements[field]
    return changed


def omission_falsifiers(witness: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for field in CORE_FIELDS:
        changed = substituted(witness, field)
        full_rejects = not verify_against_owner_witness(changed, witness, CORE_FIELDS)
        reduced = tuple(candidate for candidate in CORE_FIELDS if candidate != field)
        omission_allows_substitution = verify_against_owner_witness(changed, witness, reduced)
        if not full_rejects or not omission_allows_substitution:
            raise RuntimeError(f"field necessity falsifier failed for {field}")
        results.append(
            {
                "field": field,
                "fullCoreRejectsSubstitution": True,
                "omittingFieldAllowsSubstitution": True,
            }
        )
    return results


def union_schema_falsifier(game: dict[str, Any], security: dict[str, Any]) -> dict[str, Any]:
    union_fields = ("cognitionRunId", "planningId", "intentDigest", "migrationId", "generation")
    game_native = game["ownerNative"]
    security_native = security["ownerNative"]
    missing_game = [field for field in union_fields if field not in game_native]
    missing_security = [field for field in union_fields if field not in security_native]
    if not missing_game or not missing_security:
        raise RuntimeError("union-schema falsifier did not separate domain-native vocabularies")
    return {
        "requiredUnionFields": list(union_fields),
        "gameMissing": missing_game,
        "securityMissing": missing_security,
        "universalUnionSchemaValid": False,
        "interpretation": "Requiring the union imports foreign domain semantics; shared World proof must use opaque owner-native digests instead.",
    }


def native_field_classification(game: dict[str, Any], security: dict[str, Any]) -> dict[str, Any]:
    game_native = set(game["ownerNative"])
    security_native = set(security["ownerNative"])
    return {
        "gameOnly": sorted(game_native - security_native),
        "securityOnly": sorted(security_native - game_native),
        "sharedNativeLabels": sorted(game_native & security_native),
        "note": "Shared labels scope/admission/occurrence are proof roles, not shared domain schemas.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--security", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    game_source = json.loads(args.game.read_text())
    security_source = json.loads(args.security.read_text())
    game = game_projection(game_source)
    security = security_projection(security_source)
    if game["subjectRef"] != security["subjectRef"]:
        raise RuntimeError("cross-domain comparison requires the same continuity subject")
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5b-b2-cross-domain-minimum-falsifier",
        "status": "passed",
        "candidateCoreFields": list(CORE_FIELDS),
        "gameProof": game,
        "securityProof": security,
        "gameFieldNecessity": omission_falsifiers(game),
        "securityFieldNecessity": omission_falsifiers(security),
        "unionSchemaFalsifier": union_schema_falsifier(game, security),
        "nativeFieldClassification": native_field_classification(game, security),
        "proven": {
            "sameSubjectCanBeExpressedWithoutSharedDomainVocabulary": True,
            "eachCoreCoordinateIsNecessaryAgainstItsCorrespondingSubstitution": True,
            "cognitionIsNotRequiredBySecurityCommonCore": True,
            "migrationAndGenerationAreNotRequiredByGameCommonCore": True,
            "planningAndIntentAreNotRequiredBySecurityCommonCore": True,
            "ownerNativeScopeAdmissionOccurrenceCanRemainOpaqueToWorld": True,
        },
        "law": "Shared World invariant is a proof interface, not a universal domain model.",
        "limitations": [
            "This is a research proof projection, not a production schema.",
            "Trusted-local owner-authored evidence is assumed; issuer authentication across an untrusted relay is not proven.",
            "The experiment compares two positive bounded occurrence domains, not persistent Presence.",
            "A third materially different consumer has not yet tested whether all six coordinates remain minimal.",
        ],
    }
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidateCoreFields": result["candidateCoreFields"],
        "gameOnly": result["nativeFieldClassification"]["gameOnly"],
        "securityOnly": result["nativeFieldClassification"]["securityOnly"],
        "unionSchemaValid": result["unionSchemaFalsifier"]["universalUnionSchemaValid"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
