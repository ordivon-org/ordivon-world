from __future__ import annotations

from collections.abc import Callable
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Protocol
from urllib.parse import quote

from anc_canonical import JsonValue, canonical_digest
from ordivon_host import (
    ArtifactRef,
    DeliveryUncertain,
    DispatchEnvelope,
    ObservationEnvelope,
)

from .correlation import HashChainJournal
from .models import ProviderArtifact, ProviderPendingReceipt, ProviderReceipt


class ProviderProtocolError(RuntimeError):
    pass


class ProviderClient(Protocol):
    def fetch(self, request_id: str, payload: dict[str, object]) -> tuple[ProviderReceipt, bool]: ...

    def receipt(self, request_id: str) -> ProviderReceipt | ProviderPendingReceipt | None: ...

    def artifact(self, artifact: ProviderArtifact) -> bytes: ...


def provider_request_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def provider_body_digest(payload: dict[str, object]) -> str:
    return hashlib.sha256(provider_request_bytes(payload)).hexdigest()


def provider_request_digest(payload: dict[str, object]) -> str:
    idempotency_request = "\n".join(
        (
            "ordivon-edge-idempotency-v1",
            "POST",
            "/v1/fetch",
            provider_body_digest(payload),
        )
    )
    return hashlib.sha256(idempotency_request.encode("utf-8")).hexdigest()


def _receipt_from_envelope(raw: bytes) -> tuple[ProviderReceipt, bool]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ProviderProtocolError("provider returned invalid JSON") from error
    if not isinstance(value, dict) or set(value) != {"receipt", "replayed"}:
        raise ProviderProtocolError("provider Receipt envelope fields differ")
    if not isinstance(value["replayed"], bool):
        raise ProviderProtocolError("provider replay flag is invalid")
    return ProviderReceipt.from_dict(value["receipt"]), value["replayed"]


class SignedEdgeClient:
    """Adapter over the inherited signed provider client; it owns no World state."""

    def __init__(
        self,
        *,
        repository_root: str | Path,
        config_path: str | Path | None = None,
    ) -> None:
        root = Path(repository_root)
        module_path = root / "providers/cloudflare/scripts/ordivon_edge_client.py"
        spec = importlib.util.spec_from_file_location("ordivon_world_w1_edge_client", module_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load inherited Edge client")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        self.module = module
        resolved_config = module.DEFAULT_CONFIG if config_path is None else Path(config_path).expanduser()
        self.config = module.load_config(resolved_config)

    def fetch(self, request_id: str, payload: dict[str, object]) -> tuple[ProviderReceipt, bool]:
        status, _, body = self.module.request(
            self.config,
            "POST",
            "/v1/fetch",
            body=provider_request_bytes(payload),
            request_id=request_id,
            transport_attempts=1,
        )
        if status != 200:
            raise ProviderProtocolError(f"Fetch returned HTTP {status}")
        receipt, replayed = _receipt_from_envelope(body)
        self._validate_request(receipt, request_id, payload)
        return receipt, replayed

    def receipt(self, request_id: str) -> ProviderReceipt | ProviderPendingReceipt | None:
        status, _, body = self.module.request(
            self.config,
            "GET",
            f"/v1/receipts/{quote(request_id, safe='')}",
            transport_attempts=1,
        )
        if status == 404:
            return None
        try:
            value = json.loads(body)
        except json.JSONDecodeError as error:
            raise ProviderProtocolError("receipt lookup returned invalid JSON") from error
        if status == 202:
            return ProviderPendingReceipt.from_dict(value)
        if status == 200:
            return ProviderReceipt.from_dict(value)
        raise ProviderProtocolError(f"Receipt lookup returned HTTP {status}")

    def artifact(self, artifact: ProviderArtifact) -> bytes:
        encoded = "/".join(quote(segment, safe="") for segment in artifact.key.split("/"))
        status, headers, body = self.module.request(
            self.config,
            "GET",
            f"/v1/artifacts/{encoded}",
            transport_attempts=1,
        )
        if status != 200:
            raise ProviderProtocolError(f"Artifact retrieval returned HTTP {status}")
        normalized = {str(key).lower(): str(value) for key, value in headers.items()}
        actual = hashlib.sha256(body).hexdigest()
        header_digest = normalized.get("x-ordivon-sha256")
        if actual != artifact.sha256 or header_digest != artifact.sha256:
            raise ProviderProtocolError("Artifact digest differs from Receipt or provider metadata")
        if len(body) != artifact.bytes:
            raise ProviderProtocolError("Artifact byte length differs from Receipt")
        return body

    @staticmethod
    def _validate_request(receipt: ProviderReceipt, request_id: str, payload: dict[str, object]) -> None:
        if receipt.receipt_id != request_id:
            raise ProviderProtocolError("Receipt identity differs from Request ID")
        if receipt.request_digest != provider_request_digest(payload):
            raise ProviderProtocolError("Receipt request digest differs from canonical provider body")


class CloudflareFetchExecutor:
    executor_id = "executor:cloudflare-fetch-v2"

    def __init__(
        self,
        client: ProviderClient,
        *,
        record: Callable[[str, dict[str, Any]], None],
        correlation: HashChainJournal | None = None,
        inject_post_commit_loss: bool = False,
    ) -> None:
        self.client = client
        self.record = record
        self.correlation = correlation
        self.inject_post_commit_loss = inject_post_commit_loss
        self.last_receipt: ProviderReceipt | None = None

    def deliver(
        self,
        dispatch: DispatchEnvelope,
        request: dict[str, JsonValue],
    ) -> ObservationEnvelope:
        request_id, payload = self._request(dispatch, request)
        self.record("provider_post_attempt", {"requestId": request_id})
        receipt, replayed = self.client.fetch(request_id, payload)
        self.last_receipt = receipt
        self.record(
            "provider_fetch_response",
            {
                "requestId": request_id,
                "receiptDigest": receipt.digest,
                "status": receipt.status,
                "replayed": replayed,
            },
        )
        if self.correlation is not None:
            self.correlation.append(
                "provider_receipt_committed",
                {
                    "providerRequestId": request_id,
                    "providerRequestDigest": receipt.request_digest,
                    "receiptId": receipt.receipt_id,
                    "receiptDigest": receipt.digest,
                    "status": receipt.status,
                    "policyVersion": receipt.execution.policy_version,
                    "capabilityVersion": receipt.execution.capability_version,
                    "workerVersionId": receipt.execution.worker_version_id,
                    "leaseGeneration": receipt.execution.lease_generation,
                    "artifact": None if receipt.artifact is None else receipt.artifact.to_dict(),
                },
            )
        if self.inject_post_commit_loss:
            if receipt.status != "succeeded" or receipt.artifact is None:
                raise ProviderProtocolError("W1 fault requires a succeeded committed Fetch Receipt")
            self.record(
                "fault_injected",
                {
                    "faultPoint": "after-provider-receipt-commit-before-host-admission",
                    "requestId": request_id,
                },
            )
            if self.correlation is not None:
                self.correlation.append(
                    "caller_response_dropped",
                    {
                        "providerRequestId": request_id,
                        "receiptDigest": receipt.digest,
                        "faultPoint": "after-provider-receipt-commit-before-host-admission",
                    },
                )
            raise DeliveryUncertain("W1 injected response loss after provider Receipt commit")
        return self._observation(dispatch, receipt)

    def observe(
        self,
        dispatch: DispatchEnvelope,
        request: dict[str, JsonValue],
    ) -> ObservationEnvelope | None:
        request_id, payload = self._request(dispatch, request)
        self.record("provider_receipt_query", {"requestId": request_id})
        record = self.client.receipt(request_id)
        if record is None:
            self.record("provider_receipt_missing", {"requestId": request_id})
            return None
        if isinstance(record, ProviderPendingReceipt):
            if record.request_digest != provider_request_digest(payload):
                raise ProviderProtocolError("Pending Receipt request digest differs")
            self.record("provider_receipt_pending", {"requestId": request_id})
            return None
        if record.request_digest != provider_request_digest(payload):
            raise ProviderProtocolError("Reconciled Receipt request digest differs")
        self.last_receipt = record
        self.record(
            "provider_receipt_reconciled",
            {"requestId": request_id, "receiptDigest": record.digest, "status": record.status},
        )
        if self.correlation is not None:
            self.correlation.append(
                "provider_receipt_reconciled",
                {
                    "providerRequestId": request_id,
                    "receiptDigest": record.digest,
                    "status": record.status,
                },
            )
        return self._observation(dispatch, record)

    def retrieve_artifact(self) -> tuple[ProviderReceipt, ProviderArtifact, bytes]:
        receipt = self.last_receipt
        if receipt is None or receipt.status != "succeeded" or receipt.artifact is None:
            raise ProviderProtocolError("no succeeded reconciled Receipt is available")
        self.record(
            "provider_artifact_download",
            {"receiptId": receipt.receipt_id, "artifactKey": receipt.artifact.key},
        )
        body = self.client.artifact(receipt.artifact)
        self.record(
            "provider_artifact_verified",
            {
                "artifactKey": receipt.artifact.key,
                "artifactSha256": receipt.artifact.sha256,
                "bytes": len(body),
            },
        )
        return receipt, receipt.artifact, body

    @staticmethod
    def _request(
        dispatch: DispatchEnvelope,
        request: dict[str, JsonValue],
    ) -> tuple[str, dict[str, object]]:
        request_id = request.get("providerRequestId")
        payload = request.get("providerPayload")
        expected = request.get("providerRequestDigest")
        if not isinstance(request_id, str) or request_id != dispatch.idempotency_key:
            raise ProviderProtocolError("Host request and Dispatch Request ID differ")
        if not isinstance(payload, dict):
            raise ProviderProtocolError("Host request omitted provider payload")
        provider_payload = dict(payload)
        if expected != provider_request_digest(provider_payload):
            raise ProviderProtocolError("Host request provider digest differs")
        return request_id, provider_payload

    def _observation(self, dispatch: DispatchEnvelope, receipt: ProviderReceipt) -> ObservationEnvelope:
        evidence: tuple[ArtifactRef, ...] = ()
        if receipt.artifact is not None:
            evidence = (
                ArtifactRef(
                    ref=f"cloudflare-artifact:{receipt.artifact.key}",
                    kind="cloudflare-fetch-artifact",
                    digest=f"sha256:{receipt.artifact.sha256}",
                ),
            )
        return ObservationEnvelope(
            dispatch_id=dispatch.dispatch_id,
            executor_id=self.executor_id,
            status=receipt.status,
            payload_digest=receipt.digest,
            evidence_refs=evidence,
        )
