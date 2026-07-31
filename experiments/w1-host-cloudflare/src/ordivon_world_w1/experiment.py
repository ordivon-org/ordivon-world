from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import time
from typing import Any

from anc_canonical import canonical_digest
from ordivon_host import (
    ArtifactRef,
    DispatchEnvelope,
    EffectLifecycleHost,
    HostStorage,
    StateRef,
    TaskDescriptor,
    TaskOutcome,
    TaskState,
    VerificationReceipt,
    VerificationResultItem,
)

from .correlation import HashChainJournal
from .models import ProbeProjection
from .provider import CloudflareFetchExecutor, ProviderClient, provider_request_digest


class TrialArm(str, Enum):
    DIRECT = "b0-direct"
    CORRELATION = "b1-correlation"


class MonotonicClock:
    def __init__(self) -> None:
        self.last = 0

    def __call__(self) -> int:
        current = int(time.time() * 1000)
        self.last = max(current, self.last + 1)
        return self.last


@dataclass(frozen=True, slots=True)
class TrialConfig:
    arm: TrialArm
    trial_id: str
    root: Path

    def __post_init__(self) -> None:
        if not self.trial_id or self.trial_id != self.trial_id.strip():
            raise ValueError("trial id must be a non-empty trimmed string")

    @property
    def token(self) -> str:
        return hashlib.sha256(f"{self.arm.value}:{self.trial_id}".encode()).hexdigest()[:16]

    @property
    def goal_id(self) -> str:
        return f"goal:w1:{self.token}"

    @property
    def task_id(self) -> str:
        return f"task:w1:{self.token}"

    @property
    def effect_id(self) -> str:
        return f"effect:w1:{self.token}"

    @property
    def dispatch_id(self) -> str:
        return f"dispatch:w1:{self.token}"

    @property
    def provider_request_id(self) -> str:
        return f"w1_{hashlib.sha256(self.trial_id.encode()).hexdigest()[:32]}"

    @property
    def host_root(self) -> Path:
        return self.root / "host"

    @property
    def evidence_root(self) -> Path:
        return self.root / "evidence"

    @property
    def trial_journal_path(self) -> Path:
        return self.evidence_root / "trial-events.jsonl"

    @property
    def correlation_path(self) -> Path:
        return self.root / "correlation.jsonl"

    @property
    def final_report_path(self) -> Path:
        return self.evidence_root / "final-report.json"


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def _journals(config: TrialConfig, clock: MonotonicClock) -> tuple[HashChainJournal, HashChainJournal | None]:
    trial = HashChainJournal(config.trial_journal_path, clock_ms=clock, label=f"trial:{config.token}")
    correlation = None
    if config.arm is TrialArm.CORRELATION:
        correlation = HashChainJournal(
            config.correlation_path,
            clock_ms=clock,
            label=f"correlation:{config.token}",
        )
    return trial, correlation


def _record_callback(journal: HashChainJournal):
    def record(event_type: str, payload: dict[str, Any]) -> None:
        journal.append(event_type, payload)

    return record


def _provider_payload() -> dict[str, object]:
    return {
        "url": "https://example.com/",
        "maximum_bytes": 65_536,
        "timeout_ms": 10_000,
        "accept": "text/html",
    }


def _host_request(config: TrialConfig, probe: ProbeProjection) -> dict[str, object]:
    payload = _provider_payload()
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.w1.cloudflare-fetch-request",
        "arm": config.arm.value,
        "providerRequestId": config.provider_request_id,
        "providerRequestDigest": provider_request_digest(payload),
        "providerPayload": payload,
        "pathObservationDigest": probe.digest,
    }


def _task_descriptor(config: TrialConfig) -> TaskDescriptor:
    return TaskDescriptor(
        task_id=config.task_id,
        goal_id=config.goal_id,
        workload_id="ordivon.world.w1.fetch.v1",
        assignee_ref="participant:world-w1-runner",
        provider_policy_ref="provider-policy:cloudflare-fetch-v2",
        domain_ref="world-experiment:w1:example-com",
    )


def dispatch_phase(
    config: TrialConfig,
    *,
    provider: ProviderClient,
    probe_source: dict[str, object],
) -> dict[str, object]:
    clock = MonotonicClock()
    trial, correlation = _journals(config, clock)
    probe = ProbeProjection.from_source(probe_source)
    config.evidence_root.mkdir(parents=True, exist_ok=True)
    _write_json(config.evidence_root / "probe-source.json", probe_source)
    _write_json(config.evidence_root / "probe-projection.json", probe.to_dict())
    request = _host_request(config, probe)
    effect = {
        "schemaVersion": 1,
        "kind": "ordivon.world.w1.fetch-effect",
        "effectId": config.effect_id,
        "target": "w1-example",
        "consequence": "read-public-document",
    }
    dispatch = DispatchEnvelope(
        dispatch_id=config.dispatch_id,
        effect_id=config.effect_id,
        executor_id=CloudflareFetchExecutor.executor_id,
        request_digest=canonical_digest(request),
        idempotency_key=config.provider_request_id,
        required_state_refs=(
            StateRef(
                ref=f"path-observation:{probe.collection_id}:{probe.sample_index}",
                digest=probe.digest,
            ),
        ),
        expected_observation_kind="ordivon.world.w1.cloudflare-fetch-receipt.v1",
    )
    descriptor = _task_descriptor(config)
    with HostStorage(config.host_root) as storage:
        host = EffectLifecycleHost(storage, clock_ms=clock)
        host.create_task(descriptor, frontier=f"node:w1:{config.token}:prepare")
        prepared = host.prepare(
            task_id=config.task_id,
            prepare_frontier=f"node:w1:{config.token}:prepare",
            reconcile_frontier=f"node:w1:{config.token}:reconcile",
            verify_frontier=f"node:w1:{config.token}:verify",
            result_frontier=f"node:w1:{config.token}:result",
            effect=effect,
            request=request,
            dispatch=dispatch,
        )
        trial.append(
            "host_dispatch_prepared",
            {
                "arm": config.arm.value,
                "goalId": config.goal_id,
                "taskId": config.task_id,
                "taskRevision": prepared.task_revision,
                "effectId": config.effect_id,
                "dispatchId": config.dispatch_id,
                "pathObservationDigest": probe.digest,
                "providerRequestId": config.provider_request_id,
                "providerRequestDigest": request["providerRequestDigest"],
            },
        )
        if correlation is not None:
            correlation.append(
                "interaction_prepared",
                {
                    "host": {
                        "goalId": config.goal_id,
                        "taskId": config.task_id,
                        "taskRevision": prepared.task_revision,
                        "effectId": config.effect_id,
                        "dispatchId": config.dispatch_id,
                    },
                    "pathObservation": {
                        "ref": dispatch.required_state_refs[0].ref,
                        "digest": probe.digest,
                    },
                    "provider": {
                        "endpointLabel": "edge.ordivon.com",
                        "operation": "fetch",
                        "requestId": config.provider_request_id,
                        "requestDigest": request["providerRequestDigest"],
                    },
                },
            )
        executor = CloudflareFetchExecutor(
            provider,
            record=_record_callback(trial),
            correlation=correlation,
            inject_post_commit_loss=True,
        )
        step = host.deliver(prepared, executor)
        if step.state is not TaskState.WAITING or step.frontier != prepared.reconcile_frontier:
            raise RuntimeError("W1 fault did not leave the Host at reconcile-first WAITING")
        trial.append(
            "host_unknown_recorded",
            {
                "taskId": config.task_id,
                "revision": step.revision,
                "dispatchId": config.dispatch_id,
                "next": "reconcile-original-request",
            },
        )
        receipt = {
            "schemaVersion": 1,
            "kind": "ordivon.world.w1.dispatch-phase-receipt",
            "arm": config.arm.value,
            "trialId": config.trial_id,
            "taskId": config.task_id,
            "taskRevision": step.revision,
            "taskState": step.state.value,
            "frontier": step.frontier,
            "providerRequestId": config.provider_request_id,
            "pathObservationDigest": probe.digest,
            "hostEventCount": storage.journal.event_count(config.task_id),
            "hostObjectCount": storage.journal.object_ref_count(),
        }
    _write_json(config.evidence_root / "dispatch-phase.json", receipt)
    return receipt


def resume_phase(
    config: TrialConfig,
    *,
    provider: ProviderClient,
    reconcile_attempts: int = 5,
    reconcile_delay_seconds: float = 0.25,
) -> dict[str, object]:
    if reconcile_attempts < 1:
        raise ValueError("reconcile attempts must be positive")
    clock = MonotonicClock()
    trial, correlation = _journals(config, clock)
    resume_started = time.monotonic()
    trial.append(
        "fresh_process_started",
        {"taskId": config.task_id, "next": "reconcile-original-request"},
    )
    with HostStorage(config.host_root) as storage:
        host = EffectLifecycleHost(storage, clock_ms=clock)
        executor = CloudflareFetchExecutor(
            provider,
            record=_record_callback(trial),
            correlation=correlation,
            inject_post_commit_loss=False,
        )
        step = None
        for attempt in range(1, reconcile_attempts + 1):
            trial.append("host_reconcile_attempt", {"attempt": attempt, "taskId": config.task_id})
            step = host.reconcile(config.task_id, executor)
            if step.state is not TaskState.WAITING:
                break
            if attempt < reconcile_attempts:
                time.sleep(reconcile_delay_seconds)
        assert step is not None
        if step.state is TaskState.WAITING:
            report = _report(
                config,
                storage=storage,
                trial=trial,
                correlation=correlation,
                phase="pending",
                recovery_latency_ms=int((time.monotonic() - resume_started) * 1000),
            )
            _write_json(config.final_report_path, report)
            return report
        if step.state is not TaskState.VERIFYING:
            raise RuntimeError(f"reconciled provider result cannot be verified: {step.state.value}")

        verified_artifact: ArtifactRef | None = None

        def verify(prepared, observation):
            nonlocal verified_artifact
            receipt, artifact, body = executor.retrieve_artifact()
            actual = hashlib.sha256(body).hexdigest()
            digest_ok = actual == artifact.sha256
            content_ok = b"Example Domain" in body
            receipt_ok = (
                receipt.status == "succeeded"
                and receipt.request_digest == provider_request_digest(_provider_payload())
                and receipt.fetch is not None
                and receipt.fetch.get("http_status") == 200
            )
            accepted = receipt_ok and digest_ok and content_ok
            verified_artifact = ArtifactRef(
                ref=f"cloudflare-artifact:{artifact.key}",
                kind="cloudflare-fetch-artifact",
                digest=f"sha256:{artifact.sha256}",
            )
            results = (
                VerificationResultItem(
                    subject_ref=f"provider-receipt:{receipt.receipt_id}",
                    decision_digest=canonical_digest({"check": "receipt", "accepted": receipt_ok}),
                    status="succeeded" if receipt_ok else "failed",
                    reason=None if receipt_ok else "provider Receipt did not prove the frozen Fetch",
                    evidence_digest=receipt.digest,
                ),
                VerificationResultItem(
                    subject_ref=verified_artifact.ref,
                    decision_digest=canonical_digest({"check": "sha256", "accepted": digest_ok}),
                    status="succeeded" if digest_ok else "failed",
                    reason=None if digest_ok else "Artifact bytes did not match the provider digest",
                    evidence_digest=f"sha256:{actual}",
                ),
                VerificationResultItem(
                    subject_ref="acceptance:w1-example-domain",
                    decision_digest=canonical_digest({"check": "content", "accepted": content_ok}),
                    status="succeeded" if content_ok else "failed",
                    reason=None if content_ok else "Artifact omitted the bounded Example Domain predicate",
                    evidence_digest=f"sha256:{actual}",
                ),
            )
            trial.append(
                "independent_verification",
                {
                    "receiptAccepted": receipt_ok,
                    "artifactDigestAccepted": digest_ok,
                    "contentPredicateAccepted": content_ok,
                    "accepted": accepted,
                },
            )
            if correlation is not None:
                correlation.append(
                    "host_verification_recorded",
                    {
                        "taskId": config.task_id,
                        "dispatchId": prepared.dispatch.dispatch_id,
                        "receiptDigest": receipt.digest,
                        "artifactRef": verified_artifact.to_dict(),
                        "accepted": accepted,
                    },
                )
            return VerificationReceipt(
                dispatch_id=prepared.dispatch.dispatch_id,
                method="world-w1-example-domain.v1",
                accepted=accepted,
                observation_digest=canonical_digest(observation.to_dict()),
                result_items=results,
            )

        verified = host.verify(config.task_id, verify)
        accepted = verified.state is TaskState.READY
        outcome = TaskOutcome(
            task_id=config.task_id,
            goal_id=config.goal_id,
            status="completed" if accepted else "blocked",
            verification_digest=verified.verification_digest,
            artifact_refs=() if verified_artifact is None else (verified_artifact,),
        )
        completed = host.complete(config.task_id, outcome)
        trial.append(
            "task_outcome_recorded",
            {
                "taskId": config.task_id,
                "state": completed.state.value,
                "outcomeDigest": completed.outcome_digest,
            },
        )
        if correlation is not None:
            correlation.append(
                "task_outcome_recorded",
                {
                    "taskId": config.task_id,
                    "taskRevision": completed.revision,
                    "state": completed.state.value,
                    "outcomeDigest": completed.outcome_digest,
                },
            )
        report = _report(
            config,
            storage=storage,
            trial=trial,
            correlation=correlation,
            phase="completed" if accepted else "blocked",
            recovery_latency_ms=int((time.monotonic() - resume_started) * 1000),
        )
    _write_json(config.final_report_path, report)
    return report


def _report(
    config: TrialConfig,
    *,
    storage: HostStorage,
    trial: HashChainJournal,
    correlation: HashChainJournal | None,
    phase: str,
    recovery_latency_ms: int,
) -> dict[str, object]:
    events = trial.events()
    post_attempts = sum(event.event_type == "provider_post_attempt" for event in events)
    fetch_responses = [event for event in events if event.event_type == "provider_fetch_response"]
    provider_executions = sum(event.payload.get("replayed") is False for event in fetch_responses)
    task_outcomes = sum(event.event_type == "task_outcome_recorded" for event in events)
    projection = storage.journal.get_task(config.task_id)
    final_state = None if projection is None else projection.state.value
    evidence_bytes = sum(
        path.stat().st_size
        for path in config.evidence_root.rglob("*")
        if path.is_file()
    )
    host_object_bytes = sum(
        path.stat().st_size
        for path in (config.host_root / "objects").rglob("*")
        if path.is_file()
    )
    host_database_bytes = (config.host_root / "host.sqlite3").stat().st_size
    correlation_events = () if correlation is None else correlation.events()
    correlation_bytes = 0 if correlation is None else config.correlation_path.stat().st_size
    receipt = None
    for event in reversed(events):
        if event.event_type == "provider_receipt_reconciled":
            receipt = {
                "requestId": event.payload.get("requestId"),
                "receiptDigest": event.payload.get("receiptDigest"),
                "status": event.payload.get("status"),
            }
            break
    return {
        "schemaVersion": 1,
        "kind": "ordivon.world.w1.trial-report",
        "arm": config.arm.value,
        "trialId": config.trial_id,
        "phase": phase,
        "goalId": config.goal_id,
        "taskId": config.task_id,
        "effectId": config.effect_id,
        "dispatchId": config.dispatch_id,
        "providerRequestId": config.provider_request_id,
        "finalTaskState": final_state,
        "providerPostAttempts": post_attempts,
        "providerExecutions": provider_executions,
        "duplicateExternalEffects": max(0, provider_executions - 1),
        "unsafeRedispatchAttempts": max(0, post_attempts - 1),
        "receiptQueries": sum(event.event_type == "provider_receipt_query" for event in events),
        "artifactDownloads": sum(event.event_type == "provider_artifact_download" for event in events),
        "operatorInterventions": 0,
        "recoveryLatencyMs": recovery_latency_ms,
        "hostEventCount": storage.journal.event_count(config.task_id),
        "hostObjectCount": storage.journal.object_ref_count(),
        "hostObjectBytes": host_object_bytes,
        "hostDatabaseBytes": host_database_bytes,
        "trialEventCount": len(events),
        "taskOutcomeEvents": task_outcomes,
        "exactlyOnceCompletion": final_state == "completed" and task_outcomes == 1,
        "correlationExists": correlation is not None,
        "correlationEventCount": len(correlation_events),
        "correlationBytes": correlation_bytes,
        "correlationHeadDigest": None if not correlation_events else correlation_events[-1].digest,
        "providerReceipt": receipt,
        "evidenceBytesBeforeFinalReport": evidence_bytes,
        "firstAdmissibleAfterRestart": "reconcile-original-request",
    }
