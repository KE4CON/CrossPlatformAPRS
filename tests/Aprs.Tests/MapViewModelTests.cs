using Aprs.Desktop.ViewModels;
using Aprs.Mapping;
using Aprs.Services;
using Xunit;

namespace Aprs.Tests;

public sealed class MapViewModelTests
{
    private static readonly DateTimeOffset TestNow = new(2026, 6, 10, 12, 0, 0, TimeSpan.Zero);

    [Fact]
    public void StationMarker_TryCreatePreservesCallsignAndDisplayName()
    {
        var station = CreateStation("KD8ABC-7", "Tactical 7", 39.1, -84.5);

        var created = StationMarker.TryCreate(station, out var marker);

        Assert.True(created);
        Assert.NotNull(marker);
        Assert.Equal("KD8ABC-7", marker.Callsign);
        Assert.Equal("Tactical 7", marker.DisplayName);
        Assert.Equal(39.1, marker.Latitude);
        Assert.Equal(-84.5, marker.Longitude);
        Assert.Equal("Car / mobile station", marker.SymbolDescription);
        Assert.Equal("car", marker.MarkerIconKey);
        Assert.Equal("C", marker.FallbackMarkerText);
    }

    [Fact]
    public void StationMarker_TryCreateRejectsStationWithoutPosition()
    {
        var station = CreateStation("KD8ABC-7", "KD8ABC-7", latitude: null, longitude: null);

        var created = StationMarker.TryCreate(station, out var marker);

        Assert.False(created);
        Assert.Null(marker);
    }

    [Fact]
    public void MapViewModel_CreateDesignTimeLoadsSampleMarkers()
    {
        var viewModel = MapViewModel.CreateDesignTime();

        Assert.True(viewModel.MarkerCount >= 3);
        Assert.NotNull(viewModel.SelectedStation);
        Assert.Contains(viewModel.Markers, marker => marker.Callsign == "N0CALL" && marker.DisplayName == "Net Control");
    }

    [Fact]
    public void MapViewModel_FromStationsLoadsPositionedStationsOnly()
    {
        var positioned = CreateStation("KD8ABC-7", "Tactical 7", 39.1, -84.5);
        var unpositioned = CreateStation("N0POS", "N0POS", latitude: null, longitude: null);

        var viewModel = MapViewModel.FromStations([positioned, unpositioned]);

        var marker = Assert.Single(viewModel.Markers);
        Assert.Equal("KD8ABC-7", marker.Callsign);
        Assert.Equal("Tactical 7", marker.DisplayName);
    }

    [Fact]
    public void SelectStation_UpdatesSelectedStation()
    {
        var viewModel = new MapViewModel(
        [
            CreateMarker("N0CALL", "Net Control", 39.0, -84.0),
            CreateMarker("W1AW-9", "Mobile 9", 41.0, -72.0)
        ]);

        var selected = viewModel.Markers.Single(marker => marker.Callsign == "W1AW-9");

        viewModel.SelectStation(selected);

        Assert.Same(selected, viewModel.SelectedStation);
    }

    [Fact]
    public void StationMarkerViewModel_ExposesMapCoordinatesWithinPercentRange()
    {
        var marker = new StationMarkerViewModel(CreateMarker("N0CALL", "Net Control", 39.0, -84.0));

        Assert.InRange(marker.MapLeftPercent, 0, 100);
        Assert.InRange(marker.MapTopPercent, 0, 100);
    }

    private static StationMarker CreateMarker(string callsign, string displayName, double latitude, double longitude)
    {
        return StationMarker.Create(
            callsign,
            displayName,
            latitude,
            longitude,
            '/',
            '>',
            TestNow,
            StationLifecycleState.Active,
            AprsPacketSource.Simulation,
            CourseDegrees: 180,
            SpeedKnots: 12);
    }

    private static StationSnapshot CreateStation(string callsign, string displayName, double? latitude, double? longitude)
    {
        return new StationSnapshot(
            Callsign: callsign.Split('-')[0],
            Ssid: callsign.Contains('-') ? 7 : null,
            RealCallsign: callsign,
            TacticalLabel: displayName == callsign ? null : displayName,
            DisplayName: displayName,
            LifecycleState: StationLifecycleState.Active,
            IsManuallyHidden: false,
            Latitude: latitude,
            Longitude: longitude,
            SymbolTableIdentifier: '/',
            SymbolCode: '>',
            Comment: "Test station",
            LastHeardUtc: TestNow,
            LastPacketUtc: TestNow,
            LastRawPacket: $"{callsign}>APRS:>Test",
            LastPacketType: "PositionAprsPacket",
            CourseDegrees: 180,
            SpeedKnots: 12,
            AltitudeFeet: 1234,
            PacketCount: 1,
            SourcePath: ["WIDE1-1"],
            PacketSource: AprsPacketSource.Simulation,
            HasMessagingCapability: true,
            Weather: null);
    }
}
