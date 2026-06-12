namespace AprsCommand.Contracts;

public sealed record AlertDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? AlertId = null,
    string? AlertType = null,
    string? Severity = null,
    string? Title = null,
    string? Message = null,
    DateTimeOffset? TriggeredUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
