"""Generate Skills Pack PDF with Romanian diacritics support."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Flowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ---------------------------------------------------------------------------
# FONT REGISTRATION (DejaVu = full Romanian diacritics support)
# ---------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DV",      f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-Bold",  f"{FONT_DIR}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-Mono",  f"{FONT_DIR}/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DV-MonoB", f"{FONT_DIR}/DejaVuSansMono-Bold.ttf"))

# Map font family for <b> tags in Paragraphs
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DV-Bold")
registerFontFamily("DV-Mono", normal="DV-Mono", bold="DV-MonoB")

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Skills-Pack-Claude-Code.pdf")

TEXT_PRIMARY = HexColor("#111111")
TEXT_DIM     = HexColor("#555555")
TEXT_MUTED   = HexColor("#888888")

SKILL_COLORS = [
    HexColor("#059669"),  # 1 emerald
    HexColor("#d97706"),  # 2 amber
    HexColor("#7c3aed"),  # 3 violet
    HexColor("#e11d48"),  # 4 rose
    HexColor("#0891b2"),  # 5 cyan
    HexColor("#2563eb"),  # 6 blue
    HexColor("#ea580c"),  # 7 orange
    HexColor("#c026d3"),  # 8 fuchsia
]

# ---------------------------------------------------------------------------
# STYLES
# ---------------------------------------------------------------------------
def make_styles():
    s = {}
    s["hero_title"] = ParagraphStyle(
        "hero_title", fontName="DV-Bold", fontSize=36,
        leading=40, textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceAfter=4*mm)
    s["hero_desc"] = ParagraphStyle(
        "hero_desc", fontName="DV", fontSize=11,
        leading=16, textColor=TEXT_DIM, alignment=TA_LEFT, spaceAfter=3*mm)
    s["section_label"] = ParagraphStyle(
        "section_label", fontName="DV-Bold", fontSize=8,
        leading=10, textColor=TEXT_MUTED, alignment=TA_LEFT, spaceAfter=2*mm)
    s["section_title"] = ParagraphStyle(
        "section_title", fontName="DV-Bold", fontSize=22,
        leading=26, textColor=TEXT_PRIMARY, alignment=TA_LEFT,
        spaceBefore=8*mm, spaceAfter=3*mm)
    s["section_desc"] = ParagraphStyle(
        "section_desc", fontName="DV", fontSize=10,
        leading=15, textColor=TEXT_DIM, alignment=TA_LEFT, spaceAfter=6*mm)
    s["card_title"] = ParagraphStyle(
        "card_title", fontName="DV-Bold", fontSize=12,
        leading=16, textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceAfter=2*mm)
    s["card_body"] = ParagraphStyle(
        "card_body", fontName="DV", fontSize=9.5,
        leading=14, textColor=TEXT_DIM, alignment=TA_LEFT, spaceAfter=2*mm)
    s["skill_num"] = ParagraphStyle(
        "skill_num", fontName="DV-Bold", fontSize=28,
        leading=30, textColor=TEXT_MUTED, alignment=TA_LEFT)
    s["skill_name"] = ParagraphStyle(
        "skill_name", fontName="DV-Bold", fontSize=13,
        leading=17, textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceAfter=2*mm)
    s["skill_desc"] = ParagraphStyle(
        "skill_desc", fontName="DV", fontSize=9.5,
        leading=14, textColor=TEXT_DIM, alignment=TA_LEFT, spaceAfter=3*mm)
    s["skill_prompt"] = ParagraphStyle(
        "skill_prompt", fontName="DV-Mono", fontSize=7.5,
        leading=11, textColor=HexColor("#444444"), alignment=TA_LEFT, spaceAfter=2*mm)
    s["skill_tags"] = ParagraphStyle(
        "skill_tags", fontName="DV", fontSize=7.5,
        leading=10, textColor=TEXT_MUTED, alignment=TA_LEFT)
    s["tip_title"] = ParagraphStyle(
        "tip_title", fontName="DV-Bold", fontSize=11,
        leading=14, textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceAfter=1*mm)
    s["tip_body"] = ParagraphStyle(
        "tip_body", fontName="DV", fontSize=9,
        leading=13, textColor=TEXT_DIM, alignment=TA_LEFT)
    s["footer"] = ParagraphStyle(
        "footer", fontName="DV", fontSize=8,
        leading=11, textColor=TEXT_MUTED, alignment=TA_CENTER)
    return s


# ---------------------------------------------------------------------------
# FLOWABLES
# ---------------------------------------------------------------------------
class ColorBar(Flowable):
    def __init__(self, color, width=None, height=2.5):
        super().__init__()
        self.bar_color = color
        self.bar_width = width
        self.bar_height = height
    def wrap(self, availWidth, availHeight):
        self.bar_width = self.bar_width or availWidth
        return (self.bar_width, self.bar_height)
    def draw(self):
        self.canv.setFillColor(self.bar_color)
        self.canv.roundRect(0, 0, self.bar_width, self.bar_height, 1, fill=1, stroke=0)


class GradientBar(Flowable):
    def __init__(self, c1, c2, width=None, height=2.5):
        super().__init__()
        self.c1, self.c2 = c1, c2
        self.bar_width = width
        self.bar_height = height
    def wrap(self, availWidth, availHeight):
        self.bar_width = self.bar_width or min(40*mm, availWidth)
        return (self.bar_width, self.bar_height)
    def draw(self):
        steps = 40
        w = self.bar_width / steps
        r1, g1, b1 = self.c1.red, self.c1.green, self.c1.blue
        r2, g2, b2 = self.c2.red, self.c2.green, self.c2.blue
        for i in range(steps):
            t = i / (steps - 1)
            self.canv.setFillColorRGB(
                r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t)
            x = i * w
            self.canv.rect(max(0, x - 0.5), 0, w + 1, self.bar_height, fill=1, stroke=0)


class SkillCard(Flowable):
    def __init__(self, num, name, desc, prompt, tags, color, styles, card_width=None):
        super().__init__()
        self.num, self.name, self.desc = num, name, desc
        self.prompt, self.tags = prompt, tags
        self.color, self.styles = color, styles
        self.card_width = card_width
        self._height = 0

    def wrap(self, availWidth, availHeight):
        w = self.card_width or availWidth
        inner = w - 8*mm
        self._paras = [
            Paragraph(self.num, self.styles["skill_num"]),
            Paragraph(self.name, self.styles["skill_name"]),
            Paragraph(self.desc, self.styles["skill_desc"]),
            Paragraph(f"&gt; {self.prompt}", self.styles["skill_prompt"]),
            Paragraph(self.tags, self.styles["skill_tags"]),
        ]
        self._heights = [p.wrap(inner, 999)[1] for p in self._paras]
        self._inner_w = inner
        self._height = 3 + 5*mm + sum(self._heights) + 1.5*mm * 4 + 4*mm
        self.card_width = w
        return (w, self._height)

    def draw(self):
        c = self.canv
        w, h = self.card_width, self._height
        # Card bg
        c.setFillColor(HexColor("#fafafa"))
        c.setStrokeColor(HexColor("#e4e4e7"))
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=1)
        # Top color bar
        c.setFillColor(self.color)
        c.roundRect(0, h - 3, w, 3, 1.5, fill=1, stroke=0)
        # Text
        y, x, sp = h - 3 - 5*mm, 4*mm, 1.5*mm
        for i in range(3):
            y -= self._heights[i]
            self._paras[i].drawOn(c, x, y)
            y -= sp
        # Prompt block
        ph = self._heights[3]
        y -= 1*mm
        c.setFillColor(HexColor("#f0f0f2"))
        c.setStrokeColor(HexColor("#e0e0e4"))
        c.setLineWidth(0.3)
        c.roundRect(x - 1*mm, y - ph - 1.5*mm, self._inner_w + 2*mm, ph + 3*mm, 3, fill=1, stroke=1)
        c.setFillColor(self.color)
        c.roundRect(x - 1*mm, y - ph - 1.5*mm, 2, ph + 3*mm, 1, fill=1, stroke=0)
        y -= ph
        self._paras[3].drawOn(c, x + 1*mm, y)
        y -= sp + 2*mm
        # Tags
        y -= self._heights[4]
        self._paras[4].drawOn(c, x, y)


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
SKILLS = [
    {"num": "01", "name": "Analyzing Financial Statements",
     "desc": "Calculeaz\u0103 \u0219i interpreteaz\u0103 indicatori financiari cheie \u2014 profitabilitate, lichiditate, \u00eendatorare, eficien\u021b\u0103 \u0219i valuare \u2014 din orice format de raport financiar.",
     "prompt": "Analizeaz\u0103 acest raport financiar \u0219i calculeaz\u0103 to\u021bi indicatorii cheie",
     "tags": "Excel  \u00b7  CSV  \u00b7  PDF  \u00b7  ROE  \u00b7  P/E  \u00b7  DCF"},
    {"num": "02", "name": "Applying Brand Guidelines",
     "desc": "Aplic\u0103 consistent culorile, fonturile, layout-ul \u0219i tonul de comunicare al brandului t\u0103u pe toate documentele generate de Claude.",
     "prompt": "Creeaz\u0103 o prezentare PowerPoint cu branding-ul nostru despre rezultatele Q3",
     "tags": "PowerPoint  \u00b7  PDF  \u00b7  Excel  \u00b7  Customizabil"},
    {"num": "03", "name": "Brainstorming",
     "desc": "Explorare structurat\u0103 a ideilor cu metodologia Design Thinking. Genereaz\u0103 2-3 abord\u0103ri diferite cu pro \u0219i contra \u00eenainte de implementare.",
     "prompt": "Vreau s\u0103 adaug un sistem de notific\u0103ri \u00een aplica\u021bie \u2014 hai s\u0103 facem brainstorming",
     "tags": "Design Thinking  \u00b7  Planning  \u00b7  Pro/Contra"},
    {"num": "04", "name": "Competitive Ads Extractor",
     "desc": "Extrage \u0219i analizeaz\u0103 reclamele concuren\u021bei din Facebook Ad Library \u0219i LinkedIn. Identific\u0103 mesaje, tipare vizuale \u0219i strategii care func\u021bioneaz\u0103.",
     "prompt": "Extrage reclamele active de la Notion din Facebook Ad Library",
     "tags": "Facebook  \u00b7  LinkedIn  \u00b7  Screenshots  \u00b7  Copy Analysis"},
    {"num": "05", "name": "Creating Financial Models",
     "desc": "Modele financiare avansate: DCF cu WACC \u0219i valoare terminal\u0103, analiz\u0103 de sensibilitate, simul\u0103ri Monte Carlo \u0219i planificare pe scenarii.",
     "prompt": "Construie\u0219te un model DCF pentru aceast\u0103 companie cu datele financiare ata\u0219ate",
     "tags": "DCF  \u00b7  Monte Carlo  \u00b7  Sensibilitate  \u00b7  Scenarii"},
    {"num": "06", "name": "Deep Researcher",
     "desc": "Cercetare comprehensiv\u0103 \u00een 6 pa\u0219i: definire scope, explorare, investiga\u021bie profund\u0103, validare cross-references, sintez\u0103 \u0219i raport structurat.",
     "prompt": "Cerceteaz\u0103 pia\u021ba HR Tech SaaS: dimensiune, juc\u0103tori principali, tendin\u021be",
     "tags": "Multi-surs\u0103  \u00b7  Cross-referencing  \u00b7  Raport structurat"},
    {"num": "07", "name": "File Organizer",
     "desc": "Organizeaz\u0103 inteligent fi\u0219iere \u0219i foldere: g\u0103se\u0219te duplicate prin MD5, sugereaz\u0103 structuri logice \u0219i automatizeaz\u0103 cleanup-ul cu aprobare prealabil\u0103.",
     "prompt": "Organizeaz\u0103 folderul meu Downloads \u2014 e haos acolo",
     "tags": "Duplicate  \u00b7  Cleanup  \u00b7  Arhivare  \u00b7  Restructurare"},
    {"num": "08", "name": "Prompt Factory",
     "desc": "Genereaz\u0103 prompturi world-class prin 7 \u00eentreb\u0103ri sau din 69 presets pre-configurate din 15 domenii. Output \u00een XML, Claude, ChatGPT sau Gemini.",
     "prompt": "Folose\u0219te preset-ul Senior Full-Stack Engineer \u00een format Claude",
     "tags": "69 Presets  \u00b7  XML  \u00b7  Claude  \u00b7  ChatGPT  \u00b7  Gemini"},
]

TIPS = [
    ("Fii specific",
     '"Cerceteaz\u0103 pia\u021ba EV batteries: dimensiune, top 5 juc\u0103tori, tendin\u021be" bate "Cerceteaz\u0103 ceva despre baterii" de fiecare dat\u0103.'),
    ("Ata\u0219eaz\u0103 fi\u0219iere",
     "Trage fi\u0219iere direct \u00een Claude Code prin drag & drop. Rapoarte financiare, documente de brand, date CSV \u2014 totul func\u021bioneaz\u0103."),
    ("Combin\u0103 skill-uri",
     "Deep Researcher pentru research, apoi Financial Models pentru valuare, apoi Brand Guidelines pentru prezentare. Un pipeline complet."),
    ("Personalizeaz\u0103",
     "Editeaz\u0103 SKILL.md din folderul oric\u0103rui skill pentru a-l adapta nevoilor tale: culori de brand, template-uri, presets custom."),
]


# ---------------------------------------------------------------------------
# BUILD PDF
# ---------------------------------------------------------------------------
def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        topMargin=20*mm, bottomMargin=15*mm,
        leftMargin=20*mm, rightMargin=20*mm,
        title="Skills Pack \u2014 Claude Code", author="AI Accelerator")

    page_w = A4[0] - 40*mm
    story = []

    # ===== PAGE 1: HERO =====
    story.append(Spacer(1, 25*mm))
    story.append(GradientBar(HexColor("#7c3aed"), HexColor("#2563eb"), width=40*mm, height=3))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("CLAUDE CODE", ParagraphStyle(
        "badge", fontName="DV-Mono", fontSize=9, leading=11,
        textColor=TEXT_MUTED, spaceAfter=4*mm)))
    story.append(Paragraph("Skills Pack", styles["hero_title"]))
    story.append(Paragraph("8 skill-uri profesionale", ParagraphStyle(
        "hero_count", fontName="DV-Bold", fontSize=16,
        leading=20, textColor=TEXT_MUTED, spaceAfter=8*mm)))
    story.append(Paragraph(
        "Transform\u0103 Claude Code \u00eentr-un specialist pe finan\u021be, marketing, research, "
        "organizare, branding \u0219i generare de prompturi.", styles["hero_desc"]))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "Finan\u021be  \u00b7  Branding  \u00b7  Brainstorming  \u00b7  Marketing  \u00b7  Research  \u00b7  Organizare  \u00b7  Prompturi",
        ParagraphStyle("hero_tags", fontName="DV-Mono", fontSize=8, leading=11,
                       textColor=TEXT_MUTED, spaceAfter=2*mm)))
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("Webinar AI Accelerator \u00b7 2026", styles["footer"]))
    story.append(PageBreak())

    # ===== PAGE 2: INSTALARE =====
    story.append(Paragraph("CUM PORNE\u0218TI", styles["section_label"]))
    story.append(GradientBar(HexColor("#7c3aed"), HexColor("#2563eb"), width=30*mm, height=2.5))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Instalare", styles["section_title"]))
    story.append(Paragraph(
        "Trei moduri de a folosi skill-urile. \u00cencepe cu varianta 1 \u2014 e cea mai simpl\u0103.",
        styles["section_desc"]))

    install_data = [
        ("01", "Deschide \u00een VS Code \u0219i porne\u0219te Claude",
         "\u2714 Cel mai simplu",
         "Deschide <b>VS Code</b>, apoi <b>File \u2192 Open Folder</b> \u0219i selecteaz\u0103 folderul "
         "<b>skills-pack</b>. Deschide terminalul din VS Code (<b>Terminal \u2192 New Terminal</b>) "
         "\u0219i scrie comanda de mai jos. Skill-urile sunt detectate automat \u2014 gata, po\u021bi lucra!",
         "claude --dangerously-skip-permissions"),
        ("02", "Copiaz\u0103 skill-urile \u00een alt proiect", None,
         "Dac\u0103 vrei aceste skill-uri \u00eentr-un proiect existent: copiaz\u0103 folderul <b>.claude</b> "
         "(cu tot ce e \u00een el) din skills-pack \u0219i pune-l \u00een folderul proiectului t\u0103u. "
         "Data viitoare c\u00e2nd porne\u0219ti Claude acolo, le va detecta automat.",
         "Copiaz\u0103 folderul .claude/ \u00een proiectul t\u0103u"),
        ("03", "Instalare global\u0103 (peste tot)", None,
         "Ca s\u0103 ai skill-urile disponibile \u00een orice proiect: copiaz\u0103 folderele de skill-uri "
         "\u00een loca\u021bia global\u0103 Claude. Pe Windows: <b>C:\\Users\\NUMELE_TAU\\.claude\\skills\\</b>. "
         "Pe Mac/Linux: <b>~/.claude/skills/</b>.",
         "Windows: %USERPROFILE%\\.claude\\skills\\"),
    ]

    for num, title, badge_text, desc, code in install_data:
        elements = []
        badge_html = ""
        if badge_text:
            badge_html = f'  <font color="#059669" size="7">{badge_text}</font>'
        elements.append(Paragraph(
            f'<font color="#aaaaaa" size="20"><b>{num}</b></font>  {badge_html}',
            styles["card_body"]))
        elements.append(Spacer(1, 1*mm))
        elements.append(Paragraph(f"<b>{title}</b>", styles["card_title"]))
        elements.append(Paragraph(desc, styles["card_body"]))
        elements.append(Spacer(1, 1*mm))
        elements.append(Paragraph(
            f'<font face="DV-Mono" color="#333333" size="8">{code}</font>',
            styles["card_body"]))
        elements.append(Spacer(1, 5*mm))
        story.append(KeepTogether(elements))

    story.append(PageBreak())

    # ===== PAGES 3-4: SKILL-URI =====
    story.append(Paragraph("CAPABILIT\u0102\u021aI", styles["section_label"]))
    story.append(GradientBar(HexColor("#7c3aed"), HexColor("#2563eb"), width=30*mm, height=2.5))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Skill-uri incluse", styles["section_title"]))
    story.append(Paragraph(
        "Fiecare skill transform\u0103 Claude Code \u00eentr-un specialist. Activeaz\u0103-l cu o singur\u0103 propozi\u021bie.",
        styles["section_desc"]))

    card_w = (page_w - 5*mm) / 2
    for i in range(0, len(SKILLS), 2):
        if i == 4:
            story.append(PageBreak())
        row = []
        for j in [i, i + 1]:
            if j < len(SKILLS):
                sk = SKILLS[j]
                row.append(SkillCard(
                    sk["num"], sk["name"], sk["desc"], sk["prompt"], sk["tags"],
                    SKILL_COLORS[j], styles, card_width=card_w))
            else:
                row.append("")
        t = Table([row], colWidths=[card_w, card_w], spaceBefore=0, spaceAfter=4*mm)
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2.5*mm),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(t)

    story.append(PageBreak())

    # ===== LAST PAGE: TIPS =====
    story.append(Paragraph("WORKFLOW", styles["section_label"]))
    story.append(GradientBar(HexColor("#7c3aed"), HexColor("#2563eb"), width=30*mm, height=2.5))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Sfaturi de utilizare", styles["section_title"]))
    story.append(Paragraph(
        "Patru principii care fac diferen\u021ba \u00eentre rezultate mediocre \u0219i rezultate excelente.",
        styles["section_desc"]))

    for title, body in TIPS:
        elements = []
        elements.append(Paragraph(f"<b>{title}</b>", styles["tip_title"]))
        elements.append(Spacer(1, 1*mm))
        elements.append(Paragraph(body, styles["tip_body"]))
        elements.append(Spacer(1, 5*mm))
        story.append(KeepTogether(elements))

    story.append(Spacer(1, 15*mm))
    story.append(ColorBar(HexColor("#e4e4e7"), height=0.5))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Skills Pack \u2014 Claude Code", ParagraphStyle(
        "ft_brand", fontName="DV-Bold", fontSize=10,
        leading=13, textColor=TEXT_MUTED, alignment=TA_CENTER, spaceAfter=1*mm)))
    story.append(Paragraph("Webinar AI Accelerator \u00b7 2026", styles["footer"]))

    doc.build(story)
    print(f"PDF generat: {OUTPUT}")


if __name__ == "__main__":
    build()
