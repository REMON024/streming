from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import BalancedColumns
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import date

# Brand colors
RED     = HexColor('#E50914')
DARK    = HexColor('#141414')
SURFACE = HexColor('#1f1f1f')
GRAY    = HexColor('#757575')
LIGHT   = HexColor('#f5f5f1')
WHITE   = colors.white
BLACK   = colors.black

PAGE_W, PAGE_H = A4

# ─── Numbered page canvas ──────────────────────────────────────────────────────

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_page_number(num_pages)
            super().showPage()
        super().save()

    def _draw_page_number(self, page_count):
        p = self._pageNumber
        if p == 1:
            return
        self.setFont("Helvetica", 8)
        self.setFillColor(GRAY)
        self.drawRightString(PAGE_W - 2*cm, 1.2*cm, f"Page {p} of {page_count}")
        self.setStrokeColor(HexColor('#e0e0e0'))
        self.setLineWidth(0.5)
        self.line(2*cm, 1.6*cm, PAGE_W - 2*cm, 1.6*cm)


# ─── Style helpers ─────────────────────────────────────────────────────────────

def make_styles(base=None):
    s = getSampleStyleSheet()

    styles = {
        'cover_company': ParagraphStyle('cover_company',
            fontName='Helvetica-Bold', fontSize=11, textColor=RED,
            spaceAfter=6, alignment=TA_CENTER),

        'cover_title': ParagraphStyle('cover_title',
            fontName='Helvetica-Bold', fontSize=32, textColor=WHITE,
            spaceAfter=10, alignment=TA_CENTER, leading=40),

        'cover_sub': ParagraphStyle('cover_sub',
            fontName='Helvetica', fontSize=14, textColor=LIGHT,
            spaceAfter=6, alignment=TA_CENTER),

        'cover_meta': ParagraphStyle('cover_meta',
            fontName='Helvetica', fontSize=9, textColor=GRAY,
            alignment=TA_CENTER),

        'h1': ParagraphStyle('h1',
            fontName='Helvetica-Bold', fontSize=20, textColor=RED,
            spaceBefore=20, spaceAfter=6, leading=24),

        'h2': ParagraphStyle('h2',
            fontName='Helvetica-Bold', fontSize=14, textColor=DARK,
            spaceBefore=14, spaceAfter=4, leading=18),

        'h3': ParagraphStyle('h3',
            fontName='Helvetica-Bold', fontSize=11, textColor=DARK,
            spaceBefore=10, spaceAfter=3, leading=14),

        'body': ParagraphStyle('body',
            fontName='Helvetica', fontSize=10, textColor=HexColor('#333333'),
            spaceAfter=6, leading=15, alignment=TA_JUSTIFY),

        'bullet': ParagraphStyle('bullet',
            fontName='Helvetica', fontSize=10, textColor=HexColor('#333333'),
            spaceAfter=4, leading=14, leftIndent=16, bulletIndent=4),

        'code': ParagraphStyle('code',
            fontName='Courier', fontSize=8.5, textColor=HexColor('#1a1a1a'),
            backColor=HexColor('#f4f4f4'), spaceAfter=4, leading=13,
            leftIndent=12, rightIndent=12),

        'table_header': ParagraphStyle('table_header',
            fontName='Helvetica-Bold', fontSize=9, textColor=WHITE),

        'table_cell': ParagraphStyle('table_cell',
            fontName='Helvetica', fontSize=9, textColor=DARK, leading=12),

        'caption': ParagraphStyle('caption',
            fontName='Helvetica-Oblique', fontSize=8, textColor=GRAY,
            spaceAfter=8, alignment=TA_CENTER),

        'toc_h1': ParagraphStyle('toc_h1',
            fontName='Helvetica-Bold', fontSize=11, textColor=DARK,
            spaceAfter=3, leftIndent=0),

        'toc_h2': ParagraphStyle('toc_h2',
            fontName='Helvetica', fontSize=10, textColor=HexColor('#555555'),
            spaceAfter=2, leftIndent=16),
    }
    return styles


def hr(width=1, color=HexColor('#e0e0e0'), space=6):
    return [HRFlowable(width='100%', thickness=width, color=color,
                       spaceAfter=space, spaceBefore=space)]


def divider_red():
    return [HRFlowable(width='100%', thickness=2, color=RED,
                       spaceAfter=8, spaceBefore=0)]


def section_header(title, st):
    return [
        Spacer(1, 6),
        Paragraph(title, st['h1']),
        *divider_red(),
    ]


def subsection(title, st):
    return [Paragraph(title, st['h2'])]


def bullets(items, st, symbol='•'):
    return [Paragraph(f"{symbol}  {item}", st['bullet']) for item in items]


def kv_table(rows, st, col_widths=None):
    col_widths = col_widths or [5*cm, 11*cm]
    data = []
    for k, v in rows:
        data.append([
            Paragraph(f"<b>{k}</b>", st['table_cell']),
            Paragraph(v, st['table_cell']),
        ])
    tbl = Table(data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f9f9f9')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, HexColor('#fafafa')]),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#ddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return [tbl, Spacer(1, 8)]


def header_table(headers, rows, st, col_widths=None):
    data = [[Paragraph(h, st['table_header']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), st['table_cell']) for c in row])
    tbl = Table(data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), RED),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, HexColor('#fafafa')]),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#ddd')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return [tbl, Spacer(1, 8)]


def cover_page(title, subtitle, doc_type, version, st):
    """Returns flowables for a dark cover page."""
    today = date.today().strftime("%B %d, %Y")
    return [
        # Big top spacer
        Spacer(1, 3*cm),
        Paragraph("STREAMIX", st['cover_company']),
        Spacer(1, 0.4*cm),
        Paragraph(title, st['cover_title']),
        Spacer(1, 0.3*cm),
        Paragraph(subtitle, st['cover_sub']),
        Spacer(1, 1.5*cm),
        HRFlowable(width='60%', thickness=1.5, color=RED, hAlign='CENTER',
                   spaceAfter=12, spaceBefore=0),
        Spacer(1, 0.3*cm),
        Paragraph(doc_type, st['cover_meta']),
        Paragraph(f"Version {version}  ·  {today}", st['cover_meta']),
        Paragraph("Confidential — For Internal and Investor Use Only", st['cover_meta']),
        PageBreak(),
    ]


def cover_background(canvas_obj, doc):
    """Paint dark background on page 1."""
    if canvas_obj._pageNumber == 1:
        canvas_obj.saveState()
        canvas_obj.setFillColor(DARK)
        canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        # Red accent bar at top
        canvas_obj.setFillColor(RED)
        canvas_obj.rect(0, PAGE_H - 6*mm, PAGE_W, 6*mm, fill=1, stroke=0)
        # Red accent bar at bottom
        canvas_obj.rect(0, 0, PAGE_W, 4*mm, fill=1, stroke=0)
        canvas_obj.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
#  BUSINESS DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════

def build_business_doc(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Streamix – Business Document",
        author="Streamix Team",
    )

    st = make_styles()
    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += cover_page(
        "Streamix",
        "Next-Generation Video Streaming Platform",
        "BUSINESS DOCUMENT",
        "1.0",
        st,
    )

    # ── Table of Contents ──────────────────────────────────────────────────────
    story += section_header("Table of Contents", st)
    toc = [
        ("1", "Executive Summary"),
        ("2", "Company & Vision"),
        ("3", "Market Opportunity"),
        ("4", "Product Overview"),
        ("5", "Target Audience"),
        ("6", "Subscription & Revenue Model"),
        ("7", "Competitive Landscape"),
        ("8", "Go-to-Market Strategy"),
        ("9", "Technology & Operations"),
        ("10", "Risk & Mitigation"),
        ("11", "Financial Projections"),
        ("12", "Roadmap"),
    ]
    for num, title in toc:
        story.append(Paragraph(f"{num}.  {title}", st['toc_h1']))
    story.append(PageBreak())

    # ── 1. Executive Summary ───────────────────────────────────────────────────
    story += section_header("1. Executive Summary", st)
    story.append(Paragraph(
        "Streamix is a cloud-native video streaming platform built to deliver cinema-quality "
        "entertainment — movies, TV series, live sports, and documentary content — to subscribers "
        "globally. The platform combines adaptive HLS streaming, real-time transcoding, personalized "
        "recommendations, and multi-profile household management under a tiered subscription model.",
        st['body']))
    story.append(Spacer(1, 6))
    story += bullets([
        "Multi-bitrate adaptive streaming (360p → 4K) powered by a dedicated Go transcoding service.",
        "Clean, responsive Next.js 15 web application with a mobile-first design philosophy.",
        "Scalable .NET Core 8 backend following Clean Architecture with CQRS via MediatR.",
        "PostgreSQL full-text search with pg_trgm fuzzy matching for instant content discovery.",
        "Four subscription tiers (Free → Premium) designed to maximize average revenue per user.",
        "Designed for horizontal scalability: each service is independently containerized.",
    ], st)
    story.append(PageBreak())

    # ── 2. Company & Vision ────────────────────────────────────────────────────
    story += section_header("2. Company & Vision", st)
    story += subsection("Mission Statement", st)
    story.append(Paragraph(
        "To make premium entertainment accessible to every screen — delivering fast, "
        "reliable, beautifully presented video to subscribers regardless of device, "
        "bandwidth, or geography.",
        st['body']))
    story += subsection("Core Values", st)
    story += bullets([
        "Quality — every stream is adaptive, never buffering.",
        "Accessibility — content available across all devices and connection speeds.",
        "Personalization — intelligent recommendations powered by watch history.",
        "Transparency — clear pricing, no hidden fees.",
        "Privacy — user data is never sold to third parties.",
    ], st)
    story += subsection("Long-Term Vision", st)
    story.append(Paragraph(
        "Within five years, Streamix aims to become the leading independent streaming "
        "platform in its target markets, expanding from web-only to native iOS/Android apps, "
        "smart TV SDKs, and adding original content production as a differentiator.",
        st['body']))
    story.append(PageBreak())

    # ── 3. Market Opportunity ──────────────────────────────────────────────────
    story += section_header("3. Market Opportunity", st)
    story += subsection("Global Streaming Market", st)
    story.append(Paragraph(
        "The global video streaming market was valued at USD 544 billion in 2023 and is "
        "forecast to grow at a CAGR of 21.5% through 2030, driven by rising internet "
        "penetration, proliferation of connected devices, and the ongoing shift from "
        "traditional broadcast to on-demand consumption.",
        st['body']))
    story.append(Spacer(1, 6))

    story += header_table(
        ["Segment", "2023 Value", "2028 Forecast", "CAGR"],
        [
            ["SVOD (Subscription)", "$100B", "$190B", "13.7%"],
            ["AVOD (Ad-supported)", "$50B", "$130B", "21.1%"],
            ["Live Streaming", "$70B", "$185B", "21.5%"],
            ["Total OTT", "$220B", "$505B", "18.1%"],
        ],
        st, col_widths=[5*cm, 3.5*cm, 3.5*cm, 3.5*cm]
    )
    story.append(Paragraph("Source: Industry estimates, 2024.", st['caption']))

    story += subsection("Addressable Market", st)
    story += bullets([
        "Total Addressable Market (TAM): USD 220B global OTT video market (2023).",
        "Serviceable Addressable Market (SAM): USD 42B — English & MENA-language SVOD.",
        "Serviceable Obtainable Market (SOM): USD 210M — achievable in 36 months at 0.5% SAM share.",
    ], st)

    story += subsection("Tailwinds", st)
    story += bullets([
        "Over 5.4 billion internet users globally, growing by 150M per year.",
        "Smart TV penetration exceeds 60% of households in target markets.",
        "Mobile data costs falling 15% annually in emerging markets.",
        "Cord-cutting accelerating: cable TV household share dropped from 83% (2014) to 51% (2024).",
        "COVID-19 permanently elevated streaming consumption habits in 18–45 age cohort.",
    ], st)
    story.append(PageBreak())

    # ── 4. Product Overview ────────────────────────────────────────────────────
    story += section_header("4. Product Overview", st)
    story.append(Paragraph(
        "Streamix delivers video content through a web application and API-first platform "
        "that allows rapid extension to native mobile and TV applications. The product "
        "experience is designed around three pillars: discovery, playback quality, and "
        "personalization.",
        st['body']))

    story += subsection("Core Features", st)
    story += kv_table([
        ("Browse & Discover", "Curated rows by genre, trending, new releases, and editor picks. "
                              "Full-text fuzzy search across title and description."),
        ("Adaptive Streaming", "HLS multi-bitrate playback (360p / 720p / 1080p / 4K). "
                               "Player auto-selects quality based on bandwidth; manual override available."),
        ("Live Streaming", "Live sports, events, and TV channels with low-latency HLS delivery. "
                           "Live badge, real-time viewer count, upcoming schedule."),
        ("Multi-Profile", "Up to 5 profiles per account with independent watch history, "
                          "recommendations, and optional PIN protection."),
        ("Watch Progress", "Resume exactly where you left off across any device. "
                           "Continue Watching row auto-populated."),
        ("Watchlist", "Add/remove titles with optimistic UI. Accessible from any profile."),
        ("Subtitles & CC", "WebVTT subtitle tracks selectable per-play. "
                           "Auto-converted from SRT on upload."),
        ("Search", "Instant fuzzy search with pg_trgm similarity + PostgreSQL full-text vectors. "
                   "Filter by type, genre, and release year."),
        ("Subscription Mgmt", "Self-service tier upgrades/downgrades, billing history, "
                               "and cancellation with a 30-day notice period."),
        ("Admin Dashboard", "Content upload (presigned MinIO URLs), transcode status monitoring, "
                            "channel management, live event scheduling."),
    ], st, col_widths=[4.5*cm, 11*cm])
    story.append(PageBreak())

    # ── 5. Target Audience ─────────────────────────────────────────────────────
    story += section_header("5. Target Audience", st)
    story += subsection("Primary Segments", st)

    story += header_table(
        ["Segment", "Age", "Behaviour", "Primary Device"],
        [
            ["Young Adults", "18–34", "Heavy binge-watchers; mobile-first; price-sensitive", "Smartphone / Laptop"],
            ["Families", "28–45", "Multi-profile; value Kids Mode; weekend viewing", "Smart TV"],
            ["Sports Fans", "22–50", "Live-event driven; high churn risk if no live rights", "Smart TV / Mobile"],
            ["Cinephiles", "25–55", "Quality over quantity; independent & arthouse content", "Laptop / Tablet"],
        ],
        st, col_widths=[3.5*cm, 2*cm, 7*cm, 3*cm]
    )

    story += subsection("Geographic Focus", st)
    story += bullets([
        "Phase 1 (Year 1): English-language markets — US, UK, Canada, Australia.",
        "Phase 2 (Year 2): MENA Arabic-language markets — UAE, Saudi Arabia, Egypt.",
        "Phase 3 (Year 3): Localisation for South & Southeast Asia.",
    ], st)
    story.append(PageBreak())

    # ── 6. Subscription & Revenue Model ───────────────────────────────────────
    story += section_header("6. Subscription & Revenue Model", st)
    story += subsection("Tier Structure", st)

    story += header_table(
        ["Tier", "Price / Month", "Streams", "Max Quality", "Ads", "Downloads"],
        [
            ["Free",     "USD 0",    "1",  "720p",  "Yes",  "No"],
            ["Basic",    "USD 7.99", "1",  "1080p", "No",   "No"],
            ["Standard", "USD 13.99","2",  "1080p", "No",   "Yes (2 titles)"],
            ["Premium",  "USD 19.99","4",  "4K HDR","No",   "Yes (unlimited)"],
        ],
        st, col_widths=[3*cm, 3*cm, 2.5*cm, 2.5*cm, 2*cm, 2.5*cm]
    )

    story += subsection("Revenue Streams", st)
    story += bullets([
        "Subscription Revenue (SVOD): Primary revenue — recurring monthly fees.",
        "Advertising (AVOD): Banner and pre-roll ads served to Free tier users via third-party ad network.",
        "Pay-Per-View (PPV): Premium live events (boxing, concerts) available as one-time purchases.",
        "B2B Licensing: API access for airlines, hotels, and corporate wellness platforms.",
    ], st)

    story += subsection("Unit Economics (Target, Year 2)", st)
    story += kv_table([
        ("ARPU (blended)",       "USD 11.40 / month"),
        ("Customer Acquisition Cost", "USD 8.50"),
        ("LTV (24-month avg.)",  "USD 274"),
        ("LTV / CAC Ratio",      "32× (target: >3×)"),
        ("Gross Margin (streaming)", "~72%"),
        ("Monthly Churn Target", "<2.8%"),
    ], st)
    story.append(PageBreak())

    # ── 7. Competitive Landscape ───────────────────────────────────────────────
    story += section_header("7. Competitive Landscape", st)

    story += header_table(
        ["Platform", "Strengths", "Weaknesses", "Our Advantage"],
        [
            ["Netflix",
             "Massive content library, global brand, strong recommendation engine",
             "High subscription cost; no free tier; password sharing crackdown",
             "Free tier; lower price point; live sports"],
            ["Disney+",
             "Franchise content (Marvel, Star Wars, Pixar); family focus",
             "Limited adult content; minimal live sports",
             "Broader genre coverage; live events"],
            ["Amazon Prime",
             "Bundled with Prime; strong originals",
             "Complex UI; content mixed with rentals",
             "Cleaner UX; transparent pricing"],
            ["YouTube",
             "Free; massive user-generated content",
             "Low premium content quality; ad-heavy",
             "Professional content; no UGC noise"],
            ["Streamix",
             "Adaptive streaming tech; live + VOD; free tier",
             "Smaller content library at launch",
             "—"],
        ],
        st, col_widths=[2.8*cm, 4.5*cm, 4*cm, 4.2*cm]
    )

    story += subsection("Differentiation Strategy", st)
    story += bullets([
        "Technical superiority: In-house Go streaming service enables lower latency and cost than third-party CDNs.",
        "Live + VOD hybrid: Most SVOD platforms lack integrated live event infrastructure.",
        "Free tier as acquisition funnel: Drives top-of-funnel growth without paid marketing.",
        "Developer-first API: B2B licensing opens revenue from enterprise partners.",
    ], st)
    story.append(PageBreak())

    # ── 8. Go-to-Market Strategy ───────────────────────────────────────────────
    story += section_header("8. Go-to-Market Strategy", st)
    story += subsection("Launch Phases", st)
    story += kv_table([
        ("Phase 1 — Beta (Month 1–3)",
         "Invite-only access to 5,000 beta users. Collect NPS feedback. Fix critical UX issues. "
         "Seed content library with 200+ licensed titles."),
        ("Phase 2 — Soft Launch (Month 4–6)",
         "Open registration. Free tier open to all. Paid tiers launched. "
         "Target 50,000 registered users, 8,000 paid subscribers."),
        ("Phase 3 — Growth (Month 7–18)",
         "Performance marketing campaigns (Google, Meta, TikTok). "
         "Referral program (30-day free Premium). Influencer / creator partnerships. "
         "Target 500,000 registered users, 80,000 paid subscribers."),
        ("Phase 4 — Expansion (Month 19–36)",
         "Launch iOS & Android native apps. Enter MENA market. "
         "Secure live sports rights for regional leagues."),
    ], st, col_widths=[5*cm, 10.5*cm])

    story += subsection("Customer Acquisition Channels", st)
    story += bullets([
        "SEO / Content marketing — streaming guides, genre landing pages.",
        "Social media advertising — short-form video clips as ads (TikTok, Instagram Reels).",
        "Referral program — both referrer and referred receive 1 month free Standard.",
        "Partnerships — ISP bundle deals; smart TV manufacturer pre-installs.",
        "App Store Optimisation (post mobile launch).",
    ], st)
    story.append(PageBreak())

    # ── 9. Technology & Operations ─────────────────────────────────────────────
    story += section_header("9. Technology & Operations", st)
    story += subsection("Technology Stack Summary", st)
    story += kv_table([
        ("Frontend",           "Next.js 15, React 18, TypeScript 5, TailwindCSS, HLS.js, TanStack Query, Zustand"),
        ("Backend API",        ".NET Core 8, ASP.NET Core, MediatR, FluentValidation, AutoMapper, EF Core 8"),
        ("Streaming Service",  "Go 1.24, Chi router, FFmpeg (multi-bitrate HLS), MinIO SDK, go-redis"),
        ("Database",           "PostgreSQL 16 with pg_trgm + tsvector full-text search"),
        ("Cache",              "Redis 7 — API response cache, refresh tokens, session data"),
        ("Object Storage",     "MinIO (S3-compatible) — raw video, HLS segments, thumbnails, subtitles"),
        ("Infrastructure",     "Docker, Docker Compose; production: Kubernetes with horizontal pod autoscaling"),
        ("CDN (production)",   "CloudFront / Cloudflare for HLS segment delivery at the edge"),
        ("Auth",               "JWT (HS256, 15-min access + 7-day refresh), NextAuth.js v5"),
        ("Monitoring",         "Serilog + Seq, health check endpoints, Prometheus + Grafana"),
    ], st, col_widths=[4.5*cm, 11*cm])

    story += subsection("Content Operations", st)
    story += bullets([
        "Content ingest: Admin uploads raw video via presigned MinIO URL (no size limit).",
        "Transcoding SLA: 360p/720p/1080p variants ready within 30 minutes of upload.",
        "Quality assurance: Automated playback smoke test after transcoding confirms segments play.",
        "Subtitles: Uploaded as SRT; auto-converted to WebVTT by the Go service.",
        "Metadata: Managed via Admin API (title, description, genres, release year, maturity rating).",
    ], st)
    story.append(PageBreak())

    # ── 10. Risk & Mitigation ──────────────────────────────────────────────────
    story += section_header("10. Risk & Mitigation", st)
    story += header_table(
        ["Risk", "Likelihood", "Impact", "Mitigation"],
        [
            ["Content licensing costs exceed projections", "Medium", "High",
             "Start with public domain + Creative Commons content; license incrementally as revenue grows."],
            ["Infrastructure costs at scale", "Medium", "Medium",
             "CDN for HLS delivery (cost per GB declines at volume); auto-scaling to match demand."],
            ["Churn due to thin content library", "High (early)", "High",
             "Free tier retains users; focus on live sports/events as sticky content."],
            ["Competitor price war", "Low", "Medium",
             "Cost leadership via in-house streaming stack; diversify into B2B licensing."],
            ["DRM / piracy", "Medium", "Medium",
             "Integrate Widevine / FairPlay DRM in Phase 2; short-lived signed streaming tokens now."],
            ["Regulatory / geo-blocking", "Low", "Low",
             "Geo-filtering by IP; legal review per market before expansion."],
            ["Cybersecurity breach", "Low", "High",
             "bcrypt password hashing; JWT short expiry; Redis token rotation; regular pen tests."],
        ],
        st, col_widths=[4*cm, 2.2*cm, 2*cm, 7.3*cm]
    )
    story.append(PageBreak())

    # ── 11. Financial Projections ──────────────────────────────────────────────
    story += section_header("11. Financial Projections", st)
    story.append(Paragraph(
        "The following projections are illustrative estimates based on comparable SVOD platforms "
        "at similar stages of growth. Actuals will vary with content licensing spend, marketing "
        "efficiency, and geographic mix.",
        st['body']))
    story.append(Spacer(1, 6))

    story += header_table(
        ["Metric", "Year 1", "Year 2", "Year 3"],
        [
            ["Registered Users",        "100,000",   "500,000",   "2,000,000"],
            ["Paid Subscribers",        "15,000",    "80,000",    "350,000"],
            ["ARPU (USD/month)",        "$9.20",     "$11.40",    "$12.80"],
            ["Monthly Recurring Rev.",  "$138K",     "$912K",     "$4.48M"],
            ["Annual Revenue",          "$1.65M",    "$10.9M",    "$53.8M"],
            ["Content Licensing Cost",  "$0.6M",     "$3.2M",     "$14.0M"],
            ["Infrastructure Cost",     "$0.3M",     "$1.1M",     "$3.8M"],
            ["Gross Profit",            "$0.75M",    "$6.6M",     "$36.0M"],
            ["Gross Margin",            "45%",       "61%",       "67%"],
        ],
        st, col_widths=[5.5*cm, 3*cm, 3*cm, 3*cm]
    )
    story.append(Paragraph("All figures in USD. Projections exclude capital expenditure.", st['caption']))
    story.append(PageBreak())

    # ── 12. Roadmap ────────────────────────────────────────────────────────────
    story += section_header("12. Roadmap", st)
    story += header_table(
        ["Quarter", "Milestone"],
        [
            ["Q1 2025", "MVP launch: web app, VOD, 4 subscription tiers, 200 titles"],
            ["Q2 2025", "Live streaming: sports events, TV channels"],
            ["Q3 2025", "iOS & Android native apps (React Native)"],
            ["Q4 2025", "Widevine / FairPlay DRM integration; offline downloads"],
            ["Q1 2026", "MENA market launch; Arabic UI & subtitles"],
            ["Q2 2026", "Smart TV apps (Samsung Tizen, LG webOS)"],
            ["Q3 2026", "Recommendation engine (collaborative filtering)"],
            ["Q4 2026", "Original content production — first 3 exclusive titles"],
            ["2027",    "Series A fundraising; expand to South & Southeast Asia"],
        ],
        st, col_widths=[3*cm, 12.5*cm]
    )
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("— End of Document —", st['caption']))

    # ── Build ──────────────────────────────────────────────────────────────────
    def on_page(canvas_obj, doc):
        cover_background(canvas_obj, doc)
        if canvas_obj._pageNumber > 1:
            canvas_obj.saveState()
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.setFillColor(RED)
            canvas_obj.drawString(2*cm, PAGE_H - 1.5*cm, "STREAMIX")
            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(GRAY)
            canvas_obj.drawRightString(PAGE_W - 2*cm, PAGE_H - 1.5*cm, "Business Document  |  Confidential")
            canvas_obj.setStrokeColor(HexColor('#e0e0e0'))
            canvas_obj.setLineWidth(0.5)
            canvas_obj.line(2*cm, PAGE_H - 1.8*cm, PAGE_W - 2*cm, PAGE_H - 1.8*cm)
            canvas_obj.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page,
              canvasmaker=NumberedCanvas)
    print(f"✓  Business document: {path}")


# ══════════════════════════════════════════════════════════════════════════════
#  TECHNICAL DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════

def build_technical_doc(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Streamix – Technical Document",
        author="Streamix Engineering",
    )

    st = make_styles()
    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += cover_page(
        "Streamix",
        "Technical Architecture & Engineering Reference",
        "TECHNICAL DOCUMENT",
        "1.0",
        st,
    )

    # ── Table of Contents ──────────────────────────────────────────────────────
    story += section_header("Table of Contents", st)
    toc = [
        ("1", "System Architecture Overview"),
        ("2", "Technology Stack"),
        ("3", "Repository & Project Structure"),
        ("4", "Backend Service — .NET Core 8"),
        ("5", "Streaming Service — Go"),
        ("6", "Frontend — Next.js 15"),
        ("7", "Database Schema"),
        ("8", "API Reference"),
        ("9", "Infrastructure & DevOps"),
        ("10", "Security Architecture"),
        ("11", "Scalability & Performance"),
        ("12", "Development Workflow"),
    ]
    for num, title in toc:
        story.append(Paragraph(f"{num}.  {title}", st['toc_h1']))
    story.append(PageBreak())

    # ── 1. System Architecture Overview ───────────────────────────────────────
    story += section_header("1. System Architecture Overview", st)
    story.append(Paragraph(
        "Streamix follows a microservices architecture with three independently deployable "
        "services, each built in the language best suited to its responsibility. All services "
        "are containerised and orchestrated via Docker Compose (development) or Kubernetes "
        "(production).",
        st['body']))

    story += subsection("High-Level Architecture", st)
    story.append(Paragraph(
        "The diagram below shows data flow between client, services, and storage layers:",
        st['body']))
    story.append(Spacer(1, 4))

    # ASCII architecture diagram as styled code block
    arch = [
        "  ┌──────────────────────────────────────────────────────────┐",
        "  │                  CLIENT BROWSER / APP                   │",
        "  └────────────┬─────────────────────────┬──────────────────┘",
        "               │  REST/JSON (JWT)          │  HLS + WebVTT",
        "               ▼                           ▼",
        "  ┌────────────────────┐     ┌─────────────────────────────┐",
        "  │   .NET Core 8 API  │     │    Go Streaming Service     │",
        "  │   port 5000        │     │    port 8080                │",
        "  │                    │     │                             │",
        "  │  Auth, Content,    │──►  │  HLS manifest serving       │",
        "  │  Watchlist,        │     │  Multi-bitrate segments      │",
        "  │  Progress, Search  │◄──  │  FFmpeg transcoding          │",
        "  │  Live, Admin       │     │  Subtitle SRT→VTT            │",
        "  └──────┬─────────────┘     └──────┬──────────────────────┘",
        "         │                           │",
        "    ┌────▼────┐   ┌────────┐   ┌────▼────────────┐",
        "  │ Postgres │   │ Redis  │   │    MinIO         │",
        "  │ 16       │   │ 7      │   │  (S3-compat)    │",
        "  │          │   │        │   │  videos-raw      │",
        "  │ Main DB  │   │ Cache  │   │  videos-hls      │",
        "  │          │   │ Tokens │   │  thumbnails      │",
        "  └──────────┘   └────────┘   │  subtitles       │",
        "                              └──────────────────┘",
    ]
    for line in arch:
        story.append(Paragraph(line, st['code']))
    story.append(Spacer(1, 8))

    story += subsection("Service Responsibilities", st)
    story += kv_table([
        (".NET Core 8 API",
         "Authentication (JWT), user & profile management, content catalogue, "
         "watchlist, watch progress, search, subscription management, admin operations, "
         "internal callbacks from the Go service. Only service with direct PostgreSQL access."),
        ("Go Streaming Service",
         "Receives raw video paths from the backend, runs FFmpeg to produce multi-bitrate HLS, "
         "stores segments in MinIO, and serves signed HLS manifests and segments to clients. "
         "No direct DB access — queries backend (Redis-cached) for content metadata."),
        ("Next.js 15 Frontend",
         "Server-side rendered and client-side React application. App Router with Server "
         "Components for browse/search pages; Client Components for player, watchlist, and "
         "interactive UI. Acts as API gateway via Next.js rewrites to avoid browser CORS issues."),
    ], st, col_widths=[4.5*cm, 11*cm])
    story.append(PageBreak())

    # ── 2. Technology Stack ────────────────────────────────────────────────────
    story += section_header("2. Technology Stack", st)

    story += header_table(
        ["Layer", "Technology", "Version", "Rationale"],
        [
            ["Frontend Framework", "Next.js", "15.x", "App Router, Server Components, built-in rewrites"],
            ["UI Language", "TypeScript", "5.x", "Type safety across API boundaries"],
            ["Styling", "Tailwind CSS", "3.x", "Utility-first; dark theme with brand tokens"],
            ["HLS Player", "HLS.js", "1.5.x", "Adaptive bitrate, quality selection, DRM-ready"],
            ["Server State", "TanStack Query", "5.x", "Caching, background refetch, infinite scroll"],
            ["Client State", "Zustand", "4.x", "Auth store with localStorage persistence"],
            ["Auth (FE)", "NextAuth.js", "5.x (beta)", "App Router compatible; credentials + OAuth"],
            ["Backend Framework", ".NET / ASP.NET Core", "8.0 / 10.0", "High-performance, mature ecosystem"],
            ["ORM", "Entity Framework Core", "8.x", "Code-first migrations, LINQ, Npgsql driver"],
            ["CQRS Bus", "MediatR", "12.x", "Decoupled handlers, pipeline behaviours"],
            ["Validation", "FluentValidation", "11.x", "Declarative rules, MediatR integration"],
            ["Mapping", "AutoMapper", "13.x", "Entity ↔ DTO projection"],
            ["Streaming Lang.", "Go", "1.24", "Goroutines for parallel transcoding; low memory"],
            ["HTTP Router (Go)", "Chi", "5.x", "Lightweight, idiomatic, middleware-first"],
            ["Redis Client (Go)", "go-redis", "9.x", "Full Redis 7 support"],
            ["MinIO Client (Go)", "minio-go", "7.x", "S3-compatible presigned URLs"],
            ["Transcoder", "FFmpeg", "6.x", "Industry-standard multi-bitrate HLS"],
            ["Database", "PostgreSQL", "16", "JSONB, tsvector, pg_trgm, uuid_generate_v4"],
            ["Cache", "Redis", "7", "Strings, sorted sets, TTL-based token storage"],
            ["Object Storage", "MinIO", "latest", "S3-compatible; self-hosted; no egress fees in dev"],
            ["Reverse Proxy", "Nginx", "1.25", "SSL termination, routing, static file serving"],
            ["Containerisation", "Docker / Compose", "v5", "Dev orchestration; prod → Kubernetes"],
        ],
        st, col_widths=[4*cm, 3.5*cm, 2.5*cm, 5.5*cm]
    )
    story.append(PageBreak())

    # ── 3. Repository Structure ────────────────────────────────────────────────
    story += section_header("3. Repository & Project Structure", st)
    story.append(Paragraph("Monorepo layout under <b>streming/</b>:", st['body']))

    tree = [
        "streming/",
        "├── .env.example",
        "├── docker-compose.yml",
        "├── docker-compose.dev.yml",
        "├── Makefile",
        "├── apps/",
        "│   ├── frontend/                 # Next.js 15",
        "│   │   ├── src/",
        "│   │   │   ├── app/              # App Router pages",
        "│   │   │   ├── components/       # browse/ player/ live/ ui/ layout/",
        "│   │   │   ├── lib/api/          # axios wrappers per domain",
        "│   │   │   ├── hooks/            # useDebounce, useWatchlist, useProfile",
        "│   │   │   ├── store/            # Zustand auth store",
        "│   │   │   └── types/            # TS interfaces mirroring backend DTOs",
        "│   │   ├── Dockerfile",
        "│   │   └── package.json",
        "│   ├── backend/                  # .NET Core 8",
        "│   │   ├── src/",
        "│   │   │   ├── StreamingPlatform.API/",
        "│   │   │   ├── StreamingPlatform.Application/",
        "│   │   │   ├── StreamingPlatform.Domain/",
        "│   │   │   └── StreamingPlatform.Infrastructure/",
        "│   │   ├── StreamingPlatform.sln",
        "│   │   └── Dockerfile",
        "│   └── streaming/                # Go",
        "│       ├── cmd/server/main.go",
        "│       ├── internal/",
        "│       │   ├── config/ handler/ service/",
        "│       │   ├── storage/ cache/",
        "│       │   └── transcoder/ middleware/",
        "│       ├── go.mod",
        "│       └── Dockerfile",
        "└── infra/",
        "    ├── postgres/init.sql         # Extensions + schema bootstrap",
        "    ├── redis/redis.conf",
        "    ├── minio/setup.sh            # Bucket creation",
        "    └── nginx/nginx.conf",
    ]
    for line in tree:
        story.append(Paragraph(line, st['code']))
    story.append(PageBreak())

    # ── 4. Backend Service ─────────────────────────────────────────────────────
    story += section_header("4. Backend Service — .NET Core 8", st)
    story += subsection("Clean Architecture Layers", st)
    story += kv_table([
        ("Domain",
         "Pure C# entities and enums. No framework dependencies. "
         "Entities: User, Profile, Subscription, Content, Season, Episode, "
         "VideoAsset, Subtitle, Genre, WatchlistItem, WatchProgress, Channel, LiveEvent."),
        ("Application",
         "Use cases implemented as MediatR IRequest<T> command/query handlers. "
         "Interfaces (IApplicationDbContext, ITokenService, ICacheService, IStorageService, "
         "IStreamingService) defined here; implementations in Infrastructure. "
         "FluentValidation validators injected as MediatR pipeline behaviours."),
        ("Infrastructure",
         "EF Core ApplicationDbContext, 14 IEntityTypeConfiguration<T> files, "
         "TokenService (JWT), CacheService (Redis), MinioStorageService, "
         "StreamingServiceClient (HttpClient). All registered via DependencyInjection.cs."),
        ("API",
         "7 ASP.NET Core controllers, ExceptionHandlingMiddleware (ProblemDetails RFC 7807), "
         "Serilog request logging, Swagger/OpenAPI with Bearer scheme, health checks, "
         "auto-migration on startup in development."),
    ], st, col_widths=[3.5*cm, 12*cm])

    story += subsection("Key Domain Enums", st)
    story += header_table(
        ["Enum", "Values"],
        [
            ["ContentType",      "Movie | Series | Documentary | ShortFilm"],
            ["VideoQuality",     "Q360p | Q720p | Q1080p | Q4K"],
            ["ProcessingStatus", "Pending | Processing | Ready | Failed"],
            ["SubscriptionTier", "Free(0) | Basic(1) | Standard(2) | Premium(3)"],
        ],
        st, col_widths=[5*cm, 10.5*cm]
    )

    story += subsection("JWT Token Design", st)
    story += kv_table([
        ("Algorithm",         "HS256 with 256-bit secret from environment"),
        ("Access Token TTL",  "15 minutes"),
        ("Refresh Token TTL", "7 days, stored in Redis as refresh:{token} → userId"),
        ("Claims",            "userId, email, profileId, subscriptionTier, jti"),
        ("Rotation",          "Each /auth/refresh issues a new refresh token and invalidates the old one"),
    ], st)

    story += subsection("Search Implementation", st)
    story.append(Paragraph(
        "PostgreSQL full-text search using a generated <b>tsvector</b> column combined with "
        "<b>pg_trgm</b> similarity for fuzzy matching:",
        st['body']))
    sql = [
        "-- Generated column on content table:",
        "search_vector tsvector GENERATED ALWAYS AS",
        "  (to_tsvector('english', title || ' ' || coalesce(description,''))) STORED",
        "",
        "-- GIN indexes:",
        "CREATE INDEX idx_content_search ON content USING GIN (search_vector);",
        "CREATE INDEX idx_title_trgm    ON content USING GIN (title gin_trgm_ops);",
        "",
        "-- Query (raw SQL in SearchController):",
        "WHERE similarity(title, @q) > 0.2",
        "   OR search_vector @@ plainto_tsquery('english', @q)",
        "ORDER BY similarity(title, @q) DESC, ts_rank(search_vector, ...) DESC",
    ]
    for line in sql:
        story.append(Paragraph(line, st['code']))
    story.append(PageBreak())

    # ── 5. Streaming Service ───────────────────────────────────────────────────
    story += section_header("5. Streaming Service — Go", st)
    story += subsection("Transcoding Pipeline", st)
    story.append(Paragraph(
        "When the backend receives a confirmed raw video upload it calls "
        "<b>POST /internal/transcode</b> on the Go service. The service enqueues the job "
        "in a bounded worker pool (default: 3 concurrent FFmpeg processes) and returns "
        "<b>202 Accepted</b> immediately.",
        st['body']))

    pipeline = [
        "1. Job received → push to buffered channel (worker pool queue)",
        "2. Worker picks up job → downloads raw file from MinIO (videos-raw bucket)",
        "3. FFmpeg invoked with multi-bitrate filter_complex:",
        "   [0:v] split=3 → scale to 360p / 720p / 1080p",
        "   libx264 encoding: 800k / 2800k / 5000k bitrates",
        "   HLS output: 6-second segments, VOD playlist type",
        "   Output: videos-hls/{assetId}/master.m3u8 + v0/ v1/ v2/ segment trees",
        "4. All segment files uploaded to MinIO (videos-hls bucket)",
        "5. PATCH /api/admin/assets/{id}/status called on backend",
        "   Body: { status: 'ready', hlsManifestPath, processedAt }",
        "   Header: X-Internal-Key: {INTERNAL_API_KEY}",
    ]
    for line in pipeline:
        story.append(Paragraph(f"  {line}", st['code']))
    story.append(Spacer(1, 8))

    story += subsection("HLS Manifest Rewriting (Token Gating)", st)
    story.append(Paragraph(
        "The Go service does not expose raw MinIO URLs to clients. Instead it rewrites "
        "HLS playlist files on-the-fly to replace segment paths with token-gated URLs "
        "that pass through the service:",
        st['body']))
    hls_flow = [
        "Client  →  GET /stream/{contentId}/master.m3u8?token=JWT",
        "Go      →  1. Validate JWT",
        "           2. Check subscriptionTier >= content.requiredTier",
        "              (content metadata from Redis or backend call)",
        "           3. Fetch master.m3u8 from MinIO",
        "           4. Rewrite each variant playlist URL:",
        "              /stream/{contentId}/v{q}/prog_index.m3u8?token=JWT",
        "           5. Return rewritten playlist (200 OK)",
        "",
        "Client  →  GET /stream/{contentId}/v1/seg003.ts?token=JWT",
        "Go      →  1. Validate JWT",
        "           2. Generate presigned MinIO GET URL (1-hour expiry)",
        "           3. Return 302 redirect to presigned URL",
        "              (MinIO serves bytes; Go does not proxy the stream)",
    ]
    for line in hls_flow:
        story.append(Paragraph(f"  {line}", st['code']))
    story.append(Spacer(1, 8))

    story += subsection("Go Project Structure", st)
    go_tree = [
        "apps/streaming/",
        "├── cmd/server/main.go            # Wire config, router, start HTTP server",
        "├── internal/",
        "│   ├── config/config.go          # Viper env-based config",
        "│   ├── server/server.go          # Chi router + CORS + auth middleware",
        "│   ├── handler/",
        "│   │   ├── stream_handler.go     # Manifest + segment endpoints",
        "│   │   ├── transcode_handler.go  # POST /internal/transcode",
        "│   │   └── health_handler.go",
        "│   ├── service/",
        "│   │   ├── stream_service.go     # Resolve asset paths, check tiers",
        "│   │   └── transcode_service.go  # FFmpeg orchestration",
        "│   ├── storage/minio_client.go   # GetObject, PutObject, PresignedURL",
        "│   ├── cache/redis_client.go     # Token cache, segment metadata",
        "│   ├── transcoder/",
        "│   │   ├── ffmpeg.go             # Command builder",
        "│   │   ├── pipeline.go           # Multi-quality runner (errgroup)",
        "│   │   └── worker_pool.go        # Bounded goroutine pool",
        "│   └── middleware/auth.go        # JWT validation (shared secret)",
        "└── pkg/models/",
        "    ├── transcode_job.go",
        "    └── stream_token.go",
    ]
    for line in go_tree:
        story.append(Paragraph(line, st['code']))
    story.append(PageBreak())

    # ── 6. Frontend ────────────────────────────────────────────────────────────
    story += section_header("6. Frontend — Next.js 15", st)
    story += subsection("App Router Page Structure", st)
    pages = [
        ("/ (root)",               "Redirects to /browse"),
        ("/(auth)/login",          "CredentialsProvider login form with react-hook-form + zod"),
        ("/(auth)/register",       "Registration form; calls POST /api/auth/register"),
        ("/browse",                "Server Component: Hero + ContentRow per genre (parallel fetch)"),
        ("/browse/[genre]",        "Filtered grid; GenreFilter pill navigation"),
        ("/title/[contentId]",     "Full detail page: backdrop, synopsis, episodes, watchlist btn"),
        ("/watch/[contentId]",     "Full-screen player; no navbar; loads HLS via VideoPlayer"),
        ("/search",                "Debounced search bar + TanStack Query result grid"),
        ("/live",                  "Live Now / Upcoming / TV Channels sections"),
        ("/live/[eventId]",        "LivePlayer (low-latency HLS, no seek bar)"),
        ("/sports",                "Sport-type filter tabs"),
        ("/tv",                    "Channel category grid"),
        ("/profile/select",        "Who's Watching avatar picker; switches active profile"),
        ("/profile/[profileId]",   "Profile settings: name, maturity rating, language"),
        ("/profile/[profileId]/watchlist", "Watchlist grid for active profile"),
        ("/account",               "Membership tier, billing history, password change"),
    ]
    story += header_table(["Route", "Description"], pages, st, col_widths=[6*cm, 9.5*cm])

    story += subsection("VideoPlayer Architecture", st)
    story += kv_table([
        ("Library",         "HLS.js v1.5 with native HLS fallback for Safari"),
        ("Quality switch",  "hls.currentLevel = n (-1 = auto); live quality list from hls.levels"),
        ("Token auth",      "xhrSetup callback adds Authorization Bearer header to XHR requests"),
        ("Subtitles",       "<track> elements added after HLS attach; VTT served from MinIO"),
        ("Resume",          "videoRef.currentTime = startPosition after HLS is attached"),
        ("Keyboard shorts", "Space/K=play-pause, ←/→=±10s, M=mute, F=fullscreen, ↑/↓=volume"),
        ("Progress sync",   "useProgressSync hook: useDebouncedCallback(10s) + fire on pause/unmount"),
        ("Inactivity hide", "Controls hidden after 3s of no mouse movement; shown on mousemove"),
    ], st)

    story += subsection("API Client Pattern", st)
    story.append(Paragraph(
        "All API calls go through <b>src/lib/api/client.ts</b> — an axios instance with "
        "two interceptors:",
        st['body']))
    story += bullets([
        "Request interceptor: reads accessToken from Zustand store → sets Authorization: Bearer {token}.",
        "Response interceptor: on 401 → calls POST /api/auth/refresh with stored refresh token → "
        "retries original request; on second 401 → clears store and redirects to /login.",
    ], st)

    story += subsection("Edge Middleware", st)
    story.append(Paragraph(
        "<b>src/middleware.ts</b> runs on the Next.js edge runtime and protects routes before "
        "any page code executes. Routes <code>/browse/*</code>, <code>/watch/*</code>, "
        "<code>/title/*</code>, <code>/profile/*</code>, and <code>/account</code> redirect "
        "to <code>/login</code> when no valid session cookie is present.",
        st['body']))
    story.append(PageBreak())

    # ── 7. Database Schema ─────────────────────────────────────────────────────
    story += section_header("7. Database Schema", st)
    story += subsection("Entity Relationship Summary", st)

    story += header_table(
        ["Table", "Primary Key", "Foreign Keys / Relations"],
        [
            ["users",          "uuid (uuid_generate_v4)", "—"],
            ["profiles",       "uuid", "user_id → users.id"],
            ["subscriptions",  "uuid", "user_id → users.id"],
            ["genres",         "uuid", "—"],
            ["content",        "uuid", "—  (+ generated search_vector tsvector)"],
            ["content_genres", "composite (content_id, genre_id)", "both → their tables"],
            ["seasons",        "uuid", "content_id → content.id"],
            ["episodes",       "uuid", "season_id → seasons.id"],
            ["video_assets",   "uuid", "content_id → content.id  OR  episode_id → episodes.id"],
            ["subtitles",      "uuid", "content_id / episode_id (nullable)"],
            ["watchlist",      "uuid", "profile_id → profiles.id, content_id → content.id"],
            ["watch_progress", "uuid", "profile_id, content_id, episode_id (nullable)"],
            ["channels",       "uuid", "—  (live TV channels)"],
            ["live_events",    "uuid", "channel_id → channels.id (nullable)"],
        ],
        st, col_widths=[4*cm, 4*cm, 7.5*cm]
    )

    story += subsection("Critical Indexes", st)
    idx = [
        "-- Full-text search",
        "CREATE INDEX idx_content_search  ON content USING GIN (search_vector);",
        "CREATE INDEX idx_title_trgm      ON content USING GIN (title gin_trgm_ops);",
        "",
        "-- User activity (sort by recency)",
        "CREATE INDEX idx_progress_profile ON watch_progress (profile_id, last_watched_at DESC);",
        "CREATE INDEX idx_watchlist_profile ON watchlist      (profile_id, added_at DESC);",
        "",
        "-- Content browsing",
        "CREATE INDEX idx_content_type       ON content (type, is_published);",
        "CREATE INDEX idx_content_genre      ON content_genres (genre_id);",
        "",
        "-- Asset lookup",
        "CREATE INDEX idx_video_asset_content  ON video_assets (content_id, quality);",
        "CREATE INDEX idx_video_asset_episode  ON video_assets (episode_id, quality);",
    ]
    for line in idx:
        story.append(Paragraph(line, st['code']))
    story.append(PageBreak())

    # ── 8. API Reference ───────────────────────────────────────────────────────
    story += section_header("8. API Reference", st)

    def api_group(name, endpoints):
        result = [Paragraph(name, st['h3'])]
        data = [["Method", "Path", "Auth", "Description"]]
        for m, p, a, d in endpoints:
            data.append([
                Paragraph(m, st['table_cell']),
                Paragraph(p, st['code']),
                Paragraph(a, st['table_cell']),
                Paragraph(d, st['table_cell']),
            ])
        tbl = Table(data, colWidths=[1.5*cm, 6.5*cm, 1.5*cm, 6*cm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), RED),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, HexColor('#fafafa')]),
            ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#ddd')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ]))
        result += [tbl, Spacer(1, 8)]
        return result

    story += api_group("Authentication — /api/auth", [
        ("POST", "/api/auth/register",  "—",       "Register new account; returns token pair"),
        ("POST", "/api/auth/login",     "—",       "Authenticate; returns token pair"),
        ("POST", "/api/auth/refresh",   "Refresh", "Rotate refresh token; returns new pair"),
        ("POST", "/api/auth/logout",    "Bearer",  "Invalidate refresh token in Redis"),
    ])

    story += api_group("Content — /api/content", [
        ("GET", "/api/content",              "—",      "Paginated list; ?page&pageSize&type"),
        ("GET", "/api/content/featured",     "—",      "Featured titles (Redis cached 10 min)"),
        ("GET", "/api/content/trending",     "—",      "Trending (Redis cached 10 min)"),
        ("GET", "/api/content/genres",       "—",      "All genre slugs + names"),
        ("GET", "/api/content/genre/{slug}", "—",      "Content by genre, paginated"),
        ("GET", "/api/content/{id}",         "—",      "Full detail with seasons, assets, subtitles"),
        ("GET", "/api/content/{id}/stream",  "Bearer", "Returns master M3U8 URL + qualities + subtitles"),
        ("POST","/api/content/{id}/upload",  "Admin",  "Returns presigned MinIO PUT URL"),
    ])

    story += api_group("Search — /api/search", [
        ("GET", "/api/search", "—", "?q=&type=&genre=&year= — fuzzy + full-text search"),
    ])

    story += api_group("Watch Progress — /api/progress", [
        ("GET", "/api/progress",            "Bearer", "All progress for active profile (continue watching)"),
        ("GET", "/api/progress/{contentId}","Bearer", "Progress for one title"),
        ("PUT", "/api/progress/{contentId}","Bearer", "Upsert position; marks completed at ≥90%"),
    ])

    story += api_group("Watchlist — /api/watchlist", [
        ("GET",    "/api/watchlist",            "Bearer", "All watchlist items for active profile"),
        ("POST",   "/api/watchlist/{contentId}","Bearer", "Add title; idempotent"),
        ("DELETE", "/api/watchlist/{contentId}","Bearer", "Remove title"),
    ])

    story += api_group("Users & Profiles — /api/users", [
        ("GET", "/api/users/me",                    "Bearer", "Current user info"),
        ("PUT", "/api/users/me",                    "Bearer", "Update name / email"),
        ("GET", "/api/users/me/profiles",           "Bearer", "List all profiles"),
        ("POST","/api/users/me/profiles",           "Bearer", "Create profile (max 5)"),
        ("PUT", "/api/users/me/profiles/{id}",      "Bearer", "Update profile"),
        ("DELETE","/api/users/me/profiles/{id}",    "Bearer", "Delete profile"),
        ("GET", "/api/users/me/subscription",       "Bearer", "Active subscription details"),
    ])

    story += api_group("Streaming Service — Go (port 8080)", [
        ("GET",  "/stream/{contentId}/master.m3u8",       "?token=", "Rewritten HLS variant playlist"),
        ("GET",  "/stream/{contentId}/{q}/prog_index.m3u8","?token=", "Quality-level HLS playlist"),
        ("GET",  "/stream/{contentId}/{q}/{seg}.ts",       "?token=", "302 redirect to presigned MinIO URL"),
        ("POST", "/internal/transcode",                   "X-Key",   "Enqueue transcode job (backend→Go)"),
        ("PATCH","/api/admin/assets/{id}/status",         "X-Key",   "Transcode complete callback (Go→backend)"),
        ("GET",  "/health",                               "—",       "Liveness probe"),
    ])
    story.append(PageBreak())

    # ── 9. Infrastructure & DevOps ─────────────────────────────────────────────
    story += section_header("9. Infrastructure & DevOps", st)
    story += subsection("Docker Compose Services", st)
    story += header_table(
        ["Service", "Image", "Port(s)", "Depends On"],
        [
            ["postgres",    "postgres:16-alpine",    "5432",       "—"],
            ["redis",       "redis:7-alpine",         "6379",       "—"],
            ["minio",       "minio/minio:latest",     "9000, 9001", "—"],
            ["minio-init",  "minio/mc:latest",        "—",          "minio"],
            ["backend",     "apps/backend Dockerfile","5000→8080",  "postgres, redis, minio"],
            ["streaming",   "apps/streaming Dockerfile","8080",     "minio, redis"],
            ["frontend",    "apps/frontend Dockerfile","3000",      "backend, streaming"],
            ["nginx",       "infra/nginx Dockerfile", "80, 443",    "frontend, backend, streaming"],
        ],
        st, col_widths=[3*cm, 4.5*cm, 3*cm, 5*cm]
    )

    story += subsection("MinIO Buckets", st)
    story += header_table(
        ["Bucket", "Access", "Content"],
        [
            ["videos-raw",   "Private",      "Original uploaded video files (any format)"],
            ["videos-hls",   "Public read",  "Transcoded HLS segments + master playlists"],
            ["thumbnails",   "Public read",  "Poster and backdrop JPEG/WebP images"],
            ["subtitles",    "Public read",  "WebVTT subtitle files per language"],
        ],
        st, col_widths=[4*cm, 3*cm, 8.5*cm]
    )

    story += subsection("Nginx Routing Rules", st)
    story += bullets([
        "location /api/ → proxy_pass http://backend:8080/",
        "location /stream/ → proxy_pass http://streaming:8080/",
        "location / → proxy_pass http://frontend:3000/",
        "client_max_body_size 5G — allows large video uploads through Nginx",
        "proxy_read_timeout 3600s — prevents timeout during long FFmpeg transcode status polling",
    ], st)

    story += subsection("Makefile Targets", st)
    story += header_table(
        ["Target", "Command Run"],
        [
            ["dev",            "docker compose -f docker-compose.yml -f docker-compose.dev.yml up"],
            ["build",          "docker compose build"],
            ["migrate",        "docker compose run --rm backend dotnet ef database update"],
            ["seed",           "docker compose run --rm backend dotnet run --project tools/Seeder"],
            ["test-backend",   "cd apps/backend && dotnet test"],
            ["test-streaming", "cd apps/streaming && go test ./..."],
            ["test-frontend",  "cd apps/frontend && pnpm test"],
            ["lint-go",        "cd apps/streaming && golangci-lint run"],
        ],
        st, col_widths=[4*cm, 11.5*cm]
    )
    story.append(PageBreak())

    # ── 10. Security Architecture ──────────────────────────────────────────────
    story += section_header("10. Security Architecture", st)
    story += subsection("Authentication & Authorisation", st)
    story += bullets([
        "Passwords hashed with bcrypt (cost factor 12). Never stored in plaintext.",
        "Access tokens are short-lived (15 min) to limit blast radius of token theft.",
        "Refresh tokens are opaque random strings stored server-side in Redis. "
        "Stolen refresh tokens can be revoked instantly by deleting the Redis key.",
        "Refresh tokens are rotated on every use — each refresh invalidates the previous token.",
        "Subscription tier is embedded in the JWT claim; backend and Go service both enforce access.",
        "Profile switching requires a separate claim update (new JWT issued); PIN-protected profiles "
        "require PIN verification before JWT is re-issued.",
    ], st)

    story += subsection("Transport Security", st)
    story += bullets([
        "All external traffic via HTTPS (Nginx terminates TLS; cert from Let's Encrypt in production).",
        "Internal Docker network: services communicate over the Docker bridge network, not exposed externally.",
        "Internal API calls (backend ↔ Go) authenticated with X-Internal-Key shared secret.",
        "HLS segments gated by short-lived JWT query tokens; even public-read MinIO URLs are presigned "
        "with 1-hour expiry.",
    ], st)

    story += subsection("Input Validation & Injection Prevention", st)
    story += bullets([
        "All backend inputs validated by FluentValidation before reaching handlers.",
        "EF Core uses parameterised queries throughout — no raw string concatenation.",
        "Raw SQL in SearchController uses Npgsql parameters (@q) — immune to SQL injection.",
        "Frontend form inputs validated with zod schemas before submission.",
        "File upload restricted to video MIME types; file size validated server-side.",
    ], st)

    story += subsection("Planned Security Enhancements (Phase 2)", st)
    story += bullets([
        "Widevine (Chrome/Android) + FairPlay (Safari/iOS) DRM for Premium tier content.",
        "Rate limiting on auth endpoints (Redis sliding window, 5 attempts / 15 min).",
        "OWASP-aligned Content Security Policy headers via Nginx.",
        "Regular dependency audit: dependabot for NuGet/npm/Go; automated CVE scanning in CI.",
    ], st)
    story.append(PageBreak())

    # ── 11. Scalability & Performance ─────────────────────────────────────────
    story += section_header("11. Scalability & Performance", st)
    story += subsection("Horizontal Scaling Strategy", st)
    story += kv_table([
        ("Frontend (Next.js)",
         "Stateless — scale replicas behind Nginx load balancer. "
         "SSR pages cached at CDN edge (Cloudflare) with stale-while-revalidate."),
        ("Backend (.NET Core)",
         "Stateless — session data in Redis, no in-memory state. "
         "Scale to N replicas; PostgreSQL connection pool via Npgsql (default: 10–100 connections). "
         "Read-heavy endpoints backed by Redis (10-min TTL for featured/trending content)."),
        ("Go Streaming",
         "Worker pool controls FFmpeg concurrency (default: 3). "
         "HLS serving is cheap — just presigned URL redirects, no byte proxying. "
         "Scale replicas freely; MinIO is the shared state."),
        ("PostgreSQL",
         "Read replicas for read-heavy browse/search traffic. "
         "Write traffic (progress updates, watchlist) to primary only. "
         "GIN indexes keep search fast at 1M+ content rows."),
        ("Redis",
         "Redis Cluster for high availability. "
         "Separate logical databases for tokens (TTL-critical) vs. content cache."),
        ("MinIO / CDN",
         "MinIO in production replaced by or fronted by S3 + CloudFront. "
         "HLS segments served at edge — each .ts file is ~200KB, highly cacheable."),
    ], st, col_widths=[4*cm, 11.5*cm])

    story += subsection("Performance Targets", st)
    story += header_table(
        ["Metric", "Target"],
        [
            ["Time to first byte (API)",         "< 100ms p95"],
            ["Search response time",             "< 200ms p95 (PostgreSQL GIN)"],
            ["HLS manifest response",            "< 50ms (Redis-cached path resolution)"],
            ["Transcode time (90-min movie)",    "< 25 min (3 quality levels parallel)"],
            ["Segment cache hit rate",           "> 85% (CloudFront / Nginx proxy cache)"],
            ["Player startup time",              "< 3 seconds on 5 Mbps connection"],
            ["Uptime SLA",                       "99.9% monthly"],
        ],
        st, col_widths=[7*cm, 8.5*cm]
    )
    story.append(PageBreak())

    # ── 12. Development Workflow ───────────────────────────────────────────────
    story += section_header("12. Development Workflow", st)
    story += subsection("Local Development Setup", st)

    setup_steps = [
        "1.  git clone https://github.com/remon024/streming && cd streming",
        "2.  cp .env.example .env  # fill in secrets",
        "3.  make dev              # starts all 7 Docker containers",
        "4.  make migrate          # runs EF Core migrations",
        "5.  make seed             # loads sample genres + content",
        "6.  Open http://localhost:3000  (frontend)",
        "    Open http://localhost:5000/swagger  (backend API docs)",
        "    Open http://localhost:9001  (MinIO console)",
    ]
    for step in setup_steps:
        story.append(Paragraph(step, st['code']))
    story.append(Spacer(1, 8))

    story += subsection("End-to-End Upload & Stream Test", st)
    e2e = [
        "1. Register admin account: POST /api/auth/register",
        "2. Get presigned upload URL: POST /api/content/{id}/upload",
        "3. Upload video file via HTTP PUT to presigned URL",
        "4. Backend calls POST http://streaming:8080/internal/transcode",
        "5. Go service transcodes → uploads HLS → calls PATCH /api/admin/assets/{id}/status",
        "6. Poll GET /api/content/{id} until videoAssets[].status === 'ready'",
        "7. GET /api/content/{id}/stream → returns masterM3u8Url",
        "8. Open /watch/{id} in browser → VideoPlayer loads master.m3u8",
        "9. Confirm 360p / 720p / 1080p quality levels appear in QualitySelector",
        "10. Play 30 seconds → check PUT /api/progress/{id} fires",
        "11. Refresh page → confirm player resumes at correct position",
    ]
    for step in e2e:
        story.append(Paragraph(step, st['code']))
    story.append(Spacer(1, 8))

    story += subsection("Branch Strategy", st)
    story += kv_table([
        ("main",       "Production-ready code only. Protected branch."),
        ("develop",    "Integration branch for feature PRs."),
        ("feature/*",  "Individual feature branches off develop."),
        ("hotfix/*",   "Critical fixes branched from main; merged to both main and develop."),
    ], st)

    story += subsection("Testing Strategy", st)
    story += bullets([
        "Backend: xUnit unit tests for Application handlers + Infrastructure services. "
        "Integration tests use TestContainers (real PostgreSQL + Redis containers).",
        "Go: Standard library testing package; table-driven unit tests for FFmpeg command builder "
        "and HLS manifest rewriter.",
        "Frontend: Vitest + React Testing Library for component tests; Playwright for E2E.",
        "CI pipeline (GitHub Actions): lint → unit tests → integration tests → Docker build on every PR.",
    ], st)

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("— End of Document —", st['caption']))

    # ── Build ──────────────────────────────────────────────────────────────────
    def on_page(canvas_obj, doc):
        cover_background(canvas_obj, doc)
        if canvas_obj._pageNumber > 1:
            canvas_obj.saveState()
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.setFillColor(RED)
            canvas_obj.drawString(2*cm, PAGE_H - 1.5*cm, "STREAMIX")
            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(GRAY)
            canvas_obj.drawRightString(PAGE_W - 2*cm, PAGE_H - 1.5*cm,
                                       "Technical Document  |  Engineering Reference")
            canvas_obj.setStrokeColor(HexColor('#e0e0e0'))
            canvas_obj.setLineWidth(0.5)
            canvas_obj.line(2*cm, PAGE_H - 1.8*cm, PAGE_W - 2*cm, PAGE_H - 1.8*cm)
            canvas_obj.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page,
              canvasmaker=NumberedCanvas)
    print(f"✓  Technical document: {path}")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_business_doc("/home/user/streming/Streamix_Business_Document.pdf")
    build_technical_doc("/home/user/streming/Streamix_Technical_Document.pdf")
    print("Done.")
