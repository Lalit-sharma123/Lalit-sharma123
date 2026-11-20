"""
Gives the contribution-snake SVGs the profile's dark background (Platane/snk outputs a
transparent image, which shows GitHub's white page through it).
Usage: python tools/frame_snake.py dist/github-snake-dark.svg [...]
"""
import re, sys

SEAM = "#09071c"
for path in sys.argv[1:]:
    svg = open(path, encoding="utf-8").read()
    m = re.search(r"<svg\b[^>]*>", svg)
    if not m or 'data-framed="1"' in svg:
        continue
    bg = f'<rect data-framed="1" x="-5000" y="-5000" width="20000" height="20000" fill="{SEAM}"/>'
    open(path, "w", encoding="utf-8").write(svg[:m.end()] + bg + svg[m.end():])
    print("framed", path)
