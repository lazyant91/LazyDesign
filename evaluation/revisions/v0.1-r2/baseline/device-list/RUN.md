# Evaluation Run Record

Condition: baseline
Scenario: device-list
Run date and local time: 2026-08-09T02:29:42.489438+09:00
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
Build command: python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/v0.1-r2/baseline/device-list --matrix evaluation/revisions/v0.1-r2/run-matrix.json
Build result: exit 0
Rendered checks performed: ["commandbar_overflow","content_width","dark_theme","empty_state","english_long_content","keyboard_navigation","korean_long_content","listview_selection","remove_command_state","rendered_runtime"]
Checks not performed: ["accessibility_insights","focus_visual","high_contrast","light_theme","narrator","text_scaling"]
Notes: Fresh-context generation completed without intervention and used no network/web access. Controller reconciliation matched the reported two-file delta. The controlled build succeeded with 0 warnings and 0 errors. Runtime/UIA verification rendered at 520 DIP, exercised ListView selection and Remove state, keyboard traversal, dynamic CommandBar overflow at a narrower width, both required long names, and the empty-state transition. A controller-only UIA verifier indexing bug was corrected and rerun without modifying generated source. Packet hashes are recorded in PACKET.json.
