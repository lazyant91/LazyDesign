from pathlib import Path
from datetime import datetime

packet = Path(r"Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r4\guided\failure-confirmation")
x = (packet / "project" / "MainWindow.xaml").read_text(encoding="utf-8")
c = (packet / "project" / "MainWindow.xaml.cs").read_text(encoding="utf-8")
required_message = "\uc7a5\uce58\uac00 \uc751\ub2f5\ud558\uc9c0 \uc54a\uc558\uc2b5\ub2c8\ub2e4. \uc7a5\uce58\uac00 \ucf1c\uc838 \uc788\uace0 \ub3d9\uc77c\ud55c \ub124\ud2b8\uc6cc\ud06c\uc5d0 \uc5f0\uacb0\ub418\uc5b4 \uc788\ub294\uc9c0 \ud655\uc778\ud55c \ud6c4 \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694."
checks = {
    "InfoBar": "<InfoBar" in x,
    "ErrorSeverity": 'Severity="Error"' in x,
    "InfoBarClosable": 'IsClosable="True"' in x,
    "RetryAction": "<InfoBar.ActionButton>" in x and 'Click="RetryConnection_Click"' in x,
    "ExactKoreanFailureMessage": required_message in x,
    "ContentDialog": "<ContentDialog" in x,
    "DialogIdentifiesSelectedDevice": "\ud68c\uc758\uc2e4 \ub514\uc2a4\ud50c\ub808\uc774" in x and "\uc120\ud0dd\ud55c \uc7a5\uce58" in x,
    "PrimaryRemove": 'PrimaryButtonText="Remove"' in x,
    "CloseCancel": 'CloseButtonText="Cancel"' in x,
    "SafeDefaultClose": 'DefaultButton="Close"' in x,
    "RetryAccessibleName": 'AutomationProperties.Name="\uc7a5\uce58 \uc5f0\uacb0 \ub2e4\uc2dc \uc2dc\ub3c4"' in x,
    "RemoveAccessibleName": 'AutomationProperties.Name="\ud68c\uc758\uc2e4 \ub514\uc2a4\ud50c\ub808\uc774 \uc800\uc7a5\ub41c \uc7a5\uce58 \uc81c\uac70"' in x,
    "NoControlTemplate": "ControlTemplate" not in x,
    "RetryHandlerImplemented": "RetryConnection_Click" in c and "ConnectionErrorInfoBar.IsOpen = true" in c,
    "RemoveHandlerImplemented": "RemoveDeviceButton_Click" in c and "RemoveDeviceDialog.ShowAsync" in c,
    "DialogXamlRootAssigned": "RemoveDeviceDialog.XamlRoot = Content.XamlRoot" in c,
    "SystemNamespaceImported": "using System;" in c,
    "MinimalCodeBehind": len(c) < 5000,
}
lines = ["# Read-only static review of frozen generated source", f"Recorded at: {datetime.now().astimezone().isoformat()}"]
lines += [f"{k}={v}" for k, v in checks.items()]
lines.append("Result=" + ("PASS" if all(checks.values()) else "FAIL"))
(packet / "evidence" / "static-review.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
