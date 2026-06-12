namespace AprsCommand.Contracts;

public sealed record StationUpdateDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? Callsign = null,
    string? DisplayName = null,
    double? Latitude = null,
    double? Longitude = null,
    string? SymbolTable = null,
    string? SymbolCode = null,
    DateTimeOffset? LastHeardUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
