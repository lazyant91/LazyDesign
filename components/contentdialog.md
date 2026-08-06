# ContentDialog

## 1. Purpose and characteristic

Use `ContentDialog` for a modal decision or critical information that requires the user to respond before returning to the current window.

### WINUI-CONTENTDIALOG-PURPOSE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** blocking routine status information behind unnecessary modal UI

Use a ContentDialog only when the current task must pause for a decision, confirmation, or critical acknowledgment. Use an inline control such as InfoBar for non-blocking status messages.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `MS-WIN-CONTROLS-INFOBAR`

### WINUI-CONTENTDIALOG-SINGLE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** runtime exceptions caused by overlapping modal dialogs

Ensure only one ContentDialog is open per window. Queue or suppress additional dialog requests rather than calling `ShowAsync` for a second dialog concurrently.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`

## 2. Anatomy

A native ContentDialog contains a title, content region, and built-in command area with a required safe close action plus optional primary and secondary actions.

### WINUI-CONTENTDIALOG-ANATOMY-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** custom modal panels that lose native layout, keyboard, and command behavior

Use `Title`, `Content`, `PrimaryButtonText`, `SecondaryButtonText`, and `CloseButtonText` as applicable. Prefer the built-in command area over manually placing peer buttons inside the content region.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`

### WINUI-CONTENTDIALOG-CLOSE-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** a dialog without a safe, nondestructive exit

Provide a safe close action through `CloseButtonText`. The close action must let users leave the dialog without performing the destructive or committing operation.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`

## 3. Content rules

### WINUI-CONTENTDIALOG-CONTENT-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** vague confirmation dialogs that do not identify the affected object or consequence

Use a concise title that states the decision and content that identifies the affected object, consequence, and any essential recovery information.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `MS-WIN-DESIGN-CONTENT`

### WINUI-CONTENTDIALOG-ACTION-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** ambiguous or misordered dialog commands

Use `PrimaryButtonText` for the first committing action, `SecondaryButtonText` only for a second distinct committing action, and `CloseButtonText` for the safe exit. Keep each label concise and action-oriented.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`

### WINUI-CONTENTDIALOG-DESTRUCTIVE-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** accidental destructive actions caused by generic labels or hidden consequences

For destructive confirmation, name the action explicitly, identify the selected item in the content, and use a safe close label such as `Cancel`. Do not rely on button color alone to communicate risk.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `MS-WIN-ACCESSIBILITY-CHECKLIST`

### WINUI-CONTENTDIALOG-DENSITY-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** replacing an entire page or complex workflow with a cramped modal form

Keep dialog content focused on one decision. Move dense forms, multi-step workflows, and large information structures to a page or dedicated surface.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `MS-WIN-DESIGN-CONTENT`

## 4. Sizing and layout

### WINUI-CONTENTDIALOG-LONG-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** long localized content pushing commands off-screen or clipping

Test the longest supported Korean and English title, body, and action labels. When the content must be long, place the body in an appropriate scrolling container while keeping the built-in command area intact.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `MS-WIN-ACCESSIBLE-TEXT`

### WINUI-CONTENTDIALOG-BUTTONS-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** command buttons becoming hidden by the on-screen keyboard or laid out inconsistently

Use the built-in ContentDialog buttons instead of manually positioning the primary, secondary, and close actions. The native command area provides the expected placement and input behavior.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`

## 5. States and interaction

### WINUI-CONTENTDIALOG-XAMLROOT-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** a WinUI 3 runtime exception when displaying the dialog

Set `XamlRoot` to the current visual root before calling `ShowAsync` in WinUI 3.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`

### WINUI-CONTENTDIALOG-DEFAULT-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** Enter invoking an unintended action or no action at all

Set `DefaultButton` only after deciding which action should receive default keyboard activation. For destructive decisions, do not make the destructive action the default without a documented product requirement and explicit review.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `WINUI-GALLERY-V2-9-3`

### WINUI-CONTENTDIALOG-KEYBOARD-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** mouse-only dialog completion or lost focus

Verify initial focus, Tab navigation, Enter behavior, and the safe close path. Preserve the native command buttons and focus visuals.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `MS-WIN-KEYBOARD-INTERACTIONS`

## 6. Theme, accessibility, and localization

### WINUI-CONTENTDIALOG-ACCESSIBILITY-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** screen-reader users encountering an unnamed modal or unclear action consequences

Provide a meaningful title, readable content, and explicit button labels. Verify that focus enters the dialog when it opens and returns to a sensible control when it closes.

**Sources:** `MS-WIN-CONTROLS-DIALOGS`, `MS-WIN-ACCESSIBILITY-CHECKLIST`

### WINUI-CONTENTDIALOG-THEME-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** dialog content or command states disappearing in Dark or contrast themes

Use native styles and theme resources. Verify Light, Dark, and contrast themes separately when dialog content or button styling is customized.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Using a ContentDialog for routine success or background status information.
- Opening a second ContentDialog while one is already open.
- Forgetting to set `XamlRoot` before `ShowAsync` in WinUI 3.
- Omitting a safe close action.
- Using generic labels such as `Yes` and `No` when action names are clearer.
- Placing custom command buttons inside the content instead of using built-in button properties.
- Making a destructive action the default without review.
- Putting a full settings page or multi-step workflow inside the dialog.
- Fixing dialog content height so localized text clips.
- Replacing the native template for superficial styling.

## 8. Minimal native XAML

```xml
<ContentDialog x:Name="RemoveDeviceDialog"
               Title="Remove saved device?"
               PrimaryButtonText="Remove"
               CloseButtonText="Cancel"
               DefaultButton="Close">
    <TextBlock Text="The saved device 'Conference room display' will be removed."
               TextWrapping="Wrap" />
</ContentDialog>
```

Display it from code after assigning the current root:

```csharp
RemoveDeviceDialog.XamlRoot = Content.XamlRoot;
ContentDialogResult result = await RemoveDeviceDialog.ShowAsync();
```

No local `ControlTemplate` or manually composed command row is required.

## 9. Verification checklist

- [ ] The interaction truly requires a modal decision or acknowledgment.
- [ ] Only one ContentDialog can be open in the window.
- [ ] Title and content identify the decision, affected object, and consequence.
- [ ] A safe `CloseButtonText` action is present.
- [ ] Primary and secondary labels name their actions explicitly.
- [ ] `XamlRoot` is set before `ShowAsync`.
- [ ] `DefaultButton` matches the intended keyboard behavior.
- [ ] Tab, Enter, and safe close behavior were tested.
- [ ] Long Korean and English content remains readable and the command area stays visible.
- [ ] Focus enters and leaves the dialog sensibly.
- [ ] Light, Dark, and contrast themes were checked when styling changed.
- [ ] No dense page-sized workflow or superficial `ControlTemplate` replacement was introduced.

## 10. Sources

- `MS-WIN-CONTROLS-DIALOGS`
- `MS-WIN-CONTROLS-INFOBAR`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.
