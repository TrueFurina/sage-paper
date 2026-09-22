# -*- coding: utf-8 -*-
"""清理善后：修悬空引用。

三类问题：
  A. 13 的复原元信息里点了已删脚本 `_rebuild13.py`，且称"本工作区无 git"（现已不成立）。
  B. audit/ 下两个脚本被移入子目录后，`ROOT = dirname(__file__)` 指向 audit/ 本身 →
     它们引用的 `01_*.md` / `logs/` / `data/` 全部失效。必须回到父目录。
  C. 若干保留脚本仍把中间产物写到仓库根目录（`_ld_summary.out` 等），会重新长出垃圾。

写盘纪律：每文件先在内存构造完整 payload → 写 `.tmp` → `os.replace`；替换 `assert count==1`。
"""
import io
import os

REPO = os.path.dirname(os.path.abspath(__file__))
report = []


def patch(relpath, pairs, note):
    """pairs: [(old, new), ...] 每对必须恰好命中一次。"""
    p = os.path.join(REPO, relpath)
    if not os.path.isfile(p):
        report.append("MISS  %-34s 文件不存在" % relpath)
        return False
    with io.open(p, encoding="utf-8") as f:
        T = f.read()
    orig = T
    for old, new in pairs:
        n = T.count(old)
        if n != 1:
            report.append("ABORT %-34s 期望命中 1 次，实际 %d 次: %r" % (relpath, n, old[:60]))
            return False
        T = T.replace(old, new)
    if T == orig:
        report.append("NOOP  %-34s" % relpath)
        return False
    with io.open(p + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        f.write(T)
    os.replace(p + ".tmp", p)
    report.append("OK    %-34s %s" % (relpath, note))
    return True


# ---------- A. 13 的复原元信息 ----------
NEW138 = (
    "> **2026-09-22 文件复原说明（元信息，非论文内容）**：本文件曾被一次**失败的写操作截断为 0 字节**"
    "（脚本以 `'w'` 模式打开目标后才抛异常）。当时本工作区**无 git、无备份**，故由 `pdf/` 下 "
    "**02:57 的渲染件 HTML 反解重建**（转换器为一次性脚本，即 `md2pdf.py` markdown 子集的逆运算）。"
    "🔴 **该次重建被检出有缺陷**：其\"改动清单\"漏记了 TutorRL 与 Puech 两轮的全部正文改动"
    "（§2.3.1 两条目段、§2.3(d) 段、§2.4.1 区分、§2.4.2 撤回），"
    "而本表第 25–27 行却已把这些改动记为 ✅ 已完成 —— 表格与正文脱节；"
    "其中 §2.4.2 一度**恢复了 TutorRL 已证伪的那条断言**，构成红线违规。"
    "已于同日以合并脚本修复全部 9 处（现 §2.3.1 计七条、§2.4.1/§2.4.2 标题与 §2.6 收尾句均已改写）。"
    "⚠️ **第 24–27 行的文本系据 `25_AppendixE_Bilingual_References.md` 的同源记载重写，非原字节**；"
    "本文件行号与 02:57 版相比有小幅偏移。"
    "✅ **2026-09-22 已建立版本控制**（`main` 分支，基线提交 `d47dbb2`），本类事故不再需要靠渲染件反解。"
    "复原与合并所用的一次性脚本已移出工作树，留存于该基线提交，通用方法固化为 `doc-truncation-recovery` 技能。"
)

p13 = os.path.join(REPO, "13_Section2_Literature_Review_en.md")
with io.open(p13, encoding="utf-8") as f:
    lines = f.read().split("\n")
hits = [i for i, l in enumerate(lines) if "文件复原说明" in l]
if len(hits) == 1:
    lines[hits[0]] = NEW138
    with io.open(p13 + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    os.replace(p13 + ".tmp", p13)
    report.append("OK    %-34s 复原元信息重写（去悬空脚本名 + 补记缺陷 + 记录已建 git）" % "13_..._en.md")
else:
    report.append("ABORT 13_..._en.md 定位到 %d 处'文件复原说明'" % len(hits))

# ---------- B. audit/ 脚本的 ROOT 与输出路径 ----------
patch("audit/audit_numbers.py", [
    ("ROOT = os.path.dirname(os.path.abspath(__file__))",
     "HERE = os.path.dirname(os.path.abspath(__file__))      # audit/\n"
     "ROOT = os.path.dirname(HERE)                          # 仓库根（本脚本在 audit/ 子目录内）"),
    ("输出: _audit_claims.txt / _audit_containers.txt / _audit_trace.txt",
     "输出: audit/claim_inventory.txt / audit/container_inventory.txt / audit/trace_rough.txt"),
    ("os.path.join(ROOT, '_audit_claims.txt')", "os.path.join(HERE, 'claim_inventory.txt')"),
    ("os.path.join(ROOT, '_audit_containers.txt')", "os.path.join(HERE, 'container_inventory.txt')"),
    ("os.path.join(ROOT, '_audit_trace.txt')", "os.path.join(HERE, 'trace_rough.txt')"),
], "ROOT 回到仓库根 + 输出改名到 audit/")

patch("audit/audit_trace_final.py", [
    ("ROOT = os.path.dirname(os.path.abspath(__file__))",
     "HERE = os.path.dirname(os.path.abspath(__file__))      # audit/\n"
     "ROOT = os.path.dirname(HERE)                          # 仓库根"),
    ("输出 _audit_final.txt", "输出 audit/traceability_report.txt"),
    ("os.path.join(ROOT, '_audit_final.txt')", "os.path.join(HERE, 'traceability_report.txt')"),
], "ROOT 回到仓库根 + 输出改名")

# ---------- C. 保留脚本不再往根目录吐垃圾 ----------
patch("_ld_collect.py", [('open("_ld_summary.out", "w"', 'open("logs/_ld_summary.out", "w"')],
      "输出移入 logs/")
patch("_refcheck.py", [('OUT = os.path.join(HERE, "_refcheck_out.txt")',
                        'OUT = os.path.join(HERE, "logs", "_refcheck_out.txt")')],
      "输出移入 logs/")
patch("_refcheck.py", [("Writes findings to _refcheck_out.txt (stdout is unreliable in this shell).",
                        "Writes findings to logs/_refcheck_out.txt (stdout is unreliable in this shell).")],
      "docstring 同步")
patch("_fontfix.py", [("io.open('_hits.txt', 'w', encoding='utf-8')",
                       "io.open('logs/_fontfix_hits.txt', 'w', encoding='utf-8')")],
      "输出移入 logs/")

with io.open(os.path.join(REPO, "_postclean_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")
print("\n".join(report))
