#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "README.md",
    "ARCHITECTURE.md",
    "STATUS.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "docs/authority.md",
    "docs/compatibility.md",
    "docs/contracts.md",
    "docs/data-and-privacy.md",
    "docs/operations.md",
    "docs/retained-boundaries.md",
    "docs/verification.md",
)
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


class DocumentationError(RuntimeError):
    pass


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
        and ".venv" not in path.parts
        and "node_modules" not in path.parts
        and "target" not in path.parts
    )


def main() -> int:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        raise DocumentationError(f"required documentation is missing: {missing}")
    broken: list[str] = []
    checked = 0
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        if "\t" in text:
            raise DocumentationError(f"tab character in Markdown: {path.relative_to(ROOT)}")
        for target in LINK.findall(text):
            target = target.strip()
            if (
                not target
                or target.startswith(("http://", "https://", "mailto:", "#"))
            ):
                continue
            location = target.split("#", 1)[0]
            if not location:
                continue
            resolved = (path.parent / location).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                broken.append(f"{path.relative_to(ROOT)} -> {target} (escapes repository)")
                continue
            checked += 1
            if not resolved.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    if broken:
        raise DocumentationError("broken local documentation links:\n" + "\n".join(broken))
    print(
        json.dumps(
            {
                "ok": True,
                "required": len(REQUIRED),
                "markdownFiles": len(markdown_files()),
                "localLinks": checked,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
