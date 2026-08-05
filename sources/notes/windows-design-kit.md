# Source Note: Microsoft Windows Design Kit for Figma

## Identity

- Source ID: `MS-WINDOWS-DESIGN-KIT-FIGMA`
- Source kind: `ui-kit`
- Official entry point: `https://learn.microsoft.com/windows/apps/design/downloads/`
- Community file: `https://www.figma.com/community/file/1440832812269040007`
- Stable community-file ID: `1440832812269040007`
- Retrieval date: 2026-08-06
- Connected Figma account seat: View
- Current inspection status: identity verified; semantic component inspection pending

## Scope inspected

The source-lock pass verified the official Microsoft Learn entry point and the stable Figma Community file identity. It did not yet claim that component sets, variants, variables, or internal anatomy were inspected.

The v0.1 component-authoring pass must inspect only these eight component families when available in the kit:

- Button
- TextBox
- ToggleSwitch
- ComboBox
- CommandBar or the corresponding command components
- ListView or the corresponding list-item patterns
- InfoBar
- ContentDialog or dialog patterns

For each family, the author must record the exact Figma page, component-set name, variant properties, inspected states, and any absence or naming mismatch.

## Relevant observations

- Microsoft presents the Windows Design Kit as a Windows design resource containing components, patterns, styles, and tokens.
- The kit is visual composition evidence. It can support anatomy, variant, state, icon-placement, and spacing observations for the inspected revision.
- A Figma component or frame does not define WinUI runtime behavior, keyboard interaction, automation semantics, adaptive layout, or implementation API requirements.

## Conflicts or limitations

- The Community file does not expose a semantic version in the source information currently recorded by LazyDesign. The pinned revision is therefore the stable file ID plus retrieval date until a visible kit version is confirmed.
- A View seat is sufficient for reading when the file and connector permit it, but it may limit duplication, library publishing, or some metadata workflows.
- UI-kit evidence remains inactive until the relevant component set is actually inspected and recorded.
- If connector access fails, the component page may proceed from Microsoft Learn and Gallery evidence but must mark UI-kit verification as incomplete. It cannot be called precision-complete.
- The kit must not be exported, mirrored, screenshotted into the repository, or redistributed without a verified right to do so.

## Rules supported

No active rules; source-lock phase.

## Copyright and storage decision

LazyDesign stores the official URL, stable file identifier, retrieval date, component-set names, and paraphrased observations. It does not store Figma assets, exported libraries, screenshots, fonts, or authentication data.
