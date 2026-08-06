#!/usr/bin/env python3
"""Calculate the LazyDesign v0.1 quality gate from scored evaluation metrics."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCENARIOS = ("connection-settings", "device-list", "failure-confirmation")
CONDITIONS = ("baseline", "guided")
DEFECT_KEYS = (
    "overflow",
    "anatomy",
    "accessibility",
    "control_template",
    "complexity",
    "build_failures",
    "render_failures",
)
CONDITION_LABELS = {
    "score-improvement": "Guided total improved by at least 20%",
    "overflow-reduction": "Clipping/content-overflow defects decreased by at least 50%",
    "anatomy-accessibility": "Missing anatomy and accessibility requirements decreased",
    "template-nonincrease": "Unnecessary ControlTemplate replacement did not increase",
    "complexity-nonincrease": "Irrelevant XAML or complexity did not materially increase",
    "rule-traceability": "Improvements are traceable to specific reference rules",
}
RULE_PATTERN = re.compile(r"^### ([A-Z][A-Z0-9-]+)\s*$", flags=re.MULTILINE)


def _known_rule_ids(repo_root: Path) -> set[str]:
    rule_ids: set[str] = set()
    for directory in (repo_root / "components", repo_root / "foundations"):
        for path in directory.glob("*.md"):
            rule_ids.update(RULE_PATTERN.findall(path.read_text(encoding="utf-8-sig")))
    return rule_ids


def _is_nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _validate_metrics(repo_root: Path, metrics: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if metrics.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    scenarios = metrics.get("scenarios")
    if not isinstance(scenarios, dict) or set(scenarios) != set(SCENARIOS):
        errors.append("scenarios must contain exactly the three fixed scenarios")
        scenarios = {}
    for scenario in SCENARIOS:
        scenario_data = scenarios.get(scenario, {})
        if not isinstance(scenario_data, dict) or set(scenario_data) != set(CONDITIONS):
            errors.append(f"{scenario} must contain baseline and guided")
            continue
        for condition in CONDITIONS:
            result = scenario_data.get(condition, {})
            if not isinstance(result, dict) or set(result) != {
                "scores",
                "score_evidence",
                "defects",
            }:
                errors.append(
                    f"{scenario}/{condition} must contain exactly scores, score_evidence, and defects"
                )
                result = result if isinstance(result, dict) else {}
            scores = result.get("scores")
            if not isinstance(scores, list) or len(scores) != 10:
                errors.append(f"{scenario}/{condition} scores must contain 10 values")
            elif any(
                not isinstance(score, int)
                or isinstance(score, bool)
                or score < 0
                or score > 2
                for score in scores
            ):
                errors.append(f"{scenario}/{condition} scores must be integers from 0 to 2")
            score_evidence = result.get("score_evidence")
            if not isinstance(score_evidence, list) or len(score_evidence) != 10:
                errors.append(
                    f"{scenario}/{condition} score_evidence must contain 10 entries"
                )
            else:
                categories: list[int] = []
                for index, entry in enumerate(score_evidence):
                    label = f"{scenario}/{condition} score_evidence[{index}]"
                    if not isinstance(entry, dict) or set(entry) != {
                        "category",
                        "score",
                        "evidence",
                        "uncertainty",
                    }:
                        errors.append(
                            f"{label} must contain exactly category, score, evidence, and uncertainty"
                        )
                        continue
                    category = entry.get("category")
                    score = entry.get("score")
                    if (
                        not isinstance(category, int)
                        or isinstance(category, bool)
                        or not 1 <= category <= 10
                    ):
                        errors.append(f"{label} category must be an integer from 1 to 10")
                    else:
                        categories.append(category)
                        if (
                            isinstance(scores, list)
                            and len(scores) == 10
                            and score != scores[category - 1]
                        ):
                            errors.append(f"{label} score differs from scores[{category - 1}]")
                    if (
                        not isinstance(score, int)
                        or isinstance(score, bool)
                        or score < 0
                        or score > 2
                    ):
                        errors.append(f"{label} score must be an integer from 0 to 2")
                    evidence = entry.get("evidence")
                    if not isinstance(evidence, list) or not evidence or any(
                        not isinstance(item, str) or not item.strip() for item in evidence
                    ):
                        errors.append(f"{label} must contain one or more evidence entries")
                    uncertainty = entry.get("uncertainty")
                    if not isinstance(uncertainty, str) or not uncertainty.strip():
                        errors.append(f"{label} uncertainty must be a non-empty string")
                if sorted(categories) != list(range(1, 11)):
                    errors.append(
                        f"{scenario}/{condition} score_evidence categories must be exactly 1 through 10"
                    )
            defects = result.get("defects")
            if not isinstance(defects, dict) or set(defects) != set(DEFECT_KEYS):
                errors.append(
                    f"{scenario}/{condition} defects must contain exactly {', '.join(DEFECT_KEYS)}"
                )
            elif any(not _is_nonnegative_int(defects[key]) for key in DEFECT_KEYS):
                errors.append(f"{scenario}/{condition} defect counts must be nonnegative integers")

    known_rules = _known_rule_ids(repo_root)
    traces = metrics.get("traceable_improvements")
    if not isinstance(traces, list):
        errors.append("traceable_improvements must be a list")
        traces = []
    for index, trace in enumerate(traces):
        label = f"traceable_improvements[{index}]"
        if not isinstance(trace, dict):
            errors.append(f"{label} must be an object")
            continue
        if trace.get("scenario") not in SCENARIOS:
            errors.append(f"{label} has an invalid scenario")
        category = trace.get("category")
        if not isinstance(category, int) or isinstance(category, bool) or not 1 <= category <= 10:
            errors.append(f"{label} category must be an integer from 1 to 10")
        rule_ids = trace.get("rule_ids")
        if not isinstance(rule_ids, list) or not rule_ids or any(
            not isinstance(rule_id, str) or not rule_id for rule_id in rule_ids
        ):
            errors.append(f"{label} must contain one or more rule_ids")
        else:
            for rule_id in rule_ids:
                if rule_id not in known_rules:
                    errors.append(f"{label} references unknown rule ID {rule_id}")
        evidence = trace.get("evidence")
        if not isinstance(evidence, list) or not evidence or any(
            not isinstance(item, str) or not item.strip() for item in evidence
        ):
            errors.append(f"{label} must contain one or more evidence entries")
    return errors


def _aggregate_defects(metrics: dict[str, Any], condition: str) -> dict[str, int]:
    return {
        key: sum(
            metrics["scenarios"][scenario][condition]["defects"][key]
            for scenario in SCENARIOS
        )
        for key in DEFECT_KEYS
    }


def _condition(condition_id: str, passed: bool, detail: str) -> dict[str, str]:
    return {
        "id": condition_id,
        "status": "pass" if passed else "fail",
        "label": CONDITION_LABELS[condition_id],
        "detail": detail,
    }


def evaluate_gate(repo_root: Path, metrics: dict[str, Any]) -> dict[str, Any]:
    errors = _validate_metrics(repo_root, metrics)
    if errors:
        raise ValueError("invalid gate metrics: " + "; ".join(errors))

    baseline_total = sum(
        sum(metrics["scenarios"][scenario]["baseline"]["scores"])
        for scenario in SCENARIOS
    )
    guided_total = sum(
        sum(metrics["scenarios"][scenario]["guided"]["scores"])
        for scenario in SCENARIOS
    )
    baseline_defects = _aggregate_defects(metrics, "baseline")
    guided_defects = _aggregate_defects(metrics, "guided")
    conditions: list[dict[str, str]] = []

    if baseline_total == 0:
        improvement_percent = None
        conditions.append(
            _condition(
                "score-improvement",
                False,
                "not demonstrated because the baseline total is zero",
            )
        )
    else:
        improvement_percent = round(
            ((guided_total - baseline_total) / baseline_total) * 100, 2
        )
        passed = (guided_total - baseline_total) * 100 >= baseline_total * 20
        conditions.append(
            _condition(
                "score-improvement",
                passed,
                f"baseline {baseline_total}, guided {guided_total}, improvement {improvement_percent}%",
            )
        )

    baseline_overflow = baseline_defects["overflow"]
    guided_overflow = guided_defects["overflow"]
    if baseline_overflow == 0:
        overflow_reduction_percent = None
        conditions.append(
            _condition(
                "overflow-reduction",
                False,
                "not demonstrated because the baseline overflow count is zero",
            )
        )
    else:
        overflow_reduction_percent = round(
            ((baseline_overflow - guided_overflow) / baseline_overflow) * 100, 2
        )
        passed = (baseline_overflow - guided_overflow) * 100 >= baseline_overflow * 50
        conditions.append(
            _condition(
                "overflow-reduction",
                passed,
                f"baseline {baseline_overflow}, guided {guided_overflow}, reduction {overflow_reduction_percent}%",
            )
        )

    anatomy_passed = guided_defects["anatomy"] < baseline_defects["anatomy"]
    accessibility_passed = (
        guided_defects["accessibility"] < baseline_defects["accessibility"]
    )
    conditions.append(
        _condition(
            "anatomy-accessibility",
            anatomy_passed and accessibility_passed,
            "anatomy "
            f"{baseline_defects['anatomy']} to {guided_defects['anatomy']}; "
            "accessibility "
            f"{baseline_defects['accessibility']} to {guided_defects['accessibility']}",
        )
    )

    conditions.append(
        _condition(
            "template-nonincrease",
            guided_defects["control_template"] <= baseline_defects["control_template"],
            "ControlTemplate defects "
            f"{baseline_defects['control_template']} to {guided_defects['control_template']}",
        )
    )
    conditions.append(
        _condition(
            "complexity-nonincrease",
            guided_defects["complexity"] <= baseline_defects["complexity"],
            "complexity defects "
            f"{baseline_defects['complexity']} to {guided_defects['complexity']}",
        )
    )

    positive_changes = {
        (scenario, category)
        for scenario in SCENARIOS
        for category, (baseline, guided) in enumerate(
            zip(
                metrics["scenarios"][scenario]["baseline"]["scores"],
                metrics["scenarios"][scenario]["guided"]["scores"],
            ),
            start=1,
        )
        if guided > baseline
    }
    covered_changes = {
        (trace["scenario"], trace["category"])
        for trace in metrics["traceable_improvements"]
    }
    missing_changes = sorted(positive_changes - covered_changes)
    if not positive_changes:
        trace_detail = "no positive category changes were recorded"
        trace_passed = False
    elif missing_changes:
        trace_detail = "missing traces for " + ", ".join(
            f"{scenario} category {category}"
            for scenario, category in missing_changes
        )
        trace_passed = False
    else:
        trace_detail = f"all {len(positive_changes)} positive category changes have rule IDs and evidence"
        trace_passed = True
    conditions.append(
        _condition("rule-traceability", trace_passed, trace_detail)
    )

    overall = "PASS" if all(item["status"] == "pass" for item in conditions) else "FAIL"
    return {
        "schema_version": 1,
        "overall": overall,
        "baseline_total": baseline_total,
        "guided_total": guided_total,
        "improvement_percent": improvement_percent,
        "overflow_reduction_percent": overflow_reduction_percent,
        "baseline_defects": baseline_defects,
        "guided_defects": guided_defects,
        "conditions": conditions,
    }


def render_gate_markdown(result: dict[str, Any]) -> str:
    improvement = (
        "not demonstrated"
        if result["improvement_percent"] is None
        else f"{result['improvement_percent']}%"
    )
    overflow = (
        "not demonstrated"
        if result["overflow_reduction_percent"] is None
        else f"{result['overflow_reduction_percent']}%"
    )
    lines = [
        "# LazyDesign v0.1 Gate Decision",
        "",
        f"Overall result: **{result['overall']}**",
        "",
        "## Totals",
        "",
        "| Metric | Result |",
        "|---|---:|",
        f"| Baseline total | {result['baseline_total']} / 60 |",
        f"| Guided total | {result['guided_total']} / 60 |",
        f"| Score improvement | {improvement} |",
        f"| Overflow reduction | {overflow} |",
        "",
        "## Mechanical conditions",
        "",
    ]
    for item in result["conditions"]:
        lines.append(
            f"- [{item['status']}] {item['label']}. {item['detail']}."
        )
    lines.extend(
        [
            "",
            "The overall result is PASS only when all six conditions pass.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    try:
        metrics = json.loads(args.metrics.read_text(encoding="utf-8-sig"))
        result = evaluate_gate(repo_root, metrics)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    markdown = render_gate_markdown(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0 if result["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
