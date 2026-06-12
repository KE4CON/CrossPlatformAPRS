using System.Xml.Linq;
using Xunit;

namespace Aprs.Tests;

public sealed class BuildAndPublishTests
{
    private static readonly string[] RuntimeIdentifiers =
    [
        "win-x64",
        "osx-arm64",
        "osx-x64",
        "linux-x64",
        "linux-arm64"
    ];

    [Fact]
    public void PublishProfiles_ExistForSupportedRuntimeIdentifiers()
    {
        foreach (var runtimeIdentifier in RuntimeIdentifiers)
        {
            var profilePath = Path.Combine(RepositoryRoot, "src", "Aprs.Desktop", "Properties", "PublishProfiles", $"{runtimeIdentifier}.pubxml");

            Assert.True(File.Exists(profilePath), profilePath);

            var document = XDocument.Load(profilePath);
            Assert.Equal(runtimeIdentifier, Value(document, "RuntimeIdentifier"));
            Assert.Equal("Release", Value(document, "Configuration"));
            Assert.Equal("true", Value(document, "SelfContained"));
            Assert.Equal("false", Value(document, "PublishSingleFile"));
            Assert.Contains($"artifacts/publish/{runtimeIdentifier}", Value(document, "PublishDir"), StringComparison.Ordinal);
        }
    }

    [Fact]
    public void PublishScripts_ExistForSupportedRuntimeIdentifiers()
    {
        foreach (var runtimeIdentifier in RuntimeIdentifiers)
        {
            var scriptPath = Path.Combine(RepositoryRoot, "scripts", $"publish-{runtimeIdentifier}.sh");

            Assert.True(File.Exists(scriptPath), scriptPath);
            var script = File.ReadAllText(scriptPath);

            Assert.Contains("publish-runtime.sh", script, StringComparison.Ordinal);
            Assert.Contains(runtimeIdentifier, script, StringComparison.Ordinal);
        }
    }

    [Fact]
    public void SharedPublishScript_RestoresBuildsTestsAndPublishes()
    {
        var script = File.ReadAllText(Path.Combine(RepositoryRoot, "scripts", "publish-runtime.sh"));

        Assert.Contains("APRS Command", script, StringComparison.Ordinal);
        Assert.Contains("dotnet restore", script, StringComparison.Ordinal);
        Assert.Contains("dotnet build", script, StringComparison.Ordinal);
        Assert.Contains("dotnet test", script, StringComparison.Ordinal);
        Assert.Contains("dotnet publish", script, StringComparison.Ordinal);
        Assert.Contains("artifacts/publish/$RID", script, StringComparison.Ordinal);
        Assert.DoesNotContain("rm -rf", script, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("TransmitEnabled=true", script, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("passcode", script, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("api_key", script, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("secret", script, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("token", script, StringComparison.OrdinalIgnoreCase);
    }

    [Fact]
    public void BuildAndPublishDocumentation_ListsSupportedCommandsAndSafetyLimits()
    {
        var document = File.ReadAllText(Path.Combine(RepositoryRoot, "docs", "BUILD_AND_PUBLISH.md"));

        Assert.Contains("APRS Command Build and Publish", document, StringComparison.Ordinal);
        Assert.Contains("dotnet restore", document, StringComparison.Ordinal);
        Assert.Contains("dotnet build", document, StringComparison.Ordinal);
        Assert.Contains("dotnet test", document, StringComparison.Ordinal);
        Assert.Contains("dotnet run --project src/Aprs.Desktop", document, StringComparison.Ordinal);
        Assert.Contains("artifacts/publish/<runtime-identifier>/", document, StringComparison.Ordinal);
        Assert.Contains("These scripts create publish folders only", document, StringComparison.Ordinal);

        foreach (var runtimeIdentifier in RuntimeIdentifiers)
        {
            Assert.Contains(runtimeIdentifier, document, StringComparison.Ordinal);
            Assert.Contains($"./scripts/publish-{runtimeIdentifier}.sh", document, StringComparison.Ordinal);
        }

        Assert.Contains("enable transmit", document, StringComparison.OrdinalIgnoreCase);
        Assert.Contains("generate final installers", document, StringComparison.OrdinalIgnoreCase);
    }

    private static string RepositoryRoot
    {
        get
        {
            var directory = new DirectoryInfo(AppContext.BaseDirectory);
            while (directory is not null && !File.Exists(Path.Combine(directory.FullName, "CrossPlatformAprs.sln")))
            {
                directory = directory.Parent;
            }

            return directory?.FullName ?? throw new DirectoryNotFoundException("Could not locate repository root.");
        }
    }

    private static string Value(XDocument document, string elementName)
    {
        return document.Descendants(elementName).Single().Value;
    }
}
