"""
Shared building blocks for the "aurora glass" SVGs (imported by generate_assets.py
and build_stats.py). Every image is a full-bleed dark tile: the aurora fades to the
same SEAM colour at the top and bottom edge, so stacked images join seamlessly.
"""
import os, random
from html import escape as E

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

SANS = "font-family:'Segoe UI',Inter,'Helvetica Neue',ui-sans-serif,system-ui,-apple-system,Roboto,Arial,sans-serif"
MONO = "font-family:'JetBrains Mono','Fira Code','Cascadia Code',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
# ============================== THEME ==============================
# Pick a preset, run  python tools/generate_assets.py  and commit.
# (The stats card and snake pick it up on the next workflow run.)
THEME = "sunset"

THEMES = {
    # warm neon dusk: amber -> magenta -> violet over deep plum
    "sunset": dict(seam="#0c0614", bg1="#1f0b26", base="#14081a",
                   a1="#ffa94d", a2="#ff4f9a", a3="#9f6bff",
                   acc=["#ffa94d", "#ff5fa2", "#b794ff", "#ffd166", "#ff7a6b", "#7dd3fc"],
                   text="#fff5ee", muted="#d4bfcf", dim="#937a98",
                   live="#4ade80", live_text="#bbf7d0",
                   lang=["#d97706", "#db2777", "#7c3aed", "#0891b2", "#65a30d", "#2563eb"], other="#78716c",
                   snake="#ffa94d", dots=["#1d1022", "#4a1942", "#8a2b5f", "#e0457b", "#ffa94d"]),
    # the previous look: cyan -> violet -> pink over ink blue
    "aurora": dict(seam="#09071c", bg1="#0e0a26", base="#0a0820",
                   a1="#22d3ee", a2="#a855f7", a3="#f472b6",
                   acc=["#22d3ee", "#c084fc", "#f472b6", "#2dd4bf", "#818cf8", "#fb923c"],
                   text="#f1f5f9", muted="#a5b0c2", dim="#6b7590",
                   live="#22c55e", live_text="#bbf7d0",
                   lang=["#0891b2", "#a855f7", "#ea580c", "#ec4899", "#65a30d", "#6366f1"], other="#64748b",
                   snake="#22d3ee", dots=["#161233", "#3b1f6e", "#6d28d9", "#a855f7", "#f472b6"]),
    # deep sea: sky -> indigo -> teal over midnight navy
    "ocean": dict(seam="#050b18", bg1="#0a1a33", base="#071226",
                  a1="#38bdf8", a2="#6366f1", a3="#2dd4bf",
                  acc=["#38bdf8", "#818cf8", "#2dd4bf", "#a78bfa", "#60a5fa", "#fbbf24"],
                  text="#f0f9ff", muted="#a8bcd4", dim="#6a809c",
                  live="#4ade80", live_text="#bbf7d0",
                  lang=["#0891b2", "#7c3aed", "#d97706", "#db2777", "#65a30d", "#2563eb"], other="#64748b",
                  snake="#38bdf8", dots=["#0d1b30", "#0c3a5e", "#0369a1", "#0ea5e9", "#7dd3fc"]),
}
T = THEMES[THEME]
SEAM = T["seam"]          # colour every image fades to at its edges
BG0, BG1, GLASS_BASE = SEAM, T["bg1"], T["base"]
TEXT, MUTED, DIM = T["text"], T["muted"], T["dim"]
CYAN, VIOLET, PINK = T["a1"], T["a2"], T["a3"]   # primary / secondary / tertiary accent
ACC = T["acc"]             # six accents for projects, skills, buttons
LIVE, LIVE_TEXT = T["live"], T["live_text"]

CSS = """
.f{animation:fi .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes fi{from{transform:translateY(14px)}to{transform:translateY(0)}}
.blink{animation:bl 1.05s steps(1) infinite}
@keyframes bl{50%{opacity:0}}
.pulse{animation:pu 2.4s ease-in-out infinite}
@keyframes pu{0%,100%{opacity:.35}50%{opacity:1}}
@media (prefers-reduced-motion:reduce){.f,.blink,.pulse{animation:none}}
"""


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg)


def tw(s, fs, k=0.56):  # rough rendered text width
    return len(s) * fs * k


def rrect_path(x, y, w, h, r):
    return (f"M{x+r} {y}H{x+w-r}A{r} {r} 0 0 1 {x+w} {y+r}V{y+h-r}A{r} {r} 0 0 1 {x+w-r} {y+h}"
            f"H{x+r}A{r} {r} 0 0 1 {x} {y+h-r}V{y+r}A{r} {r} 0 0 1 {x+r} {y}Z")


def svg_open(w, h, label, extra_css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" '
            f'role="img" aria-label="{E(label)}"><title>{E(label)}</title><style>{CSS}{extra_css}</style>')


def page_path(w, h, c):
    tl, tr, br, bl = c
    return (f"M{tl} 0H{w-tr}" + (f"A{tr} {tr} 0 0 1 {w} {tr}" if tr else "") + f"V{h-br}"
            + (f"A{br} {br} 0 0 1 {w-br} {h}" if br else "") + f"H{bl}"
            + (f"A{bl} {bl} 0 0 1 0 {h-bl}" if bl else "") + f"V{tl}"
            + (f"A{tl} {tl} 0 0 1 {tl} 0" if tl else "") + "Z")


def _fade(id_, length, size, vertical):
    e = min(60, size * .3) / size
    x2, y2 = ("0", str(size)) if vertical else (str(size), "0")
    return (f'<linearGradient id="{id_}g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="#000"/><stop offset="{e:.3f}" stop-color="#fff"/>'
            f'<stop offset="{1-e:.3f}" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
            f'<mask id="{id_}" maskUnits="userSpaceOnUse" x="-10" y="-10" width="99999" height="99999">'
            f'<rect x="-10" y="-10" width="99999" height="99999" fill="url(#{id_}g)"/></mask>')


def defs(w, h, blobs, corners=(0, 0, 0, 0)):
    """Shared defs: background, aurora blob layer (#blobs), filters, glass gradients."""
    circles = ""
    for cx, cy, r, col, dx, dy, dur in blobs:
        circles += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity=".62">'
                    f'<animateTransform attributeName="transform" type="translate" dur="{dur}s" '
                    f'repeatCount="indefinite" values="0 0;{dx} {dy};{-dx*.6:.0f} {dy*.5:.0f};0 0" '
                    f'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></circle>')
    pad = 400
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset=".55" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
<g id="blobs">{circles}</g>
<filter id="soft" filterUnits="userSpaceOnUse" x="-{pad}" y="-{pad}" width="{w+2*pad}" height="{h+2*pad}"><feGaussianBlur stdDeviation="70"/></filter>
<filter id="frost" filterUnits="userSpaceOnUse" x="-{pad}" y="-{pad}" width="{w+2*pad}" height="{h+2*pad}"><feGaussianBlur stdDeviation="38"/><feColorMatrix type="saturate" values="1.5"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0"/></filter>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#ffffff" fill-opacity=".07"/></pattern>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".35" stop-color="#fff" stop-opacity=".08"/><stop offset=".7" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="{VIOLET}" stop-opacity=".55"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset=".45" stop-color="#fff" stop-opacity=".02"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="shimmer" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="520" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1040 0" dur="7s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<clipPath id="page"><path d="{page_path(w, h, corners)}"/></clipPath>
{_fade("vf", w, h, True)}{_fade("hf", h, w, False)}
</defs>'''


def background(w, h, dots=True, hfade=False):
    """Full-bleed dark tile. The aurora fades out toward the top/bottom edges (and the
    side edges with hfade=True) so neighbouring images meet on the same SEAM colour."""
    blobs = f'<use href="#blobs" filter="url(#soft)" opacity=".62"/>'
    if hfade:
        blobs = f'<g mask="url(#hf)">{blobs}</g>'
    return (f'<g clip-path="url(#page)"><rect width="{w}" height="{h}" fill="{SEAM}"/>'
            f'<g mask="url(#vf)">{blobs}</g>'
            + (f'<rect width="{w}" height="{h}" fill="url(#dots)"/>' if dots else "") + '</g>')


def reset_ids():
    _gid[0] = 0


_gid = [0]


def glass(shape, w, h, sweep=True, sweep_dur=8, sweep_begin=0, tint=None, strength=.42, shadow=True):
    """Frosted-glass panel. `shape` is an SVG shape element string (rect/circle/path) WITHOUT closing '/>'."""
    _gid[0] += 1
    k = _gid[0]
    out = ""
    if shadow:
        out += f'<g transform="translate(0 14)" opacity=".55">{shape} fill="#000" filter="url(#shadow)"/></g>'
    out += f'<clipPath id="g{k}">{shape}/></clipPath><g clip-path="url(#g{k})">'
    out += f'<rect width="{w}" height="{h}" fill="{GLASS_BASE}" fill-opacity=".68"/>'
    out += f'<use href="#blobs" filter="url(#frost)" opacity="{strength}"/>'
    if tint:
        out += f'<rect width="{w}" height="{h}" fill="{tint}" fill-opacity=".05"/>'
    out += f'<rect width="{w}" height="{h}" fill="#fff" fill-opacity=".035"/>'
    out += f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".05"/>'
    out += f'{shape} fill="url(#sheen)"/>'
    if sweep:
        out += (f'<polygon points="0,0 140,0 60,{h} -80,{h}" fill="url(#sweep)">'
                f'<animateTransform attributeName="transform" type="translate" values="-300 0;{w+300} 0;{w+300} 0" '
                f'keyTimes="0;.45;1" dur="{sweep_dur}s" begin="{sweep_begin}s" repeatCount="indefinite"/></polygon>')
    out += '</g>'
    out += f'{shape} fill="none" stroke="url(#edge)" stroke-width="1.3"/>'
    return out


def comet(path, color, dur=6, length=120, width=2.4, begin=0):
    """A bright segment that travels around a path (path should be ~1000 user units via pathLength)."""
    return (f'<path d="{path}" pathLength="1000" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-dasharray="{length} {1000-length}" filter="url(#glow)">'
            f'<animate attributeName="stroke-dashoffset" from="1000" to="0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path>')


def particles(w, h, n, seed, colors=(CYAN, VIOLET, PINK, "#ffffff")):
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(.8, 2.2)
        dur = rnd.uniform(7, 15)
        rise = rnd.uniform(40, 110)
        c = rnd.choice(colors)
        out += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{c}">'
                f'<animate attributeName="cy" values="{y:.0f};{y-rise:.0f}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;.9;0" dur="{dur:.1f}s" repeatCount="indefinite"/></circle>')
    return out


def chip(x, y, label, col, fs=15, h=34, cls="", delay=0.0):
    w = tw(label, fs, .58) + 34
    style = f' class="{cls}" style="animation-delay:{delay:.2f}s"' if cls else ""
    return (f'<g{style}><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{col}" fill-opacity=".10" '
            f'stroke="{col}" stroke-opacity=".55"/>'
            f'<rect x="{x+1:.1f}" y="{y+1}" width="{w-2:.1f}" height="{h/2-1}" rx="{h/2-1}" fill="#fff" fill-opacity=".05"/>'
            f'<circle cx="{x+15:.1f}" cy="{y+h/2}" r="3.2" fill="{col}" filter="url(#glow)"/>'
            f'<text x="{x+25:.1f}" y="{y+h/2+fs*.36:.1f}" font-size="{fs}" fill="{TEXT}" style="{SANS}">{E(label)}</text></g>'), w


