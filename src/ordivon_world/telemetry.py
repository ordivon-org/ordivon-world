from __future__ import annotations

from dataclasses import dataclass
import re

_TRACEPARENT = re.compile(r"^[0-9a-f]{2}-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


@dataclass(frozen=True, slots=True)
class TraceContext:
    traceparent: str
    tracestate: str | None = None

    def __post_init__(self) -> None:
        match = _TRACEPARENT.fullmatch(self.traceparent)
        if match is None or match.group(1) == "0" * 32 or match.group(2) == "0" * 16:
            raise ValueError("traceparent is not a valid W3C trace context")
        if self.tracestate is not None:
            if not self.tracestate or len(self.tracestate.encode("utf-8")) > 512:
                raise ValueError("tracestate must be non-empty and at most 512 bytes")
            if any(character in "\r\n\0" for character in self.tracestate):
                raise ValueError("tracestate contains a forbidden character")

    def headers(self) -> dict[str, str]:
        headers = {"traceparent": self.traceparent}
        if self.tracestate is not None:
            headers["tracestate"] = self.tracestate
        return headers

    def to_dict(self) -> dict[str, str | None]:
        return {"traceparent": self.traceparent, "tracestate": self.tracestate}
