using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed record Device(string Name, string ConnectionType, string Status);

public sealed partial class MainWindow : Window
{
    public ObservableCollection<Device> Devices { get; } = new()
    {
        new("회의실 디스플레이 무선 프레젠테이션 수신 장치", "Wi-Fi", "Connected"),
        new("Portable conference-room presentation receiver", "USB-C", "Available"),
        new("Desk speakerphone", "Bluetooth", "Disconnected")
    };

    public MainWindow()
    {
        InitializeComponent();
        UpdateEmptyState();
    }

    private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e) =>
        RemoveButton.IsEnabled = DeviceList.SelectedItem is Device;

    private void AddButton_Click(object sender, RoutedEventArgs e)
    {
        var device = new Device("New device", "Bluetooth", "Available");
        Devices.Add(device);
        UpdateEmptyState();
        DeviceList.SelectedItem = device;
    }

    private void RemoveButton_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceList.SelectedItem is Device device) Devices.Remove(device);
        UpdateEmptyState();
    }

    private void RefreshButton_Click(object sender, RoutedEventArgs e)
    {
        if (Devices.Count > 0 && DeviceList.SelectedItem is null) DeviceList.SelectedIndex = 0;
    }

    private void UpdateEmptyState()
    {
        bool empty = Devices.Count == 0;
        DeviceList.Visibility = empty ? Visibility.Collapsed : Visibility.Visible;
        EmptyState.Visibility = empty ? Visibility.Visible : Visibility.Collapsed;
        if (empty) RemoveButton.IsEnabled = false;
    }
}