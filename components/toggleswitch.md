# ToggleSwitch

## 1. Purpose and characteristic

Use `ToggleSwitch` for two mutually exclusive states whose change takes effect immediately.

### WINUI-TOGGLE-PURPOSE-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** using a switch for deferred confirmation or multi-option choice

Use a toggle only for an on/off choice with immediate results. Use another control when the user must confirm the change later or choose among more than two options.

**Sources:** `MS-WIN-CONTROLS-TOGGLES`

## 2. Anatomy

A toggle can include a persistent `Header`, the switch track/thumb, and optional `OnContent` and `OffContent` that describe the current state.

### WINUI-TOGGLE-ANATOMY-001
**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** switches whose subject or current state is unclear

Provide a concise header when surrounding context does not clearly identify what is being controlled. Use state content only when “On” and “Off” are not sufficiently descriptive.

**Sources:** `MS-WIN-CONTROLS-TOGGLES`, `WINUI-GALLERY-V2-9-3`

## 3. Content rules

### WINUI-TOGGLE-CONTENT-001
**Level:** MUST  
**Evidence:** derived  
**Prevents:** labels describing actions instead of states

Label the setting or state, not the gesture. Prefer “Bluetooth” with state text such as “On/Off” over “Turn Bluetooth on”.

**Derived reasoning:** The ToggleSwitch source describes a setting and its on/off state; wording the header as the setting rather than as the gesture is inferred from that state model, not quoted as a universal Microsoft wording rule.

**Sources:** `MS-WIN-CONTROLS-TOGGLES`

### WINUI-TOGGLE-CONTENT-002
**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** long state text destabilizing layout

Keep `OnContent` and `OffContent` short and semantically parallel. Put explanatory detail outside the control.

**Derived reasoning:** The ToggleSwitch source supplies separate on/off content and Windows content guidance favors concise control text; keeping the two state labels short and parallel combines those sources into a conservative rule.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `MS-WIN-CONTROLS-TOGGLES`

## 4. Sizing and layout

### WINUI-TOGGLE-SIZE-001
**Level:** MUST  
**Evidence:** derived  
**Prevents:** long localized header or state text clipping

Avoid fixed width unless the longest supported header and both state labels have been tested in Korean, English, and text scaling.

**Derived reasoning:** ToggleSwitch exposes a header and state labels, and accessible-text guidance requires scaled text to remain readable; verifying all three strings before fixing width follows from those combined facts.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`, `MS-WIN-CONTROLS-TOGGLES`

### WINUI-TOGGLE-LAYOUT-001
**Level:** SHOULD  
**Evidence:** gallery  
**Prevents:** state-dependent layout jumps and poor alignment

Align switches consistently in settings groups and reserve sufficient space for both states. Gallery demonstrates a toggle paired with dependent progress feedback without replacing the native control.

**Sources:** `WINUI-GALLERY-V2-9-3`

## 5. States and interaction

### WINUI-TOGGLE-STATE-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** a switch changing visually without applying the setting

Keep the visual `IsOn` state synchronized with the actual setting. If an asynchronous operation can fail, expose progress and restore or explain the resulting state.

**Sources:** `MS-WIN-CONTROLS-TOGGLES`, `WINUI-GALLERY-V2-9-3`

### WINUI-TOGGLE-KEYBOARD-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** mouse-only setting changes

Verify focus visibility and keyboard activation, not only pointer interaction.

**Sources:** `MS-WIN-KEYBOARD-INTERACTIONS`

## 6. Theme, accessibility, and localization

### WINUI-TOGGLE-A11Y-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** assistive technology announcing a state without its subject

Ensure the accessible name identifies the setting and the control exposes its on/off state. Do not rely on color alone.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-CONTROLS-TOGGLES`

### WINUI-TOGGLE-THEME-001
**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** track, thumb, focus, or disabled state disappearing in alternate themes

Preserve native theme resources and verify Light, Dark, and contrast themes after styling changes.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`

## 7. Common failures

- Using a toggle for a change that requires an Apply button.
- Using it for three or more choices.
- Labeling the gesture rather than the setting.
- Long `OnContent` and `OffContent` strings with different structures.
- Updating `IsOn` without applying or persisting the actual setting.
- Replacing the native template to recolor the track.

## 8. Minimal native XAML

```xml
<ToggleSwitch Header="Bluetooth"
              OffContent="Off"
              OnContent="On"
              IsOn="{x:Bind ViewModel.IsBluetoothEnabled, Mode=TwoWay}" />
```

## 9. Verification checklist

- [ ] The setting is binary and takes effect immediately.
- [ ] Header identifies the setting.
- [ ] State labels are short and parallel.
- [ ] Long Korean and English strings and text scaling were checked.
- [ ] `IsOn` remains synchronized with the actual setting.
- [ ] Keyboard focus and activation work.
- [ ] Accessible name and state are exposed.
- [ ] Light, Dark, and contrast themes were checked after styling changes.

## 10. Sources

- `MS-WIN-CONTROLS-TOGGLES`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-KEYBOARD-INTERACTIONS`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `WINUI-GALLERY-V2-9-3`

Windows Design Kit evidence remains inactive because component-level inspection has not been completed.