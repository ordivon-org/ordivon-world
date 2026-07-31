from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from anc_canonical import canonical_digest


def _record(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _exact(value: dict[str, Any], required: set[str], optional: set[str], label: str) -> None:
    fields = set(value)
    if not required <= fields or not fields <= required | optional:
        raise ValueError(f"{label} fields differ")


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{label} must be a non-empty trimmed string")
    return value


def _integer(value: object, label: str, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def _optional_milliseconds_to_microseconds(value: object, label: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative number or null")
    return round(float(value) * 1_000)


@dataclass(frozen=True, slots=True)
class ProviderArtifact:
    key: str
    sha256: str
    bytes: int
    media_type: str
    etag: str | None = None

    @classmethod
    def from_dict(cls, raw: object) -> ProviderArtifact:
        value = _record(raw, "Provider Artifact")
        _exact(value, {"key", "sha256", "bytes", "media_type"}, {"etag"}, "Provider Artifact")
        digest = _string(value["sha256"], "Artifact sha256")
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ValueError("Artifact sha256 must be a lowercase raw SHA-256")
        return cls(
            key=_string(value["key"], "Artifact key"),
            sha256=digest,
            bytes=_integer(value["bytes"], "Artifact bytes"),
            media_type=_string(value["media_type"], "Artifact media type"),
            etag=None if value.get("etag") is None else _string(value["etag"], "Artifact etag"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "key": self.key,
            "sha256": self.sha256,
            "bytes": self.bytes,
            "media_type": self.media_type,
            **({} if self.etag is None else {"etag": self.etag}),
        }


@dataclass(frozen=True, slots=True)
class ProviderExecution:
    policy_version: str
    capability_version: str
    worker_version_id: str
    worker_version_tag: str
    worker_version_timestamp: str
    lease_generation: int

    @classmethod
    def from_dict(cls, raw: object) -> ProviderExecution:
        value = _record(raw, "Provider execution")
        required = {
            "policy_version",
            "capability_version",
            "worker_version_id",
            "worker_version_tag",
            "worker_version_timestamp",
            "lease_generation",
        }
        _exact(value, required, set(), "Provider execution")
        return cls(
            policy_version=_string(value["policy_version"], "policy version"),
            capability_version=_string(value["capability_version"], "capability version"),
            worker_version_id=_string(value["worker_version_id"], "Worker version id"),
            worker_version_tag=_string(value["worker_version_tag"], "Worker version tag"),
            worker_version_timestamp=_string(value["worker_version_timestamp"], "Worker version timestamp"),
            lease_generation=_integer(value["lease_generation"], "lease generation", 1),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "policy_version": self.policy_version,
            "capability_version": self.capability_version,
            "worker_version_id": self.worker_version_id,
            "worker_version_tag": self.worker_version_tag,
            "worker_version_timestamp": self.worker_version_timestamp,
            "lease_generation": self.lease_generation,
        }


@dataclass(frozen=True, slots=True)
class ProviderReceipt:
    receipt_id: str
    request_digest: str
    status: str
    started_at: str
    completed_at: str
    duration_ms: int
    execution: ProviderExecution
    artifact: ProviderArtifact | None
    fetch: dict[str, object] | None
    error_code: str | None = None

    @classmethod
    def from_dict(cls, raw: object) -> ProviderReceipt:
        value = _record(raw, "Provider Receipt")
        required = {
            "schema_version",
            "receipt_id",
            "request_digest",
            "operation",
            "status",
            "started_at",
            "completed_at",
            "duration_ms",
            "execution",
        }
        _exact(value, required, {"artifact", "artifacts", "fetch", "error_code"}, "Provider Receipt")
        if value["schema_version"] != 1 or value["operation"] != "fetch":
            raise ValueError("Receipt is not a W1 Fetch Receipt")
        status = _string(value["status"], "Receipt status")
        if status not in {"succeeded", "failed", "rejected"}:
            raise ValueError("Receipt status is invalid")
        request_digest = _string(value["request_digest"], "Receipt request digest")
        if len(request_digest) != 64 or any(character not in "0123456789abcdef" for character in request_digest):
            raise ValueError("Receipt request digest must be a raw SHA-256")
        artifact = None if value.get("artifact") is None else ProviderArtifact.from_dict(value["artifact"])
        if status == "succeeded" and artifact is None:
            raise ValueError("Succeeded Fetch Receipt omitted its Artifact")
        fetch = None
        if value.get("fetch") is not None:
            fetch_value = _record(value["fetch"], "Fetch details")
            _exact(
                fetch_value,
                {"requested_url", "final_url", "http_status", "redirect_count"},
                set(),
                "Fetch details",
            )
            fetch = {
                "requested_url": _string(fetch_value["requested_url"], "requested URL"),
                "final_url": _string(fetch_value["final_url"], "final URL"),
                "http_status": _integer(fetch_value["http_status"], "HTTP status", 100),
                "redirect_count": _integer(fetch_value["redirect_count"], "redirect count"),
            }
        error_code = None if value.get("error_code") is None else _string(value["error_code"], "error code")
        if status == "succeeded" and error_code is not None:
            raise ValueError("Succeeded Receipt cannot carry an error code")
        if status != "succeeded" and error_code is None:
            raise ValueError("Non-succeeded Receipt requires an error code")
        return cls(
            receipt_id=_string(value["receipt_id"], "Receipt id"),
            request_digest=request_digest,
            status=status,
            started_at=_string(value["started_at"], "Receipt started_at"),
            completed_at=_string(value["completed_at"], "Receipt completed_at"),
            duration_ms=_integer(value["duration_ms"], "Receipt duration"),
            execution=ProviderExecution.from_dict(value["execution"]),
            artifact=artifact,
            fetch=fetch,
            error_code=error_code,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "receipt_id": self.receipt_id,
            "request_digest": self.request_digest,
            "operation": "fetch",
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "execution": self.execution.to_dict(),
            **({} if self.artifact is None else {"artifact": self.artifact.to_dict(), "artifacts": [self.artifact.to_dict()]}),
            **({} if self.fetch is None else {"fetch": dict(self.fetch)}),
            **({} if self.error_code is None else {"error_code": self.error_code}),
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True, slots=True)
class ProviderPendingReceipt:
    receipt_id: str
    request_digest: str
    started_at: str
    lease_expires_at: str
    execution: ProviderExecution

    @classmethod
    def from_dict(cls, raw: object) -> ProviderPendingReceipt:
        value = _record(raw, "Pending Receipt")
        required = {
            "schema_version",
            "receipt_id",
            "request_digest",
            "operation",
            "status",
            "started_at",
            "lease_expires_at",
            "execution",
        }
        _exact(value, required, set(), "Pending Receipt")
        if value["schema_version"] != 1 or value["operation"] != "fetch" or value["status"] != "pending":
            raise ValueError("Receipt is not a pending W1 Fetch")
        return cls(
            receipt_id=_string(value["receipt_id"], "Receipt id"),
            request_digest=_string(value["request_digest"], "request digest"),
            started_at=_string(value["started_at"], "started_at"),
            lease_expires_at=_string(value["lease_expires_at"], "lease_expires_at"),
            execution=ProviderExecution.from_dict(value["execution"]),
        )


@dataclass(frozen=True, slots=True)
class ProbeProjection:
    probe_kind: str
    collection_id: str
    sample_index: int
    target: str
    network: str
    route: str
    protocol: str
    started_at: str
    dns_us: int | None
    connect_us: int | None
    tls_us: int | None
    ttfb_us: int | None
    total_us: int | None
    http_status: int | None
    success: bool
    failure_class: str | None
    termination: str | None

    @classmethod
    def from_source(cls, raw: object) -> ProbeProjection:
        value = _record(raw, "ProbeResult")
        if value.get("schema_version") != 1:
            raise ValueError("ProbeResult schema is unsupported")
        if value.get("target") != "w1-example" or value.get("url") != "https://example.com/":
            raise ValueError("ProbeResult targets another W1 resource")
        if value.get("protocol") != "http_tls":
            raise ValueError("W1 accepts only the HTTP/TLS probe")
        collection_id = _string(value.get("collection_id"), "collection id")
        sample_index = _integer(value.get("sample_index"), "sample index", 1)
        success = value.get("success")
        if not isinstance(success, bool):
            raise ValueError("Probe success must be boolean")
        http_status_value = value.get("http_status")
        http_status = None if http_status_value is None else _integer(http_status_value, "HTTP status", 100)
        return cls(
            probe_kind=_string(value.get("probe_kind"), "probe kind"),
            collection_id=collection_id,
            sample_index=sample_index,
            target="w1-example",
            network=_string(value.get("network"), "network label"),
            route=_string(value.get("route"), "route label"),
            protocol="http_tls",
            started_at=_string(value.get("started_at"), "probe started_at"),
            dns_us=_optional_milliseconds_to_microseconds(value.get("dns_ms"), "dns_ms"),
            connect_us=_optional_milliseconds_to_microseconds(value.get("connect_ms"), "connect_ms"),
            tls_us=_optional_milliseconds_to_microseconds(value.get("tls_ms"), "tls_ms"),
            ttfb_us=_optional_milliseconds_to_microseconds(value.get("ttfb_ms"), "ttfb_ms"),
            total_us=_optional_milliseconds_to_microseconds(value.get("total_ms"), "total_ms"),
            http_status=http_status,
            success=success,
            failure_class=None if value.get("failure_class") is None else _string(value["failure_class"], "failure class"),
            termination=None if value.get("termination") is None else _string(value["termination"], "termination"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.w1.path-observation-projection",
            "probeKind": self.probe_kind,
            "collectionId": self.collection_id,
            "sampleIndex": self.sample_index,
            "target": self.target,
            "network": self.network,
            "route": self.route,
            "protocol": self.protocol,
            "startedAt": self.started_at,
            "dnsUs": self.dns_us,
            "connectUs": self.connect_us,
            "tlsUs": self.tls_us,
            "ttfbUs": self.ttfb_us,
            "totalUs": self.total_us,
            "httpStatus": self.http_status,
            "success": self.success,
            "failureClass": self.failure_class,
            "termination": self.termination,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())
