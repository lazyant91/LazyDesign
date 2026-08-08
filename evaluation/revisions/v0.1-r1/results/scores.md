# LazyDesign v0.1 Scores

## Scenario totals

| Scenario | Baseline | Guided | Delta |
|---|---:|---:|---:|
| Connection settings | 11 / 20 | 19 / 20 | +8 |
| Device list | 2 / 20 | 15 / 20 | +13 |
| Failure and confirmation | 2 / 20 | 2 / 20 | +0 |
| **Total** | **15 / 60** | **36 / 60** | **+21** |

## Connection settings

| # | Category | Baseline | Guided | Baseline evidence | Guided evidence | Baseline uncertainty | Guided uncertainty |
|---:|---|---:|---:|---|---|---|---|
| 1 | Content length and overflow | 1 | 2 | baseline/connection-settings/evidence/static-review.txt:6-9<br>baseline/connection-settings/evidence/runtime-uia.txt:1-3 | guided/connection-settings/evidence/runtime-uia.txt:3-12 | The source wraps growing text and avoids horizontal scrolling, but the runtime crashed before 420-DIP content fit could be observed. | The required controls and growing text were directly bounded inside the measured 420-DIP client width; text scaling above 100 percent was not exercised. |
| 2 | Information hierarchy | 1 | 2 | baseline/connection-settings/generated/MainWindow.xaml:9-30 | guided/connection-settings/generated/MainWindow.xaml:10-45 | Basic grouping exists, but hierarchy relies on local FontSize, FontWeight, and Opacity treatment and repeats the automatic-reconnect concept in a separate heading. | none |
| 3 | Component anatomy | 1 | 2 | baseline/connection-settings/generated/MainWindow.xaml:13-30 | guided/connection-settings/generated/MainWindow.xaml:15-45 | Native controls are present, but TextBox and ComboBox use adjacent TextBlocks rather than native associated headers. | none |
| 4 | Native interaction states | 1 | 2 | baseline/connection-settings/evidence/static-review.txt:6-10<br>baseline/connection-settings/evidence/runtime-uia.txt:1-3 | guided/connection-settings/evidence/runtime-uia.txt:15-20 | Native controls and state handlers are present statically, but the executable crashed before keyboard, popup, toggle, validation, or save states could be exercised. | ComboBox open/selection, ToggleSwitch state, keyboard traversal, validation, and Save activation were exercised; focus visuals were not separately inspected. |
| 5 | Accessibility basics | 0 | 1 | baseline/connection-settings/generated/MainWindow.xaml:13-31 | guided/connection-settings/evidence/runtime-uia.txt:4-18<br>guided/connection-settings/generated/MainWindow.xaml:15-45 | The TextBox and ComboBox lack an associated native label or explicit AutomationProperties.Name, so important interactive naming/association is missing even before runtime verification. | Meaningful UIA names and keyboard operation were observed, but focus-visual, Narrator, and Accessibility Insights verification were not performed. |
| 6 | Localization and scaling resilience | 1 | 2 | baseline/connection-settings/evidence/static-review.txt:7-9<br>baseline/connection-settings/evidence/runtime-uia.txt:1-3 | guided/connection-settings/evidence/runtime-uia.txt:3-12 | Required Korean strings are present with wrapping-oriented structure, but the 420-DIP runtime and text scaling could not be verified because launch failed. | The required 420-DIP constrained-width behavior was measured directly; text scaling above 100 percent was not exercised. |
| 7 | Native WinUI style preservation | 1 | 2 | baseline/connection-settings/generated/MainWindow.xaml:9-31 | guided/connection-settings/generated/MainWindow.xaml:12-45<br>guided/connection-settings/evidence/static-review.txt:6-13 | Native controls and a ThemeResource critical brush are used, but local font-size/weight/opacity styling duplicates semantic styling that built-in styles could provide. | Native controls and built-in semantic/accent styles are used with no local ControlTemplate or fixed-color replacement; Light and High Contrast were not run. |
| 8 | Component-specific characteristics | 1 | 2 | baseline/connection-settings/evidence/static-review.txt:6-8<br>baseline/connection-settings/evidence/runtime-uia.txt:1-3 | guided/connection-settings/evidence/runtime-uia.txt:15-18 | The intended TextBox, ComboBox, ToggleSwitch, and Button characteristics are represented statically, but scenario-specific runtime behavior was not observable. | none |
| 9 | Label, helper, and explanation separation | 2 | 2 | baseline/connection-settings/generated/MainWindow.xaml:13-31 | guided/connection-settings/generated/MainWindow.xaml:15-45 | Labels, helper text, validation text, values, and the save action are structurally distinct despite the missing native associations. | none |
| 10 | XAML simplicity and relevance | 2 | 2 | baseline/connection-settings/generated/MainWindow.xaml:1-35<br>baseline/connection-settings/generated/MainWindow.xaml.cs:1-30 | guided/connection-settings/generated/MainWindow.xaml:1-49<br>guided/connection-settings/generated/MainWindow.xaml.cs:1-44 | The implementation is compact and contains only scenario-related XAML and minimal validation/save code. | The output stays within the requested native controls and uses only small event handlers needed for validation and state tracking. |

## Device list

| # | Category | Baseline | Guided | Baseline evidence | Guided evidence | Baseline uncertainty | Guided uncertainty |
|---:|---|---:|---:|---|---|---|---|
| 1 | Content length and overflow | 0 | 1 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/generated/MainWindow.xaml:43-111<br>guided/device-list/evidence/runtime-crash.txt:5-12 | Generation produced no device-list implementation or required long fixtures. | Long names use wrapping-oriented layout, but the executable crashed before the required 520-DIP content fit could be rendered. |
| 2 | Information hierarchy | 0 | 2 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/generated/MainWindow.xaml:15-40<br>guided/device-list/generated/MainWindow.xaml:63-111 | No scenario information hierarchy was generated. | none |
| 3 | Component anatomy | 0 | 2 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/evidence/static-review.txt:5-12 | Required CommandBar, ListView, and empty-state anatomy are absent. | The required native anatomy is explicit statically; runtime rendering later failed before the screen appeared. |
| 4 | Native interaction states | 0 | 1 | baseline/device-list/evidence/generation-failure.txt:13-22<br>baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/evidence/static-review.txt:6-10<br>guided/device-list/evidence/runtime-crash.txt:5-12 | No selection, command, overflow, keyboard, or disabled-state implementation was generated. | Selection and command enable/disable plumbing are present, but native selection visibility, keyboard behavior, and overflow could not be exercised. |
| 5 | Accessibility basics | 0 | 1 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/generated/MainWindow.xaml:23-52<br>guided/device-list/evidence/runtime-crash.txt:5-12 | No requested interactive controls or keyboard/accessibility path exists in the empty generation result. | Native labeled commands and an item AutomationProperties.Name are present, but keyboard, focus, selected-state, and UIA runtime exposure could not be verified. |
| 6 | Localization and scaling resilience | 0 | 1 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/generated/MainWindow.xaml:63-111<br>guided/device-list/generated/MainWindow.xaml.cs:9-13<br>guided/device-list/evidence/runtime-crash.txt:12-12 | Neither required long-language fixture was generated, so localization or 520-DIP resilience is absent. | Both required long fixtures and wrapping are present, but 520-DIP rendering and text scaling were not verified because runtime failed. |
| 7 | Native WinUI style preservation | 2 | 2 | baseline/device-list/CAPTURE.json:1-28<br>baseline/device-list/evidence/static-review.txt:5-11 | guided/device-list/evidence/static-review.txt:5-12 | No scenario implementation was generated, but the preserved starter source introduces no custom ControlTemplate, fixed-color system, or native-style replacement; this category does not imply the scenario itself was implemented. | Native CommandBar/ListView controls and built-in text styles are used without custom ControlTemplate or fixed-color replacement; theme rendering was not available. |
| 8 | Component-specific characteristics | 0 | 1 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/evidence/static-review.txt:6-10<br>guided/device-list/evidence/runtime-crash.txt:12-12 | No CommandBar or ListView characteristic is implemented. | Remove is placed in SecondaryCommands and ListView selection plumbing exists, but overflow and selection characteristics were not runnable. |
| 9 | Label, helper, and explanation separation | 0 | 2 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/generated/MainWindow.xaml:63-111 | No device labels, metadata, values, or empty-state explanation were generated. | Device name, connection label/value, status label/value, and empty-state explanation are separated structurally. |
| 10 | XAML simplicity and relevance | 0 | 2 | baseline/device-list/evidence/static-review.txt:5-14 | guided/device-list/generated/MainWindow.xaml:1-115<br>guided/device-list/generated/MainWindow.xaml.cs:1-56 | The unchanged starter project is small but is not the smallest clear implementation necessary for this scenario because it does not implement the scenario at all. | The XAML and code-behind are limited to the requested commands, list, empty state, data, selection, and small mutation handlers; no unrelated architecture is added. |

## Failure and confirmation

| # | Category | Baseline | Guided | Baseline evidence | Guided evidence | Baseline uncertainty | Guided uncertainty |
|---:|---|---:|---:|---|---|---|---|
| 1 | Content length and overflow | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/static-review.txt:5-10 | The required Korean failure message and dialog content were never generated. | Generation never began, so the required message and dialog content are absent. |
| 2 | Information hierarchy | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/static-review.txt:5-10 | No scenario status, explanation, or destructive-action hierarchy exists. | No scenario information hierarchy was generated. |
| 3 | Component anatomy | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/static-review.txt:5-10 | InfoBar and ContentDialog are both absent. | InfoBar and ContentDialog are absent because generation never began. |
| 4 | Native interaction states | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/generation-failure.txt:6-17<br>guided/failure-confirmation/evidence/static-review.txt:5-10 | Retry, dismissal, dialog actions, keyboard behavior, and focus flow are absent. | No Retry, dismissal, dialog, keyboard, or focus interaction was generated or run. |
| 5 | Accessibility basics | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/static-review.txt:5-10 | The requested interactive controls, accessible names, and focus behavior are absent. | No requested interactive controls or accessibility relationships exist in the empty generation result. |
| 6 | Localization and scaling resilience | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/static-review.txt:5-10 | The required Korean message and dialog explanation are absent, so localization/scaling resilience is not implemented. | The required Korean content was not generated, so localization/scaling resilience is absent. |
| 7 | Native WinUI style preservation | 2 | 2 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/CAPTURE.json:1-28<br>guided/failure-confirmation/evidence/static-review.txt:5-10 | The partial generation introduces no custom ControlTemplate or fixed-color replacement; this category does not imply the scenario was implemented. | No scenario implementation was generated, but the unchanged starter source introduces no custom ControlTemplate or fixed-color replacement; this does not imply the scenario was implemented. |
| 8 | Component-specific characteristics | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/static-review.txt:5-10 | No InfoBar or ContentDialog characteristic is implemented. | No InfoBar or ContentDialog characteristic was generated. |
| 9 | Label, helper, and explanation separation | 0 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/static-review.txt:5-10 | No status title/message, action labels, or dialog explanation were generated. | No status, action, or dialog text roles were generated. |
| 10 | XAML simplicity and relevance | 0 | 0 | baseline/failure-confirmation/generated/MainWindow.xaml:1-9<br>baseline/failure-confirmation/evidence/static-review.txt:5-16 | guided/failure-confirmation/evidence/generation-failure.txt:6-17<br>guided/failure-confirmation/evidence/static-review.txt:5-10 | The source is tiny but is only a title change over the starter and does not implement the requested scenario. | The unchanged starter project is not a scenario implementation. |

## Defect counts

| Scenario | Defect | Baseline | Guided |
|---|---|---:|---:|
| Connection settings | Clipping or content overflow | 0 | 0 |
| Connection settings | Missing component anatomy | 1 | 0 |
| Connection settings | Missing accessibility requirements | 2 | 0 |
| Connection settings | Unnecessary ControlTemplate replacements | 0 | 0 |
| Connection settings | Irrelevant XAML or complexity | 0 | 0 |
| Connection settings | Build failures | 0 | 0 |
| Connection settings | Rendered verification failures | 1 | 0 |
| Device list | Clipping or content overflow | 0 | 0 |
| Device list | Missing component anatomy | 3 | 0 |
| Device list | Missing accessibility requirements | 1 | 0 |
| Device list | Unnecessary ControlTemplate replacements | 0 | 0 |
| Device list | Irrelevant XAML or complexity | 0 | 0 |
| Device list | Build failures | 0 | 0 |
| Device list | Rendered verification failures | 0 | 1 |
| Failure and confirmation | Clipping or content overflow | 0 | 0 |
| Failure and confirmation | Missing component anatomy | 2 | 2 |
| Failure and confirmation | Missing accessibility requirements | 1 | 1 |
| Failure and confirmation | Unnecessary ControlTemplate replacements | 0 | 0 |
| Failure and confirmation | Irrelevant XAML or complexity | 0 | 0 |
| Failure and confirmation | Build failures | 0 | 0 |
| Failure and confirmation | Rendered verification failures | 0 | 0 |

## Traceable improvements

| Scenario | Category | Rule IDs | Evidence |
|---|---:|---|---|
| Connection settings | 1 | `WINUI-SIZE-WIDTH-001`, `WINUI-TEXT-LOCALIZATION-001` | guided/connection-settings/evidence/runtime-uia.txt:3-12 |
| Connection settings | 2 | `WINUI-TEXT-HIERARCHY-001` | guided/connection-settings/generated/MainWindow.xaml:10-29 |
| Connection settings | 3 | `WINUI-TEXTBOX-ANATOMY-001`, `WINUI-COMBO-ANATOMY-001`, `WINUI-TOGGLE-ANATOMY-001` | guided/connection-settings/generated/MainWindow.xaml:15-41 |
| Connection settings | 4 | `WINUI-A11Y-KEYBOARD-001`, `WINUI-COMBO-STATE-001`, `WINUI-TOGGLE-STATE-001` | guided/connection-settings/evidence/runtime-uia.txt:15-20 |
| Connection settings | 5 | `WINUI-A11Y-NAME-001`, `WINUI-A11Y-LABEL-001`, `WINUI-COMBO-A11Y-001` | guided/connection-settings/evidence/runtime-uia.txt:4-18<br>guided/connection-settings/generated/MainWindow.xaml:15-45 |
| Connection settings | 6 | `WINUI-SIZE-WIDTH-001`, `WINUI-TEXT-LOCALIZATION-001` | guided/connection-settings/evidence/runtime-uia.txt:3-12 |
| Connection settings | 7 | `WINUI-THEME-RESOURCE-001`, `WINUI-THEME-ACCENT-001` | guided/connection-settings/generated/MainWindow.xaml:12-45 |
| Connection settings | 8 | `WINUI-COMBO-STATE-001`, `WINUI-TOGGLE-STATE-001`, `WINUI-TEXTBOX-STATE-001` | guided/connection-settings/evidence/runtime-uia.txt:15-18 |
| Device list | 1 | `WINUI-LISTVIEW-LAYOUT-001`, `WINUI-TEXT-LOCALIZATION-001` | guided/device-list/generated/MainWindow.xaml:43-111 |
| Device list | 2 | `WINUI-TEXT-HIERARCHY-001`, `WINUI-LISTVIEW-CONTENT-001` | guided/device-list/generated/MainWindow.xaml:15-40<br>guided/device-list/generated/MainWindow.xaml:63-111 |
| Device list | 3 | `WINUI-COMMANDBAR-ANATOMY-001`, `WINUI-LISTVIEW-ANATOMY-001` | guided/device-list/evidence/static-review.txt:5-12 |
| Device list | 4 | `WINUI-COMMANDBAR-STATE-001`, `WINUI-LISTVIEW-STATE-001` | guided/device-list/evidence/static-review.txt:6-10 |
| Device list | 5 | `WINUI-COMMANDBAR-A11Y-001`, `WINUI-LISTVIEW-A11Y-001` | guided/device-list/generated/MainWindow.xaml:23-52 |
| Device list | 6 | `WINUI-TEXT-LOCALIZATION-001`, `WINUI-LISTVIEW-LAYOUT-001` | guided/device-list/generated/MainWindow.xaml:63-111<br>guided/device-list/generated/MainWindow.xaml.cs:9-13 |
| Device list | 8 | `WINUI-COMMANDBAR-STATE-001`, `WINUI-LISTVIEW-STATE-001` | guided/device-list/evidence/static-review.txt:6-10 |
| Device list | 9 | `WINUI-LISTVIEW-CONTENT-001`, `WINUI-LISTVIEW-CONTENT-002` | guided/device-list/generated/MainWindow.xaml:63-111 |
| Device list | 10 | `WINUI-LISTVIEW-XBIND-001`, `WINUI-SIZE-NATIVE-001` | guided/device-list/generated/MainWindow.xaml.cs:9-56<br>guided/device-list/evidence/static-review.txt:11-15 |
