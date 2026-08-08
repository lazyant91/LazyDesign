# States and themes

This foundation defines the minimum treatment of native visual states and Windows themes. Component pages specify which states are relevant to each control.

## Preserve native states

### WINUI-STATE-NATIVE-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** a local style or template preserving only the rest state while losing pointer-over, pressed, focused, disabled, selected, checked, validation, or open-state behavior.

Use the native WinUI control template and theme resources unless a documented product requirement cannot be met by supported properties or styles. A customization that changes one state must be reviewed against every state relevant to the control.

**Derived reasoning:** WinUI and Gallery evidence establish native templates and state behavior, while theme resources provide supported customization points; preserving the template unless properties or styles are insufficient is the conservative inference.

**Sources:** `MS-WINUI3-OVERVIEW`, `MS-WIN-XAML-THEME-RESOURCES`, `WINUI-GALLERY-V2-9-3`

### WINUI-STATE-COMPLETE-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** text, icons, borders, or state indicators becoming unreadable because foreground and background changes were considered independently.

When visual-state colors or brushes are customized, verify the complete foreground/background/border/icon combination for that state. Do not change only one side of a readable native pairing without validating the resulting contrast.

**Derived reasoning:** Accessible-text and theme-resource guidance treat foreground, background, borders, and icons as a readable system; validating the whole state pairing follows from that combined evidence.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`, `MS-WIN-XAML-THEME-RESOURCES`

### WINUI-STATE-DISABLED-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** disabled controls looking active or disabled content being used as the sole explanation for why an action is unavailable.

Preserve the native disabled state. When the reason for unavailability is important, provide that explanation in surrounding content or another accessible mechanism rather than encoding the reason only through reduced opacity or color.

**Derived reasoning:** The accessibility checklist and Gallery demonstrate a native disabled state but do not guarantee it explains the reason for unavailability; preserving the state and adding accessible explanation when needed is the resulting inference.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `WINUI-GALLERY-V2-9-3`

## Light and Dark themes

### WINUI-THEME-RESOURCE-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** fixed colors that work in one theme but disappear, clash, or lose contrast in another.

Use named XAML theme resources, system brushes, and inherited control foregrounds before fixed color values. Theme resources resolve at runtime for Light, Dark, and contrast themes.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-THEMING`

### WINUI-THEME-LIGHT-DARK-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** documentation claiming theme support based only on resource names or a successful build.

Render and inspect each modified visual state in both Light and Dark themes before claiming Light/Dark verification. Static XAML review may identify obvious fixed-color risks but does not prove rendered readability.

**Derived reasoning:** The theming sources define separate Light and Dark resource behavior, and accessible-text guidance requires rendered readability; therefore static resource inspection or a build cannot substitute for rendering both themes.

**Sources:** `MS-WIN-THEMING`, `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-ACCESSIBLE-TEXT`

## Contrast themes

### WINUI-THEME-CONTRAST-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** custom styling overriding system-selected contrast colors and making controls unusable for contrast-theme users.

Preserve system-aware contrast behavior and use the documented system color resources when explicit contrast-theme resources are necessary. Do not disable `HighContrastAdjustment` or replace contrast resources without a verified reason and rendered test.

**Sources:** `MS-WIN-CONTRAST-THEMES`, `MS-WIN-XAML-THEME-RESOURCES`

### WINUI-THEME-CONTRAST-002

**Level:** MUST  
**Evidence:** derived  
**Prevents:** High Contrast support being inferred from Light/Dark results.

Treat contrast-theme verification as a separate environment test. Record the Windows contrast theme, control states exercised, and whether system settings were changed or only simulated.

**Derived reasoning:** Contrast-theme guidance defines a distinct Windows environment and accessibility testing requires environment-specific evidence; treating it separately from Light and Dark is the direct operational inference.

**Sources:** `MS-WIN-CONTRAST-THEMES`, `MS-WIN-ACCESSIBILITY-TESTING`

## Accent and meaning

### WINUI-THEME-ACCENT-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** application-local accent colors conflicting with the user's Windows accent preference or losing contrast across themes.

Use system accent and theme resources when the control's native style already supports them. Introduce a fixed brand color only as a product-level decision with theme and contrast verification.

**Sources:** `MS-WIN-THEMING`, `MS-WIN-XAML-THEME-RESOURCES`

### WINUI-STATE-COLOR-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** users missing error, selection, severity, or status information when they cannot distinguish the chosen colors.

Do not rely on color alone to communicate state. Retain text, icon, shape, selection, or another accessible state cue appropriate to the component.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-ACCESSIBLE-TEXT`

## Verification checklist

- [ ] Relevant native states remain present after styling.
- [ ] Foreground, background, border, and icon combinations were reviewed together.
- [ ] Disabled controls remain distinguishable and important reasons are explained accessibly.
- [ ] Theme resources are used before fixed colors.
- [ ] Modified states were rendered in Light and Dark themes.
- [ ] Contrast-theme verification is recorded separately.
- [ ] System accent behavior is preserved unless a product-level exception exists.
- [ ] No state depends on color alone.

## Sources

- `MS-WINUI3-OVERVIEW`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-THEMING`
- `MS-WIN-CONTRAST-THEMES`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-ACCESSIBILITY-TESTING`
- `WINUI-GALLERY-V2-9-3`
