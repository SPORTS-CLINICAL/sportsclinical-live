#!/usr/bin/env python3
"""
SPORTS CLINICAL, queue item 4. Site Pack v1.24.

Two changes, both across all 31 pages.

1. SELF-HOSTED FONTS. v1.23 pulled Josefin Sans and Jost from
   fonts.googleapis.com and fonts.gstatic.com on every page load, which sent
   each visitor's IP and user agent to Google. The cookie notice states in
   its own words that no fonts are fetched from someone else's server, so the
   site contradicted its own published statement. The three link lines are
   replaced with local @font-face rules serving woff2 subsets from fonts/.

2. NOSCRIPT FALLBACK. .marquee carries overflow:hidden and is scrolled by
   requestAnimationFrame. With JavaScript off, the strip never moves and
   everything past the first viewport width is unreachable. The same is true
   for anyone with prefers-reduced-motion set, because the script returns
   early. Both now get overflow-x:auto so the strip can be scrolled by hand.

Font weights are the weights the pages actually use, counted across all 31:
Josefin 300, 400, 600, 700 and Jost 300, 400, 500, 600. No italic is used
anywhere, so the italic axis in the old Google request is dropped.

The subset range is derived from the characters the site actually renders,
not guessed. U+2630, the menu glyph, is in neither family and was never in
the Google copies either; the browser falls back for it, as before.
"""

import os
import re
import glob
import shutil
import hashlib
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_SITE = "/home/claude/site/SPORTS_CLINICAL_Site_Pack_v1.23"
SRC_FONTS = "/home/claude/f34/out"
OUT = os.path.join(HERE, "SPORTS_CLINICAL_Site_Pack_v1.24")

WEIGHTS = [
    ("JosefinSans-Light", "Josefin Sans", 300),
    ("JosefinSans-Regular", "Josefin Sans", 400),
    ("JosefinSans-SemiBold", "Josefin Sans", 600),
    ("JosefinSans-Bold", "Josefin Sans", 700),
    ("Jost-Light", "Jost", 300),
    ("Jost-Regular", "Jost", 400),
    ("Jost-Medium", "Jost", 500),
    ("Jost-SemiBold", "Jost", 600),
]

# Basic Latin, Latin-1 Supplement, and the exact punctuation the site renders.
UNICODES = "U+0020-007E,U+00A0-00FF,U+2018-201D,U+2022,U+2026,U+2039-203A"

OLD_BLOCK = re.compile(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*'
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">'
)


def face(stem, family, weight):
    return (
        "@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
        "font-display:swap;src:url('fonts/%s.woff2') format('woff2')}"
        % (family, weight, stem)
    )


NEW_BLOCK = (
    '<link rel="preload" href="fonts/JosefinSans-SemiBold.woff2" as="font" '
    'type="font/woff2" crossorigin>\n'
    '<link rel="preload" href="fonts/JosefinSans-Light.woff2" as="font" '
    'type="font/woff2" crossorigin>\n'
    "<style>\n"
    + "\n".join(face(s, f, w) for s, f, w in WEIGHTS)
    + "\n</style>\n"
    "<style>@media (prefers-reduced-motion: reduce){"
    ".marquee{overflow-x:auto;-webkit-overflow-scrolling:touch}}</style>\n"
    "<noscript><style>"
    ".marquee{overflow-x:auto;-webkit-overflow-scrolling:touch}"
    "</style></noscript>"
)


def build_fonts():
    dest = os.path.join(OUT, "fonts")
    os.makedirs(dest, exist_ok=True)
    rows = []
    for stem, _family, _weight in WEIGHTS:
        src = os.path.join(SRC_FONTS, stem + ".ttf")
        out = os.path.join(dest, stem + ".woff2")
        subprocess.run(
            [
                "pyftsubset", src,
                "--unicodes=" + UNICODES,
                "--layout-features=kern,liga,calt",
                "--flavor=woff2",
                "--output-file=" + out,
            ],
            check=True,
        )
        with open(out, "rb") as fh:
            rows.append((stem + ".woff2", os.path.getsize(out),
                         hashlib.md5(fh.read()).hexdigest()))
    return rows


def patch_pages():
    rows = []
    for src in sorted(glob.glob(os.path.join(SRC_SITE, "*.html"))):
        name = os.path.basename(src)
        s = open(src, encoding="utf-8").read()

        assert OLD_BLOCK.search(s), "%s: the Google font block was not found" % name
        s = OLD_BLOCK.sub(NEW_BLOCK, s)

        # Post-patch assertions, per page.
        assert "googleapis" not in s, "%s: googleapis survived" % name
        assert "gstatic" not in s, "%s: gstatic survived" % name
        assert "@font-face" in s, "%s: no @font-face written" % name
        assert s.count("@font-face") == len(WEIGHTS), "%s: wrong face count" % name
        assert "<noscript>" in s, "%s: no noscript fallback" % name
        assert "www.sportsclinical.co.uk" in s, "%s: canonical URL damaged" % name
        assert "\u2014" not in s and "\u2013" not in s, "%s: em or en dash" % name

        dest = os.path.join(OUT, name)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(s)
        with open(dest, "rb") as fh:
            rows.append((name, os.path.getsize(dest),
                         hashlib.md5(fh.read()).hexdigest()))
    return rows


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    fonts = build_fonts()
    pages = patch_pages()

    assert len(pages) == 31, "expected 31 pages, patched %d" % len(pages)

    print("FONTS, %d subset woff2 files\n" % len(fonts))
    for n, b, h in fonts:
        print("  %-28s %6d bytes  %s" % (n, b, h))
    total_fonts = sum(b for _n, b, _h in fonts)
    print("\n  total font payload: %d bytes\n" % total_fonts)

    print("PAGES, %d patched\n" % len(pages))
    for n, b, h in pages:
        print("  %-38s %8d bytes  %s" % (n, b, h))


if __name__ == "__main__":
    main()
