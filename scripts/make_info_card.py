"""
Build a neofetch-style info card SVG to sit to the RIGHT of the ASCII portrait.
Uses CSS @keyframes animations (NOT SMIL) so it renders correctly on GitHub.
Edit ROWS below to customise content, then re-run to regenerate info-card.svg.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")

W, H = 480, 376
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 20.5

BG     = "#0d1117"
BG2    = "#111722"
FRAME  = "#30363d"
MUTED  = "#7d8590"
INK    = "#c9d1d9"
KEY    = "#ffa657"      # orange keys
SECTION= "#58a6ff"      # blue section headers
GREEN  = "#3fb950"
ACCENT = "#22d3ee"

# ── Edit your content here ──────────────────────────────────────────────────
# Row types:
#   ("host",)            →  VishuddhaChakra7@github header
#   ("kv", key, value)   →  orange key  +  light value
#   ("sec", title)       →  blue  "— title —"  section rule
#   ("bul", text)        →  green dot bullet
#   ("gap",)             →  half-line vertical spacer
ROWS = [
    ("host",),
    ("kv", "Now",      "Student @ CMR Institute of Technology"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Frontend", "HTML, CSS, JavaScript, React"),
    ("kv", "Backend",  "Node.js, Python"),
    ("gap",),
    ("sec", "Links"),
    ("bul", "github.com/VishuddhaChakra7"),
]
# ────────────────────────────────────────────────────────────────────────────


def esc(s):
    return html.escape(s)


# ── Build CSS (one class per row, staggered fade-up) ─────────────────────
ROW_DUR = 0.4
STAGGER = 0.08

css_rules = ["@keyframes ri{0%{opacity:0;transform:translateY(5px)}100%{opacity:1;transform:translateY(0)}}"]
visible_rows = [r for r in ROWS if r[0] != "gap"]
for idx in range(len(visible_rows)):
    delay = 0.15 + idx * STAGGER
    css_rules.append(
        f".r{idx}{{opacity:0;animation:ri {ROW_DUR}s cubic-bezier(.2,.8,.2,1) {delay:.2f}s both}}"
    )
css = "".join(css_rules)

# ── SVG skeleton ─────────────────────────────────────────────────────────
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
    f'<style>{css}</style>',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

# macOS dots
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2:.1f}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4:.1f}" fill="{MUTED}" font-size="12" '
    f'text-anchor="middle">VishuddhaChakra7@github: ~$ neofetch</text>'
)

# ── Rows ─────────────────────────────────────────────────────────────────
y = TITLEBAR_H + 30
css_idx = 0      # tracks index among non-gap rows for CSS class assignment

for row in ROWS:
    kind = row[0]

    if kind == "gap":
        y += LINE_H * 0.5
        continue

    cls = f"r{css_idx}"
    css_idx += 1

    if kind == "host":
        svg_inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
            f'<tspan fill="{GREEN}">VishuddhaChakra7</tspan>'
            f'<tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{ACCENT}">github</tspan></text>'
            f'<line x1="{KEY_X+236}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.8"/>'
        )
    elif kind == "sec":
        title = esc(row[1])
        rule_x = KEY_X + 12 + len(row[1]) * 8
        svg_inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
            f'&#8212; {title}</text>'
            f'<line x1="{rule_x}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.8"/>'
        )
    elif kind == "kv":
        k, v = esc(row[1]), esc(row[2])
        svg_inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{k}</text>'
            f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{v}</text>'
        )
    elif kind == "bul":
        txt = esc(row[1])
        svg_inner = (
            f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
            f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>'
        )
    else:
        continue

    parts.append(f'<g class="{cls}">{svg_inner}</g>')
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}  {len(svg)} bytes;  {W}x{H}  content_bottom={round(y)}")
