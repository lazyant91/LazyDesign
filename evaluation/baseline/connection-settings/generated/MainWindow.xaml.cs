using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        UpdateNameValidation();
    }

    private void ConnectionNameTextBox_TextChanged(object sender, TextChangedEventArgs e)
    {
        UpdateNameValidation();
    }

    private void SaveButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateNameValidation();
        if (string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text))
        {
            ConnectionNameTextBox.Focus(FocusState.Programmatic);
        }
    }

    private void UpdateNameValidation()
    {
        NameValidationText.Visibility = string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text)
            ? Visibility.Visible
            : Visibility.Collapsed;
    }
}