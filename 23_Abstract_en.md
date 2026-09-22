# SAGE · Abstract (English draft)

> **Status (2026-09-21)**: first English draft. Target: **100–120 words** (per `05`). Current: **≈120 words**.
> **Why this file exists separately**: the abstract is the last thing to write and the first thing a reviewer reads, so its
> every clause is checked against the body below. Do not edit the abstract without re-checking the mapping table.
> **Hard constraint**: the abstract must be *consistent with* the title. The title says *A Simulation Study*; the abstract
> must therefore state the study's form, and must not let a reader infer a classroom.

---

> **★ 中文要略（仅供审读；非翻译源，非口径依据 —— 一切以英文正文为准）**
>
> 摘要共五步：① LLM 导师默认给答案；② 守约型导师面对一个**归因问题**——泄露变少的同时学习者变好，等于同时动了两个变量，而现有设计不能把它们拆开；③ SAGE 的做法是把脚手架与守约放在**可独立切换**的两条通道上，于是拆解是设计属性而非事后统计，守约强度作为标量进入目标函数，其代价按**边界**而非梯度建模；④ 结果（密码学课程的**模拟研究**）：泄露率随强度从 0.85 降到 0.000，无泄露的独立解出率先升后降，内部改善中 **86% 归因于脚手架而非单纯少泄露**，变异检验会拒绝归因不成立的模型；⑤ 收尾句硬钉"这些是装置在规定式学习者模型下的性质，不是关于学生的发现"——**这句删掉，摘要就变成学习宣称**。

## Abstract

LLM tutors default to giving the answer. Tutors that withhold it face an attribution problem: one that leaks less while its learners improve has varied two things at once, and no system we reviewed separates them. In SAGE, scaffolding and answer-withholding act through independently switchable channels, so the two are separable by design; withholding enters the objective as a scalar intensity whose cost is a boundary, not a gradient. In a simulation on a graduate cryptography curriculum, leakage falls from 0.85 to 0.000 with intensity, earned independent solves rise then fall, and 86% of the improvement is attributable to scaffolding, not to withholding; mutation tests reject models in which it is not. Results are properties of the apparatus under a stipulated learner model — one in which leaked answers do not teach — not students.

**Keywords**: intelligent tutoring systems; scaffolding; answer leakage; attribution; multi-agent systems; simulation study

---

## Clause-by-clause mapping (internal, removed at submission)

| Clause | Maps to | Check |
|---|---|---|
| "LLM tutors default to giving the answer." | §1.1 / §2.2 | ✅ 有出处（Sun et al. 2026 answer-oriented mode；Suvernev 600 人课程） |
| "one that leaks less while its learners improve has varied two things at once" | §2.4.3 包问题 | ✅ 与 §7.1 同口径 |
| "no system we reviewed separates them" | §2.3 五层定位 + §2.4.3 | ✅ **2026-09-22 已按本条自身预案降级**（原文 "none separates them"）。触发原因：四库补检发现两处反例 —— Kadir (2026, arXiv 2608.00515) 做 **component attribution**、Fan et al. (2026, arXiv 2607.28128) 做**固定政策对比**，均属"归因"但归因对象不是**通道份额**；详见 `13` §2.4.3 与 `26` §2.1b。降级后仍可辩护，且不再依赖"无一例外"式断言 |
| "independently switchable channels" | §4.1 / §5.1 Arm B | ✅ 第一宣称，与题名 "Separating…" 对齐 |
| "whose cost is a boundary, not a gradient" | §3.2 Proposition 1 | ✅ 与 D6 一致；**摘要不得写 optimal intensity** |
| "In a simulation on a graduate cryptography curriculum" | §5.1 / §6.2 | ✅ 明示研究形态，与题名一致 |
| "leakage falls from 0.85 to 0.000" | §6.1.2（0.8524 → 0.0004） | ✅ 阈值形式数字，**不得用旧连续形式** |
| "earned independent solves rise then fall" | §6.1.2 | ✅ 非单调是论文对题名问题的直接回答 |
| "86% … attributable to scaffolding, not to withholding" | §6.1.3 | ⚠️ **2026-09-22 加限定**：摘要篇幅所限不展开敏感性，但收尾句已改为 "a stipulated learner model — one in which leaked answers do not teach"。**这句删不得**：86% 是 `leak_durable = 0.012` 的后果（`08` §5.4 / §6.3.1），无此限定即成无条件宣称 |
| "a stipulated learner model — one in which leaked answers do not teach" | §6.3.1 / §7.1 | ✅ **2026-09-22 新增**，把最敏感的规定值写进摘要 |
| "mutation tests reject models in which it is not" | §6.1.3 | ✅ 宣称的是**判据会拒绝**，不是数字本身 |
| "Results are properties of the apparatus under a stipulated learner model, not students." | §6.2 / §8.3 | ✅ 诚实收尾，**不可删**——删了摘要即变成学习宣称 |

## Red lines observed

- ❌ 未出现 "students learned / improved learning / classroom / course evaluation" 类措辞（"learners improve" 出现在**归因问题**的表述里，指"某导师系统的学习者变好"，不是我们的结果）。
- ❌ 未出现 "optimal / optimum / best setting"。
- ❌ 未出现 "first / novel mechanism"。
- ✅ 研究形态（simulation）与场景（graduate cryptography）均明示。

## Honest-status notes (not for publication)

| # | Item | Status |
|---|---|---|
| 1 | 词数 | ≈120，卡在上限。**若 FEDC 实际要求 ≤120，投稿前须再压 5–8 词**（候选删减：第 2 句 "and none separates them"） |
| 2 | "86%" 的敏感性区间 | 摘要未展开（正文 §6.1.3 报 76–88%）；若审稿要求，可在关键词后加一句，但会超词数 |
| 3 | Keywords | FEDC 是否要求关键词待核；若要求，控制在 5–6 个 |
| 4 | 与 §9 的关系 | §9 是摘要的展开版，**两处数字必须一致**（0.85→0.000 / 86% / 边界区间 [0.20,0.45]） |
| 5 | D9 | 若阶梯改按模态定义，M2 重跑 → 摘要数字**整体作废**，须重写 |
