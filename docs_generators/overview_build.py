#!/usr/bin/env python3
"""
FieldComms IMS v1.0 — One-Page System Overview
Presentation-quality single page for grant applications,
briefings, and stakeholder presentations.
Output: /mnt/user-data/outputs/IncidentManagement_Overview.pdf
"""
import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.pdfgen import canvas

# ── Palette ───────────────────────────────────────────────────────────────────
EOC    = HexColor('#1a3a6b')
EOC_LT = HexColor('#2d6ab4')
EOC_BG = HexColor('#eef2f7')
GOLD   = HexColor('#f0c040')
LINE   = HexColor('#c0cfe0')
LGRAY  = HexColor('#f0f3f6')
GREEN  = HexColor('#1a7a3a')
AMBER  = HexColor('#c8760a')
PURPLE = HexColor('#5b2d8c')
SGREEN = HexColor('#1a6b2a')
RED    = HexColor('#b82020')
MUTED  = HexColor('#4a6080')

TODAY  = datetime.date.today().strftime('%B %Y')
ORG    = 'McHenry County Emergency Services Volunteers and Emergency Management Agency'
SHORT  = 'MCESV / MCEMA  ·  K9ESV  ·  RACES / ARES / Starcom'
PAGE_W, PAGE_H = letter
M  = 0.48 * inch
CW = PAGE_W - 2 * M

# ── Canvas — full-page cover chrome ──────────────────────────────────────────
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
            self.TOTAL = total
            n = self._pageNumber
            # ── Top header bar ────────────────────────────────────────────────
            self.setFillColor(EOC)
            self.rect(0, PAGE_H - 0.52*inch, PAGE_W, 0.52*inch, fill=1, stroke=0)
            self.setFillColor(GOLD)
            self.rect(0, PAGE_H - 0.54*inch, PAGE_W, 0.022*inch, fill=1, stroke=0)

            # Logo
            logo = Path('/home/claude/esv-logo.png')
            if logo.exists():
                try:
                    self.drawImage(str(logo), M, PAGE_H - 0.49*inch,
                                   width=1.0*inch, height=0.40*inch,
                                   preserveAspectRatio=True, mask='auto')
                except Exception:
                    pass

            # Org name
            self.setFillColor(white)
            self.setFont('Helvetica-Bold', 11)
            self.drawString(M + 1.15*inch, PAGE_H - 0.24*inch,
                'FieldComms  Incident Management System  v1.0')
            self.setFont('Helvetica', 8)
            self.setFillColor(HexColor('#c0d4f0'))
            self.drawString(M + 1.15*inch, PAGE_H - 0.38*inch, SHORT)

            # Date right
            self.setFillColor(HexColor('#8090b0'))
            self.setFont('Helvetica', 8)
            self.drawRightString(PAGE_W - M, PAGE_H - 0.30*inch, TODAY)

            # ── Bottom footer bar ─────────────────────────────────────────────
            self.setFillColor(EOC)
            self.rect(0, 0, PAGE_W, 0.32*inch, fill=1, stroke=0)
            self.setFillColor(GOLD)
            self.rect(0, 0.32*inch, PAGE_W, 0.015*inch, fill=1, stroke=0)
            self.setFillColor(white)
            self.setFont('Helvetica', 7)
            self.drawString(M, 0.115*inch,
                f'{ORG}  ·  For Authorized Personnel Only')
            self.drawRightString(PAGE_W - M, 0.115*inch,
                'EMCOMM-NET  ·  http://192.168.50.1')

            super().showPage()
        super().save()

# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=8.5, textColor=black,
             leading=11, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

def P(t, s=None): return Paragraph(t, s or S('b'))
def SP(n=3):      return Spacer(1, n)
def HR(c=LINE, t=0.4):
    return HRFlowable(width='100%', thickness=t, color=c, spaceBefore=1, spaceAfter=1)

def section_hdr(icon, title, color, bg):
    t = Table([[
        P(f'{icon}  {title}',
          S('sh', fontName='Helvetica-Bold', fontSize=9,
            textColor=color, leading=11)),
    ]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW',     (0,0), (-1,-1), 1.5, color),
    ]))
    return t

def bullet(text, color=EOC_LT):
    return P(f'<font color="#{color.hexval()}" size="9">▸</font>  {text}',
             S('bl', fontSize=8, leading=11,
               leftIndent=14, firstLineIndent=-10))

def col_bullets(items, color=EOC_LT):
    """Two-column bullet layout."""
    mid = (len(items) + 1) // 2
    left  = items[:mid]
    right = items[mid:]
    left_para  = [bullet(i, color) for i in left]
    right_para = [bullet(i, color) for i in right]

    # Pad to same length
    while len(left_para) < len(right_para):
        left_para.append(Spacer(1, 11))
    while len(right_para) < len(left_para):
        right_para.append(Spacer(1, 11))

    rows = [[l, r] for l, r in zip(left_para, right_para)]
    t = Table(rows, colWidths=[CW*0.5, CW*0.5])
    t.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ]))
    return t

def hex_str(c):
    """Return hex string without #."""
    r = int(c.red * 255)
    g = int(c.green * 255)
    b = int(c.blue * 255)
    return f'{r:02x}{g:02x}{b:02x}'

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── INTRODUCTION ───────────────────────────────────────────────────────────────
story.append(SP(4))
story.append(P(
    '<b>FieldComms</b> is a self-contained emergency communications server '
    'built on a Raspberry Pi 5 for McHenry County RACES, ARES, and Starcom operations. '
    'Any smartphone, tablet, or laptop connects to the <b>EMCOMM-NET</b> Wi-Fi access point '
    'and reaches the full dashboard at <b>http://192.168.50.1</b> — '
    'no internet, no app installation, no per-device configuration required. '
    'All 30 tools, all ICS forms, all reference materials, and all offline maps '
    'remain fully functional when the site has no internet connectivity.',
    S('intro', fontSize=8.5, leading=12.5, alignment=TA_JUSTIFY,
      textColor=HexColor('#1a2a3a'))))
story.append(SP(6))

# ── THREE-COLUMN CAPABILITY SUMMARY ───────────────────────────────────────────
cap_hdr = Table([[
    P('📻  AMATEUR RADIO',
      S('ch', fontName='Helvetica-Bold', fontSize=8.5, textColor=white, leading=11,
        alignment=TA_CENTER)),
    P('🚔  STARCOM / PUBLIC SAFETY',
      S('ch', fontName='Helvetica-Bold', fontSize=8.5, textColor=white, leading=11,
        alignment=TA_CENTER)),
    P('🏛  ICS INCIDENT COMMAND',
      S('ch', fontName='Helvetica-Bold', fontSize=8.5, textColor=white, leading=11,
        alignment=TA_CENTER)),
]], colWidths=[CW/3, CW/3, CW/3])
cap_hdr.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (0,-1), EOC_LT),
    ('BACKGROUND',    (1,0), (1,-1), SGREEN),
    ('BACKGROUND',    (2,0), (2,-1), PURPLE),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('LINEAFTER',     (0,0), (1,-1), 0.5, white),
]))
story.append(cap_hdr)

def cap_bullets(items, color):
    content = [P(f'• {i}', S('cb', fontSize=7.5, leading=10.5,
                              leftIndent=8, firstLineIndent=-6,
                              textColor=black)) for i in items]
    t = Table([[c] for c in content], colWidths=[CW/3])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LGRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('LINEBELOW',     (0,-1), (-1,-1), 1, color),
    ]))
    return t

amateur_items = [
    'Net Control Logger — FCC auto-fill',
    'Callsign Lookup — 800K licensees offline',
    'Observer Mode — read-only agency view',
    'APRS Tactical Map — Graywolf + YAAC',
    'HF Propagation — band conditions live',
    'Repeater Database — ARES/band filters',
    'Dead Man\'s Switch — net inactivity alert',
    'NTS Radiogram — ARRL formatted traffic',
    'JS8Call — HF keyboard digital messaging',
    'Pat Winlink — backup email over radio',
]
starcom_items = [
    'Starcom Net Logger — Radio ID / unit-based',
    'Weather Net — storm spotter check-in',
    'SAR Net — search and rescue radio ops',
    'Resource Tracking Map — unit placement',
    'Resource Board — 5-state status cycle',
    'Member Roster — certifications, activations',
    'Facilities Directory — EOC, shelters, hospitals',
    'Multiple simultaneous nets on one screen',
    'Observer link for served agencies',
    'ICS platform integration from Starcom mode',
]
ics_items = [
    'Command — objectives, safety, staff',
    'Operations — T-card board, assignments',
    'Planning — IAP tracker, resource status',
    'Logistics — ICS-205 comms plan, supplies',
    'Finance/Admin — cost, time, procurement',
    'Planning P — 15-phase planning cycle guide',
    'ICS-213 / ICS-214 / ICS-309 forms',
    'Winlink Form Import — XML to incident',
    'Incident types: Disaster, HazMat, SAR, MCI',
    'Multi-user — all sections see live data',
]

cap_body = Table([[
    cap_bullets(amateur_items, EOC_LT),
    cap_bullets(starcom_items, SGREEN),
    cap_bullets(ics_items, PURPLE),
]], colWidths=[CW/3, CW/3, CW/3])
cap_body.setStyle(TableStyle([
    ('VALIGN',      (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING',(0,0), (-1,-1), 0),
    ('TOPPADDING',  (0,0), (-1,-1), 0),
    ('BOTTOMPADDING',(0,0), (-1,-1), 0),
    ('LINEAFTER',   (0,0), (1,-1), 0.5, LINE),
]))
story.append(cap_body)
story.append(SP(6))

# ── CONNECTIVITY ───────────────────────────────────────────────────────────────
story.append(section_hdr('📡', 'Connectivity — Dual WAN with Automatic Failover',
                         AMBER, HexColor('#fef3d8')))
story.append(SP(3))
wan_tbl = Table([[
    P('InstyConnect Cellular  (Primary WAN)',
      S('wh', fontName='Helvetica-Bold', fontSize=8, textColor=EOC, leading=10)),
    P('Starlink Satellite  (Automatic Failover)',
      S('wh', fontName='Helvetica-Bold', fontSize=8, textColor=EOC, leading=10)),
    P('AMPRNet / 44Net  (Amateur Radio IP)',
      S('wh', fontName='Helvetica-Bold', fontSize=8, textColor=EOC, leading=10)),
]], colWidths=[CW/3, CW/3, CW/3])
wan_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), HexColor('#e0e8f4')),
    ('TOPPADDING',    (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('LINEAFTER',     (0,0), (1,-1), 0.5, LINE),
]))
story.append(wan_tbl)

wan_desc = Table([[
    P('InstyConnect Drum omnidirectional antenna + Switchblade directional backup. '
      'T-Mobile + Verizon dual-carrier. Pauses at $5/month between activations.',
      S('wd', fontSize=7.5, leading=10.5)),
    P('Automatic failover when cellular drops. '
      'ASUS RT-BE58 Go manages failover with no operator action required. '
      'All FieldComms features remain active during satellite operation.',
      S('wd', fontSize=7.5, leading=10.5)),
    P('Dedicated Raspberry Pi 5 gateway. '
      'WireGuard tunnel to amprgw.ampr.org. '
      'Routes 44.0.0.0/8 for all EMCOMM-NET devices. '
      'AMPRNet allocation required from portal.ampr.org.',
      S('wd', fontSize=7.5, leading=10.5)),
]], colWidths=[CW/3, CW/3, CW/3])
wan_desc.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LGRAY),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('LINEAFTER',     (0,0), (1,-1), 0.5, LINE),
    ('LINEBELOW',     (0,0), (-1,-1), 1, AMBER),
]))
story.append(wan_desc)
story.append(SP(6))

# ── HARDWARE ───────────────────────────────────────────────────────────────────
story.append(section_hdr('🖥', 'Hardware Platform', EOC, EOC_BG))
story.append(SP(3))

hw_data = [
    ['COMPONENT', 'SPECIFICATION', 'ROLE'],
    ['FieldComms Server',
     'Raspberry Pi 5  16 GB  ·  Pironman MAX 5  ·  2× 1 TB NVMe RAID 1',
     'Runs all 30 web pages, 12 Python services, FCC database, offline maps, Kiwix library'],
    ['44Net Gateway',
     'Raspberry Pi 5  16 GB  ·  Argon NEO 5  ·  256 GB M.2 SSD  ·  Pi OS Desktop',
     'Dedicated AMPRNet WireGuard gateway  ·  routes 44.0.0.0/8 for all devices'],
    ['Wi-Fi Access Point',
     'ASUS RT-BE58 Go  Wi-Fi 7  ·  Dual WAN  (cellular primary + satellite failover)',
     'EMCOMM-NET SSID  ·  DHCP server  ·  WAN gateway with automatic failover'],
    ['Network Switch',
     'UniFi Switch Lite 16 PoE  ·  16-port GbE  ·  8× PoE  ·  2× SFP uplink',
     'Wired distribution  ·  both Pis, workstations, printer, spare ports'],
    ['Primary Cellular WAN',
     'InstyConnect Drum  (omni)  +  Switchblade  (directional backup)  ·  5G/LTE',
     'T-Mobile + Verizon dual-carrier  ·  PoE Ethernet to ASUS WAN port'],
    ['Satellite WAN Backup',
     'Starlink Standard or Flat HP dish  ·  auto-failover via ASUS USB WAN',
     'Secondary internet when cellular unavailable  ·  CGNAT  ·  no inbound connections'],
    ['Radio Station',
     'Icom IC-7300  ·  Windows laptop  ·  Winlink Express + VARA HF  ·  JS8Call',
     'HF digital voice and data  ·  Winlink email over radio  ·  IC-7300 via single USB'],
    ['Operator Workstations',
     'Raspberry Pi 500 / 500+  ×4  ·  Raspberry Pi Monitor 15.6"  ×4',
     'Browser-based  ·  one per operator station  ·  USB-C powered from monitor'],
]

hw_rows = []
for i, row in enumerate(hw_data):
    fs = 7.5 if i == 0 else 8
    fn = 'Helvetica-Bold' if i == 0 else 'Helvetica'
    tc = white if i == 0 else black
    hw_rows.append([P(str(c), S('hw', fontName=fn, fontSize=fs,
                                 textColor=tc, leading=10)) for c in row])

hw_t = Table(hw_rows, colWidths=[1.2*inch, 2.8*inch, CW-4.0*inch],
             repeatRows=1)
hw_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  EOC),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
    ('GRID',          (0,0), (-1,-1), 0.3, LINE),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING',    (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
    ('RIGHTPADDING',  (0,0), (-1,-1), 5),
]))
story.append(hw_t)
story.append(SP(5))

# ── REFERENCE + ACCESS ─────────────────────────────────────────────────────────
ref_col = Table([[
    # Reference tools
    Table([[
        P('Reference & Administration',
          S('rh', fontName='Helvetica-Bold', fontSize=8, textColor=EOC_LT, leading=10)),
        SP(2),
        P('• Kiwix Offline Library — WikiMed, Wikipedia, iFixit, Wikivoyage',
          S('rb', fontSize=7.5, leading=10)),
        P('• Reference Library — upload, tag, and serve field documents',
          S('rb', fontSize=7.5, leading=10)),
        P('• Radio Cheat Sheets — phonetics, Q-codes, prowords, band plan',
          S('rb', fontSize=7.5, leading=10)),
        P('• Print Center — all ICS forms, reference cards, operator access cards',
          S('rb', fontSize=7.5, leading=10)),
        P('• Pre-Flight Checklist — GO / CAUTION / NO-GO deployment readiness',
          S('rb', fontSize=7.5, leading=10)),
        P('• FCC Callsign Lookup — 800K licensees, offline, instant response',
          S('rb', fontSize=7.5, leading=10)),
        P('• System Health Monitor — CPU, memory, disk, all services, GPS, WAN',
          S('rb', fontSize=7.5, leading=10)),
        P('• WAN Status Dashboard — InstyConnect, Starlink, 44Net status live',
          S('rb', fontSize=7.5, leading=10)),
    ]], colWidths=[CW*0.48]),
    # How to access + key specs
    Table([[
        P('How to Access',
          S('ah', fontName='Helvetica-Bold', fontSize=8, textColor=GREEN, leading=10)),
        SP(2),
        P('<b>1.</b>  Connect to Wi-Fi:  <b>EMCOMM-NET</b>',
          S('ab', fontSize=8, leading=11)),
        P('<b>2.</b>  Open any browser to:  <b>http://192.168.50.1</b>',
          S('ab', fontSize=8, leading=11)),
        P('<b>3.</b>  Enter your callsign or Radio ID',
          S('ab', fontSize=8, leading=11)),
        SP(5),
        P('No app  ·  No login  ·  No internet required',
          S('ac', fontName='Helvetica-Bold', fontSize=8,
            textColor=GREEN, leading=10, alignment=TA_CENTER)),
        SP(5),
        HR(LINE, 0.4),
        SP(4),
        P('Key Statistics',
          S('kh', fontName='Helvetica-Bold', fontSize=8, textColor=EOC, leading=10)),
        SP(2),
        Table([[
            P('30', S('kn', fontName='Helvetica-Bold', fontSize=16,
                       textColor=EOC_LT, alignment=TA_CENTER, leading=18)),
            P('12', S('kn', fontName='Helvetica-Bold', fontSize=16,
                       textColor=GREEN, alignment=TA_CENTER, leading=18)),
            P('3', S('kn', fontName='Helvetica-Bold', fontSize=16,
                      textColor=AMBER, alignment=TA_CENTER, leading=18)),
            P('6', S('kn', fontName='Helvetica-Bold', fontSize=16,
                      textColor=PURPLE, alignment=TA_CENTER, leading=18)),
        ]], colWidths=[(CW*0.48)/4]*4),
        Table([[
            P('Web Pages', S('kl', fontSize=7, textColor=MUTED,
                              alignment=TA_CENTER, leading=9)),
            P('Background\nServices', S('kl', fontSize=7, textColor=MUTED,
                                        alignment=TA_CENTER, leading=9)),
            P('Dashboard\nModes', S('kl', fontSize=7, textColor=MUTED,
                                     alignment=TA_CENTER, leading=9)),
            P('WAN\nSources', S('kl', fontSize=7, textColor=MUTED,
                                  alignment=TA_CENTER, leading=9)),
        ]], colWidths=[(CW*0.48)/4]*4),
    ]], colWidths=[CW*0.48]),
]], colWidths=[CW*0.52, CW*0.48])
ref_col.setStyle(TableStyle([
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING',   (0,0), (-1,-1), 0),
    ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ('TOPPADDING',    (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('LINEAFTER',     (0,0), (0,-1), 0.5, LINE),
    ('LEFTPADDING',   (1,0), (1,-1), 10),
]))
story.append(ref_col)
story.append(SP(5))

# ── FUNDING NOTE ───────────────────────────────────────────────────────────────
fund = Table([[
    P('501(c)(3) Grant Eligible  ·  Funding Sources:  '
      'FEMA BRIC  ·  ARPA-E  ·  ARRL Foundation  ·  ARES Special Fund  ·  '
      'DHS BRIC Nonprofit Security Grant Program  ·  Illinois Homeland Security',
      S('fn', fontName='Helvetica', fontSize=7.5, textColor=white,
        leading=10, alignment=TA_CENTER)),
]], colWidths=[CW])
fund.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), EOC),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ('LINEABOVE',     (0,0), (-1,-1), 1.5, GOLD),
]))
story.append(fund)

# ── Build ──────────────────────────────────────────────────────────────────────
out = '/mnt/user-data/outputs/IncidentManagement_Overview.pdf'
doc = SimpleDocTemplate(
    out, pagesize=letter,
    leftMargin=M, rightMargin=M,
    topMargin=0.62*inch, bottomMargin=0.44*inch,
    title='FieldComms IMS v1.0 — System Overview',
    author='McHenry County Emergency Services Volunteers and McHenry County Emergency Management Agency')
doc.build(story, canvasmaker=NC)

from pypdf import PdfReader
r = PdfReader(out)
print(f'BUILT: {out}')
print(f'Pages: {len(r.pages)}')
