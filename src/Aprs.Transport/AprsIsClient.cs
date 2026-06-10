using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Channels;

namespace Aprs.Transport;

public sealed class AprsIsClient : IAprsIsClient
{
    private readonly AprsIsClientConfiguration configuration;
    private readonly Func<AprsIsClientConfiguration, CancellationToken, Task<Stream>> streamFactory;
    private readonly Channel<AprsIsRawPacketReceivedEventArgs> receivedPackets = Channel.CreateUnbounded<AprsIsRawPacketReceivedEventArgs>();
    private CancellationTokenSource? connectionCancellation;
    private Task? receiveTask;
    private Stream? stream;

    public AprsIsClient(AprsIsClientConfiguration configuration)
        : this(configuration, CreateTcpStreamAsync)
    {
    }

    public AprsIsClient(
        AprsIsClientConfiguration configuration,
        Func<AprsIsClientConfiguration, CancellationToken, Task<Stream>> streamFactory)
    {
        this.configuration = configuration;
        this.streamFactory = streamFactory;
    }

    public event EventHandler<AprsIsRawPacketReceivedEventArgs>? RawPacketReceived;

    public AprsIsConnectionState State { get; private set; } = AprsIsConnectionState.Disconnected;

    public Exception? LastError { get; private set; }

    public async Task ConnectAsync(CancellationToken cancellationToken)
    {
        if (State is AprsIsConnectionState.Connected or AprsIsConnectionState.Connecting)
        {
            return;
        }

        AprsIsLoginLineBuilder.Validate(configuration);
        connectionCancellation = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        LastError = null;
        State = AprsIsConnectionState.Connecting;

        try
        {
            stream = await streamFactory(configuration, connectionCancellation.Token).ConfigureAwait(false);
            await WriteLoginLineAsync(stream, connectionCancellation.Token).ConfigureAwait(false);
            State = AprsIsConnectionState.Connected;
            receiveTask = Task.Run(() => ReceiveLoopAsync(connectionCancellation.Token), CancellationToken.None);
        }
        catch (Exception exception) when (exception is not OperationCanceledException)
        {
            LastError = exception;
            State = AprsIsConnectionState.Faulted;
            throw;
        }
    }

    public async Task DisconnectAsync(CancellationToken cancellationToken)
    {
        connectionCancellation?.Cancel();

        if (stream is not null)
        {
            await stream.DisposeAsync().ConfigureAwait(false);
            stream = null;
        }

        if (receiveTask is not null)
        {
            try
            {
                await receiveTask.WaitAsync(cancellationToken).ConfigureAwait(false);
            }
            catch (OperationCanceledException)
            {
            }
            catch (ObjectDisposedException)
            {
            }
        }

        State = AprsIsConnectionState.Disconnected;
    }

    public async IAsyncEnumerable<AprsIsRawPacketReceivedEventArgs> ReadPacketsAsync(
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        while (await receivedPackets.Reader.WaitToReadAsync(cancellationToken).ConfigureAwait(false))
        {
            while (receivedPackets.Reader.TryRead(out var packet))
            {
                yield return packet;
            }
        }
    }

    public async ValueTask DisposeAsync()
    {
        await DisconnectAsync(CancellationToken.None).ConfigureAwait(false);
        connectionCancellation?.Dispose();
    }

    private async Task ReceiveLoopAsync(CancellationToken cancellationToken)
    {
        try
        {
            while (!cancellationToken.IsCancellationRequested && stream is not null)
            {
                using var reader = new StreamReader(stream, Encoding.ASCII, detectEncodingFromByteOrderMarks: false, leaveOpen: true);
                while (!cancellationToken.IsCancellationRequested)
                {
                    var line = await reader.ReadLineAsync(cancellationToken).ConfigureAwait(false);
                    if (line is null)
                    {
                        break;
                    }

                    if (line.StartsWith('#'))
                    {
                        continue;
                    }

                    PublishPacket(line);
                }

                if (!configuration.ReconnectEnabled || cancellationToken.IsCancellationRequested)
                {
                    State = AprsIsConnectionState.Disconnected;
                    break;
                }

                State = AprsIsConnectionState.Reconnecting;
                await Task.Delay(configuration.ReconnectDelay, cancellationToken).ConfigureAwait(false);
                stream = await streamFactory(configuration, cancellationToken).ConfigureAwait(false);
                await WriteLoginLineAsync(stream, cancellationToken).ConfigureAwait(false);
                State = AprsIsConnectionState.Connected;
            }
        }
        catch (Exception exception) when (exception is not OperationCanceledException and not ObjectDisposedException)
        {
            LastError = exception;
            State = AprsIsConnectionState.Faulted;
        }
    }

    private void PublishPacket(string line)
    {
        var packet = new AprsIsRawPacketReceivedEventArgs(line, DateTimeOffset.UtcNow);
        receivedPackets.Writer.TryWrite(packet);
        RawPacketReceived?.Invoke(this, packet);
    }

    private async Task WriteLoginLineAsync(Stream targetStream, CancellationToken cancellationToken)
    {
        var loginLine = AprsIsLoginLineBuilder.Build(configuration) + "\r\n";
        var bytes = Encoding.ASCII.GetBytes(loginLine);
        await targetStream.WriteAsync(bytes, cancellationToken).ConfigureAwait(false);
        await targetStream.FlushAsync(cancellationToken).ConfigureAwait(false);
    }

    private static async Task<Stream> CreateTcpStreamAsync(
        AprsIsClientConfiguration configuration,
        CancellationToken cancellationToken)
    {
        var tcpClient = new TcpClient();
        await tcpClient.ConnectAsync(configuration.ServerHost, configuration.ServerPort, cancellationToken).ConfigureAwait(false);

        return tcpClient.GetStream();
    }
}
