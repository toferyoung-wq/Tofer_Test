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



W, H = 920, 344
DARK = "#37474F"
NOTE = "#607D8B"

# ======================= (a) Direction construction =======================
tab("(a) Direction construction", 8, 4, 200)

uh = f'<span style="background-color:{FPHL}">&nbsp;uh&nbsp;</span>'
s1 = text(f"the boy is {uh} taking a cookie", 8, 36, 180, 20, 12.5)
s2 = text("the boy is taking a cookie", 8, 58, 180, 20, 12.5)
pre = f'<span style="background-color:{COOL_F};border-bottom:2px solid {COOL_S}">&nbsp;is&nbsp;</span>'
s3 = text(f"the boy {pre} uh taking a cookie", 8, 100, 180, 20, 12.5)
text("pre-FP vs. pre-ordinary positions", 8, 120, 190, 16, 10.5, NOTE)

# LM stack
sx, sy, sw = 204, 30, 40
layers = []
for i in range(9):
    hl = i == 2
    layers.append(v("", sx, sy + i * 12, sw, 9,
                    f"rounded=1;arcSize=30;html=1;strokeWidth=0.8;"
                    f"fillColor={'#FFE0CC' if hl else '#ECEFF1'};strokeColor={'#F08A4B' if hl else '#B0BEC5'};"))
text("LM, block 21/28", sx - 30, sy + 110, sw + 60, 14, 10.5, NOTE, "center")
for s, y in ((s1, 46), (s2, 68), (s3, 110)):
    e(s, None, FLOW, tp=(sx, y))

# difference operators and directions
m1 = v("−", 266, 48, 20, 20, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=14;fontStyle=1;" + FONT)
m2 = v("−", 266, 100, 20, 20, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=14;fontStyle=1;" + FONT)
e(None, m1, FLOW, sp=(sx + sw, 58))
e(None, m2, FLOW, sp=(sx + sw, 110))
c1 = v("", 330, 42, 34, 30, f"shape=cube;size=7;html=1;fillColor={WARM_F};strokeColor={WARM_S};strokeWidth=1.3;")
c2 = v("", 330, 94, 34, 30, f"shape=cube;size=7;html=1;fillColor={COOL_F};strokeColor={COOL_S};strokeWidth=1.3;")
e(m1, c1, FLOW)
e(m2, c2, FLOW)
text("<b>FP</b>", 370, 42, 60, 30, 14, WARM_S)
text("<b>FPpred</b>", 370, 94, 70, 30, 14, COOL_S)
text(f"{serif('h')}<sub>disfl</sub> − {serif('h')}<sub>fluent</sub>", 252, 24, 90, 16, 11, NOTE, "center")
text(f"{serif('h')}<sub>pre-FP</sub> − {serif('h')}<sub>pre-ord</sub>", 248, 124, 100, 16, 11, NOTE, "center")

# residual space glyph
text("residual space (schematic)", 474, 4, 190, 16, 10.5, NOTE, "center", "fontStyle=2;")
v("", 486, 22, 168, 136, "ellipse;html=1;fillColor=#FAFAFA;strokeColor=#CFD8DC;dashed=1;")
ox, oy = 512, 136
for (x, y) in [(530, 60), (552, 84), (566, 50), (536, 104), (560, 116), (582, 76), (548, 40), (522, 84)]:
    v("", x - 4, y - 4, 8, 8, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#90A4AE;strokeWidth=1;")
for (x, y) in [(604, 100), (618, 118), (596, 122), (626, 92), (612, 76)]:
    text("★", x - 7, y - 8, 14, 14, 13, WARM_S, "center")
e(None, None, "endArrow=none;dashed=1;strokeColor=#9DC3E6;strokeWidth=1;", sp=(496, oy), tp=(652, oy))
e(None, None, f"endArrow=blockThin;endFill=1;strokeColor={WARM_S};strokeWidth=2.2;", sp=(ox, oy), tp=(ox, 34))
e(None, None, f"endArrow=blockThin;endFill=1;strokeColor={COOL_S};strokeWidth=2.2;", sp=(ox, oy), tp=(644, oy))
text(f"{serif('v')}<sub>FP</sub>", ox + 4, 26, 34, 16, 12, WARM_S)
text(f"{serif('v')}<sub>FPpred</sub>", 600, oy + 2, 56, 16, 12, COOL_S)
text(f'<span style="color:{WARM_S}">★</span> upcoming FP&nbsp;&nbsp;<span style="color:#90A4AE">○</span> ordinary',
     486, 156, 168, 14, 10.5, NOTE, "center")

# setup / legend box
v("", 694, 18, 218, 146, "rounded=1;arcSize=5;html=1;fillColor=#FFFFFF;strokeColor=#CFD8DC;")
text(f"<b>Data</b><br><font color='{NOTE}'>Pitt Cookie Theft descriptions<br>(older adults)</font>",
     704, 24, 200, 44, 11.5, DARK, "left", "verticalAlign=top;")
text(f"<b>Models</b><br><font color='{NOTE}'>Llama-3.2-3B · Qwen2.5-1.5B / -7B</font>",
     704, 70, 206, 32, 11.5, DARK, "left", "verticalAlign=top;")
text(f"<b>Scored for</b><br>{R} <font color='{NOTE}'>rate (how many)</font><br>{P} <font color='{NOTE}'>placement (where)</font>",
     704, 108, 206, 50, 11.5, DARK, "left", "verticalAlign=top;")

# (a) -> (b)
e(None, None, "shape=flexArrow;endArrow=classic;html=1;fillColor=#ECEFF1;strokeColor=#B0BEC5;width=9;endSize=5;endWidth=10;",
  sp=(347, 140), tp=(347, 206))
text(f"apply {serif('v')} at block 21", 358, 164, 140, 18, 11.5, NOTE)

# ======================= (b) Interventions =======================
tab("(b) Interventions on the residual stream", 8, 176, 290)
stream_y = 216
e(None, None, "endArrow=blockThin;endFill=1;strokeColor=#90A4AE;strokeWidth=2.4;", sp=(8, stream_y), tp=(912, stream_y))
text(f"{serif('h')}", 900, stream_y - 20, 14, 14, 12, NOTE)

top, bot = 234, 338
cols = [
    ("Read", 8, 196, "#E6F3FF", "#9DC3E6", "·", f"project {serif('h·v')}"),
    ("Use", 212, 196, "#E0F2F1", "#80CBC4", "⊖", f"{serif('h')} − ({serif('h·v')} − {serif('μ')}){serif('v')}"),
    ("Write", 416, 496, "#F3E5F5", "#CE93D8", "⊕", f"{serif('h')} + {serif('ασ')}<sub>F</sub>{serif('v')}"),
]
pos = {}
for name, x, w, f, s, op, formula in cols:
    v("", x, top, w, bot - top, f"rounded=1;arcSize=4;html=1;fillColor={f};strokeColor={s};")
    text(f"<b>{name}</b>&nbsp;&nbsp;<font style='font-size:12px' color='{NOTE}'>{formula}</font>",
         x + 8, top + 4, w - 12, 20, 13.5, DARK)
    hx = x + w / 2 - 10
    hook = v(op, hx, stream_y - 10, 20, 20,
             f"ellipse;html=1;fillColor=#FFFFFF;strokeColor={s};strokeWidth=1.8;fontSize=13;fontStyle=1;" + FONT)
    e(hook, None, f"endArrow=blockThin;endFill=1;strokeColor={s};strokeWidth=1.3;", tp=(hx + 10, top))
    pos[name] = (x, w)


def items(x, y0, w, rows, dy=24, size=12.5):
    for i, r in enumerate(rows):
        text(r, x, y0 + i * dy, w, 20, size, DARK)


x, w = pos["Read"]
items(x + 10, 262, w - 12, [f"Position readout {P}", f"Beyond covariates {P}", f"Surprisal link {P}"])
x, w = pos["Use"]
items(x + 10, 262, w - 12, [f"Ablate FP {R}", f"Ablate FPpred {R}{P}"])

wx, ww = pos["Write"]
ug = (wx + 8, 158)
et = (wx + 174, ww - 182)
for (bx, bw), title in ((ug, "Ungated"), (et, "Externally timed")):
    v("", bx, 260, bw, 72, "rounded=1;arcSize=6;html=1;fillColor=#FFFFFF;strokeColor=#CE93D8;")
    text(f"<i>{title}</i>", bx + 8, 262, bw - 10, 16, 11, "#7B1FA2")
items(ug[0] + 8, 282, ug[1] - 10, [f"Add FP {R}{P} {tag('TF · Gen')}", f"Add FPpred {R}{P} {tag('TF')}"], dy=22)
items(et[0] + 8, 282, 200, [f"Oracle timing {R}{P} {tag('Gen')}", f"Gated by FPpred {R}{P} {tag('TF · Gen')}"], dy=22)

# gate glyph: FPpred score per position, threshold, inject where above
gx0, gbase = et[0] + et[1] - 104, 326
scores = [9, 13, 30, 11, 8, 25, 10]
for i, hgt in enumerate(scores):
    bx = gx0 + i * 13
    over = hgt > 20
    v("", bx, gbase - hgt, 8, hgt, f"rounded=0;html=1;strokeColor=none;fillColor={COOL_S if over else '#CFD8DC'};")
    if over:
        text("⊕", bx - 4, gbase - hgt - 14, 16, 12, 11, "#7B1FA2", "center", "fontStyle=1;")
thr = gbase - 19
e(None, None, "endArrow=none;dashed=1;strokeColor=#7B1FA2;strokeWidth=1;", sp=(gx0 - 4, thr), tp=(gx0 + 92, thr))
text("top <i>k</i>%", gx0 - 44, thr - 8, 40, 14, 10, "#7B1FA2", "right")

# external gate: FPpred direction -> gate glyph
gate_x = gx0 + 30
e(None, None, f"endArrow=blockThin;endFill=1;dashed=1;strokeColor={COOL_S};strokeWidth=1.4;",
  sp=(644, oy), pts=[(664, oy), (664, 176), (gate_x, 176)], tp=(gate_x, gbase - 46))
text("FPpred score as external gate", 680, 178, 180, 14, 10.5, COOL_S, "left", "fontStyle=2;")

xml = ('<mxfile host="drawio"><diagram id="overview" name="Overview">'
       f'<mxGraphModel dx="{W}" dy="{H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       f'fold="1" page="0" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
       "</root></mxGraphModel></diagram></mxfile>")
open(OUT, "w").write(xml)
print(OUT, len(cells), "cells")
