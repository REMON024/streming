"""
Streamix — Customer Feature Document with UI mockup illustrations.
Every feature section includes a hand-drawn vector UI mockup.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Circle, Line, Polygon,
    Group, Path
)
from reportlab.graphics import renderPDF

def _rrect(x, y, w, h, r, fillColor=None, strokeColor=None, strokeWidth=0):
    """Draw a rounded rectangle as a Path."""
    r = min(r, w / 2, h / 2)
    p = Path(fillColor=fillColor,
             strokeColor=strokeColor if strokeColor else fillColor,
             strokeWidth=strokeWidth)
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.curveTo(x + w, y, x + w, y, x + w, y + r)
    p.lineTo(x + w, y + h - r)
    p.curveTo(x + w, y + h, x + w, y + h, x + w - r, y + h)
    p.lineTo(x + r, y + h)
    p.curveTo(x, y + h, x, y + h, x, y + h - r)
    p.lineTo(x, y + r)
    p.curveTo(x, y, x, y, x + r, y)
    p.closePath()
    return p
from reportlab.pdfgen import canvas
from datetime import date

# ── Palette ────────────────────────────────────────────────────────────────────
RED     = HexColor('#E50914')
DARK    = HexColor('#141414')
MID     = HexColor('#1f1f1f')
CARD    = HexColor('#2a2a2a')
GRAY    = HexColor('#757575')
LGRAY   = HexColor('#d4d4d4')
XLIGHT  = HexColor('#f0f0f0')
WHITE   = white
GOLD    = HexColor('#f5c518')
GREEN   = HexColor('#46d369')
BLUE    = HexColor('#0071eb')
PURPLE  = HexColor('#b81d8a')
ORANGE  = HexColor('#e87c1e')

PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 5*cm   # usable width

# ── Numbered canvas ────────────────────────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self._draw_footer(total)
            super().showPage()
        super().save()

    def _draw_footer(self, total):
        self.setFont("Helvetica", 7.5)
        self.setFillColor(GRAY)
        self.drawCentredString(PAGE_W / 2, 1.2*cm, f"{self._pageNumber}")
        self.setStrokeColor(HexColor('#e0e0e0'))
        self.setLineWidth(0.4)
        self.line(2.5*cm, 1.6*cm, PAGE_W - 2.5*cm, 1.6*cm)


# ── Styles ─────────────────────────────────────────────────────────────────────
def S():
    return {
        'ct': ParagraphStyle('ct', fontName='Helvetica-Bold', fontSize=38,
                             textColor=WHITE, alignment=TA_CENTER, leading=46,
                             spaceAfter=12),
        'cs': ParagraphStyle('cs', fontName='Helvetica', fontSize=16,
                             textColor=HexColor('#cccccc'), alignment=TA_CENTER,
                             leading=22, spaceAfter=8),
        'cm': ParagraphStyle('cm', fontName='Helvetica', fontSize=9,
                             textColor=HexColor('#888'), alignment=TA_CENTER,
                             spaceAfter=3),
        'feature_tag': ParagraphStyle('feature_tag', fontName='Helvetica-Bold',
                             fontSize=9, textColor=RED, spaceAfter=4,
                             letterSpacing=2),
        'feature_h': ParagraphStyle('feature_h', fontName='Helvetica-Bold',
                             fontSize=26, textColor=DARK, leading=32,
                             spaceAfter=8),
        'feature_sub': ParagraphStyle('feature_sub', fontName='Helvetica',
                             fontSize=11.5, textColor=HexColor('#444'),
                             leading=17, spaceAfter=10, alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=10.5,
                             textColor=HexColor('#333'), leading=15,
                             spaceAfter=5, leftIndent=14),
        'plan_name': ParagraphStyle('plan_name', fontName='Helvetica-Bold',
                             fontSize=13, textColor=WHITE, alignment=TA_CENTER,
                             spaceAfter=2),
        'plan_price': ParagraphStyle('plan_price', fontName='Helvetica-Bold',
                             fontSize=22, textColor=WHITE, alignment=TA_CENTER,
                             spaceAfter=2),
        'plan_feat': ParagraphStyle('plan_feat', fontName='Helvetica',
                             fontSize=9, textColor=HexColor('#ccc'),
                             alignment=TA_CENTER, leading=13, spaceAfter=2),
        'step_n': ParagraphStyle('step_n', fontName='Helvetica-Bold',
                             fontSize=22, textColor=RED, spaceAfter=2,
                             alignment=TA_CENTER),
        'step_h': ParagraphStyle('step_h', fontName='Helvetica-Bold',
                             fontSize=12, textColor=DARK, spaceAfter=2),
        'step_b': ParagraphStyle('step_b', fontName='Helvetica', fontSize=9.5,
                             textColor=HexColor('#555'), leading=14),
        'caption': ParagraphStyle('caption', fontName='Helvetica-Oblique',
                             fontSize=8, textColor=GRAY, alignment=TA_CENTER,
                             spaceAfter=6),
        'toc_h': ParagraphStyle('toc_h', fontName='Helvetica-Bold',
                             fontSize=11, textColor=DARK, spaceAfter=4,
                             leftIndent=0),
        'section_h': ParagraphStyle('section_h', fontName='Helvetica-Bold',
                             fontSize=18, textColor=DARK, spaceAfter=4,
                             spaceBefore=6),
    }

def bg_dark(canv, doc):
    if canv._pageNumber == 1:
        canv.saveState()
        canv.setFillColor(DARK)
        canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canv.setFillColor(RED)
        canv.rect(0, PAGE_H-6*mm, PAGE_W, 6*mm, fill=1, stroke=0)
        canv.rect(0, 0, PAGE_W, 4*mm, fill=1, stroke=0)
        canv.restoreState()

def page_header(canv, doc, label="Customer Feature Guide"):
    if canv._pageNumber > 1:
        canv.saveState()
        canv.setFont("Helvetica-Bold", 8)
        canv.setFillColor(RED)
        canv.drawString(2.5*cm, PAGE_H - 1.4*cm, "STREAMIX")
        canv.setFont("Helvetica", 8)
        canv.setFillColor(GRAY)
        canv.drawRightString(PAGE_W - 2.5*cm, PAGE_H - 1.4*cm, label)
        canv.setStrokeColor(HexColor('#e8e8e8'))
        canv.setLineWidth(0.4)
        canv.line(2.5*cm, PAGE_H - 1.7*cm, PAGE_W - 2.5*cm, PAGE_H - 1.7*cm)
        canv.restoreState()

def hr(color=HexColor('#e0e0e0'), thick=0.5, before=4, after=8):
    return HRFlowable(width='100%', thickness=thick, color=color,
                      spaceBefore=before, spaceAfter=after)

def red_hr():
    return HRFlowable(width='100%', thickness=2.5, color=RED,
                      spaceBefore=0, spaceAfter=10)

def gap(n=10):
    return Spacer(1, n)


# ══════════════════════════════════════════════════════════════════════════════
#  VECTOR UI MOCKUPS
# ══════════════════════════════════════════════════════════════════════════════

def text_s(d, x, y, txt, size=8, color=WHITE, bold=False, align='left'):
    fn = "Helvetica-Bold" if bold else "Helvetica"
    s = String(x, y, txt, fontName=fn, fontSize=size, fillColor=color)
    if align == 'center':
        s.textAnchor = 'middle'
    elif align == 'right':
        s.textAnchor = 'end'
    d.add(s)

def rr(d, x, y, w, h, rx=3, color=CARD, stroke=None, stroke_w=0.5):
    r = _rrect(x, y, w, h, rx, fillColor=color,
                  strokeColor=stroke, strokeWidth=stroke_w if stroke else 0)
    d.add(r)

def pill(d, x, y, w, h, color=RED, label='', lsize=7, lcolor=WHITE):
    rr(d, x, y, w, h, rx=h/2, color=color, stroke=None)
    if label:
        text_s(d, x + w/2, y + h/2 - lsize*0.35, label, size=lsize,
               color=lcolor, bold=True, align='center')

def icon_play(d, x, y, r=7, color=WHITE):
    pts = [x - r*0.4, y - r*0.6,
           x - r*0.4, y + r*0.6,
           x + r*0.6, y]
    d.add(Polygon(pts, fillColor=color, strokeColor=None))

def icon_check(d, x, y, size=6, color=GREEN):
    c = Circle(x, y, size, fillColor=color, strokeColor=None)
    d.add(c)
    text_s(d, x, y - size*0.35, '✓', size=size*1.1, color=WHITE,
           bold=True, align='center')

def thumbnail_card(d, x, y, w, h, bg=None, title='', label=None):
    """A content thumbnail card."""
    bg = bg or HexColor('#333')
    rr(d, x, y, w, h, rx=3, color=bg)
    # gradient overlay at bottom
    d.add(Rect(x, y, w, h*0.4,
               fillColor=HexColor('#00000060'), strokeColor=None))
    if title:
        text_s(d, x + 4, y + 5, title, size=6, color=WHITE)
    if label:
        pill(d, x + 3, y + h - 14, 28, 10, color=RED, label=label, lsize=6)

# ── Mockup 1: Browser / Browse page ────────────────────────────────────────────
def mockup_browse(W=420, H=240):
    d = Drawing(W, H)
    # browser shell
    d.add(_rrect(0, 0, W, H, 6, fillColor=HexColor('#1a1a1a'), strokeColor=None))
    # browser chrome bar
    d.add(Rect(0, H-22, W, 22, fillColor=HexColor('#2d2d2d'), strokeColor=None))
    # url bar
    rr(d, W*0.25, H-17, W*0.5, 11, rx=5,
       color=HexColor('#444'), stroke=None)
    text_s(d, W*0.5, H-13, 'streamix.app/browse', size=7,
           color=HexColor('#aaa'), align='center')
    # traffic lights
    for i, c in enumerate([HexColor('#ff5f56'), HexColor('#ffbd2e'), HexColor('#27c93f')]):
        d.add(Circle(12 + i*14, H-11, 4, fillColor=c, strokeColor=None))

    # navbar inside page
    d.add(Rect(0, H-42, W, 20, fillColor=HexColor('#111'), strokeColor=None))
    text_s(d, 12, H-34, 'STREAMIX', size=9, color=RED, bold=True)
    for i, lbl in enumerate(['Home', 'TV Shows', 'Movies', 'New', 'Live']):
        text_s(d, 60 + i*54, H-34, lbl, size=7, color=HexColor('#ccc'))
    pill(d, W-55, H-38, 40, 12, color=RED, label='▶  Watch', lsize=6.5)

    # hero section
    hero_y = H-115
    d.add(Rect(0, hero_y, W, 73, fillColor=HexColor('#3a1c1c'), strokeColor=None))
    # gradient
    d.add(Rect(0, hero_y, W*0.5, 73, fillColor=HexColor('#00000060'), strokeColor=None))
    text_s(d, 12, hero_y+52, 'Featured Today', size=7.5, color=HexColor('#ccc'))
    text_s(d, 12, hero_y+36, 'The Last Horizon', size=14, color=WHITE, bold=True)
    text_s(d, 12, hero_y+22, 'Action · Sci-Fi · 2024', size=7, color=HexColor('#aaa'))
    pill(d, 12, hero_y+5, 44, 14, color=WHITE, label='▶  Play', lsize=7, lcolor=DARK)
    pill(d, 62, hero_y+5, 52, 14, color=HexColor('#55555588'),
         label='+ My List', lsize=7)

    # content rows
    row_y = hero_y - 18
    text_s(d, 8, row_y+2, 'Trending Now', size=8, color=WHITE, bold=True)
    colors_row = [HexColor('#8b2020'), HexColor('#1a3c5e'), HexColor('#1e4d1e'),
                  HexColor('#4a2060'), HexColor('#5c3000'), HexColor('#1a1a4a')]
    titles = ['Neon City', 'Deep Blue', 'Roots', 'Shadow', 'Desert Run', 'Orbit']
    for i, (c, t) in enumerate(zip(colors_row, titles)):
        thumbnail_card(d, 8 + i*68, row_y-38, 62, 36, bg=c, title=t)

    return d


# ── Mockup 2: Video Player ─────────────────────────────────────────────────────
def mockup_player(W=420, H=240):
    d = Drawing(W, H)
    # outer frame
    d.add(_rrect(0, 0, W, H, 6, fillColor=HexColor('#0a0a0a'), strokeColor=None))
    # video content bg (movie scene colour)
    d.add(Rect(0, 28, W, H-28, fillColor=HexColor('#0d1f3c'), strokeColor=None))

    # faint scene elements
    d.add(Circle(W*0.5, H*0.6, 18,
                 fillColor=HexColor('#ffffff08'), strokeColor=None))
    d.add(Circle(W*0.35, H*0.5, 30,
                 fillColor=HexColor('#ffffff05'), strokeColor=None))

    # title top-left overlay
    text_s(d, 12, H-12, 'The Last Horizon — Ep. 3', size=8, color=WHITE)

    # quality badge top-right
    pill(d, W-46, H-16, 34, 11, color=HexColor('#333'), label='1080p HD', lsize=6)

    # big play button (paused state)
    d.add(Circle(W/2, H/2 + 14, 20,
                 fillColor=HexColor('#ffffff22'), strokeColor=None))
    icon_play(d, W/2, H/2 + 14, r=10, color=WHITE)

    # bottom gradient
    d.add(Rect(0, 28, W, 55, fillColor=HexColor('#000000cc'), strokeColor=None))

    # progress bar
    bar_y = 62
    bar_w = W - 24
    d.add(_rrect(12, bar_y, bar_w, 3, 1.5,
                    fillColor=HexColor('#555'), strokeColor=None))
    # watched portion
    d.add(_rrect(12, bar_y, bar_w*0.42, 3, 1.5,
                    fillColor=RED, strokeColor=None))
    # scrubber thumb
    d.add(Circle(12 + bar_w*0.42, bar_y+1.5, 5,
                 fillColor=WHITE, strokeColor=None))
    # timestamps
    text_s(d, 14, bar_y-8, '38:21', size=7, color=HexColor('#aaa'))
    text_s(d, W-14, bar_y-8, '1:32:05', size=7, color=HexColor('#aaa'), align='right')

    # control row
    ctrl_y = 38
    # play/pause
    pill(d, 12, ctrl_y-5, 22, 14, color=HexColor('#ffffff22'), label='⏸', lsize=9, lcolor=WHITE)
    # skip
    pill(d, 38, ctrl_y-5, 22, 14, color=HexColor('#ffffff22'), label='⏭', lsize=9, lcolor=WHITE)
    # volume
    text_s(d, 70, ctrl_y+1, '🔊', size=9, color=WHITE)
    rr(d, 82, ctrl_y+2, 50, 5, rx=2, color=HexColor('#555'))
    rr(d, 82, ctrl_y+2, 38, 5, rx=2, color=WHITE)

    # right controls
    pill(d, W-120, ctrl_y-5, 52, 14, color=HexColor('#ffffff22'),
         label='CC | EN', lsize=7, lcolor=WHITE)
    pill(d, W-64, ctrl_y-5, 30, 14, color=HexColor('#ffffff22'),
         label='720p ▾', lsize=7, lcolor=WHITE)
    pill(d, W-30, ctrl_y-5, 20, 14, color=HexColor('#ffffff22'),
         label='⛶', lsize=9, lcolor=WHITE)

    # bottom bar
    d.add(Rect(0, 0, W, 28, fillColor=HexColor('#1a1a1a'), strokeColor=None))
    text_s(d, W/2, 10, 'The Last Horizon · Season 1 · Episode 3 · "Edge of Everything"',
           size=7, color=HexColor('#888'), align='center')

    return d


# ── Mockup 3: Live Streaming ───────────────────────────────────────────────────
def mockup_live(W=420, H=240):
    d = Drawing(W, H)
    rr(d, 0, 0, W, H, rx=6, color=HexColor('#111'))

    # section title
    text_s(d, 12, H-16, 'LIVE NOW', size=10, color=WHITE, bold=True)
    pill(d, 90, H-19, 28, 12, color=RED, label='● LIVE', lsize=7)

    # main featured event card
    d.add(_rrect(8, H-95, W-16, 68, 5,
                    fillColor=HexColor('#1a3c5e'), strokeColor=None))
    d.add(Rect(8, H-95, W-16, 68,
               fillColor=HexColor('#00000040'), strokeColor=None))
    # sport scene element
    d.add(Circle(W*0.75, H-60, 22,
                 fillColor=HexColor('#ffffff08'), strokeColor=None))
    text_s(d, 18, H-38, '⚽  Premier League', size=8, color=HexColor('#aaa'))
    text_s(d, 18, H-52, 'Manchester · vs · Arsenal', size=12, color=WHITE, bold=True)
    text_s(d, 18, H-66, '67\'   2 — 1', size=10, color=GOLD, bold=True)
    pill(d, 18, H-82, 40, 13, color=RED, label='● LIVE', lsize=7)
    text_s(d, 65, H-78, '142,309 watching', size=7, color=HexColor('#aaa'))
    pill(d, W-60, H-82, 44, 13, color=WHITE, label='▶  Watch', lsize=7, lcolor=DARK)

    # smaller event cards row
    card_y = H - 160
    text_s(d, 10, card_y + 14, 'Upcoming Events', size=8, color=WHITE, bold=True)
    events = [
        (HexColor('#1e2a50'), '🏀', 'NBA Finals', 'Tonight 8pm'),
        (HexColor('#1a3a1a'), '🎾', 'Wimbledon', 'Tomorrow 2pm'),
        (HexColor('#3a1a1a'), '🏎', 'F1 Monaco', 'Sun 3pm'),
        (HexColor('#2a1a3a'), '🥊', 'Boxing PPV', 'Sat 10pm'),
    ]
    for i, (c, icon, name, time_) in enumerate(events):
        cx = 8 + i*(W-16)/4
        cw = (W-16)/4 - 4
        rr(d, cx, card_y-35, cw, 40, rx=4, color=c)
        text_s(d, cx + cw/2, card_y-4, icon, size=11, color=WHITE, align='center')
        text_s(d, cx + cw/2, card_y-18, name, size=7.5, color=WHITE,
               bold=True, align='center')
        text_s(d, cx + cw/2, card_y-28, time_, size=6.5, color=HexColor('#aaa'),
               align='center')

    # TV channels strip
    ch_y = card_y - 52
    text_s(d, 10, ch_y + 10, 'TV Channels', size=8, color=WHITE, bold=True)
    ch_colors = [HexColor('#2244aa'), HexColor('#aa3322'), HexColor('#225522'),
                 HexColor('#aa6622'), HexColor('#222244')]
    ch_names = ['CNN', 'BBC', 'NatGeo', 'ESPN', 'Sky']
    for i, (c, n) in enumerate(zip(ch_colors, ch_names)):
        cx = 8 + i*82
        rr(d, cx, ch_y-18, 76, 20, rx=4, color=c)
        text_s(d, cx+38, ch_y-5, n, size=8.5, color=WHITE, bold=True, align='center')
        pill(d, cx+54, ch_y-15, 18, 8, color=RED, label='LIVE', lsize=5)

    return d


# ── Mockup 4: Profile Selector ─────────────────────────────────────────────────
def mockup_profiles(W=420, H=240):
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=DARK, strokeColor=None))

    text_s(d, W/2, H-22, "Who's Watching?", size=16,
           color=WHITE, bold=True, align='center')

    profiles = [
        (HexColor('#E50914'), 'Alex', False),
        (HexColor('#0071eb'), 'Sam',  False),
        (HexColor('#46d369'), 'Kids', True),
        (HexColor('#f5c518'), 'Guest',False),
    ]
    total = len(profiles)
    spacing = W / (total + 1)
    avatar_r = 36
    ay = H / 2 - 10

    for i, (color, name, is_kids) in enumerate(profiles):
        x = spacing * (i + 1)
        # avatar circle
        d.add(Circle(x, ay, avatar_r, fillColor=color, strokeColor=None))
        # initial letter
        text_s(d, x, ay - 8, name[0], size=26, color=WHITE,
               bold=True, align='center')
        # kids badge
        if is_kids:
            pill(d, x - 18, ay - avatar_r - 14, 36, 12,
                 color=GOLD, label='KIDS', lsize=7, lcolor=DARK)
        # name below
        text_s(d, x, ay - avatar_r - 26, name, size=9,
               color=HexColor('#ccc'), align='center')

    # PIN lock icon on 2nd profile
    lock_x = spacing * 2
    d.add(Circle(lock_x + avatar_r - 5, ay + avatar_r - 5, 9,
                 fillColor=HexColor('#333'), strokeColor=None))
    text_s(d, lock_x + avatar_r - 5, ay + avatar_r - 8, '🔒', size=8,
           align='center')

    # Manage Profiles button
    pill(d, W/2 - 60, 18, 120, 22, color=HexColor('#333'),
         label='Manage Profiles', lsize=8, lcolor=LGRAY)

    return d


# ── Mockup 5: Search ────────────────────────────────────────────────────────────
def mockup_search(W=420, H=240):
    d = Drawing(W, H)
    rr(d, 0, 0, W, H, rx=6, color=HexColor('#111'))

    # search bar
    bar_y = H - 34
    rr(d, 10, bar_y, W - 20, 22, rx=11, color=HexColor('#2a2a2a'),
       stroke=HexColor('#555'), stroke_w=1)
    text_s(d, 30, bar_y + 7, '🔍', size=10, color=GRAY)
    text_s(d, 50, bar_y + 8, 'sci-fi action 2024', size=9,
           color=HexColor('#fff'))
    # clear X
    d.add(Circle(W - 22, bar_y + 11, 7, fillColor=HexColor('#555'), strokeColor=None))
    text_s(d, W - 22, bar_y + 8, '×', size=9, color=WHITE, align='center')

    # result label
    text_s(d, 12, bar_y - 12, '24 results for "sci-fi action 2024"',
           size=8, color=HexColor('#aaa'))

    # filter pills
    filters = ['All', 'Movies', 'Series', 'Live', '2024', 'Action', 'Sci-Fi']
    fx = 10
    for f in filters:
        fw = len(f) * 7 + 14
        is_active = f in ('All',)
        pill(d, fx, bar_y - 34, fw, 14,
             color=RED if is_active else HexColor('#333'),
             label=f, lsize=7,
             lcolor=WHITE if is_active else HexColor('#ccc'))
        fx += fw + 6

    # result grid
    grid_colors = [
        HexColor('#1a2a4a'), HexColor('#2a1a1a'), HexColor('#1a3a1a'),
        HexColor('#2a1a3a'), HexColor('#3a2a0a'), HexColor('#0a2a3a'),
        HexColor('#2a2a1a'), HexColor('#1a1a3a'), HexColor('#3a1a2a'),
        HexColor('#0a3a2a'),
    ]
    titles2 = ['Interstellar 2', 'Red Planet', 'Jungle Run', 'Shadow Realm',
               'Sunfall', 'Deep Space', 'Lost Signal', 'Void Station', 'Dark Matter', 'Echo Base']
    years   = ['2024','2024','2023','2024','2024','2023','2024','2024','2023','2024']
    gx, gy = 8, bar_y - 45
    card_w, card_h = 76, 52
    for i, (c, t, y) in enumerate(zip(grid_colors, titles2, years)):
        col = i % 5
        row = i // 5
        cx = gx + col * (card_w + 6)
        cy = gy - row * (card_h + 8)
        rr(d, cx, cy, card_w, card_h, rx=4, color=c)
        d.add(Rect(cx, cy, card_w, card_h*0.35,
                   fillColor=HexColor('#00000066'), strokeColor=None))
        text_s(d, cx + 4, cy + 5, t, size=6, color=WHITE)
        text_s(d, cx + 4, cy + 14, y, size=5.5, color=HexColor('#aaa'))
        # rating star
        text_s(d, cx + card_w - 20, cy + card_h - 10, '★ 8.2', size=6, color=GOLD)

    return d


# ── Mockup 6: Watchlist ─────────────────────────────────────────────────────────
def mockup_watchlist(W=420, H=240):
    d = Drawing(W, H)
    rr(d, 0, 0, W, H, rx=6, color=HexColor('#111'))

    text_s(d, 12, H-16, 'My List', size=12, color=WHITE, bold=True)
    text_s(d, 12, H-28, '18 titles', size=8, color=GRAY)

    view_colors = [
        HexColor('#2d1a0a'), HexColor('#0a1a2d'), HexColor('#0a2d1a'),
        HexColor('#1a0a2d'), HexColor('#2d1a1a'), HexColor('#0a1a0a'),
        HexColor('#2d2d0a'), HexColor('#1a0a0a'),
    ]
    wl_titles = ['Breaking Dawn', 'Ocean\'s Echo', 'Wild North', 'Phantom Code',
                 'Crimson Peak', 'Forest Dark', 'Desert Sun', 'Last Stand']
    wl_genres = ['Drama','Thriller','Doc.','Sci-Fi','Horror','Nature','Action','War']

    grid_y = H - 42
    for i in range(8):
        col = i % 4
        row = i // 4
        cx = 8 + col * ((W-16)/4)
        cy = grid_y - row * 96
        cw = (W-16)/4 - 6
        ch = 82
        rr(d, cx, cy, cw, ch, rx=4, color=view_colors[i])

        # progress bar for "in progress" items
        if i in (0, 2, 5):
            pct = [0.65, 0.30, 0.85][0 if i==0 else (1 if i==2 else 2)]
            d.add(Rect(cx, cy, cw, 3, fillColor=HexColor('#555'), strokeColor=None))
            d.add(Rect(cx, cy, cw*pct, 3, fillColor=RED, strokeColor=None))

        text_s(d, cx+4, cy+8, wl_titles[i], size=6.5, color=WHITE, bold=True)
        text_s(d, cx+4, cy+18, wl_genres[i], size=6, color=GRAY)

        # remove button top-right
        d.add(Circle(cx+cw-8, cy+ch-8, 7,
                     fillColor=HexColor('#333'), strokeColor=None))
        text_s(d, cx+cw-8, cy+ch-11, '×', size=8, color=WHITE, align='center')

        # play overlay
        d.add(Circle(cx+cw/2, cy+ch/2, 12,
                     fillColor=HexColor('#ffffff18'), strokeColor=None))
        icon_play(d, cx+cw/2, cy+ch/2, r=6, color=WHITE)

    return d


# ── Mockup 7: Mobile view (Continue Watching) ──────────────────────────────────
def mockup_continue_watching(W=420, H=240):
    d = Drawing(W, H)
    rr(d, 0, 0, W, H, rx=6, color=HexColor('#111'))

    text_s(d, 12, H-16, 'Continue Watching', size=11, color=WHITE, bold=True)
    text_s(d, 12, H-29, 'Pick up where you left off, on any device', size=7.5, color=GRAY)

    cw_colors = [
        (HexColor('#1a2a4a'), 'The Last Horizon',  'Ep 3 of 8', 0.42),
        (HexColor('#2a1a0a'), 'Desert Run',         'Ep 5 of 10', 0.70),
        (HexColor('#0a2d1a'), 'Wild North',         '38 min left', 0.28),
        (HexColor('#2d0a1a'), 'Phantom Code',       'Ep 1 of 6',  0.12),
    ]
    for i, (c, title, sub, pct) in enumerate(cw_colors):
        cx = 8 + i * 101
        cy = H - 105
        cw_ = 94
        ch  = 68
        rr(d, cx, cy, cw_, ch, rx=4, color=c)

        # gradient
        d.add(Rect(cx, cy, cw_, ch*0.4,
                   fillColor=HexColor('#00000077'), strokeColor=None))

        text_s(d, cx + 4, cy + 8, title, size=6.5, color=WHITE, bold=True)
        text_s(d, cx + 4, cy + 18, sub, size=6, color=HexColor('#aaa'))

        # progress bar
        d.add(Rect(cx, cy, cw_, 3.5, fillColor=HexColor('#444'), strokeColor=None))
        d.add(Rect(cx, cy, cw_*pct, 3.5, fillColor=RED, strokeColor=None))

        # play button
        d.add(Circle(cx+cw_/2, cy+ch/2+4, 14,
                     fillColor=HexColor('#ffffff20'), strokeColor=None))
        icon_play(d, cx+cw_/2, cy+ch/2+4, r=8, color=WHITE)

        # device icons row
        text_s(d, cx+4, cy-10, '💻 📱 📺', size=8, color=HexColor('#888'))

    # sync indicator
    pill(d, W/2-65, H-160, 130, 18, color=HexColor('#1a3a1a'),
         label='✓  Progress synced across all devices', lsize=7.5,
         lcolor=HexColor('#46d369'))

    return d


# ── Mockup 8: Account / Subscription page ──────────────────────────────────────
def mockup_account(W=420, H=240):
    d = Drawing(W, H)
    rr(d, 0, 0, W, H, rx=6, color=HexColor('#111'))

    # sidebar
    d.add(Rect(0, 0, 100, H, fillColor=HexColor('#1a1a1a'), strokeColor=None))
    text_s(d, 50, H-18, 'Account', size=10, color=WHITE, bold=True, align='center')
    menu = ['Membership', 'Billing', 'Profiles', 'Security', 'Language']
    for i, m in enumerate(menu):
        is_sel = i == 0
        if is_sel:
            d.add(Rect(0, H - 40 - i*28, 100, 24,
                       fillColor=HexColor('#2a2a2a'), strokeColor=None))
            d.add(Rect(0, H - 40 - i*28, 3, 24,
                       fillColor=RED, strokeColor=None))
        text_s(d, 14, H - 30 - i*28, m, size=8,
               color=WHITE if is_sel else HexColor('#888'))

    # main content area
    content_x = 112
    cw = W - content_x - 10
    text_s(d, content_x, H-18, 'Membership & Billing', size=10,
           color=WHITE, bold=True)

    # current plan card
    rr(d, content_x, H-75, cw, 50, rx=5, color=HexColor('#1f1f1f'),
       stroke=RED, stroke_w=1.5)
    pill(d, content_x+8, H-34, 58, 14, color=RED, label='● PREMIUM', lsize=7)
    text_s(d, content_x+8, H-50, '$19.99 / month', size=11,
           color=WHITE, bold=True)
    text_s(d, content_x+8, H-62, 'Next billing: July 10, 2025', size=7,
           color=HexColor('#aaa'))
    pill(d, content_x+cw-68, H-55, 60, 16, color=HexColor('#333'),
         label='Change Plan', lsize=7)

    # feature list
    features = [
        ('4K Ultra HD',          True),
        ('4 Streams at once',    True),
        ('Unlimited downloads',  True),
        ('No advertisements',    True),
        ('All live events',      True),
    ]
    for i, (feat, ok) in enumerate(features):
        fy = H - 92 - i*22
        icon_check(d, content_x+10, fy+5, size=6, color=GREEN)
        text_s(d, content_x+24, fy+2, feat, size=8, color=HexColor('#ccc'))

    return d


# ── Mockup 9: Ad experience (Free tier) ────────────────────────────────────────
def mockup_ads(W=420, H=240):
    d = Drawing(W, H)
    rr(d, 0, 0, W, H, rx=6, color=HexColor('#0a0a0a'))

    # video bg (player)
    d.add(Rect(0, 30, W, H-30, fillColor=HexColor('#0d1a2a'), strokeColor=None))

    # Ad overlay (pre-roll)
    d.add(Rect(0, 30, W, H-30, fillColor=HexColor('#000000aa'), strokeColor=None))

    # Ad video area (centered)
    aw, ah = 200, 110
    ax = (W-aw)/2
    ay = (H - ah)/2 + 10
    rr(d, ax, ay, aw, ah, rx=4, color=HexColor('#1a3050'))
    # ad content
    d.add(Circle(ax+aw/2, ay+ah/2+10, 18,
                 fillColor=HexColor('#E50914'), strokeColor=None))
    text_s(d, ax+aw/2, ay+ah/2+2, 'STREAMIX', size=9, color=WHITE,
           bold=True, align='center')
    text_s(d, ax+aw/2, ay+ah/2+16, 'PREMIUM', size=7, color=GOLD,
           align='center')
    text_s(d, ax+aw/2, ay+ah/2-12, 'Go ad-free today', size=8,
           color=HexColor('#ccc'), align='center')

    # AD badge top-left
    pill(d, ax+6, ay+ah-16, 22, 11, color=GOLD, label='AD', lsize=7, lcolor=DARK)
    text_s(d, ax+32, ay+ah-11, 'Streamix Premium', size=7,
           color=HexColor('#aaa'))

    # Ad progress bar
    d.add(Rect(ax, ay, aw, 3, fillColor=HexColor('#444'), strokeColor=None))
    d.add(Rect(ax, ay, aw*0.35, 3, fillColor=GOLD, strokeColor=None))

    # Skip button (counting down)
    pill(d, ax+aw-72, ay+6, 64, 18, color=HexColor('#333'),
         label='Skip in 3s ▶▶', lsize=7)

    # bottom label
    text_s(d, W/2, 10,
           'Free tier: short ads before and during content  ·  Upgrade to remove all ads',
           size=7, color=GRAY, align='center')

    # mid-roll banner mockup (small, at bottom of player)
    rr(d, 10, 36, W-20, 22, rx=4, color=HexColor('#1f1f1f'),
       stroke=HexColor('#444'), stroke_w=0.5)
    d.add(Rect(10, 36, 34, 22, fillColor=HexColor('#E50914'), strokeColor=None))
    text_s(d, 27, 44, 'AD', size=9, color=WHITE, bold=True, align='center')
    text_s(d, 52, 49, 'Upgrade for unlimited ad-free streaming', size=7.5,
           color=WHITE, bold=True)
    text_s(d, 52, 40, 'From $7.99/month', size=7, color=HexColor('#aaa'))
    pill(d, W-90, 40, 60, 13, color=WHITE, label='Upgrade Now', lsize=7, lcolor=DARK)
    d.add(Circle(W-22, 47, 6, fillColor=HexColor('#444'), strokeColor=None))
    text_s(d, W-22, 44, '×', size=8, color=WHITE, align='center')

    return d


# ── Mockup 10: Multi-device ─────────────────────────────────────────────────────
def mockup_devices(W=420, H=240):
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=HexColor('#0a0a0a'), strokeColor=None))

    # TV
    tv_x, tv_y, tv_w, tv_h = 20, 60, 190, 120
    rr(d, tv_x, tv_y, tv_w, tv_h, rx=4, color=HexColor('#1a1a1a'),
       stroke=HexColor('#333'), stroke_w=1.5)
    # screen
    rr(d, tv_x+6, tv_y+8, tv_w-12, tv_h-22, rx=2, color=HexColor('#0d1f3c'))
    icon_play(d, tv_x+tv_w/2, tv_y+tv_h/2, r=12, color=WHITE)
    # stand
    d.add(Rect(tv_x+tv_w/2-15, tv_y-6, 30, 8,
               fillColor=HexColor('#333'), strokeColor=None))
    d.add(Rect(tv_x+tv_w/2-22, tv_y-8, 44, 3,
               fillColor=HexColor('#333'), strokeColor=None))
    text_s(d, tv_x+tv_w/2, tv_y-14, 'Smart TV', size=7.5,
           color=GRAY, align='center')

    # Laptop
    lap_x, lap_y, lap_w, lap_h = 220, 70, 140, 95
    rr(d, lap_x, lap_y, lap_w, lap_h, rx=3, color=HexColor('#222'),
       stroke=HexColor('#333'), stroke_w=1)
    rr(d, lap_x+5, lap_y+6, lap_w-10, lap_h-14, rx=2, color=HexColor('#0d1f3c'))
    icon_play(d, lap_x+lap_w/2, lap_y+lap_h/2+2, r=9, color=WHITE)
    d.add(Rect(lap_x-8, lap_y-4, lap_w+16, 4,
               fillColor=HexColor('#222'), strokeColor=None))
    d.add(Rect(lap_x-18, lap_y-8, lap_w+36, 4,
               fillColor=HexColor('#333'), strokeColor=None))
    text_s(d, lap_x+lap_w/2, lap_y-18, 'Laptop', size=7.5,
           color=GRAY, align='center')

    # Phone
    ph_x, ph_y, ph_w, ph_h = 372, 90, 38, 72
    rr(d, ph_x, ph_y, ph_w, ph_h, rx=6, color=HexColor('#222'),
       stroke=HexColor('#333'), stroke_w=1)
    rr(d, ph_x+3, ph_y+8, ph_w-6, ph_h-14, rx=2, color=HexColor('#0d1f3c'))
    icon_play(d, ph_x+ph_w/2, ph_y+ph_h/2+1, r=7, color=WHITE)
    # notch
    rr(d, ph_x+ph_w/2-6, ph_y+ph_h-6, 12, 4, rx=2, color=HexColor('#333'))
    text_s(d, ph_x+ph_w/2, ph_y-8, 'Mobile', size=7.5,
           color=GRAY, align='center')

    # sync arc (visual)
    text_s(d, W/2, 30, '⟳  Seamlessly synced across all your screens', size=9,
           color=HexColor('#888'), align='center')

    # feature pills
    pills_data = [
        (W/2 - 120, 10, 'Continue on any device'),
        (W/2 + 10,  10, 'Progress auto-saved'),
    ]
    for px, py, lbl in pills_data:
        pill(d, px, py, len(lbl)*6+14, 14, color=HexColor('#1a1a1a'),
             label=lbl, lsize=7, lcolor=HexColor('#aaa'))

    return d


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════

def build_customer_doc(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Streamix – Customer Feature Guide",
        author="Streamix",
    )
    st = S()
    story = []
    TODAY = date.today().strftime("%B %d, %Y")

    def mockup_block(drawing, caption=''):
        """Wrap a Drawing in a centred block with optional caption."""
        items = [gap(6)]
        # centre via a 1-cell table
        tbl = Table([[drawing]], colWidths=[drawing.width])
        tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        items.append(tbl)
        if caption:
            items.append(Paragraph(caption, st['caption']))
        items.append(gap(10))
        return items

    def feature_header(tag, title, body):
        return [
            Paragraph(tag.upper(), st['feature_tag']),
            Paragraph(title, st['feature_h']),
            red_hr(),
            Paragraph(body, st['feature_sub']),
        ]

    def bul(items):
        return [Paragraph(f"✦  {i}", st['bullet']) for i in items]

    # ── COVER ──────────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 2.6*cm),
        Paragraph("STREAMIX", st['feature_tag']),
        Spacer(1, 0.5*cm),
        Paragraph("Everything You Love\nAbout Streaming,\nPerfected.", st['ct']),
        Spacer(1, 0.5*cm),
        Paragraph("Movies · Series · Live Sports · TV Channels\n"
                  "All in one place, on every screen you own.", st['cs']),
        Spacer(1, 1.6*cm),
        HRFlowable(width='50%', thickness=1.5, color=RED,
                   hAlign='CENTER', spaceBefore=0, spaceAfter=14),
        Paragraph("Customer Feature Guide", st['cm']),
        Paragraph(f"Updated {TODAY}", st['cm']),
        PageBreak(),
    ]

    # ── TABLE OF CONTENTS ──────────────────────────────────────────────────────
    story.append(Paragraph("What's Inside", st['section_h']))
    story.append(red_hr())
    toc = [
        ("01", "Browse a World of Content"),
        ("02", "Crystal-Clear Video Quality"),
        ("03", "Live Sports & Events"),
        ("04", "Multiple Profiles for Everyone"),
        ("05", "Find Exactly What You Want"),
        ("06", "Your Watchlist & Continue Watching"),
        ("07", "Free Tier & Ad Experience"),
        ("08", "Watch on Any Screen"),
        ("09", "Your Account & Subscription Plans"),
        ("10", "Getting Started in 3 Steps"),
    ]
    tbl_data = []
    for i in range(0, len(toc), 2):
        row = []
        for j in range(2):
            if i + j < len(toc):
                num, ttl = toc[i + j]
                row.append(
                    Paragraph(f"<font color='#E50914'><b>{num}</b></font>  {ttl}",
                              st['toc_h'])
                )
            else:
                row.append(Paragraph("", st['toc_h']))
        tbl_data.append(row)
    tbl = Table(tbl_data, colWidths=[CONTENT_W/2 - 5, CONTENT_W/2 - 5])
    tbl.setStyle(TableStyle([
        ('VALIGN',  (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.4, HexColor('#e8e8e8')),
    ]))
    story.append(tbl)
    story.append(PageBreak())

    # ── 01 BROWSE ──────────────────────────────────────────────────────────────
    story += feature_header(
        "01 · Browse",
        "A World of Content\nAt Your Fingertips",
        "Thousands of movies, TV series, documentaries, and short films organised "
        "into beautiful, curated rows. Streamix surfaces exactly the right content "
        "for you — whether you're in the mood for a blockbuster, an indie gem, "
        "or something brand new.")
    story += mockup_block(mockup_browse(),
                          "Browse page — Hero banner + Trending row")
    story += bul([
        "Curated genre rows updated daily — Action, Drama, Comedy, Thriller, Documentary, Kids, and more.",
        "Hero banner highlights today's must-watch pick with a one-click Play button.",
        "Trending Now row shows what the Streamix community is watching right now.",
        "New Releases row keeps you up to date with the latest additions every week.",
        "Content filter pills let you narrow by Movies, Series, or All with one tap.",
    ])
    story.append(PageBreak())

    # ── 02 PLAYER ──────────────────────────────────────────────────────────────
    story += feature_header(
        "02 · Video Quality",
        "Crystal-Clear Video,\nEvery Time",
        "Streamix adapts the video quality to your connection in real time. "
        "Whether you're on fibre broadband or a busy mobile network, "
        "you always get the sharpest picture possible — no manual settings needed.")
    story += mockup_block(mockup_player(),
                          "Video player — controls, progress bar, quality selector")
    story += bul([
        "Adaptive bitrate: automatically switches between 360p, 720p, 1080p, and 4K based on your bandwidth.",
        "Manual quality override: lock to a specific resolution from the quality menu at any time.",
        "Multi-language subtitles and closed captions — select your language from the CC button.",
        "Keyboard shortcuts for power users: Space to play/pause, ← → to skip 10 seconds, M to mute.",
        "Controls disappear after 3 seconds of inactivity for a truly immersive, distraction-free view.",
        "Full-screen mode with one click — works on laptop, desktop, and smart TV browsers.",
    ])
    story.append(PageBreak())

    # ── 03 LIVE ────────────────────────────────────────────────────────────────
    story += feature_header(
        "03 · Live",
        "Never Miss a Live\nMoment",
        "From Premier League football to boxing, Formula 1, NBA, tennis, "
        "and live concerts — Streamix brings you the world's biggest moments "
        "as they happen. Plus 24/7 TV channels for news, sports, and entertainment.")
    story += mockup_block(mockup_live(),
                          "Live page — Featured match, upcoming events, TV channels")
    story += bul([
        "Live Now — jump straight into matches and events happening right this second.",
        "Upcoming Schedule — see all events for the next 7 days, set reminders with one tap.",
        "Real-time stats: live score, current time, and viewer count shown on every live card.",
        "TV Channels — 24/7 linear channels including news, sports, entertainment, and documentary.",
        "Pay-Per-View events — buy access to premium boxing, MMA, and concert events individually.",
        "Low-latency HLS delivery — less than 5 seconds behind real time.",
    ])
    story.append(PageBreak())

    # ── 04 PROFILES ────────────────────────────────────────────────────────────
    story += feature_header(
        "04 · Profiles",
        "One Account,\nEveryone's Space",
        "Up to 5 individual profiles per account — each with its own watch history, "
        "recommendations, language settings, and maturity controls. "
        "Everyone in the household gets a Streamix experience built just for them.")
    story += mockup_block(mockup_profiles(),
                          "Profile selector — 'Who's Watching?' screen")
    story += bul([
        "Up to 5 profiles per account — perfect for families, flatmates, and housemates.",
        "Independent watch history: your viewing never influences someone else's feed.",
        "Kids profile with maturity lock — only age-appropriate content is visible.",
        "PIN-protected profiles: set a PIN to keep your profile private on shared devices.",
        "Custom avatar and display name for each profile.",
        "Individual language and subtitle preferences saved per profile.",
        "Profile switching is instant — no need to log out and back in.",
    ])
    story.append(PageBreak())

    # ── 05 SEARCH ──────────────────────────────────────────────────────────────
    story += feature_header(
        "05 · Search",
        "Find Exactly\nWhat You Want",
        "Streamix's intelligent search finds what you're looking for instantly — "
        "even if you're not sure of the exact title. Fuzzy matching understands "
        "typos and partial names, and powerful filters narrow your results in seconds.")
    story += mockup_block(mockup_search(),
                          "Search page — results grid with filters")
    story += bul([
        "Type any word from a title, actor name, or genre — results appear as you type.",
        "Fuzzy matching: 'inter stelar' still finds Interstellar. No exact spelling required.",
        "Filter results by Type (Movies / Series), Genre, and Release Year simultaneously.",
        "Each result card shows title, year, and average rating at a glance.",
        "Results update in real time with no page refresh needed.",
    ])
    story.append(PageBreak())

    # ── 06 WATCHLIST & CONTINUE WATCHING ──────────────────────────────────────
    story += feature_header(
        "06 · Watchlist",
        "Save It Now,\nWatch It Later",
        "Spotted something you want to watch but aren't ready yet? "
        "Add it to My List in one tap. Pick up any title exactly where you stopped — "
        "even if you switch from your phone to your TV mid-episode.")
    story += mockup_block(mockup_watchlist(),
                          "My List — watchlist grid with progress bars")
    story += mockup_block(mockup_continue_watching(),
                          "Continue Watching — resume on any device")
    story += bul([
        "Add any title to My List from the browse page, search results, or title detail page.",
        "My List is personal to each profile — different lists for different household members.",
        "Progress bars on each card show how far you've watched.",
        "Continue Watching row on the browse page surfaces your in-progress titles automatically.",
        "Progress syncs instantly across all your devices — pause on your phone, resume on your TV.",
        "Mark as complete: skip to the next episode or the next title in your list.",
    ])
    story.append(PageBreak())

    # ── 07 ADS ─────────────────────────────────────────────────────────────────
    story += feature_header(
        "07 · Free Tier",
        "Stream for Free,\nUpgrade Anytime",
        "The Streamix Free tier gives you access to thousands of titles at no cost. "
        "Free viewing is supported by short, non-intrusive ads. "
        "Ready for an uninterrupted experience? Upgrading to a paid plan removes all ads instantly.")
    story += mockup_block(mockup_ads(),
                          "Free tier ad experience — pre-roll and mid-roll banner")
    story += bul([
        "Pre-roll ad: a short video ad (up to 30 seconds) plays before your content starts. Skip after 5 seconds.",
        "Mid-roll banner: a small overlay ad appears every 15 minutes. Dismiss after 5 seconds.",
        "Ad volume can be muted independently — your content volume is preserved.",
        "Every ad includes a direct link to upgrade and remove all ads immediately.",
        "Paid tiers (Basic, Standard, Premium) are 100% ad-free — no pre-roll, no mid-roll, ever.",
        "Free tier still gives you full access to the catalogue up to 720p resolution.",
    ])
    story.append(PageBreak())

    # ── 08 DEVICES ─────────────────────────────────────────────────────────────
    story += feature_header(
        "08 · Any Screen",
        "Watch on Every\nScreen You Own",
        "Streamix is designed for every device you use — smart TV, laptop, tablet, "
        "or smartphone. Your watch progress, watchlist, and preferences follow you "
        "everywhere automatically.")
    story += mockup_block(mockup_devices(),
                          "Seamless experience across Smart TV, Laptop, and Mobile")
    story += bul([
        "Smart TV: available through your TV's web browser; native app coming in a future update.",
        "Laptop / Desktop: full feature experience on any modern browser (Chrome, Firefox, Safari, Edge).",
        "Mobile: responsive web app optimised for touch on iOS and Android — native apps coming soon.",
        "Automatic quality adjustment: 4K on your TV, 720p on mobile to save data.",
        "Progress syncs in real time — pause on one device, continue on another within seconds.",
        "Standard plan: stream on 2 devices simultaneously. Premium plan: stream on 4 devices at once.",
    ])
    story.append(PageBreak())

    # ── 09 PLANS ───────────────────────────────────────────────────────────────
    story += feature_header(
        "09 · Plans",
        "Choose the Plan\nThat's Right for You",
        "Whether you're a casual viewer or a whole household of streaming enthusiasts, "
        "there's a Streamix plan for you. Start free and upgrade whenever you're ready.")
    story.append(gap(8))

    plan_colors = [HexColor('#1f1f1f'), HexColor('#0d1f3c'),
                   HexColor('#0a2d1a'), HexColor('#2d1020')]
    plan_borders = [HexColor('#444'), BLUE, GREEN, RED]
    plans = [
        ("FREE",     "$0",     "/mo", [
            "Unlimited browsing",
            "Up to 720p",
            "1 stream",
            "Short ads",
            "All genres",
        ]),
        ("BASIC",    "$7.99",  "/mo", [
            "Everything in Free",
            "Up to 1080p Full HD",
            "1 stream",
            "No ads",
            "All live events",
        ]),
        ("STANDARD", "$13.99", "/mo", [
            "Everything in Basic",
            "Up to 1080p Full HD",
            "2 simultaneous streams",
            "2 offline downloads",
            "All live events",
        ]),
        ("PREMIUM",  "$19.99", "/mo", [
            "Everything in Standard",
            "Up to 4K Ultra HD",
            "4 simultaneous streams",
            "Unlimited downloads",
            "All live + PPV events",
        ]),
    ]

    plan_cells = []
    for (name, price, period, feats), bg, border in zip(plans, plan_colors, plan_borders):
        is_pop = name == "PREMIUM"
        cell_items = []
        if is_pop:
            cell_items.append(
                Paragraph("<font color='#E50914'>★ Most Popular</font>",
                          st['plan_feat']))
        cell_items.append(Paragraph(name, st['plan_name']))
        cell_items.append(
            Paragraph(f"<b>{price}</b><font size=9>{period}</font>",
                      st['plan_price']))
        for feat in feats:
            cell_items.append(
                Paragraph(f"<font color='#46d369'>✓</font>  {feat}",
                          st['plan_feat']))
        plan_cells.append(cell_items)

    # render as 4-column table
    plan_tbl = Table(
        [plan_cells],
        colWidths=[(CONTENT_W)/4] * 4,
        rowHeights=[None]
    )
    plan_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), plan_colors[0]),
        ('BACKGROUND', (1,0), (1,0), plan_colors[1]),
        ('BACKGROUND', (2,0), (2,0), plan_colors[2]),
        ('BACKGROUND', (3,0), (3,0), plan_colors[3]),
        ('BOX', (0,0), (0,0), 1,   plan_borders[0]),
        ('BOX', (1,0), (1,0), 1,   plan_borders[1]),
        ('BOX', (2,0), (2,0), 1,   plan_borders[2]),
        ('BOX', (3,0), (3,0), 2.5, plan_borders[3]),
        ('VALIGN',   (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 14),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),

    ]))
    story.append(plan_tbl)
    story.append(gap(8))
    story.append(
        Paragraph("All plans include access to the full Streamix content library. "
                  "Cancel anytime — no contracts, no cancellation fees.",
                  st['caption']))
    story.append(PageBreak())

    # ── 10 GETTING STARTED ─────────────────────────────────────────────────────
    story += feature_header(
        "10 · Get Started",
        "Ready to Watch?\nHere's How",
        "Getting started with Streamix takes less than two minutes. "
        "No credit card required for the Free tier — just create an account and start watching.")
    story.append(gap(16))

    steps = [
        ("1", "Create Your Account",
         "Visit streamix.app and click Sign Up. Enter your email address "
         "and choose a password. That's it — your account is ready immediately."),
        ("2", "Pick Your Plan",
         "Choose Free to start watching right away with short ads, "
         "or select Basic, Standard, or Premium for an ad-free experience "
         "with higher quality and more simultaneous streams."),
        ("3", "Start Watching",
         "Browse the catalogue, search for a title you love, "
         "or let Streamix suggest something based on your mood. "
         "Hit Play and enjoy."),
    ]

    step_data = []
    for num, heading, body in steps:
        step_data.append([
            Paragraph(num, st['step_n']),
            [
                Paragraph(heading, st['step_h']),
                Paragraph(body, st['step_b']),
            ]
        ])

    step_tbl = Table(step_data,
                     colWidths=[1.2*cm, CONTENT_W - 1.4*cm])
    step_tbl.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor('#eeeeee')),
    ]))
    story.append(step_tbl)
    story.append(gap(20))
    story.append(hr(color=RED, thick=2))
    story.append(
        Paragraph(
            "Questions? Visit our <u>Help Centre</u> at streamix.app/help  "
            "or email <u>support@streamix.app</u>",
            st['feature_sub']))
    story.append(gap(10))
    story.append(
        Paragraph(
            f"© {date.today().year} Streamix. All rights reserved.  "
            "Streamix is a registered trademark. Content availability varies by region.",
            st['cm']))

    # ── BUILD ──────────────────────────────────────────────────────────────────
    def on_page(c, d):
        bg_dark(c, d)
        page_header(c, d, "Customer Feature Guide")

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page,
              canvasmaker=NumberedCanvas)
    print(f"✓  Customer feature guide: {path}")


if __name__ == "__main__":
    build_customer_doc("/home/user/streming/Streamix_Customer_Feature_Guide.pdf")
    print("Done.")
