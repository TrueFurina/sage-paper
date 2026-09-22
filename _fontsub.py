"""
Build a compact CJK font subset for PDF rendering.

Two problems had to be solved, and the "merge donor fonts" approach did NOT
work (fontTools' Merger asserts when vertical-metrics tables differ across
inputs).  The working approach is:

  PROBLEM 1 (size): PyMuPDF Story renders CJK with its bundled
  "Droid Sans Fallback" (~3.4 MB) and embeds it as a *raw uncompressed
  stream*, so every PDF was ~4 MB.  FIX: build a subset of Microsoft YaHei
  containing only the glyphs the docs actually use (~0.6 MB) and feed it to
  the renderer via a `fitz.Archive` + `@font-face`.

  PROBLEM 2 (residual 3.4 MB): Microsoft YaHei lacks ~15 of the symbols the
  docs use (notably U+207B SUPERSCRIPT MINUS from "10⁻⁴", plus ✅ ❌ ↔ ⇒ ...).
  For any glyph missing from our subset, PyMuPDF silently falls back to the
  full Droid font and the file balloons again.  FIX: map those characters to
  visually-acceptable equivalents that YaHei *does* contain (see SYMBOL_MAP),
  so the subset has 100% coverage and no fallback is ever triggered.

`SYMBOL_MAP` is applied to the Markdown before rendering (see md2pdf.py), so
both the text layer and the glyph coverage stay consistent.
"""
from __future__ import annotations

import os
import sys
from typing import Iterable, Optional

WORK = os.path.dirname(os.path.abspath(__file__))
OUT_TTF = os.path.join(WORK, "_sage_subset.ttf")
SRC_TTF = r"C:\Windows\Fonts\msyh.ttc"
SRC_FALLBACKS = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
    r"C:\Windows\Fonts\Deng.ttf",
]

# Characters Microsoft YaHei is missing -> safe in-font equivalents.
# NOTE: listed explicitly so the substitution is auditable, not silent.
SYMBOL_MAP = {
    "\u207b": "^",     # ⁻ SUPERSCRIPT MINUS   (10⁻⁴ -> 10^-4)
    "\u2070": "^0",    # ⁰
    "\u00b9": "^1",    # ¹
    "\u00b2": "^2",    # ²
    "\u00b3": "^3",    # ³
    "\u2074": "^4",    # ⁴
    "\u2075": "^5",
    "\u2076": "^6",
    "\u2077": "^7",
    "\u2078": "^8",
    "\u2079": "^9",
    "\u2080": "0",     # ₀ SUBSCRIPT ZERO — YaHei has NO subscript glyphs at
    "\u2081": "1",     # ₁              all; without these PyMuPDF silently
    "\u2082": "2",     # ₂              embeds a 3.4 MB fallback font and the
    "\u2083": "3",     # ₃              PDF grows ~5x (see 08 section 7,
    "\u2084": "4",     # ₄              "CAUSE B"). Added 2026-09-22 after
    "\u2085": "5",     # ₅              21_Section4 failed the hygiene gate
    "\u2086": "6",     # ₆              on (c₁, c₂) in its worked example.
    "\u2087": "7",     # ₇
    "\u2088": "8",     # ₈
    "\u2089": "9",     # ₉
    "\u2705": "[OK]",  # ✅
    "\u274c": "[X]",   # ❌
    "\u2194": "<->",   # ↔
    "\u21d2": "=>",    # ⇒
    "\u21e2": "->",    # ⇢
    "\u2200": "for all",   # ∀
    "\u2203": "exists",    # ∃
    "\u2209": "not in",    # ∉
    "\u2282": "subset",    # ⊂
    "\u2286": "subseteq",  # ⊆
    "\u246a": "(11)",  # ⑪
    "\u246b": "(12)",  # ⑫
    "\u26a0": "[!]",   # ⚠ WARNING SIGN
    "\ufe0f": "",      # variation selector-16 (invisible; drop it)
    "\u2713": "[v]",   # ✓ CHECK MARK
    "\u2717": "[x]",   # ✗ BALLOT X
    "\U0001f525": "[!]",  # 🔥 FIRE (not in YaHei)
    "\U0001f534": "[!!]",  # 🔴 RED CIRCLE
    "\U0001f6ab": "[NO]",  # 🚫 NO ENTRY
    "\U0001f7e1": "[?]",   # 🟡 YELLOW CIRCLE
    "\U0001f7e2": "[+]",   # 🟢 GREEN CIRCLE
}

# Characters Microsoft YaHei genuinely cannot render.  `BASE_CHARS` must not
# contain any of these, because BASE_CHARS is unioned into the subset request
# *after* SYMBOL_MAP has been applied -- anything listed here would bypass the
# mapping and come back as an uncovered glyph, silently re-embedding PyMuPDF's
# 3.4 MB Droid fallback.  `assert_base_chars_safe()` enforces this invariant.
YAHEI_MISSING = set("↔⇒⇢∀∃∉⊂⊆⑪⑫⚠✓✗\ufe0f🔥🔴🚫🟡")


def assert_base_chars_safe() -> None:
    """Fail loudly if BASE_CHARS lists a glyph YaHei lacks.

    This guards a real bug (2026-09-19): BASE_CHARS contained 12 glyphs that
    SYMBOL_MAP also mapped, so the mapping never applied to them and the
    coverage check kept reporting 13 uncovered chars no matter what was added
    to SYMBOL_MAP.  The fix is to REMOVE them from BASE_CHARS, not to keep
    re-adding them to SYMBOL_MAP.
    """
    bad = sorted(set(BASE_CHARS) & YAHEI_MISSING)
    if bad:
        raise AssertionError(
            f"BASE_CHARS contains glyphs YaHei lacks: {''.join(bad)!r}. "
            "Remove them from BASE_CHARS; SYMBOL_MAP substitutes them in text."
        )


def apply_symbol_map(text: str) -> str:
    for k, v in SYMBOL_MAP.items():
        if k in text:
            text = text.replace(k, v)
    return text

# Always include these so that headings/numbers/symbols never tofu.
# INVARIANT: must not contain any char in YAHEI_MISSING (see assertion below).
BASE_CHARS = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    " \t\n"
    "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    "→←↑↓×÷≤≥≠≈±−—–…·•"          # ⇢ ⇒ ↔ moved to SYMBOL_MAP
    "①②③④⑤⑥⑦⑧⑨⑩"            # ⑪ ⑫ moved to SYMBOL_MAP
    "§¶†‡‰°′″"
    "αβγδεζηθικλμνξπρστυφχψω"
    "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΠΡΣΤΥΦΧΨΩ"
    "★☆●○■□◆◇▲▼"               # ✓ ✗ moved to SYMBOL_MAP
    "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ"
    "∂∑∏∫√∞∈∪∩¬∧∨"              # ∉ ⊂ ⊆ ∀ ∃ moved to SYMBOL_MAP
)


def collect_chars(md_paths: Iterable[str]) -> set:
    """Collect every character that will be rendered, AFTER symbol mapping.

    Order matters: SYMBOL_MAP must be applied first, otherwise the gap
    characters (⁻ ✅ ↔ ...) leak into the subset request, the subset fails to
    cover them, and PyMuPDF silently embeds its 3.4 MB fallback font.
    This is also asserted in build_subset().

    NOTE (2026-09-19 bug): mapping the *document text* is not sufficient,
    because BASE_CHARS is unioned in afterwards.  Any YaHei-missing glyph that
    BASE_CHARS itself lists will bypass SYMBOL_MAP entirely.  Hence
    assert_base_chars_safe() is called first.
    """
    assert_base_chars_safe()
    chars = set(BASE_CHARS)
    for p in md_paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                chars |= set(apply_symbol_map(f.read()))
        except Exception as e:
            print(f"  [subset] skip {p}: {e}")
    # Keep every character that could need a glyph.  Do NOT use str.strip() here:
    # it treats U+3000 (ideographic space) as whitespace and drops it -- but
    # U+3000 is a VISIBLE-WIDTH character that needs its own glyph, so dropping
    # it silently made PyMuPDF embed its 3.4 MB fallback font for any document
    # using full-width spaces as separators.  Worse, build_subset's own coverage
    # report then said "coverage OK", because it re-checked the already-filtered
    # set -- a check that can never fail (see md2pdf.subset_covers, which is the
    # honest gate: it filters only on real control characters).
    _INVISIBLE = set("\n\r\t\x0b\x0c\u200b\u200c\u200d\u200e\u200f\u2060\ufeff")
    return {c for c in chars if c not in _INVISIBLE}


def build_subset(md_paths: Iterable[str], out_ttf: str = OUT_TTF) -> Optional[str]:
    try:
        from fontTools import subset as ft_subset
        from fontTools.ttLib import TTFont
    except Exception as e:
        print(f"[subset] fontTools unavailable ({e}); skipping subset")
        return None

    src = next((p for p in SRC_FALLBACKS if os.path.exists(p)), None)
    if not src:
        print("[subset] no source CJK font found")
        return None

    # Collect chars AFTER applying SYMBOL_MAP, so the subset is built for the
    # characters that will actually be rendered (see md2pdf.apply_symbol_map).
    chars = collect_chars(md_paths)
    # Control characters are never glyphs.
    chars = {c for c in chars if c not in "\n\r\t\x0b\x0c"}

    # Guard: BASE_CHARS deliberately lists some symbols that Microsoft YaHei
    # does NOT contain (⇢ ⇒ ↔ ⑪ ⑫ ∉ ⊂ ⊆ ∀ ∃).  If SYMBOL_MAP ever fails to map
    # one of them, the subset will not cover it and PyMuPDF will silently embed
    # its 3.4 MB fallback font.  Detect that here and say exactly which chars to
    # add to SYMBOL_MAP, instead of shipping a bloated PDF.
    text = "".join(sorted(chars))
    print(f"[subset] source={os.path.basename(src)} "
          f"chars={len(chars)} -> target={os.path.basename(out_ttf)}")

    # ---- 1. subset the CJK face -------------------------------------------
    tmp_cjk = os.path.join(WORK, "_tmp_cjk.ttf")
    try:
        font = TTFont(src, fontNumber=0, lazy=True)
        options = ft_subset.Options()
        options.layout_features = ["*"]
        options.name_IDs = ["*"]
        options.notdef_outline = True
        options.recalc_bounds = True
        options.drop_tables += ["DSIG"]
        subsetter = ft_subset.Subsetter(options=options)
        subsetter.populate(text=text)
        subsetter.subset(font)
        font.flavor = None
        font.save(tmp_cjk)
        font.close()
        print(f"[subset] CJK subset -> {os.path.getsize(tmp_cjk)/1024:.0f} KB")
    except Exception as e:
        import traceback
        print(f"[subset] CJK subset failed: {type(e).__name__}: {e}")
        traceback.print_exc()
        return None

    # ---- 2. verify 100% coverage (no residual fallback font) --------------
    # ---- 2. verify 100% coverage against the HONEST need set --------------
    # Checking coverage against `chars` (the FILTERED set) is a check that can
    # never fail: if a filter drops a real glyph-needing character, the subset
    # and the check lose it together, and the report still says "coverage OK".
    # That is exactly how U+3000 stayed missing for three render rounds while
    # this line reported success.  So verify against every character the sources
    # contain, excluding only real control characters -- the same predicate
    # md2pdf.subset_covers (the honest gate) uses.
    honest: set = set(BASE_CHARS)
    for p in md_paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                honest |= set(apply_symbol_map(f.read()))
        except Exception:
            continue
    honest = {c for c in honest if c not in "\n\r\t\x0b\x0c"}

    fh = TTFont(tmp_cjk, lazy=True)
    have = set()
    for t in fh["cmap"].tables:
        have |= set(t.cmap.keys())
    fh.close()
    still = sorted(c for c in honest if ord(c) not in have)
    if still:
        print(f"[subset] *** WARNING: {len(still)} chars uncovered ***")
        print(f"[subset]     {''.join(still)[:100]!r}")
        # Two different causes, two different fixes -- do not conflate them.
        try:
            _src = TTFont(SRC_TTF, fontNumber=0)
            _src_cmap = set()
            for t in _src["cmap"].tables:
                _src_cmap |= set(t.cmap.keys())
            _src.close()
        except Exception:
            _src_cmap = set()
        no_glyph = [c for c in still if ord(c) not in _src_cmap]
        dropped = [c for c in still if ord(c) in _src_cmap]
        if dropped:
            print("[subset]     CAUSE A -- present in the source font but DROPPED "
                  "by collect_chars' filter:")
            print(f"[subset]       {''.join(dropped)[:60]!r}  "
                  f"(U+{ord(dropped[0]):04X} ...)")
            print("[subset]       FIX: repair the filter in collect_chars.  Do NOT "
                  "add these to SYMBOL_MAP -- they have real glyphs.")
        if no_glyph:
            print("[subset]     CAUSE B -- no glyph in the source font at all:")
            print(f"[subset]       {''.join(no_glyph)[:60]!r}")
            print("[subset]       FIX: add them to SYMBOL_MAP (or delete them from "
                  "the text).  Otherwise PyMuPDF embeds its 3.4 MB fallback and "
                  "every PDF grows ~5x.")
        for c in still:
            # Emit a VALID Python escape. Characters outside the BMP (all the
            # colour emoji, e.g. U+1F7E2) need the 8-digit \U form; printing
            # them as \u{04x} yields "\u1f7e2", which is not a valid escape and
            # would be copied into SYMBOL_MAP as a corrupted literal.
            esc = f"\\u{ord(c):04x}" if ord(c) <= 0xFFFF else f"\\U{ord(c):08x}"
            print(f'    "{esc}": "?",   # {c!r}')
    else:
        print("[subset] coverage OK: every rendered char is in the subset "
              "(no fallback font will be embedded)")

    import shutil
    shutil.copyfile(tmp_cjk, out_ttf)
    for tmp in (tmp_cjk, os.path.join(WORK, "_tmp_merged.ttf")):
        try:
            if tmp != out_ttf and os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass

    print(f"[subset] wrote {out_ttf} "
          f"({os.path.getsize(out_ttf)/1024:.0f} KB, from "
          f"{os.path.getsize(src)/1024/1024:.1f} MB)")
    return out_ttf


if __name__ == "__main__":
    import glob
    here = WORK
    mds = sorted(glob.glob(os.path.join(here, "*.md")))
    r = build_subset(mds)
    sys.exit(0 if r else 1)
