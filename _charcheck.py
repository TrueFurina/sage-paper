"""Pre-render character guard: find .md characters with NO glyph source.

Run this BEFORE md2pdf.py whenever you have created or edited a .md file.

Why this exists: PyMuPDF silently embeds a ~3.4 MB fallback font (Droid Sans
Fallback / Noto Sans Symbols) for any glyph missing from the CJK subset, which
inflates the PDF several-fold.  md2pdf.py does catch this AFTER rendering (the
`unembedded_fallback_fonts` post-guard) and rebuilds the subset BEFORE rendering
(the `subset_covers` pre-check) -- but a character that exists in NEITHER the
source font (msyh.ttc) NOR `SYMBOL_MAP` can never be covered, so the render is
guaranteed to be bloated.  This script tells you that in ~1 second, by name.

Usage:
    python _charcheck.py            # scan all *.md in the repo root
    python _charcheck.py a.md b.md  # scan specific files

Exit code 0 = every character has a glyph source.  1 = at least one does not.

Historical hits (the reason this file exists):
    README.md  -> 4 emoji (U+1F4E6 / U+1F512 / U+1F5FA / U+1F9ED)   2026-09-20
    07_/09_    -> U+26D4 (no-entry sign), replaced with the mapped U+1F6AB  2026-09-20
    12_        -> U+23F0 (alarm clock), removed entirely                   2026-09-20
Rule of thumb: do NOT "fix" a hit by adding the character to SYMBOL_MAP --
that normalises the habit.  Remove the character (or use plain text) instead.
"""
from __future__ import annotations

import glob
import glob as _glob
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_FONT = r"C:\Windows\Fonts\msyh.ttc"
CONTROL = "\n\r\t\x0b\x0c"


def _cmap(path: str, font_number: int | None = None) -> set:
    from fontTools.ttLib import TTFont
    f = TTFont(path, fontNumber=font_number) if font_number is not None else TTFont(path)
    out: set = set()
    for t in f["cmap"].tables:
        out |= set(t.cmap.keys())
    return out


def main(argv: list[str]) -> int:
    sys.path.insert(0, HERE)
    from _fontsub import apply_symbol_map

    targets = argv[1:] or sorted(_glob.glob(os.path.join(HERE, "*.md")))
    if not targets:
        print("[charcheck] no .md files found")
        return 0

    # Two independent gates, because they answer different questions:
    #   subset  -> what md2pdf will ship today (rebuilt automatically if stale)
    #   source  -> what the subset COULD EVER contain (the hard ceiling)
    have_subset = _cmap(os.path.join(HERE, "_sage_subset.ttf"))
    have_source = _cmap(SRC_FONT, 0)

    unmappable: list[tuple[str, str]] = []   # missing from source font -> fatal
    stale: list[tuple[str, str]] = []        # only missing from the subset -> auto-heals

    for p in targets:
        try:
            s = io.open(p, encoding="utf-8").read()
        except OSError as e:
            print(f"[charcheck] cannot read {p}: {e}")
            continue
        rendered = apply_symbol_map(s)
        for c in sorted({c for c in rendered if c not in CONTROL}):
            cp = ord(c)
            if cp in have_source:
                if cp not in have_subset:
                    stale.append((os.path.basename(p), c))
            else:
                unmappable.append((os.path.basename(p), c))

    for label, rows in (("STALE (auto-rebuild, not fatal)", stale),
                        ("NO GLYPH SOURCE (fatal -- fix the text)", unmappable)):
        if not rows:
            continue
        print(f"[charcheck] {label}:")
        for f, c in rows:
            print(f"    {f}: U+{ord(c):04X}  {c!r}")

    if unmappable:
        print(f"[charcheck] {len(unmappable)} character(s) have no glyph source -- "
              f"remove them (do NOT add to SYMBOL_MAP).")
        return 1

    if stale:
        print(f"[charcheck] {len(stale)} character(s) missing from the shipped subset; "
              f"md2pdf.py will rebuild it automatically.")
    print("[charcheck] OK: every character has a glyph source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
