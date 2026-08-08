# Source Note: WinUI 3 Gallery v2.9.3

## Identity

- Source ID: `WINUI-GALLERY-V2-9-3`
- Source kind: `gallery`
- Repository: `microsoft/WinUI-Gallery`
- Tag: `v2.9.3`
- Commit: `14a4a1a2b8ddc527dc4a7d5f7e743d7c2bc97db7`
- Release date: 2025-05-19
- Retrieval date: 2026-08-06
- License: MIT

## Scope inspected

The source-lock pass inspected:

- `LICENSE`
- `Directory.Build.props`
- `standalone.props`
- `WinUIGallery/WinUIGallery.csproj`
- `WinUIGallery/Samples/Button/ButtonPage.xaml`
- `WinUIGallery/Samples/Button/ButtonBuiltInStyles.txt`
- `WinUIGallery/Samples/Button/ButtonSimple.txt`
- `WinUIGallery/Samples/Button/ButtonWithImage.txt`
- `WinUIGallery/Samples/Button/ButtonWrapping.txt`
- `WinUIGallery/Samples/TextBox/TextBoxPage.xaml`
- `WinUIGallery/Samples/TextBox/SimpleTextbox.txt`
- `WinUIGallery/Samples/TextBox/TextboxHeaderPlaceholderText.txt`
- `WinUIGallery/Samples/ToggleSwitch/ToggleSwitchPage.xaml`

The remaining v0.1 sample directories are registered for later component-specific inspection:

- `WinUIGallery/Samples/ComboBox/`
- `WinUIGallery/Samples/CommandBar/`
- `WinUIGallery/Samples/ListView/`
- `WinUIGallery/Samples/InfoBar/`
- `WinUIGallery/Samples/ContentDialog/`

A directory being registered does not mean every file in it has been reviewed.

## Relevant observations

- The tagged standalone build declares `net9.0-windows10.0.22621.0`, Windows App SDK package `2.0.1`, and target Windows SDK `10.0.22621.756`.
- These versions describe the pinned Gallery build environment. They are not LazyDesign minimum requirements for unrelated WinUI 3 projects.
- Button samples include built-in styles, image content, and an explicit wrapping example. This makes the Gallery useful for observing supported native composition and constrained-content behavior.
- TextBox samples distinguish simple input from header and placeholder usage.
- ToggleSwitch samples demonstrate `Header`, `OffContent`, `OnContent`, `IsOn`, and an accessible automation name.
- Gallery samples are executable evidence and examples. A sample choice is not automatically a universal requirement.

## Conflicts or limitations

- The Gallery release is a point-in-time implementation and may differ from later Microsoft Learn guidance or later Windows App SDK behavior.
- The Gallery does not state every small design constraint as a normative rule.
- A successful Gallery build does not prove that generated LazyDesign evaluation pages render correctly.
- Theme, High Contrast, text scaling, keyboard, and assistive-technology claims require separate target-app verification.
- Some sample files carry Microsoft copyright headers even though the repository is MIT licensed. LazyDesign will paraphrase observations and use original minimal examples rather than copying substantial sample code.

## Rules supported

No active rules; source-lock phase.

## Copyright and storage decision

LazyDesign records paths, revisions, environment metadata, and paraphrased observations. It does not vendor the Gallery repository or copy complete sample pages. Any small excerpt used later must be necessary, attributed, and compatible with the repository license.
