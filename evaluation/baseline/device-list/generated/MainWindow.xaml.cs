using System.Collections.ObjectModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

namespace LazyDesign.Evaluation;

public sealed partial class MainWindow : Window
{
    public ObservableCollection<DeviceItem> Devices { get; } = new();
    private int _newDeviceNumber = 1;

    public MainWindow()
    {
        InitializeComponent();
        LoadFixture();
        UpdateView();
    }

    private void LoadFixture()
    {
        Devices.Clear();
        Devices.Add(new DeviceItem("회의실 디스플레이 무선 프레젠테이션 수신 장치", "Wi-Fi", "Connected"));
        Devices.Add(new DeviceItem("Portable conference-room presentation receiver", "USB-C", "Available"));
    }

    private void Refresh_Click(object sender, RoutedEventArgs e) { LoadFixture(); DeviceList.SelectedItem = null; UpdateView(); }
    private void AddDevice_Click(object sender, RoutedEventArgs e)
    {
        var device = new DeviceItem($"New device {_newDeviceNumber++}", "Wi-Fi", "Available");
        Devices.Add(device); DeviceList.SelectedItem = device; DeviceList.ScrollIntoView(device); DeviceList.Focus(FocusState.Programmatic); UpdateView();
    }
    private void Remove_Click(object sender, RoutedEventArgs e)
    {
        if (DeviceList.SelectedItem is DeviceItem selected) Devices.Remove(selected);
        UpdateView();
    }
    private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e) => UpdateView();
    private void UpdateView()
    {
        bool hasDevices = Devices.Count > 0;
        ContentGrid.Visibility = hasDevices ? Visibility.Visible : Visibility.Collapsed;
        EmptyState.Visibility = hasDevices ? Visibility.Collapsed : Visibility.Visible;
        RemoveButton.IsEnabled = DeviceList.SelectedItem is DeviceItem;
    }
}

public sealed record DeviceItem(string Name, string ConnectionType, string Status);