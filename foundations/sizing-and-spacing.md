# Sizing and spacing

This foundation defines cross-component sizing defaults. It does not replace component-specific minimums, popup sizing, item templates, or adaptive layout rules.

## Native sizing first

### WINUI-SIZE-NATIVE-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** arbitrary local dimensions overriding WinUI's native desired size, padding, typography, and interaction-state layout.

Begin with the native WinUI control and its default style. Add `Width`, `Height`, `MinWidth`, `MaxWidth`, or local padding only when the surrounding layout or product requirement provides a concrete reason.

**Derived reasoning:** WinUI documentation and Gallery samples establish native controls and default styles as the supported baseline; requiring a concrete reason before overriding dimensions or padding is a conservative maintenance inference.

**Sources:** `MS-WINUI3-OVERVIEW`, `WINUI-GALLERY-V2-9-3`

### WINUI-SIZE-FIXED-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** localized or scaled text being clipped by a dimension chosen from one design-time string.

Do not use a fixed dimension merely to reproduce the bounds of one Figma frame. When a bounded dimension is required, verify the longest supported content, text scaling, and the minimum supported window width.

**Derived reasoning:** Windows content and accessible-text guidance require localized scaled content to remain usable, while the UI kit represents one inspected visual frame; rejecting dimensions copied solely from that frame follows from those evidence limits.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `MS-WIN-ACCESSIBLE-TEXT`, `MS-WINDOWS-DESIGN-KIT-FIGMA`

## Internal and external spacing

### WINUI-SPACING-BOUNDARY-001

**Level:** MUST  
**Evidence:** derived  
**Prevents:** page-layout spacing being implemented by replacing a control's internal padding or template.

Treat control-internal padding and page-layout spacing as separate responsibilities. Use layout containers, row/column gaps, or margins between siblings for page composition. Preserve native internal padding unless the component page documents a supported customization.

**Derived reasoning:** Windows content guidance defines page composition and Gallery controls retain native internal spacing; separating sibling layout spacing from template padding is the inference that preserves both responsibilities.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `WINUI-GALLERY-V2-9-3`

### WINUI-SPACING-GROUP-001

**Level:** SHOULD  
**Evidence:** official-doc  
**Prevents:** inconsistent gaps obscuring which controls and content belong together.

Use consistent Windows spacing patterns to group related controls and separate distinct content regions. Prefer a small, repeated spacing vocabulary over unrelated local margin values.

**Sources:** `MS-WIN-DESIGN-CONTENT`

### WINUI-SPACING-VALUE-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** one example value from being elevated into a universal rule for all controls and contexts.

Use numeric spacing examples only within the context stated by the source. Do not infer a universal page grid or control padding from one screenshot, one Gallery sample, or one UI-kit frame.

**Derived reasoning:** The cited sources provide context-specific examples rather than a universal numeric system; limiting each spacing value to its documented context is therefore an evidence-bound inference.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `MS-WINDOWS-DESIGN-KIT-FIGMA`, `WINUI-GALLERY-V2-9-3`

## Width behavior

### WINUI-SIZE-WIDTH-001

**Level:** SHOULD  
**Evidence:** derived  
**Prevents:** intrinsic command controls expanding across an entire row without a product or layout reason.

Allow controls whose content naturally determines their width to use native desired size unless the component or surrounding layout is explicitly designed to fill, share, or constrain available space.

**Derived reasoning:** Windows content guidance and Gallery examples distinguish intrinsic command sizing from filling layout regions; allowing native desired width unless the surrounding layout says otherwise is the conservative synthesis.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `WINUI-GALLERY-V2-9-3`

### WINUI-SIZE-WIDTH-002

**Level:** MUST  
**Evidence:** derived  
**Prevents:** a flexible input or collection being given an unbounded or unusably narrow width.

When a control is expected to grow with its layout region, define the containing grid or panel behavior and verify both the minimum supported width and the expanded state. Do not rely on implicit `Stretch` without understanding the parent layout.

**Derived reasoning:** Windows content and accessible-text guidance require layouts to remain usable at minimum and expanded widths; defining parent layout behavior rather than relying blindly on Stretch is the resulting implementation inference.

**Sources:** `MS-WIN-DESIGN-CONTENT`, `MS-WIN-ACCESSIBLE-TEXT`

## Verification checklist

- [ ] Native control size and style were evaluated before local dimensions were added.
- [ ] Every fixed width or height has a documented content or layout reason.
- [ ] Long localized content and text scaling were tested for bounded controls.
- [ ] Page spacing is implemented outside the control template.
- [ ] Repeated gaps use a consistent vocabulary.
- [ ] Minimum and expanded window widths were reviewed.
- [ ] No Figma frame measurement is presented as a universal runtime requirement.

## Sources

- `MS-WINUI3-OVERVIEW`
- `MS-WIN-DESIGN-CONTENT`
- `MS-WIN-ACCESSIBLE-TEXT`
- `MS-WINDOWS-DESIGN-KIT-FIGMA`
- `WINUI-GALLERY-V2-9-3`
