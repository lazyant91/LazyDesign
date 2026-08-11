# Evaluation Run Record

Condition: guided
Scenario: connection-settings
Run date and local time: 2026-08-10T20:50:41.8690323+09:00
Model identifier: GPT-5.6 Sol
Reasoning level: not exposed by client
Fresh context: yes
Generation stopping condition: PROMPT.md requirements implemented; source frozen before build
Starting project repository and SHA: lazyant91/LazyDesign 2ffa7d4dcfe76d4ed7671e116bbdbe5d62528e90
Operating system: Microsoft Windows NT 10.0.19045.0
.NET SDK: 9.0.313
Windows App SDK package: 2.0.1
Tool access: ChatGPT Remote local filesystem/process tools; Windows PowerShell; Windows UI Automation; no local Codex, subagent, or parallel agent
Network access: generation used no network/web access
Reference files supplied: see PACKET.json
Generation intervention: none
Generated file list: {"changed":["MainWindow.xaml","MainWindow.xaml.cs"],"deleted":[]}
Generation completion status: completed; stopping condition reached
Build command: python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/v0.1-r4/guided/connection-settings --matrix evaluation/revisions/v0.1-r4/run-matrix.json
Build result: exit 0
Rendered checks performed: ["combobox_popup","content_width","dark_theme","keyboard_navigation","korean_long_content","rendered_runtime","save_button_activation","textbox_validation","toggleswitch_state"]
Checks not performed: ["accessibility_insights","english_long_content","focus_visual","high_contrast","light_theme","narrator","text_scaling"]
Notes: The generator reported that no project files were modified, but controller reconciliation against PACKET.json hashes found MainWindow.xaml and MainWindow.xaml.cs changed with no deletions; disk state is authoritative for capture. No timeout, safety inspection, transport failure, or other material infrastructure interruption was reported, and the fixed stopping condition was reached, so the attempt is valid. The controlled pinned build exited 0. Read-only static review found the prompt requirements and relevant guided accessibility/state guidance represented in frozen source. Runtime UI Automation at exactly 420 DIP exercised validation, native ComboBox expansion and Bluetooth selection, ToggleSwitch Off-to-On, keyboard traversal, and empty-name Save focus return. All observed major controls and visible text remained inside horizontal client bounds. Controller-only verifier path/environment corrections were made without changing generated source hashes.
