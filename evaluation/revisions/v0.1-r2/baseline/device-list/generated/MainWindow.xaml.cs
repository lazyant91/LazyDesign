using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private int _newDeviceNumber = 1;

    public ObservableCollection<DeviceItem> Devices { get; } = new()
    {
        new("회의실 디스플레이 무선 프레젠테이션 수신 장치", "Wi-Fi", "Connected"),
        new("Portable conference-room presentation receiver", "Ethernet", "Available"),
        new("Lobby signage player", "Bluetooth", "Disconnected")
    };

    public MainWindow()
    {
        InitializeComponent();
        Devices.CollectionChanged += (_, _) => UpdateEmptyState();
        UpdateEmptyState();
    }

    private void Refresh_Click(object sender, RoutedEventArgs e) => DeviceList.ItemsSource = Devices;

    private void AddDevice_Click(object sender, RoutedEventArgs e)
    {
        var device = new DeviceItem($"New device {_newDeviceNumber++}", "Wi-Fi", "Available");
        Devices.Add(device);
        DeviceList.SelectedItem = device;
        DeviceList.ScrollIntoView(device);
    }

    private void RemoveDevice_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceList.SelectedItem is DeviceItem device)
            Devices.Remove(device);
    }

    private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e) =>
        RemoveButton.IsEnabled = DeviceList.SelectedItem is not null;

    private void UpdateEmptyState()
    {
        var isEmpty = Devices.Count == 0;
        DeviceList.Visibility = isEmpty ? Visibility.Collapsed : Visibility.Visible;
        ColumnHeader.Visibility = isEmpty ? Visibility.Collapsed : Visibility.Visible;
        EmptyState.Visibility = isEmpty ? Visibility.Visible : Visibility.Collapsed;
        RemoveButton.IsEnabled = !isEmpty && DeviceList.SelectedItem is not null;
    }
}

public sealed class DeviceItem(string name, string connectionType, string status)
{
    public string Name { get; } = name;
    public string ConnectionType { get; } = connectionType;
    public string Status { get; } = status;
}
