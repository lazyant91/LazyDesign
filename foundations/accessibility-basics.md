# Accessibility basics

This foundation records the minimum cross-component accessibility contract. It is not a substitute for the full Microsoft accessibility guidance or target-user testing.

## Name, role, value, and state

### WINUI-A11Y-NAME-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** an interactive control being announced without a meaningful purpose.

Ensure every interactive control has an accessible name from its visible label, header, content, or an explicit automation property. The name must describe the action or field, not the class name, glyph, or implementation detail.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-A11Y-ROLE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** assistive technologies reporting static content as editable or an interactive element as an unrelated role.

Use the native control whose UI Automation role matches the intended interaction. Do not use `TextBox` for static text or a generic focusable container to imitate a standard control without implementing the corresponding accessible behavior.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`, `MS-WINUI3-OVERVIEW`

### WINUI-A11Y-STATE-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** selection, checked state, expansion, validation, or availability being visible but not exposed to assistive technologies.

Preserve the native control properties and state model so WinUI can expose value and state through UI Automation. A custom visual must not replace the semantic state without an equivalent accessible representation.

**Derived reasoning:** The accessibility checklist requires names and states, while native Gallery controls expose semantics through their property models; preserving those properties instead of replacing them with visuals is the conservative implementation inference.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `WINUI-GALLERY-V2-9-3`

## Keyboard and focus

### WINUI-A11Y-KEYBOARD-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** a control being operable by pointer but unreachable or unusable by keyboard.

Preserve the native keyboard behavior of the selected WinUI control. Verify tab navigation, directional navigation where applicable, activation keys, dismissal keys, and text-input priority for controls that edit text.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`, `MS-WIN-ACCESSIBILITY-CHECKLIST`

### WINUI-A11Y-FOCUS-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** keyboard users losing track of the active control after local styling or template changes.

Keep a visible focus indicator in every supported theme and state. Do not remove native focus visuals unless the replacement is rendered and verified for keyboard users and contrast themes.

**Derived reasoning:** Keyboard, contrast, and accessibility-testing guidance require visible, testable focus; retaining native focus visuals unless a replacement is verified across themes follows from those combined requirements.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`, `MS-WIN-CONTRAST-THEMES`, `MS-WIN-ACCESSIBILITY-TESTING`

### WINUI-A11Y-TABORDER-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** tab order following implementation structure rather than the visible and logical task order.

Arrange focusable elements so keyboard navigation follows the visible reading and task sequence. Avoid adding static explanatory text to the tab order merely to make a screen reader announce it.

**Derived reasoning:** Keyboard guidance defines logical navigation and accessible-text guidance distinguishes readable content from focusable controls; aligning tab order with the task sequence without focusing static prose is the resulting inference.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`, `MS-WIN-ACCESSIBLE-TEXT`

## Perceivable content

### WINUI-A11Y-CONTRAST-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** visible text becoming unreadable against its background.

Verify visible text contrast against its rendered background. The Windows accessible-text guidance requires a minimum luminance contrast ratio of 4.5:1 for ordinary visible text, subject to the documented exceptions.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-A11Y-COLOR-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** meaning being lost for users who cannot distinguish the selected colors.

Do not use color as the only indicator of error, selection, severity, status, or required action. Add a textual, iconic, structural, or native state cue.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-A11Y-SCALE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** text and controls clipping, overlapping, or becoming unreachable under Windows text and display scaling.

Retain default WinUI text scaling and verify the supported Windows text-size and display-scale settings. A static code review cannot establish scaling support.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`, `MS-WIN-ACCESSIBILITY-TESTING`

## Labels and instructions

### WINUI-A11Y-LABEL-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** an input being visually labeled but announced without that label, or a placeholder being mistaken for a persistent field name.

Associate visible labels or headers with the input's accessible name. Keep persistent identification outside transient placeholder content when losing the placeholder would make the field ambiguous.

**Derived reasoning:** The accessibility checklist, TextBox guidance, and accessible-text requirements distinguish persistent labels from transient hints; associating the label and avoiding placeholder-only identification is the conservative synthesis.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-CONTROLS-TEXTBOX`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-A11Y-ERROR-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** validation being shown only by color or being announced without a specific problem and recovery direction.

Expose validation state and a concise message that identifies the affected field or action and explains how to recover. Verify focus and announcement behavior in the actual application when validation appears dynamically.

**Derived reasoning:** Accessibility guidance requires perceivable state and testing of dynamic behavior; pairing validation state with a specific recovery message and verifying announcement is the implementation inference from those sources.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-ACCESSIBILITY-TESTING`

## Verification levels

Accessibility claims must state the evidence level:

1. static review of names, roles, properties, and tab order;
2. successful build;
3. rendered keyboard and focus test;
4. Windows theme, contrast, and scaling test;
5. assistive-technology test, such as Narrator and Accessibility Insights.

Passing a lower level does not imply a higher level.

## Verification checklist

- [ ] Every interactive control has a meaningful accessible name.
- [ ] Native control roles and states are preserved.
- [ ] Keyboard navigation and activation were exercised.
- [ ] Focus remains visible in supported themes.
- [ ] Tab order follows the visible task sequence.
- [ ] Text contrast and non-color state cues were verified.
- [ ] Text and display scaling were tested before claiming support.
- [ ] Inputs have persistent, associated labels where needed.
- [ ] Dynamic errors identify the problem and recovery action.
- [ ] The reported accessibility evidence level matches the tests actually performed.

## Sources

- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-ACCESSIBILITY-TESTING`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-CONTRAST-THEMES`
- `MS-WIN-CONTROLS-TEXTBOX`
- `MS-WINUI3-OVERVIEW`
- `WINUI-GALLERY-V2-9-3`
