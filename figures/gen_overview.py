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



W, H = 920, 312
DARK = "#37474F"
NOTE = "#607D8B"
GREY_BAR = "#CFD8DC"
PURPLE = "#7B1FA2"
AXIS = "strokeColor=#90A4AE;strokeWidth=1;"
OPC = "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=15;fontStyle=1;" + FONT


def bar(x, base, h, fill, w=8, extra=""):
    return v("", x, base - h, w, h, f"rounded=0;html=1;strokeColor=none;fillColor={fill};{extra}")


def hline(x0, x1, y, style):
    e(None, None, "endArrow=none;" + style, sp=(x0, y), tp=(x1, y))


def row(x, y, w, label, dots="", tags="", size=12):
    s_ = label + (f" {dots}" if dots else "") + (f" {tag(tags)}" if tags else "")
    return text(s_, x, y, w, 18, size, DARK)


# ======================= top: direction construction (mirrored: right -> left) =======================
uh = f'<span style="background-color:{FPHL}">&nbsp;uh&nbsp;</span>'
pre = f'<span style="background-color:{COOL_F};border-bottom:2px solid {COOL_S}">&nbsp;is&nbsp;</span>'
FPY, PRY = 46, 112
TX = 300                                  # sentences on the right
s1 = text(f"the boy is {uh} taking a cookie", TX, FPY - 26, 210, 22, 14)
s2 = text("the boy is taking a cookie", TX, FPY - 2, 210, 22, 14)
text("disfluent − fluent pairs", TX, FPY + 20, 210, 16, 11.5, NOTE)
s3 = text(f"the boy {pre} uh taking a cookie", TX, PRY - 11, 210, 22, 14)
text("pre-FP − pre-ordinary positions", TX, PRY + 13, 210, 16, 11.5, NOTE)

sx, sy, sw = 218, 18, 40
for k, (ox_, oy_) in enumerate(((-12, -8), (-6, -4), (0, 0))):
    front = k == 2
    for i in range(9):
        hl = i == 3
        fill = ('#FFE0CC' if hl else '#ECEFF1') if front else ('#FFF1E8' if hl else '#F5F7F8')
        stroke = ('#F08A4B' if hl else '#B0BEC5') if front else ('#F6C3A2' if hl else '#D5DCE0')
        v("", sx + ox_, sy + oy_ + i * 13, sw, 8,
          f"rounded=1;arcSize=30;html=1;strokeWidth=0.9;fillColor={fill};strokeColor={stroke};")
for y in (FPY - 15, FPY + 9, PRY):
    e(None, None, FLOW, sp=(TX - 4, y), tp=(sx + sw, y))

m1 = v("−", 170, FPY - 11, 22, 22, OPC)
m2 = v("−", 170, PRY - 11, 22, 22, OPC)
e(None, m1, FLOW, sp=(sx - 14, FPY))
e(None, m2, FLOW, sp=(sx - 14, PRY))
c1 = v("", 110, FPY - 17, 36, 34, f"shape=cube;size=8;html=1;fillColor={WARM_F};strokeColor={WARM_S};strokeWidth=1.5;")
c2 = v("", 110, PRY - 17, 36, 34, f"shape=cube;size=8;html=1;fillColor={COOL_F};strokeColor={COOL_S};strokeWidth=1.5;")
e(m1, c1, FLOW)
e(m2, c2, FLOW)
text("<b>FP</b>", 98, FPY - 40, 60, 20, 15, WARM_S, "center")
text("<b>FPpred</b>", 90, PRY - 40, 76, 20, 15, COOL_S, "center")



# both directions merge into one line: left -> right, taps Read and Use, ends in Write
RL = 158
LINE = "#546E7A"
WX = 562
e(None, None, f"endArrow=none;strokeColor={WARM_S};strokeWidth=2.4;", sp=(110, FPY), pts=[(30, FPY)], tp=(30, PRY))
e(None, None, f"endArrow=none;strokeColor={COOL_S};strokeWidth=2.4;", sp=(110, PRY), tp=(30, PRY))
v("", 25, PRY - 5, 10, 10, f"ellipse;html=1;fillColor={LINE};strokeColor=none;")
e(None, None, f"endArrow=blockThin;endFill=1;strokeColor={LINE};strokeWidth=2.8;", sp=(30, PRY), pts=[(30, RL)], tp=(WX, RL))

# ======================= stages =======================
PY, PH = 176, 128
WY, WH = 8, PY + PH - 8
PANELS = {"Read": (8, 266, PY, PH), "Use": (282, 266, PY, PH), "Write": (WX, 912 - WX, WY, WH)}
STYLE = {"Read": ("#F2F8FE", "#CFE6FB", "#7FB0DD", "·", f"project {serif('h·v')}"),
         "Use": ("#F1F9F8", "#CDEBE7", "#6FBFB4", "⊖", f"mean-ablate {serif('v')}"),
         "Write": ("#FAF3FB", "#EBD5F0", "#BF8FCC", "⊕", f"add {serif('ασ')}<sub>F</sub>{serif('v')}")}
for name, (x, w, y, h) in PANELS.items():
    body, head, stroke, op, formula = STYLE[name]
    v("", x, y, w, h, f"rounded=1;arcSize=3;html=1;fillColor={body};strokeColor={stroke};strokeWidth=1.2;")
    v("", x, y, w, 24, f"rounded=1;arcSize=12;html=1;fillColor={head};strokeColor={stroke};strokeWidth=1.2;")
    v(op, x + 6, y + 3, 18, 18, f"ellipse;html=1;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=1.6;fontSize=12;fontStyle=1;" + FONT)
    text(f"<b>{name}</b>&nbsp;&nbsp;<font style='font-size:11.5px'>{formula}</font>", x + 30, y + 2, w - 34, 20, 14, DARK)
    if name != "Write":
        cx_ = x + w / 2
        v("", cx_ - 5, RL - 5, 10, 10, f"ellipse;html=1;fillColor={LINE};strokeColor=none;")
        e(None, None, f"endArrow=blockThin;endFill=1;strokeColor={LINE};strokeWidth=2;", sp=(cx_, RL), tp=(cx_, y))

# ---- Read: h·v peaks just before the FP
x, w, y, h = PANELS["Read"]
words = ["the", "boy", "is", "uh", "taking", "a", "cookie"]
dx, gx = 32, x + 22
base = y + 94
v("", gx + 3 * dx + 1, y + 36, 30, 74, f"rounded=0;html=1;strokeColor=none;fillColor={FPHL};opacity=60;")
hv = [8, 10, 40, 0, 9, 7, 10]
for i in range(len(words)):
    if i != 3:
        bar(gx + i * dx + 9, base, hv[i], COOL_S if i == 2 else GREY_BAR, w=14)
hline(gx, gx + len(words) * dx, base, AXIS)
for i, wd in enumerate(words):
    text(wd, gx + i * dx - 4, base + 2, dx + 8, 14, 10.5, "#455A64", "center")
text(f"{serif('h·v')}", x + 8, y + 32, 30, 14, 11, COOL_S)

# ---- Use: next-token distribution before (dashed) / after ablation (filled)
x, w, y, h = PANELS["Use"]
cands = ["uh", "the", "and", "boy", "a", "um"]
before = [42, 30, 20, 16, 12, 20]
after = [20, 30, 20, 16, 12, 10]
base, dx, gx = y + 94, 38, x + 28
for i in range(len(cands)):
    xx = gx + i * dx
    bar(xx, base, before[i], "none", w=16, extra="strokeColor=#90A4AE;dashed=1;strokeWidth=1;")
    bar(xx, base, after[i], WARM_S if cands[i] in ("uh", "um") else GREY_BAR, w=16)
    text(cands[i], xx - 12, base + 2, 40, 14, 10.5, "#455A64", "center")
hline(gx - 8, gx + len(cands) * dx - 14, base, AXIS)

# ---- Write (tall): every position, selected positions, free generation
x, w, y, h = PANELS["Write"]
blocks = (("every position", y + 34), (f"gated by <b><font color='{COOL_S}'>FPpred</font></b> score", y + 122))
for k, (title, ty) in enumerate(blocks):
    text(f"<i>{title}</i>", x + 12, ty, 220, 14, 11, PURPLE)
    base = ty + 66
    n = 7 if k == 0 else 9
    ddx = (w - 40) / n
    sc = [8, 12, 30, 10, 7, 26, 9, 12, 8]
    for i in range(n):
        xx = x + 22 + i * ddx
        if k == 0:
            bar(xx, base, 10, GREY_BAR, w=11)
            text("⊕", xx - 3, base - 30, 17, 14, 12, PURPLE, "center", "fontStyle=1;")
        else:
            over = sc[i] > 18
            bar(xx, base, sc[i], COOL_S if over else GREY_BAR, w=11)
            if over:
                text("⊕", xx - 3, base - sc[i] - 17, 17, 14, 13, WARM_S, "center", "fontStyle=1;")
    hline(x + 14, x + w - 14, base, AXIS)
    if k == 1:
        hline(x + 14, x + w - 14, base - 18, "dashed=1;strokeColor=#7B1FA2;strokeWidth=1;")
        text("top <i>k</i>%", x + w - 60, base - 34, 46, 12, 10, PURPLE, "right")

gy = y + 226
text("<i>free generation</i>", x + 12, gy, 160, 14, 11, PURPLE)
pc = v("prompt", x + 14, gy + 22, 60, 24,
       "rounded=1;arcSize=20;html=1;fillColor=#F5F5F5;strokeColor=#B0BEC5;fontSize=10.5;fontColor=#455A64;whiteSpace=wrap;" + FONT)
gl = x + 92
for i in range(3):
    v("", gl, gy + 23 + i * 8, 24, 6, "rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor=#ECEFF1;strokeColor=#B0BEC5;")
text("⊕", gl + 18, gy + 12, 16, 12, 11, PURPLE, "center", "fontStyle=1;")
e(pc, None, FLOW, tp=(gl, gy + 34))
oc = v("the boy <span style='background-color:#ECEFF1;color:#78909C'>&nbsp;[FP]&nbsp;</span> is taking a cookie …",
       gl + 42, gy + 22, x + w - 14 - (gl + 42), 24,
       "rounded=1;arcSize=20;html=1;fillColor=#FFFFFF;strokeColor=#B0BEC5;fontSize=11;fontColor=#263238;whiteSpace=wrap;" + FONT)
e(None, oc, FLOW, sp=(gl + 26, gy + 34))

xml = ('<mxfile host="drawio"><diagram id="overview" name="Overview">'
       f'<mxGraphModel dx="{W}" dy="{H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       f'fold="1" page="0" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
       "</root></mxGraphModel></diagram></mxfile>")
open(OUT, "w").write(xml)
print(OUT, len(cells), "cells")
