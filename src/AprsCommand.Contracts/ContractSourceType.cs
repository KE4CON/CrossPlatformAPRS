namespace AprsCommand.Contracts;

public enum ContractSourceType
{
    Unknown,
    AprsIs,
    Rf,
    TcpKiss,
    SerialKiss,
    Direwolf,
    Agwpe,
    Replay,
    Simulation,
    Training,
    WeatherDriver,
    Gps,
    ManualEntry,
    FileImport,
    LocalApi,
    Plugin,
    LocalGenerated
}
