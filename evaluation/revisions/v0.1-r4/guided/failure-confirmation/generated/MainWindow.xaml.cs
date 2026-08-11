using System;
using Microsoft.UI.Xaml;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private void RetryConnection_Click(object sender, RoutedEventArgs e)
    {
        ConnectionErrorInfoBar.IsOpen = true;
    }

    private async void RemoveDeviceButton_Click(object sender, RoutedEventArgs e)
    {
        RemoveDeviceDialog.XamlRoot = Content.XamlRoot;
        await RemoveDeviceDialog.ShowAsync();
    }
}
