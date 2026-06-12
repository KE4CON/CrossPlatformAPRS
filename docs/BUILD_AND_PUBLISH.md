# APRS Command Build and Publish

Phase 15.2 adds repeatable build and publish scripts for APRS Command. These scripts create publish folders only. They do not create installers, package managers, signed bundles, notarized apps, or final release archives.

## Prerequisites

- Install the .NET 10 SDK.
- Run commands from the repository root unless a script says otherwise.
- Keep transmit, RF, APRS-IS transmit, iGate, digipeater, beaconing, weather beaconing, REST API, WebSocket, file hooks, and plugin loading disabled unless a later explicit setup step enables them.

## Verify the Repository

```bash
dotnet restore
dotnet build
dotnet test
dotnet run --project src/Aprs.Desktop
```

## Supported Runtime Identifiers

The repeatable publish profiles cover:

- `win-x64`
- `osx-arm64`
- `osx-x64`
- `linux-x64`
- `linux-arm64`

Raspberry Pi 5 ARM64 uses `linux-arm64`.

## Publish Scripts

Each script restores, builds in Release, runs tests, and publishes `src/Aprs.Desktop`.

```bash
./scripts/publish-win-x64.sh
./scripts/publish-osx-arm64.sh
./scripts/publish-osx-x64.sh
./scripts/publish-linux-x64.sh
./scripts/publish-linux-arm64.sh
./scripts/publish-all.sh
```

Windows PowerShell helper:

```powershell
.\scripts\publish-win-x64.ps1
```

Generic helper:

```bash
./scripts/publish-runtime.sh linux-arm64
```

## Publish Profiles

MSBuild publish profiles are stored under:

```text
src/Aprs.Desktop/Properties/PublishProfiles/
```

Direct profile examples:

```bash
dotnet publish src/Aprs.Desktop/Aprs.Desktop.csproj -c Release /p:PublishProfile=linux-x64
dotnet publish src/Aprs.Desktop/Aprs.Desktop.csproj -c Release /p:PublishProfile=osx-arm64
dotnet publish src/Aprs.Desktop/Aprs.Desktop.csproj -c Release /p:PublishProfile=win-x64
```

## Output Folders

Script output is written to:

```text
artifacts/publish/<runtime-identifier>/
```

The `artifacts/` folder is ignored by Git and should not be committed.

## Publish Mode

Phase 15.2 uses self-contained publish output by default so first-user testing does not depend on a separately installed runtime. The profiles deliberately avoid final installer decisions.

Framework-dependent publish can still be tested manually when needed:

```bash
dotnet publish src/Aprs.Desktop/Aprs.Desktop.csproj -c Release -r linux-x64 --self-contained false -o artifacts/publish/linux-x64-framework-dependent
```

## Platform Notes

Windows:
- Verify `win-x64` output before creating future installers.
- Later installer work should add Start Menu shortcuts, uninstall metadata, and display name `APRS Command`.

macOS:
- Verify `osx-arm64` and `osx-x64` output.
- Later packaging work should handle `.app` layout, signing, notarization, and quarantine behavior.

Linux:
- Verify `linux-x64` and `linux-arm64` output.
- Later package work should add `.desktop` metadata, icons, AppImage/deb/rpm decisions, and Raspberry Pi notes.

## Safety

Publish scripts and profiles must not:

- enable transmit
- enable APRS-IS transmit
- enable RF transmit
- enable iGate or digipeater operation
- embed APRS-IS passcodes, API tokens, weather credentials, GitHub tokens, or other secrets
- generate final installers or signed release packages

Transmit safety remains centralized in runtime services and is not changed by publishing.
