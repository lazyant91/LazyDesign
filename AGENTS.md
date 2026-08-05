# LazyDesign repository instructions

These instructions apply to all work in this repository.

## Product intent

LazyDesign is a source-backed WinUI 3 Fluent component reference for AI-assisted UI development. Its first responsibility is to prevent small, repeated component mistakes by making official and observed component behavior explicit.

The project does not choose controls for the agent, design complete screens, or replace native WinUI behavior.

## Current scope

The active scope is the v0.1 vertical slice:

- WinUI 3 only;
- Button, TextBox, ToggleSwitch, ComboBox, CommandBar, ListView, InfoBar, and ContentDialog;
- text and localization, sizing and spacing, icons, states and themes, and accessibility basics;
- Markdown reference content and an evaluation harness;
- no rule engine, resolver, adapter, validator, custom control library, or Gallery clone.

Do not broaden the scope until the v0.1 evaluation gate passes and the repository owner approves the next phase.

## Source policy

Use sources in this order:

1. Microsoft Learn documentation for Windows and WinUI.
2. The official `microsoft/WinUI-Gallery` repository and released Gallery app.
3. The Microsoft Windows Design Kit for Figma.
4. Fluent 2 documentation for supplemental principles that do not override Windows-specific guidance.

Do not treat web, Android, iOS, React, or other Fluent implementations as WinUI requirements.

Every normative rule must record:

- a stable local rule ID;
- requirement level: `MUST`, `SHOULD`, or `MAY`;
- evidence type: `official-doc`, `gallery`, `ui-kit`, or `derived`;
- one or more source references;
- the concrete failure the rule prevents.

A `derived` rule must state the reasoning that connects its sources to the guidance. Never describe a derived rule as an explicit Microsoft requirement.

## Documentation style

- Write concise operational guidance, not broad tutorials.
- Preserve official control and property names.
- Separate component facts from screen-level design advice.
- State what an agent must verify, not only what a control can do.
- Prefer short native XAML examples over custom templates.
- Include long Korean and English content where overflow or localization matters.
- Do not copy large passages, screenshots, exported Figma assets, or source files into the repository.
- Paraphrase guidance and retain links, retrieval dates, and source revisions.

## Component page contract

Every component page must use the same top-level sections:

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

A component page is incomplete if it omits a relevant section without explaining why that section does not apply.

## Evidence and ambiguity

- Conflicting official sources must be recorded, not silently reconciled.
- A rule unsupported by available sources must be omitted or marked `derived` with explicit reasoning.
- Figma observations describe the inspected kit revision only; they do not automatically define runtime behavior.
- Gallery samples demonstrate supported behavior but are not automatically universal requirements.
- When the source does not answer a question, say that the reference does not define it.

## Evaluation policy

The project is successful only if the reference improves generated UI.

For v0.1:

- use the same model, reasoning level, prompt, project state, and evaluation rubric for baseline and guided runs;
- run baseline and guided tasks in fresh contexts;
- record generated files and scoring evidence;
- distinguish static XAML review, successful build, and rendered runtime verification;
- do not claim theme, high-contrast, scaling, or accessibility success unless that check was actually performed.

## Git workflow

- Do not implement features directly on `main`.
- Use a focused branch and a pull request.
- Keep source research, component authoring, and evaluation changes reviewable.
- Do not add GitHub Actions unless the repository owner explicitly requests them.
- Do not rewrite or delete unrelated user changes.
- Before reporting completion, verify the branch, final commit SHA, changed files, document links, and working-tree or pull-request state.

## Completion boundary

Documentation bootstrap is complete when README, repository instructions, the agent-facing entry point, the approved design specification, and the v0.1 implementation plan are internally consistent and committed.

v0.1 implementation is complete only after the eight component pages, five foundation pages, source manifest, fixed evaluation prompts, baseline and guided results, and gate decision are committed with evidence.
