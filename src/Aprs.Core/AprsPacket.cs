namespace Aprs.Core;

public abstract record AprsPacket(
    string RawLine,
    string SourceCallsign,
    int? SourceSsid,
    string Destination,
    IReadOnlyList<string> Path,
    string Information,
    DateTimeOffset ReceivedAtUtc,
    bool IsValid,
    IReadOnlyList<string> ValidationErrors);

public sealed record RawAprsPacket(
    string RawLine,
    string SourceCallsign,
    int? SourceSsid,
    string Destination,
    IReadOnlyList<string> Path,
    string Information,
    DateTimeOffset ReceivedAtUtc,
    bool IsValid,
    IReadOnlyList<string> ValidationErrors,
    string? QConstruct)
    : AprsPacket(
        RawLine,
        SourceCallsign,
        SourceSsid,
        Destination,
        Path,
        Information,
        ReceivedAtUtc,
        IsValid,
        ValidationErrors);
