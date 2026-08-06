# CommandBar

## 1. Purpose and characteristic

Use `CommandBar` to expose frequent app-level or page-level commands while moving lower-priority commands into overflow.

### WINUI-COMMANDBAR-PURPOSE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** command bars becoming arbitrary content containers

Use a command bar for commands and closely related contextual content. Do not use it as a general page-layout container.

**Sources:** `MS-WIN-CONTROLS-COMMANDBAR`

## 2. Anatomy

A command bar can contain primary commands, secondary commands in overflow, optional content, and the ellipsis affordance. Native command elements include `AppBarButton`, `AppBarToggleButton`, and `AppBarSeparator`.

### WINUI-COMMANDBAR-ANATOMY-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** unsupported custom command elements and broken overflow behavior

Use native app-bar command controls for commands unless a documented requirement needs custom content.

**Sources:** `MS-WIN-CONTROLS-COMMANDBAR`

## 3. Content rules

### WINUI-COMMANDBAR-CONTENT-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** important commands becoming hidden unpredictably

Place the most frequent and important commands in `PrimaryCommands`; place less frequent commands in `SecondaryCommands`.

**Sources:** `MS-WIN-CONTROLS-COMMANDBAR`

### WINUI-COMMANDBAR-CONTENT-002

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** icon-only command bars that are difficult to learn

Use recognizable icons and concise labels. Preserve labels in overflow and provide accessible names for icon-only compact presentation.

**Derived reasoning:** CommandBar guidance defines compact and overflow presentations and the icon guidance does not make every symbol self-evident; combining labels, recognizable icons, and accessible names is therefore a conservative inference.

**Sources:** `MS-WIN-CONTROLS-COMMANDBAR`, `MS-WIN-CONTROLS-ICONS`

## 4. Sizing and layout

### WINUI-COMMANDBAR-SIZE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** commands clipping instead of entering overflow

Allow the native overflow mechanism to respond to available width. Do not force a fixed bar width that defeats adaptive command placement.

**Sources:** `MS-WIN-CONTROLS-COMMANDBAR`

## 5. States and interaction

### WINUI-COMMANDBAR-STATE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** toggle commands losing their state semantics

Use `AppBarToggleButton` for commands with persistent on/off state and keep its checked state synchronized with application state.

**Sources:** `MS-WIN-CONTROLS-COMMANDBAR`

### WINUI-COMMANDBAR-KEYBOARD-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** inaccessible command and overflow navigation

Verify keyboard focus order, command activation, overflow opening, navigation, dismissal, and focus return.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`

## 6. Theme, accessibility, and localization

### WINUI-COMMANDBAR-A11Y-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** icon commands announced without purpose

Every command must expose a meaningful accessible name, role, and state. Do not rely on icon shape or color alone.

**Sources:** `MS-WIN-CONTROLS-ICONS`, `MS-WIN-ACCESSIBILITY-CHECKLIST`

### WINUI-COMMANDBAR-LOCALIZATION-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** localized labels clipping or changing overflow priority unexpectedly

Test long Korean and English command labels in both primary and overflow presentations at constrained widths.

**Derived reasoning:** The CommandBar source defines primary and overflow layouts, and accessible-text guidance requires localized scaled text to remain readable; testing long labels in both presentations follows from those two sources.

**Sources:** `MS-WIN-CONTROLS-COMMANDBAR`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-COMMANDBAR-THEME-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** icons, labels, focus, or checked state disappearing across themes

Preserve native theme resources and verify closed, open, overflow, disabled, and checked states in Light, Dark, and contrast themes after styling changes.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Putting every command in `PrimaryCommands`.
- Using unfamiliar icons without labels or accessible names.
- Using `AppBarButton` for persistent toggle state.
- Fixed width that clips commands instead of permitting overflow.
- Testing only the closed bar and not overflow.
- Replacing templates to restyle individual commands superficially.

## 8. Minimal native XAML

```xml
<CommandBar DefaultLabelPosition="Right">
    <AppBarButton Icon="Add"
                  Label="Add device"
                  Command="{x:Bind ViewModel.AddDeviceCommand}" />
    <AppBarButton Icon="Refresh"
                  Label="Refresh"
                  Command="{x:Bind ViewModel.RefreshCommand}" />
    <CommandBar.SecondaryCommands>
        <AppBarButton Icon="Setting"
                      Label="Settings"
                      Command="{x:Bind ViewModel.OpenSettingsCommand}" />
    </CommandBar.SecondaryCommands>
</CommandBar>
```

## 9. Verification checklist

- [ ] Primary commands are frequent and important.
- [ ] Secondary commands appear correctly in overflow.
- [ ] Icons, labels, accessible names, roles, and states are present.
- [ ] Toggle commands use `AppBarToggleButton`.
- [ ] Compact, open, and overflow states were inspected.
- [ ] Constrained widths and long Korean/English labels were checked.
- [ ] Keyboard navigation, dismissal, and focus return work.
- [ ] Light, Dark, and contrast themes were checked after styling changes.
- [ ] No superficial template replacement was introduced.

## 10. Sources

- `MS-WIN-CONTROLS-COMMANDBAR`
- `MS-WIN-CONTROLS-ICONS`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.