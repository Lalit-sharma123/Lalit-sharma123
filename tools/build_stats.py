"""
Builds assets/stats.svg - a glass-style GitHub stats panel that matches the rest of
the profile (replaces the third-party stat cards, which bring their own margins).

Runs in .github/workflows/profile-assets.yml. Locally:
    GITHUB_TOKEN=<token> python tools/build_stats.py Lalit-sharma123
    python tools/build_stats.py --demo          # sample data, no network

Token: STATS_TOKEN if set (a personal token also counts private contributions),
otherwise the workflow's GITHUB_TOKEN (public activity only).
"""
import datetime as dt, json, os, sys, urllib.request
from glass import *  # noqa: F401,F403

# Categorical order for languages comes from the theme; each preset's list is validated
# (lightness band, colour-blind separation, contrast) against that theme's panel surface.
LANG_COLORS, OTHER = T["lang"], T["other"]

QUERY = """
query($login:String!, $after:String){ user(login:$login){
  followers{totalCount}
  pullRequests{totalCount}
  issues{totalCount}
  repositories(ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC, first:100, after:$after){
    totalCount pageInfo{hasNextPage endCursor}
    nodes{ stargazerCount languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name } } } } }
  contributionsCollection{ totalCommitContributions contributionCalendar{ totalContributions
    weeks{ contributionDays{ date contributionCount } } } } } }"""


def fetch(login, token):
    data, after, repos = None, None, []
    while True:
        req = urllib.request.Request("https://api.github.com/graphql",
                                     json.dumps({"query": QUERY, "variables": {"login": login, "after": after}}).encode(),
                                     {"Authorization": f"bearer {token}", "Content-Type": "application/json",
                                      "User-Agent": "profile-stats"})
        out = json.load(urllib.request.urlopen(req, timeout=30))
        if out.get("errors"):
            raise SystemExit(f"GraphQL error: {out['errors']}")
        u = out["data"]["user"]
        data = data or u
        repos += u["repositories"]["nodes"]
        pi = u["repositories"]["pageInfo"]
        if not pi["hasNextPage"]:
            break
        after = pi["endCursor"]
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    cal = data["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    return dict(stars=sum(r["stargazerCount"] for r in repos), repos=data["repositories"]["totalCount"],
                followers=data["followers"]["totalCount"], prs=data["pullRequests"]["totalCount"],
                issues=data["issues"]["totalCount"], commits=data["contributionsCollection"]["totalCommitContributions"],
                total=cal["totalContributions"], days=days, langs=langs)


def demo():
    import random
    rnd, start = random.Random(4), dt.date.today() - dt.timedelta(days=364)
    days = [((start + dt.timedelta(i)).isoformat(), max(0, int(rnd.gauss(3 + 3 * (i / 365), 3)))) for i in range(365)]
    return dict(stars=48, repos=67, followers=2, prs=23, issues=11, commits=612, total=sum(c for _, c in days),
                days=days, langs={"Python": 900, "Jupyter Notebook": 400, "JavaScript": 220, "HTML": 150,
                                  "TypeScript": 90, "CSS": 60, "Shell": 20, "Dockerfile": 8})


def streaks(days):
    today = dt.date.today().isoformat()
    counts = [c for d, c in days if d <= today]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today not counted yet is not a broken streak
        i -= 1
    while i >= 0 and counts[i]:
        cur, i = cur + 1, i - 1
    return cur, longest


def fmt(n):
    return f"{n/1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def build(s, login):
    reset_ids()
    W, H = 1200, 720
    b = [(160, 160, 240, CYAN, 120, 60, 19), (1040, 300, 260, VIOLET, -140, 50, 23), (560, 640, 240, PINK, 90, -60, 17)]
    cur, longest = streaks(s["days"])
    tiles = [("Contributions", fmt(s["total"]), "last 12 months"), ("Current streak", f"{cur}d", "consecutive days"),
             ("Longest streak", f"{longest}d", "last 12 months"), ("Stars earned", fmt(s["stars"]), "public repos"),
             ("Pull requests", fmt(s["prs"]), "all time"), ("Public repos", fmt(s["repos"]), "owned, not forks")]
    out = ""
    tw_, gap, x0 = 168, 12, 76
    for i, (label, val, sub) in enumerate(tiles):
        x = x0 + i * (tw_ + gap)
        out += glass(f'<rect x="{x}" y="64" width="{tw_}" height="124" rx="18"', W, H, sweep=False, strength=.3, shadow=False)
        out += (f'<g class="f" style="animation-delay:{.1+i*.08:.2f}s">'
                f'<text x="{x+18}" y="94" font-size="13" fill="{MUTED}" style="{SANS}">{E(label)}</text>'
                f'<text x="{x+18}" y="144" font-size="38" font-weight="800" fill="{TEXT}" style="{SANS}">{E(val)}</text>'
                f'<text x="{x+18}" y="170" font-size="12" fill="{DIM}" style="{SANS}">{E(sub)}</text></g>')

    # --- weekly contributions: one series -> no legend; title names it ---
    weeks = []
    for i in range(0, len(s["days"]), 7):
        chunk = s["days"][i:i + 7]
        if len(chunk) == 7:  # skip the partial current week so the line doesn't dive to 0
            weeks.append((chunk[0][0], sum(c for _, c in chunk)))
    cx0, cx1, cy0, cy1 = 104, 1096, 300, 456
    peak = max([c for _, c in weeks] + [1])
    n = len(weeks)
    pts = [(cx0 + (cx1 - cx0) * i / max(n - 1, 1), cy1 - (cy1 - cy0) * c / peak) for i, (_, c) in enumerate(weeks)]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = line + f" L{cx1} {cy1} L{cx0} {cy1}Z"
    grid = "".join(f'<line x1="{cx0}" x2="{cx1}" y1="{cy1-(cy1-cy0)*k/4:.0f}" y2="{cy1-(cy1-cy0)*k/4:.0f}" stroke="#fff" stroke-opacity=".06"/>'
                   for k in range(1, 5))
    ylab = (f'<text x="{cx0-12}" y="{cy0+4}" font-size="12" fill="{DIM}" text-anchor="end" style="{SANS}">{peak}</text>'
            f'<text x="{cx0-12}" y="{cy1+4}" font-size="12" fill="{DIM}" text-anchor="end" style="{SANS}">0</text>')
    months, last = "", None
    for i, (d, _) in enumerate(weeks):
        m = d[:7]
        if m != last and i > 0:
            x = pts[i][0]
            months += f'<text x="{x:.0f}" y="{cy1+24}" font-size="12" fill="{DIM}" text-anchor="middle" style="{SANS}">{dt.date.fromisoformat(d).strftime("%b")}</text>'
        last = m
    pk = max(range(n), key=lambda i: weeks[i][1]) if n else 0
    px, py = pts[pk]
    peak_lbl = (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{CYAN}" stroke="{SEAM}" stroke-width="2"/>'
                f'<text x="{min(max(px, cx0+60), cx1-60):.0f}" y="{py-14:.0f}" font-size="12.5" fill="{TEXT}" text-anchor="middle" style="{SANS}">'
                f'peak week: {weeks[pk][1]}</text>') if n else ""
    out += glass(f'<rect x="76" y="212" width="1048" height="290" rx="20"', W, H, sweep=False, strength=.3, shadow=False)
    out += (f'<text x="104" y="246" font-size="16" font-weight="700" fill="{TEXT}" style="{SANS}">Contributions per week</text>'
            f'<text x="1096" y="246" font-size="13" fill="{MUTED}" text-anchor="end" style="{SANS}">{fmt(s["commits"])} commits · last 12 months</text>'
            f'<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>'
            f'{grid}<line x1="{cx0}" x2="{cx1}" y1="{cy1}" y2="{cy1}" stroke="#fff" stroke-opacity=".18"/>{ylab}{months}'
            f'<path d="{area}" fill="url(#ar)"/>'
            f'<path d="{line}" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" pathLength="1000" stroke-dasharray="1000">'
            f'<animate attributeName="stroke-dashoffset" values="1000;0" dur="2.4s" fill="freeze"/></path>{peak_lbl}')

    # --- languages: segmented bar, 2px gaps, legend with name + share ---
    langs = sorted(s["langs"].items(), key=lambda kv: -kv[1])
    total = sum(v for _, v in langs) or 1
    top, rest = langs[:6], sum(v for _, v in langs[6:])
    segs = [(nm, v, LANG_COLORS[i]) for i, (nm, v) in enumerate(top)] + ([("Other", rest, OTHER)] if rest else [])
    out += glass(f'<rect x="76" y="526" width="1048" height="150" rx="20"', W, H, sweep=False, strength=.3, shadow=False)
    out += f'<text x="104" y="560" font-size="16" font-weight="700" fill="{TEXT}" style="{SANS}">Languages across public repos</text>'
    bx, bw = 104, 992
    x = bx
    for i, (nm, v, c) in enumerate(segs):
        w = max(bw * v / total - 2, 2)
        r = 4 if i in (0, len(segs) - 1) else 0
        out += f'<rect x="{x:.1f}" y="578" width="{w:.1f}" height="14" rx="{r}" fill="{c}"><title>{E(nm)} {100*v/total:.1f}%</title></rect>'
        x += w + 2
    lx, ly = 104, 626
    for nm, v, c in segs:
        label = f"{nm}  {100*v/total:.1f}%"
        w = tw(label, 13.5, .55) + 40
        if lx + w > 1110:
            lx, ly = 104, ly + 28
        out += (f'<rect x="{lx}" y="{ly-10}" width="10" height="10" rx="2" fill="{c}"/>'
                f'<text x="{lx+18}" y="{ly}" font-size="13.5" fill="{TEXT}" style="{SANS}">{E(nm)}'
                f'<tspan fill="{MUTED}">  {100*v/total:.1f}%</tspan></text>')
        lx += w
    stamp = dt.datetime.utcnow().strftime("%d %b %Y")
    label = (f"GitHub stats for {login}: {s['total']} contributions in the last year, current streak {cur} days, "
             f"longest streak {longest} days, {s['stars']} stars, {s['prs']} pull requests, {s['repos']} public repos. "
             f"Top languages: " + ", ".join(f"{nm} {100*v/total:.0f}%" for nm, v, _ in segs))
    svg = svg_open(W, H, label) + defs(W, H, b) + f'''
{background(W, H)}
{glass(f'<rect x="40" y="24" width="1120" height="{H-48}" rx="28"', W, H, sweep_dur=10)}
{comet(rrect_path(40, 24, 1120, H - 48, 28), CYAN, dur=12, length=80)}
{out}
<text x="1124" y="{H-34}" font-size="11" fill="{DIM}" text-anchor="end" style="{MONO}">updated {stamp}</text>
</svg>'''
    save("stats.svg", svg)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    login = args[0] if args else os.environ.get("GITHUB_REPOSITORY_OWNER", "Lalit-sharma123")
    if "--demo" in sys.argv:
        build(demo(), login)
    else:
        tok = os.environ.get("STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not tok:
            raise SystemExit("Set GITHUB_TOKEN (or STATS_TOKEN), or pass --demo.")
        build(fetch(login, tok), login)
    print("wrote assets/stats.svg")
