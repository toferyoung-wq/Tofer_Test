import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
cells = []
_n = [1]


def nid():
    _n[0] += 1
    return f"c{_n[0]}"


def q(s):
    return escape(s, {'"': "&quot;"})


FONT = "fontFamily=Helvetica;"
TXT = "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;" + FONT


def v(value, x, y, w, h, style, cid=None):
    cid = cid or nid()
    cells.append(
        f'<mxCell id="{cid}" value="{q(value)}" style="{style}" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return cid


def text(value, x, y, w, h, size=11, color="#263238", align="left", extra=""):
    return v(value, x, y, w, h, TXT + f"fontSize={size};fontColor={color};align={align};verticalAlign=middle;" + extra)


def e(src=None, tgt=None, style="", pts=None, sp=None, tp=None, value="", lstyle=""):
    cid = nid()
    s = f' source="{src}"' if src else ""
    t = f' target="{tgt}"' if tgt else ""
    geo = ""
    if sp:
        geo += f'<mxPoint x="{sp[0]}" y="{sp[1]}" as="sourcePoint"/>'
    if tp:
        geo += f'<mxPoint x="{tp[0]}" y="{tp[1]}" as="targetPoint"/>'
    if pts:
        geo += '<Array as="points">' + "".join(f'<mxPoint x="{a}" y="{b}"/>' for a, b in pts) + "</Array>"
    cells.append(
        f'<mxCell id="{cid}" value="{q(value)}" style="html=1;{FONT}fontSize=10;{style}" edge="1" parent="1"{s}{t}>'
        f'<mxGeometry relative="1" as="geometry">{geo}</mxGeometry></mxCell>')
    return cid


AMBER, TEAL = "#E69F00", "#009E73"
WARM_F, WARM_S = "#FFE0CC", "#F08A4B"
COOL_F, COOL_S = "#E3EEF7", "#7FA7C9"
FPHL = "#FAD7B5"
FLOW = "edgeStyle=none;rounded=0;strokeColor=#546E7A;strokeWidth=1.2;endArrow=blockThin;endFill=1;endSize=4;"
R = f'<font color="{AMBER}">●</font>'
P = f'<font color="{TEAL}">●</font>'


def tag(s):
    return f'<font style="font-size:10px" color="#78909C">{s}</font>'


def serif(s):
    return f'<i style="font-family:Times New Roman">{s}</i>'


def tab(label, x, y, w):
    return v(label, x, y, w, 20, "rounded=0;fillColor=#EEEEEE;strokeColor=none;html=1;" + FONT +
             "fontSize=12;fontStyle=3;fontColor=#37474F;align=left;spacingLeft=6;")



W, H = 920, 386
DARK = "#37474F"
NOTE = "#607D8B"
GREY_BAR = "#CFD8DC"
PURPLE = "#7B1FA2"
AXIS = "strokeColor=#90A4AE;strokeWidth=1;"


def bar(x, base, h, fill, w=8, extra=""):
    return v("", x, base - h, w, h, f"rounded=0;html=1;strokeColor=none;fillColor={fill};{extra}")


def hline(x0, x1, y, style):
    e(None, None, "endArrow=none;" + style, sp=(x0, y), tp=(x1, y))


def chip(name):
    f, c = {"FP": (WARM_F, WARM_S), "FPpred": (COOL_F, COOL_S), "LM": ("#ECEFF1", "#78909C")}[name]
    return (f'<span style="background-color:{f};color:{c};font-size:10px;font-weight:bold">'
            f'&nbsp;{name}&nbsp;</span>')


def row(x, y, w, chips, label, dots="", tags="", color=DARK):
    s_ = " ".join(chip(c) for c in chips) + f"&nbsp; {label}"
    if dots:
        s_ += f" {dots}"
    if tags:
        s_ += f" {tag(tags)}"
    return text(s_, x, y, w, 18, 12, color)


# ======================= left: direction construction =======================
uh = f'<span style="background-color:{FPHL}">&nbsp;uh&nbsp;</span>'
pre = f'<span style="background-color:{COOL_F};border-bottom:2px solid {COOL_S}">&nbsp;is&nbsp;</span>'
FPY, PRY = 150, 236                      # row centres of FP / FPpred
s1 = text(f"the boy is {uh} taking a cookie", 8, FPY - 22, 170, 18, 12)
s2 = text("the boy is taking a cookie", 8, FPY - 2, 170, 18, 12)
text("disfluent − fluent pairs", 8, FPY + 18, 170, 14, 10, NOTE)
s3 = text(f"the boy {pre} uh taking a cookie", 8, PRY - 9, 170, 18, 12)
text("pre-FP − pre-ordinary positions", 8, PRY + 11, 170, 14, 10, NOTE)

sx, sy, sw = 190, FPY - 40, 32
for k, (ox_, oy_) in enumerate(((10, -8), (5, -4), (0, 0))):
    front = k == 2
    for i in range(11):
        hl = i == 3
        fill = ('#FFE0CC' if hl else '#ECEFF1') if front else ('#FFF1E8' if hl else '#F5F7F8')
        stroke = ('#F08A4B' if hl else '#B0BEC5') if front else ('#F6C3A2' if hl else '#D5DCE0')
        v("", sx + ox_, sy + oy_ + i * 15, sw, 9,
          f"rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor={fill};strokeColor={stroke};")
for s_, y in ((s1, FPY - 13), (s2, FPY + 7), (s3, PRY)):
    e(s_, None, FLOW, tp=(sx, y))

m1 = v("−", 240, FPY - 9, 18, 18, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=13;fontStyle=1;" + FONT)
m2 = v("−", 240, PRY - 9, 18, 18, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=13;fontStyle=1;" + FONT)
e(None, m1, FLOW, sp=(sx + sw + 10, FPY))
e(None, m2, FLOW, sp=(sx + sw + 10, PRY))
c1 = v("", 270, FPY - 13, 28, 26, f"shape=cube;size=6;html=1;fillColor={WARM_F};strokeColor={WARM_S};strokeWidth=1.3;")
c2 = v("", 270, PRY - 13, 28, 26, f"shape=cube;size=6;html=1;fillColor={COOL_F};strokeColor={COOL_S};strokeWidth=1.3;")
e(m1, c1, FLOW)
e(m2, c2, FLOW)
text("<b>FP</b>", 258, FPY - 32, 52, 16, 13, WARM_S, "center")
text("<b>FPpred</b>", 250, PRY - 32, 68, 16, 13, COOL_S, "center")

# ======================= right: three stages, top to bottom =======================
PX = 352
PW = 912 - PX
PANELS = {"Read": (8, 112), "Use": (128, 104), "Write": (240, 140)}
STYLE = {"Read": ("#F2F8FE", "#CFE6FB", "#7FB0DD", "·", f"project {serif('h·v')}"),
         "Use": ("#F1F9F8", "#CDEBE7", "#6FBFB4", "⊖", f"mean-ablate {serif('v')}"),
         "Write": ("#FAF3FB", "#EBD5F0", "#BF8FCC", "⊕", f"add {serif('ασ')}<sub>F</sub>{serif('v')}")}
LIST_W = 250                 # left part of each panel: header + analyses
CH_X = PX + LIST_W + 16      # chart area
CH_W = 912 - CH_X - 12

for name, (y, h) in PANELS.items():
    body, head, stroke, op, formula = STYLE[name]
    v("", PX, y, PW, h, f"rounded=1;arcSize=4;html=1;fillColor={body};strokeColor={stroke};strokeWidth=1.2;")
    v("", PX, y, 26, h, f"rounded=1;arcSize=20;html=1;fillColor={head};strokeColor={stroke};strokeWidth=1.2;")
    v(op, PX + 4, y + 6, 18, 18, f"ellipse;html=1;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=1.5;fontSize=12;fontStyle=1;" + FONT)
    text(f"<b>{name}</b>", PX + 1, y + 30, 24, h - 36, 13, DARK, "center", "horizontal=0;")
    text(f"<font color='{NOTE}' style='font-size:11px'>{formula}</font>", PX + 34, y + 4, LIST_W - 20, 16, 11, DARK)

# fan-in from both directions to every stage
e(c1, None, f"endArrow=none;strokeColor={WARM_S};strokeWidth=2;", tp=(318, FPY))
e(c2, None, f"endArrow=none;strokeColor={COOL_S};strokeWidth=2;", tp=(330, PRY))
for colr, xoff, cy_ in ((WARM_S, 318, FPY), (COOL_S, 330, PRY)):
    e(None, None, f"endArrow=none;strokeColor={colr};strokeWidth=2;", sp=(xoff, PANELS['Read'][0] + 30), tp=(xoff, PANELS['Write'][0] + 40))
    for name, (y, h) in PANELS.items():
        yy = y + 30 + (0 if colr == WARM_S else 10)
        e(None, None, f"endArrow=blockThin;endFill=1;strokeColor={colr};strokeWidth=1.6;", sp=(xoff, yy), tp=(PX, yy))

# ---- Read: analyses + two-row distribution over positions
y0, h0 = PANELS["Read"]
lx = PX + 34
row(lx, y0 + 24, LIST_W, ["FPpred"], "Position readout (AUC)", P)
row(lx, y0 + 44, LIST_W, ["FPpred"], "Beyond covariates (ΔAUC)", P)
row(lx, y0 + 64, LIST_W, ["FP"], "Position readout", P, "comparison", "#78909C")
row(lx, y0 + 86, LIST_W, ["LM"], "Surprisal link", P)
words = ["the", "boy", "is", "uh", "taking", "a", "cookie"]
dx = 34
gx = CH_X + 46
b1, b2 = y0 + 44, y0 + 84
v("", gx + 3 * dx + 1, y0 + 8, 32, 96, f"rounded=0;html=1;strokeColor=none;fillColor={FPHL};opacity=60;")
hv = [6, 8, 26, 0, 7, 5, 8]
sp_ = [6, 7, 6, 0, 24, 6, 8]
for i in range(len(words)):
    if i == 3:
        continue
    bar(gx + i * dx + 11, b1, hv[i], COOL_S if i == 2 else GREY_BAR, w=12)
    bar(gx + i * dx + 11, b2, sp_[i], "#78909C" if i == 4 else GREY_BAR, w=12)
for yy in (b1, b2):
    hline(gx, gx + len(words) * dx, yy, AXIS)
for i, wd in enumerate(words):
    text(wd, gx + i * dx - 4, b2 + 2, dx + 8, 14, 10.5, "#455A64", "center")
text(f"{serif('h')}·{serif('v')}<sub>FPpred</sub>", CH_X - 4, b1 - 16, 56, 14, 10.5, COOL_S)
text("surprisal", CH_X - 4, b2 - 16, 52, 14, 10, "#78909C")

# ---- Use: next-token distribution, before (dashed) vs after ablation (filled)
y0, h0 = PANELS["Use"]
row(lx, y0 + 30, LIST_W, ["FP"], "Ablate FP", R)
row(lx, y0 + 54, LIST_W, ["FPpred"], "Ablate FPpred", R + P)
text(f"<i>vs. matched random directions</i>", lx, y0 + 78, LIST_W, 14, 10, NOTE)
cands = ["uh", "the", "and", "boy", "a", "um"]
before = [30, 22, 15, 12, 9, 14]
after = [14, 22, 15, 12, 9, 7]
base, dx, gx = y0 + 80, 40, CH_X + 50
for i in range(len(cands)):
    xx = gx + i * dx
    bar(xx, base, before[i], "none", w=16, extra="strokeColor=#90A4AE;dashed=1;strokeWidth=1;")
    filler = cands[i] in ("uh", "um")
    bar(xx, base, after[i], WARM_S if filler else GREY_BAR, w=16)
    text(cands[i], xx - 12, base + 2, 40, 14, 10.5, "#455A64", "center")
hline(gx - 8, gx + len(cands) * dx - 20, base, AXIS)
text("<i>P(next token)</i>", CH_X - 4, y0 + 8, 100, 14, 10, NOTE)
text(f"dashed: before&nbsp;&nbsp; <span style='color:{WARM_S}'>■</span> after ablation",
     CH_X + 140, y0 + 8, 160, 14, 10, NOTE)

# ---- Write: every position vs selected positions, plus free generation
y0, h0 = PANELS["Write"]
row(lx, y0 + 26, LIST_W, ["FP"], "Add FP", R + P, "TF · Gen")
row(lx, y0 + 48, LIST_W, ["FPpred"], "Add FPpred", R + P, "TF")
row(lx, y0 + 70, LIST_W, ["FP"], "Oracle timing", R + P, "Gen")
row(lx, y0 + 92, LIST_W, ["FP", "FPpred"], "Gated injection", R + P, "TF · Gen")
text(f"<i>{chip('FPpred')} score chooses where {chip('FP')} is added</i>", lx, y0 + 112, LIST_W, 14, 10, NOTE)

half = (CH_W - 10) // 2
for k, title in enumerate(("every position", "selected positions")):
    bx = CH_X + k * (half + 10)
    text(f"<i>{title}</i>", bx, y0 + 6, half, 14, 10.5, PURPLE)
    base = y0 + 62
    n = 5 if k == 0 else 7
    ddx = (half - 20) / n
    sc = [7, 10, 24, 8, 6, 20, 9]
    for i in range(n):
        xx = bx + 10 + i * ddx
        if k == 0:
            bar(xx, base, 8, GREY_BAR, w=9)
            text("⊕", xx - 3, base - 26, 16, 14, 11, PURPLE, "center", "fontStyle=1;")
        else:
            over = sc[i] > 14
            bar(xx, base, sc[i], COOL_S if over else GREY_BAR, w=9)
            if over:
                text("⊕", xx - 3, base - sc[i] - 16, 16, 14, 11, PURPLE, "center", "fontStyle=1;")
    hline(bx + 4, bx + half - 6, base, AXIS)
    if k == 1:
        hline(bx + 4, bx + half - 6, base - 14, "dashed=1;strokeColor=#7B1FA2;strokeWidth=1;")
        text("top <i>k</i>%", bx + half - 40, base - 28, 40, 12, 9.5, PURPLE, "right")

# free generation strip inside the Write panel
gy = y0 + 84
v("", CH_X, gy, CH_W, 44, "rounded=1;arcSize=10;html=1;fillColor=#FFFFFF;strokeColor=#D7B6E0;")
text(f"<b>Gen</b>", CH_X + 6, gy + 13, 34, 18, 11.5, PURPLE)
pc = v("picture prompt", CH_X + 42, gy + 11, 84, 22,
       "rounded=1;arcSize=20;html=1;fillColor=#F5F5F5;strokeColor=#B0BEC5;fontSize=10;fontColor=#455A64;whiteSpace=wrap;" + FONT)
gl = CH_X + 140
for i in range(3):
    v("", gl, gy + 12 + i * 8, 24, 6, "rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor=#ECEFF1;strokeColor=#B0BEC5;")
text("⊕", gl + 18, gy + 2, 16, 12, 10, PURPLE, "center", "fontStyle=1;")
e(pc, None, FLOW, tp=(gl, gy + 22))
oc = v("the boy <span style='background-color:#ECEFF1;color:#78909C'>&nbsp;[FP]&nbsp;</span> is …",
       gl + 40, gy + 11, CH_W - (gl + 40 - CH_X) - 8, 22,
       "rounded=1;arcSize=20;html=1;fillColor=#FFFFFF;strokeColor=#B0BEC5;fontSize=10.5;fontColor=#263238;whiteSpace=wrap;" + FONT)
e(None, oc, FLOW, sp=(gl + 26, gy + 22))

xml = ('<mxfile host="drawio"><diagram id="overview" name="Overview">'
       f'<mxGraphModel dx="{W}" dy="{H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       f'fold="1" page="0" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
       "</root></mxGraphModel></diagram></mxfile>")
open(OUT, "w").write(xml)
print(OUT, len(cells), "cells")
