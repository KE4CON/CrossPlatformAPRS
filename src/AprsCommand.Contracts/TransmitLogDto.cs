namespace AprsCommand.Contracts;

public sealed record TransmitLogDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? RawPacketText = null,
    string? DestinationTransport = null,
    bool Success = false,
    string? FailureReason = null,
    string? ConnectedState = null,
    DateTimeOffset? TimestampUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
