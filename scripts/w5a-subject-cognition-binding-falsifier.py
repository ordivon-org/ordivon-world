#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from ordivon_world.canonical import sha256_digest


class W5ASubjectCognitionBindingError(ValueError):
    pass


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise W5ASubjectCognitionBindingError(f"{label} must be an object")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise W5ASubjectCognitionBindingError(f"{label} must be non-empty")
    return value


def _sha256(value: object, label: str) -> str:
    text = _text(value, label)
    if not text.startswith("sha256:") or len(text) != 71:
        raise W5ASubjectCognitionBindingError(f"{label} must be sha256:<64 hex>")
    return text


def verify_binding(
    *,
    subject_ref: str,
    game_input: dict[str, Any],
    harness_evidence: dict[str, Any],
) -> dict[str, Any]:
    _text(subject_ref, "continuity subject")
    if harness_evidence.get("kind") != "ordivon.world.w5a-harness-cognition-evidence":
        raise W5ASubjectCognitionBindingError("Harness evidence kind is unsupported")

    context_digest = _sha256(harness_evidence.get("contextDigest"), "Harness Context digest")
    if sha256_digest(game_input) != context_digest:
        raise W5ASubjectCognitionBindingError("Harness Context digest does not bind the exact Game cognition input")

    receipt = _object(harness_evidence.get("runReceipt"), "Harness Run Receipt")
    receipt_digest = _sha256(harness_evidence.get("runReceiptDigest"), "Harness Run Receipt digest")
    if sha256_digest(receipt) != receipt_digest:
        raise W5ASubjectCognitionBindingError("Harness Run Receipt digest differs from content")
    if receipt.get("kind") != "ordivon.independent-harness-run-receipt":
        raise W5ASubjectCognitionBindingError("Harness Run Receipt kind is unsupported")
    if receipt.get("stopReason") != "completed" or receipt.get("terminationCode") != "candidate_completed":
        raise W5ASubjectCognitionBindingError("Harness Run did not complete with a candidate")
    if receipt.get("harnessRunId") != harness_evidence.get("harnessRunId"):
        raise W5ASubjectCognitionBindingError("Harness Run identity drifted")
    if receipt.get("contractDigest") != harness_evidence.get("contractDigest"):
        raise W5ASubjectCognitionBindingError("Harness Contract digest drifted")
    if receipt.get("callerId") != harness_evidence.get("callerId"):
        raise W5ASubjectCognitionBindingError("Harness caller authority identity drifted")
    if receipt.get("callerRunRef") != subject_ref or harness_evidence.get("callerRunRef") != subject_ref:
        raise W5ASubjectCognitionBindingError("Harness Run is not bound to the requested continuity subject")

    trace_digest = _sha256(harness_evidence.get("traceDigest"), "Harness Trace digest")
    if receipt.get("traceDigest") != trace_digest:
        raise W5ASubjectCognitionBindingError("Harness Trace digest differs from Run Receipt")

    conclusion = _object(harness_evidence.get("conclusion"), "Harness conclusion")
    conclusion_digest = _sha256(harness_evidence.get("conclusionDigest"), "Harness conclusion digest")
    if sha256_digest(conclusion) != conclusion_digest or receipt.get("conclusionDigest") != conclusion_digest:
        raise W5ASubjectCognitionBindingError("Harness conclusion digest differs from terminal evidence")
    if conclusion.get("status") != "candidate_completed":
        raise W5ASubjectCognitionBindingError("Harness conclusion is not a completed candidate")
    summary = _text(conclusion.get("summary"), "Harness conclusion summary")
    try:
        model_decision = json.loads(summary)
    except json.JSONDecodeError as error:
        raise W5ASubjectCognitionBindingError("Harness conclusion summary is not the W5-A decision object") from error
    model_decision = _object(model_decision, "Harness decision")

    context = _object(game_input.get("context"), "Game Agent Context")
    candidates = context.get("candidates")
    if not isinstance(candidates, list):
        raise W5ASubjectCognitionBindingError("Game Agent Context candidates are missing")
    candidate_id = _text(model_decision.get("candidateId"), "Harness-selected Candidate identity")
    selected = next(
        (
            item
            for item in candidates
            if isinstance(item, dict) and item.get("candidateId") == candidate_id
        ),
        None,
    )
    if not isinstance(selected, dict):
        raise W5ASubjectCognitionBindingError("Harness decision is not an admitted Game candidate")
    selected_intent = _object(selected.get("intent"), "selected Game Candidate Intent")
    decision = {"candidateId": candidate_id, "intent": selected_intent}
    if "intent" in model_decision and model_decision.get("intent") != selected_intent:
        raise W5ASubjectCognitionBindingError("Harness decision changed the admitted Game Candidate Intent")

    choice = _object(harness_evidence.get("choice"), "Harness retained choice")
    if decision != choice:
        raise W5ASubjectCognitionBindingError("Harness conclusion Candidate differs from retained exact choice")
    choice_digest = _sha256(harness_evidence.get("choiceDigest"), "Harness choice digest")
    if sha256_digest(choice) != choice_digest:
        raise W5ASubjectCognitionBindingError("Harness choice digest differs from choice content")

    fresh = _object(harness_evidence.get("freshProcess"), "fresh Harness evidence")
    if (
        fresh.get("runReceiptDigest") != receipt_digest
        or fresh.get("traceDigest") != trace_digest
        or fresh.get("conclusion") != conclusion
        or fresh.get("doctorHealthy") is not True
    ):
        raise W5ASubjectCognitionBindingError("fresh Harness process did not recover the exact cognition evidence")

    intent = selected_intent
    actor_id = _text(game_input.get("actorId"), "Game Actor identity")
    if intent.get("actorId") != actor_id or context.get("actor", {}).get("actorId") != actor_id:
        raise W5ASubjectCognitionBindingError("Harness-selected Intent belongs to another Actor")
    if intent.get("expectedWorldRevision") != game_input.get("worldRevision"):
        raise W5ASubjectCognitionBindingError("Harness-selected Intent targets another World revision")
    if context.get("worldDigest") != game_input.get("worldDigest"):
        raise W5ASubjectCognitionBindingError("Game Context World digest differs from exported cognition input")
    if context.get("planningId") != game_input.get("planningId"):
        raise W5ASubjectCognitionBindingError("Game Context belongs to another Planning")

    binding = {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5a-experimental-subject-cognition-binding",
        "subjectRef": subject_ref,
        "subjectAuthorityId": receipt["callerId"],
        "harnessRunId": receipt["harnessRunId"],
        "harnessRunReceiptDigest": receipt_digest,
        "harnessContractDigest": receipt["contractDigest"],
        "harnessTraceDigest": trace_digest,
        "harnessConclusionDigest": conclusion_digest,
        "harnessChoiceDigest": choice_digest,
        "gameRunId": game_input["runId"],
        "planningId": game_input["planningId"],
        "worldRevision": game_input["worldRevision"],
        "worldDigest": game_input["worldDigest"],
        "actorId": actor_id,
        "candidateId": decision["candidateId"],
        "intentDigest": sha256_digest(intent),
    }
    return {"binding": binding, "bindingDigest": sha256_digest(binding), "decision": decision}


def _expect_rejected(label: str, operation) -> dict[str, Any]:
    try:
        operation()
    except W5ASubjectCognitionBindingError as error:
        return {"case": label, "rejected": True, "reason": str(error)}
    raise RuntimeError(f"W5-A negative case unexpectedly passed: {label}")


def run(game_path: Path, harness_path: Path, subject_ref: str) -> dict[str, Any]:
    game = _object(json.loads(game_path.read_text(encoding="utf-8")), "Game cognition input")
    harness = _object(json.loads(harness_path.read_text(encoding="utf-8")), "Harness cognition evidence")
    verified = verify_binding(subject_ref=subject_ref, game_input=game, harness_evidence=harness)

    def wrong_subject() -> dict[str, Any]:
        return verify_binding(
            subject_ref="continuity-subject:mallory",
            game_input=game,
            harness_evidence=harness,
        )
    changed_conclusion = copy.deepcopy(harness)
    changed_conclusion["conclusion"]["summary"] = json.dumps(
        {
            "candidateId": "candidate:substituted",
            "intent": verified["decision"]["intent"],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    changed_context = copy.deepcopy(game)
    changed_context["context"]["candidates"] = [
        item
        for item in changed_context["context"]["candidates"]
        if item.get("candidateId") != verified["decision"]["candidateId"]
    ]

    negative = [
        _expect_rejected("subject-substitution", wrong_subject),
        _expect_rejected(
            "conclusion-substitution",
            lambda: verify_binding(subject_ref=subject_ref, game_input=game, harness_evidence=changed_conclusion),
        ),
        _expect_rejected(
            "game-context-substitution",
            lambda: verify_binding(subject_ref=subject_ref, game_input=changed_context, harness_evidence=harness),
        ),
    ]
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.w5a-subject-cognition-binding-falsifier",
        "status": "passed",
        "binding": verified["binding"],
        "bindingDigest": verified["bindingDigest"],
        "negativeCases": negative,
        "trustProfile": {
            "name": "trusted-local-owner-originated-caller",
            "untrustedRelayAuthentication": False,
            "worldMintsSubjectIdentity": False,
            "worldOwnsHarnessCognition": False,
            "worldOwnsGameActor": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="W5-A Subject → Harness cognition → Game candidate binding falsifier")
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--harness", type=Path, required=True)
    parser.add_argument("--subject-ref", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.game, args.harness, args.subject_ref)
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
