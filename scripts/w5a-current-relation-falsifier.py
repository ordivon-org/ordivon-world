#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from ordivon_world.canonical import sha256_digest


class W5ACurrentRelationError(ValueError):
    pass


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise W5ACurrentRelationError(f"{label} must be an object")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise W5ACurrentRelationError(f"{label} must be non-empty")
    return value


def _digest(value: object, label: str) -> str:
    text = _text(value, label)
    if not text.startswith("sha256:") or len(text) != 71:
        raise W5ACurrentRelationError(f"{label} must be sha256:<64 hex>")
    return text


def create_query(
    *, query_id: str, subject_ref: str, body_ref: str, owner_id: str, scope: dict[str, Any]
) -> dict[str, Any]:
    query = {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5a-current-relation-query",
        "queryId": _text(query_id, "query identity"),
        "subjectRef": _text(subject_ref, "continuity subject"),
        "bodyRef": _text(body_ref, "Body reference"),
        "ownerId": _text(owner_id, "owner identity"),
        "scope": _object(scope, "query scope"),
    }
    return {"query": query, "queryDigest": sha256_digest(query)}


def verify_observation(query_value: dict[str, Any], observation_value: dict[str, Any]) -> dict[str, Any]:
    query = _object(query_value.get("query"), "Current Relation query")
    query_digest = _digest(query_value.get("queryDigest"), "Current Relation query digest")
    if sha256_digest(query) != query_digest:
        raise W5ACurrentRelationError("Current Relation query digest differs from content")
    if query.get("kind") != "ordivon.world.w5a-current-relation-query":
        raise W5ACurrentRelationError("Current Relation query kind is unsupported")

    observation = _object(observation_value.get("observation"), "owner Current Relation observation")
    observation_digest = _digest(
        observation_value.get("observationDigest"), "owner Current Relation observation digest"
    )
    if sha256_digest(observation) != observation_digest:
        raise W5ACurrentRelationError("owner observation digest differs from content")
    if observation.get("kind") != "ordivon.world.w5a-current-relation-observation":
        raise W5ACurrentRelationError("owner Current Relation observation kind is unsupported")
    if observation.get("queryDigest") != query_digest:
        raise W5ACurrentRelationError("owner observation belongs to another Current Relation query")

    for field in ("subjectRef", "bodyRef", "ownerId", "scope"):
        if observation.get(field) != query.get(field):
            raise W5ACurrentRelationError(f"owner observation {field} differs from query")

    body_currentness = observation.get("bodyCurrentness")
    binding_currentness = observation.get("bindingCurrentness")
    if body_currentness not in {"current", "absent", "unknown"}:
        raise W5ACurrentRelationError("Body currentness is unsupported")
    if binding_currentness not in {"current", "absent", "unknown"}:
        raise W5ACurrentRelationError("binding currentness is unsupported")
    evidence = _object(observation.get("evidence"), "owner observation evidence")
    for key, value in evidence.items():
        if key.endswith("Digest") and value is not None:
            _digest(value, f"owner evidence {key}")

    if body_currentness == "absent":
        relation_state = "absent-through-body"
    elif body_currentness == "current" and binding_currentness == "current":
        relation_state = "present-within-scope"
    else:
        relation_state = "unknown"

    projection = {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5a-current-relation-projection",
        "queryId": query["queryId"],
        "queryDigest": query_digest,
        "subjectRef": query["subjectRef"],
        "bodyRef": query["bodyRef"],
        "ownerId": query["ownerId"],
        "scope": query["scope"],
        "bodyCurrentness": body_currentness,
        "bindingCurrentness": binding_currentness,
        "relationState": relation_state,
        "ownerObservationDigest": observation_digest,
        "ownerEvidence": evidence,
        "authority": "informational-current-observation-not-action-authority",
    }
    return {"projection": projection, "projectionDigest": sha256_digest(projection)}


def _expect_rejected(label: str, operation) -> dict[str, Any]:
    try:
        operation()
    except W5ACurrentRelationError as error:
        return {"case": label, "rejected": True, "reason": str(error)}
    raise RuntimeError(f"W5-A current-relation negative case unexpectedly passed: {label}")


def run(query_path: Path, observation_path: Path) -> dict[str, Any]:
    query = _object(json.loads(query_path.read_text(encoding="utf-8")), "query envelope")
    observation = _object(
        json.loads(observation_path.read_text(encoding="utf-8")), "observation envelope"
    )
    verified = verify_observation(query, observation)

    new_query = copy.deepcopy(query)
    new_query["query"]["queryId"] = str(new_query["query"]["queryId"]) + ":fresh"
    new_query["queryDigest"] = sha256_digest(new_query["query"])

    changed_subject = copy.deepcopy(query)
    changed_subject["query"]["subjectRef"] = "continuity-subject:substituted"
    changed_subject["queryDigest"] = sha256_digest(changed_subject["query"])

    changed_body = copy.deepcopy(query)
    changed_body["query"]["bodyRef"] = str(changed_body["query"]["bodyRef"]) + ":replacement"
    changed_body["queryDigest"] = sha256_digest(changed_body["query"])

    negative = [
        _expect_rejected(
            "old-observation-replayed-to-fresh-query",
            lambda: verify_observation(new_query, observation),
        ),
        _expect_rejected(
            "subject-substitution",
            lambda: verify_observation(changed_subject, observation),
        ),
        _expect_rejected(
            "body-substitution",
            lambda: verify_observation(changed_body, observation),
        ),
    ]
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5a-current-relation-falsifier",
        "status": "passed",
        **verified,
        "negativeCases": negative,
        "laws": [
            "Current relation observation is query-bound informational evidence, not action authority",
            "Observation replay across a fresh query is stale and rejected",
            "Body absence proves absence only through that exact Body",
            "Body currentness plus unknown binding currentness yields UNKNOWN",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="W5-A current Subject/Body relation query falsifier")
    sub = parser.add_subparsers(dest="command", required=True)

    make = sub.add_parser("make-query")
    make.add_argument("--query-id", required=True)
    make.add_argument("--subject-ref", required=True)
    make.add_argument("--body-ref", required=True)
    make.add_argument("--owner-id", required=True)
    make.add_argument("--scope-json", required=True)
    make.add_argument("--output", type=Path, required=True)

    check = sub.add_parser("verify")
    check.add_argument("--query", type=Path, required=True)
    check.add_argument("--observation", type=Path, required=True)
    check.add_argument("--output", type=Path)

    args = parser.parse_args()
    if args.command == "make-query":
        scope = _object(json.loads(args.scope_json), "query scope")
        result = create_query(
            query_id=args.query_id,
            subject_ref=args.subject_ref,
            body_ref=args.body_ref,
            owner_id=args.owner_id,
            scope=scope,
        )
    else:
        result = run(args.query, args.observation)

    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if getattr(args, "output", None) is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
