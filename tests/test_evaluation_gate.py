from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path

from scripts.evaluation_gate import evaluate_gate, render_gate_markdown


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
                    "evidence": [f"{scenario}/generated/MainWindow.xaml:1-5"],
                }
            )
    return {
        "schema_version": 1,
        "scenarios": scenarios,
        "traceable_improvements": traces,
    }


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
