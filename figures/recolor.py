"""Re-colour overview.drawio with the lab palette (blue #9EAAD1, coral #F59790,
cyan #CDE2E8, lavender #DACFE5, peach #F5DBB6, light blue #C8D4E9, grey #D9D9D9).
Usage: python3 recolor.py in.drawio out.drawio"""
import re
import sys

MAP = {
    # FP direction: coral
    "#FFE0CC": "#FCD9D6", "#F08A4B": "#E8776F", "#FAD7B5": "#FCD9D6",
    # FPpred direction: blue
    "#E3EEF7": "#DDE2F1", "#7FA7C9": "#8593C6",
    # Read panel: cyan
    "#F2F8FE": "#F1F7F9", "#CFE6FB": "#CDE2E8", "#7FB0DD": "#8DB8C5",
    # Use panel: peach
    "#F1F9F8": "#FDF7EE", "#CDEBE7": "#F5DBB6", "#6FBFB4": "#D8AE73",
    # Write panel: lavender
    "#FAF3FB": "#F7F4FA", "#EBD5F0": "#DACFE5", "#BF8FCC": "#A895C6",
    "#D7B6E0": "#CEC3E0", "#7B1FA2": "#6F5C99",
    # neutrals: grey bars, light-blue network layers
    "#CFD8DC": "#D9D9D9", "#ECEFF1": "#E4EAF4", "#F5F7F8": "#EFF3F9",
    "#D5DCE0": "#C8D4E9",
}

src, dst = sys.argv[1], sys.argv[2]
xml = open(src).read()
xml = re.sub(r"#[0-9A-Fa-f]{6}", lambda m: MAP.get(m.group(0).upper(), m.group(0)), xml)
open(dst, "w").write(xml)
print(dst)
