"""统计英文正文的篇幅，用于对照 FEDC 的 20–50 页（双倍行距 12pt ≈ 250 words/page）要求。

扣掉非论文内容：H1 标题块、`★ 中文要略` 块、`honest-status notes` 节、内部锚点行。
输出落盘 _wc_out.txt。
"""
from __future__ import annotations

import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_wc_out.txt")

BODY = [
    ("Abstract", "23_Abstract_en.md"),
    ("§1 Introduction", "07_Introduction动机链_原文证据锚定.md"),
    ("§2 Literature", "13_Section2_Literature_Review_en.md"),
    ("§3 Theory", "01_theoretical_framework_en.md"),
    ("§4 Design", "21_Section4_System_Design_en.md"),
    ("§5 Method", "17_Section5_Method_en.md"),
    ("§6 Results", "15_Section6_Results_en.md"),
    ("§7 Discussion", "22_Section7_Discussion_en.md"),
    ("§8 Limitations", "14_Section8_Limitations_en.md"),
    ("§9 Conclusion", "24_Section9_Conclusion_en.md"),
    ("App A–C", "28_AppendixABC_en.md"),
    ("App E", "25_AppendixE_Bilingual_References.md"),
]

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def strip_non_paper(text: str) -> tuple[str, int, int]:
    """返回 (正文, 去掉的中文字符数, 去掉的块数)"""
    blocks = 0

    # 1) 去掉整节：honest-status / 内部注记 / 素材说明（从标题行起直到下一个 ## 或 EOF）
    lines = text.split("\n")
    keep: list[str] = []
    skipping = False
    for ln in lines:
        low = ln.lower()
        if re.match(r"^#{2,6}\s", ln):
            skipping = bool(re.search(r"honest-status|honest status|not for publication|内部|素材|诚实状态", low))
        if not skipping:
            keep.append(ln)
    text = "\n".join(keep)

    # 2) 去掉中文要略块（引用块中以 ★ 中文要略 开头，直到该引用块结束）
    out: list[str] = []
    skipping = False
    for ln in text.split("\n"):
        if "中文要略" in ln:
            skipping = True
            blocks += 1
            continue
        if skipping:
            if ln.startswith(">"):
                continue
            skipping = False
        out.append(ln)
    text = "\n".join(out)

    # 3) 去掉纯中文行（内部注记常用中文写）
    out = []
    for ln in text.split("\n"):
        han = len(re.findall(r"[\u4e00-\u9fff]", ln))
        if han:  # 含中文的行整行不计入英文词数
            out.append("")
            continue
        out.append(ln)
    text = "\n".join(out)

    # 4) 去 markdown 标记
    text = re.sub(r"[`*>#|_]", " ", text)
    return text, 0, blocks


rows = []
total = 0
for label, fn in BODY:
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        rows.append(f"{label:<18} MISSING {fn}")
        continue
    raw = io.open(p, encoding="utf-8").read()
    body, _, blocks = strip_non_paper(raw)
    n = len(WORD.findall(body))
    total += n
    rows.append(f"{label:<18} {n:>6} words   (剥离 {blocks} 个内部块)")

rows.append("-" * 52)
rows.append(f"{'TOTAL':<18} {total:>6} words")
rows.append(f"按双倍行距 12pt ≈ 250 words/page  →  约 {total / 250:.1f} 页")
rows.append(f"按单倍行距 ≈ 500 words/page      →  约 {total / 500:.1f} 页")
rows.append("")
rows.append("FEDC 要求：blinded manuscript 20–50 页（A4, 1in 边距, 12pt TNR, 双倍行距）")

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(rows))
print("\n".join(rows))
