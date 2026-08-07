# Failure and Confirmation Evaluation Task

Create WinUI 3 UI for a failed device connection and a destructive removal confirmation.

Requirements:

- Use an InfoBar to show a connection failure with title, message, severity, a Retry action, and dismissal.
- Use a ContentDialog to confirm removal of a saved device.
- The failure message must include: `장치가 응답하지 않았습니다. 장치가 켜져 있고 동일한 네트워크에 연결되어 있는지 확인한 후 다시 시도하세요.`
- The dialog must identify the selected device and provide Remove, Cancel, and close behavior appropriate to the native control.
- Preserve keyboard focus, accessible names, and native WinUI visual states.
- Do not create custom control templates.
- Implement the UI in XAML with the smallest necessary C# or ViewModel support.
