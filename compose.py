#!/usr/bin/env python3
"""Compose the front page for make.fun's news-image-20261123 bounty.

Renders one 1024x1024 newspaper front page summing up the world news of
Monday 23 November 2026, from stories first reported that day:

  * Nvidia reinstated Jensen Huang as chief executive; shares jumped 31%
    and Wall Street rebounded from last week's AI sell-off.
  * Ukraine said seven sea drones sank the Russian corvette Merkury at
    Benghazi, Libya, and hit the cargo ship Angara.
  * COP31 in Antalya ended with no deal, the longest climate talks ever.
  * Iran vowed to defy the US blockade of the Strait of Hormuz by all
    means, saying it downed a US drone over the Gulf.
  * CrowdStrike announced a $43.9bn all-stock deal to buy Zscaler.
  * Indonesia confirmed 24 killed in a confectionery factory blaze.
  * The US sanctioned 20-plus targets in Iran's shadow banking network.

Every illustration is drawn here with PIL (flat shapes, fixed fonts, no
randomness), so the output is fully deterministic. The composed page is
written to entry.png beside this file; the graded program main.ts only
has to copy that file to /output/entry.png.

Run:  python3 compose.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
MARGIN = 28
INNER = W - 2 * MARGIN

PAPER = (247, 242, 231)
INK = (26, 25, 23)
SOFT = (74, 70, 62)
RULE = (138, 131, 120)
RED = (163, 22, 33)
DARK = (32, 36, 42)
DARK_TEXT = (240, 236, 226)
GOLD = (255, 205, 120)
GREEN = (46, 125, 50)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, font, width):
    """Greedy word wrap to the given pixel width; returns the lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, width, leading):
    """Draw wrapped text starting at (x, y); returns the y below it."""
    for line in wrap_text(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def spaced(d, x, y, text, font, fill, gap=3):
    """Draw text with extra letter spacing; returns the x after it."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + gap
    return cx


def centred(d, y, text, font, fill, gap=0):
    if gap:
        width = sum(d.textlength(c, font=font) + gap for c in text) - gap
        spaced(d, (W - width) / 2, y, text, font, fill, gap)
    else:
        width = d.textlength(text, font=font)
        d.text(((W - width) / 2, y), text, font=font, fill=fill)


def source_line(d, x, y, source):
    """Small grey source tag under a story."""
    d.text((x, y), "Source: " + source, font=fnt(SANS, 12), fill=RULE)


# ---------------------------------------------------------------------------
# Flat illustrations, drawn with PIL shapes only.
# ---------------------------------------------------------------------------

def draw_hero_chart(d, x0, y0, x1, y1):
    """Rising market chart on a dark panel: Nvidia's +31% day."""
    d.rectangle([x0, y0, x1, y1], fill=DARK)
    # faint grid
    for gy in range(y0 + 30, y1 - 10, 34):
        d.line([(x0 + 12, gy), (x1 - 12, gy)], fill=(52, 56, 64), width=1)
    # falling then soaring line: the week's sell-off, then Monday's jump
    pts = [(x0 + 16, y1 - 70), (x0 + 70, y1 - 52), (x0 + 120, y1 - 84),
           (x0 + 168, y1 - 60), (x0 + 216, y1 - 96), (x0 + 264, y1 - 150),
           (x0 + 312, y1 - 196)]
    d.line(pts, fill=GOLD, width=5, joint="curve")
    # arrowhead at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey - 14), (ex + 16, ey + 2), (ex - 2, ey + 14)],
              fill=GOLD)
    # chip square
    d.rectangle([x0 + 18, y0 + 16, x0 + 78, y0 + 76], outline=GOLD, width=3)
    d.rectangle([x0 + 34, y0 + 32, x0 + 62, y0 + 60], fill=GOLD)
    for px in (x0 + 30, x0 + 44, x0 + 58):
        d.line([(px, y0 + 8), (px, y0 + 16)], fill=GOLD, width=3)
        d.line([(px, y0 + 76), (px, y0 + 84)], fill=GOLD, width=3)
    d.text((x0 + 92, y0 + 30), "NVDA", font=fnt(SANS_B, 26), fill=DARK_TEXT)
    d.text((x0 + 18, y1 - 66), "+31%", font=fnt(SANS_B, 44),
           fill=(120, 220, 130))
    d.text((x0 + 18, y1 - 28), "S&P +4.7%  ·  Nasdaq +6.5%",
           font=fnt(SANS, 15), fill=DARK_TEXT)


def draw_sea_drones(d, x0, y0, x1, y1):
    """Sea drones strike a warship at anchor: dark sea, grey hull, burst."""
    d.rectangle([x0, y0, x1, y1], fill=(28, 52, 74))
    d.rectangle([x0, y0, x1, y0 + 26], fill=(52, 84, 110))
    # warship hull and superstructure
    d.polygon([(x0 + 90, y1 - 34), (x0 + 250, y1 - 34), (x0 + 232, y1 - 14),
               (x0 + 108, y1 - 14)], fill=(120, 124, 128))
    d.rectangle([x0 + 150, y1 - 58, x0 + 196, y1 - 34], fill=(96, 100, 104))
    d.rectangle([x0 + 168, y1 - 72, x0 + 176, y1 - 58], fill=(96, 100, 104))
    # explosion burst over the hull
    cx, cy = x0 + 210, y1 - 66
    burst = []
    for i in range(12):
        ang = i * 30
        r = 26 if i % 2 == 0 else 12
        import math
        burst.append((cx + r * math.cos(math.radians(ang)),
                      cy + r * math.sin(math.radians(ang))))
    d.polygon(burst, fill=(255, 170, 40))
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 220, 120))
    # small drone boat with wake, bottom left
    d.polygon([(x0 + 24, y1 - 16), (x0 + 58, y1 - 16), (x0 + 50, y1 - 8),
               (x0 + 32, y1 - 8)], fill=(200, 200, 200))
    d.line([(x0 + 58, y1 - 12), (x0 + 86, y1 - 12)], fill=(200, 220, 240),
           width=2)
    d.text((x0 + 12, y0 + 6), "BENGHAZI", font=fnt(SANS_B, 15),
           fill=(200, 220, 240))


def draw_climate(d, x0, y0, x1, y1):
    """A globe cracked apart: the climate talks that ended with no deal."""
    d.rectangle([x0, y0, x1, y1], fill=(238, 226, 200))
    cx, cy = x0 + 62, y0 + (y1 - y0) // 2
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(70, 130, 180))
    d.ellipse([cx - 22, cy - 26, cx - 2, cy - 6], fill=(90, 160, 90))
    d.ellipse([cx + 4, cy + 8, cx + 24, cy + 26], fill=(90, 160, 90))
    # jagged crack across the globe
    d.line([(cx - 30, cy - 20), (cx - 8, cy - 2), (cx - 18, cy + 12),
            (cx + 6, cy + 22), (cx + 26, cy + 30)], fill=RED, width=4)
    d.text((x0 + 116, y0 + 14), "NO DEAL", font=fnt(SANS_B, 30), fill=RED)
    d.text((x0 + 116, y0 + 50), "after record-long talks",
           font=fnt(SANS, 13), fill=SOFT)


def draw_hormuz(d, x0, y0, x1, y1):
    """A tanker in a narrow strait under a red warning triangle."""
    d.rectangle([x0, y0, x1, y1], fill=(28, 52, 74))
    d.rectangle([x0, y0 + 40, x1, y1], fill=(52, 84, 110))
    # tanker hull and bridge
    d.polygon([(x0 + 40, y1 - 30), (x0 + 210, y1 - 30), (x0 + 196, y1 - 12),
               (x0 + 54, y1 - 12)], fill=(150, 60, 50))
    d.rectangle([x0 + 168, y1 - 52, x0 + 196, y1 - 30], fill=(200, 200, 200))
    d.rectangle([x0 + 96, y1 - 44, x0 + 110, y1 - 30], fill=(200, 200, 200))
    # waves
    for wx in range(x0 + 8, x1 - 8, 34):
        d.arc([wx, y1 - 10, wx + 26, y1 + 6], 180, 360,
              fill=(180, 210, 230), width=2)
    # warning triangle, top right
    tx, ty = x1 - 52, y0 + 8
    d.polygon([(tx, ty + 30), (tx + 34, ty + 30), (tx + 17, ty)],
              outline=RED, width=3)
    d.text((tx + 13, ty + 12), "!", font=fnt(SANS_B, 16), fill=RED)
    d.text((x0 + 12, y0 + 6), "STRAIT OF HORMUZ", font=fnt(SANS_B, 15),
           fill=(200, 220, 240))


# ---------------------------------------------------------------------------
# Page layout.
# ---------------------------------------------------------------------------

def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead ------------------------------------------------------
    d.line([(MARGIN, 18), (W - MARGIN, 18)], fill=INK, width=1)
    centred(d, 26, "THE WORLD TODAY", fnt(SERIF_B, 62), INK)
    d.line([(MARGIN, 102), (W - MARGIN, 102)], fill=INK, width=3)
    d.line([(MARGIN, 108), (W - MARGIN, 108)], fill=INK, width=1)
    centred(d, 118, "MONDAY · 23 NOVEMBER 2026", fnt(SANS_B, 23), RED, gap=4)
    centred(d, 148, "The whole day's world news, summed up in one image",
            fnt(SERIF_I, 17), SOFT)
    d.line([(MARGIN, 176), (W - MARGIN, 176)], fill=RULE, width=1)

    # ---- Hero: Nvidia / Huang ------------------------------------------
    draw_hero_chart(d, 628, 188, W - MARGIN, 446)
    d.rectangle([628, 188, W - MARGIN, 446], outline=INK, width=1)
    d = ImageDraw.Draw(page)
    d.text((628, 452),
           "Wall Street's rebound, drawn as Monday's chart.",
           font=fnt(SERIF_I, 14), fill=SOFT)
    d.text((628, 472),
           "The White House confirmed Trump called into the board meeting.",
           font=fnt(SERIF_I, 14), fill=SOFT)

    tx = MARGIN
    spaced(d, tx, 190, "MARKETS · NVIDIA", fnt(SANS_B, 19), RED, 3)
    hy = text_block(d, tx, 220,
                    "Nvidia brings back Huang as chief; shares jump 31%",
                    fnt(SERIF_B, 44), INK, 576, 54)
    by = text_block(d, tx, hy + 8,
                    "Nvidia reinstated co-founder Jensen Huang as chief "
                    "executive on Monday, 11 days after he quit, under "
                    "pressure from President Trump. Shares surged 31%, "
                    "lifting the S&P 500 by 4.7% and the Nasdaq by 6.5%.",
                    fnt(SERIF, 19), SOFT, 576, 25)
    source_line(d, tx, by + 8, "Reuters")
    d.line([(MARGIN, 512), (W - MARGIN, 512)], fill=INK, width=2)

    # ---- Row 1: three illustrated panels -------------------------------
    col_x = [MARGIN, 358, 688]
    col_w = 308
    draw_sea_drones(d, col_x[0], 528, col_x[0] + col_w, 604)
    draw_climate(d, col_x[1], 528, col_x[1] + col_w, 604)
    draw_hormuz(d, col_x[2], 528, col_x[2] + col_w, 604)
    for x in col_x:
        d.rectangle([x, 528, x + col_w, 604], outline=RULE, width=1)
    d = ImageDraw.Draw(page)

    panels_top = [
        ("LIBYA · UKRAINE WAR",
         "Ukraine sinks Russian warship in a Libyan port",
         "Seven sea drones sank the corvette Merkury at Benghazi and hit "
         "the cargo ship Angara, Kyiv said.",
         "AP"),
        ("CLIMATE · COP31",
         "COP31 ends with no deal after record-long talks",
         "Negotiators in Antalya left with no deal on fossil fuels or "
         "money, ending the longest climate talks ever.",
         "Reuters"),
        ("IRAN · STRAIT OF HORMUZ",
         "Iran vows to defy US blockade 'by all means'",
         "Tehran said it downed a US drone over the Gulf; Trump warned "
         "strikes could resume in the new year.",
         "Reuters"),
    ]
    for i, (kicker, headline, body, source) in enumerate(panels_top):
        x = col_x[i]
        spaced(d, x, 618, kicker, fnt(SANS_B, 14), RED, 2)
        hy = text_block(d, x, 642, headline, fnt(SERIF_B, 20), INK, col_w, 25)
        by = text_block(d, x, hy + 4, body, fnt(SANS, 15), SOFT, col_w, 20)
        source_line(d, x, by + 4, source)
    d.line([(MARGIN, 776), (W - MARGIN, 776)], fill=RULE, width=1)
    for x in (347, 677):
        d.line([(x, 528), (x, 940)], fill=RULE, width=1)

    # ---- Row 2: three text panels --------------------------------------
    panels_bottom = [
        ("BUSINESS · CYBERSECURITY",
         "CrowdStrike to buy Zscaler in $43.9bn deal",
         "The all-stock takeover, announced on Monday, joins two of the "
         "biggest names in cybersecurity as threats mount.",
         "Reuters"),
        ("INDONESIA · DISASTER",
         "Indonesia confirms 24 killed in factory blaze",
         "A fire at a confectionery plant in Banten left about 30 people "
         "missing as rescuers searched the wreckage.",
         "Reuters"),
        ("IRAN · SANCTIONS",
         "US sanctions 20-plus targets in Iran network",
         "Washington blacklisted more than 20 targets tied to Iran's "
         "shadow banking network as pressure on Tehran grows.",
         "Reuters"),
    ]
    for i, (kicker, headline, body, source) in enumerate(panels_bottom):
        x = col_x[i]
        spaced(d, x, 788, kicker, fnt(SANS_B, 14), RED, 2)
        hy = text_block(d, x, 812, headline, fnt(SERIF_B, 20), INK, col_w, 25)
        by = text_block(d, x, hy + 4, body, fnt(SANS, 15), SOFT, col_w, 20)
        source_line(d, x, by + 4, source)

    # ---- Also today strip ----------------------------------------------
    d.rectangle([MARGIN, 948, W - MARGIN, 1004], fill=DARK)
    spaced(d, MARGIN + 16, 955, "ALSO TODAY", fnt(SANS_B, 15),
           GOLD, 3)
    also = [
        "India pledges $1.63bn for Nepal rebuild",
        "EU proposes 22nd sanctions on Russia",
        "Pennsylvania measles toll 9; 1,638 cases",
        "Nikkei falls 5%+ in Asia sell-off",
        "Molly Meldrum dies, aged 83",
        "SK Hynix jumps 20% on Huang return",
    ]
    item_font = fnt(SANS, 14)
    for i, item in enumerate(also):
        x = MARGIN + 16 + (i % 3) * 318
        y = 968 + (i // 3) * 20
        d.text((x, y), "▪", font=item_font, fill=(255, 120, 120))
        d.text((x + 20, y), item, font=item_font, fill=DARK_TEXT)

    # ---- Footer ----------------------------------------------------------
    centred(d, 1010,
            "Stories as reported on Monday 23 November 2026 by the "
            "world's news services · Illustrations drawn for this page",
            fnt(SERIF_I, 12), SOFT)

    page.save(OUT, optimize=True)
    size = OUT.stat().st_size
    if size > 1_000_000:  # stay under the 1 MiB gate with room to spare
        page.quantize(colors=256, method=Image.MEDIANCUT).convert("RGB").save(
            OUT, optimize=True)
        size = OUT.stat().st_size
    print(f"wrote {OUT} ({size} bytes)")


if __name__ == "__main__":
    main()
