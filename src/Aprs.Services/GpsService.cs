namespace Aprs.Services;

public sealed class GpsService : IGpsService
{
    private readonly INmeaParser parser;

    public GpsService(INmeaParser? parser = null)
    {
        this.parser = parser ?? new NmeaParser();
    }

    public GpsPosition? CurrentPosition { get; private set; }

    public bool HasValidFix => CurrentPosition?.FixValid == true
        && CurrentPosition.Latitude is not null
        && CurrentPosition.Longitude is not null;

    public NmeaParseResult AcceptSentence(string rawSentence, string sourceName = "NMEA", DateTimeOffset? receivedAtUtc = null)
    {
        var result = parser.Parse(rawSentence, sourceName, receivedAtUtc);
        if (result.IsParsed && result.Position is not null)
        {
            CurrentPosition = Merge(CurrentPosition, result.Position);
        }

        return result;
    }

    public void Reset()
    {
        CurrentPosition = null;
    }

    private static GpsPosition Merge(GpsPosition? current, GpsPosition update)
    {
        if (current is null)
        {
            return update;
        }

        return new GpsPosition(
            update.Latitude ?? current.Latitude,
            update.Longitude ?? current.Longitude,
            update.AltitudeMeters ?? current.AltitudeMeters,
            update.SpeedKnots ?? current.SpeedKnots,
            update.CourseDegrees ?? current.CourseDegrees,
            update.TimestampUtc ?? current.TimestampUtc,
            update.FixValid,
            update.FixQuality ?? current.FixQuality,
            update.SatelliteCount ?? current.SatelliteCount,
            update.Hdop ?? current.Hdop,
            update.SourceName,
            update.RawNmeaSentence,
            update.LastUpdateUtc);
    }
}
