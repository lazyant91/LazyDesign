using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    private int _newDeviceNumber = 1;

    public ObservableCollection<DeviceViewModel> Devices { get; } =
        new()
        {
            new DeviceViewModel
            {
                Name = "회의실 디스플레이 무선 프레젠테이션 수신 장치",
                ConnectionType = "Wi-Fi",
                Status = "Connected",
            },
            new DeviceViewModel
            {
                Name = "Portable conference-room presentation receiver",
                ConnectionType = "USB-C",
                Status = "Available",
            },
        };

    public MainWindow()
    {
        InitializeComponent();
        DeviceList.SelectedIndex = 0;
        UpdateDeviceState();
    }

    private void RefreshButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateDeviceState();
    }

    private void AddDeviceButton_Click(object sender, RoutedEventArgs e)
    {
        var device = new DeviceViewModel
        {
            Name = $"New device {_newDeviceNumber++}",
            ConnectionType = "Wi-Fi",
            Status = "Available",
        };

        Devices.Add(device);
        DeviceList.SelectedItem = device;
        DeviceList.ScrollIntoView(device);
        UpdateDeviceState();
    }

    private void RemoveDeviceButton_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceList.SelectedItem is not DeviceViewModel selectedDevice)
        {
            return;
        }

        Devices.Remove(selectedDevice);
        UpdateDeviceState();
    }

    private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        UpdateDeviceState();
    }

    private void UpdateDeviceState()
    {
        var hasDevices = Devices.Count > 0;
        DeviceList.Visibility = hasDevices ? Visibility.Visible : Visibility.Collapsed;
        EmptyState.Visibility = hasDevices ? Visibility.Collapsed : Visibility.Visible;
        RemoveDeviceButton.IsEnabled = DeviceList.SelectedItem is DeviceViewModel;
    }
}

public sealed class DeviceViewModel
{
    public string Name { get; set; } = string.Empty;

    public string ConnectionType { get; set; } = string.Empty;

    public string Status { get; set; } = string.Empty;
}
