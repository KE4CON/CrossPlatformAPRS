# CrossPlatform APRS Client

A modern C# / .NET cross-platform APRS client inspired by UI-View32, focused only on amateur-radio APRS features.

Target platforms:
- Windows
- Linux
- Raspberry Pi
- macOS

Recommended stack:
- .NET 8 or newer
- Avalonia UI for the desktop app
- Mapsui or equivalent map rendering layer
- SQLite for local station/history storage

This repository is intentionally scaffolded for Codex-driven development. Start with `AGENTS.md` and `codex-tasks/MASTER_TASK_LIST.md`.

## First local setup

```bash
dotnet --info
dotnet restore
dotnet build
```

## Project layout

```text
src/Aprs.Core        APRS packet models, parser, symbol logic, validation
src/Aprs.Transport   APRS-IS, KISS, AGWPE, Direwolf, serial/network transport
src/Aprs.Services    Station database, beacon scheduler, messaging, object manager
src/Aprs.Mapping     Map tile cache, APRS marker rendering, offline map support
src/Aprs.Desktop     Avalonia desktop user interface
tests/Aprs.Tests     Unit and integration tests
codex-tasks/         Codex-ready implementation tasks
```

## Licensing note

Do not copy UI-View32 source code, icons, maps, proprietary artwork, or documentation text. Use UI-View only as a feature reference and implement original code.
