using Aprs.Core;

namespace Aprs.Services;

/// <summary>
/// Maintains latest-known APRS station state from parsed packets.
/// </summary>
public interface IStationDatabase
{
    /// <summary>
    /// Applies a parsed APRS packet to the station database.
    /// </summary>
    void ProcessPacket(AprsPacket packet, AprsPacketSource packetSource = AprsPacketSource.Unknown);

    /// <summary>
    /// Returns all known stations.
    /// </summary>
    IReadOnlyCollection<StationSnapshot> GetAllStations();

    /// <summary>
    /// Returns one station by callsign or callsign-SSID.
    /// </summary>
    StationSnapshot? GetStation(string callsign);

    /// <summary>
    /// Removes all station state.
    /// </summary>
    void Clear();
}
