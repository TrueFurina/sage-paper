# audit/ —— 数字可追溯性审计（声明 → 原始文件 + 字段）

> 目的：论文里每一个**承重数字**都必须能追到「权威容器 + 字段」，且同表各行的配置指纹一致。
> 起因：本工作区反复在**索引层与配置标签**上出错（不是数字错，而是"指错了出处"或"把两个配置的读数并列不加限定"）。

## 文件

| 文件 | 角色 | 怎么跑 |
|---|---|---|
| `audit_numbers.py` | 步骤 1–4：抽取正文全部数字声明 → 汇总权威容器 config 指纹 → 逐条回溯 | `python audit/audit_numbers.py` |
| `audit_trace_final.py` | 对每个承重数字在权威容器中做**数字边界检索**并打印上下文 | `python audit/audit_trace_final.py` |
| `claim_inventory.txt` | 产物：正文数字声明清单（数字 + 上下文） | 由 `audit_numbers.py` 生成 |
| `container_inventory.txt` | 产物：权威容器指纹（seeds / learners / problems / bootstrap） | 由 `audit_numbers.py` 生成 |
| `trace_rough.txt` | 产物：粗回溯（早期版本，保留以对照） | 由 `audit_numbers.py` 生成 |
| `traceability_report.txt` | 产物：**逐条"声明 → 出处"的最终报告**（结论表） | 由 `audit_trace_final.py` 生成 |

脚本以 `__file__` 的**父目录**为仓库根（本目录是子目录），因此可在任意工作目录调用。

## 2026-09-22 审计结论（摘要）

**承重数字全部可溯源，无一编造。** 缺陷 5 处，全部在索引层/配置标签，已修：

1. `15` §6.1.3 与同文件 §6.3.1 **自相矛盾**（43% vs 28%）
2. `24` §9 英文正文同样写 43%
3. `22` 中文要略写 43%
4. `data/README.md` 把 `m2_lambda_alr_summary.json` 记为"主结果"，实际它是 **16 seeds** 的旧 run，**根本不含** 0.5659 / 86%
5. `15` §6.7 第 4 行的出处写成 `data/README.md` —— **循环引用**（索引不是数据源）

**最重要的一条（初判错误 → 实跑自纠）**：43% 与 28% **都是真值，只是配置不同**。
28% = 主配置（40 seeds/240 learners/25 problems）下 `leak_durable=0.50`；
43% = `_check_threshold_mutants.py` **自身小配置**（10/120/12）下同一变异体的实测值。
→ 正确处置是**加配置限定**，**不是单向覆盖**。照初判动手会把一个真值改成另一个真值，并毁掉原出处。

**只在日志里、未进索引的三条权威出处**（现已写入 `data/README.md` 与 `15`）：

| 量 | 出处 |
|---|---|
| 主 sweep + 校准门 G1–G5（λ\*=0.30 / gain\*=0.5659 / θ=0.3578） | `logs/_main_threshold.log` |
| λ\* 区间 **[0.20, 0.45]** 与归因 **76–88%** | `logs/_a9_threshold.log` |
| "86% 在深度扫描下恒定" | `logs/_a9_damping.log` |

**根因**：脚本用**固定输出名 + 不同配置反复覆盖**同一文件 → 最后一次 run 胜出 → 索引再也指不到它声称的东西。
已作废值黑名单见 `data/README.md`。

## 清理记录（2026-09-22）

| 文件 | 说明 |
|---|---|
| `cleanup_20260922_resume.py` | 临时文件清理脚本（续跑版，幂等） |
| `cleanup_manifest.txt` | 清理清单：删了什么、多大 |
| `postclean_fix_20260922.py` | 清理善后：修悬空引用 |
| `postclean_report.txt` | 善后结果 |

删除内容：73 个一次性临时文件 + 4 个目录（`__pycache__`、`_archive` 全树）。
保留判据不是"文件名看起来像临时的"，而是**引用反查**：被正文或工具链引用者留，仅被其他临时脚本引用者删。
全部删除项留存于基线提交 `d47dbb2`，可用 `git checkout d47dbb2 -- <path>` 取回。
