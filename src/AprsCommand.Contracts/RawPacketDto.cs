namespace AprsCommand.Contracts;

public sealed record RawPacketDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? RawPacketText = null,
    string? PacketType = null,
    string? SourceCallsign = null,
    string? Destination = null,
    IReadOnlyList<string>? Path = null,
    string? Direction = null,
    DateTimeOffset? TimestampUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
