#!/usr/bin/env python3
from __future__ import annotations

from ordivon_world.browser import RetrievedArtifact
from ordivon_world.cloudflare import (
    CloudflareConfig,
    CloudflareWorldAdapter,
    SignedHttpTransport,
    TransportError,
)
from ordivon_world.host import HostWorldExtension

import argparse
import itertools
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import Any, Literal

from ordivon_host import (
    EventKind,
    HostExtensionPort,
    HostKernel,
    HostStorage,
    VerificationReceipt,
    VerificationResultItem,
)


from ordivon_world.canonical import sha256_digest, sha256_hex
from ordivon_world.cloudflare import CloudflareTransport, HttpResponse, WorldObservation

Operation = Literal["fetch", "browser"]


class AcceptanceError(RuntimeError):
    pass


class DropCommittedResponseTransport:
    """Discard one successful POST response after the provider has committed it."""

    def __init__(self, delegate: CloudflareTransport) -> None:
        self.delegate = delegate
        self.post_count = 0
        self.dropped = False
        self.committed_response_digest: str | None = None
        self.committed_response_replayed: bool | None = None

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
                if value["receipt"].get("status") != "succeeded":
                    raise AcceptanceError(
                        "provider returned 2xx without a succeeded committed Receipt"
                    )
                replayed = value.get("replayed")
                if replayed is not False:
                    raise AcceptanceError(
                        "live acceptance requires a first execution, not a replayed Receipt"
                    )
                self.dropped = True
                self.committed_response_replayed = replayed
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


def artifact_summary(artifact: RetrievedArtifact) -> dict[str, Any]:
    return {
        "ref": artifact.reference.ref,
        "kind": artifact.reference.kind,
        "digest": artifact.reference.digest,
        "bytes": artifact.content_length,
        "etag": artifact.etag,
    }


def prepare_operation(
    adapter: CloudflareWorldAdapter,
    *,
    operation: Operation,
    dispatch_id: str,
    effect_id: str,
    url: str,
    capability: Any,
):
    if operation == "fetch":
        return adapter.prepare_fetch(
            dispatch_id=dispatch_id,
            effect_id=effect_id,
            url=url,
            capability=capability,
            maximum_bytes=262_144,
            timeout_ms=15_000,
        )
    return adapter.prepare_browser(
        dispatch_id=dispatch_id,
        effect_id=effect_id,
        url=url,
        capability=capability,
        viewport_width=1365,
        viewport_height=768,
        full_page=False,
        wait_until="domcontentloaded",
        timeout_ms=30_000,
        wait_after_ms=0,
    )


def verify_operation_evidence(
    adapter: CloudflareWorldAdapter,
    observation: WorldObservation,
    *,
    operation: Operation,
    dispatch_id: str,
) -> tuple[
    tuple[RetrievedArtifact, ...],
    VerificationReceipt,
    dict[str, Any],
    dict[str, bool],
]:
    if operation == "fetch":
        if len(observation.envelope.evidence_refs) != 1:
            raise AcceptanceError("Fetch Observation does not contain exactly one Artifact")
        artifact = adapter.read_artifact_record(
            observation.envelope.evidence_refs[0]
        )
        if not artifact.body:
            raise AcceptanceError("recovered Fetch Artifact is empty")
        decision = {
            "method": "world-w1-artifact-digest-and-nonempty.v1",
            "dispatchId": dispatch_id,
            "artifact": artifact_summary(artifact),
        }
        decision_digest = sha256_digest(decision)
        verification = VerificationReceipt(
            dispatch_id=dispatch_id,
            method=decision["method"],
            accepted=True,
            observation_digest=observation.envelope.payload_digest,
            result_items=(
                VerificationResultItem(
                    subject_ref=artifact.reference.ref,
                    decision_digest=decision_digest,
                    status="succeeded",
                    reason=None,
                    evidence_digest=artifact.reference.digest,
                ),
            ),
        )
        return (
            (artifact,),
            verification,
            {"artifact": artifact_summary(artifact)},
            {
                "artifactCountMatchesOperation": True,
                "allArtifactDigestsVerified": (
                    "sha256:" + sha256_hex(artifact.body)
                    == artifact.reference.digest
                ),
            },
        )

    bundle = adapter.read_browser_bundle(observation)
    artifacts = bundle.artifacts
    decision = {
        "method": "world-p2-browser-bundle-integrity.v1",
        "dispatchId": dispatch_id,
        "receiptId": bundle.receipt_id,
        "browser": bundle.browser,
        "artifacts": [artifact_summary(item) for item in artifacts],
        "manifest": bundle.manifest_document,
    }
    decision_digest = sha256_digest(decision)
    verification = VerificationReceipt(
        dispatch_id=dispatch_id,
        method=decision["method"],
        accepted=True,
        observation_digest=observation.envelope.payload_digest,
        result_items=tuple(
            VerificationResultItem(
                subject_ref=item.reference.ref,
                decision_digest=decision_digest,
                status="succeeded",
                reason=None,
                evidence_digest=item.reference.digest,
            )
            for item in artifacts
        ),
    )
    return (
        artifacts,
        verification,
        {
            "browser": bundle.browser,
            "manifest": {
                "schemaVersion": bundle.manifest_document["schema_version"],
                "artifact": artifact_summary(bundle.manifest),
            },
        },
        {
            "artifactCountMatchesOperation": len(artifacts) == 3,
            "allArtifactDigestsVerified": all(
                "sha256:" + sha256_hex(item.body) == item.reference.digest
                for item in artifacts
            ),
            "browserManifestVerified": (
                bundle.manifest_document["receipt_id"] == bundle.receipt_id
            ),
            "browserScreenshotPng": bundle.screenshot.body.startswith(
                b"\x89PNG\r\n\x1a\n"
            ),
            "browserContentUtf8": bool(
                bundle.content.body.decode("utf-8", errors="strict")
            ),
        },
    )


def run_acceptance(
    *,
    repository: Path,
    source_revision: str,
    config_path: Path,
    url: str,
    operation: Operation = "fetch",
) -> dict[str, Any]:
    revision = verify_source(repository, source_revision)
    config = CloudflareConfig.load(config_path)
    initial_transport = SignedHttpTransport(config, attempts=3)
    dropping_transport = DropCommittedResponseTransport(initial_transport)
    initial_adapter = CloudflareWorldAdapter(dropping_transport)
    capability = initial_adapter.capabilities()

    suffix = revision[:12]
    stage = "w1" if operation == "fetch" else "p2-browser"
    provider_operation = "fetch" if operation == "fetch" else "browser.run"
    task_id = f"task:world-{stage}:{suffix}"
    goal_id = f"goal:world-{stage}:{suffix}"
    effect_id = f"effect:world-{stage}:{suffix}:{operation}"
    dispatch_id = f"dispatch:world-{stage}:{suffix}:{operation}:r1"
    clock = itertools.count(int(time.time() * 1000)).__next__

    with tempfile.TemporaryDirectory(prefix=f"ordivon-world-{stage}-") as directory:
        state_root = Path(directory) / "host-state"
        with HostStorage(state_root) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=clock,
                owner_id=f"host:world-{stage}:initial",
            )
            created = kernel.create_task(
                event_id=f"event:world-{stage}:{suffix}:created",
                kind=EventKind.TASK_CREATED,
                task_id=task_id,
                goal_id=goal_id,
                payload={
                    "scenario": f"cloudflare-{operation}-response-loss",
                    "sourceRevision": revision,
                },
                frontier=(f"node:world-{stage}:{suffix}:{operation}",),
            ).projection
            world = HostWorldExtension(HostExtensionPort(storage, kernel))
            prepared = prepare_operation(
                initial_adapter,
                operation=operation,
                dispatch_id=dispatch_id,
                effect_id=effect_id,
                url=url,
                capability=capability,
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
                owner_id=f"host:world-{stage}:fresh",
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
            if observation.receipt["operation"] != provider_operation:
                raise AcceptanceError("recovered Receipt operation differs")

            artifacts, verification, operation_details, operation_checks = (
                verify_operation_evidence(
                    fresh_adapter,
                    observation,
                    operation=operation,
                    dispatch_id=dispatch_id,
                )
            )
            verification_digest = sha256_digest(verification.to_dict())
            final_snapshot = reopened.read_task_event(task_id)

    checks = {
        "sourceRevisionExact": revision == source_revision,
        "preparedPersistedBeforeDispatch": (
            prepared_step.task_revision == created.revision + 1
        ),
        "oneExternalPost": dropping_transport.post_count == 1,
        "responseDroppedAfterCommit": dropping_transport.dropped,
        "firstExecutionNotReplay": (
            dropping_transport.committed_response_replayed is False
        ),
        "unknownPersisted": (
            unknown_snapshot.data["worldDispatches"][dispatch_id].get(
                "worldOutcomeState"
            )
            == "unknown"
        ),
        "freshHostRecoveredPreparedDispatch": (
            restored.provider_request_id == prepared.provider_request_id
        ),
        "freshHostQueriedOriginalRequest": (
            observation.receipt["receipt_id"] == prepared.provider_request_id
        ),
        "worldObservationAvailabilityRecorded": (
            isinstance(observation.available_at, str) and bool(observation.available_at)
        ),
        "providerCompletionTimeRetained": (
            isinstance(observation.receipt.get("completed_at"), str)
            and bool(observation.receipt.get("completed_at"))
        ),
        "receiptDigestMatchesRequest": (
            observation.receipt["request_digest"]
            == prepared.provider_request_digest
        ),
        "operationIdentityMatches": (
            observation.receipt["operation"] == provider_operation
        ),
        "verificationAccepted": verification.accepted,
        "verificationCoversAllArtifacts": (
            len(verification.result_items) == len(artifacts)
        ),
        "taskStatePreserved": final_snapshot.projection.state == created.state,
        "readyFrontierPreserved": (
            final_snapshot.projection.ready_frontier == created.ready_frontier
        ),
        "noTaskCompletionClaim": not final_snapshot.projection.state.terminal,
        **operation_checks,
    }
    if not all(checks.values()):
        raise AcceptanceError(f"live acceptance checks failed: {checks}")

    receipt: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": (
            "ordivon.world-w1-live-receipt"
            if operation == "fetch"
            else "ordivon.world-p2-browser-live-receipt"
        ),
        "sourceRevision": revision,
        "scenario": (
            "host-cloudflare-fetch-response-loss-reconciliation"
            if operation == "fetch"
            else "host-cloudflare-browser-bundle-response-loss-reconciliation"
        ),
        "operation": operation,
        "task": {
            "taskId": task_id,
            "goalId": goal_id,
            "initialRevision": created.revision,
            "preparedRevision": prepared_step.task_revision,
            "unknownRevision": unknown_step.task_revision,
            "observationRevision": recovered.task_revision,
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
            "committedResponseReplayed": (
                dropping_transport.committed_response_replayed
            ),
            "postCount": dropping_transport.post_count,
            "receiptStatus": observation.receipt["status"],
            "receiptPayloadDigest": observation.envelope.payload_digest,
            "startedAt": observation.receipt["started_at"],
            "completedAt": observation.receipt.get("completed_at"),
            "worldObservationAvailableAt": observation.available_at,
        },
        "artifacts": [artifact_summary(item) for item in artifacts],
        "verification": {
            "digest": verification_digest,
            "method": verification.method,
            "accepted": verification.accepted,
            "observationDigest": verification.observation_digest,
            "resultItems": len(verification.result_items),
        },
        **operation_details,
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
    parser.add_argument(
        "--operation",
        choices=("fetch", "browser"),
        default="fetch",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    receipt = run_acceptance(
        repository=Path(args.source_repo),
        source_revision=args.source_revision,
        config_path=Path(args.config),
        url=args.url,
        operation=args.operation,
    )
    output = Path(args.output)
    write_private_json(output, receipt)
    print(
        json.dumps(
            {
                "ok": True,
                "operation": receipt["operation"],
                "receipt": str(output),
                "sourceRevision": receipt["sourceRevision"],
                "providerRequestId": receipt["effect"]["providerRequestId"],
                "payloadDigest": receipt["integrity"]["payloadDigest"],
                "checks": len(receipt["checks"]),
                "artifacts": len(receipt["artifacts"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
