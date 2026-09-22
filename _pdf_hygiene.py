# -*- coding: utf-8 -*-
"""Pre-submission PDF hygiene check: no fallback fonts, no bloat.

Run this before any hand-off / upload.  Exit code 1 means at least one PDF is
carrying an embedded fallback font, which makes it several times larger than
necessary and means the subset font was stale at render time.

Historical note (2026-09-19): 08_M2实验审计记录.pdf shipped at 4467 KB instead
of 993 KB for exactly this reason.  The renderer reported no error and the
character-coverage assertion in _fontsub.py reported "coverage OK", because
that assertion compared the sources against a subset built from those same
sources -- it could never see a stale artifact.  The truth only exists in the
rendered PDF, which is what this script reads.
"""
import os
import sys
import glob

try:
    import pymupdf as fitz
except Exception:
    import fitz  # noqa

WORK = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(WORK, "pdf")

FALLBACK_MARKERS = ("Droid Sans Fallback", "Noto Sans Math",
                    "Noto Sans Symbols", "Noto Serif")

# A PDF is "bloated" if the embedded font payload exceeds this share of the
# file.  Normal SAGE docs carry ~709 KB of subset font; aborted renders carry
# 3.4 MB+.  Using a ratio keeps this meaningful if the docs grow.
MAX_FONT_SHARE = 0.92


def audit(pdf: str) -> dict:
    doc = fitz.open(pdf)
    fonts, payload = {}, 0
    for pno in range(doc.page_count):
        for f in doc.get_page_fonts(pno):
            base = f[3] or ""
            if base in fonts:
                continue
            sz = 0
            try:
                _, _, _, content = doc.extract_font(f[0])
                sz = len(content) if content else 0
            except Exception:
                pass
            fonts[base] = sz
            payload += sz
    pages = doc.page_count
    droid_spans = 0
    for pno in range(pages):
        for blk in doc[pno].get_text("dict")["blocks"]:
            for line in blk.get("lines", []):
                for span in line.get("spans", []):
                    if any(m in span["font"] for m in FALLBACK_MARKERS):
                        droid_spans += 1
    doc.close()
    size = os.path.getsize(pdf)
    bad = [n for n in fonts if any(m in n for m in FALLBACK_MARKERS)]
    return {"size": size, "pages": pages, "fonts": fonts, "payload": payload,
            "bad": bad, "spans": droid_spans,
            "share": payload / size if size else 0.0}


pdfs = sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf")))
if not pdfs:
    print("no PDFs found in", PDF_DIR)
    sys.exit(1)

fails = []
print(f"{'file':<44} {'KB':>7} {'pg':>4} {'font KB':>8} {'share':>6}  fonts")
print("-" * 110)
for p in pdfs:
    a = audit(p)
    problems = []
    if a["bad"]:
        problems.append(f"fallback-font:{a['bad']}")
    if a["share"] > MAX_FONT_SHARE and a["payload"] > 2_000_000:
        problems.append(f"bloat({a['share']:.0%})")
    status = "FAIL" if problems else "ok  "
    if problems:
        fails.append((os.path.basename(p), problems))
    print(f"{status} {os.path.basename(p):<43} {a['size']/1024:7.0f} "
          f"{a['pages']:>4} {a['payload']/1024:8.0f} {a['share']:>5.0%}  "
          f"{list(a['fonts'])}")

print()
if fails:
    print(f"[pdf-hygiene] FAIL: {len(fails)}/{len(pdfs)} PDF(s) need a rebuild")
    for name, why in fails:
        print(f"   {name}: {'; '.join(why)}")
    print("   FIX: python _fontsub.py && python md2pdf.py")
    sys.exit(1)
print(f"[pdf-hygiene] PASS: {len(pdfs)}/{len(pdfs)} PDFs clean "
      f"(no fallback font embedded, no bloat)")
