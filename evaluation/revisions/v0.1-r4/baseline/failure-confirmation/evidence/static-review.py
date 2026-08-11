from pathlib import Path
from datetime import datetime

packet = Path(r"Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r4\baseline\failure-confirmation")
x = (packet / "project" / "MainWindow.xaml").read_text(encoding="utf-8")
c = (packet / "project" / "MainWindow.xaml.cs").read_text(encoding="utf-8")
message = "\uc7a5\uce58\uac00 \uc751\ub2f5\ud558\uc9c0 \uc54a\uc558\uc2b5\ub2c8\ub2e4. \uc7a5\uce58\uac00 \ucf1c\uc838 \uc788\uace0 \ub3d9\uc77c\ud55c \ub124\ud2b8\uc6cc\ud06c\uc5d0 \uc5f0\uacb0\ub418\uc5b4 \uc788\ub294\uc9c0 \ud655\uc778\ud55c \ud6c4 \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694."
checks = {
    "InfoBar": "<InfoBar" in x,
    "ErrorSeverity": 'Severity="Error"' in x,
    "Closable": 'IsClosable="True"' in x,
    "RetryAction": "<InfoBar.ActionButton>" in x and 'x:Name="RetryButton"' in x and 'Click="RetryButton_Click"' in x,
    "ExactKoreanFailureMessage": message in x,
    "ContentDialog": "<ContentDialog" in x,
    "DialogIdentifiesDevice": "\uac70\uc2e4 \uc2a4\ud53c\ucee4" in x,
    "PrimaryRemove": 'PrimaryButtonText="\uc81c\uac70"' in x,
    "CloseCancel": 'CloseButtonText="\ucde8\uc18c"' in x,
    "SafeDefaultClose": 'DefaultButton="Close"' in x,
    "AccessibleNames": "AutomationProperties.Name=" in x,
    "NoControlTemplate": "ControlTemplate" not in x,
    "RetryHandlerImplemented": "RetryButton_Click" in c,
    "RemoveHandlerImplemented": "RemoveDeviceButton_Click" in c,
    "FocusReturnLogic": "FocusManager.GetFocusedElement" in c and "_focusBeforeDialog?.Focus" in c,
    "ShowAsyncAwaited": "await RemoveDeviceDialog.ShowAsync()" in c,
    "SystemNamespaceImported": "using System;" in c,
}
lines = ["# Read-only static review of frozen generated source", f"Recorded at: {datetime.now().astimezone().isoformat()}"]
lines += [f"{k}={v}" for k, v in checks.items()]
lines.append("BuildCompatibility=False")
lines.append("BuildCompatibilityDetail=ContentDialog.ShowAsync() returns IAsyncOperation<ContentDialogResult>; generated code awaits it without importing System, and the controlled build failed CS4036 because GetAwaiter was unavailable.")
lines.append("Result=FAIL")
(packet / "evidence" / "static-review.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
