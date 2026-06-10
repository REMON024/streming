"""
Streamix PDF documentation generator — v2.0
Reflects the full current codebase (as of latest commit).
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import date

# ── Brand palette ──────────────────────────────────────────────────────────────
RED     = HexColor('#E50914')
DARK    = HexColor('#141414')
MID     = HexColor('#2d2d2d')
GRAY    = HexColor('#757575')
LGRAY   = HexColor('#e8e8e8')
LIGHT   = HexColor('#f5f5f1')
WHITE   = colors.white
BLACK   = colors.black
GOLD    = HexColor('#f5a623')
BLUE    = HexColor('#1a73e8')

PAGE_W, PAGE_H = A4

# ── Page numbering canvas ──────────────────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(total)
            super().showPage()
        super().save()

    def _draw_footer(self, total):
        p = self._pageNumber
        if p == 1:
            return
        self.setFont("Helvetica", 8)
        self.setFillColor(GRAY)
        self.drawRightString(PAGE_W - 2*cm, 1.1*cm, f"Page {p} of {total}")
        self.setStrokeColor(LGRAY)
        self.setLineWidth(0.4)
        self.line(2*cm, 1.55*cm, PAGE_W - 2*cm, 1.55*cm)


# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    return {
        'cover_tag': ParagraphStyle('cover_tag',
            fontName='Helvetica-Bold', fontSize=10, textColor=RED,
            spaceAfter=8, alignment=TA_CENTER, letterSpacing=3),
        'cover_title': ParagraphStyle('cover_title',
            fontName='Helvetica-Bold', fontSize=36, textColor=WHITE,
            spaceAfter=10, alignment=TA_CENTER, leading=44),
        'cover_sub': ParagraphStyle('cover_sub',
            fontName='Helvetica', fontSize=14, textColor=LIGHT,
            spaceAfter=6, alignment=TA_CENTER, leading=20),
        'cover_meta': ParagraphStyle('cover_meta',
            fontName='Helvetica', fontSize=9, textColor=HexColor('#888888'),
            alignment=TA_CENTER, spaceAfter=3),
        'h1': ParagraphStyle('h1',
            fontName='Helvetica-Bold', fontSize=20, textColor=RED,
            spaceBefore=22, spaceAfter=4, leading=25),
        'h2': ParagraphStyle('h2',
            fontName='Helvetica-Bold', fontSize=13, textColor=DARK,
            spaceBefore=14, spaceAfter=4, leading=17),
        'h3': ParagraphStyle('h3',
            fontName='Helvetica-Bold', fontSize=10.5, textColor=HexColor('#333'),
            spaceBefore=10, spaceAfter=3, leading=14),
        'body': ParagraphStyle('body',
            fontName='Helvetica', fontSize=10, textColor=HexColor('#2e2e2e'),
            spaceAfter=6, leading=15, alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet',
            fontName='Helvetica', fontSize=10, textColor=HexColor('#2e2e2e'),
            spaceAfter=4, leading=14, leftIndent=14, bulletIndent=2),
        'subbullet': ParagraphStyle('subbullet',
            fontName='Helvetica', fontSize=9.5, textColor=HexColor('#444'),
            spaceAfter=3, leading=13, leftIndent=28, bulletIndent=16),
        'code': ParagraphStyle('code',
            fontName='Courier', fontSize=8.5, textColor=HexColor('#1a1a1a'),
            backColor=HexColor('#f6f6f6'), spaceAfter=2, leading=13,
            leftIndent=10, rightIndent=10),
        'code_label': ParagraphStyle('code_label',
            fontName='Courier-Bold', fontSize=8.5, textColor=HexColor('#1a1a1a'),
            backColor=HexColor('#ececec'), spaceAfter=1, leading=13,
            leftIndent=10, rightIndent=10),
        'th': ParagraphStyle('th',
            fontName='Helvetica-Bold', fontSize=9, textColor=WHITE),
        'td': ParagraphStyle('td',
            fontName='Helvetica', fontSize=9, textColor=DARK, leading=12),
        'td_code': ParagraphStyle('td_code',
            fontName='Courier', fontSize=8, textColor=HexColor('#1a1a1a'), leading=11),
        'td_bold': ParagraphStyle('td_bold',
            fontName='Helvetica-Bold', fontSize=9, textColor=DARK, leading=12),
        'caption': ParagraphStyle('caption',
            fontName='Helvetica-Oblique', fontSize=8, textColor=GRAY,
            spaceAfter=8, alignment=TA_CENTER),
        'toc': ParagraphStyle('toc',
            fontName='Helvetica-Bold', fontSize=11, textColor=DARK,
            spaceAfter=4, leftIndent=0),
        'toc2': ParagraphStyle('toc2',
            fontName='Helvetica', fontSize=10, textColor=HexColor('#555'),
            spaceAfter=2, leftIndent=18),
        'callout': ParagraphStyle('callout',
            fontName='Helvetica', fontSize=9.5, textColor=HexColor('#1a3a5c'),
            backColor=HexColor('#eaf2fb'), spaceAfter=8, leading=14,
            leftIndent=10, rightIndent=10, spaceBefore=4),
        'note': ParagraphStyle('note',
            fontName='Helvetica-Oblique', fontSize=9.5, textColor=HexColor('#5c4a00'),
            backColor=HexColor('#fffbe6'), spaceAfter=8, leading=14,
            leftIndent=10, rightIndent=10, spaceBefore=4),
    }


# ── Layout helpers ─────────────────────────────────────────────────────────────
def divider(color=LGRAY, thick=0.5, before=4, after=6):
    return [HRFlowable(width='100%', thickness=thick, color=color,
                       spaceBefore=before, spaceAfter=after)]

def section(title, st):
    return [
        Spacer(1, 4),
        Paragraph(title, st['h1']),
        HRFlowable(width='100%', thickness=2, color=RED,
                   spaceBefore=2, spaceAfter=10),
    ]

def sub(title, st):
    return [Paragraph(title, st['h2'])]

def sub3(title, st):
    return [Paragraph(title, st['h3'])]

def p(text, st):
    return [Paragraph(text, st['body'])]

def bullets(items, st):
    return [Paragraph(f"• {i}", st['bullet']) for i in items]

def subbullets(items, st):
    return [Paragraph(f"◦ {i}", st['subbullet']) for i in items]

def callout(text, st):
    return [Paragraph(text, st['callout'])]

def note(text, st):
    return [Paragraph(text, st['note'])]

def gap(n=8):
    return [Spacer(1, n)]


# ── Table builders ─────────────────────────────────────────────────────────────
_TS_BASE = [
    ('VALIGN',      (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING',  (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING',(0,0), (-1,-1), 8),
    ('GRID',        (0,0), (-1,-1), 0.4, HexColor('#dddddd')),
]

def htable(headers, rows, st, cw=None):
    data = [[Paragraph(h, st['th']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), st['td']) for c in row])
    tbl = Table(data, colWidths=cw)
    tbl.setStyle(TableStyle(_TS_BASE + [
        ('BACKGROUND', (0,0), (-1,0), RED),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor('#fafafa')]),
    ]))
    return [tbl, Spacer(1, 8)]

def kv(rows, st, cw=None):
    cw = cw or [4.5*cm, 11*cm]
    data = [[Paragraph(f"<b>{k}</b>", st['td']), Paragraph(v, st['td'])]
            for k, v in rows]
    tbl = Table(data, colWidths=cw)
    tbl.setStyle(TableStyle(_TS_BASE + [
        ('BACKGROUND', (0,0), (0,-1), HexColor('#f9f9f9')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [WHITE, HexColor('#fafafa')]),
    ]))
    return [tbl, Spacer(1, 8)]

def code_block(lines, st, label=None):
    out = []
    if label:
        out.append(Paragraph(label, st['code_label']))
    for ln in lines:
        out.append(Paragraph(ln if ln.strip() else " ", st['code']))
    out.append(Spacer(1, 6))
    return out


# ── Cover page ─────────────────────────────────────────────────────────────────
def cover(title, subtitle, doc_type, version, st):
    today = date.today().strftime("%B %d, %Y")
    return [
        Spacer(1, 2.8*cm),
        Paragraph("STREAMIX", st['cover_tag']),
        Spacer(1, 0.4*cm),
        Paragraph(title, st['cover_title']),
        Spacer(1, 0.3*cm),
        Paragraph(subtitle, st['cover_sub']),
        Spacer(1, 1.4*cm),
        HRFlowable(width='55%', thickness=1.5, color=RED,
                   hAlign='CENTER', spaceBefore=0, spaceAfter=14),
        Paragraph(doc_type, st['cover_meta']),
        Paragraph(f"Version {version}  ·  {today}", st['cover_meta']),
        Paragraph("Confidential — For Internal and Investor Use Only", st['cover_meta']),
        PageBreak(),
    ]

def cover_bg(canv, doc):
    if canv._pageNumber == 1:
        canv.saveState()
        canv.setFillColor(DARK)
        canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canv.setFillColor(RED)
        canv.rect(0, PAGE_H - 7*mm, PAGE_W, 7*mm, fill=1, stroke=0)
        canv.rect(0, 0, PAGE_W, 4*mm, fill=1, stroke=0)
        canv.restoreState()

def page_header(canv, doc, right_text):
    if canv._pageNumber > 1:
        canv.saveState()
        canv.setFont("Helvetica-Bold", 8)
        canv.setFillColor(RED)
        canv.drawString(2*cm, PAGE_H - 1.4*cm, "STREAMIX")
        canv.setFont("Helvetica", 8)
        canv.setFillColor(GRAY)
        canv.drawRightString(PAGE_W - 2*cm, PAGE_H - 1.4*cm, right_text)
        canv.setStrokeColor(LGRAY)
        canv.setLineWidth(0.4)
        canv.line(2*cm, PAGE_H - 1.7*cm, PAGE_W - 2*cm, PAGE_H - 1.7*cm)
        canv.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
#  BUSINESS DOCUMENT  v2
# ══════════════════════════════════════════════════════════════════════════════

def build_business(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Streamix – Business Document v2",
        author="Streamix",
    )
    st = make_styles()
    s = []

    # Cover
    s += cover("Streamix", "Next-Generation Video Streaming Platform",
               "BUSINESS DOCUMENT", "2.0", st)

    # TOC
    s += section("Table of Contents", st)
    toc = [
        ("1", "Executive Summary"),
        ("2", "Company & Vision"),
        ("3", "Market Opportunity"),
        ("4", "Product Overview"),
        ("5", "Content & Live Streaming Strategy"),
        ("6", "Target Audience"),
        ("7", "Subscription & Revenue Model"),
        ("8", "Advertising (AVOD) System"),
        ("9", "Competitive Landscape"),
        ("10", "Go-to-Market Strategy"),
        ("11", "Technology & Operations"),
        ("12", "Risk & Mitigation"),
        ("13", "Financial Projections"),
        ("14", "Roadmap"),
    ]
    for num, title in toc:
        s.append(Paragraph(f"{num}.  {title}", st['toc']))
    s.append(PageBreak())

    # ── 1 ─────────────────────────────────────────────────────────────────────
    s += section("1. Executive Summary", st)
    s += p(
        "Streamix is a cloud-native video streaming platform delivering cinema-quality "
        "on-demand movies, TV series, live sports, and documentary content to global subscribers. "
        "Built on a modern three-service architecture — Next.js 15 frontend, .NET Core 8 API, "
        "and a dedicated Go streaming engine — the platform is engineered for speed, reliability, "
        "and cost-efficient scalability.", st)
    s += gap()
    s += bullets([
        "Adaptive multi-bitrate HLS streaming (360p → 4K) with per-segment token authentication.",
        "Four subscription tiers (Free → Premium) supporting both SVOD and AVOD revenue streams.",
        "Configurable ad system: pre-roll video ads and mid-roll banner overlays managed entirely from backend configuration — no frontend redeployment needed to update ad campaigns.",
        "Live streaming for sports, events, and TV channels with low-latency HLS delivery.",
        "PostgreSQL full-text + fuzzy search (pg_trgm) across the entire content catalogue.",
        "Multi-profile household management with independent watch history and PIN protection.",
        "All services containerised; ready for Docker Compose (dev) or Kubernetes (production).",
    ], st)
    s.append(PageBreak())

    # ── 2 ─────────────────────────────────────────────────────────────────────
    s += section("2. Company & Vision", st)
    s += sub("Mission Statement", st)
    s += p("To make premium entertainment accessible on every screen — delivering fast, reliable, "
           "beautifully presented video to subscribers regardless of device, bandwidth, or geography.", st)
    s += sub("Core Values", st)
    s += bullets([
        "Quality — every stream is adaptive; buffering is a failure state.",
        "Accessibility — content available across all devices and connection speeds.",
        "Personalization — intelligent recommendations driven by real watch history.",
        "Transparency — clear pricing, no hidden fees, no dark patterns.",
        "Privacy — user data is never sold to third parties.",
    ], st)
    s += sub("Long-Term Vision", st)
    s += p("Within five years, Streamix aims to become the leading independent streaming platform "
           "in its target markets — expanding from web-only to native iOS/Android apps, smart TV SDKs, "
           "and adding original content production as a differentiator.", st)
    s.append(PageBreak())

    # ── 3 ─────────────────────────────────────────────────────────────────────
    s += section("3. Market Opportunity", st)
    s += sub("Global Streaming Market", st)
    s += p("The global video streaming market was valued at USD 544 billion in 2023 and is forecast "
           "to grow at a CAGR of 21.5% through 2030, driven by rising internet penetration, "
           "proliferation of connected devices, and the ongoing shift from traditional broadcast "
           "to on-demand and live streaming.", st)
    s += gap()
    s += htable(
        ["Segment", "2023 Value", "2028 Forecast", "CAGR"],
        [
            ["SVOD (Subscription)", "$100B", "$190B", "13.7%"],
            ["AVOD (Ad-supported)",  "$50B",  "$130B", "21.1%"],
            ["Live Streaming",       "$70B",  "$185B", "21.5%"],
            ["Total OTT",           "$220B",  "$505B", "18.1%"],
        ],
        st, cw=[5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    s += [Paragraph("Source: Industry estimates, 2024.", st['caption'])]

    s += sub("Addressable Market", st)
    s += bullets([
        "Total Addressable Market (TAM): USD 220B — global OTT video (2023).",
        "Serviceable Addressable Market (SAM): USD 42B — English & MENA-language SVOD/AVOD.",
        "Serviceable Obtainable Market (SOM): USD 210M — achievable in 36 months at 0.5% SAM share.",
    ], st)
    s += sub("Key Tailwinds", st)
    s += bullets([
        "5.4 billion internet users globally, growing ~150M per year.",
        "Smart TV penetration exceeds 60% of households in primary target markets.",
        "Mobile data costs falling ~15% annually in emerging markets.",
        "Cable TV household share has dropped from 83% (2014) to 51% (2024) — cord-cutting accelerating.",
        "AVOD growth outpacing SVOD: ad-supported tiers now represent 40%+ of new streaming sign-ups.",
    ], st)
    s.append(PageBreak())

    # ── 4 ─────────────────────────────────────────────────────────────────────
    s += section("4. Product Overview", st)
    s += p("Streamix delivers content through a web application and API-first platform designed "
           "for rapid extension to native mobile and TV applications. The product is built around "
           "three pillars: discovery, playback quality, and personalization.", st)
    s += sub("Core Feature Set", st)
    s += kv([
        ("Browse & Discover",     "Curated rows per genre, trending, new releases, and editor picks. Real-time fuzzy search with pg_trgm similarity and PostgreSQL tsvector full-text indexing."),
        ("Adaptive Streaming",    "HLS multi-bitrate playback (360p / 720p / 1080p / 4K). Player auto-selects quality based on bandwidth; manual override available via quality selector."),
        ("Live Streaming",        "Live sports, events, and TV channels with low-latency HLS. Live Now / Upcoming / TV Channels pages. Animated live badge, real-time viewer count, event schedule."),
        ("Ad-Supported Free Tier","Free tier users see a pre-roll video ad before content and mid-roll banner overlays every 15 minutes. All ad parameters (video URL, skip delay, interval, messaging) are managed centrally from backend configuration — zero redeployment required to change campaigns."),
        ("Multi-Profile",         "Up to 5 profiles per account with independent watch history, recommendations, and optional PIN protection. 'Who's Watching' selector screen."),
        ("Watch Progress",        "Resume exactly where you left off across any device. Continue Watching row auto-populated. Progress marked complete at ≥90% of duration."),
        ("Watchlist",             "Add/remove titles with optimistic UI. Accessible from any profile with per-profile isolation."),
        ("Subtitles & CC",        "WebVTT subtitle tracks selectable per-play, with auto-conversion from SRT on upload."),
        ("Search",                "Instant fuzzy search with pg_trgm + tsvector. Filter by content type, genre, and release year."),
        ("Subscription Mgmt",     "Self-service tier upgrades/downgrades, billing history, and cancellation through the account page."),
        ("Admin Dashboard",       "Content upload via presigned MinIO URLs, transcode status monitoring, channel and live event management."),
    ], st, cw=[4.5*cm, 11*cm])
    s.append(PageBreak())

    # ── 5 ─────────────────────────────────────────────────────────────────────
    s += section("5. Content & Live Streaming Strategy", st)
    s += sub("VOD Content", st)
    s += bullets([
        "Movies, TV series, documentaries, and short films.",
        "Multi-season series with per-episode progress tracking.",
        "Every title encoded at 360p / 720p / 1080p by default; 4K for Premium tier.",
        "Subtitle support in multiple languages per title.",
    ], st)
    s += sub("Live Streaming", st)
    s += bullets([
        "Live sports events (match-by-match rights acquisition model in Phase 1).",
        "Live TV channels — 24/7 streams managed via the Channel entity.",
        "Pay-per-view premium events: boxing, concerts, e-sports finals.",
        "Low-latency HLS delivery via the Go streaming service (liveSyncDurationCount: 3).",
        "Upcoming events schedule with countdown and reminder system.",
    ], st)
    s += sub("Content Acquisition Phases", st)
    s += htable(
        ["Phase", "Content Focus", "Volume Target"],
        [
            ["Launch (Month 1–3)",   "Public domain films, indie content, licensed short-form",   "200+ titles"],
            ["Growth (Month 4–12)",  "Regional movie studio deals, sports event PPV rights",       "1,000+ titles"],
            ["Scale (Year 2+)",      "Major studio licensing, original co-productions, live sports","5,000+ titles"],
        ],
        st, cw=[4*cm, 8*cm, 3.5*cm])
    s.append(PageBreak())

    # ── 6 ─────────────────────────────────────────────────────────────────────
    s += section("6. Target Audience", st)
    s += htable(
        ["Segment", "Age", "Key Behaviour", "Primary Device", "Best Tier"],
        [
            ["Young Adults",  "18–34", "Heavy binge-watchers; mobile-first; price-sensitive",          "Smartphone / Laptop", "Free → Basic"],
            ["Families",      "28–45", "Multi-profile; value Kids Mode; weekend viewing",              "Smart TV",            "Standard"],
            ["Sports Fans",   "22–50", "Live-event driven; high churn if no live rights",              "Smart TV / Mobile",   "Standard → Premium"],
            ["Cinephiles",    "25–55", "Quality over quantity; independent and arthouse content",      "Laptop / Tablet",     "Premium"],
            ["Casual Viewers","18–65", "Occasional watching; cost-averse; accept ads",                "Any",                 "Free (AVOD)"],
        ],
        st, cw=[3.2*cm, 1.8*cm, 6*cm, 3*cm, 2.5*cm])
    s += sub("Geographic Roll-out", st)
    s += bullets([
        "Phase 1 (Year 1): English-language markets — US, UK, Canada, Australia.",
        "Phase 2 (Year 2): MENA Arabic-language markets — UAE, Saudi Arabia, Egypt.",
        "Phase 3 (Year 3): Localisation for South and Southeast Asia.",
    ], st)
    s.append(PageBreak())

    # ── 7 ─────────────────────────────────────────────────────────────────────
    s += section("7. Subscription & Revenue Model", st)
    s += sub("Tier Structure", st)
    s += htable(
        ["Tier", "Price/Month", "Concurrent Streams", "Max Quality", "Ads", "Downloads", "Live"],
        [
            ["Free",     "USD 0",    "1", "720p",  "Pre-roll + Mid-roll", "No",             "Limited"],
            ["Basic",    "USD 7.99", "1", "1080p", "None",                "No",             "Yes"],
            ["Standard", "USD 13.99","2", "1080p", "None",                "2 titles",       "Yes"],
            ["Premium",  "USD 19.99","4", "4K HDR","None",                "Unlimited",      "Yes + PPV"],
        ],
        st, cw=[2.5*cm, 2.5*cm, 3*cm, 2.5*cm, 3.5*cm, 2.5*cm, 2*cm])
    s += sub("Revenue Streams", st)
    s += bullets([
        "SVOD — Recurring monthly subscription fees (Basic / Standard / Premium tiers).",
        "AVOD — Pre-roll video and mid-roll banner advertising revenue from Free tier users.",
        "Pay-Per-View (PPV) — Premium live events sold as one-time purchases (boxing, concerts, e-sports).",
        "B2B API Licensing — API access for airlines, hotels, corporate wellness, and IPTV operators.",
    ], st)
    s += sub("Unit Economics (Target, Year 2)", st)
    s += kv([
        ("ARPU (blended)",            "USD 11.40 / month"),
        ("Customer Acquisition Cost", "USD 8.50"),
        ("LTV (24-month avg.)",       "USD 274"),
        ("LTV / CAC Ratio",           "32× (industry benchmark: >3×)"),
        ("Gross Margin (streaming)",  "~72%"),
        ("Monthly Churn Target",      "<2.8%"),
        ("AVOD eCPM Target",          "USD 4.50 per 1,000 ad impressions"),
    ], st)
    s.append(PageBreak())

    # ── 8 ─────────────────────────────────────────────────────────────────────
    s += section("8. Advertising (AVOD) System", st)
    s += p("The Streamix AVOD system is purpose-built for operational simplicity. All ad parameters "
           "are managed through a single backend configuration section — marketing and ad operations "
           "teams can update campaigns, swap creative assets, adjust timing, and enable or disable "
           "ads entirely without touching frontend code or triggering a deployment.", st)
    s += sub("Ad Formats", st)
    s += htable(
        ["Format", "Trigger", "Skip Policy", "Default Duration", "Placement"],
        [
            ["Pre-roll Video Ad",   "Player mount (before content starts)", "Skippable after 5 seconds", "15–30 seconds", "Full-screen overlay"],
            ["Mid-roll Banner Ad",  "Every 15 minutes of playback",         "Dismissible after 5 seconds", "30 seconds (auto-close)", "Bottom overlay bar"],
        ],
        st, cw=[3.5*cm, 4*cm, 3.5*cm, 3*cm, 3*cm])
    s += sub("Operational Control", st)
    s += bullets([
        "Enable / disable all ads instantly via the Enabled flag in appsettings.json.",
        "Swap pre-roll video creative by updating a single VideoUrl config value — change takes effect within 5 minutes (client cache TTL).",
        "Adjust mid-roll frequency by changing MidRollIntervalMinutes — affects all active sessions within one cache cycle.",
        "All ad config is served via GET /api/ads/config with a 5-minute ResponseCache header; the frontend caches it via TanStack Query (staleTime: 5 min).",
        "Paid users (Basic / Standard / Premium) never receive ad config — the frontend hook is disabled for subscriptionTier > 0.",
    ], st)
    s += sub("Ad Revenue Model", st)
    s += bullets([
        "Pre-roll CPM: Charged per 1,000 impressions at session start.",
        "Mid-roll CPM: Charged per banner display (every 15 min per active viewer).",
        "Click-through revenue: CPC model on Learn More and upgrade CTA clicks.",
        "Third-party ad network integration planned for Phase 2 (VAST/VMAP tags).",
    ], st)
    s += callout("Conversion opportunity: every ad unit includes an 'Upgrade to remove ads' link "
                 "pointing to the subscription page — turning ad impressions into potential SVOD conversions.", st)
    s.append(PageBreak())

    # ── 9 ─────────────────────────────────────────────────────────────────────
    s += section("9. Competitive Landscape", st)
    s += htable(
        ["Platform", "Strengths", "Weaknesses", "Our Advantage"],
        [
            ["Netflix",
             "Massive library, global brand, strong recommendation AI",
             "No free tier; high cost; password-sharing crackdown",
             "Free AVOD tier; live sports; lower price point"],
            ["Disney+",
             "Franchise IP (Marvel, Star Wars, Pixar); family-friendly",
             "Limited adult content; weak live sports",
             "Broader genre coverage; live events; AVOD tier"],
            ["Amazon Prime Video",
             "Prime bundle value; strong originals",
             "Complex UI mixing rental and subscription content",
             "Cleaner UX; transparent ad-based free tier"],
            ["YouTube",
             "Free; massive UGC; global brand recognition",
             "Low professional content quality; heavy ad load",
             "Professional content; controlled ad experience; no UGC noise"],
            ["Streamix",
             "Adaptive HLS tech; live + VOD; configurable AVOD; lower cost",
             "Smaller library at launch",
             "—"],
        ],
        st, cw=[2.8*cm, 4.5*cm, 3.8*cm, 4.4*cm])
    s.append(PageBreak())

    # ── 10 ────────────────────────────────────────────────────────────────────
    s += section("10. Go-to-Market Strategy", st)
    s += kv([
        ("Phase 1 — Beta (Month 1–3)",
         "Invite-only. 5,000 beta users. NPS feedback loop. Fix critical UX issues. "
         "Seed content library with 200+ licensed titles. Validate AVOD ad metrics."),
        ("Phase 2 — Soft Launch (Month 4–6)",
         "Open registration. All tiers live. Free AVOD tier drives top-of-funnel. "
         "Target: 50,000 registered users, 8,000 paid subscribers, 42,000 active Free users."),
        ("Phase 3 — Growth (Month 7–18)",
         "Performance marketing (Google, Meta, TikTok). Referral program (30-day free Premium). "
         "Influencer / creator partnerships. Target: 500,000 registered, 80,000 paid."),
        ("Phase 4 — Expansion (Month 19–36)",
         "iOS & Android native apps. MENA market launch. Live sports rights for regional leagues. "
         "VAST/VMAP integration for programmatic ad buying."),
    ], st, cw=[5*cm, 10.5*cm])
    s += sub("Customer Acquisition Channels", st)
    s += bullets([
        "SEO / content marketing — streaming guides, genre landing pages, search-optimised title pages.",
        "Social media advertising — short-form video clips as creatives (TikTok, Instagram Reels, YouTube Shorts).",
        "Referral program — both referrer and referred receive 1 month free Standard.",
        "Partnerships — ISP bundle deals; smart TV manufacturer pre-installs.",
        "AVOD flywheel: Free tier users share content; social sharing drives organic acquisition.",
    ], st)
    s.append(PageBreak())

    # ── 11 ────────────────────────────────────────────────────────────────────
    s += section("11. Technology & Operations", st)
    s += kv([
        ("Frontend",          "Next.js 15, React 18, TypeScript 5, Tailwind CSS 3, HLS.js, TanStack Query 5, Zustand 4, NextAuth.js 5, Framer Motion"),
        ("Backend API",       ".NET Core 8, ASP.NET Core, Clean Architecture (4-project solution), MediatR, FluentValidation, AutoMapper, EF Core 8 + Npgsql"),
        ("Streaming Service", "Go 1.24, Chi v5, FFmpeg (multi-bitrate HLS), MinIO SDK, go-redis, golang-jwt"),
        ("Database",          "PostgreSQL 16 with pg_trgm + tsvector full-text search + uuid-ossp"),
        ("Cache",             "Redis 7 — API response cache (10 min TTL), JWT refresh tokens (7 days), ad config (5 min)"),
        ("Object Storage",    "MinIO (S3-compatible) — raw video, HLS segments, thumbnails, subtitles"),
        ("Infrastructure",    "Docker, Docker Compose v5 (7 services); production target: Kubernetes"),
        ("CDN (production)",  "CloudFront / Cloudflare for HLS segment delivery; 5-min cache on ad config"),
        ("Ad Configuration",  "Backend appsettings.json 'Ads' section — live control with no frontend deployment"),
    ], st, cw=[4.5*cm, 11*cm])
    s += sub("Content Operations", st)
    s += bullets([
        "Admin uploads raw video via presigned MinIO URL — no file size limit.",
        "Go service transcodes to 360p / 720p / 1080p in parallel; SLA < 25 min for a 90-min movie.",
        "Subtitles uploaded as SRT; auto-converted to WebVTT by the Go transcoder.",
        "Post-transcode callback from Go to backend updates asset status to 'ready'.",
    ], st)
    s.append(PageBreak())

    # ── 12 ────────────────────────────────────────────────────────────────────
    s += section("12. Risk & Mitigation", st)
    s += htable(
        ["Risk", "Likelihood", "Impact", "Mitigation"],
        [
            ["Content licensing exceeds budget",   "Medium", "High",   "Start public domain + CC; license incrementally as revenue grows."],
            ["Infrastructure costs at scale",      "Medium", "Medium", "CDN for HLS (cost per GB falls at volume); auto-scaling."],
            ["Churn — thin content library",       "High (Y1)","High", "Free AVOD tier retains cost-sensitive users; live sports as stickiness anchor."],
            ["Ad revenue lower than projected",    "Medium", "Medium", "AVOD is supplementary; SVOD is primary. Adjust ad frequency/format via config."],
            ["Competitor price war",               "Low",    "Medium", "Cost leadership via in-house streaming stack; B2B licensing as hedge."],
            ["DRM / piracy of premium content",    "Medium", "Medium", "Short-lived signed segment tokens (implemented). Widevine/FairPlay in Phase 2."],
            ["Regulatory / geo-blocking",          "Low",    "Low",    "IP-based geo-filtering; legal review per market before launch."],
            ["Cybersecurity breach",               "Low",    "High",   "bcrypt passwords; JWT short expiry; Redis refresh token rotation; pen testing."],
            ["Ad config exposure (sensitive URLs)", "Low",   "Low",    "Ad config endpoint is public but read-only; no secrets exposed in response."],
        ],
        st, cw=[4*cm, 2.2*cm, 2*cm, 7.3*cm])
    s.append(PageBreak())

    # ── 13 ────────────────────────────────────────────────────────────────────
    s += section("13. Financial Projections", st)
    s += p("Illustrative estimates based on comparable SVOD/AVOD platforms at similar growth stages. "
           "AVOD projections assume ad monetisation via direct brand deals in Year 1, "
           "programmatic networks from Year 2.", st)
    s += gap()
    s += htable(
        ["Metric", "Year 1", "Year 2", "Year 3"],
        [
            ["Registered Users",          "100,000",   "500,000",   "2,000,000"],
            ["Paid Subscribers",          "15,000",    "80,000",    "350,000"],
            ["Free (AVOD) Active Users",  "60,000",    "300,000",   "1,200,000"],
            ["ARPU — Paid (USD/month)",   "$9.20",     "$11.40",    "$12.80"],
            ["AVOD Revenue / Free User",  "$0.80/mo",  "$1.10/mo",  "$1.40/mo"],
            ["Monthly SVOD Revenue",      "$138K",     "$912K",     "$4.48M"],
            ["Monthly AVOD Revenue",      "$48K",      "$330K",     "$1.68M"],
            ["Annual Total Revenue",      "$2.2M",     "$14.9M",    "$73.9M"],
            ["Content Licensing Cost",    "$0.7M",     "$4.1M",     "$18.0M"],
            ["Infrastructure Cost",       "$0.3M",     "$1.3M",     "$4.5M"],
            ["Gross Profit",              "$1.2M",     "$9.5M",     "$51.4M"],
            ["Gross Margin",              "55%",       "64%",       "70%"],
        ],
        st, cw=[6*cm, 2.8*cm, 2.8*cm, 2.8*cm])
    s += [Paragraph("All figures USD. Projections exclude capex. AVOD row assumes Free tier MAU × eCPM.", st['caption'])]
    s.append(PageBreak())

    # ── 14 ────────────────────────────────────────────────────────────────────
    s += section("14. Roadmap", st)
    s += htable(
        ["Quarter", "Milestone"],
        [
            ["Q1 2025", "MVP web launch: VOD, 4 subscription tiers, AVOD ad system, 200 titles"],
            ["Q2 2025", "Live streaming: sports events, TV channels, PPV events"],
            ["Q3 2025", "iOS & Android native apps (React Native)"],
            ["Q4 2025", "Widevine / FairPlay DRM; offline downloads for Standard/Premium"],
            ["Q1 2026", "VAST/VMAP programmatic ad network integration for AVOD scale"],
            ["Q2 2026", "MENA launch: Arabic UI, RTL layout, regional content"],
            ["Q3 2026", "Smart TV apps (Samsung Tizen, LG webOS)"],
            ["Q4 2026", "ML-powered recommendation engine (collaborative filtering)"],
            ["2027",    "Original content production — first 3 exclusive titles; Series A raise"],
        ],
        st, cw=[3*cm, 12.5*cm])
    s += gap(12)
    s += [Paragraph("— End of Document —", st['caption'])]

    def on_page(c, d):
        cover_bg(c, d)
        page_header(c, d, "Business Document  |  Confidential")

    doc.build(s, onFirstPage=on_page, onLaterPages=on_page,
              canvasmaker=NumberedCanvas)
    print(f"✓  Business document: {path}")


# ══════════════════════════════════════════════════════════════════════════════
#  TECHNICAL DOCUMENT  v2
# ══════════════════════════════════════════════════════════════════════════════

def build_technical(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Streamix – Technical Document v2",
        author="Streamix Engineering",
    )
    st = make_styles()
    s = []

    # Cover
    s += cover("Streamix", "Technical Architecture & Engineering Reference",
               "TECHNICAL DOCUMENT", "2.0", st)

    # TOC
    s += section("Table of Contents", st)
    toc = [
        ("1",  "System Architecture Overview"),
        ("2",  "Technology Stack"),
        ("3",  "Repository Structure"),
        ("4",  "Backend Service — .NET Core 8"),
        ("5",  "Streaming Service — Go 1.24"),
        ("6",  "Frontend — Next.js 15"),
        ("7",  "Ad System Architecture"),
        ("8",  "Database Schema"),
        ("9",  "API Reference"),
        ("10", "Infrastructure & DevOps"),
        ("11", "Security Architecture"),
        ("12", "Scalability & Performance"),
        ("13", "Development Workflow"),
    ]
    for num, title in toc:
        s.append(Paragraph(f"{num}.  {title}", st['toc']))
    s.append(PageBreak())

    # ── 1 ─────────────────────────────────────────────────────────────────────
    s += section("1. System Architecture Overview", st)
    s += p("Streamix is a three-service microservices platform. Each service is built in the language "
           "best suited to its workload and communicates over HTTP. All services are containerised and "
           "share MinIO object storage and Redis for caching and session management.", st)

    s += sub("Service Architecture Diagram", st)
    arch = [
        "  ┌───────────────────────────────────────────────────────────┐",
        "  │              BROWSER / NEXT.JS APP (port 3000)            │",
        "  └─────────┬─────────────────────────┬───────────────────┘",
        "           │  REST/JSON (JWT Bearer)      │  HLS + WebVTT + Ads Config",
        "           ▼                            ▼",
        "  ┌───────────────────┐         ┌────────────────────────┐",
        "  │ .NET Core 8 API      │         │ Go Streaming Service       │",
        "  │ port 5000            │         │ port 8080                  │",
        "  │                      │         │                            │",
        "  │ Auth, Content,       │───►     │ HLS manifest serving       │",
        "  │ Watchlist, Progress  │ POST    │ Multi-bitrate transcoding  │",
        "  │ Search, Live, Ads    │◄─────  │ Subtitle SRT→VTT           │",
        "  │ Admin, Channels      │ PATCH   │ Live stream proxy          │",
        "  └────┬──────────────┘         └─────┬──────────────────┘",
        "         │                               │",
        "  ┌─────┼───────┐   ┌────────┐  ┌─────┼──────────┐",
        "  │ Postgres │   │ Redis  │  │    MinIO           │",
        "  │   16     │   │   7    │  │ videos-raw         │",
        "  │          │   │ Cache  │  │ videos-hls         │",
        "  │ Main DB  │   │ Tokens │  │ thumbnails         │",
        "  └─────────┘   └────────┘  │ subtitles          │",
        "                              └──────────────────┘",
    ]
    for line in arch:
        s.append(Paragraph(line, st['code']))
    s += gap()

    s += sub("Service Responsibilities", st)
    s += kv([
        (".NET Core 8 API",
         "Authentication (JWT), users, profiles, subscription management, content catalogue, "
         "watchlist, watch progress, search, live events, channels, admin operations, "
         "ad configuration endpoint, and internal callbacks from Go. "
         "Only service with direct PostgreSQL access."),
        ("Go Streaming Service",
         "Receives raw video paths from backend, runs FFmpeg to produce multi-bitrate HLS, "
         "uploads segments to MinIO, serves token-gated HLS manifests and segments. "
         "Handles live stream proxy and SRT→VTT subtitle conversion. No DB access."),
        ("Next.js 15 Frontend",
         "Server-side and client-side React app using App Router. Server Components for "
         "browse/search pages; Client Components for player, ads, watchlist, and interactive UI. "
         "Proxies all API and streaming requests via Next.js rewrites (no browser CORS)."),
    ], st, cw=[4*cm, 11.5*cm])
    s.append(PageBreak())

    # ── 2 ─────────────────────────────────────────────────────────────────────
    s += section("2. Technology Stack", st)
    s += htable(
        ["Layer", "Technology", "Version", "Rationale"],
        [
            ["Frontend Framework",  "Next.js",              "15.x",   "App Router, Server Components, rewrites"],
            ["UI Language",         "TypeScript",           "5.x",    "Type safety across API boundaries"],
            ["Styling",             "Tailwind CSS",         "3.x",    "Utility-first; dark theme with brand tokens"],
            ["HLS Player",          "HLS.js",               "1.5.x",  "Adaptive bitrate, quality selection, DRM-ready"],
            ["Server State",        "TanStack Query",       "5.x",    "Caching, background refetch, infinite scroll, ad config"],
            ["Client State",        "Zustand",              "4.x",    "Auth store with localStorage persistence"],
            ["Auth (FE)",           "NextAuth.js",          "5.x",    "App Router compatible; CredentialsProvider"],
            ["Animations",          "Framer Motion",        "11.x",   "Card hover, modal transitions"],
            ["Backend Framework",   "ASP.NET Core",         "8.0",    "High-performance, mature ecosystem"],
            ["Architecture",        "Clean Architecture",   "—",      "Domain / Application / Infrastructure / API"],
            ["CQRS",                "MediatR",              "12.x",   "Decoupled command/query handlers + pipeline"],
            ["Validation",          "FluentValidation",     "11.x",   "Declarative rules, MediatR pipeline behaviour"],
            ["ORM",                 "EF Core + Npgsql",     "8.x",    "Code-first migrations, LINQ, PostgreSQL driver"],
            ["Streaming Language",  "Go",                   "1.24",   "Goroutines for parallel transcoding; low memory"],
            ["HTTP Router (Go)",    "Chi",                  "5.x",    "Lightweight, idiomatic, middleware-first"],
            ["Transcoder",          "FFmpeg",               "6.x",    "Industry-standard multi-bitrate HLS"],
            ["Database",            "PostgreSQL",           "16",     "tsvector, pg_trgm, uuid-ossp, GIN indexes"],
            ["Cache / Sessions",    "Redis",                "7",      "API cache, JWT refresh tokens, ad config TTL"],
            ["Object Storage",      "MinIO",                "latest", "S3-compatible; self-hosted; presigned URLs"],
            ["Reverse Proxy",       "Nginx",                "1.25",   "SSL termination, routing, large upload support"],
            ["Containerisation",    "Docker / Compose",     "v5",     "7-service dev orchestration; Kubernetes for prod"],
        ],
        st, cw=[4*cm, 3.5*cm, 2*cm, 6*cm])
    s.append(PageBreak())

    # ── 3 ─────────────────────────────────────────────────────────────────────
    s += section("3. Repository Structure", st)
    s += p("Monorepo under <b>streming/</b> — three service directories plus shared infrastructure configs:", st)
    tree = [
        "streming/",
        "├── .env.example",
        "├── docker-compose.yml",
        "├── docker-compose.dev.yml",
        "├── Makefile",
        "├── apps/",
        "│   ├── frontend/                    # Next.js 15",
        "│   │   ├── src/app/                 # App Router pages",
        "│   │   ├── src/components/",
        "│   │   │   ├── browse/              # HeroSection, ContentRow, ContentCard",
        "│   │   │   ├── player/              # VideoPlayer, PlayerControls, AdPlayer, AdBanner",
        "│   │   │   ├── live/                # LivePlayer, LiveBadge, LiveEventCard, ChannelCard",
        "│   │   │   ├── title/               # TitleDetail, EpisodeList, WatchlistButton",
        "│   │   │   ├── search/              # SearchBar, SearchResults",
        "│   │   │   ├── layout/              # Navbar, Footer",
        "│   │   │   └── ui/                  # Button, Input, Badge, Skeleton, Modal",
        "│   │   ├── src/hooks/           # useAdConfig, useWatchlist, useProfile, useDebounce",
        "│   │   ├── src/lib/api/         # client, auth, content, ads, live, channels...",
        "│   │   ├── src/store/           # Zustand auth store",
        "│   │   ├── src/types/           # content, user, live, api",
        "│   │   ├── src/middleware.ts    # Edge middleware: route protection",
        "│   │   ├── Dockerfile",
        "│   │   └── package.json",
        "│   ├── backend/                     # .NET Core 8",
        "│   │   ├── src/StreamingPlatform.API/",
        "│   │   │   ├── Controllers/         # Auth, Content, Ads, Live, Channels, Admin...",
        "│   │   │   ├── Middleware/          # ExceptionHandlingMiddleware",
        "│   │   │   └── appsettings.json     # Jwt, Minio, Redis, Ads, StreamingService",
        "│   │   ├── src/StreamingPlatform.Application/",
        "│   │   │   ├── Common/DTOs/",
        "│   │   │   ├── Common/Interfaces/",
        "│   │   │   └── Common/Models/",
        "│   │   ├── src/StreamingPlatform.Domain/",
        "│   │   │   ├── Entities/            # 14 entities",
        "│   │   │   └── Enums/               # ContentType, VideoQuality, ProcessingStatus...",
        "│   │   ├── src/StreamingPlatform.Infrastructure/",
        "│   │   │   ├── Persistence/         # ApplicationDbContext + 14 EF configs",
        "│   │   │   └── Services/            # TokenService, CacheService, MinioStorageService...",
        "│   │   └── Dockerfile",
        "│   └── streaming/                   # Go 1.24",
        "│       ├── cmd/server/main.go",
        "│       ├── internal/",
        "│       │   ├── config/ handler/ service/ storage/ cache/",
        "│       │   ├── transcoder/          # ffmpeg, pipeline, worker_pool, subtitle",
        "│       │   └── middleware/          # auth.go (JWT validation)",
        "│       ├── pkg/models/models.go",
        "│       └── Dockerfile",
        "└── infra/",
        "    ├── postgres/init.sql            # uuid-ossp, pg_trgm, unaccent extensions",
        "    ├── redis/redis.conf",
        "    ├── minio/setup.sh               # create 4 buckets",
        "    └── nginx/nginx.conf             # reverse proxy rules",
    ]
    for line in tree:
        s.append(Paragraph(line, st['code']))
    s.append(PageBreak())

    # ── 4 ─────────────────────────────────────────────────────────────────────
    s += section("4. Backend Service — .NET Core 8", st)
    s += sub("Clean Architecture Layers", st)
    s += kv([
        ("Domain",
         "14 entities (User, Profile, Subscription, Content, Season, Episode, VideoAsset, "
         "Subtitle, Genre, ContentGenre, WatchlistItem, WatchProgress, Channel, LiveEvent). "
         "5 enums: ContentType, VideoQuality, ProcessingStatus, SubscriptionTier, LiveStreamStatus. "
         "No framework dependencies."),
        ("Application",
         "5 interfaces: IApplicationDbContext, ITokenService, ICacheService, IStorageService, "
         "IStreamingService. 15 DTOs. PaginatedList<T> and Result<T> models. "
         "MediatR + FluentValidation registered in DependencyInjection.cs."),
        ("Infrastructure",
         "ApplicationDbContext with 14 IEntityTypeConfiguration<T> files. "
         "TokenService (HS256 JWT), CacheService (Redis), MinioStorageService (presigned URLs), "
         "StreamingServiceClient (HttpClient with X-Internal-Key)."),
        ("API",
         "11 controllers: Auth, Content, Search, Progress, Watchlist, Users, "
         "Channels, Live, Admin, Ads. ExceptionHandlingMiddleware (RFC 7807 ProblemDetails). "
         "Swagger/OpenAPI with Bearer scheme. Health checks. Auto-migrate on startup."),
    ], st, cw=[3.5*cm, 12*cm])

    s += sub("appsettings.json Configuration Sections", st)
    s += htable(
        ["Section", "Key Settings"],
        [
            ["Jwt",             "Issuer, Audience, AccessTokenMinutes (15), RefreshTokenDays (7)"],
            ["Minio",           "Endpoint, AccessKey, SecretKey, UseSSL, bucket names (4 buckets)"],
            ["Redis",           "CacheTtlMinutes (10)"],
            ["StreamingService","BaseUrl — internal URL of the Go service"],
            ["Ads",             "Enabled (bool), MidRollIntervalMinutes, PreRoll.VideoUrl, PreRoll.SkipAfterSeconds, MidRoll.ImageUrl, MidRoll.Headline, MidRoll.DurationSeconds, MidRoll.CloseAfterSeconds"],
            ["ConnectionStrings","DefaultConnection (PostgreSQL), Redis"],
        ],
        st, cw=[3.5*cm, 12*cm])

    s += sub("JWT Design", st)
    s += kv([
        ("Algorithm",         "HS256 — 256-bit secret from environment variable Jwt:Secret"),
        ("Access Token TTL",  "15 minutes; claims: userId, email, profileId, subscriptionTier, jti"),
        ("Refresh Token TTL", "7 days; opaque random string stored in Redis as refresh:{token} → userId"),
        ("Token Rotation",    "Each /auth/refresh call issues a new refresh token and invalidates the previous"),
        ("Tier Enforcement",  "subscriptionTier claim read by both backend and Go service; ad system reads it on frontend"),
    ], st)
    s.append(PageBreak())

    # ── 5 ─────────────────────────────────────────────────────────────────────
    s += section("5. Streaming Service — Go 1.24", st)
    s += sub("Key Files", st)
    s += htable(
        ["File", "Responsibility"],
        [
            ["cmd/server/main.go",              "Wire config, router, worker pool; start HTTP server"],
            ["internal/config/config.go",       "Viper env-based configuration"],
            ["internal/server/server.go",       "Chi router, CORS, auth middleware registration"],
            ["internal/handler/stream_handler.go",    "GET /stream — manifest rewriting + segment redirect"],
            ["internal/handler/transcode_handler.go", "POST /internal/transcode — enqueue job"],
            ["internal/handler/live_handler.go",      "GET /live — low-latency HLS proxy for live channels"],
            ["internal/handler/health_handler.go",    "GET /health — liveness probe"],
            ["internal/service/stream_service.go",    "Resolve MinIO paths, check subscription tier"],
            ["internal/service/transcode_service.go", "FFmpeg pipeline orchestration"],
            ["internal/storage/minio_client.go",      "GetObject, PutObject, PresignedGet, PresignedPut"],
            ["internal/cache/redis_client.go",        "Token cache, content metadata cache"],
            ["internal/transcoder/ffmpeg.go",         "FFmpeg multi-bitrate command builder"],
            ["internal/transcoder/pipeline.go",       "Parallel quality-level runner (errgroup)"],
            ["internal/transcoder/worker_pool.go",    "Bounded goroutine pool (default: 3 concurrent FFmpeg)"],
            ["internal/transcoder/subtitle.go",       "Pure-Go SRT → WebVTT converter"],
            ["internal/middleware/auth.go",           "JWT validation (shared HS256 secret with backend)"],
            ["pkg/models/models.go",                  "TranscodeJob, StreamToken, TranscodeResult structs"],
        ],
        st, cw=[6.5*cm, 9*cm])

    s += sub("Multi-Bitrate FFmpeg Pipeline", st)
    s += p("A single FFmpeg invocation produces all three quality levels in parallel via "
           "<b>filter_complex</b>, outputting 6-second HLS segments:", st)
    s += code_block([
        "// Three renditions in one pass:",
        "// 360p  →  800k video + 96k  audio  →  v0/seg*.ts",
        "// 720p  → 2800k video + 128k audio  →  v1/seg*.ts",
        "// 1080p → 5000k video + 192k audio  →  v2/seg*.ts",
        "",
        "// Output in MinIO videos-hls bucket:",
        "// {assetId}/master.m3u8   (variant playlist)",
        "// {assetId}/v0/prog_index.m3u8 + seg000.ts ...",
        "// {assetId}/v1/prog_index.m3u8 + seg000.ts ...",
        "// {assetId}/v2/prog_index.m3u8 + seg000.ts ...",
    ], st)

    s += sub("HLS Token-Gating Flow", st)
    s += code_block([
        "1. Client → GET /stream/{contentId}/master.m3u8?token=JWT",
        "2. Go     → Validate JWT; check subscriptionTier ≥ content.requiredTier",
        "3. Go     → Fetch master.m3u8 from MinIO",
        "4. Go     → Rewrite each segment URL:",
        "             /stream/{contentId}/v{q}/{seg}.ts?token=JWT",
        "5. Go     → Return rewritten playlist (200 OK)",
        "",
        "6. Client → GET /stream/{contentId}/v1/seg003.ts?token=JWT",
        "7. Go     → Validate JWT; generate presigned MinIO GET URL (1hr expiry)",
        "8. Go     → 302 redirect to presigned URL",
        "             (MinIO serves bytes; Go does NOT proxy the stream)",
    ], st)
    s.append(PageBreak())

    # ── 6 ─────────────────────────────────────────────────────────────────────
    s += section("6. Frontend — Next.js 15", st)
    s += sub("App Router Pages", st)
    s += htable(
        ["Route", "Rendering", "Description"],
        [
            ["/",                         "Server",  "Redirect to /browse"],
            ["/(auth)/login",             "Client",  "CredentialsProvider login form (react-hook-form + zod)"],
            ["/(auth)/register",          "Client",  "Registration form"],
            ["/browse",                   "Server",  "Hero + ContentRows by genre; parallel data fetching"],
            ["/browse/[genre]",           "Server",  "Genre-filtered grid with GenreFilter pills"],
            ["/title/[contentId]",        "Server",  "TitleDetail: backdrop, synopsis, episodes, watchlist button"],
            ["/watch/[contentId]",        "Client",  "Full-screen VideoPlayer; ad system active for Free tier"],
            ["/search",                   "Client",  "Debounced search bar + TanStack Query result grid"],
            ["/live",                     "Server",  "Live Now / Upcoming / TV Channels sections"],
            ["/live/[eventId]",           "Client",  "LivePlayer (low-latency HLS, no seek bar)"],
            ["/sports",                   "Server",  "Sport-type filter tabs (Football, Basketball, F1, etc.)"],
            ["/tv",                       "Server",  "TV channel category grid"],
            ["/profile/select",           "Client",  "'Who's Watching?' avatar picker"],
            ["/profile/[profileId]",      "Client",  "Profile settings: name, maturity rating, language, PIN"],
            ["/profile/[profileId]/watchlist","Server","Watchlist grid for active profile"],
            ["/account",                  "Client",  "Subscription tier, billing history, password change"],
        ],
        st, cw=[5*cm, 2.2*cm, 8.3*cm])

    s += sub("Key Hooks", st)
    s += htable(
        ["Hook", "File", "Purpose"],
        [
            ["useAdConfig",      "src/hooks/useAdConfig.ts",   "Fetch GET /api/ads/config via React Query; enabled only for Free tier; staleTime 5min"],
            ["useWatchlist",     "src/hooks/useWatchlist.ts",  "Optimistic add/remove via useMutation; refetch on settle"],
            ["useProfile",       "src/hooks/useProfile.ts",    "Switch active profile; update Zustand store and JWT claim"],
            ["useProgressSync",  "src/components/player/useProgressSync.ts", "Debounced 10s progress PUT; fires on pause and unmount"],
            ["useDebounce",      "src/hooks/useDebounce.ts",   "Debounce helper used by SearchBar"],
        ],
        st, cw=[3.5*cm, 5.5*cm, 6.5*cm])

    s += sub("VideoPlayer Architecture", st)
    s += kv([
        ("HLS Library",       "HLS.js v1.5 with native Safari fallback via <code>video.canPlayType()</code>"),
        ("Auth on segments",  "xhrSetup callback injects Authorization Bearer header"),
        ("Quality switching", "hls.currentLevel = n (-1 = auto); level list from hls.levels on MANIFEST_PARSED"),
        ("Subtitles",         "<track> elements added post-attach; VTT files served from MinIO public bucket"),
        ("Resume playback",   "videoRef.currentTime = startPosition after HLS attach"),
        ("Keyboard shortcuts","Space/K=play-pause, ←/→=±10s, M=mute, F=fullscreen, ↑/↓=volume"),
        ("Controls hide",     "Hidden after 3s inactivity via setTimeout; shown on mousemove"),
        ("Ad integration",    "showPreRoll state triggers AdPlayer before first play; showMidRoll triggers AdBanner at midRollInterval ticks"),
    ], st)
    s.append(PageBreak())

    # ── 7 ─────────────────────────────────────────────────────────────────────
    s += section("7. Ad System Architecture", st)
    s += p("The ad system spans all three services. The backend owns the configuration; "
           "the frontend fetches it and renders the appropriate ad component; "
           "the Go service is not involved in ad delivery.", st)

    s += sub("Data Flow", st)
    s += code_block([
        "appsettings.json",
        "  └─ 'Ads' section (Enabled, MidRollIntervalMinutes, PreRoll.*, MidRoll.*)",
        "       │",
        "       ▼  IOptions<AdsSettings> injected into AdsController",
        "  GET /api/ads/config  (ResponseCache: 300s, no auth required)",
        "       │",
        "       ▼  fetchAdsConfig() in src/lib/api/ads.ts",
        "       │",
        "       ▼  useAdConfig() hook (TanStack Query, staleTime: 5min)",
        "            enabled: subscriptionTier === 0  (Free tier only)",
        "       │",
        "       ▼  VideoPlayer.tsx",
        "            ├─ adConfig.preRoll  →  <AdPlayer />  (before content, full-screen)",
        "            └─ adConfig.midRoll  →  <AdBanner />  (every midRollIntervalSeconds)",
    ], st)

    s += sub("Backend: AdsController", st)
    s += kv([
        ("File",          "apps/backend/src/StreamingPlatform.API/Controllers/AdsController.cs"),
        ("Endpoint",      "GET /api/ads/config"),
        ("Auth",          "None — anonymous access; ad config contains no secrets"),
        ("Cache",         "[ResponseCache(Duration = 300)] — 5-minute HTTP cache header"),
        ("Config binding","IOptions<AdsSettings> bound from appsettings.json 'Ads' section; registered via Configure<AdsSettings>() in Program.cs"),
        ("Response DTOs", "AdsConfigResponse, PreRollDto, MidRollDto — C# records"),
    ], st)

    s += sub("Frontend: AdPlayer Component", st)
    s += kv([
        ("File",        "apps/frontend/src/components/player/AdPlayer.tsx"),
        ("Trigger",     "Shown when showPreRoll === true and adsEnabled (subscriptionTier === 0 and config loaded)"),
        ("Skip button", "Locked for skipAfterSeconds (from config); shows countdown; unlocks to allow dismiss"),
        ("Controls",    "Mute toggle, Learn More link (clickThroughUrl), ad progress bar, advertiser name"),
        ("Completion",  "onComplete() fires on natural end or skip → VideoPlayer resumes main content"),
        ("Conversion",  "'Upgrade to remove ads' link pointing to /account"),
    ], st)

    s += sub("Frontend: AdBanner Component", st)
    s += kv([
        ("File",        "apps/frontend/src/components/player/AdBanner.tsx"),
        ("Trigger",     "Fired when Math.floor(currentTime / midRollIntervalSeconds) changes to a new slot"),
        ("Behaviour",   "Pauses main video; resumes on close. Auto-closes after durationSeconds (from config)"),
        ("Close button","Locked for closeAfterSeconds (from config); shows countdown; unlocks to dismiss"),
        ("Content",     "Image (imageUrl), headline, advertiser name, CTA button (Learn More), upgrade link"),
    ], st)

    s += sub("Updating Ad Campaigns (Zero-Downtime)", st)
    s += code_block([
        "// Edit appsettings.json (or appsettings.Production.json):",
        '"Ads": {',
        '  "Enabled": true,',
        '  "MidRollIntervalMinutes": 20,       // was 15 — stretch interval',
        '  "PreRoll": {',
        '    "VideoUrl": "https://cdn.example.com/new-campaign.mp4",',
        '    "AdvertiserName": "Acme Corp",',
        '    "SkipAfterSeconds": 5',
        '  },',
        '  "MidRoll": {',
        '    "ImageUrl": "https://cdn.example.com/banner.jpg",',
        '    "Headline": "Summer Sale — 50% off Premium",',
        '    "DurationSeconds": 20',
        '  }',
        '}',
        "// Restart backend container. Frontend cache expires in 5 min.",
        "// No frontend build or deployment needed.",
    ], st, label="appsettings.Production.json")
    s.append(PageBreak())

    # ── 8 ─────────────────────────────────────────────────────────────────────
    s += section("8. Database Schema", st)
    s += sub("Tables & Relationships", st)
    s += htable(
        ["Table", "PK", "Notable Columns / Relations"],
        [
            ["users",          "uuid", "email (unique), password_hash, name"],
            ["profiles",       "uuid", "user_id → users; name, avatar_url, pin_hash, is_kids_profile"],
            ["subscriptions",  "uuid", "user_id → users; tier (enum), starts_at, ends_at, stripe_subscription_id"],
            ["genres",         "uuid", "name, slug (unique)"],
            ["content",        "uuid", "title, slug, description, type (enum), required_tier, is_published, search_vector (generated tsvector)"],
            ["content_genres", "composite", "content_id → content, genre_id → genres"],
            ["seasons",        "uuid", "content_id → content, season_number"],
            ["episodes",       "uuid", "season_id → seasons, episode_number, duration_minutes"],
            ["video_assets",   "uuid", "content_id / episode_id (nullable); quality (enum), hls_manifest_path, raw_file_path, status (enum), bitrate_kbps"],
            ["subtitles",      "uuid", "content_id / episode_id (nullable); language_code, file_url (WebVTT in MinIO)"],
            ["watchlist",      "uuid", "profile_id → profiles, content_id → content, added_at"],
            ["watch_progress", "uuid", "profile_id, content_id, episode_id (nullable), position_seconds, is_completed (true at ≥90%), last_watched_at"],
            ["channels",       "uuid", "name, stream_url, category, is_live, thumbnail_url"],
            ["live_events",    "uuid", "channel_id → channels (nullable), title, scheduled_at, status (enum), stream_key"],
        ],
        st, cw=[4*cm, 2.5*cm, 9*cm])

    s += sub("Key Indexes", st)
    s += code_block([
        "-- Full-text search (generated tsvector column):",
        "CREATE INDEX idx_content_search  ON content USING GIN (search_vector);",
        "CREATE INDEX idx_title_trgm      ON content USING GIN (title gin_trgm_ops);",
        "",
        "-- User activity sorted by recency:",
        "CREATE INDEX idx_progress_profile ON watch_progress (profile_id, last_watched_at DESC);",
        "CREATE INDEX idx_watchlist_profile ON watchlist      (profile_id, added_at DESC);",
        "",
        "-- Content browsing:",
        "CREATE INDEX idx_content_type    ON content       (type, is_published);",
        "CREATE INDEX idx_content_genre   ON content_genres (genre_id);",
        "",
        "-- Asset lookup by content or episode:",
        "CREATE INDEX idx_asset_content   ON video_assets (content_id, quality);",
        "CREATE INDEX idx_asset_episode   ON video_assets (episode_id, quality);",
    ], st)
    s.append(PageBreak())

    # ── 9 ─────────────────────────────────────────────────────────────────────
    s += section("9. API Reference", st)

    def api_group(name, endpoints, st):
        out = [Paragraph(name, st['h3'])]
        data = [[Paragraph(h, st['th']) for h in ["Method", "Path", "Auth", "Description"]]]
        for m, p_, a, d in endpoints:
            data.append([
                Paragraph(m, st['td_bold']),
                Paragraph(p_, st['td_code']),
                Paragraph(a, st['td']),
                Paragraph(d, st['td']),
            ])
        tbl = Table(data, colWidths=[1.4*cm, 6.5*cm, 1.6*cm, 6*cm])
        tbl.setStyle(TableStyle(_TS_BASE + [
            ('BACKGROUND', (0,0), (-1,0), RED),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, HexColor('#fafafa')]),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        out += [tbl, Spacer(1, 10)]
        return out

    s += api_group("Authentication", [
        ("POST", "/api/auth/register", "—",       "Register; returns { accessToken, refreshToken, user }"),
        ("POST", "/api/auth/login",    "—",       "Login; returns { accessToken, refreshToken, user }"),
        ("POST", "/api/auth/refresh",  "Refresh", "Rotate refresh token; returns new token pair"),
        ("POST", "/api/auth/logout",   "Bearer",  "Invalidate refresh token in Redis"),
    ], st)

    s += api_group("Content", [
        ("GET",  "/api/content",                "—",     "Paginated list; ?page&pageSize&type"),
        ("GET",  "/api/content/featured",       "—",     "Featured titles (Redis cached 10 min)"),
        ("GET",  "/api/content/trending",       "—",     "Trending (Redis cached 10 min)"),
        ("GET",  "/api/content/genres",         "—",     "All genre slugs and names"),
        ("GET",  "/api/content/genre/{slug}",   "—",     "Content by genre, paginated"),
        ("GET",  "/api/content/{id}",           "—",     "Full detail: seasons, assets, subtitles"),
        ("GET",  "/api/content/{id}/stream",    "Bearer","Returns master M3U8 URL + qualities + subtitles"),
        ("POST", "/api/content/{id}/upload",    "Admin", "Returns presigned MinIO PUT URL for raw video"),
    ], st)

    s += api_group("Ads", [
        ("GET", "/api/ads/config", "—", "Returns full AdsConfigResponse (Enabled, PreRoll, MidRoll, MidRollIntervalSeconds). ResponseCache 300s."),
    ], st)

    s += api_group("Search", [
        ("GET", "/api/search", "—", "?q=&type=&genre=&year=  pg_trgm similarity + tsvector full-text"),
    ], st)

    s += api_group("Watch Progress", [
        ("GET", "/api/progress",             "Bearer", "All progress for active profile (Continue Watching)"),
        ("GET", "/api/progress/{contentId}", "Bearer", "Progress for one title"),
        ("PUT", "/api/progress/{contentId}", "Bearer", "Upsert position; marks completed at ≥90%"),
    ], st)

    s += api_group("Watchlist", [
        ("GET",    "/api/watchlist",             "Bearer", "All watchlist items for active profile"),
        ("POST",   "/api/watchlist/{contentId}", "Bearer", "Add title; idempotent"),
        ("DELETE", "/api/watchlist/{contentId}", "Bearer", "Remove title"),
    ], st)

    s += api_group("Users & Profiles", [
        ("GET",    "/api/users/me",                 "Bearer", "Current user info"),
        ("PUT",    "/api/users/me",                 "Bearer", "Update name / email"),
        ("GET",    "/api/users/me/profiles",        "Bearer", "List all profiles"),
        ("POST",   "/api/users/me/profiles",        "Bearer", "Create profile (max 5)"),
        ("PUT",    "/api/users/me/profiles/{id}",   "Bearer", "Update profile"),
        ("DELETE", "/api/users/me/profiles/{id}",   "Bearer", "Delete profile"),
        ("GET",    "/api/users/me/subscription",    "Bearer", "Active subscription details"),
    ], st)

    s += api_group("Live & Channels", [
        ("GET", "/api/live",           "—",     "Upcoming + live events list"),
        ("GET", "/api/live/{id}",      "Bearer","Live event detail + stream URL"),
        ("GET", "/api/channels",       "—",     "All TV channels"),
        ("GET", "/api/channels/{id}",  "Bearer","Channel detail + live HLS URL"),
    ], st)

    s += api_group("Go Streaming Service (port 8080)", [
        ("GET",  "/stream/{contentId}/master.m3u8",        "?token=", "Rewritten HLS variant playlist"),
        ("GET",  "/stream/{contentId}/{q}/prog_index.m3u8","?token=", "Quality-level playlist"),
        ("GET",  "/stream/{contentId}/{q}/{seg}.ts",       "?token=", "302 redirect to presigned MinIO URL"),
        ("GET",  "/live/{channelId}/stream.m3u8",          "?token=", "Live HLS stream proxy"),
        ("POST", "/internal/transcode",                   "X-Key",   "Enqueue transcode job (backend → Go)"),
        ("PATCH","/api/admin/assets/{id}/status",         "X-Key",   "Transcode complete callback (Go → backend)"),
        ("GET",  "/health",                               "—",       "Liveness probe"),
    ], st)
    s.append(PageBreak())

    # ── 10 ────────────────────────────────────────────────────────────────────
    s += section("10. Infrastructure & DevOps", st)
    s += sub("Docker Compose Services", st)
    s += htable(
        ["Service", "Image", "Port(s)", "Depends On"],
        [
            ["postgres",   "postgres:16-alpine",     "5432",       "—"],
            ["redis",      "redis:7-alpine",          "6379",       "—"],
            ["minio",      "minio/minio:latest",      "9000, 9001", "—"],
            ["minio-init", "minio/mc:latest",         "—",         "minio"],
            ["backend",    "apps/backend Dockerfile", "5000→8080",  "postgres, redis, minio"],
            ["streaming",  "apps/streaming Dockerfile","8080",      "minio, redis"],
            ["frontend",   "apps/frontend Dockerfile", "3000",      "backend, streaming"],
            ["nginx",      "infra/nginx Dockerfile",  "80, 443",    "all"],
        ],
        st, cw=[3*cm, 4.5*cm, 3*cm, 5*cm])

    s += sub("MinIO Buckets", st)
    s += htable(
        ["Bucket", "Access", "Contents"],
        [
            ["videos-raw",  "Private",     "Original uploaded video files (any container format)"],
            ["videos-hls",  "Public read", "Transcoded HLS segments + master playlists"],
            ["thumbnails",  "Public read", "Poster and backdrop images (JPEG / WebP)"],
            ["subtitles",   "Public read", "WebVTT subtitle files per language per title"],
        ],
        st, cw=[4*cm, 3*cm, 8.5*cm])

    s += sub("Nginx Routing", st)
    s += bullets([
        "location /api/ → proxy_pass http://backend:8080/ (REST API)",
        "location /stream/ → proxy_pass http://streaming:8080/ (HLS delivery)",
        "location /live/ → proxy_pass http://streaming:8080/ (live HLS)",
        "location / → proxy_pass http://frontend:3000/ (Next.js SSR + static)",
        "client_max_body_size 5G — permits large direct video uploads via Nginx",
        "proxy_read_timeout 3600s — prevents timeout waiting for long transcode callbacks",
    ], st)
    s.append(PageBreak())

    # ── 11 ────────────────────────────────────────────────────────────────────
    s += section("11. Security Architecture", st)
    s += sub("Authentication & Authorisation", st)
    s += bullets([
        "Passwords hashed with bcrypt (cost factor 12). Never stored or logged in plaintext.",
        "Access tokens are short-lived (15 min) — limits blast radius of any token theft.",
        "Refresh tokens are opaque server-side strings in Redis; can be revoked instantly by deleting the Redis key.",
        "Refresh tokens are rotated on every use — each /auth/refresh invalidates the previous token.",
        "Subscription tier is embedded in JWT claims; enforced by both backend (policy attribute) and Go middleware.",
        "Ad config endpoint is deliberately anonymous — it contains no secrets and must load even for unauthenticated sessions.",
    ], st)

    s += sub("Transport & Network Security", st)
    s += bullets([
        "All external traffic via HTTPS — Nginx terminates TLS; Let's Encrypt cert in production.",
        "Internal Docker network: services communicate over a private bridge network, not exposed externally.",
        "Backend ↔ Go service calls authenticated with X-Internal-Key header (shared secret, never in JWT).",
        "HLS segments gated by short-lived JWT query tokens; presigned MinIO URLs expire in 1 hour.",
    ], st)

    s += sub("Input Validation & Injection Prevention", st)
    s += bullets([
        "All inputs validated by FluentValidation pipeline behaviour before reaching MediatR handlers.",
        "EF Core uses parameterised queries throughout — no raw string SQL concatenation.",
        "Raw SQL in SearchController uses Npgsql parameters (@q) — immune to SQL injection.",
        "Frontend form inputs validated with zod schemas before API submission.",
        "File uploads restricted to video MIME types; size validated server-side.",
    ], st)

    s += sub("Phase 2 Security Enhancements", st)
    s += bullets([
        "Widevine (Chrome/Android) + FairPlay (Safari/iOS) DRM for Premium tier content.",
        "Rate limiting on auth endpoints — Redis sliding window, 5 attempts per 15 minutes.",
        "OWASP Content Security Policy headers added via Nginx.",
        "Automated dependency audits: Dependabot for NuGet, npm, Go modules; SAST in CI.",
    ], st)
    s.append(PageBreak())

    # ── 12 ────────────────────────────────────────────────────────────────────
    s += section("12. Scalability & Performance", st)
    s += sub("Horizontal Scaling Strategy", st)
    s += kv([
        ("Next.js Frontend",
         "Stateless — scale replicas behind Nginx. Server-rendered browse pages "
         "cached at CDN edge with stale-while-revalidate. Ad config cached 5 min at browser."),
        (".NET Core Backend",
         "Stateless — session data in Redis, no in-memory state. Npgsql connection pooling (10–100). "
         "Featured/trending content cached in Redis (10 min TTL). Ad config cached 5 min via ResponseCache."),
        ("Go Streaming",
         "Worker pool controls FFmpeg concurrency (default: 3 simultaneous processes). "
         "HLS serving = presigned redirects — no byte proxying. Scale replicas freely; MinIO is shared state."),
        ("PostgreSQL",
         "Read replicas for browse/search traffic. Write traffic to primary only. "
         "GIN indexes keep pg_trgm search fast at 1M+ rows."),
        ("Redis",
         "Redis Cluster for high availability. Separate logical DBs for tokens (TTL-critical) "
         "vs. content cache vs. rate limiting."),
        ("MinIO / CDN",
         "MinIO in production fronted by CloudFront. HLS .ts segments (~200KB each) are "
         "highly cacheable with long TTLs. Ad creative assets (video, images) served from CDN."),
    ], st, cw=[4*cm, 11.5*cm])

    s += sub("Performance Targets", st)
    s += htable(
        ["Metric", "Target"],
        [
            ["API response time (p95)",        "< 100ms"],
            ["Search response time",           "< 200ms (PostgreSQL GIN)"],
            ["HLS manifest response",          "< 50ms (Redis-cached path resolution)"],
            ["Ad config response",             "< 30ms (IOptions<T>, in-memory binding)"],
            ["Transcode time (90-min movie)",  "< 25 min (3 quality levels, parallel FFmpeg)"],
            ["Player startup time",            "< 3 seconds on 5 Mbps connection"],
            ["HLS segment cache hit rate",     "> 85% (CloudFront / Nginx proxy cache)"],
            ["Uptime SLA",                     "99.9% monthly"],
        ],
        st, cw=[7*cm, 8.5*cm])
    s.append(PageBreak())

    # ── 13 ────────────────────────────────────────────────────────────────────
    s += section("13. Development Workflow", st)
    s += sub("Local Setup", st)
    s += code_block([
        "git clone https://github.com/remon024/streming && cd streming",
        "cp .env.example .env          # fill in secrets",
        "make dev                      # starts all 7 Docker containers",
        "make migrate                  # runs EF Core migrations",
        "make seed                     # loads sample genres + content",
        "",
        "# Access points:",
        "http://localhost:3000         # Next.js frontend",
        "http://localhost:5000/swagger # Backend Swagger UI",
        "http://localhost:9001         # MinIO console",
        "http://localhost:8080/health  # Go service health check",
    ], st)

    s += sub("Ad System Verification Checklist", st)
    s += code_block([
        "1. GET http://localhost:5000/api/ads/config",
        "   → Returns JSON with enabled:true, midRollIntervalSeconds:900, preRoll, midRoll",
        "",
        "2. Log in as a Free tier user (subscriptionTier: 0)",
        "3. Navigate to /watch/{contentId}",
        "   → AdPlayer (pre-roll) appears before video starts",
        "   → Skip button is disabled for first 5 seconds, shows countdown",
        "   → Skip button enables; clicking it dismisses ad and starts content",
        "",
        "4. Fast-forward to 15:01 (or change MidRollIntervalMinutes: 1 in config to test quickly)",
        "   → Video pauses; AdBanner appears at bottom of player",
        "   → Close button locked for 5 seconds, then dismissible",
        "   → Video resumes after close",
        "",
        "5. Log in as a paid user (subscriptionTier: 1+)",
        "   → GET /api/ads/config is never called (useAdConfig disabled)",
        "   → No AdPlayer, no AdBanner — zero ad components rendered",
        "",
        "6. Update VideoUrl in appsettings.json, restart backend",
        "   → Wait 5 minutes (or clear browser TanStack Query cache)",
        "   → New ad creative plays on next /watch page load",
    ], st)

    s += sub("End-to-End Content Upload & Stream Test", st)
    s += code_block([
        "1.  POST /api/auth/register  → get access token",
        "2.  POST /api/content/{id}/upload  → get presigned MinIO PUT URL",
        "3.  PUT <presigned-url>  → upload raw video file",
        "4.  Backend calls POST http://streaming:8080/internal/transcode",
        "5.  Go service transcodes → uploads HLS → PATCH /api/admin/assets/{id}/status",
        "6.  Poll GET /api/content/{id} until videoAssets[].status === 'ready'",
        "7.  GET /api/content/{id}/stream → returns masterM3u8Url",
        "8.  Open /watch/{id} → VideoPlayer loads master.m3u8",
        "9.  Confirm 360p / 720p / 1080p levels in QualitySelector",
        "10. Play 30s → verify PUT /api/progress/{id} fires via browser Network tab",
        "11. Refresh page → player resumes at correct position",
    ], st)

    s += gap(12)
    s += [Paragraph("— End of Document —", st['caption'])]

    def on_page(c, d):
        cover_bg(c, d)
        page_header(c, d, "Technical Document  |  Engineering Reference")

    doc.build(s, onFirstPage=on_page, onLaterPages=on_page,
              canvasmaker=NumberedCanvas)
    print(f"✓  Technical document: {path}")


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_business("/home/user/streming/Streamix_Business_Document.pdf")
    build_technical("/home/user/streming/Streamix_Technical_Document.pdf")
    print("Done.")
