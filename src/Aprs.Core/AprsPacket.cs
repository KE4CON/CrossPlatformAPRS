namespace Aprs.Core;

public abstract record AprsPacket(
    string SourceCallsign,
    string Destination,
    IReadOnlyList<string> Path,
    string Information,
    DateTimeOffset ReceivedAtUtc);

public sealed record RawAprsPacket(
    string RawLine,
    string SourceCallsign,
    string Destination,
    IReadOnlyList<string> Path,
    string Information,
    DateTimeOffset ReceivedAtUtc)
    : AprsPacket(SourceCallsign, Destination, Path, Information, ReceivedAtUtc);
