# -*- coding: utf-8 -*-
"""Mutation check: prove the new guard can actually FAIL.

A test that has never been seen failing is not a test.

Problem encountered on the first attempt: the pre-flight in main() rebuilds a
stale subset automatically, so CASE A never reached the PDF-level guard and
the check reported a false FAIL.  The two mechanisms must be tested
SEPARATELY:

  CASE A -- pre-flight only: stale subset, run normally.
            Expect: "[subset] ... rebuilding", then a clean small PDF.
  CASE B -- PDF guard only: render with a stale subset by calling the internal
            API so the pre-flight is bypassed, then assert
            unembedded_fallback_fonts() finds Droid Sans Fallback.
  CASE C -- fresh subset: no rebuild, no fallback.
"""
import os
import shutil
import subprocess
import sys

WORK = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
SUBSET = os.path.join(WORK, "_sage_subset.ttf")
BACKUP = os.path.join(WORK, "_sage_subset.ttf.good_backup")
STALE_SRC = os.path.join(WORK, "_stale_subset_for_test.ttf")

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont
sys.path.insert(0, WORK)
from _fontsub import apply_symbol_map

SRC = r"C:\Windows\Fonts\msyh.ttc"

# --- build a stale subset from 05's charset (no 旧/峰/粗/噪/...) -------------
with open(os.path.join(WORK, "05_论文大纲.md"), "r", encoding="utf-8") as f:
    stale_chars = apply_symbol_map(f.read())
font = TTFont(SRC, fontNumber=0, lazy=True)
opts = ft_subset.Options()
opts.layout_features = ["*"]
opts.name_IDs = ["*"]
opts.notdef_outline = True
opts.recalc_bounds = True
opts.drop_tables += ["DSIG"]
s = ft_subset.Subsetter(options=opts)
s.populate(text=stale_chars + "0123456789abcXYZ ")
s.subset(font)
font.flavor = None
font.save(STALE_SRC)
font.close()
print(f"stale subset built: {os.path.getsize(STALE_SRC)/1024:.0f} KB")

shutil.copyfile(SUBSET, BACKUP)
results = {}

try:
    # ---- CASE A: pre-flight detects staleness and rebuilds ---------------
    shutil.copyfile(STALE_SRC, SUBSET)
    r = subprocess.run([PY, "md2pdf.py", "08_M2实验审计记录.md"],
                       cwd=WORK, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    rebuilt = "rebuilding" in out
    results["preflight_rebuilt"] = rebuilt
    print(f"\n[CASE A preflight] exit={r.returncode}  rebuilt={rebuilt}")
    for line in out.splitlines():
        if any(k in line for k in ("rebuilding", "->", "done", "BLOATED")):
            print(f"      {line.strip()}")
    results["preflight_clean"] = "BLOATED" not in out

    # ---- CASE B: bypass pre-flight, exercise the PDF guard directly ------
    import pymupdf as fitz
    import md2pdf
    shutil.copyfile(STALE_SRC, SUBSET)
    md_path = os.path.join(WORK, "08_M2实验审计记录.md")
    with open(md_path, "r", encoding="utf-8") as f:
        raw = f.read()
    mapped = apply_symbol_map(raw)
    _, fname = md2pdf.find_font()
    html_doc = md2pdf.build_html(mapped, "08_test", fname)
    probe_pdf = os.path.join(WORK, "pdf", "_guard_probe.pdf")
    md2pdf.pdf_via_pymupdf(html_doc, probe_pdf, fname)
    fb = md2pdf.unembedded_fallback_fonts(probe_pdf)
    sz = os.path.getsize(probe_pdf) if os.path.exists(probe_pdf) else 0
    print(f"\n[CASE B direct]   size={sz/1024:.0f} KB  fallback_fonts={fb}")
    results["guard_detects"] = bool(fb)
    try:
        os.remove(probe_pdf)
    except Exception:
        pass

    # ---- CASE C: fresh subset -> no rebuild, no fallback -----------------
    shutil.copyfile(BACKUP, SUBSET)
    r2 = subprocess.run([PY, "md2pdf.py", "08_M2实验审计记录.md"],
                        cwd=WORK, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    out2 = (r2.stdout or "") + (r2.stderr or "")
    results["fresh_no_rebuild"] = "rebuilding" not in out2
    results["fresh_clean"] = "BLOATED" not in out2
    print(f"\n[CASE C fresh]    exit={r2.returncode} "
          f"no_rebuild={results['fresh_no_rebuild']}")
    for line in out2.splitlines():
        if any(k in line for k in ("rebuilding", "->", "done", "BLOATED")):
            print(f"      {line.strip()}")
finally:
    shutil.copyfile(BACKUP, SUBSET)
    for p in (BACKUP, STALE_SRC):
        try:
            os.remove(p)
        except Exception as e:
            print(f"(cleanup note: {p}: {e})")

print("\n=== RESULT ===")
for k, v in results.items():
    print(f"  {k:<20} = {v}")
ok = all(results.values())
print(f"  MUTATION CHECK {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
