#!/usr/bin/env python3
"""Generate Task 11 score, findings, and gate reports from one metrics file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from scripts.evaluation_gate import (
        CONDITIONS,
        DEFECT_KEYS,
        FINDING_SECTIONS,
        SCENARIOS,
        evaluate_gate,
        render_gate_markdown,
    )
except ModuleNotFoundError:
    from evaluation_gate import (
        CONDITIONS,
        DEFECT_KEYS,
        FINDING_SECTIONS,
        SCENARIOS,
        evaluate_gate,
        render_gate_markdown,
    )

try:
    from scripts.evaluation_harness import validate_results
except ModuleNotFoundError:
    from evaluation_harness import validate_results

CATEGORY_LABELS = (
    "Content length and overflow",
    "Information hierarchy",
    "Component anatomy",
    "Native interaction states",
    "Accessibility basics",
    "Localization and scaling resilience",
    "Native WinUI style preservation",
    "Component-specific characteristics",
    "Label, helper, and explanation separation",
    "XAML simplicity and relevance",
)
SCENARIO_LABELS = {
    "connection-settings": "Connection settings",
    "device-list": "Device list",
    "failure-confirmation": "Failure and confirmation",
}
DEFECT_LABELS = {
    "overflow": "Clipping or content overflow",
    "anatomy": "Missing component anatomy",
    "accessibility": "Missing accessibility requirements",
    "control_template": "Unnecessary ControlTemplate replacements",
    "complexity": "Irrelevant XAML or complexity",
    "build_failures": "Build failures",
    "render_failures": "Rendered verification failures",
}
FINDING_LABELS = {
    "attributable_improvements": "Improvements attributable to reference rules",
    "unchanged_defects": "Unchanged defects",
    "regressions": "Regressions introduced by guidance",
    "ambiguous_decisions": "Ambiguous rubric decisions",
    "ignored_rules": "Rules the model ignored",
    "unnecessary_output": "Rules or guidance that caused unnecessary output",
}


def _parse_evidence_reference(reference: str) -> tuple[PurePosixPath, int | None, int | None]:
    path_text = reference
    start: int | None = None
    end: int | None = None
    head, separator, tail = reference.rpartition(":")
    if separator:
        pieces = tail.split("-", maxsplit=1)
        if all(piece.isdigit() for piece in pieces):
            path_text = head
            start = int(pieces[0])
            end = int(pieces[-1])
    path = PurePosixPath(path_text)
    return path, start, end


def _validate_reference(
    evaluation_root: Path,
    reference: str,
    label: str,
    expected_prefix: tuple[str, str] | None,
) -> list[str]:
    errors: list[str] = []
    path, start, end = _parse_evidence_reference(reference)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        return [f"{label}: evidence path must remain inside the evaluation directory"]
    if expected_prefix and path.parts[:2] != expected_prefix:
        errors.append(
            f"{label}: evidence must reference {expected_prefix[0]}/{expected_prefix[1]}"
        )
    if path.parts[0] not in CONDITIONS or len(path.parts) < 3 or path.parts[1] not in SCENARIOS:
        errors.append(f"{label}: evidence must reference a baseline or guided scenario result")
    target = evaluation_root.joinpath(*path.parts).resolve()
    if not target.is_relative_to(evaluation_root.resolve()):
        errors.append(f"{label}: evidence path escapes the evaluation directory")
        return errors
    if not target.is_file():
        errors.append(f"{label}: missing evidence file {path.as_posix()}")
        return errors
    if start is not None:
        if start < 1 or end is None or end < start:
            errors.append(f"{label}: invalid line range in {reference}")
        else:
            try:
                line_count = len(target.read_text(encoding="utf-8-sig").splitlines())
            except UnicodeDecodeError:
                errors.append(f"{label}: line range requires a UTF-8 text file")
            else:
                if end > line_count:
                    errors.append(
                        f"{label}: line range {start}-{end} exceeds {path.as_posix()} ({line_count} lines)"
                    )
    return errors


def validate_metric_evidence(evaluation_root: Path, metrics: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for scenario in SCENARIOS:
        for condition in CONDITIONS:
            entries = metrics["scenarios"][scenario][condition]["score_evidence"]
            for entry in entries:
                for reference in entry["evidence"]:
                    errors.extend(
                        _validate_reference(
                            evaluation_root,
                            reference,
                            f"{condition}/{scenario} category {entry['category']}",
                            (condition, scenario),
                        )
                    )
    for index, trace in enumerate(metrics["traceable_improvements"]):
        for reference in trace["evidence"]:
            errors.extend(
                _validate_reference(
                    evaluation_root,
                    reference,
                    f"traceable_improvements[{index}]",
                    ("guided", trace["scenario"]),
                )
            )
    for section in FINDING_SECTIONS:
        for index, finding in enumerate(metrics["findings"][section]):
            for reference in finding["evidence"]:
                errors.extend(
                    _validate_reference(
                        evaluation_root,
                        reference,
                        f"findings.{section}[{index}]",
                        None,
                    )
                )
    return errors


def _cell(value: Any) -> str:
    if isinstance(value, list):
        value = "<br>".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def render_scores_markdown(metrics: dict[str, Any], gate: dict[str, Any]) -> str:
    lines = [
        "# LazyDesign v0.1 Scores",
        "",
        "## Scenario totals",
        "",
        "| Scenario | Baseline | Guided | Delta |",
        "|---|---:|---:|---:|",
    ]
    for scenario in SCENARIOS:
        baseline = sum(metrics["scenarios"][scenario]["baseline"]["scores"])
        guided = sum(metrics["scenarios"][scenario]["guided"]["scores"])
        lines.append(
            f"| {SCENARIO_LABELS[scenario]} | {baseline} / 20 | {guided} / 20 | {guided - baseline:+d} |"
        )
    lines.extend(
        [
            f"| **Total** | **{gate['baseline_total']} / 60** | **{gate['guided_total']} / 60** | **{gate['guided_total'] - gate['baseline_total']:+d}** |",
            "",
        ]
    )

    for scenario in SCENARIOS:
        data = metrics["scenarios"][scenario]
        baseline_evidence = {
            item["category"]: item for item in data["baseline"]["score_evidence"]
        }
        guided_evidence = {
            item["category"]: item for item in data["guided"]["score_evidence"]
        }
        lines.extend(
            [
                f"## {SCENARIO_LABELS[scenario]}",
                "",
                "| # | Category | Baseline | Guided | Baseline evidence | Guided evidence | Baseline uncertainty | Guided uncertainty |",
                "|---:|---|---:|---:|---|---|---|---|",
            ]
        )
        for category, label in enumerate(CATEGORY_LABELS, start=1):
            baseline = baseline_evidence[category]
            guided = guided_evidence[category]
            lines.append(
                "| "
                f"{category} | {label} | {baseline['score']} | {guided['score']} | "
                f"{_cell(baseline['evidence'])} | {_cell(guided['evidence'])} | "
                f"{_cell(baseline['uncertainty'])} | {_cell(guided['uncertainty'])} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Defect counts",
            "",
            "| Scenario | Defect | Baseline | Guided |",
            "|---|---|---:|---:|",
        ]
    )
    for scenario in SCENARIOS:
        for defect in DEFECT_KEYS:
            lines.append(
                f"| {SCENARIO_LABELS[scenario]} | {DEFECT_LABELS[defect]} | "
                f"{metrics['scenarios'][scenario]['baseline']['defects'][defect]} | "
                f"{metrics['scenarios'][scenario]['guided']['defects'][defect]} |"
            )
    lines.extend(
        [
            "",
            "## Traceable improvements",
            "",
        ]
    )
    traces = metrics["traceable_improvements"]
    if not traces:
        lines.append("None recorded.")
    else:
        lines.extend(
            [
                "| Scenario | Category | Rule IDs | Evidence |",
                "|---|---:|---|---|",
            ]
        )
        for trace in traces:
            rules = ", ".join(f"`{rule_id}`" for rule_id in trace["rule_ids"])
            lines.append(
                f"| {SCENARIO_LABELS[trace['scenario']]} | {trace['category']} | "
                f"{rules} | {_cell(trace['evidence'])} |"
            )
    lines.append("")
    return "\n".join(lines)


def render_findings_markdown(metrics: dict[str, Any]) -> str:
    lines = ["# LazyDesign v0.1 Findings", ""]
    for section in FINDING_SECTIONS:
        lines.extend([f"## {FINDING_LABELS[section]}", ""])
        items = metrics["findings"][section]
        if not items:
            lines.extend(["None recorded.", ""])
            continue
        for item in items:
            lines.append(f"- {item['summary']}")
            if item["rule_ids"]:
                rules = ", ".join(f"`{rule_id}`" for rule_id in item["rule_ids"])
                lines.append(f"  - Rules: {rules}")
            else:
                lines.append("  - Rules: none")
            lines.append(f"  - Evidence: {_cell(item['evidence'])}")
        lines.append("")
    return "\n".join(lines)


def generate_reports(repo_root: Path, metrics: dict[str, Any]) -> dict[str, str]:
    gate = evaluate_gate(repo_root, metrics)
    return {
        "scores.md": render_scores_markdown(metrics, gate),
        "findings.md": render_findings_markdown(metrics),
        "gate-decision.md": render_gate_markdown(gate),
    }


def write_reports(
    repo_root: Path,
    metrics: dict[str, Any],
    output_dir: Path,
    require_complete_results: bool = True,
) -> dict[str, Any]:
    resolved = output_dir.resolve()
    if not resolved.is_relative_to(repo_root.resolve()):
        raise ValueError("report output directory must remain inside the repository workspace")
    evaluation_root = resolved.parent
    reports = generate_reports(repo_root, metrics)
    if require_complete_results:
        result_errors = validate_results(repo_root, evaluation_root)
        if result_errors:
            raise ValueError("invalid evaluation results: " + "; ".join(result_errors))
    evidence_errors = validate_metric_evidence(evaluation_root, metrics)
    if evidence_errors:
        raise ValueError("invalid metric evidence: " + "; ".join(evidence_errors))
    resolved.mkdir(parents=True, exist_ok=True)
    for filename, content in reports.items():
        (resolved / filename).write_text(content, encoding="utf-8")
    return evaluate_gate(repo_root, metrics)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    try:
        metrics = json.loads(args.metrics.read_text(encoding="utf-8-sig"))
        result = write_reports(repo_root, metrics, args.output_dir)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0 if result["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
