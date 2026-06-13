#!/usr/bin/env python3
"""Generate examples/demo.gif — a looping terminal-cast demo of the resume-agent
pipeline (gap analysis -> rewrite -> ATS scan, score climbing 88 -> 96).

Pure Pillow: text is drawn with a monospace font; all decorative marks (traffic
dots, step triangles, progress bars, checkmark) are drawn as primitives so the
output is crisp and does not depend on exotic glyph coverage. Rendered at 2x and
downscaled for clean anti-aliasing.

    python examples/make_demo_gif.py
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image, ImageDraw, ImageFont

W, H, S = 760, 460, 2  # logical size, supersample factor
OUT = Path(__file__).resolve().parent / "demo.gif"

# ---- colors ----
BG = (27, 27, 31)
TBAR = (37, 37, 43)
SEP = (15, 15, 18)
TXT = (231, 231, 234)
DIM = (199, 199, 205)
MUT = (139, 139, 148)
TEAL = (43, 212, 160)
TEAL2 = (78, 230, 176)
AMB = (243, 183, 101)
TRACK = (52, 52, 60)
BOXLINE = (58, 58, 66)
RED, AMD, GRN = (255, 95, 86), (255, 189, 46), (39, 201, 63)


def load_font(bold, size):
    cands = (["consolab.ttf", "courbd.ttf", "DejaVuSansMono-Bold.ttf"] if bold
             else ["consola.ttf", "cour.ttf", "DejaVuSansMono.ttf"])
    for name in cands:
        for base in ("C:/Windows/Fonts/", ""):
            try:
                return ImageFont.truetype(base + name, size)
            except OSError:
                continue
    return ImageFont.load_default()


MONO = load_font(False, 15 * S)
SMALL = load_font(False, 13 * S)
TITLE = load_font(False, 13 * S)
BIG = load_font(True, 30 * S)


def sc(v):
    return int(round(v * S))


def run(d, x, yc, text, font, color):
    """Draw a left-middle anchored text run at already-scaled (x, yc). Returns new x."""
    d.text((x, yc), text, font=font, fill=color, anchor="lm")
    return x + d.textlength(text, font)


def tri_right(d, mx, yc, color):
    d.polygon([(sc(mx), sc(yc - 5)), (sc(mx), sc(yc + 5)), (sc(mx + 8), sc(yc))], fill=color)


def tri_up(d, x, yc, color):
    d.polygon([(sc(x), sc(yc + 4)), (sc(x + 9), sc(yc + 4)), (sc(x + 4.5), sc(yc - 5))], fill=color)


def check(d, x, yc, color):
    pts = [(sc(x), sc(yc + 1)), (sc(x + 4), sc(yc + 6)), (sc(x + 12), sc(yc - 6))]
    d.line(pts, fill=color, width=sc(2), joint="curve")


def make_frame(step, bar, score):
    im = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(im)

    # title bar
    d.rectangle([0, 0, W * S, sc(38)], fill=TBAR)
    d.line([0, sc(38), W * S, sc(38)], fill=SEP, width=S)
    for cx, col in ((20, RED), (40, AMD), (60, GRN)):
        d.ellipse([sc(cx - 6), sc(13), sc(cx + 6), sc(25)], fill=col)
    run(d, sc(84), sc(19), "resume-agent  ·  scripts/build.py", TITLE, MUT)

    if step >= 1:
        x = run(d, sc(44), sc(66), ">", MONO, TEAL)
        x = run(d, x, sc(66), " tailor my résumé for this role  ", MONO, TXT)
        run(d, x, sc(66), "+ meridian-jd.txt", MONO, MUT)

    if step >= 2:
        d.rectangle([sc(30), sc(91), sc(32), sc(133)], fill=AMB)
        run(d, sc(44), sc(100), "Working Student · Global Compliance / IT Governance", MONO, AMB)
        run(d, sc(44), sc(124), "Meridian Capital Services · Frankfurt", MONO, MUT)

    def stepline(yc, head, tail):
        tri_right(d, 44, yc, TEAL)
        x = run(d, sc(64), sc(yc), head, MONO, TXT)
        run(d, x, sc(yc), tail, MONO, MUT)

    if step >= 3:
        stepline(160, "gap analysis", "    match 5/10 · 10 keywords missing")
    if step >= 4:
        stepline(184, "rewrite", "         ATS bullets · keywords woven · one page")
    if step >= 5:
        stepline(208, "ats scan", "        building resume.pdf ...")

    if step >= 6:
        d.rounded_rectangle([sc(26), sc(236), sc(734), sc(392)], radius=sc(10), outline=BOXLINE, width=S)
        run(d, sc(44), sc(260), "ATS AUDIT  ·  resume.pdf", SMALL, MUT)
        rows = [("parse integrity", "30/30", 1.0), ("keyword coverage", "36/40", 0.9),
                ("anti-stuffing", "10/10", 1.0), ("formatting", "20/20", 1.0)]
        for i, (lbl, val, tgt) in enumerate(rows):
            yc = 286 + i * 28
            run(d, sc(44), sc(yc), lbl, MONO, DIM)
            d.text((sc(250), sc(yc)), val, font=MONO, fill=TXT, anchor="rm")
            bx0, bx1, bh = 272, 712, 12
            d.rounded_rectangle([sc(bx0), sc(yc - bh / 2), sc(bx1), sc(yc + bh / 2)],
                                radius=sc(bh / 2), fill=TRACK)
            fw = (bx1 - bx0) * tgt * bar
            if fw >= 1:
                rr = min(bh / 2, fw / 2)
                d.rounded_rectangle([sc(bx0), sc(yc - bh / 2), sc(bx0 + fw), sc(yc + bh / 2)],
                                    radius=sc(rr), fill=TEAL)

    if step >= 7:
        yc = 424
        x = run(d, sc(44), sc(yc), "ATS score   ", MONO, MUT)
        x = run(d, x, sc(yc), str(score), BIG, TEAL2)
        x = run(d, x, sc(yc), "/100", MONO, MUT)
        x += sc(22)
        tri_up(d, x / S, yc, TEAL)
        x = run(d, x + sc(13), sc(yc), "+8", SMALL, TEAL)
        x += sc(24)
        x = run(d, x, sc(yc), "PAGES 1", MONO, MUT)
        x += sc(24)
        check(d, x / S, yc, TEAL)
        run(d, x + sc(18), sc(yc), "resume.pdf ready", MONO, TEAL)

    return im.resize((W, H), Image.LANCZOS)


frames, durs = [], []


def add(im, dur):
    frames.append(im)
    durs.append(dur)


add(make_frame(1, 0, 88), 650)
add(make_frame(2, 0, 88), 700)
add(make_frame(3, 0, 88), 700)
add(make_frame(4, 0, 88), 700)
add(make_frame(5, 0, 88), 700)
add(make_frame(6, 0, 88), 280)
for i in range(1, 15):
    add(make_frame(6, i / 14.0, 88), 70)
add(make_frame(7, 1, 88), 380)
for s in range(89, 97):
    add(make_frame(7, 1, s), 150)
add(make_frame(7, 1, 96), 2400)

pframes = [f.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
           for f in frames]
pframes[0].save(OUT, save_all=True, append_images=pframes[1:], duration=durs,
                loop=0, optimize=True, disposal=2)

total = sum(durs)
print(f"wrote {OUT}")
print(f"frames={len(pframes)}  loop={total} ms  size={OUT.stat().st_size/1024:.0f} KB")
