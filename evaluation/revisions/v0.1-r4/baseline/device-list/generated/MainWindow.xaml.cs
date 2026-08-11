using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public ObservableCollection<DeviceItem> Devices { get; } =
    [
        new("회의실 디스플레이 무선 프레젠테이션 수신 장치", "Wi-Fi", "Connected"),
        new("Portable conference-room presentation receiver", "USB-C", "Available"),
        new("Studio projector", "Ethernet", "Offline")
    ];

    public MainWindow()
    {
        InitializeComponent();
        UpdateEmptyState();
    }

    private void RefreshButton_Click(object sender, RoutedEventArgs e)
    {
        DeviceList.ItemsSource = null;
        DeviceList.ItemsSource = Devices;
        UpdateEmptyState();
    }

    private void AddButton_Click(object sender, RoutedEventArgs e)
    {
        var device = new DeviceItem("New presentation device", "Wi-Fi", "Available");
        Devices.Add(device);
        DeviceList.SelectedItem = device;
        DeviceList.ScrollIntoView(device);
        UpdateEmptyState();
    }

    private void RemoveButton_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceList.SelectedItem is DeviceItem device)
            Devices.Remove(device);
        UpdateEmptyState();
    }

    private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e) =>
        RemoveButton.IsEnabled = DeviceList.SelectedItem is not null;

    private void UpdateEmptyState() =>
        EmptyState.Visibility = Devices.Count == 0 ? Visibility.Visible : Visibility.Collapsed;
}

public sealed record DeviceItem(string Name, string ConnectionType, string Status);
