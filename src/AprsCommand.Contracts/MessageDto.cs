namespace AprsCommand.Contracts;

public sealed record MessageDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? MessageId = null,
    string? Sender = null,
    string? Recipient = null,
    string? Body = null,
    string? Direction = null,
    string? Status = null,
    DateTimeOffset? CreatedUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
