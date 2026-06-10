using Aprs.Services;

namespace Aprs.Mapping;

public sealed record StationMarker(
    string Callsign,
    string DisplayName,
    double Latitude,
    double Longitude,
    char? SymbolTableIdentifier,
    char? SymbolCode,
    DateTimeOffset LastHeardUtc,
    StationLifecycleState AgeState,
    AprsPacketSource PacketSource,
    int? CourseDegrees,
    int? SpeedKnots)
{
    public static bool TryCreate(StationSnapshot station, out StationMarker? marker)
    {
        if (station.Latitude is null || station.Longitude is null)
        {
            marker = null;
            return false;
        }

        marker = new StationMarker(
            station.RealCallsign,
            station.DisplayName,
            station.Latitude.Value,
            station.Longitude.Value,
            station.SymbolTableIdentifier,
            station.SymbolCode,
            station.LastHeardUtc,
            station.LifecycleState,
            station.PacketSource,
            station.CourseDegrees,
            station.SpeedKnots);

        return true;
    }
}
