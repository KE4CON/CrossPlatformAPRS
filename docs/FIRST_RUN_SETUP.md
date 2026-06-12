# APRS Command First-Run Setup

Phase 15.1 adds the first-run setup foundation for APRS Command. This is setup preparation only; it does not enable transmit, start network listeners, load plugins, or create final installers.

## First-Run State

The first-run setup model tracks:

- whether first-run setup is complete
- application data, logs, packet logs, exports, file hooks, plugin, and map cache folders
- station profile, safety, APRS-IS, RF/TNC, and map review flags
- created and updated timestamps

All transmit and extension entry points remain disabled by default:

- APRS-IS transmit disabled
- RF transmit disabled
- iGate disabled
- digipeater disabled
- beaconing disabled
- weather beaconing disabled
- REST API disabled
- WebSocket streams disabled
- file hooks disabled
- plugin loading disabled

## Default Folders

APRS Command prepares a platform-appropriate application data root named `APRS Command`. Operators may choose a different root later.

Default layout:

```text
APRS Command/
  config/
  logs/
  packet-logs/
  event-logs/
  maps/
  map-cache/
  exports/
  file-hooks/
    incoming/
    processed/
    rejected/
    exports/
  plugins/
  backups/
  training/
  replay/
```

The folder service uses .NET application data paths and `Path.Combine`; it does not hardcode Windows-only paths.

## Placeholder Configuration Files

The setup service prepares safe placeholder JSON files under `config/`:

- `appsettings.safe-defaults.json`
- `station-profile.placeholder.json`
- `aprs-is.placeholder.json`
- `rf-tnc.placeholder.json`
- `map-cache.placeholder.json`
- `safety.safe-defaults.json`
- `extensions.safe-defaults.json`

These files must not contain real callsigns, APRS-IS passcodes, API tokens, weather credentials, or plugin credentials.

## Desktop UI

The Settings area includes a First Run tab that shows:

- welcome text
- application data folder
- log folder
- map cache folder
- export folder
- safe transmit and extension defaults
- a placeholder command to mark setup complete

This is intentionally lightweight. Final packaging work can replace it with a fuller wizard after the folder and safety model stabilizes.

## Platform Notes

Windows:
- Use the user application data location by default.
- Final installers should create shortcuts and uninstall metadata without changing safe defaults.

macOS:
- Use the user application support location by default.
- Final packages should account for signing and notarization.

Linux:
- Use the user application data location or an equivalent user-writable location.
- Desktop files and package metadata should display `APRS Command`.

Raspberry Pi / Linux ARM64:
- Use the same Linux folder behavior.
- Keep map cache and logs on user-writable storage and document SD-card space considerations.

## Safety

First-run setup is not permission to transmit. Operators must explicitly configure and review station identity, APRS-IS transmit, RF transmit, beaconing, iGate, digipeater, and weather beacon settings before any future transmit path can operate.
