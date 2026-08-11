using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Automation;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private const string ConnectionNameHelpText = "장치를 구분할 수 있는 이름을 입력하세요.";
    private const string ConnectionNameValidationText = "연결 프로필 이름을 입력하세요.";
    private bool _showNameValidation;

    public MainWindow()
    {
        InitializeComponent();
        AutomationProperties.SetHelpText(ConnectionNameTextBox, ConnectionNameHelpText);
    }

    private void ConnectionNameTextBox_TextChanged(object sender, TextChangedEventArgs e)
    {
        if (_showNameValidation)
        {
            UpdateConnectionNameValidation();
        }
    }

    private void SaveButton_Click(object sender, RoutedEventArgs e)
    {
        _showNameValidation = true;

        if (!UpdateConnectionNameValidation())
        {
            ConnectionNameTextBox.Focus(FocusState.Programmatic);
            return;
        }

        _showNameValidation = false;
    }

    private bool UpdateConnectionNameValidation()
    {
        bool isValid = !string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text);

        NameValidationText.Visibility = isValid ? Visibility.Collapsed : Visibility.Visible;
        AutomationProperties.SetHelpText(
            ConnectionNameTextBox,
            isValid ? ConnectionNameHelpText : ConnectionNameValidationText);

        return isValid;
    }
}
