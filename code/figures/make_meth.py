#!/usr/bin/env python3
"""Generate the corrected methodology figure (SVG -> PDF + PNG)."""
import cairosvg

W, H = 1740, 2420
SCALE = 1.34
GAP = 60          # extra vertical space inserted below Stage 1
YOFF = 0          # running vertical offset (raised to GAP after Stage 1)
FS = "font-family='Helvetica, Arial, sans-serif'"
els = []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def box(x, y, w, h, fill, stroke, lines, tcolor="#222", rx=16, sw=2):
    """lines = list of (text, font_size, weight, color_or_None)."""
    y = y + YOFF
    els.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' "
               f"fill='{fill}' stroke='{stroke}' stroke-width='{sw}'/>")
    if not lines:
        return
    lines = [(t, int(fs * SCALE), "700", c) for (t, fs, _w, c) in lines]
    total = sum(fs + 8 for _, fs, _, _ in lines)
    cy = y + h/2 - total/2 + lines[0][1]
    cx = x + w/2
    for txt, fs, wt, col in lines:
        c = col or tcolor
        els.append(f"<text x='{cx}' y='{cy}' text-anchor='middle' {FS} "
                   f"font-size='{fs}' font-weight='{wt}' fill='{c}'>{esc(txt)}</text>")
        cy += fs + 8

def label(x, y, txt):
    y = y + YOFF
    fs = int(30 * SCALE)
    els.append(f"<text x='{x}' y='{y}' {FS} font-size='{fs}' font-weight='800' "
               f"fill='#1a1a1a'>{esc(txt)}</text>")

def arrow(pts, color="#555", sw=3, dash=None):
    pts = [(px, py + YOFF) for px, py in pts]
    d = " ".join(f"{px},{py}" for px, py in pts)
    da = f" stroke-dasharray='{dash}'" if dash else ""
    els.append(f"<polyline points='{d}' fill='none' stroke='{color}' "
               f"stroke-width='{sw}'{da}/>")
    (x2, y2), (x1, y1) = pts[-1], pts[-2]
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    s = 11
    p1 = (x2 - s*math.cos(ang - .5), y2 - s*math.sin(ang - .5))
    p2 = (x2 - s*math.cos(ang + .5), y2 - s*math.sin(ang + .5))
    els.append(f"<polygon points='{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} "
               f"{p2[0]:.1f},{p2[1]:.1f}' fill='{color}'/>")

def line(pts, color="#555", sw=3, dash=None):
    pts = [(px, py + YOFF) for px, py in pts]
    d = " ".join(f"{px},{py}" for px, py in pts)
    da = f" stroke-dasharray='{dash}'" if dash else ""
    els.append(f"<polyline points='{d}' fill='none' stroke='{color}' "
               f"stroke-width='{sw}'{da}/>")

def small(x, y, txt, col="#666", fs=20, anchor="middle", wt="600"):
    y = y + YOFF
    fs = int(fs * SCALE)
    els.append(f"<text x='{x}' y='{y}' text-anchor='{anchor}' {FS} "
               f"font-size='{fs}' font-weight='700' fill='{col}'>{esc(txt)}</text>")

# ---------- palette: white / very light greys only ----------
C = dict(
    s1="#ECE9E1", s1s="#B9B2A5",
    s2="#EEECFB", s2s="#B4ABE6",
    mod="#E3F3EA", mods="#93CBAB", modt="#1f7a47",
    tech="#EFEBFB", techt="#5b4bb0",
    rep="#FBEEE9", reps="#E0B19F", rept="#9c3b1e",
    s3="#FBEBCF", s3s="#DFB46B", s3t="#8a5a12", s3sub="#FFF6E6",
    hv="#E1F0EC", hvs="#5FA993", hvt="#1d6f5c",
    cg="#E8E3F5", cgs="#9B86D0", cgt="#4b3b8f",
    s4="#DEEAF7", s4s="#93B4DF", s4t="#1f4e96",
    fin="#E4EFD8", fins="#93BC68", fint="#3e6b1f",
)

# ===================== STAGE 1 =====================
label(36, 56, "Stage 1 — Data preparation")
box(110, 80, 410, 116, C["s1"], C["s1s"],
    [("UCF-Crime videos", 30, "700", None), ("807 anomalous", 22, "600", "#666")])
box(650, 80, 410, 116, C["s1"], C["s1s"],
    [("Frame sampling", 30, "700", None), ("20 frames / batch", 22, "600", "#666")])
box(1190, 80, 420, 116, C["s1"], C["s1s"],
    [("UCA annotations", 30, "700", None), ("expert ground truth", 22, "600", "#666")])

# arrows: videos + frames -> stage 2 ; UCA -> (routed to judges, far right)
arrow([(315, 196), (315, 286 + GAP)])
arrow([(855, 196), (855, 286 + GAP)])

YOFF = GAP   # everything from Stage 2 downward shifts down by GAP

# ===================== STAGE 2 =====================
label(36, 262, "Stage 2 — Report generation")
box(110, 290, 1500, 300, C["s2"], C["s2s"], [], rx=20)
small(860, 348, "3 MLLMs  ×  8 prompting techniques", "#3a2f86", 32, "middle", "700")
box(150, 380, 420, 86, C["mod"], C["mods"], [("Claude Opus 4.7", 27, "700", C["modt"])])
box(620, 380, 420, 86, C["mod"], C["mods"], [("GPT-5.5", 27, "700", C["modt"])])
box(1090, 380, 420, 86, C["mod"], C["mods"], [("Gemini 3.1 Pro", 27, "700", C["modt"])])
box(150, 480, 1410, 84, C["tech"], C["s2s"],
    [("Zero-shot · self-consistency · meta · CoT · sequential · ReAct · least-to-most · iterative", 22, "700", C["techt"])])
arrow([(860, 590), (860, 646)])

# reports
box(560, 648, 600, 110, C["rep"], C["reps"],
    [("19,361 forensic reports", 31, "700", C["rept"]), ("21.8M words", 23, "600", C["rept"])])
arrow([(860, 758), (860, 856)])

# ===================== STAGE 3 =====================
label(36, 832, "Stage 3 — Panel-of-judges evaluation")
box(110, 860, 1160, 300, C["s3"], C["s3s"], [], rx=20)
small(690, 940, "3-judge LLM panel  (cross-judged)", C["s3t"], 31, "middle", "700")
box(150, 1000, 520, 110, C["s3sub"], C["s3s"],
    [("H1–H6 majority-vote labels", 24, "700", C["s3t"])])
box(710, 1000, 520, 110, C["s3sub"], C["s3s"],
    [("Inter-judge agreement", 24, "700", C["s3t"])])

# GT routed to judges along far-right margin (NOT into generation).
# Connects fixed Stage-1 UCA box to the shifted Stage-3 panel, so draw it
# with no running offset and bake GAP into the lower (Stage-3) points.
YOFF = 0
arrow([(1610, 138), (1680, 138), (1680, 1010 + GAP), (1272, 1010 + GAP)],
      color="#8a5a12", sw=3)
YOFF = GAP

line([(690, 1160), (690, 1466)])  # spine down to a distributor rail
line([(365, 1466), (1380, 1466)])
arrow([(365, 1466), (365, 1508)])
arrow([(865, 1466), (865, 1508)])
arrow([(1380, 1466), (1380, 1508)])

# ===================== VALIDATION & ROBUSTNESS LAYER =====================
# Human validation (left branch off the panel)
box(110, 1230, 540, 110, C["hv"], C["hvs"],
    [("Human-in-the-loop validation", 24, "700", C["hvt"])])
arrow([(345, 1160), (345, 1228)], color="#1d6f5c")

# Cross-generation pilot (right branch)
box(980, 1230, 470, 110, C["cg"], C["cgs"],
    [("Cross-generation pilot", 24, "700", C["cgt"])])
arrow([(1450, 1285), (1672, 1285), (1672, 1722), (1614, 1722)], color="#4b3b8f")

# incoming: panel (inter-judge agreement) -> cross-generation pilot
arrow([(1100, 1160), (1100, 1228)], color="#4b3b8f")
# outgoing: human-in-the-loop validation -> findings, routed around the
# left margin (mirror of the cross-generation route), clearing the Stage-4 label
arrow([(110, 1285), (28, 1285), (28, 1722), (148, 1722)], color="#1d6f5c")

# ===================== STAGE 4 =====================
label(36, 1490, "Stage 4 — Analysis")
box(150, 1510, 430, 110, C["s4"], C["s4s"],
    [("Statistical tests", 26, "700", C["s4t"])])
box(660, 1510, 410, 110, C["s4"], C["s4s"],
    [("Embeddings", 26, "700", C["s4t"])])
box(1150, 1510, 460, 110, C["s4"], C["s4s"],
    [("Detectability", 26, "700", C["s4t"])])
for cx in (365, 865, 1380):
    arrow([(cx, 1620), (cx, 1660)])

# findings
box(150, 1662, 1460, 124, C["fin"], C["fins"],
    [("Hallucination profiles & findings", 36, "700", C["fint"])])

HH = 1830 + GAP
svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{HH}' "
       f"viewBox='0 0 {W} {HH}'><rect width='{W}' height='{HH}' fill='white'/>"
       + "".join(els) + "</svg>")
open("meth1.svg", "w").write(svg)
cairosvg.svg2pdf(bytestring=svg.encode(), write_to="meth1.pdf")
cairosvg.svg2png(bytestring=svg.encode(), write_to="meth1.png", output_width=2200)
print("wrote meth1.svg / meth1.pdf / meth1.png")
