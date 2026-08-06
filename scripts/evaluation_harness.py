#!/usr/bin/env python3
"""Prepare, capture, and validate controlled LazyDesign evaluation runs."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
import tarfile
import uuid
from pathlib import Path, PurePosixPath
from typing import Any

MATRIX_PATH = Path("evaluation/run-matrix.json")
EXPECTED_SCENARIOS = {"connection-settings", "device-list", "failure-confirmation"}
EXPECTED_WIDTHS = {"connection-settings": 420, "device-list": 520, "failure-confirmation": None}
IGNORED_PROJECT_PARTS = {"bin", "obj", ".vs"}
RUN_FIELDS = (
    "Condition",
    "Scenario",
    "Run date and local time",
    "Model identifier",
    "Reasoning level",
    "Fresh context",
    "Generation stopping condition",
    "Starting project repository and SHA",
    "Operating system",
    ".NET SDK",
    "Windows App SDK package",
    "Tool access",
    "Network access",
    "Reference files supplied",
    "Generation intervention",
    "Generated file list",
    "Generation completion status",
    "Build command",
    "Build result",
    "Rendered checks performed",
    "Checks not performed",
    "Notes",
)
CONSISTENT_RUN_FIELDS = (
    "Model identifier",
    "Reasoning level",
    "Generation stopping condition",
    "Starting project repository and SHA",
    "Operating system",
    ".NET SDK",
    "Windows App SDK package",
    "Tool access",
    "Network access",
)
PLACEHOLDER_FRAGMENTS = (
    "record before generation",
    "record after generation",
    "record after verification",
    "none | record exact intervention",
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_matrix(repo_root: Path) -> dict[str, Any]:
    return _load_json(repo_root / MATRIX_PATH)


def _safe_repo_path(repo_root: Path, relative: str) -> Path:
    candidate = (repo_root / relative).resolve()
    if not candidate.is_relative_to(repo_root.resolve()):
        raise ValueError(f"path escapes repository: {relative}")
    return candidate


def _require_workspace_path(repo_root: Path, path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(repo_root.resolve()):
        raise ValueError(f"{label} must remain inside the repository workspace")
    return resolved


def _git_object_exists(repo_root: Path, object_name: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", object_name],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def _git_file_bytes(repo_root: Path, commit: str, relative: str) -> bytes:
    _safe_repo_path(repo_root, relative)
    return subprocess.check_output(
        ["git", "show", f"{commit}:{relative}"],
        cwd=repo_root,
    )


def validate_matrix(repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        matrix = _load_matrix(repo_root)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load {MATRIX_PATH}: {exc}"]

    if matrix.get("schema_version") != 1:
        errors.append("run matrix schema_version must be 1")
    input_commit = matrix.get("input_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", input_commit):
        errors.append("input commit must be a full lowercase SHA")
    elif not _git_object_exists(repo_root, f"{input_commit}^{{commit}}"):
        errors.append(f"input commit does not exist: {input_commit}")
    start = matrix.get("start_project", {})
    commit = start.get("commit", "")
    project_path = start.get("path", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        errors.append("start project commit must be a full lowercase SHA")
    elif not _git_object_exists(repo_root, f"{commit}^{{commit}}"):
        errors.append(f"start project commit does not exist: {commit}")
    if not project_path:
        errors.append("start project path is missing")
    elif commit and not _git_object_exists(repo_root, f"{commit}:{project_path}"):
        errors.append(f"start project tree is missing at {commit}:{project_path}")

    scenarios = matrix.get("scenarios", {})
    if set(scenarios) != EXPECTED_SCENARIOS:
        errors.append("run matrix must contain exactly the three fixed scenarios")
    for name in sorted(EXPECTED_SCENARIOS & set(scenarios)):
        scenario = scenarios[name]
        if scenario.get("content_width_dip") != EXPECTED_WIDTHS[name]:
            errors.append(f"unexpected content width for {name}")
        prompt = scenario.get("prompt", "")
        references = scenario.get("guided_references", [])
        try:
            _safe_repo_path(repo_root, prompt)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if input_commit and not _git_object_exists(repo_root, f"{input_commit}:{prompt}"):
                errors.append(f"missing prompt at input commit: {prompt}")
        if not references or len(references) != len(set(references)):
            errors.append(f"guided reference set is empty or duplicated: {name}")
        for relative in references:
            try:
                _safe_repo_path(repo_root, relative)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if input_commit and not _git_object_exists(
                    repo_root, f"{input_commit}:{relative}"
                ):
                    errors.append(f"missing guided reference at input commit: {relative}")
    return errors


def _project_archive_bytes(repo_root: Path, commit: str, project_path: str) -> bytes:
    return subprocess.run(
        [
            "git",
            "archive",
            "--format=tar",
            "--prefix=project/",
            f"{commit}:{project_path}",
        ],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout


def _extract_project(repo_root: Path, commit: str, project_path: str, destination: Path) -> None:
    archive = _project_archive_bytes(repo_root, commit, project_path)
    prefix = PurePosixPath("project")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar.getmembers():
            member_path = PurePosixPath(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError(f"unsafe archive member: {member.name}")
            relative = member_path.relative_to(prefix)
            target = destination.joinpath(*relative.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                source = tar.extractfile(member)
                if source is None:
                    raise ValueError(f"cannot read archive member: {member.name}")
                target.write_bytes(source.read())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _file_hashes(root: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_PROJECT_PARTS for part in relative.parts):
            continue
        records.append(
            {
                "path": relative.as_posix(),
                "sha256": _sha256(path),
            }
        )
    return sorted(records, key=lambda item: (item["path"].casefold(), item["path"]))


def _git_project_file_hashes(
    repo_root: Path, commit: str, project_path: str
) -> list[dict[str, str]]:
    archive = _project_archive_bytes(repo_root, commit, project_path)
    prefix = PurePosixPath("project")
    records: list[dict[str, str]] = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            member_path = PurePosixPath(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError(f"unsafe archive member: {member.name}")
            relative = member_path.relative_to(prefix)
            if any(part in IGNORED_PROJECT_PARTS for part in relative.parts):
                continue
            source = tar.extractfile(member)
            if source is None:
                raise ValueError(f"cannot read archive member: {member.name}")
            records.append(
                {
                    "path": relative.as_posix(),
                    "sha256": hashlib.sha256(source.read()).hexdigest(),
                }
            )
    return sorted(records, key=lambda item: (item["path"].casefold(), item["path"]))


def prepare_run_packet(
    repo_root: Path, condition: str, scenario_name: str, destination: Path
) -> dict[str, Any]:
    errors = validate_matrix(repo_root)
    if errors:
        raise ValueError("invalid run matrix: " + "; ".join(errors))
    if condition not in {"baseline", "guided"}:
        raise ValueError(f"unsupported condition: {condition}")
    matrix = _load_matrix(repo_root)
    if scenario_name not in matrix["scenarios"]:
        raise ValueError(f"unsupported scenario: {scenario_name}")
    destination = _require_workspace_path(repo_root, destination, "run packet destination")
    if destination.exists():
        raise FileExistsError(f"run packet already exists: {destination}")

    temp = destination.with_name(f".{destination.name}.tmp-{uuid.uuid4().hex}")
    try:
        temp.mkdir(parents=True)
        input_commit = matrix["input_commit"]
        start = matrix["start_project"]
        scenario = matrix["scenarios"][scenario_name]
        _extract_project(repo_root, start["commit"], start["path"], temp / "project")
        prompt_bytes = _git_file_bytes(repo_root, input_commit, scenario["prompt"])
        (temp / "PROMPT.md").write_bytes(prompt_bytes)

        references: list[dict[str, str]] = []
        if condition == "guided":
            for relative in scenario["guided_references"]:
                reference_bytes = _git_file_bytes(repo_root, input_commit, relative)
                target = temp / "context" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(reference_bytes)
                references.append(
                    {
                        "path": relative,
                        "sha256": hashlib.sha256(reference_bytes).hexdigest(),
                    }
                )

        manifest: dict[str, Any] = {
            "schema_version": 1,
            "condition": condition,
            "scenario": scenario_name,
            "input_commit": input_commit,
            "start_project_commit": start["commit"],
            "start_project_path": start["path"],
            "content_width_dip": scenario["content_width_dip"],
            "prompt_path": scenario["prompt"],
            "prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
            "references": references,
            "project_files": _file_hashes(temp / "project"),
        }
        (temp / "PACKET.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (temp / "RUN.template.md").write_text(_run_template(manifest), encoding="utf-8")
        temp.rename(destination)
        return manifest
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def _run_template(manifest: dict[str, Any]) -> str:
    supplied = "none" if not manifest["references"] else "see PACKET.json"
    return f"""# Evaluation Run Record

Condition: {manifest['condition']}
Scenario: {manifest['scenario']}
Run date and local time: record after generation
Model identifier: record before generation
Reasoning level: record before generation
Fresh context: record before generation
Generation stopping condition: record before generation
Starting project repository and SHA: lazyant91/LazyDesign {manifest['start_project_commit']}
Operating system: record before generation
.NET SDK: record before generation
Windows App SDK package: 2.0.1
Tool access: record before generation
Network access: record before generation
Reference files supplied: {supplied}
Generation intervention: none | record exact intervention
Generated file list: record after generation
Generation completion status: record after generation
Build command: not performed
Build result: not performed
Rendered checks performed: not performed
Checks not performed: record after verification
Notes: packet hashes are recorded in PACKET.json
"""


def _validate_packet(repo_root: Path, packet_dir: Path) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    try:
        packet = _load_json(packet_dir / "PACKET.json")
        matrix = _load_matrix(repo_root)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot load packet: {exc}"]

    condition = packet.get("condition")
    scenario_name = packet.get("scenario")
    if condition not in {"baseline", "guided"}:
        errors.append(f"invalid packet condition: {condition}")
    if scenario_name not in matrix["scenarios"]:
        errors.append(f"invalid packet scenario: {scenario_name}")
        return packet, errors
    scenario = matrix["scenarios"][scenario_name]
    input_commit = matrix["input_commit"]
    start = matrix["start_project"]
    if packet.get("input_commit") != input_commit:
        errors.append("packet input commit differs from run matrix")
    if packet.get("start_project_commit") != start["commit"]:
        errors.append("packet start project commit differs from run matrix")
    if packet.get("start_project_path") != start["path"]:
        errors.append("packet start project path differs from run matrix")
    expected_project_files = _git_project_file_hashes(
        repo_root, start["commit"], start["path"]
    )
    if packet.get("project_files") != expected_project_files:
        errors.append("packet start project file hashes differ from the pinned fixture")
    if packet.get("content_width_dip") != scenario["content_width_dip"]:
        errors.append("packet content width differs from run matrix")

    prompt = packet_dir / "PROMPT.md"
    prompt_bytes = _git_file_bytes(repo_root, input_commit, scenario["prompt"])
    expected_prompt_hash = hashlib.sha256(prompt_bytes).hexdigest()
    if not prompt.is_file() or _sha256(prompt) != expected_prompt_hash:
        errors.append("packet PROMPT.md differs from the fixed prompt bytes")
    if packet.get("prompt_sha256") != expected_prompt_hash:
        errors.append("packet prompt hash differs from the fixed prompt")

    expected_references = [] if condition == "baseline" else scenario["guided_references"]
    packet_references = packet.get("references", [])
    if [item.get("path") for item in packet_references] != expected_references:
        errors.append("packet reference list differs from the fixed condition set")
    context = packet_dir / "context"
    actual_context = []
    if context.exists():
        actual_context = [
            path.relative_to(context).as_posix()
            for path in sorted(context.rglob("*"))
            if path.is_file()
        ]
    if sorted(actual_context) != sorted(expected_references):
        errors.append("packet context files differ from the fixed condition set")
    for item in packet_references:
        relative = item.get("path", "")
        reference_bytes = _git_file_bytes(repo_root, input_commit, relative)
        context_file = context / relative
        source_hash = hashlib.sha256(reference_bytes).hexdigest()
        if item.get("sha256") != source_hash:
            errors.append(f"packet reference hash differs from source: {relative}")
        if not context_file.is_file() or _sha256(context_file) != source_hash:
            errors.append(f"packet reference content changed: {relative}")
    return packet, errors


def _parse_run_record(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return {}, [f"missing run record: {path}"]
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        for field in RUN_FIELDS:
            prefix = f"{field}:"
            if line.startswith(prefix):
                values[field] = line[len(prefix) :].strip()
                break
    for field in RUN_FIELDS:
        if field not in values:
            errors.append(f"missing RUN.md field: {field}")
        elif not values[field]:
            errors.append(f"blank RUN.md field: {field}")
        elif any(fragment in values[field] for fragment in PLACEHOLDER_FRAGMENTS):
            errors.append(f"unresolved RUN.md field: {field}")
    return values, errors


def capture_run(
    repo_root: Path, packet_dir: Path, destination: Path
) -> dict[str, Any]:
    packet_dir = _require_workspace_path(repo_root, packet_dir, "run packet")
    destination = _require_workspace_path(repo_root, destination, "result destination")
    if destination.exists():
        raise FileExistsError(f"result already exists: {destination}")
    packet, errors = _validate_packet(repo_root, packet_dir)
    run_values, run_errors = _parse_run_record(packet_dir / "RUN.md")
    errors.extend(run_errors)
    if run_values:
        if run_values.get("Condition") != packet.get("condition"):
            errors.append("RUN.md condition differs from PACKET.json")
        if run_values.get("Scenario") != packet.get("scenario"):
            errors.append("RUN.md scenario differs from PACKET.json")
        if packet.get("start_project_commit", "") not in run_values.get(
            "Starting project repository and SHA", ""
        ):
            errors.append("RUN.md start project SHA differs from PACKET.json")
    if errors:
        raise ValueError("invalid run packet: " + "; ".join(errors))

    original = {item["path"]: item["sha256"] for item in packet.get("project_files", [])}
    current_records = _file_hashes(packet_dir / "project")
    current = {item["path"]: item["sha256"] for item in current_records}
    changed = [item for item in current_records if original.get(item["path"]) != item["sha256"]]
    deleted = sorted(set(original) - set(current))

    temp = destination.with_name(f".{destination.name}.tmp-{uuid.uuid4().hex}")
    try:
        temp.mkdir(parents=True)
        for name in ("PROMPT.md", "PACKET.json", "RUN.md"):
            shutil.copyfile(packet_dir / name, temp / name)
        evidence = packet_dir / "evidence"
        if evidence.is_dir():
            shutil.copytree(evidence, temp / "evidence")
        for item in changed:
            source = packet_dir / "project" / item["path"]
            target = temp / "generated" / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        capture: dict[str, Any] = {
            "schema_version": 1,
            "condition": packet["condition"],
            "scenario": packet["scenario"],
            "generated_files": changed,
            "deleted_files": deleted,
        }
        (temp / "CAPTURE.json").write_text(
            json.dumps(capture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        temp.rename(destination)
        return capture
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def _validate_result(
    repo_root: Path, result_dir: Path, condition: str, scenario_name: str
) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    try:
        packet = _load_json(result_dir / "PACKET.json")
        capture = _load_json(result_dir / "CAPTURE.json")
        matrix = _load_matrix(repo_root)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{condition}/{scenario_name}: cannot load result metadata: {exc}"]
    scenario = matrix["scenarios"][scenario_name]
    input_commit = matrix["input_commit"]
    start = matrix["start_project"]
    prefix = f"{condition}/{scenario_name}"
    if packet.get("condition") != condition or packet.get("scenario") != scenario_name:
        errors.append(f"{prefix}: PACKET.json identity mismatch")
    if capture.get("condition") != condition or capture.get("scenario") != scenario_name:
        errors.append(f"{prefix}: CAPTURE.json identity mismatch")
    if packet.get("input_commit") != input_commit:
        errors.append(f"{prefix}: input commit mismatch")
    if packet.get("start_project_commit") != start["commit"]:
        errors.append(f"{prefix}: start project SHA mismatch")
    expected_project_files = _git_project_file_hashes(
        repo_root, start["commit"], start["path"]
    )
    if packet.get("project_files") != expected_project_files:
        errors.append(f"{prefix}: start project file hashes differ")
    prompt_bytes = _git_file_bytes(repo_root, input_commit, scenario["prompt"])
    prompt = result_dir / "PROMPT.md"
    expected_prompt_hash = hashlib.sha256(prompt_bytes).hexdigest()
    if not prompt.is_file() or _sha256(prompt) != expected_prompt_hash:
        errors.append(f"{prefix}: PROMPT.md bytes differ")
    if packet.get("prompt_sha256") != expected_prompt_hash:
        errors.append(f"{prefix}: PACKET.json prompt hash differs")
    expected_references = [] if condition == "baseline" else scenario["guided_references"]
    if [item.get("path") for item in packet.get("references", [])] != expected_references:
        errors.append(f"{prefix}: reference set differs")
    for item in packet.get("references", []):
        reference_bytes = _git_file_bytes(repo_root, input_commit, item["path"])
        if item.get("sha256") != hashlib.sha256(reference_bytes).hexdigest():
            errors.append(f"{prefix}: reference hash differs for {item['path']}")
    for item in capture.get("generated_files", []):
        generated = result_dir / "generated" / item.get("path", "")
        if not generated.is_file() or _sha256(generated) != item.get("sha256"):
            errors.append(f"{prefix}: captured generated file differs: {item.get('path')}")
    run_values, run_errors = _parse_run_record(result_dir / "RUN.md")
    errors.extend(f"{prefix}: {error}" for error in run_errors)
    if run_values:
        if run_values.get("Condition") != condition:
            errors.append(f"{prefix}: RUN.md condition differs")
        if run_values.get("Scenario") != scenario_name:
            errors.append(f"{prefix}: RUN.md scenario differs")
        if run_values.get("Fresh context", "").lower() != "yes":
            errors.append(f"{prefix}: fresh context was not confirmed")
        if run_values.get("Generation intervention", "").lower() != "none":
            errors.append(f"{prefix}: generation intervention was not none")
    return run_values, errors


def validate_results(repo_root: Path, results_root: Path) -> list[str]:
    errors = validate_matrix(repo_root)
    if errors:
        return errors
    all_runs: list[tuple[str, dict[str, str]]] = []
    for condition in ("baseline", "guided"):
        for scenario_name in sorted(EXPECTED_SCENARIOS):
            label = f"{condition}/{scenario_name}"
            result_dir = results_root / condition / scenario_name
            if not result_dir.is_dir():
                errors.append(f"missing result directory: {label}")
                continue
            values, result_errors = _validate_result(
                repo_root, result_dir, condition, scenario_name
            )
            errors.extend(result_errors)
            if values:
                all_runs.append((label, values))
    if len(all_runs) == 6:
        for field in CONSISTENT_RUN_FIELDS:
            distinct = {values[field] for _, values in all_runs if field in values}
            if len(distinct) != 1:
                errors.append(f"{field} differs across the six runs")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--condition", choices=("baseline", "guided"), required=True)
    prepare.add_argument("--scenario", choices=tuple(sorted(EXPECTED_SCENARIOS)), required=True)
    prepare.add_argument("--destination", type=Path, required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--packet", type=Path, required=True)
    capture.add_argument("--destination", type=Path, required=True)
    validate_completed = subparsers.add_parser("validate-results")
    validate_completed.add_argument("--root", type=Path, default=Path("evaluation"))
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if args.command == "validate":
        errors = validate_matrix(repo_root)
        success = "evaluation run matrix passed"
    elif args.command == "validate-results":
        errors = validate_results(repo_root, args.root)
        success = "evaluation results passed"
    elif args.command == "prepare":
        manifest = prepare_run_packet(repo_root, args.condition, args.scenario, args.destination)
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    else:
        capture_manifest = capture_run(repo_root, args.packet, args.destination)
        print(json.dumps(capture_manifest, ensure_ascii=False, indent=2))
        return 0
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(success)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
