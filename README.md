# LazyDesign

LazyDesign is a source-backed **WinUI 3 Fluent component reference for AI-assisted UI development**.

Its purpose is narrow: give an agent the component-specific facts it is most likely to miss when generating WinUI 3 XAML. The reference focuses on basic composition, content limits, sizing behavior, visual states, accessibility, localization, and common implementation mistakes.

LazyDesign is not a UI generator, a control-selection engine, a design-token resolver, or a replacement for WinUI.

## Problem

A capable coding model can still produce small but repeated UI defects when it lacks explicit component guidance. Typical failures include:

- button labels that clip or contain paragraph-length text;
- headers, placeholders, helper text, and validation messages used interchangeably;
- icon-only controls without an accessible name;
- native pointer, pressed, focused, or disabled states replaced incompletely;
- fixed widths and heights that fail with Korean, English, or text scaling;
- control contents that exceed the component's intended visual hierarchy;
- custom templates added where the native WinUI control already provides the required behavior.

LazyDesign reduces those failures by converting official Windows sources into concise, agent-readable component contracts.

## Product boundary

### Included

- WinUI 3 and Windows App SDK desktop UI;
- Fluent behavior as implemented and documented for Windows;
- component anatomy and required elements;
- text, icon, content, sizing, layout, state, theme, accessibility, and localization rules;
- common failure examples and minimal native XAML examples;
- provenance for every normative rule;
- before/after agent evaluation using fixed prompts and scoring criteria.

### Excluded from the initial product

- WPF, UWP, MAUI, Qt, or web Fluent implementations;
- automatic control selection or screen-level UX planning;
- semantic screen contracts, design resolvers, framework adapters, or generated resource dictionaries;
- static analyzers and runtime validators;
- a replacement or fork of WinUI 3 Gallery;
- bulk copies of Microsoft documentation or Figma assets.

These exclusions remain in force until the v0.1 reference demonstrates measurable improvement in agent output.

## Source model

LazyDesign uses four source classes:

1. **Windows documentation** — normative Windows and WinUI guidance.
2. **WinUI 3 Gallery** — executable examples, native behavior, and sample XAML.
3. **Windows Design Kit for Figma** — component anatomy, variants, states, and visual composition.
4. **Fluent 2 documentation** — supplemental cross-cutting guidance only when it does not conflict with Windows-specific behavior.

A rule records both its requirement level (`MUST`, `SHOULD`, or `MAY`) and its evidence type (`official-doc`, `gallery`, `ui-kit`, or `derived`). Derived guidance must never be presented as an explicit Microsoft requirement.

Exact URLs, retrieval dates, revisions, licenses, and evidence limits are recorded in [`sources/manifest.yaml`](sources/manifest.yaml). Source-specific extraction limits are recorded under [`sources/notes/`](sources/notes/).

## v0.1 vertical slice

The candidate reference covers eight representative controls:

- Button
- TextBox
- ToggleSwitch
- ComboBox
- CommandBar
- ListView
- InfoBar
- ContentDialog

It also defines five shared foundations:

- text and localization;
- sizing and spacing;
- icons;
- states and themes;
- accessibility basics.

All thirteen pages remain `v0.1-candidate`. The controlled v0.1 comparison is complete, but the mechanical quality gate failed: baseline scored 44/60 and guided scored 46/60, a 4.55% improvement rather than the required 20%. No baseline clipping/content-overflow defect was directly observed, so the required 50% reduction is not demonstrated. The detailed result is recorded in [`evaluation/results/gate-decision.md`](evaluation/results/gate-decision.md).

The guided connection-settings run improved hierarchy, component anatomy, accessible naming, and theme-resource use. The device-list pair retained the same CS8852 typed-`x:Bind`/positional-record build failure, both failure-confirmation runs retained the same CS4036 `ContentDialog.ShowAsync()` await/projection build failure, and the guided failure-confirmation run additionally generated an inert Retry button. Precision expansion is therefore blocked.

## Repository layout

```text
LazyDesign/
├─ README.md
├─ AGENTS.md
├─ DESIGN.md
├─ components/                 # Eight v0.1 component candidates
├─ foundations/                # Five shared foundation candidates
├─ evaluation/                 # Fixed prompts, rubric, run rules, and later results
├─ sources/                    # Source manifest and extraction notes
├─ scripts/                    # Structural reference checks
└─ docs/
   └─ superpowers/
      ├─ specs/                # Approved design specifications
      └─ plans/                # Executable implementation plans
```

## Documents

- [`DESIGN.md`](DESIGN.md) — agent-facing entry point, reference status, and usage contract.
- [`components/`](components/) — the eight component candidates.
- [`foundations/`](foundations/) — the five shared foundation candidates.
- [`evaluation/README.md`](evaluation/README.md) — controlled run procedure and local Windows execution boundary.
- [`evaluation/rubric.md`](evaluation/rubric.md) — fixed 60-point scoring rubric.
- [`sources/manifest.yaml`](sources/manifest.yaml) — pinned evidence set and source status.
- [`docs/superpowers/specs/2026-08-06-winui3-component-reference-design.md`](docs/superpowers/specs/2026-08-06-winui3-component-reference-design.md) — product and information architecture.
- [`docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`](docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md) — v0.1 implementation plan.

## Authoritative starting sources

- Windows controls and patterns: <https://learn.microsoft.com/windows/apps/design/controls/>
- Windows design resources: <https://learn.microsoft.com/windows/apps/design/downloads/>
- WinUI 3 overview: <https://learn.microsoft.com/windows/apps/winui/winui3/>
- WinUI 3 Gallery: <https://github.com/microsoft/WinUI-Gallery>
- Fluent 2 design resources: <https://fluent2.microsoft.design/get-started/design>

## Current status

Completed in the current v0.1 branch:

- source manifest and source notes;
- component/foundation document contract and structural checker;
- five shared foundations and eight component candidates;
- fixed evaluation procedure, three immutable prompts, and 10-category rubric;
- three baseline and three guided fresh-context artifacts from the same pinned WinUI start project;
- controlled build and available runtime/UI Automation evidence;
- immutable capture validation for all six runs;
- mechanical scoring, findings, and v0.1 gate decision.

The v0.1 gate result is **FAIL**, so the existing eight components and five foundations remain candidates and no new control family is approved. Before rerunning the same gate, revise these exact reference areas from source-backed evidence:

- `components/listview.md` — add build-safe typed-`x:Bind` data-model guidance or an equivalent verified pattern that prevents the observed positional-record/init-only CS8852 failure;
- `components/contentdialog.md` — add a compile-verified minimal `ShowAsync()` C# pattern, including the WinRT async projection/import requirements needed by the pinned evaluation project, to prevent the observed CS4036 failure;
- `components/infobar.md` — strengthen the action verification guidance so an `ActionButton` such as Retry is confirmed to have actual activation behavior rather than only a label.

Keep the existing guided-context scope and fresh-context controls unchanged for the next comparison unless a separately reviewed evaluation-procedure defect is found. The approved local workspace is `Z:\workspace\LazyDesign`. Precision expansion remains blocked until a revised v0.1 run passes the mechanical gate.
