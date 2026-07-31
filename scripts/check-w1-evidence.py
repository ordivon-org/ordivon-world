#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/w1/w1-live-20260731c.json"
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
REVISION = re.compile(r"^[0-9a-f]{40}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


document = json.loads(EVIDENCE.read_text())
require(document.get("schemaVersion") == 1, "unsupported W1 evidence schema")
require(document.get("kind") == "ordivon.world.w1.closeout-evidence", "invalid W1 evidence identity")
require(document.get("experimentId") == "w1-live-20260731c", "unexpected W1 experiment identity")

source = document.get("source", {})
for field in ("worldBaseRevision", "implementationRevision", "implementationTree", "hostRevision"):
    require(bool(REVISION.fullmatch(source.get(field, ""))), f"invalid W1 source revision: {field}")
require(source.get("implementationRevision") == "41024df17e70b41c84705bf59c7966d6c90609ef", "W1 implementation revision drifted")
require(source.get("providerCapabilityVersion") == "fetch.v2", "W1 provider capability drifted")

workload = document.get("frozenWorkload", {})
require(workload.get("target") == "https://example.com/", "W1 target drifted")
require(workload.get("operation") == "fetch", "W1 operation drifted")
require(
    workload.get("faultPoint") == "after-provider-receipt-commit-before-host-admission",
    "W1 fault drifted",
)
require(
    workload.get("providerRequestDigest")
    == "8e6cebfe3a2abe4290e3e6b7517292612b8e2705d6db7533286bd19f53f1b9c4",
    "W1 provider digest drifted",
)
require(bool(SHA256.fullmatch(workload.get("probeProjectionDigest", ""))), "invalid probe projection digest")

arms = document.get("arms", {})
require(set(arms) == {"b0-direct", "b1-correlation"}, "W1 arms differ")
for name, arm in arms.items():
    require(arm.get("providerPostAttempts") == 1, f"{name} did not issue exactly one POST")
    require(arm.get("providerExecutions") == 1, f"{name} did not execute exactly once")
    require(arm.get("receiptQueries") == 1, f"{name} did not reconcile once")
    require(arm.get("artifactDownloads") == 1, f"{name} did not retrieve one Artifact")
    require(arm.get("duplicateExternalEffects") == 0, f"{name} duplicated an Effect")
    require(arm.get("unsafeRedispatchAttempts") == 0, f"{name} blindly redispatched")
    require(arm.get("operatorInterventions") == 0, f"{name} required operator intervention")
    require(arm.get("exactlyOnceCompletion") is True, f"{name} did not complete exactly once")
    require(arm.get("firstAdmissibleAfterRestart") == "reconcile-original-request", f"{name} resumed incorrectly")
    require(bool(SHA256.fullmatch(arm.get("providerReceiptDigest", ""))), f"invalid {name} Receipt digest")
    require(len(arm.get("artifactSha256", "")) == 64, f"invalid {name} Artifact digest")

comparison = document.get("comparison", {})
require(comparison.get("bothCompletedExactlyOnce") is True, "W1 pair did not complete exactly once")
require(comparison.get("bothAvoidedDuplicateEffects") is True, "W1 pair duplicated an Effect")
require(comparison.get("sameArtifactContent") is True, "W1 arms produced different content")
require(comparison.get("b1AdditionalCorrelationEvents") == 6, "unexpected B1 event cost")
require(comparison.get("b1CorrelationBytes") == 4535, "unexpected B1 byte cost")
require(comparison.get("b1HostObjectDelta") == 0, "B1 changed Host object count")
require(comparison.get("correlationImplementationLines") == 169, "B1 implementation cost drifted")

negative = document.get("negativeEvidence", {})
require(negative.get("reasonCode") == "provider-request-digest-semantics-mislabeled", "negative evidence missing")
require(negative.get("artifactVerified") is True, "invalid Trial Artifact was not reconciled")

fields = document.get("fieldDispositions", [])
require(len(fields) == 9, "W1 field disposition count differs")
require(any(item.get("disposition") == "delete-as-production-layer" for item in fields), "correlation layer disposition missing")

decision = document.get("decision", {})
require(decision.get("worldCorrelationLayer") == "do-not-retain", "W1 architecture decision drifted")
require(decision.get("semantics") == "absorb-into-host-and-provider-observation-adapters", "W1 ownership decision drifted")
require(decision.get("w2") == "remain-conditional-not-activated", "W2 was activated without evidence")

for label, digest in document.get("artifacts", {}).items():
    require(bool(SHA256.fullmatch(digest)), f"invalid W1 Artifact digest: {label}")

serialized = EVIDENCE.read_text().lower()
for forbidden in ("authorization", "hmac_secret", "private_key", "remote_ip"):
    require(forbidden not in serialized, f"W1 evidence contains forbidden field: {forbidden}")

print("ordivon-world W1 closeout evidence: ok")
