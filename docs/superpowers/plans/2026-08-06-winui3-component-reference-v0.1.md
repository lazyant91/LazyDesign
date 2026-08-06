# WinUI 3 Component Reference v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and evaluate a source-backed v0.1 reference for eight WinUI 3 controls that measurably reduces common agent-generated component defects.

**Architecture:** The repository remains a Markdown-first reference. Official evidence is pinned in a source manifest, normalized into five foundation pages and eight component pages, and consumed through `DESIGN.md`. Three fixed WinUI tasks are generated in baseline and guided conditions, scored with one rubric, and used as the gate for full precision expansion.

**Tech Stack:** Markdown, YAML source manifest, Git, Microsoft Learn, `microsoft/WinUI-Gallery` release `v2.9.3`, Windows Design Kit for Figma, WinUI 3, Windows App SDK version declared by the pinned Gallery release, PowerShell or Git-compatible shell for repository checks.

## Global Constraints

- WinUI 3 is the only framework in v0.1.
- The active controls are Button, TextBox, ToggleSwitch, ComboBox, CommandBar, ListView, InfoBar, and ContentDialog.
- The active foundations are text and localization, sizing and spacing, icons, states and themes, and accessibility basics.
- Do not implement control selection, screen planning, a semantic contract language, a rule resolver, framework adapters, UI validators, custom controls, or a Gallery clone.
- Use Microsoft Learn, the official WinUI 3 Gallery, the Microsoft Windows Design Kit, and non-conflicting Fluent 2 guidance in that order.
- Every normative rule must include a stable ID, requirement level, evidence type, prevented failure, and source reference.
- `derived` guidance must never be presented as an explicit Microsoft requirement.
- Do not commit copied documentation pages, large Gallery source excerpts, Figma exports, screenshots without a verified redistribution basis, fonts, or credentials.
- Do not add GitHub Actions.
- A build result is not rendered, theme, scaling, high-contrast, keyboard, or accessibility verification.
- Work on a focused branch and merge only after review.

---

## Planned file structure

```text
LazyDesign/
├─ README.md
├─ AGENTS.md
├─ DESIGN.md
├─ components/
│  ├─ README.md
│  ├─ button.md
│  ├─ textbox.md
│  ├─ toggleswitch.md
│  ├─ combobox.md
│  ├─ commandbar.md
│  ├─ listview.md
│  ├─ infobar.md
│  └─ contentdialog.md
├─ foundations/
│  ├─ README.md
│  ├─ text-and-localization.md
│  ├─ sizing-and-spacing.md
│  ├─ icons.md
│  ├─ states-and-themes.md
│  └─ accessibility-basics.md
├─ sources/
│  ├─ manifest.yaml
│  └─ notes/
│     ├─ windows-design-kit.md
│     └─ winui-gallery.md
├─ evaluation/
│  ├─ README.md
│  ├─ rubric.md
│  ├─ prompts/
│  │  ├─ connection-settings.md
│  │  ├─ device-list.md
│  │  └─ failure-confirmation.md
│  ├─ baseline/
│  │  ├─ connection-settings/
│  │  ├─ device-list/
│  │  └─ failure-confirmation/
│  ├─ guided/
│  │  ├─ connection-settings/
│  │  ├─ device-list/
│  │  └─ failure-confirmation/
│  └─ results/
│     ├─ scores.md
│     ├─ findings.md
│     └─ gate-decision.md
├─ docs/
│  ├─ templates/
│  │  ├─ component-reference.md
│  │  └─ source-note.md
│  └─ superpowers/
│     ├─ specs/
│     └─ plans/
└─ scripts/
   └─ check_reference.py
```

`baseline/` and `guided/` contain original generated artifacts and run metadata. Each scenario directory must include `PROMPT.md`, `RUN.md`, and generated XAML/C# files or a patch that reconstructs them.

---

### Task 1: Lock sources and repository conventions

**Files:**
- Create: `sources/manifest.yaml`
- Create: `sources/notes/winui-gallery.md`
- Create: `sources/notes/windows-design-kit.md`
- Create: `docs/templates/source-note.md`
- Modify: `README.md`
- Modify: `DESIGN.md`

**Interfaces:**
- Consumes: the source hierarchy in the approved design specification.
- Produces: source IDs referenced by every foundation and component rule.

- [ ] **Step 1: Inspect the pinned Gallery release**

Open `microsoft/WinUI-Gallery` at tag `v2.9.3`. Record:

- tag name;
- tag commit SHA;
- release date;
- license;
- Windows App SDK or WinUI package versions declared by the tagged project files;
- paths for the eight component sample pages;
- paths for design-guidance and accessibility pages used by the reference.

Do not use `main` as the v0.1 evidence revision.

- [ ] **Step 2: Inspect Microsoft Learn source pages**

Start from these source families and follow their current control links:

```text
https://learn.microsoft.com/windows/apps/develop/ui/controls/
https://learn.microsoft.com/windows/apps/design/downloads/
https://learn.microsoft.com/windows/apps/winui/winui3/
```

Record one manifest entry per control-specific or cross-cutting page actually used. Do not add a URL merely because it might be useful later.

- [ ] **Step 3: Inspect the Windows Design Kit**

Open the Windows Design Kit linked from Microsoft Learn. Use the official Figma file directly when the connector supports inspection. Otherwise duplicate the official file to the connected Figma account without modifying the source components.

Record:

- official source URL;
- Figma file key or stable file identifier;
- visible kit/library version when supplied;
- extraction date;
- pages and component sets inspected;
- the exact eight component sets used by v0.1.

Do not export or commit the kit.

- [ ] **Step 4: Create the source manifest**

Use this schema for every record:

```yaml
schema_version: 1
sources:
  - id: WINUI-GALLERY-V2-9-3
    kind: gallery
    url: https://github.com/microsoft/WinUI-Gallery/tree/v2.9.3
    retrieved_at: 2026-08-06
    revision: <exact-tag-commit-sha>
    license: MIT
    scope:
      - shared
    notes: Pinned executable and source reference for v0.1.
```

Replace `<exact-tag-commit-sha>` with the SHA returned by GitHub before committing. This token must not remain in the committed file.

For Microsoft Learn pages, `revision` contains the page's visible last-updated date when available; otherwise it contains `retrieved-2026-08-06`. For the Figma kit, `revision` contains its visible version or `file-<file-key>-retrieved-2026-08-06`.

- [ ] **Step 5: Create source note files**

`docs/templates/source-note.md` must contain these headings:

```markdown
# Source Note: <descriptive title>

## Identity
## Scope inspected
## Relevant observations
## Conflicts or limitations
## Rules supported
## Copyright and storage decision
```

Before committing, replace the template title token in each actual note file. The template may retain `<descriptive title>` because it is an authoring template, not an unfinished source note.

`winui-gallery.md` records sample paths, runtime limitations, and the fact that a sample demonstrates behavior without automatically making it a universal requirement.

`windows-design-kit.md` records inspected component sets, anatomy/variant observations, and the fact that Figma does not define WinUI runtime behavior.

- [ ] **Step 6: Verify manifest integrity**

Run:

```bash
git grep -n "<exact-tag-commit-sha>\|TBD\|TODO" -- sources README.md DESIGN.md
```

Expected: no output.

Run:

```bash
git diff --check
```

Expected: exit code 0.

- [ ] **Step 7: Commit**

```bash
git add sources docs/templates/source-note.md README.md DESIGN.md
git commit -m "docs: pin v0.1 design sources"
```

---

### Task 2: Add the reference templates and structural checker

**Files:**
- Create: `docs/templates/component-reference.md`
- Create: `components/README.md`
- Create: `foundations/README.md`
- Create: `scripts/check_reference.py`

**Interfaces:**
- Consumes: source IDs from `sources/manifest.yaml`.
- Produces: the fixed component-page contract and a repository-level structural check used by later tasks.

- [ ] **Step 1: Create the component template**

Create `docs/templates/component-reference.md` with exactly these top-level sections:

```markdown
# <ControlName>

## 1. Purpose and characteristic
## 2. Anatomy
## 3. Content rules
## 4. Sizing and layout
## 5. States and interaction
## 6. Theme, accessibility, and localization
## 7. Common failures
## 8. Minimal native XAML
## 9. Verification checklist
## 10. Sources
```

Include this rule block under the first section as the authoring format:

```markdown
### <RULE-ID>

**Level:** MUST | SHOULD | MAY  
**Evidence:** official-doc | gallery | ui-kit | derived  
**Prevents:** <one observable failure>

<Concise operational guidance.>

**Sources:** `<SOURCE-ID>`
```

The template may retain angle-bracket tokens. Actual component pages may not.

- [ ] **Step 2: Create directory index pages**

`components/README.md` explains that pages document selected controls without choosing between unrelated controls. It lists all eight v0.1 files.

`foundations/README.md` explains that foundation pages contain only shared guidance and lists all five files.

- [ ] **Step 3: Write the structural checker test first**

Create `scripts/check_reference.py` with a failing check for missing component files and headings. The checker must:

- use only the Python standard library;
- load the eight expected component paths and five foundation paths;
- require all ten component headings;
- reject `TBD`, `TODO`, `<RULE-ID>`, `<SOURCE-ID>`, and `<ControlName>` in actual reference pages;
- require at least one `**Sources:**` line in every component page;
- require all referenced source IDs to occur in `sources/manifest.yaml`;
- print one actionable error per violation;
- return exit code 1 when any violation exists and 0 when none exist.

Use these constants:

```python
COMPONENTS = (
    "button.md",
    "textbox.md",
    "toggleswitch.md",
    "combobox.md",
    "commandbar.md",
    "listview.md",
    "infobar.md",
    "contentdialog.md",
)

FOUNDATIONS = (
    "text-and-localization.md",
    "sizing-and-spacing.md",
    "icons.md",
    "states-and-themes.md",
    "accessibility-basics.md",
)
```

- [ ] **Step 4: Run the checker to verify the expected failure**

Run:

```bash
python scripts/check_reference.py
```

Expected: exit code 1 with missing-file errors for all component and foundation pages.

- [ ] **Step 5: Verify the script itself**

Run:

```bash
python -m py_compile scripts/check_reference.py
```

Expected: exit code 0.

- [ ] **Step 6: Commit**

```bash
git add docs/templates/component-reference.md components/README.md foundations/README.md scripts/check_reference.py
git commit -m "docs: define component reference contract"
```

---

### Task 3: Author the five shared foundation pages

**Files:**
- Create: `foundations/text-and-localization.md`
- Create: `foundations/sizing-and-spacing.md`
- Create: `foundations/icons.md`
- Create: `foundations/states-and-themes.md`
- Create: `foundations/accessibility-basics.md`
- Modify: `DESIGN.md`

**Interfaces:**
- Consumes: pinned source IDs and the requirement/evidence model.
- Produces: shared rule IDs linked from component pages.

- [ ] **Step 1: Author text and localization guidance**

Cover only cross-component requirements:

- distinguish visible label, header, placeholder, helper text, value, and validation text;
- keep concise control labels separate from explanatory paragraphs;
- test long Korean and English strings;
- avoid arbitrary fixed width when text length is variable;
- record when wrapping, trimming, or scrolling is component-specific rather than global;
- avoid embedding untranslated strings in reusable examples.

Every normative statement must use a rule block and source IDs.

- [ ] **Step 2: Author sizing and spacing guidance**

Cover:

- native desired size and default style as the starting point;
- fixed dimension risks under localization and scaling;
- distinction between control-internal padding and page-layout spacing;
- minimum interactive size only when supported by a Windows source;
- verification at constrained widths;
- prohibition on inferring universal pixel values from one Figma frame.

- [ ] **Step 3: Author icon guidance**

Cover:

- Segoe Fluent Icons or supported icon sources;
- relationship between visible icon and text label;
- accessible names for icon-only controls;
- decorative versus semantic icons;
- consistent baseline and size within a control;
- avoiding manually drawn glyph approximations when a native icon exists.

- [ ] **Step 4: Author states and themes guidance**

Cover:

- preservation of native normal, pointer-over, pressed, focused, disabled, selected, and validation states when relevant;
- Light and Dark theme verification;
- Windows High Contrast as a separate environment check;
- system accent and theme resources before fixed colors;
- the difference between Gallery observation and verified behavior in the target app.

- [ ] **Step 5: Author accessibility basics**

Cover:

- accessible name and state;
- keyboard operation and focus visibility;
- label association;
- not relying on color alone;
- text scaling and readable content;
- distinction between static review and assistive-technology verification.

Do not attempt to replace Microsoft accessibility documentation with a complete accessibility standard.

- [ ] **Step 6: Update the foundation index**

Change each v0.1 foundation status in `DESIGN.md` from `planned` to `draft-reviewed` only after its rules have source IDs and no unresolved placeholder text.

- [ ] **Step 7: Run checks**

Run:

```bash
python scripts/check_reference.py
```

Expected: missing-file errors only for the eight component pages; no foundation-file or foundation-placeholder errors.

Run:

```bash
git diff --check
```

Expected: exit code 0.

- [ ] **Step 8: Commit**

```bash
git add foundations DESIGN.md
git commit -m "docs: add WinUI shared component foundations"
```

---

### Task 4: Author Button and TextBox pages

**Files:**
- Create: `components/button.md`
- Create: `components/textbox.md`
- Modify: `DESIGN.md`

**Interfaces:**
- Consumes: all five foundations and pinned Button/TextBox sources.
- Produces: the first command and input component contracts used by evaluation Scenario A.

- [ ] **Step 1: Extract Button evidence**

Inspect the pinned Microsoft Learn Button guidance, Gallery Button page and source, and Button component set in the Windows Design Kit.

Record evidence for:

- basic anatomy;
- text and icon content;
- accent or emphasis variants supported by Windows sources;
- default states;
- long-content behavior;
- accessible labeling;
- default sizing and layout behavior;
- cases where Gallery examples use wrapped text or constrained layout.

- [ ] **Step 2: Write `components/button.md`**

The page must include rules that prevent:

- paragraph-length labels;
- ambiguous action text;
- clipping from arbitrary fixed width;
- inaccessible icon-only buttons;
- excessive emphasis;
- incomplete local state templates;
- custom templates used only for superficial styling.

The minimal XAML section must use a native `Button` and a native accent style example without defining a `ControlTemplate`.

- [ ] **Step 3: Extract TextBox evidence**

Inspect the pinned TextBox guidance, Gallery samples, and TextBox component set. Record evidence for:

- header or label;
- placeholder;
- current value;
- helper or validation relationship;
- single-line versus multi-line behavior;
- clear button or other native affordances when documented;
- text fit, wrapping, and scrolling;
- disabled, read-only, focus, and validation states;
- accessible naming and instructions.

- [ ] **Step 4: Write `components/textbox.md`**

The page must explicitly separate:

- persistent label/header;
- placeholder hint;
- entered value;
- helper text;
- validation feedback.

It must prevent use of PlaceholderText as the only persistent label when that would remove necessary context after entry.

The minimal XAML example must use native `TextBox` properties and place helper or validation content outside the editable text value.

- [ ] **Step 5: Update `DESIGN.md` statuses**

Set Button and TextBox to `draft-reviewed`.

- [ ] **Step 6: Run checks**

Run:

```bash
python scripts/check_reference.py
```

Expected: missing-file errors for six component pages only.

Run:

```bash
git grep -n "ControlTemplate" -- components/button.md components/textbox.md
```

Expected: occurrences only in explanation or common-failure sections, not inside the minimal native XAML blocks.

- [ ] **Step 7: Commit**

```bash
git add components/button.md components/textbox.md DESIGN.md
git commit -m "docs: add Button and TextBox references"
```

---

### Task 5: Author ToggleSwitch and ComboBox pages

**Files:**
- Create: `components/toggleswitch.md`
- Create: `components/combobox.md`
- Modify: `DESIGN.md`

**Interfaces:**
- Consumes: text/localization, sizing, states/themes, and accessibility foundations.
- Produces: setting and selection control contracts used by Scenario A.

- [ ] **Step 1: Author ToggleSwitch evidence and rules**

Cover:

- control label and switch state;
- On/Off content only where it clarifies the state;
- accessible state communication;
- keyboard and focus behavior;
- immediate setting changes as observed or documented, without expanding into control-selection advice;
- long localized labels outside the switch track;
- preservation of native checked, unchecked, disabled, and focused states.

- [ ] **Step 2: Author ComboBox evidence and rules**

Cover:

- visible selection and placeholder behavior;
- label/header relationship;
- long-item and popup-width behavior supported by sources;
- item templates without excessive information density;
- keyboard, focus, disabled, and selected states;
- accessible name and selected value;
- avoiding arbitrary fixed widths without longest-item verification.

- [ ] **Step 3: Add minimal native XAML**

Use native `ToggleSwitch` and `ComboBox` examples. Do not introduce custom templates or a custom popup.

- [ ] **Step 4: Update statuses and run checks**

Set both statuses to `draft-reviewed`.

Run:

```bash
python scripts/check_reference.py
```

Expected: missing-file errors for CommandBar, ListView, InfoBar, and ContentDialog only.

- [ ] **Step 5: Commit**

```bash
git add components/toggleswitch.md components/combobox.md DESIGN.md
git commit -m "docs: add ToggleSwitch and ComboBox references"
```

---

### Task 6: Author CommandBar and ListView pages

**Files:**
- Create: `components/commandbar.md`
- Create: `components/listview.md`
- Modify: `DESIGN.md`

**Interfaces:**
- Consumes: icon, text/localization, sizing, states/themes, and accessibility foundations.
- Produces: command and collection contracts used by Scenario B.

- [ ] **Step 1: Author CommandBar evidence and rules**

Cover:

- primary and secondary command areas;
- icon and label composition;
- command priority and overflow behavior as documented or demonstrated;
- concise labels and accessible names;
- keyboard and focus behavior;
- narrow-width behavior;
- avoiding an excessive number of equally prominent commands;
- preservation of native overflow and state handling.

Do not turn the page into a general command-selection framework.

- [ ] **Step 2: Author ListView evidence and rules**

Cover:

- item anatomy and consistent item templates;
- primary and secondary text hierarchy;
- long-item content;
- selection, focus, pointer, disabled, and empty-content relationships;
- accessible item name and selected state;
- virtualization-safe item templates when supported by sources;
- avoiding paragraph-heavy items and arbitrary per-item controls.

Do not define a universal list-detail page pattern.

- [ ] **Step 3: Add minimal native XAML**

Use native `CommandBar`, `AppBarButton`, and `ListView` examples. Examples must preserve native overflow and selection behavior.

- [ ] **Step 4: Update statuses and run checks**

Set both statuses to `draft-reviewed`.

Run:

```bash
python scripts/check_reference.py
```

Expected: missing-file errors for InfoBar and ContentDialog only.

- [ ] **Step 5: Commit**

```bash
git add components/commandbar.md components/listview.md DESIGN.md
git commit -m "docs: add CommandBar and ListView references"
```

---

### Task 7: Author InfoBar and ContentDialog pages

**Files:**
- Create: `components/infobar.md`
- Create: `components/contentdialog.md`
- Modify: `DESIGN.md`

**Interfaces:**
- Consumes: text/localization, sizing, states/themes, icons, and accessibility foundations.
- Produces: feedback and modal contracts used by Scenario C.

- [ ] **Step 1: Author InfoBar evidence and rules**

Cover:

- title, message, severity, action, icon, and close affordance;
- concise title versus longer message;
- action placement and labeling;
- dismissible versus persistent behavior only as supported by sources;
- accessible severity and content;
- long-message layout;
- avoiding multiple competing actions or decorative severity changes.

- [ ] **Step 2: Author ContentDialog evidence and rules**

Cover:

- title, content, primary, secondary, and close actions;
- concise action labels;
- default focus and keyboard behavior when documented;
- long and scrollable content behavior;
- destructive confirmation wording without prescribing product policy;
- accessible title and focus containment;
- avoiding dense forms or whole-page replacement inside a dialog.

- [ ] **Step 3: Add minimal native XAML**

Use native `InfoBar` and `ContentDialog`. Do not define local control templates.

- [ ] **Step 4: Update statuses**

Set all eight component statuses and all five foundation statuses in `DESIGN.md` to `v0.1-candidate`.

- [ ] **Step 5: Run the complete structural check**

Run:

```bash
python scripts/check_reference.py
```

Expected: exit code 0 and a success summary listing 8 component pages and 5 foundation pages.

Run:

```bash
git grep -n "TBD\|TODO\|<RULE-ID>\|<SOURCE-ID>\|<ControlName>" -- components foundations sources
```

Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add components/infobar.md components/contentdialog.md DESIGN.md
git commit -m "docs: complete v0.1 component references"
```

---

### Task 8: Create the fixed evaluation harness

**Files:**
- Create: `evaluation/README.md`
- Create: `evaluation/rubric.md`
- Create: `evaluation/prompts/connection-settings.md`
- Create: `evaluation/prompts/device-list.md`
- Create: `evaluation/prompts/failure-confirmation.md`

**Interfaces:**
- Consumes: the eight candidate component pages and five foundations.
- Produces: fixed prompts and scoring rules used by both baseline and guided runs.

- [ ] **Step 1: Write evaluation run rules**

`evaluation/README.md` must require:

- same model family and reasoning level;
- fresh context per run;
- identical task prompt and starting project;
- network access disabled during the generation run unless both conditions receive it;
- baseline run without LazyDesign content;
- guided run with `DESIGN.md` and only relevant component/foundation pages;
- no prompt repair during a run;
- exact run metadata in `RUN.md`;
- separate reporting of static review, build, and rendered verification.

- [ ] **Step 2: Write the exact rubric**

`evaluation/rubric.md` defines 0, 1, and 2 anchors for each category:

1. content length and overflow;
2. information hierarchy;
3. component anatomy;
4. native interaction states;
5. accessibility basics;
6. localization and scaling resilience;
7. native WinUI style preservation;
8. component-specific characteristics;
9. label/helper/explanation separation;
10. XAML simplicity and relevance.

For every category:

- `0` means the defect is present or the requirement is omitted;
- `1` means partial or inconsistent handling;
- `2` means the generated implementation and evidence satisfy the scenario.

The rubric requires a file/line or rendered observation for every score.

- [ ] **Step 3: Create Scenario A prompt**

`connection-settings.md` must contain this task text:

```markdown
# Connection Settings Evaluation Task

Create a WinUI 3 settings page for configuring a device connection.

Requirements:

- Use a TextBox for the connection name.
- Use a ComboBox for the transport with USB, Wi-Fi, and Bluetooth options.
- Use a ToggleSwitch for automatic reconnection.
- Use a Button to save the settings.
- Show persistent labels, one short helper sentence for the connection name, and an inline validation message when the name is empty.
- The page must remain usable in a 420-DIP-wide content area.
- Include these Korean strings in the UI fixture:
  - `연결 프로필 이름`
  - `장치를 구분할 수 있는 이름을 입력하세요.`
  - `사용 가능한 장치에 자동으로 다시 연결`
  - `연결 설정 저장`
- Preserve keyboard operation and native WinUI visual states.
- Implement the page in XAML with the smallest necessary C# or ViewModel support.
```

- [ ] **Step 4: Create Scenario B prompt**

`device-list.md` must contain this task text:

```markdown
# Device List Evaluation Task

Create a WinUI 3 device list page.

Requirements:

- Use a CommandBar with Refresh, Add device, and Remove commands.
- Use a ListView to show device name, connection type, and current status.
- Include an empty state when no devices exist.
- Include selected and unselected item behavior.
- The fixture must contain the long name `회의실 디스플레이 무선 프레젠테이션 수신 장치` and the English name `Portable conference-room presentation receiver`.
- The page must remain usable in a 520-DIP-wide content area.
- Preserve keyboard operation, command overflow behavior, selection visibility, and native WinUI states.
- Implement the page in XAML with the smallest necessary C# or ViewModel support.
```

- [ ] **Step 5: Create Scenario C prompt**

`failure-confirmation.md` must contain this task text:

```markdown
# Failure and Confirmation Evaluation Task

Create WinUI 3 UI for a failed device connection and a destructive removal confirmation.

Requirements:

- Use an InfoBar to show a connection failure with title, message, severity, a Retry action, and dismissal.
- Use a ContentDialog to confirm removal of a saved device.
- The failure message must include: `장치가 응답하지 않았습니다. 장치가 켜져 있고 동일한 네트워크에 연결되어 있는지 확인한 후 다시 시도하세요.`
- The dialog must identify the selected device and provide Remove, Cancel, and close behavior appropriate to the native control.
- Preserve keyboard focus, accessible names, and native WinUI visual states.
- Do not create custom control templates.
- Implement the UI in XAML with the smallest necessary C# or ViewModel support.
```

- [ ] **Step 6: Verify prompt equality rules**

Run:

```bash
git diff --check
python scripts/check_reference.py
```

Expected: both commands exit 0.

- [ ] **Step 7: Commit**

```bash
git add evaluation/README.md evaluation/rubric.md evaluation/prompts
git commit -m "test: add fixed WinUI reference evaluation"
```

---

### Task 9: Run and record the baseline condition

**Files:**
- Create: `evaluation/baseline/connection-settings/PROMPT.md`
- Create: `evaluation/baseline/connection-settings/RUN.md`
- Create: generated Scenario A artifacts under `evaluation/baseline/connection-settings/`
- Create: corresponding files under `evaluation/baseline/device-list/`
- Create: corresponding files under `evaluation/baseline/failure-confirmation/`

**Interfaces:**
- Consumes: fixed prompts and a clean WinUI evaluation project that does not contain LazyDesign reference files.
- Produces: immutable baseline artifacts for scoring.

- [ ] **Step 1: Create one clean evaluation project snapshot**

Create a minimal WinUI 3 project using the Windows App SDK version pinned from Gallery `v2.9.3`. Commit or record the exact initial project SHA used for all six runs.

The project contains no LazyDesign component or foundation content.

Use evaluation packet contract v2 and a new ignored root under `evaluation/.runs/v2/`. Do not reuse or modify any earlier v1 packet. Before each baseline run, prepare and inspect that one packet:

```bash
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
```

The inspection must report `ready` before generation and `capture_ready` before capture. Use the corresponding scenario name for Scenarios B and C.

- [ ] **Step 2: Run Scenario A in a fresh context**

Use the exact contents of `evaluation/prompts/connection-settings.md`. Do not add design advice or repair the prompt.

Copy the prompt into `PROMPT.md`. Record in `RUN.md`:

- date and time;
- model identifier;
- reasoning level;
- starting project SHA;
- tool access;
- whether the generation completed without intervention;
- generated file list;
- build command and result;
- rendered checks actually performed.

- [ ] **Step 3: Run Scenarios B and C identically**

Repeat from fresh contexts using the exact prompt files.

- [ ] **Step 4: Preserve failures**

Do not correct baseline artifacts. If a generated project fails to build, record the build failure and retain the generated files as the baseline result.

- [ ] **Step 5: Commit**

```bash
git add evaluation/baseline
git commit -m "test: record unguided WinUI baseline"
```

---

### Task 10: Run and record the guided condition

**Files:**
- Create: `evaluation/guided/connection-settings/PROMPT.md`
- Create: `evaluation/guided/connection-settings/RUN.md`
- Create: generated Scenario A artifacts under `evaluation/guided/connection-settings/`
- Create: corresponding files under `evaluation/guided/device-list/`
- Create: corresponding files under `evaluation/guided/failure-confirmation/`

**Interfaces:**
- Consumes: the same project snapshot and prompts as Task 9 plus relevant LazyDesign pages.
- Produces: immutable guided artifacts for scoring.

- [ ] **Step 1: Reset to the exact evaluation project snapshot**

Use the same starting SHA recorded in every baseline `RUN.md`.

Prepare each guided packet under the same v2 root immediately before its fresh-context run, then inspect it:

```bash
python scripts/evaluation_harness.py prepare --condition guided --scenario connection-settings --destination evaluation/.runs/v2/guided/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/guided/connection-settings --condition guided --scenario connection-settings
```

The inspection must report `ready` before generation and `capture_ready` before capture. Never migrate or patch a v1 packet into v2.

- [ ] **Step 2: Provide the fixed reference set**

For Scenario A provide:

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

For Scenario B provide:

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

For Scenario C provide:

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

Do not provide unrelated component pages.

- [ ] **Step 3: Run all scenarios in fresh contexts**

Use the exact task text from the prompt files. The only experimental difference is the supplied LazyDesign reference set.

Record the same metadata and verification evidence required by Task 9.

- [ ] **Step 4: Preserve failures and commit**

Do not repair guided artifacts before scoring.

```bash
git add evaluation/guided
git commit -m "test: record LazyDesign-guided WinUI output"
```

---

### Task 11: Score results and decide the v0.1 gate

**Files:**
- Create: `evaluation/results/scores.md`
- Create: `evaluation/results/findings.md`
- Create: `evaluation/results/gate-decision.md`
- Modify: `DESIGN.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: baseline and guided artifacts, run metadata, rubric, and reference rule IDs.
- Produces: the evidence-backed decision to revise v0.1 or expand toward full precision.

- [ ] **Step 1: Score all six artifacts**

For each rubric category, record:

- baseline score;
- guided score;
- file/line evidence or rendered observation;
- related LazyDesign rule IDs when a guided improvement is attributable;
- evaluator uncertainty.

Compute scenario totals and the 60-point total.

- [ ] **Step 2: Count target defects**

Record counts for:

- clipping or content overflow;
- missing component anatomy;
- missing accessible names or states;
- unnecessary local templates;
- irrelevant XAML or added complexity;
- build failures;
- rendered verification failures.

- [ ] **Step 3: Write findings**

`findings.md` separates:

- improvements attributable to specific reference rules;
- unchanged defects;
- regressions introduced by guidance;
- ambiguous rubric decisions;
- rules the model ignored;
- rules that caused unnecessary output.

- [ ] **Step 4: Apply the gate mechanically**

`gate-decision.md` must answer each condition:

```text
[pass/fail] Guided total improved by at least 20%.
[pass/fail] Clipping/content-overflow defects decreased by at least 50%.
[pass/fail] Missing anatomy and accessibility requirements decreased.
[pass/fail] Unnecessary ControlTemplate replacement did not increase.
[pass/fail] Irrelevant XAML or complexity did not materially increase.
[pass/fail] Improvements are traceable to specific reference rules.
```

The overall result is `PASS` only if all six conditions pass.

Record the ten category scores with matching evidence, defect counts, traceable improvements, and all six findings sections in `evaluation/results/metrics.json` using `evaluation/gate-metrics.schema.json`. Then generate all three result documents together:

```bash
python scripts/evaluation_report.py evaluation/results/metrics.json --output-dir evaluation/results
```

Before writing reports, the command must rerun six-result validation, verify post-capture hashes, and resolve every score, trace, and finding evidence path inside the allowed baseline or guided scenario. Text line ranges must exist. The command writes `scores.md`, `findings.md`, and `gate-decision.md` from the same validated input. Exit code 0 means PASS, 2 means a valid FAIL decision, and 1 means invalid or incomplete results or metrics.

- [ ] **Step 5: Update repository status**

If the gate passes:

- set v0.1 component and foundation statuses in `DESIGN.md` to `validated-v0.1`;
- state in README that precision expansion is approved;
- define the next component family from the design specification.

If the gate fails:

- leave statuses as `v0.1-candidate`;
- state in README that expansion is blocked;
- list the exact pages or retrieval behavior to revise;
- do not add new controls.

- [ ] **Step 6: Run final checks**

Run:

```bash
python scripts/check_reference.py
git diff --check
git grep -n "TBD\|TODO" -- README.md DESIGN.md components foundations evaluation sources
```

Expected:

- structural checker exits 0;
- `git diff --check` exits 0;
- placeholder search returns no output.

- [ ] **Step 7: Commit**

```bash
git add evaluation/results README.md DESIGN.md
git commit -m "test: decide LazyDesign v0.1 quality gate"
```

---

### Task 12: Review and prepare the v0.1 pull request

**Files:**
- Review all files changed by Tasks 1-11.
- Modify only files with verified inconsistencies.

**Interfaces:**
- Consumes: complete v0.1 branch.
- Produces: a reviewable pull request with accurate evidence and no unsupported completion claims.

- [ ] **Step 1: Review source traceability**

For every component page, confirm that each source ID exists in `sources/manifest.yaml` and supports the rule as written.

- [ ] **Step 2: Review provenance wording**

Search all `derived` rules and confirm that each explains its reasoning and does not use language such as “Microsoft requires” unless the cited official source explicitly says so.

Run:

```bash
git grep -n "derived" -- components foundations
```

Review every match manually.

- [ ] **Step 3: Review scope**

Confirm the branch contains no:

- WPF, UWP, MAUI, Qt, web, Android, or iOS rules;
- semantic contract or resolver code;
- framework adapters;
- custom WinUI control library;
- UI static analyzer;
- Gallery clone or copied source tree;
- GitHub Actions workflow.

- [ ] **Step 4: Verify final state**

Run:

```bash
python scripts/check_reference.py
python -m py_compile scripts/check_reference.py
git diff --check
git status --short
git log --oneline --decorate -12
```

Expected:

- checks exit 0;
- working tree is clean;
- commit history reflects source capture, foundations, component families, evaluation harness, baseline, guided output, and gate decision.

- [ ] **Step 5: Open the pull request**

Use a title that reflects the gate result:

```text
feat: validate WinUI component reference v0.1
```

The PR body must include:

- source revisions;
- eight components and five foundations;
- exact evaluation model and reasoning level;
- baseline and guided scores;
- gate result;
- build and rendered checks performed;
- checks not performed;
- copyright/storage decisions;
- known limitations;
- next step only when the gate passed.

Do not merge without repository-owner approval.

---

## Plan self-review

### Spec coverage

- Product purpose and non-goals: Tasks 1-3 and repository bootstrap.
- Source hierarchy and revision pinning: Task 1.
- Rule/evidence model: Tasks 2-7.
- Five foundations: Task 3.
- Eight component pages: Tasks 4-7.
- Controlled evaluation: Tasks 8-10.
- Gate and full-precision decision: Task 11.
- Git, evidence, and completion reporting: Task 12.

### Scope boundary

The plan produces one independently testable vertical slice. It does not implement the later full-precision component families. Expansion requires a passing v0.1 gate and a separate implementation plan.

### Placeholder policy

Angle-bracket markers are allowed only in authoring templates and the illustrative manifest snippet before Task 1 replaces the Gallery SHA. Actual source, foundation, component, evaluation, and result files must contain no unresolved placeholder markers.
