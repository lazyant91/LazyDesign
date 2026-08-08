# Evaluation Execution Reliability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Do not dispatch subagents for this repository unless the user explicitly authorizes them.

**Goal:** Add a backward-compatible Gate v3 execution-validity prerequisite so infrastructure-interrupted generation attempts are captured but cannot be scored as model-quality results.

**Architecture:** Keep historical matrix schema 1 and packet/capture schema 2 unchanged. Matrix schema 2 opts into a controller-reconciled generation-attempt record, packet/capture validation of that record, a six-run `validate-execution` readiness command, and report refusal with an INCOMPLETE exit when any attempt is infrastructure-invalid. The generation-attempt validator lives in a focused module; the existing harness owns matrix/packet/capture integration and the report layer owns score-output blocking.

**Tech Stack:** Python 3 standard library, `unittest`, existing LazyDesign evaluation harness, Git-pinned WinUI fixture metadata.

## Global Constraints

- Repository: `Z:\workspace\LazyDesign` (`lazyant91/LazyDesign`).
- Branch: `test/v0.1-evaluation-reliability`.
- Do not modify or rescore `evaluation/baseline/`, `evaluation/guided/`, `evaluation/results/`, or `evaluation/revisions/v0.1-r1/`.
- Keep `evaluation/run-matrix.json` and `evaluation/revisions/v0.1-r1/run-matrix.json` schema 1 and byte semantics unchanged.
- Matrix schema 2 must require `execution_contract: controller-reconciled-v1`.
- Schema-2 matrices must pin a fixture commit whose `App.xaml` contains `XamlControlsResources`.
- One experiment version has exactly six fresh attempts and no replacement-selection loop.
- `valid` model failures remain scoreable; only material external infrastructure interruption is `infrastructure_invalid`.
- Preserve the preexisting untracked `evaluation/rehearsal/` directory.
- Use TDD: every production behavior begins with a failing test that fails for the intended reason.

---

### Task 1: Add matrix schema 2 and corrected-fixture validation

**Files:**
- Modify: `scripts/evaluation_harness.py`
- Modify: `tests/test_evaluation_harness.py`

**Interfaces:**
- Consumes: existing `validate_matrix(repo_root, matrix_path)` and `_git_file_bytes(...)`.
- Produces: `validate_matrix` accepts schema 1 or schema 2; schema 2 requires `execution_contract == "controller-reconciled-v1"` and a pinned `App.xaml` containing `XamlControlsResources`.

- [ ] **Step 1: Write failing schema-2 matrix tests**

Add test helpers that clone the default matrix into a temporary file, set `schema_version = 2`, set `execution_contract`, and set `start_project.commit` to the current committed `HEAD` so the test uses the already-corrected fixture without hard-coding a branch-only SHA.

Add tests:

```python
def test_schema2_matrix_requires_execution_contract(self) -> None:
    ...
    self.assertTrue(any("execution_contract" in error for error in errors))


def test_schema2_matrix_requires_xaml_controls_resources_in_pinned_fixture(self) -> None:
    ...
    matrix["start_project"]["commit"] = START_SHA
    ...
    self.assertTrue(any("XamlControlsResources" in error for error in errors))


def test_schema2_matrix_accepts_corrected_committed_fixture(self) -> None:
    ...
    self.assertEqual([], validate_matrix(ROOT, matrix_path))
```

- [ ] **Step 2: Run only the new matrix tests and verify RED**

Run:

```powershell
python -m unittest discover -s tests -p "test_evaluation_harness.py" -k schema2_matrix -v
```

Expected: FAIL because `validate_matrix` currently rejects every schema other than 1 and does not validate the execution-contract or fixture resource dictionary.

- [ ] **Step 3: Implement minimal matrix-version helpers**

In `scripts/evaluation_harness.py`:

```python
EXECUTION_CONTRACT = "controller-reconciled-v1"


def _matrix_schema_version(matrix: dict[str, Any]) -> int | None:
    value = matrix.get("schema_version")
    return value if isinstance(value, int) and not isinstance(value, bool) else None
```

Update `validate_matrix` to accept only versions `{1, 2}`. For version 1, reject an execution contract if present only if it conflicts with the historical exact-field assumptions already enforced elsewhere; do not require a new field. For version 2, require the exact execution contract.

After validating `start_project.commit` and `start_project.path`, load `<path>/App.xaml` from the pinned commit, parse it with `ElementTree`, locate `Application.Resources`, and require a child whose tag ends with `XamlControlsResources`.

- [ ] **Step 4: Run schema-2 and historical matrix tests GREEN**

Run:

```powershell
python -m unittest discover -s tests -p "test_evaluation_harness.py" -k "matrix" -v
python scripts/evaluation_harness.py validate
python scripts/evaluation_harness.py validate --matrix evaluation/revisions/v0.1-r1/run-matrix.json
```

Expected: new tests PASS; both historical matrix commands exit 0.

- [ ] **Step 5: Commit**

```powershell
git add scripts/evaluation_harness.py tests/test_evaluation_harness.py
git commit -m "test: add schema2 execution matrix contract"
```

---

### Task 2: Add generation-attempt evidence validation

**Files:**
- Create: `scripts/evaluation_execution.py`
- Create: `tests/test_evaluation_execution.py`

**Interfaces:**
- Produces: `generation_attempt_template(condition: str, scenario: str) -> dict[str, Any]`.
- Produces: `validate_generation_attempt(record: Any, evidence_root: Path, *, condition: str, scenario: str, changed: list[str], deleted: list[str]) -> list[str]`.
- Produces: `load_and_validate_generation_attempt(path: Path, *, condition: str, scenario: str, changed: list[str], deleted: list[str]) -> list[str]`.

- [ ] **Step 1: Write failing validator tests**

Create tests covering these exact behaviors:

```python
def test_valid_model_result_can_stop_before_stopping_condition(self): ...
def test_valid_attempt_rejects_non_none_blocker(self): ...
def test_infrastructure_invalid_requires_blocker_and_evidence(self): ...
def test_evidence_path_must_exist_inside_evidence_directory(self): ...
def test_project_delta_must_match_controller_delta(self): ...
def test_condition_and_scenario_must_match_packet(self): ...
```

Use real temporary evidence files. No mocks.

- [ ] **Step 2: Run the new test file and verify RED**

Run:

```powershell
python -m unittest discover -s tests -p "test_evaluation_execution.py" -v
```

Expected: import failure because `scripts/evaluation_execution.py` does not exist.

- [ ] **Step 3: Implement the minimal focused validator module**

Use constants:

```python
VALIDITIES = {"valid", "infrastructure_invalid"}
BLOCKERS = {
    "none",
    "remote_safety_inspection",
    "remote_transport",
    "tool_timeout",
    "other_infrastructure",
}
ATTEMPT_FIELDS = {
    "schema_version",
    "condition",
    "scenario",
    "validity",
    "blocker",
    "stopping_condition_reached",
    "project_delta",
    "evidence",
    "reason",
}
```

Require exact fields, schema version 1, boolean stopping-condition value, exact project-delta keys `changed` and `deleted`, sorted unique non-empty relative paths, exact match with controller-provided changed/deleted lists, non-empty reason, and safe existing evidence entries with exactly `path` and `detail`.

The template may contain explicit `record after generation` marker strings because it is a preparation artifact, not a completed record.

- [ ] **Step 4: Run generation-attempt tests GREEN**

Run:

```powershell
python -m unittest discover -s tests -p "test_evaluation_execution.py" -v
```

Expected: all new tests PASS.

- [ ] **Step 5: Commit**

```powershell
git add scripts/evaluation_execution.py tests/test_evaluation_execution.py
git commit -m "test: validate generation attempt evidence"
```

---

### Task 3: Integrate generation-attempt evidence into schema-2 packet and capture flow

**Files:**
- Modify: `scripts/evaluation_harness.py`
- Modify: `tests/test_evaluation_harness.py`

**Interfaces:**
- Consumes: Task 2 generation-attempt functions.
- Produces: schema-2 `prepare_run_packet` adds `evidence/generation-attempt.template.json`; schema 1 does not.
- Produces: schema-2 `inspect_packet` and `capture_run` require a valid `evidence/generation-attempt.json` whose delta matches the actual project delta.
- Produces: schema-2 captured result validation checks the immutable captured generation-attempt record.

- [ ] **Step 1: Write failing packet/capture tests**

Add tests:

```python
def test_schema1_prepare_does_not_add_generation_attempt_template(self): ...
def test_schema2_prepare_adds_generation_attempt_template(self): ...
def test_schema2_inspect_requires_generation_attempt_before_capture_ready(self): ...
def test_schema2_capture_accepts_infrastructure_invalid_attempt(self): ...
def test_schema2_capture_rejects_generation_attempt_delta_mismatch(self): ...
def test_schema2_validate_results_rejects_modified_generation_attempt(self): ...
```

Build a temporary schema-2 matrix with current committed HEAD as its corrected start-project commit. Reuse existing `complete_run(...)` helpers, extending them only when the test explicitly opts into schema 2.

- [ ] **Step 2: Run the new schema-2 packet tests and verify RED**

Run:

```powershell
python -m unittest discover -s tests -p "test_evaluation_harness.py" -k "generation_attempt" -v
```

Expected: FAIL because preparation/inspection/capture currently know only verification evidence.

- [ ] **Step 3: Implement schema-aware packet integration**

Import Task 2 helpers in `evaluation_harness.py` with the same direct-script fallback pattern used for `evaluation_evidence`.

Add:

```python
def _uses_execution_contract(matrix: dict[str, Any]) -> bool:
    return matrix.get("schema_version") == 2
```

For schema 2 only:

- write the exact generation-attempt template during preparation;
- validate that template in `_validate_packet`;
- exclude the template from `_packet_activity` but count completed `generation-attempt.json` as evidence activity;
- in `inspect_packet`, load and validate the completed record using controller-derived changed/deleted paths before returning `capture_ready`;
- in capture/result validation, validate the copied record and rely on existing capture hashing to detect later modification.

Do not change `PACKET_SCHEMA_VERSION` or `CAPTURE_SCHEMA_VERSION`.

- [ ] **Step 4: Run targeted and historical regression tests GREEN**

Run:

```powershell
python -m unittest discover -s tests -p "test_evaluation_harness.py" -k "generation_attempt" -v
python -m unittest discover -s tests -p "test_evaluation_harness.py" -k "initial_and_revision_matrices_are_valid" -v
python scripts/evaluation_harness.py validate-results --root evaluation
python scripts/evaluation_harness.py validate-results --root evaluation/revisions/v0.1-r1 --matrix evaluation/revisions/v0.1-r1/run-matrix.json
```

Expected: all exit 0.

- [ ] **Step 5: Commit**

```powershell
git add scripts/evaluation_harness.py tests/test_evaluation_harness.py
git commit -m "test: capture controller reconciled attempts"
```

---

### Task 4: Add six-run execution readiness and Gate v3 report blocking

**Files:**
- Modify: `scripts/evaluation_harness.py`
- Modify: `scripts/evaluation_report.py`
- Modify: `tests/test_evaluation_harness.py`
- Modify: `tests/test_evaluation_report.py`
- Modify: `evaluation/README.md`
- Modify: `README.md`
- Modify: `DESIGN.md`

**Interfaces:**
- Produces: `execution_readiness(repo_root: Path, results_root: Path, matrix_path: Path = MATRIX_PATH) -> tuple[dict[str, Any], list[str]]`.
- CLI: `evaluation_harness.py validate-execution --root ... --matrix ...` exits 0 ready, 2 incomplete, 1 malformed/invalid.
- Produces: `ExecutionIncompleteError(ValueError)` in `evaluation_report.py`; CLI maps it to exit 3 without writing score/findings/gate files.

- [ ] **Step 1: Write failing readiness tests**

Add harness tests that materialize six schema-2 result cells containing generation-attempt records and assert:

```python
def test_execution_readiness_is_ready_for_six_valid_attempts(self): ...
def test_execution_readiness_is_incomplete_for_infrastructure_invalid_attempt(self): ...
def test_validate_execution_cli_returns_two_for_incomplete_experiment(self): ...
def test_execution_readiness_rejects_schema1_matrix(self): ...
```

The readiness summary must list `condition`, `scenario`, and `blocker` for every invalid cell in deterministic order.

- [ ] **Step 2: Run readiness tests and verify RED**

Run:

```powershell
python -m unittest discover -s tests -p "test_evaluation_harness.py" -k "execution_readiness" -v
```

Expected: FAIL because the function and command do not exist.

- [ ] **Step 3: Implement readiness and CLI semantics**

Implement `execution_readiness` for schema 2 only. Structural validation errors return a non-empty errors list. Otherwise return:

```python
{
    "status": "ready" | "incomplete",
    "invalid_attempts": [
        {"condition": "...", "scenario": "...", "blocker": "..."}
    ],
}
```

Add `validate-execution` parser arguments identical to `validate-results`. CLI behavior:

- errors -> print `ERROR:` lines and return 1;
- incomplete -> print JSON summary and return 2;
- ready -> print JSON summary and return 0.

- [ ] **Step 4: Write failing report-blocking tests**

Add real-file tests that use a temporary schema-2 matrix and six generation-attempt records:

```python
def test_schema2_report_refuses_infrastructure_incomplete_experiment(self): ...
def test_schema2_report_allows_six_valid_attempts_when_other_validation_is_disabled_for_fixture_test(self): ...
```

The incomplete test must assert the output directory is not created or changed.

- [ ] **Step 5: Implement report blocking**

Import `execution_readiness` and add:

```python
class ExecutionIncompleteError(ValueError):
    pass
```

In `write_reports`, load the selected matrix. When matrix schema is 2, check execution readiness before metric evidence or report writes. If incomplete, raise `ExecutionIncompleteError` with the invalid cell list. In `main`, catch this class before the generic validation exception, print an `INCOMPLETE:` message, and return exit code 3.

Schema-1 report behavior and Gate v1/v2 exit codes stay unchanged.

- [ ] **Step 6: Update operating documentation**

Document:

- controller performs `inspect-packet` before handing work to the fresh generation context;
- fresh generation context no longer executes that harness preflight in schema-2 experiments;
- controller writes `generation-attempt.json` from observed infrastructure outcome plus reconciled disk delta;
- any infrastructure-invalid cell makes Gate v3 incomplete;
- a rerun is a new matrix version with six fresh contexts, never a replacement attempt inside the same experiment.

- [ ] **Step 7: Run full verification**

Run:

```powershell
python scripts/check_reference.py
python -m py_compile scripts/check_reference.py scripts/evaluation_evidence.py scripts/evaluation_execution.py scripts/evaluation_gate.py scripts/evaluation_harness.py scripts/evaluation_report.py tests/test_evaluation_evidence.py tests/test_evaluation_execution.py tests/test_evaluation_gate.py tests/test_evaluation_harness.py tests/test_evaluation_report.py
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/evaluation_harness.py validate
python scripts/evaluation_harness.py validate --matrix evaluation/revisions/v0.1-r1/run-matrix.json
python scripts/evaluation_harness.py validate-results --root evaluation
python scripts/evaluation_harness.py validate-results --root evaluation/revisions/v0.1-r1 --matrix evaluation/revisions/v0.1-r1/run-matrix.json
python scripts/evaluation_report.py evaluation/results/metrics.json --output-dir evaluation/results
python scripts/evaluation_report.py evaluation/revisions/v0.1-r1/results/metrics.json --output-dir evaluation/revisions/v0.1-r1/results --matrix evaluation/revisions/v0.1-r1/run-matrix.json
git diff --check
```

Expected:

- reference, compile, all tests, both matrix validations, and both result validations pass;
- historical Gate v1 and Gate v2 report commands retain their valid FAIL exit 2;
- no historical scored artifact changes;
- only preexisting `evaluation/rehearsal/` remains untracked after the final commit.

- [ ] **Step 8: Commit**

```powershell
git add scripts/evaluation_harness.py scripts/evaluation_report.py tests/test_evaluation_harness.py tests/test_evaluation_report.py evaluation/README.md README.md DESIGN.md
git commit -m "test: block scoring on invalid execution attempts"
```
