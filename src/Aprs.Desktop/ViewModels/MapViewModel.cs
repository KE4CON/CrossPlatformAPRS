using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Aprs.Mapping;
using Aprs.Services;

namespace Aprs.Desktop.ViewModels;

public sealed class MapViewModel : INotifyPropertyChanged
{
    private StationMarkerViewModel? selectedStation;

    public MapViewModel(IEnumerable<StationMarker> markers)
    {
        Markers = new ObservableCollection<StationMarkerViewModel>(
            markers.Select(marker => new StationMarkerViewModel(marker)));
        selectedStation = Markers.FirstOrDefault();
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public ObservableCollection<StationMarkerViewModel> Markers { get; }

    public StationMarkerViewModel? SelectedStation
    {
        get => selectedStation;
        private set
        {
            if (ReferenceEquals(selectedStation, value))
            {
                return;
            }

            selectedStation = value;
            OnPropertyChanged();
        }
    }

    public int MarkerCount => Markers.Count;

    public void SelectStation(StationMarkerViewModel marker)
    {
        if (Markers.Contains(marker))
        {
            SelectedStation = marker;
        }
    }

    public static MapViewModel FromStations(IEnumerable<StationSnapshot> stations)
    {
        var markers = stations
            .Select(station => StationMarker.TryCreate(station, out var marker) ? marker : null)
            .OfType<StationMarker>();

        return new MapViewModel(markers);
    }

    public static MapViewModel CreateDesignTime()
    {
        var now = DateTimeOffset.UtcNow;
        return new MapViewModel(
        [
            new StationMarker(
                "N0CALL",
                "Net Control",
                39.0583,
                -84.5083,
                '/',
                '-',
                now.AddMinutes(-8),
                StationLifecycleState.Active,
                AprsPacketSource.Simulation,
                CourseDegrees: null,
                SpeedKnots: null),
            new StationMarker(
                "W1AW-9",
                "W1AW-9",
                41.3908,
                -72.6819,
                '/',
                '>',
                now.AddMinutes(-22),
                StationLifecycleState.Active,
                AprsPacketSource.Simulation,
                CourseDegrees: 123,
                SpeedKnots: 45),
            new StationMarker(
                "WX9XYZ",
                "Weather WX9XYZ",
                38.6270,
                -90.1994,
                '/',
                '_',
                now.AddMinutes(-74),
                StationLifecycleState.Stale,
                AprsPacketSource.Simulation,
                CourseDegrees: null,
                SpeedKnots: null)
        ]);
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
