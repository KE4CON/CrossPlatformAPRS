namespace Aprs.Services;

public enum AprsPacketSource
{
    Unknown,
    AprsIs,
    Rf,
    Replay,
    Simulation
}

public sealed record StationSnapshot(
    string Callsign,
    int? Ssid,
    string DisplayName,
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
