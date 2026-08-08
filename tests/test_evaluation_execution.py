from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_execution import validate_generation_attempt


ROOT = Path(__file__).resolve().parents[1]


def attempt_record(
    *,
    condition: str = "guided",
    scenario: str = "device-list",
    validity: str = "valid",
    blocker: str = "none",
    stopping_condition_reached: bool = True,
    changed: list[str] | None = None,
    deleted: list[str] | None = None,
    evidence: list[dict[str, str]] | None = None,
    reason: str = "controller observed no infrastructure interruption",
) -> dict:
    return {
        "schema_version": 1,
        "condition": condition,
        "scenario": scenario,
        "validity": validity,
        "blocker": blocker,
        "stopping_condition_reached": stopping_condition_reached,
        "project_delta": {
            "changed": changed or [],
            "deleted": deleted or [],
        },
        "evidence": evidence or [],
        "reason": reason,
    }


class EvaluationExecutionTests(unittest.TestCase):
    def test_valid_model_result_can_stop_before_stopping_condition(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            record = attempt_record(stopping_condition_reached=False)
            self.assertEqual(
                [],
                validate_generation_attempt(
                    record,
                    evidence_root,
                    condition="guided",
                    scenario="device-list",
                    changed=[],
                    deleted=[],
                ),
            )

    def test_valid_attempt_rejects_non_none_blocker(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            record = attempt_record(blocker="remote_transport")
            errors = validate_generation_attempt(
                record,
                Path(temp),
                condition="guided",
                scenario="device-list",
                changed=[],
                deleted=[],
            )
            self.assertTrue(any("valid attempt" in error and "blocker" in error for error in errors))

    def test_infrastructure_invalid_requires_blocker_and_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            record = attempt_record(
                validity="infrastructure_invalid",
                blocker="none",
                stopping_condition_reached=False,
                reason="Remote operation was blocked",
            )
            errors = validate_generation_attempt(
                record,
                Path(temp),
                condition="guided",
                scenario="device-list",
                changed=[],
                deleted=[],
            )
            self.assertTrue(any("infrastructure_invalid" in error and "blocker" in error for error in errors))
            self.assertTrue(any("infrastructure_invalid" in error and "evidence" in error for error in errors))

    def test_infrastructure_invalid_accepts_existing_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            (evidence_root / "generation-failure.txt").write_text(
                "Remote safety inspection blocked the write.\n", encoding="utf-8"
            )
            record = attempt_record(
                validity="infrastructure_invalid",
                blocker="remote_safety_inspection",
                stopping_condition_reached=False,
                evidence=[
                    {
                        "path": "generation-failure.txt",
                        "detail": "Remote safety inspection blocked generation.",
                    }
                ],
                reason="External safety inspection interrupted generation.",
            )
            self.assertEqual(
                [],
                validate_generation_attempt(
                    record,
                    evidence_root,
                    condition="guided",
                    scenario="device-list",
                    changed=[],
                    deleted=[],
                ),
            )

    def test_evidence_path_must_exist_inside_evidence_directory(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            evidence_root = Path(temp)
            outside = evidence_root.parent / "outside-generation-evidence.txt"
            outside.write_text("outside\n", encoding="utf-8")
            try:
                record = attempt_record(
                    validity="infrastructure_invalid",
                    blocker="remote_transport",
                    stopping_condition_reached=False,
                    evidence=[
                        {
                            "path": "../outside-generation-evidence.txt",
                            "detail": "must not escape evidence root",
                        }
                    ],
                    reason="Remote transport interrupted generation.",
                )
                errors = validate_generation_attempt(
                    record,
                    evidence_root,
                    condition="guided",
                    scenario="device-list",
                    changed=[],
                    deleted=[],
                )
                self.assertTrue(any("escapes evidence directory" in error for error in errors))
            finally:
                outside.unlink(missing_ok=True)

    def test_project_delta_must_match_controller_delta(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            record = attempt_record(changed=["MainWindow.xaml"])
            errors = validate_generation_attempt(
                record,
                Path(temp),
                condition="guided",
                scenario="device-list",
                changed=["MainWindow.xaml.cs"],
                deleted=[],
            )
            self.assertTrue(any("project_delta" in error for error in errors))

    def test_condition_and_scenario_must_match_packet(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            record = attempt_record(condition="baseline", scenario="connection-settings")
            errors = validate_generation_attempt(
                record,
                Path(temp),
                condition="guided",
                scenario="device-list",
                changed=[],
                deleted=[],
            )
            self.assertTrue(any("condition" in error for error in errors))
            self.assertTrue(any("scenario" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
