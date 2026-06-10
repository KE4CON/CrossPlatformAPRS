namespace Aprs.Core;

public interface IAprsParser
{
    bool TryParse(string rawLine, DateTimeOffset receivedAtUtc, out AprsPacket? packet, out string? error);
}
