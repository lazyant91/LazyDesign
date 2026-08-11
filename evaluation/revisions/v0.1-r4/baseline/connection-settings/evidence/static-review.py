from pathlib import Path
from datetime import datetime

packet = Path(r"Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r4\baseline\connection-settings")
x = (packet / "project" / "MainWindow.xaml").read_text(encoding="utf-8")
c = (packet / "project" / "MainWindow.xaml.cs").read_text(encoding="utf-8")
checks = {
    "TextBox": "<TextBox" in x,
    "ComboBox": "<ComboBox" in x,
    "USB": 'Content="USB"' in x,
    "WiFi": 'Content="Wi-Fi"' in x,
    "Bluetooth": 'Content="Bluetooth"' in x,
    "ToggleSwitch": "<ToggleSwitch" in x,
    "SaveButton": "<Button" in x and "SaveSettingsButton_Click" in x,
    "PersistentNameLabel": 'Header="\uc5f0\uacb0 \ud504\ub85c\ud544 \uc774\ub984"' in x,
    "PersistentTransportLabel": 'Header="\uc804\uc1a1 \ubc29\uc2dd"' in x,
    "HelperSentence": "\uc7a5\uce58\ub97c \uad6c\ubd84\ud560 \uc218 \uc788\ub294 \uc774\ub984\uc744 \uc785\ub825\ud558\uc138\uc694." in x,
    "InlineValidation": "NameValidationInfoBar" in x and "\uc5f0\uacb0 \ud504\ub85c\ud544 \uc774\ub984\uc744 \uc785\ub825\ud558\uc138\uc694." in x,
    "KoreanToggle": "\uc0ac\uc6a9 \uac00\ub2a5\ud55c \uc7a5\uce58\uc5d0 \uc790\ub3d9\uc73c\ub85c \ub2e4\uc2dc \uc5f0\uacb0" in x,
    "KoreanSave": "\uc5f0\uacb0 \uc124\uc815 \uc800\uc7a5" in x,
    "HorizontalScrollDisabled": 'HorizontalScrollMode="Disabled"' in x and 'HorizontalScrollBarVisibility="Disabled"' in x,
    "WidthConstraint420": 'MaxWidth="420"' in x,
    "ValidationChangesWithText": "ConnectionNameTextBox_TextChanged" in x and "NameValidationInfoBar.IsOpen" in c,
    "InvalidSaveFocusReturn": "ConnectionNameTextBox.Focus" in c,
    "NativeControlsNoCustomTemplate": "ControlTemplate" not in x,
    "MinimalCodeBehind": len(c) < 5000,
}
lines = ["# Read-only static review of frozen generated source", f"Recorded at: {datetime.now().astimezone().isoformat()}"]
lines += [f"{k}={v}" for k, v in checks.items()]
lines.append("Result=" + ("PASS" if all(checks.values()) else "FAIL"))
(packet / "evidence" / "static-review.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
