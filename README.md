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

All thirteen pages remain `v0.1-candidate`. The initial controlled v0.1 comparison remains preserved as Gate v1 **FAIL**: baseline scored 44/60 and guided scored 46/60 (+4.55%), and the original zero-baseline overflow rule was not demonstrated. That historical decision remains in [`evaluation/results/gate-decision.md`](evaluation/results/gate-decision.md).

The separate `v0.1-r1` comparison also returns **Gate v2 FAIL**. Its scored totals are 15/60 baseline and 36/60 guided (+140.0%); overflow remains zero-to-zero as a non-regression floor, anatomy defects decrease 6→2, accessibility defects decrease 4→1, ControlTemplate and complexity counts remain 0→0, and all 17 positive category deltas have rule/evidence traces. However, the hard guided-build prerequisite fails because guided build statuses are `connection-settings=pass`, `device-list=pass`, `failure-confirmation=not_run`. The detailed revision decision is recorded in [`evaluation/revisions/v0.1-r1/results/gate-decision.md`](evaluation/revisions/v0.1-r1/results/gate-decision.md).

The revision result is also strongly confounded by execution infrastructure: baseline device-list produced no source, baseline failure-confirmation produced only a partial title change, and guided failure-confirmation never began generation because the Temporary Chat's mandatory harness invocation was blocked by the Remote safety inspection. A post-hoc controller investigation also reproduced the two `Microsoft.UI.Xaml.dll` startup crashes and traced both to the historical start fixture omitting `XamlControlsResources`; adding only that resource dictionary made both frozen generated screens render. The scored captures, historical matrices, and Gate v2 decision remain immutable. The working-tree fixture is corrected only for future evaluation revisions, and the harness now has a versioned schema-2 execution contract that records controller-reconciled generation attempts and blocks scoring when external infrastructure interruption makes any cell invalid. No new six-run experiment has been executed under that contract yet. See [`evaluation/investigations/2026-08-08-runtime-startup.md`](evaluation/investigations/2026-08-08-runtime-startup.md) and [`docs/superpowers/specs/2026-08-08-evaluation-execution-reliability-design.md`](docs/superpowers/specs/2026-08-08-evaluation-execution-reliability-design.md).

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
- [`docs/superpowers/specs/2026-08-08-evaluation-execution-reliability-design.md`](docs/superpowers/specs/2026-08-08-evaluation-execution-reliability-design.md) — schema-2 execution-validity and Gate v3 design.
- [`docs/superpowers/plans/2026-08-08-evaluation-execution-reliability.md`](docs/superpowers/plans/2026-08-08-evaluation-execution-reliability.md) — implementation plan for execution readiness and report blocking.
- [`docs/superpowers/plans/2026-08-08-v0.1-r2-clean-evaluation.md`](docs/superpowers/plans/2026-08-08-v0.1-r2-clean-evaluation.md) — next clean six-run evaluation plan; the r2 matrix is intentionally deferred until the reliability branch has a stable squash-merged main SHA to pin.

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

The initial v0.1 Gate v1 result remains **FAIL**, and the separate `v0.1-r1` Gate v2 result is also **FAIL**. The revision changed only typed `x:Bind` item-model compatibility in `components/listview.md`, C#/WinRT `ContentDialog.ShowAsync()` awaitability in `components/contentdialog.md`, and actual InfoBar action activation in `components/infobar.md`; the clean scored input snapshot is `d40d08504baf73cf80d8b4f16248a1ee86d8c252`. Prompt bytes, the pinned starting fixture, constrained widths, and scenario-specific reference path sets remained unchanged.

The revision's six captured results validate mechanically, but the run set contains execution failures that limit interpretation. Baseline device-list is an empty generation after Remote safety inspection blocked source writes; baseline failure-confirmation contains only a partial title change; guided failure-confirmation is an empty generation after its mandatory pre-generation harness command was blocked. Guided connection-settings built and completed the available 420-DIP runtime/UIA checks. Guided device-list built successfully with the revised public get/set typed-`x:Bind` model, removing the prior CS8852 failure, but the historical fixture then failed XAML resource lookup before rendering.

Gate v2 scored 15/60 baseline and 36/60 guided (+140.0%). All six quality conditions pass mechanically, including zero-defect overflow non-regression, but the hard build prerequisite fails because the three guided build statuses are `pass`, `pass`, and `not_run`. The approved local workspace is `Z:\workspace\LazyDesign`. All pages therefore remain candidates and precision expansion remains blocked. The runtime-startup root cause is isolated to the historical fixture's missing `XamlControlsResources` merge, and the working-tree fixture plus schema-2 execution-validity contract are now corrected for future revisions. The next controlled step is a new versioned six-run experiment: every cell must be execution-valid under Gate v3 before the existing Gate v2 quality formula is allowed to produce a PASS/FAIL decision. The v0.1-r2 execution plan is prepared, but its matrix must not be created until these reliability changes are squash-merged and a stable main-branch fixture SHA exists to pin.
