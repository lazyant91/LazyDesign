# Text and localization

This foundation defines cross-component text roles and localization safeguards. Component pages decide whether a specific control wraps, trims, scrolls, or constrains content.

## Visible text roles

### WINUI-TEXT-ROLE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** editable controls being used to display static explanatory text, which misreports the UI Automation role and adds an unexpected tab stop.

Use `TextBlock` or `RichTextBlock` for static text. Use `TextBox` or `RichEditBox` only when the content is editable or intentionally selectable/copyable with the corresponding edit/read-only behavior.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-TEXT-ROLE-002

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** headers, labels, placeholders, helper text, values, and validation messages being collapsed into one visually noisy string.

Keep each text role separate:

- a label or header identifies the control or field;
- placeholder text gives a short input hint and disappears as the user enters content;
- helper text explains constraints or consequences outside the value area;
- the value is the user's current data;
- validation text reports a specific problem and recovery direction.

Do not rely on placeholder text as the only persistent label for an important field.

**Derived reasoning:** The cited content and control sources assign different purposes to labels, placeholders, values, help, and validation; keeping those roles separate is the conservative synthesis rather than a single quoted Microsoft rule.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`, `MS-WIN-DESIGN-CONTENT`, `MS-WIN-ACCESSIBLE-TEXT`

## Concision and hierarchy

### WINUI-TEXT-CONTENT-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** paragraph-length content inside controls intended for concise labels, commands, states, or values.

Keep control-internal text limited to the control's immediate purpose. Put explanatory paragraphs in surrounding text content, an `InfoBar`, a dialog body, or another component designed for explanation.

**Derived reasoning:** Windows content and typography guidance distinguish concise control text from explanatory prose; moving paragraphs to a suitable surrounding surface is inferred from that hierarchy.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `MS-WIN-DESIGN-TYPOGRAPHY`

### WINUI-TEXT-HIERARCHY-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** hierarchy being expressed through arbitrary font sizes and inconsistent spacing.

Use the Windows type ramp and semantic text styles to distinguish title, body, body-strong, and caption roles. Use spacing and weight together with type role rather than inventing a new font size for every local distinction.

**Sources:** `MS-WIN-DESIGN-TYPOGRAPHY`, `MS-WIN-DESIGN-CONTENT`

## Localization and variable length

### WINUI-TEXT-LOCALIZATION-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** labels and values clipping when Korean, English, or another supported translation is longer than the design-time string.

Treat visible UI strings as variable-length content. Do not choose a fixed width solely because the current language fits. When a bounded width is required, verify the longest supported labels and values in the target layout.

**Derived reasoning:** Accessible-text and content guidance require readable localized text but do not define one fixed width; treating strings as variable length and testing bounded layouts is the resulting inference.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`, `MS-WIN-DESIGN-CONTENT`

### WINUI-TEXT-LOCALIZATION-002

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** a global wrapping rule from making command surfaces, list rows, or input controls behave inconsistently.

Choose wrapping, trimming, scrolling, or layout expansion at the component level. The surrounding layout must provide a deliberate fallback for long content; this foundation does not prescribe one universal text-overflow behavior.

**Derived reasoning:** Windows content guidance and Gallery examples show that overflow behavior depends on the component; choosing wrapping, trimming, scrolling, or expansion per control is therefore an inference against a universal rule.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `WINUI-GALLERY-V2-9-3`

### WINUI-TEXT-LOCALIZATION-003

**Level:** MUST  
**Evidence:** derived  
**Prevents:** reusable examples and generated pages containing hidden, non-localizable UI strings.

Keep user-visible text identifiable and localizable. Do not bury visible strings in drawing data, images, or reusable templates where the application cannot translate or replace them.

**Derived reasoning:** Accessible-text guidance requires user-visible content to remain available to users and assistive technology; keeping strings outside opaque drawing data or images is a localization-oriented inference from that requirement.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`

## Text scaling

### WINUI-TEXT-SCALE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** text becoming unreadable, clipped, or overlapping when Windows text size or display scaling is increased.

Preserve the default text-scaling behavior of WinUI text controls unless a documented exception exists. Verify that surrounding layout, line wrapping, and control sizing remain usable under the supported Windows text and display settings.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`

## Verification checklist

- [ ] Static explanatory content uses a static text element rather than an edit-role control.
- [ ] Labels, placeholders, helper text, values, and validation messages are not used interchangeably.
- [ ] Control-internal text is concise and the explanation is placed outside the control.
- [ ] The layout was reviewed with long Korean and English strings.
- [ ] Fixed widths have a stated layout reason and verified long-content behavior.
- [ ] Text scaling or display scaling was tested before claiming scaling support.
- [ ] User-visible strings remain localizable.

## Sources

- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-CONTROLS-TEXTBOX`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-DESIGN-TYPOGRAPHY`
- `WINUI-GALLERY-V2-9-3`
