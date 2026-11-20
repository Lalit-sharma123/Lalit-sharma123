"""
Regenerates every SVG in ../assets  (run:  python tools/generate_assets.py)
Edit the CONFIG block below, run it, then commit the new SVGs. Optional: the SVGs
can also be edited by hand in any text editor.
"""
import os, textwrap
from html import escape as E

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

# ----------------------------- CONFIG -----------------------------
ROLES = ["AI Engineer", "Generative AI Developer", "AI Agent Builder",
         "RAG Systems Engineer", "Python Developer"]

PROJECTS = [  # (file, name, problem, stack, accent)
 ("hospital-agent", "Hospital AI Agent",
  "An agent that answers hospital information and routine queries from connected data.",
  ["LLM agents", "LangChain", "Databases"], "#00f5d4"),
 ("tryonai", "TryOnAI: Virtual Fashion Try-On",
  "See how clothing looks on you before you buy it.",
  ["Computer Vision", "Generative AI", "Python"], "#9d4edd"),
 ("voice-assistant", "Personal Voice AI Assistant",
  "Hands-free help with everyday tasks through speech and LLMs.",
  ["Speech", "LLMs", "Python"], "#39ff14"),
 ("rag-knowledge", "RAG Knowledge Intelligence",
  "Ask questions across your own documents and get answers grounded in them.",
  ["RAG", "Vector DB", "LangChain", "LangGraph"], "#00f5d4"),
 ("database-agent", "Database AI Agent",
  "Ask a database questions in plain English and let the agent work out the SQL.",
  ["LLMs", "SQL", "FastAPI"], "#9d4edd"),
 ("ai-analytics", "AI Analytics Platform",
  "An AI layer on top of business data that explains what the numbers mean.",
  ["Python", "LLMs", "SQL"], "#39ff14"),
]

ARSENAL = [  # (label, accent, chips)
 ("AI / ML", "#00f5d4", ["Machine Learning", "Deep Learning", "NLP", "Computer Vision"]),
 ("Generative AI", "#9d4edd", ["LLMs", "RAG", "Prompt Engineering", "AI Agents", "Multi-Agent Systems", "MCP"]),
 ("Frameworks", "#39ff14", ["LangChain", "LangGraph", "FastAPI", "Streamlit"]),
 ("Programming", "#00f5d4", ["Python", "SQL", "JavaScript"]),
 ("Data", "#9d4edd", ["Pandas", "NumPy", "Visualization"]),
 ("Databases", "#39ff14", ["PostgreSQL", "MySQL", "MariaDB", "SQL Server", "MongoDB", "Redis", "Vector Databases"]),
 ("Tools", "#00f5d4", ["Git", "GitHub", "Docker", "Linux", "REST APIs"]),
]

SECTIONS = [("about", "About"), ("arsenal", "AI Engineering Arsenal"),
            ("projects", "Featured AI Projects"), ("lab", "Current AI Lab"),
            ("stats", "GitHub Statistics"), ("snake", "Contribution Snake"),
            ("connect", "Connect")]

PROFILE = [("role", "AI Developer / AI Engineer"),
           ("builds", "LLM apps, RAG systems, AI agents, automation"),
           ("stack", "Python, FastAPI, LangChain, LangGraph"),
           ("data", "SQL databases + vector search"),
           ("ships", "Docker, REST APIs"),
           ("interest", "self-hosted and open-source AI models")]
# ------------------------------------------------------------------

MONO = "font-family:'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
def save(name, svg): open(os.path.join(OUT, name), "w", encoding="utf-8").write(svg)
def chip_w(s, fs): return int(len(s) * fs * 0.62 + 22)

# ---------------- header ----------------
layers = [(800,[100,170,240]),(920,[70,135,205,270]),(1040,[100,170,240]),(1140,[140,200])]
lines, nodes = [], []
for (x1,a),(x2,b) in zip(layers, layers[1:]):
    for y1 in a:
        for y2 in b: lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
for i,(x,ys) in enumerate(layers):
    for j,y in enumerate(ys):
        c = "#00f5d4" if (i+j)%2==0 else "#9d4edd"
        nodes.append(f'<circle class="pulse" style="animation-delay:{i*0.5+j*0.4:.1f}s" cx="{x}" cy="{y}" r="7" fill="{c}"/>')

FS, CW, X0, SLOT, TYPE, HOLD = 26, 26*0.6, 94.0, 2.5, 1.2, 2.2
CYCLE = SLOT*len(ROLES)
def timeline(role_i, n):
    s = role_i*SLOT + 0.2
    pts = [(s + k*TYPE/n, k) for k in range(n+1)]
    pts.append((s+HOLD, 0))
    return pts
def anim(attr, role_widths, fn):
    pts = [(0.0, 0)]
    for i, r in enumerate(ROLES): pts += timeline(i, len(r))
    pts.append((CYCLE, 0))
    times = [min(t/CYCLE,1.0) for t,_ in pts]
    # make times strictly increasing
    for k in range(1,len(times)):
        if times[k] <= times[k-1]: times[k] = times[k-1] + 1e-4
    times[-1] = 1.0
    vals = [fn(k, i) for (t,k),i in zip(pts, range(len(pts)))]
    return f'<animate attributeName="{attr}" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{";".join(f"{t:.4f}" for t in times)}" values="{";".join(vals)}"/>'

# per-role clip: only that role shows, and only during its slot
clips, texts = "", ""
for i, r in enumerate(ROLES):
    n = len(r)
    pts = [(0.0, 0)]
    pts.append((i*SLOT, 0))
    pts += timeline(i, n)
    pts.append((CYCLE, 0))
    # dedupe/monotone
    clean = []
    for t,w in pts:
        if clean and t <= clean[-1][0]: t = clean[-1][0] + 1e-3
        clean.append((t,w))
    clean[0] = (0.0, clean[0][1]); clean[-1] = (CYCLE, 0)
    kt = ";".join(f"{min(t/CYCLE,1):.4f}" for t,_ in clean)
    vs = ";".join(f"{w*CW:.1f}" for _,w in clean)
    clips += (f'<clipPath id="c{i}"><rect x="{X0}" y="232" height="44" width="0">'
              f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vs}"/></rect></clipPath>')
    texts += f'<text style="{MONO}" x="{X0}" y="262" font-size="{FS}" fill="#00f5d4" clip-path="url(#c{i})">{E(r)}</text>'

# caret follows the typed width of whichever role is active
cp = [(0.0, 0)]
for i, r in enumerate(ROLES): cp += [(p[0], p[1]) for p in timeline(i, len(r))]
cp.append((CYCLE, 0))
clean = []
for t,w in cp:
    if clean and t <= clean[-1][0]: t = clean[-1][0] + 1e-3
    clean.append((t,w))
clean[0] = (0.0, clean[0][1]); clean[-1] = (CYCLE, 0)
caret = (f'<rect y="238" width="11" height="28" fill="#39ff14" x="{X0}">'
         f'<animate attributeName="x" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" '
         f'keyTimes="{";".join(f"{min(t/CYCLE,1):.4f}" for t,_ in clean)}" values="{";".join(f"{X0+w*CW:.1f}" for _,w in clean)}"/>'
         f'<animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;0.5" values="1;0"/></rect>')

header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" width="100%" role="img" aria-labelledby="t">
<title id="t">AI Engineer // Building intelligent systems. Roles: {E(", ".join(ROLES))}</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07090d"/><stop offset="1" stop-color="#110d1f"/></linearGradient>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#00f5d4"/><stop offset="1" stop-color="#9d4edd"/></linearGradient>
<linearGradient id="sc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00f5d4" stop-opacity="0"/><stop offset="1" stop-color="#00f5d4" stop-opacity=".18"/></linearGradient>
<radialGradient id="g1" cx=".85" cy=".3" r=".5"><stop offset="0" stop-color="#9d4edd" stop-opacity=".35"/><stop offset="1" stop-color="#9d4edd" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx=".08" cy=".95" r=".45"><stop offset="0" stop-color="#00f5d4" stop-opacity=".16"/><stop offset="1" stop-color="#00f5d4" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#00f5d4" stroke-opacity=".07"/></pattern>
<clipPath id="clip"><rect width="1200" height="340" rx="14"/></clipPath>
{clips}
</defs>
<style>
.scan{{animation:scan 7s linear infinite}}
@keyframes scan{{0%{{transform:translateY(-60px)}}100%{{transform:translateY(360px)}}}}
.pulse{{animation:pulse 3s ease-in-out infinite;opacity:.55}}
@keyframes pulse{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.scan,.pulse{{animation:none}}}}
</style>
<g clip-path="url(#clip)">
<rect width="1200" height="340" fill="url(#bg)"/><rect width="1200" height="340" fill="url(#grid)"/>
<rect width="1200" height="340" fill="url(#g1)"/><rect width="1200" height="340" fill="url(#g2)"/>
<g stroke="#00f5d4" stroke-opacity=".22">{"".join(lines)}</g><g>{"".join(nodes)}</g>
<g class="scan"><rect width="1200" height="60" fill="url(#sc)"/><rect y="59" width="1200" height="1.5" fill="#00f5d4" fill-opacity=".5"/></g>
<text style="{MONO}" x="60" y="72" font-size="16" fill="#00f5d4" fill-opacity=".85">$ whoami</text>
<text style="{MONO}" x="60" y="150" font-size="68" font-weight="700" fill="url(#ac)" letter-spacing="2">AI ENGINEER</text>
<text style="{MONO}" x="62" y="196" font-size="22" fill="#c9d1d9">// BUILDING INTELLIGENT SYSTEMS</text>
<text style="{MONO}" x="62" y="262" font-size="{FS}" fill="#8b949e">&gt;</text>
{texts}{caret}
<text style="{MONO}" x="62" y="310" font-size="14" fill="#8b949e">LLM apps  ·  RAG  ·  AI agents  ·  automation</text>
<rect x=".5" y=".5" width="1199" height="339" rx="14" fill="none" stroke="#00f5d4" stroke-opacity=".25"/>
</g></svg>'''
save("header.svg", header)

# ---------------- section headers ----------------
for key, title in SECTIONS:
    save(f"sec-{key}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 64" width="100%" role="img" aria-label="{E(title)}">
<defs><linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#00f5d4"/><stop offset="1" stop-color="#9d4edd"/></linearGradient></defs>
<rect width="900" height="64" rx="10" fill="#0a0e14"/>
<rect x=".5" y=".5" width="899" height="63" rx="10" fill="none" stroke="#00f5d4" stroke-opacity=".25"/>
<rect x="18" y="16" width="5" height="32" rx="2.5" fill="url(#l)"/>
<text x="38" y="40" font-size="24" font-weight="700" fill="#e6edf3" style="{MONO}">{E(title)}</text>
<text x="882" y="38" font-size="14" fill="#8b949e" text-anchor="end" style="{MONO}">~/{key}</text>
<rect x="18" y="58" width="864" height="2" rx="1" fill="url(#l)" fill-opacity=".55"/>
</svg>''')

# ---------------- about card ----------------
rows = ""
for i,(k,v) in enumerate(PROFILE):
    y = 92 + i*34
    rows += (f'<text x="34" y="{y}" font-size="17" fill="#9d4edd" style="{MONO}">{E(k)}:</text>'
             f'<text x="150" y="{y}" font-size="17" fill="#c9d1d9" style="{MONO}">{E(v)}</text>')
H = 92 + len(PROFILE)*34 + 8
save("about-card.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {H}" width="100%" role="img" aria-label="Profile summary">
<rect width="900" height="{H}" rx="12" fill="#0a0e14"/><rect x=".5" y=".5" width="899" height="{H-1}" rx="12" fill="none" stroke="#00f5d4" stroke-opacity=".25"/>
<circle cx="28" cy="26" r="6" fill="#ff5f56"/><circle cx="50" cy="26" r="6" fill="#ffbd2e"/><circle cx="72" cy="26" r="6" fill="#27c93f"/>
<text x="450" y="31" font-size="14" fill="#8b949e" text-anchor="middle" style="{MONO}">profile.yml</text>
{rows}</svg>''')

# ---------------- arsenal ----------------
FSZ, GAP, LX, MAXX = 15, 10, 190, 870
y = 24; body = ""
for label, col, chips in ARSENAL:
    x, line_y = LX, y
    body += f'<text x="30" y="{y+27}" font-size="16" font-weight="700" fill="{col}" style="{MONO}">{E(label)}</text>'
    for c in chips:
        w = chip_w(c, FSZ)
        if x + w > MAXX: x, y = LX, y + 42
        body += (f'<rect x="{x}" y="{y+6}" width="{w}" height="30" rx="15" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".6"/>'
                 f'<text x="{x+w/2}" y="{y+26}" font-size="{FSZ}" fill="#e6edf3" text-anchor="middle" style="{MONO}">{E(c)}</text>')
        x += w + GAP
    y += 52
    body += f'<rect x="30" y="{y-8}" width="840" height="1" fill="#1f2937"/>'
H = y + 8
save("arsenal.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {H}" width="100%" role="img" aria-label="Technologies I work with">
<rect width="900" height="{H}" rx="12" fill="#0a0e14"/><rect x=".5" y=".5" width="899" height="{H-1}" rx="12" fill="none" stroke="#00f5d4" stroke-opacity=".25"/>
{body}</svg>''')

# ---------------- project cards ----------------
for fid, name, problem, stack, col in PROJECTS:
    wrapped = textwrap.wrap(problem, 46)[:3]
    prob = "".join(f'<text x="28" y="{104+i*22}" font-size="15" fill="#9da7b3" style="{MONO}">{E(l)}</text>' for i,l in enumerate(wrapped))
    x, cy, chips = 28, 178, ""
    for s in stack:
        w = chip_w(s, 13)
        if x + w > 412: x, cy = 28, cy + 34
        chips += (f'<rect x="{x}" y="{cy}" width="{w}" height="26" rx="13" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".6"/>'
                  f'<text x="{x+w/2}" y="{cy+18}" font-size="13" fill="#e6edf3" text-anchor="middle" style="{MONO}">{E(s)}</text>')
        x += w + 8
    save(f"card-{fid}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 260" width="100%" role="img" aria-label="{E(name)}: {E(problem)}">
<defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{col}"/><stop offset="1" stop-color="#9d4edd" stop-opacity=".2"/></linearGradient></defs>
<style>.c{{transition:none}}</style>
<rect width="440" height="260" rx="14" fill="#0a0e14"/><rect x=".5" y=".5" width="439" height="259" rx="14" fill="none" stroke="{col}" stroke-opacity=".35"/>
<rect x="0" y="0" width="440" height="4" rx="2" fill="url(#a)"/>
<text x="28" y="52" font-size="20" font-weight="700" fill="#f0f6fc" style="{MONO}">{E(name if len(name)<=30 else name[:29]+'…')}</text>
<rect x="28" y="66" width="48" height="2" fill="{col}"/>
{prob}{chips}
<text x="412" y="244" font-size="13" fill="{col}" text-anchor="end" style="{MONO}">open repository ↗</text>
</svg>''')
print("assets written:", sorted(os.listdir(OUT)))
