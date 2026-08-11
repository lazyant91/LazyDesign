from pathlib import Path
from datetime import datetime

packet = Path(r"Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r3\guided\connection-settings")
x = (packet / "project" / "MainWindow.xaml").read_text(encoding="utf-8")
c = (packet / "project" / "MainWindow.xaml.cs").read_text(encoding="utf-8")
checks = {
    "TextBox": "<TextBox" in x,
    "ComboBox": "<ComboBox" in x,
    "ToggleSwitch": "<ToggleSwitch" in x,
    "SaveButton": "<Button" in x,
    "KoreanHeader": "\uc5f0\uacb0 \ud504\ub85c\ud544 \uc774\ub984" in x,
    "KoreanHelper": "\uc7a5\uce58\ub97c \uad6c\ubd84\ud560 \uc218 \uc788\ub294 \uc774\ub984\uc744 \uc785\ub825\ud558\uc138\uc694." in x,
    "KoreanToggle": "\uc0ac\uc6a9 \uac00\ub2a5\ud55c \uc7a5\uce58\uc5d0 \uc790\ub3d9\uc73c\ub85c \ub2e4\uc2dc \uc5f0\uacb0" in x,
    "ValidationMessage": "\uc5f0\uacb0 \ud504\ub85c\ud544 \uc774\ub984\uc744 \uc785\ub825\ud558\uc138\uc694." in x,
    "HorizontalScrollDisabled": 'HorizontalScrollMode="Disabled"' in x,
    "NativeControlsNoCustomTemplate": "ControlTemplate" not in x,
    "AccentSaveStyle": "AccentButtonStyle" in x,
    "HelpText": "AutomationProperties.HelpText" in x,
    "InvalidFocusReturn": "ConnectionNameTextBox.Focus" in c,
    "MinimalCodeBehind": len(c) < 5000,
}
lines = ["# Read-only static review of frozen generated source", f"Recorded at: {datetime.now().astimezone().isoformat()}"]
lines += [f"{k}={v}" for k, v in checks.items()]
lines.append("Result=" + ("PASS" if all(checks.values()) else "FAIL"))
(packet / "evidence" / "static-review.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
