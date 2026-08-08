#!/usr/bin/env python3
"""Validate controller-reconciled generation-attempt evidence."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any

VALIDITIES = {"valid", "infrastructure_invalid"}
BLOCKERS = {
    "none",
    "remote_safety_inspection",
    "remote_transport",
    "tool_timeout",
    "other_infrastructure",
}
ATTEMPT_FIELDS = {
    "schema_version",
    "condition",
    "scenario",
    "validity",
    "blocker",
    "stopping_condition_reached",
    "project_delta",
    "evidence",
    "reason",
}
ATTEMPT_RECORD_NAMES = {
    "generation-attempt.json",
    "generation-attempt.template.json",
}


def generation_attempt_template(condition: str, scenario: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "condition": condition,
        "scenario": scenario,
        "validity": "record after generation",
        "blocker": "record after generation",
        "stopping_condition_reached": False,
        "project_delta": {"changed": [], "deleted": []},
        "evidence": [],
        "reason": "record after generation",
    }


def _safe_evidence_path(root: Path, relative: str) -> Path | None:
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        return None
    return candidate


def _validate_relative_paths(label: str, value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    valid: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{label}[{index}] must be a non-empty string")
            continue
        pure = PurePosixPath(item)
        if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != item:
            errors.append(f"{label}[{index}] must be a normalized relative path")
            continue
        valid.append(item)
    if len(valid) != len(set(valid)):
        errors.append(f"{label} must not contain duplicates")
    if valid != sorted(valid, key=lambda item: (item.casefold(), item)):
        errors.append(f"{label} must be sorted")
    return valid


def _validate_evidence(entries: Any, evidence_root: Path, errors: list[str]) -> None:
    if not isinstance(entries, list):
        errors.append("evidence must be a list")
        return
    for index, entry in enumerate(entries):
        label = f"evidence[{index}]"
        if not isinstance(entry, dict) or set(entry) != {"path", "detail"}:
            errors.append(f"{label} must contain exactly path and detail")
            continue
        relative = entry.get("path")
        detail = entry.get("detail")
        if not isinstance(relative, str) or not relative.strip():
            errors.append(f"{label}.path must be a non-empty string")
            continue
        if not isinstance(detail, str) or not detail.strip():
            errors.append(f"{label}.detail must be a non-empty string")
        candidate = _safe_evidence_path(evidence_root, relative)
        if candidate is None:
            errors.append(f"{label}: evidence path escapes evidence directory")
        elif candidate.name.casefold() in ATTEMPT_RECORD_NAMES:
            errors.append(f"{label}: evidence cannot be the generation-attempt record or template")
        elif not candidate.is_file():
            errors.append(f"{label}: missing evidence file {relative}")


def validate_generation_attempt(
    record: Any,
    evidence_root: Path,
    *,
    condition: str,
    scenario: str,
    changed: list[str],
    deleted: list[str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["generation-attempt record must be an object"]
    if set(record) != ATTEMPT_FIELDS:
        errors.append("generation-attempt record must contain the exact required fields")
    if record.get("schema_version") != 1:
        errors.append("generation-attempt schema_version must be 1")
    if record.get("condition") != condition:
        errors.append("generation-attempt condition differs from packet")
    if record.get("scenario") != scenario:
        errors.append("generation-attempt scenario differs from packet")

    validity = record.get("validity")
    blocker = record.get("blocker")
    if validity not in VALIDITIES:
        errors.append(f"invalid generation-attempt validity {validity!r}")
    if blocker not in BLOCKERS:
        errors.append(f"invalid generation-attempt blocker {blocker!r}")
    if validity == "valid" and blocker != "none":
        errors.append("valid attempt requires blocker none")
    if validity == "infrastructure_invalid" and blocker == "none":
        errors.append("infrastructure_invalid attempt requires a concrete blocker")

    stopping = record.get("stopping_condition_reached")
    if not isinstance(stopping, bool):
        errors.append("stopping_condition_reached must be a boolean")

    delta = record.get("project_delta")
    if not isinstance(delta, dict) or set(delta) != {"changed", "deleted"}:
        errors.append("project_delta must contain exactly changed and deleted")
        actual_changed: list[str] = []
        actual_deleted: list[str] = []
    else:
        actual_changed = _validate_relative_paths(
            "project_delta.changed", delta.get("changed"), errors
        )
        actual_deleted = _validate_relative_paths(
            "project_delta.deleted", delta.get("deleted"), errors
        )
    expected_changed = sorted(changed, key=lambda item: (item.casefold(), item))
    expected_deleted = sorted(deleted, key=lambda item: (item.casefold(), item))
    if actual_changed != expected_changed or actual_deleted != expected_deleted:
        errors.append("generation-attempt project_delta differs from controller project delta")

    evidence = record.get("evidence")
    _validate_evidence(evidence, evidence_root, errors)
    if validity == "infrastructure_invalid" and (
        not isinstance(evidence, list) or not evidence
    ):
        errors.append("infrastructure_invalid attempt requires evidence")

    reason = record.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        errors.append("generation-attempt reason must be a non-empty string")
    return errors


def load_and_validate_generation_attempt(
    path: Path,
    *,
    condition: str,
    scenario: str,
    changed: list[str],
    deleted: list[str],
) -> list[str]:
    try:
        record = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load generation-attempt record: {exc}"]
    return validate_generation_attempt(
        record,
        path.parent,
        condition=condition,
        scenario=scenario,
        changed=changed,
        deleted=deleted,
    )
