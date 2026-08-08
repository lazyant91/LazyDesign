from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path

from scripts.evaluation_gate import evaluate_gate, evaluate_gate_v2, render_gate_markdown


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("connection-settings", "device-list", "failure-confirmation")
DEFECTS = (
    "overflow",
    "anatomy",
    "accessibility",
    "control_template",
    "complexity",
    "build_failures",
    "render_failures",
)


def passing_metrics() -> dict:
    scenarios = {}
    traces = []

    def score_evidence(condition: str, scenario: str, scores: list[int]) -> list[dict]:
        return [
            {
                "category": category,
                "score": score,
                "evidence": [f"{condition}/{scenario}/evidence/category-{category}.txt"],
                "uncertainty": "none",
            }
            for category, score in enumerate(scores, start=1)
        ]
    for scenario in SCENARIOS:
        baseline_scores = [1] * 10
        guided_scores = [2] * 6 + [1] * 4
        scenarios[scenario] = {
            "baseline": {
                "scores": baseline_scores,
                "score_evidence": score_evidence("baseline", scenario, baseline_scores),
                "defects": {
                    "overflow": 2,
                    "anatomy": 2,
                    "accessibility": 2,
                    "control_template": 0,
                    "complexity": 1,
                    "build_failures": 0,
                    "render_failures": 0,
                },
            },
            "guided": {
                "scores": guided_scores,
                "score_evidence": score_evidence("guided", scenario, guided_scores),
                "defects": {
                    "overflow": 1,
                    "anatomy": 1,
                    "accessibility": 1,
                    "control_template": 0,
                    "complexity": 1,
                    "build_failures": 0,
                    "render_failures": 0,
                },
            },
        }
        for category in range(1, 7):
            traces.append(
                {
                    "scenario": scenario,
                    "category": category,
                    "rule_ids": ["WINUI-BUTTON-CONTENT-001"],
                    "evidence": [f"guided/{scenario}/generated/MainWindow.xaml:1-5"],
                }
            )
    return {
        "schema_version": 1,
        "scenarios": scenarios,
        "traceable_improvements": traces,
        "findings": {
            key: []
            for key in (
                "attributable_improvements",
                "unchanged_defects",
                "regressions",
                "ambiguous_decisions",
                "ignored_rules",
                "unnecessary_output",
            )
        },
    }


def passing_metrics_v2() -> dict:
    metrics = deepcopy(passing_metrics())
    metrics["schema_version"] = 2
    return metrics


def guided_builds(status: str = "pass") -> dict[str, str]:
    return {scenario: status for scenario in SCENARIOS}


class EvaluationGateTests(unittest.TestCase):
    def test_passing_metrics_pass_all_six_conditions(self) -> None:
        result = evaluate_gate(ROOT, passing_metrics())
        self.assertEqual("PASS", result["overall"])
        self.assertEqual(30, result["baseline_total"])
        self.assertEqual(48, result["guided_total"])
        self.assertEqual(60.0, result["improvement_percent"])
        self.assertEqual(50.0, result["overflow_reduction_percent"])
        self.assertTrue(all(item["status"] == "pass" for item in result["conditions"]))

    def test_zero_overflow_baseline_is_not_demonstrated(self) -> None:
        metrics = passing_metrics()
        for scenario in SCENARIOS:
            metrics["scenarios"][scenario]["baseline"]["defects"]["overflow"] = 0
            metrics["scenarios"][scenario]["guided"]["defects"]["overflow"] = 0
        result = evaluate_gate(ROOT, metrics)
        overflow = next(item for item in result["conditions"] if item["id"] == "overflow-reduction")
        self.assertEqual("fail", overflow["status"])
        self.assertIsNone(result["overflow_reduction_percent"])
        self.assertIn("not demonstrated", overflow["detail"])

    def test_gate_v1_zero_overflow_behavior_is_unchanged(self) -> None:
        metrics = passing_metrics()
        for scenario in SCENARIOS:
            metrics["scenarios"][scenario]["baseline"]["defects"]["overflow"] = 0
            metrics["scenarios"][scenario]["guided"]["defects"]["overflow"] = 0
        result = evaluate_gate(ROOT, metrics)
        overflow = next(
            item for item in result["conditions"] if item["id"] == "overflow-reduction"
        )
        self.assertEqual("fail", overflow["status"])
        self.assertIsNone(result["overflow_reduction_percent"])

    def test_gate_v2_zero_overflow_non_regression_passes(self) -> None:
        metrics = passing_metrics_v2()
        for scenario in SCENARIOS:
            metrics["scenarios"][scenario]["baseline"]["defects"]["overflow"] = 0
            metrics["scenarios"][scenario]["guided"]["defects"]["overflow"] = 0
        result = evaluate_gate_v2(ROOT, metrics, guided_builds())
        overflow = next(
            item for item in result["conditions"] if item["id"] == "overflow-non-regression"
        )
        self.assertEqual("pass", overflow["status"])
        self.assertEqual("non-regression", result["overflow_mode"])
        self.assertIsNone(result["overflow_reduction_percent"])

    def test_gate_v2_zero_baseline_overflow_regression_fails(self) -> None:
        metrics = passing_metrics_v2()
        for scenario in SCENARIOS:
            metrics["scenarios"][scenario]["baseline"]["defects"]["overflow"] = 0
            metrics["scenarios"][scenario]["guided"]["defects"]["overflow"] = 0
        metrics["scenarios"]["device-list"]["guided"]["defects"]["overflow"] = 1
        result = evaluate_gate_v2(ROOT, metrics, guided_builds())
        overflow = next(
            item for item in result["conditions"] if item["id"] == "overflow-non-regression"
        )
        self.assertEqual("fail", overflow["status"])

    def test_gate_v2_positive_overflow_baseline_still_requires_half_reduction(self) -> None:
        metrics = passing_metrics_v2()
        for scenario in SCENARIOS:
            metrics["scenarios"][scenario]["baseline"]["defects"]["overflow"] = 0
            metrics["scenarios"][scenario]["guided"]["defects"]["overflow"] = 0
        metrics["scenarios"]["device-list"]["baseline"]["defects"]["overflow"] = 4
        metrics["scenarios"]["device-list"]["guided"]["defects"]["overflow"] = 3
        result = evaluate_gate_v2(ROOT, metrics, guided_builds())
        overflow = next(
            item for item in result["conditions"] if item["id"] == "overflow-reduction"
        )
        self.assertEqual("fail", overflow["status"])
        metrics["scenarios"]["device-list"]["guided"]["defects"]["overflow"] = 2
        result = evaluate_gate_v2(ROOT, metrics, guided_builds())
        overflow = next(
            item for item in result["conditions"] if item["id"] == "overflow-reduction"
        )
        self.assertEqual("pass", overflow["status"])

    def test_gate_v2_requires_all_guided_builds_to_pass(self) -> None:
        metrics = passing_metrics_v2()
        statuses = guided_builds()
        statuses["device-list"] = "fail"
        result = evaluate_gate_v2(ROOT, metrics, statuses)
        self.assertEqual("FAIL", result["overall"])
        self.assertEqual("fail", result["guided_build_prerequisite"]["status"])

    def test_gate_v2_not_run_guided_build_fails_prerequisite(self) -> None:
        metrics = passing_metrics_v2()
        statuses = guided_builds()
        statuses["failure-confirmation"] = "not_run"
        result = evaluate_gate_v2(ROOT, metrics, statuses)
        self.assertEqual("FAIL", result["overall"])

    def test_gate_v2_markdown_reports_build_prerequisite_and_non_regression(self) -> None:
        metrics = passing_metrics_v2()
        for scenario in SCENARIOS:
            metrics["scenarios"][scenario]["baseline"]["defects"]["overflow"] = 0
            metrics["scenarios"][scenario]["guided"]["defects"]["overflow"] = 0
        markdown = render_gate_markdown(
            evaluate_gate_v2(ROOT, metrics, guided_builds())
        )
        self.assertIn("## Guided build prerequisite", markdown)
        self.assertIn("Overflow mode | non-regression", markdown)
        self.assertIn("Overflow reduction | not measurable", markdown)
        self.assertIn(
            "guided build prerequisite and all six quality conditions pass",
            markdown,
        )

    def test_each_positive_score_change_requires_rule_trace(self) -> None:
        metrics = passing_metrics()
        metrics["traceable_improvements"].pop()
        result = evaluate_gate(ROOT, metrics)
        traceability = next(item for item in result["conditions"] if item["id"] == "rule-traceability")
        self.assertEqual("fail", traceability["status"])
        self.assertIn("failure-confirmation category 6", traceability["detail"])

    def test_missing_score_evidence_is_rejected(self) -> None:
        metrics = passing_metrics()
        for scenario in SCENARIOS:
            for condition in ("baseline", "guided"):
                scores = metrics["scenarios"][scenario][condition]["scores"]
                metrics["scenarios"][scenario][condition]["score_evidence"] = [
                    {
                        "category": category,
                        "score": score,
                        "evidence": [f"{condition}/{scenario}/evidence/category-{category}.txt"],
                        "uncertainty": "none",
                    }
                    for category, score in enumerate(scores, start=1)
                ]
        del metrics["scenarios"]["device-list"]["guided"]["score_evidence"]
        with self.assertRaises(ValueError):
            evaluate_gate(ROOT, metrics)

    def test_non_object_metrics_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_gate(ROOT, [])

    def test_invalid_score_is_rejected(self) -> None:
        metrics = passing_metrics()
        metrics["scenarios"]["device-list"]["guided"]["scores"][0] = 3
        with self.assertRaises(ValueError):
            evaluate_gate(ROOT, metrics)

    def test_markdown_contains_mechanical_decision(self) -> None:
        markdown = render_gate_markdown(evaluate_gate(ROOT, passing_metrics()))
        self.assertIn("Overall result: **PASS**", markdown)
        self.assertIn("[pass] Guided total improved by at least 20%", markdown)
        self.assertIn("Baseline total | 30 / 60", markdown)


if __name__ == "__main__":
    unittest.main()
