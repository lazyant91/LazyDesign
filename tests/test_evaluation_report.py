from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_report import generate_reports, write_reports
from test_evaluation_gate import passing_metrics, passing_metrics_v2


ROOT = Path(__file__).resolve().parents[1]


def _reference_path(reference: str) -> str:
    head, separator, tail = reference.rpartition(":")
    if separator and tail.replace("-", "").isdigit():
        return head
    return reference


def materialize_evidence(root: Path, metrics: dict) -> None:
    references: set[str] = set()
    for scenario in metrics["scenarios"].values():
        for result in scenario.values():
            for item in result["score_evidence"]:
                references.update(item["evidence"])
    for trace in metrics["traceable_improvements"]:
        references.update(trace["evidence"])
    for items in metrics["findings"].values():
        for item in items:
            references.update(item["evidence"])
    for reference in references:
        path = root / _reference_path(reference)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("line 1\nline 2\nline 3\nline 4\nline 5\n", encoding="utf-8")


def materialize_guided_build_verifications(
    root: Path,
    statuses: dict[str, str],
) -> None:
    for scenario, status in statuses.items():
        path = root / "guided" / scenario / "evidence" / "verification.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "checks": {
                        "build": {
                            "status": status,
                            "evidence": (
                                []
                                if status == "not_run"
                                else [{"path": "build.txt", "detail": "test"}]
                            ),
                            "reason": "not run" if status == "not_run" else "",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )


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
            evaluation_root = Path(temp)
            materialize_evidence(evaluation_root, metrics)
            output = evaluation_root / "results"
            result = write_reports(
                ROOT, metrics, output, require_complete_results=False
            )
            self.assertEqual("PASS", result["overall"])
            self.assertEqual(
                {"scores.md", "findings.md", "gate-decision.md"},
                {path.name for path in output.iterdir()},
            )

    def test_v2_report_uses_immutable_guided_build_statuses(self) -> None:
        metrics = passing_metrics_v2()
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evaluation_root = Path(temp)
            materialize_evidence(evaluation_root, metrics)
            materialize_guided_build_verifications(
                evaluation_root,
                {
                    scenario: "pass"
                    for scenario in (
                        "connection-settings",
                        "device-list",
                        "failure-confirmation",
                    )
                },
            )
            result = write_reports(
                ROOT,
                metrics,
                evaluation_root / "results",
                require_complete_results=False,
            )
            self.assertEqual(
                "pass", result["guided_build_prerequisite"]["status"]
            )

    def test_v2_report_rejects_build_failure_count_that_disagrees_with_verification(self) -> None:
        metrics = passing_metrics_v2()
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evaluation_root = Path(temp)
            materialize_evidence(evaluation_root, metrics)
            materialize_guided_build_verifications(
                evaluation_root,
                {
                    "connection-settings": "pass",
                    "device-list": "fail",
                    "failure-confirmation": "pass",
                },
            )
            with self.assertRaisesRegex(ValueError, "build_failures"):
                write_reports(
                    ROOT,
                    metrics,
                    evaluation_root / "results",
                    require_complete_results=False,
                )

    def test_write_reports_rejects_missing_score_evidence_file(self) -> None:
        metrics = passing_metrics()
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evaluation_root = Path(temp)
            materialize_evidence(evaluation_root, metrics)
            missing = evaluation_root / "guided/device-list/evidence/category-1.txt"
            missing.unlink()
            with self.assertRaises(ValueError):
                write_reports(
                    ROOT,
                    metrics,
                    evaluation_root / "results",
                    require_complete_results=False,
                )

    def test_write_reports_rejects_cross_scenario_score_evidence(self) -> None:
        metrics = passing_metrics()
        metrics["scenarios"]["device-list"]["guided"]["score_evidence"][0][
            "evidence"
        ] = ["guided/connection-settings/evidence/category-1.txt"]
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evaluation_root = Path(temp)
            materialize_evidence(evaluation_root, metrics)
            with self.assertRaises(ValueError):
                write_reports(
                    ROOT,
                    metrics,
                    evaluation_root / "results",
                    require_complete_results=False,
                )

    def test_write_reports_rejects_out_of_range_line_evidence(self) -> None:
        metrics = passing_metrics()
        metrics["scenarios"]["device-list"]["guided"]["score_evidence"][0][
            "evidence"
        ] = ["guided/device-list/evidence/category-1.txt:1-99"]
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evaluation_root = Path(temp)
            materialize_evidence(evaluation_root, metrics)
            with self.assertRaises(ValueError):
                write_reports(
                    ROOT,
                    metrics,
                    evaluation_root / "results",
                    require_complete_results=False,
                )

    def test_write_reports_requires_complete_captured_results_by_default(self) -> None:
        metrics = passing_metrics()
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evaluation_root = Path(temp)
            materialize_evidence(evaluation_root, metrics)
            with self.assertRaises(ValueError):
                write_reports(ROOT, metrics, evaluation_root / "results")
            self.assertFalse((evaluation_root / "results").exists())

    def test_missing_findings_are_rejected(self) -> None:
        metrics = passing_metrics()
        del metrics["findings"]
        with self.assertRaises(ValueError):
            generate_reports(ROOT, metrics)


if __name__ == "__main__":
    unittest.main()
