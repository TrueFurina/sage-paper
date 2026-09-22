# SAGE · Method (Section 5 — English draft)

> **Status (2026-09-21, revised 2026-09-21)**: English draft, **converted to a fully simulated study** (D20 path ②).
> Application scenario: **graduate cryptography curriculum** (replaces the prior Computer Science 408 classroom framing).
> Chinese mother draft `16_M3真实课堂准实验设计.md` is now archived (`_archive/408_assets_for_studyhelp/`) as a 408 reference for the study-help-pro project.
> **This section is written with the design pre-specified and the unresolved items left visibly unresolved.**
> Square brackets mark values that cannot be fixed until the simulation configuration and the cryptography item bank are finalised;
> they are placeholders, not omissions, and nothing here may be filled in after seeing data.
> Items marked `pending design decision` depend on internal choices not yet ratified.

---

> **★ 中文要略（仅供审读；非翻译源，非口径依据 —— 一切以英文正文为准）**
>
> §5 是**全模拟设定，无真实被试**（D20 路径②）。核心是四臂设计：**A 完整干预 / B 只守约不引导（归因对照）/ C 给答案的助手 / D 传统自学**——**B 臂是本文存在的原因**，因为 A 与 B 压制泄露的程度相同、只差有无引导，`A−B` 才是脚手架的贡献、`B−C` 才是"单纯少泄露"的贡献；没有 B 臂就与 §2.4.3 批评的那类评估同类。三处刻意处理：① **不用自己模拟器的效应量算样本量**（循环论证：学习器是我们规定的），功效计算改用外部文献（Brender d=0.50 → 每组约 48 人），并明示这是给**未来课堂扩展**用的；② 公开了一条**分辨率下限**——≤8 seeds 时判据会把泄漏通道的效应错记到脚手架账上，即样本不足时结论**系统性偏向我们想证明的方向**，故本报告用 40 seeds；③ 主结局是**无泄露的独立解出率**而非总解出率（总解出率会让泄露解与独立解一比一抵消）。另有两条测量禁令：泄露量**不用**目标函数里的互信息估计（已证明退化），也不用任何自我报告指标（仿真里没有自我报告）。

## 5.1 Design

We use a **fully simulated evaluation with no human participants**, set in the **graduate cryptography curriculum**. Rather than recruiting a class, we instantiate a stipulated learner model and run the four conditions of the attribution design over it. This is the design mandated by D20 (path ②): the paper is a methodology study of the *attribution apparatus*, and the cryptography course is the application scenario under which the apparatus is validated — not a claim about student learning. The cost of that choice is paid explicitly in §5.7 and §8.3.

Conditions are defined by two independently switchable channels: **withholding** (whether the tutor is permitted to reveal answers) and **scaffolding** (whether it actively guides). Crossing them yields four arms:

| Arm | Withholding | Scaffolding | Role in the design |
|---|---|---|---|
| A — SAGE | on | on | Full intervention |
| B — withholding without scaffolding | on | **off** | **Attribution control** |
| C — answer-oriented assistant | off | off | Conventional AI baseline |
| D — conventional self-study | — | — | No-AI comparison |

**Arm B is the reason this study exists.** Because A and B suppress leakage to the same degree and differ only in whether scaffolding is present, `A − B` estimates the contribution of scaffolding and `B − C` estimates the contribution of leaking less. Without arm B the two are confounded, and the study would join the class of evaluations that report a gain without being able to say what produced it — precisely the problem identified in §2.4.3. We regard this arm as non-negotiable, and we note its internal-validity cost openly below rather than burying it.

## 5.2 Simulated learners and the stipulated learner model

The evaluation runs over **240** stipulated learners, each attempting roughly twenty problems drawn from the cryptography item bank (§5.3). The learner model is **stipulated, not measured**: its functional form and constants are listed in full in `m2_lambda_sweep.py`. The configuration used for the reported results is 240 simulated learners, 25 problems each, 40 seeds, and a single scalar answer-channel bias θ fitted once (θ = 0.3578) so that the unconstrained tutor leaks at a target rate of 0.85. We expose these constants rather than hide them, because a stipulated learner can be made to show any effect we choose; the value of the simulation is in the *design* (the two independently switchable channels), not in any parameter it returns.

**One of these constants deserves to be named in the text, because it is not like the others.** The others govern where the withholding boundary falls and how sharply the tutor's delivery collapses; they move the *location* of an effect whose existence is stable. The constant governing how much durable mastery a leaked answer confers — `leak_durable`, set to 0.012 at baseline, i.e. the stipulation that a revealed answer teaches almost nothing — moves the *attributable share itself*, and it is the only constant we have found that can carry that share across the threshold at which the attribution claim fails. It is therefore reported as a first-class sensitivity in §6.3.1 rather than among the collapse constants, and we state here what that section shows: the share is a function of this constant, not a measurement of the world. We claim no empirical warrant for the value 0.012. It encodes a position — that handing a student a complete solution does not, by itself, produce durable competence — for which there is support in the intelligent-tutoring literature but no measurement in the LLM-tutoring setting, and we did not obtain one. A classroom deployment attempting to use this apparatus would need to estimate it, not stipulate it.

### 5.2.1 Why the power calculation does not use our own simulation

Our simulation reports very large effects. We do not use them to size the present simulation, and the reason matters: the simulated learner is stipulated, so its effect size is whatever we made it. Computing the required sample size from it would validate our assumptions using our assumptions. The external-effect-size reasoning below is presented for the **future classroom extension** that §8.7 calls for, not for the present study; power is therefore computed from externally published contrasts of comparable classroom interventions.

Using an external effect size rather than our own simulated effect — for reasons given above — detecting a contrast of the magnitude reported by Brender et al. (2026, d = 0.50) at conventional levels (α = 0.05 two-sided, power = 0.80) requires roughly **48 analysable students per arm** when the pre-test is used as a covariate, so about 190 across four arms; recruitment must target roughly 230 to absorb attrition and non-compliance. If the true effect is the smaller value typical of brief interventions (d = 0.40), the requirement rises to about 75 per arm, which a single course is unlikely to supply.

### 5.2.2 A resolution floor beneath which the simulation credits the wrong channel

A separate consideration bounds the simulation from below. Re-running it at reduced resolution (≤8 seeds) showed that the attribution criterion is **not** sample-size-free: with too few observations it credited scaffolding for an effect the leak channel had produced — the exact error the apparatus is built to prevent. There is thus a resolution floor beneath which the simulation yields not weak evidence but **evidence biased in the direction of our own hypothesis**. We report this because it constrains the simulation configuration (the reported results use 40 seeds, comfortably above the floor), and because it would constrain any future classroom study: a small under-powered classroom study would be worse than no study.

### 5.2.3 Clustering

Each simulated learner attempts roughly twenty problems, so the number of observations greatly exceeds the number of learners. Observations are not independent: they are clustered within learners. All analyses are clustered at the learner level, and the figures in §5.2.1 are per-learner requirements for any future classroom extension.

## 5.3 Materials

The item bank covers the **graduate cryptography curriculum** and is tagged along three dimensions — knowledge point, topic, and layer (L0 foundational through L3 advanced, per the domain knowledge graph in §19) — with knowledge-point tags mapped onto nodes of that graph, together with difficulty, item type (derivation / implementation / analysis), and whether the item is a far-transfer item. Far-transfer items require integrating at least two knowledge points and do not signal which points are required; these are reserved for the attribution-control contrasts. The bank is a **constructed evaluation instrument** for this study: items are authored against the 46 nodes of the cryptography knowledge graph (§19) across the three item types above, spanning layers L0–L3, and are self-authored rather than reproduced from any copyrighted examination, with a subset human-reviewed before inclusion. **No item count enters any parameter of the simulation** — the learner model samples by knowledge point and difficulty rather than by item identity — so the size of the bank is descriptive of the instrument and carries no weight in §6; we therefore report the construction rule rather than a count we could not defend. Because the bank is constructed rather than drawn from a validated external examination, item-level results are reported as illustrations of the apparatus, not as measurements of curriculum mastery.

## 5.4 Measures

**Primary outcome — earned independent solve.** The proportion of problems the learner solves with no answer revealed at any point in the dialogue. We deliberately do not use total solve rate: leaked solves fall as reservation rises while earned solves rise, so the two approximately cancel and the improvement disappears. The chosen outcome also matches the field's requirement that benefit be demonstrated after assistance is unavailable, since a solve reached without a leaked answer is a proxy for capability that survives withdrawal of the tutor.

**Answer-leakage rate.** The proportion of tutor turns that disclose the answer, using the *Telling@N* definition (Macina et al., 2023). The criterion is binary and is stated in advance: a turn counts as leaking if it supplies a complete proof, a complete derivation, a working implementation, or the final numerical or ciphertext result; it does not count if it offers only a counter-question, a local hint, a micro-explanation of a prerequisite, or a sub-problem. In the **simulation** this criterion is applied by the model's own emission event, which is logged per turn, so no human coding is performed and no agreement statistic is reported here; the resulting values are therefore properties of the stipulated model rather than independent measurements (§3.2, §8.2). The double-coded protocol — two raters, at least 20% of the corpus, agreement reported — applies to any **future classroom extension** (§8.7), and is pre-specified now rather than left to that study. We do **not** use the mutual-information estimate appearing in the training objective: as a measurement it is degenerate, returning its ceiling value regardless of whether leakage is present or absent (§8.2).

**Secondary outcomes.** Far-transfer performance on unseen integrated items; a **behavioural** measure of answer dependency — frequency of direct answer requests, whether the learner attempted the problem before asking, and continuation to the next ladder level after a first hint (the cascade of §4.3). Help-seeking is measured rather than treated as noise because it is not peripheral: a review of help seeking in interactive learning environments (Aleven, Stahl, Schworm, Fischer, & Wallace, 2003) treats how a learner seeks and uses help as central to what they gain from an environment that offers it, which is the same reason §4.3 places the interception at the first request rather than at the last. Alongside these, four log-derived behavioural indicators of learners' interaction patterns — clarity of conception, connectedness of knowledge, help-seeking quality (reported as two opposing sub-indicators, which we do not collapse into a single score), and persistence under difficulty `pending design decision`.

Two restrictions on the secondary measures should be stated rather than left implicit. No time-on-task measure is used, since duration has repeatedly failed to predict learning in this literature. And the four indicators are reported as **behavioural indicators**, not as a validated learner profile. Their validity is not assessed in this study: doing so would require human learners and a measurement design this study does not have, so the paper makes no claim that the profile measures anything beyond the logged behaviour it is computed from.

## 5.5 Procedure

Following instantiation of the learner model and the item bank, the four conditions are run **in parallel over the simulated cohort**; parallel timing is required so that the stipulated conditions differ only by the two switched channels and not by drift in the simulated environment. Dialogue logs are retained for the whole run. The primary and secondary measures (§5.4) are computed over the logged interactions. No human participants are involved; there is no pre-test, post-test, or delayed test in the human sense — the "pre" and "post" framing of the learner model is internal to the simulation. Leakage is determined from the logged emission event under the criterion fixed in §5.4; no human coding of tutor turns is performed in this study, and the double-coded protocol is reserved for a classroom extension (§8.7).

## 5.6 Analysis plan

Analyses are specified in advance. For the primary outcome and far transfer we use analysis of covariance with the simulated pre-state as covariate, which addresses the selection threat inherent in the stipulated learner model; group differences at baseline are reported in full rather than tested away. Clustering is handled by resampling at the learner level for interval estimates, and by multilevel models where appropriate. Multiplicity among secondary outcomes is handled by pre-specified ordering or Holm correction; effects are not selected for discussion on the basis of significance.

The attributable share is estimated as `(A − B) / (A − C)` with an interval obtained by learner-level resampling, and we report its sensitivity to unmeasured assumptions rather than a point claim about mechanism. Location parameters derived from the simulation are reported as intervals, never as recommended settings.

## 5.7 Ethics

**This study involves no human participants**, so the human-subjects approval, informed-consent, and de-identification machinery of a classroom study does not apply. The ethical concern that would attend a classroom deployment — that arm B's learners receive a tutor that refuses answers but does not guide — does not arise here, because arm B is now an internal-validity property of the simulation rather than a burden on real students (the classroom study contemplated in earlier drafts is not run in the present paper; see D20 path ②). We retain the design note about arm B because omitting it would silently remove the study's ability to make its primary claim, and we would rather state that dependency than conceal it.

---

## Honest-status notes (not for publication)

| # | Item | Status |
|---|---|---|
| 1 | Site, N, dates, subjects | **N/A** — no human participants (D20 path ②); §5.2 now describes the simulated cohort, not a site |
| 2 | Effect size basis | External (Brender et al., 2026, d = 0.50), computed by `_power_calc.py`; deliberately **not** from our simulator; now framed for the future classroom extension (§8.7) |
| 3 | Four-indicator learner description | `pending design decision` (D11); may be reduced to three |
| 4 | Intent detection component | `pending design decision` (D10); if adopted, described as descriptive only |
| 5 | Moderator variables | `pending design decision` (D13); two continuous dimensions if adopted |
| 6 | Scaffolding ladder calibration | `pending design decision` (D9); affects how arm A is described |
| 7 | M3 classroom study | **Dropped** (D20 path ②, fully simulated). `16_M3真实课堂准实验设计.md` archived to `_archive/408_assets_for_studyhelp/` |
| 8 | Cryptography item bank size | ✅ **2026-09-22 已解决，正文不再有 [N]**：§5.3 改为陈述**构造规则**（46 个图谱节点 × 3 题型 × L0–L3 层），并写明**条目数不进入模拟的任何参数**（learner model 按知识点与难度抽样，不按题目身份）→ 报构造规则而不报一个无法辩护的数字。本行保留以说明该决定 |
