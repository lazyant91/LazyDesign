#!/usr/bin/env python3
"""Validate the structural contract of the LazyDesign reference."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMPONENTS = (
    "button.md",
    "textbox.md",
    "toggleswitch.md",
    "combobox.md",
    "commandbar.md",
    "listview.md",
    "infobar.md",
    "contentdialog.md",
)

FOUNDATIONS = (
    "text-and-localization.md",
    "sizing-and-spacing.md",
    "icons.md",
    "states-and-themes.md",
    "accessibility-basics.md",
)

COMPONENT_HEADINGS = (
    "## 1. Purpose and characteristic",
    "## 2. Anatomy",
    "## 3. Content rules",
    "## 4. Sizing and layout",
    "## 5. States and interaction",
    "## 6. Theme, accessibility, and localization",
    "## 7. Common failures",
    "## 8. Minimal native XAML",
    "## 9. Verification checklist",
    "## 10. Sources",
)

FORBIDDEN_MARKERS = ("TBD", "TODO", "<RULE-ID>", "<SOURCE-ID>", "<ControlName>")
SOURCE_ID_PATTERN = re.compile(r"`([A-Z][A-Z0-9-]+)`")
RULE_BLOCK_PATTERN = re.compile(
    r"^### (?P<rule_id>[A-Z][A-Z0-9-]+)[ \t]*\r?\n"
    r"(?P<body>.*?)(?=^### |^## |\Z)",
    flags=re.MULTILINE | re.DOTALL,
)
DERIVED_REASONING_PATTERN = re.compile(
    r"^\*\*Derived reasoning:\*\*\s+\S.*$",
    flags=re.MULTILINE,
)


def read_text(path: Path, errors: list[str]) -> str | None:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"invalid UTF-8: {path.relative_to(ROOT)}: {exc}")
        return None


def manifest_source_ids(errors: list[str]) -> set[str]:
    manifest = ROOT / "sources" / "manifest.yaml"
    text = read_text(manifest, errors)
    if text is None:
        return set()
    return set(re.findall(r"^\s*- id:\s*([A-Z][A-Z0-9-]+)\s*$", text, flags=re.MULTILINE))


def check_forbidden(path: Path, text: str, errors: list[str]) -> None:
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            errors.append(f"unresolved marker {marker!r}: {path.relative_to(ROOT)}")


def check_derived_reasoning(path: Path, text: str, errors: list[str]) -> None:
    for match in RULE_BLOCK_PATTERN.finditer(text):
        body = match.group("body")
        if "**Evidence:** derived" not in body:
            continue
        if DERIVED_REASONING_PATTERN.search(body) is None:
            errors.append(
                f"missing derived reasoning for {match.group('rule_id')}: "
                f"{path.relative_to(ROOT)}"
            )


def check_component(path: Path, source_ids: set[str], errors: list[str]) -> None:
    text = read_text(path, errors)
    if text is None:
        return

    check_forbidden(path, text, errors)
    check_derived_reasoning(path, text, errors)

    positions: list[int] = []
    for heading in COMPONENT_HEADINGS:
        position = text.find(heading)
        if position < 0:
            errors.append(f"missing heading {heading!r}: {path.relative_to(ROOT)}")
        else:
            positions.append(position)

    if len(positions) == len(COMPONENT_HEADINGS) and positions != sorted(positions):
        errors.append(f"component headings out of order: {path.relative_to(ROOT)}")

    source_lines = [line for line in text.splitlines() if line.startswith("**Sources:**")]
    if not source_lines:
        errors.append(f"missing **Sources:** rule citation: {path.relative_to(ROOT)}")
        return

    referenced_ids = {
        source_id
        for line in source_lines
        for source_id in SOURCE_ID_PATTERN.findall(line)
    }
    if not referenced_ids:
        errors.append(f"no source IDs found in **Sources:** lines: {path.relative_to(ROOT)}")
        return

    for source_id in sorted(referenced_ids - source_ids):
        errors.append(
            f"unknown source ID {source_id!r}: {path.relative_to(ROOT)}; "
            "add it to sources/manifest.yaml"
        )


def check_foundation(path: Path, source_ids: set[str], errors: list[str]) -> None:
    text = read_text(path, errors)
    if text is None:
        return

    check_forbidden(path, text, errors)
    check_derived_reasoning(path, text, errors)

    source_lines = [line for line in text.splitlines() if line.startswith("**Sources:**")]
    if not source_lines:
        errors.append(f"missing **Sources:** rule citation: {path.relative_to(ROOT)}")
        return

    referenced_ids = {
        source_id
        for line in source_lines
        for source_id in SOURCE_ID_PATTERN.findall(line)
    }
    if not referenced_ids:
        errors.append(f"no source IDs found in **Sources:** lines: {path.relative_to(ROOT)}")
        return

    for source_id in sorted(referenced_ids - source_ids):
        errors.append(
            f"unknown source ID {source_id!r}: {path.relative_to(ROOT)}; "
            "add it to sources/manifest.yaml"
        )


def main() -> int:
    errors: list[str] = []
    source_ids = manifest_source_ids(errors)

    for filename in COMPONENTS:
        check_component(ROOT / "components" / filename, source_ids, errors)

    for filename in FOUNDATIONS:
        check_foundation(ROOT / "foundations" / filename, source_ids, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"reference check failed: {len(errors)} violation(s)")
        return 1

    print("reference check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
