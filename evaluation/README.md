# LazyDesign v0.1 Evaluation

This directory defines the controlled comparison used to decide whether the v0.1 reference improves agent-generated WinUI 3 UI.

## Experimental question

Does providing only the relevant LazyDesign component and foundation pages reduce observable WinUI component defects without increasing unnecessary XAML or complexity?

## Conditions

Each scenario is run twice.

### Baseline

- exact scenario prompt;
- clean WinUI 3 starting project;
- no LazyDesign content;
- no extra design guidance.

### Guided

- the same exact scenario prompt;
- the exact same starting project SHA;
- `DESIGN.md`;
- only the component and foundation pages listed for that scenario;
- no unrelated LazyDesign pages or extra design guidance.

The supplied reference set is the only experimental difference.

## Required controls

Every baseline/guided pair must use:

- the same model family and exact model identifier where available;
- the same reasoning level;
- a fresh context for every run;
- the same task prompt bytes;
- the same starting project SHA;
- the same tool permissions;
- the same network-access policy;
- the same generation stopping condition;
- no prompt repair or implementation correction during generation.

Network access must be disabled during all generation runs unless it is deliberately enabled for both members of every pair and recorded.

A model-caused run that fails to generate or build is still a result. Preserve it without repair before scoring. For future schema-2 experiments, a material external infrastructure interruption is also preserved, but it is recorded as `infrastructure_invalid` and makes the six-run experiment `INCOMPLETE` before scoring rather than counting as model quality.

## Scenario reference sets

### Connection settings

```text
DESIGN.md
foundations/text-and-localization.md
foundations/sizing-and-spacing.md
foundations/states-and-themes.md
foundations/accessibility-basics.md
components/button.md
components/textbox.md
components/toggleswitch.md
components/combobox.md
```

### Device list

```text
DESIGN.md
foundations/text-and-localization.md
foundations/sizing-and-spacing.md
foundations/icons.md
foundations/states-and-themes.md
foundations/accessibility-basics.md
components/button.md
components/commandbar.md
components/listview.md
```

### Failure and confirmation

```text
DESIGN.md
foundations/text-and-localization.md
foundations/sizing-and-spacing.md
foundations/icons.md
foundations/states-and-themes.md
foundations/accessibility-basics.md
components/button.md
components/infobar.md
components/contentdialog.md
```

## Run directory contract

Each condition/scenario directory must contain:

- `PROMPT.md` — an exact copy of the fixed prompt;
- `RUN.md` — immutable run metadata and verification record;
- generated XAML and C# files, or a patch that reconstructs them exactly;
- build output or a concise build-failure excerpt;
- rendered observations only when the UI was actually run.

`RUN.md` must record:

```text
Condition:
Scenario:
Run date and local time:
Model identifier:
Reasoning level:
Fresh context:
Generation stopping condition:
Starting project repository and SHA:
Operating system:
.NET SDK:
Windows App SDK package:
Tool access:
Network access:
Reference files supplied:
Generation intervention: none | description
Generated file list:
Generation completion status:
Build command:
Build result:
Rendered checks performed:
Checks not performed:
Notes:
```

Do not leave a field blank. Use `not performed`, `not available`, or `not applicable` only for free-text fields where the contract permits them. The four artifact/verification fields supplied by `expected_run_metadata` must use those exact values instead.

## Verification layers

Report these as independent results:

1. **Static review** — source structure and rubric observations.
2. **Build** — exact command, configuration, target architecture, and result.
3. **Rendered runtime** — application launched and target screen displayed.
4. **Theme and environment** — Light, Dark, contrast theme, scaling, constrained width.
5. **Input and accessibility** — keyboard, focus, UI Automation or assistive-technology checks.

A successful build is not rendered verification. A screenshot is not keyboard or assistive-technology verification.

## Local Windows execution phase

Tasks 9–11 require a local Windows workspace because they need a real WinUI 3 project, exact starting SHA, build tools, runtime rendering, and fresh generation contexts. The approved workspace is:

```text
Z:\workspace\LazyDesign
```

Before the first run:

1. read the agent-home and repository `AGENTS.md` files;
2. record branch, HEAD, worktree status, remotes, and installed SDK versions;
3. create or verify the clean evaluation project snapshot;
4. run `python scripts/check_reference.py` and `python -m py_compile scripts/check_reference.py`;
5. preserve the snapshot SHA for all six runs.

The local phase must not alter baseline artifacts after generation. Any corrected implementation belongs outside the scored run directories.

## Controlled run packets

`evaluation/run-matrix.json` pins the input-document commit, evaluation fixture commit, prompt path, constrained width, and exact guided reference set for each scenario. Validate it before preparing any run:

```powershell
python scripts/evaluation_harness.py validate
```

Inspect any existing packet root before using it:

```powershell
python scripts/evaluation_harness.py inspect-packets --root evaluation/.runs/v2
```

The command reports exactly six entries with one of these states:

- `missing` — the expected packet directory does not exist;
- `stale` — its contract version, fixed inputs, or templates are invalid;
- `ready` — it is a clean current-contract packet with no execution activity;
- `in_progress` — it is valid but contains generated changes, build artifacts, metadata, or evidence that are not capture-ready;
- `capture_ready` — `RUN.md` and `verification.json` are complete and valid; schema-2 execution-contract packets also require a valid controller-recorded `generation-attempt.json`.

It exits 1 when any packet is `missing` or `stale`. Existing packet directories are never modified. Prepare each run into a new ignored workspace directory. The command refuses to reuse or modify an existing packet:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
```

The single-packet inspection must report `ready` before generation. For every valid packet it returns artifact-derived `expected_run_metadata`. After generation and the controlled build, complete `verification.json` and its evidence first. Inspection then returns all four exact RUN values: `Reference files supplied`, `Generated file list`, `Rendered checks performed`, and `Checks not performed`. Copy them into `RUN.md`, then inspect again and require `capture_ready` before capture.

A packet contains:

- `project/` reconstructed from the matrix-pinned fixture commit (the historical schema-1 matrices use `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`);
- byte-identical `PROMPT.md` extracted from the matrix-pinned input commit (the original schema-1 matrix uses `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`);
- `context/` only for guided runs, containing exactly the matrix-listed reference files;
- `PACKET.json` using packet contract `schema_version: 2`, with prompt, reference, and starting-project SHA-256 values;
- `RUN.template.md` for the required execution metadata;
- `evidence/verification.template.json` with the exact scenario verification checklist;
- for matrix schema 2 only, `evidence/generation-attempt.template.json` for the controller-reconciled execution record.

Use one newly prepared packet in one fresh model context. Do not add files to a baseline context, change `PROMPT.md`, change the guided context set, or reuse a context between runs. The packet tool does not invoke a model, repair generated output, or treat a build as rendered verification. In schema-2 experiments, the controller performs packet inspection before opening the fresh generation context; the generation context is not required to execute `evaluation_harness.py inspect-packet` itself.

`RUN.template.md` pins `.NET SDK: 9.0.313` and `Windows App SDK package: 2.0.1` from the starting-project commit. Do not replace these values with the SDK selected from the repository root. SDK selection depends on the process working directory, so a root-level `dotnet build <project-path>` may select a different installed SDK.

Build each generated packet only through the controlled helper:

```powershell
python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/connection-settings
```

The helper reconstructs the pinned `global.json` in a temporary workspace directory, verifies that `dotnet --version` resolves to `9.0.313`, then builds the exact top-level project file selected from the starting-project commit with Debug/x64. It does not rediscover or switch to an alternate project added by generation. If the pinned project file was deleted, the actual `dotnet build` failure is recorded rather than treating the generated result as an invalid packet.

The helper writes a one-shot pre-capture record to `evidence/build.txt` and never overwrites an existing build record. The evidence records the exact harness command, pinned build command, project file count, and a canonical SHA-256 of every non-build-output project file after the build. Inspection and capture validate the record; capture then includes its file hash in the immutable result. Exit code 0 means build success, 2 means the build ran and failed, and 1 means the packet or pinned build environment was invalid. Build failure remains a valid scored result and must not be repaired before capture.

When build was performed, `verification.json` must mark `build` as `pass` or `fail` and reference `build.txt`; `RUN.md` must exactly match the harness command and `exit <code>` in the evidence. The project source must not change after the controlled build. When build was not performed, the verification check, RUN command, and RUN result must all say so consistently. Inspection and capture reject stale build evidence, a command for another packet, changed project files after build, or other contradictory metadata.

`RUN.md` artifact metadata is also mechanical:

```text
Reference files supplied: none
Generated file list: {"changed":["MainWindow.xaml"],"deleted":["app.manifest"]}
```

Baseline must use `none`; guided runs must use `see PACKET.json`. `Generated file list` is compact JSON with sorted repository-relative paths for every non-build-output file changed or added and every starting-project file deleted. `bin`, `obj`, and `.vs` are excluded. Inspection, capture, and result validation reject a mismatch.

RUN verification metadata is also mechanical:

```text
Rendered checks performed: ["dark_theme","rendered_runtime"]
Checks not performed: ["accessibility_insights","high_contrast","narrator"]
```

`Rendered checks performed` is a sorted compact JSON array of non-build, non-static verification check IDs whose status is `pass` or `fail`; a failed check was still performed. `Checks not performed` is a sorted compact JSON array of every check whose status is `not_run`, including `build` or `static_review` when applicable. Prose summaries such as `render and theme` or `not performed` are invalid. After `verification.json` and referenced evidence are complete, copy both exact arrays from `inspect-packet`'s `expected_run_metadata`. Inspection, capture, and result validation reject any contradiction with verification statuses.

After generation and verification, copy `evidence/verification.template.json` to `evidence/verification.json`. For every check:

- use `pass` or `fail` only when at least one referenced evidence file exists under `evidence/`;
- use `not_run` with an empty evidence list and a concrete reason when the check was not performed;
- record 420 or 520 DIP exactly for the scenarios that define a constrained width;
- record a text scale above 100 when text-scaling verification was performed;
- record `ko-KR` and `en-US` when the corresponding long-content checks were performed;
- record the actual Windows contrast-theme name when High Contrast was performed.

The scenario-specific check set is fixed. It includes ComboBox popup, CommandBar overflow, ListView selection, InfoBar actions, ContentDialog actions, keyboard/focus, Narrator, and Accessibility Insights where relevant. Validate the record before capture:

```powershell
python scripts/evaluation_evidence.py evaluation/.runs/v2/baseline/connection-settings/evidence/verification.json
```

After generation, copy `RUN.template.md` to `RUN.md`, replace every record placeholder, and keep generated work inside `project/`. Capture the immutable result without repairing it:

```powershell
python scripts/evaluation_harness.py capture --packet evaluation/.runs/v2/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

Capture verifies prompt and reference hashes, rejects an incomplete `RUN.md` or invalid `verification.json`, ignores build directories, and preserves changed or added files under `generated/` plus deleted paths in `CAPTURE.json`. The capture manifest uses `schema_version: 2` and records SHA-256 values for `PROMPT.md`, `PACKET.json`, `RUN.md`, every generated file, and every evidence file. Failed or empty generations may still be captured when their completion status and every unperformed verification have concrete reasons.

After all six results are captured, verify the controlled conditions mechanically:

```powershell
python scripts/evaluation_harness.py validate-results --root evaluation
```

The result validator requires all six directories, exact prompt and reference hashes, the same start SHA, model, reasoning level, stopping condition, operating environment, tool access, and network policy, plus `Fresh context: yes` and `Generation intervention: none` for every scored run. It rejects any post-capture change, addition, or removal in `RUN.md`, `PACKET.json`, `generated/`, or `evidence/`. Capture and result validation also reject `.NET SDK` or Windows App SDK metadata that differs from the pinned starting-project values.

## Scoring and gate

Score every artifact with `rubric.md`. Every category score requires file/line evidence or a rendered observation. The gate is evaluated only after all six immutable artifacts are available.

Record the ten category scores, ten matching `score_evidence` entries, seven defect counts, rule traces, and all six findings sections in `evaluation/results/metrics.json` using `evaluation/gate-metrics.schema.json`. Each score-evidence entry must repeat its category and score, provide one or more evidence locations, and record evaluator uncertainty. Evidence paths are relative to `evaluation/`; score evidence must remain inside its own `baseline|guided/<scenario>/` result, and a traceable improvement must point to its guided scenario. A UTF-8 text reference may append `:<start>-<end>`, and the range must exist in the referenced file. Every category whose guided score is higher than its baseline score also requires a matching `traceable_improvements` entry with at least one existing LazyDesign rule ID and one evidence location.

Generate the three Task 11 reports without editing them by hand:

```powershell
python scripts/evaluation_report.py evaluation/results/metrics.json --output-dir evaluation/results
```

Before writing anything, the command reruns six-result validation and verifies that every score, trace, and finding evidence path exists in the allowed scenario directory; invalid or out-of-range references stop report generation. It then writes `scores.md`, `findings.md`, and `gate-decision.md`. For the historical schema-1 matrices it returns exit code 0 for PASS, 2 for a valid FAIL decision, and 1 for invalid or incomplete results or metrics. Schema-2 execution-incomplete behavior is defined separately under Gate v3 below. A zero baseline denominator is `not demonstrated`, not an automatic pass. Anatomy and accessibility defect counts must each decrease; unnecessary `ControlTemplate` and complexity defect counts must not increase.

Do not mark v0.1 validated or approve precision expansion before the mechanical gate in the implementation plan passes.

## v0.1-r1 revision

The initial Gate v1 experiment remains bound to `evaluation/run-matrix.json`. Existing Gate v1 commands omit `--matrix` and continue to use that file by default; the original `evaluation/baseline/`, `evaluation/guided/`, and `evaluation/results/` artifacts are not replaced or reinterpreted.

The `v0.1-r1` comparison uses an explicitly selected revision matrix for every harness and report command:

```powershell
--matrix evaluation/revisions/v0.1-r1/run-matrix.json
```

Revision captures and reports live under `evaluation/revisions/v0.1-r1/`. A revision command must pass the revision matrix explicitly rather than relying on path-based auto-detection or a newest-matrix convention.

Gate v2 keeps the same ten scoring categories and six quality conditions, and adds a hard prerequisite that all three guided controlled builds have `build: pass` in their immutable `verification.json` evidence. The report generator derives those statuses from the captured evidence and cross-checks the guided `build_failures` defect counts before evaluating the gate.

For overflow, Gate v2 preserves the existing 50% reduction rule when baseline observed overflow is greater than zero. When baseline observed overflow is zero, guided overflow must also remain zero to satisfy a non-regression floor. Zero-to-zero is reported as `non-regression`; it is not described as a measurable 50% reduction.

## Post-v0.1-r1 fixture correction

A 2026-08-08 post-hoc controller investigation reproduced the baseline connection-settings and guided device-list `Microsoft.UI.Xaml.dll` startup crashes outside the immutable scored artifacts. Both inner failures were `XamlParseException` resource lookups, and both disappeared when the start fixture merged `XamlControlsResources` without changing the frozen generated `MainWindow` source. The working-tree fixture now declares that WinUI resource dictionary and a regression test protects the requirement. See `evaluation/investigations/2026-08-08-runtime-startup.md`.

Do not update the existing v0.1 or v0.1-r1 matrices to point at this corrected working-tree fixture. Those matrices continue to identify the historical start-project commit used by their completed experiments. A future evaluation revision must pin a new start-project commit containing the correction and must treat that as a new versioned input state.

The fixture correction does not rewrite or rescore the separate Temporary Chat / Remote safety-inspection failures in v0.1-r1. Those historical captures remain evidence of the environment actually used by that experiment.

## Schema-2 execution validity and Gate v3

Future evaluation revisions can opt into the controller-reconciled execution contract with matrix `schema_version: 2` and `execution_contract: controller-reconciled-v1`. Schema 2 is accepted only when the matrix pins a start-project commit whose `App.xaml` declares `XamlControlsResources`. Existing v0.1 and v0.1-r1 matrices remain schema 1 and keep their historical behavior.

For every schema-2 cell, the controller must:

1. prepare a new packet and run `inspect-packet` itself until the untouched packet reports `ready`;
2. open exactly one fresh generation context, without requiring that context to execute the harness preflight command;
3. after generation returns, reconcile the actual non-build-output `project/` delta from disk rather than trusting the model's self-report;
4. write `evidence/generation-attempt.json` with the observed validity, blocker, stopping-condition status, exact changed/deleted paths, evidence files, and reason;
5. perform the controlled build and available verification without repairing generated source;
6. require `inspect-packet` to report `capture_ready`, then capture the immutable result.

`generation-attempt.json` uses `schema_version: 1`. `validity` is either `valid` or `infrastructure_invalid`. A valid model result uses `blocker: none`; this includes bad XAML, incomplete implementation, build failure, or another model-caused failure when no external infrastructure event interrupted generation. `infrastructure_invalid` requires a concrete blocker (`remote_safety_inspection`, `remote_transport`, `tool_timeout`, or `other_infrastructure`) and at least one existing evidence file. A partial write does not become valid merely because source changed: if an external infrastructure event materially interrupted the attempt, the controller preserves the real disk delta and records the attempt as infrastructure-invalid.

After all six schema-2 results are captured, validate execution readiness before scoring:

```powershell
python scripts/evaluation_harness.py validate-execution --root <evaluation-version-root> --matrix <schema-2-matrix>
```

The command first validates the matrix and all six immutable captures, then reads the six generation-attempt records. Exit code 0 means all six are execution-valid and the experiment is score-ready. Exit code 2 means the captures are structurally valid but at least one attempt is infrastructure-invalid; the experiment is `INCOMPLETE`. Exit code 1 means the matrix, capture set, or execution evidence is invalid.

For a schema-2 matrix, `evaluation_report.py` enforces this readiness check before metric evidence or score output. An incomplete experiment writes no `scores.md`, `findings.md`, or `gate-decision.md`, prints `INCOMPLETE:`, and exits 3. Only an execution-ready experiment proceeds to the existing Gate v2 quality calculation and guided-build prerequisite; this execution-first composition is Gate v3.

Do not retry a blocked cell until one succeeds inside the same experiment. One versioned experiment contains exactly six fresh attempts. If any cell is infrastructure-invalid, preserve all six captures and start any rerun as a new versioned matrix with six new fresh contexts. This prevents replacement selection from becoming another experimental confounder.
