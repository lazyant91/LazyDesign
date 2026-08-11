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
            SaveStatusTextBlock.Visibility = Visibility.Collapsed;
            ConnectionNameTextBox.Focus(FocusState.Programmatic);
            return;
        }

        SaveStatusTextBlock.Visibility = Visibility.Visible;
    }

    private void UpdateNameValidation()
    {
        bool isNameEmpty = string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text);
        NameValidationTextBlock.Visibility = isNameEmpty ? Visibility.Visible : Visibility.Collapsed;

        if (isNameEmpty)
        {
            SaveStatusTextBlock.Visibility = Visibility.Collapsed;
        }
    }
}