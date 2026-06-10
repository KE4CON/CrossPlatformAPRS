using System.Globalization;

namespace Aprs.Core;

public sealed class AprsPositionParser
{
    public PositionAprsPacket Parse(RawAprsPacket rawPacket)
    {
        var validationErrors = rawPacket.ValidationErrors.ToList();
        var information = rawPacket.Information;
        var positionType = information.Length > 0 ? information[0] : '\0';
        var hasTimestamp = positionType is '/' or '@';
        var latitudeStart = hasTimestamp ? 8 : 1;
        var timestamp = hasTimestamp && information.Length >= 8
            ? information.Substring(1, 7)
            : null;

        if (hasTimestamp && timestamp is null)
        {
            validationErrors.Add("Position packet timestamp is missing or incomplete.");
        }

        var latitudeText = SliceOrEmpty(information, latitudeStart, 8);
        var symbolTableIndex = latitudeStart + 8;
        var symbolTableIdentifier = TryGetChar(information, symbolTableIndex);
        var longitudeStart = symbolTableIndex + 1;
        var longitudeText = SliceOrEmpty(information, longitudeStart, 9);
        var symbolCodeIndex = longitudeStart + 9;
        var symbolCode = TryGetChar(information, symbolCodeIndex);
        var commentStart = symbolCodeIndex + 1;
        var comment = commentStart <= information.Length ? information[commentStart..] : string.Empty;

        if (latitudeText.Length != 8)
        {
            validationErrors.Add("Position packet latitude is missing or incomplete.");
        }

        if (longitudeText.Length != 9)
        {
            validationErrors.Add("Position packet longitude is missing or incomplete.");
        }

        if (symbolTableIdentifier is null)
        {
            validationErrors.Add("Position packet symbol table identifier is missing.");
        }

        if (symbolCode is null)
        {
            validationErrors.Add("Position packet symbol code is missing.");
        }

        var latitude = TryParseLatitude(latitudeText, validationErrors);
        var longitude = TryParseLongitude(longitudeText, validationErrors);
        var positionAmbiguity = CountPositionAmbiguity(latitudeText, longitudeText);
        var (courseDegrees, speedKnots) = ParseCourseAndSpeed(comment);
        var altitudeFeet = ParseAltitude(comment);

        return new PositionAprsPacket(
            rawPacket.RawLine,
            rawPacket.SourceCallsign,
            rawPacket.SourceSsid,
            rawPacket.Destination,
            rawPacket.Path,
            rawPacket.Information,
            rawPacket.ReceivedAtUtc,
            rawPacket.IsValid && validationErrors.Count == 0,
            validationErrors,
            rawPacket.QConstruct,
            positionType,
            timestamp,
            latitude,
            longitude,
            symbolTableIdentifier,
            symbolCode,
            comment,
            courseDegrees,
            speedKnots,
            altitudeFeet,
            positionAmbiguity);
    }

    private static string SliceOrEmpty(string value, int start, int length)
    {
        if (start >= value.Length)
        {
            return string.Empty;
        }

        return value.Substring(start, Math.Min(length, value.Length - start));
    }

    private static char? TryGetChar(string value, int index)
    {
        return index >= 0 && index < value.Length ? value[index] : null;
    }

    private static double? TryParseLatitude(string latitudeText, List<string> validationErrors)
    {
        if (latitudeText.Length != 8)
        {
            return null;
        }

        var hemisphere = latitudeText[7];
        if (hemisphere is not ('N' or 'S'))
        {
            validationErrors.Add("Position packet latitude hemisphere is invalid.");
            return null;
        }

        var normalized = latitudeText[..7].Replace(' ', '0');
        if (!int.TryParse(normalized[..2], NumberStyles.None, CultureInfo.InvariantCulture, out var degrees)
            || !double.TryParse(normalized[2..], NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture, out var minutes)
            || degrees > 90
            || minutes >= 60)
        {
            validationErrors.Add("Position packet latitude is invalid.");
            return null;
        }

        var decimalDegrees = degrees + minutes / 60;
        return hemisphere == 'S' ? -decimalDegrees : decimalDegrees;
    }

    private static double? TryParseLongitude(string longitudeText, List<string> validationErrors)
    {
        if (longitudeText.Length != 9)
        {
            return null;
        }

        var hemisphere = longitudeText[8];
        if (hemisphere is not ('E' or 'W'))
        {
            validationErrors.Add("Position packet longitude hemisphere is invalid.");
            return null;
        }

        var normalized = longitudeText[..8].Replace(' ', '0');
        if (!int.TryParse(normalized[..3], NumberStyles.None, CultureInfo.InvariantCulture, out var degrees)
            || !double.TryParse(normalized[3..], NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture, out var minutes)
            || degrees > 180
            || minutes >= 60)
        {
            validationErrors.Add("Position packet longitude is invalid.");
            return null;
        }

        var decimalDegrees = degrees + minutes / 60;
        return hemisphere == 'W' ? -decimalDegrees : decimalDegrees;
    }

    private static int CountPositionAmbiguity(string latitudeText, string longitudeText)
    {
        var latitudeAmbiguity = latitudeText.Take(7).Count(character => character == ' ');
        var longitudeAmbiguity = longitudeText.Take(8).Count(character => character == ' ');

        return Math.Max(latitudeAmbiguity, longitudeAmbiguity);
    }

    private static (int? CourseDegrees, int? SpeedKnots) ParseCourseAndSpeed(string comment)
    {
        if (comment.Length < 7
            || !comment.Take(3).All(char.IsDigit)
            || comment[3] != '/'
            || !comment.Skip(4).Take(3).All(char.IsDigit))
        {
            return (null, null);
        }

        var course = int.Parse(comment[..3], CultureInfo.InvariantCulture);
        var speed = int.Parse(comment.Substring(4, 3), CultureInfo.InvariantCulture);

        return course <= 360 ? (course, speed) : (null, speed);
    }

    private static int? ParseAltitude(string comment)
    {
        var altitudeIndex = comment.IndexOf("/A=", StringComparison.Ordinal);
        if (altitudeIndex < 0 || altitudeIndex + 9 > comment.Length)
        {
            return null;
        }

        var altitudeText = comment.Substring(altitudeIndex + 3, 6);
        return int.TryParse(altitudeText, NumberStyles.None, CultureInfo.InvariantCulture, out var altitude)
            ? altitude
            : null;
    }
}
