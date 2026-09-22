"""Mutation check for the U+3000 / "self-check that cannot fail" fix in _fontsub.py.

Two independent claims are verified here:

  CASE A  With the collect_chars filter MUTATED back to its buggy form (dropping
          U+3000), build_subset must REPORT the char as uncovered and must
          attribute it to "CAUSE A -- dropped by collect_chars' filter".
          Before the fix this same situation printed "coverage OK".
  CASE B  With the real filter, the rebuilt subset must actually CONTAIN U+3000
          (and build_subset must report no uncovered characters).

CASE A is the one that matters: a check that has never been seen to fail is
decoration.  Run:  python _munge_charcheck.py
"""
from __future__ import annotations

import glob
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _fontsub as F  # noqa: E402

TARGET = "\u3000"          # ideographic space -- visible width, needs a glyph


def _capture_build(frame_tag: str) -> str:
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        F.build_subset(sorted(glob.glob(os.path.join(F.WORK, "*.md"))))
    finally:
        sys.stdout = real
    out = buf.getvalue()
    print(f"--- {frame_tag} ---")
    for line in out.splitlines():
        if line.startswith("[subset]"):
            print("   ", line)
    return out


def _subset_has(ch: str) -> bool:
    from fontTools.ttLib import TTFont
    f = TTFont(F.OUT_TTF, lazy=True)
    have = set()
    for t in f["cmap"].tables:
        have |= set(t.cmap.keys())
    f.close()
    return ord(ch) in have


def main() -> int:
    results: list[tuple[str, bool]] = []

    # ---------- CASE A: mutate the filter back to the buggy behaviour --------
    real_collect = F.collect_chars

    def buggy_collect(md_paths):
        chars = real_collect(md_paths)
        chars.discard(TARGET)          # exactly what str.strip() did to U+3000
        return chars

    F.collect_chars = buggy_collect
    try:
        out = _capture_build("CASE A: filter mutated to drop U+3000")
    finally:
        F.collect_chars = real_collect

    reported = "uncovered" in out
    attributed = "CAUSE A" in out
    results.append(("A1 mutated filter is REPORTED as uncovered (was: 'coverage OK')",
                    reported))
    results.append(("A2 it is attributed to CAUSE A (filter drop), not CAUSE B",
                    attributed))

    # ---------- CASE B: real filter must include the char -------------------
    out = _capture_build("CASE B: real filter")
    results.append(("B1 U+3000 is actually IN the rebuilt subset", _subset_has(TARGET)))
    results.append(("B2 no uncovered characters reported", "uncovered" not in out))

    print()
    failed = [n for n, ok in results if not ok]
    for n, ok in results:
        print(f"{'ok  ' if ok else 'FAIL'} {n}")
    print()
    if failed:
        print(f"[munge] {len(failed)}/{len(results)} FAILED")
        return 1
    print(f"[munge] {len(results)}/{len(results)} mutation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
