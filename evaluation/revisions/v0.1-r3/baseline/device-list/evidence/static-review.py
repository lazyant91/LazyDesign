from pathlib import Path
import datetime

root = Path(__file__).resolve().parents[1] / "project"
xaml = (root / "MainWindow.xaml").read_text(encoding="utf-8")
code = (root / "MainWindow.xaml.cs").read_text(encoding="utf-8")
checks = {
    "CommandBar": "<CommandBar" in xaml,
    "DynamicOverflow": 'IsDynamicOverflowEnabled="True"' in xaml,
    "Refresh": 'Label="Refresh"' in xaml and "RefreshButton_Click" in code,
    "Add": 'Label="Add device"' in xaml and "AddButton_Click" in code,
    "Remove": 'Label="Remove"' in xaml and "RemoveButton_Click" in code,
    "RemoveInitiallyDisabled": 'IsEnabled="False"' in xaml,
    "ListView": "<ListView" in xaml and "DeviceListView" in xaml,
    "NameBinding": "{Binding Name}" in xaml,
    "ConnectionBinding": "{Binding ConnectionType}" in xaml,
    "StatusBinding": "{Binding Status}" in xaml,
    "SingleSelection": 'SelectionMode="Single"' in xaml,
    "EmptyState": "No devices" in xaml and "EmptyStatePanel" in code,
    "SelectionChangesRemove": "DeviceListView_SelectionChanged" in xaml and "RemoveButton.IsEnabled = hasSelection" in code,
    "KoreanLong": any(ord(ch) > 127 for ch in code) and "Wi-Fi" in code,
    "EnglishLong": "Portable conference-room presentation receiver" in code,
    "NoControlTemplate": "ControlTemplate" not in xaml,
}
lines = [
    "# Read-only static review of frozen generated source",
    "Recorded at: " + datetime.datetime.now().astimezone().isoformat(),
]
lines += [f"{key}={value}" for key, value in checks.items()]
lines.append("Result=" + ("PASS" if all(checks.values()) else "FAIL"))
(Path(__file__).with_name("static-review.txt")).write_text("\n".join(lines) + "\n", encoding="utf-8")
