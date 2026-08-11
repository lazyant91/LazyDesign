using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private void ConnectionNameTextBox_TextChanged(object sender, TextChangedEventArgs e)
    {
        ConnectionNameValidationText.Visibility = string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text)
            ? Visibility.Visible
            : Visibility.Collapsed;
    }

    private void SaveSettingsButton_Click(object sender, RoutedEventArgs e)
    {
        if (!string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text))
        {
            ConnectionNameValidationText.Visibility = Visibility.Collapsed;
            return;
        }

        ConnectionNameValidationText.Visibility = Visibility.Visible;
        ConnectionNameTextBox.Focus(FocusState.Programmatic);
    }
}
