# Evaluation Run Record

Condition: baseline
Scenario: connection-settings
Run date and local time: 2026-08-09T02:14:58.4149491+09:00
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
Reference files supplied: none
Generation intervention: none
Generated file list: {"changed":["MainWindow.xaml","MainWindow.xaml.cs"],"deleted":[]}
Generation completion status: completed
Build command: python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/v0.1-r2/baseline/connection-settings --matrix evaluation/revisions/v0.1-r2/run-matrix.json
Build result: exit 0
Rendered checks performed: ["combobox_popup","content_width","dark_theme","keyboard_navigation","korean_long_content","rendered_runtime","save_button_activation","textbox_validation","toggleswitch_state"]
Checks not performed: ["accessibility_insights","english_long_content","focus_visual","high_contrast","light_theme","narrator","text_scaling"]
Notes: Fresh-context generation completed without intervention or infrastructure interruption. Controller reconciliation matched the reported two-file delta. Frozen source built with 0 warnings and 0 errors and completed runtime UI Automation at exactly 420 DIP. A PowerShell default-decoding issue in the controller static-review evidence was corrected by rereading the unchanged UTF-8 source with -Encoding UTF8; no generated source repair or generation rerun was performed. Packet hashes are recorded in PACKET.json.
