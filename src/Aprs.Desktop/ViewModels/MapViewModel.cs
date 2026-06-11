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
    private ObjectMarkerViewModel? selectedObject;
    private ObjectManagerViewModel? objectManager;
    private readonly IMapCoordinateConverter coordinateConverter;

    public MapViewModel(IEnumerable<StationMarker> markers)
        : this(markers, MapTileCacheConfiguration.Default, CreateDefaultProvider(), new PlaceholderMapCoordinateConverter())
    {
    }

    public MapViewModel(
        IEnumerable<StationMarker> markers,
        MapTileCacheConfiguration tileCacheConfiguration,
        MapTileProviderDefinition tileProvider)
        : this(markers, tileCacheConfiguration, tileProvider, new PlaceholderMapCoordinateConverter())
    {
    }

    public MapViewModel(
        IEnumerable<StationMarker> markers,
        MapTileCacheConfiguration tileCacheConfiguration,
        MapTileProviderDefinition tileProvider,
        IMapCoordinateConverter coordinateConverter)
    {
        Markers = new ObservableCollection<StationMarkerViewModel>(
            markers.Select(marker => new StationMarkerViewModel(marker)));
        ObjectMarkers = [];
        TileCacheConfiguration = tileCacheConfiguration;
        TileProvider = tileProvider;
        this.coordinateConverter = coordinateConverter;
        BeginCreateObjectCommand = new DesktopCommand(BeginCreateObjectPlacement);
        ClearObjectSelectionCommand = new DesktopCommand(ClearObjectSelection);
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public ObservableCollection<StationMarkerViewModel> Markers { get; }

    public ObservableCollection<ObjectMarkerViewModel> ObjectMarkers { get; }

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

    public int ObjectMarkerCount => ObjectMarkers.Count;

    public int TotalMarkerCount => MarkerCount + ObjectMarkerCount;

    public bool IsCreateObjectMode { get; private set; }

    public string ObjectPlacementStatus { get; private set; } = "Object placement inactive.";

    public ObjectMarkerViewModel? SelectedObject
    {
        get => selectedObject;
        private set
        {
            if (ReferenceEquals(selectedObject, value))
            {
                return;
            }

            selectedObject = value;
            OnPropertyChanged();
            OnPropertyChanged(nameof(HasSelectedObject));
        }
    }

    public bool HasSelectedObject => SelectedObject is not null;

    public DesktopCommand BeginCreateObjectCommand { get; }

    public DesktopCommand ClearObjectSelectionCommand { get; }

    public void SelectStation(StationMarkerViewModel marker)
    {
        if (Markers.Contains(marker))
        {
            SelectedStation = marker;
            SelectedObject = null;
        }
    }

    public void AttachObjectManager(ObjectManagerViewModel manager)
    {
        objectManager = manager;
        RefreshObjectMarkers();
    }

    public void RefreshObjectMarkers()
    {
        ObjectMarkers.Clear();
        if (objectManager is not null)
        {
            foreach (var marker in objectManager.GetObjectStates()
                .Select(state => ObjectMarker.TryCreate(state, out var marker) ? marker : null)
                .OfType<ObjectMarker>())
            {
                ObjectMarkers.Add(new ObjectMarkerViewModel(marker));
            }
        }

        if (SelectedObject is not null && ObjectMarkers.FirstOrDefault(marker => string.Equals(marker.ObjectName, SelectedObject.ObjectName, StringComparison.OrdinalIgnoreCase)) is { } refreshed)
        {
            SelectedObject = refreshed;
        }

        OnPropertyChanged(nameof(ObjectMarkers));
        OnPropertyChanged(nameof(ObjectMarkerCount));
        OnPropertyChanged(nameof(TotalMarkerCount));
    }

    public void SelectObject(ObjectMarkerViewModel marker)
    {
        if (!ObjectMarkers.Contains(marker))
        {
            return;
        }

        SelectedStation = null;
        SelectedObject = marker;
        objectManager?.SelectObjectByName(marker.ObjectName);
        ObjectPlacementStatus = $"Selected object {marker.ObjectName}.";
        OnPropertyChanged(nameof(ObjectPlacementStatus));
    }

    public void ClearObjectSelection()
    {
        SelectedObject = null;
        ObjectPlacementStatus = "Object selection cleared.";
        OnPropertyChanged(nameof(ObjectPlacementStatus));
    }

    public void BeginCreateObjectPlacement()
    {
        IsCreateObjectMode = true;
        SelectedObject = null;
        ObjectPlacementStatus = "Click the map to place a new local object draft.";
        OnPropertyChanged(nameof(IsCreateObjectMode));
        OnPropertyChanged(nameof(ObjectPlacementStatus));
    }

    public bool HandleMapClick(double xPercent, double yPercent)
    {
        var coordinate = coordinateConverter.FromNormalizedPoint(xPercent, yPercent);
        if (IsCreateObjectMode)
        {
            return PlaceObjectAt(coordinate.Latitude, coordinate.Longitude);
        }

        if (SelectedObject is not null)
        {
            return MoveSelectedObjectTo(coordinate.Latitude, coordinate.Longitude);
        }

        ObjectPlacementStatus = $"Map coordinate {coordinate.Latitude:0.0000}, {coordinate.Longitude:0.0000}.";
        OnPropertyChanged(nameof(ObjectPlacementStatus));
        return false;
    }

    public bool PlaceObjectAt(double latitude, double longitude)
    {
        if (objectManager is null)
        {
            ObjectPlacementStatus = "Object editor is not connected.";
            OnPropertyChanged(nameof(ObjectPlacementStatus));
            return false;
        }

        objectManager.CreateObjectDraftAt(latitude, longitude);
        IsCreateObjectMode = false;
        ObjectPlacementStatus = $"Draft object coordinates set to {latitude:0.0000}, {longitude:0.0000}.";
        OnPropertyChanged(nameof(IsCreateObjectMode));
        OnPropertyChanged(nameof(ObjectPlacementStatus));
        return true;
    }

    public bool MoveSelectedObjectTo(double latitude, double longitude, bool adoptIfRemote = false)
    {
        if (objectManager is null || SelectedObject is null)
        {
            ObjectPlacementStatus = "Select an object before moving it.";
            OnPropertyChanged(nameof(ObjectPlacementStatus));
            return false;
        }

        var moved = objectManager.MoveObjectTo(SelectedObject.ObjectName, latitude, longitude, adoptIfRemote);
        ObjectPlacementStatus = moved
            ? $"Moved {SelectedObject.ObjectName} to {latitude:0.0000}, {longitude:0.0000}."
            : objectManager.StatusText;
        RefreshObjectMarkers();
        OnPropertyChanged(nameof(ObjectPlacementStatus));
        return moved;
    }

    public void ClearSelection()
    {
        SelectedStation = null;
        ClearObjectSelection();
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
