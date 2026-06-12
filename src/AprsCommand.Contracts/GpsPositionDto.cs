namespace AprsCommand.Contracts;

public sealed record GpsPositionDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    double? Latitude = null,
    double? Longitude = null,
    double? AltitudeMeters = null,
    double? SpeedKnots = null,
    double? CourseDegrees = null,
    bool FixValid = false,
    int? FixQuality = null,
    int? SatelliteCount = null,
    int? UsedSatelliteCount = null,
    double? Hdop = null,
    DateTimeOffset? FixTimestampUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
