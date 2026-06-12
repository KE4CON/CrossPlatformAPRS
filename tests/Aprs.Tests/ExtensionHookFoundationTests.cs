using Aprs.Services;
using AprsCommand.Contracts;
using Xunit;

namespace Aprs.Tests;

public class ExtensionHookFoundationTests
{
    [Fact]
    public void PublicDtosCanBeInstantiatedWithSafeContractMetadata()
    {
        var source = new DtoSourceMetadata(
            "APRS-IS",
            ContractSourceType.AprsIs,
            "aprs-is",
            DateTimeOffset.UtcNow,
            ContractDataOrigin.Received,
            ContractSourceTrustLevel.OperatorConfigured);

        var station = new StationUpdateDto(Source: source, Callsign: "N0CALL", DisplayName: "Net Control");
        var weather = new WeatherObservationDto(Source: source, StationId: "WX9XYZ", TemperatureFahrenheit: 72);
        var aprsObject = new AprsObjectDto(Source: source, Name: "CHECKPNT1", OwnerCallsign: "OBJ1");
        var gps = new GpsPositionDto(Source: source, Latitude: 39.058333, Longitude: -84.508333, FixValid: true);
        var raw = new RawPacketDto(Source: source, RawPacketText: "N0CALL>APRS:>Test");
        var message = new MessageDto(Source: source, Sender: "K8ABC", Recipient: "N0CALL", Body: "Hello");
        var port = new PortStatusDto(Source: source, PortId: "aprs-is", PortName: "APRS-IS");
        var alert = new AlertDto(Source: source, AlertId: "alert-1", Title: "Station heard");
        var transmit = new TransmitLogDto(Source: source, RawPacketText: "N0CALL>APRS:>Test", Success: false);

        Assert.Equal(PublicContractDefaults.SchemaVersion, station.SchemaVersion);
        Assert.Equal(ContractSourceType.AprsIs, station.Source?.SourceType);
        Assert.Equal("WX9XYZ", weather.StationId);
        Assert.Equal("CHECKPNT1", aprsObject.Name);
        Assert.True(gps.FixValid);
        Assert.Equal("N0CALL>APRS:>Test", raw.RawPacketText);
        Assert.Equal("Hello", message.Body);
        Assert.Equal("aprs-is", port.PortId);
        Assert.Equal("Station heard", alert.Title);
        Assert.False(transmit.Success);
    }

    [Fact]
    public void SourceMetadataDefaultsToUnknownAndUntrusted()
    {
        var now = DateTimeOffset.UtcNow;

        var source = SourceMetadata.Unknown(now);

        Assert.Null(source.SourceName);
        Assert.Equal(DataSourceType.Unknown, source.SourceType);
        Assert.Equal(DataOrigin.Unknown, source.Origin);
        Assert.Equal(SourceTrustLevel.Untrusted, source.TrustLevel);
        Assert.Equal(now, source.TimestampUtc);
    }

    [Fact]
    public void SourceMetadataCreateNormalizesBlankFields()
    {
        var now = DateTimeOffset.UtcNow;

        var source = SourceMetadata.Create("  Training  ", DataSourceType.Training, "  scenario-1  ", now, DataOrigin.Training, SourceTrustLevel.Internal);

        Assert.Equal("Training", source.SourceName);
        Assert.Equal("scenario-1", source.SourceId);
        Assert.Equal(DataSourceType.Training, source.SourceType);
        Assert.Equal(SourceTrustLevel.Internal, source.TrustLevel);
    }

    [Fact]
    public void DefaultExtensionPermissionIsReadOnly()
    {
        var permissions = ExtensionPermissionSet.Default;

        Assert.True(permissions.HasPermission(ExtensionPermission.ReadOnly));
        Assert.False(permissions.HasPermission(ExtensionPermission.SubmitLocalData));
        Assert.False(permissions.HasTransmitPermission);
    }

    [Theory]
    [InlineData(ExtensionPermission.TransmitAprsIs)]
    [InlineData(ExtensionPermission.TransmitRf)]
    [InlineData(ExtensionPermission.QueuePackets)]
    public void TransmitRelatedPermissionsAreNotEnabledByDefault(ExtensionPermission permission)
    {
        Assert.False(ExtensionPermissionSet.Default.HasPermission(permission));
    }

    [Fact]
    public void EventBusPublishesToMatchingSubscriber()
    {
        var bus = new ApplicationEventBus();
        var now = DateTimeOffset.UtcNow;
        ApplicationEvent? received = null;

        using var subscription = bus.Subscribe(ApplicationEventType.StationUpdated, evt => received = evt);
        var applicationEvent = ApplicationEvent.Create(
            ApplicationEventType.StationUpdated,
            now,
            SourceMetadata.Create("Simulation", DataSourceType.Simulation, "sim", now, DataOrigin.Simulated),
            "N0CALL",
            "Station updated");

        bus.Publish(applicationEvent);

        Assert.Same(applicationEvent, received);
    }

    [Fact]
    public void EventBusCanPublishWithNoSubscribers()
    {
        var bus = new ApplicationEventBus();
        var now = DateTimeOffset.UtcNow;

        bus.Publish(ApplicationEvent.Create(ApplicationEventType.RawPacketReceived, now));
    }

    [Fact]
    public void EventBusSubscriptionCanBeDisposed()
    {
        var bus = new ApplicationEventBus();
        var count = 0;
        var now = DateTimeOffset.UtcNow;

        var subscription = bus.Subscribe(ApplicationEventType.AlertTriggered, _ => count++);
        subscription.Dispose();

        bus.Publish(ApplicationEvent.Create(ApplicationEventType.AlertTriggered, now));

        Assert.Equal(0, count);
    }
}
