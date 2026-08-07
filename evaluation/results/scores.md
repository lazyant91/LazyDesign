# LazyDesign v0.1 Scores

## Scenario totals

| Scenario | Baseline | Guided | Delta |
|---|---:|---:|---:|
| Connection settings | 15 / 20 | 19 / 20 | +4 |
| Device list | 14 / 20 | 14 / 20 | +0 |
| Failure and confirmation | 15 / 20 | 13 / 20 | -2 |
| **Total** | **44 / 60** | **46 / 60** | **+2** |

## Connection settings

| # | Category | Baseline | Guided | Baseline evidence | Guided evidence | Baseline uncertainty | Guided uncertainty |
|---:|---|---:|---:|---|---|---|---|
| 1 | Content length and overflow | 2 | 2 | baseline/connection-settings/evidence/runtime-uia.txt:3-14 | guided/connection-settings/evidence/runtime-uia.txt:3-13 | none | none |
| 2 | Information hierarchy | 1 | 2 | baseline/connection-settings/generated/MainWindow.xaml:9-46 | guided/connection-settings/generated/MainWindow.xaml:10-39 | Hierarchy is judged from static structure; the screen also duplicates the automatic-reconnect concept between the ToggleSwitch header and a separate required-string TextBlock. | none |
| 3 | Component anatomy | 1 | 2 | baseline/connection-settings/generated/MainWindow.xaml:14-44<br>baseline/connection-settings/evidence/runtime-uia.txt:4-8 | guided/connection-settings/generated/MainWindow.xaml:12-37 | The required visible labels exist, but TextBox and ComboBox use adjacent TextBlocks instead of associated native headers; UI Automation shows the TextBox announced by placeholder text and the ComboBox with an empty name. | none |
| 4 | Native interaction states | 2 | 2 | baseline/connection-settings/evidence/runtime-uia.txt:15-23 | guided/connection-settings/evidence/runtime-uia.txt:14-21 | Pointer-over and focus visuals were not separately inspected, but keyboard traversal and the scenario-specific ComboBox, ToggleSwitch, validation, and Save transitions were exercised. | Pointer-over and focus visuals were not separately inspected, but keyboard traversal and scenario-specific native transitions were exercised. |
| 5 | Accessibility basics | 0 | 1 | baseline/connection-settings/evidence/runtime-uia.txt:4-8 | guided/connection-settings/evidence/runtime-uia.txt:4-9<br>guided/connection-settings/evidence/verification.json:1-102 | none | Accessible names and keyboard paths were observed, but focus-visual, Narrator, and Accessibility Insights checks were not performed, so the full score-2 anchor is not established. |
| 6 | Localization and scaling resilience | 2 | 2 | baseline/connection-settings/evidence/runtime-uia.txt:3-14 | guided/connection-settings/evidence/runtime-uia.txt:3-13 | Text scaling above 100 percent was not exercised; the scenario's required 420-DIP constrained-width behavior was directly measured. | Text scaling above 100 percent was not exercised; the scenario's required 420-DIP constrained-width behavior was directly measured. |
| 7 | Native WinUI style preservation | 1 | 2 | baseline/connection-settings/generated/MainWindow.xaml:20-24 | guided/connection-settings/generated/MainWindow.xaml:10-39<br>guided/connection-settings/evidence/static-review.txt:5-12 | The controls remain native, but the validation text hard-codes Foreground=Red instead of a theme/system resource; Light and contrast themes were not run. | Light and contrast themes were not run, but the generated source uses native controls and built-in semantic/accent styles without fixed colors or a local ControlTemplate. |
| 8 | Component-specific characteristics | 2 | 2 | baseline/connection-settings/evidence/runtime-uia.txt:15-23 | guided/connection-settings/evidence/runtime-uia.txt:14-20 | none | none |
| 9 | Label, helper, and explanation separation | 2 | 2 | baseline/connection-settings/generated/MainWindow.xaml:14-44 | guided/connection-settings/generated/MainWindow.xaml:12-37 | The ToggleSwitch subject is repeated, but field label, placeholder, helper, validation, values, and action text remain structurally distinct. | none |
| 10 | XAML simplicity and relevance | 2 | 2 | baseline/connection-settings/generated/MainWindow.xaml:1-49<br>baseline/connection-settings/generated/MainWindow.xaml.cs:1-34 | guided/connection-settings/generated/MainWindow.xaml:1-45<br>guided/connection-settings/generated/MainWindow.xaml.cs:1-35 | none | none |

## Device list

| # | Category | Baseline | Guided | Baseline evidence | Guided evidence | Baseline uncertainty | Guided uncertainty |
|---:|---|---:|---:|---|---|---|---|
| 1 | Content length and overflow | 1 | 1 | baseline/device-list/generated/MainWindow.xaml:25-35<br>baseline/device-list/evidence/build.txt:20-32 | guided/device-list/generated/MainWindow.xaml:25-31<br>guided/device-list/evidence/build.txt:20-32 | The required long strings are present with wrapping/trimming structure, but the build failure prevented 520-DIP rendered overflow verification. | The item template is structurally more fluid than the baseline, but the build failure prevented 520-DIP rendered overflow verification. |
| 2 | Information hierarchy | 2 | 2 | baseline/device-list/generated/MainWindow.xaml:25-35 | guided/device-list/generated/MainWindow.xaml:7-40 | none | none |
| 3 | Component anatomy | 2 | 2 | baseline/device-list/evidence/static-review.txt:5-8 | guided/device-list/evidence/static-review.txt:5-8 | Runtime anatomy could not be rendered because the frozen project did not build, but the required native component regions are explicit in XAML. | Runtime anatomy could not be rendered because the frozen project did not build, but the required native component regions are explicit in XAML. |
| 4 | Native interaction states | 1 | 1 | baseline/device-list/evidence/static-review.txt:5-16<br>baseline/device-list/evidence/build.txt:20-32 | guided/device-list/evidence/static-review.txt:5-16<br>guided/device-list/evidence/build.txt:20-32 | Native controls and selection/disabled state plumbing are present statically, but selection visibility, keyboard behavior, and overflow were not runnable. | Native selection and command-state plumbing are present statically, but selection visibility, keyboard behavior, and native overflow could not be exercised. |
| 5 | Accessibility basics | 1 | 1 | baseline/device-list/generated/MainWindow.xaml:9-22<br>baseline/device-list/evidence/build.txt:20-32 | guided/device-list/generated/MainWindow.xaml:12-17<br>guided/device-list/evidence/build.txt:20-32 | Native labeled AppBarButtons are present, but the build failure prevented UI Automation, keyboard, focus, and selected-state accessibility verification. | Explicit command names are present, but the build failure prevented UI Automation, focus, keyboard, and selected-state accessibility verification. |
| 6 | Localization and scaling resilience | 1 | 1 | baseline/device-list/generated/MainWindow.xaml:25-35<br>baseline/device-list/generated/MainWindow.xaml.cs:19-22 | guided/device-list/generated/MainWindow.xaml:27-31<br>guided/device-list/generated/MainWindow.xaml.cs:11-16 | Both long-language fixtures are present, but 520-DIP rendering and text scaling were not verified because the project did not build. | Both long-language fixtures are present with wrapping-oriented layout, but 520-DIP rendering and text scaling were not verified because the project did not build. |
| 7 | Native WinUI style preservation | 2 | 2 | baseline/device-list/generated/MainWindow.xaml:1-43 | guided/device-list/generated/MainWindow.xaml:1-44 | Rendered theme behavior was unavailable, but no custom ControlTemplate or fixed-color replacement appears in the frozen source. | Rendered theme behavior was unavailable, but no custom ControlTemplate or fixed-color replacement appears in the frozen source. |
| 8 | Component-specific characteristics | 1 | 1 | baseline/device-list/evidence/static-review.txt:5-16 | guided/device-list/evidence/static-review.txt:5-16 | CommandBar overflow and ListView selection semantics are represented statically but could not be exercised. | Remove is explicitly secondary for native overflow, but overflow and ListView selection could not be exercised because the project did not build. |
| 9 | Label, helper, and explanation separation | 2 | 2 | baseline/device-list/generated/MainWindow.xaml:25-35 | guided/device-list/generated/MainWindow.xaml:25-31 | none | none |
| 10 | XAML simplicity and relevance | 1 | 1 | baseline/device-list/generated/MainWindow.xaml:1-43<br>baseline/device-list/generated/MainWindow.xaml.cs:1-47 | guided/device-list/generated/MainWindow.xaml:7-40<br>guided/device-list/generated/MainWindow.xaml.cs:11-53 | The implementation is compact but adds three explicit keyboard accelerators and mutation/event plumbing beyond the minimum native controls, so it is not the smallest clear form. | The output adds a page title/subtitle, an ItemContainerStyle, and a third fixture device beyond the minimum requested scenario, while remaining straightforward. |

## Failure and confirmation

| # | Category | Baseline | Guided | Baseline evidence | Guided evidence | Baseline uncertainty | Guided uncertainty |
|---:|---|---:|---:|---|---|---|---|
| 1 | Content length and overflow | 1 | 1 | baseline/failure-confirmation/generated/MainWindow.xaml:16-43<br>baseline/failure-confirmation/evidence/build.txt:20-30 | guided/failure-confirmation/generated/MainWindow.xaml:8-39<br>guided/failure-confirmation/evidence/build.txt:20-30 | The long Korean message and dialog content have native/wrapping structure, but the build failure prevented rendered content-fit verification. | The required long Korean message and wrapped dialog explanation are present statically, but the build failure prevented rendered content-fit verification. |
| 2 | Information hierarchy | 2 | 2 | baseline/failure-confirmation/generated/MainWindow.xaml:12-43 | guided/failure-confirmation/generated/MainWindow.xaml:18-39 | none | none |
| 3 | Component anatomy | 2 | 2 | baseline/failure-confirmation/evidence/static-review.txt:5-10 | guided/failure-confirmation/evidence/static-review.txt:5-10 | The required native anatomy is explicit statically; runtime confirmation was unavailable because the project did not build. | The required native anatomy is explicit statically; runtime confirmation was unavailable because the project did not build. |
| 4 | Native interaction states | 1 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-14<br>baseline/failure-confirmation/evidence/build.txt:20-30 | guided/failure-confirmation/evidence/static-review.txt:11-16 | Retry, dismissal, dialog close/default, and focus-return plumbing exist in source but could not be exercised. | none |
| 5 | Accessibility basics | 1 | 1 | baseline/failure-confirmation/generated/MainWindow.xaml:18-21<br>baseline/failure-confirmation/generated/MainWindow.xaml:32-40 | guided/failure-confirmation/generated/MainWindow.xaml:19-39<br>guided/failure-confirmation/evidence/build.txt:20-30 | Explicit names and native roles are present, but keyboard/focus behavior and assistive-technology exposure could not be verified after the build failure. | Explicit button names and native roles are present, but the build failure prevented keyboard/focus and assistive-technology verification. |
| 6 | Localization and scaling resilience | 1 | 1 | baseline/failure-confirmation/generated/MainWindow.xaml:16-18<br>baseline/failure-confirmation/generated/MainWindow.xaml:40-42 | guided/failure-confirmation/generated/MainWindow.xaml:20-22<br>guided/failure-confirmation/evidence/build.txt:20-30 | The required Korean message and wrapped dialog explanation are present statically; no rendered scaling or long-content check was possible. | The required Korean message is present; rendered scaling and long-content behavior were not available. |
| 7 | Native WinUI style preservation | 2 | 2 | baseline/failure-confirmation/generated/MainWindow.xaml:1-44 | guided/failure-confirmation/generated/MainWindow.xaml:1-42 | Rendered theme behavior was unavailable, but native InfoBar/ContentDialog controls are used without a custom ControlTemplate or fixed-color system. | Rendered theme behavior was unavailable, but native InfoBar/ContentDialog controls are used without a custom ControlTemplate or fixed-color system. |
| 8 | Component-specific characteristics | 1 | 0 | baseline/failure-confirmation/evidence/static-review.txt:5-14 | guided/failure-confirmation/evidence/static-review.txt:11-16 | Scenario-relevant InfoBar and ContentDialog behavior is wired in source but could not be run. | none |
| 9 | Label, helper, and explanation separation | 2 | 2 | baseline/failure-confirmation/generated/MainWindow.xaml:16-43 | guided/failure-confirmation/generated/MainWindow.xaml:19-39 | none | none |
| 10 | XAML simplicity and relevance | 2 | 2 | baseline/failure-confirmation/generated/MainWindow.xaml:1-44<br>baseline/failure-confirmation/generated/MainWindow.xaml.cs:1-28 | guided/failure-confirmation/generated/MainWindow.xaml:1-42<br>guided/failure-confirmation/generated/MainWindow.xaml.cs:1-23 | none | none |

## Defect counts

| Scenario | Defect | Baseline | Guided |
|---|---|---:|---:|
| Connection settings | Clipping or content overflow | 0 | 0 |
| Connection settings | Missing component anatomy | 1 | 0 |
| Connection settings | Missing accessibility requirements | 2 | 0 |
| Connection settings | Unnecessary ControlTemplate replacements | 0 | 0 |
| Connection settings | Irrelevant XAML or complexity | 0 | 0 |
| Connection settings | Build failures | 0 | 0 |
| Connection settings | Rendered verification failures | 0 | 0 |
| Device list | Clipping or content overflow | 0 | 0 |
| Device list | Missing component anatomy | 0 | 0 |
| Device list | Missing accessibility requirements | 0 | 0 |
| Device list | Unnecessary ControlTemplate replacements | 0 | 0 |
| Device list | Irrelevant XAML or complexity | 1 | 1 |
| Device list | Build failures | 1 | 1 |
| Device list | Rendered verification failures | 0 | 0 |
| Failure and confirmation | Clipping or content overflow | 0 | 0 |
| Failure and confirmation | Missing component anatomy | 0 | 0 |
| Failure and confirmation | Missing accessibility requirements | 0 | 0 |
| Failure and confirmation | Unnecessary ControlTemplate replacements | 0 | 0 |
| Failure and confirmation | Irrelevant XAML or complexity | 0 | 0 |
| Failure and confirmation | Build failures | 1 | 1 |
| Failure and confirmation | Rendered verification failures | 0 | 0 |

## Traceable improvements

| Scenario | Category | Rule IDs | Evidence |
|---|---:|---|---|
| Connection settings | 2 | `WINUI-TEXT-HIERARCHY-001` | guided/connection-settings/generated/MainWindow.xaml:10-22 |
| Connection settings | 3 | `WINUI-TEXTBOX-ANATOMY-001`, `WINUI-TOGGLE-ANATOMY-001` | guided/connection-settings/generated/MainWindow.xaml:12-37 |
| Connection settings | 5 | `WINUI-A11Y-NAME-001`, `WINUI-A11Y-LABEL-001`, `WINUI-COMBO-A11Y-001` | guided/connection-settings/generated/MainWindow.xaml:12-37<br>guided/connection-settings/evidence/runtime-uia.txt:4-9 |
| Connection settings | 7 | `WINUI-THEME-RESOURCE-001` | guided/connection-settings/generated/MainWindow.xaml:10-39 |
