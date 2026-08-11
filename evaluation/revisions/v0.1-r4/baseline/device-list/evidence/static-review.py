from pathlib import Path
from datetime import datetime

packet = Path(r"Z:\workspace\LazyDesign\evaluation\.runs\v2\v0.1-r4\baseline\device-list")
x = (packet / "project" / "MainWindow.xaml").read_text(encoding="utf-8")
c = (packet / "project" / "MainWindow.xaml.cs").read_text(encoding="utf-8")
checks = {
    "CommandBar": "<CommandBar" in x,
    "DynamicOverflow": 'IsDynamicOverflowEnabled="True"' in x,
    "Refresh": 'Label="Refresh"' in x,
    "AddDevice": 'Label="Add device"' in x,
    "Remove": 'Label="Remove"' in x,
    "RemoveInitiallyDisabled": 'IsEnabled="False"' in x,
    "ListView": "<ListView" in x,
    "NameBinding": "{x:Bind Name}" in x,
    "ConnectionBinding": "{x:Bind ConnectionType}" in x,
    "StatusBinding": "{x:Bind Status}" in x,
    "SingleSelection": 'SelectionMode="Single"' in x,
    "EmptyState": 'x:Name="EmptyState"' in x and 'Text="No devices"' in x,
    "SelectionChangesRemove": "RemoveButton.IsEnabled = DeviceList.SelectedItem is not null" in c,
    "KoreanLong": "\ud68c\uc758\uc2e4 \ub514\uc2a4\ud50c\ub808\uc774 \ubb34\uc120 \ud504\ub808\uc820\ud14c\uc774\uc158 \uc218\uc2e0 \uc7a5\uce58" in c,
    "EnglishLong": "Portable conference-room presentation receiver" in c,
    "NoControlTemplate": "ControlTemplate" not in x,
    "RecordWithInitOnlyProperties": "public sealed record DeviceItem" in c,
}
lines = ["# Read-only static review of frozen generated source", f"Recorded at: {datetime.now().astimezone().isoformat()}"]
lines += [f"{k}={v}" for k, v in checks.items()]
lines += [
    "BuildCompatibility=False",
    "BuildCompatibilityDetail=DeviceItem is a positional record, so Name/ConnectionType/Status are init-only; controlled WinUI XAML generation emitted setters in XamlTypeInfo.g.cs and failed with CS8852 for all three properties.",
    "Result=FAIL",
]
(packet / "evidence" / "static-review.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
