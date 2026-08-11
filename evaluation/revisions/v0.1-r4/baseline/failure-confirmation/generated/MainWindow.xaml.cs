using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private Control? _focusBeforeDialog;

    public MainWindow()
    {
        InitializeComponent();
    }

    private void RetryButton_Click(object sender, RoutedEventArgs e)
    {
        ConnectionErrorInfoBar.IsOpen = true;
        RetryButton.Focus(FocusState.Programmatic);
    }

    private async void RemoveDeviceButton_Click(object sender, RoutedEventArgs e)
    {
        _focusBeforeDialog = FocusManager.GetFocusedElement(Content.XamlRoot) as Control;
        RemoveDeviceDialog.XamlRoot = Content.XamlRoot;

        await RemoveDeviceDialog.ShowAsync();

        _focusBeforeDialog?.Focus(FocusState.Programmatic);
        _focusBeforeDialog = null;
    }
}
