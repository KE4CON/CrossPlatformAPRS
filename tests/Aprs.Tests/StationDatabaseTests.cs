using Aprs.Core;
using Aprs.Services;
using Xunit;

namespace Aprs.Tests;

public sealed class StationDatabaseTests
{
    private static readonly DateTimeOffset FirstHeardUtc = new(2026, 6, 10, 12, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset SecondHeardUtc = FirstHeardUtc.AddMinutes(5);

    [Fact]
    public void ProcessPacket_CreatesNewStation_FromPositionPacket()
    {
        var database = new StationDatabase();
        var packet = Parse("N0CALL>APRS,TCPIP*:!3903.50N/08430.50W-Test beacon", FirstHeardUtc);

        database.ProcessPacket(packet, AprsPacketSource.AprsIs);

        var station = database.GetStation("N0CALL");
        Assert.NotNull(station);
        Assert.Equal("N0CALL", station.Callsign);
        Assert.Null(station.Ssid);
        Assert.Equal("N0CALL", station.DisplayName);
        Assert.Equal(39.058333, station.Latitude!.Value, 6);
        Assert.Equal(-84.508333, station.Longitude!.Value, 6);
        Assert.Equal('/', station.SymbolTableIdentifier);
        Assert.Equal('-', station.SymbolCode);
        Assert.Equal("Test beacon", station.Comment);
        Assert.Equal(FirstHeardUtc, station.LastHeardUtc);
        Assert.Equal(FirstHeardUtc, station.LastPacketUtc);
        Assert.Equal("PositionAprsPacket", station.LastPacketType);
        Assert.Equal("N0CALL>APRS,TCPIP*:!3903.50N/08430.50W-Test beacon", station.LastRawPacket);
        Assert.Equal(1, station.PacketCount);
        Assert.Equal(new[] { "TCPIP*" }, station.SourcePath);
        Assert.Equal(AprsPacketSource.AprsIs, station.PacketSource);
    }

    [Fact]
    public void ProcessPacket_UpdatesExistingStation_AndPreservesPositionForStatus()
    {
        var database = new StationDatabase();
        database.ProcessPacket(Parse("N0CALL>APRS:!3903.50N/08430.50W-Test beacon", FirstHeardUtc));

        database.ProcessPacket(Parse("N0CALL>APRS:>Net control station online", SecondHeardUtc), AprsPacketSource.Rf);

        var station = database.GetStation("n0call");
        Assert.NotNull(station);
        Assert.Equal(39.058333, station.Latitude!.Value, 6);
        Assert.Equal(-84.508333, station.Longitude!.Value, 6);
        Assert.Equal("Net control station online", station.Comment);
        Assert.Equal(2, station.PacketCount);
        Assert.Equal(SecondHeardUtc, station.LastHeardUtc);
        Assert.Equal(SecondHeardUtc, station.LastPacketUtc);
        Assert.Equal("StatusAprsPacket", station.LastPacketType);
        Assert.Equal(AprsPacketSource.Rf, station.PacketSource);
    }

    [Fact]
    public void ProcessPacket_UpdatesCourseSpeedAltitude_FromLaterPosition()
    {
        var database = new StationDatabase();
        database.ProcessPacket(Parse("MOBILE-9>APRS:!3903.50N/08430.50W>Moving", FirstHeardUtc));

        database.ProcessPacket(Parse("MOBILE-9>APRS:!3904.50N/08431.50W>123/045/A=000789 Moving test", SecondHeardUtc));

        var station = database.GetStation("MOBILE-9");
        Assert.NotNull(station);
        Assert.Equal("MOBILE", station.Callsign);
        Assert.Equal(9, station.Ssid);
        Assert.Equal("MOBILE-9", station.DisplayName);
        Assert.Equal(39.075, station.Latitude!.Value, 6);
        Assert.Equal(-84.525, station.Longitude!.Value, 6);
        Assert.Equal(123, station.CourseDegrees);
        Assert.Equal(45, station.SpeedKnots);
        Assert.Equal(789, station.AltitudeFeet);
        Assert.Equal(2, station.PacketCount);
    }

    [Fact]
    public void ProcessPacket_MarksMessagingCapability_FromMessagePacket()
    {
        var database = new StationDatabase();

        database.ProcessPacket(Parse("K8ABC>APRS::N0CALL   :Hello there{01", FirstHeardUtc));

        var station = database.GetStation("K8ABC");
        Assert.NotNull(station);
        Assert.True(station.HasMessagingCapability);
        Assert.Equal("MessageAprsPacket", station.LastPacketType);
    }

    [Fact]
    public void ProcessPacket_CreatesObjectAndItemStations_WhenTheyHavePosition()
    {
        var database = new StationDatabase();

        database.ProcessPacket(Parse("OBJ1>APRS:;CHECKPNT1*111111z3903.50N/08430.50W-Checkpoint 1", FirstHeardUtc));
        database.ProcessPacket(Parse("ITEM1>APRS:)REPEATER!3903.50N/08430.50WrLocal repeater", SecondHeardUtc));

        var objectStation = database.GetStation("CHECKPNT1");
        var itemStation = database.GetStation("REPEATER");
        Assert.NotNull(objectStation);
        Assert.NotNull(itemStation);
        Assert.Equal("Checkpoint 1", objectStation.Comment);
        Assert.Equal("Local repeater", itemStation.Comment);
        Assert.Equal("ObjectAprsPacket", objectStation.LastPacketType);
        Assert.Equal("ItemAprsPacket", itemStation.LastPacketType);
    }

    [Fact]
    public void ProcessPacket_UpdatesWeatherStationState()
    {
        var database = new StationDatabase();

        database.ProcessPacket(Parse("WX9XYZ>APRS:!3903.50N/08430.50W_180/005g010t072r000p000P000h50b10132", FirstHeardUtc), AprsPacketSource.Simulation);

        var station = database.GetStation("WX9XYZ");
        Assert.NotNull(station);
        Assert.Equal(39.058333, station.Latitude!.Value, 6);
        Assert.Equal(-84.508333, station.Longitude!.Value, 6);
        Assert.NotNull(station.Weather);
        Assert.Equal(180, station.Weather.WindDirectionDegrees);
        Assert.Equal(5, station.Weather.WindSpeedMph);
        Assert.Equal(10, station.Weather.WindGustMph);
        Assert.Equal(72, station.Weather.TemperatureFahrenheit);
        Assert.Equal(1013.2, station.Weather.BarometricPressureMillibars);
        Assert.Equal(AprsPacketSource.Simulation, station.PacketSource);
    }

    [Fact]
    public void ProcessPacket_IgnoresMalformedPackets_WithoutCrashing()
    {
        var database = new StationDatabase();
        var malformedPacket = Parse("BADPOS>APRS:!9999.99N/99999.99W-Bad position", FirstHeardUtc);

        var exception = Record.Exception(() => database.ProcessPacket(malformedPacket));

        Assert.Null(exception);
        Assert.Empty(database.GetAllStations());
    }

    [Fact]
    public void Clear_RemovesAllStations()
    {
        var database = new StationDatabase();
        database.ProcessPacket(Parse("N0CALL>APRS:!3903.50N/08430.50W-Test beacon", FirstHeardUtc));

        database.Clear();

        Assert.Empty(database.GetAllStations());
        Assert.Null(database.GetStation("N0CALL"));
    }

    private static AprsPacket Parse(string rawLine, DateTimeOffset receivedAtUtc)
    {
        var parser = new AprsParser();
        parser.TryParse(rawLine, receivedAtUtc, out var packet, out _);

        return Assert.IsAssignableFrom<AprsPacket>(packet);
    }
}
