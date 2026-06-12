namespace AprsCommand.Contracts;

public sealed record DtoSourceMetadata(
    string? SourceName = null,
    ContractSourceType SourceType = ContractSourceType.Unknown,
    string? SourceId = null,
    DateTimeOffset? Timestamp = null,
    ContractDataOrigin Origin = ContractDataOrigin.Unknown,
    ContractSourceTrustLevel TrustLevel = ContractSourceTrustLevel.Untrusted);
