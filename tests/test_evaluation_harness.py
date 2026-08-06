from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_harness import (
    capture_run,
    prepare_run_packet,
    validate_matrix,
    validate_results,
)


ROOT = Path(__file__).resolve().parents[1]
START_SHA = "b73babad19d0153707a49e5ba1ed9fb0a42c33ef"
SCENARIOS = ("connection-settings", "device-list", "failure-confirmation")


def complete_run(packet: Path, model: str = "gpt-5.6-test") -> None:
    values = {
        "Condition": json.loads((packet / "PACKET.json").read_text(encoding="utf-8"))["condition"],
        "Scenario": json.loads((packet / "PACKET.json").read_text(encoding="utf-8"))["scenario"],
        "Run date and local time": "2026-08-06 17:00 KST",
        "Model identifier": model,
        "Reasoning level": "high",
        "Fresh context": "yes",
        "Generation stopping condition": "model completed the requested implementation",
        "Starting project repository and SHA": f"lazyant91/LazyDesign {START_SHA}",
        "Operating system": "Windows 10.0.19045 x64",
        ".NET SDK": "9.0.313",
        "Windows App SDK package": "2.0.1",
        "Tool access": "filesystem and build only",
        "Network access": "disabled",
        "Reference files supplied": "see PACKET.json",
        "Generation intervention": "none",
        "Generated file list": "captured automatically",
        "Generation completion status": "completed",
        "Build command": "dotnet build -c Debug -p:Platform=x64",
        "Build result": "exit 0",
        "Rendered checks performed": "not performed",
        "Checks not performed": "render, theme, input, accessibility",
        "Notes": "test fixture",
    }
    text = "# Evaluation Run Record\n\n" + "\n".join(f"{key}: {value}" for key, value in values.items()) + "\n"
    (packet / "RUN.md").write_text(text, encoding="utf-8")
    template = packet / "evidence/verification.template.json"
    verification = packet / "evidence/verification.json"
    verification_data = json.loads(template.read_text(encoding="utf-8"))
    for check in verification_data["checks"].values():
        check["reason"] = "test fixture does not perform runtime verification"
    verification.write_text(
        json.dumps(verification_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


class EvaluationHarnessTests(unittest.TestCase):
    def test_matrix_is_valid(self) -> None:
        self.assertEqual([], validate_matrix(ROOT))

    def test_prepare_baseline_uses_exact_prompt_and_no_references(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            destination = Path(temp) / "baseline-connection-settings"
            manifest = prepare_run_packet(ROOT, "baseline", "connection-settings", destination)

            prompt_path = "evaluation/prompts/connection-settings.md"
            prompt_bytes = subprocess.check_output(
                ["git", "show", f"{manifest['input_commit']}:{prompt_path}"], cwd=ROOT
            )
            self.assertEqual(prompt_bytes, (destination / "PROMPT.md").read_bytes())
            self.assertTrue((destination / "project/LazyDesign.EvaluationApp.csproj").is_file())
            self.assertFalse((destination / "context").exists())
            self.assertEqual(START_SHA, manifest["start_project_commit"])
            self.assertEqual([], manifest["references"])
            self.assertTrue(manifest["project_files"])
            self.assertEqual(hashlib.sha256(prompt_bytes).hexdigest(), manifest["prompt_sha256"])

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
                pinned = subprocess.check_output(
                    ["git", "show", f"{manifest['input_commit']}:{relative}"], cwd=ROOT
                )
                self.assertEqual(pinned, (destination / "context" / relative).read_bytes())

    def test_prepare_refuses_to_modify_existing_packet(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            destination = Path(temp) / "existing"
            destination.mkdir()
            with self.assertRaises(FileExistsError):
                prepare_run_packet(ROOT, "baseline", "connection-settings", destination)

    def test_prepare_reads_guided_inputs_from_pinned_commit(self) -> None:
        source = ROOT / "components/button.md"
        original = source.read_bytes()
        try:
            source.write_bytes(original + b"\nworking tree mutation\n")
            with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
                destination = Path(temp) / "guided-pinned"
                manifest = prepare_run_packet(ROOT, "guided", "connection-settings", destination)
                pinned = subprocess.check_output(
                    ["git", "show", f"{manifest['input_commit']}:components/button.md"],
                    cwd=ROOT,
                )
                self.assertEqual(pinned, (destination / "context/components/button.md").read_bytes())
        finally:
            source.write_bytes(original)

    def test_capture_refuses_missing_verification_record(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "connection-settings", packet)
            complete_run(packet)
            (packet / "evidence/verification.json").unlink()
            with self.assertRaises(ValueError):
                capture_run(ROOT, packet, result)
            self.assertFalse(result.exists())

    def test_capture_refuses_tampered_prompt(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "connection-settings", packet)
            complete_run(packet)
            (packet / "PROMPT.md").write_text("changed", encoding="utf-8")
            with self.assertRaises(ValueError):
                capture_run(ROOT, packet, result)
            self.assertFalse(result.exists())

    def test_capture_refuses_tampered_start_project_hashes(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "device-list", packet)
            complete_run(packet)
            packet_path = packet / "PACKET.json"
            data = json.loads(packet_path.read_text(encoding="utf-8"))
            data["project_files"][0]["sha256"] = "0" * 64
            packet_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                capture_run(ROOT, packet, result)
            self.assertFalse(result.exists())

    def test_capture_preserves_changed_and_deleted_project_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "guided", "failure-confirmation", packet)
            complete_run(packet)
            changed = packet / "project/MainWindow.xaml"
            changed.write_text(changed.read_text(encoding="utf-8") + "\n<!-- generated -->\n", encoding="utf-8")
            (packet / "project/app.manifest").unlink()
            (packet / "project/bin/ignored.txt").parent.mkdir(parents=True)
            (packet / "project/bin/ignored.txt").write_text("ignore", encoding="utf-8")

            capture = capture_run(ROOT, packet, result)

            self.assertEqual(changed.read_bytes(), (result / "generated/MainWindow.xaml").read_bytes())
            self.assertEqual(["app.manifest"], capture["deleted_files"])
            self.assertFalse((result / "generated/bin/ignored.txt").exists())

    def test_validate_results_enforces_identical_run_conditions(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            root = Path(temp)
            results = root / "results"
            for condition in ("baseline", "guided"):
                for scenario in SCENARIOS:
                    packet = root / "packets" / condition / scenario
                    result = results / condition / scenario
                    prepare_run_packet(ROOT, condition, scenario, packet)
                    complete_run(packet)
                    main_window = packet / "project/MainWindow.xaml"
                    main_window.write_text(
                        main_window.read_text(encoding="utf-8") + f"\n<!-- {condition}-{scenario} -->\n",
                        encoding="utf-8",
                    )
                    capture_run(ROOT, packet, result)

            self.assertEqual([], validate_results(ROOT, results))
            run_path = results / "guided/device-list/RUN.md"
            run_path.write_text(
                run_path.read_text(encoding="utf-8").replace("gpt-5.6-test", "different-model"),
                encoding="utf-8",
            )
            errors = validate_results(ROOT, results)
            self.assertTrue(any("Model identifier differs" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
