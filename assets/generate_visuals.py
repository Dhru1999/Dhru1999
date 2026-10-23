"""Generate the journey map and project cards (light + dark) for the profile README.

Edit STOPS (journey) or CARDS (projects) below, then run from the repo root:
    python assets/generate_visuals.py assets
No dependencies beyond the Python standard library.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(sys.argv[1])
(OUT / "cards").mkdir(parents=True, exist_ok=True)

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "light": dict(bg="#ffffff", text="#1f2328", muted="#59636e", track="#d0d7de", card="#f6f8fa",
                  border="#d0d7de", edu="#0969da", work="#bf8700", data="#1a7f37", ai="#8250df", flight="#8c959f"),
    "dark":  dict(bg="#0d1117", text="#e6edf3", muted="#9198a1", track="#3d444d", card="#151b23",
                  border="#3d444d", edu="#4493f8", work="#d29922", data="#3fb950", ai="#ab7df8", flight="#6e7681"),
}

# ── Journey map ──────────────────────────────────────────────────────────
W, H = 920, 470
Y1, Y2, Y3 = 96, 236, 376
R = 70  # turn radius

SEGMENTS = [  # (path, colour key, dashed)
    (f"M90 {Y1} H490", "edu", False),
    (f"M490 {Y1} H800 A{R} {R} 0 0 1 800 {Y2} H640", "work", False),
    (f"M640 {Y2} H470", "flight", True),
    (f"M470 {Y2} H100 A{R} {R} 0 0 0 100 {Y3} H245", "data", False),
    (f"M245 {Y3} H840", "ai", False),
    (f"M840 {Y3} H900", "ai", True),
]
FULL_ROUTE = f"M90 {Y1} H800 A{R} {R} 0 0 1 800 {Y2} H100 A{R} {R} 0 0 0 100 {Y3} H840"

# (x, y, top label, title, subtitle, colour, kind, anchor)
STOPS = [
    (90,  Y1, "the start",      "Surat, India",      "where I learned to code",  "edu",  "city", "middle"),
    (250, Y1, "2017 – 2020",    "B.Sc.",             "Computer Applications",    "edu",  "stop", "middle"),
    (410, Y1, "2020 – 2022",    "M.Sc.",             "Computer Applications",    "edu",  "stop", "middle"),
    (570, Y1, "2022",           "Casepoint",         "intern, led 10 interns",   "work", "stop", "middle"),
    (730, Y1, "2022 – 2024",    "Software Engineer", "10+ GB of documents a day","work", "stop", "middle"),
    (720, Y2, "Oct 2023",       "Excellence Award",  "Casepoint",                "work", "stop", "middle"),
    (450, Y2, "new chapter",    "Hamburg",           "new city, new language",   "data", "city", "middle"),
    (250, Y2, "2026",           "ReDI School",       "Data Analytics",           "data", "stop", "middle"),
    (160, Y3, "Jun 2026",       "Solar map",         "384,908 buildings",        "data", "stop", "middle"),
    (330, Y3, "Jun 2026",       "Follow-up tool",    "C# + Claude API",          "ai",   "stop", "middle"),
    (500, Y3, "Jul 2026",       "Retail ETL",        "no row lost quietly",      "data", "stop", "middle"),
    (670, Y3, "Oct 2026",       "First ML model",    "test R² 0.88",             "ai",   "stop", "middle"),
    (840, Y3, "now",            "AI / ML",           "learning in public",       "ai",   "now",  "end"),
]


def journey(t):
    c = THEMES[t]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'role="img" aria-labelledby="t d">',
           '<title id="t">Dhrupti\'s journey</title>',
           '<desc id="d">A route map from Surat, India (B.Sc. and M.Sc. in Computer Applications) through '
           'Casepoint (intern, software engineer, Excellence Award 2023) to Hamburg (ReDI School data analytics, '
           'a solar map of 384,908 buildings, a C# follow-up tool using the Claude API, a retail ETL pipeline, '
           'a first ML model) and now AI/ML.</desc>',
           f'<style>text{{font-family:{FONT};}} .yr{{font-size:11px;fill:{c["muted"]};letter-spacing:.04em;text-transform:uppercase}}'
           f' .ti{{font-size:14px;font-weight:600;fill:{c["text"]}}} .su{{font-size:11.5px;fill:{c["muted"]}}}'
           f' .city{{font-size:15.5px;font-weight:700}} .lg{{font-size:11.5px;fill:{c["muted"]}}}'
           ' @media (prefers-reduced-motion: reduce){.anim{display:none}}</style>']

    # legend
    lx = 24
    for key, label in [("edu", "studies"), ("work", "Casepoint"), ("data", "data"), ("ai", "AI & LLMs")]:
        out.append(f'<rect x="{lx:.0f}" y="16" width="18" height="6" rx="3" fill="{c[key]}"/>'
                   f'<text class="lg" x="{lx + 24:.0f}" y="23">{esc(label)}</text>')
        lx += 24 + len(label) * 6.6 + 22

    # base track + coloured chapters
    out.append(f'<path d="{FULL_ROUTE}" fill="none" stroke="{c["track"]}" stroke-width="10" stroke-linecap="round" opacity=".45"/>')
    for d, key, dashed in SEGMENTS:
        dash = ' stroke-dasharray="2 12"' if dashed else ""
        width = 4 if dashed else 6
        out.append(f'<path d="{d}" fill="none" stroke="{c[key]}" stroke-width="{width}" stroke-linecap="round"{dash}/>')
    # plane on the flight segment
    out.append(f'<text x="555" y="{Y2 + 6}" text-anchor="middle" font-size="18" fill="{c["flight"]}">✈</text>'
               .replace("✈", "&#9992;"))

    # travelling light
    out.append(f'<circle class="anim" r="5" fill="{c["text"]}" opacity=".85">'
               f'<animateMotion dur="16s" repeatCount="indefinite" path="{FULL_ROUTE}"/></circle>')

    for x, y, yr, title, sub, key, kind, anchor in STOPS:
        col = c[key]
        if kind == "city":
            out.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{c["bg"]}" stroke="{col}" stroke-width="5"/>'
                       f'<circle cx="{x}" cy="{y}" r="4" fill="{col}"/>')
        elif kind == "now":
            out.append(f'<circle class="anim" cx="{x}" cy="{y}" r="11" fill="none" stroke="{col}" stroke-width="2">'
                       '<animate attributeName="r" values="11;24" dur="2s" repeatCount="indefinite"/>'
                       '<animate attributeName="opacity" values=".9;0" dur="2s" repeatCount="indefinite"/></circle>'
                       f'<circle cx="{x}" cy="{y}" r="11" fill="{col}"/>'
                       f'<circle cx="{x}" cy="{y}" r="4" fill="{c["bg"]}"/>')
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{c["bg"]}" stroke="{col}" stroke-width="4"/>')
        tx = x if anchor == "middle" else x + 12
        title_cls = "ti city" if kind == "city" else "ti"
        out.append(f'<text class="yr" x="{tx}" y="{y - 20}" text-anchor="{anchor}">{esc(yr)}</text>')
        out.append(f'<text class="{title_cls}" x="{tx}" y="{y + 32}" text-anchor="{anchor}">{esc(title)}</text>')
        out.append(f'<text class="su" x="{tx}" y="{y + 49}" text-anchor="{anchor}">{esc(sub)}</text>')

    out.append("</svg>")
    return "\n".join(out)


# ── Project cards ────────────────────────────────────────────────────────
CW, CH = 440, 226
CARDS = [
    dict(slug="solar", key="data", kicker="GEOSPATIAL · TEAM PROJECT", date="Jun 2026",
         title="Rooftop Solar, Hamburg", metric="384,908", metric_sub=["buildings joined", "to 104 districts"],
         lines=["Where does Hamburg's rooftop solar", "capacity sit? A spatial join of the", "city's open data, district by district."],
         lesson="Check what a join drops, not only what it keeps.",
         tags=["Python", "GeoPandas", "Looker Studio"]),
    dict(slug="followup", key="ai", kicker="C# · LLM TOOL", date="Jun 2026",
         title="Follow-Up Assistant", metric="0", metric_sub=["emails sent", "without review"],
         lines=["Reads an Excel job tracker, finds", "who is due a follow-up, and drafts", "the email with the Claude API."],
         lesson="An .xlsm file is just a zip of XML.",
         tags=["C#", ".NET 9", "Claude API", "xUnit"]),
    dict(slug="etl", key="data", kicker="DATA ENGINEERING", date="Jul 2026",
         title="Smart Retail ETL", metric="14 + 3", metric_sub=["loaded + quarantined", "= all 17 rows in"],
         lines=["A pipeline built around one rule:", "no row disappears quietly. Every", "reject is saved with its reason."],
         lesson="Silent success is worse than a loud crash.",
         tags=["Python", "pandas", "PostgreSQL", "pytest"]),
    dict(slug="ml", key="ai", kicker="MACHINE LEARNING", date="Oct 2026",
         title="Mental Health Signal", metric="0.88", metric_sub=["R² on held-out", "test data"],
         lines=["My first model behind an API: a", "scikit-learn pipeline served with", "FastAPI. A learning project."],
         lesson="Train 0.98 vs test 0.88: the gap is the story.",
         tags=["scikit-learn", "FastAPI", "JavaScript"]),
]


def card(cd, t):
    c = THEMES[t]
    col = c[cd["key"]]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" role="img" '
           f'aria-label="{esc(cd["title"])}: {esc(" ".join(cd["lines"]))}">',
           f'<style>text{{font-family:{FONT};}}</style>',
           f'<rect x="1" y="1" width="{CW - 2}" height="{CH - 2}" rx="12" fill="{c["card"]}" stroke="{c["border"]}"/>',
           f'<rect x="1" y="1" width="6" height="{CH - 2}" rx="3" fill="{col}"/>',
           f'<text x="24" y="32" font-size="10.5" font-weight="700" letter-spacing=".08em" fill="{col}">{esc(cd["kicker"])}</text>',
           f'<text x="{CW - 20}" y="32" font-size="11" text-anchor="end" fill="{c["muted"]}">{esc(cd["date"])}</text>',
           f'<text x="24" y="60" font-size="20" font-weight="700" fill="{c["text"]}">{esc(cd["title"])}</text>']
    for i, line in enumerate(cd["lines"]):
        out.append(f'<text x="24" y="{88 + i * 18}" font-size="12.5" fill="{c["muted"]}">{esc(line)}</text>')
    # metric block on the right
    mx = CW - 24
    out.append(f'<text x="{mx}" y="104" font-size="30" font-weight="800" text-anchor="end" fill="{col}">{esc(cd["metric"])}</text>')
    for i, s in enumerate(cd["metric_sub"]):
        out.append(f'<text x="{mx}" y="{122 + i * 14}" font-size="10.5" text-anchor="end" fill="{c["muted"]}">{esc(s)}</text>')
    # lesson
    out.append(f'<line x1="24" y1="158" x2="{CW - 24}" y2="158" stroke="{c["border"]}"/>')
    out.append(f'<text x="24" y="178" font-size="12" font-style="italic" fill="{c["text"]}">'
               f'<tspan font-weight="700" font-style="normal" fill="{col}">Lesson </tspan>{esc(cd["lesson"])}</text>')
    # tags
    x = 24
    for tag in cd["tags"]:
        w = len(tag) * 6.4 + 16
        out.append(f'<rect x="{x}" y="192" width="{w:.0f}" height="20" rx="10" fill="none" stroke="{c["border"]}"/>'
                   f'<text x="{x + w / 2:.0f}" y="206" font-size="11" text-anchor="middle" fill="{c["muted"]}" '
                   f'font-family="{MONO}">{esc(tag)}</text>')
        x += w + 6
    out.append("</svg>")
    return "\n".join(out)


for theme in THEMES:
    (OUT / f"journey-{theme}.svg").write_text(journey(theme), encoding="utf-8")
    for cd in CARDS:
        (OUT / "cards" / f"{cd['slug']}-{theme}.svg").write_text(card(cd, theme), encoding="utf-8")
print("wrote", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*.svg")))
