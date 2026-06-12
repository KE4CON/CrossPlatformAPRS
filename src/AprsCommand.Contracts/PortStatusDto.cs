namespace AprsCommand.Contracts;

public sealed record PortStatusDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? PortId = null,
    string? PortName = null,
    string? PortType = null,
    string? ConnectionState = null,
    bool ReceiveEnabled = false,
    bool TransmitEnabled = false,
    int PacketCountReceived = 0,
    int PacketCountTransmitted = 0,
    DateTimeOffset? LastPacketReceivedUtc = null,
    string? LastError = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
