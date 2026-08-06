# TextBox

## 1. Purpose and characteristic

Use `TextBox` for plain-text entry or editable plain text. Do not use it to display static text.

### WINUI-TEXTBOX-PURPOSE-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** static text being exposed as editable UI

Use `TextBlock` for static text and `TextBox` only when users can enter, edit, copy, or select plain text as an input experience.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`, `MS-WIN-ACCESSIBLE-TEXT`

## 2. Anatomy

A typical field consists of an optional `Header`, the editable surface, optional `PlaceholderText`, and separate helper or validation text outside the control.

### WINUI-TEXTBOX-ANATOMY-001
**Level:** MUST  
**Evidence:** derived  
**Prevents:** header, placeholder, helper, and validation text being used interchangeably

Use `Header` for the persistent field label, `PlaceholderText` only for a temporary hint, and adjacent text for help or validation.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`, `MS-WIN-CONTROLS-FORMS`

## 3. Content rules

### WINUI-TEXTBOX-CONTENT-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** required meaning disappearing after typing begins

Do not put essential instructions or the only field label in `PlaceholderText`, because it disappears when content is entered.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`, `MS-WIN-CONTROLS-FORMS`

### WINUI-TEXTBOX-CONTENT-002
**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** single-line fields receiving uncontrolled paragraphs

Choose `AcceptsReturn`, wrapping, and scrolling deliberately according to whether the field is single-line or multiline.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`, `WINUI-GALLERY-V2-9-3`

## 4. Sizing and layout

### WINUI-TEXTBOX-SIZE-001
**Level:** MUST  
**Evidence:** derived  
**Prevents:** localized headers or entered values clipping

Avoid arbitrary fixed width. When width is constrained, test the longest supported header, placeholder, entered value, Korean and English content, and text scaling.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-TEXTBOX-SIZE-002
**Level:** SHOULD  
**Evidence:** gallery  
**Prevents:** fields being sized without regard to their expected input

Size the field for its expected value rather than making every form field the same width. Gallery examples demonstrate both simple and multiline configurations.

**Sources:** `WINUI-GALLERY-V2-9-3`

## 5. States and interaction

### WINUI-TEXTBOX-STATE-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** editable and read-only states appearing identical or behaving incorrectly

Use `IsReadOnly` for selectable non-editable text and `IsEnabled="False"` only when the field is unavailable. Verify focus, clear-button behavior, selection, and keyboard input.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`, `WINUI-GALLERY-V2-9-3`

### WINUI-TEXTBOX-INPUT-001
**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** inappropriate keyboard or input behavior

Set input-related properties such as `InputScope`, `MaxLength`, spell checking, and text prediction when the data type requires them.

**Sources:** `MS-WIN-CONTROLS-TEXTBOX`

## 6. Theme, accessibility, and localization

### WINUI-TEXTBOX-A11Y-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** unlabeled fields in UI Automation

Provide a persistent visible label or an accessible name. Ensure validation identifies both the problem and how to correct it.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-CONTROLS-FORMS`

### WINUI-TEXTBOX-THEME-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** focus, border, text, or validation state loss across themes

Preserve native theme resources and verify Light, Dark, and contrast themes after style changes.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Using a `TextBox` to display static text.
- Using placeholder text as the only label.
- Mixing helper and validation messages.
- Fixed width that clips localized headers or long values.
- Multiline input without intentional wrapping and scrolling.
- Disabling a field when read-only behavior is intended.
- Replacing the template for a superficial border or color change.

## 8. Minimal native XAML

```xml
<StackPanel Spacing="4">
    <TextBox Header="Device name"
             PlaceholderText="Enter a name"
             MaxLength="80" />
    <TextBlock Text="Use a recognizable name."
               Style="{StaticResource CaptionTextBlockStyle}" />
</StackPanel>
```

Multiline:

```xml
<TextBox Header="Notes"
         AcceptsReturn="True"
         TextWrapping="Wrap"
         MinHeight="96" />
```

## 9. Verification checklist

- [ ] The control is genuinely editable or intentionally read-only.
- [ ] Header, placeholder, helper, and validation roles are distinct.
- [ ] Single-line versus multiline behavior is explicit.
- [ ] Long Korean and English content and text scaling were checked.
- [ ] Keyboard input, focus, selection, and clear behavior were checked.
- [ ] Accessible name and validation guidance are available.
- [ ] Light, Dark, and contrast themes were checked after styling changes.
- [ ] No superficial `ControlTemplate` replacement was introduced.

## 10. Sources

- `MS-WIN-CONTROLS-TEXTBOX`
- `MS-WIN-CONTROLS-FORMS`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.