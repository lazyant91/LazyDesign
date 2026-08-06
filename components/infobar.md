# InfoBar

## 1. Purpose and characteristic

Use `InfoBar` for an important status message that should be noticeable without interrupting the user's current flow. It is an inline layout element, not a modal dialog or transient toast.

### WINUI-INFOBAR-PURPOSE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** blocking users with a modal dialog for non-blocking status information

Use `InfoBar` when users must be informed of, acknowledge, or act on a changed application state while continuing to use the current page.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`

### WINUI-INFOBAR-LIFETIME-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** important status messages disappearing before users can understand or act on them

Keep the InfoBar open until the status is resolved or the user dismisses it when dismissal is appropriate. Control visibility with `IsOpen`; do not simulate an InfoBar by briefly showing an unrelated panel.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`

## 2. Anatomy

A native InfoBar can contain a severity indicator, optional icon, title, message, optional action content, and an optional close affordance. It participates in normal page layout and occupies space while open.

### WINUI-INFOBAR-ANATOMY-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** incomplete custom banners that omit severity, dismissal, or native accessibility behavior

Use the native `InfoBar` and its `Title`, `Message`, `Severity`, `ActionButton`, `IsClosable`, `IsIconVisible`, and `IsOpen` properties as applicable before considering custom composition.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`

### WINUI-INFOBAR-SEVERITY-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** decorative or misleading severity styling

Set `Severity` to the actual message meaning: `Informational`, `Success`, `Warning`, or `Error`. Do not change severity only to obtain a preferred color or icon.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`

## 3. Content rules

### WINUI-INFOBAR-CONTENT-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** duplicated or inverted title and message hierarchy

Use `Title` for a concise summary and `Message` for the explanation, consequence, or recovery guidance. Do not repeat the same sentence in both properties.

**Derived reasoning:** InfoBar guidance exposes distinct Title and Message properties, while Windows content guidance separates summary from explanation; assigning those roles without duplication is the inference drawn from both.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`, `MS-WIN-DESIGN-CONTENT`

### WINUI-INFOBAR-CONTENT-002

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** status banners that contain excessive prose and obscure the page

Keep the message focused on the current status and the user's next useful step. Move detailed troubleshooting or documentation to a separate destination.

**Derived reasoning:** InfoBar guidance provides a status surface and Windows content guidance limits competing explanatory detail; focusing the message on status and the next useful step is a conservative content-hierarchy inference.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`, `MS-WIN-DESIGN-CONTENT`

### WINUI-INFOBAR-ACTION-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** multiple competing actions inside one status message

Provide one directly related action through `ActionButton` when the user can resolve or investigate the status immediately. Use a concise action label such as `Retry` or `View details`.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`, `WINUI-GALLERY-V2-9-3`

### WINUI-INFOBAR-DISMISS-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** users dismissing an unresolved blocking condition or being unable to dismiss obsolete information

Set `IsClosable` according to message lifetime. Allow dismissal when the information can safely be ignored or revisited; keep it non-closable only when the status must remain visible until the application resolves it.

**Derived reasoning:** The InfoBar source documents closable behavior but does not prescribe every product lifetime; tying IsClosable to whether the status can safely disappear is an explicit product-context inference from that capability.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`

## 4. Sizing and layout

### WINUI-INFOBAR-LAYOUT-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** overlay banners covering page content or receiving incorrect z-order behavior

Place the InfoBar in the page's normal layout. Let it use available width rather than positioning it as a floating overlay unless a documented product requirement calls for a different control.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`

### WINUI-INFOBAR-LONG-001

**Level:** MUST  
**Evidence:** gallery  
**Prevents:** long localized messages clipping or colliding with actions and the close button

Test short and long Korean and English messages at the narrowest supported width. The pinned Gallery explicitly demonstrates short/long messages and optional button or hyperlink actions, so message length and action composition require deliberate verification.

**Sources:** `WINUI-GALLERY-V2-9-3`

## 5. States and interaction

### WINUI-INFOBAR-OPEN-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** an InfoBar being configured correctly but never displayed

Set and update `IsOpen` from application state. An InfoBar is not visible by default, so verify both opening and closing transitions.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`

### WINUI-INFOBAR-INTERACTION-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** mouse-only retry or dismissal behavior

Verify keyboard focus and activation for the action and close affordances. Preserve native focus visuals and do not replace the control template to change a single state color.

**Derived reasoning:** Keyboard guidance requires operable focus paths, InfoBar supplies native action and close affordances, and theme resources preserve state visuals; verifying those native affordances follows from the combined evidence.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`, `MS-WIN-CONTROLS-INFOBAR`, `MS-WIN-XAML-THEME-RESOURCES`

## 6. Theme, accessibility, and localization

### WINUI-INFOBAR-ACCESSIBILITY-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** severity being communicated only by icon or color

Write title and message text that communicates the condition without relying on severity color or icon alone. Ensure an icon-only custom action, when unavoidable, exposes an accessible name.

**Derived reasoning:** InfoBar severity is visually represented while the accessibility and icon sources warn against color-only or unnamed meaning; communicating the condition in text and naming icon-only actions is the resulting inference.

**Sources:** `MS-WIN-CONTROLS-INFOBAR`, `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-CONTROLS-ICONS`

### WINUI-INFOBAR-THEME-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** status text, icon, action, or close affordance disappearing in Dark or contrast themes

Retain native severity and theme resources. Verify Light, Dark, and contrast themes separately when any foreground, background, or icon styling is changed.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Using InfoBar for a decision that must block progress.
- Repeating the same text in `Title` and `Message`.
- Selecting `Error` only to obtain a red visual treatment.
- Adding several unrelated buttons to one InfoBar.
- Making a persistent unresolved error freely dismissible without another visible status location.
- Fixing the height so a long Korean message clips.
- Communicating severity only through color or icon.
- Replacing the native template for superficial styling.

## 8. Minimal native XAML

```xml
<InfoBar x:Name="ConnectionErrorInfoBar"
         Title="Connection failed"
         Message="Check that the device is powered on and try again."
         Severity="Error"
         IsOpen="True"
         IsClosable="True">
    <InfoBar.ActionButton>
        <Button Content="Retry"
                Click="RetryConnection_Click" />
    </InfoBar.ActionButton>
</InfoBar>
```

No local `ControlTemplate` is required.

## 9. Verification checklist

- [ ] The message is important but does not require a modal decision.
- [ ] `Title` summarizes and `Message` explains without duplication.
- [ ] `Severity` matches meaning rather than decorative preference.
- [ ] At most one directly related action is present.
- [ ] `IsClosable` matches the status lifetime.
- [ ] `IsOpen` transitions were verified.
- [ ] Long Korean and English messages remain readable at constrained width.
- [ ] Action and close affordances work with keyboard input and show focus.
- [ ] Severity remains understandable without color or icon alone.
- [ ] Light, Dark, and contrast themes were checked when styling changed.
- [ ] No superficial `ControlTemplate` replacement was introduced.

## 10. Sources

- `MS-WIN-CONTROLS-INFOBAR`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-CONTROLS-ICONS`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.
