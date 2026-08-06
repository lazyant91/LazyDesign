#!/usr/bin/env python3
"""Prepare, capture, and validate controlled LazyDesign evaluation runs."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from scripts.evaluation_evidence import load_and_validate, verification_template
except ModuleNotFoundError:
    from evaluation_evidence import load_and_validate, verification_template

MATRIX_PATH = Path("evaluation/run-matrix.json")
PACKET_SCHEMA_VERSION = 2
CAPTURE_SCHEMA_VERSION = 2
EXPECTED_SCENARIOS = {"connection-settings", "device-list", "failure-confirmation"}
EXPECTED_WIDTHS = {"connection-settings": 420, "device-list": 520, "failure-confirmation": None}
IGNORED_PROJECT_PARTS = {"bin", "obj", ".vs"}
PACKET_FIELDS = {
    "schema_version",
    "condition",
    "scenario",
    "input_commit",
    "start_project_commit",
    "start_project_path",
    "content_width_dip",
    "prompt_path",
    "prompt_sha256",
    "references",
    "project_files",
}
CAPTURE_FIELDS = {
    "schema_version",
    "condition",
    "scenario",
    "prompt_sha256",
    "packet_sha256",
    "run_sha256",
    "generated_files",
    "deleted_files",
    "evidence_files",
}
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


def pinned_build_environment(repo_root: Path) -> dict[str, str]:
    matrix = _load_matrix(repo_root)
    start = matrix["start_project"]
    commit = start["commit"]
    project_path = start["path"].rstrip("/")
    global_data = json.loads(
        _git_file_bytes(repo_root, commit, f"{project_path}/global.json").decode(
            "utf-8-sig"
        )
    )
    project_xml = ET.fromstring(
        _git_file_bytes(
            repo_root,
            commit,
            f"{project_path}/LazyDesign.EvaluationApp.csproj",
        ).decode("utf-8-sig")
    )
    packages = {
        item.attrib.get("Include", ""): item.attrib.get("Version", "")
        for item in project_xml.findall(".//PackageReference")
    }
    return {
        "dotnet_sdk": global_data["sdk"]["version"],
        "windows_app_sdk": packages["Microsoft.WindowsAppSDK"],
        "windows_sdk_build_tools": packages["Microsoft.Windows.SDK.BuildTools"],
        "start_commit": commit,
        "start_project_path": project_path,
    }


def _validate_run_environment(
    repo_root: Path, values: dict[str, str], prefix: str = ""
) -> list[str]:
    environment = pinned_build_environment(repo_root)
    label = f"{prefix}: " if prefix else ""
    errors: list[str] = []
    if values.get(".NET SDK") != environment["dotnet_sdk"]:
        errors.append(
            f"{label}.NET SDK must be pinned value {environment['dotnet_sdk']}"
        )
    if values.get("Windows App SDK package") != environment["windows_app_sdk"]:
        errors.append(
            f"{label}Windows App SDK package must be pinned value "
            f"{environment['windows_app_sdk']}"
        )
    return errors


def _build_evidence_values(path: Path) -> tuple[dict[str, str], list[str]]:
    required = {
        "Expected .NET SDK",
        "Selected .NET SDK",
        "Starting Windows App SDK package",
        "Starting Windows SDK BuildTools",
        "Command",
        "Exit code",
    }
    if not path.is_file():
        return {}, ["build: missing controlled evidence/build.txt"]
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        for key in required:
            prefix = f"{key}:"
            if line.startswith(prefix):
                values[key] = line[len(prefix) :].strip()
                break
    missing = sorted(required - set(values))
    return values, [f"build: build.txt missing field {key}" for key in missing]


def _validate_controlled_build(
    repo_root: Path,
    result_root: Path,
    run_values: dict[str, str],
    verification_path: Path,
    prefix: str = "",
) -> list[str]:
    label = f"{prefix}: " if prefix else ""
    try:
        verification = _load_json(verification_path)
    except (OSError, json.JSONDecodeError):
        return []
    build_check = verification.get("checks", {}).get("build", {})
    status = build_check.get("status")
    build_path = result_root / "evidence/build.txt"
    errors: list[str] = []
    if status == "not_run":
        if build_path.exists():
            errors.append(f"{label}build: build.txt exists while check is not_run")
        if run_values.get("Build command") != "not performed":
            errors.append(f"{label}build: RUN.md command must be not performed")
        if run_values.get("Build result") != "not performed":
            errors.append(f"{label}build: RUN.md result must be not performed")
        return errors
    if status not in {"pass", "fail"}:
        return errors

    evidence_paths = {
        item.get("path")
        for item in build_check.get("evidence", [])
        if isinstance(item, dict)
    }
    if "build.txt" not in evidence_paths:
        errors.append(f"{label}build: completed check must reference build.txt")
    values, evidence_errors = _build_evidence_values(build_path)
    errors.extend(f"{label}{error}" for error in evidence_errors)
    if evidence_errors:
        return errors

    environment = pinned_build_environment(repo_root)
    if values["Expected .NET SDK"] != environment["dotnet_sdk"]:
        errors.append(f"{label}build: expected SDK differs from pinned value")
    if values["Selected .NET SDK"] != environment["dotnet_sdk"]:
        errors.append(f"{label}build: selected SDK differs from pinned value")
    if values["Starting Windows App SDK package"] != environment["windows_app_sdk"]:
        errors.append(f"{label}build: Windows App SDK differs from pinned value")
    if values["Starting Windows SDK BuildTools"] != environment["windows_sdk_build_tools"]:
        errors.append(f"{label}build: Windows SDK BuildTools differs from pinned value")
    try:
        exit_code = int(values["Exit code"])
    except ValueError:
        errors.append(f"{label}build: exit code must be an integer")
        return errors
    if status == "pass" and exit_code != 0:
        errors.append(f"{label}build: pass requires exit code 0")
    if status == "fail" and exit_code == 0:
        errors.append(f"{label}build: fail requires a nonzero exit code")
    command = run_values.get("Build command", "")
    if not command.startswith("python scripts/evaluation_harness.py build --packet "):
        errors.append(f"{label}build: RUN.md must record the controlled harness command")
    if run_values.get("Build result") != f"exit {exit_code}":
        errors.append(f"{label}build: RUN.md result must match build.txt exit code")
    return errors


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
            "schema_version": PACKET_SCHEMA_VERSION,
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
        (temp / "RUN.template.md").write_text(
            _run_template(manifest, pinned_build_environment(repo_root)),
            encoding="utf-8",
        )
        evidence_dir = temp / "evidence"
        evidence_dir.mkdir()
        (evidence_dir / "verification.template.json").write_text(
            json.dumps(verification_template(scenario_name), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temp.rename(destination)
        return manifest
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def _run_template(
    manifest: dict[str, Any], environment: dict[str, str]
) -> str:
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
.NET SDK: {environment['dotnet_sdk']}
Windows App SDK package: {environment['windows_app_sdk']}
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

    if not isinstance(packet, dict):
        return {}, ["packet must be a JSON object"]
    if set(packet) != PACKET_FIELDS:
        errors.append("packet must contain exactly the current contract fields")
    if packet.get("schema_version") != PACKET_SCHEMA_VERSION:
        errors.append(
            f"packet schema_version must be {PACKET_SCHEMA_VERSION}"
        )
    if errors:
        return packet, errors

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

    run_template = packet_dir / "RUN.template.md"
    expected_run_template = _run_template(packet, pinned_build_environment(repo_root))
    if (
        not run_template.is_file()
        or run_template.read_text(encoding="utf-8-sig") != expected_run_template
    ):
        errors.append("packet RUN.template.md differs from the current contract")
    verification_path = packet_dir / "evidence/verification.template.json"
    try:
        actual_verification = _load_json(verification_path)
    except (OSError, json.JSONDecodeError):
        errors.append("packet verification template is missing or invalid")
    else:
        if actual_verification != verification_template(scenario_name):
            errors.append("packet verification template differs from the current contract")
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


def _packet_activity(packet_dir: Path, packet: dict[str, Any]) -> list[str]:
    activity: list[str] = []
    project = packet_dir / "project"
    if _file_hashes(project) != packet.get("project_files", []):
        activity.append("project files changed")
    build_files = [
        path
        for path in project.rglob("*")
        if path.is_file()
        and any(part in IGNORED_PROJECT_PARTS for part in path.relative_to(project).parts)
    ]
    if build_files:
        activity.append("build artifacts present")
    if (packet_dir / "RUN.md").is_file():
        activity.append("RUN.md present")
    if (packet_dir / "evidence/verification.json").is_file():
        activity.append("verification.json present")
    evidence_root = packet_dir / "evidence"
    if evidence_root.is_dir():
        additional = [
            path
            for path in evidence_root.rglob("*")
            if path.is_file()
            and path.relative_to(evidence_root).as_posix()
            not in {"verification.template.json", "verification.json"}
        ]
        if additional:
            activity.append("additional evidence present")
    return activity


def inspect_packet(
    repo_root: Path,
    packet_dir: Path,
    expected_condition: str,
    expected_scenario: str,
) -> dict[str, Any]:
    packet_dir = _require_workspace_path(repo_root, packet_dir, "run packet")
    relative = packet_dir.relative_to(repo_root.resolve()).as_posix()
    result: dict[str, Any] = {
        "condition": expected_condition,
        "scenario": expected_scenario,
        "path": relative,
        "status": "missing",
        "activity": [],
        "errors": [],
    }
    if not packet_dir.is_dir():
        return result

    packet, errors = _validate_packet(repo_root, packet_dir)
    if packet:
        if packet.get("condition") != expected_condition:
            errors.append("packet condition differs from expected directory")
        if packet.get("scenario") != expected_scenario:
            errors.append("packet scenario differs from expected directory")
        result["activity"] = _packet_activity(packet_dir, packet)
    if errors:
        result["status"] = "stale"
        result["errors"] = errors
        return result

    activity = result["activity"]
    run_path = packet_dir / "RUN.md"
    verification_path = packet_dir / "evidence/verification.json"
    if run_path.is_file() and verification_path.is_file():
        run_values, completion_errors = _parse_run_record(run_path)
        completion_errors.extend(_validate_run_environment(repo_root, run_values))
        completion_errors.extend(
            f"verification: {error}" for error in load_and_validate(verification_path)
        )
        completion_errors.extend(
            _validate_controlled_build(
                repo_root, packet_dir, run_values, verification_path
            )
        )
        if run_values.get("Condition") != expected_condition:
            completion_errors.append("RUN.md condition differs from packet")
        if run_values.get("Scenario") != expected_scenario:
            completion_errors.append("RUN.md scenario differs from packet")
        if packet.get("start_project_commit", "") not in run_values.get(
            "Starting project repository and SHA", ""
        ):
            completion_errors.append("RUN.md start project SHA differs from packet")
        if not completion_errors:
            result["status"] = "capture_ready"
            return result
        result["completion_errors"] = completion_errors

    result["status"] = "in_progress" if activity else "ready"
    return result


def inspect_packets(repo_root: Path, packets_root: Path) -> list[dict[str, Any]]:
    packets_root = _require_workspace_path(repo_root, packets_root, "packet root")
    return [
        inspect_packet(
            repo_root,
            packets_root / condition / scenario,
            condition,
            scenario,
        )
        for condition in ("baseline", "guided")
        for scenario in sorted(EXPECTED_SCENARIOS)
    ]


def build_packet(repo_root: Path, packet_dir: Path) -> dict[str, Any]:
    packet_dir = _require_workspace_path(repo_root, packet_dir, "run packet")
    packet, errors = _validate_packet(repo_root, packet_dir)
    if errors:
        raise ValueError("invalid run packet: " + "; ".join(errors))

    evidence_path = packet_dir / "evidence/build.txt"
    if evidence_path.exists():
        raise FileExistsError(f"build evidence already exists: {evidence_path}")

    projects = sorted((packet_dir / "project").glob("*.csproj"))
    if len(projects) != 1:
        raise ValueError("packet project must contain exactly one top-level .csproj")
    project = projects[0]
    environment = pinned_build_environment(repo_root)
    control_root = repo_root / "evaluation/.remote-temp" / f"sdk-{uuid.uuid4().hex}"
    control_root.mkdir(parents=True, exist_ok=False)
    try:
        global_bytes = _git_file_bytes(
            repo_root,
            environment["start_commit"],
            f"{environment['start_project_path']}/global.json",
        )
        (control_root / "global.json").write_bytes(global_bytes)
        process_environment = os.environ.copy()
        process_environment["DOTNET_CLI_UI_LANGUAGE"] = "en-US"
        process_environment["DOTNET_NOLOGO"] = "1"
        selected_sdk = subprocess.run(
            ["dotnet", "--version"],
            cwd=control_root,
            env=process_environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        ).stdout.decode("utf-8", errors="replace").strip()
        if selected_sdk != environment["dotnet_sdk"]:
            raise ValueError(
                f"selected .NET SDK {selected_sdk!r} differs from pinned "
                f"{environment['dotnet_sdk']}"
            )

        command = [
            "dotnet",
            "build",
            str(project.resolve()),
            "-c",
            "Debug",
            "-p:Platform=x64",
        ]
        completed = subprocess.run(
            command,
            cwd=control_root,
            env=process_environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = completed.stdout.decode("utf-8", errors="replace")
        relative_project = project.relative_to(repo_root).as_posix()
        evidence = "\n".join(
            (
                "# Evaluation Build Evidence",
                "",
                f"Recorded at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
                f"Packet: {packet['condition']}/{packet['scenario']}",
                f"Pinned start: {environment['start_commit']}:{environment['start_project_path']}",
                f"Expected .NET SDK: {environment['dotnet_sdk']}",
                f"Selected .NET SDK: {selected_sdk}",
                f"Starting Windows App SDK package: {environment['windows_app_sdk']}",
                f"Starting Windows SDK BuildTools: {environment['windows_sdk_build_tools']}",
                f"Command: dotnet build {relative_project} -c Debug -p:Platform=x64",
                f"Exit code: {completed.returncode}",
                "",
                "## Output",
                "",
                output.rstrip(),
                "",
            )
        )
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence_path.write_text(evidence, encoding="utf-8")
        return {
            "condition": packet["condition"],
            "scenario": packet["scenario"],
            "expected_sdk": environment["dotnet_sdk"],
            "selected_sdk": selected_sdk,
            "windows_app_sdk": environment["windows_app_sdk"],
            "exit_code": completed.returncode,
            "evidence": evidence_path.relative_to(repo_root).as_posix(),
        }
    finally:
        shutil.rmtree(control_root, ignore_errors=True)


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
    errors.extend(_validate_run_environment(repo_root, run_values))
    verification_path = packet_dir / "evidence/verification.json"
    verification_errors = load_and_validate(verification_path)
    errors.extend(f"verification: {error}" for error in verification_errors)
    errors.extend(
        _validate_controlled_build(
            repo_root, packet_dir, run_values, verification_path
        )
    )
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
        evidence_files = _file_hashes(temp / "evidence") if (temp / "evidence").is_dir() else []
        for item in changed:
            source = packet_dir / "project" / item["path"]
            target = temp / "generated" / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        capture: dict[str, Any] = {
            "schema_version": CAPTURE_SCHEMA_VERSION,
            "condition": packet["condition"],
            "scenario": packet["scenario"],
            "prompt_sha256": _sha256(temp / "PROMPT.md"),
            "packet_sha256": _sha256(temp / "PACKET.json"),
            "run_sha256": _sha256(temp / "RUN.md"),
            "generated_files": changed,
            "deleted_files": deleted,
            "evidence_files": evidence_files,
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
    prefix = f"{condition}/{scenario_name}"
    if not isinstance(packet, dict):
        return {}, [f"{prefix}: PACKET.json must be an object"]
    if not isinstance(capture, dict):
        return {}, [f"{prefix}: CAPTURE.json must be an object"]
    if set(packet) != PACKET_FIELDS:
        errors.append(f"{prefix}: PACKET.json contract fields differ")
    if packet.get("schema_version") != PACKET_SCHEMA_VERSION:
        errors.append(
            f"{prefix}: PACKET.json schema_version must be {PACKET_SCHEMA_VERSION}"
        )
    if set(capture) != CAPTURE_FIELDS:
        errors.append(f"{prefix}: CAPTURE.json contract fields differ")
    if capture.get("schema_version") != CAPTURE_SCHEMA_VERSION:
        errors.append(
            f"{prefix}: CAPTURE.json schema_version must be {CAPTURE_SCHEMA_VERSION}"
        )

    scenario = matrix["scenarios"][scenario_name]
    input_commit = matrix["input_commit"]
    start = matrix["start_project"]
    if packet.get("condition") != condition or packet.get("scenario") != scenario_name:
        errors.append(f"{prefix}: PACKET.json identity mismatch")
    if capture.get("condition") != condition or capture.get("scenario") != scenario_name:
        errors.append(f"{prefix}: CAPTURE.json identity mismatch")
    if packet.get("input_commit") != input_commit:
        errors.append(f"{prefix}: input commit mismatch")
    prompt_path = result_dir / "PROMPT.md"
    packet_path = result_dir / "PACKET.json"
    run_path = result_dir / "RUN.md"
    if not prompt_path.is_file() or capture.get("prompt_sha256") != _sha256(prompt_path):
        errors.append(f"{prefix}: captured prompt differs")
    if not packet_path.is_file() or capture.get("packet_sha256") != _sha256(packet_path):
        errors.append(f"{prefix}: captured packet metadata differs")
    if not run_path.is_file() or capture.get("run_sha256") != _sha256(run_path):
        errors.append(f"{prefix}: captured run record differs")
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
    captured_generated = capture.get("generated_files")
    actual_generated = (
        _file_hashes(result_dir / "generated")
        if (result_dir / "generated").is_dir()
        else []
    )
    if captured_generated != actual_generated:
        errors.append(f"{prefix}: captured generated files differ")
    captured_evidence = capture.get("evidence_files")
    actual_evidence = (
        _file_hashes(result_dir / "evidence")
        if (result_dir / "evidence").is_dir()
        else []
    )
    if captured_evidence != actual_evidence:
        errors.append(f"{prefix}: captured evidence files differ")
    run_values, run_errors = _parse_run_record(result_dir / "RUN.md")
    errors.extend(f"{prefix}: {error}" for error in run_errors)
    errors.extend(_validate_run_environment(repo_root, run_values, prefix))
    verification_path = result_dir / "evidence/verification.json"
    verification_errors = load_and_validate(verification_path)
    errors.extend(f"{prefix}: verification: {error}" for error in verification_errors)
    errors.extend(
        _validate_controlled_build(
            repo_root, result_dir, run_values, verification_path, prefix
        )
    )
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
    build = subparsers.add_parser("build")
    build.add_argument("--packet", type=Path, required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--packet", type=Path, required=True)
    capture.add_argument("--destination", type=Path, required=True)
    inspect_one = subparsers.add_parser("inspect-packet")
    inspect_one.add_argument("--packet", type=Path, required=True)
    inspect_one.add_argument(
        "--condition", choices=("baseline", "guided"), required=True
    )
    inspect_one.add_argument(
        "--scenario", choices=tuple(sorted(EXPECTED_SCENARIOS)), required=True
    )
    inspect = subparsers.add_parser("inspect-packets")
    inspect.add_argument("--root", type=Path, default=Path("evaluation/.runs"))
    validate_completed = subparsers.add_parser("validate-results")
    validate_completed.add_argument("--root", type=Path, default=Path("evaluation"))
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if args.command == "validate":
        errors = validate_matrix(repo_root)
        success = "evaluation run matrix passed"
    elif args.command == "validate-results":
        results_root = args.root if args.root.is_absolute() else repo_root / args.root
        errors = validate_results(repo_root, results_root)
        success = "evaluation results passed"
    elif args.command == "build":
        packet = args.packet if args.packet.is_absolute() else repo_root / args.packet
        build_result = build_packet(repo_root, packet)
        print(json.dumps(build_result, ensure_ascii=False, indent=2))
        return 0 if build_result["exit_code"] == 0 else 2
    elif args.command == "inspect-packet":
        packet = args.packet if args.packet.is_absolute() else repo_root / args.packet
        status = inspect_packet(
            repo_root, packet, args.condition, args.scenario
        )
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 1 if status["status"] in {"stale", "missing"} else 0
    elif args.command == "inspect-packets":
        packets_root = args.root if args.root.is_absolute() else repo_root / args.root
        statuses = inspect_packets(repo_root, packets_root)
        counts = {
            status: sum(item["status"] == status for item in statuses)
            for status in ("ready", "in_progress", "capture_ready", "stale", "missing")
        }
        print(
            json.dumps(
                {"schema_version": 1, "summary": counts, "packets": statuses},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1 if counts["stale"] or counts["missing"] else 0
    elif args.command == "prepare":
        destination = (
            args.destination
            if args.destination.is_absolute()
            else repo_root / args.destination
        )
        manifest = prepare_run_packet(
            repo_root, args.condition, args.scenario, destination
        )
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    else:
        packet = args.packet if args.packet.is_absolute() else repo_root / args.packet
        destination = (
            args.destination
            if args.destination.is_absolute()
            else repo_root / args.destination
        )
        capture_manifest = capture_run(repo_root, packet, destination)
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
