namespace Aprs.Services;

public sealed record AprsMessageRecord(
    Guid Id,
    string? MessageId,
    string LocalStationCallsign,
    string RemoteStationCallsign,
    string Addressee,
    string Sender,
    string Recipient,
    string MessageBody,
    string? RawPacket,
    AprsMessageDirection Direction,
    AprsMessageStatus Status,
    DateTimeOffset CreatedAtUtc,
    DateTimeOffset? SentAtUtc,
    DateTimeOffset? ReceivedAtUtc,
    DateTimeOffset LastUpdatedAtUtc,
    AprsPacketSource Source,
    AprsMessageKind Kind,
    IReadOnlyList<string> ValidationErrors);
