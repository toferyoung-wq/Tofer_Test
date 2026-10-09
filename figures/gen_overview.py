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



W, H = 920, 406
DARK = "#37474F"
NOTE = "#607D8B"
GREY_BAR = "#CFD8DC"


def bar(x, base, h, fill, w=8, extra=""):
    return v("", x, base - h, w, h, f"rounded=0;html=1;strokeColor=none;fillColor={fill};{extra}")


def hline(x0, x1, y, style):
    e(None, None, "endArrow=none;" + style, sp=(x0, y), tp=(x1, y))


# ======================= (a) Directions (compact) =======================
uh = f'<span style="background-color:{FPHL}">&nbsp;uh&nbsp;</span>'
s1 = text(f"the boy is {uh} taking a cookie", 8, 30, 176, 18, 12)
s2 = text("the boy is taking a cookie", 8, 50, 176, 18, 12)
pre = f'<span style="background-color:{COOL_F};border-bottom:2px solid {COOL_S}">&nbsp;is&nbsp;</span>'
s3 = text(f"the boy {pre} uh taking a cookie", 8, 84, 176, 18, 12)

sx, sy, sw = 196, 26, 38
for k, (ox_, oy_) in enumerate(((10, -8), (5, -4), (0, 0))):
    front = k == 2
    for i in range(8):
        hl = i == 2
        fill = ('#FFE0CC' if hl else '#ECEFF1') if front else ('#FFF1E8' if hl else '#F5F7F8')
        stroke = ('#F08A4B' if hl else '#B0BEC5') if front else ('#F6C3A2' if hl else '#D5DCE0')
        v("", sx + ox_, sy + oy_ + i * 11, sw, 8,
          f"rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor={fill};strokeColor={stroke};")
text(f"Llama-3.2-3B · Qwen2.5-1.5B · Qwen2.5-7B <font color='#F08A4B'>(block 21)</font>",
     8, 116, 300, 14, 10.5, NOTE)
for s, y in ((s1, 39), (s2, 59), (s3, 93)):
    e(s, None, FLOW, tp=(sx, y))
m1 = v("−", 256, 40, 18, 18, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=13;fontStyle=1;" + FONT)
m2 = v("−", 256, 84, 18, 18, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=13;fontStyle=1;" + FONT)
e(None, m1, FLOW, sp=(sx + sw + 12, 49))
e(None, m2, FLOW, sp=(sx + sw + 12, 93))
c1 = v("", 304, 34, 30, 27, f"shape=cube;size=6;html=1;fillColor={WARM_F};strokeColor={WARM_S};strokeWidth=1.3;")
c2 = v("", 304, 79, 30, 27, f"shape=cube;size=6;html=1;fillColor={COOL_F};strokeColor={COOL_S};strokeWidth=1.3;")
e(m1, c1, FLOW)
e(m2, c2, FLOW)
text(f"<b>FP</b> <font style='font-size:10.5px' color='{NOTE}'>disfluent − fluent</font>", 340, 34, 150, 27, 13.5, WARM_S)
text(f"<b>FPpred</b> <font style='font-size:10.5px' color='{NOTE}'>pre-FP − pre-ordinary</font>", 340, 79, 170, 27, 13.5, COOL_S)

# (a) -> (b)
e(None, None, "shape=flexArrow;endArrow=classic;html=1;fillColor=#ECEFF1;strokeColor=#B0BEC5;width=9;endSize=5;endWidth=10;",
  sp=(319, 112), tp=(319, 152))
text(f"apply {serif('v')} at block 21", 332, 120, 150, 16, 11, NOTE)

# ======================= (b) Read / Use / Write =======================
stream_y = 162
e(None, None, "endArrow=blockThin;endFill=1;strokeColor=#90A4AE;strokeWidth=2.4;", sp=(8, stream_y), tp=(912, stream_y))
text(f"residual stream {serif('h')}", 800, stream_y - 18, 112, 14, 10.5, NOTE, "right")

top, bot = 180, 398
cols = [
    ("Read", 8, 250, "#F2F8FE", "#CFE6FB", "#7FB0DD", "·", f"project {serif('h·v')}"),
    ("Use", 266, 214, "#F1F9F8", "#CDEBE7", "#6FBFB4", "⊖", f"mean-ablate {serif('v')}"),
    ("Write", 488, 424, "#FAF3FB", "#EBD5F0", "#BF8FCC", "⊕", f"add {serif('ασ')}<sub>F</sub>{serif('v')}"),
]
pos = {}
for name, x, w, body, head, s, op, formula in cols:
    v("", x, top, w, bot - top, f"rounded=1;arcSize=3;html=1;fillColor={body};strokeColor={s};strokeWidth=1.2;")
    v("", x, top, w, 24, f"rounded=1;arcSize=12;html=1;fillColor={head};strokeColor={s};strokeWidth=1.2;")
    text(f"<b>{name}</b>&nbsp;&nbsp;<font style='font-size:11.5px' color='{DARK}'>{formula}</font>",
         x + 10, top + 2, w - 14, 20, 14, DARK)
    hx = x + w / 2 - 10
    hook = v(op, hx, stream_y - 10, 20, 20,
             f"ellipse;html=1;fillColor=#FFFFFF;strokeColor={s};strokeWidth=1.8;fontSize=13;fontStyle=1;" + FONT)
    e(hook, None, f"endArrow=blockThin;endFill=1;strokeColor={s};strokeWidth=1.3;", tp=(hx + 10, top))
    pos[name] = (x, w)


def items(x, y0, w, rows, dy=21, size=12.5):
    for i, r in enumerate(rows):
        text(r, x, y0 + i * dy, w, 18, size, DARK)


def word_strip(x0, y, words, dx, hl=None, size=10.5):
    for i, wd in enumerate(words):
        style = ""
        if hl is not None and i == hl:
            wd = f'<span style="background-color:{COOL_F}">{wd}</span>'
        text(wd, x0 + i * dx - 8, y, dx + 16, 14, size, "#455A64", "center", style)


# ---- Read glyph: projection score per position, pre-FP position stands out
rx, rw = pos["Read"]
words = ["the", "boy", "is", "taking", "a", "cookie"]
base, dx, gx = 290, 34, rx + 26
scores = [8, 10, 30, 9, 7, 11]
for i, sc in enumerate(scores):
    bar(gx + i * dx + 9, base, sc, COOL_S if i == 2 else GREY_BAR, w=10)
hline(gx, gx + 6 * dx, base, "strokeColor=#90A4AE;strokeWidth=1;")
word_strip(gx, base + 2, words, dx, hl=2)
text(f"<i>FP follows</i>", gx + 2 * dx + 18, base - 44, 70, 12, 9.5, COOL_S)
text(f"{serif('h·v')}", rx + 6, base - 34, 22, 14, 11, NOTE)
items(rx + 12, 318, rw - 16, [f"Position readout (AUC) {P}", f"Beyond covariates {P}", f"Surprisal link {P}"], dy=26)

# ---- Use glyph: next-token distribution before (outline) / after (filled)
ux, uw = pos["Use"]
cands = ["uh", "the", "and", "boy"]
base, dx, gx = 290, 44, ux + 32
before = [30, 22, 14, 10]
after = [14, 22, 14, 10]
for i, (b0, b1) in enumerate(zip(before, after)):
    x = gx + i * dx
    bar(x, base, b0, "none", w=14, extra="strokeColor=#90A4AE;dashed=1;strokeWidth=1;")
    bar(x, base, b1, WARM_S if i == 0 else GREY_BAR, w=14)
hline(gx - 6, gx + 4 * dx - 16, base, "strokeColor=#90A4AE;strokeWidth=1;")
word_strip(gx + 7 - 8, base + 2, cands, dx, size=10.5)
text("<i>P(next token)</i>", ux + 6, base - 46, 90, 12, 9.5, NOTE)
text("<i>does P(uh) drop?</i>", gx + 22, base - 34, 100, 12, 9.5, WARM_S)
items(ux + 12, 318, uw - 16, [f"Ablate FP {R}", f"Ablate FPpred {R}{P}"], dy=26)

# ---- Write: two sub-panels with their own glyphs
wx, ww = pos["Write"]
ug = (wx + 10, 168)
et = (wx + 188, ww - 198)
for (bx, bw), title in ((ug, "Ungated · every position"), (et, "Externally timed")):
    v("", bx, 210, bw, 112, "rounded=1;arcSize=5;html=1;fillColor=#FFFFFF;strokeColor=#D7B6E0;")
    text(f"<i>{title}</i>", bx + 8, 212, bw - 10, 16, 10.5, "#7B1FA2")

# ungated glyph: ⊕ above every position
base, dx, gx = 266, 26, ug[0] + 18
for i in range(6):
    x = gx + i * dx
    bar(x, base, 10, GREY_BAR, w=8)
    text("⊕", x - 4, base - 30, 16, 14, 12, "#7B1FA2", "center", "fontStyle=1;")
hline(gx - 6, gx + 6 * dx - 10, base, "strokeColor=#90A4AE;strokeWidth=1;")
items(ug[0] + 8, 278, ug[1] - 10, [f"Add FP {R}{P} {tag('TF · Gen')}", f"Add FPpred {R}{P} {tag('TF')}"], dy=22)

# externally timed glyph: position scores, threshold, ⊕ only above it
base, dx, gx = 268, 22, et[0] + 24
scores = [6, 9, 20, 8, 5, 24, 7, 9]
for i, sc in enumerate(scores):
    x = gx + i * dx
    over = sc > 15
    bar(x, base, sc, COOL_S if over else GREY_BAR, w=8)
    if over:
        text("⊕", x - 4, base - sc - 16, 16, 14, 12, "#7B1FA2", "center", "fontStyle=1;")
thr = base - 15
hline(gx - 6, gx + 8 * dx - 6, base, "strokeColor=#90A4AE;strokeWidth=1;")
hline(gx - 6, gx + 8 * dx - 6, thr, "dashed=1;strokeColor=#7B1FA2;strokeWidth=1;")
text("top <i>k</i>%", gx + 8 * dx - 2, thr - 7, 40, 14, 10, "#7B1FA2")
gate_x = gx + 5 * dx + 4
items(et[0] + 8, 278, et[1] - 10, [
    f"Oracle timing {R}{P} {tag('Gen')}",
    f"Gated by FPpred {R}{P} {tag('TF · Gen')}",
], dy=22)


# free generation strip: prompt -> steered LM -> description with fillers
gy, gh = 328, 62
v("", wx + 10, gy, ww - 20, gh, "rounded=1;arcSize=6;html=1;fillColor=#FFFFFF;strokeColor=#D7B6E0;")
text(f"<i>Free generation</i> {tag('(Gen)')}", wx + 18, gy + 2, 160, 16, 10.5, "#7B1FA2")
p_chip = v("Interviewer: …<br>Participant:", wx + 18, gy + 22, 128, 32,
           "rounded=1;arcSize=12;html=1;fillColor=#F5F5F5;strokeColor=#B0BEC5;fontSize=9.5;fontColor=#455A64;align=left;spacingLeft=4;whiteSpace=wrap;" + FONT)
lx, ly = wx + 166, gy + 22
for i in range(4):
    v("", lx, ly + i * 8, 26, 6, "rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor=#ECEFF1;strokeColor=#B0BEC5;")
text("⊕", lx + 22, ly - 8, 16, 14, 12, "#7B1FA2", "center", "fontStyle=1;")
e(p_chip, None, FLOW, tp=(lx, ly + 15))
fp = lambda w_: f'<span style="background-color:{FPHL}">{w_}</span>'
o_chip = v(f"the boy {fp('uh')} is taking a cookie and {fp('um')} the mother is …", lx + 52, gy + 22, ww - 20 - (lx + 52 - wx - 10) - 10, 32,
           "rounded=1;arcSize=12;html=1;fillColor=#FFFFFF;strokeColor=#B0BEC5;fontSize=10.5;fontColor=#263238;align=left;spacingLeft=4;whiteSpace=wrap;" + FONT)
e(None, o_chip, FLOW, sp=(lx + 28, ly + 15))

# external gate: FPpred direction -> scores in the timed panel
e(c2, None, f"endArrow=blockThin;endFill=1;dashed=1;strokeColor={COOL_S};strokeWidth=1.4;exitX=1;exitY=0.75;",
  pts=[(gate_x, 99)], tp=(gate_x, base - 30 - 18))
text("FPpred score as external gate", 560, 101, 190, 14, 10.5, COOL_S, "left", "fontStyle=2;")

xml = ('<mxfile host="drawio"><diagram id="overview" name="Overview">'
       f'<mxGraphModel dx="{W}" dy="{H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       f'fold="1" page="0" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
       "</root></mxGraphModel></diagram></mxfile>")
open(OUT, "w").write(xml)
print(OUT, len(cells), "cells")
