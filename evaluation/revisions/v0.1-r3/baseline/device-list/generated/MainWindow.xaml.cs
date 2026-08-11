using System;
using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private readonly ObservableCollection<DeviceInfo> _devices = new()
    {
        new("회의실 디스플레이 무선 프레젠테이션 수신 장치", "Wi-Fi", "Connected"),
        new("Portable conference-room presentation receiver", "USB-C", "Available"),
        new("Studio speaker", "Bluetooth", "Offline")
    };

    private int _nextDeviceNumber = 1;

    public MainWindow()
    {
        InitializeComponent();
        DeviceListView.ItemsSource = _devices;
        UpdateUiState();
    }

    private void RefreshButton_Click(object sender, RoutedEventArgs e) =>
        LastUpdatedText.Text = $"Refreshed {DateTime.Now:t}";

    private void AddButton_Click(object sender, RoutedEventArgs e)
    {
        var device = new DeviceInfo($"New device {_nextDeviceNumber++}", "Bluetooth", "Available");
        _devices.Add(device);
        DeviceListView.SelectedItem = device;
        DeviceListView.ScrollIntoView(device);
        UpdateUiState();
    }

    private void RemoveButton_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceListView.SelectedItem is DeviceInfo selected)
            _devices.Remove(selected);
        UpdateUiState();
    }

    private void DeviceListView_SelectionChanged(object sender, SelectionChangedEventArgs e) => UpdateUiState();

    private void UpdateUiState()
    {
        var hasDevices = _devices.Count > 0;
        var hasSelection = DeviceListView.SelectedItem is not null;
        DeviceListView.Visibility = hasDevices ? Visibility.Visible : Visibility.Collapsed;
        EmptyStatePanel.Visibility = hasDevices ? Visibility.Collapsed : Visibility.Visible;
        RemoveButton.IsEnabled = hasSelection;
        SummaryText.Text = hasDevices
            ? hasSelection ? $"{_devices.Count} devices • 1 selected" : $"{_devices.Count} devices • Select a device to remove it"
            : "0 devices";
    }
}

public sealed record DeviceInfo(string Name, string ConnectionType, string Status);
