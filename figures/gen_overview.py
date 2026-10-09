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



W, H = 920, 340
DARK = "#37474F"
NOTE = "#607D8B"
GREY_BAR = "#CFD8DC"
PURPLE = "#7B1FA2"


def bar(x, base, h, fill, w=8, extra=""):
    return v("", x, base - h, w, h, f"rounded=0;html=1;strokeColor=none;fillColor={fill};{extra}")


def hline(x0, x1, y, style):
    e(None, None, "endArrow=none;" + style, sp=(x0, y), tp=(x1, y))


def item(s_, x, y, w, size=12, color=DARK, extra=""):
    return text(s_, x, y, w, 18, size, color, "left", extra)


# ---------------- grid geometry ----------------
GX = 304                       # grid left edge
COLS = {"Read": (GX, 176), "Use": (GX + 180, 140), "Write": (GX + 324, 912 - GX - 324)}
HEAD_Y, HEAD_H = 8, 22
GLY_Y, GLY_H = 30, 76
ROWS = {"FP": (112, 80), "FPpred": (196, 62), "LM": (262, 32)}
GRID_BOT = 294
ROW_TINT = {"FP": "#FFF5EE", "FPpred": "#F0F6FC", "LM": "#F6F7F8"}
COL_STYLE = {"Read": ("#CFE6FB", "#7FB0DD", "·", f"project {serif('h·v')}"),
             "Use": ("#CDEBE7", "#6FBFB4", "⊖", f"mean-ablate {serif('v')}"),
             "Write": ("#EBD5F0", "#BF8FCC", "⊕", f"add {serif('ασ')}<sub>F</sub>{serif('v')}")}

# row bands (span whole grid)
for r, (y, h) in ROWS.items():
    v("", GX, y, 912 - GX, h, f"rounded=0;html=1;fillColor={ROW_TINT[r]};strokeColor=none;")
# column headers, glyph panels, column frames
for c, (x, w) in COLS.items():
    head, stroke, op, formula = COL_STYLE[c]
    v("", x, HEAD_Y, w, GRID_BOT - HEAD_Y, f"rounded=1;arcSize=2;html=1;fillColor=none;strokeColor={stroke};strokeWidth=1.2;")
    v("", x, HEAD_Y, w, HEAD_H, f"rounded=1;arcSize=14;html=1;fillColor={head};strokeColor={stroke};strokeWidth=1.2;")
    v(op, x + 6, HEAD_Y + 2, 18, 18, f"ellipse;html=1;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=1.5;fontSize=12;fontStyle=1;" + FONT)
    text(f"<b>{c}</b>&nbsp;&nbsp;<font style='font-size:11px' color='{DARK}'>{formula}</font>", x + 28, HEAD_Y + 1, w - 30, 20, 13.5, DARK)
# row separators
for r, (y, h) in ROWS.items():
    hline(GX, 912, y, "strokeColor=#E0E0E0;strokeWidth=1;")
hline(GX, 912, GRID_BOT, "strokeColor=#E0E0E0;strokeWidth=1;")


def cell(col, row):
    x, w = COLS[col]
    y, h = ROWS[row]
    return x + 8, y, w - 12, h


# ---------------- column glyphs ----------------
# Read: h·v peaks before the FP, surprisal peaks on the word after it
x, w = COLS["Read"]
words = ["boy", "is", "uh", "taking", "a"]
dx, gx = 26, x + 40
b1, b2 = GLY_Y + 32, GLY_Y + 60
hv = [8, 20, 0, 7, 5]
sp_ = [7, 6, 0, 18, 6]
v("", gx + 2 * dx + 1, GLY_Y + 6, 24, 70, f"rounded=0;html=1;strokeColor=none;fillColor={FPHL};opacity=60;")
for i in range(len(words)):
    if i == 2:
        continue
    bar(gx + i * dx + 8, b1, hv[i], COOL_S if i == 1 else GREY_BAR, w=9)
    bar(gx + i * dx + 8, b2, sp_[i], "#78909C" if i == 3 else GREY_BAR, w=9)
for yy in (b1, b2):
    hline(gx, gx + len(words) * dx, yy, "strokeColor=#90A4AE;strokeWidth=1;")
for i, wd in enumerate(words):
    text(wd, gx + i * dx - 6, b2 + 1, dx + 12, 12, 9.5, "#455A64", "center")
text(f"{serif('h·v')}", x + 4, b1 - 13, 36, 12, 10.5, COOL_S)
text("surprisal", x + 2, b2 - 13, 40, 12, 9, "#78909C")

# Use: next-token distribution before (dashed) / after (filled)
x, w = COLS["Use"]
cands = ["uh", "the", "and"]
base, dx, gx = GLY_Y + 58, 38, x + 26
for i, (b0, b1_) in enumerate(zip([26, 18, 12], [12, 18, 12])):
    xx = gx + i * dx
    bar(xx, base, b0, "none", w=13, extra="strokeColor=#90A4AE;dashed=1;strokeWidth=1;")
    bar(xx, base, b1_, WARM_S if i == 0 else GREY_BAR, w=13)
    text(cands[i], xx - 10, base + 1, 33, 12, 9.5, "#455A64", "center")
hline(gx - 6, gx + 3 * dx - 16, base, "strokeColor=#90A4AE;strokeWidth=1;")
text("<i>P(next token)</i>", x + 6, GLY_Y + 2, 90, 12, 9, NOTE)
text("<i>P(uh) drops?</i>", gx + 26, GLY_Y + 18, 80, 12, 9, WARM_S)

# Write: every position vs. selected positions
x, w = COLS["Write"]
base = GLY_Y + 60
text("<i>every position</i>", x + 10, GLY_Y + 2, 110, 12, 9.5, PURPLE)
gx = x + 16
for i in range(5):
    xx = gx + i * 22
    bar(xx, base, 8, GREY_BAR, w=8)
    text("⊕", xx - 4, base - 26, 16, 14, 11, PURPLE, "center", "fontStyle=1;")
hline(gx - 4, gx + 5 * 22 - 8, base, "strokeColor=#90A4AE;strokeWidth=1;")
text("<i>selected positions</i>", x + 140, GLY_Y + 2, 130, 12, 9.5, PURPLE)
gx = x + 146
sc = [6, 9, 22, 7, 5, 18, 8]
thr = base - 13
for i, h_ in enumerate(sc):
    xx = gx + i * 18
    over = h_ > 13
    bar(xx, base, h_, COOL_S if over else GREY_BAR, w=8)
    if over:
        text("⊕", xx - 4, base - h_ - 15, 16, 14, 11, PURPLE, "center", "fontStyle=1;")
hline(gx - 4, gx + 7 * 18 - 6, base, "strokeColor=#90A4AE;strokeWidth=1;")
hline(gx - 4, gx + 7 * 18 - 6, thr, "dashed=1;strokeColor=#7B1FA2;strokeWidth=1;")

# ---------------- cell contents ----------------
def tagged(name, dots, tags=""):
    return f"{name} {dots}" + (f" {tag(tags)}" if tags else "")


cx, cy, cw, ch = cell("Read", "FP")
item(tagged("Position readout", P) + f" {tag('(comparison)')}", cx, cy + 8, cw, 12, "#78909C")
cx, cy, cw, ch = cell("Use", "FP")
item(tagged("Ablate FP", R), cx, cy + 8, cw)
cx, cy, cw, ch = cell("Write", "FP")
item(tagged("Add FP", R + P, "TF · Gen"), cx, cy + 6, cw)
item(tagged("Oracle timing", R + P, "Gen"), cx, cy + 30, cw)
gated = item(tagged("Gated FP injection", R + P, "TF · Gen"), cx, cy + 54, cw)

cx, cy, cw, ch = cell("Read", "FPpred")
item(tagged("Position readout", P), cx, cy + 8, cw)
item(tagged("Beyond covariates", P), cx, cy + 32, cw)
cx, cy, cw, ch = cell("Use", "FPpred")
item(tagged("Ablate FPpred", R + P), cx, cy + 8, cw)
cx, cy, cw, ch = cell("Write", "FPpred")
item(tagged("Add FPpred", R + P, "TF"), cx, cy + 8, cw)
gate_lbl = item(f"<i>score as gate</i>", cx + 128, cy + 33, 110, 11, COOL_S)

cx, cy, cw, ch = cell("Read", "LM")
item(tagged("Surprisal link", P), cx, cy + 7, cw)
for c in ("Use", "Write"):
    cx, cy, cw, ch = cell(c, "LM")
    text("—", cx, cy + 7, cw, 18, 12, "#B0BEC5", "center")

# gate: FPpred score selects positions for the FP injection
gx_ = COLS["Write"][0] + 128
e(None, None, f"endArrow=blockThin;endFill=1;dashed=1;strokeColor={COOL_S};strokeWidth=1.4;",
  sp=(gx_, ROWS["FPpred"][0] + 40), tp=(gx_, ROWS["FP"][0] + 73))


# free generation, used by the Gen-tagged Write analyses
wx_, ww_ = COLS["Write"]
gy = GRID_BOT + 6
v("", wx_, gy, ww_, 34, "rounded=1;arcSize=10;html=1;fillColor=#FAF3FB;strokeColor=#BF8FCC;strokeWidth=1.2;")
text(f"<b>Gen</b>", wx_ + 6, gy + 8, 34, 18, 11.5, PURPLE)
pc = v("prompt", wx_ + 40, gy + 7, 52, 20,
       "rounded=1;arcSize=20;html=1;fillColor=#F5F5F5;strokeColor=#B0BEC5;fontSize=9;fontColor=#455A64;whiteSpace=wrap;" + FONT)
lx = wx_ + 104
for i in range(3):
    v("", lx, gy + 8 + i * 7, 22, 5, "rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor=#ECEFF1;strokeColor=#B0BEC5;")
text("⊕", lx + 16, gy + 1, 16, 12, 10, PURPLE, "center", "fontStyle=1;")
e(pc, None, FLOW, tp=(lx, gy + 17))
oc = v("the boy <span style='background-color:#ECEFF1;color:#78909C'>&nbsp;[FP]&nbsp;</span> is …", lx + 40, gy + 7, ww_ - (lx + 40 - wx_) - 8, 20,
       "rounded=1;arcSize=20;html=1;fillColor=#FFFFFF;strokeColor=#B0BEC5;fontSize=10;fontColor=#263238;whiteSpace=wrap;" + FONT)
e(None, oc, FLOW, sp=(lx + 24, gy + 17))

# ---------------- left: direction construction ----------------
text(f"<b>Three base LMs</b><br><font color='{NOTE}'>Llama-3.2-3B<br>Qwen2.5-1.5B · Qwen2.5-7B</font><br>"
     f"<font color='#F08A4B'>residual stream, block 21</font>", 8, 18, 220, 72, 11.5, DARK, "left", "verticalAlign=top;")

uh = f'<span style="background-color:{FPHL}">&nbsp;uh&nbsp;</span>'
pre = f'<span style="background-color:{COOL_F};border-bottom:2px solid {COOL_S}">&nbsp;is&nbsp;</span>'
s1 = text(f"the boy is {uh} taking a cookie", 8, 124, 166, 18, 11.5)
s2 = text("the boy is taking a cookie", 8, 144, 166, 18, 11.5)
text("disfluent − fluent pairs", 8, 164, 166, 14, 10, NOTE)
s3 = text(f"the boy {pre} uh taking a cookie", 8, 208, 166, 18, 11.5)
text("pre-FP − pre-ordinary positions", 8, 228, 166, 14, 10, NOTE)

sx, sy, sw = 182, 118, 30
for k, (ox_, oy_) in enumerate(((8, -6), (4, -3), (0, 0))):
    front = k == 2
    for i in range(11):
        hl = i == 3
        fill = ('#FFE0CC' if hl else '#ECEFF1') if front else ('#FFF1E8' if hl else '#F5F7F8')
        stroke = ('#F08A4B' if hl else '#B0BEC5') if front else ('#F6C3A2' if hl else '#D5DCE0')
        v("", sx + ox_, sy + oy_ + i * 13, sw, 8,
          f"rounded=1;arcSize=30;html=1;strokeWidth=0.8;fillColor={fill};strokeColor={stroke};")
for s_, y in ((s1, 133), (s2, 153), (s3, 217)):
    e(s_, None, FLOW, tp=(sx, y))

ROWC = {r: y + h / 2 for r, (y, h) in ROWS.items()}
m1 = v("−", 228, ROWC["FP"] - 9, 18, 18, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=13;fontStyle=1;" + FONT)
m2 = v("−", 228, ROWC["FPpred"] - 9, 18, 18, "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#546E7A;fontSize=13;fontStyle=1;" + FONT)
e(None, m1, FLOW, sp=(sx + sw + 8, ROWC["FP"]))
e(None, m2, FLOW, sp=(sx + sw + 8, ROWC["FPpred"]))
c1 = v("", 256, ROWC["FP"] - 12, 26, 24, f"shape=cube;size=6;html=1;fillColor={WARM_F};strokeColor={WARM_S};strokeWidth=1.3;")
c2 = v("", 256, ROWC["FPpred"] - 12, 26, 24, f"shape=cube;size=6;html=1;fillColor={COOL_F};strokeColor={COOL_S};strokeWidth=1.3;")
e(m1, c1, FLOW)
e(m2, c2, FLOW)
text("<b>FP</b>", 244, ROWC["FP"] - 30, 50, 16, 12.5, WARM_S, "center")
text("<b>FPpred</b>", 236, ROWC["FPpred"] - 30, 66, 16, 12.5, COOL_S, "center")
e(c1, None, f"endArrow=blockThin;endFill=1;strokeColor={WARM_S};strokeWidth=2.4;", tp=(GX, ROWC["FP"]))
e(c2, None, f"endArrow=blockThin;endFill=1;strokeColor={COOL_S};strokeWidth=2.4;", tp=(GX, ROWC["FPpred"]))

# LM's own output row
lm_lbl = text(f"LM's own {serif('P')}(filler)", 150, ROWC["LM"] - 9, 140, 18, 11.5, NOTE, "right")
e(None, None, "endArrow=blockThin;endFill=1;strokeColor=#90A4AE;strokeWidth=1.6;", sp=(sx + 15, sy + 10 * 13 + 10),
  pts=[(sx + 15, ROWC["LM"] + 12), (GX - 30, ROWC["LM"] + 12)], tp=(GX, ROWC["LM"] + 12))

xml = ('<mxfile host="drawio"><diagram id="overview" name="Overview">'
       f'<mxGraphModel dx="{W}" dy="{H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
       f'fold="1" page="0" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) +
       "</root></mxGraphModel></diagram></mxfile>")
open(OUT, "w").write(xml)
print(OUT, len(cells), "cells")
