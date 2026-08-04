#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import Any

from ordivon_host import (
    EventKind,
    HostExtensionPort,
    HostKernel,
    HostStorage,
    VerificationReceipt,
    VerificationResultItem,
)

from ordivon_world import (
    CloudflareConfig,
    CloudflareWorldAdapter,
    HostWorldExtension,
    SignedHttpTransport,
    TransportError,
)
from ordivon_world.canonical import sha256_digest, sha256_hex
from ordivon_world.cloudflare import CloudflareTransport, HttpResponse


class AcceptanceError(RuntimeError):
    pass


class DropCommittedResponseTransport:
    """Discard one successful POST response after the provider has committed it."""

    def __init__(self, delegate: CloudflareTransport) -> None:
        self.delegate = delegate
        self.post_count = 0
        self.dropped = False
        self.committed_response_digest: str | None = None

    def request(
        self,
        method: str,
        path: str,
        *,
        body: bytes = b"",
        request_id: str,
        extra_headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        response = self.delegate.request(
            method,
            path,
            body=body,
            request_id=request_id,
            extra_headers=extra_headers,
        )
        if method == "POST":
            self.post_count += 1
            if not self.dropped and 200 <= response.status < 300:
                try:
                    value = json.loads(response.body)
                except json.JSONDecodeError as error:
                    raise AcceptanceError(
                        "provider POST succeeded with a non-JSON response"
                    ) from error
                if not isinstance(value, dict) or not isinstance(
                    value.get("receipt"), dict
                ):
                    raise AcceptanceError(
                        "provider POST response has no committed Receipt"
                    )
                self.dropped = True
                self.committed_response_digest = sha256_digest(response.body)
                raise TransportError(
                    "acceptance injected response loss after provider commit"
                )
        return response


def git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise AcceptanceError(
            f"Git command failed: {' '.join(arguments)}: "
            + (completed.stderr or completed.stdout).strip()
        )
    return completed.stdout.strip()


def verify_source(repository: Path, revision: str) -> str:
    repository = repository.resolve()
    head = git(repository, "rev-parse", "HEAD")
    resolved = git(repository, "rev-parse", f"{revision}^{{commit}}")
    if head != resolved:
        raise AcceptanceError(
            f"source HEAD {head} differs from requested revision {resolved}"
        )
    status = git(repository, "status", "--porcelain")
    if status:
        raise AcceptanceError("live acceptance requires a clean source tree")
    return resolved


def write_private_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        os.chmod(path, 0o600)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary.unlink(missing_ok=True)
        raise


def run_acceptance(
    *,
    repository: Path,
    source_revision: str,
    config_path: Path,
    url: str,
) -> dict[str, Any]:
    revision = verify_source(repository, source_revision)
    config = CloudflareConfig.load(config_path)
    initial_transport = SignedHttpTransport(config, attempts=3)
    dropping_transport = DropCommittedResponseTransport(initial_transport)
    initial_adapter = CloudflareWorldAdapter(dropping_transport)
    capability = initial_adapter.capabilities()

    suffix = revision[:12]
    task_id = f"task:world-w1:{suffix}"
    goal_id = f"goal:world-w1:{suffix}"
    effect_id = f"effect:world-w1:{suffix}:fetch"
    dispatch_id = f"dispatch:world-w1:{suffix}:fetch:r1"
    clock = itertools.count(int(time.time() * 1000)).__next__

    with tempfile.TemporaryDirectory(prefix="ordivon-world-w1-") as directory:
        state_root = Path(directory) / "host-state"
        with HostStorage(state_root) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=clock,
                owner_id="host:world-w1:initial",
            )
            created = kernel.create_task(
                event_id=f"event:world-w1:{suffix}:created",
                kind=EventKind.TASK_CREATED,
                task_id=task_id,
                goal_id=goal_id,
                payload={
                    "scenario": "cloudflare-response-loss",
                    "sourceRevision": revision,
                },
                frontier=(f"node:world-w1:{suffix}:fetch",),
            ).projection
            world = HostWorldExtension(HostExtensionPort(storage, kernel))
            prepared = initial_adapter.prepare_fetch(
                dispatch_id=dispatch_id,
                effect_id=effect_id,
                url=url,
                capability=capability,
                maximum_bytes=262_144,
                timeout_ms=15_000,
            )
            prepared_step = world.prepare(task_id, prepared)
            unknown_step = world.deliver(task_id, initial_adapter)
            unknown_snapshot = storage.read_task_event(task_id)
            if unknown_step.status != "unknown":
                raise AcceptanceError("injected response loss did not become UNKNOWN")
            if dropping_transport.post_count != 1 or not dropping_transport.dropped:
                raise AcceptanceError("response-loss transport did not commit exactly one POST")

        fresh_adapter = CloudflareWorldAdapter(
            SignedHttpTransport(CloudflareConfig.load(config_path), attempts=3)
        )
        with HostStorage(state_root) as reopened:
            fresh_kernel = HostKernel(
                reopened,
                clock_ms=clock,
                owner_id="host:world-w1:fresh",
            )
            port = HostExtensionPort(reopened, fresh_kernel)
            fresh_world = HostWorldExtension(port)
            restored = fresh_world.load_prepared(task_id)
            recovered = fresh_world.reconcile(task_id, fresh_adapter)
            if recovered.observation is None:
                raise AcceptanceError("fresh Host did not recover a final Observation")
            if recovered.status != "succeeded" or not recovered.reconciled:
                raise AcceptanceError("fresh Host reconciliation did not succeed")
            if dropping_transport.post_count != 1:
                raise AcceptanceError("fresh Host redispatched the external Effect")
            observation = recovered.observation
            if not observation.envelope.evidence_refs:
                raise AcceptanceError("recovered Observation has no ArtifactRef")
            artifact = observation.envelope.evidence_refs[0]
            artifact_body = fresh_adapter.read_artifact(artifact)
            if not artifact_body:
                raise AcceptanceError("recovered Artifact is empty")
            if "sha256:" + sha256_hex(artifact_body) != artifact.digest:
                raise AcceptanceError("recovered Artifact digest differs")

            decision = {
                "method": "world-w1-artifact-digest-and-nonempty.v1",
                "dispatchId": dispatch_id,
                "artifactRef": artifact.ref,
                "artifactDigest": artifact.digest,
                "artifactBytes": len(artifact_body),
            }
            verification = VerificationReceipt(
                dispatch_id=dispatch_id,
                method=decision["method"],
                accepted=True,
                observation_digest=observation.envelope.payload_digest,
                result_items=(
                    VerificationResultItem(
                        subject_ref=artifact.ref,
                        decision_digest=sha256_digest(decision),
                        status="succeeded",
                        reason=None,
                        evidence_digest=artifact.digest,
                    ),
                ),
            )
            verification_object = port.put_object(
                verification.to_dict(),
                kind="verification-receipt",
            )
            current = port.load(task_id)
            observed_object = port.inspect_object(
                str(current.data["worldObservationDigest"])
            )
            verified = port.append_preserving(
                task_id=task_id,
                expected_revision=current.projection.revision,
                event_id=f"event:world-w1:{suffix}:verified:r{current.projection.revision + 1}",
                kind=EventKind.VERIFICATION_RECORDED,
                updates={
                    "worldVerificationDigest": verification_object.digest,
                    "worldVerificationAccepted": True,
                },
                referenced_objects=(observed_object, verification_object),
                label="World W1 verifier",
            )
            final_snapshot = reopened.read_task_event(task_id)

    checks = {
        "sourceRevisionExact": revision == source_revision,
        "preparedPersistedBeforeDispatch": prepared_step.task_revision == created.revision + 1,
        "oneExternalPost": dropping_transport.post_count == 1,
        "responseDroppedAfterCommit": dropping_transport.dropped,
        "unknownPersisted": unknown_snapshot.data.get("worldOutcomeState") == "unknown",
        "freshHostRecoveredPreparedDispatch": (
            restored.provider_request_id == prepared.provider_request_id
        ),
        "freshHostQueriedOriginalRequest": (
            observation.receipt["receipt_id"] == prepared.provider_request_id
        ),
        "receiptDigestMatchesRequest": (
            observation.receipt["request_digest"]
            == prepared.provider_request_digest
        ),
        "artifactReadAndVerified": bool(artifact_body),
        "verificationAccepted": verification.accepted,
        "taskStatePreserved": final_snapshot.projection.state == created.state,
        "readyFrontierPreserved": (
            final_snapshot.projection.ready_frontier == created.ready_frontier
        ),
        "noTaskCompletionClaim": not final_snapshot.projection.state.terminal,
    }
    if not all(checks.values()):
        raise AcceptanceError(f"live acceptance checks failed: {checks}")

    receipt: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.world-w1-live-receipt",
        "sourceRevision": revision,
        "scenario": "host-cloudflare-fetch-response-loss-reconciliation",
        "task": {
            "taskId": task_id,
            "goalId": goal_id,
            "initialRevision": created.revision,
            "preparedRevision": prepared_step.task_revision,
            "unknownRevision": unknown_step.task_revision,
            "verifiedRevision": verified.projection.revision,
            "finalState": final_snapshot.projection.state.value,
            "readyFrontier": list(final_snapshot.projection.ready_frontier),
        },
        "effect": {
            "effectId": effect_id,
            "dispatchId": dispatch_id,
            "providerRequestId": prepared.provider_request_id,
            "providerRequestDigest": prepared.provider_request_digest,
            "capabilityConditionDigest": prepared.capability_condition_digest,
            "capabilityVersion": prepared.capability_version,
        },
        "provider": {
            "policyVersion": capability.raw["policy_version"],
            "workerVersion": capability.raw["worker_version"],
            "deploymentIdentity": capability.raw["deployment_identity"],
            "committedResponseDigest": dropping_transport.committed_response_digest,
            "postCount": dropping_transport.post_count,
            "receiptStatus": observation.receipt["status"],
            "receiptPayloadDigest": observation.envelope.payload_digest,
        },
        "artifact": {
            "ref": artifact.ref,
            "kind": artifact.kind,
            "digest": artifact.digest,
            "bytes": len(artifact_body),
        },
        "verification": {
            "objectDigest": verification_object.digest,
            "method": verification.method,
            "accepted": verification.accepted,
            "observationDigest": verification.observation_digest,
        },
        "checks": checks,
    }
    receipt["integrity"] = {
        "payloadDigest": sha256_digest(receipt),
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-repo", default="/root/projects/ordivon-world")
    parser.add_argument("--source-revision", required=True)
    parser.add_argument(
        "--config",
        default="/root/.config/ordivon/secrets/edge-client.json",
    )
    parser.add_argument(
        "--url",
        default="https://developers.cloudflare.com/",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    receipt = run_acceptance(
        repository=Path(args.source_repo),
        source_revision=args.source_revision,
        config_path=Path(args.config),
        url=args.url,
    )
    output = Path(args.output)
    write_private_json(output, receipt)
    print(
        json.dumps(
            {
                "ok": True,
                "receipt": str(output),
                "sourceRevision": receipt["sourceRevision"],
                "providerRequestId": receipt["effect"]["providerRequestId"],
                "payloadDigest": receipt["integrity"]["payloadDigest"],
                "checks": len(receipt["checks"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
