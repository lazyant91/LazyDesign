# Icons

This foundation covers shared icon behavior. Component pages define whether an icon is required, optional, hidden in overflow, or paired with a visible label.

## Native icon sources

### WINUI-ICON-SOURCE-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** manually drawn or font-substituted approximations that render inconsistently across scale, theme, and state.

Use a WinUI icon element or icon source supported by the target property, such as `SymbolIcon`, `FontIcon`, `PathIcon`, `BitmapIcon`, or the corresponding `IconSource`. Prefer a platform-provided symbol when it clearly represents the intended action.

**Sources:** `MS-WIN-CONTROLS-ICONS`

### WINUI-ICON-SOURCE-002

**Level:** MUST  
**Evidence:** derived  
**Prevents:** an icon example silently depending on a private font, copied asset, or unavailable glyph.

Document the icon source used by reusable XAML. Do not commit font files or copied Windows Design Kit assets. If a custom asset is required by a product, keep that decision outside the generic LazyDesign rule.

**Sources:** `MS-WIN-CONTROLS-ICONS`, `MS-WINDOWS-DESIGN-KIT-FIGMA`

## Meaning and labels

### WINUI-ICON-MEANING-001

**Level:** MUST  
**Evidence:** official-doc  
**Prevents:** icon-only interactive controls being unnamed or announced as an implementation detail.

Provide an accessible name for an icon-only interactive control. The name must describe the action or state, not the glyph shape or Unicode value.

**Sources:** `MS-WIN-ACCESSIBILITY-CHECKLIST`, `MS-WIN-CONTROLS-ICONS`

### WINUI-ICON-MEANING-002

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** unfamiliar icons being treated as self-explanatory and forcing users to guess an action.

Pair an icon with a visible text label when the icon is not broadly recognizable in the target context or when the component normally exposes labels. Do not remove a required label only to save space without verifying the component's overflow or compact behavior.

**Sources:** `MS-WIN-CONTROLS-ICONS`, `MS-WIN-CONTROLS-COMMANDBAR`, `MS-WIN-DESIGN-CONTENT`

### WINUI-ICON-DECORATIVE-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** decorative icons being announced redundantly or semantic icons being hidden from assistive technologies.

Classify each icon as semantic or decorative. A semantic icon must have an accessible equivalent through the control name or surrounding content. A decorative icon must not create a duplicate or misleading announcement.

**Sources:** `MS-WIN-ACCESSIBLE-TEXT`, `MS-WIN-ACCESSIBILITY-CHECKLIST`

## Alignment and state

### WINUI-ICON-LAYOUT-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** mixed icon sizes and baselines making related commands appear visually unstable.

Use one deliberate icon size and alignment convention within a component or command group. Let the native control style position the icon when it provides an icon property or standard content structure.

**Sources:** `MS-WIN-CONTROLS-ICONS`, `WINUI-GALLERY-V2-9-3`

### WINUI-ICON-THEME-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** icons disappearing or losing meaning in Dark or contrast themes because of a fixed foreground or baked-in color.

Use inherited foreground or theme resources for monochrome icons unless color is essential to the meaning and verified in all supported themes. Do not rely on color alone to communicate state.

**Sources:** `MS-WIN-XAML-THEME-RESOURCES`, `MS-WIN-CONTRAST-THEMES`, `MS-WIN-ACCESSIBILITY-CHECKLIST`

## Verification checklist

- [ ] The icon uses a documented WinUI icon type or a product-owned asset.
- [ ] Icon-only interactive controls have action-oriented accessible names.
- [ ] Unfamiliar icons retain a visible label or other clear explanation.
- [ ] Decorative and semantic icons are distinguished.
- [ ] Related icons use consistent size and alignment.
- [ ] Icon foreground remains visible in Light, Dark, and contrast themes.
- [ ] State is not communicated by icon color alone.

## Sources

- `MS-WIN-CONTROLS-ICONS`
- `MS-WIN-CONTROLS-COMMANDBAR`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WIN-ACCESSIBILITY-CHECKLIST`
- `MS-WIN-XAML-THEME-RESOURCES`
- `MS-WIN-CONTRAST-THEMES`
- `MS-WINDOWS-DESIGN-KIT-FIGMA`
- `WINUI-GALLERY-V2-9-3`
