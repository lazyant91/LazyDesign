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
        ConnectionFailureInfoBar.IsOpen = false;
        RemoveDeviceButton.Focus(FocusState.Programmatic);
    }

    private async void RemoveDeviceButton_Click(object sender, RoutedEventArgs e)
    {
        RemoveDeviceDialog.XamlRoot = RootGrid.XamlRoot;
        ContentDialogResult result = await RemoveDeviceDialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            RemovalStatusText.Text = "거실 TV 장치 제거를 확인했습니다.";
            RemovalStatusText.Visibility = Visibility.Visible;
        }

        RemoveDeviceButton.Focus(FocusState.Programmatic);
    }
}
