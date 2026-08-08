#!/usr/bin/env python3
"""Validate structured runtime evidence for LazyDesign evaluation results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCENARIO_WIDTHS = {
    "connection-settings": 420,
    "device-list": 520,
    "failure-confirmation": None,
}
COMMON_CHECKS = {
    "static_review",
    "build",
    "rendered_runtime",
    "light_theme",
    "dark_theme",
    "high_contrast",
    "text_scaling",
    "korean_long_content",
    "english_long_content",
    "keyboard_navigation",
    "focus_visual",
    "narrator",
    "accessibility_insights",
}
SCENARIO_CHECKS = {
    "connection-settings": {
        "content_width",
        "textbox_validation",
        "combobox_popup",
        "toggleswitch_state",
        "save_button_activation",
    },
    "device-list": {
        "content_width",
        "commandbar_overflow",
        "listview_selection",
        "empty_state",
        "remove_command_state",
    },
    "failure-confirmation": {
        "infobar_retry_action",
        "infobar_dismissal",
        "contentdialog_default_action",
        "contentdialog_close_action",
        "focus_return",
    },
}
STATUSES = {"pass", "fail", "not_run"}
PLACEHOLDER_REASONS = {
    "not performed",
    "record why this check was not performed",
}
PARAMETER_KEYS = {
    "content_width_dip",
    "text_scale_percent",
    "languages",
    "contrast_theme",
}


def required_checks(scenario: str) -> set[str]:
    if scenario not in SCENARIO_CHECKS:
        raise ValueError(f"unsupported scenario: {scenario}")
    return COMMON_CHECKS | SCENARIO_CHECKS[scenario]


def verification_template(scenario: str) -> dict[str, Any]:
    checks = {
        check_id: {
            "status": "not_run",
            "evidence": [],
            "reason": "record why this check was not performed",
        }
        for check_id in sorted(required_checks(scenario))
    }
    return {
        "schema_version": 1,
        "scenario": scenario,
        "parameters": {
            "content_width_dip": SCENARIO_WIDTHS[scenario],
            "text_scale_percent": [],
            "languages": [],
            "contrast_theme": "",
        },
        "checks": checks,
    }


def _safe_evidence_path(root: Path, relative: str) -> Path | None:
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        return None
    return candidate


def _validate_evidence_entries(
    check_id: str, entries: Any, evidence_root: Path, errors: list[str]
) -> None:
    if not isinstance(entries, list) or not entries:
        errors.append(f"{check_id}: completed check requires evidence")
        return
    for index, entry in enumerate(entries):
        label = f"{check_id}.evidence[{index}]"
        if not isinstance(entry, dict) or set(entry) != {"path", "detail"}:
            errors.append(f"{label}: must contain exactly path and detail")
            continue
        relative = entry.get("path")
        detail = entry.get("detail")
        if not isinstance(relative, str) or not relative.strip():
            errors.append(f"{label}: path must be a non-empty string")
            continue
        if not isinstance(detail, str) or not detail.strip():
            errors.append(f"{label}: detail must be a non-empty string")
        candidate = _safe_evidence_path(evidence_root, relative)
        if candidate is None:
            errors.append(f"{label}: evidence path escapes evidence directory")
        elif candidate.name.casefold() in {
            "verification.json",
            "verification.template.json",
        }:
            errors.append(f"{label}: evidence cannot be the verification record or template")
        elif not candidate.is_file():
            errors.append(f"{label}: missing evidence file {relative}")


def validate_verification(record: Any, evidence_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["verification record must be an object"]
    if record.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    scenario = record.get("scenario")
    if scenario not in SCENARIO_CHECKS:
        errors.append(f"unsupported scenario: {scenario}")
        return errors

    parameters = record.get("parameters")
    if not isinstance(parameters, dict) or set(parameters) != PARAMETER_KEYS:
        errors.append("parameters must contain the exact required fields")
        parameters = {}
    if parameters.get("content_width_dip") != SCENARIO_WIDTHS[scenario]:
        errors.append(
            f"content_width_dip must be {SCENARIO_WIDTHS[scenario]!r} for {scenario}"
        )
    scales = parameters.get("text_scale_percent")
    if not isinstance(scales, list) or any(
        not isinstance(value, int) or isinstance(value, bool) or value <= 0
        for value in scales
    ):
        errors.append("text_scale_percent must be a list of positive integers")
        scales = []
    languages = parameters.get("languages")
    if not isinstance(languages, list) or any(
        not isinstance(value, str) or not value.strip() for value in languages
    ):
        errors.append("languages must be a list of non-empty strings")
        languages = []
    contrast_theme = parameters.get("contrast_theme")
    if not isinstance(contrast_theme, str):
        errors.append("contrast_theme must be a string")
        contrast_theme = ""

    checks = record.get("checks")
    expected = required_checks(scenario)
    if not isinstance(checks, dict) or set(checks) != expected:
        errors.append("checks must contain the exact required check set")
        checks = checks if isinstance(checks, dict) else {}

    for check_id in sorted(expected & set(checks)):
        check = checks[check_id]
        if not isinstance(check, dict) or set(check) != {"status", "evidence", "reason"}:
            errors.append(
                f"{check_id}: check must contain exactly status, evidence, and reason"
            )
            continue
        status = check.get("status")
        evidence = check.get("evidence")
        reason = check.get("reason")
        if status not in STATUSES:
            errors.append(f"{check_id}: invalid status {status!r}")
            continue
        if not isinstance(reason, str):
            errors.append(f"{check_id}: reason must be a string")
            reason = ""
        if status == "not_run":
            if evidence != []:
                errors.append(f"{check_id}: not_run check must not contain evidence")
            if not reason.strip():
                errors.append(f"{check_id}: not_run check requires a reason")
            elif reason.strip().casefold() in PLACEHOLDER_REASONS:
                errors.append(f"{check_id}: not_run check contains a placeholder reason")
        else:
            _validate_evidence_entries(check_id, evidence, evidence_root, errors)

    if checks.get("text_scaling", {}).get("status") in {"pass", "fail"} and not any(
        value > 100 for value in scales
    ):
        errors.append("text_scaling: completed check requires a scale greater than 100")
    if checks.get("korean_long_content", {}).get("status") in {"pass", "fail"} and "ko-KR" not in languages:
        errors.append("korean_long_content: completed check requires ko-KR")
    if checks.get("english_long_content", {}).get("status") in {"pass", "fail"} and "en-US" not in languages:
        errors.append("english_long_content: completed check requires en-US")
    if checks.get("high_contrast", {}).get("status") in {"pass", "fail"} and not contrast_theme.strip():
        errors.append("high_contrast: completed check requires contrast_theme")
    return errors


def load_and_validate(path: Path) -> list[str]:
    try:
        record = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load verification record: {exc}"]
    return validate_verification(record, path.parent)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("verification", type=Path)
    args = parser.parse_args()
    errors = load_and_validate(args.verification)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("evaluation verification evidence passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
