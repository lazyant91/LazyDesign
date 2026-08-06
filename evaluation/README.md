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

Prepare each run into a new ignored workspace directory. The command refuses to reuse or modify an existing packet:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/baseline/connection-settings
```

A packet contains:

- `project/` reconstructed from fixture commit `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`;
- byte-identical `PROMPT.md` extracted from input commit `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`;
- `context/` only for guided runs, containing exactly the matrix-listed reference files;
- `PACKET.json` with prompt and reference SHA-256 values;
- `RUN.template.md` for the required execution metadata.

Use one newly prepared packet in one fresh model context. Do not add files to a baseline context, change `PROMPT.md`, change the guided context set, or reuse a context between runs. The packet tool does not invoke a model, repair generated output, or treat a build as rendered verification.

After generation, copy `RUN.template.md` to `RUN.md`, replace every record placeholder, and keep generated work inside `project/`. Capture the immutable result without repairing it:

```powershell
python scripts/evaluation_harness.py capture --packet evaluation/.runs/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

Capture verifies prompt and reference hashes, rejects an incomplete `RUN.md`, ignores build directories, and preserves changed or added files under `generated/` plus deleted paths in `CAPTURE.json`. Failed or empty generations may still be captured when their completion status and missing checks are recorded accurately.

After all six results are captured, verify the controlled conditions mechanically:

```powershell
python scripts/evaluation_harness.py validate-results --root evaluation
```

The result validator requires all six directories, exact prompt and reference hashes, the same start SHA, model, reasoning level, stopping condition, operating environment, tool access, and network policy, plus `Fresh context: yes` and `Generation intervention: none` for every scored run.

## Scoring and gate

Score every artifact with `rubric.md`. Every category score requires file/line evidence or a rendered observation. The gate is evaluated only after all six immutable artifacts are available.

Do not mark v0.1 validated or approve precision expansion before the mechanical gate in the implementation plan passes.
