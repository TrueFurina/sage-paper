"""Fetch a reference PDF and grep it for the numbers we cite.

Writes findings to logs/_refcheck_out.txt (stdout is unreliable in this shell).
"""
from __future__ import annotations

import io
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "logs", "_refcheck_out.txt")
TMP = os.path.join(HERE, "_refs")
os.makedirs(TMP, exist_ok=True)

URLS = {
    "ED537206": "https://files.eric.ed.gov/fulltext/ED537206.pdf",
}

PATTERNS = ["87%", "88%", "87 ", "88 ", "next hint", "continue", "level 1", "level 2",
            "bottom-out", "reading time", "neither short nor long"]

lines: list[str] = []


def extract(path: str) -> str:
    try:
        import fitz  # PyMuPDF
    except Exception as e:  # noqa: BLE001
        lines.append(f"[!] PyMuPDF unavailable: {e}")
        return ""
    try:
        doc = fitz.open(path)
    except Exception as e:  # noqa: BLE001
        lines.append(f"[!] cannot open {path}: {e}")
        return ""
    text = "\n".join(page.get_text() for page in doc)
    lines.append(f"[i] pages={doc.page_count} chars={len(text)}")
    return text


def main() -> int:
    for key, url in URLS.items():
        dst = os.path.join(TMP, f"{key}.pdf")
        if not os.path.exists(dst):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                with open(dst, "wb") as f:
                    f.write(data)
                lines.append(f"[i] downloaded {key}: {len(data)} bytes")
            except Exception as e:  # noqa: BLE001
                lines.append(f"[!] download failed {key}: {e}")
                continue
        else:
            lines.append(f"[i] cached {key}: {os.path.getsize(dst)} bytes")

        text = extract(dst)
        if not text:
            continue
        low = text.lower()
        for p in PATTERNS:
            hits = [m.start() for m in re.finditer(re.escape(p.lower()), low)]
            lines.append(f"--- pattern {p!r}: {len(hits)} hit(s)")
            for h in hits[:6]:
                snippet = text[max(0, h - 160): h + 160].replace("\n", " ")
                lines.append(f"      ...{snippet}...")
    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
