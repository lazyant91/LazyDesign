# Button

## 1. Purpose and characteristic

Use `Button` for an immediate command. The visible label should describe the action, not the object or a paragraph of explanation.

### WINUI-BUTTON-PURPOSE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** ambiguous commands whose result is unclear

Use concise, action-oriented text that states what happens when the button is invoked.

**Sources:** `MS-WIN-CONTROLS-BUTTONS`

### WINUI-BUTTON-EMPHASIS-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** multiple competing primary actions

Use the accent button style for the single primary action in a local decision area. Keep peer actions at the default emphasis unless product requirements establish a different hierarchy.

**Derived reasoning:** The Button guidance documents built-in accent emphasis and the Gallery demonstrates that native style; reserving it for one local primary action is a conservative hierarchy inference, not an explicit universal Microsoft limit.

**Sources:** `MS-WIN-CONTROLS-BUTTONS`, `WINUI-GALLERY-V2-9-3`

## 2. Anatomy

A native button consists of the control surface, its content presenter, and WinUI-provided interaction states. Content may be text, an icon, or a small composition of both.

### WINUI-BUTTON-ANATOMY-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** loss of native states and input behavior

Preserve the native `Button` control and default template unless a documented product requirement cannot be met through properties, styles, or content.

**Sources:** `MS-WIN-CONTROLS-BUTTONS`

## 3. Content rules

### WINUI-BUTTON-CONTENT-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** paragraph-length labels and severe wrapping

Keep the visible label short. Place explanatory text beside or above the button instead of inside it.

**Derived reasoning:** The Button content model permits text while Windows content guidance separates actions from explanation; keeping labels concise and moving explanation outside the control is therefore an inference to prevent wrapping, not a fixed Microsoft word-count rule.

**Sources:** `MS-WIN-CONTROLS-BUTTONS`, `MS-WIN-DESIGN-CONTENT`

### WINUI-BUTTON-ICON-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** inaccessible icon-only commands

When a button has only an icon, provide an accessible name that communicates the command.

**Sources:** `MS-WIN-CONTROLS-ICONS`, `MS-WIN-ACCESSIBILITY-CHECKLIST`

### WINUI-BUTTON-ICON-002

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** unfamiliar or ambiguous icon commands

Retain a text label when the icon is not universally recognizable in the target context.

**Derived reasoning:** The icon guidance defines supported icon usage but does not guarantee that every glyph is self-explanatory; retaining text for unfamiliar icons is a conservative usability inference from that limitation.

**Sources:** `MS-WIN-CONTROLS-ICONS`

## 4. Sizing and layout

### WINUI-BUTTON-SIZE-001

**Level:** MUST  
**Evidence:** gallery  
**Prevents:** localized labels clipping inside arbitrary fixed widths

Start with the native desired size. When a fixed or constrained width is necessary, verify the longest supported Korean and English labels and text scaling. Gallery includes an explicit wrapped-content example, which demonstrates that long content requires deliberate layout handling.

**Sources:** `WINUI-GALLERY-V2-9-3`

### WINUI-BUTTON-LAYOUT-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** inconsistent button rows and accidental stretching

Use a shared layout container for peer buttons. Let content determine width unless equal-width buttons are a documented layout requirement.

**Derived reasoning:** Windows content guidance distinguishes page layout from control content; using a shared container for peer buttons and content-driven widths applies that principle without asserting a universal equal-width rule.

**Sources:** `MS-WIN-DESIGN-CONTENT`

## 5. States and interaction

### WINUI-BUTTON-STATES-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** incomplete pointer, pressed, focused, or disabled states

Do not replace the template merely to change one visual property. Preserve native normal, pointer-over, pressed, focused, and disabled behavior.

**Sources:** `MS-WIN-CONTROLS-BUTTONS`, `MS-WIN-XAML-THEME-RESOURCES`

### WINUI-BUTTON-KEYBOARD-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** mouse-only command execution

Verify keyboard focus and activation. A successful click test does not prove keyboard support.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`

## 6. Theme, accessibility, and localization

Use the shared foundations for icons, states, accessible naming, text scaling, and localization.

### WINUI-BUTTON-THEME-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** labels or states disappearing in Dark or contrast themes

Prefer theme resources and native styles over fixed foreground/background pairs. Verify Light, Dark, and contrast themes separately when styling is changed.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Using nouns such as “Settings” where the actual action is “Open settings”.
- Putting instructions or error details inside the button.
- Giving every action the accent style.
- Fixing width without testing localized text.
- Replacing `ControlTemplate` to change color or corner radius.
- Omitting `AutomationProperties.Name` on an icon-only button.

## 8. Minimal native XAML

```xml
<StackPanel Orientation="Horizontal" Spacing="8">
    <Button Content="Cancel" />
    <Button Content="Save"
            Style="{StaticResource AccentButtonStyle}" />
</StackPanel>
```

Icon-only command:

```xml
<Button AutomationProperties.Name="Refresh">
    <SymbolIcon Symbol="Refresh" />
</Button>
```

## 9. Verification checklist

- [ ] Label describes the action and remains concise.
- [ ] Only the intended primary action uses accent emphasis.
- [ ] Long Korean and English labels do not clip.
- [ ] Keyboard focus and activation work.
- [ ] Icon-only buttons expose an accessible name.
- [ ] Native pointer, pressed, focused, and disabled states remain intact.
- [ ] Light, Dark, and contrast themes were checked when styling changed.
- [ ] No superficial `ControlTemplate` replacement was introduced.

## 10. Sources

- `MS-WIN-CONTROLS-BUTTONS`
- `MS-WIN-CONTROLS-ICONS`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.