# Codex Master Task List — CrossPlatform APRS Client

Use this as the project backlog. Give Codex one task at a time. Do not ask Codex to build the whole app in one prompt.

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

### Task 10.1 — Weather station display
Display APRS weather stations.

Features:
- weather marker
- weather details popup
- last weather update
- graph recent values later

Acceptance criteria:
- Weather packets update station state

### Task 10.2 — Local WX beacon support
Add optional local weather beaconing.

Features:
- manual weather input
- file/API input plugin later
- APRS-IS interval
- RF interval
- stale data warning

Acceptance criteria:
- WX transmit disabled by default
- Stale weather does not transmit without warning

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
