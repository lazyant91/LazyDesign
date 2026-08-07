using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private async void RemoveSavedDevice_Click(object sender, RoutedEventArgs e)
    {
        var invoker = sender as Control;
        var dialog = (ContentDialog)RootGrid.Resources["RemoveDeviceDialog"];

        dialog.XamlRoot = RootGrid.XamlRoot;
        await dialog.ShowAsync();

        invoker?.Focus(FocusState.Programmatic);
    }
}
