using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private void RetryButton_Click(object sender, RoutedEventArgs e)
    {
        ConnectionFailureInfoBar.IsOpen = true;
    }

    private async void RemoveDeviceButton_Click(object sender, RoutedEventArgs e)
    {
        RemoveDeviceDialog.XamlRoot = RootGrid.XamlRoot;
        await RemoveDeviceDialog.ShowAsync();
    }

    private void RemoveDeviceDialog_Closed(ContentDialog sender, ContentDialogClosedEventArgs args)
    {
        RemoveDeviceButton.Focus(FocusState.Programmatic);
    }
}
