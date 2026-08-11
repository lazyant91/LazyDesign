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
        NameValidationInfoBar.IsOpen = string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text);
    }

    private void SaveSettingsButton_Click(object sender, RoutedEventArgs e)
    {
        bool nameIsEmpty = string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text);
        NameValidationInfoBar.IsOpen = nameIsEmpty;

        if (nameIsEmpty)
        {
            ConnectionNameTextBox.Focus(FocusState.Programmatic);
        }
    }
}
