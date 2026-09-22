"""EduDial (arXiv:2510.12899) 全文取回 + 逐条核对我们正文里引用的数字。

输出落盘 _edudial_check.txt（本机会话 stdout 不可靠）。
"""
from __future__ import annotations

import io
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_edudial_check.txt")
TMP = os.path.join(HERE, "_refs")
os.makedirs(TMP, exist_ok=True)

DEST = os.path.join(TMP, "edudial_2510.12899.pdf")

URLS = [
    "https://arxiv.org/pdf/2510.12899",
    "https://export.arxiv.org/pdf/2510.12899",
    "http://arxiv.org/pdf/2510.12899v1",
]

PATTERNS = [
    "34,250", "34250", "345", "knowledge point", "Bloom",
    "questioning strateg", "zone of proximal", "ZPD", "metacognitive",
    "eleven", "11-dimension", "11 dimension", "dimension",
    "EduDial-LLM", "32B", "corpus",
]

lines: list[str] = []


def download() -> bool:
    if os.path.exists(DEST) and os.path.getsize(DEST) > 50_000:
        lines.append(f"[i] cached {os.path.getsize(DEST)} bytes")
        return True
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            if data[:4] != b"%PDF":
                lines.append(f"[!] {url}: not a PDF (first bytes={data[:16]!r})")
                continue
            with open(DEST, "wb") as f:
                f.write(data)
            lines.append(f"[i] downloaded {url} -> {len(data)} bytes")
            return True
        except Exception as e:  # noqa: BLE001
            lines.append(f"[!] {url} failed: {type(e).__name__}: {e}")
    return False


def main() -> int:
    if not download():
        lines.append("[X] 所有通道均失败")
        with io.open(OUT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return 1

    try:
        import fitz  # PyMuPDF
    except Exception as e:  # noqa: BLE001
        lines.append(f"[!] PyMuPDF unavailable: {e}")
        with io.open(OUT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return 1

    doc = fitz.open(DEST)
    text = "\n".join(p.get_text() for p in doc)
    lines.append(f"[i] pages={doc.page_count} chars={len(text)}")

    for p in PATTERNS:
        hits = [m.start() for m in re.finditer(re.escape(p), text, re.IGNORECASE)]
        lines.append(f"\n--- {p!r}: {len(hits)} hit(s)")
        for h in hits[:4]:
            sn = text[max(0, h - 200): h + 200].replace("\n", " ")
            lines.append(f"    ...{sn}...")

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
