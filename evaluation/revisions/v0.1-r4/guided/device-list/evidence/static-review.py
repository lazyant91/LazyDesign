from pathlib import Path
from datetime import datetime

packet = Path(r"Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r4\guided\device-list")
x = (packet / "project" / "MainWindow.xaml").read_text(encoding="utf-8")
c = (packet / "project" / "MainWindow.xaml.cs").read_text(encoding="utf-8")
checks = {
    "CommandBar": "<CommandBar" in x,
    "DynamicOverflow": 'IsDynamicOverflowEnabled="True"' in x,
    "RefreshCommand": 'Label="Refresh"' in x,
    "AddDeviceCommand": 'Label="Add device"' in x,
    "RemoveCommand": 'Label="Remove"' in x,
    "RemoveAsSecondaryCommand": "<CommandBar.SecondaryCommands>" in x,
    "ListView": "<ListView" in x,
    "NameBinding": 'Text="{x:Bind Name}"' in x,
    "ConnectionTypeBinding": 'Text="{x:Bind ConnectionType}"' in x,
    "StatusBinding": 'Text="{x:Bind Status}"' in x,
    "SingleSelection": 'SelectionMode="Single"' in x,
    "SelectionDrivenRemoveState": "RemoveDeviceButton.IsEnabled = DeviceList.SelectedItem is DeviceViewModel" in c,
    "EmptyState": 'x:Name="EmptyState"' in x and "Devices.Count > 0" in c,
    "KoreanLongFixture": "\ud68c\uc758\uc2e4 \ub514\uc2a4\ud50c\ub808\uc774 \ubb34\uc120 \ud504\ub808\uc820\ud14c\uc774\uc158 \uc218\uc2e0 \uc7a5\uce58" in c,
    "EnglishLongFixture": "Portable conference-room presentation receiver" in c,
    "NativeControlsNoCustomTemplate": "ControlTemplate" not in x,
    "ValidEmptyStateIcon": 'Symbol="World"' in x,
    "MutableViewModelProperties": "public string Name { get; set; }" in c and "public string ConnectionType { get; set; }" in c and "public string Status { get; set; }" in c,
    "MinimalCodeBehind": len(c) < 8000,
}
lines = ["# Read-only static review of frozen generated source", f"Recorded at: {datetime.now().astimezone().isoformat()}"]
lines += [f"{k}={v}" for k, v in checks.items()]
lines.append("Result=" + ("PASS" if all(checks.values()) else "FAIL"))
(packet / "evidence" / "static-review.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
