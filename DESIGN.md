# LazyDesign: WinUI 3 Component Reference

## Purpose

Use this reference when implementing or reviewing WinUI 3 UI. It supplies component-specific constraints that a coding agent might otherwise guess or omit.

This reference does not select controls, invent a visual identity, or override product requirements. The project or user still decides what the screen must do and which control is appropriate. LazyDesign explains how a selected control should preserve its basic WinUI and Fluent characteristics.

## Current status

The v0.1 source manifest, five shared foundation pages, and all eight component pages are present as source-backed evaluation candidates. They are ready for controlled baseline/guided comparison, but they have not yet passed the v0.1 quality gate. Windows Design Kit identity is recorded, while component-level UI-kit inspection remains pending and does not support active rules.

An absent rule is not permission to present a guess as official guidance.

## How an agent must use the reference

1. Identify the WinUI controls already required by the task or existing code.
2. Read the relevant component pages.
3. Read only the foundation pages referenced by those component pages.
4. Apply `MUST` rules before implementation details.
5. Apply `SHOULD` rules unless the product requirement provides a concrete reason not to.
6. Preserve native WinUI styling, visual states, input behavior, and accessibility unless a documented requirement requires customization.
7. Run the component verification checklist after implementation.
8. Report which checks were performed and which were not.

## Rule notation

Each normative rule uses two independent labels.

### Requirement level

- `MUST` — required for conformance within the rule's stated scope.
- `SHOULD` — recommended default; deviation requires a concrete reason.
- `MAY` — supported option or conditional guidance.

### Evidence type

- `official-doc` — explicitly supported by Microsoft Windows or WinUI documentation.
- `gallery` — demonstrated by the official WinUI 3 Gallery app or source.
- `ui-kit` — observed in the inspected Microsoft Windows Design Kit revision.
- `derived` — a conservative conclusion from cited official evidence, clearly identified as an inference.

Example:

```text
WINUI-BUTTON-CONTENT-001 · MUST · official-doc
Keep the visible label concise and action-oriented.
Prevents: paragraph-length button content and ambiguous action labels.
```

The example above demonstrates the format only. Active rules appear in component or foundation pages with source references.

## Global defaults

These defaults apply while component-specific guidance is being evaluated:

- Prefer native WinUI controls and styles.
- Do not replace a `ControlTemplate` merely to change a basic color, radius, padding, or state appearance.
- Do not remove native pointer-over, pressed, focused, disabled, selected, or validation states.
- Do not use fixed dimensions where localized text or text scaling can change the required size, unless the official component behavior requires a fixed dimension.
- Do not place explanatory paragraphs inside controls intended for concise labels or values.
- Icon-only interactive controls require an accessible name.
- A successful XAML build is not evidence that rendered states, text scaling, contrast themes, keyboard behavior, or assistive technology were verified.

Component pages replace these defaults with more precise source-backed guidance where applicable.

## v0.1 component index

| Component | Reference status | Primary risk covered |
|---|---|---|
| Button | v0.1-candidate | label overflow, icon use, emphasis, native states |
| TextBox | v0.1-candidate | header/placeholder/helper confusion, text fit, validation |
| ToggleSwitch | v0.1-candidate | state labeling, immediate setting behavior, accessibility |
| ComboBox | v0.1-candidate | placeholder and selection content, popup width, long items |
| CommandBar | v0.1-candidate | icon/label composition, priority, overflow behavior |
| ListView | v0.1-candidate | item information density, selection states, long content |
| InfoBar | v0.1-candidate | title/message/action composition, severity, dismissal |
| ContentDialog | v0.1-candidate | title/body/button composition, long content, focus |

## v0.1 foundation index

| Foundation | Reference status |
|---|---|
| Text and localization | v0.1-candidate |
| Sizing and spacing | v0.1-candidate |
| Icons | v0.1-candidate |
| States and themes | v0.1-candidate |
| Accessibility basics | v0.1-candidate |

`v0.1-candidate` means the page has source IDs, no unresolved authoring markers, and has been checked for scope and internal consistency. It does not mean the controlled evaluation, WinUI build, rendered state checks, scaling, contrast theme, keyboard, or assistive-technology verification has passed.

## Source authority

Use the following order when evidence differs:

1. Current Windows or WinUI documentation for the target control and behavior.
2. Runtime behavior and source from the pinned WinUI 3 Gallery revision.
3. Component structure and visual states from the pinned Windows Design Kit revision.
4. Fluent 2 supplemental guidance that is not platform-specific.
5. A rule marked `derived`, with its reasoning and limits.

The exact source set and evidence status are in `sources/manifest.yaml`. A source marked inspection-pending cannot support an active `ui-kit` rule.

Do not import implementation rules from another Fluent platform merely because the component has the same name.

## Non-goals

Do not use LazyDesign to:

- choose between unrelated controls;
- generate a complete information architecture;
- enforce a brand or theme;
- introduce custom resource dictionaries automatically;
- install a framework adapter;
- reject all hard-coded values categorically;
- claim Microsoft endorsement for derived guidance;
- replace WinUI 3 Gallery or Microsoft Learn.

## Evaluation gate

The v0.1 reference advances to full component coverage only when controlled before/after evaluation demonstrates:

- at least 20% improvement in the total rubric score;
- at least 50% reduction in clipping or content-overflow defects;
- fewer missing anatomy and accessibility requirements;
- no increase in unnecessary `ControlTemplate` replacement;
- no material increase in irrelevant XAML or prompt-driven overengineering;
- traceability from observed improvements to specific reference rules.

Until all gate conditions pass, these pages remain `v0.1-candidate` and expansion to additional controls is blocked.

The detailed product design and execution plan are stored in:

- `docs/superpowers/specs/2026-08-06-winui3-component-reference-design.md`
- `docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`
