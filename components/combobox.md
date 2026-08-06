# ComboBox

## 1. Purpose and characteristic

Use `ComboBox` to present a compact single-selection list that expands on demand. Use editable mode only when typed values are intentionally supported.

### WINUI-COMBO-PURPOSE-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** using a compact selector where multiple selection or persistent comparison is required

Use `ComboBox` for one selection from a list. Use another control when users must compare many choices at once or select multiple items.

**Sources:** `MS-WIN-CONTROLS-COMBOBOX`

## 2. Anatomy

A combo box consists of an optional `Header`, a compact selection field, optional `PlaceholderText`, an expand affordance, and a popup list of items.

### WINUI-COMBO-ANATOMY-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** ambiguous empty state and missing field identity

Provide a persistent header when context does not identify the field. Use placeholder text to explain the unselected state, not as the only label.

**Sources:** `MS-WIN-CONTROLS-COMBOBOX`, `MS-WIN-CONTROLS-FORMS`

## 3. Content rules

### WINUI-COMBO-CONTENT-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** mixing direct items and a bound source

Populate the control through either `Items` or `ItemsSource`, not both.

**Sources:** `MS-WIN-CONTROLS-COMBOBOX`

### WINUI-COMBO-CONTENT-002
**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** inconsistent or hard-to-scan option lists

Use concise, parallel option labels. Avoid explanatory paragraphs inside list items; provide supporting text outside the selector when needed.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `MS-WIN-CONTROLS-COMBOBOX`

### WINUI-COMBO-EDITABLE-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** accepting arbitrary text when only listed values are valid

Set `IsEditable="True"` only when typed input is part of the product requirement and validation handles values not present in the list.

**Sources:** `MS-WIN-CONTROLS-COMBOBOX`

## 4. Sizing and layout

### WINUI-COMBO-SIZE-001
**Level:** MUST  
**Evidence:** derived  
**Prevents:** selected value or popup item clipping

Size for the longest realistic selected item and inspect the expanded popup. Test Korean, English, and text scaling rather than sizing only for placeholder text.

**Sources:** `MS-WIN-CONTROLS-COMBOBOX`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-COMBO-SIZE-002
**Level:** SHOULD  
**Evidence:** gallery  
**Prevents:** every selector receiving an arbitrary identical fixed width

Use `MinWidth` when a minimum field size is needed and let layout provide additional space. Gallery demonstrates inline items, bound item templates, and editable mode without replacing the native template.

**Sources:** `WINUI-GALLERY-V2-9-3`

## 5. States and interaction

### WINUI-COMBO-STATE-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** selection shown in UI but not reflected in application state

Keep `SelectedItem`, `SelectedValue`, or `SelectedIndex` synchronized with the actual value. Handle the no-selection state explicitly.

**Sources:** `MS-WIN-CONTROLS-COMBOBOX`

### WINUI-COMBO-KEYBOARD-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** inaccessible popup navigation

Verify keyboard focus, opening, item navigation, selection, cancellation, and focus return.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`

## 6. Theme, accessibility, and localization

### WINUI-COMBO-A11Y-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** an unlabeled selector or unclear current value

Expose a clear accessible name and current selection. Ensure custom item templates preserve readable text and logical navigation.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-CONTROLS-COMBOBOX`

### WINUI-COMBO-THEME-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** popup, selection, focus, or disabled states disappearing across themes

Preserve native theme resources and verify the closed field and expanded popup in Light, Dark, and contrast themes after styling changes.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Using `ComboBox` for multiple selection.
- Placeholder text acting as the only field label.
- Mixing `Items` and `ItemsSource`.
- Enabling editable mode without validation.
- Sizing only for the placeholder and clipping selected values.
- Testing the closed control but not the expanded popup.
- Custom item templates that remove readable labels or focus cues.

## 8. Minimal native XAML

```xml
<ComboBox Header="Connection mode"
          PlaceholderText="Choose a mode"
          MinWidth="220"
          ItemsSource="{x:Bind ViewModel.ConnectionModes}"
          SelectedItem="{x:Bind ViewModel.SelectedConnectionMode, Mode=TwoWay}" />
```

Editable:

```xml
<ComboBox Header="Font size"
          IsEditable="True"
          ItemsSource="{x:Bind ViewModel.CommonFontSizes}" />
```

## 9. Verification checklist

- [ ] Single-selection compact disclosure is appropriate.
- [ ] Header and placeholder serve distinct roles.
- [ ] Only one population mechanism is used.
- [ ] Editable mode has a validation path.
- [ ] Long selected values and popup items do not clip.
- [ ] Korean, English, and text scaling were checked.
- [ ] Keyboard popup navigation and focus return work.
- [ ] Accessible name and current selection are exposed.
- [ ] Closed and expanded states were checked across themes.

## 10. Sources

- `MS-WIN-CONTROLS-COMBOBOX`
- `MS-WIN-CONTROLS-FORMS`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.