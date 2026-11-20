"""
Regenerates every SVG in ../assets   (run:  python tools/generate_assets.py)

Style: "aurora glass" - animated aurora light behind frosted-glass panels.
Every image paints its own dark background, so the profile never shows a white
panel (GitHub light theme included). Animations use SMIL + CSS, both of which
GitHub renders inside <img> tags. No external fonts, scripts or images.

Edit the CONFIG block, run the script, commit the new SVGs.
"""
import math, os, random, textwrap
from html import escape as E
from glass import *  # noqa: F401,F403  (helpers, colours, save, glass, chip ...)

# ============================== CONFIG ==============================
NAME = "Lalit Kumar Sharma"
INITIALS = "LS"
HEADLINE = "AI Engineer  ·  Generative AI Developer"
ROLES = ["AI Engineer", "Generative AI Developer", "AI Agent Builder",
         "RAG Systems Engineer", "Python Developer"]
HERO_TAGS = ["LLM Apps", "RAG", "AI Agents", "Automation"]

BIO = ("I build AI-powered software meant to be used: LLM applications, "
       "retrieval-augmented generation (RAG) systems, AI agents, and automation "
       "that connects to real databases and APIs. My work sits where models meet "
       "engineering: designing agent workflows, wiring LLMs to SQL and vector "
       "stores, serving everything through FastAPI, and packaging it with Docker.")

PROFILE = [("role", "AI Developer / AI Engineer"),
           ("builds", "LLM apps, RAG systems, AI agents, automation"),
           ("stack", "Python, FastAPI, LangChain, LangGraph"),
           ("data", "SQL databases + vector search"),
           ("ships", "Docker, REST APIs"),
           ("interest", "self-hosted and open-source AI models")]

PROJECTS = [  # (file, name, problem, stack, accent)
 ("hospital-agent", "Hospital AI Agent",
  "An agent that answers hospital information and routine queries from connected data.",
  ["LLM agents", "LangChain", "Databases"], "#22d3ee"),
 ("tryonai", "TryOnAI: Virtual Fashion Try-On",
  "See how clothing looks on you before you buy it.",
  ["Computer Vision", "Generative AI", "Python"], "#c084fc"),
 ("voice-assistant", "Personal Voice AI Assistant",
  "Hands-free help with everyday tasks through speech and LLMs.",
  ["Speech", "LLMs", "Python"], "#f472b6"),
 ("rag-knowledge", "RAG Knowledge Intelligence",
  "Ask questions across your own documents and get answers grounded in them.",
  ["RAG", "Vector DB", "LangChain", "LangGraph"], "#2dd4bf"),
 ("database-agent", "Database AI Agent",
  "Ask a database questions in plain English and let the agent work out the SQL.",
  ["LLMs", "SQL", "FastAPI"], "#818cf8"),
 ("ai-analytics", "AI Analytics Platform",
  "An AI layer on top of business data that explains what the numbers mean.",
  ["Python", "LLMs", "SQL"], "#fb923c"),
]

ARSENAL = [  # (label, accent, chips)
 ("AI / ML", "#22d3ee", ["Machine Learning", "Deep Learning", "NLP", "Computer Vision"]),
 ("Generative AI", "#c084fc", ["LLMs", "RAG", "Prompt Engineering", "AI Agents", "Multi-Agent Systems", "MCP"]),
 ("Frameworks", "#f472b6", ["LangChain", "LangGraph", "FastAPI", "Streamlit"]),
 ("Programming", "#2dd4bf", ["Python", "SQL", "JavaScript"]),
 ("Data", "#818cf8", ["Pandas", "NumPy", "Visualization"]),
 ("Databases", "#fb923c", ["PostgreSQL", "MySQL", "MariaDB", "SQL Server", "MongoDB", "Redis", "Vector Databases"]),
 ("Tools", "#22d3ee", ["Git", "GitHub", "Docker", "Linux", "REST APIs"]),
]

LAB = ["AI agents", "Advanced RAG pipelines", "LLM application architecture",
       "AI-powered analytics", "Self-hosted AI systems"]

SECTIONS = [("about", "About Me", "01"), ("arsenal", "AI Engineering Arsenal", "02"),
            ("projects", "Featured AI Projects", "03"), ("lab", "Current AI Lab", "04"),
            ("stats", "GitHub Statistics", "05"), ("snake", "Contribution Snake", "06"),
            ("connect", "Let's Connect", "07")]

BUTTONS = [("linkedin", "LinkedIn", "#38bdf8"), ("email", "Email", "#f472b6"),
           ("portfolio", "Portfolio", "#c084fc"), ("github", "GitHub", "#2dd4bf")]

QUOTE = "Models make predictions. Engineering makes them dependable."
QUOTE_SUB = "Built to run in production, not just in a notebook."
# ====================================================================


# ============================== HEADER ==============================
W, H = 1200, 470
hero_blobs = [(160, 90, 230, CYAN, 120, 60, 18), (1000, 140, 260, VIOLET, -140, 70, 22),
              (640, 470, 240, PINK, 100, -80, 20), (420, 260, 150, "#6366f1", -80, -50, 16)]

# typing roles (discrete width animation on a clip per role)
FS, CW, X0, YT = 22, 22 * 0.6, 112, 336
SLOT, TYPE, HOLD = 2.8, 1.2, 2.4
CYCLE = SLOT * len(ROLES)


def timeline(i, n):
    s = i * SLOT + 0.2
    pts = [(s + k * TYPE / n, k) for k in range(n + 1)]
    pts.append((s + HOLD, 0))
    return pts


def monotone(pts):
    clean = []
    for t, w in pts:
        if clean and t <= clean[-1][0]:
            t = clean[-1][0] + 1e-3
        clean.append((t, w))
    clean[0] = (0.0, clean[0][1])
    clean[-1] = (CYCLE, 0)
    return clean


clips, texts = "", ""
for i, r in enumerate(ROLES):
    n = len(r)
    c = monotone([(0.0, 0), (i * SLOT, 0)] + timeline(i, n) + [(CYCLE, 0)])
    kt = ";".join(f"{min(t/CYCLE,1):.4f}" for t, _ in c)
    vs = ";".join(f"{(w*CW + (CW*3 if w == n else 0)):.1f}" for _, w in c)
    clips += (f'<clipPath id="c{i}"><rect x="{X0}" y="{YT-26}" height="38" width="0">'
              f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" '
              f'keyTimes="{kt}" values="{vs}"/></rect></clipPath>')
    texts += f'<text x="{X0}" y="{YT}" font-size="{FS}" fill="url(#shimmer)" style="{MONO}" clip-path="url(#c{i})">{E(r)}</text>'
cp = [(0.0, 0)]
for i, r in enumerate(ROLES):
    cp += timeline(i, len(r))
cp = monotone(cp + [(CYCLE, 0)])
caret = (f'<rect y="{YT-20}" width="10" height="26" rx="2" fill="{CYAN}" filter="url(#glow)" x="{X0}">'
         f'<animate attributeName="x" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" '
         f'keyTimes="{";".join(f"{min(t/CYCLE,1):.4f}" for t,_ in cp)}" values="{";".join(f"{X0+w*CW+3:.1f}" for _,w in cp)}"/>'
         f'<animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.5" values="1;0"/></rect>')

# hero tag chips
tags, tx = "", 80
for j, t in enumerate(HERO_TAGS):
    s, w = chip(tx, 378, t, [CYAN, VIOLET, PINK, "#818cf8"][j % 4], fs=15, cls="f", delay=1.2 + j * .15)
    tags += s
    tx += w + 10

# orb (right side): glass sphere, orbit rings, neural core
OX, OY, OR = 960, 236, 172
orbits = ""
for k, (rx_, ry_, rot, col, dur) in enumerate([(205, 64, -18, CYAN, 9), (190, 58, 32, VIOLET, 12), (215, 52, 78, PINK, 15)]):
    p = f"M{OX-rx_} {OY}a{rx_} {ry_} 0 1 0 {2*rx_} 0a{rx_} {ry_} 0 1 0 {-2*rx_} 0"
    orbits += (f'<g transform="rotate({rot} {OX} {OY})"><path d="{p}" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="1.2"/>'
               f'<circle r="5.5" fill="{col}" filter="url(#glow)"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{p}"/></circle>'
               f'<circle r="3" fill="#fff" opacity=".8"><animateMotion dur="{dur}s" begin="-{dur/2}s" repeatCount="indefinite" path="{p}"/></circle></g>')
rnd = random.Random(3)
nodes = [(OX + 105 * math.cos(a * 0.6283), OY + 105 * math.sin(a * 0.6283)) for a in range(10)]
net = ""
for a in range(10):
    for b in (a + 3, a + 5):
        x1, y1 = nodes[a]; x2, y2 = nodes[b % 10]
        net += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"/>'
    x1, y1 = nodes[a]
    net += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{OX}" y2="{OY}"/>'
node_dots = "".join(
    f'<circle class="pulse" style="animation-delay:{i*.3:.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{[CYAN, VIOLET, PINK][i%3]}" filter="url(#glow)"/>'
    for i, (x, y) in enumerate(nodes))
signals = "".join(
    f'<circle r="2.6" fill="#fff"><animateMotion dur="{2.2+i*.35:.2f}s" begin="{i*.4:.1f}s" repeatCount="indefinite" '
    f'path="M{nodes[i][0]:.0f} {nodes[i][1]:.0f}L{OX} {OY}"/><animate attributeName="opacity" values="0;1;0" '
    f'dur="{2.2+i*.35:.2f}s" begin="{i*.4:.1f}s" repeatCount="indefinite"/></circle>' for i in range(0, 10, 2))

header = svg_open(W, H, f"{NAME} - {HEADLINE}. Roles: {', '.join(ROLES)}") + defs(W, H, hero_blobs, corners=(26, 26, 0, 0)) + f'''
<defs>{clips}
<radialGradient id="core"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="{CYAN}"/><stop offset=".7" stop-color="{VIOLET}" stop-opacity=".5"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="orbHL" cx=".32" cy=".25" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
</defs>
{background(W, H)}
<g clip-path="url(#page)">{particles(W, H, 34, 11)}</g>
{glass(f'<rect x="40" y="40" width="700" height="390" rx="28"', W, H, sweep_dur=9)}
{comet(rrect_path(40, 40, 700, 390, 28), CYAN, dur=10, length=90)}
<g class="f" style="animation-delay:.1s">
<rect x="80" y="82" width="272" height="34" rx="17" fill="#22c55e" fill-opacity=".10" stroke="#22c55e" stroke-opacity=".5"/>
<circle class="pulse" cx="100" cy="99" r="5" fill="#22c55e" filter="url(#glow)"/>
<text x="114" y="104.5" font-size="14" fill="#bbf7d0" style="{MONO}">online · building AI systems</text></g>
<text class="f" style="animation-delay:.3s;{SANS}" x="80" y="168" font-size="24" fill="{MUTED}">Hi there, I'm</text>
<text class="f" style="animation-delay:.5s;{SANS}" x="78" y="232" font-size="56" font-weight="800" letter-spacing="-.5" fill="url(#shimmer)">{E(NAME)}</text>
<text class="f" style="animation-delay:.7s;{SANS}" x="80" y="278" font-size="21" fill="{TEXT}" fill-opacity=".9">{E(HEADLINE)}</text>
<g class="f" style="animation-delay:.9s">
<rect x="80" y="304" width="620" height="46" rx="12" fill="#000" fill-opacity=".28" stroke="#fff" stroke-opacity=".08"/>
<text x="96" y="{YT}" font-size="{FS}" fill="{DIM}" style="{MONO}">&gt;</text>{texts}{caret}</g>
{tags}
<circle cx="{OX}" cy="{OY}" r="{OR+40}" fill="{VIOLET}" fill-opacity=".10" filter="url(#soft)"/>
{glass(f'<circle cx="{OX}" cy="{OY}" r="{OR}"', W, H, sweep_dur=7, sweep_begin=2, strength=.8)}
<circle cx="{OX}" cy="{OY}" r="{OR}" fill="url(#orbHL)"/>
<g stroke="#fff" stroke-opacity=".10">{net}</g>
<g>{node_dots}</g>{signals}
<circle cx="{OX}" cy="{OY}" r="46" fill="url(#core)"><animate attributeName="r" values="42;54;42" dur="3.2s" repeatCount="indefinite"/></circle>
<g><animateTransform attributeName="transform" type="rotate" from="0 {OX} {OY}" to="360 {OX} {OY}" dur="40s" repeatCount="indefinite"/>
<circle cx="{OX}" cy="{OY}" r="{OR-14}" fill="none" stroke="url(#acc)" stroke-opacity=".5" stroke-dasharray="2 10"/></g>
<text x="{OX}" y="{OY+11}" font-size="30" font-weight="800" fill="#0b0820" text-anchor="middle" style="{SANS}">AI</text>
{orbits}
<text x="1160" y="452" font-size="13" fill="{DIM}" text-anchor="end" style="{MONO}">github.com/Lalit-sharma123</text>
</svg>'''
save("header.svg", header)

# ========================== SECTION HEADERS ==========================
for key, title, num in SECTIONS:
    W, H = 1200, 104
    reset_ids()
    b = [(120, 50, 140, CYAN, 160, 10, 14), (700, 60, 160, VIOLET, -180, 0, 17), (1100, 40, 130, PINK, -80, 10, 12)]
    pw = 1120
    tline = 140 + tw(title, 30, .56)
    save(f"sec-{key}.svg", svg_open(W, H, title) + defs(W, H, b) + f'''
{background(W, H)}
{glass(f'<rect x="40" y="16" width="{pw}" height="72" rx="22"', W, H, sweep_dur=6, sweep_begin=int(num) * .6, shadow=False)}
{comet(rrect_path(40, 16, pw, 72, 22), CYAN, dur=8, length=70, begin=-int(num))}
<circle cx="88" cy="52" r="22" fill="url(#acc)" fill-opacity=".18" stroke="url(#acc)" stroke-opacity=".7"/>
<text x="88" y="58" font-size="16" font-weight="700" fill="{TEXT}" text-anchor="middle" style="{MONO}">{num}</text>
<text x="128" y="62" font-size="30" font-weight="800" fill="{TEXT}" style="{SANS}">{E(title)}</text>
<rect x="{tline:.0f}" y="51" width="{max(0, 1000 - tline):.0f}" height="1.5" fill="url(#acc)" opacity=".35"/>
<circle cy="51.75" r="3" fill="#fff" filter="url(#glow)"><animate attributeName="cx" values="{tline:.0f};1000" dur="3.5s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;1;0" dur="3.5s" repeatCount="indefinite"/></circle>
<text x="1136" y="57" font-size="14" fill="{MUTED}" text-anchor="end" style="{MONO}">~/{key}</text>
</svg>''')

# =============================== ABOUT ===============================
W = 1200
reset_ids()
bio_lines = textwrap.wrap(BIO, 74)
bio_y0 = 108
card_y = bio_y0 + len(bio_lines) * 31 + 22
card_h = 76 + len(PROFILE) * 34
H = card_y + card_h + 60
b = [(200, 160, 200, CYAN, 80, 80, 16), (900, 120, 230, VIOLET, -120, 60, 20), (700, H, 220, PINK, 90, -60, 18)]
bio = "".join(f'<text class="f" style="animation-delay:{.2+i*.08:.2f}s;{SANS}" x="384" y="{bio_y0+i*31}" font-size="19" fill="{TEXT}" fill-opacity=".88">{E(l)}</text>'
              for i, l in enumerate(bio_lines))
rows = ""
for i, (k, v) in enumerate(PROFILE):
    y = card_y + 72 + i * 34
    rows += (f'<g class="f" style="animation-delay:{.9+i*.12:.2f}s"><text x="410" y="{y}" font-size="16" fill="{DIM}" style="{MONO}">{i+1:02d}</text>'
             f'<text x="452" y="{y}" font-size="16" fill="#c084fc" style="{MONO}">{E(k)}<tspan fill="{DIM}">:</tspan></text>'
             f'<text x="572" y="{y}" font-size="16" fill="#e2e8f0" style="{MONO}">{E(v)}</text></g>')
AX, AY = 210, 150
about = svg_open(W, H, f"About {NAME}. {BIO} " + "; ".join(f"{k}: {v}" for k, v in PROFILE)) + defs(W, H, b) + f'''
<defs><linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>
{background(W, H)}
{glass(f'<rect x="40" y="24" width="1120" height="{H-48}" rx="28"', W, H, sweep_dur=10)}
<circle cx="{AX}" cy="{AY}" r="112" fill="{VIOLET}" fill-opacity=".25" filter="url(#soft)"/>
{glass(f'<circle cx="{AX}" cy="{AY}" r="92"', W, H, sweep=False, strength=.9, shadow=False)}
<g><animateTransform attributeName="transform" type="rotate" from="0 {AX} {AY}" to="360 {AX} {AY}" dur="8s" repeatCount="indefinite"/>
<circle cx="{AX}" cy="{AY}" r="102" fill="none" stroke="url(#ring)" stroke-width="4" stroke-linecap="round" stroke-dasharray="220 420" filter="url(#glow)"/></g>
<g><animateTransform attributeName="transform" type="rotate" from="360 {AX} {AY}" to="0 {AX} {AY}" dur="14s" repeatCount="indefinite"/>
<circle cx="{AX}" cy="{AY}" r="114" fill="none" stroke="#fff" stroke-opacity=".25" stroke-dasharray="1 9"/></g>
<text x="{AX}" y="{AY+22}" font-size="62" font-weight="800" fill="url(#shimmer)" text-anchor="middle" style="{SANS}">{E(INITIALS)}</text>
<text x="{AX}" y="{AY+150}" font-size="22" font-weight="700" fill="{TEXT}" text-anchor="middle" style="{SANS}">{E(NAME)}</text>
<text x="{AX}" y="{AY+178}" font-size="15" fill="{MUTED}" text-anchor="middle" style="{SANS}">AI Engineer</text>
<g class="f" style="animation-delay:.4s"><rect x="{AX-100}" y="{AY+196}" width="200" height="32" rx="16" fill="#22c55e" fill-opacity=".1" stroke="#22c55e" stroke-opacity=".45"/>
<circle class="pulse" cx="{AX-82}" cy="{AY+212}" r="4.5" fill="#22c55e" filter="url(#glow)"/>
<text x="{AX-70}" y="{AY+217}" font-size="13.5" fill="#bbf7d0" style="{MONO}">open to collaborate</text></g>
<rect x="352" y="64" width="1" height="{H-128}" fill="url(#acc)" opacity=".35"/>
<text x="384" y="74" font-size="15" fill="{CYAN}" style="{MONO}">$ cat about.md</text>
{bio}
{glass(f'<rect x="384" y="{card_y}" width="740" height="{card_h}" rx="18"', W, H, sweep=False, strength=.4, shadow=False)}
<circle cx="408" cy="{card_y+24}" r="6" fill="#ff5f57"/><circle cx="428" cy="{card_y+24}" r="6" fill="#febc2e"/><circle cx="448" cy="{card_y+24}" r="6" fill="#28c840"/>
<text x="754" y="{card_y+29}" font-size="13" fill="{MUTED}" text-anchor="middle" style="{MONO}">profile.yml</text>
<rect x="384" y="{card_y+42}" width="740" height="1" fill="#fff" fill-opacity=".08"/>
{rows}
</svg>'''
save("about.svg", about)

# ============================== ARSENAL ==============================
W = 1200
reset_ids()
LX, MAXX, y = 300, 1120, 64
body, d = "", 0.15
for label, col, chips in ARSENAL:
    x = LX
    row_top = y
    body += (f'<g class="f" style="animation-delay:{d:.2f}s"><rect x="76" y="{y}" width="196" height="38" rx="12" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>'
             f'<rect x="76" y="{y}" width="4" height="38" rx="2" fill="{col}" filter="url(#glow)"/>'
             f'<text x="96" y="{y+25}" font-size="16" font-weight="700" fill="{TEXT}" style="{SANS}">{E(label)}</text></g>')
    for c in chips:
        w = tw(c, 15, .58) + 34
        if x + w > MAXX:
            x, y = LX, y + 46
        d += .05
        s, w = chip(x, y + 2, c, col, cls="f", delay=d)
        body += s
        x += w + 10
    y += 46 + 14
    body += f'<rect x="76" y="{y-8}" width="1044" height="1" fill="#fff" fill-opacity=".06"/>'
    d += .1
H = y + 44
b = [(150, 100, 220, CYAN, 140, 80, 18), (1050, H / 2, 240, VIOLET, -150, 40, 22), (600, H, 220, PINK, 80, -70, 16)]
save("arsenal.svg", svg_open(W, H, "Technologies: " + "; ".join(f"{l}: {', '.join(c)}" for l, _, c in ARSENAL))
     + defs(W, H, b) + f'''
{background(W, H)}
{glass(f'<rect x="40" y="24" width="1120" height="{H-48}" rx="28"', W, H, sweep_dur=9)}
{comet(rrect_path(40, 24, 1120, H - 48, 28), VIOLET, dur=12, length=80)}
{body}
</svg>''')

# ============================ PROJECT CARDS ===========================
for idx, (fid, name, problem, stack, col) in enumerate(PROJECTS, 1):
    reset_ids()
    W, H = 600, 360
    b = [(80, 60, 170, col, 90, 50, 14 + idx), (560, 330, 170, VIOLET, -90, -40, 17 + idx), (420, 40, 110, PINK, -40, 40, 12)]
    wrapped = textwrap.wrap(problem, 50)[:3]
    prob = "".join(f'<text class="f" style="animation-delay:{.3+i*.1:.1f}s;{SANS}" x="48" y="{170+i*27}" font-size="17" fill="{MUTED}">{E(l)}</text>'
                   for i, l in enumerate(wrapped))
    x, cy, chips_s = 48, 262, ""
    for j, s in enumerate(stack):
        w = tw(s, 13.5, .58) + 34
        if x + w > 552:
            x, cy = 48, cy + 38
        cs, w = chip(x, cy, s, col, fs=13.5, h=30, cls="f", delay=.6 + j * .1)
        chips_s += cs
        x += w + 8
    title = name if len(name) <= 34 else name[:33] + "…"
    card = rrect_path(16, 16, 568, 328, 24)
    save(f"card-{fid}.svg", svg_open(W, H, f"{name}: {problem} Stack: {', '.join(stack)}") + defs(W, H, b) + f'''
{background(W, H, hfade=True)}
{glass(f'<path d="{card}"', W, H, sweep_dur=7, sweep_begin=idx * .8, tint=col, strength=.5)}
<path d="{card}" fill="none" stroke="{col}" stroke-opacity=".25" stroke-width="1.2"/>
{comet(card, col, dur=6 + idx * .4, length=150, width=2.6, begin=-idx)}
<circle cx="78" cy="78" r="28" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".6"/>
<circle cx="78" cy="78" r="28" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="30 146" filter="url(#glow)">
<animateTransform attributeName="transform" type="rotate" from="0 78 78" to="360 78 78" dur="4s" repeatCount="indefinite"/></circle>
<text x="78" y="85" font-size="19" font-weight="700" fill="{TEXT}" text-anchor="middle" style="{MONO}">{idx:02d}</text>
<text x="544" y="70" font-size="12.5" fill="{col}" text-anchor="end" letter-spacing="2" style="{MONO}">AI PROJECT</text>
<circle class="pulse" cx="544" cy="88" r="4" fill="{col}" filter="url(#glow)"/>
<text class="f" style="animation-delay:.15s;{SANS}" x="48" y="138" font-size="25" font-weight="800" fill="{TEXT}">{E(title)}</text>
{prob}{chips_s}
<g><text x="552" y="{H-38}" font-size="14" fill="{col}" text-anchor="end" style="{SANS}" font-weight="600">View repository</text>
<text x="568" y="{H-38}" font-size="15" fill="{col}" text-anchor="end" style="{SANS}">→<animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur="1.6s" repeatCount="indefinite"/></text></g>
</svg>''')

# ================================ LAB ================================
W = 1200
reset_ids()
H = 160 + len(LAB) * 52 + 110
b = [(220, 120, 220, CYAN, 120, 60, 18), (1000, H - 80, 240, VIOLET, -130, -40, 21), (650, 40, 160, PINK, 90, 60, 15)]
lines = (f'<text class="f" style="animation-delay:.2s;{MONO}" x="84" y="138" font-size="18" fill="{MUTED}"><tspan fill="{CYAN}">❯</tspan> ai-lab --status --watch</text>'
         f'<text class="f" style="animation-delay:.7s;{MONO}" x="84" y="180" font-size="15" fill="{PINK}" letter-spacing="3" font-weight="700">CURRENTLY BUILDING</text>')
for i, item in enumerate(LAB):
    y = 226 + i * 52
    dly = 1.1 + i * .35
    col = [CYAN, VIOLET, PINK, "#818cf8", "#2dd4bf"][i % 5]
    lines += (f'<g class="f" style="animation-delay:{dly:.2f}s">'
              f'<circle cx="94" cy="{y-6}" r="5" fill="{col}" filter="url(#glow)"/>'
              f'<text x="114" y="{y}" font-size="19" fill="{TEXT}" style="{MONO}">{E(item)}</text>'
              f'<rect x="700" y="{y-12}" width="380" height="10" rx="5" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".06"/>'
              f'<clipPath id="lb{i}"><rect x="700" y="{y-12}" width="380" height="10" rx="5"/></clipPath>'
              f'<g clip-path="url(#lb{i})"><rect y="{y-12}" width="140" height="10" rx="5" fill="{col}" filter="url(#glow)">'
              f'<animate attributeName="x" values="560;1080" dur="{2.4+i*.3:.1f}s" repeatCount="indefinite"/></rect></g>'
              f'<text x="1120" y="{y-2}" font-size="12" fill="{DIM}" text-anchor="end" style="{MONO}" class="pulse">wip</text></g>')
lines += f'<text class="blink" x="84" y="{226+len(LAB)*52-6}" font-size="20" fill="{CYAN}" style="{MONO}">▋</text>'
save("lab-terminal.svg", svg_open(W, H, "Currently building: " + ", ".join(LAB)) + defs(W, H, b) + f'''
{background(W, H)}
{glass(f'<rect x="40" y="24" width="1120" height="{H-48}" rx="24"', W, H, sweep_dur=8)}
{comet(rrect_path(40, 24, 1120, H - 48, 24), CYAN, dur=11, length=70)}
<path d="M40 76V48a24 24 0 0 1 24-24h1072a24 24 0 0 1 24 24v28z" fill="#fff" fill-opacity=".04"/>
<rect x="40" y="76" width="1120" height="1" fill="#fff" fill-opacity=".1"/>
<circle cx="72" cy="50" r="7" fill="#ff5f57"/><circle cx="96" cy="50" r="7" fill="#febc2e"/><circle cx="120" cy="50" r="7" fill="#28c840"/>
<text x="600" y="55" font-size="14" fill="{MUTED}" text-anchor="middle" style="{MONO}">ai-lab — ~/current-work</text>
<circle class="pulse" cx="1092" cy="50" r="5" fill="#22c55e" filter="url(#glow)"/><text x="1104" y="55" font-size="13" fill="#86efac" style="{MONO}">live</text>
{lines}
</svg>''')

# ============================== FOOTER ==============================
W, H = 1200, 240
reset_ids()
b = [(150, 120, 200, CYAN, 160, 30, 16), (600, 200, 220, VIOLET, -100, -40, 19), (1050, 80, 200, PINK, -150, 40, 17)]
wave = "M80 186H420l14-16 14 32 18-52 16 44 12-20 10 12H1120"
save("footer.svg", svg_open(W, H, QUOTE) + defs(W, H, b, corners=(0, 0, 26, 26)) + f'''
{background(W, H)}
<g clip-path="url(#page)">{particles(W, H, 22, 5)}</g>
{glass(f'<rect x="40" y="24" width="1120" height="{H-48}" rx="28"', W, H, sweep_dur=8)}
<text class="f" x="600" y="86" font-size="27" font-weight="700" fill="url(#shimmer)" text-anchor="middle" style="{SANS}">{E(QUOTE)}</text>
<text class="f" style="animation-delay:.3s;{MONO}" x="600" y="118" font-size="15" fill="{MUTED}" text-anchor="middle">{E(QUOTE_SUB)}</text>
<path d="{wave}" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="2"/>
{comet(wave, CYAN, dur=4, length=160, width=3)}
{comet(wave, PINK, dur=4, length=60, width=3, begin=-2)}
<text x="1120" y="208" font-size="12" fill="{DIM}" text-anchor="end" style="{MONO}">thanks for visiting ✦</text>
</svg>''')

# ========================== CONNECT BUTTONS ==========================
ICONS = {
    "linkedin": lambda c: f'<rect x="-13" y="-13" width="26" height="26" rx="6" fill="none" stroke="{c}" stroke-width="2.2"/><text x="0" y="6" font-size="15" font-weight="800" fill="{c}" text-anchor="middle" style="{SANS}">in</text>',
    "email": lambda c: f'<rect x="-14" y="-10" width="28" height="20" rx="4" fill="none" stroke="{c}" stroke-width="2.2"/><path d="M-13 -8l13 10 13-10" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round"/>',
    "portfolio": lambda c: f'<circle r="13" fill="none" stroke="{c}" stroke-width="2.2"/><ellipse rx="6" ry="13" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M-13 0h26" stroke="{c}" stroke-width="1.8"/>',
    "github": lambda c: f'<text x="0" y="5" font-size="15" font-weight="800" fill="{c}" text-anchor="middle" style="{MONO}">&lt;/&gt;</text>',
}
for i, (key, label, col) in enumerate(BUTTONS):
    reset_ids()
    W, H = 300, 96
    b = [(50, 48, 80, col, 130, 0, 6 + i), (250, 48, 80, VIOLET, -130, 0, 8 + i)]
    save(f"btn-{key}.svg", svg_open(W, H, label) + defs(W, H, b) + f'''
{background(W, H, dots=False, hfade=True)}
{glass(f'<rect x="16" y="16" width="268" height="64" rx="18"', W, H, sweep_dur=5, sweep_begin=i * .7, tint=col, shadow=False)}
{comet(rrect_path(16, 16, 268, 64, 18), col, dur=5, length=120, begin=-i)}
<circle cx="56" cy="48" r="22" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>
<g transform="translate(56 48)" filter="url(#glow)">{ICONS[key](col)}</g>
<text x="92" y="55" font-size="19" font-weight="700" fill="{TEXT}" style="{SANS}">{E(label)}</text>
<text x="258" y="55" font-size="18" fill="{col}" text-anchor="end" style="{SANS}">↗<animateTransform attributeName="transform" type="translate" values="0 0;3 -3;0 0" dur="1.8s" repeatCount="indefinite"/></text>
</svg>''')

# remove assets from the previous design that are no longer used
for old in ("about-card.svg",):
    p = os.path.join(OUT, old)
    if os.path.exists(p):
        os.remove(p)
print("assets written:", sorted(os.listdir(OUT)))
