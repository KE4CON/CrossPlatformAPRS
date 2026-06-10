using Aprs.Core;
using Xunit;

namespace Aprs.Tests;

public sealed class AprsParserTests
{
    private static readonly DateTimeOffset ReceivedAtUtc = new(2026, 6, 10, 12, 0, 0, TimeSpan.Zero);

    [Theory]
    [InlineData(
        "N0CALL>APRS,TCPIP*:!3903.50N/08430.50W-Test beacon",
        "N0CALL",
        null,
        "APRS",
        new[] { "TCPIP*" },
        "!3903.50N/08430.50W-Test beacon")]
    [InlineData(
        "W1AW-9>APRS,WIDE1-1,WIDE2-1:=4123.45N/07234.56W>Mobile test",
        "W1AW",
        9,
        "APRS",
        new[] { "WIDE1-1", "WIDE2-1" },
        "=4123.45N/07234.56W>Mobile test")]
    [InlineData(
        "K8ABC>APRS::N0CALL   :Hello{01",
        "K8ABC",
        null,
        "APRS",
        new string[] { },
        ":N0CALL   :Hello{01")]
    public void TryParse_ReturnsRawPacket_ForValidAprsTextLine(
        string rawLine,
        string expectedSourceCallsign,
        int? expectedSourceSsid,
        string expectedDestination,
        string[] expectedPath,
        string expectedInformation)
    {
        var parser = new AprsParser();

        var isValid = parser.TryParse(rawLine, ReceivedAtUtc, out var packet, out var error);

        var rawPacket = Assert.IsType<RawAprsPacket>(packet);
        Assert.True(isValid);
        Assert.True(rawPacket.IsValid);
        Assert.Null(error);
        Assert.Empty(rawPacket.ValidationErrors);
        Assert.Equal(rawLine, rawPacket.RawLine);
        Assert.Equal(expectedSourceCallsign, rawPacket.SourceCallsign);
        Assert.Equal(expectedSourceSsid, rawPacket.SourceSsid);
        Assert.Equal(expectedDestination, rawPacket.Destination);
        Assert.Equal(expectedPath, rawPacket.Path);
        Assert.Equal(expectedInformation, rawPacket.Information);
        Assert.Equal(ReceivedAtUtc, rawPacket.ReceivedAtUtc);
    }

    [Fact]
    public void TryParse_AllowsEmptyInformationField()
    {
        var parser = new AprsParser();

        var isValid = parser.TryParse("N0CALL>APRS:", ReceivedAtUtc, out var packet, out var error);

        var rawPacket = Assert.IsType<RawAprsPacket>(packet);
        Assert.True(isValid);
        Assert.True(rawPacket.IsValid);
        Assert.Null(error);
        Assert.Equal("N0CALL", rawPacket.SourceCallsign);
        Assert.Equal("APRS", rawPacket.Destination);
        Assert.Empty(rawPacket.Path);
        Assert.Equal(string.Empty, rawPacket.Information);
    }

    [Theory]
    [InlineData("BADPACKETWITHOUTSEPARATOR")]
    [InlineData(">APRS:missing source")]
    [InlineData("")]
    public void TryParse_ReturnsInvalidRawPacket_ForMalformedLine(string rawLine)
    {
        var parser = new AprsParser();

        var exception = Record.Exception(() =>
        {
            var isValid = parser.TryParse(rawLine, ReceivedAtUtc, out var packet, out var error);

            var rawPacket = Assert.IsType<RawAprsPacket>(packet);
            Assert.False(isValid);
            Assert.False(rawPacket.IsValid);
            Assert.NotEmpty(rawPacket.ValidationErrors);
            Assert.Equal(rawLine, rawPacket.RawLine);
            Assert.Equal(rawPacket.ValidationErrors[0], error);
        });

        Assert.Null(exception);
    }

    [Fact]
    public void TryParse_ExtractsValidationErrors_ForMissingSource()
    {
        var parser = new AprsParser();

        parser.TryParse(">APRS:missing source", ReceivedAtUtc, out var packet, out var error);

        var rawPacket = Assert.IsType<RawAprsPacket>(packet);
        Assert.Equal("APRS", rawPacket.Destination);
        Assert.Equal("missing source", rawPacket.Information);
        Assert.Contains("Packet source callsign is missing.", rawPacket.ValidationErrors);
        Assert.Equal("Packet source callsign is missing.", error);
    }

    [Fact]
    public void TryParse_ExtractsQConstruct_WhenPresentInPath()
    {
        var parser = new AprsParser();

        parser.TryParse("N0CALL>APRS,TCPIP*,qAC,T2SERVER:>status", ReceivedAtUtc, out var packet, out _);

        var rawPacket = Assert.IsType<RawAprsPacket>(packet);
        Assert.True(rawPacket.IsValid);
        Assert.Equal("qAC", rawPacket.QConstruct);
        Assert.Equal(new[] { "TCPIP*", "qAC", "T2SERVER" }, rawPacket.Path);
    }
}
