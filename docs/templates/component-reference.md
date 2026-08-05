# <ControlName>

## 1. Purpose and characteristic

State the control's defining role and the characteristic that must remain recognizable after implementation. Do not compare unrelated controls unless the distinction is necessary to explain this control.

### <RULE-ID>

**Level:** MUST | SHOULD | MAY  
**Evidence:** official-doc | gallery | ui-kit | derived  
**Prevents:** <one observable failure>

<Concise operational guidance.>

**Sources:** `<SOURCE-ID>`

## 2. Anatomy

List required and optional visible parts. Distinguish control content from labels, descriptions, helper content, validation, and surrounding layout.

## 3. Content rules

Define text, icon, value, item, and action-content constraints. Include localization and overflow conditions relevant to this control.

## 4. Sizing and layout

Describe native desired-size behavior, legitimate constraints, alignment, surrounding layout, and failure modes caused by arbitrary fixed dimensions.

## 5. States and interaction

Cover only states relevant to the control, such as rest, pointer-over, pressed, focused, disabled, selected, checked, validation, open, or dismissed. State which native behavior must be preserved.

## 6. Theme, accessibility, and localization

Record accessible name/state requirements, keyboard and focus behavior, theme-resource expectations, text scaling, and long Korean/English verification.

## 7. Common failures

List concrete bad outputs an agent is likely to create. Explain why each output violates a rule or loses a native characteristic.

## 8. Minimal native XAML

Provide the smallest original example that demonstrates the intended native control usage. Do not copy a complete Gallery sample or add a custom `ControlTemplate` unless the page specifically documents a justified template case.

## 9. Verification checklist

Use checkboxes that can be answered from static review, build evidence, rendered behavior, or environment testing. Label the required evidence level where ambiguity is possible.

## 10. Sources

List every source ID used by the page and the exact inspected page, file, or component-set path. Note unresolved conflicts and missing evidence.
