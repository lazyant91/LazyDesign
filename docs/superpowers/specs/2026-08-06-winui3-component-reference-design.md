# WinUI 3 Component Reference Design

**Date:** 2026-08-06  
**Status:** Approved initial direction  
**Repository:** `lazyant91/LazyDesign`

## 1. Summary

LazyDesign will be a source-backed, agent-readable reference that documents the basic composition and behavior of WinUI 3 controls.

The product addresses a specific model limitation: when explicit component guidance is unavailable, an agent fills gaps through inference. Even a strong model can then generate small but repeated defects such as clipped labels, excessive text inside controls, missing accessible names, incomplete visual states, and unnecessary custom templates.

LazyDesign reduces that inference surface. It does not make screen-level product decisions and does not choose controls for the agent. It tells the agent what must remain true after a control has been selected.

The final target is precise coverage of the core WinUI 3 control set. Development begins with an eight-control vertical slice so that the project can measure whether the reference improves generated XAML before investing in full coverage.

## 2. Problem statement

Official information relevant to a WinUI component is distributed across several places:

- Microsoft Learn control and design guidance;
- the WinUI 3 Gallery application and source repository;
- the Windows Design Kit for Figma;
- general Fluent 2 guidance.

A coding agent working on an ordinary project should not have to rediscover, reconcile, and interpret those sources for every screen. More importantly, asking the model to retrieve the sources does not guarantee that it will notice the small rules that affect implementation quality.

The desired result is a local reference that makes those rules explicit and easy to retrieve at the moment a component is implemented.

## 3. Goals

LazyDesign must:

1. Record the basic anatomy and characteristic behavior of each covered WinUI 3 component.
2. State concrete text, icon, content, sizing, layout, state, theme, accessibility, and localization guidance.
3. Identify common implementation failures that an agent is likely to produce.
4. Prefer native WinUI controls, styles, states, and accessibility behavior.
5. Separate explicit Microsoft guidance from Gallery observations, UI-kit observations, and derived conclusions.
6. Provide concise, valid native XAML examples.
7. Give the agent a short verification checklist for each component.
8. Demonstrate measurable improvement through controlled baseline and guided generation runs.
9. Pin the source revision and retrieval date used to author each page.
10. Remain useful without requiring network access during ordinary project work.

## 4. Non-goals

LazyDesign will not initially:

- select controls or design a complete screen flow;
- infer product information architecture;
- generate a visual identity or brand theme;
- define a semantic screen-contract language;
- resolve tokens into deterministic XAML values;
- ship WinUI resource dictionaries, wrapper controls, or framework adapters;
- implement static analyzers or runtime validators;
- support WPF, UWP, MAUI, Qt, web, Android, or iOS;
- fork, reimplement, or package WinUI 3 Gallery;
- mirror Microsoft documentation or distribute the Windows Design Kit;
- treat every hard-coded value as an error;
- guarantee rendered correctness from static Markdown guidance alone.

These are deliberate scope boundaries, not future commitments.

## 5. Approaches considered

### 5.1 Executable design-rule platform

This approach would normalize sources into a rule registry, semantic contracts, a resolver, framework adapters, validators, and completion gates.

**Advantages**

- deterministic enforcement;
- machine-readable rule IDs;
- potential for automated audits.

**Disadvantages**

- creates a second UI framework above WinUI;
- requires extensive infrastructure before user value can be measured;
- risks encoding project-specific decisions as universal rules;
- expands quickly into multiple frameworks and screen-level decisions;
- does not directly prove that concise component knowledge improves the agent.

**Decision:** rejected for the initial product.

### 5.2 Use WinUI 3 Gallery without a local reference

This approach would direct the agent or developer to inspect the Gallery whenever a component question arises.

**Advantages**

- official, maintained, interactive source;
- real XAML and code-behind samples;
- no duplicate sample application.

**Disadvantages**

- ordinary project work still depends on external inspection;
- Gallery examples do not consistently state the small implementation constraints as agent instructions;
- the agent must infer rules from sample code and rendered behavior;
- information remains distributed across Gallery, Learn, and Figma.

**Decision:** use Gallery as evidence and runtime reference, not as the final agent-facing artifact.

### 5.3 Thin component reference with controlled evaluation

This approach creates concise Markdown component pages from official sources and tests whether those pages improve generated output.

**Advantages**

- directly addresses the identified failure mode;
- useful before any enforcement infrastructure exists;
- low implementation cost;
- easy to inspect and revise;
- does not replace native WinUI;
- can later support tooling if evidence justifies it.

**Disadvantages**

- guidance is not automatically enforced;
- quality depends on source extraction and evaluation discipline;
- runtime defects still require actual build and rendered checks.

**Decision:** selected.

## 6. Product architecture

The product is a small document system with four layers.

```text
Official source evidence
        ↓
Source manifest and extraction notes
        ↓
Foundation and component reference pages
        ↓
Agent entry point and controlled evaluation
```

### 6.1 `DESIGN.md`

`DESIGN.md` is the agent-facing entry point. It explains:

- the purpose and limits of the reference;
- how an agent locates and applies component guidance;
- requirement and evidence labels;
- global native-control defaults;
- the component and foundation index;
- the evaluation gate.

It must remain concise enough to load at the beginning of a UI task. Detailed guidance belongs in component and foundation pages.

### 6.2 Foundation pages

Foundation pages contain rules shared by several components:

- `foundations/text-and-localization.md`
- `foundations/sizing-and-spacing.md`
- `foundations/icons.md`
- `foundations/states-and-themes.md`
- `foundations/accessibility-basics.md`

A component page links only to the foundations it needs. Foundation pages must not become broad Fluent design tutorials.

### 6.3 Component pages

The v0.1 component pages are:

- `components/button.md`
- `components/textbox.md`
- `components/toggleswitch.md`
- `components/combobox.md`
- `components/commandbar.md`
- `components/listview.md`
- `components/infobar.md`
- `components/contentdialog.md`

Each component page uses the same structure:

1. Purpose and characteristic
2. Anatomy
3. Content rules
4. Sizing and layout
5. States and interaction
6. Theme, accessibility, and localization
7. Common failures
8. Minimal native XAML
9. Verification checklist
10. Sources

The page explains the selected component. It does not compare every possible alternative control.

### 6.4 Source records

`sources/manifest.yaml` records the exact evidence set used by the active reference.

Each source record contains:

```yaml
id: MS-WIN-CONTROLS-BUTTON
kind: official-doc
url: https://learn.microsoft.com/windows/apps/develop/ui/controls/buttons
retrieved_at: 2026-08-06
revision: page-last-updated-or-content-commit
scope:
  - button
notes: Windows button guidance used by the v0.1 Button page.
```

The manifest records facts about source identity and version. It does not store copied documentation text.

For WinUI 3 Gallery, `revision` is an exact release tag or commit SHA. For the Windows Design Kit, `revision` is the inspected Figma file or library version plus extraction date. If the kit does not expose a semantic version, the manifest records the stable file identifier and extraction date.

### 6.5 Extraction notes

Short extraction notes may be stored under `sources/notes/` when a source contains information that must be reconciled with another source. Notes must paraphrase and link; they must not become a local mirror.

## 7. Rule model

A rule is a concise statement embedded in a component or foundation page. There is no executable rule engine in v0.1.

Each rule has:

- a stable local ID;
- a requirement level;
- an evidence type;
- the guidance statement;
- the failure it prevents;
- source references;
- a scope or condition when the guidance is not universal.

Example format:

```markdown
### WINUI-BUTTON-LAYOUT-003

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** localized label clipping caused by an arbitrary fixed width.

Allow the button to size to its content when the layout does not require a bounded width. When a bounded width is required, verify the longest supported localized label and text scaling rather than relying on the design-time English label.

**Sources:** `MS-WIN-CONTROLS-BUTTON`, `WINUI-GALLERY-BUTTON`
```

### 7.1 Requirement levels

- `MUST` means a conformance requirement within the stated scope.
- `SHOULD` means the default recommendation; a deviation needs a concrete product or platform reason.
- `MAY` documents a supported option or conditional behavior.

Requirement level expresses obligation, not source authority.

### 7.2 Evidence types

- `official-doc`: explicitly supported by Microsoft Windows or WinUI documentation.
- `gallery`: demonstrated by the pinned Gallery release or source.
- `ui-kit`: observed in the pinned Windows Design Kit revision.
- `derived`: conservative guidance inferred from cited official evidence.

Evidence type expresses provenance, not importance.

### 7.3 Conflict handling

When sources conflict:

1. record the conflict in the page or extraction note;
2. prefer current Windows/WinUI documentation for runtime behavior;
3. use Gallery to confirm executable behavior for the pinned revision;
4. treat the UI kit as visual composition evidence, not runtime authority;
5. avoid a normative rule when the conflict cannot be resolved;
6. state that the reference does not define the disputed behavior.

Do not silently merge two sources into a stronger rule than either source supports.

## 8. Source acquisition and copyright boundary

The authoring process may inspect official pages, Gallery source, and the Windows Design Kit. The repository stores only what is necessary for the reference:

- paraphrased rules;
- small attributed code examples when needed;
- source identifiers and retrieval metadata;
- concise extraction notes;
- original evaluation fixtures created for LazyDesign.

The repository must not store:

- copied documentation pages;
- large portions of Gallery source;
- exported Windows Design Kit libraries;
- Figma screenshots or assets without a verified redistribution basis;
- font files;
- credentials or Figma access tokens.

The license for original LazyDesign content must be chosen before public release of the first component pages. Third-party excerpts retain their own license and attribution requirements.

## 9. v0.1 vertical slice

The first eight controls were chosen to cover different failure classes:

| Control | Failure classes exercised |
|---|---|
| Button | concise labels, icons, emphasis, content sizing, native states |
| TextBox | header/placeholder/helper separation, validation, text fit |
| ToggleSwitch | state labels, immediate setting behavior, accessible state |
| ComboBox | selection content, placeholder, popup and long-item behavior |
| CommandBar | icons, labels, priority, overflow |
| ListView | item density, selection, long content, empty state relationships |
| InfoBar | severity, title/message/action composition, dismissal |
| ContentDialog | title/body/actions, long content, focus and keyboard flow |

The slice is intentionally broader than the smallest possible Button-only test because it must prove that the document schema works across input, command, collection, feedback, and modal components.

## 10. Evaluation design

### 10.1 Comparison

Each evaluation scenario has two runs:

- **Baseline:** the model receives the task and project context without LazyDesign.
- **Guided:** the model receives the identical task and project context plus `DESIGN.md` and the relevant component/foundation pages.

Both runs use:

- the same model family and reasoning level;
- fresh contexts;
- the same starting repository state;
- the same task text;
- the same Windows App SDK and project settings;
- the same evaluator and rubric.

The comparison must not give the guided run additional product requirements that are absent from the baseline prompt.

### 10.2 Scenarios

#### Scenario A: connection settings

Required controls:

- TextBox
- ComboBox
- ToggleSwitch
- Button

The fixture includes long Korean labels, helper text, validation feedback, and a narrow layout.

#### Scenario B: device list

Required controls:

- CommandBar
- ListView
- Button

The fixture includes long item names, secondary metadata, selection, empty content, and constrained width.

#### Scenario C: failure and confirmation

Required controls:

- InfoBar
- ContentDialog
- Button

The fixture includes a long failure explanation, severity, an optional recovery action, destructive confirmation, and keyboard interaction requirements.

### 10.3 Rubric

Each category scores 0, 1, or 2:

1. content length and overflow;
2. information hierarchy;
3. required component anatomy;
4. native interaction states;
5. accessibility basics;
6. localization and text scaling resilience;
7. preservation of native WinUI styling;
8. component-specific characteristics;
9. separation of labels, helper text, and explanatory content;
10. XAML simplicity and relevance.

Maximum score: 20 per scenario, 60 total.

### 10.4 Gate

v0.1 passes when all conditions are met:

- guided total score improves by at least 20%;
- clipping and content-overflow defects decrease by at least 50%;
- missing anatomy and accessibility requirements decrease;
- unnecessary `ControlTemplate` replacement does not increase;
- guided output does not materially increase irrelevant XAML or complexity;
- the evaluator can trace the observed improvements to specific reference rules.

If the gate fails, the project revises retrieval, page structure, or rule wording before adding more controls.

## 11. Verification levels

LazyDesign reports verification evidence precisely.

1. **Document review** — internal consistency and source traceability.
2. **Static XAML review** — component structure and obvious properties.
3. **Build verification** — the generated WinUI project compiles.
4. **Rendered verification** — the target state was observed in a running app.
5. **Environment verification** — specific themes, high contrast, text scaling, DPI, keyboard, or assistive behavior were tested.

A lower level never implies a higher one.

The official WinUI 3 Gallery is reused as a runtime and source reference. LazyDesign does not create a replacement Gallery. Evaluation fixtures may use minimal WinUI pages solely to render generated results.

## 12. Precision-version expansion

After the v0.1 gate passes, full precision work proceeds by component families rather than by arbitrary page count:

1. remaining basic input and command controls;
2. text, selection, and picker controls;
3. collection and data-presentation controls;
4. navigation controls;
5. flyouts, dialogs, teaching, and feedback controls;
6. progress, media, and specialized controls;
7. shared Windows foundations and design guidance.

The final precision version adds:

- all relevant documented variants and states;
- Light and Dark rendered checks;
- Windows High Contrast checks where supported;
- keyboard and focus checks;
- 100%, 125%, 150%, and 200% scaling or text-scaling checks as applicable;
- long Korean and English fixtures;
- exact Gallery revision records;
- Windows Design Kit revision records;
- cross-page terminology and contradiction review;
- repeated agent evaluation across representative tasks.

Full precision does not mean copying every API property. It means that the component's basic visual and interaction contract is complete enough to prevent avoidable agent mistakes.

## 13. Error handling and incomplete evidence

- If an official page is unavailable, record the failed retrieval and do not fabricate its contents.
- If Figma access is unavailable, author the page from available official sources and mark UI-kit evidence as unverified; the page cannot be called precision-complete.
- If Gallery behavior differs from documentation, record both and scope the active rule to the pinned environment.
- If an example does not build, keep the failing evidence and do not publish it as a minimal valid example.
- If an evaluation run is interrupted or uses a different model configuration, discard it from the controlled comparison and record the reason.
- If a rule does not affect observable output, keep it as informational guidance or remove it from the v0.1 normative set.

## 14. Repository and delivery strategy

- `main` contains reviewed, internally consistent reference releases.
- Work occurs on focused branches and enters through pull requests.
- Source capture, component authoring, and evaluation may be separate commits but must remain traceable as one vertical slice.
- GitHub Actions are not part of the initial design.
- The first PR contains documentation bootstrap only.
- The second implementation phase creates the source manifest, foundations, component pages, and evaluation materials described in the companion plan.

## 15. Definition of done

### Documentation bootstrap

Complete when:

- README accurately states purpose and non-goals;
- repository instructions constrain scope and evidence handling;
- `DESIGN.md` gives agents a usable entry point;
- this design specification is internally consistent;
- the v0.1 implementation plan maps every requirement to a concrete task;
- all files are committed on a focused branch.

### v0.1 implementation

Complete when:

- the source manifest pins all evidence used by the slice;
- five foundation pages are reviewed;
- eight component pages satisfy the page contract;
- all minimal XAML examples build in the pinned environment;
- fixed baseline and guided prompts are committed;
- all six controlled runs are recorded;
- rubric scoring and evidence are committed;
- the gate decision and required revisions are documented.

### Full precision target

Complete when the agreed core WinUI 3 control set has source-backed component pages, relevant rendered and environment checks, cross-page consistency review, and repeated evaluation evidence showing that the reference continues to improve agent output.
