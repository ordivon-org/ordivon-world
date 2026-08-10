from __future__ import annotations

import base64
from dataclasses import dataclass
import datetime as dt
import hashlib
import hmac
import http.client
import json
from pathlib import Path
import time
from typing import Any, Protocol
import urllib.error
import urllib.parse
import urllib.request
import uuid

from ordivon_host import ArtifactRef, DispatchEnvelope, ObservationEnvelope, StateRef

from .browser import BrowserArtifactBundle, RetrievedArtifact
from .canonical import canonical_bytes, sha256_digest, sha256_hex
from .schemas import validate_contract
from .telemetry import TraceContext

DEFAULT_CONFIG = Path("/root/.config/ordivon/secrets/edge-client.json")
_EXECUTOR_ID = "world.cloudflare"


class WorldAdapterError(RuntimeError):
    pass


class WorldProviderError(WorldAdapterError):
    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class WorldBindingStale(WorldAdapterError):
    pass


class TransportError(WorldAdapterError):
    pass


@dataclass(frozen=True, slots=True)
class CloudflareConfig:
    endpoint: str
    key_id: str
    secret: bytes

    @classmethod
    def load(cls, path: Path = DEFAULT_CONFIG) -> CloudflareConfig:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as error:
            raise WorldAdapterError(
                f"Cloudflare client configuration does not exist: {path}"
            ) from error
        except (OSError, json.JSONDecodeError) as error:
            raise WorldAdapterError(
                f"cannot read Cloudflare client configuration: {path}"
            ) from error
        if not isinstance(raw, dict):
            raise WorldAdapterError("Cloudflare client configuration must be an object")
        endpoint = raw.get("endpoint")
        key_id = raw.get("key_id")
        secret_text = raw.get("secret")
        if not all(
            isinstance(item, str) and item
            for item in (endpoint, key_id, secret_text)
        ):
            raise WorldAdapterError("Cloudflare client configuration is incomplete")
        try:
            secret = base64.urlsafe_b64decode(
                secret_text + "=" * (-len(secret_text) % 4)
            )
        except ValueError as error:
            raise WorldAdapterError(
                "Cloudflare client secret is not valid base64url"
            ) from error
        if len(secret) < 32:
            raise WorldAdapterError("Cloudflare client secret is too short")
        return cls(endpoint=endpoint.rstrip("/"), key_id=key_id, secret=secret)


@dataclass(frozen=True, slots=True)
class HttpResponse:
    status: int
    headers: dict[str, str]
    body: bytes


class CloudflareTransport(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        body: bytes = b"",
        request_id: str,
        extra_headers: dict[str, str] | None = None,
    ) -> HttpResponse: ...


class SignedHttpTransport:
    def __init__(
        self,
        config: CloudflareConfig,
        *,
        attempts: int = 3,
        timeout_seconds: float = 30.0,
        sleep: Any = time.sleep,
    ) -> None:
        if attempts < 1 or timeout_seconds <= 0:
            raise ValueError("transport attempts and timeout must be positive")
        self.config = config
        self.attempts = attempts
        self.timeout_seconds = timeout_seconds
        self.sleep = sleep

    def request(
        self,
        method: str,
        path: str,
        *,
        body: bytes = b"",
        request_id: str,
        extra_headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        url = f"{self.config.endpoint}{path}"
        last_error: BaseException | None = None
        for attempt in range(1, self.attempts + 1):
            headers = self._signed_headers(method, url, body, request_id)
            headers["Accept"] = "application/json"
            if body:
                headers["Content-Type"] = "application/json"
            if extra_headers:
                headers.update(extra_headers)
            invocation = urllib.request.Request(
                url,
                data=body if method.upper() not in {"GET", "HEAD"} else None,
                method=method.upper(),
                headers=headers,
            )
            try:
                with urllib.request.urlopen(
                    invocation, timeout=self.timeout_seconds
                ) as response:
                    return HttpResponse(
                        status=response.status,
                        headers={
                            key.lower(): value
                            for key, value in response.headers.items()
                        },
                        body=response.read(),
                    )
            except urllib.error.HTTPError as error:
                return HttpResponse(
                    status=error.code,
                    headers={
                        key.lower(): value for key, value in error.headers.items()
                    },
                    body=error.read(),
                )
            except (
                urllib.error.URLError,
                http.client.HTTPException,
                ConnectionError,
                TimeoutError,
            ) as error:
                last_error = error
                if attempt < self.attempts:
                    self.sleep(0.25 * (2 ** (attempt - 1)))
        detail = (
            getattr(last_error, "reason", None)
            or str(last_error)
            or "transport failure"
        )
        raise TransportError(
            f"Cloudflare request failed after {self.attempts} attempts: {detail}"
        )

    def _signed_headers(
        self,
        method: str,
        url: str,
        body: bytes,
        request_id: str,
    ) -> dict[str, str]:
        timestamp = int(time.time())
        parsed = urllib.parse.urlsplit(url)
        target = urllib.parse.urlunsplit(
            ("", "", parsed.path or "/", parsed.query, "")
        )
        body_digest = sha256_hex(body)
        canonical = "\n".join(
            [
                "ordivon-edge-v1",
                method.upper(),
                target,
                request_id,
                str(timestamp),
                body_digest,
            ]
        )
        signature = base64.urlsafe_b64encode(
            hmac.new(
                self.config.secret,
                canonical.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        ).rstrip(b"=").decode("ascii")
        return {
            "Authorization": f"Ordivon-HMAC {self.config.key_id}:{signature}",
            "X-Ordivon-Request-Id": request_id,
            "X-Ordivon-Timestamp": str(timestamp),
            "User-Agent": "ordivon-world/0.1",
        }


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    provider: str
    captured_at: str
    raw: dict[str, Any]
    condition_digest: str
    observation_digest: str

    @classmethod
    def from_document(
        cls,
        value: dict[str, Any],
        captured_at: str,
    ) -> CapabilitySnapshot:
        validate_contract("edge-capabilities", value)
        condition = {
            "provider": "cloudflare",
            "policyVersion": value["policy_version"],
            "retention": value["retention"],
            "capabilities": value["capabilities"],
            "workerVersion": value["worker_version"],
            "deploymentIdentity": value["deployment_identity"],
        }
        observation = {**condition, "capturedAt": captured_at}
        return cls(
            provider="cloudflare",
            captured_at=captured_at,
            raw=value,
            condition_digest=sha256_digest(condition),
            observation_digest=sha256_digest(observation),
        )

    def capability_version(self, operation: str) -> str:
        for capability in self.raw["capabilities"]:
            if capability["id"] == operation:
                return str(capability["version"])
        raise WorldBindingStale(f"Cloudflare capability is unavailable: {operation}")


@dataclass(frozen=True, slots=True)
class PreparedWorldDispatch:
    operation: str
    path: str
    provider_request_id: str
    provider_request_digest: str
    request: dict[str, Any]
    request_body: bytes
    capability_condition_digest: str
    capability_version: str
    dispatch: DispatchEnvelope
    trace_context: TraceContext | None = None

    def to_dict(self) -> dict[str, Any]:
        value = {
            "schemaVersion": 1,
            "kind": "ordivon.world-prepared-dispatch",
            "operation": self.operation,
            "path": self.path,
            "providerRequestId": self.provider_request_id,
            "providerRequestDigest": self.provider_request_digest,
            "request": self.request,
            "capabilityConditionDigest": self.capability_condition_digest,
            "capabilityVersion": self.capability_version,
            "dispatch": self.dispatch.to_dict(),
        }
        if self.trace_context is not None:
            value["traceContext"] = self.trace_context.to_dict()
        validate_contract("world-prepared-dispatch", value)
        return value

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PreparedWorldDispatch:
        validate_contract("world-prepared-dispatch", value)
        trace = value.get("traceContext")
        context = (
            None
            if trace is None
            else TraceContext(trace["traceparent"], trace["tracestate"])
        )
        request = value["request"]
        body = canonical_bytes(request)
        return cls(
            operation=value["operation"],
            path=value["path"],
            provider_request_id=value["providerRequestId"],
            provider_request_digest=value["providerRequestDigest"],
            request=request,
            request_body=body,
            capability_condition_digest=value["capabilityConditionDigest"],
            capability_version=value["capabilityVersion"],
            dispatch=DispatchEnvelope.from_dict(value["dispatch"]),
            trace_context=context,
        )


@dataclass(frozen=True, slots=True)
class WorldObservation:
    envelope: ObservationEnvelope
    receipt: dict[str, Any]
    reconciled: bool
    replayed: bool
    available_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = {
            "schemaVersion": 1,
            "kind": "ordivon.world-cloudflare-observation",
            "envelope": self.envelope.to_dict(),
            "receipt": self.receipt,
            "reconciled": self.reconciled,
            "replayed": self.replayed,
        }
        if self.available_at is not None:
            value["availableAt"] = self.available_at
        validate_contract("world-observation", value)
        return value

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> WorldObservation:
        validate_contract("world-observation", value)
        return cls(
            envelope=ObservationEnvelope.from_dict(value["envelope"]),
            receipt=value["receipt"],
            reconciled=bool(value["reconciled"]),
            replayed=bool(value["replayed"]),
            available_at=(
                str(value["availableAt"])
                if value.get("availableAt") is not None
                else None
            ),
        )


@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    found: bool
    pending: bool
    observation: WorldObservation | None


class WorldOutcomeUnknown(WorldAdapterError):
    def __init__(
        self,
        prepared: PreparedWorldDispatch,
        cause: BaseException,
    ) -> None:
        super().__init__(
            "Cloudflare outcome is unknown for "
            f"{prepared.provider_request_id}; reconcile before redispatch"
        )
        self.prepared = prepared
        self.__cause__ = cause


class CloudflareWorldAdapter:
    def __init__(self, transport: CloudflareTransport) -> None:
        self.transport = transport

    @classmethod
    def from_config(
        cls,
        path: Path = DEFAULT_CONFIG,
        *,
        attempts: int = 3,
    ) -> CloudflareWorldAdapter:
        return cls(
            SignedHttpTransport(CloudflareConfig.load(path), attempts=attempts)
        )

    def capabilities(self) -> CapabilitySnapshot:
        request_id = "observe_" + uuid.uuid4().hex[:40]
        response = self.transport.request(
            "GET",
            "/v1/capabilities",
            request_id=request_id,
        )
        value = self._json_object(response, "Cloudflare capabilities")
        if not 200 <= response.status < 300:
            raise WorldProviderError(
                "Cloudflare capabilities request failed",
                status=response.status,
            )
        captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return CapabilitySnapshot.from_document(value, captured_at)

    def prepare_fetch(
        self,
        *,
        dispatch_id: str,
        effect_id: str,
        url: str,
        capability: CapabilitySnapshot,
        maximum_bytes: int = 262_144,
        timeout_ms: int = 15_000,
        accept: str = "*/*",
        required_state_refs: tuple[StateRef, ...] = (),
    ) -> PreparedWorldDispatch:
        request = {
            "accept": accept,
            "maximum_bytes": maximum_bytes,
            "timeout_ms": timeout_ms,
            "url": url,
        }
        validate_contract("fetch-request", request)
        return self._prepare(
            operation="fetch",
            path="/v1/fetch",
            dispatch_id=dispatch_id,
            effect_id=effect_id,
            request=request,
            capability=capability,
            required_state_refs=required_state_refs,
        )

    def prepare_browser(
        self,
        *,
        dispatch_id: str,
        effect_id: str,
        url: str,
        capability: CapabilitySnapshot,
        viewport_width: int = 1365,
        viewport_height: int = 768,
        full_page: bool = False,
        wait_until: str = "domcontentloaded",
        timeout_ms: int = 15_000,
        wait_after_ms: int = 0,
        required_state_refs: tuple[StateRef, ...] = (),
    ) -> PreparedWorldDispatch:
        request = {
            "full_page": full_page,
            "timeout_ms": timeout_ms,
            "url": url,
            "viewport_height": viewport_height,
            "viewport_width": viewport_width,
            "wait_after_ms": wait_after_ms,
            "wait_until": wait_until,
        }
        validate_contract("browser-request", request)
        return self._prepare(
            operation="browser.run",
            path="/v1/browser/run",
            dispatch_id=dispatch_id,
            effect_id=effect_id,
            request=request,
            capability=capability,
            required_state_refs=required_state_refs,
        )

    def _prepare(
        self,
        *,
        operation: str,
        path: str,
        dispatch_id: str,
        effect_id: str,
        request: dict[str, Any],
        capability: CapabilitySnapshot,
        required_state_refs: tuple[StateRef, ...],
    ) -> PreparedWorldDispatch:
        body = canonical_bytes(request)
        request_digest = sha256_digest(body)
        material = canonical_bytes(
            {
                "dispatchId": dispatch_id,
                "effectId": effect_id,
                "operation": operation,
                "requestDigest": request_digest,
            }
        )
        provider_request_id = (
            "world_" + hashlib.sha256(material).hexdigest()[:58]
        )
        provider_request_digest = self._provider_request_digest(path, body)
        capability_version = capability.capability_version(operation)
        state_refs = (
            StateRef(
                ref=f"world:cloudflare:capability:{operation}",
                digest=capability.condition_digest,
            ),
            *required_state_refs,
        )
        dispatch = DispatchEnvelope(
            dispatch_id=dispatch_id,
            effect_id=effect_id,
            executor_id=_EXECUTOR_ID,
            request_digest=request_digest,
            idempotency_key=provider_request_id,
            required_state_refs=state_refs,
            expected_observation_kind="ordivon.world-cloudflare-observation",
        )
        return PreparedWorldDispatch(
            operation=operation,
            path=path,
            provider_request_id=provider_request_id,
            provider_request_digest=provider_request_digest,
            request=request,
            request_body=body,
            capability_condition_digest=capability.condition_digest,
            capability_version=capability_version,
            dispatch=dispatch,
            trace_context=None,
        )

    def deliver(
        self,
        prepared: PreparedWorldDispatch,
        *,
        check_conditions: bool = True,
    ) -> WorldObservation:
        if check_conditions:
            current = self.capabilities()
            if current.condition_digest != prepared.capability_condition_digest:
                raise WorldBindingStale(
                    "Cloudflare capability condition changed before dispatch"
                )
        headers = {"x-ordivon-dispatch-id": prepared.dispatch.dispatch_id}
        try:
            response = self.transport.request(
                "POST",
                prepared.path,
                body=prepared.request_body,
                request_id=prepared.provider_request_id,
                extra_headers=headers,
            )
        except TransportError as error:
            raise WorldOutcomeUnknown(prepared, error) from error
        value = self._json_object(response, "Cloudflare operation")
        receipt = value.get("receipt")
        if not isinstance(receipt, dict):
            detail = (
                value.get("error")
                if isinstance(value.get("error"), str)
                else "provider response has no receipt"
            )
            raise WorldProviderError(str(detail), status=response.status)
        replayed = value.get("replayed") is True
        return self._observation(
            prepared,
            receipt,
            reconciled=False,
            replayed=replayed,
        )

    def reconcile(
        self,
        prepared: PreparedWorldDispatch,
    ) -> ReconciliationResult:
        response = self.transport.request(
            "GET",
            f"/v1/receipts/{prepared.provider_request_id}",
            request_id="observe_" + uuid.uuid4().hex[:40],
            extra_headers={},
        )
        if response.status == 404:
            return ReconciliationResult(
                found=False,
                pending=False,
                observation=None,
            )
        receipt = self._json_object(response, "Cloudflare receipt")
        observation = self._observation(
            prepared,
            receipt,
            reconciled=True,
            replayed=False,
        )
        return ReconciliationResult(
            found=True,
            pending=receipt.get("status") == "pending",
            observation=observation,
        )

    def read_artifact(self, reference: ArtifactRef) -> bytes:
        return self.read_artifact_record(reference).body

    def read_artifact_record(self, reference: ArtifactRef) -> RetrievedArtifact:
        if not reference.ref.startswith("cloudflare-r2:"):
            raise WorldAdapterError(
                "ArtifactRef is not a Cloudflare R2 reference"
            )
        key = reference.ref.removeprefix("cloudflare-r2:")
        path = "/v1/artifacts/" + "/".join(
            urllib.parse.quote(segment, safe="") for segment in key.split("/")
        )
        response = self.transport.request(
            "GET",
            path,
            request_id="observe_" + uuid.uuid4().hex[:40],
        )
        if response.status != 200:
            raise WorldProviderError(
                "Cloudflare Artifact read failed",
                status=response.status,
            )
        expected = reference.digest.removeprefix("sha256:")
        observed = sha256_hex(response.body)
        header = response.headers.get("x-ordivon-sha256")
        if header != expected or observed != expected:
            raise WorldProviderError("Cloudflare Artifact digest differs")
        media_type = response.headers.get("x-ordivon-media-type")
        if media_type is None or media_type != reference.kind:
            raise WorldProviderError("Cloudflare Artifact media type differs")
        if response.headers.get("content-type") != "application/octet-stream":
            raise WorldProviderError("Cloudflare Artifact download type differs")
        length_text = response.headers.get("content-length")
        try:
            content_length = int(length_text) if length_text is not None else -1
        except ValueError as error:
            raise WorldProviderError(
                "Cloudflare Artifact content length is invalid"
            ) from error
        if content_length != len(response.body):
            raise WorldProviderError("Cloudflare Artifact content length differs")
        return RetrievedArtifact(
            reference=reference,
            body=response.body,
            media_type=media_type,
            content_length=content_length,
            etag=response.headers.get("etag"),
        )

    def read_browser_bundle(
        self,
        observation: WorldObservation,
    ) -> BrowserArtifactBundle:
        return BrowserArtifactBundle.retrieve(self, observation)

    def _observation(
        self,
        prepared: PreparedWorldDispatch,
        receipt: dict[str, Any],
        *,
        reconciled: bool,
        replayed: bool,
    ) -> WorldObservation:
        validate_contract("edge-receipt", receipt)
        if receipt["receipt_id"] != prepared.provider_request_id:
            raise WorldProviderError("Cloudflare Receipt identity differs")
        if receipt["request_digest"] != prepared.provider_request_digest:
            raise WorldProviderError(
                "Cloudflare Receipt request digest differs"
            )
        if receipt["operation"] != prepared.operation:
            raise WorldProviderError("Cloudflare Receipt operation differs")
        execution = receipt["execution"]
        if execution["capability_version"] != prepared.capability_version:
            raise WorldProviderError(
                "Cloudflare Receipt capability version differs"
            )
        references = tuple(
            ArtifactRef(
                ref="cloudflare-r2:" + item["key"],
                kind=item["media_type"],
                digest="sha256:" + item["sha256"],
            )
            for item in receipt.get("artifacts", [])
        )
        envelope = ObservationEnvelope(
            dispatch_id=prepared.dispatch.dispatch_id,
            executor_id=_EXECUTOR_ID,
            status=receipt["status"],
            payload_digest=sha256_digest(receipt),
            evidence_refs=references,
        )
        return WorldObservation(
            envelope=envelope,
            receipt=receipt,
            reconciled=reconciled,
            replayed=replayed,
            available_at=dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z"),
        )

    @staticmethod
    def _provider_request_digest(path: str, body: bytes) -> str:
        value = "\n".join(
            [
                "ordivon-edge-idempotency-v1",
                "POST",
                path,
                sha256_hex(body),
            ]
        )
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _json_object(
        response: HttpResponse,
        label: str,
    ) -> dict[str, Any]:
        try:
            value = json.loads(response.body)
        except json.JSONDecodeError as error:
            raise WorldProviderError(
                f"{label} returned non-JSON",
                status=response.status,
            ) from error
        if not isinstance(value, dict):
            raise WorldProviderError(
                f"{label} returned a non-object",
                status=response.status,
            )
        return value
