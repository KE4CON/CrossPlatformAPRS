using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Aprs.Mapping;
using Aprs.Services;

namespace Aprs.Desktop.ViewModels;

public sealed class MapViewModel : INotifyPropertyChanged
{
    private StationMarkerViewModel? selectedStation;
    private StationDetailsViewModel? selectedStationDetails;

    public MapViewModel(IEnumerable<StationMarker> markers)
        : this(markers, MapTileCacheConfiguration.Default, CreateDefaultProvider())
    {
    }

    public MapViewModel(
        IEnumerable<StationMarker> markers,
        MapTileCacheConfiguration tileCacheConfiguration,
        MapTileProviderDefinition tileProvider)
    {
        Markers = new ObservableCollection<StationMarkerViewModel>(
            markers.Select(marker => new StationMarkerViewModel(marker)));
        TileCacheConfiguration = tileCacheConfiguration;
        TileProvider = tileProvider;
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public ObservableCollection<StationMarkerViewModel> Markers { get; }

    public MapTileCacheConfiguration TileCacheConfiguration { get; }

    public MapTileProviderDefinition TileProvider { get; }

    public bool TileCacheEnabled => TileCacheConfiguration.CacheEnabled;

    public bool InternetTileDownloadAllowed => TileCacheConfiguration.AllowInternetTileDownload && TileProvider.InternetDownloadAllowed;

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
            selectedStationDetails = value is null
                ? null
                : new StationDetailsViewModel(value, DateTimeOffset.UtcNow);
            OnPropertyChanged();
            OnPropertyChanged(nameof(SelectedStationDetails));
            OnPropertyChanged(nameof(HasSelectedStation));
        }
    }

    public StationDetailsViewModel? SelectedStationDetails => selectedStationDetails;

    public bool HasSelectedStation => selectedStationDetails is not null;

    public int MarkerCount => Markers.Count;

    public void SelectStation(StationMarkerViewModel marker)
    {
        if (Markers.Contains(marker))
        {
            SelectedStation = marker;
        }
    }

    public void ClearSelection()
    {
        SelectedStation = null;
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
            StationMarker.Create(
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
                SpeedKnots: null,
                altitudeFeet: 820,
                lastPath: ["TCPIP*"],
                comment: "Net control station online",
                lastRawPacket: "N0CALL>APRS,TCPIP*:!3903.50N/08430.50W-Net control station online",
                packetCount: 4),
            StationMarker.Create(
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
                SpeedKnots: 45,
                altitudeFeet: 510,
                lastPath: ["WIDE1-1", "WIDE2-1"],
                comment: "Mobile test",
                lastRawPacket: "W1AW-9>APRS,WIDE1-1,WIDE2-1:=4123.45N/07234.56W>Mobile test",
                packetCount: 2),
            StationMarker.Create(
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
                SpeedKnots: null,
                altitudeFeet: null,
                lastPath: ["TCPIP*"],
                comment: "Weather station",
                lastRawPacket: "WX9XYZ>APRS:!3903.50N/08430.50W_180/005g010t072r000p000P000h50b10132",
                packetCount: 7)
        ]);
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private static MapTileProviderDefinition CreateDefaultProvider()
    {
        return new MapTileProviderDefinition(
            Name: "SampleGrid",
            UrlTemplate: string.Empty,
            MinimumZoom: 0,
            MaximumZoom: 18,
            AttributionText: "Placeholder grid, no external map tiles loaded.",
            SupportsOfflineCaching: true,
            InternetDownloadAllowed: false);
    }
}
