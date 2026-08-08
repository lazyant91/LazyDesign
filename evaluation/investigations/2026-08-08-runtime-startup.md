# WinUI runtime-startup investigation — 2026-08-08

## Scope

This is a post-hoc controller investigation performed outside the immutable scored v0.1-r1 artifacts. It does not alter or reinterpret any captured source, evidence, score, metric, or Gate v2 decision.

## Observed failures

Two v0.1-r1 runs built successfully and then exited before a top-level window became available:

- `baseline/connection-settings`: `Microsoft.UI.Xaml.dll`, exception `0xc000027b`, fault offset `0x3ac82d`.
- `guided/device-list`: the same module, exception code, and fault offset.

`guided/connection-settings` ran successfully on the same Windows host with the same pinned .NET SDK and Windows App SDK package, so the failure was not treated as a host-wide WinUI startup failure.

## Controlled reproduction

The controller reconstructed temporary copies from the pinned start fixture commit `b73babad19d0153707a49e5ba1ed9fb0a42c33ef` and copied the frozen generated `MainWindow.xaml` and `MainWindow.xaml.cs` files without changing them.

Using .NET SDK `9.0.313` and the fixture's Windows App SDK `2.0.1` dependency:

- the baseline connection-settings copy rebuilt with 0 warnings / 0 errors and reproduced exit `-1073741189` (`0xc000027b`);
- a guided connection-settings control copy rebuilt and produced a top-level window.

Temporary diagnostic exception logging around `MainWindow` construction exposed the inner XAML load failures:

- baseline connection-settings: `Cannot find a Resource with the Name/Key SystemFillColorCriticalBrush` at `MainWindow.xaml` line 17;
- guided device-list: `Cannot find a Resource with the Name/Key BodyStrongTextBlockStyle` at `MainWindow.xaml` line 106.

Both failures occurred in `MainWindow.InitializeComponent()` as `Microsoft.UI.Xaml.Markup.XamlParseException` instances.

## Resource evidence

The installed `Microsoft.WindowsAppSDK.WinUI` package used by the Windows App SDK 2.0.1 restore contains both resource keys in its `generic.xaml`; they were not nonexistent package resources. Microsoft Learn also documents `BodyStrongTextBlockStyle` as part of the Windows XAML type ramp.

The pinned start fixture instead had an empty `Application.Resources` element and did not merge `XamlControlsResources`.

Microsoft documents `Microsoft.UI.Xaml.Controls.XamlControlsResources` as the resource dictionary that supplies the default styles for controls in the WinUI library and shows it under `Application.Resources`:

- https://learn.microsoft.com/windows/windows-app-sdk/api/winrt/microsoft.ui.xaml.controls.xamlcontrolsresources
- https://learn.microsoft.com/windows/apps/develop/platform/xaml/xaml-theme-resources

## Root-cause test

The controller created new temporary copies of the two failing projects and changed only `App.xaml` to include:

```xml
<Application.Resources>
    <XamlControlsResources xmlns="using:Microsoft.UI.Xaml.Controls" />
</Application.Resources>
```

No generated `MainWindow` source was changed.

Results:

- baseline connection-settings: build passed and a top-level window was created;
- guided device-list: build passed and a top-level `Device list` window was created;
- a separate future-fixture smoke copy directly using both `BodyStrongTextBlockStyle` and `SystemFillColorCriticalBrush` also built with 0 warnings / 0 errors and created a window.

This isolates the missing `XamlControlsResources` merge in the evaluation start fixture as the cause of both observed v0.1-r1 startup crashes.

## Interpretation

The two recorded runtime failures remain valid observations of the immutable v0.1-r1 run environment, but they are confounded by the start fixture. They must not be attributed to Windows App SDK instability or generated UI quality without this fixture caveat.

The existing v0.1 and v0.1-r1 matrices and captured results remain unchanged. They intentionally continue to pin the historical start fixture commit used by those experiments.

## Forward correction

For future evaluation revisions:

1. the working-tree start fixture must merge `XamlControlsResources`;
2. a regression test must prevent that resource dictionary from being removed from future fixture commits;
3. any new run matrix must pin a new start-project commit that contains this correction rather than silently changing the fixture under an existing matrix;
4. a build pass must continue to be treated separately from rendered runtime verification.

The separate Temporary Chat / Remote safety-inspection reliability issue remains unresolved by this fixture correction and should be handled as an evaluation-execution contract problem, not bundled into the runtime fix.
