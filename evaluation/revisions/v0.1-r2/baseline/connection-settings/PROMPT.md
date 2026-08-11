# Connection Settings Evaluation Task

Create a WinUI 3 settings page for configuring a device connection.

Requirements:

- Use a TextBox for the connection name.
- Use a ComboBox for the transport with USB, Wi-Fi, and Bluetooth options.
- Use a ToggleSwitch for automatic reconnection.
- Use a Button to save the settings.
- Show persistent labels, one short helper sentence for the connection name, and an inline validation message when the name is empty.
- The page must remain usable in a 420-DIP-wide content area.
- Include these Korean strings in the UI fixture:
  - `연결 프로필 이름`
  - `장치를 구분할 수 있는 이름을 입력하세요.`
  - `사용 가능한 장치에 자동으로 다시 연결`
  - `연결 설정 저장`
- Preserve keyboard operation and native WinUI visual states.
- Implement the page in XAML with the smallest necessary C# or ViewModel support.
