using System;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private bool _isRemoveDialogOpen;

    public MainWindow()
    {
        InitializeComponent();
    }

    private void RetryConnection_Click(object sender, RoutedEventArgs e)
    {
        ConnectionErrorInfoBar.Title = "거실 디스플레이에 다시 연결하는 중입니다.";
        ConnectionErrorInfoBar.Message = "연결을 다시 시도하고 있습니다.";
        ConnectionErrorInfoBar.Severity = InfoBarSeverity.Informational;
        ConnectionErrorInfoBar.IsClosable = false;
        RetryButton.IsEnabled = false;
    }

    private async void RemoveDeviceButton_Click(object sender, RoutedEventArgs e)
    {
        if (_isRemoveDialogOpen)
        {
            return;
        }

        _isRemoveDialogOpen = true;

        try
        {
            RemoveDeviceDialog.XamlRoot = RootGrid.XamlRoot;
            await RemoveDeviceDialog.ShowAsync();
        }
        finally
        {
            _isRemoveDialogOpen = false;
            RemoveDeviceButton.Focus(FocusState.Programmatic);
        }
    }
}
