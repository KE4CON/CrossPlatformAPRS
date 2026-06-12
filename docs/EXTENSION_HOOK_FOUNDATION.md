# Extension Hook Foundation

Phase 14.5 prepares APRS Command for future local APIs, event streams, file import/export, plugins, and third-party drivers without implementing those runtime systems yet.

## What Phase 14.5 Adds

- `AprsCommand.Contracts` for external DTO placeholders.
- Internal source/origin metadata primitives in `Aprs.Services`.
- A lightweight internal application event bus.
- A future-facing extension permission model.
- Documentation for extension safety and architecture boundaries.

This phase is intentionally foundational. The REST API, WebSocket server, file watcher/import runtime, plugin loader, SDK packaging, and developer examples remain Phase 16 work.

## Public DTO Contract Strategy

External integrations must not bind directly to mutable internal domain models. Public contracts live in `AprsCommand.Contracts` and are intended to be explicit, versionable DTOs.

Initial placeholder DTOs include:

- `StationUpdateDto`
- `WeatherObservationDto`
- `AprsObjectDto`
- `GpsPositionDto`
- `RawPacketDto`
- `MessageDto`
- `PortStatusDto`
- `AlertDto`
- `TransmitLogDto`

Each public DTO carries a `SchemaVersion`, source metadata, validation warnings, validation errors, and notes where appropriate. Future Phase 16 work should add mapping/adapters between internal models and these contracts rather than exposing internal records directly.

## Source Tagging Standard

All incoming, generated, imported, replayed, simulated, training, API, file, plugin, packet, station, object, weather, GPS, message, alert, and transmit-log data should carry source metadata.

Source metadata should identify:

- source name
- source type
- source ID, port ID, driver ID, or integration ID
- received or generated timestamp
- origin
- trust level

Supported source types include:

- APRS-IS
- RF
- TCP KISS
- Serial KISS
- Direwolf
- AGWPE
- Replay
- Simulation
- Training
- Weather driver
- GPS
- Manual entry
- File import
- Local API
- Plugin
- Local generated
- Unknown

Default metadata should be unknown and untrusted until a service or operator configuration proves otherwise.

## Internal Event Bus Purpose

The internal event bus is a small service abstraction for publishing application events without hardwiring future API, WebSocket, plugin, or UI consumers into core services.

Initial event types include:

- `RawPacketReceived`
- `AprsPacketParsed`
- `StationUpdated`
- `ObjectUpdated`
- `WeatherUpdated`
- `MessageReceived`
- `GpsUpdated`
- `PortStatusChanged`
- `AlertTriggered`
- `PacketTransmitted`
- `TransmitBlocked`
- `IGateDecisionMade`
- `DigipeaterDecisionMade`
- `TrainingStateChanged`
- `SimulationStateChanged`
- `ReplayStateChanged`

The event bus is not intended to become an enterprise messaging system. It should stay simple, testable, and isolated from Avalonia views.

## Extension Permission Model

External software, future APIs, file imports, and plugins must default to read-only permissions.

Planned permission levels:

- `ReadOnly`
- `SubmitLocalData`
- `CreateLocalObjects`
- `QueuePackets`
- `TransmitAprsIs`
- `TransmitRf`
- `Admin`

Transmit-related permissions must never be granted implicitly. Operator configuration and centralized transmit safety checks are required before any extension can queue or request transmit-capable work.

## Intentionally Deferred to Phase 16

Phase 16 builds the runtime hook system:

- Phase 16.1: Public Data Contracts Finalization
- Phase 16.2: Local REST API
- Phase 16.3: WebSocket Event Streams
- Phase 16.4: File Import/Export Hooks
- Phase 16.5: Plugin/Driver Framework
- Phase 16.6: Extension Permission Enforcement
- Phase 16.7: Developer Documentation and Examples

Phase 14.5 should not add network listeners, WebSocket endpoints, plugin loading, file watchers, SDK packaging, or public transmit endpoints.
