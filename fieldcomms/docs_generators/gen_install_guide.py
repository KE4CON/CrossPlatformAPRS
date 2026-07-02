#!/usr/bin/env python3
"""
gen_install_guide.py — FieldComms Installation Guide Generator
Complete installation guide covering hardware, software, configuration, and reference.
Output: /mnt/user-data/outputs/FieldComms_Installation_Guide.pdf
"""
import datetime, io, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.pdfgen import canvas

# ── Palette ──────────────────────────────────────────────────────────────────
EOC    = HexColor('#1a3a6b')
EOC_LT = HexColor('#2d6ab4')
EOC_BG = HexColor('#eef2f7')
GOLD   = HexColor('#f0c040')
LINE   = HexColor('#c0cfe0')
LGRAY  = HexColor('#f0f3f6')
MGRAY  = HexColor('#e0e8f0')
GREEN  = HexColor('#1a7a3a')
AMBER  = HexColor('#c8760a')
AMBER_BG = HexColor('#fef3d8')
RED    = HexColor('#b82020')
PURPLE = HexColor('#5b2d8c')
MUTED  = HexColor('#4a6080')

ORG    = ('McHenry County Emergency Services Volunteers and '
          'McHenry County Emergency Management Agency')
SHORT  = 'MCESV/MCEMA  ·  K9ESV'
TODAY  = datetime.date.today().strftime('%B %d, %Y')
PAGE_W, PAGE_H = letter
M  = 0.65*inch
CW = PAGE_W - 2*M

# ── Canvas ────────────────────────────────────────────────────────────────────
class NC(canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        total = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            n = self._pageNumber
            if n > 1:
                self.setFillColor(EOC)
                self.rect(0, PAGE_H-0.40*inch, PAGE_W, 0.40*inch, fill=1, stroke=0)
                self.setFillColor(GOLD)
                self.rect(0, PAGE_H-0.42*inch, PAGE_W, 0.02*inch, fill=1, stroke=0)
                self.setFillColor(white)
                self.setFont('Helvetica-Bold', 8)
                self.drawString(M, PAGE_H-0.22*inch, 'FieldComms IMS v1.0')
                self.setFont('Helvetica', 7.5)
                self.drawRightString(PAGE_W-M, PAGE_H-0.22*inch, 'Installation Guide')
            self.setFillColor(EOC)
            self.rect(0, 0, PAGE_W, 0.32*inch, fill=1, stroke=0)
            self.setFillColor(GOLD)
            self.rect(0, 0.32*inch, PAGE_W, 0.015*inch, fill=1, stroke=0)
            self.setFillColor(white)
            self.setFont('Helvetica', 6.5)
            if n > 1:
                self.drawString(M, 0.11*inch,
                    'For Amateur Radio Emergency Communications (EmComm) Use')
                self.drawRightString(PAGE_W-M, 0.11*inch, f'Page {n} of {total}')
            else:
                self.drawCentredString(PAGE_W/2, 0.11*inch,
                    f'FieldComms IMS v1.0  ·  {ORG}  ·  {TODAY}')
            super().showPage()
        super().save()

# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, textColor=black,
             leading=12, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

def P(t, s=None):  return Paragraph(t, s or S('b'))
def SP(n=4):       return Spacer(1, n)
def PB():          return PageBreak()
def HR(c=LINE, t=0.4):
    return HRFlowable(width='100%', thickness=t, color=c, spaceBefore=2, spaceAfter=2)

def H1(t): return P(t, S('h1', fontName='Helvetica-Bold', fontSize=14,
                           textColor=EOC, leading=18, spaceBefore=8, spaceAfter=4))
def H2(t): return P(t, S('h2', fontName='Helvetica-Bold', fontSize=11,
                           textColor=EOC_LT, leading=14, spaceBefore=6, spaceAfter=3))
def H3(t): return P(t, S('h3', fontName='Helvetica-Bold', fontSize=9.5,
                           textColor=EOC, leading=13, spaceBefore=4, spaceAfter=2))

def tbl(headers, rows, widths, hbg=EOC):
    data = [[P(str(h), S('TH', fontName='Helvetica-Bold', fontSize=8,
                           textColor=white, leading=11)) for h in headers]]
    for row in rows:
        data.append([P(str(c), S('TC', fontSize=8.5, leading=12)) for c in row])
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  hbg),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ]))
    return t

def CodeBlock(lines):
    code = '\n'.join(lines)
    t = Table([[P(f'<font face="Courier" size="8">{code}</font>',
                   S('cb', fontSize=8, leading=11, fontName='Courier'))]],
              colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LGRAY),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX',           (0,0), (-1,-1), 0.5, LINE),
    ]))
    return t

def NoteBox(text, kind='note'):
    cfg = {'note': (EOC_LT, EOC_BG, '📝'), 'tip': (GREEN, HexColor('#e4f5ea'), '💡'),
           'warn': (AMBER, AMBER_BG, '⚠'), 'warning': (AMBER, AMBER_BG, '⚠')}
    c, bg, icon = cfg.get(kind, cfg['note'])
    t = Table([[
        P(icon, S('ni', fontSize=11, textColor=c, leading=13)),
        P(text, S('nt', fontSize=8.5, leading=12)),
    ]], colWidths=[0.28*inch, CW-0.28*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',  (0,0), (-1,-1), 5), ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('LINEAFTER',   (0,0), (0,-1),  2, c),
    ]))
    return t

def StepBox(num, title):
    t = Table([[
        P(str(num), S('sn', fontName='Helvetica-Bold', fontSize=22,
                       textColor=white, leading=26, alignment=TA_CENTER)),
        P(title, S('st', fontName='Helvetica-Bold', fontSize=13,
                    textColor=white, leading=17)),
    ]], colWidths=[0.55*inch, CW-0.55*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), EOC_LT),
        ('BACKGROUND',    (1,0), (1,-1), EOC),
        ('TOPPADDING',    (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10), ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW',     (0,0), (-1,-1), 2, GOLD),
    ]))
    return t

def steps(items):
    data = [[
        P('STEP', S('sh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=9)),
        P('ACTION', S('sh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=9)),
    ]]
    for i, item in enumerate(items, 1):
        data.append([
            P(str(i), S('sn2', fontName='Helvetica-Bold', fontSize=9,
                          textColor=EOC_LT, alignment=TA_CENTER, leading=11)),
            P(item, S('sa', fontSize=8.5, leading=12)),
        ])
    t = Table(data, colWidths=[0.38*inch, CW-0.38*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  EOC),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6), ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ]))
    return t

def make_table_style(ncols):
    return TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  EOC),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6), ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ])

def ref_tbl_2col(headers, rows, widths):
    data = [[P(str(h), S('TH', fontName='Helvetica-Bold', fontSize=8.5,
                           textColor=white, leading=11)) for h in headers]]
    for row in rows:
        data.append([P(str(c), S('TC', fontSize=8.5, leading=12)) for c in row])
    t = Table(data, colWidths=widths)
    t.setStyle(make_table_style(2))
    return t

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story.append(SP(50))
cov = Table([[Table([[
    P('FIELDCOMMS', S('ct', fontName='Helvetica-Bold', fontSize=36,
                       textColor=white, alignment=TA_CENTER, leading=42)),
    SP(4),
    P('Incident Management System v1.0',
      S('cs', fontName='Helvetica', fontSize=14, textColor=GOLD,
        alignment=TA_CENTER, leading=18)),
    SP(14),
    HR(GOLD, 0.5),
    SP(8),
    P('Installation Guide',
      S('cg', fontName='Helvetica-Bold', fontSize=22, textColor=white,
        alignment=TA_CENTER, leading=26)),
    SP(8),
    P('ASUS RT-BE58 Go  ·  UniFi Switch  ·  Raspberry Pi 5  ·  Pironman MAX 5',
      S('ch', fontName='Helvetica', fontSize=9, textColor=HexColor('#8090b0'),
        alignment=TA_CENTER, leading=13)),
    SP(18),
    P(f'K9ESV  ·  MCESV/MCEMA  ·  {TODAY}',
      S('cf', fontName='Helvetica', fontSize=9, textColor=HexColor('#6070a0'),
        alignment=TA_CENTER, leading=12)),
]], colWidths=[CW])]], colWidths=[CW])
cov.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), EOC),
    ('TOPPADDING', (0,0), (-1,-1), 50), ('BOTTOMPADDING', (0,0), (-1,-1), 50),
    ('LEFTPADDING', (0,0), (-1,-1), 40), ('RIGHTPADDING', (0,0), (-1,-1), 40),
]))
story.append(cov)
story.append(PB())

# ── TABLE OF CONTENTS ─────────────────────────────────────────────────────────
story.append(H1('Table of Contents'))
story.append(HR(GOLD, 1.0))
story.append(SP(8))

TOC = [
    ('1.', 'Overview & What\'s Included', '3'),
    ('2.', 'Hardware Requirements', '4'),
    ('3.', 'Before You Begin — Prerequisites', '11'),
    ('4.', 'Step 1: Network Hardware Setup', '13'),
    ('5.', 'Step 2: Download & Run the Installer', '16'),
    ('6.', 'Step 3: Installer Configuration Options', '19'),
    ('7.', 'Step 4: Raspberry Pi 5 — Static IP Configuration', '20'),
    ('7b.', 'Step 4b: RAID 1 NVMe Setup — Pironman MAX 5', '22'),
    ('8.', 'Step 5: Kiwix Offline Library Setup', '24'),
    ('9.', 'Step 6: FCC Amateur Database', '26'),
    ('10.', 'Step 7: APRS Setup (Graywolf + YAAC)', '27'),
    ('11.', 'Step 8: Printer Setup', '31'),
    ('12.', 'Step 9: Pat Winlink — Verify & Configure', '36'),
    ('12.', 'Step 10: Windows Laptop — Winlink Express + JS8Call', '37'),
    ('13.', 'Step 11: First Boot Verification', '41'),
    ('14.', 'Network Architecture Reference', '43'),
    ('14.', 'Web Dashboard Reference', '45'),
    ('14.', 'Service & Port Reference', '46'),
    ('15.', 'Maintenance & Updates', '47'),
    ('16.', 'Troubleshooting', '48'),
    ('17.', 'Quick Reference Card', '50'),
]
for num, title, pg in TOC:
    row = Table([[
        P(num, S('tn', fontName='Helvetica-Bold', fontSize=8.5,
                  textColor=EOC_LT, alignment=TA_CENTER, leading=11)),
        P(title, S('tt', fontSize=8.5, leading=11)),
        P(pg, S('tp', fontSize=8.5, leading=11, alignment=TA_CENTER)),
    ]], colWidths=[0.4*inch, CW-0.8*inch, 0.4*inch])
    row.setStyle(TableStyle([
        ('LINEBELOW',     (0,0), (-1,-1), 0.2, LINE),
        ('TOPPADDING',    (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING',   (0,0), (-1,-1), 4), ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(row)
story.append(PB())

# ── SECTION 1 — OVERVIEW ──────────────────────────────────────────────────────
story.append(H1('1. Overview & What\'s Included'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(P(
    'FieldComms is a complete off-grid emergency communications server for Raspberry Pi. '
    'It provides a Wi-Fi access point (EMCOMM-NET) that any phone, tablet, or laptop on scene '
    'can connect to, then access all EmComm tools through a web browser — no internet required. '
    'When Ethernet internet is available, live features such as NWS weather alerts, HF propagation '
    'data, and APRS-IS automatically activate.',
    S('body', fontSize=9.5, leading=14, alignment=TA_JUSTIFY)))
story.append(SP(8))
story.append(tbl(['COMPONENT', 'DESCRIPTION', 'COMPONENT', 'DESCRIPTION'], [
    ['30 Web Pages', 'Full dashboard, net logs, ICS forms, maps, roster, cheat sheets',
     'Dead Man\'s Switch', 'Per-net inactivity monitor with warning and trigger states'],
    ['Net Control Logger', 'Amateur + Starcom nets, FCC autofill, ICS-309 export',
     'Pre-Flight Checklist', 'GO/CAUTION/NO-GO deployment readiness check'],
    ['ICS Platform', 'Command, Operations, Planning, Logistics, Finance sections',
     'HF Propagation', 'Solar indices, band conditions, A/K-index'],
    ['APRS Tactical Map', 'Graywolf + YAAC merged, offline tiles, overlays',
     'Repeater Database', 'RepeaterBook CSV, filter by band, mode, ARES affiliation'],
    ['Member Roster', 'MCESV/MCEMA directory with certs, equipment, activations',
     'Reference Library', 'Upload and serve field reference docs across EMCOMM-NET'],
    ['NTS Radiogram', 'ARRL-formatted radiogram generator with traffic log',
     'Kiwix Library', 'WikiMed, Wikipedia, iFixit — offline at port 8081'],
    ['ICS-213/214/309', 'Fillable ICS forms with print output and incident archiving',
     'FCC Callsign Lookup', '~800K licensees — instant offline search'],
    ['Winlink Form Import', 'Import Winlink Express XML forms to incident archive',
     'Pat Winlink', 'Browser-based backup Winlink client at port 8090'],
    ['JS8Call Integration', 'Dashboard card opens JS8Call web API on Windows laptop',
     'ICS Planning P', 'Interactive 15-phase planning cycle guide'],
], [1.2*inch, 1.8*inch, 1.4*inch, CW-4.4*inch]))
story.append(PB())

# ── SECTION 2 — HARDWARE REQUIREMENTS ────────────────────────────────────────
story.append(H1('2. Hardware Requirements'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(H2('Supported Hardware — Pi Server'))
story.append(tbl(['CONFIGURATION', 'STORAGE', 'NOTES'], [
    ['Pi 5 (16 GB) + Pironman MAX 5 enclosure',
     '2× 1 TB NVMe SSD RAID 1 mirror',
     'Tower form factor with OLED display, active cooling, dual M.2 NVMe slots. '
     'Two 1 TB SSDs configured as RAID 1 — drives mirror each other for data redundancy. '
     'If one SSD fails, the system keeps running on the other with no data loss.'],
], [2.0*inch, 1.4*inch, CW-3.4*inch]))
story.append(SP(6))
story.append(H2('Network Hardware'))
story.append(P('Wi-Fi is provided by the ASUS RT-BE58 Go travel router — the Pi does not run a Wi-Fi hotspot. '
               'The UniFi switch provides wired 2.5 GbE ports for the Pi and other fixed devices.'))
story.append(SP(4))
story.append(tbl(['DEVICE', 'ROLE', 'NOTES'], [
    ['ASUS RT-BE58 Go', 'Wi-Fi 7 access point + DHCP server',
     'Dual-band Wi-Fi 7 (802.11be), 2.5G LAN port, USB-C 18W power.'],
    ['UniFi Switch Flex 2.5G-5', '5-port 2.5 GbE managed switch',
     'PoE powered. Ports: 1=uplink to ASUS, 2=Pi, 3=laptop, 4-5=spare.'],
], [1.6*inch, 1.6*inch, CW-3.2*inch]))
story.append(SP(8))
story.append(H2('Accessories & Cables'))
acc_data = [
    ['ITEM', 'REQUIRED?', 'PURPOSE'],
    ['USB-A drive (32 GB+, labeled FIELDCOMMS)', 'Recommended',
     'Auto-backup trigger — insert to back up all runtime data instantly'],
    ['External USB hard drive 1 TB+ (e.g. LaCie Rugged or LaCie Mobile Drive)', 'Recommended',
     'Incident archive and full system backup. LaCie Rugged is shock/drop/crush resistant. '
     'Label FIELDCOMMS for auto-backup compatibility.'],
    ['USB GPS receiver (u-blox or GlobalSat)', 'Optional',
     'Live position for tactical map and NWS alerts'],
    ['USB TNC — Digirig Mobile or SignaLink USB', 'Optional',
     'Required for APRS transmit/receive via Graywolf or YAAC. '
     'FieldComms assigns a stable /dev/tnc0 device name via udev.'],
    ['Powered USB hub (4- or 7-port, with power supply)', 'Optional',
     'Recommended if connecting GPS + TNC + backup drive simultaneously. '
     'Must be powered — unpowered hubs can cause instability.'],
    ['USB Printer (e.g. Brother HL-L2350DW, HP LaserJet)', 'Optional',
     'Shared across EMCOMM-NET via CUPS (installed automatically). '
     'Or connect a Wi-Fi printer directly to EMCOMM-NET.'],
]
acc_table = Table([[P(c, S('TH' if i==0 else 'TC',
                            fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                            fontSize=8, textColor=white if i==0 else black, leading=11))
                    for c in row] for i, row in enumerate(acc_data)],
                   colWidths=[2.3*inch, 1.0*inch, CW-3.3*inch])
acc_table.setStyle(make_table_style(3))
story.append(acc_table)
story.append(SP(8))

# USB Hub section
story.append(H2('USB Hub & Multi-Device Setup'))
story.append(P('The Pi 5 has four USB ports. A powered USB hub lets you connect GPS, TNC, backup drive, '
               'and other peripherals simultaneously. FieldComms uses udev rules to assign stable device '
               'names regardless of hub port or plug order.'))
story.append(SP(4))
hub_data = [['DEVICE', 'STABLE NAME', 'HOW ASSIGNED', 'SERVICE'],
    ['USB GPS receiver', '/dev/gps0', 'udev rule matches by USB vendor/product ID', 'gpsd → tactical map'],
    ['Digirig Mobile TNC', '/dev/tnc0\n/dev/digirig',
     'udev rule matches by vendor ID + product string "Digirig Mobile". Distinguished from GPS even though both use CP2102 chip.',
     'YAAC / Graywolf APRS'],
    ['SignaLink USB TNC', '/dev/tnc0\n/dev/signalink',
     'udev rule matches by Texas Instruments PCM2904 chip. No conflict with GPS.',
     'YAAC / Graywolf APRS'],
    ['LaCie / USB backup drive (labeled FIELDCOMMS)', '/dev/sdX (auto-mounted)',
     'udev backup rule triggers on label FIELDCOMMS. Drive letter assigned dynamically.',
     'fieldcomms-backup@.service'],
]
hub_t = Table([[P(c, S('TH' if i==0 else 'TC',
                        fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                        fontSize=8, textColor=white if i==0 else black, leading=11))
                for c in row] for i, row in enumerate(hub_data)],
               colWidths=[1.5*inch, 1.0*inch, 2.2*inch, CW-4.7*inch])
hub_t.setStyle(make_table_style(4))
story.append(hub_t)
story.append(SP(6))
story.append(NoteBox(
    'Both the Digirig Mobile TNC and GlobalSat BU-353-S4 GPS use the same USB chip '
    '(Silicon Labs CP2102, vendor 10c4:ea60). FieldComms distinguishes them by USB product '
    'description string. The GPS rule excludes Digirig; the TNC rule requires the Digirig '
    'product string. Verify with: udevadm info -a -n /dev/ttyUSB0 | grep -E "idVendor|idProduct|product"',
    'note'))
story.append(SP(6))
story.append(CodeBlock([
    '# List all USB serial devices',
    'ls -la /dev/ttyUSB* /dev/ttyACM* 2>/dev/null',
    '# Check the stable symlinks',
    'ls -la /dev/gps0 /dev/tnc0 2>/dev/null',
    '# Confirm GPS is outputting NMEA sentences',
    'sudo cat /dev/gps0',
    '# Use /dev/tnc0 in YAAC → Configure → Ports → Serial TNC',
]))
story.append(SP(8))

# Complete BOM
story.append(H2('Complete Bill of Materials'))
story.append(SP(4))
bom_data = [['ITEM', 'MODEL / SPEC', 'WHERE TO BUY']]

def cat_row(title):
    return [P(f'<b>— {title} —</b>',
              S('cat', fontName='Helvetica-Bold', fontSize=8.5, textColor=EOC_LT)),
            P('', S('TC')), P('', S('TC'))]

bom_rows = [
    cat_row('Core Server'),
    ['Raspberry Pi 5 — 16 GB RAM', 'Raspberry Pi 5 Model B (16 GB)', 'raspberrypi.com · Adafruit · PiShop.us'],
    ['Pironman MAX 5 enclosure', 'Pironman MAX 5 (tower, dual NVMe, OLED, fans)', '52pi.com · Amazon'],
    ['NVMe SSD × 2 (for RAID 1)', '1 TB M.2 2280 PCIe Gen 3/4 NVMe (e.g. WD Blue SN580)', 'Amazon · B&H · Newegg'],
    ['Pi 5 USB-C power supply', 'Official Raspberry Pi 27W USB-C PD power supply', 'raspberrypi.com · Adafruit · Amazon'],
    ['MicroSD card (boot / initial RAID setup)', '32 GB Class 10 / A1 microSD', 'Amazon'],
    cat_row('Networking'),
    ['ASUS RT-BE58 Go travel router', 'ASUS RT-BE58 Go (Wi-Fi 7, 2.5G LAN, USB-C power)', 'Amazon · Best Buy · B&H'],
    ['UniFi Switch Flex 2.5G-5', 'Ubiquiti USW-Flex-2.5G-5 (5-port 2.5 GbE)', 'ui.com · Amazon · B&H'],
    ['CAT 6 Ethernet cables × 4', '3 ft – 10 ft CAT 6 patch cables (router→switch, switch→Pi, spares)', 'Amazon · Monoprice'],
    cat_row('Radio & Comms'),
    ['Icom IC-7300 HF transceiver', 'Icom IC-7300 (HF/50 MHz, built-in USB sound card)', 'Ham Radio Outlet · DX Engineering · Amazon'],
    ['USB-A to USB-B cable (IC-7300 to laptop)', 'USB-A to USB-B, shielded, 6 ft', 'Amazon · Monoprice'],
    ['Windows laptop (Winlink Express + JS8Call)', 'Any Windows 10/11 laptop with USB-A port and Wi-Fi', 'Best Buy · Amazon'],
    cat_row('Accessories'),
    ['USB-A drive (32 GB+, labeled FIELDCOMMS)', '32 GB+ USB 3.0 drive — auto-backup trigger when inserted', 'Amazon'],
    ['External USB hard drive 1 TB+ (e.g. LaCie Rugged)', '1 TB+ USB 3.0/USB-C portable — Label FIELDCOMMS', 'B&H · Amazon · Best Buy'],
    ['USB GPS receiver (optional)', 'GlobalSat BU-353-S4 or u-blox USB GPS puck', 'Amazon'],
    ['USB TNC — Digirig Mobile (optional)', 'Digirig Mobile v1.x — USB soundcard + serial CAT in one unit', 'digirig.net · Amazon'],
    ['USB TNC — SignaLink USB (optional)', 'Tigertronics SignaLink USB — rig-specific cable required', 'tigertronics.com · Ham Radio Outlet · Amazon'],
    ['Powered USB hub (optional)', 'Anker 7-Port USB 3.0 with power adapter — powered hub required', 'Amazon · Best Buy'],
    ['USB Printer — laser (recommended)', 'Brother HL-L2350DW or HP LaserJet P1102w — shared via CUPS', 'Best Buy · Amazon'],
    ['USB Printer — portable/battery (optional)', 'Canon PIXMA TR150 or HP OfficeJet 200 — battery-powered', 'Best Buy · Amazon · Office Depot'],
    ['Avery 5371 business card sheets (operator cards)', 'Avery 5371, 10 cards per sheet — laser or inkjet', 'Office Depot · Amazon · Staples'],
]
all_bom = [bom_data[0]] + [[r[0], r[1], r[2]] if len(r)==3 else r for r in bom_rows]
bom_t = Table([[P(str(c), S('TH' if i==0 else 'TC',
                             fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                             fontSize=8, textColor=white if i==0 else black, leading=11))
                for c in row] for i, row in enumerate(all_bom)],
               colWidths=[2.2*inch, 2.5*inch, CW-4.7*inch])
bom_t.setStyle(make_table_style(3))
story.append(bom_t)
story.append(SP(8))

# Mesh BOM
story.append(H2('AiMesh Coverage Extension — Optional Bill of Materials'))
mesh_data = [['ITEM', 'MODEL / SPEC', 'WHERE TO BUY'],
    ['AiMesh node router (wireless backhaul)',
     'ASUS RT-BE58 Go (same as primary — simplest pairing) or any AiMesh-compatible ASUS router',
     'Amazon · Best Buy · B&H'],
    ['AiMesh node router (high-capacity venues)',
     'ASUS ZenWiFi Pro ET12 or RT-AX88U Pro — better range and capacity for large buildings',
     'Amazon · B&H · Costco'],
    ['CAT 6 Ethernet cable (wired backhaul — recommended)',
     'CAT 6 cable from UniFi switch to node LAN port. Length as needed.',
     'Amazon · Monoprice · Home Depot'],
    ['USB-C power bank (field power for node)',
     '10,000+ mAh, 18W+ USB-C PD — one per node for field deployment without shore power',
     'Amazon'],
]
mesh_t = Table([[P(c, S('TH' if i==0 else 'TC',
                         fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                         fontSize=8, textColor=white if i==0 else black, leading=11))
                 for c in row] for i, row in enumerate(mesh_data)],
                colWidths=[1.8*inch, 3.0*inch, CW-4.8*inch])
mesh_t.setStyle(make_table_style(3))
story.append(mesh_t)
story.append(SP(6))
story.append(ref_tbl_2col(['DEPLOYMENT SCENARIO', 'RECOMMENDED SETUP'], [
    ['Single room EOC (≤ 2,500 sq ft)', '1× RT-BE58 Go primary only — no extension needed'],
    ['Multi-room EOC or large shelter (2,500–7,500 sq ft)', '1× RT-BE58 Go primary + 1 AiMesh node (wireless or wired backhaul)'],
    ['Large building or campus (7,500–20,000 sq ft)', '1× primary + 2–3 nodes, wired backhaul recommended for all nodes'],
    ['Outdoor SAR staging area', '1× primary at command post + RT-BE58 Go nodes at field positions on battery'],
], [2.3*inch, CW-2.3*inch]))
story.append(SP(4))
story.append(NoteBox('You do not need to pre-purchase AiMesh nodes for every deployment. '
                     'Start with the primary RT-BE58 Go and add nodes only when coverage is insufficient. '
                     'Pairing a new node takes under 5 minutes on site.', 'tip'))
story.append(SP(8))

# SD card sizing
story.append(H2('SD Card / Storage Sizing Guide'))
story.append(ref_tbl_2col(['TIER', 'WHAT FITS / REQUIREMENT'], [
    ['Minimum (boot only)', '8 GB — OS only, RAID boot loader. FieldComms runs from NVMe RAID.'],
    ['Recommended', '32 GB — OS + swap + logs + temp files during initial RAID setup.'],
    ['Kiwix Tier 1', '~3 GB additional on RAID — WikiMed + Wikipedia Mini + Wikivoyage.'],
    ['Kiwix Tier 2', '~10 GB additional on RAID — adds iFixit, Wikibooks, Wikiversity.'],
    ['FCC Database', '~600 MB on RAID — full US amateur license database (~800K records).'],
], [1.2*inch, CW-1.2*inch]))
story.append(PB())

# ── SECTION 3 — PREREQUISITES ────────────────────────────────────────────────
story.append(H1('3. Before You Begin — Prerequisites'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(P('Complete these prerequisites before running the installer. The installer requires an internet '
               'connection for package downloads, the FCC database, and Kiwix ZIM files. After installation, '
               'the server operates fully offline.'))
story.append(SP(8))
story.append(H2('3.1  Flash the Operating System'))
story.append(tbl(['OS EDITION', 'PROS', 'CONS'], [
    ['Raspberry Pi OS Lite (64-bit) — Recommended for production',
     'Minimal overhead, faster boot, all RAM available to FieldComms services, smaller attack surface',
     'No local browser or GUI — all interaction via SSH or EMCOMM-NET browser'],
    ['Raspberry Pi OS Desktop (64-bit) — Good for setup and troubleshooting',
     'GUI for initial setup, Raspberry Pi Configuration tool, local browser for testing',
     'More RAM used by desktop environment; install takes longer'],
    ['Ubuntu Server 24.04 LTS — Also supported',
     'LTS kernel, familiar to Linux admins, good for organizations standardized on Ubuntu',
     'Slightly larger memory footprint; some package names differ'],
], [2.0*inch, 2.0*inch, CW-4.0*inch]))
story.append(SP(6))
story.append(H2('3.2  First Boot — Initial Setup'))
story.append(steps([
    'On first boot, complete the initial setup wizard: set username to <b>fieldcomms</b>, set a strong password, configure locale and keyboard, expand filesystem.',
    'If using Desktop edition: complete the initial desktop setup wizard.',
    'Enable SSH (Lite only): run <font face="Courier">sudo raspi-config → Interface Options → SSH → Enable</font>',
]))
story.append(SP(6))
story.append(P('Run a full system update before installing FieldComms (works the same on both editions — Terminal or SSH):'))
story.append(SP(4))
story.append(CodeBlock([
    '# Update all packages to latest versions',
    'sudo apt-get update && sudo apt-get full-upgrade -y',
    '# Reboot to apply kernel updates',
    'sudo reboot',
]))
story.append(SP(6))
story.append(H2('3.3  Verify Disk Space'))
story.append(CodeBlock([
    '# Check available space — should show 20GB+ free for Tier 2 install',
    'df -h /',
    '# Verify RAM',
    'free -h',
]))
story.append(SP(6))
story.append(H2('3.4  Internet Connection'))
story.append(P('Connect the Pi to the internet via Ethernet before running the installer. Wi-Fi can be used, '
               'but Ethernet is preferred for downloading large files (FCC database ~600 MB, Kiwix ZIMs up to 25 GB).'))
story.append(SP(4))
story.append(NoteBox(
    'Wi-Fi is provided by the ASUS RT-BE58 Go router — the Pi does NOT run hostapd. '
    'During installation, connect the Pi to the internet via Ethernet through the UniFi switch and ASUS router. '
    'After installation, the Pi is always reachable at 192.168.50.1 via wired Ethernet.', 'note'))
story.append(PB())

# ── STEP 1 — NETWORK SETUP ────────────────────────────────────────────────────
story.append(StepBox(1, 'Network Hardware Setup — ASUS Router + UniFi Switch'))
story.append(SP(8))
story.append(H1('4. Step 1: Network Hardware Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('Complete this step before running the FieldComms installer. The ASUS router must be configured '
               'with the correct LAN subnet (192.168.50.x) before FieldComms is reachable at http://192.168.50.1.'))
story.append(SP(6))
story.append(H2('1.1  Physical Wiring'))
story.append(CodeBlock([
    'ASUS RT-BE58 Go WAN port  →  Ethernet uplink (EOC internet) or leave unplugged for offline',
    'ASUS RT-BE58 Go LAN port  →  UniFi Switch Flex 2.5G-5, Port 1 (uplink)',
    'UniFi Switch Port 2       →  Raspberry Pi 5 Ethernet',
    'UniFi Switch Port 3       →  Windows laptop (optional, or use Wi-Fi)',
    'UniFi Switch Ports 4–5    →  Spare (second TNC, Starlink, etc.)',
    '',
    'Power:',
    '  ASUS router  — USB-C 18W PD adapter or power bank',
    '  UniFi switch — included USB-C 5V/1A adapter (or PoE from uplink)',
    '  Pi 5         — 27W USB-C PD supply via Pironman MAX 5 enclosure PSU',
]))
story.append(SP(6))
story.append(H2('1.2  Configure the ASUS RT-BE58 Go'))
story.append(steps([
    'Power on the router. Connect a device to it via Wi-Fi (default SSID on label) or Ethernet. Open http://192.168.50.1 (or the default router IP on the label).',
    'Complete the router setup wizard. When it asks for WAN, choose Automatic IP (DHCP) or skip if no internet is connected.',
    'Go to <b>LAN → LAN IP</b>. Set the LAN IP to <b>192.168.50.1</b>, subnet <b>255.255.255.0</b>. Apply.',
    'Go to <b>LAN → DHCP Server</b>. Set IP pool: <b>192.168.50.100 – 192.168.50.200</b>. Apply.',
    'Change the ASUS router admin password to something strong. Record it on a piece of paper stored on the FIELDCOMMS USB drive.',
    'Set Manually Assigned IP for the Pi: go to <b>LAN → DHCP Server → Manually Assigned IP</b>. Enter the Pi\'s MAC address → assign IP <b>192.168.50.1</b>. (Or set the Pi\'s static IP manually in Step 4.)',
    'Set the Wi-Fi SSID: go to <b>Wireless → General</b>. Set both the 2.4 GHz and 5 GHz SSIDs to <b>EMCOMM-NET</b>. Set a strong WPA3/WPA2 password. Apply.',
]))
story.append(SP(6))
story.append(tbl(['WAN SOURCE', 'SETTING', 'WHEN TO USE'], [
    ['No WAN (offline only)',    'Leave WAN unplugged', 'Default field posture — all FieldComms tools work without internet'],
    ['Ethernet uplink',          'WAN → Automatic IP', 'EOC with site network — enables NWS alerts, HF prop data, APRS-IS'],
    ['USB smartphone tether',    'Enable tethering on phone, plug into ASUS USB port, WAN → USB', 'Field site with cellular coverage'],
    ['WISP (connect to site Wi-Fi)', 'ASUS Web UI → Operation Mode → WISP', 'Hospital / shelter with guest Wi-Fi available'],
], [1.5*inch, 1.8*inch, CW-3.3*inch]))
story.append(SP(8))
story.append(H2('1.3  AiMesh Coverage Extension (Optional)'))
story.append(steps([
    'Factory reset the node router. Hold reset button for 5–10 seconds until power LED flashes.',
    'Power on the node within 30 ft of the primary router for initial pairing.',
    'On primary router (http://192.168.50.1): go to <b>AiMesh → Add AiMesh Node</b>.',
    'Select the new node. Click Connect. The primary pushes EMCOMM-NET config to the node (1–3 minutes).',
    'Move the node to its final position. Test coverage with a phone on EMCOMM-NET.',
]))
story.append(PB())

# ── STEP 2 — DOWNLOAD & INSTALL ──────────────────────────────────────────────
story.append(StepBox(2, 'Download & Run the FieldComms Installer'))
story.append(SP(8))
story.append(H1('5. Step 2: Download & Run the FieldComms Installer'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(H2('Method A — Direct download to the Pi (requires internet on Pi)'))
story.append(P('<b>Lite:</b> SSH into the Pi and run these commands. '
               '<b>Desktop:</b> open a Terminal window (taskbar → Terminal) and run the same commands.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Create working directory',
    'mkdir -p ~/fieldcomms-install && cd ~/fieldcomms-install',
    '# Download the FieldComms package from GitHub or your storage location',
    'wget -O fieldcomms-v1.zip https://github.com/KE4CON/CrossPlatformAPRS/releases/latest/download/fieldcomms-v1.zip',
    '# Unzip the package',
    'unzip fieldcomms-v1.zip',
    'cd fieldcomms',
]))
story.append(SP(8))
story.append(H2('Method B — Copy from your computer using SCP (Lite/headless)'))
story.append(CodeBlock([
    '# Run this on YOUR COMPUTER, not the Pi',
    'scp fieldcomms-v1.zip fieldcomms@[pi-ip-address]:~/',
    '# Then SSH into the Pi and unzip',
    'ssh fieldcomms@[pi-ip-address]',
    'mkdir -p ~/fieldcomms-install',
    'mv fieldcomms-v1.zip ~/fieldcomms-install/',
    'cd ~/fieldcomms-install && unzip fieldcomms-v1.zip',
    'cd fieldcomms',
]))
story.append(SP(8))
story.append(H2('Method B2 — Download directly on the Pi Desktop (Desktop edition)'))
story.append(tbl(['OPTION', 'HOW'], [
    ['Browser download',
     'Open Chromium on the Pi. Go to the GitHub releases page or download URL. '
     'Download fieldcomms-v1.zip — it saves to ~/Downloads/ automatically.'],
    ['USB drive',
     'Copy fieldcomms-v1.zip to a USB drive. Insert the USB into the Pi. '
     'Open File Manager, drag the zip to your home folder.'],
], [1.3*inch, CW-1.3*inch]))
story.append(SP(4))
story.append(CodeBlock([
    '# If downloaded to ~/Downloads/:',
    'mkdir -p ~/fieldcomms-install',
    'cp ~/Downloads/fieldcomms-v1.zip ~/fieldcomms-install/',
    '# Unzip (same for all methods):',
    'cd ~/fieldcomms-install && unzip fieldcomms-v1.zip',
    'cd fieldcomms',
]))
story.append(SP(8))
story.append(H2('Method C — USB drive transfer (fully offline)'))
story.append(P('<b>Lite:</b> commands below via SSH. '
               '<b>Desktop:</b> use File Manager to copy the zip from USB to your home folder, '
               'then open a Terminal for the unzip step.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Copy fieldcomms-v1.zip to a USB drive on your computer',
    '# Insert USB drive into the Pi, then:',
    'sudo mount /dev/sda1 /mnt   # or check lsblk for your device',
    'cp /mnt/fieldcomms-v1.zip ~/fieldcomms-install/',
    'cd ~/fieldcomms-install && unzip fieldcomms-v1.zip',
    'cd fieldcomms',
]))
story.append(SP(6))
story.append(H2('Launch the Installer'))
story.append(P('<b>Lite:</b> run via SSH. '
               '<b>Desktop:</b> open a Terminal window from the taskbar or Accessories → Terminal. '
               'The installer runs identically on both.'))
story.append(SP(4))
story.append(CodeBlock([
    'cd ~/fieldcomms-install/fieldcomms',
    'sudo bash scripts/install.sh',
]))
story.append(PB())

# ── STEP 3 — INSTALLER CONFIGURATION ─────────────────────────────────────────
story.append(StepBox(3, 'Installer Configuration Options'))
story.append(SP(8))
story.append(H1('6. Step 3: Installer Configuration Options'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(tbl(['PROMPT', 'DEFAULT', 'DESCRIPTION'], [
    ['Station callsign', 'W8ABC', 'Your amateur callsign. Patched into all HTML pages.'],
    ['Station latitude', '42.3153', 'Decimal degrees. Used for APRS station marker, NWS alerts, propagation, distance calc.'],
    ['Station longitude', '-88.4473', 'Decimal degrees (negative = West). Default: Woodstock IL (McHenry County seat).'],
    ['Wi-Fi AP SSID', 'EMCOMM-NET', 'The Wi-Fi network name that field devices connect to.'],
    ['Wi-Fi AP password', 'fieldcomms2026', 'WPA2 password for EMCOMM-NET. Change this for operational security.'],
    ['Server IP address', '192.168.50.1', 'The Pi\'s static IP on EMCOMM-NET. Devices browse to http://192.168.50.1/'],
    ['Download FCC database', 'N', '~600 MB download of the FCC amateur license database. Recommended: Y'],
    ['Kiwix tier', '1', 'Tier 1: WikiMed + Wikipedia Mini + Wikivoyage (~2.5 GB). Tier 2 adds iFixit (~5 GB more).'],
], [1.6*inch, 1.2*inch, CW-2.8*inch]))
story.append(SP(6))
story.append(H2('What the Installer Does Automatically'))
for item in [
    'Installs system packages: Python 3, nginx, kiwix-tools, rsync, gpsd, ufw, mdadm, java',
    'Creates the <b>fieldcomms</b> system user and directory structure at /opt/fieldcomms/',
    'Creates a Python virtual environment and installs Flask, flask-cors, requests, gpsd-py3',
    'Deploys all 30 HTML pages to /opt/fieldcomms/html/ and patches your callsign and coordinates into each file',
    'Installs all 14 systemd service and timer units and enables them at boot',
    'Configures nginx with the correct web root (/opt/fieldcomms/html/) and proxy rules for all API ports',
    '<b>Does NOT configure a Wi-Fi access point</b> — Wi-Fi is handled by the ASUS RT-BE58 Go router. The Pi connects as a wired client only.',
    'Configures the Pi static IP (192.168.50.1/24) on the Ethernet interface (eth0) via NetworkManager',
    'Configures the firewall (ufw) — opens all required ports',
    'Downloads and installs YAAC (Java APRS client) and Graywolf to /opt/yaac/ and /opt/graywolf/',
    'Installs the USB backup udev rule (plug in a USB drive labeled FIELDCOMMS to trigger auto-backup)',
    'Downloads and installs Pat Winlink (browser-based Winlink backup client, port 8090)',
    'Runs the Kiwix ZIM downloader for the selected content tier',
    'Downloads the FEMA ICS forms PDFs to /opt/fieldcomms/data/ics_forms/ (22 forms)',
    'Optionally downloads and builds the FCC amateur license database (~600 MB)',
    'Starts all services and verifies they are running',
]:
    story.append(P(f'• {item}', S('bl', fontSize=8.5, leading=12, leftIndent=14, firstLineIndent=-10)))
story.append(SP(4))
story.append(NoteBox(
    'The ASUS RT-BE58 Go router must be configured before running the installer — see Step 1. '
    'The Pi does NOT run hostapd or dnsmasq. All Wi-Fi, DHCP, and SSID management is handled by the ASUS router.',
    'warning'))
story.append(PB())

# ── STEP 4 — STATIC IP ───────────────────────────────────────────────────────
story.append(StepBox(4, 'Raspberry Pi 5 — Static IP Configuration'))
story.append(SP(8))
story.append(H1('7. Step 4: Raspberry Pi 5 — Static IP Configuration'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('The Pi must always be reachable at 192.168.50.1. If the installer already set this via a DHCP '
               'reservation in the ASUS router, verify with <font face="Courier">ip addr show eth0</font> and '
               'skip to Step 5 if 192.168.50.1/24 is shown.'))
story.append(SP(6))
story.append(H2('Path A — Raspberry Pi OS Lite (SSH)'))
story.append(CodeBlock([
    '# SSH into the Pi (use the IP shown in your router DHCP table)',
    'ssh fieldcomms@[current-pi-ip]',
    '# Find the Ethernet connection name',
    'nmcli con show',
    '# Usually: "Wired connection 1" or "Preconfigured Connection 1"',
    '# Set static IP',
    'sudo nmcli con mod "Wired connection 1" \\',
    '  ipv4.addresses 192.168.50.1/24 \\',
    '  ipv4.method manual',
    '# Apply the change',
    'sudo nmcli con up "Wired connection 1"',
    '# Verify — should show inet 192.168.50.1/24',
    'ip addr show eth0',
]))
story.append(SP(6))
story.append(H2('Path B — Raspberry Pi OS Desktop (GUI)'))
story.append(steps([
    'Click the <b>network icon</b> in the taskbar (top-right corner).',
    'Click <b>Advanced Options → Edit Connections</b>.',
    'Select your <b>Wired connection</b> and click the gear/edit icon.',
    'Click the <b>IPv4 Settings</b> tab.',
    'Change <b>Method</b> from "Automatic (DHCP)" to <b>Manual</b>.',
    'Click <b>Add</b> and enter: Address: 192.168.50.1 · Netmask: 255.255.255.0 · Gateway: (leave blank)',
    'Click <b>Save</b>, then close the Network Connections window.',
    'Disconnect and reconnect the Ethernet cable, or reboot the Pi.',
    'Open the <b>Terminal</b> and verify: <font face="Courier">ip addr show eth0</font> — should show <b>inet 192.168.50.1/24</b>.',
    'Open <b>Chromium</b> on the Pi and go to http://192.168.50.1 to confirm FieldComms loads locally.',
]))
story.append(SP(4))
story.append(NoteBox(
    'Alternatively, open a Terminal on the desktop and use the same nmcli commands shown in Path A. '
    'The terminal method works identically on the Desktop edition.', 'tip'))
story.append(SP(6))
story.append(H2('Path C — raspi-config (if available)'))
story.append(CodeBlock([
    '# Open raspi-config:',
    'sudo raspi-config',
    '# Navigate to: System Options → Network → (set static IP if option is present)',
    '# NOTE: Static IP configuration via raspi-config was removed in Raspberry Pi OS Bookworm.',
    '# If the option is not visible, use Path A (nmcli) or Path B (GUI Network Connections).',
]))
story.append(PB())

# ── STEP 4b — RAID ───────────────────────────────────────────────────────────
story.append(StepBox('4b', 'RAID 1 NVMe Setup — Pironman MAX 5'))
story.append(SP(8))
story.append(H1('7b. RAID 1 NVMe Setup — Pironman MAX 5'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('The Pironman MAX 5 enclosure has two M.2 NVMe slots. Configure them as a RAID 1 mirror so '
               'both drives contain identical data. If one drive fails, the system continues running on the '
               'surviving drive with no data loss and no operator action required.'))
story.append(SP(4))
story.append(NoteBox('Complete this step before running the FieldComms installer. The RAID array must be '
                     'assembled and the OS installed on it before FieldComms is deployed. If your Pi OS is '
                     'already on a single drive, back it up first.', 'warn'))
story.append(SP(6))
story.append(H2('Physical Installation'))
story.append(steps([
    'Install both 1 TB NVMe SSDs into the Pironman MAX 5 M.2 slots. Slot 1 (primary) → /dev/nvme0n1 · Slot 2 (mirror) → /dev/nvme1n1',
    'Boot from a Raspberry Pi OS microSD card for the initial RAID setup. After RAID is built and OS is installed, the SD card is removed.',
]))
story.append(SP(6))
story.append(H2('Build the RAID 1 Array'))
story.append(CodeBlock([
    '# Install mdadm (RAID management tool)',
    'sudo apt-get install -y mdadm',
    '# Create RAID 1 array from the two NVMe drives',
    'sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 \\',
    '  /dev/nvme0n1 /dev/nvme1n1',
    '# Confirm array is building (will show [=>...............] resync progress)',
    'cat /proc/mdstat',
    '# Create a filesystem on the RAID array',
    'sudo mkfs.ext4 -L fieldcomms-raid /dev/md0',
    '# Mount it',
    'sudo mkdir -p /mnt/raid',
    'sudo mount /dev/md0 /mnt/raid',
    '# Copy running OS to RAID array',
    'sudo apt-get install -y rsync',
    'sudo rsync -axv --progress / /mnt/raid/',
    '# Save RAID configuration so it persists across reboots',
    'sudo mdadm --detail --scan | sudo tee -a /mnt/raid/etc/mdadm/mdadm.conf',
]))
story.append(SP(6))
story.append(H2('RAID Health Reference'))
story.append(ref_tbl_2col(['SITUATION', 'WHAT TO DO'], [
    ['Both drives show [UU]', 'Normal healthy state. No action needed.'],
    ['One drive fails — [_U] or [U_]',
     '1. Power down. 2. Remove failed drive. 3. Insert new 1 TB NVMe. 4. Power on. '
     '5. Run: sudo mdadm /dev/md0 --add /dev/nvme1n1. 6. Array rebuilds automatically (~30 min).'],
    ['Check RAID health anytime', 'cat /proc/mdstat  or  sudo mdadm --detail /dev/md0'],
], [1.8*inch, CW-1.8*inch]))
story.append(SP(4))
story.append(NoteBox('RAID 1 protects against drive failure — it is NOT a backup. Both drives contain '
                     'identical data, so accidental deletion or corruption affects both drives simultaneously. '
                     'Continue to use the USB auto-backup (insert FIELDCOMMS USB drive) for regular data backups.', 'warn'))
story.append(PB())

# ── STEP 5 — KIWIX ───────────────────────────────────────────────────────────
story.append(StepBox(5, 'Kiwix Offline Library Setup'))
story.append(SP(8))
story.append(H1('8. Step 5: Kiwix Offline Library Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('Kiwix provides an offline web library served on port 8081. All devices on EMCOMM-NET can browse '
               'it at http://192.168.50.1:8081. Content is packaged as ZIM files.'))
story.append(SP(6))
story.append(tbl(['TIER', 'NAME', 'SIZE', 'DESCRIPTION'], [
    ['1 — Essential', 'WikiMed — Medical Encyclopedia', '~471 MB',
     'Offline medical encyclopedia: symptoms, treatments, drugs, procedures. Critical for mass-casualty events.'],
    ['1 — Essential', 'Wikipedia (Mini)', '~1.2 GB',
     'Compact English Wikipedia — essential facts, geography, science.'],
    ['1 — Essential', 'Wikivoyage', '~820 MB',
     'Emergency shelters, evacuation routes, local resources and travel logistics.'],
    ['2 — Extended', 'Wikibooks — How-To & Field Manuals', '~4.2 GB',
     'First aid, survival, ham radio, electronics, cooking, field skills.'],
    ['2 — Extended', 'iFixit — Equipment Repair Manuals', '~3.1 GB',
     'Step-by-step repair guides for electronics, tools, vehicles.'],
    ['2 — Extended', 'Wikipedia (Full English)', '~22 GB',
     'Complete English Wikipedia. Large download — requires 30 GB+ free.'],
], [0.7*inch, 1.6*inch, 0.9*inch, CW-3.2*inch]))
story.append(SP(6))
story.append(CodeBlock([
    '# Check what is installed and service status',
    'sudo bash /opt/fieldcomms/scripts/kiwix_setup.sh --status',
    '# Add Tier 2 content later (resumes interrupted downloads)',
    'sudo bash /opt/fieldcomms/scripts/kiwix_setup.sh --tier 2',
    '# Service management',
    'sudo systemctl status kiwix',
    'sudo systemctl restart kiwix    # after adding new ZIM files',
]))
story.append(SP(4))
story.append(NoteBox('ZIM downloads are resumable. If a download is interrupted, simply re-run '
                     'kiwix_setup.sh with the same --tier flag. curl will resume from where it stopped.', 'tip'))
story.append(PB())

# ── STEP 6 — FCC ─────────────────────────────────────────────────────────────
story.append(StepBox(6, 'FCC Amateur Database'))
story.append(SP(8))
story.append(H1('9. Step 6: FCC Amateur Database'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('The FCC database provides offline callsign lookup for the entire US amateur license database '
               '(~800,000 licensees). Once built, lookups are instant and completely offline.'))
story.append(SP(6))
story.append(CodeBlock([
    '# If you selected "y" during install, it already ran.',
    '# To build or rebuild manually:',
    'sudo -u fieldcomms \\',
    '  /opt/fieldcomms/venv/bin/python \\',
    '  /opt/fieldcomms/python/build_fcc_db.py',
    '# Automatic weekly refresh timer:',
    'sudo systemctl status fcc-refresh.timer',
    '# Force immediate refresh:',
    'sudo systemctl start fcc-refresh.service',
]))
story.append(PB())

# ── STEP 7 — APRS ────────────────────────────────────────────────────────────
story.append(StepBox(7, 'APRS Setup — Graywolf + YAAC'))
story.append(SP(8))
story.append(H1('10. Step 7: APRS Setup (Graywolf + YAAC)'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('FieldComms supports two simultaneous APRS clients: Graywolf TNC (port 8080) and YAAC — '
               'Yet Another APRS Client (port 8082). Both are optional — FieldComms runs fully without them.'))
story.append(SP(4))
story.append(NoteBox('The FieldComms installer attempts to download and install both YAAC and Graywolf automatically. '
                     'If internet was available during installation, they should already be present. '
                     'Skip to Section 9.3 (YAAC port configuration) if the installer succeeded.', 'info'))
story.append(SP(6))
story.append(H2('9.1  Verify Automatic Installation'))
story.append(CodeBlock([
    '# Check if Java is installed',
    'java -version',
    '# Check if YAAC was installed',
    'ls -lh /opt/yaac/YAAC.jar',
    '# Check if Graywolf was installed',
    'ls -lh /opt/graywolf/graywolf.jar',
    '# Check service status',
    'sudo systemctl status yaac',
    'sudo systemctl status graywolf',
]))
story.append(SP(6))
story.append(H2('9.2  Manual Install — If Automatic Install Failed'))
story.append(CodeBlock([
    '# Step 1 — Install Java runtime (required by both clients)',
    'sudo apt install -y default-jre',
    '# Step 2 — Install YAAC',
    'sudo mkdir -p /opt/yaac',
    'cd /tmp && wget http://www.ka2ddo.org/ka2ddo/YAAC.zip',
    'sudo unzip YAAC.zip "*.jar" -d /opt/yaac/',
    'sudo mv /opt/yaac/YAAC*.jar /opt/yaac/YAAC.jar 2>/dev/null || true',
    'sudo chown -R fieldcomms:fieldcomms /opt/yaac',
    '# Step 3 — Install Graywolf',
    'sudo mkdir -p /opt/graywolf',
    'sudo wget -O /opt/graywolf/graywolf.jar \\',
    '  https://github.com/vk2tds/graywolf/releases/latest/download/graywolf.jar',
    'sudo chown -R fieldcomms:fieldcomms /opt/graywolf',
    '# Step 4 — Enable services',
    'sudo systemctl enable --now yaac',
    'sudo systemctl enable --now graywolf',
]))
story.append(SP(6))
story.append(H2('9.3  YAAC Port Configuration (Required — First Run)'))
story.append(steps([
    'Run YAAC once on a desktop/monitor: <font face="Courier">java -jar /opt/yaac/YAAC.jar</font>',
    'Go to <b>File → Configure → Web Server</b> tab.',
    'Set <b>Port: 8082</b> · Check <b>Enable REST API</b> · Check <b>Enable WebSocket</b> · Click Save.',
    'Close YAAC. The yaac.service will use these settings when running headlessly.',
]))
story.append(SP(6))
story.append(H2('9.4  Connect a TNC or Radio Interface'))
story.append(tbl(['INTERFACE TYPE', 'PORT TYPE IN YAAC', 'SETTINGS'], [
    ['USB TNC (Digirig, SignaLink, etc.)', 'Serial TNC', '/dev/tnc0, baud rate 9600 or 1200'],
    ['KISS TNC over TCP (Direwolf)', 'KISS TNC (TCP)', 'Host: localhost, Port: 8001'],
    ['AGW packet engine (Direwolf)', 'AGW', 'Host: localhost, Port: 8000'],
    ['APRS-IS internet (if WAN connected)', 'APRS-IS', 'Server: noam.aprs2.net:14580, Filter: r/42.31/-88.44/50'],
], [1.5*inch, 1.5*inch, CW-3.0*inch]))
story.append(SP(6))
story.append(H2('9.5  Verify APRS is Working'))
story.append(CodeBlock([
    '# Test YAAC REST API (should return JSON list of heard stations)',
    'curl http://localhost:8082/api/stations',
    '# Test Graywolf REST API',
    'curl http://localhost:8080/api/stations',
    '# Check service logs if no stations appear',
    'journalctl -u yaac -n 30',
    'journalctl -u graywolf -n 30',
]))
story.append(PB())

# ── STEP 8 — PRINTER ─────────────────────────────────────────────────────────
story.append(StepBox(8, 'Printer Setup — Three Connection Options'))
story.append(SP(8))
story.append(H1('11. Step 8: Printer Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('FieldComms has print buttons on 17 pages. All printing uses the browser standard '
               'window.print() function, which sends the job to whatever printer the operator\'s browser '
               'can reach. Three printer connection methods are supported:'))
story.append(SP(6))
story.append(H2('Option A — Client Device Prints to Its Own Printer (Simplest)'))
story.append(P('Each operator\'s laptop or tablet prints to its own locally connected printer. '
               'No Pi configuration needed. Zero setup required — works immediately.'))
story.append(SP(6))
story.append(NoteBox('This is the simplest option and requires zero configuration on the Pi. '
                     'The only requirement is that the operator\'s device has a printer configured.', 'tip'))
story.append(SP(8))
story.append(H2('Option B — USB Printer Shared via Pi (CUPS)'))
story.append(P('A USB printer is connected directly to the Pi. CUPS shares it across EMCOMM-NET. '
               'Installed automatically by the FieldComms installer. CUPS admin UI at http://192.168.50.1:631.'))
story.append(SP(4))
story.append(H3('B.2  Add the USB Printer via CUPS Web Admin'))
story.append(steps([
    'Plug the USB printer into one of the Pi\'s USB ports (or powered USB hub).',
    'On any device on EMCOMM-NET, open a browser and go to: <b>http://192.168.50.1:631</b>',
    'Click <b>Administration → Add Printer</b>.',
    'If prompted for credentials, enter the Pi username and password (e.g. fieldcomms / your password).',
    'Your USB printer appears in the <b>Local Printers</b> list. Select it and click <b>Continue</b>.',
    'Enter a Name (e.g. FieldComms-Printer), Description, and Location. Check <b>Share This Printer</b>. Click Continue.',
    'Select the correct printer driver. Click <b>Add Printer</b>.',
    'Set default options (paper size: Letter) and click <b>Set Default Options</b>.',
    'Click <b>Print Test Page</b> to confirm the printer is working.',
]))
story.append(SP(6))
story.append(H3('B.3  Add the Shared Printer on Operator Devices'))
story.append(tbl(['DEVICE TYPE', 'HOW TO ADD THE SHARED PRINTER'], [
    ['Windows laptop', 'Settings → Bluetooth & devices → Printers & scanners → Add a printer. '
                       'Windows discovers the CUPS printer automatically on EMCOMM-NET.'],
    ['Mac / macOS', 'System Settings → Printers & Scanners → + Add Printer. '
                    'The printer appears under the Default tab via Bonjour. Select it and click Add.'],
    ['iPad / iPhone', 'iOS prints via AirPrint. CUPS with Avahi shares the printer as AirPrint-compatible. '
                      'Tap Share → Print in any FieldComms page and select the printer.'],
    ['Android', 'Install the CUPS Print app (Google Play). Add printer at IP 192.168.50.1, port 631, protocol IPP.'],
    ['Chromebook', 'Settings → Advanced → Printing → Add Printer. '
                   'Enter: Address=192.168.50.1, Protocol=IPP, Queue=/printers/FieldComms-Printer.'],
], [1.4*inch, CW-1.4*inch]))
story.append(SP(6))
story.append(H3('B.4  Recommended Printers for Field Use'))
story.append(tbl(['PRINTER', 'TYPE', 'WHY IT WORKS WELL'], [
    ['Brother HL-L2350DW', 'Laser, USB + Wi-Fi',
     'Excellent Linux support. Fast, compact, duplex, great field durability.'],
    ['HP LaserJet P1102w', 'Laser, USB + Wi-Fi',
     'Excellent Linux driver via HPLIP. Fast, reliable, low cost per page.'],
    ['Canon PIXMA TR150', 'Inkjet, USB + Wi-Fi, battery',
     'Portable battery-powered option for mobile deployments. ~200 pages per charge.'],
    ['HP OfficeJet 200', 'Inkjet, USB + Wi-Fi, battery',
     'Portable battery printer with larger paper tray. Good field option without shore power.'],
], [1.6*inch, 1.3*inch, CW-2.9*inch]))
story.append(PB())

story.append(H2('Option C — Network Printer on EMCOMM-NET (Simplest Shared Setup)'))
story.append(P('A Wi-Fi or Ethernet printer is connected directly to the ASUS router or UniFi switch — '
               'no Pi involvement at all. All devices on EMCOMM-NET can discover and print to it.'))
story.append(SP(6))
story.append(tbl(['CONNECTION METHOD', 'HOW TO SET UP'], [
    ['Wi-Fi (wireless)',
     'Use the printer\'s own control panel to connect it to EMCOMM-NET. Enter the password when prompted. '
     'The printer receives an IP in the 192.168.50.100–200 range from the ASUS router DHCP server.'],
    ['Ethernet (wired)',
     'Run a CAT 6 cable from the printer\'s Ethernet port to any spare port on the UniFi Switch (Ports 3–5). '
     'The printer receives an IP automatically. Check the ASUS router DHCP table for the assigned IP.'],
], [1.5*inch, CW-1.5*inch]))
story.append(SP(6))
story.append(H3('Reserve a Static IP for the Printer (Recommended)'))
story.append(CodeBlock([
    '# On the ASUS router web UI (http://192.168.50.1):',
    '# LAN → DHCP Server → Manually Assigned IP',
    '# Enter the printer MAC address → assign a fixed IP, e.g.: 192.168.50.10',
    '# Reboot the printer to pick up the reservation',
    '# Confirm: ping 192.168.50.10',
]))
story.append(SP(6))
story.append(H2('Printer Option Comparison'))
story.append(tbl(['', 'Option A — Client Printer', 'Option B — USB via Pi / CUPS', 'Option C — Network Printer'], [
    ['Pi configuration needed', 'None', 'CUPS (auto-installed)', 'None'],
    ['One printer for all operators', 'Each device needs own printer', 'Shared across EMCOMM-NET', 'Shared across EMCOMM-NET'],
    ['Works without internet', 'Yes', 'Yes', 'Yes'],
    ['iOS / AirPrint support', 'Requires AirPrint printer', 'Yes via CUPS + Avahi', 'Yes if AirPrint printer'],
    ['Battery printer support', 'Yes', 'Yes (USB connected)', 'Yes (Wi-Fi connected)'],
    ['Best for', 'Single operator or tablet with own printer', 'Any USB printer, shared to all devices', 'Wi-Fi/Ethernet printer already on site'],
], [1.6*inch, 1.4*inch, 1.7*inch, CW-4.7*inch]))
story.append(SP(4))
story.append(NoteBox('For most K9ESV field activations, Option B (USB printer via CUPS) is recommended. '
                     'A Brother HL-L2350DW or HP LaserJet plugged into the Pi USB hub covers all ICS forms, '
                     'net logs, and cheat sheets needed for a typical activation.', 'tip'))
story.append(PB())

# ── STEP 9 — PAT WINLINK ─────────────────────────────────────────────────────
story.append(StepBox(9, 'Pat Winlink — Verify & Configure'))
story.append(SP(8))
story.append(H1('12. Step 9: Pat Winlink — Verify & Configure'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('Pat Winlink is installed automatically by the FieldComms installer. It runs as pat.service '
               'and provides a browser-based backup Winlink client at http://192.168.50.1:8090.'))
story.append(SP(6))
story.append(CodeBlock([
    '# Check pat.service status',
    'sudo systemctl status pat',
    '# If not running:',
    'sudo systemctl start pat && sudo systemctl enable pat',
    '# Confirm port 8090 is listening',
    'ss -tlnp | grep 8090',
    '# Add your Winlink password:',
    'sudo nano /opt/fieldcomms/.config/pat/config.json',
    '# Verify / update these fields:',
    '#   "mycall": "K9ESV"                 ← set by installer',
    '#   "secure_login_password": "xxxxx"   ← add your Winlink password',
    '#   "http_addr": "0.0.0.0:8090"       ← must be 0.0.0.0 for EMCOMM-NET access',
]))
story.append(PB())

# ── STEP 10 — WINDOWS LAPTOP ─────────────────────────────────────────────────
story.append(StepBox(10, 'Windows Laptop — Winlink Express + JS8Call'))
story.append(SP(8))
story.append(H1('12. Step 10: Windows Laptop Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('The Windows laptop is the primary HF digital station. It runs Winlink Express and JS8Call '
               'with the IC-7300 connected via a single USB cable. Connect the laptop to EMCOMM-NET '
               '(Wi-Fi) or the UniFi switch Port 3 (wired Ethernet).'))
story.append(SP(6))
story.append(H2('9.1  IC-7300 One-Time Radio Setup'))
story.append(tbl(['IC-7300 MENU PATH', 'SETTING'], [
    ['SET → Connectors → CI-V Baud Rate', '115200'],
    ['SET → Connectors → CI-V Transceive', 'ON'],
    ['SET → Connectors → USB Send/Keying → USB Send', 'RTS'],
    ['SET → Connectors → MOD Input → USB MOD Level', '40–50%'],
    ['COMP button (speech compression)', 'OFF'],
    ['Mode for digital operation', 'USB-D'],
], [2.5*inch, CW-2.5*inch]))
story.append(SP(6))
story.append(H2('9.2  Install Winlink Express + VARA HF'))
story.append(steps([
    'Download Winlink Express from: <b>winlink.org/client-software</b>. Run installer, accept defaults.',
    'On first launch: enter your callsign, Winlink password, and grid square EN52 (McHenry County, IL).',
    'Settings → Radio Setup: Radio=IC-7300, Control Port=(check Device Manager), Baud Rate=115200, PTT via CAT=checked.',
    'Settings → Sound Card: Input=USB Audio CODEC (IC-7300), Output=USB Audio CODEC (IC-7300).',
    'Download and install VARA HF from: winlink.org → VARA → VARA HF Modem. Set same audio devices in VARA HF Settings.',
    'Test: Open a VARA HF session in Winlink Express → connect to any Winlink RMS gateway on 40m to confirm audio and CAT control work.',
]))
story.append(SP(6))
story.append(H2('9.3  Install JS8Call'))
story.append(steps([
    'Download JS8Call from: <b>js8call.com</b> → Windows installer. Run installer, accept defaults.',
    'Launch JS8Call. Open File → Settings (F2). General tab: My Call=K9ESV, My Grid=EN52.',
    'Audio tab: Input=USB Audio CODEC (IC-7300), Output=USB Audio CODEC (IC-7300).',
    'Radio tab: Rig=IC-7300, PTT Method=CAT, Serial Port=(same COM port as Winlink), Baud Rate=115200.',
    'Reporting tab (CRITICAL): TCP Server Hostname=<b>0.0.0.0</b> (MUST change from 127.0.0.1). Enable TCP Server API=checked. TCP Server Port=<b>2442</b>. Accept TCP Requests=checked.',
    'Click OK. Restart JS8Call for API settings to take effect.',
    'Set VFO to 7.078 MHz (JS8 40m calling frequency). Mode → Normal.',
]))
story.append(SP(6))
story.append(H2('9.4  Windows Firewall — Allow JS8Call Port 2442'))
story.append(CodeBlock([
    '1. Search "Windows Defender Firewall" → Advanced Settings',
    '2. Inbound Rules → New Rule → Port → TCP → Specific port: 2442 → Allow → All profiles',
    '3. Name the rule: JS8Call API',
]))
story.append(SP(6))
story.append(H2('9.5  Find the Windows Laptop IP on EMCOMM-NET'))
story.append(CodeBlock([
    '# Run in Windows Command Prompt:',
    'ipconfig',
    '# Note the IPv4 Address for the EMCOMM-NET adapter (e.g. 192.168.50.105)',
    '# Set a DHCP reservation (recommended — gives laptop a fixed IP):',
    '# ASUS Web UI → LAN → DHCP Server → Manually Assigned IP',
    '# Enter laptop MAC address → assign 192.168.50.2',
    '',
    '# Configure the FieldComms dashboard JS8Call card:',
    '# 1. Connect to EMCOMM-NET, open http://192.168.50.1',
    '# 2. Find the JS8Call card (purple) in Amateur Radio section',
    '# 3. Tap/click the card',
    '# 4. Enter the Windows laptop IP (e.g. 192.168.50.105)',
    '# 5. Card saves IP and opens http://192.168.50.105:2442',
]))
story.append(SP(6))
story.append(tbl(['SWITCHING TO...', 'PROCEDURE'], [
    ['Winlink Express', 'Close/disconnect JS8Call → open VARA HF → it reclaims USB audio → open Winlink Express'],
    ['JS8Call', 'Finish any Winlink TX → close VARA HF → minimize Winlink Express → open JS8Call and click Connect'],
    ['Both simultaneously (two radios)',
     'Connect a second HF radio to the laptop via a separate USB audio and CAT interface. Configure JS8Call to use the second radio port. Both can run at the same time with no conflicts.'],
], [1.5*inch, CW-1.5*inch]))
story.append(PB())

# ── STEP 11 — FIRST BOOT ─────────────────────────────────────────────────────
story.append(StepBox(11, 'First Boot Verification'))
story.append(SP(8))
story.append(H1('13. Step 11: First Boot Verification'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(CodeBlock([
    '# Check all FieldComms services',
    'for svc in fcc-lookup health-monitor deadmans ics-platform kiwix nginx pat; do',
    '  echo "$svc: $(systemctl is-active $svc)"',
    'done',
    '',
    '# Test the dashboard from the Pi itself',
    'curl -s http://localhost/ | head -5',
    '# Test API endpoints',
    'curl http://localhost:5050/health      # FCC API health check',
    'curl http://localhost:5051/health      # System health monitor',
    '# Verify Pi has the correct static IP',
    'ip addr show eth0',
    '# Should show: inet 192.168.50.1/24',
]))
story.append(PB())

# ── REFERENCE SECTIONS ────────────────────────────────────────────────────────
story.append(H1('14. Network Architecture Reference'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(H2('Network Topology'))
story.append(P('Wi-Fi is provided by the ASUS RT-BE58 Go router. The Pi is a wired client with a static IP of '
               '192.168.50.1, connected via the UniFi Switch Flex 2.5G-5. The Pi does not run hostapd or dnsmasq.'))
story.append(SP(4))
story.append(tbl(['DEVICE', 'IP ADDRESS', 'ROLE', 'CONNECTION'], [
    ['ASUS RT-BE58 Go', '192.168.50.1 (LAN gateway)', 'Wi-Fi AP + DHCP server',
     'WAN: site Ethernet or USB tether (optional)'],
    ['UniFi Switch Flex 2.5G-5', 'N/A (Layer 2 switch)', 'Wired distribution',
     'Port 1 → ASUS router · Port 2 → Pi · Ports 3–5 spare'],
    ['Raspberry Pi 5', '192.168.50.1 (static)', 'FieldComms application server',
     'Wired Ethernet via UniFi switch'],
    ['Windows laptop', '192.168.50.2 (recommended static)', 'Winlink Express + JS8Call station',
     'Wi-Fi (EMCOMM-NET) or wired via UniFi Port 3'],
    ['Field devices (phones, tablets)', '192.168.50.100–200 (DHCP)', 'Operator browsers',
     'Wi-Fi (EMCOMM-NET, 2.4 GHz or 5 GHz)'],
], [1.5*inch, 1.3*inch, 1.5*inch, CW-4.3*inch]))
story.append(SP(6))
story.append(NoteBox(
    'Recommended: set the ASUS router LAN IP to 192.168.50.254 and the Pi static IP to 192.168.50.1. '
    'This keeps the FieldComms URL clean and the router admin clearly separate at http://192.168.50.254.',
    'tip'))
story.append(PB())

story.append(H1('13. Web Dashboard Reference'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(tbl(['PAGE', 'URL', 'DESCRIPTION'], [
    ['Dashboard', '/', 'Main hub — UTC clock, NWS weather alerts, APRS table, tool cards, DMS status'],
    ['Amateur Net Control', '/netcontrol.html', 'Multi-net logger, FCC autofill, precedence, ICS-309 export, server sync'],
    ['Starcom Net Logger', '/starcom.html', 'Public safety net log with Radio IDs, sc- prefix nets, ICS-309 export'],
    ['Net Observer', '/observer.html?net=NETNAME', 'Read-only net viewer — 15-second auto-refresh, no login'],
    ['Member Roster', '/roster.html', 'Directory with 11 certs, 13 equipment fields, 4 roles, CSV import/export'],
    ['Resource Board', '/resources.html', 'Equipment, vehicle, personnel tracking with status cycling'],
    ['Tactical APRS Map', '/tactical.html', 'Leaflet map — Graywolf + YAAC merged, live WebSocket, APRS symbols'],
    ['Starcom Resource Map', '/resmap.html', 'Unit positioning map with zone and polygon drawing tools'],
    ['Callsign Lookup', '/callsign.html', 'FCC local database — ~800K licensees, instant offline search'],
    ['ICS Platform', '/ics/', 'Command, Operations, Planning, Logistics, Finance sections'],
    ['ICS-213', '/ics213.html', 'General Message form with print output and form log'],
    ['ICS-214', '/ics214.html', 'Activity Log with personnel and timestamped activity rows'],
    ['ICS-309', '/ics309.html', 'Communications Log with incident archiving'],
    ['NTS Radiogram', '/nts.html', 'ARRL-format radiogram generator and traffic log'],
    ['Winlink Form Import', '/winlink-import.html', 'Import Winlink Express XML forms to incident archive'],
    ['Pre-Flight', '/preflight.html', 'GO/CAUTION/NO-GO deployment readiness assessment'],
    ['Health Monitor', ':5051/health', 'Live CPU/memory/disk/temp, all service status, GPS, internet'],
    ['Pat Winlink', ':8090', 'Browser-based backup Winlink client'],
    ['Kiwix Library', ':8081/', 'Offline reference library — WikiMed, Wikipedia, iFixit'],
    ['Print Center', '/printcenter.html', 'All printable documents in one place + incident cover sheet generator'],
], [1.4*inch, 1.4*inch, CW-2.8*inch]))
story.append(PB())

story.append(H1('14. Service & Port Reference'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(tbl(['PORT', 'SERVICE', 'SYSTEMD UNIT', 'DESCRIPTION'], [
    ['80',   'nginx',           'nginx.service',          'Web frontend — serves all HTML pages'],
    ['5050', 'FCC Lookup Server', 'fcc-lookup.service',   'Main API: callsign lookup, net logs, roster, resources, DMS, ICS forms'],
    ['5051', 'Health Monitor',  'health-monitor.service', 'System health: CPU temp, memory, disk, GPS, all service status'],
    ['5055', 'ICS Platform',    'ics-platform.service',   'ICS incident management: incidents, objectives, resources, T-cards'],
    ['5056', 'References API',  'fieldcomms-refs.service','Reference library API'],
    ['8080', 'Graywolf APRS',  '(graywolf.service)',     'APRS TNC client — REST API + WebSocket live stream'],
    ['8081', 'Kiwix Library',   'kiwix.service',          'Offline web library — WikiMed, Wikipedia, iFixit, etc.'],
    ['8082', 'YAAC APRS',      'yaac.service',            'YAAC Java APRS client — REST API + WebSocket'],
    ['8083', 'Tile Server',     'fieldcomms-tiles.service','Offline map tile server (MBTiles)'],
    ['8090', 'Pat Winlink',     'pat.service',             'Winlink email-over-radio — Packet, VARA HF, VARA FM'],
    ['631',  'CUPS Printer',    'cups.service',            'Print server — USB printer shared to EMCOMM-NET'],
    ['2442', 'JS8Call',         '(JS8Call app on laptop)', 'HF digital keyboard messaging — TCP API on Windows laptop'],
], [0.6*inch, 1.4*inch, 1.6*inch, CW-3.6*inch]))
story.append(PB())

story.append(H1('15. Maintenance & Updates'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(CodeBlock([
    '# Interactive maintenance menu:',
    'sudo bash /opt/fieldcomms/scripts/update.sh',
    '',
    '# Menu options:',
    '#  1) Restart all services',
    '#  2) Stop all services',
    '#  3) Check service status',
    '#  4) View live logs',
    '#  5) Refresh FCC database',
    '#  6) Fetch repeater data',
    '#  7) Update web files from current directory',
    '#  8) Backup data to /tmp',
    '#  9) Show disk usage',
]))
story.append(SP(6))
story.append(H2('USB Auto-Backup'))
story.append(P('Insert a USB drive formatted with the label <b>FIELDCOMMS</b> to trigger an automatic backup '
               'of all runtime data. The backup copies /opt/fieldcomms/data/ to a timestamped folder on the USB drive.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Format a USB drive with label FIELDCOMMS (Linux):',
    'sudo mkfs.vfat -n FIELDCOMMS /dev/sda1',
    '# Or on Windows: format as FAT32, set volume label to FIELDCOMMS',
    '# Backup destination on USB:',
    '# /media/fieldcomms/backup/YYYYMMDD_HHMMSS',
]))
story.append(PB())

story.append(H1('16. Troubleshooting'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(ref_tbl_2col(['SYMPTOM', 'LIKELY CAUSE / FIX'], [
    ['http://192.168.50.1 not reachable', 'Pi not running, or ASUS router not configured with 192.168.50.x subnet. Check Pi power LED. Verify router LAN IP is 192.168.50.1.'],
    ['Dashboard loads but cards give errors', 'Not connected to EMCOMM-NET — device is on a different network. Check Wi-Fi — must show EMCOMM-NET.'],
    ['FCC lookup returns no results', 'FCC database not yet built. Run: sudo systemctl start fcc-refresh.service (needs internet)'],
    ['APRS map shows no stations', 'Graywolf or YAAC not running, or no RF received yet. Check Health Monitor for service status. Confirm antenna connected.'],
    ['Winlink form import fails', 'Wrong file type — must be the XML attachment, not the message body. In Winlink Express, right-click .xml attachment → Save As → then import.'],
    ['Service dot is red on Health Monitor', 'Background service has stopped. SSH to Pi: sudo systemctl restart <service-name>'],
    ['Pat Winlink not accessible at port 8090', 'pat.service not running. Run: sudo systemctl start pat && sudo systemctl enable pat'],
    ['JS8Call card does not open', 'TCP Server API not enabled in JS8Call, or wrong IP entered. Verify: File → Settings → Reporting → Enable TCP Server API, port 2442, hostname 0.0.0.0.'],
    ['Printer not visible on EMCOMM-NET', 'avahi-daemon not running, or CUPS printer not shared. Check: sudo systemctl status avahi-daemon cups. Verify Share This Printer is checked in CUPS UI.'],
    ['Issue: Services crash on startup', 'Low disk space or permission error. Check: df -h / and ls -la /opt/fieldcomms/. Verify fieldcomms user owns /opt/fieldcomms/.'],
], [1.8*inch, CW-1.8*inch]))
story.append(SP(4))
story.append(NoteBox('For any issue not covered here — open the Health Monitor at http://192.168.50.1:5051/health '
                     'or check the system log with: journalctl -u fcc-lookup -n 50', 'tip'))
story.append(PB())

story.append(H1('17. Quick Reference Card'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(tbl(['ITEM', 'VALUE'], [
    ['FieldComms dashboard', 'http://192.168.50.1'],
    ['Wi-Fi network (SSID)', 'EMCOMM-NET'],
    ['Pi static IP', '192.168.50.1'],
    ['ASUS router admin', 'http://192.168.50.1  (or http://192.168.50.254 if reconfigured)'],
    ['CUPS printer admin', 'http://192.168.50.1:631'],
    ['Pat Winlink (backup)', 'http://192.168.50.1:8090'],
    ['Kiwix offline library', 'http://192.168.50.1:8081'],
    ['Health monitor (raw)', 'http://192.168.50.1:5051/health'],
    ['JS8Call TCP API (laptop)', 'http://[laptop-ip]:2442'],
    ['Callsign K9ESV', 'McHenry County Emergency Services Volunteers and EMA'],
    ['McHenry County grid', 'EN52'],
    ['Default coordinates', '42.3153 N  /  88.4473 W  (Woodstock, IL)'],
    ['Install log', '/var/log/fieldcomms-install.log'],
    ['Application data', '/opt/fieldcomms/data/'],
    ['HTML pages', '/opt/fieldcomms/html/'],
    ['Update script', 'sudo bash /opt/fieldcomms/scripts/update.sh'],
], [2.0*inch, CW-2.0*inch]))

# ── Build ─────────────────────────────────────────────────────────────────────
out = '/mnt/user-data/outputs/FieldComms_Installation_Guide.pdf'
doc = SimpleDocTemplate(
    out, pagesize=letter,
    leftMargin=M, rightMargin=M,
    topMargin=0.55*inch, bottomMargin=0.42*inch,
    title='FieldComms IMS v1.0 — Installation Guide',
    author='McHenry County Emergency Services Volunteers and McHenry County Emergency Management Agency')
doc.build(story, canvasmaker=NC)

# Append Pi 500 addendum
from pypdf import PdfReader, PdfWriter
addendum = '/home/claude/pi500_addendum.pdf'
if os.path.exists(addendum):
    base = PdfReader(out); add = PdfReader(addendum)
    w = PdfWriter()
    for p in base.pages: w.add_page(p)
    for p in add.pages:  w.add_page(p)
    buf = io.BytesIO()
    w.write(buf)
    with open(out, 'wb') as f: f.write(buf.getvalue())

r = PdfReader(out)
print(f'BUILT: {out}')
print(f'Pages: {len(r.pages)}')
