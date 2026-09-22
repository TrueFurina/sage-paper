# -*- coding: utf-8 -*-
"""双盲清理：把内部文档里暗示"作者与某具体系统/申报书存在私人关系"的措辞改为中性表述。

发现的措辞（英文正文已干净，问题都在中文内部文档）：
  · "导师系统内 formalise" —— 暗示该系统的 formalise 来自作者导师
  · "导师申报书" —— 暗示与导师的基金申报目标重合
改法：改为"其自身系统""立项申报"，去掉私人关系，事实陈述不变。

纪律：每文件 tmp + os.replace；每处替换 assert count==1。
"""
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS = [
    ("11_论文成稿进度地图.md",
     "已在导师系统内 formalise 该概念",
     "已在**其自身系统内** formalise 该概念"),
    ("13_Section2_Literature_Review_en.md",
     "已在导师系统里 formalise 了 answer leakage",
     "已在**其自身系统里** formalise 了 answer leakage"),
    ("18_密码学方向迁移_评估与方案.md",
     "而它与导师申报书的目标高度重叠",
     "而它与此前一份立项申报的目标高度重叠"),
    ("26_四库交叉核验与方向锐评.md",
     "2025 年就有人在导师系统里把它 formalise 了",
     "2025 年就有人在**其自身系统里**把它 formalise 了"),
]

report = []
for rel, old, new in PAIRS:
    p = os.path.join(REPO, rel)
    if not os.path.isfile(p):
        report.append("MISS  %s" % rel)
        continue
    with io.open(p, encoding="utf-8") as f:
        T = f.read()
    n = T.count(old)
    if n != 1:
        report.append("ABORT %-38s 命中 %d 次: %r" % (rel, n, old[:40]))
        continue
    T = T.replace(old, new)
    with io.open(p + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        f.write(T)
    os.replace(p + ".tmp", p)
    report.append("OK    %-38s" % rel)

# 复查：全仓是否仍有身份暗示措辞
import glob
leftovers = []
for pat in ["导师申报", "导师系统", "导师的申报", "supervisor's (proposal|grant)"]:
    for f in glob.glob(os.path.join(REPO, "**", "*.md"), recursive=True):
        if ".git" in f or "MEMORY" in f or "2026-09-22.md" in f:
            continue  # 记忆/日志属内部历史叙事，保留原始记录
        try:
            T = io.open(f, encoding="utf-8").read()
        except Exception:
            continue
        if pat in T:
            leftovers.append("%s :: %s" % (os.path.relpath(f, REPO), pat))

report.append("")
report.append("复查残留（已排除 memory/日志，它们是内部历史叙事）：")
report += ["  " + x for x in leftovers] or ["  （无）"]

with io.open(os.path.join(REPO, "_blind_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")
print("\n".join(report))
