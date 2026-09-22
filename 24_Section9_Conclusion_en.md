# SAGE · Conclusion (Section 9 — English draft)

> **Status (2026-09-21)**: first English draft. Corresponds to `05_论文大纲.md` §9 (1 p.).
> **Rules for this section**: (i) no new claim, no new citation, no new number — §9 re-states, it does not argue;
> (ii) the study's form is stated once and plainly; (iii) §9 does not soften or re-open anything §8 conceded.
> **Cross-check**: every number below must match §6.1 and the abstract (`23`) exactly.

---

> **★ 中文要略（仅供审读；非翻译源，非口径依据 —— 一切以英文正文为准）**
>
> §9 只重述、不新增论断。对题名问题的回答是两层：**一是形状**——引导在一个两侧有界的区间里起作用，约束太弱时导师替学生做题（买到 0.670 的解 vs 自己解出 0.128），约束太强时引导自身坍缩、学生被关在门外（0.735 完全未解出），中间升到 0.5659 再回落到 0.2651；上边界不是可以和左侧权衡的偏好，而是"导师不再提供学生无法自给之物"的失效点，所以全文不写"最优强度"，也**不推荐任何工作点**（位置随规定常数在 [0.20, 0.45] 移动）。**二是方法论**——到底是引导起了作用还是只是少泄了答案，从结局里读不出来，因为两者同时被改变；分离必须在收集数据前就长在设计里。 claiming 的东西不是 86% 这个数字，而是**这个判据会失败**：删掉脚手架贡献它拒绝，把泄露的答案变成有教益的它同样拒绝（份额掉到 25–30%，见 §6.3.1）。末段给设计者两条便宜建议（暴露强度参数并记日志、评估时加一个"只守约不引导"的臂），并把"真实学习者身上是否亦然"留作本文答不了的问题。

The question this paper asks is the one in its title: *when* does guidance still help. Two answers have emerged, and they are of different kinds.

The first is a shape. Guidance helps inside a range that is bounded on both sides. Where the tutor is barely constrained, it performs the task: in our simulation most apparent success at that end is bought rather than earned, 0.670 leaked solves against 0.128 earned. Where the tutor is over-constrained, its guidance collapses and the learner is shut out: at the far end 0.735 of problems are never solved by any route. Between the two, earned independent solves rise to 0.5659 and then fall back to 0.2651. The upper edge of that range is not a preference to be traded against the lower one; it is the point at which the tutor stops supplying what the learner cannot supply. We have therefore avoided the language of an optimal intensity throughout, and we decline to recommend a setting: the boundary's location moved across [0.20, 0.45] as we varied constants we stipulated and never measured.

The second answer is methodological, and it is the paper's principal claim. Whether a tutor's benefit comes from guiding or merely from leaking less cannot be read off its outcomes, even when both quantities have been measured carefully, because the two move together. Separating them is a property the design must have before data are collected — a condition in which withholding moves without guidance — and not a technique to be applied afterwards. In the design reported here the two channels are carried by separate components and can be switched independently; running the identical sweep with scaffolding disabled moves the outcome by 0.0594 against 0.4380 for the full intervention, which is what the 86% attributable share means — under the stipulation, built into the learner model, that a revealed answer confers almost no durable mastery. That stipulation is doing real work: the share is a function of it rather than a constant of nature, and raising it moves the share down toward the 28% obtained at the main configuration in the case where leaked answers genuinely teach (§6.3.1). The apparatus is therefore not a number but a test, and its value is that it fails: it refuses the proposition when scaffolding's contribution is removed, and it refuses it when the share is driven below the bar.

What this paper does not claim should be as legible as what it does. It does not claim that SAGE taught anyone, that withholding answers is better than answering them, or that the boundary sits anywhere in particular. Every result reported here is a property of the apparatus under a stipulated learner model, obtained in simulation over a graduate cryptography curriculum. The curriculum was chosen because the distance between a hint and a complete answer is graded natively in that discipline, which makes the leakage variable annotatable rather than a matter of judgement; nothing in the paper is a finding about cryptography students, about learners, or about classrooms.

Two consequences follow for anyone building a guidance-oriented tutor, and both are cheap. Expose guidance strength as a parameter and log it, so that "how much guidance" is a reproducible condition rather than an impression. And include a withholding-only arm in the evaluation, so that a gain can be attributed rather than merely reported. A system that will not do the second is not one whose success can be interpreted, however large the gain.

The field has already said what it needs: gains that cannot be attributed to a mechanism are not yet findings, and capability should be measured after assistance is withdrawn. This paper supplies a design that meets both requirements and shows, in simulation, that meeting them changes what can be concluded. Whether the same decomposition holds for real learners is the question this study cannot answer, and it is the one that would make the rest worth having.

---

## Honest-status notes (not for publication)

| # | Item | Status |
|---|---|---|
| 1 | 数字一致性 | 0.670 / 0.128 / 0.735 / 0.5659 / 0.2651 / [0.20,0.45] / 0.0594 / 0.4380 / 86% / 25–30% —— 全部取自 `15` §6.1 与 §6.3.1 阈值形式，**与 `23` 摘要一致**；不得混入旧连续形式（0.35 / 0.5204 / 85%）。⚠️ **43% 已于 2026-09-22 作废**：该值实为**变异检查小配置**（10/120/12）读数；40-seed 主配置实测 ld=0.50 → **28%**（§6.3.1） |
| 2 | "no new citation" | ✅ 本节零新增引用（Kapur / Goldin / Weidlich 等均在 §2–§7 已引）；若后续要加，须回到对应章节先落地 |
| 3 | 与 §7.5 / §8 的关系 | §9 不复述 limitation，只在末段指向"真实学习者"这一未答问题；若 §8.7 改写，末段措辞须同步 |
| 4 | 篇幅 | ≈570 词，约 1 页（目标 1 页 ✅） |
| 5 | D9 | 若阶梯改按模态定义 → M2 重跑 → 本节数字整体作废 |
