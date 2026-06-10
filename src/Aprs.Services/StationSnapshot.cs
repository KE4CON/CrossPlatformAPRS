namespace Aprs.Services;

public sealed record StationSnapshot(
    string Callsign,
    double? Latitude,
    double? Longitude,
    string? Symbol,
    string? Comment,
    DateTimeOffset LastHeardUtc,
    string Source);
