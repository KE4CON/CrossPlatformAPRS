using System.Text.RegularExpressions;

namespace Aprs.Services;

public sealed partial class DecodedEventLogService : IDecodedEventLogService
{
    private readonly IBeaconSchedulerClock clock;
    private readonly DecodedEventLogConfiguration configuration;
    private readonly List<DecodedEventLogEntry> entries = [];

    public DecodedEventLogService(
        DecodedEventLogConfiguration? configuration = null,
        IBeaconSchedulerClock? clock = null)
    {
        this.configuration = configuration ?? DecodedEventLogConfiguration.Default;
        this.clock = clock ?? new SystemBeaconSchedulerClock();
    }

    public DecodedEventLogEntry? AddEvent(
        DecodedEventType eventType,
        DecodedEventCategory eventCategory,
        DecodedEventSeverity severity,
        string summary,
        string? details = null,
        string? sourceCallsign = null,
        string? relatedEntity = null,
        AprsPacketSource? packetSource = null,
        Guid? relatedRawPacketLogEntryId = null,
        IReadOnlyDictionary<string, string>? structuredEventData = null,
        IReadOnlyList<string>? validationErrors = null,
        IReadOnlyList<string>? validationWarnings = null,
        string? notes = null,
        DateTimeOffset? timestampUtc = null)
    {
        if (!configuration.DecodedEventLoggingEnabled)
        {
            return null;
        }

        var sanitizedData = (structuredEventData ?? new Dictionary<string, string>())
            .ToDictionary(pair => SanitizeRequired(pair.Key), pair => SanitizeRequired(pair.Value), StringComparer.OrdinalIgnoreCase);

        var entry = new DecodedEventLogEntry(
            Guid.NewGuid(),
            timestampUtc ?? clock.UtcNow,
            eventType,
            eventCategory,
            severity,
            Sanitize(sourceCallsign),
            Sanitize(relatedEntity),
            packetSource,
            relatedRawPacketLogEntryId,
            SanitizeRequired(summary),
            Sanitize(details),
            sanitizedData,
            (validationErrors ?? []).Select(SanitizeRequired).ToArray(),
            (validationWarnings ?? []).Select(SanitizeRequired).ToArray(),
            Sanitize(notes));

        entries.Add(entry);
        TrimEntries();
        return entry;
    }

    public DecodedEventLogEntry? AddStationEvent(DecodedEventType eventType, string callsign, string summary, AprsPacketSource? packetSource = null, string? details = null)
    {
        return AddEvent(eventType, DecodedEventCategory.Station, DecodedEventSeverity.Info, summary, details, callsign, callsign, packetSource);
    }

    public DecodedEventLogEntry? AddObjectEvent(DecodedEventType eventType, string objectName, string summary, AprsPacketSource? packetSource = null, string? ownerCallsign = null)
    {
        var severity = eventType == DecodedEventType.ObjectKilled ? DecodedEventSeverity.Warning : DecodedEventSeverity.Info;
        return AddEvent(eventType, DecodedEventCategory.Object, severity, summary, relatedEntity: objectName, sourceCallsign: ownerCallsign, packetSource: packetSource);
    }

    public DecodedEventLogEntry? AddWeatherEvent(string sourceName, string summary, AprsPacketSource? packetSource = null, string? details = null)
    {
        return AddEvent(DecodedEventType.WeatherUpdated, DecodedEventCategory.Weather, DecodedEventSeverity.Info, summary, details, relatedEntity: sourceName, packetSource: packetSource);
    }

    public DecodedEventLogEntry? AddMessageEvent(DecodedEventType eventType, string remoteCallsign, string summary, AprsPacketSource? packetSource = null, string? details = null)
    {
        var severity = eventType == DecodedEventType.MessageRejected ? DecodedEventSeverity.Warning : DecodedEventSeverity.Info;
        return AddEvent(eventType, DecodedEventCategory.Message, severity, summary, details, remoteCallsign, remoteCallsign, packetSource);
    }

    public DecodedEventLogEntry? AddGpsEvent(string sourceName, string summary, DecodedEventSeverity severity = DecodedEventSeverity.Info, string? details = null)
    {
        return AddEvent(DecodedEventType.GpsUpdated, DecodedEventCategory.GPS, severity, summary, details, relatedEntity: sourceName);
    }

    public DecodedEventLogEntry? AddPortEvent(DecodedEventType eventType, string portName, string summary, DecodedEventSeverity severity = DecodedEventSeverity.Info, string? details = null)
    {
        var category = eventType is DecodedEventType.AprsIsConnected or DecodedEventType.AprsIsDisconnected
            ? DecodedEventCategory.AprsIs
            : DecodedEventCategory.Port;
        return AddEvent(eventType, category, severity, summary, details, relatedEntity: portName);
    }

    public DecodedEventLogEntry? AddTransmitEvent(DecodedEventType eventType, string summary, AprsPacketSource? packetSource = null, string? sourceCallsign = null, string? details = null)
    {
        var severity = eventType == DecodedEventType.PacketTransmitBlocked ? DecodedEventSeverity.Warning : DecodedEventSeverity.Info;
        return AddEvent(eventType, DecodedEventCategory.Packet, severity, summary, details, sourceCallsign, sourceCallsign, packetSource);
    }

    public DecodedEventLogEntry? AddIGateEvent(IGateGatingDecisionRecord decision)
    {
        var gated = decision.Decision == IGateDecision.Allowed;
        return AddEvent(
            gated ? DecodedEventType.IGatePacketGated : DecodedEventType.IGatePacketBlocked,
            DecodedEventCategory.IGate,
            gated ? DecodedEventSeverity.Info : DecodedEventSeverity.Warning,
            gated ? "RF packet gated to APRS-IS." : "iGate candidate blocked.",
            decision.Reason,
            decision.SourceCallsign,
            decision.ReceivedRfPort,
            AprsPacketSource.Rf,
            structuredEventData: new Dictionary<string, string>
            {
                ["Decision"] = decision.Decision.ToString(),
                ["PacketType"] = decision.ParsedPacketType,
                ["TransmitAttempted"] = decision.TransmitAttempted.ToString()
            },
            validationErrors: decision.ValidationErrors,
            validationWarnings: decision.ValidationWarnings);
    }

    public DecodedEventLogEntry? AddDigipeaterEvent(DigipeaterDecisionRecord decision)
    {
        var repeated = decision.Decision == DigipeaterDecision.Allowed;
        return AddEvent(
            repeated ? DecodedEventType.DigipeaterPacketRepeated : DecodedEventType.DigipeaterPacketBlocked,
            DecodedEventCategory.Digipeater,
            repeated ? DecodedEventSeverity.Info : DecodedEventSeverity.Warning,
            repeated ? "RF packet digipeated." : "Digipeater packet blocked.",
            decision.Reason,
            decision.SourceCallsign,
            decision.TransmitRfPort ?? decision.ReceivedRfPort,
            AprsPacketSource.Rf,
            structuredEventData: new Dictionary<string, string>
            {
                ["Decision"] = decision.Decision.ToString(),
                ["PacketType"] = decision.ParsedPacketType,
                ["TransmitAttempted"] = decision.TransmitAttempted.ToString()
            },
            validationErrors: decision.ValidationErrors,
            validationWarnings: decision.ValidationWarnings);
    }

    public IReadOnlyList<DecodedEventLogEntry> GetRecentEvents(int? maximumCount = null)
    {
        var query = entries.OrderByDescending(entry => entry.EventTimestampUtc).ThenByDescending(entry => entry.EventId);
        return maximumCount is > 0 ? query.Take(maximumCount.Value).ToArray() : query.ToArray();
    }

    public IReadOnlyList<DecodedEventLogEntry> GetEventsByType(DecodedEventType eventType)
    {
        return GetRecentEvents().Where(entry => entry.EventType == eventType).ToArray();
    }

    public IReadOnlyList<DecodedEventLogEntry> GetEventsByCategory(DecodedEventCategory category)
    {
        return GetRecentEvents().Where(entry => entry.EventCategory == category).ToArray();
    }

    public IReadOnlyList<DecodedEventLogEntry> GetEventsBySeverity(DecodedEventSeverity severity)
    {
        return GetRecentEvents().Where(entry => entry.Severity == severity).ToArray();
    }

    public IReadOnlyList<DecodedEventLogEntry> GetEventsByCallsignOrSource(string callsignOrSource)
    {
        if (string.IsNullOrWhiteSpace(callsignOrSource))
        {
            return [];
        }

        var query = callsignOrSource.Trim();
        return GetRecentEvents()
            .Where(entry =>
                string.Equals(entry.SourceCallsign, query, StringComparison.OrdinalIgnoreCase)
                || string.Equals(entry.RelatedEntity, query, StringComparison.OrdinalIgnoreCase))
            .ToArray();
    }

    public IReadOnlyList<DecodedEventLogEntry> SearchEvents(string searchText)
    {
        if (string.IsNullOrWhiteSpace(searchText))
        {
            return GetRecentEvents();
        }

        var query = searchText.Trim();
        return GetRecentEvents()
            .Where(entry =>
                entry.Summary.Contains(query, StringComparison.OrdinalIgnoreCase)
                || (entry.Details?.Contains(query, StringComparison.OrdinalIgnoreCase) ?? false)
                || (entry.Notes?.Contains(query, StringComparison.OrdinalIgnoreCase) ?? false)
                || entry.StructuredEventData.Any(pair =>
                    pair.Key.Contains(query, StringComparison.OrdinalIgnoreCase)
                    || pair.Value.Contains(query, StringComparison.OrdinalIgnoreCase)))
            .ToArray();
    }

    public void ClearEventLog()
    {
        entries.Clear();
    }

    private void TrimEntries()
    {
        var maximum = Math.Max(0, configuration.MaximumInMemoryEvents);
        if (maximum == 0)
        {
            entries.Clear();
            return;
        }

        while (entries.Count > maximum)
        {
            var oldest = entries.OrderBy(entry => entry.EventTimestampUtc).ThenBy(entry => entry.EventId).First();
            entries.Remove(oldest);
        }
    }

    private static string? Sanitize(string? value)
    {
        if (value is null)
        {
            return null;
        }

        var sanitized = AprsIsPassRegex().Replace(value, "$1[REDACTED]");
        sanitized = CredentialKeyValueRegex().Replace(sanitized, "$1[REDACTED]");
        return sanitized;
    }

    private static string SanitizeRequired(string value)
    {
        return Sanitize(value) ?? string.Empty;
    }

    [GeneratedRegex(@"(?i)\b(pass\s+)(\S+)")]
    private static partial Regex AprsIsPassRegex();

    [GeneratedRegex(@"(?i)\b((?:api[_-]?key|token|password|passcode|secret)\s*[:=]\s*)([^\s,;]+)")]
    private static partial Regex CredentialKeyValueRegex();
}
