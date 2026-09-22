# -*- coding: utf-8 -*-
"""把 MEMORY.md 的 §3b（承重引用已核事实，最长一段）拆到同目录详表，
主文件只留最关键的 3 条 + 指针，使主文件回到可完整注入的体积。

以标题行做切分（不用长文本精确匹配），tmp + os.replace 落盘。
"""
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 本脚本在 audit/ 下，取父目录
D = os.path.join(REPO, ".workbuddy", "memory")
MAIN = os.path.join(D, "MEMORY.md")
DETAIL = os.path.join(D, "MEMORY-references.md")

T = io.open(MAIN, encoding="utf-8").read()
lines = T.split("\n")

i0 = next(i for i, l in enumerate(lines) if l.startswith("## 3b."))
i1 = next(i for i, l in enumerate(lines) if l.startswith("## 4."))
block = lines[i0:i1]
assert block and i1 > i0, "切分失败"
body = "\n".join(block).strip("\n")

header = """# MEMORY-references.md — 承重引用的已核事实（SAGE）

> 从 `MEMORY.md` §3b 拆出（2026-09-22），因主文件超出可完整注入的体积。
> **改任何正文里引用了这些文献的句子之前，必须先读本文件。**
> 通用核验方法见 `MEMORY.md` §5；文献总表见 `25_AppendixE_Bilingual_References.md`。

"""

io.open(DETAIL + ".tmp", "w", encoding="utf-8", newline="\n").write(header + body + "\n")
os.replace(DETAIL + ".tmp", DETAIL)

summary = """## 3b. 承重引用的已核事实（改正文前必查）

> 完整清单（含 Bastani / Tweed & Lehman / OpenAlex 陷阱 / leak_durable / 86% 条件性 / λ\\* 语义 / mi_hat 等逐条细节）
> 已拆到同目录 **`MEMORY-references.md`** —— **改引用相关句子前必须先读它**。此处只留最易犯的三条：

1. 🚫 **Bastani et al. (2025, PNAS 122(26), e2422633122)**：随机化单位是 **classroom 不是 student**（honors 班排除）；
   GPT Tutor 护栏**同时变了三样**（给 hints 不给答案 + 逐步引导 + 提示词注入教师正确解法与常见错误反馈）
   → **不得再写成只变了两样**；护栏**全在提示词层**。
2. 🔴 **Tweed & Lehman (2002)**：其主旨是两传统的**差异**，**不得用来支持"趋同"**（`13` §2.1 已把趋同限缩为时机条件）。
3. 🔴 **86% 是条件值**：必须带"在 `leak_durable=0.012`（泄露的答案不教人）的规定下"；且 `leak_durable` 是**唯一能推翻第一宣称**的规定常数，**一律引用 40/240/25 同配置值**。
"""
lines[i0:i1] = summary.split("\n")
io.open(MAIN + ".tmp", "w", encoding="utf-8", newline="\n").write("\n".join(lines))
os.replace(MAIN + ".tmp", MAIN)

print("main=%d B  detail=%d B" % (os.path.getsize(MAIN), os.path.getsize(DETAIL)))
