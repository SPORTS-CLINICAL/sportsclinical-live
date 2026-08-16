SPORTS CLINICAL, SITE PACK v1.24
================================
16 August 2026. Supersedes v1.23. Queue item 4.

WHAT CHANGED, ALL 31 PAGES
--------------------------

1. SELF-HOSTED FONTS.
   v1.23 loaded Josefin Sans and Jost from fonts.googleapis.com and
   fonts.gstatic.com on every page. Every visitor's IP address and user
   agent therefore reached Google before a word of the page was read.
   The cookie notice states, in its own words, that no fonts are fetched
   from someone else's server, so the site contradicted its own published
   statement on all 31 pages. That is the reason this is a positioning fix
   and not an optimisation.

   The three link lines are replaced with eight local @font-face rules
   serving woff2 subsets from fonts/. Two preload hints cover the two
   heaviest-used weights, Josefin SemiBold and Josefin Light.

2. NOSCRIPT FALLBACK, AND THE SAME FIX FOR REDUCED MOTION.
   .marquee carries overflow:hidden and is scrolled by requestAnimationFrame.
   With JavaScript off, the strip never moved and everything past the first
   viewport width was unreachable. The same was true for any visitor with
   prefers-reduced-motion set, because the script returns early for them and
   nothing restored the ability to scroll. The strip appears on 29 of the 31
   pages. Both cases now get overflow-x:auto so it can be scrolled by hand.

FONTS SHIPPED, fonts/
---------------------
Josefin Sans  Light 300, Regular 400, SemiBold 600, Bold 700
Jost          Light 300, Regular 400, Medium 500, SemiBold 600

These are the weights the pages actually use, counted across all 31: 600 in
720 declarations, 300 in 563, 400 in 123, then 700 and 500. No italic is
used anywhere on the site, so the italic axis carried in the old Google
request is dropped.

Both families are SIL Open Font Licence 1.1. Licence texts travel with the
masters in the Brand Pack. The genuine ITC Kabel Std and Century Gothic Std
are Desktop licensed and appear nowhere in this pack, in any form.

Subset range is derived from the characters the site actually renders, not
guessed: Basic Latin, Latin-1 Supplement, and the exact punctuation in use.
Total font payload 75,836 bytes across eight files, of which any one page
loads only the four to six faces it uses.

KNOWN AND UNCHANGED
-------------------
U+2630, the menu glyph, exists in neither substitute family and did not
exist in the Google copies either. The browser falls back to a system font
for that one character, exactly as it did before.

contact-and-booking.html carries an OpenStreetMap iframe. It is the only
third-party request left anywhere in the pack, and it is unchanged from
v1.23. Recorded as a finding, not touched here.

BUILD
-----
build_site_v124.py rebuilds this pack from the v1.23 source and the font
masters. It asserts, per page, that no Google host survives, that eight
faces are written, that the noscript block is present, that the canonical
URL keeps its s, and that no em or en dash is present. It fails loudly
rather than producing a quiet near-miss.

VERIFIED BEFORE MINT
--------------------
- Zero requests to any Google host, measured in a headless browser rather
  than by reading the source.
- All eight faces load from fonts/ with no 404 and no console error, checked
  across five pages.
- Rendering compared against v1.23 at the same viewport.
- Every page hashed individually. Hashes are in the handover.
