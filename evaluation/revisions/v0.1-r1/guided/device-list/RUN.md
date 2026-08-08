# Evaluation Run Record

Condition: guided
Scenario: device-list
Run date and local time: 2026-08-08T20:43:07+09:00
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
Reference files supplied: see PACKET.json
Generation intervention: none
Generated file list: {"changed":["MainWindow.xaml","MainWindow.xaml.cs"],"deleted":[]}
Generation completion status: completed
Build command: python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/v0.1-r1/guided/device-list --matrix evaluation/revisions/v0.1-r1/run-matrix.json
Build result: exit 0
Rendered checks performed: ["rendered_runtime"]
Checks not performed: ["accessibility_insights","commandbar_overflow","content_width","dark_theme","empty_state","english_long_content","focus_visual","high_contrast","keyboard_navigation","korean_long_content","light_theme","listview_selection","narrator","remove_command_state","text_scaling"]
Notes: Fresh Temporary Chat generation completed without intervention and read only the exact nine packet-local references. Controller verification preserved frozen source. The controlled build succeeded with 0 warnings and 0 errors, eliminating the original CS8852 typed-x:Bind model build failure. A read-only runtime/UIA launch was then attempted once, but the executable exited before a top-level window appeared; Windows Application event 1000 identified Microsoft.UI.Xaml.dll with exception code 0xc000027b. No generated source repair or regeneration was performed. Packet hashes are recorded in PACKET.json.
