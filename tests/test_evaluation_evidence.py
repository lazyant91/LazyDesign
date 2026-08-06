from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_evidence import (
    required_checks,
    validate_verification,
    verification_template,
)


ROOT = Path(__file__).resolve().parents[1]


def completed_record(scenario: str, evidence_root: Path) -> dict:
    record = verification_template(scenario)
    for check_id, check in record["checks"].items():
        path = evidence_root / f"{check_id}.txt"
        path.write_text(f"observed {check_id}\n", encoding="utf-8")
        check.update(
            {
                "status": "pass",
                "evidence": [{"path": path.name, "detail": f"verified {check_id}"}],
                "reason": "",
            }
        )
    return record


class EvaluationEvidenceTests(unittest.TestCase):
    def test_valid_complete_connection_record(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            record = completed_record("connection-settings", evidence_root)
            record["parameters"].update(
                {
                    "content_width_dip": 420,
                    "text_scale_percent": [100, 150],
                    "languages": ["ko-KR", "en-US"],
                    "contrast_theme": "Desert",
                }
            )
            self.assertEqual([], validate_verification(record, evidence_root))

    def test_template_requires_concrete_not_run_reasons(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            record = verification_template("device-list")
            errors = validate_verification(record, Path(temp))
            self.assertTrue(any("placeholder reason" in error for error in errors))

    def test_not_run_requires_reason(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            record = verification_template("device-list")
            record["checks"]["narrator"]["reason"] = ""
            errors = validate_verification(record, evidence_root)
            self.assertTrue(any("narrator" in error and "reason" in error for error in errors))

    def test_completed_check_requires_existing_evidence_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            record = verification_template("failure-confirmation")
            record["checks"]["contentdialog_close_action"] = {
                "status": "pass",
                "evidence": [{"path": "missing.txt", "detail": "Escape closed dialog"}],
                "reason": "",
            }
            errors = validate_verification(record, evidence_root)
            self.assertTrue(any("missing evidence file" in error for error in errors))

    def test_verification_record_cannot_be_its_own_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            verification = evidence_root / "verification.json"
            verification.write_text("{}\n", encoding="utf-8")
            record = verification_template("failure-confirmation")
            record["checks"]["contentdialog_close_action"] = {
                "status": "pass",
                "evidence": [{"path": verification.name, "detail": "self reference"}],
                "reason": "",
            }
            errors = validate_verification(record, evidence_root)
            self.assertTrue(any("cannot be the verification record" in error for error in errors))

    def test_content_width_must_match_scenario(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            record = verification_template("connection-settings")
            record["parameters"]["content_width_dip"] = 520
            errors = validate_verification(record, evidence_root)
            self.assertTrue(any("content_width_dip" in error for error in errors))

    def test_scenario_specific_checks_are_exact(self) -> None:
        record = verification_template("device-list")
        self.assertEqual(required_checks("device-list"), set(record["checks"]))
        record["checks"]["combobox_popup"] = {
            "status": "not_run",
            "evidence": [],
            "reason": "not applicable",
        }
        errors = validate_verification(record, ROOT / "evaluation")
        self.assertTrue(any("exact required check set" in error for error in errors))

    def test_text_scaling_pass_requires_scaled_value(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            record = verification_template("connection-settings")
            path = evidence_root / "scaling.txt"
            path.write_text("100 percent only\n", encoding="utf-8")
            record["checks"]["text_scaling"] = {
                "status": "pass",
                "evidence": [{"path": path.name, "detail": "checked default scale"}],
                "reason": "",
            }
            record["parameters"]["text_scale_percent"] = [100]
            errors = validate_verification(record, evidence_root)
            self.assertTrue(any("greater than 100" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
