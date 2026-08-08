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
        if (ConnectionNameError is null)
        {
            return;
        }

        ConnectionNameError.Visibility = string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text)
            ? Visibility.Visible
            : Visibility.Collapsed;
    }

    private void SaveButton_Click(object sender, RoutedEventArgs e)
    {
        if (!string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text))
        {
            return;
        }

        ConnectionNameError.Visibility = Visibility.Visible;
        ConnectionNameTextBox.Focus(FocusState.Programmatic);
    }
}
