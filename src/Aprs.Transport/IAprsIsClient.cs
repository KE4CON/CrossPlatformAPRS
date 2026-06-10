namespace Aprs.Transport;

public interface IAprsIsClient : IAsyncDisposable
{
    event EventHandler<AprsIsRawPacketReceivedEventArgs>? RawPacketReceived;

    AprsIsConnectionState State { get; }

    Exception? LastError { get; }

    Task ConnectAsync(CancellationToken cancellationToken);

    Task DisconnectAsync(CancellationToken cancellationToken);

    IAsyncEnumerable<AprsIsRawPacketReceivedEventArgs> ReadPacketsAsync(CancellationToken cancellationToken);
}
