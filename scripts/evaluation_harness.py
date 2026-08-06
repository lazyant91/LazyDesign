#!/usr/bin/env python3
"""Prepare immutable-input packets for controlled LazyDesign evaluation runs."""

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


def _load_matrix(repo_root: Path) -> dict[str, Any]:
    return json.loads((repo_root / MATRIX_PATH).read_text(encoding="utf-8-sig"))


def _safe_repo_path(repo_root: Path, relative: str) -> Path:
    candidate = (repo_root / relative).resolve()
    if not candidate.is_relative_to(repo_root.resolve()):
        raise ValueError(f"path escapes repository: {relative}")
    return candidate


def _git_object_exists(repo_root: Path, object_name: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", object_name],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def validate_matrix(repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        matrix = _load_matrix(repo_root)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load {MATRIX_PATH}: {exc}"]

    if matrix.get("schema_version") != 1:
        errors.append("run matrix schema_version must be 1")
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
            prompt_path = _safe_repo_path(repo_root, prompt)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if not prompt_path.is_file():
                errors.append(f"missing prompt: {prompt}")
        if not references or len(references) != len(set(references)):
            errors.append(f"guided reference set is empty or duplicated: {name}")
        for relative in references:
            try:
                reference_path = _safe_repo_path(repo_root, relative)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if not reference_path.is_file():
                    errors.append(f"missing guided reference: {relative}")
    return errors


def _extract_project(repo_root: Path, commit: str, project_path: str, destination: Path) -> None:
    archive = subprocess.run(
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
    destination = destination.resolve()
    if not destination.is_relative_to(repo_root.resolve()):
        raise ValueError("run packet destination must remain inside the repository workspace")
    if destination.exists():
        raise FileExistsError(f"run packet already exists: {destination}")

    temp = destination.with_name(f".{destination.name}.tmp-{uuid.uuid4().hex}")
    try:
        temp.mkdir(parents=True)
        start = matrix["start_project"]
        scenario = matrix["scenarios"][scenario_name]
        _extract_project(repo_root, start["commit"], start["path"], temp / "project")
        prompt_source = _safe_repo_path(repo_root, scenario["prompt"])
        shutil.copyfile(prompt_source, temp / "PROMPT.md")

        references: list[dict[str, str]] = []
        if condition == "guided":
            for relative in scenario["guided_references"]:
                source = _safe_repo_path(repo_root, relative)
                target = temp / "context" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                references.append({"path": relative, "sha256": _sha256(source)})

        manifest: dict[str, Any] = {
            "schema_version": 1,
            "condition": condition,
            "scenario": scenario_name,
            "start_project_commit": start["commit"],
            "start_project_path": start["path"],
            "content_width_dip": scenario["content_width_dip"],
            "prompt_path": scenario["prompt"],
            "prompt_sha256": _sha256(prompt_source),
            "references": references,
        }
        (temp / "PACKET.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (temp / "RUN.template.md").write_text(
            _run_template(manifest), encoding="utf-8"
        )
        temp.rename(destination)
        return manifest
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def _run_template(manifest: dict[str, Any]) -> str:
    supplied = "none" if not manifest["references"] else "\n".join(
        f"- {item['path']} ({item['sha256']})" for item in manifest["references"]
    )
    return f"""# Evaluation Run Record

Condition: {manifest['condition']}
Scenario: {manifest['scenario']}
Run date and local time: record after generation
Model identifier: record before generation
Reasoning level: record before generation
Starting project repository and SHA: lazyant91/LazyDesign {manifest['start_project_commit']}
Operating system: record before generation
.NET SDK: record before generation
Windows App SDK package: 2.0.1
Tool access: record before generation
Network access: record before generation
Reference files supplied:
{supplied}
Generation intervention: none | record exact intervention
Generated file list: record after generation
Generation completion status: record after generation
Build command: not performed
Build result: not performed
Rendered checks performed: not performed
Checks not performed: record after verification
Notes: packet hashes are recorded in PACKET.json
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--condition", choices=("baseline", "guided"), required=True)
    prepare.add_argument("--scenario", choices=tuple(sorted(EXPECTED_SCENARIOS)), required=True)
    prepare.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if args.command == "validate":
        errors = validate_matrix(repo_root)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("evaluation run matrix passed")
        return 0
    manifest = prepare_run_packet(repo_root, args.condition, args.scenario, args.destination)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

