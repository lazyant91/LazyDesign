# Evaluation Run Record

Condition: guided
Scenario: connection-settings
Run date and local time: 2026-08-08T18:44:35+09:00
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
Build command: python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/v0.1-r1/guided/connection-settings --matrix evaluation/revisions/v0.1-r1/run-matrix.json
Build result: exit 0
Rendered checks performed: ["combobox_popup","content_width","dark_theme","keyboard_navigation","korean_long_content","rendered_runtime","save_button_activation","textbox_validation","toggleswitch_state"]
Checks not performed: ["accessibility_insights","english_long_content","focus_visual","high_contrast","light_theme","narrator","text_scaling"]
Notes: Fresh Temporary Chat generation completed without intervention and read only the exact nine packet-local references. Controller verification preserved frozen source. The controlled build succeeded with 0 warnings and 0 errors. The first copied runtime verifier used an exact ToggleSwitch accessible-name selector and stopped after launch; a read-only UIA diagnostic confirmed AutomationId AutoReconnectToggle with TogglePattern, so only the evidence verifier selector was changed to AutomationId and the same runtime sequence rerun. Generated source was never changed. Runtime at 420 DIP then completed; Save with an empty name showed validation but focus remained on the Save Button. Packet hashes are recorded in PACKET.json.
