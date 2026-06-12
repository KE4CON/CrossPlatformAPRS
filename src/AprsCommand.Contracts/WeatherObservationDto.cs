namespace AprsCommand.Contracts;

public sealed record WeatherObservationDto(
    string SchemaVersion = PublicContractDefaults.SchemaVersion,
    DtoSourceMetadata? Source = null,
    string? StationId = null,
    double? Latitude = null,
    double? Longitude = null,
    double? WindDirectionDegrees = null,
    double? WindSpeedMph = null,
    double? WindGustMph = null,
    double? TemperatureFahrenheit = null,
    double? RainLastHourInches = null,
    double? RainLast24HoursInches = null,
    double? RainSinceMidnightInches = null,
    double? HumidityPercent = null,
    double? BarometricPressureMillibars = null,
    double? Luminosity = null,
    double? UvIndex = null,
    double? SnowInches = null,
    DateTimeOffset? ObservedAtUtc = null,
    IReadOnlyList<string>? ValidationWarnings = null,
    IReadOnlyList<string>? ValidationErrors = null,
    string? Notes = null);
