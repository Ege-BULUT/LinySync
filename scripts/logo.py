"""ANSI Shadow word marks for the *ySync family, drawn as shapes so they don't depend on fonts. Same generator as
MacySync's and WavySync's logos; each family member has its own colours and its own line shape.

    python3 -I logo.py <name> <out.svg>      name: anysync | windysync | linysync"""
import sys

G = {
    "N": ["███╗   ██╗", "████╗  ██║", "██╔██╗ ██║", "██║╚██╗██║", "██║ ╚████║", "╚═╝  ╚═══╝"],
    "W": ["██╗    ██╗", "██║    ██║", "██║ █╗ ██║", "██║███╗██║", "╚███╔███╔╝", " ╚══╝╚══╝ "],
    "L": ["██╗     ", "██║     ", "██║     ", "██║     ", "███████╗", "╚══════╝"],
    "Y": ["██╗   ██╗", "╚██╗ ██╔╝", " ╚████╔╝ ", "  ╚██╔╝  ", "   ██║   ", "   ╚═╝   "],
    "S": ["███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"],
}
W, H, CW, CH, Y0 = 1000, 320, 16, 22, 48
SEG = {"═": "lr", "║": "ud", "╗": "ld", "╔": "rd", "╚": "ur", "╝": "ul"}

# each: word, gradient stops, line colours (dim, bright, light), shadow stroke, frame, tagline (accent marks ~)
FAMILY = {
    # any to any: three platforms meet; a spectrum from violet through magenta to teal, lines that cross
    "anysync": dict(word="NYSYN", label="AnySync", stops=["#f1e9ff", "#c49bff", "#8b5cf6", "#3b1d8f"],
                    line=("#7c3aed", "#d946ef", "#5eead4"), shadow="#8e86a3", bg="#120f1c", frame="#2e2547",
                    tag="MAC ~ WINDOWS ~ LINUX ~ ANY TO ANY", accent="#d946ef", shape="cross"),
    # Windows to Windows: wind, straight gusts that curl at the end; aqua and white, apart from MacySync's blue
    "windysync": dict(word="WYSY", label="WindySync", stops=["#effeff", "#a5f3fc", "#22d3ee", "#0e7490"],
                      line=("#0891b2", "#67e8f9", "#ecfeff"), shadow="#86a3a8", bg="#0b1517", frame="#1d3a40",
                      tag="YOUR PC ~ ANY PC ~ END TO END", accent="#67e8f9", shape="gust"),
    # Linux to Linux: circuit traces with right angles; amber on charcoal
    "linysync": dict(word="LYSY", label="LinySync", stops=["#fff7e0", "#ffd166", "#f59e0b", "#8a4b08"],
                     line=("#d97706", "#fbbf24", "#fef3c7"), shadow="#9a8f7d", bg="#14120e", frame="#3a3122",
                     tag="ANY DISTRO ~ ANY DISTRO ~ END TO END", accent="#fbbf24", shape="trace"),
}

SHAPES = {  # (base path, second path) under the letters
    "cross": ("M 30 270 C 260 270 360 190 500 214 S 760 262 970 182", "M 30 182 C 240 262 380 236 500 214 S 780 170 970 270"),
    "gust": ("M 30 262 H 640 C 720 262 740 222 706 206 C 676 192 650 220 676 236", "M 120 284 H 860 C 920 284 940 252 914 240"),
    "trace": ("M 30 262 H 300 V 238 H 560 V 262 H 760 V 222 H 970", "M 70 274 H 380 V 250 H 620 V 274 H 930"),
}


def mark(word: str) -> tuple[list[str], float]:
    rows = ["".join(G[ch][r] for ch in word) for r in range(6)]
    x0 = (W - len(rows[0]) * CW) / 2
    cols = []
    for c in range(len(rows[0])):
        blocks, shadow = [], []
        for r, row in enumerate(rows):
            ch, x, y = row[c], x0 + c * CW, Y0 + r * CH
            if ch == "█":
                blocks.append(f'<rect x="{x:g}" y="{y:g}" width="{CW+0.6:g}" height="{CH+0.6:g}"/>')
            elif ch in SEG:
                cx, cy = x + CW / 2, y + CH / 2
                for off in (-2.5, 2.5):
                    for s in SEG[ch]:
                        if s == "l": shadow.append(f"M{x:g} {cy+off:g}H{cx+off*(1 if ch in '╗╝' else -1):g}")
                        if s == "r": shadow.append(f"M{cx-off*(1 if ch in '╔╚' else -1):g} {cy+off:g}H{x+CW:g}")
                        if s == "u": shadow.append(f"M{cx+off:g} {y:g}V{cy-off*(1 if ch in '╚╝' else -1):g}")
                        if s == "d": shadow.append(f"M{cx+off:g} {cy+off*(1 if ch in '╗╔' else -1):g}V{y+CH:g}")
        if blocks or shadow:
            b = "".join(blocks)
            s = f'<path class="sh" d="{"".join(shadow)}"/>' if shadow else ""
            cols.append(f'<g class="c" style="animation-delay:-{(len(rows[0])-c)*0.08:.2f}s">{s}<g fill="url(#g)">{b}</g><g fill="url(#sheen)">{b}</g></g>')
    return cols, x0


def svg(name: str) -> str:
    f = FAMILY[name]
    cols, _ = mark(f["word"])
    a, b = SHAPES[f["shape"]]
    dim, bright, light = f["line"]
    st = f["stops"]
    tag = f["tag"].replace("~", f'<tspan fill="{f["accent"]}">~</tspan>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{f["label"]}">
<defs>
<linearGradient id="g" x1="0" y1="{Y0}" x2="0" y2="{Y0+6*CH}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{st[0]}"/><stop offset=".3" stop-color="{st[1]}"/><stop offset=".62" stop-color="{st[2]}"/><stop offset="1" stop-color="{st[3]}"/></linearGradient>
<linearGradient id="sheen" x1="-260" y1="0" x2="-60" y2="0" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;{W+320} 0" dur="5s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{dim}" stop-opacity="0"/><stop offset=".45" stop-color="{bright}"/><stop offset="1" stop-color="{light}" stop-opacity="0"/></linearGradient>
</defs>
<style>
.c {{ animation: bob 2.8s ease-in-out infinite; }}
@keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
.sh {{ fill: none; stroke: {f["shadow"]}; stroke-width: 1.3; stroke-linecap: square; opacity: .85; }}
.sw {{ fill: none; stroke-linecap: round; stroke-linejoin: round; }}
.base {{ stroke: {f["frame"]}; stroke-width: 1.2; }}
.a {{ stroke: url(#line); stroke-width: 3; stroke-dasharray: 240 1300; animation: flow 3.4s linear infinite; }}
.b {{ stroke: {light}; stroke-width: 1.5; stroke-dasharray: 90 1000; animation: flow 4.6s linear infinite reverse; opacity: .7; }}
@keyframes flow {{ from {{ stroke-dashoffset: 1400; }} to {{ stroke-dashoffset: 0; }} }}
.t {{ font: 600 15px -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; fill: #c9ccd3; letter-spacing: 3px; }}
@media (prefers-reduced-motion: reduce) {{ .c, .a, .b {{ animation: none; }} }}
</style>
<rect width="{W}" height="{H}" rx="26" fill="{f["bg"]}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="25.5" fill="none" stroke="{f["frame"]}"/>
<path class="sw base" d="{a}"/>
<path class="sw a" d="{a}"/>
<path class="sw b" d="{b}"/>
{"".join(cols)}
<text class="t" x="{W/2:g}" y="{H-26}" text-anchor="middle">{tag}</text>
</svg>
'''


if __name__ == "__main__":
    open(sys.argv[2], "w", encoding="utf-8").write(svg(sys.argv[1]))
