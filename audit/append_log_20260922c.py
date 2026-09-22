# -*- coding: utf-8 -*-
"""追加当日记忆（append-only 语义：读全文 → 内存拼接 → tmp → replace）。"""
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, ".workbuddy", "memory", "2026-09-22.md")

ADD = """

## 13:50–14:05 双盲缺口：扫描 + 边界划线（新建 `27_投稿前检查清单_双盲.md`）

- 扫描结论：**英文正文本身干净** —— `supervisor` 只出现在描述 Pisan 架构的技术用法；`grant` 只是 "the request is not granted"；
  `@` 全部是 `Telling@N` 指标名（**无邮箱**）；无 `E:\\Program…` 类本机路径、无 `鹏城`/`Pengcheng`、无 `Department of`/`Acknowledg`/基金号。
- 修 4 处**语义无损**的措辞收窄：`11` L28、`13` L22/ L161、`18` L61、`26` L166 ——
  把"**导师**系统内 formalise"/"**导师**申报书"改为"其自身系统内 formalise"/"此前一份立项申报"。
- 🔴 **关键判断：不为双盲去改写内部决策文档。** `09`/`11`/`12`/`18`/`19`/`FEDC…` 里的"导师申报书"是**决策依据本身**，
  改中性只会让文档变模糊。正确处置是**划边界**：明确"哪些文件会投出、哪些不得随稿投出"，而不是删信息。
- 由此产出 `27`：分四类划清文件边界；列投稿前必做项（重点：**稿件里的 `★ 中文要略` 块与
  `honest-status notes (not for publication)` 节必须剥离** —— 它们不是论文内容；`pdf/` 渲染件**含要略块，不可直接当投稿 PDF**）；
  给出可复跑的身份扫描命令，并写明判读纪律（`University`/`@` 的命中不必然是问题，`导师` 在中文里也指"教学导师"，须看上下文）。
- ⚠️ 尚未做（已列入 `27`）：写 `strip_meta.py` 生成 `submission/`（**不原地删除**）；清 docx/pdf 的 Office/XMP 元数据。
"""

with io.open(P, encoding="utf-8") as f:
    T = f.read()
with io.open(P + ".tmp", "w", encoding="utf-8", newline="\n") as f:
    f.write(T.rstrip("\n") + "\n" + ADD)
os.replace(P + ".tmp", P)
print("log=%d B" % os.path.getsize(P))
