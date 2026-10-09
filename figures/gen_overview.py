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
    return f'<font style="font-size:9px" color="#78909C">{s}</font>'


def serif(s):
    return f'<i style="font-family:Times New Roman">{s}</i>'


def tab(label, x, y, w):
    return v(label, x, y, w, 18, "rounded=0;fillColor=#EEEEEE;strokeColor=none;html=1;" + FONT +
             "fontSize=11;fontStyle=3;fontColor=#37474F;align=left;spacingLeft=6;")


# ---------- A. Direction construction ----------
tab("Direction Construction", 8, 6, 160)
uh = f'<span style="background-color:{FPHL}">&nbsp;uh&nbsp;</span>'
s1 = text(f"the boy is {uh} taking a cookie", 8, 36, 150, 18, 11)
s2 = text("the boy is taking a cookie", 8, 62, 150, 18, 11)
# LM stack
stack_x, stack_y = 168, 30
layers = []
for i in range(6):
    hl = i == 1
    layers.append(v("", stack_x, stack_y + i * 9, 38, 7,
                    f"rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor={'#FFE0CC' if hl else '#ECEFF1'};"
                    f"strokeColor={'#F08A4B' if hl else '#B0BEC5'};"))
text("LM", stack_x, stack_y + 54, 38, 12, 10, "#546E7A", "center", "fontStyle=1;")
text("block 21/28", stack_x + 40, stack_y + 4, 60, 12, 9, "#F08A4B")
e(s1, None, FLOW, tp=(stack_x, stack_y + 22))
e(s2, None, FLOW, tp=(stack_x, stack_y + 36))
minus = v("−", stack_x + 10, 104, 18, 18, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=13;fontStyle=1;" + FONT)
e(None, minus, FLOW, sp=(stack_x + 19, stack_y + 68))
text(f"{serif('h')}<sub>disfl</sub> − {serif('h')}<sub>fluent</sub>", 96, 106, 76, 14, 10, "#546E7A", "right")

dirs = [
    ("FP", WARM_F, WARM_S, "", "disfluent − fluent"),
    ("PSEUDO", "#EEEEEE", "#9E9E9E", "", "optional-word pairs (<i>well, so</i>)"),
    ("FP<sub>⊥</sub>", WARM_F, WARM_S, "dashed=1;", "FP − PSEUDO component"),
    ("FPpred", COOL_F, COOL_S, "", "pre-FP − pre-ordinary positions"),
]
cubes = []
for i, (name, f, s, ex, note) in enumerate(dirs):
    y = 132 + i * 30
    cubes.append(v("", 14, y, 22, 20, f"shape=cube;size=5;html=1;fillColor={f};strokeColor={s};{ex}"))
    text(f"<b>{name}</b>&nbsp; <font color='#607D8B' style='font-size:9.5px'>{note}</font>", 42, y, 200, 20, 11)
e(minus, None, FLOW + "exitX=0.5;exitY=1;", tp=(25, 130), pts=[(stack_x + 19, 124), (25, 124)])
text("Llama-3.2-3B<br>Qwen2.5-1.5B / -7B", 8, 84, 90, 26, 9.5, "#78909C")

# ---------- B. Activation space ----------
tab("Activation Space", 262, 6, 120)
v("", 266, 32, 176, 200, "ellipse;html=1;fillColor=#FAFAFA;strokeColor=#CFD8DC;dashed=1;")
ox, oy = 296, 196
stars = [(388, 150), (404, 170), (376, 172), (414, 140), (396, 124), (420, 162)]
circs = [(312, 92), (334, 120), (350, 80), (318, 146), (346, 160), (366, 108), (330, 70), (300, 120), (358, 140)]
for (x, y) in circs:
    v("", x - 4, y - 4, 8, 8, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#90A4AE;strokeWidth=1;")
for (x, y) in stars:
    text("★", x - 7, y - 8, 14, 14, 13, WARM_S, "center")
# projection axis along FPpred
e(None, None, "endArrow=none;dashed=1;strokeColor=#7FA7C9;strokeWidth=1;", sp=(282, oy), tp=(436, oy))
e(None, None, f"endArrow=blockThin;endFill=1;strokeColor={COOL_S};strokeWidth=2;", sp=(ox, oy), tp=(424, oy))
e(None, None, f"endArrow=blockThin;endFill=1;strokeColor={WARM_S};strokeWidth=2;", sp=(ox, oy), tp=(ox, 52))
e(None, None, "endArrow=blockThin;endFill=1;strokeColor=#B0BEC5;strokeWidth=1.2;dashed=1;", sp=(ox, oy), tp=(330, 212))
text(f"{serif('v')}<sub>FP</sub>", ox + 3, 46, 30, 14, 11, WARM_S)
fppred_lbl = text(f"{serif('v')}<sub>FPpred</sub>", 400, oy + 2, 44, 14, 11, COOL_S)
text("matched random controls", 318, 214, 110, 12, 9, "#90A4AE")
text("schematic", 380, 32, 60, 12, 8.5, "#B0BEC5", "right", "fontStyle=2;")
text(f'<span style="color:{WARM_S}">★</span> upcoming FP&nbsp;&nbsp; <span style="color:#90A4AE">○</span> ordinary',
     266, 236, 180, 12, 9.5, "#607D8B", "center")

# ---------- C. Read / Use / Write ----------
cx0, top, bot = 456, 62, 238
stream_y = 44
text(f"residual stream {serif('h')}", cx0, 24, 120, 14, 10, "#546E7A")
e(None, None, "endArrow=blockThin;endFill=1;strokeColor=#90A4AE;strokeWidth=2.2;", sp=(cx0, stream_y), tp=(996, stream_y))

cols = [
    ("Read", cx0, 118, "#E6F3FF", "#9DC3E6", "·", f"{serif('h·v')}"),
    ("Use", cx0 + 124, 128, "#E0F2F1", "#80CBC4", "⊖", f"{serif('h')} − ({serif('h·v')} − {serif('μ')}){serif('v')}"),
    ("Write", cx0 + 258, 282, "#F3E5F5", "#CE93D8", "⊕", f"{serif('h')} + {serif('ασ')}<sub>F</sub>{serif('v')}"),
]
colpos = {}
for name, x, w, f, s, op, formula in cols:
    v("", x, top, w, bot - top, f"rounded=1;arcSize=3;html=1;fillColor={f};strokeColor={s};dashed=1;")
    text(f"<b>{name}</b>", x + 6, top + 4, 50, 16, 12, "#37474F")
    text(formula, x + 6, top + 20, w - 12, 14, 10.5, "#37474F")
    hx = x + w / 2 - 9
    hook = v(op, hx, stream_y - 9, 18, 18, f"ellipse;html=1;fillColor=#FFFFFF;strokeColor={s};strokeWidth=1.5;fontSize=12;fontStyle=1;" + FONT)
    e(hook, None, f"endArrow=blockThin;endFill=1;strokeColor={s};strokeWidth=1.2;", tp=(hx + 9, top))
    colpos[name] = (x, w)


def items(x, y0, w, rows, dy=19, size=10.5):
    for i, r in enumerate(rows):
        text(r, x, y0 + i * dy, w, 16, size)


rx, rw = colpos["Read"]
items(rx + 6, 104, rw - 8, [f"Position readout {P}", f"Beyond covariates {P}", f"Surprisal link {P}"])
ux, uw = colpos["Use"]
items(ux + 6, 104, uw - 8, [f"Ablate FP {R}", f"FP<sub>⊥</sub> specificity {R}", f"Ablate FPpred {R}{P}"])

wx, ww = colpos["Write"]
# sub-boxes
ugx, ugw = wx + 6, 96
etx, etw = wx + 108, ww - 114
v("", ugx, 98, ugw, 134, "rounded=1;arcSize=4;html=1;fillColor=#FFFFFF;strokeColor=#CE93D8;opacity=80;")
v("", etx, 98, etw, 134, "rounded=1;arcSize=4;html=1;fillColor=#FFFFFF;strokeColor=#CE93D8;opacity=80;")
text("<i>Ungated</i>", ugx + 4, 100, 80, 14, 10, "#7B1FA2")
text("<i>Externally timed</i>", etx + 4, 100, 120, 14, 10, "#7B1FA2")
items(ugx + 4, 118, ugw - 6, [f"Add FP {R}{P}<br>{tag('TF · Gen')}", f"Add FPpred {R}{P}<br>{tag('TF')}"], dy=34, size=10.5)
items(etx + 4, 116, etw - 6, [
    f"Oracle timing {R}{P} {tag('Gen')}<br>{tag('timing source: human transcript')}",
    f"Gated by FPpred {R}{P} {tag('TF · Gen')}<br>{tag('timing source: FPpred score')}",
], dy=30, size=10.5)

# mini gate glyph: score bars + threshold + ⊕ on bars above it
gx0, gbase = etx + 10, 226
scores = [10, 14, 30, 12, 9, 26, 11]
bars = []
for i, hgt in enumerate(scores):
    bx = gx0 + i * 14
    over = hgt > 20
    bars.append(v("", bx, gbase - hgt, 8, hgt,
                  f"rounded=0;html=1;strokeColor=none;fillColor={COOL_S if over else '#CFD8DC'};"))
    if over:
        text("⊕", bx - 4, gbase - hgt - 14, 16, 12, 10, "#7B1FA2", "center", "fontStyle=1;")
thr_y = gbase - 20
e(None, None, "endArrow=none;dashed=1;strokeColor=#7B1FA2;strokeWidth=1;", sp=(gx0 - 4, thr_y), tp=(gx0 + 7 * 14, thr_y))
text("top <i>k</i>%", gx0 + 7 * 14 + 2, thr_y - 7, 40, 14, 9, "#7B1FA2")
gate_tgt = bars[0]

# external gate: from v_FPpred (activation space) to the score bars, routed under the columns
e(fppred_lbl, None, f"endArrow=blockThin;endFill=1;dashed=1;strokeColor={COOL_S};strokeWidth=1.3;exitX=1;exitY=0.5;",
  pts=[(452, oy + 9), (452, 244), (gx0 + 40, 244)], tp=(gx0 + 40, gbase + 1), value="")
text("external gate", 600, 239, 70, 11, 9, COOL_S, "center", "fontStyle=2;labelBackgroundColor=#FFFFFF;")

# ---------- D. Rate vs placement ----------
by0 = 256
tab("Rate vs. Placement", 8, by0, 130)
text(f"{serif('P')}(filler at {serif('t')}) = <b><font color='{AMBER}'>{serif('g')}</font></b> · "
     f"<b><font color='{TEAL}'>{serif('f')}</font></b>(context<sub>{serif('t')}</sub>)",
     390, by0, 220, 18, 12, "#263238", "center")

words = ["the", "boy", "is", "", "taking", "a", "cookie"]
base = [9, 7, 8, 12, 8, 6, 9]


def strip(x0, color, mode, title, sub):
    v("", x0, by0 + 22, 482, 94, f"rounded=1;arcSize=4;html=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=1.2;")
    text(f"<b><font color='{color}'>{title}</font></b>", x0 + 8, by0 + 26, 140, 14, 11)
    bl = by0 + 84
    for i, (wd, b) in enumerate(zip(words, base)):
        cx = x0 + 210 + i * 36
        fp = wd == ""
        if fp:
            v("", cx - 3, bl - 46, 26, 66, f"rounded=0;html=1;strokeColor=none;fillColor={FPHL};opacity=70;")
        inc = round(b * 0.9) if mode == "rate" else (22 if fp else 0)
        v("", cx + 5, bl - b, 10, b, "rounded=0;html=1;strokeColor=none;fillColor=#B0BEC5;")
        if inc:
            v("", cx + 5, bl - b - inc, 10, inc, f"rounded=0;html=1;strokeColor=none;fillColor={color};")
        text(wd if wd else "▢", cx - 6, bl + 2, 32, 12, 9.5, "#455A64", "center")
    text(sub, x0 + 8, by0 + 44, 190, 60, 9.5, "#607D8B", "left", "verticalAlign=top;")


strip(8, AMBER, "rate", "Rate (how many, g)",
      "all positions rise together<br><br>net Δlog P(filler)<br>valid FPs per output")
strip(514, TEAL, "place", "Placement (where, f)",
      "only FP positions rise<br><br>FP vs. matched ordinary sites<br>O/E of generated FPs")

xml = ('<mxfile host="drawio"><diagram id="overview" name="Overview">'
       '<mxGraphModel dx="1000" dy="380" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       'fold="1" page="0" pageScale="1" pageWidth="1000" pageHeight="380" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
       "</root></mxGraphModel></diagram></mxfile>")
open(OUT, "w").write(xml)
print(OUT, len(cells), "cells")
