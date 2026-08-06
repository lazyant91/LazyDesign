from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_report import generate_reports, write_reports
from test_evaluation_gate import passing_metrics


ROOT = Path(__file__).resolve().parents[1]


class EvaluationReportTests(unittest.TestCase):
    def test_generate_reports_contains_scores_findings_and_gate(self) -> None:
        metrics = passing_metrics()
        metrics["findings"] = {
            "attributable_improvements": [
                {
                    "summary": "Button labels became concise.",
                    "evidence": ["guided/connection-settings/generated/MainWindow.xaml:1-5"],
                    "rule_ids": ["WINUI-BUTTON-CONTENT-001"],
                }
            ],
            "unchanged_defects": [],
            "regressions": [],
            "ambiguous_decisions": [],
            "ignored_rules": [],
            "unnecessary_output": [],
        }
        reports = generate_reports(ROOT, metrics)
        self.assertIn("Connection settings", reports["scores.md"])
        self.assertIn("Content length and overflow", reports["scores.md"])
        self.assertIn("Button labels became concise", reports["findings.md"])
        self.assertIn("Overall result: **PASS**", reports["gate-decision.md"])

    def test_write_reports_creates_exact_task_11_files(self) -> None:
        metrics = passing_metrics()
        metrics["findings"] = {
            key: []
            for key in (
                "attributable_improvements",
                "unchanged_defects",
                "regressions",
                "ambiguous_decisions",
                "ignored_rules",
                "unnecessary_output",
            )
        }
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            output = Path(temp) / "results"
            result = write_reports(ROOT, metrics, output)
            self.assertEqual("PASS", result["overall"])
            self.assertEqual(
                {"scores.md", "findings.md", "gate-decision.md"},
                {path.name for path in output.iterdir()},
            )

    def test_missing_findings_are_rejected(self) -> None:
        metrics = passing_metrics()
        del metrics["findings"]
        with self.assertRaises(ValueError):
            generate_reports(ROOT, metrics)


if __name__ == "__main__":
    unittest.main()
