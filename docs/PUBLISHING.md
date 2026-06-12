# APRS Command Publishing Guidance

Phase 14.13 upgrades APRS Command to target .NET 10 LTS. Phase 15 will verify and automate final packaging.

This document is a placeholder for publish guidance only. It does not create installers.

## SDK Requirement

Install the .NET 10 SDK.

```bash
dotnet --version
dotnet restore
dotnet build
dotnet test
```

The repository includes `global.json` pinned to the current .NET 10 SDK feature band.

## Desktop Run

```bash
dotnet run --project src/Aprs.Desktop
```

## Future Runtime Identifiers

Phase 15 should verify final publish commands for:

- Windows x64: `win-x64`
- macOS Apple Silicon: `osx-arm64`
- macOS Intel, if supported: `osx-x64`
- Linux x64: `linux-x64`
- Linux ARM64: `linux-arm64`
- Raspberry Pi 5 ARM64: `linux-arm64`

## Placeholder Publish Commands

These are guidance placeholders, not final release commands:

```bash
dotnet publish src/Aprs.Desktop -c Release -r win-x64 --self-contained true
dotnet publish src/Aprs.Desktop -c Release -r osx-arm64 --self-contained true
dotnet publish src/Aprs.Desktop -c Release -r osx-x64 --self-contained true
dotnet publish src/Aprs.Desktop -c Release -r linux-x64 --self-contained true
dotnet publish src/Aprs.Desktop -c Release -r linux-arm64 --self-contained true
```

Phase 15 should confirm Avalonia app packaging, signing/notarization needs, settings storage, first-run setup, and platform-specific dependencies.

## Safety

Packaging must preserve safe defaults:

- APRS-IS transmit disabled unless explicitly configured
- RF transmit disabled unless explicitly configured
- API/WebSocket/file/plugin transmit paths blocked by default
- replay, simulation, training, iGate, digipeater, beacon, object, message, and weather transmit flows gated by central safety checks
