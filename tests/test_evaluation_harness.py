from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_harness import (
    CAPTURE_SCHEMA_VERSION,
    PACKET_SCHEMA_VERSION,
    build_packet,
    capture_run,
    inspect_packet,
    inspect_packets,
    pinned_build_environment,
    prepare_run_packet,
    validate_matrix,
    validate_results,
)


ROOT = Path(__file__).resolve().parents[1]
START_SHA = "b73babad19d0153707a49e5ba1ed9fb0a42c33ef"
SCENARIOS = ("connection-settings", "device-list", "failure-confirmation")


def complete_run(
    packet: Path, model: str = "gpt-5.6-test", build: dict | None = None
) -> None:
    build_command = "not performed"
    build_result = "not performed"
    if build is not None:
        build_command = build["harness_command"]
        build_result = f"exit {build['exit_code']}"
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
        "Build command": build_command,
        "Build result": build_result,
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
    if build is not None:
        build_check = verification_data["checks"]["build"]
        build_check["status"] = "pass" if build["exit_code"] == 0 else "fail"
        build_check["evidence"] = [
            {
                "path": "build.txt",
                "detail": f"controlled build exited {build['exit_code']}",
            }
        ]
        build_check["reason"] = ""
    verification.write_text(
        json.dumps(verification_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


class EvaluationHarnessTests(unittest.TestCase):
    def test_matrix_is_valid(self) -> None:
        self.assertEqual([], validate_matrix(ROOT))

    def test_pinned_build_environment_matches_fixture_contract(self) -> None:
        environment = pinned_build_environment(ROOT)
        self.assertEqual("9.0.313", environment["dotnet_sdk"])
        self.assertEqual("2.0.1", environment["windows_app_sdk"])
        self.assertEqual("10.0.26100.4948", environment["windows_sdk_build_tools"])

    def test_prepare_writes_current_packet_contract_version(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            manifest = prepare_run_packet(ROOT, "baseline", "connection-settings", packet)
            self.assertEqual(2, PACKET_SCHEMA_VERSION)
            self.assertEqual(PACKET_SCHEMA_VERSION, manifest["schema_version"])
            template = (packet / "RUN.template.md").read_text(encoding="utf-8")
            self.assertIn(".NET SDK: 9.0.313", template)
            self.assertIn("Windows App SDK package: 2.0.1", template)

    def test_build_packet_uses_pinned_sdk_and_writes_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            prepare_run_packet(ROOT, "baseline", "connection-settings", packet)
            (packet / "project/global.json").write_text(
                '{"sdk":{"version":"10.0.302"}}\n', encoding="utf-8"
            )
            result = build_packet(ROOT, packet)
            self.assertEqual("9.0.313", result["selected_sdk"])
            self.assertEqual("9.0.313", result["expected_sdk"])
            self.assertEqual(0, result["exit_code"])
            evidence = packet / "evidence/build.txt"
            self.assertTrue(evidence.is_file())
            self.assertIn("Selected .NET SDK: 9.0.313", evidence.read_text(encoding="utf-8"))
            complete_run(packet, build=result)
            status = inspect_packet(ROOT, packet, "baseline", "connection-settings")
            self.assertEqual("capture_ready", status["status"])
            captured = Path(temp) / "captured"
            capture_run(ROOT, packet, captured)
            self.assertTrue((captured / "evidence/build.txt").is_file())

    def test_build_missing_pinned_project_is_preserved_as_failure(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result_dir = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "device-list", packet)
            (packet / "project/LazyDesign.EvaluationApp.csproj").unlink()
            build = build_packet(ROOT, packet)
            self.assertNotEqual(0, build["exit_code"])
            self.assertTrue((packet / "evidence/build.txt").is_file())
            complete_run(packet, build=build)
            self.assertEqual(
                "capture_ready",
                inspect_packet(ROOT, packet, "baseline", "device-list")["status"],
            )
            capture = capture_run(ROOT, packet, result_dir)
            self.assertIn("LazyDesign.EvaluationApp.csproj", capture["deleted_files"])

    def test_build_targets_pinned_project_when_alternate_project_is_added(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            prepare_run_packet(ROOT, "baseline", "connection-settings", packet)
            (packet / "project/Alternate.csproj").write_text(
                '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
                '<TargetFramework>net9.0</TargetFramework>'
                '</PropertyGroup></Project>\n',
                encoding="utf-8",
            )
            build = build_packet(ROOT, packet)
            self.assertEqual(0, build["exit_code"])
            evidence = (packet / "evidence/build.txt").read_text(encoding="utf-8")
            command_line = next(
                line for line in evidence.splitlines() if line.startswith("Command:")
            )
            self.assertIn("LazyDesign.EvaluationApp.csproj", command_line)
            self.assertNotIn("Alternate.csproj", command_line)

    def test_capture_refuses_project_changed_after_controlled_build(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "connection-settings", packet)
            generated = packet / "project/MainWindow.xaml"
            generated.write_text(
                generated.read_text(encoding="utf-8") + "\n<!-- generated before build -->\n",
                encoding="utf-8",
            )
            build = build_packet(ROOT, packet)
            complete_run(packet, build=build)
            generated.write_text(
                generated.read_text(encoding="utf-8") + "\n<!-- changed after build -->\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                capture_run(ROOT, packet, result)
            self.assertFalse(result.exists())

    def test_capture_refuses_build_command_for_another_packet(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "connection-settings", packet)
            build = build_packet(ROOT, packet)
            complete_run(packet, build=build)
            run_path = packet / "RUN.md"
            run_path.write_text(
                run_path.read_text(encoding="utf-8").replace(
                    build["harness_command"],
                    "python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/guided/device-list",
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                capture_run(ROOT, packet, result)
            self.assertFalse(result.exists())

    def test_inspect_fresh_packet_is_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            prepare_run_packet(ROOT, "guided", "device-list", packet)
            status = inspect_packet(ROOT, packet, "guided", "device-list")
            self.assertEqual("ready", status["status"])
            self.assertEqual([], status["errors"])

    def test_inspect_packet_cli_reports_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            prepare_run_packet(ROOT, "baseline", "failure-confirmation", packet)
            process = subprocess.run(
                [
                    sys.executable,
                    "scripts/evaluation_harness.py",
                    "inspect-packet",
                    "--packet",
                    str(packet),
                    "--condition",
                    "baseline",
                    "--scenario",
                    "failure-confirmation",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, process.returncode, process.stderr)
            self.assertEqual("ready", json.loads(process.stdout)["status"])

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

    def test_inspect_legacy_packet_is_stale(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            prepare_run_packet(ROOT, "baseline", "device-list", packet)
            manifest_path = packet / "PACKET.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["schema_version"] = 1
            del manifest["input_commit"]
            del manifest["project_files"]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            artifact = packet / "project/bin/legacy-build.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("legacy\n", encoding="utf-8")
            status = inspect_packet(ROOT, packet, "baseline", "device-list")
            self.assertEqual("stale", status["status"])
            self.assertEqual(
                [
                    "packet must contain exactly the current contract fields",
                    "packet schema_version must be 2",
                ],
                status["errors"],
            )
            self.assertIn("build artifacts present", status["activity"])

    def test_inspect_modified_packet_is_in_progress(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            prepare_run_packet(ROOT, "guided", "connection-settings", packet)
            main_window = packet / "project/MainWindow.xaml"
            main_window.write_text(main_window.read_text(encoding="utf-8") + "\n<!-- work -->\n", encoding="utf-8")
            status = inspect_packet(ROOT, packet, "guided", "connection-settings")
            self.assertEqual("in_progress", status["status"])
            self.assertIn("project files changed", status["activity"])

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

    def test_capture_refuses_wrong_pinned_sdk_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "device-list", packet)
            complete_run(packet)
            run_path = packet / "RUN.md"
            run_path.write_text(
                run_path.read_text(encoding="utf-8").replace(
                    ".NET SDK: 9.0.313", ".NET SDK: 10.0.302"
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                capture_run(ROOT, packet, result)
            self.assertFalse(result.exists())

    def test_capture_refuses_uncontrolled_build_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            result = Path(temp) / "result"
            prepare_run_packet(ROOT, "baseline", "device-list", packet)
            complete_run(packet)
            run_path = packet / "RUN.md"
            run_path.write_text(
                run_path.read_text(encoding="utf-8")
                .replace("Build command: not performed", "Build command: dotnet build")
                .replace("Build result: not performed", "Build result: exit 0"),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                capture_run(ROOT, packet, result)
            self.assertFalse(result.exists())

    def test_inspect_completed_packet_is_capture_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            packet = Path(temp) / "packet"
            prepare_run_packet(ROOT, "guided", "failure-confirmation", packet)
            complete_run(packet)
            status = inspect_packet(ROOT, packet, "guided", "failure-confirmation")
            self.assertEqual("capture_ready", status["status"])
            self.assertEqual([], status["errors"])

    def test_inspect_packets_returns_exact_matrix_entries(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            statuses = inspect_packets(ROOT, Path(temp))
            self.assertEqual(6, len(statuses))
            self.assertEqual({"missing"}, {item["status"] for item in statuses})
            self.assertEqual(
                {(condition, scenario) for condition in ("baseline", "guided") for scenario in SCENARIOS},
                {(item["condition"], item["scenario"]) for item in statuses},
            )

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

            self.assertEqual(2, CAPTURE_SCHEMA_VERSION)
            self.assertEqual(CAPTURE_SCHEMA_VERSION, capture["schema_version"])
            self.assertEqual(changed.read_bytes(), (result / "generated/MainWindow.xaml").read_bytes())
            self.assertEqual(["app.manifest"], capture["deleted_files"])
            self.assertFalse((result / "generated/bin/ignored.txt").exists())

    def _create_complete_results(self, root: Path) -> Path:
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
                (packet / "evidence/notes.txt").write_text(
                    f"{condition}/{scenario} evidence\n", encoding="utf-8"
                )
                capture_run(ROOT, packet, result)
        return results

    def test_validate_results_enforces_identical_run_conditions(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            results = self._create_complete_results(Path(temp))
            self.assertEqual([], validate_results(ROOT, results))
            run_path = results / "guided/device-list/RUN.md"
            run_path.write_text(
                run_path.read_text(encoding="utf-8").replace("gpt-5.6-test", "different-model"),
                encoding="utf-8",
            )
            errors = validate_results(ROOT, results)
            self.assertTrue(any("Model identifier differs" in error for error in errors))

    def test_validate_results_rejects_modified_captured_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            results = self._create_complete_results(Path(temp))
            notes = results / "guided/device-list/evidence/notes.txt"
            notes.write_text("modified after capture\n", encoding="utf-8")
            errors = validate_results(ROOT, results)
            self.assertTrue(any("captured evidence files differ" in error for error in errors))

    def test_validate_results_rejects_added_generated_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            results = self._create_complete_results(Path(temp))
            added = results / "guided/device-list/generated/AddedAfterCapture.xaml"
            added.write_text("<Page />\n", encoding="utf-8")
            errors = validate_results(ROOT, results)
            self.assertTrue(any("captured generated files differ" in error for error in errors))

    def test_validate_results_rejects_modified_run_record(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            results = self._create_complete_results(Path(temp))
            run_path = results / "guided/device-list/RUN.md"
            run_path.write_text(
                run_path.read_text(encoding="utf-8").replace(
                    "Notes: test fixture", "Notes: modified after capture"
                ),
                encoding="utf-8",
            )
            errors = validate_results(ROOT, results)
            self.assertTrue(any("captured run record differs" in error for error in errors))

    def test_validate_results_rejects_modified_packet_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "evaluation") as temp:
            results = self._create_complete_results(Path(temp))
            packet_path = results / "guided/device-list/PACKET.json"
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            packet["post_capture_note"] = "modified"
            packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
            errors = validate_results(ROOT, results)
            self.assertTrue(any("captured packet metadata differs" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
