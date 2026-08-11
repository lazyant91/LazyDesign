using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private int _nextDeviceNumber = 1;

    public ObservableCollection<DeviceViewModel> Devices { get; } = new();

    public MainWindow()
    {
        InitializeComponent();
        SeedDevices();
        UpdateCollectionState();
    }

    private void SeedDevices()
    {
        Devices.Add(new DeviceViewModel
        {
            Name = "회의실 디스플레이 무선 프레젠테이션 수신 장치",
            ConnectionType = "Wi-Fi Direct",
            Status = "Connected",
        });

        Devices.Add(new DeviceViewModel
        {
            Name = "Portable conference-room presentation receiver",
            ConnectionType = "USB-C",
            Status = "Available",
        });
    }

    private void RefreshDevices_Click(object sender, RoutedEventArgs e)
    {
        UpdateCollectionState();
    }

    private void AddDevice_Click(object sender, RoutedEventArgs e)
    {
        var device = new DeviceViewModel
        {
            Name = $"New device {_nextDeviceNumber++}",
            ConnectionType = "Wi-Fi",
            Status = "Available",
        };

        Devices.Add(device);
        DeviceList.SelectedItem = device;
        DeviceList.ScrollIntoView(device);
        UpdateCollectionState();
    }

    private void RemoveDevice_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceList.SelectedItem is DeviceViewModel selectedDevice)
        {
            Devices.Remove(selectedDevice);
        }

        UpdateCollectionState();
    }

    private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        RemoveDeviceButton.IsEnabled = DeviceList.SelectedItem is not null;
    }

    private void UpdateCollectionState()
    {
        var hasDevices = Devices.Count > 0;
        DeviceList.Visibility = hasDevices ? Visibility.Visible : Visibility.Collapsed;
        EmptyState.Visibility = hasDevices ? Visibility.Collapsed : Visibility.Visible;
        RemoveDeviceButton.IsEnabled = hasDevices && DeviceList.SelectedItem is not null;
    }
}

public sealed class DeviceViewModel
{
    public string Name { get; set; } = string.Empty;
    public string ConnectionType { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
}
