# SAGE · Results (Section 6 — English draft)

> **Status (2026-09-21, revised 2026-09-21)**: partial draft. **Only the simulation study (M2) has data.**
> The classroom study (M3) is **dropped** under D20 (path ②): this is a fully simulated methodology paper,
> and the cryptography course is the application scenario, not a data-collection site (see §6.2).
> **Every number in §6.1 was re-run on 2026-09-21** with `python m2_lambda_sweep.py --seeds 40 --problems 25`
> and reproduces the archived values exactly (θ = 0.3578). Do not mix §6.1 numbers with the
> superseded continuous-form values (λ\* 0.35 / gain 0.5204 / share 85%); see `12` D9 连带发现.

---

> **★ 中文要略（仅供审读；非翻译源，非口径依据 —— 一切以英文正文为准）**
>
> §6 **只有仿真有数据；课堂研究（M3）已取消**（D20 路径②），§6.2 因此改为"全模拟范围说明"，不再是 `NO DATA` 占位——因为占位本身就是一种断言。**§6.1.2 曲线**：泄露率随强度单调下降（0.8524 → 0.0004），而无泄露独立解出率**非单调**：升到边界处 0.5659，随后回落并**触底走平**（0.2642 → 0.2651，区间重叠且末值回升）——这是"离散策略切换"而非连续代价的特征。**§6.1.3 归因**：对照臂（关掉脚手架、只留守约）只带来 +0.0594，而完整干预是 +0.4380 → **可归因份额 86%**（敏感性区间 76–88%，全篇最稳的量）。真正宣称的不是这个数字，而是**判据会拒绝**：删掉脚手架的掌握增益则拒绝；把泄露的答案改成有教益的（份额降到约 28%，见 §6.3.1 同配置表）同样拒绝。**§6.1.4 主动公开一条坏消息**：≤8 seeds 时"有教益的泄露"变异体**判错**（应拒绝却支持），16 seeds 起恢复——即判据**不是样本量无关的**，样本不足时会犯它本该防止的那个错误，故本报告用 40 seeds。
> ⚠️ 所有数字均为**阈值形式**（λ\*=0.30 / 0.5659 / 86%），不得与旧连续形式（0.35 / 0.5204 / 85%）混用。

## 6.1 Simulation study (M2): does the attribution apparatus work?

### 6.1.1 What this study is and is not

This study asks a narrow question: **under an explicitly stipulated learner model, can the design separate the contribution of scaffolding from the contribution of merely leaking less?** It does not ask whether any student learned anything, and nothing in this section is evidence about learning. The learner model and its constants are stipulated, not measured; they are listed in full so that a reader can see exactly what the simulation assumes (`m2_lambda_sweep.py`, model block).

Configuration: 240 simulated learners, 25 problems each, 40 seeds, a single scalar answer-channel bias θ fitted once (θ = 0.3578) so that the unconstrained tutor leaks at a target rate of 0.85, and a 19-point intensity grid. Calibration gates were checked before interpretation: the unconstrained tutor does leak heavily (ALR = 0.852), leakage does fall to 0.000 as intensity rises, the earned-solve peak is not saturated (0.566), a boundary is located, and crossing it does degrade performance.

### 6.1.2 The leakage curve and the boundary

Answer leakage falls monotonically with scaffolding intensity, from 0.852 at λ = 0 to 0.0004 at λ = 0.8. Earned-solve rate — the outcome we care about, a solve reached without any answer being leaked — does **not** follow it monotonically. It rises as leakage is suppressed, peaks at the boundary, and then falls as the tutor's own output collapses and the learner is locked out.

| λ | ALR [95% CI] | earned-solve [95% CI] | leak-solves | never solved |
|---|---|---|---|---|
| 0.00 | 0.8524 [0.851, 0.854] | 0.1279 [0.126, 0.129] | 0.6700 | 0.2020 |
| 0.10 | 0.5684 [0.566, 0.571] | 0.3239 [0.321, 0.326] | 0.4558 | 0.2204 |
| 0.20 | 0.2546 [0.253, 0.256] | 0.4993 [0.497, 0.502] | 0.2076 | 0.2931 |
| **0.30** | **0.0863 [0.085, 0.088]** | **0.5659 [0.564, 0.568]** | 0.0733 | 0.3608 |
| 0.40 | 0.0316 [0.031, 0.032] | 0.4870 [0.485, 0.489] | 0.0261 | 0.4870 |
| 0.60 | 0.0038 [0.004, 0.004] | 0.2705 [0.269, 0.272] | 0.0030 | 0.7265 |
| 0.80 | 0.0004 [0.000, 0.000] | 0.2651 [0.263, 0.267] | 0.0003 | 0.7347 |

Both branches are large and their confidence intervals do not overlap the peak: the rising side carries **+0.4380** (0.1279 → 0.5659) and the falling side **+0.3008** (0.5659 → 0.2651). The decomposition in the right-hand columns is the substantive point. At low intensity most solves are bought rather than earned (0.670 leak-solves against 0.128 earned); at high intensity almost nothing is solved by either route and the learner is simply shut out (0.735 never solved). The same "success" rate can be produced by leaking and by teaching, and the two are only distinguishable because we counted them separately.

We locate the **withholding boundary at λ\* = 0.30**, and we report its position as an interval rather than as a point: across the full range of the stipulated A9 constants, the located boundary falls in **[0.20, 0.45]**. The existence of the boundary and the attributable share below are stable across that range; only the location moves.

### 6.1.3 Attribution: what share is actually due to scaffolding (RQ1 analogue)

The attribution control re-runs the identical sweep with the scaffolding channel disabled, leaving only leak suppression. That control moves the outcome by **+0.0594**. The observed improvement on the rising side is **+0.4380**. The scaffolding-attributable share is therefore **86%**: roughly seven-eighths of the interior improvement is produced by scaffolding, and about one-seventh would have been obtained by suppressing leakage alone, with no improvement in guidance at all.

Across the collapse constants this share stays high, between **76% and 88%**, and it is considerably more stable than the boundary's location. It is the number on which the paper's first claim rests — and §6.3.1 establishes the precise sense in which it is conditional: stable under every constant governing the collapse, and strongly dependent on the one governing how much a leaked answer teaches.

That the control is live, rather than decorative, is established by mutation testing. Thirteen mutation checks were run; all thirteen behaved as predicted. The two that matter most for the attribution claim are: removing scaffolding's mastery gain entirely collapses the effect and the diagnostic **rejects** the proposition (share falls far below the bar); and making leaked answers genuinely instructive — so that leakage really does teach — also **rejects** it, with the scaffolding-attributable share falling to roughly **28%** at the main configuration (§6.3.1; the identical mutant reads **43%** at the smaller configuration the mutation check itself runs at) and the rest correctly credited to the leak channel. A diagnostic that could not tell these two model worlds apart would be worthless for our purpose, and this one can.

**What the mutation checks do and do not establish.** They are checks of *internal consistency*, not of external validity. Each mutant alters one parameter of the stipulated learner model and asks whether the diagnostic reacts in the direction the mechanism predicts; a pass therefore shows that the apparatus responds correctly to manipulations of a model it was built on, not that it recovers true attribution on data it has not seen. The distinction matters for how the 86% should be read: it is a property of this model under these stipulated constants, and it has not been validated against any external data set in which the true scaffolding contribution is known by other means. We know of no such data set for LLM tutoring, and we did not construct one; establishing the apparatus against one is the natural next step and is flagged as such in §8.7. Until that is done, the honest reading of this section is that the apparatus is *demonstrated to be internally coherent and reject-capable*, which is a precondition for its use, not proof of its accuracy in the field.

### 6.1.4 A caution discovered while re-running this study

One finding deserves to be reported because it constrains the simulation configuration. At 8 seeds and 8 problems per learner — a smaller configuration than the one reported above — the mutation check in which leaks are made instructive **failed**: the diagnostic returned "supported" when it should have rejected, and the harness accordingly refused to endorse the proposition. At 16 seeds the same check passes, and it passes at the configuration reported here. The diagnostic is therefore **not sample-size-free**: below a certain resolution it will credit scaffolding for an effect the leak channel produced, which is precisely the error the apparatus exists to prevent. We report this rather than quietly dropping the smaller run, because it has a direct consequence for the simulation: the reported results must use a configuration at or above the resolution floor (40 seeds here), and any future classroom extension would have to be powered well above this threshold.

## 6.2 Scope of the present evidence: simulation only (no classroom study)

**This paper reports simulation evidence only.** Following D20 (path ②), the classroom study (M3) contemplated in earlier drafts is **not run**; the graduate-cryptography course is the application scenario under which the attribution apparatus is validated, not a site from which learner data are collected. Consequently every number in this section is evidence about the *apparatus* under a stipulated learner model, and nothing here is evidence about learning (see §8.3).

The coupling of the apparatus to the cryptography curriculum is established at the **design level**: the learner model is anchored to the cryptography knowledge graph (§19), and the item bank (§5.3) is drawn from that curriculum. Because the learner model is stipulated and domain-independent, the qualitative conclusions of §6.1 carry over to the cryptography instantiation without further argument. **We state this as a limitation rather than as a result.** It means the cryptography curriculum contributes the content anchoring of the study — the knowledge graph that structures the learner model, and the item bank from which problems are drawn (§5.3) — but contributes no evidence of its own. A reader who deletes "cryptography" from the preceding sections and substitutes any other structured domain would obtain the same numbers. Nothing in §6.1 is an empirical finding about cryptography instruction, and we do not present it as one; a classroom validation of the transfer is future work (§8.7).

Two commitments are fixed now for any future classroom extension. The primary outcome would be **earned independent solve** — a solve reached without any leaked answer — not performance measured while the tutor is present. And leakage would be **double-coded** with agreement reported, since the modelled leakage estimate is not a valid measurement instrument (§8.2) and the attributable share inherits the reliability of that coding.

## 6.3 Sensitivity

Sensitivity was assessed over the stipulated constants governing collapse depth, boundary location and boundary sharpness, and over the knowledge-durability parameter. The qualitative conclusions are stable throughout: a boundary exists, crossing it degrades performance, and most of the interior improvement is attributable to scaffolding. The boundary's **location** is not stable — it moves across **[0.20, 0.45]** as the constants vary, which is why we report an interval. The attributable share varies over **76–88%** across this family of constants, never approaching the 50% bar *within that family*. That family does not include `leak_durable`, the stipulated parameter governing how much durable mastery a leaked answer confers. It is reported separately in §6.3.1 because, unlike the collapse constants, it is capable of moving the share across the bar.

### 6.3.1 The one constant that moves the share: how much a leaked answer teaches

The constants examined above govern where the boundary falls and how sharply delivery collapses. They move the boundary's *location*, which is why that location is reported as an interval. One stipulated constant behaves differently: it does not move the boundary at all, and it moves the attributable share itself. That constant is the durability of what a leaked answer confers — how much lasting mastery a learner retains from an answer that was simply given (`leak_durable`, baseline 0.012, i.e. the stipulation that a revealed answer teaches almost nothing).

This parameter matters more than its size suggests, because the attribution claim is decided by whether the share clears a bar. A parameter that shifts the share from 86% to 80% is uninteresting; one that can carry it below 50% decides the claim. We therefore scanned it at the same configuration as the main result (40 seeds, 240 learners, 25 problems), refitting the answer-channel bias θ at each value so that the unconstrained tutor leaks at the target rate of 0.85 in every case and the columns remain comparable.

| `leak_durable` | 0.012 | 0.05 | 0.10 | 0.20 | **0.22** | 0.30 | 0.50 | 0.70 |
|---|---|---|---|---|---|---|---|---|
| attributable share | **86%** | 81% | 72% | 52% | **48%** | 41% | 28% | 25% |
| verdict | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED | **REJECTED** | REJECTED | REJECTED | REJECTED |
| located boundary λ\* | 0.30 | 0.30 | 0.30 | 0.30 | **0.30** | 0.30 | 0.30 | 0.30 |

Three things follow. First, the response is smooth and monotone: the share falls from 86% to 25% across the range, crossing the 50% bar between **0.20 and 0.22**. The bar is therefore a point on a measured curve rather than a value chosen to flatter the result, and it is asserted on both sides — the scan contains values that pass and values that fail. Second, the boundary's location is **unaffected**: λ\* = 0.30 at every value, so this parameter moves how much of the improvement is creditable to guidance, not where guidance stops working. The two quantities that §6 reports are accordingly independent, and the instability of the boundary's location under the collapse constants (§6.3) does not carry over to the share. Third, and consequently, the 86% of §6.1.3 must be read as conditional: it is the value under the stipulation that a revealed answer teaches almost nothing, and it is not an estimate of the share in any population of learners.

We did not obtain an empirical value for this parameter and we do not present one. The baseline encodes a substantive position — that handing a learner a complete solution does not by itself produce durable competence — for which there is support in the intelligent-tutoring literature but no measurement we could locate in the LLM-tutoring setting. If real learners retain more from a revealed answer than our model assumes, the true share is lower than 86%, and the scan shows how much lower: at the far end of the range it is a quarter rather than seven-eighths. This is the single assumption on which the paper's first claim most directly rests, and we would rather name it than let it be discovered.

## 6.4 Summary

Under a stipulated learner model, the design produces a non-monotonic relationship between scaffolding intensity and earned independent solves, locates a withholding boundary whose position is conditional on unmeasured constants, and attributes **86%** of the interior improvement to scaffolding rather than to leak suppression, under the stipulation that a revealed answer teaches almost nothing (§6.3.1). Mutation testing shows the attribution diagnostic responds correctly to every mechanism it depends on, and fails loudly when a mechanism is removed. These are properties of the *apparatus*, demonstrated in simulation; they are not findings about students. Whether the same separation holds for human learners in a cryptography course is the question §8.7 flags as future work and this paper does not answer.

---

## Honest-status notes (not for publication)

| # | Item | Status |
|---|---|---|
| 1 | All §6.1 numbers | ✅ **Re-run 2026-09-21**, 40 seeds / 240 learners / 25 problems / θ = 0.3578; reproduces archived values |
| 2 | Mutation checks | ✅ **13/13 at 16 seeds** (README 口径). ⚠️ `08` §五 still records the older **9/9** — that count predates the addition of M8, M9 and the three liveness checks and should be updated |
| 3 | 8-seed failure | ✅ Investigated and dismissed as small-sample (resolution-floor) instability (passes at 16 seeds). **Reported in §6.1.4** as a simulation-configuration constraint, not a classroom-power constraint |
| 4 | Boundary interval / share range | Traced to the sweep logs, not to the index: `logs/_a9_threshold.log` (λ\* over its six non-structural values = 0.20/0.20/0.25/0.30/0.35/0.45 → **interval [0.20, 0.45]**; its own summary line reads `attribution share range = 76% – 88%`), with `logs/_a9_damping.log` (5/5, share constant at 86%) and `logs/_a9_sharpness.log` (4/4, 83–86%) as the other two arms. ⚠️ `data/README.md` previously served as the stated provenance — that was circular, since the README is an index, not data; corrected 2026-09-22 |
| 5 | Dead-parameter audit | **Not re-run** (`_audit_dead_params.py` did not complete in this session); README expects 17/17 |
| 6 | M3 | **Dropped** (D20 path ②, fully simulated). No classroom data will be collected; §6.2 restated as simulation-only scope |
| 7 | D9 | ✅ **2026-09-22 已裁决为接近度轴**（`12` D9）。⚠️ 原写「§6.1 replaced wholesale」**过重，已更正**：M2 的 `level_gate`/`scaffold_gain` 按 level 索引，**重排标签不改数值 → §6.1 数字不变**，仅需改 `02` §2 / `21` §4.2 的描述与示例标注（已完成） |
| 8 | §6.3.1 leak_durable 扫描 | ✅ **2026-09-22 新增并重跑**（`_ld_sensitivity.py --seeds 40 --problems 25 --learners 240`，13 值）。基线 **86%** 与主结果逐位一致（λ\*=0.30 / gain 0.5659 / left +0.4380 / ctrl +0.0594）→ **86% 确认为真值，`08` §5.4 的 84% 作废**。**翻转点修正为 (0.20, 0.22)**，旧记 0.45 系异配置扫描所致，已同步修 `01` §3.2 / `22` §7.1 / `08` §5.4 |
| 9 | λ\* 对 leak_durable 不敏感 | ✅ 新扫描实测 **λ\*=0.30 在全部 13 个取值下恒定** → 该参数只移动份额、不移动边界位置，两个量相互独立 |
| 10 | 口径统一：`43%` vs `28%` | 🔴 **2026-09-22 审计发现**：§6.1.3 曾写 "roughly 43%"，而**同一文件** §6.3.1 的表写 ld=0.50 → 28% —— 同文并列即矛盾。定案：**两值都真，但属不同配置**。43% 是变异检查自身小配置（10/120/12）下该变异体的实测值（`_check_threshold_mutants.py` 实跑 attr=43%）；28% 是主配置（40/240/25）同世界读数。正文已改为**主配置值 28% 并标注小配置读数 43%**，两值不再混用 |
| 11 | 变异检查实跑复核 | ✅ 2026-09-22 实跑 `_check_threshold_mutants.py`（默认 10/120/12）：**7/7 通过**，退出码 0。M3(0.50)→attr 43% REJECTED、M3(0.35)→attr 55% SUPPORTED。⚠️ 由此确认 **"0.35 在翻转点之内"只对该小配置成立**；主配置翻转点是 (0.20, 0.22)，两侧值应为 0.20（52%）/ 0.50（28%）。`08` §5.4 已加配置限定 |
| 12 | `[0.20, 0.45]` 与 `76–88%` 的出处 | ✅ 2026-09-22 定案：**均出自 `logs/_a9_threshold.log`**（λ_c 六值 = 0.20/0.20/0.25/0.30/0.35/0.45；日志自带 `attribution share range = 76% – 88%`）。此前第 4 行把出处写成 `data/README.md`，属**循环引用**（README 是索引不是数据），已改 |
