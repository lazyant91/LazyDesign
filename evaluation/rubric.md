# LazyDesign v0.1 Scoring Rubric

Score each generated scenario independently. Use only the immutable generated files, recorded build output, and runtime observations made before any repair.

Each category receives `0`, `1`, or `2` points. A score without evidence is invalid.

## Evidence format

For every category record:

```text
Score: 0 | 1 | 2
Evidence: <file:line-range, build record, or rendered observation>
Related rules: <LazyDesign rule IDs or none>
Uncertainty: none | <specific reason>
```

Static source evidence must identify a file and line range. Runtime evidence must state the environment and observed state. Do not infer rendered behavior from XAML alone.

## 1. Content length and overflow

### 0

One or more required labels, values, messages, commands, list items, or dialog contents are clipped, obscured, overlap another element, or use a control-inappropriate amount of text. The generated layout contains an obvious fixed-size risk with no evidence that the required fixture can fit.

### 1

Most content is readable, but one required long string has weak handling, unnecessary truncation, unverified wrapping, or a fragile fixed dimension. Static structure suggests resilience but rendered evidence is absent where it is needed to resolve doubt.

### 2

All required Korean and English fixture strings remain readable in the specified constrained width. Wrapping, scrolling, popup layout, or intrinsic sizing matches each component's role, with no observable clipping or collision.

## 2. Information hierarchy

### 0

Primary, secondary, helper, validation, status, or action information is visually or structurally indistinguishable. The screen presents competing emphasis or hides the user's next action.

### 1

The basic hierarchy is present but inconsistent. One section over-emphasizes secondary content, repeats information, or weakens grouping.

### 2

The implementation consistently separates primary labels and actions from helper, status, metadata, and validation content. Grouping and emphasis make the next action clear without adding unrelated design structure.

## 3. Component anatomy

### 0

A required native component is replaced, or essential parts are omitted or placed in the wrong region. Examples include a TextBox without a persistent label when required, an InfoBar without required status content, or manually placed ContentDialog command buttons.

### 1

The native component is present and most anatomy is correct, but one required part is missing, duplicated, or represented through an improvised adjacent element without clear association.

### 2

Every required component uses its expected native anatomy and properties. Required titles, messages, headers, actions, command areas, item contents, selections, and validation relationships are present and correctly associated.

## 4. Native interaction states

### 0

The implementation removes, replaces incompletely, or visibly breaks required native states such as pointer-over, pressed, focused, disabled, selected, checked, open, error, dialog, or overflow behavior.

### 1

Native controls are retained, but a required state is unhandled, not visible, or not verified. Static code does not obviously break states, yet required runtime evidence is incomplete.

### 2

Required native states and transitions remain intact and are verified for the scenario, including keyboard focus and scenario-specific selected, checked, open, dialog, or overflow behavior.

## 5. Accessibility basics

### 0

A required interactive element lacks an accessible name, state, label association, keyboard path, or meaningful non-color status. The implementation creates a clearly misleading UI Automation role.

### 1

Most accessible names and native roles are preserved, but one important association, state announcement, focus path, or non-color cue is missing or unverified.

### 2

Native roles are preserved; interactive elements expose meaningful names and states; labels and values are associated; keyboard operation and focus visibility are verified; status and severity remain understandable without color alone.

## 6. Localization and scaling resilience

### 0

The implementation hard-codes dimensions or content placement that fails the supplied Korean or English strings, or it has an observable text-scaling failure.

### 1

The supplied strings fit statically, but a fragile dimension, untested popup, fixed item height, or missing scaling evidence leaves a material risk.

### 2

The required Korean and English strings work at the specified width, and relevant text-scaling or constrained-width behavior is verified without loss of content or control operation.

## 7. Native WinUI style preservation

### 0

The output introduces a local `ControlTemplate`, hand-built substitute, or fixed color system that unnecessarily replaces native WinUI styling or theme behavior.

### 1

Native controls are used, but superficial local styling duplicates built-in styles, relies on fixed colors, or creates avoidable maintenance risk.

### 2

The implementation uses native WinUI controls, built-in styles, and theme resources. No unnecessary template replacement or custom imitation is introduced.

## 8. Component-specific characteristics

### 0

One or more required controls are used in a way that contradicts their documented characteristic. Examples include a ToggleSwitch whose state does not match the applied setting, a ComboBox with broken selection semantics, or a non-modal substitute for ContentDialog.

### 1

The components broadly match their intended behavior, but one scenario-specific characteristic such as CommandBar overflow, ListView selection, InfoBar lifetime, or dialog default action is weak or unverified.

### 2

Each required control preserves the scenario-relevant characteristics described by its component page, with corresponding source or runtime evidence.

## 9. Label, helper, and explanation separation

### 0

Persistent labels, placeholders, helper text, validation text, values, or explanatory paragraphs are used interchangeably or embedded in the wrong control.

### 1

Most roles are separated, but one helper, placeholder, validation, list metadata, InfoBar message, or dialog explanation is duplicated or ambiguously placed.

### 2

Persistent labels identify controls; placeholders remain optional hints; helper text supports entry; validation identifies a problem and recovery; explanations remain outside concise action labels and values.

## 10. XAML simplicity and relevance

### 0

The generated output contains substantial unrelated UI, unnecessary abstractions, custom controls, template code, or complexity that obscures the requested scenario.

### 1

The implementation is usable but includes avoidable wrappers, repeated resources, event plumbing, or styling not required by the task.

### 2

The output contains the smallest clear XAML and supporting code necessary for the scenario, with no unrelated architecture or speculative feature work.

## Scenario totals

Each scenario has a maximum of 20 points.

```text
Connection settings: baseline __ / 20, guided __ / 20
Device list: baseline __ / 20, guided __ / 20
Failure and confirmation: baseline __ / 20, guided __ / 20
Total: baseline __ / 60, guided __ / 60
```

## Target defect counts

Record these separately from the point score:

- clipping or content-overflow defects;
- missing component anatomy;
- missing accessible names, states, or associations;
- unnecessary local `ControlTemplate` replacements;
- irrelevant XAML or added complexity;
- build failures;
- rendered verification failures.

A single defect may affect more than one rubric category, but count the observable defect once in the defect table and explain its rubric impact.

## Gate calculations

Use the implementation plan's mechanical gate.

```text
Improvement percent = ((guided total - baseline total) / baseline total) * 100
Overflow reduction percent = ((baseline overflow defects - guided overflow defects) / baseline overflow defects) * 100
```

When the baseline denominator is zero, mark the percentage condition `not demonstrated` rather than treating it as automatically passed. The overall gate passes only when every required condition has affirmative evidence.
