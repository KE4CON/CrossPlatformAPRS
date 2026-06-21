#!/usr/bin/env python3
"""manual_ch_19_36.py — Chapters 19–36 + Appendix of the FieldComms User Manual."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from manual_framework import *


def ch19():
    s = chapter(19, 'ICS Logistics Section',
                'http://192.168.50.1/ics/logistics.html')
    s.append(P(
        'Logistics provides all facilities, services, and materials that support the '
        'incident. It owns the communications plan and tracks supplies, food, medical, '
        'facilities, and check-in.'))
    s.append(SP(6))
    s.append(tbl(['TAB', 'HOW TO USE IT'], [
        ['Comms Plan (ICS-205)',
         'Build the radio communications plan. Each row is a channel: function, channel name, '
         'frequency, CTCSS tone, mode, remarks. Click <b>Add Comms Row</b> to add a channel. '
         'Pre-filled with McHenry County Starcom channels.'],
        ['Supply',
         'Log supply requests: item, category, quantity needed, quantity on hand, priority. '
         'A progress bar shows the fill rate. Use <b>Add Supply</b>.'],
        ['Facilities',
         'ICP location, base/camp details, staging area manager, and medical aid station info.'],
        ['Food / Medical (ICS-206)',
         'Meal service log (meal type, count served, menu) plus medical unit leader, '
         'ambulance status, hospital contacts.'],
        ['Check-In (ICS-211)',
         'Personnel check-in list. Records name, ICS position, agency, and arrival time. '
         'Links to the Member Roster for pre-populated entries.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(PB())
    return s


def ch20():
    s = chapter(20, 'ICS Finance / Admin Section',
                'http://192.168.50.1/ics/finance.html')
    s.append(P(
        'Finance/Admin manages all financial aspects of the incident: cost accounting, '
        'time tracking, procurement, and administrative records for reimbursement.'))
    s.append(SP(6))
    s.append(tbl(['TAB', 'HOW TO USE IT'], [
        ['Cost',
         'Log expenditures: category (personnel, equipment, supply, food, transport), '
         'amount, description, vendor, and approver. A running total is shown. Use <b>Add Cost</b>.'],
        ['Time',
         'Log person-hours per operator: name, position, agency, hours worked, hourly rate '
         '(0 = volunteer). Used for reimbursement claims. Use <b>Add Time</b>.'],
        ['Procurement',
         'Track purchase orders: item, vendor, PO number, amount, status '
         '(Requested, Ordered, Delivered, Closed). Use <b>Add Procurement</b>.'],
        ['Admin',
         'Finance/Admin Section Chief info, billing agency, cost-share type, claim deadline, '
         'and supporting documentation notes.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))
    s.append(note(
        'All finance data can be exported to CSV for submission to the agency '
        'finance officer or FEMA reimbursement process. Click <b>Export CSV</b> '
        'on any Finance tab.', 'tip'))
    s.append(PB())
    return s


def ch21():
    s = chapter(21, 'NTS Radiogram Generator',
                'http://192.168.50.1/nts.html')
    s.append(P(
        'Generate properly formatted ARRL National Traffic System radiograms. '
        'The form produces the standard preamble, address block, and text section, '
        'and keeps a traffic log.'))
    s.append(SP(6))
    s.append(P('Creating a Radiogram', H2))
    s += steps([
        'Click <b>Auto-fill Number</b> for the next sequential message number, or enter one.',
        'Set the <b>Precedence</b>: EMERGENCY, PRIORITY, WELFARE, or ROUTINE.',
        'Choose <b>Handling Instructions</b> (HX codes) if needed — HXA through HXF.',
        'Enter <b>Station of Origin</b>, <b>Place of Origin</b>, and click <b>Auto-fill Date/Time</b>.',
        'Enter the addressee name, address, and phone.',
        'Type the message <b>Text</b> in ARRL all-caps style. The Check (word count) calculates automatically.',
        'Enter the <b>Signature</b>, then click <b>Generate Radiogram</b>.',
        'Click <b>Save to Log</b> to keep a copy, then <b>Print</b> for the paper record.',
    ])
    s.append(SP(6))
    s.append(P('Handling Instruction (HX) Codes', H2))
    s.append(tbl(['CODE', 'MEANING'], [
        ['HXA', 'Collect landline delivery authorized up to $ amount'],
        ['HXB', 'Cancel message if not delivered within X hours'],
        ['HXC', 'Report date and time of delivery to originating station'],
        ['HXD', 'Report to originating station the identity of station from which received'],
        ['HXE', 'Delivering station get reply from addressee'],
        ['HXF', 'Hold delivery until (date)'],
        ['HXG', 'Delivery by mail or landline toll call not required'],
    ], widths=[0.8*inch, CW-0.8*inch]))
    s.append(PB())
    return s


def ch22():
    s = chapter(22, 'ICS-213 General Message',
                'http://192.168.50.1/ics213.html')
    s.append(P(
        'The ICS-213 is the standard written message form for inter- and intra-agency '
        'communications on an incident. Use it when you need a written record of a '
        'request, situation update, or resource order.'))
    s.append(SP(6))
    s.append(P('Completing an ICS-213', H2))
    s += steps([
        'Fill in the header: incident name, To, From, position/agency, date/time, and subject.',
        'Click <b>Auto-fill</b> to populate the current date and time.',
        'Type the message in the body.',
        'Click <b>Generate Form</b> to render a print-formatted version.',
        'Use the <b>Print</b> button to produce a field-ready paper copy.',
        'Click <b>Save to Log</b> to keep a copy in the form log.',
    ])
    s.append(SP(4))
    s.append(note(
        'Use the ICS-213 for formal written traffic. For routine spoken radio traffic, '
        'use the Net Control log instead.', 'note'))
    s.append(PB())
    return s


def ch23():
    s = chapter(23, 'ICS-214 Activity Log & ICS-309',
                'http://192.168.50.1/ics214.html')
    s.append(P(
        'The ICS-214 is a unit-level activity log required for every ICS section and '
        'unit. It records personnel assigned and a timestamped log of activities '
        'through the operational period.'))
    s.append(SP(6))
    s.append(P('Completing an ICS-214', H2))
    s += steps([
        'Enter the incident name, operational period, unit name, and unit leader.',
        'Click <b>Add Personnel</b> to list each person assigned to the unit (name, position, agency).',
        'For each activity, click <b>Add Entry</b>, then <b>Auto Timestamp</b> for the current time, and type what happened.',
        'Entries accumulate in time order throughout the period.',
        'Click <b>Generate Form</b> and <b>Print</b> for the incident record. <b>Save Local</b> keeps a copy on the device.',
    ])
    s.append(SP(8))
    s.append(P('ICS-309 Communications Log', H2))
    s.append(P(
        'The companion ICS-309 page (Dashboard → ICS mode → ICS-309 Comms Log) records '
        'a formal communications log for the operational period. Each entry has a '
        'timestamp, from, to, and message subject. Click <b>Save to Incident</b> to '
        'file it with the active incident for after-action review.'))
    s.append(SP(4))
    s += steps([
        'Click <b>Add (timestamp now)</b> to add a row with the current UTC time.',
        'Fill in From, To, and the message Subject for each entry.',
        'Click <b>Generate Form</b> to render the printable ICS-309.',
        'Click <b>Save to Incident</b> to file it in the incident record.',
    ])
    s.append(PB())
    return s


def ch24():
    s = chapter(24, 'Winlink Form Import & Incident Archiving',
                'http://192.168.50.1/winlink-import.html')
    s.append(P(
        'Winlink Express has its own built-in ICS forms. This chapter explains how to '
        'bring that form data into the FieldComms server so the whole incident is '
        'documented and archived in one place — and how to re-print a received '
        'ICS-213, ICS-214, or ICS-309 on the Pi.'))
    s.append(SP(6))
    s.append(P('Step-by-Step Import', H2))
    s += steps([
        'In Winlink Express, open the ICS form message (sent or received).',
        'Right-click the <b>RMS_Express_Form_*.xml</b> attachment and save it to your computer.',
        'On the Winlink Form Import page, drag the saved XML file onto the drop zone, or click Browse.',
        'Click <b>Parse Form Data</b>. The page detects the form type and extracts all fields.',
        'Review the extracted fields in the editable grid. Fix any fields that need correction.',
        'Choose the Incident and Direction (Received/Sent), then click <b>💾 Archive to incident</b>.',
    ])
    s.append(SP(6))
    s.append(tbl(['FORM', 'RE-PRINT ON PI?', 'NOTES'], [
        ['ICS-213 General Message', 'Yes', 'Re-renders as the Pi\'s ICS-213 for printing'],
        ['ICS-214 Activity Log',    'Yes', 'Activity and personnel lines split into rows automatically'],
        ['ICS-309 Comms Log',       'Yes', 'Log rows parsed into the comms log'],
        ['Other Winlink forms',     'Archive only', 'Data captured and archived — no ICS re-print'],
    ], widths=[1.8*inch, 1.0*inch, CW-2.8*inch]))
    s.append(SP(6))
    s.append(P('Recommended Workflow', H2))
    s += steps([
        'Run Winlink traffic in Express as your operators normally do.',
        'At the end of each operational period, collect any RMS_Express_Form_*.xml files from operators.',
        'Import them via the Winlink Form Import page to complete the incident record.',
        'Cross-check the ICS-309 log with the Net Control log for completeness.',
    ])
    s.append(PB())
    return s


def ch25():
    s = chapter(25, 'HF Propagation', 'http://192.168.50.1/propagation.html')
    s.append(P(
        'The propagation page fetches live solar and geomagnetic data from hamqsl.com '
        '(when internet is available) and uses it to estimate current HF band conditions.'))
    s.append(SP(6))
    s.append(P('Reading the Indicators', H2))
    s.append(tbl(['INDICATOR', 'WHAT IT MEANS FOR HF'], [
        ['SFI (Solar Flux)',  'Higher = better high-band propagation. >130 excellent; 90–130 good; <90 40m/80m only.'],
        ['Sunspot Number',    'More sunspots = more solar activity = better HF. Follows the 11-year cycle.'],
        ['A-Index',           'Daily geomagnetic activity. <10 quiet (good HF); 10–30 unsettled; >30 disturbed.'],
        ['K-Index (0–9)',     '3-hour geomagnetic snapshot. ≤2 quiet; 3–4 unsettled; ≥5 storm (HF degraded); ≥7 severe.'],
        ['X-Ray Flux Class',  'Solar flare class. A/B/C minor; M moderate (SID possible); X strong HF blackout risk.'],
        ['Band Condition Bars','Green = good / Amber = fair / Red = poor for each band from 10m through 80m.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(note(
        'When the Pi has no internet connection, the propagation page shows the last '
        'fetched values with a timestamp. For field activations without WAN, check '
        'propagation before departing on a device with internet, then switch to the '
        'offline Pi for the activation.', 'note'))
    s.append(PB())
    return s


def ch26():
    s = chapter(26, 'Repeater Database', 'http://192.168.50.1/repeaters.html')
    s.append(P(
        'The Repeater Database displays repeater data with rich filtering. It works '
        'in three modes: an offline file you load yourself (most reliable), the server '
        'API, or built-in sample data. Real repeater data comes from RepeaterBook.com.'))
    s.append(SP(6))
    s.append(P('The Three Sources', H2))
    s.append(tbl(['SOURCE', 'HOW TO USE IT'], [
        ['Offline File (recommended)',
         'Load a RepeaterBook CSV or JSON export. Drag-and-drop the file onto the drop zone, '
         'or click Browse. Data persists in your browser after the first load. '
         'This needs no API token and is the most dependable method.'],
        ['Server API',
         'Pulls from the FieldComms server if the net manager has run fetch_repeaters.py '
         'to download RepeaterBook data. Requires a RepeaterBook API token.'],
        ['Sample Data',
         'Three placeholder entries (SAMPLE-1/2/3) for testing the interface. '
         'Shows a "not a real repeater" warning. Do not use for operations.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))
    s.append(P('Filtering and Sorting', H2))
    s.append(tbl(['FILTER', 'OPTIONS'], [
        ['Band',  '2m, 70cm, 23cm, 6m, 10m, 1.25m'],
        ['State', 'IL, WI, IN, IA (default), or any US state'],
        ['Affiliation', 'ARES, SKYWARN, RACES, SATERN, EmComm'],
        ['Mode', 'FM, DMR, C4FM/Fusion, D-STAR, P25, NXDN'],
        ['Sort', 'Callsign, Frequency, City, Distance (nearest first)'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(4))
    s.append(note(
        'A systemd timer (repeater-refresh.timer) runs the fetch automatically on '
        'the first of each month at 04:00, as long as the token is saved in the '
        'repeaterbook.env file and the Pi has internet at that time.', 'tip'))
    s.append(PB())
    return s


def ch27():
    s = chapter(27, 'Facilities Directory',
                'http://192.168.50.1/facilities.html')
    s.append(P(
        'Maintain a directory of EOC locations, hospitals, shelters, staging areas, '
        'and command posts. Each entry stores address, coordinates, radio frequencies, '
        'CTCSS tone, contact person, on-site callsign, generator status, ADA access, '
        'capacity, and operational notes.'))
    s.append(SP(6))
    s.append(P('Default Facilities', H2))
    s.append(P(
        'On first startup, FieldComms seeds four McHenry County facilities: '
        'the McHenry County EOC (Woodstock), Centegra Hospital Woodstock, '
        'the McHenry County Fairgrounds staging area, and Centegra Hospital McHenry. '
        'Edit these with your actual operational details.'))
    s.append(SP(6))
    s.append(P('Managing Facilities', H2))
    s += steps([
        'Click <b>+ Add</b> to create a facility, or click any facility card to view its full detail.',
        'In the detail view, click <b>Edit</b> to change fields, or <b>Delete</b> to remove it.',
        'Use <b>Copy Address</b> to copy the street address to clipboard for navigation apps.',
        'Click <b>Export CSV</b> to download the full directory for offline reference.',
    ])
    s.append(PB())
    return s


def ch28():
    s = chapter(28, 'Grid Square Calculator',
                'http://192.168.50.1/grid.html')
    s.append(P(
        'Convert between decimal latitude/longitude and Maidenhead grid squares in '
        'both directions, and calculate distance and bearing between two grid squares. '
        'Supports 4-character (EN52) and 6-character (EN52ab) precision.'))
    s.append(SP(6))
    s.append(P('Using the Calculator', H2))
    s += steps([
        'To convert coordinates to a grid square: enter latitude and longitude, click <b>Calculate from Lat/Lon</b>.',
        'To convert a grid square to coordinates: enter the grid square, click <b>Calculate from Grid</b>.',
        'To use your current location: click <b>Use My Location</b> (requires location permission, or uses the configured/GPS coordinates).',
        'To find distance and bearing: enter two grid squares and click <b>Calculate Distance</b>.',
    ])
    s.append(SP(4))
    s.append(P(
        'The map on the page highlights the grid square on a North America outline '
        'for quick visual reference. McHenry County, IL is in grid square <b>EN52</b>.'))
    s.append(PB())
    return s


def ch29():
    s = chapter(29, 'Radio Cheat Sheets',
                'http://192.168.50.1/cheatsheets.html')
    s.append(P(
        'A quick-reference set of radio and ICS cheat sheets, organized into tabs. '
        'No internet needed — everything is built in.'))
    s.append(SP(6))
    s.append(tbl(['TAB', 'CONTENTS'], [
        ['Phonetic Alphabet', 'NATO phonetics A–Z with pronunciation, plus ITU number pronunciation (Zero, WUN, TOO, TREE, FOW-er, FIFE, SIX, SEV-en, AIT, NIN-er)'],
        ['Q-Codes',           'Common amateur Q-codes (QRM, QRN, QRP, QSL, QTH...) and EmComm net Q-codes (QNI, QNS, QND, QNN...)'],
        ['Prowords',          'Full procedure word reference — ROGER, WILCO, SAY AGAIN, BREAK, OVER, OUT, CORRECTION, SILENCE, AUTHENTICATE, and more, with meanings and examples'],
        ['Band Plan',         '2m and 70cm segments, HF emergency frequencies (ARES, ARRL, IARU, 60m channels), and service bands (MURS, FRS, GMRS, Marine, Aviation)'],
        ['NTS Precedence',    'EMERGENCY / PRIORITY / WELFARE / ROUTINE — definitions, when to use each, and examples'],
        ['ICS Positions',     'Standard ICS command and general staff titles with abbreviations (IC, OSC, PSC, LSC, FSC, SO, IO, LO)'],
        ['CTCSS/DCS Tones',   'Standard CTCSS tone table (67.0–254.1 Hz) and DCS code table for repeater access'],
        ['Signal Reports',    'RST and RS signal report codes, S-meter calibration, and signal quality descriptions'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(PB())
    return s


def ch30():
    s = chapter(30, 'Print Center', 'http://192.168.50.1/printcenter.html')
    s.append(P(
        'The Print Center is a one-stop hub for every printable document, plus a '
        'built-in incident cover-sheet generator.'))
    s.append(SP(6))
    s.append(tbl(['CATEGORY', 'DOCUMENTS'], [
        ['ICS / NTS Forms',   'ICS-213 General Message, ICS-214 Activity Log, NTS Radiogram, Pre-Flight Checklist'],
        ['Reference Cards',   'Phonetic Alphabet, Q-Codes & Prowords, ICS Structure & Forms, CTCSS/DCS & Signal Reports'],
        ['Operations',        'Net Control Log (ICS-309), Starcom Net Log (ICS-309), Member Roster, Resource Board'],
        ['Cover Sheet',       'Generate a formatted IAP cover sheet from incident details'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))
    s.append(P('Generating an Incident Cover Sheet', H2))
    s += steps([
        'Fill in incident name, number, IC, operational period, frequency, location, and situation summary.',
        'Click <b>Generate Cover</b> to preview it in the page.',
        'Click <b>Print Cover</b> to print it in a new window.',
        'Click <b>Clear</b> to reset the form.',
    ])
    s.append(SP(6))
    s.append(P('Connecting a Printer to EMCOMM-NET', H2))
    s.append(P(
        'FieldComms has print buttons on 17 pages. All printing uses the browser '
        'standard print function — it sends the job to whatever printer the '
        'operator\'s browser can reach. Three options are supported:'))
    s.append(SP(4))
    s.append(tbl(['OPTION', 'HOW IT WORKS', 'BEST FOR'], [
        ['A — Own printer',
         'Each operator prints to their own locally connected printer. No Pi setup needed.',
         'Single operator with their own printer'],
        ['B — USB printer via Pi (CUPS)',
         'USB printer plugged into the Pi. CUPS shares it across EMCOMM-NET. '
         'Installed automatically. Admin at http://192.168.50.1:631. '
         'Supports Windows, Mac, iOS AirPrint, Android, Chromebook.',
         'Field activations — one shared printer for all operators'],
        ['C — Network printer',
         'Wi-Fi or Ethernet printer connected directly to EMCOMM-NET. '
         'Devices discover it via Bonjour/mDNS automatically.',
         'Sites with an existing Wi-Fi capable printer'],
    ], widths=[1.3*inch, 2.6*inch, CW-3.9*inch]))
    s.append(SP(4))
    s.append(P('Setting Up Option B — USB Printer via CUPS', H2))
    s += steps([
        'Plug the USB printer into the Pi or powered USB hub.',
        'Open <b>http://192.168.50.1:631</b> from any device on EMCOMM-NET.',
        'Click <b>Administration → Add Printer</b> and log in with the Pi username/password.',
        'Select the printer from Local Printers. Check <b>Share This Printer</b>. Click Continue.',
        'Select the driver, click Add Printer, then print a test page.',
        'Windows: Settings → Printers → Add a printer — it appears automatically on EMCOMM-NET.',
        'iOS/iPad: tap Share → Print in any FieldComms page — AirPrint finds it automatically.',
        'Android: install CUPS Print app → add printer at 192.168.50.1 port 631.',
    ])
    s.append(note(
        'Recommended field printers: <b>Brother HL-L2350DW</b> (laser, excellent Linux support), '
        '<b>Canon PIXMA TR150</b> or <b>HP OfficeJet 200</b> (battery-powered portable options). '
        'See the Installation Guide Step 8 for full setup instructions and the complete '
        'comparison of all three printer connection options.', 'tip'))
    s.append(PB())
    return s


def ch31():
    s = chapter(31, 'Reference Library', 'http://192.168.50.1/refs.html')
    s.append(P(
        'The Reference Library is a document-management system for all field reference '
        'materials — radio manuals, interoperability plans, ICS form packages, SOGs, '
        'agency plans, and training documents. Files are stored on the Pi and '
        'accessible from any device on EMCOMM-NET.'))
    s.append(SP(6))
    s.append(tbl(['TAB', 'CONTENTS'], [
        ['📻 Amateur Radio',     'Radio manuals, frequency plans, ARRL publications, band plans, antenna refs'],
        ['🏛 ICS / Emergency Mgmt','SWIC plans, NIMS docs, ICS form packages, agency SOGs, mutual aid plans'],
        ['📂 All Documents',     'Every uploaded document regardless of category'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))
    s.append(P('Uploading a Document', H2))
    s += steps([
        'Click <b>⬆ Upload Document</b>. A panel slides in from the right.',
        'Drag-and-drop a file or click Browse. Accepts PDF, Word, Excel, PowerPoint, images, KML, ZIP, GPX — up to 200 MB.',
        'Fill in Title, Category, Source, Description, Tags, Revision, and Expiry (if relevant).',
        'Under <b>Show on tab(s)</b>, check Amateur Radio, ICS/EmMgmt, or both.',
        'Click <b>⬆ Upload Document</b>. PDFs get an automatic thumbnail.',
    ])
    s.append(SP(6))
    s.append(P('Finding Documents', H2))
    s += steps([
        'Use the Category filter, tag cloud, or sort options (Newest, Title, Most Downloaded).',
        'Switch between grid and list view using the view toggle.',
        'Click any document to open its detail, then Download, Edit, or Delete.',
    ])
    s.append(PB())
    return s


def ch32():
    s = chapter(32, 'Kiwix Offline Library', 'http://192.168.50.1:8081/')
    s.append(P(
        'Kiwix serves a complete offline reference library from the Pi on port 8081. '
        'Every device on EMCOMM-NET can browse it with no internet. Content is stored '
        'as ZIM files — compressed, self-contained web archives organized into tiers '
        'by size and operational value.'))
    s.append(SP(6))
    s.append(P('Accessing Kiwix', H2))
    s.append(P(
        'Open a browser to <b>http://192.168.50.1:8081</b>, or tap the Kiwix Library '
        'card on the dashboard. Kiwix has a built-in full-text search bar that searches '
        'across all installed content at once — type any symptom, procedure, or topic '
        'and results appear instantly, offline.'))
    s.append(SP(6))
    s.append(P('Content Catalogue', H2))
    s.append(tbl(['TIER', 'CONTENT', 'SIZE', 'BEST FOR'], [
        ['1', 'WikiMed Medical Encyclopedia', '~471 MB', 'Mass-casualty events, medical support'],
        ['1', 'Wikipedia (Mini)',             '~1.2 GB', 'General field reference, briefings'],
        ['1', 'Wikivoyage',                   '~820 MB', 'Maps, local facilities, travel info'],
        ['2', 'iFixit Repair Guides',         '~2.3 GB', 'Equipment repair in the field'],
        ['2', 'Wikipedia (Full EN)',           '~22 GB',  'Complete reference — large download'],
    ], widths=[0.5*inch, 2.0*inch, 0.9*inch, CW-3.4*inch]))
    s.append(SP(6))
    s.append(P('Adding a Custom ZIM', H2))
    s += steps([
        'Download a ZIM from kiwix.org to a device with internet.',
        'Copy it to the Pi: <font face="Courier" size="9">scp mybook.zim fieldcomms@192.168.50.1:/opt/kiwix/zim/</font>',
        'Register it: <font face="Courier" size="9">sudo kiwix-manage /opt/kiwix/library.xml add /opt/kiwix/zim/mybook.zim</font>',
        'Restart: <font face="Courier" size="9">sudo systemctl restart kiwix</font>',
        'Open http://192.168.50.1:8081 — the new content appears.',
    ])
    s.append(PB())
    return s


def ch33():
    s = chapter(33, 'Offline Maps, GPS & Health Monitor')
    s.append(P('This chapter covers three infrastructure features: the offline map '
               'tile system, GPS live position, and the system Health Monitor.'))
    s.append(SP(6))

    s.append(P('32.1  Offline Map Tile System', H2))
    s.append(P(
        'Map tiles are downloaded in advance, stored as MBTiles files on the Pi, '
        'and served locally on port 8083. Both the Tactical APRS Map and Starcom '
        'Resource Map use offline tiles by default. The default source is USGS '
        'Imagery+Topo Hybrid — public-domain satellite imagery with roads, contours, '
        'and place names.'))
    s.append(SP(4))
    s.append(P('Downloading Tiles', H3))
    s += steps([
        'Run <font face="Courier" size="9">sudo bash /opt/fieldcomms/scripts/download_tiles.sh</font> for the interactive menu (106 presets: all Illinois counties, WI/IN/IA border counties, all 50 states).',
        'Search presets: <font face="Courier" size="9">download_tiles.sh --search "mchenry"</font>',
        'Download a preset: <font face="Courier" size="9">download_tiles.sh --area "McHenry County IL" --zoom 8-16</font>',
        'Tiles are stored in /opt/fieldcomms/data/tiles/ and served by the tile server on port 8083.',
    ])
    s.append(SP(8))

    s.append(P('32.2  GPS Live Position', H2))
    s.append(P(
        'If a USB GPS receiver is connected to the Pi (via the powered USB hub), '
        'gpsd provides live coordinates to the tactical map, health monitor, and '
        'NWS alerts. The GPS receiver creates a stable <b>/dev/gps0</b> device via '
        'udev rules installed automatically.'))
    s.append(SP(4))
    s.append(tbl(['CHECK', 'COMMAND'], [
        ['GPS status',      'gpspipe -w -n 5'],
        ['GPS device',      'ls -la /dev/gps0'],
        ['gpsd status',     'sudo systemctl status gpsd'],
        ['Live fix data',   'cgps -s'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(8))

    s.append(P('32.3  Health Monitor', H2))
    s.append(P(
        'The health monitor runs as a background service on port 5051 and feeds '
        'the dashboard sidebar with live system diagnostics. '
        'Raw data is at <b>http://192.168.50.1:5051/health</b>.'))
    s.append(SP(4))
    s.append(tbl(['METRIC', 'NORMAL', 'ACTION IF EXCEEDED'], [
        ['CPU Temperature', '< 70°C',   'Improve ventilation. Pi 5 throttles at 85°C.'],
        ['Memory Usage',    '< 80%',    'Close unused browser tabs; restart non-essential services'],
        ['Disk Usage',      '< 90%',    'Archive old logs; remove unused ZIM files'],
        ['Service Status',  'All green','Red dot = service down. Restart with systemctl.'],
        ['Internet',        'Connected (if avail.)', 'Check Ethernet. Core features work offline.'],
        ['GPS',             'Fix (if attached)', 'No GPS is fine — coordinates configured at install.'],
    ], widths=[1.5*inch, 1.2*inch, CW-2.7*inch]))
    s.append(SP(4))
    s.append(P('Restarting a Stopped Service', H3))
    s.append(P('<font face="Courier" size="8.5">sudo systemctl restart fcc-lookup  '
               '# or: health-monitor, ics-platform, fieldcomms-refs, kiwix, deadmans</font>', Body))
    s.append(PB())
    return s


def ch34():
    s = chapter(34, 'Network Hardware — ASUS RT-BE58 Go & UniFi Switch Flex 2.5G')
    s.append(P(
        'FieldComms v1.0 uses a dedicated Wi-Fi 7 travel router and a 2.5 GbE managed '
        'switch instead of the Pi broadcasting its own Wi-Fi hotspot. This gives every '
        'device on scene a faster, more reliable connection and lets the Pi focus '
        'entirely on serving the FieldComms application.'))
    s.append(SP(6))
    s.append(P('Network Architecture Overview', H2))
    s.append(tbl(['DEVICE', 'ROLE', 'CONNECTION'], [
        ['ASUS RT-BE58 Go',
         'Wi-Fi 7 access point + DHCP server + WAN gateway',
         'WAN: Ethernet uplink or USB tether · LAN: 2.5G to UniFi switch'],
        ['UniFi Switch Flex 2.5G-5',
         '5-port 2.5 GbE wired distribution switch',
         'Port 1 (PoE in): uplink to ASUS router · Ports 2–5: Pi, TNC, EOC laptop, spare'],
        ['Raspberry Pi 5 (16 GB)',
         'FieldComms application server',
         'Wired 2.5 GbE via UniFi switch · Static IP: 192.168.50.1'],
        ['Windows Laptop',
         'Winlink Express + JS8Call + IC-7300',
         'Wi-Fi (EMCOMM-NET) or wired via UniFi switch'],
    ], widths=[1.6*inch, 2.2*inch, CW-3.8*inch]))
    s.append(SP(8))

    s.append(P('33.5  ASUS RT-BE58 Go Setup', H2))
    s += steps([
        'Connect a device to the router (Wi-Fi or Ethernet) and open <b>http://192.168.50.1</b> (default gateway).',
        'Change the LAN IP to <b>192.168.50.1</b> (LAN → LAN IP).',
        'Set the subnet to <b>255.255.255.0</b>.',
        'Set DHCP range to <b>192.168.50.100 – 192.168.50.200</b>.',
        'Disable the router\'s Wi-Fi security on the management interface — the router LAN IP becomes the FieldComms server IP once the Pi is assigned 192.168.50.1 via nmcli.',
        'Set the Wi-Fi SSID to <b>EMCOMM-NET</b> on both 2.4 GHz and 5 GHz bands.',
        'Set a strong WPA3/WPA2 password. Apply.',
    ])
    s.append(SP(4))
    s.append(note(
        'Write down the ASUS router admin password and store it on a USB drive labeled '
        'FIELDCOMMS. If the router is factory-reset in the field you will need it to '
        'reconfigure the LAN subnet and SSID before FieldComms is accessible.', 'warn'))
    s.append(SP(8))

    s.append(P('33.7  Power Budget & Field Deployment Notes', H2))
    s.append(tbl(['DEVICE', 'TYPICAL DRAW', 'NOTES'], [
        ['Raspberry Pi 5 (16 GB)', '~12–25W', 'Higher under load (FCC search, APRS, all services active)'],
        ['ASUS RT-BE58 Go',        '~8–12W',  'USB-C powered — power bank compatible'],
        ['UniFi Switch Flex 2.5G', '~10–18W', 'PoE input from router or separate adapter'],
        ['Raspberry Pi Monitor',   '~5–8W',   'USB-C powered from Pi USB port or separate supply'],
        ['Windows Laptop',         '~30–65W', 'Varies widely — use laptop power supply, not power bank'],
    ], widths=[1.8*inch, 1.1*inch, CW-2.9*inch]))
    s.append(SP(8))

    s.append(P('33.8  Extending Coverage — ASUS AiMesh', H2))
    s.append(P(
        'A single ASUS RT-BE58 Go covers approximately 2,000–2,500 sq ft. '
        'For larger deployments, add one or more AiMesh nodes. All nodes share the '
        'same EMCOMM-NET SSID and 192.168.50.x subnet. Devices roam automatically '
        '— the Pi remains at 192.168.50.1 regardless of which node a device connects through.'))
    s.append(SP(4))
    s.append(tbl(['SCENARIO', 'RECOMMENDED SETUP'], [
        ['Single room EOC (≤ 2,500 sq ft)',        '1× RT-BE58 Go primary only — no extension needed'],
        ['Multi-room / large shelter (2,500–7,500 sq ft)', '1× primary + 1 AiMesh node (wireless or wired backhaul)'],
        ['Large building or campus (> 7,500 sq ft)', '1× primary + 2–3 nodes, wired backhaul recommended'],
        ['Outdoor SAR staging area',                'Primary at command post + battery-powered nodes at field positions'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(SP(4))
    s += steps([
        '<b>Factory reset the node</b>. Hold reset 5–10 seconds until LED flashes.',
        '<b>Power on the node</b> within 30 ft of the primary for initial pairing.',
        'On the primary router: <b>AiMesh → Add AiMesh Node</b>. Select the node and click Connect.',
        '<b>Move the node</b> to its final position once pairing completes.',
        '<b>Test coverage</b> by walking the area with a phone on EMCOMM-NET.',
    ])
    s.append(note(
        'Up to 8 AiMesh nodes are supported. Pairing takes under 5 minutes on site. '
        'For wired Ethernet backhaul, run a CAT 6 cable from any UniFi switch port '
        'to the node LAN port — AiMesh detects the wired connection automatically.', 'tip'))
    s.append(PB())
    return s


def ch35():
    s = chapter(35, 'JS8Call — HF Digital Keyboard Messaging (Windows)')
    s.append(P(
        'JS8Call is a weak-signal HF digital mode designed for keyboard-to-keyboard '
        'messaging, store-and-forward relay, and group nets — all without an internet '
        'connection. It runs on the Windows laptop alongside Winlink Express, connected '
        'to the IC-7300 via USB. The FieldComms dashboard provides a quick-launch card '
        'that opens JS8Call\'s built-in web interface from any device on EMCOMM-NET.'))
    s.append(SP(6))
    s.append(P('What JS8Call Does', H2))
    s.append(tbl(['CAPABILITY', 'DESCRIPTION'], [
        ['Keyboard-to-keyboard', 'Type messages directly to any JS8 station within range — no internet required'],
        ['Store and forward',    'Messages are relayed station-to-station across multiple hops when no direct path exists'],
        ['Group / net messaging','Send a message addressed to a group callsign (e.g. @EMCOMM); any station in the group receives it'],
        ['Heartbeats',           'Periodic automatic transmissions that advertise station presence — great for EmComm awareness'],
        ['APRS-like reporting',  'Station info (grid, frequency, status) reported to JS8Call.info when internet is available'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('Enabling the JS8Call API', H2))
    s += steps([
        'In JS8Call, go to <b>File → Settings</b> (or press F2).',
        'Click the <b>Reporting</b> tab.',
        'Set <b>TCP Server Hostname</b> to <b>0.0.0.0</b> (allows any device on EMCOMM-NET to connect).',
        'Check <b>Enable TCP Server API</b>.',
        'Verify <b>TCP Server Port</b> is set to <b>2442</b>.',
        'Check <b>Accept TCP Requests</b>.',
        'Check <b>Allow setting station information from network</b>.',
        'Click OK. Restart JS8Call for the settings to take effect.',
    ])
    s.append(SP(6))

    s.append(P('Using JS8Call from FieldComms', H2))
    s += steps([
        'Note the Windows laptop\'s IP address on EMCOMM-NET: run <font face="Courier" size="9">ipconfig</font> in Command Prompt and look for the 192.168.50.x address.',
        'On any EMCOMM-NET device, open FieldComms and tap the <b>JS8Call</b> card.',
        'A prompt appears asking for the Windows laptop\'s IP address.',
        'Enter the IP address (e.g. 192.168.50.105). Click OK.',
        'The card opens JS8Call\'s web interface at http://192.168.50.105:2442.',
        'The IP is saved on that device. Future taps open JS8Call directly.',
    ])
    s.append(SP(4))
    s.append(note(
        'Never leave both Winlink Express and JS8Call connected to the IC-7300 in an '
        'active session simultaneously — they will key over each other. '
        'Close or disconnect one before activating the other.', 'warn'))
    s.append(SP(4))
    s.append(P('Recommended JS8Call Frequency', H3))
    s.append(P(
        '<b>7.078 MHz USB-D</b> — the 40m JS8Call calling frequency. '
        'Also used: 14.078 MHz (20m), 3.578 MHz (80m for regional/night operations).'))
    s.append(PB())
    return s


def ch36():
    s = chapter(36, 'ICS Planning P — Operational Planning Cycle',
                'http://192.168.50.1/ics/planningp.html')
    s.append(P(
        'The Planning P page is an interactive guide to the ICS operational planning '
        'cycle. It presents all 15 phases of the Planning P — from the initial incident '
        'through each operational period — with the standard agenda, required ICS forms, '
        'and attendee list for every phase. Access it from the <b>🅿 Planning P</b> tab '
        'on any ICS platform page.'))
    s.append(SP(6))

    s.append(P('The 15 Phases', H2))
    s.append(tbl(['PHASE', 'NAME', 'KEY FORMS'], [
        ['1',  'Incident / Event',                          'ICS-201 (begin)'],
        ['2',  'Notification',                              'ICS-201'],
        ['3',  'Initial Response & Assessment',             'ICS-201'],
        ['4',  'Initial UC Meeting',                        'ICS-201, ICS-202'],
        ['5',  'Incident Brief — ICS-201',                  'ICS-201'],
        ['6',  'IC/UC Develop/Update Objectives Meeting',   'ICS-202'],
        ['7',  'Command & General Staff Meeting/Briefing',  'ICS-202, ICS-203'],
        ['8',  'Preparing for the Tactics Meeting',         'ICS-215, ICS-215A'],
        ['9',  'Tactics Meeting',                           'ICS-215, ICS-215A, ICS-203, ICS-204'],
        ['10', 'Preparing for the Planning Meeting',        'ICS-204, ICS-205, ICS-206, ICS-207, ICS-208'],
        ['11', 'Planning Meeting',                          'ICS-202 through ICS-206'],
        ['12', 'IAP Prep & Approval',                       'ICS-202 through ICS-208 (complete IAP)'],
        ['13', 'Operations Briefing',                       'Complete IAP, ICS-204 by Division'],
        ['14', 'Execute Plan & Assess Progress',            'ICS-214, ICS-209, ICS-309'],
        ['15', 'New Ops Period Begins',                     'ICS-214, ICS-209'],
    ], widths=[0.4*inch, 2.4*inch, CW-2.8*inch]))
    s.append(SP(6))

    s.append(P('Using the Planning P Page', H2))
    s += steps([
        'Open the ICS Platform (http://192.168.50.1/ics/) and click the <b>🅿 Planning P</b> tab.',
        'The reference image of the official Planning P diagram is shown on the left for reference.',
        'The 15 phase buttons are listed in the center panel, organized into five color-coded groups.',
        'Click any phase button to see its details in the right panel.',
    ])
    s.append(SP(6))

    s.append(P('Phase Detail Panel', H2))
    s.append(tbl(['SECTION', 'WHAT IT SHOWS'], [
        ['Standard Agenda', 'Numbered list of the standard agenda items for that meeting or activity'],
        ['Required Forms',  'ICS form numbers as clickable chips — click to open the form directly'],
        ['Who Should Attend', 'List of ICS roles required or optional for that phase, with red/green roster dots showing who is currently checked in'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('The Phase Color Groups', H2))
    s.append(tbl(['COLOR', 'GROUP', 'PHASES', 'ICS PHASE OF PLANNING'], [
        ['Gray',   'Initial Response',           '1–5',   'Stem — initial incident response'],
        ['Yellow', 'Establish Objectives',       '6–7',   'Stem — incident objectives set by IC/UC'],
        ['Red',    'Develop the Plan',           '8–11',  'Loop — tactics through planning meeting'],
        ['Green',  'Prepare & Disseminate',      '12–13', 'Loop — IAP approval and ops briefing'],
        ['Teal',   'Execute, Evaluate & Revise', '14–15', 'Loop — field operations and next period'],
    ], widths=[0.7*inch, 1.6*inch, 0.6*inch, CW-2.9*inch]))
    s.append(SP(4))
    s.append(P('Generating a Briefing Sheet', H2))
    s += steps([
        'Select any phase by clicking its button.',
        'Click <b>Generate briefing sheet</b> in the detail panel.',
        'A printable one-page cover sheet opens with the phase name, agenda, required forms, and an attendance table with signature lines.',
        'Print it for the IAP package or the planning meeting folder.',
    ])
    s.append(note(
        'The Planning P page is a guide, not a workflow enforcer. You do not need to '
        'click through the phases in order. Use it as a quick reference during planning '
        'meetings to ensure nothing is missed — especially on activations where the '
        'planning cycle is compressed.', 'tip'))
    s.append(PB())
    return s


def ch_appendix():
    s = chapter(34, 'Appendix — Administration & Quick Reference')
    s.append(P('A1  Installation & Updates', H2))
    s.append(tbl(['COMMAND', 'WHAT IT DOES'], [
        ['sudo bash install.sh',          'Interactive installer — sets callsign, coordinates, Wi-Fi, services'],
        ['sudo bash update.sh',           'Updates FieldComms code and restarts services'],
        ['sudo bash kiwix_setup.sh',      'Install/manage Kiwix offline content'],
        ['sudo bash download_tiles.sh',   'Download offline map tiles'],
    ], widths=[2.8*inch, CW-2.8*inch]))
    s.append(SP(8))

    s.append(P('A2  Wi-Fi & Network', H2))
    s.append(tbl(['ITEM', 'DETAIL'], [
        ['SSID',         'EMCOMM-NET'],
        ['Pi IP',        '192.168.50.1 (static, set via nmcli on eth0)'],
        ['DHCP range',   '192.168.50.100 – 192.168.50.200'],
        ['Router admin', 'http://192.168.50.1 (ASUS RT-BE58 Go)'],
        ['CUPS admin',   'http://192.168.50.1:631 (printer management)'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(8))

    s.append(P('A3  Database Backup', H2))
    s.append(P(
        'The main database is a single SQLite file. Back it up by copying '
        '<b>fieldcomms.db</b> to a USB drive. Export the roster CSV monthly '
        'and keep a copy on a USB drive labeled FIELDCOMMS as a secondary backup. '
        'Plugging in a drive labeled FIELDCOMMS automatically triggers a full '
        'rsync backup of the application data via the udev backup rule.'))
    s.append(SP(8))

    s.append(P('A4  Winlink — Email Over Radio', H2))
    s.append(P(
        'MCESV/MCEMA uses <b>Winlink Express</b> as the primary Winlink client on the '
        'Windows laptop with the IC-7300 + VARA HF. '
        'The Pi also runs <b>Pat</b> as a backup browser-based Winlink client on port 8090. '
        'Never run both clients with an active session on the same radio simultaneously.'))
    s.append(SP(8))

    s.append(P('A5  Service & Port Reference', H2))
    s.append(tbl(['SERVICE', 'PORT', 'DESCRIPTION'], [
        ['nginx',              '80',   'Web server — serves all HTML pages'],
        ['fcc-lookup.service', '5050', 'FCC callsign API, net log, forms, DMS, roster, resources'],
        ['health-monitor.service','5051','System health API'],
        ['ics-platform.service','5055','ICS incident platform API'],
        ['fieldcomms-refs.service','5056','Reference library API'],
        ['Graywolf APRS',      '8080', 'APRS client with REST API and WebSocket'],
        ['Kiwix',              '8081', 'Offline library — WikiMed, Wikipedia, iFixit'],
        ['YAAC APRS',          '8082', 'Secondary APRS client'],
        ['Tile server',        '8083', 'Offline map tile server (MBTiles)'],
        ['Pat Winlink',        '8090', 'Browser-based backup Winlink client'],
        ['CUPS printer',       '631',  'Print server — USB printer shared to EMCOMM-NET'],
        ['JS8Call (Windows)',  '2442', 'JS8Call TCP API on Windows laptop'],
    ], widths=[1.8*inch, 0.6*inch, CW-2.4*inch]))
    s.append(PB())
    return s


print("Chapters 19-36 + Appendix module loaded OK")
