using Aprs.Core;

namespace Aprs.Services;

public sealed class StationDatabase : IStationDatabase
{
    private readonly Dictionary<string, StationSnapshot> stations = new(StringComparer.OrdinalIgnoreCase);
    private readonly StationAgingConfiguration agingConfiguration;

    public StationDatabase()
        : this(StationAgingConfiguration.Default)
    {
    }

    public StationDatabase(StationAgingConfiguration agingConfiguration)
    {
        this.agingConfiguration = agingConfiguration;
    }

    public void ProcessPacket(AprsPacket packet, AprsPacketSource packetSource = AprsPacketSource.Unknown)
    {
        if (!packet.IsValid)
        {
            return;
        }

        var stationKey = GetStationKey(packet);
        if (string.IsNullOrWhiteSpace(stationKey))
        {
            return;
        }

        var existing = stations.GetValueOrDefault(stationKey);
        var updated = CreateBaseUpdate(stationKey, packet, packetSource, existing);
        updated = ApplyPacketSpecificFields(updated, packet);

        stations[stationKey] = updated;
    }

    public IReadOnlyCollection<StationSnapshot> GetAllStations()
    {
        return SortStations(stations.Values);
    }

    public IReadOnlyCollection<StationSnapshot> GetVisibleStations()
    {
        return SortStations(stations.Values.Where(IsVisible));
    }

    public IReadOnlyCollection<StationSnapshot> GetActiveStations()
    {
        return SortStations(stations.Values.Where(station => station.LifecycleState == StationLifecycleState.Active));
    }

    public StationSnapshot? GetStation(string callsign)
    {
        return stations.TryGetValue(NormalizeStationKey(callsign), out var station)
            ? station
            : null;
    }

    public void UpdateAgeStates(DateTimeOffset now)
    {
        foreach (var (stationKey, station) in stations.ToArray())
        {
            stations[stationKey] = station with
            {
                LifecycleState = CalculateLifecycleState(station, now)
            };
        }
    }

    public bool HideStation(string callsign)
    {
        var stationKey = NormalizeStationKey(callsign);
        if (!stations.TryGetValue(stationKey, out var station))
        {
            return false;
        }

        stations[stationKey] = station with
        {
            IsManuallyHidden = true,
            LifecycleState = StationLifecycleState.Hidden
        };

        return true;
    }

    public bool UnhideStation(string callsign, DateTimeOffset now)
    {
        var stationKey = NormalizeStationKey(callsign);
        if (!stations.TryGetValue(stationKey, out var station))
        {
            return false;
        }

        var unhidden = station with { IsManuallyHidden = false };
        stations[stationKey] = unhidden with
        {
            LifecycleState = CalculateLifecycleState(unhidden, now)
        };

        return true;
    }

    public void ClearHiddenState(DateTimeOffset now)
    {
        foreach (var (stationKey, station) in stations.ToArray())
        {
            var unhidden = station with { IsManuallyHidden = false };
            stations[stationKey] = unhidden with
            {
                LifecycleState = CalculateLifecycleState(unhidden, now)
            };
        }
    }

    public void Clear()
    {
        stations.Clear();
    }

    private static StationSnapshot CreateBaseUpdate(
        string stationKey,
        AprsPacket packet,
        AprsPacketSource packetSource,
        StationSnapshot? existing)
    {
        var (callsign, ssid) = SplitStationKey(stationKey);

        return new StationSnapshot(
            callsign,
            ssid,
            FormatDisplayName(callsign, ssid),
            existing?.IsManuallyHidden == true ? StationLifecycleState.Hidden : StationLifecycleState.Active,
            existing?.IsManuallyHidden ?? false,
            existing?.Latitude,
            existing?.Longitude,
            existing?.SymbolTableIdentifier,
            existing?.SymbolCode,
            existing?.Comment,
            packet.ReceivedAtUtc,
            packet.ReceivedAtUtc,
            packet.RawLine,
            packet.GetType().Name,
            existing?.CourseDegrees,
            existing?.SpeedKnots,
            existing?.AltitudeFeet,
            (existing?.PacketCount ?? 0) + 1,
            packet.Path,
            packetSource,
            existing?.HasMessagingCapability,
            existing?.Weather);
    }

    private static StationSnapshot ApplyPacketSpecificFields(StationSnapshot station, AprsPacket packet)
    {
        return packet switch
        {
            PositionAprsPacket position => station with
            {
                Latitude = position.Latitude ?? station.Latitude,
                Longitude = position.Longitude ?? station.Longitude,
                SymbolTableIdentifier = position.SymbolTableIdentifier ?? station.SymbolTableIdentifier,
                SymbolCode = position.SymbolCode ?? station.SymbolCode,
                Comment = string.IsNullOrEmpty(position.Comment) ? station.Comment : position.Comment,
                CourseDegrees = position.CourseDegrees ?? station.CourseDegrees,
                SpeedKnots = position.SpeedKnots ?? station.SpeedKnots,
                AltitudeFeet = position.AltitudeFeet ?? station.AltitudeFeet
            },
            StatusAprsPacket status => station with
            {
                Comment = status.StatusText
            },
            MessageAprsPacket => station with
            {
                HasMessagingCapability = true
            },
            ObjectAprsPacket aprsObject => station with
            {
                Latitude = aprsObject.Latitude ?? station.Latitude,
                Longitude = aprsObject.Longitude ?? station.Longitude,
                SymbolTableIdentifier = aprsObject.SymbolTableIdentifier ?? station.SymbolTableIdentifier,
                SymbolCode = aprsObject.SymbolCode ?? station.SymbolCode,
                Comment = string.IsNullOrEmpty(aprsObject.Comment) ? station.Comment : aprsObject.Comment
            },
            ItemAprsPacket item => station with
            {
                Latitude = item.Latitude ?? station.Latitude,
                Longitude = item.Longitude ?? station.Longitude,
                SymbolTableIdentifier = item.SymbolTableIdentifier ?? station.SymbolTableIdentifier,
                SymbolCode = item.SymbolCode ?? station.SymbolCode,
                Comment = string.IsNullOrEmpty(item.Comment) ? station.Comment : item.Comment
            },
            WeatherAprsPacket weather => station with
            {
                Latitude = weather.Latitude ?? station.Latitude,
                Longitude = weather.Longitude ?? station.Longitude,
                SymbolTableIdentifier = weather.SymbolTableIdentifier ?? station.SymbolTableIdentifier,
                SymbolCode = weather.SymbolCode ?? station.SymbolCode,
                Comment = string.IsNullOrEmpty(weather.Comment) ? station.Comment : weather.Comment,
                Weather = new StationWeatherSnapshot(
                    weather.WindDirectionDegrees,
                    weather.WindSpeedMph,
                    weather.WindGustMph,
                    weather.TemperatureFahrenheit,
                    weather.RainLastHourHundredthsInch,
                    weather.RainLast24HoursHundredthsInch,
                    weather.RainSinceMidnightHundredthsInch,
                    weather.HumidityPercent,
                    weather.BarometricPressureMillibars,
                    weather.LuminosityWattsPerSquareMeter,
                    weather.SnowHundredthsInch,
                    weather.RawWeatherBody,
                    string.IsNullOrEmpty(weather.Comment) ? null : weather.Comment)
            },
            _ => station
        };
    }

    private static string GetStationKey(AprsPacket packet)
    {
        return packet switch
        {
            ObjectAprsPacket aprsObject => NormalizeStationKey(aprsObject.ObjectName),
            ItemAprsPacket item => NormalizeStationKey(item.ItemName),
            _ => NormalizeStationKey(FormatDisplayName(packet.SourceCallsign, packet.SourceSsid))
        };
    }

    private static string NormalizeStationKey(string callsign)
    {
        return callsign.Trim().ToUpperInvariant();
    }

    private static string FormatDisplayName(string callsign, int? ssid)
    {
        return ssid is null ? callsign : $"{callsign}-{ssid}";
    }

    private static (string Callsign, int? Ssid) SplitStationKey(string stationKey)
    {
        var parts = stationKey.Split('-', 2);
        if (parts.Length == 2 && int.TryParse(parts[1], out var ssid))
        {
            return (parts[0], ssid);
        }

        return (stationKey, null);
    }

    private static IReadOnlyCollection<StationSnapshot> SortStations(IEnumerable<StationSnapshot> stationValues)
    {
        return stationValues
            .OrderBy(station => station.Callsign, StringComparer.OrdinalIgnoreCase)
            .ThenBy(station => station.Ssid)
            .ToArray();
    }

    private bool IsVisible(StationSnapshot station)
    {
        if (station.LifecycleState == StationLifecycleState.Hidden)
        {
            return agingConfiguration.IncludeHiddenStationsInNormalLists;
        }

        return station.LifecycleState != StationLifecycleState.Expired
            || agingConfiguration.ShowExpiredStations;
    }

    private StationLifecycleState CalculateLifecycleState(StationSnapshot station, DateTimeOffset now)
    {
        if (station.IsManuallyHidden)
        {
            return StationLifecycleState.Hidden;
        }

        var age = now - station.LastHeardUtc;
        if (age < TimeSpan.Zero)
        {
            age = TimeSpan.Zero;
        }

        if (age >= agingConfiguration.HiddenThreshold)
        {
            return StationLifecycleState.Hidden;
        }

        if (age >= agingConfiguration.ExpiredThreshold)
        {
            return StationLifecycleState.Expired;
        }

        if (age > agingConfiguration.ActiveThreshold && age < agingConfiguration.StaleThreshold)
        {
            return StationLifecycleState.Stale;
        }

        if (age >= agingConfiguration.StaleThreshold)
        {
            return StationLifecycleState.Expired;
        }

        return StationLifecycleState.Active;
    }
}
