using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public ObservableCollection<DeviceItem> Devices { get; } = new()
    {
        new DeviceItem { Name = "회의실 디스플레이 무선 프레젠테이션 수신 장치", ConnectionType = "Wi-Fi", Status = "Connected" },
        new DeviceItem { Name = "Portable conference-room presentation receiver", ConnectionType = "USB-C", Status = "Ready" },
    };

    private int _newDeviceNumber = 1;

    public MainWindow()
    {
        InitializeComponent();
        UpdateEmptyState();
    }

    private void Refresh_Click(object sender, RoutedEventArgs e) => DeviceList.UpdateLayout();

    private void AddDevice_Click(object sender, RoutedEventArgs e)
    {
        var device = new DeviceItem { Name = "Presentation receiver " + _newDeviceNumber++, ConnectionType = "Bluetooth", Status = "Ready" };
        Devices.Add(device);
        UpdateEmptyState();
        DeviceList.SelectedItem = device;
        DeviceList.ScrollIntoView(device);
    }

    private void Remove_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceList.SelectedItem is DeviceItem device) Devices.Remove(device);
        UpdateEmptyState();
    }

    private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e) => RemoveButton.IsEnabled = DeviceList.SelectedItem is DeviceItem;

    private void UpdateEmptyState()
    {
        bool isEmpty = Devices.Count == 0;
        DeviceList.Visibility = isEmpty ? Visibility.Collapsed : Visibility.Visible;
        EmptyState.Visibility = isEmpty ? Visibility.Visible : Visibility.Collapsed;
        if (isEmpty) RemoveButton.IsEnabled = false;
    }
}

public sealed class DeviceItem
{
    public string Name { get; set; } = string.Empty;
    public string ConnectionType { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
}
