namespace Aprs.Services;

public enum AprsPacketSource
{
    Unknown,
    AprsIs,
    Rf,
    Replay,
    Simulation
}

public enum StationLifecycleState
{
    Active,
    Stale,
    Expired,
    Hidden
}

public sealed record StationSnapshot(
    string Callsign,
    int? Ssid,
    string DisplayName,
    StationLifecycleState LifecycleState,
    bool IsManuallyHidden,
    double? Latitude,
    double? Longitude,
    char? SymbolTableIdentifier,
    char? SymbolCode,
    string? Comment,
    DateTimeOffset LastHeardUtc,
    DateTimeOffset LastPacketUtc,
    string? LastRawPacket,
    string? LastPacketType,
    int? CourseDegrees,
    int? SpeedKnots,
    int? AltitudeFeet,
    int PacketCount,
    IReadOnlyList<string> SourcePath,
    AprsPacketSource PacketSource,
    bool? HasMessagingCapability,
    StationWeatherSnapshot? Weather);

public sealed record StationWeatherSnapshot(
    int? WindDirectionDegrees,
    int? WindSpeedMph,
    int? WindGustMph,
    int? TemperatureFahrenheit,
    int? RainLastHourHundredthsInch,
    int? RainLast24HoursHundredthsInch,
    int? RainSinceMidnightHundredthsInch,
    int? HumidityPercent,
    double? BarometricPressureMillibars,
    int? LuminosityWattsPerSquareMeter,
    int? SnowHundredthsInch,
    string RawWeatherBody,
    string? Comment);

public sealed record StationAgingConfiguration(
    TimeSpan ActiveThreshold,
    TimeSpan StaleThreshold,
    TimeSpan ExpiredThreshold,
    TimeSpan HiddenThreshold,
    bool ShowExpiredStations,
    bool IncludeHiddenStationsInNormalLists)
{
    public static StationAgingConfiguration Default { get; } = new(
        TimeSpan.FromMinutes(30),
        TimeSpan.FromHours(2),
        TimeSpan.FromHours(2),
        TimeSpan.FromHours(24),
        ShowExpiredStations: true,
        IncludeHiddenStationsInNormalLists: false);
}
