namespace AprsCommand.Contracts;

public sealed record AprsObjectDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? Name = null,
    string? ObjectType = null,
    string? OwnerCallsign = null,
    bool IsAlive = true,
    double? Latitude = null,
    double? Longitude = null,
    string? SymbolTable = null,
    string? SymbolCode = null,
    string? Comment = null,
    DateTimeOffset? LastHeardUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
