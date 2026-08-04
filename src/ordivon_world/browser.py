from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Protocol

from ordivon_host import ArtifactRef

from .schemas import validate_contract

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class BrowserBundleError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class RetrievedArtifact:
    reference: ArtifactRef
    body: bytes
    media_type: str
    content_length: int
    etag: str | None = None


class ArtifactReader(Protocol):
    def read_artifact_record(self, reference: ArtifactRef) -> RetrievedArtifact: ...


class BrowserObservation(Protocol):
    receipt: dict[str, Any]
    envelope: Any


@dataclass(frozen=True, slots=True)
class BrowserArtifactBundle:
    receipt_id: str
    execution: dict[str, Any]
    browser: dict[str, Any]
    manifest_document: dict[str, Any]
    screenshot: RetrievedArtifact
    content: RetrievedArtifact
    manifest: RetrievedArtifact

    @property
    def artifacts(self) -> tuple[RetrievedArtifact, ...]:
        return (self.screenshot, self.content, self.manifest)

    @classmethod
    def retrieve(
        cls,
        reader: ArtifactReader,
        observation: BrowserObservation,
    ) -> BrowserArtifactBundle:
        receipt = observation.receipt
        validate_contract("edge-receipt", receipt)
        if receipt.get("operation") != "browser.run":
            raise BrowserBundleError("Receipt is not a Browser operation")
        if receipt.get("status") != "succeeded":
            raise BrowserBundleError("Browser bundle requires a succeeded Receipt")

        receipt_id = str(receipt["receipt_id"])
        execution = receipt["execution"]
        browser = receipt["browser"]
        generation = execution["lease_generation"]
        base = f"browser/v2/{receipt_id}/g{generation}"
        expected_keys = {
            "screenshot": f"{base}/screenshot.png",
            "content": f"{base}/content.html",
            "manifest": f"{base}/manifest.json",
        }

        raw_artifacts = receipt["artifacts"]
        if len(raw_artifacts) != 3:
            raise BrowserBundleError("Browser Receipt must contain exactly three Artifacts")
        by_key = {item["key"]: item for item in raw_artifacts}
        if len(by_key) != 3 or set(by_key) != set(expected_keys.values()):
            raise BrowserBundleError("Browser Receipt Artifact keys or generation differ")
        primary = receipt["artifact"]
        if _artifact_value(primary) != _artifact_value(by_key[expected_keys["manifest"]]):
            raise BrowserBundleError("Browser Receipt primary Artifact is not its Manifest")

        references = tuple(observation.envelope.evidence_refs)
        refs_by_key = {
            reference.ref.removeprefix("cloudflare-r2:"): reference
            for reference in references
            if reference.ref.startswith("cloudflare-r2:")
        }
        if len(refs_by_key) != 3 or set(refs_by_key) != set(expected_keys.values()):
            raise BrowserBundleError("Host Observation does not retain the full Browser bundle")

        retrieved: dict[str, RetrievedArtifact] = {}
        for role, key in expected_keys.items():
            provider = by_key[key]
            reference = refs_by_key[key]
            if reference.digest != "sha256:" + provider["sha256"]:
                raise BrowserBundleError(f"{role} Host digest differs from the Receipt")
            if reference.kind != provider["media_type"]:
                raise BrowserBundleError(f"{role} Host media type differs from the Receipt")
            artifact = reader.read_artifact_record(reference)
            if artifact.content_length != provider["bytes"]:
                raise BrowserBundleError(f"{role} byte count differs from the Receipt")
            retrieved[role] = artifact

        screenshot = retrieved["screenshot"]
        content = retrieved["content"]
        manifest = retrieved["manifest"]
        if screenshot.media_type != "image/png" or not screenshot.body.startswith(
            _PNG_SIGNATURE
        ):
            raise BrowserBundleError("Browser screenshot is not a PNG document")
        if content.media_type != "text/html; charset=utf-8":
            raise BrowserBundleError("Browser content media type differs")
        try:
            content.body.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            raise BrowserBundleError("Browser content is not valid UTF-8") from error
        if manifest.media_type != "application/json; charset=utf-8":
            raise BrowserBundleError("Browser Manifest media type differs")
        try:
            manifest_value = json.loads(manifest.body.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise BrowserBundleError("Browser Manifest is not valid UTF-8 JSON") from error
        if not isinstance(manifest_value, dict):
            raise BrowserBundleError("Browser Manifest is not an object")
        validate_contract("browser-manifest", manifest_value)
        if manifest_value["receipt_id"] != receipt_id:
            raise BrowserBundleError("Browser Manifest Receipt identity differs")
        if manifest_value["execution"] != execution:
            raise BrowserBundleError("Browser Manifest execution identity differs")
        if manifest_value["browser"] != browser:
            raise BrowserBundleError("Browser Manifest page details differ")
        expected_manifest_artifacts = [
            _artifact_value(by_key[expected_keys["screenshot"]]),
            _artifact_value(by_key[expected_keys["content"]]),
        ]
        observed_manifest_artifacts = [
            _artifact_value(item) for item in manifest_value["artifacts"]
        ]
        if observed_manifest_artifacts != expected_manifest_artifacts:
            raise BrowserBundleError("Browser Manifest Artifact set differs from the Receipt")

        return cls(
            receipt_id=receipt_id,
            execution=execution,
            browser=browser,
            manifest_document=manifest_value,
            screenshot=screenshot,
            content=content,
            manifest=manifest,
        )


def _artifact_value(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": value["key"],
        "sha256": value["sha256"],
        "bytes": value["bytes"],
        "media_type": value["media_type"],
        **({"etag": value["etag"]} if "etag" in value else {}),
    }
