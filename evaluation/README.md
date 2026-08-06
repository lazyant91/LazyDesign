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

## Scoring and gate

Score every artifact with `rubric.md`. Every category score requires file/line evidence or a rendered observation. The gate is evaluated only after all six immutable artifacts are available.

Do not mark v0.1 validated or approve precision expansion before the mechanical gate in the implementation plan passes.
