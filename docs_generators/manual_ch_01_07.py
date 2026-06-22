#!/usr/bin/env python3
"""manual_ch_01_07.py — Chapters 1–7 of the FieldComms User Manual."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from manual_framework import *


def ch1():
    s = chapter(1, 'Introduction & System Overview')
    s.append(P(
        'FieldComms Incident Management System is a self-contained emergency communications '
        'server that runs on a Raspberry Pi. It provides a complete suite of EmComm tools '
        'accessible through any standard web browser — net control logging, an ICS incident '
        'management platform, APRS mapping, offline reference libraries, Winlink integration, '
        'and ICS form generation. No internet connection is required for any core feature. '
        'It is purpose-built for McHenry County Emergency Services Volunteers and McHenry '
        'County Emergency Management Agency operating under the RACES, ARES, and Starcom '
        'frameworks.'))
    s.append(SP(4))
    s.append(P(
        'The system runs on a Raspberry Pi 5 with 16 GB RAM inside a Pironman MAX 5 tower '
        'enclosure with dual NVMe SSDs in RAID 1. An ASUS RT-BE58 Go Wi-Fi 7 travel router '
        'provides the EMCOMM-NET wireless access point — the Pi itself is a wired server, '
        'not a hotspot. Any smartphone, tablet, or laptop within Wi-Fi range connects to '
        'EMCOMM-NET and reaches the full dashboard at http://192.168.50.1 in under a minute, '
        'with no app installation and no per-device configuration required.'))
    s.append(SP(4))
    s.append(P('How It Works', H2))
    s.append(P(
        'The Pi broadcasts its own Wi-Fi network named <b>EMCOMM-NET</b>. Any '
        'smartphone, tablet, or laptop connects to that network and opens the '
        'dashboard in a browser at <b>http://192.168.50.1</b>. The server hosts '
        'every tool locally. No app needs to be installed on any device.'))
    s.append(SP(4))
    s.append(tbl(['WHAT IT IS', 'DETAIL'], [
        ['A web server', 'nginx serves the dashboard and all 30 tool pages'],
        ['A database', 'SQLite stores members, nets, incidents, resources, forms'],
        ['An API layer', 'Python Flask services on ports 5050–5056 serve live data'],
        ['An offline library', 'Kiwix serves WikiMed, Wikipedia, and reference docs at port 8081'],
        ['An APRS receiver', 'Graywolf and YAAC receive RF APRS packets at ports 8080 and 8082'],
        ['A map tile server', 'Offline USGS tiles served at port 8083 — no internet needed'],
    ], widths=[1.8*inch, CW-1.8*inch]))
    s.append(SP(6))
    s.append(P('Key Principles', H2))
    s += steps([
        '<b>Offline-first</b> — every feature works without internet. Optional WAN connection enables FCC database refresh, NWS alerts, and propagation data.',
        '<b>Browser-based</b> — no app installs. Any device with a modern browser works.',
        '<b>Identity-aware</b> — each operator identifies once and their callsign, Radio ID, or name appears on all log entries.',
        '<b>Multi-user</b> — many operators on many devices simultaneously, all seeing the same live data.',
        '<b>Three dashboard modes</b> — Amateur Radio, Starcom / Public Safety, and ICS Incident Command keep tools organized for the task at hand.',
    ])
    s.append(PB())
    return s


def ch2():
    s = chapter(2, 'Getting Started — Connecting to FieldComms',
                'http://192.168.50.1/')
    s.append(P(
        'Getting on FieldComms takes three steps: connect to the Wi-Fi, open '
        'the dashboard, and identify yourself. The whole process takes under a minute.'))
    s.append(SP(6))
    s.append(P('Step 1 — Connect to the EMCOMM-NET Wi-Fi', H2))
    s.append(P('On your phone, tablet, or laptop, open Wi-Fi settings and connect to:'))
    s.append(SP(4))
    s.append(tbl(['SETTING', 'VALUE'], [
        ['Network Name (SSID)', 'EMCOMM-NET'],
        ['Password', 'Provided by your net manager (default: fieldcomms2026)'],
        ['Security', 'WPA2-PSK'],
        ['Wi-Fi Channel', '6 (2.4 GHz)'],
        ['Your device receives IP', '192.168.50.100 – 192.168.50.200 (automatic)'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s.append(note(
        'The Wi-Fi password is the only access control on FieldComms. Anyone with '
        'the password can use every tool — there is no separate login screen. Keep '
        'the password posted at the EOC for arriving operators and treat it as an '
        'operational credential.', 'note'))
    s.append(SP(8))

    s.append(P('Step 2 — Open the Dashboard', H2))
    s += steps([
        'Open any web browser (Chrome, Safari, Firefox, Edge — all work).',
        'Type <b>http://192.168.50.1</b> in the address bar and press Enter.',
        'The FieldComms dashboard loads. You do not need to install anything.',
    ])
    s.append(SP(8))

    s.append(P('Step 3 — Identify Yourself', H2))
    s.append(P(
        'On first visit, a prompt appears asking for your identity. Enter your '
        '<b>callsign, Radio ID, or name</b> and optionally your ICS position. '
        'This information is saved in your browser and remembered between sessions.'))
    s.append(SP(4))
    s.append(note(
        'You do not need to re-enter your identity every time you visit. '
        'Your browser remembers it until you clear browser storage or tap the '
        'identity badge to change it.', 'tip'))
    s.append(PB())
    return s


def ch3():
    s = chapter(3, 'The Main Dashboard', 'http://192.168.50.1/')
    s.append(P(
        'The dashboard is your central hub for every activation. '
        'The moment you open http://192.168.50.1 in any browser on EMCOMM-NET, '
        'you see the full picture: live NWS weather alerts with severity color coding, '
        'the real-time APRS station table from Graywolf and YAAC, '
        'system health indicators, and the Dead Man Switch state for any active net. '
        'At the very top is the MCESV/MCEMA organization header and your operator identity badge. '
        'The three-button mode switcher below it reorganizes the tool cards to match '
        'the type of operation you are running.'))
    s.append(SP(6))
    s.append(P('Three Dashboard Modes', H2))
    s.append(P(
        'Directly below the header is a three-button mode switcher. It reorganizes '
        'the tool cards to match what you are doing. Your choice is saved on your '
        'device and remembered between sessions.'))
    s.append(SP(4))
    s.append(tbl(['MODE', 'BUTTON', 'WHAT IT EMPHASIZES', 'WHEN TO USE'], [
        ['📻 Amateur Radio', '📻',
         'Net Control, APRS, Winlink, Callsign Lookup, Resource Board, Roster, '
         'DMS, Pre-Flight, NTS/ICS forms, Propagation, Repeaters, Kiwix, Cheat Sheets',
         'ARES/RACES nets, NTS traffic, weekly nets, exercises'],
        ['🚔 Starcom / Public Safety', '🚔',
         'Starcom Net Logger, Weather Net, SAR Net, Observer Mode, Resource Tracking Map, '
         'Resource Board, Member Roster, Facilities, ICS Platform, ICS-213, ICS-214',
         'Starcom activations, public safety nets, weather spotters, SAR operations'],
        ['🏛 ICS / Incident Command', '🏛',
         'ICS Platform (all five sections + Planning P), Tactical Map, Resource Map, '
         'Resource Board, Roster, Facilities, ICS forms, Winlink Import, Repeaters, Cheat Sheets',
         'Formal ICS activations, EOC operations, multi-agency incidents'],
    ], widths=[1.2*inch, 0.5*inch, 2.6*inch, CW-4.3*inch]))
    s.append(SP(8))

    s.append(P('Dashboard Elements', H2))
    s.append(tbl(['ELEMENT', 'DESCRIPTION'], [
        ['Hero bar',          'Station callsign badge, system name, live UTC clock and local 24-hour clock updated every second'],
        ['Mode switcher',     'Three mode buttons — 📻 Amateur Radio / 🚔 Starcom / 🏛 ICS — click to reorganize tool cards'],
        ['NWS Weather Alerts','Live National Weather Service alerts color-coded by severity. Click any alert to expand full details, onset time, expiry countdown, and protective action instructions'],
        ['Operation cards',   'Quick-launch tiles for every tool in the current mode — click to open'],
        ['APRS station table','Live APRS stations heard by Graywolf, with callsign, distance, course/speed, comment, and last heard time. Updates every 30 seconds'],
        ['Status sidebar',    'CPU/memory/disk/temperature, all service status dots (green=running, red=stopped), GPS status, Dead Man\'s Switch state'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))
    s.append(note(
        'The URL parameter <b>?mode=starcom</b> loads the dashboard directly in '
        'Starcom mode — useful for bookmarking on Starcom-dedicated devices.', 'tip'))
    s.append(PB())
    return s


def ch4():
    s = chapter(4, 'Member Roster', 'http://192.168.50.1/roster.html')
    s.append(P(
        'The Member Roster is the authoritative directory for all MCESV/MCEMA '
        'personnel. It tracks every member\'s identifiers, contact information, '
        'certifications, equipment, and deployment activations. It supports both '
        'amateur radio operators and non-ham members.'))
    s.append(SP(6))

    s.append(P('Member Identifiers', H2))
    s.append(P('Every member is tracked by up to three identifiers:'))
    s.append(SP(4))
    s.append(tbl(['IDENTIFIER', 'WHO HAS IT', 'EXAMPLE'], [
        ['ESV Member ID',   'All ESV members',        'ESV-042'],
        ['Starcom Radio ID','All ESV members',         '1042'],
        ['Amateur Callsign','Licensed hams only (blank for non-hams)', 'K9ESV'],
    ], widths=[1.5*inch, 2.0*inch, CW-3.5*inch]))
    s.append(SP(4))
    s.append(note(
        'Non-ham members are full members of the roster. Leave the Callsign field '
        'blank for them — the system uses their Radio ID or Member ID as their '
        'primary identifier automatically.', 'note'))
    s.append(SP(8))

    s.append(P('The Roster Tabs', H2))
    s.append(tbl(['TAB', 'CONTENTS'], [
        ['Directory',     'Full searchable member list with all identifiers, contact info, and role badges'],
        ['Certifications','Check off ICS-100/200/300/400/700/800, EmComm I/II, CERT, First Aid, FEMA IS courses'],
        ['Equipment',     'Check off capabilities: HF/VHF/UHF radio, Winlink, JS8Call, APRS, generator, antenna, laptop, go-kit'],
        ['Activations',   'Check-in log for the current activation. Click + Check In to mark a member as activated. Walk-in check-ins are added here'],
        ['Import/Export', 'Export roster to CSV for backup or sharing. Import from a CSV to bulk-load members'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(8))

    s.append(P('Role Definitions', H2))
    s.append(tbl(['ROLE', 'DESCRIPTION'], [
        ['Net Control (NCS)',         'Primary net controller — manages check-ins and traffic flow'],
        ['Operator',                  'Standard ARES/RACES field operator'],
        ['Liaison',                   'Agency liaison — interface between operators and the served agency'],
        ['Emergency Coordinator (EC)','Oversees ARES/RACES operations for the county'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(8))

    s.append(P('Importing & Exporting (CSV)', H2))
    s += steps([
        'To export: click <b>Export CSV</b>. A file downloads with all members and all columns.',
        'To import: prepare a CSV with these column headers, then click <b>Import CSV</b> and choose the file.',
    ])
    s.append(SP(4))
    s.append(P('<font face="Courier" size="8">member_id, callsign, radio_id, first_name, last_name, role, phone, email, grid, license_class</font>', Body))
    s.append(SP(6))
    s.append(note(
        'The net manager can print wallet-sized access cards for every member, '
        'generated from the roster. Each card shows the Wi-Fi network and password, '
        'the dashboard URL, and the member\'s identifiers. Run: '
        '<font face="Courier" size="9">python3 /opt/fieldcomms/scripts/gen_operator_cards.py '
        '--ssid EMCOMM-NET --password YOUR-PASSWORD</font>. '
        'Output is a print-ready PDF, 10 cards per Avery 5371 sheet.', 'tip'))
    s.append(PB())
    return s


def ch5():
    s = chapter(5, 'Operator Identity System')
    s.append(P(
        'Every FieldComms page tracks who is operating at each device so your '
        'check-ins, log entries, and form signatures are attributed correctly. '
        'There is no password — your identity is stored in your device\'s browser '
        'and remembered between sessions. The system handles all four kinds of '
        'people who show up at an activation.'))
    s.append(SP(6))

    s.append(P('The Four Identity Types', H2))
    s.append(tbl(['TYPE', 'IDENTIFIERS USED', 'BADGE'], [
        ['ESV Member + Ham',         'Member ID + Callsign + Starcom Radio ID',  '📻 K9ESV'],
        ['ESV Member, Non-Ham',      'Member ID + Starcom Radio ID (no callsign)', '🔷 ESV-042'],
        ['Visitor / Mutual Aid, Ham','Callsign + Agency name',                    '📻 W9XYZ'],
        ['Visitor / Mutual Aid, Non-Ham','Name + Agency (+ optional Radio ID)',   '👤 VISITOR'],
    ], widths=[1.8*inch, 2.2*inch, CW-4.0*inch]))
    s.append(SP(4))
    s.append(P(
        'The system always displays the most useful identifier for radio work. '
        'The priority is: callsign first, then Starcom Radio ID, then member ID, '
        'then name.'))
    s.append(SP(8))

    s.append(P('Setting Your Identity', H2))
    s += steps([
        'On first visit, a prompt appears automatically. Enter your callsign, '
        'Radio ID, or name, and optionally your ICS position.',
        'Click <b>Set Identity</b>. Your badge appears in the header.',
        'To change your identity later: click your callsign/name badge in the '
        'header and update the fields.',
    ])
    s.append(SP(6))
    s.append(note(
        'Observer Mode (http://192.168.50.1/observer.html) intentionally does NOT '
        'prompt for identity — it is read-only and requires no identification.', 'note'))
    s.append(PB())
    return s


def ch6():
    s = chapter(6, 'Amateur Net Control Logger',
                'http://192.168.50.1/netcontrol.html')
    s.append(P(
        'The Amateur Net Control Logger is the primary tool for running ARES/RACES '
        'amateur radio nets. When a station checks in, you type their callsign and '
        'press Enter — FieldComms looks up the operator in the local FCC database '
        'and fills their name and license class automatically. '
        'The check-in is timestamped in UTC and saved to the server immediately, '
        'making it visible to all connected devices including served-agency staff '
        'watching in Observer Mode.'))
    s.append(SP(4))
    s.append(P(
        'The logger supports multiple nets running simultaneously, each on its own tab, '
        'each with an independent check-in log, traffic log, and ICS-309 export. '
        'A weekly ARES net, a RACES emergency activation, and an NTS traffic session '
        'can all be logged at the same time with one operator on the keyboard.'))
    s.append(SP(6))

    s.append(P('Starting a Net', H2))
    s += steps([
        'Click <b>+ New Net</b> in the net tabs bar at the top.',
        'Enter a <b>Net Name</b> — for example "McHenry County ARES Thursday Evening Net".',
        'Enter the <b>Frequency</b> — for example "147.015 MHz / 107.2 Hz".',
        'Enter <b>Net Control</b> — your callsign (auto-filled from your identity if set).',
        'Click <b>Activate Net</b>. The net goes live and appears as a tab.',
    ])
    s.append(SP(8))

    s.append(P('The Net Selector Tabs', H2))
    s.append(P(
        'Each active net appears as a tab in the NET TABS bar at the top of the page. '
        'The active net is highlighted. Tap any tab to switch to that net\'s log. '
        'Each net has its own independent check-in log, traffic log, and export.'))
    s.append(SP(8))

    s.append(P('Logging a Check-In', H2))
    s += steps([
        'Type a callsign in the <b>Callsign</b> field and press <b>Enter</b>. '
        'The FCC database fills in the operator\'s name and license class automatically.',
        'Add <b>Location</b> and <b>Remarks</b> if needed.',
        'Click <b>+ Check In</b> or press Enter. The entry appears with a UTC timestamp.',
        'To add a non-licensed or non-US operator: type their name or identifier directly.',
    ])
    s.append(SP(4))
    s.append(note(
        'The <b>+ Roster</b> button only appears for stations not already in the '
        'roster, so you will not create duplicates. Click it to add any new '
        'station to the Member Roster directly from the net log.', 'tip'))
    s.append(SP(8))

    s.append(P('Logging Traffic', H2))
    s += steps([
        'Switch to the <b>Traffic</b> tab.',
        'Enter the From callsign, To callsign or address, traffic type, and a note.',
        'Click <b>Log Traffic</b>. The traffic item is timestamped and recorded with the net.',
    ])
    s.append(SP(8))

    s.append(P('The Roster Chips (Quick Check-In)', H2))
    s.append(P(
        'The Roster tab shows quick-tap chips for known stations. Tap a chip to '
        'instantly log that station\'s check-in without retyping the callsign — '
        'useful for regulars on a weekly net.'))
    s.append(SP(8))

    s.append(P('Sharing & Exporting', H2))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['🔗 Observer Link', 'Copies a read-only URL for the currently selected net. Share it with served-agency staff or EOC viewers — see Chapter 8.'],
        ['ICS-309',          'Exports the selected net\'s log as a formatted ICS-309 Communications Log, ready to print.'],
        ['Export JSON',      'Downloads the full net data as a JSON backup file.'],
        ['Close Net',        'Marks the net closed and archives it. The log is preserved and viewable.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))
    s.append(note(
        'Precedence levels — ROUTINE / WELFARE / PRIORITY / EMERGENCY — can be '
        'set per check-in or traffic entry. Use EMERGENCY only for life-safety traffic. '
        'PRIORITY for time-sensitive but non-emergency messages.', 'note'))
    s.append(PB())
    return s


def ch7():
    s = chapter(7, 'Starcom Net Logger', 'http://192.168.50.1/starcom.html')
    s.append(P(
        'The Starcom Net Logger has its own dedicated dashboard mode — separate from '
        'the Amateur Radio section. Select <b>🚔 Starcom / Public Safety</b> from the '
        'mode bar on the main dashboard to access it. '
        'The module is purpose-built for public safety Starcom radio net logging '
        'and handles the identifiers, terminology, and workflow that public safety '
        'operators use day to day. Units are identified by Radio ID and unit number '
        'rather than amateur callsigns. A dispatch center field tracks which agency '
        'is managing traffic on each channel. Net names use the sc- prefix by convention '
        'so they appear clearly labeled in exports and the Dead Man Switch monitor.'))
    s.append(SP(6))

    s.append(P('Running Multiple Simultaneous Nets', H2))
    s.append(P(
        'The Starcom Net Logger supports multiple simultaneous nets — identical to '
        'the Amateur Net Control Logger. This is particularly useful during large '
        'activations where you may need to run a <b>Starcom General Net</b>, a '
        '<b>Weather Net</b>, and a <b>SAR Net</b> all at the same time, each with '
        'its own independent check-in log and traffic log.'))
    s.append(SP(4))
    s += steps([
        'Click <b>+ New Net</b> to open the first net.',
        'Click <b>+ New Net</b> again for each additional net — Weather Net, SAR Net, etc.',
        'Each open net appears as a clickable badge in the <b>active nets panel</b> on the left sidebar.',
        'Click any net badge to switch to that net. The check-in log and traffic log update to show that net\'s data.',
        'Nets run independently — logging a check-in on one net does not affect the others.',
        'Close each net individually when it is no longer needed.',
    ])
    s.append(SP(4))
    s.append(note(
        'Typical multi-activation scenario: Starcom General Net (command channel) + '
        'Weather Net (storm spotters) + SAR Net (field teams) all open simultaneously. '
        'Net Control switches between them as radio traffic comes in on each channel.',
        'tip'))
    s.append(SP(8))

    s.append(P('Opening a Starcom Net', H2))
    s += steps([
        'Click <b>+ New Net</b>.',
        'Enter the <b>Net Name</b>.',
        'Choose the <b>Net Type</b>: Starcom General / Weather Net / SAR Net / Observer Net.',
        'Enter the <b>Talkgroup</b> and <b>Channel/Frequency</b>.',
        'Enter the <b>Dispatch Center</b> (e.g. MCECC, IDOT). It appears in the net header and stays set for the whole net session.',
        'Click <b>Activate Net</b>.',
    ])
    s.append(SP(8))

    s.append(P('Logging a Unit Check-In', H2))
    s += steps([
        'Enter the <b>Radio ID / Unit #</b> (e.g. 1234).',
        'Enter the <b>Unit Name / Callsign</b> (e.g. "MCHENRY CO ARES" or a callsign).',
        'Choose the status: Check-In, Traffic, Priority Traffic, Emergency, Dispatch, Check-Out, En Route, On Scene, Available, or Out of Service.',
        'Select the talkgroup type and enter the channel/frequency.',
        'Add location and remarks, then click <b>LOG ENTRY</b>. The time is stamped automatically.',
    ])
    s.append(SP(8))

    s.append(P('Exporting & Sharing', H2))
    s.append(P(
        'The Starcom logger shares the same Observer Link, ICS-309 export, and '
        'JSON backup tools as the amateur logger (see Chapter 6). '
        'Exports carry a Starcom header and keep the sc- prefix.'))
    s.append(SP(6))

    s.append(tbl(['FIELD', 'DESCRIPTION'], [
        ['Radio ID',      'Starcom unit number (e.g. 2301, 4710). Required for every check-in.'],
        ['Unit Name',     'Agency and unit description (e.g. "McHenry SO — Unit 12")'],
        ['Dispatch Ctr',  'Dispatching agency or center (e.g. MCECC, IDOT)'],
        ['Net Type',      'Starcom General / Weather Net / SAR Net / Observer Net'],
        ['Talkgroup',     'Radio talkgroup identifier for the net channel'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(PB())
    return s


print("Chapters 1-7 module loaded OK")
