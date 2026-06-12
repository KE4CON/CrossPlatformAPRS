# APRS Command

APRS Command is a modern C# / .NET cross-platform APRS client inspired by UI-View32, focused only on amateur-radio APRS features.

Target platforms:
- Windows
- Linux
- Raspberry Pi
- macOS

Recommended stack:
- .NET 10 LTS SDK
- Avalonia UI for the desktop app
- Mapsui or equivalent map rendering layer
- SQLite for local station/history storage

This repository is intentionally scaffolded for Codex-driven development. Start with `AGENTS.md` and `codex-tasks/MASTER_TASK_LIST.md`.

## First local setup

```bash
dotnet --info
dotnet --version
dotnet restore
dotnet build
dotnet test
```

The repository pins SDK selection with `global.json`. Install the .NET 10 SDK before building.

## Desktop smoke run

```bash
dotnet run --project src/Aprs.Desktop
```

The desktop opens to the original map-first shell: the map is the primary workspace, the station list stays on the right, the raw packet monitor stays below the map, and feature panels such as Messages, Objects, Weather, Events, Event Bus, Replay, RF Diagnostics, Alerts, Geofence, Simulation, Training, Files, and Settings remain available in the lower-right tab area.

## Publish guidance

Final installers are planned for a future release. Current first-run, repeatable publish, final release validation, and installer/package planning guidance is documented in `docs/FIRST_RUN_SETUP.md`, `docs/PACKAGING_PREPARATION.md`, `docs/BUILD_AND_PUBLISH.md`, `docs/FINAL_RELEASE_VALIDATION_CHECKLIST.md`, `docs/INSTALLER_AND_PACKAGE_PLAN.md`, and `docs/PUBLISHING.md`.

Portable ZIP and `tar.gz` package scripts write archives to `artifacts/packages/` and SHA256 files to `artifacts/checksums/`. Full installers, signing, notarization, and package-manager manifests are planned for later work.

## User documentation

APRS Command also includes an in-app Help button. Click Help in the application header to read the user manual, quick start guide, setup guides, safety guide, troubleshooting guide, and glossary offline from inside the desktop app.

- [Quick Start](docs/QUICK_START.md)
- [Installation Guide](docs/INSTALLATION_GUIDE.md)
- [Installer and Package Plan](docs/INSTALLER_AND_PACKAGE_PLAN.md)
- [Final Release Validation Checklist](docs/FINAL_RELEASE_VALIDATION_CHECKLIST.md)
- [User Manual](docs/USER_MANUAL.md)
- [First-Run Setup](docs/FIRST_RUN_SETUP.md)
- [Safety and Transmit Guide](docs/SAFETY_AND_TRANSMIT_GUIDE.md)
- [APRS-IS Setup Guide](docs/APRS_IS_SETUP_GUIDE.md)
- [RF/TNC Setup Guide](docs/RF_TNC_SETUP_GUIDE.md)
- [Map and Offline Maps Guide](docs/MAP_AND_OFFLINE_MAPS_GUIDE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Glossary](docs/GLOSSARY.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)

## Project layout

```text
src/Aprs.Core        APRS packet models, parser, symbol logic, validation
src/Aprs.Transport   APRS-IS, KISS, AGWPE, Direwolf, serial/network transport
src/Aprs.Services    Station database, beacon scheduler, messaging, object manager
src/Aprs.Mapping     Map tile cache, APRS marker rendering, offline map support
src/Aprs.Desktop     Avalonia desktop user interface
src/AprsCommand.Contracts  Versioned public DTO placeholders for future APIs/plugins
src/AprsCommand.Api  Local REST API foundation for future integrations
tests/Aprs.Tests     Unit and integration tests
codex-tasks/         Codex-ready implementation tasks
```

## Licensing note

Do not copy UI-View32 source code, icons, maps, proprietary artwork, or documentation text. Use UI-View only as a feature reference and implement original code.
