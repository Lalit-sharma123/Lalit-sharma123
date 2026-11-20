"""
Restyles the contribution-snake SVGs to the profile theme (tools/glass.py THEME):
recolours the snake and grid cells and paints the dark background (Platane/snk
outputs a transparent image, which would show GitHub's white page through it).
Usage: python tools/frame_snake.py dist/github-snake-dark.svg [...]
"""
import re, sys
from glass import T
SEAM = T["seam"]

root = (f":root{{--cb:{T['seam']};--cs:{T['snake']};--ce:{T['dots'][0]};"
        + "".join(f"--c{i}:{c};" for i, c in enumerate(T["dots"])) + "}")
for path in sys.argv[1:]:
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r":root\{[^}]*\}", root, svg, count=1)
    svg = re.sub(r'(<rect data-framed="1"[^>]*fill=")[^"]*"', rf'\g<1>{SEAM}"', svg)
    if 'data-framed="1"' not in svg:
        m = re.search(r"<svg\b[^>]*>", svg)
        if not m:
            continue
        bg = f'<rect data-framed="1" x="-5000" y="-5000" width="20000" height="20000" fill="{SEAM}"/>'
        svg = svg[:m.end()] + bg + svg[m.end():]
    open(path, "w", encoding="utf-8").write(svg)
    print("styled", path)
