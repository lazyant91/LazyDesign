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

A run that fails to generate or build is still a result. Preserve it without repair before scoring.

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

Do not leave a field blank. Use `not performed`, `not available`, or `not applicable` when necessary.

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
- `capture_ready` — `RUN.md` and `verification.json` are complete and valid.

It exits 1 when any packet is `missing` or `stale`. Existing packet directories are never modified. Prepare each run into a new ignored workspace directory. The command refuses to reuse or modify an existing packet:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
```

The single-packet inspection must report `ready` before generation. For every valid packet it also returns `expected_run_metadata` with the exact `Reference files supplied` and `Generated file list` values required by the current project state. After generation and the controlled build, run inspection before completing `RUN.md`, copy those two values exactly, then run it again and require `capture_ready` before capture.

A packet contains:

- `project/` reconstructed from fixture commit `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`;
- byte-identical `PROMPT.md` extracted from input commit `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`;
- `context/` only for guided runs, containing exactly the matrix-listed reference files;
- `PACKET.json` using packet contract `schema_version: 2`, with prompt, reference, and starting-project SHA-256 values;
- `RUN.template.md` for the required execution metadata;
- `evidence/verification.template.json` with the exact scenario verification checklist.

Use one newly prepared packet in one fresh model context. Do not add files to a baseline context, change `PROMPT.md`, change the guided context set, or reuse a context between runs. The packet tool does not invoke a model, repair generated output, or treat a build as rendered verification.

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

Baseline must use `none`; guided runs must use `see PACKET.json`. `Generated file list` is compact JSON with sorted repository-relative paths for every non-build-output file changed or added and every starting-project file deleted. `bin`, `obj`, and `.vs` are excluded. Copy both exact values from `inspect-packet`'s `expected_run_metadata`; inspection, capture, and result validation reject a mismatch.

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

Before writing anything, the command reruns six-result validation and verifies that every score, trace, and finding evidence path exists in the allowed scenario directory; invalid or out-of-range references stop report generation. It then writes `scores.md`, `findings.md`, and `gate-decision.md`. It returns exit code 0 for PASS, 2 for a valid FAIL decision, and 1 for invalid or incomplete results or metrics. A zero baseline denominator is `not demonstrated`, not an automatic pass. Anatomy and accessibility defect counts must each decrease; unnecessary `ControlTemplate` and complexity defect counts must not increase.

Do not mark v0.1 validated or approve precision expansion before the mechanical gate in the implementation plan passes.
