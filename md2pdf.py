#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAGE docs -> PDF converter.

Pipeline:  Markdown --(python-markdown)--> styled HTML --(engine)--> PDF

Two engines, tried in order:
  1. PyMuPDF (fitz)  -> pure wheel, no system deps, embeds CJK fonts from a
     TTF we locate on disk.  Preferred.
  2. fpdf2           -> pure python, unicode TTF fonts.  Fallback.

Why not weasyprint: it needs libgobject / Pango (GTK) which is not installed
on this machine; import succeeds but rendering raises OSError.
Why not pandoc/wkhtmltopdf: not installed.

Usage:
    python md2pdf.py                 # convert the default doc set
    python md2pdf.py file1.md ...    # convert specific files
"""

from __future__ import annotations

import html as _html
import os
import re
import sys
import glob
from typing import Iterable, List, Tuple

import markdown

from _fontsub import apply_symbol_map

# ---------------------------------------------------------------------------
# Font discovery (CJK-capable TTF/TTC)
# ---------------------------------------------------------------------------
FONT_CANDIDATES = [
    (r"C:\Windows\Fonts\msyh.ttc", "Microsoft YaHei"),
    (r"C:\Windows\Fonts\msyh.ttf", "Microsoft YaHei"),
    (r"C:\Windows\Fonts\simhei.ttf", "SimHei"),
    (r"C:\Windows\Fonts\simsun.ttc", "SimSun"),
    (r"C:\Windows\Fonts\Deng.ttf", "DengXian"),
    (r"C:\Windows\Fonts\arial.ttf", "Arial"),
]


def find_font() -> Tuple[str, str]:
    for path, name in FONT_CANDIDATES:
        if os.path.exists(path):
            return path, name
    raise RuntimeError("No CJK-capable font found in C:\\Windows\\Fonts")


# ---------------------------------------------------------------------------
# CSS  (light theme, print-oriented, matches the report's table-heavy layout)
# ---------------------------------------------------------------------------
CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body {
  font-family: "FONTNAME", "sagecjk", sans-serif;
  font-size: 10.5pt; line-height: 1.68; color: #1a1a1a; margin: 0;
}
h1 { font-size: 19pt; color: #0f2b46; margin: 0 0 6pt 0; line-height: 1.3;
     border-bottom: 2.5pt solid #1a4d7a; padding-bottom: 6pt; }
h2 { font-size: 14.5pt; color: #14456e; margin: 16pt 0 6pt 0;
     border-left: 4pt solid #1a4d7a; padding-left: 7pt; line-height: 1.35; }
h3 { font-size: 12pt; color: #1a4d7a; margin: 12pt 0 4pt 0; }
h4 { font-size: 11pt; color: #2c5f8d; margin: 10pt 0 3pt 0; }
p { margin: 5pt 0; text-align: justify; }
ul, ol { margin: 5pt 0 5pt 0; padding-left: 18pt; }
li { margin: 2pt 0; }
blockquote {
  margin: 7pt 0; padding: 6pt 10pt; background: #f2f6fa;
  border-left: 3pt solid #6f9ec4; color: #29455f; font-size: 10pt;
}
blockquote p { margin: 3pt 0; }
/* IMPORTANT: inline code and pre MUST resolve to our CJK subset, because the
   renderer's default monospace (Nimbus Mono PS) has NO CJK glyphs: a single
   Chinese char inside `...` makes PyMuPDF embed its 3.4 MB Droid fallback.
   We keep the monospace *look* via colour/background only. */
code, pre, kbd, samp, tt {
  font-family: "sagecjk", "FONTNAME", monospace;
  font-size: 9.4pt;
}
code {
  background: #f0f2f4; padding: 1pt 3pt; border-radius: 2pt; color: #9c2a1f;
}
pre {
  background: #f7f8fa; border: 0.6pt solid #d5dbe1; border-left: 3pt solid #6f9ec4;
  padding: 7pt 9pt; margin: 7pt 0; overflow-wrap: break-word;
  white-space: pre-wrap; font-size: 8.8pt; line-height: 1.44;
}
pre code { background: none; color: #1f2933; padding: 0; font-size: 8.8pt; }
/* Tables use bold header cells; make sure bold resolves to a declared face
   rather than a synthesised one the renderer would source elsewhere. */
table {
  border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 8.8pt;
}
th {
  background: #1a4d7a; color: #ffffff; font-weight: normal;
  border: 0.6pt solid #14456e; padding: 4pt 5pt; text-align: left;
}
td { border: 0.6pt solid #c9d4de; padding: 4pt 5pt; vertical-align: top; }
tr:nth-child(even) td { background: #f6f9fc; }
hr { border: none; border-top: 1.2pt solid #c9d4de; margin: 12pt 0; }
a { color: #1a4d7a; text-decoration: none; }
strong { color: #0f2b46; font-weight: normal; text-decoration: underline; }
em { font-style: normal; text-decoration: underline; }
"""


def md_to_html_body(md_text: str) -> str:
    """Markdown -> HTML fragment. Handles the GFM tables + fenced code used
    throughout the SAGE docs, and strips the LaTeX $$ blocks into styled
    monospace so they survive without a MathJax renderer."""
    # protect display math: $$ ... $$  -> styled block (no breakage)
    md_text = re.sub(
        r"\$\$(.+?)\$\$",
        lambda m: "\n```\n" + m.group(1).strip() + "\n```\n",
        md_text, flags=re.S,
    )
    # inline math $...$ -> `...`
    md_text = re.sub(r"\$([^$\n]{1,200}?)\$", lambda m: "`" + m.group(1) + "`", md_text)

    md = markdown.Markdown(extensions=[
        "tables", "fenced_code", "toc", "sane_lists", "attr_list", "nl2br",
    ])
    return md.convert(md_text)


def build_html(md_text: str, title: str, font_name: str) -> str:
    body = md_to_html_body(md_text)
    css = CSS.replace("FONTNAME", font_name)
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{_html.escape(title)}</title><style>{css}</style></head>"
        f"<body>{body}</body></html>"
    )


# ---------------------------------------------------------------------------
# Engine 1: PyMuPDF
# ---------------------------------------------------------------------------
def pdf_via_pymupdf(html_doc: str, out_path: str, font_path: str) -> bool:
    """Render via PyMuPDF Story.

    Font strategy (this took some digging):
      * PyMuPDF's Story renderer maps generic families to its bundled
        "Droid Sans Fallback" for CJK.  That font is ~3.4 MB and PyMuPDF
        embeds it as a *raw uncompressed stream*, producing ~3.7 MB PDFs.
      * So we instead point the CSS at a locally **subsetted** TTF
        (`_sage_subset.ttf`, built by _fontsub.py, ~0.5 MB) registered
        through a `fitz.Archive`.  Result: small, text-searchable PDFs.
      * If the subset is missing we fall back to the built-in CJK font
        (correct output, larger file).
    """
    try:
        import pymupdf as fitz
    except Exception:
        try:
            import fitz  # noqa
        except Exception as e:
            print(f"  [pymupdf] import failed: {e}")
            return False

    css = CSS
    archive = None
    subset = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "_sage_subset.ttf")
    if os.path.exists(subset):
        try:
            archive = fitz.Archive(os.path.dirname(subset))
            # register the subset under a stable name and use it in CSS
            css = css.replace(
                '"FONTNAME"',
                '"sagecjk"',
            ).replace(
                "sans-serif",
                "sagecjk, sans-serif",
            )
            css = (
                '@font-face { font-family: "sagecjk"; '
                'src: url("_sage_subset.ttf"); }\n' + css
            )
        except Exception as e:
            print(f"  [pymupdf] subset registration failed ({e}); "
                  f"using built-in CJK font")
            archive, css = None, CSS
    css = css.replace("FONTNAME", "")

    try:
        kwargs = {"html": html_doc, "user_css": css}
        if archive is not None:
            kwargs["archive"] = archive
        story = fitz.Story(**kwargs)
        writer = fitz.DocumentWriter(out_path)
        mediabox = fitz.paper_rect("a4")
        where = mediabox + (36, 36, -36, -36)
        more = 1
        while more:
            dev = writer.begin_page(mediabox)
            more, _ = story.place(where)
            story.draw(dev)
            writer.end_page()
        writer.close()
        return os.path.exists(out_path) and os.path.getsize(out_path) > 2000
    except Exception as e:
        print(f"  [pymupdf] render failed: {type(e).__name__}: {e}")
        return False


# ---------------------------------------------------------------------------
# Engine 2: fpdf2
# ---------------------------------------------------------------------------
def _fpdf_rich(fpdf_obj, text: str, font_name: str, size: float,
               color=(26, 26, 26)) -> None:
    """Very small inline markup handler: **bold** and `code`."""
    import re as _re
    fpdf_obj.set_font(font_name, "", size)
    fpdf_obj.set_text_color(*color)
    parts = _re.split(r"(\*\*.+?\*\*|`.+?`)", text)
    for p in parts:
        if not p:
            continue
        if p.startswith("**") and p.endswith("**") and len(p) > 4:
            fpdf_obj.set_font(font_name, "B", size)
            fpdf_obj.write(5.0, p[2:-2])
            fpdf_obj.set_font(font_name, "", size)
        elif p.startswith("`") and p.endswith("`") and len(p) > 2:
            fpdf_obj.set_font(font_name, "", size - 0.8)
            fpdf_obj.set_text_color(156, 42, 31)
            fpdf_obj.write(5.0, p[1:-1])
            fpdf_obj.set_text_color(*color)
            fpdf_obj.set_font(font_name, "", size)
        else:
            fpdf_obj.write(5.0, p)


def pdf_via_fpdf2(html_doc: str, out_path: str, font_path: str,
                  font_name: str) -> bool:
    try:
        from fpdf import FPDF
    except Exception as e:
        print(f"  [fpdf2] import failed: {e}")
        return False
    try:
        # Parse the HTML body back into a simple block list using markdown-free
        # regex over the already-generated HTML (headings / p / li / pre / table).
        body = re.search(r"<body>(.*)</body>", html_doc, re.S)
        content = body.group(1) if body else html_doc

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=16)
        pdf.add_font("cjk", "", font_path)
        pdf.add_font("cjk", "B", font_path)
        pdf.add_font("cjk", "I", font_path)
        pdf.set_margins(15, 15, 15)
        pdf.add_page()
        pdf.set_font("cjk", "", 10.5)

        W = pdf.w - 30

        def strip_tags(s: str) -> str:
            s = re.sub(r"<br\s*/?>", "\n", s)
            s = re.sub(r"<[^>]+>", "", s)
            return _html.unescape(s).strip()

        # tokenise top-level blocks
        blocks = re.findall(
            r"<(h1|h2|h3|h4|p|li|pre|blockquote|hr|table)\b[^>]*>(.*?)</\1>",
            content, re.S | re.I)
        for tag, inner in blocks:
            tag = tag.lower()
            if tag == "hr":
                pdf.ln(2)
                y = pdf.get_y()
                pdf.set_draw_color(201, 212, 222)
                pdf.line(15, y, 15 + W, y)
                pdf.ln(3)
                continue
            if tag == "table":
                rows = re.findall(r"<tr[^>]*>(.*?)</tr>", inner, re.S | re.I)
                data = []
                for r in rows:
                    cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S | re.I)
                    data.append([strip_tags(c) for c in cells])
                if not data:
                    continue
                ncol = max(len(r) for r in data)
                colw = W / ncol
                pdf.set_font("cjk", "B", 7.6)
                for i, row in enumerate(data):
                    # estimate row height
                    pdf.set_font("cjk", "B" if i == 0 else "", 7.6)
                    line_h = 3.6
                    maxlines = 1
                    for c in row:
                        # crude wrap estimate: CJK ~ 1 char per 3.6mm at 7.6pt
                        est = max(1, int(len(c) / max(1, (colw - 2) / 2.9)) + 1)
                        maxlines = max(maxlines, est)
                    h = maxlines * line_h + 1.6
                    if pdf.get_y() + h > pdf.h - 16:
                        pdf.add_page()
                    x0, y0 = 15, pdf.get_y()
                    if i == 0:
                        pdf.set_fill_color(26, 77, 122)
                        pdf.set_text_color(255, 255, 255)
                    elif i % 2 == 0:
                        pdf.set_fill_color(246, 249, 252)
                        pdf.set_text_color(26, 26, 26)
                    else:
                        pdf.set_fill_color(255, 255, 255)
                        pdf.set_text_color(26, 26, 26)
                    x = x0
                    pdf.set_draw_color(201, 212, 222)
                    for c in row:
                        pdf.rect(x, y0, colw, h, style="DF")
                        pdf.set_xy(x + 1, y0 + 0.8)
                        pdf.multi_cell(colw - 2, line_h, c)
                        x += colw
                    pdf.set_xy(x0, y0 + h)
                pdf.ln(2)
                pdf.set_text_color(26, 26, 26)
                continue
            if tag == "pre":
                txt = strip_tags(inner)
                pdf.set_font("cjk", "", 8.0)
                pdf.set_fill_color(247, 248, 250)
                pdf.set_text_color(31, 41, 51)
                for line in txt.split("\n"):
                    if pdf.get_y() > pdf.h - 20:
                        pdf.add_page()
                    y0 = pdf.get_y()
                    pdf.rect(15, y0, W, 4.0, style="F")
                    pdf.set_xy(16, y0 + 0.6)
                    pdf.cell(W - 2, 3.4, line[:180])
                    pdf.set_xy(15, y0 + 4.0)
                pdf.ln(1.5)
                pdf.set_text_color(26, 26, 26)
                continue
            if tag == "h1":
                pdf.ln(2)
                _fpdf_rich(pdf, strip_tags(inner), "cjk", 16, (15, 43, 70))
                pdf.ln(1)
                y = pdf.get_y()
                pdf.set_draw_color(26, 77, 122)
                pdf.set_line_width(0.7)
                pdf.line(15, y, 15 + W, y)
                pdf.set_line_width(0.2)
                pdf.ln(3.5)
                continue
            if tag in ("h2", "h3", "h4"):
                sizes = {"h2": 13, "h3": 11.5, "h4": 10.8}
                cols = {"h2": (20, 69, 110), "h3": (26, 77, 122), "h4": (44, 95, 141)}
                pdf.ln(2.5)
                if pdf.get_y() > pdf.h - 25:
                    pdf.add_page()
                y0 = pdf.get_y()
                if tag == "h2":
                    pdf.set_fill_color(26, 77, 122)
                    pdf.rect(15, y0 + 0.4, 1.4, sizes[tag] * 0.42, style="F")
                pdf.set_xy(18 if tag == "h2" else 15, y0)
                _fpdf_rich(pdf, strip_tags(inner), "cjk", sizes[tag], cols[tag])
                pdf.ln(1.8)
                continue
            if tag == "blockquote":
                pdf.set_fill_color(242, 246, 250)
                txt = strip_tags(inner)
                pdf.set_font("cjk", "", 9.5)
                est_lines = max(1, int(len(txt) / 72) + 1)
                h = est_lines * 4.4 + 2.5
                if pdf.get_y() + h > pdf.h - 18:
                    pdf.add_page()
                y0 = pdf.get_y()
                pdf.rect(15, y0, W, h, style="F")
                pdf.set_fill_color(111, 158, 196)
                pdf.rect(15, y0, 1.2, h, style="F")
                pdf.set_xy(18, y0 + 1.2)
                _fpdf_rich(pdf, txt, "cjk", 9.5, (41, 69, 95))
                pdf.set_xy(15, y0 + h)
                pdf.ln(2)
                continue
            if tag == "li":
                pdf.set_x(19)
                _fpdf_rich(pdf, "- " + strip_tags(inner), "cjk", 10.5)
                pdf.ln(0.6)
                continue
            # p
            txt = strip_tags(inner)
            if not txt:
                continue
            if pdf.get_y() > pdf.h - 20:
                pdf.add_page()
            pdf.set_x(15)
            _fpdf_rich(pdf, txt, "cjk", 10.5)
            pdf.ln(1.4)

        pdf.output(out_path)
        return os.path.exists(out_path) and os.path.getsize(out_path) > 2000
    except Exception as e:
        import traceback
        print(f"  [fpdf2] render failed: {type(e).__name__}: {e}")
        traceback.print_exc()
        return False


# ---------------------------------------------------------------------------
# Engine 3: PyMuPDF Story (richer HTML/CSS support than fpdf2)
# ---------------------------------------------------------------------------
# Fonts PyMuPDF injects when a glyph is not covered by our subset.  Any of
# these appearing in an output PDF means the subset was incomplete and the
# file is ~5x larger than it should be.  See unembedded_fallback_fonts().
FALLBACK_FONT_MARKERS = ("Droid Sans Fallback", "Noto Sans Math",
                         "Noto Sans Symbols", "Noto Serif")


def unembedded_fallback_fonts(pdf_path: str) -> List[str]:
    """Return any fallback fonts embedded in a rendered PDF.

    WHY THIS EXISTS (2026-09-19, second occurrence of this class of bug):
    `_fontsub.build_subset()` prints "coverage OK" by recomputing the character
    set from the .md sources and comparing it against a subset it just built
    *from that same set*.  That is self-consistency, not verification -- it can
    never detect a stale artifact.

    The real failure mode is ordering:

        edit 08_M2实验审计记录.md      (introduces new glyphs: 旧 峰 粗 噪 ...)
        python md2pdf.py               (renders against the PREVIOUS subset,
                                        which has no glyph for them)
          -> PyMuPDF silently embeds 3.4 MB Droid Sans Fallback
          -> no error, no warning; the only symptom is a 4.5 MB PDF
        python _fontsub.py             (rebuilds -- too late)

    A stale subset reproduces this reliably (measured: 5008 KB / 723 fallback
    spans versus 993 KB / 0).  So the check has to run on the FINAL PDF, which
    is the only place the truth exists.
    """
    try:
        import pymupdf as fitz
    except Exception:
        try:
            import fitz  # noqa
        except Exception:
            return []
    hits = set()
    try:
        doc = fitz.open(pdf_path)
        for pno in range(doc.page_count):
            for f in doc.get_page_fonts(pno):
                base = f[3] or ""
                for marker in FALLBACK_FONT_MARKERS:
                    if marker in base:
                        hits.add(base)
        doc.close()
    except Exception:
        return []
    return sorted(hits)


def subset_covers(md_paths: Iterable[str]) -> bool:
    """True if the shipped subset covers every char of the given sources.

    Cheap pre-flight so we can rebuild BEFORE rendering.  Note this is a
    necessary but NOT sufficient condition -- the PDF check below is the
    authoritative one.
    """
    try:
        from fontTools.ttLib import TTFont
    except Exception:
        return True
    subset = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "_sage_subset.ttf")
    if not os.path.exists(subset):
        return False
    try:
        f = TTFont(subset, lazy=True)
        have = set()
        for t in f["cmap"].tables:
            have |= set(t.cmap.keys())
        f.close()
    except Exception:
        return False
    for p in md_paths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                need = set(apply_symbol_map(fh.read()))
        except Exception:
            continue
        # Control characters are never glyphs and are deliberately absent from
        # the font cmap; excluding them here is what keeps this check honest.
        # (A first version compared them too and reported EVERY document as
        # uncovered, because '\n' has no glyph -- the check then fired on
        # correct subsets and told us nothing.)
        need = {c for c in need if c not in "\n\r\t\x0b\x0c"}
        if any(ord(c) not in have for c in need):
            return False
    return True


def convert_one(md_path: str, out_dir: str) -> str | None:
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Substitute characters the CJK font lacks, so that PyMuPDF never falls
    # back to its 3.4 MB bundled font (which would bloat the PDF ~5x).
    # Keep a copy of the ORIGINAL text for the .html sidecar so the HTML
    # remains a faithful copy of the source Markdown.
    md_text_mapped = apply_symbol_map(md_text)

    base = os.path.splitext(os.path.basename(md_path))[0]
    out_path = os.path.join(out_dir, base + ".pdf")
    font_path, font_name = find_font()
    html_doc = build_html(md_text_mapped, base, font_name)
    html_path = os.path.join(out_dir, base + ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html(md_text, base, font_name))

    print(f"[*] {os.path.basename(md_path)}  ({len(md_text)} chars)")
    for name, fn in (("pymupdf", lambda: pdf_via_pymupdf(html_doc, out_path, font_path)),
                     ("fpdf2", lambda: pdf_via_fpdf2(html_doc, out_path, font_path, font_name))):
        if fn():
            sz = os.path.getsize(out_path)
            # Authoritative check: a fallback font in the output means the
            # subset missed glyphs and the file is ~5x too big.  Report it
            # rather than shipping a silently bloated PDF.
            fb = unembedded_fallback_fonts(out_path)
            if fb:
                print(f"    -> {out_path}  ({sz/1024:.0f} KB, engine={name})")
                print(f"    !! BLOATED: fallback font(s) embedded: {fb}")
                print(f"    !! the subset _sage_subset.ttf is STALE -- rebuild it "
                      f"with: python _fontsub.py")
                return out_path + "\x00BLOATED"
            print(f"    -> {out_path}  ({sz/1024:.0f} KB, engine={name})")
            return out_path
        print(f"    engine {name} unavailable, trying next")
    print(f"    !! ALL ENGINES FAILED for {base}")
    return None


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "pdf")
    os.makedirs(out_dir, exist_ok=True)

    if len(sys.argv) > 1:
        files: List[str] = sys.argv[1:]
    else:
        order = [
            "FEDC投稿_引导式多智能体_深度研究报告.md",
            "README.md",
            "00_定位与口径_术语翻译表.md",
            "01_theoretical_framework_en.md",
            "02_系统架构与交互协议.md",
            "03_408知识图谱骨架.md",
            "04_题库方案与测量.md",
            "05_论文大纲.md",
        ]
        files = [os.path.join(here, x) for x in order
                 if os.path.exists(os.path.join(here, x))]
        # pick up anything else at top level
        for p in sorted(glob.glob(os.path.join(here, "*.md"))):
            if p not in files:
                files.append(p)

    ok, fail, bloated = [], [], []

    # Pre-flight: rebuild the subset if it does not cover the sources.  This
    # turns the silent-bloat failure mode into a one-line rebuild -- see
    # unembedded_fallback_fonts() for the full story.
    if not subset_covers(files):
        print("[subset] shipped subset does not cover all sources -> rebuilding")
        try:
            from _fontsub import build_subset
            build_subset(sorted(glob.glob(os.path.join(here, "*.md"))))
            print()
        except Exception as e:
            print(f"[subset] rebuild failed ({e}); rendering may embed "
                  f"a fallback font")

    for fp in files:
        r = convert_one(fp, out_dir)
        if r and r.endswith("\x00BLOATED"):
            bloated.append(os.path.basename(fp))
            ok.append(os.path.basename(fp))
        else:
            (ok if r else fail).append(os.path.basename(fp))

    print()
    print(f"[done] {len(ok)} ok, {len(fail)} failed")
    if fail:
        print("  failed:", ", ".join(fail))
    if bloated:
        print(f"  !! {len(bloated)} PDF(s) embed a fallback font (subset stale):")
        print(f"     {', '.join(bloated)}")
        print("     FIX: python _fontsub.py   then re-run this script")
    print(f"  output dir: {out_dir}")
    sys.exit(1 if (fail or bloated) else 0)


if __name__ == "__main__":
    main()
