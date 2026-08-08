# LazyDesign Evaluation Execution Reliability Design

## Goal

Prevent infrastructure-blocked generation attempts from being interpreted as model-quality failures or improvements while preserving every observed attempt and the existing v0.1 / v0.1-r1 history unchanged.

## Problem statement

The v0.1-r1 experiment exposed two independent confounders.

First, several fresh Temporary Chat runs were interrupted by Remote safety inspection rather than by the model's implementation decision. Baseline device-list could not write source, guided failure-confirmation could not execute its mandatory pre-generation harness command, and baseline failure-confirmation reported no generation even though controller reconciliation found a partial source change on disk. Scoring those attempts as ordinary generated results made the baseline/guided totals difficult to interpret.

Second, two build-passing runs crashed during XAML load because the historical WinUI start fixture omitted `XamlControlsResources`. That fixture issue is corrected separately in the working tree and documented in `evaluation/investigations/2026-08-08-runtime-startup.md`.

This design addresses only the execution-validity problem. It must not rescore or rewrite any existing capture.

## Design principles

1. **Controller observation is authoritative.** The model's report is evidence, but actual packet disk state determines the generated file delta.
2. **Infrastructure interruption is not model quality.** A platform, connector, transport, or tool-safety block that materially interrupts generation makes that attempt invalid for scoring.
3. **Model failure remains a valid result.** Bad XAML, build failure, incomplete implementation, or a model choosing to stop without an infrastructure blocker remains scoreable.
4. **No success-selection retry loop.** One experiment version uses exactly one fresh generation attempt for each of the six condition/scenario cells. An infrastructure-invalid cell makes that experiment version incomplete.
5. **Retries require a new experiment version.** A later rerun uses a new versioned matrix and six fresh contexts; it never replaces, deletes, or silently selects over the prior attempt.
6. **Historical contracts remain reproducible.** Existing matrix schema 1, packet contract 2, v0.1 results, and v0.1-r1 results retain their current behavior.
7. **Generator-side preflight is minimized.** The controller performs packet inspection before the fresh Temporary Chat starts. The generation context is not required to execute `evaluation_harness.py inspect-packet` itself.

## Alternatives considered

### Keep scoring all interrupted attempts

Rejected. It preserves data but conflates connector/platform behavior with model quality and can inflate or depress baseline/guided differences.

### Retry an interrupted cell until one attempt succeeds

Rejected. Selecting the first technically successful attempt while discarding or de-emphasizing earlier attempts introduces selection bias and makes the effective number of model attempts differ across cells.

### Mark interrupted attempts invalid and make the experiment incomplete

Selected. It preserves the observed failure, prevents invalid scoring, and keeps the experimental unit simple: exactly six attempts per version.

## Versioned execution contract

A new run matrix schema version `2` activates the execution-validity contract. Matrix schema version `1` continues to mean the historical behavior.

A schema-2 matrix keeps the existing fields and adds:

```json
{
  "schema_version": 2,
  "execution_contract": "controller-reconciled-v1"
}
```

`execution_contract` must equal `controller-reconciled-v1` for schema 2. No path-based or newest-version auto-detection is allowed; every non-default revision continues to pass `--matrix` explicitly.

## Generation-attempt evidence

For schema-2 matrices, packet preparation adds:

`evidence/generation-attempt.template.json`

After the fresh generation context returns, the controller creates:

`evidence/generation-attempt.json`

The record uses schema version `1`:

```json
{
  "schema_version": 1,
  "condition": "guided",
  "scenario": "device-list",
  "validity": "valid",
  "blocker": "none",
  "stopping_condition_reached": true,
  "project_delta": {
    "changed": ["MainWindow.xaml", "MainWindow.xaml.cs"],
    "deleted": []
  },
  "evidence": [
    {
      "path": "generation-report.txt",
      "detail": "Fresh generation context returned normally."
    }
  ],
  "reason": "No infrastructure blocker interrupted generation."
}
```

Allowed `validity` values:

- `valid`
- `infrastructure_invalid`

Allowed `blocker` values:

- `none`
- `remote_safety_inspection`
- `remote_transport`
- `tool_timeout`
- `other_infrastructure`

Rules:

- `valid` requires `blocker: none`.
- `infrastructure_invalid` requires a blocker other than `none` and at least one evidence entry.
- `stopping_condition_reached` records whether the configured generation stopping condition was actually reached; it does not by itself decide validity.
- A model result may be `valid` with `stopping_condition_reached: false` when no infrastructure failure caused the stop.
- `project_delta` is not trusted from the model. The harness derives the current packet delta and requires an exact match before capture.
- Evidence paths must remain under the packet/result `evidence/` directory and exist before capture.

## Controller flow

For each of the six cells in a schema-2 experiment:

1. Controller prepares a new packet.
2. Controller runs `inspect-packet` and requires `ready` before opening the fresh generation context.
3. Fresh generation context may read only the already-approved generation inputs and may modify only `project/` according to the fixed experiment rules.
4. The generation context does not run the harness preflight command.
5. After the context returns, controller inspects the packet and reconciles the actual project delta.
6. Controller records `generation-attempt.json` from observed tool outcomes plus disk state.
7. Controlled build and runtime verification proceed only according to the existing immutable-source rules. An infrastructure-invalid generation attempt may still be captured for evidence, but it is never score-ready.
8. Capture hashes `generation-attempt.json` with the rest of the evidence.

## Ambiguous partial writes

A safety or transport block can occur after a write has partially succeeded. The controller must preserve the actual disk state and record the exact derived delta. If the infrastructure event materially prevented the generation context from completing normally, validity remains `infrastructure_invalid` even when one or more source files changed.

This directly covers the v0.1-r1 baseline failure-confirmation pattern where the model report and observed disk state disagreed.

## Execution-readiness gate

The harness gains a separate command:

```powershell
python scripts/evaluation_harness.py validate-execution --root <result-root> --matrix <schema-2-matrix>
```

Return codes:

- `0`: all six captured attempts are structurally valid and have `validity: valid`;
- `2`: captures are structurally valid but at least one attempt is `infrastructure_invalid`; the experiment is `INCOMPLETE` for scoring;
- `1`: matrix, capture, hash, generation-attempt schema, evidence, or cross-run contract is invalid.

The command reports every invalid cell and blocker. It does not delete, retry, repair, or select another attempt.

## Gate behavior

For a schema-2 matrix, report generation must run execution readiness before reading score metrics.

- readiness `0`: continue with the existing Gate v2 quality formula and guided-build prerequisite;
- readiness `2`: do not generate or update score/findings reports and return an execution-incomplete status;
- readiness `1`: treat the evaluation data as invalid.

Existing schema-1 matrices bypass this new prerequisite and continue reproducing Gate v1/v2 behavior exactly.

The new execution prerequisite is referred to as **Gate v3** in future evaluation plans: execution validity first, then the existing quality conditions.

## Fixture requirement for future matrices

Any future schema-2 matrix must pin a start-project commit that contains the corrected `evaluation/fixtures/winui-start/App.xaml` with `XamlControlsResources`. The existing v0.1 and v0.1-r1 matrices continue pinning their historical fixture commit and are not edited.

The matrix validator for schema 2 must verify the pinned fixture's `App.xaml` contains `XamlControlsResources` so a future matrix cannot accidentally reintroduce the known startup confounder.

## Backward compatibility

The implementation must keep all existing commands and artifacts valid:

- `evaluation/run-matrix.json` schema 1 remains valid;
- `evaluation/revisions/v0.1-r1/run-matrix.json` schema 1 remains valid;
- packet schema version 2 remains unchanged for those matrices;
- their prepared packet shape does not gain generation-attempt templates;
- their six captured result sets continue passing `validate-results`;
- Gate v1 and Gate v2 report regeneration retains current exit codes and content semantics.

No migration of historical captures is permitted.

## Error handling

The harness must reject:

- schema-2 matrices without the exact execution-contract identifier;
- unknown validity or blocker values;
- a `valid` attempt with a non-`none` blocker;
- an `infrastructure_invalid` attempt with blocker `none`;
- an invalid attempt with no evidence;
- project-delta metadata that differs from the packet's actual source delta;
- evidence references that escape `evidence/` or do not exist;
- schema-2 capture without `generation-attempt.json`;
- schema-2 future fixture commits that omit `XamlControlsResources`.

## Testing strategy

TDD coverage must prove:

1. historical schema-1 matrices still validate and prepare byte-compatible packet contracts;
2. schema-2 matrix validation requires `execution_contract` and the corrected fixture resource dictionary;
3. schema-2 prepare creates the generation-attempt template while schema 1 does not;
4. generation-attempt validation accepts a valid model result even when the stopping condition is false;
5. infrastructure-invalid evidence requires a concrete blocker and evidence file;
6. controller-derived project delta overrides contradictory model reporting and must match the structured record;
7. capture accepts and preserves an infrastructure-invalid attempt without making it score-ready;
8. `validate-execution` returns 0 for six valid captures, 2 for structurally valid infrastructure-invalid captures, and 1 for malformed evidence;
9. report generation for schema 2 refuses to score an incomplete experiment;
10. all existing 72 tests and historical result validations remain green.

## Success criteria

The execution-reliability work is complete when a future schema-2 experiment cannot produce a quality Gate decision from infrastructure-interrupted generation attempts, while the completed v0.1 and v0.1-r1 experiments remain mechanically reproducible and immutable.
