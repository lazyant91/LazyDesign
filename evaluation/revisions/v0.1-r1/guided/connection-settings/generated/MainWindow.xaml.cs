using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private bool AutomaticReconnectEnabled { get; set; }

    public MainWindow()
    {
        InitializeComponent();
    }

    private void ConnectionNameTextBox_TextChanged(object sender, TextChangedEventArgs e)
    {
        if (!string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text))
        {
            ConnectionNameError.Visibility = Visibility.Collapsed;
        }
    }

    private void ConnectionNameTextBox_LostFocus(object sender, RoutedEventArgs e)
    {
        UpdateNameValidation();
    }

    private void AutoReconnectToggle_Toggled(object sender, RoutedEventArgs e)
    {
        AutomaticReconnectEnabled = AutoReconnectToggle.IsOn;
    }

    private void SaveButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateNameValidation();
    }

    private void UpdateNameValidation()
    {
        ConnectionNameError.Visibility = string.IsNullOrWhiteSpace(ConnectionNameTextBox.Text)
            ? Visibility.Visible
            : Visibility.Collapsed;
    }
}
