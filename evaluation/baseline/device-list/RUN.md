# Evaluation Run Record

Condition: baseline
Scenario: device-list
Run date and local time: 2026-08-07T14:32:38+09:00
Model identifier: GPT-5.6 Sol
Reasoning level: not exposed by client
Fresh context: yes
Generation stopping condition: PROMPT.md requirements implemented; source frozen before build
Starting project repository and SHA: lazyant91/LazyDesign b73babad19d0153707a49e5ba1ed9fb0a42c33ef
Operating system: Microsoft Windows NT 10.0.19045.0
.NET SDK: 9.0.313
Windows App SDK package: 2.0.1
Tool access: ChatGPT Remote local filesystem/process tools; Windows PowerShell; Windows UI Automation; no local Codex, subagent, or parallel agent
Network access: generation used no network/web access
Reference files supplied: none
Generation intervention: none
Generated file list: {"changed":["MainWindow.xaml","MainWindow.xaml.cs"],"deleted":[]}
Generation completion status: completed
Build command: python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/device-list
Build result: exit 1
Rendered checks performed: []
Checks not performed: ["accessibility_insights","commandbar_overflow","content_width","dark_theme","empty_state","english_long_content","focus_visual","high_contrast","keyboard_navigation","korean_long_content","light_theme","listview_selection","narrator","remove_command_state","rendered_runtime","text_scaling"]
Notes: generation was performed in a fresh Temporary Chat; the controlled build failed with preserved CS8852 typed-XAML/model errors, so no runtime checks were performed and no source repair was made; post-generation verification and capture were performed by the controller session; packet hashes are recorded in PACKET.json
