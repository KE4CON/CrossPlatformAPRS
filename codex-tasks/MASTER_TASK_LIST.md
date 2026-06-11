# Codex Master Task List — CrossPlatform APRS Client

Use this as the project backlog. Give Codex one task at a time. Do not ask Codex to build the whole app in one prompt.

## Cross-cutting architecture rules

These rules apply to all phases, including future refactors:
- Add source tagging to all persisted/runtime data models that represent received, generated, imported, replayed, simulated, or transmitted data.
- Keep internal domain models separate from future public DTOs/contracts. Internal models may evolve for app behavior; public contracts must be explicit, versionable, and mapped through adapters.
- Keep transmit safety centralized. APRS-IS, RF/TNC, object, message, beacon, and weather transmit flows must go through shared safety gates rather than each feature inventing its own checks.
- Keep weather, GPS, APRS-IS, RF/TNC, replay, simulation, and future inputs modular behind driver/service abstractions.
- Avoid hardwiring services directly into UI views. UI should consume view models and application services so inputs/transports can be swapped, tested, or run headless later.
- Current phases must keep data models modular, tag all incoming packet/weather/GPS/import data with source information, keep transmit safety centralized, and avoid tightly coupling UI directly to packet/weather/GPS input sources.
- Future extension surfaces must use stable contracts/adapters rather than exposing mutable internal models directly.

## Phase 0 — Repository and build foundation

### Task 0.1 — Create solution structure
Create a .NET 8 solution with these projects:
- Aprs.Core
- Aprs.Transport
- Aprs.Services
- Aprs.Mapping
- Aprs.Desktop
- Aprs.Tests

Add nullable reference types, implicit usings, dependency-injection-friendly project references, and a buildable placeholder desktop app.

Acceptance criteria:
- `dotnet restore` succeeds
- `dotnet build` succeeds
- `dotnet test` succeeds

### Task 0.2 — Add Avalonia desktop shell
Replace the console placeholder with an Avalonia desktop shell.

Initial UI panes:
- Map
- Station List
- Raw Packet Monitor
- Messages
- Objects
- Weather
- Settings

Acceptance criteria:
- App launches on desktop
- No APRS logic is inside the view layer
- ViewModels are separated from Views

---

## Phase 1 — APRS core protocol

### Task 1.1 — Raw AX.25/APRS text line parser
Implement parsing for text-form APRS packets like:
`SOURCE>DEST,PATH1,PATH2:information`

Extract:
- source callsign
- SSID
- destination
- path list
- q construct where present
- information field
- raw line
- validation errors

Acceptance criteria:
- Unit tests cover valid and invalid packet lines
- Parser never throws on malformed input

### Task 1.2 — Position packet parser
Support APRS position formats:
- uncompressed position with timestamp
- uncompressed position without timestamp
- compressed position placeholder, then full support
- position ambiguity
- symbol table and symbol code
- course/speed where present
- altitude where present
- comment field

Acceptance criteria:
- Unit tests with sample fixed and mobile packets
- Latitude/longitude parsed into decimal degrees

### Task 1.3 — Status, comment, and telemetry packet parser
Add parsers for:
- status packets
- telemetry packets
- capability packets
- free-text comments attached to positions

Acceptance criteria:
- Unit tests for each packet type
- Unknown packets are preserved as raw packet records

### Task 1.4 — APRS messages, bulletins, announcements, and queries
Implement packet models and parser support for:
- messages
- message IDs
- ACK/REJ
- bulletins
- announcements
- queries

Acceptance criteria:
- Unit tests for addressed messages and ACK detection
- Parser exposes destination callsign and message ID

### Task 1.5 — Objects and items parser
Implement APRS object and item parsing.

Support:
- live object
- killed object
- item packets
- position/symbol/comment
- owner/source tracking

Acceptance criteria:
- Unit tests for create/update/kill object packets

### Task 1.6 — Weather parser
Implement APRS weather parsing.

Support:
- wind direction/speed/gust
- temperature
- rain values
- humidity
- barometric pressure
- weather station location when included

Acceptance criteria:
- Weather model stores values with units
- Tests cover common weather packet examples

---

## Phase 2 — Station database and live APRS state

### Task 2.1 — Station database service
Create a station database that maintains latest known state per callsign.

Track:
- callsign/SSID
- latest position
- symbol
- status/comment
- last heard time
- path
- source transport
- packet count
- RF vs APRS-IS vs replay source

Acceptance criteria:
- Updates are observable by UI
- Expiration policy is configurable
- Unit tests cover updates and aging

### Task 2.2 — Station history and trails
Track historical positions for moving stations.

Features:
- configurable trail length
- per-station movement history
- export to GPX/CSV later

Acceptance criteria:
- History can be enabled/disabled
- Old history is trimmed safely

### Task 2.3 — Callsign translation and tactical labels
Implement optional aliases/tactical labels.

Features:
- callsign display name override
- tooltip shows real callsign and alias
- import/export translation list

Acceptance criteria:
- Station list and map can show alias or callsign

---

## Phase 3 — APRS-IS

### Task 3.1 — APRS-IS client
Implement APRS-IS TCP client.

Features:
- configurable server and port
- callsign/passcode/app login line
- filter string
- reconnect with backoff
- keepalive handling
- receive-only mode by default

Acceptance criteria:
- Mocked TCP tests for login and reconnect
- Received lines are published to parser pipeline

### Task 3.2 — APRS-IS server manager
Create server list management.

Features:
- default rotate.aprs.net support
- custom server list
- server status display
- connect/disconnect button
- save settings

Acceptance criteria:
- User can add/edit/delete servers
- Connection state is visible

### Task 3.3 — APRS-IS transmit safety
Add internet transmit support with safeguards.

Features:
- disabled by default
- clear indicator when transmit is enabled
- validate callsign/passcode
- prevent accidental RF transmit confusion

Acceptance criteria:
- Cannot transmit unless APRS-IS TX is explicitly enabled

---

## Phase 4 — Map and station display

### Task 4.1 — Basic map display
Add map control to desktop app.

Features:
- pan/zoom
- center on coordinate
- APRS station markers
- callsign labels
- symbol placeholders

Acceptance criteria:
- Stations from database appear on map
- Marker updates when station moves

### Task 4.2 — APRS symbol rendering
Implement APRS symbol table rendering.

Features:
- primary/alternate symbol table
- overlay support
- fallback symbol
- configurable label display

Acceptance criteria:
- Common symbols render correctly
- Unit tests map symbol codes to render metadata

### Task 4.3 — Station detail popup
Clicking a station marker opens details.

Show:
- callsign
- symbol
- lat/lon
- grid square
- distance/bearing from my station
- last heard
- path
- comment/status
- recent packets

Acceptance criteria:
- Popup does not block live updates

### Task 4.4 — Station list window
Create a sortable/filterable station list.

Columns:
- callsign
- tactical label
- symbol
- distance
- bearing
- last heard
- speed/course
- comment
- source

Acceptance criteria:
- Sort by each column
- Filter by text, distance, age, and source

### Task 4.5 — Offline map cache
Implement tile cache.

Features:
- cache tiles as used
- manage cache size
- import/export cache folder
- no internet required after tiles are cached

Acceptance criteria:
- Cached tiles display offline

### Task 4.6 — Offline map download manager
Add map download manager.

Features:
- choose rectangle/county/area
- choose zoom levels
- estimate storage size
- download progress
- support street/topo/image/hybrid providers where license permits

Acceptance criteria:
- User can pre-download incident area
- App warns about provider licensing/terms

---

## Phase 5 — Beaconing and station setup

### Task 5.1 — Station setup profile
Implement station profile settings.

Fields:
- callsign/SSID
- station latitude/longitude
- symbol table/code
- beacon comment
- PHG/DFS optional fields
- fixed/mobile mode

Acceptance criteria:
- Settings persist locally
- Invalid callsigns are rejected

### Task 5.2 — Beacon formatter
Create beacon packet formatter.

Support:
- fixed position beacon
- mobile GPS beacon
- compressed position later
- status text
- path selection
- APRS-IS vs RF destination rules

Acceptance criteria:
- Unit tests verify generated packets

### Task 5.3 — Beacon scheduler
Create scheduler for station beacons.

Features:
- APRS-IS interval
- RF interval
- disabled by default
- manual beacon now button
- rate-limit warnings

Acceptance criteria:
- RF beaconing cannot start accidentally
- Scheduler can be tested without real time delays

### Task 5.4 — SmartBeaconing-style mobile logic
Add optional smart beacon logic.

Features:
- speed-based interval
- turn-angle trigger
- minimum and maximum intervals
- clear safety defaults

Acceptance criteria:
- Unit tests simulate movement and expected beacon decisions

---

## Phase 6 — GPS support

### Task 6.1 — NMEA GPS input
Implement NMEA serial GPS parser.

Support:
- GGA
- RMC
- fix validity
- speed/course
- altitude
- UTC time

Acceptance criteria:
- Tests use sample NMEA sentences

### Task 6.2 — gpsd support for Linux/Raspberry Pi
Add gpsd client transport.

Features:
- connect to local gpsd
- parse TPV reports
- reconnect handling

Acceptance criteria:
- Can be disabled on non-Linux systems

### Task 6.3 — GPS status panel
Display GPS status.

Show:
- fix/no fix
- satellite count if available
- lat/lon
- speed/course
- altitude
- last update

Acceptance criteria:
- Mobile beaconing only uses valid fixes

---

## Phase 7 — Messaging

### Task 7.1 — Message inbox/outbox
Implement APRS messaging UI and service.

Features:
- compose message
- inbox
- outbox
- sent history
- received history
- station picker

Acceptance criteria:
- Messages are stored locally
- UI shows ACK state

### Task 7.2 — ACK/retry engine
Implement APRS message ACK/retry logic.

Features:
- message IDs
- configurable retry count
- configurable retry interval
- ACK detection
- failure state

Acceptance criteria:
- Unit tests cover ACK, timeout, retry, and failure

### Task 7.3 — Bulletins, announcements, and queries
Add UI for APRS bulletins and queries.

Acceptance criteria:
- Bulletins are visibly separate from private messages
- Queries can be disabled for safety

---

## Phase 8 — Objects and items

### Task 8.1 — Object manager
Create object manager service.

Features:
- create object
- update object
- kill object
- adopt object warning
- owner tracking
- object expiration

Acceptance criteria:
- Unit tests cover create/update/kill/adopt

### Task 8.2 — Object editor UI
Add object editor.

Features:
- object name
- symbol
- position
- comment
- transmit interval
- internet/RF transmit selection
- kill/delete button

Acceptance criteria:
- User can place object on map
- User must explicitly enable object transmission

### Task 8.3 — Drag object on map
Support moving objects on the map.

Acceptance criteria:
- Drag updates local object position
- Transmit update requires enabled object beaconing

---

## Phase 9 — RF/TNC support

### Task 9.1 — TCP KISS transport
Implement TCP KISS transport for Direwolf and network TNCs.

Acceptance criteria:
- Connects to configurable host/port
- Encodes/decodes KISS frames
- Tests cover frame escaping

### Task 9.2 — Serial KISS transport
Implement serial KISS TNC support.

Features:
- port selection
- baud rate
- connect/disconnect
- receive/transmit frames

Acceptance criteria:
- Serial code isolated behind interface
- No RF transmit unless enabled

### Task 9.3 — Direwolf helper setup
Add Direwolf profile support.

Features:
- default TCP KISS host/port
- setup notes page
- connection test

Acceptance criteria:
- User can connect to local Direwolf KISS port

### Task 9.4 — AGWPE client
Implement AGWPE network protocol support.

Acceptance criteria:
- Receive packet frames from AGWPE-compatible server
- Transmit only when explicitly enabled

### Task 9.5 — Multiple ports
Support multiple APRS ports.

Examples:
- APRS-IS receive
- RF KISS port
- second RF KISS port
- replay source

Acceptance criteria:
- Station records track source port
- Transmit rules are per-port

---

## Phase 10 — Weather

Phase 10 is not only APRS weather display. It also includes local weather station input, common weather data normalization, APRS weather packet formatting, and safe optional weather beacon transmit.

Design rules:
- Prefer local/offline-capable weather sources when possible
- Keep internet/cloud APIs optional
- Never hardcode user credentials
- Do not store credentials/tokens in plain text if avoidable
- Keep all weather drivers modular so unsupported stations can be added later
- Do not bundle vendor SDKs unless licensing is reviewed
- Keep all weather transmit features disabled by default
- Keep APRS-IS weather transmit and RF weather transmit separate
- Never transmit stale weather data
- Never transmit during unit tests

### Task 10.1 — Weather Station Display
Display APRS weather stations heard over APRS-IS/RF and display local weather station data if configured.

Requirements:
- Show weather station marker on map
- Show weather details panel
- Show wind direction
- Show wind speed
- Show wind gust
- Show temperature
- Show rain last hour
- Show rain last 24 hours
- Show rain since midnight
- Show humidity
- Show barometric pressure
- Show luminosity/solar if available
- Show snow if available
- Show lightning/event information as display/log data if available
- Show weather source
- Show last update time
- Show stale-data warning
- Do not transmit weather packets in this task

Acceptance criteria:
- APRS weather packets update station weather state
- Local weather observations can be displayed if configured
- Missing optional fields display safely
- Stale weather data is visibly indicated
- No weather packet is transmitted

### Task 10.2 — Common Weather Data Model and APRS Weather Formatter
Create one common internal weather observation model that all weather station drivers use.

Weather model should support:
- source name
- source type
- station/device ID
- timestamp
- latitude
- longitude
- wind direction
- wind speed
- wind gust
- temperature
- rain last hour
- rain last 24 hours
- rain since midnight
- humidity
- barometric pressure
- luminosity/solar radiation if available
- UV if available
- snow if available
- lightning count/distance if available
- battery/status/diagnostic fields if available
- raw source payload if available
- stale-data state
- validation errors/warnings

APRS weather formatter should:
- convert the common weather model into APRS weather packets
- support position + weather format
- support weather report without position where appropriate
- reject stale data
- reject invalid weather values
- reject missing required fields
- generate a packet preview
- not transmit anything in this task

Acceptance criteria:
- Common weather observations normalize data from APRS and future local station drivers
- APRS weather packet preview can be generated from valid observations
- Stale, invalid, or incomplete observations are rejected with clear validation errors
- Unit tests cover formatting and validation

### Task 10.3 — Weather Station Input Driver Framework
Create a plugin/driver-style framework for local and network weather station inputs.

Driver framework should support:
- manual weather entry
- file-based weather data import
- serial weather station input
- USB weather station input
- TCP/UDP network weather station input
- HTTP/REST weather station input
- WebSocket weather station input
- weather software file formats
- weather software local web/API outputs
- simulated weather source for testing

Driver framework should include:
- driver name
- driver type
- enabled flag
- connection status
- last observation
- last error
- stale-data threshold
- validation result
- start/stop methods
- configuration model
- unit-testable parser methods
- no real hardware required for tests

Acceptance criteria:
- Weather drivers share a common interface/configuration shape
- Drivers can be started/stopped and report status
- Parser methods can be unit tested without hardware or internet
- No weather packets are transmitted

### Task 10.3A — WeatherFlow Tempest Local UDP Driver
Support WeatherFlow Tempest local UDP broadcast.

Requirements:
- Listen for local UDP broadcast packets from the Tempest hub
- Default UDP port 50222
- Parse Tempest UDP JSON messages
- Support `obs_st` station observations
- Support `rapid_wind` where practical
- Support `evt_precip` rain start events where practical
- Support `evt_strike` lightning events as display/log data first
- Support `device_status` and `hub_status` for diagnostics
- Convert Tempest data into the common weather observation model
- Work without internet when the Tempest hub and computer are on the same LAN/subnet
- Do not require a Tempest cloud API token for local UDP mode
- Do not transmit weather packets automatically
- Add unit tests using sample Tempest UDP JSON messages
- Do not require an actual Tempest station for tests

Tempest mapping should include:
- wind direction
- wind speed
- wind gust
- air temperature
- relative humidity
- barometric pressure
- rain accumulation where available
- solar radiation / illuminance where available
- UV where available
- lightning event count/distance where available
- station timestamp
- device serial number
- hub serial number
- device/hub status

Acceptance criteria:
- Sample Tempest UDP JSON payloads parse into common weather observations
- Local UDP mode does not require internet or cloud tokens
- Lightning and status events are preserved for display/logging
- No weather packets are transmitted

### Task 10.3B — WeatherFlow Tempest Cloud API Driver
Support optional internet-based Tempest data access.

Requirements:
- Optional feature
- Requires internet
- Requires user-provided API token/access token
- Supports remote stations where allowed by the API
- Supports REST current observations where practical
- Supports WebSocket real-time observations where practical
- Never stores access token in plain text if avoidable
- Local UDP mode remains preferred for offline operation
- Do not require live cloud access for tests
- Use fake HTTP/WebSocket services in tests

Acceptance criteria:
- Fake REST/WebSocket services can feed sample Tempest cloud observations
- Missing credentials block cloud access with clear validation errors
- Tokens are not hardcoded or stored in plain text if avoidable

### Task 10.3C — Peet Bros / Peet Brothers ULTIMETER Driver
Support Peet Bros ULTIMETER APRS-ready weather stations.

Requirements:
- Support serial WeatherText-style data where practical
- Support common ULTIMETER models where practical, including ULTIMETER 800, 2100, and related models
- Support 2400/9600 baud options where configurable
- Parse available weather fields into the common weather observation model
- Support direct APRS-ready output recognition where practical
- Support serial-port configuration
- Do not require real Peet Bros hardware for tests
- Use sample serial data strings in tests
- Preserve raw serial payload for troubleshooting
- Do not transmit weather packets automatically

Acceptance criteria:
- Sample Peet Bros serial payloads parse without hardware
- Raw serial payloads are preserved for diagnostics
- APRS-ready output can be recognized where practical
- No weather packets are transmitted

### Task 10.3D — Davis Weather Driver
Support Davis weather stations and WeatherLink-based setups.

Requirements:
- Support WeatherLink v2 API as optional internet/cloud mode
- Support user-provided API credentials/tokens/keys
- Support WeatherLink.com-connected stations where authorized
- Support local serial/IP data logger support where practical if documentation and access are available
- Support Davis Vantage Vue and Vantage Pro2-style data through WeatherLink where practical
- Convert Davis observation fields into the common weather observation model
- Do not require live WeatherLink access for tests
- Use fake HTTP services and sample payloads in tests
- Never store credentials in plain text if avoidable
- Do not transmit weather packets automatically

Acceptance criteria:
- Sample Davis/WeatherLink payloads normalize into the common weather model
- Fake HTTP services cover cloud behavior
- Missing credentials block cloud access safely
- No weather packets are transmitted

### Task 10.3E — Ambient Weather Driver
Support Ambient Weather stations.

Requirements:
- Support Ambient Weather network/API style data where practical
- Support local/network data if available from compatible devices
- Use user-provided API credentials where required
- Convert data into common weather model
- Do not require live Ambient Weather access for tests
- Use fake HTTP/sample payloads in tests
- Do not transmit automatically

Acceptance criteria:
- Sample Ambient Weather payloads normalize into the common weather model
- API credentials are not hardcoded
- Tests do not require live Ambient Weather access

### Task 10.3F — Ecowitt / Fine Offset / GW1000-compatible Driver
Support common Ecowitt/Fine Offset/GW1000-style stations.

Requirements:
- Support local network gateway data where practical
- Support HTTP/custom upload receiver style integration where practical
- Convert observations into common weather model
- Support extra sensors where practical as optional data
- Do not require real hardware for tests
- Do not transmit automatically

Acceptance criteria:
- Sample Ecowitt/Fine Offset/GW1000 payloads normalize into the common weather model
- Extra sensors are preserved as optional data where practical
- Tests do not require hardware

### Task 10.3G — Cumulus MX / WeeWX / Weather Display / Weather Software File Driver
Support weather station software that can already talk to many hardware stations.

Requirements:
- Support file-based imports such as `realtime.txt`-style outputs where practical
- Support JSON/CSV/text weather data files
- Support local HTTP endpoint polling where practical
- Support Cumulus MX, WeeWX, Weather Display, and similar software as integration targets
- Allow user-configurable field mapping if practical
- Detect stale files/data
- Preserve raw input for diagnostics
- Do not require the actual software for tests
- Use sample files/payloads in tests
- Do not transmit automatically

Acceptance criteria:
- Sample realtime.txt, JSON, CSV, and text payloads can be parsed
- Stale files/data are detected
- Raw inputs are preserved for diagnostics
- Tests do not require weather station software

### Task 10.4 — Local Weather Beacon and APRS Weather Transmit Scheduler
Safely transmit local weather station data as APRS weather packets over APRS-IS and/or RF only when explicitly enabled.

Safety requirements:
- disabled by default
- APRS-IS weather transmit and RF weather transmit are separate settings
- stale weather data must not be transmitted
- invalid weather values must be rejected
- station profile/callsign must be valid
- weather source must be selected and valid
- transmit interval must have safe minimum limits
- all transmitted weather packets must be logged
- packet preview must be available before enabling transmit
- no live transmit during tests
- must use existing APRS-IS/RF transmit safety interfaces
- must not bypass global transmit safety settings

Acceptance criteria:
- Weather beaconing remains disabled by default
- APRS-IS and RF weather transmit can be configured separately
- Scheduler refuses stale, invalid, or unsafe observations
- Tests use fake transmit services only

### Task 10.5 — Weather Station Setup UI
Add a UI page for configuring weather station input and weather beacon transmit settings.

UI should include:
- weather source type selector
- source-specific settings panel
- Tempest UDP settings
- Tempest cloud settings
- Peet Bros serial settings
- Davis WeatherLink settings
- Ambient Weather settings
- Ecowitt/Fine Offset/GW1000 settings
- weather software file/import settings
- manual weather entry option
- data preview
- raw payload preview
- last update time
- stale data warning
- diagnostics/status
- APRS weather packet preview
- APRS-IS weather transmit enable
- RF weather transmit enable
- transmit interval
- manual preview button
- manual test transmit button that requires explicit confirmation and respects all safety settings

Acceptance criteria:
- Weather source settings are modular and source-specific
- Packet preview is available without transmit
- Manual test transmit requires explicit confirmation and respects all safety settings
- No weather transmit is enabled by default

### Task 10.6 — Weather Driver Tests and Sample Data
Add a test/sample-data structure for weather station drivers.

Requirements:
- sample Tempest UDP JSON payloads
- sample Peet Bros serial payloads
- sample Davis WeatherLink payloads
- sample Ambient Weather payloads
- sample Ecowitt/Fine Offset/GW1000 payloads
- sample realtime.txt / JSON / CSV weather software files
- parser tests for each supported source
- common weather model normalization tests
- APRS weather packet formatting tests
- stale data tests
- invalid data tests
- no tests should require real hardware, live internet, or real credentials

Acceptance criteria:
- Weather sample data is organized by source type
- Driver parser tests run fully offline
- Normalization, formatting, stale-data, and invalid-data tests cover the common model

---

## Phase 11 — Digipeater and iGate

### Task 11.1 — Receive-only iGate monitor
Show potential iGate activity but do not gate packets yet.

Features:
- RF packet source display
- APRS-IS duplicate detection
- q construct display

Acceptance criteria:
- No gating occurs in this task

### Task 11.2 — RF-to-IS iGate
Implement optional RF-to-APRS-IS gating.

Safety:
- disabled by default
- clear visual indicator
- duplicate suppression
- path/q validation
- no third-party gating mistakes

Acceptance criteria:
- Tests cover duplicate suppression
- User must explicitly enable iGate mode

### Task 11.3 — Digipeater support
Implement optional digipeater function.

Safety:
- disabled by default
- explicit configuration required
- path rules visible
- rate limiting

Acceptance criteria:
- Does not digipeat unless enabled
- Tests cover path decrement/substitution logic

---

## Phase 12 — Logging, replay, and diagnostics

### Task 12.1 — Raw packet log
Store raw packets with timestamp/source.

Acceptance criteria:
- Log can be searched and exported

### Task 12.2 — Decoded event log
Store decoded station/message/object/weather events.

Acceptance criteria:
- UI can show event timeline

### Task 12.3 — Replay mode
Replay saved APRS logs.

Features:
- speed control
- pause/resume
- no transmit in replay mode

Acceptance criteria:
- Replay updates map and station list
- Transmit is locked out during replay

### Task 12.4 — RF diagnostics
Add diagnostics views.

Features:
- packet rate by station
- duplicate packet detection
- path analysis
- heard-via digipeater display
- RF vs APRS-IS comparison

Acceptance criteria:
- Diagnostics do not affect live receive performance

---

## Phase 13 — Alerts and geofencing

### Task 13.1 — Alert rules engine
Create local alert rules.

Examples:
- callsign heard
- station not heard for X minutes
- station enters/leaves area
- APRS-IS disconnected
- TNC disconnected
- bad GPS fix
- high wind/weather threshold

Acceptance criteria:
- Alerts are configurable
- Alerts can be muted

### Task 13.2 — Geofence editor
Draw circles and polygons on the map.

Acceptance criteria:
- Rule engine can detect enter/exit events

---

## Phase 14 — Training and simulation

### Task 14.1 — Simulation source
Generate simulated APRS stations.

Features:
- moving station
- fixed station
- weather station
- message simulation
- object simulation

Acceptance criteria:
- Simulation never transmits externally

### Task 14.2 — Demo/training mode
Create a training mode that uses simulation and replay.

Acceptance criteria:
- Clear banner indicates training mode
- RF and APRS-IS TX are disabled

---

## Phase 15 — Packaging and release

### Task 15.1 — Settings import/export
Allow full app settings backup and restore.

### Task 15.2 — Cross-platform packaging
Create release packages for:
- Windows x64
- Linux x64
- Linux ARM64/Raspberry Pi
- macOS

### Task 15.3 — First-user setup wizard
Wizard steps:
- callsign
- location
- APRS-IS settings
- map cache location
- receive-only test
- optional RF/TNC setup

### Task 15.4 — Documentation
Create user documentation for:
- receive-only APRS-IS operation
- RF/TNC setup
- Direwolf setup
- messaging
- objects
- maps
- beacon safety
- iGate/digipeater safety

---

## Phase 16 — Extension Hooks, Local API, and Architecture Boundaries

Phase 16 prepares the application for long-term maintainability, extension hooks, local API access, WebSocket event streaming, import/export workflows, public DTO boundaries, plugin/driver support, and safer integration of multiple data sources and transmit paths.

### Task 16.1 — Source Tagging Audit
Audit and update all runtime data models so source/origin metadata is preserved consistently.

Models to review include:
- station snapshots
- station trails
- packet logs
- decoded event logs
- APRS messages
- bulletins/announcements/queries
- objects/items
- weather observations
- GPS fixes
- beacon decisions
- transmit logs/results
- replay/simulation events
- map markers and UI row view models where source display is needed

Source tagging should include where practical:
- source type
- source ID/port ID/driver ID
- source display name
- transport/origin such as APRS-IS, RF, TCP KISS, Serial KISS, Direwolf, AGWPE, gpsd, NMEA, weather driver, replay, simulation, manual, or unknown
- received/generated timestamp
- raw source reference or payload where useful for diagnostics

Acceptance criteria:
- No received/generated domain record loses source identity.
- Station, weather, GPS, message, object, and log records can display or export source information.
- Existing tests still pass and new tests verify source preservation.

### Task 16.2 — Internal Model vs Public DTO Boundary
Create a clear boundary between internal app models and future public/export/API DTOs.

Requirements:
- Keep current domain/service models internal to app architecture where possible.
- Add public DTO/contract models only in an explicit contracts/export layer when needed.
- Add mapping/adapters between internal models and public DTOs.
- Avoid exposing mutable internal service models directly as public contracts.
- Prepare versioning strategy for future plugin/API/export contracts.

Acceptance criteria:
- Public DTOs are not the same types as mutable/internal domain models.
- Mapping tests cover representative station, weather, GPS, object, message, and log records.
- Future plugins/importers can target stable contracts without binding to UI or service internals.

### Task 16.3 — Centralized Transmit Safety Service
Consolidate transmit safety into a shared service/policy layer.

Transmit flows covered:
- APRS-IS packets
- RF/TNC packets
- manual beacons
- scheduled beacons
- SmartBeaconing
- APRS messages
- objects/items
- weather beacons
- iGate/digipeater functions

Safety policy should enforce:
- transmit disabled by default
- global transmit safety gate
- APRS-IS transmit separate from RF transmit
- per-port transmit enable
- connected-port requirement
- valid local station profile/callsign
- stale data rejection where applicable
- interval/rate limits
- explicit confirmation for manual test transmit actions
- replay/training-mode transmit lockout
- logging of allowed and blocked transmit attempts

Acceptance criteria:
- Feature-specific transmit code calls the shared safety service.
- Unit tests cover allowed, blocked, stale, disconnected, replay, and confirmation-required cases.
- No feature bypasses global or per-port transmit gates.

### Task 16.4 — Modular Input Driver Registry
Create or refine a registry/factory model for APRS, weather, GPS, replay, and simulation inputs.

Input families:
- APRS-IS
- TCP KISS
- Serial KISS
- Direwolf
- AGWPE
- NMEA GPS
- gpsd
- weather station drivers
- file import
- replay
- simulation
- manual entry

Registry behavior:
- discover/register available drivers
- expose driver metadata and configuration schema where practical
- start/stop drivers through common lifecycle methods
- report connection/status/health
- publish normalized events to services
- allow fake drivers in tests

Acceptance criteria:
- UI and services can enumerate input sources without hardcoding concrete drivers.
- Tests can register fake drivers and verify lifecycle/status/event flow.
- No hardware, internet, or credentials are required for tests.

### Task 16.5 — UI Decoupling and Application Service Composition
Refactor any direct UI-to-transport or UI-to-parser coupling into application services/view models.

Requirements:
- Views should bind to view models only.
- View models should depend on service abstractions rather than concrete transport implementations where practical.
- Long-running driver/client lifecycles should be owned by application services, not views.
- UI screens should remain modular and movable.
- Headless tests should exercise app behavior without launching Avalonia.

Acceptance criteria:
- Major UI sections remain separate views/components.
- No view starts raw transport/network/serial work directly.
- View model tests cover source selection, status display, and command safety behavior.

### Task 16.6 — Architecture Documentation and Enforcement Tests
Document and test architectural boundaries.

Documentation should cover:
- project responsibilities
- source tagging strategy
- internal model vs public DTO strategy
- transmit safety flow
- input driver lifecycle
- UI composition rules

Tests/checks should cover where practical:
- no UI references from Core/Services/Transport/Mapping
- no transport references from Core
- no transmit path without centralized safety result
- DTO mapping behavior
- source tagging behavior

Acceptance criteria:
- Architecture docs are current.
- Boundary tests or lightweight checks catch obvious layering violations.
- Existing build/test suite remains green.

### Task 16.7 — Extension Hook Registry
Create a safe extension hook system for app events and integration points.

Hook categories:
- packet received
- packet parsed
- station updated
- object/item updated
- message received/sent/acknowledged
- weather observation updated
- GPS fix updated
- port connection state changed
- beacon generated
- transmit requested/allowed/blocked
- replay started/stopped
- import/export completed

Requirements:
- Hooks use stable event contracts/DTOs, not mutable internal models.
- Hook payloads include source tags and timestamps.
- Hooks must not bypass transmit safety.
- Hooks must not run directly on UI views.
- Hook failures should be isolated and logged.
- Hooks should be testable without external plugins.

Acceptance criteria:
- Extension hooks can be registered/unregistered through service abstractions.
- Hook events include source metadata.
- Tests verify hook isolation, ordering where important, and safety behavior.

### Task 16.8 — Local API Foundation
Add a local-only API foundation for status, diagnostics, and future integrations.

API areas:
- app health/status
- port/source status
- station list/details
- object/item list/details
- message summaries
- weather observations
- GPS status
- packet logs
- replay state
- transmit safety status

Requirements:
- Disabled by default unless explicitly enabled.
- Bind to loopback/local interfaces by default.
- Use public DTO/contracts only.
- Never expose credentials or secrets.
- Do not expose unsafe transmit endpoints without centralized safety checks and explicit enablement.
- Include versioned route/contract planning.

Acceptance criteria:
- Local API design documents endpoints and DTO boundaries.
- Tests can exercise API handlers without live network dependencies where practical.
- Transmit-related API calls route through centralized safety policy.

### Task 16.9 — WebSocket Event Stream
Add a WebSocket event stream design/foundation for local dashboards and integrations.

Event stream should support:
- packet events
- station updates
- object/item updates
- message events
- weather updates
- GPS updates
- port status updates
- alert events
- replay/training events
- transmit safety events

Requirements:
- Disabled by default unless local API/event streaming is enabled.
- Uses stable event DTOs with source tags.
- Supports subscription/filtering where practical.
- Does not expose mutable internal models.
- Applies rate limiting/backpressure where practical.
- Does not bypass transmit safety.

Acceptance criteria:
- WebSocket event contracts are versionable.
- Tests verify event serialization and source metadata.
- UI is not hardwired directly to the WebSocket implementation.

### Task 16.10 — File Import/Export Framework
Create a unified file import/export framework.

Import/export targets:
- raw APRS packet logs
- decoded event logs
- station lists
- station trails
- object/item data
- messages/bulletins/queries
- weather observations
- GPS tracks/fixes
- tactical labels
- settings/profile backup
- replay files

Requirements:
- Imported records are source-tagged as file/import/replay as appropriate.
- Importers validate data and preserve raw payloads where useful.
- Exporters use public DTO/contracts or explicit export models.
- Do not import credentials from unsafe/plain text files without warnings.
- No import path should trigger transmit automatically.
- File parsing should be testable with sample files.

Acceptance criteria:
- Import/export framework can register file handlers.
- Sample import/export tests run offline.
- Imported data source tags are preserved through station/weather/GPS/message services.

### Task 16.11 — Plugin and Driver Support Foundation
Create a plugin/driver support foundation for future optional integrations.

Plugin/driver areas:
- APRS input transports
- weather station drivers
- GPS providers
- file import/export handlers
- map providers
- alert notifiers
- diagnostics exporters
- simulation sources

Requirements:
- Plugins/drivers use explicit contracts and capability metadata.
- Drivers declare permissions/capabilities such as network, serial, file, GPS, weather, transmit-request, or read-only.
- Transmit-capable drivers cannot bypass centralized safety.
- Drivers report lifecycle state, health, errors, and source identity.
- Tests use fake plugins/drivers and do not require external hardware or services.
- Licensing and trust boundaries are documented before third-party plugin loading is enabled.

Acceptance criteria:
- Plugin/driver registry can enumerate capabilities without instantiating UI views.
- Fake drivers can publish normalized events with source tags.
- Transmit requests from drivers route through centralized safety policy.
- Unsupported drivers can be added later without rewriting UI or core services.
