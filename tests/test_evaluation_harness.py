from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_harness import prepare_run_packet, validate_matrix


ROOT = Path(__file__).resolve().parents[1]
START_SHA = "b73babad19d0153707a49e5ba1ed9fb0a42c33ef"


class EvaluationHarnessTests(unittest.TestCase):
    def test_matrix_is_valid(self) -> None:
        self.assertEqual([], validate_matrix(ROOT))

    def test_prepare_baseline_uses_exact_prompt_and_no_references(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            destination = Path(temp) / "baseline-connection-settings"
            manifest = prepare_run_packet(ROOT, "baseline", "connection-settings", destination)

            prompt = ROOT / "evaluation/prompts/connection-settings.md"
            self.assertEqual(prompt.read_bytes(), (destination / "PROMPT.md").read_bytes())
            self.assertTrue((destination / "project/LazyDesign.EvaluationApp.csproj").is_file())
            self.assertFalse((destination / "context").exists())
            self.assertEqual(START_SHA, manifest["start_project_commit"])
            self.assertEqual([], manifest["references"])
            self.assertEqual(hashlib.sha256(prompt.read_bytes()).hexdigest(), manifest["prompt_sha256"])

    def test_prepare_guided_copies_only_fixed_reference_set(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            destination = Path(temp) / "guided-device-list"
            manifest = prepare_run_packet(ROOT, "guided", "device-list", destination)

            expected = {
                "DESIGN.md",
                "foundations/text-and-localization.md",
                "foundations/sizing-and-spacing.md",
                "foundations/icons.md",
                "foundations/states-and-themes.md",
                "foundations/accessibility-basics.md",
                "components/button.md",
                "components/commandbar.md",
                "components/listview.md",
            }
            actual = {
                str(path.relative_to(destination / "context")).replace("\\", "/")
                for path in (destination / "context").rglob("*")
                if path.is_file()
            }
            self.assertEqual(expected, actual)
            self.assertEqual(expected, {item["path"] for item in manifest["references"]})
            for relative in expected:
                self.assertEqual((ROOT / relative).read_bytes(), (destination / "context" / relative).read_bytes())

    def test_prepare_refuses_to_modify_existing_packet(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            destination = Path(temp) / "existing"
            destination.mkdir()
            with self.assertRaises(FileExistsError):
                prepare_run_packet(ROOT, "baseline", "connection-settings", destination)


if __name__ == "__main__":
    unittest.main()
