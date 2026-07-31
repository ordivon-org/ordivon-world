from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable


class JournalCorruption(RuntimeError):
    pass


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


@dataclass(frozen=True, slots=True)
class JournalEvent:
    sequence: int
    event_id: str
    event_type: str
    recorded_at_ms: int
    previous_digest: str | None
    payload: dict[str, Any]
    digest: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.w1.experiment-event",
            "sequence": self.sequence,
            "eventId": self.event_id,
            "eventType": self.event_type,
            "recordedAtMs": self.recorded_at_ms,
            "previousDigest": self.previous_digest,
            "payload": self.payload,
            "digest": self.digest,
        }


class HashChainJournal:
    """Small experiment-only append log; never an authoritative World service."""

    def __init__(
        self,
        path: str | Path,
        *,
        clock_ms: Callable[[], int],
        label: str,
    ) -> None:
        if not label or label != label.strip():
            raise ValueError("journal label must be trimmed")
        self.path = Path(path)
        self.clock_ms = clock_ms
        self.label = label
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._events = self._load()

    def events(self) -> tuple[JournalEvent, ...]:
        return tuple(self._events)

    def append(
        self,
        event_type: str,
        payload: dict[str, Any],
        *,
        event_id: str | None = None,
    ) -> JournalEvent:
        if not event_type or event_type != event_type.strip():
            raise ValueError("event type must be trimmed")
        _canonical(payload)
        for existing in self._events:
            if event_id is not None and existing.event_id == event_id:
                if existing.event_type != event_type or existing.payload != payload:
                    raise JournalCorruption("event identity is bound to different content")
                return existing
        sequence = len(self._events) + 1
        identifier = event_id or f"event:{self.label}:{sequence}:{event_type}"
        previous = None if not self._events else self._events[-1].digest
        unsigned = {
            "schemaVersion": 1,
            "kind": "ordivon.world.w1.experiment-event",
            "sequence": sequence,
            "eventId": identifier,
            "eventType": event_type,
            "recordedAtMs": self.clock_ms(),
            "previousDigest": previous,
            "payload": payload,
        }
        event = JournalEvent(
            sequence=sequence,
            event_id=identifier,
            event_type=event_type,
            recorded_at_ms=int(unsigned["recordedAtMs"]),
            previous_digest=previous,
            payload=dict(payload),
            digest=_digest(unsigned),
        )
        line = _canonical(event.to_dict()) + b"\n"
        descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.write(descriptor, line)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        self._events.append(event)
        return event

    def count(self, event_type: str) -> int:
        return sum(event.event_type == event_type for event in self._events)

    def _load(self) -> list[JournalEvent]:
        if not self.path.exists():
            return []
        events: list[JournalEvent] = []
        for line_number, raw in enumerate(self.path.read_bytes().splitlines(), 1):
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as error:
                raise JournalCorruption(f"invalid journal JSON at line {line_number}") from error
            if not isinstance(value, dict) or set(value) != {
                "schemaVersion",
                "kind",
                "sequence",
                "eventId",
                "eventType",
                "recordedAtMs",
                "previousDigest",
                "payload",
                "digest",
            }:
                raise JournalCorruption(f"journal fields differ at line {line_number}")
            if value["schemaVersion"] != 1 or value["kind"] != "ordivon.world.w1.experiment-event":
                raise JournalCorruption(f"journal version differs at line {line_number}")
            if value["sequence"] != line_number:
                raise JournalCorruption(f"journal sequence differs at line {line_number}")
            previous = None if not events else events[-1].digest
            if value["previousDigest"] != previous:
                raise JournalCorruption(f"journal chain differs at line {line_number}")
            unsigned = {key: value[key] for key in value if key != "digest"}
            if value["digest"] != _digest(unsigned):
                raise JournalCorruption(f"journal digest differs at line {line_number}")
            payload = value["payload"]
            if not isinstance(payload, dict):
                raise JournalCorruption(f"journal payload differs at line {line_number}")
            events.append(
                JournalEvent(
                    sequence=line_number,
                    event_id=str(value["eventId"]),
                    event_type=str(value["eventType"]),
                    recorded_at_ms=int(value["recordedAtMs"]),
                    previous_digest=previous,
                    payload=dict(payload),
                    digest=str(value["digest"]),
                )
            )
        return events
