from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_digest


@dataclass(frozen=True, slots=True)
class ResourceEgressAuthority:
    authority_id: str
    mechanism: str
    evidence: dict[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.authority_id, str) or not self.authority_id.strip():
            raise ValueError("Resource Egress authority identity must be non-empty")
        if not isinstance(self.mechanism, str) or not self.mechanism.strip():
            raise ValueError("Resource Egress authority mechanism must be non-empty")
        if not isinstance(self.evidence, dict):
            raise ValueError("Resource Egress authority evidence must be an object")

    def to_dict(self) -> dict[str, Any]:
        return {
            "authorityId": self.authority_id,
            "mechanism": self.mechanism,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ResourceEgressAuthority:
        evidence = value.get("evidence")
        if not isinstance(evidence, dict):
            raise ValueError("Resource Egress authority evidence must be an object")
        return cls(
            authority_id=str(value["authorityId"]),
            mechanism=str(value["mechanism"]),
            evidence=dict(evidence),
        )


@dataclass(frozen=True, slots=True)
class ResourceEgressReceipt:
    """Source-World admission for one exact Resource occurrence and transfer.

    The receipt proves that a source authority admitted the named occurrence for
    the exact transfer/destination/payload tuple. Authenticating the authority
    across an untrusted relay is a separate deployment/trust problem.
    """

    transfer_id: str
    source_world_id: str
    destination_world_id: str
    resource_kind: str
    payload_digest: str
    source_occurrence_id: str
    source_occurrence_digest: str
    authority: ResourceEgressAuthority

    def __post_init__(self) -> None:
        if not self.transfer_id.startswith("transfer:"):
            raise ValueError("Resource Egress transfer identity must start with transfer:")
        for label, value in (
            ("source World identity", self.source_world_id),
            ("destination World identity", self.destination_world_id),
            ("resource kind", self.resource_kind),
            ("source occurrence identity", self.source_occurrence_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        for label, value in (
            ("payload digest", self.payload_digest),
            ("source occurrence digest", self.source_occurrence_digest),
        ):
            if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
                raise ValueError(f"{label} must be a sha256: digest")
        if not isinstance(self.authority, ResourceEgressAuthority):
            raise ValueError("Resource Egress authority must be ResourceEgressAuthority")

    @property
    def digest(self) -> str:
        return sha256_digest(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.resource-egress-receipt",
            "transferId": self.transfer_id,
            "sourceWorldId": self.source_world_id,
            "destinationWorldId": self.destination_world_id,
            "resourceKind": self.resource_kind,
            "payloadDigest": self.payload_digest,
            "sourceOccurrenceId": self.source_occurrence_id,
            "sourceOccurrenceDigest": self.source_occurrence_digest,
            "authority": self.authority.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ResourceEgressReceipt:
        if (
            value.get("schemaVersion") != 1
            or value.get("kind") != "ordivon.world.resource-egress-receipt"
        ):
            raise ValueError("Resource Egress receipt schema is unsupported")
        authority = value.get("authority")
        if not isinstance(authority, dict):
            raise ValueError("Resource Egress authority must be an object")
        return cls(
            transfer_id=str(value["transferId"]),
            source_world_id=str(value["sourceWorldId"]),
            destination_world_id=str(value["destinationWorldId"]),
            resource_kind=str(value["resourceKind"]),
            payload_digest=str(value["payloadDigest"]),
            source_occurrence_id=str(value["sourceOccurrenceId"]),
            source_occurrence_digest=str(value["sourceOccurrenceDigest"]),
            authority=ResourceEgressAuthority.from_dict(authority),
        )
