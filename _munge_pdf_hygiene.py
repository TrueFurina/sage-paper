# -*- coding: utf-8 -*-
"""Mutation check for _pdf_hygiene.py: prove it can actually FAIL.

A checker that has never been observed failing is decoration.  Build a PDF
that genuinely carries an embedded fallback font, run the hygiene audit on it,
and assert it is reported as FAIL.
"""
import os
import sys
import shutil

WORK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WORK)

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont
import pymupdf as fitz

from _fontsub import apply_symbol_map
from md2pdf import md_to_html_body, CSS
import _pdf_hygiene as hygiene

SRC = r"C:\Windows\Fonts\msyh.ttc"
SUBSET = os.path.join(WORK, "_sage_subset.ttf")
STALE = os.path.join(WORK, "_mut_stale.ttf")
BAD_PDF = os.path.join(WORK, "_mut_bad.pdf")

CSS_STALE = (
    '@font-face { font-family: "sagecjk"; src: url("_mut_stale.ttf"); }\n'
    + CSS.replace('"Microsoft YaHei"', '"sagecjk"')
         .replace("sans-serif", "sagecjk, sans-serif")
)

try:
    # a subset missing most CJK -> forces the fallback
    font = TTFont(SRC, fontNumber=0, lazy=True)
    opts = ft_subset.Options()
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.recalc_bounds = True
    opts.drop_tables += ["DSIG"]
    s = ft_subset.Subsetter(options=opts)
    s.populate(text="abc XYZ 0123456789 旧峰粗")
    s.subset(font)
    font.flavor = None
    font.save(STALE)
    font.close()

    with open(os.path.join(WORK, "08_M2实验审计记录.md"), "r", encoding="utf-8") as f:
        md = apply_symbol_map(f.read())
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>"
            + md_to_html_body(md) + "</body></html>")

    story = fitz.Story(html=html, user_css=CSS_STALE,
                       archive=fitz.Archive(WORK))
    writer = fitz.DocumentWriter(BAD_PDF)
    mediabox = fitz.paper_rect("a4")
    where = mediabox + (36, 36, -36, -36)
    more = 1
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()

    # --- run the audit function on the known-bad PDF ---------------------
    a = hygiene.audit(BAD_PDF)
    detected = bool(a["bad"])
    print(f"mutant PDF: {a['size']/1024:.0f} KB, pages={a['pages']}, "
          f"payload={a['payload']/1024:.0f} KB")
    print(f"  fonts       : {list(a['fonts'])}")
    print(f"  fallback    : {a['bad']}")
    print(f"  droid spans : {a['spans']}")
    print(f"  DETECTED    : {detected}")

    # --- confirm the same audit passes a healthy PDF ---------------------
    good = os.path.join(WORK, "pdf", "08_M2实验审计记录.pdf")
    g = hygiene.audit(good)
    print(f"\ncontrol PDF: {g['size']/1024:.0f} KB, fallback={g['bad']}")
    print(f"  CLEAN       : {not g['bad']}")

    ok = detected and not g["bad"]
    print(f"\nMUTATION CHECK {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
finally:
    for p in (STALE, BAD_PDF):
        try:
            os.remove(p)
        except Exception as e:
            print(f"(cleanup note: {p}: {e})")
