namespace Aprs.Transport;

public sealed record AprsIsClientConfiguration(
    string ServerHost,
    int ServerPort,
    string Callsign,
    string Passcode,
    string ApplicationName,
    string ApplicationVersion,
    string? Filter,
    bool ReconnectEnabled,
    TimeSpan ReconnectDelay,
    bool ReceiveOnly)
{
    public static AprsIsClientConfiguration Default { get; } = new(
        ServerHost: "rotate.aprs2.net",
        ServerPort: 14580,
        Callsign: string.Empty,
        Passcode: "-1",
        ApplicationName: "CrossPlatformAprs",
        ApplicationVersion: "0.1.0",
        Filter: null,
        ReconnectEnabled: true,
        ReconnectDelay: TimeSpan.FromSeconds(10),
        ReceiveOnly: true);

    public AprsIsClientConfiguration WithServer(AprsIsServerDefinition server)
    {
        ArgumentNullException.ThrowIfNull(server);

        return this with
        {
            ServerHost = server.HostName,
            ServerPort = server.Port
        };
    }
}
