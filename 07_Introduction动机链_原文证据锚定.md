# 07 · Introduction 动机链（按原文证据逐句锚定）

> ## ⚠️ 题名：旧版已作废（2026-09-21）
>
> ~~**When Does Guidance Still Help? Attributing Learning Gains to Scaffolding Rather Than to Reduced Answer-Giving — Evidence from a Computer Science (408) Classroom**~~
>
> **作废原因**：场景已由 408 改为**密码学（研究生）**，且实证方式改为**纯模拟、不做课堂**
> （裁决见 `09` §十三）。旧题名的 "Evidence from a Computer Science (408) Classroom"
> **承诺了一个不存在的研究**，属虚假宣称，**必须替换后才可投稿**。
>
> ## ★ 2026-09-21 已定稿（用户已批准）：采用候选 A
>
> > **When Does Guidance Still Help? Separating Scaffolding Effects from Answer-Leakage Effects in Graduate Cryptography Instruction — A Simulation Study**
>
> **已同步的六处**：`05` Title 段 / 本文件开头 / `10` §九 / `README` / `12` D8（md 与 html） / `09` §十。
>
> **落选候选（备查，勿用）**：
> | # | 候选 | 落选理由 |
> |---|---|---|
> | ~~B~~ | *…Attributing Learning Gains to Scaffolding Rather Than to Reduced Answer-Giving in Cryptography Education* | **未明示模拟** → 有被读成实证研究的风险 |
> | ~~C~~ | *Measuring What Works: An Attribution Apparatus for … Validated in Simulation on a Cryptography Curriculum* | 方法论姿态最强，但**场景弱化** |
>
> **选择纪律（仍有效）**：题名**必须明示"仿真/模拟"**，否则与不做实证的事实冲突。
> **改题名 = 改第一宣称**，三处必须同步：题名、§1.5 贡献(1)、§3.2.4 归因分解、§6 RQ1。

> 用途：论文 Section 1 的英文初稿 + 每一句论断的**出处锚定表**。
> 纪律：**不允许出现无出处的论断**。每条主张右侧必须能在「证据」列找到原文页码/小节。
> 结构：第 1 段建立问题 → 第 2 段暴露现有解法失效 → 第 3 段定位缺口 → 第 4 段给出贡献。
>
> **★ 中文要略（§1 论点；非翻译源 —— 英文正文见 §二）**
> 动机链必须收敛成一条链，不是文献堆砌：① LLM 教育工具默认直接给答案 → ② 短期表现与长期学习**脱钩**（有实证）→ ③ 学界转向引导式（Socratic），但**前三支的约束都在生成之后/之外** → ④ 于是三重实证失效（学生能主动绕过约束／引导期内不改变行为／对话不提升元认知）→ ⑤ 领域自己承认需要"更强或**不同标定**的引导"（Brender §5.1 原话）→ ⑥ 而真正的缺口是**归因**：Weidlich et al. (2025) 审计 Deng 元分析 19 项比较，三项非协商条件同时满足者仅 21%，增益"不能自信地归因于 ChatGPT"，处方是"**在处理撤除后**测量学习"。
> 三条贡献（已重瞄）：(1) **归因测量装置**（第一宣称）——两通道可独立切换，能跑同一 sweep 并扣除"仅靠少泄露"那部分，且变异检验证明该诊断**会拒绝**归因不成立的模型；(2) **有界的可训练守约约束**，其代价是**阈值而非梯度**（据 arXiv 2604.13006 的 collapse floor），报告边界**位置及其敏感性**，**不报最优强度**；(3) 密码学课程 + 图锚定学习者模型，主结局为**无泄露的独立解出**（= 撤除辅助后的能力），且明示这是**装置层面**证据。
> ⚠️ 本文件 §1.4 与 §1.5(1) 原引"AIED 2026 research-gap synthesis"，**该出处已撤回**（实为 AI 生成知识库），2026-09-21 已全部改挂 Weidlich et al. (2025)。

---

## 一、动机链的逻辑骨架（先看这个）

动机链必须**收敛**，不能是文献堆砌。链条是：

```
① 现象：LLM 教育工具默认「直接给答案」
      ↓ 但
② 这不是小毛病：短期表现↑ 与 长期学习 脱钩（有实证）
      ↓ 所以
③ 学界转向「引导式」（Socratic）——四支脉络
      ↓ 但
④ 四支中的前三支，约束都在生成之后/之外 → 三重实证失效
      · 失效1：学生能主动绕过约束       （Brender §1.2）
      · 失效2：引导期内不改变行为       （Brender §5.1）
      · 失效3：对话不提升元认知         （K-12 RCT）
      ↓ 所以
⑤ 领域自己承认：需要「更强 / 不同标定」的引导  ← Brender §5.1 原话
      ↓ 而
⑥ 无人把它做成可训练约束 + 无人给泄露量上界
      ↓ 因此
⑦ SAGE 的三条贡献
```

**第 ⑤ 步是全篇的支点**——它不是我们说的，是 AIED 2026 最佳论文在结论里说的。

---

## 二、Section 1 英文初稿

### §1.1 The answer-oriented default and why it fails (para 1–2)

> Large language models (LLMs) have been widely deployed as learning assistants, yet their default interaction pattern remains **answer-oriented**: the student asks, the model answers. This pattern is not neutral. Recent classroom research has found that while students who use LLM assistants often achieve higher task performance, these gains are **neither indicative of students' ability to perform without the tool, nor of improved learning outcomes** (Brender et al., 2026, §1.1). Randomised evidence now establishes the disconnect directly: across a series of RCTs (N = 1,222), Liu et al. (2026, arXiv:2604.04721) find that AI assistance improves performance while present but leaves participants performing significantly worse once it is withdrawn and more likely to give up — after as little as ten minutes of exposure. Compatible EEG evidence comes from Kosmyna et al. (2025, arXiv:2506.08872, MIT Media Lab), who report that brain connectivity scaled down with the amount of external support and that LLM users had difficulty quoting from essays written minutes earlier; they term the pattern **"cognitive debt"**. That study is an unreviewed preprint whose authors caution that its conclusions are preliminary.
>
> The disconnect between *performance* and *learning* is the pedagogical core of the problem. It follows that the design question is not how to make AI tutoring more accurate, but how to structure the interaction so that assistance does not replace the learner's own reconstruction of knowledge.
>
> The magnitude of the problem is now documented at cohort scale. In a first-year programming course of **600 students**, Suvernev et al. (2026) report that as generative AI use became widespread, "the mean exam score **dropped from 72% to 54%**, while the average homework grade (done outside class) **increased**." The pattern is diagnostic: unstructured LLM assistance inflates work that is completed with the tool at hand, and collapses the ability that must be demonstrated unaided. At the same time, a total prohibition is neither realistic nor defensible, a conclusion those authors reach as well — the design obligation is therefore to keep the tool available while removing the shortcut it affords.

### §1.2 Four research strands, and what the three prompt-level strands have in common (para 3)

> Research on withholding answers has developed along four strands that share a goal but differ in **where the constraint is applied**:
>
> 1. **Socratic questioning** constrains at the **prompt** level (e.g., ChatGPT Study Mode; Liu et al., 2024).
> 2. **Cognitive scaffolding** constrains at the **output post-processing** level (e.g., graduated hinting; Thonge & Thakkar, 2026, who enforce "purely Socratic constraints through multi-layered validation").
> 3. **Learner modelling** constrains on the **input** side, by adapting to a model of the learner before generating (e.g., Chudziak & Kostka, 2025).
> 4. **Objective-level constraint** places the constraint in the training signal rather than in generation-time instructions or post-hoc filters.
>
> Strand 4 is now occupied, and it must be read carefully rather than minimised. Suvernev et al. (2026) train a family of open-source hint models for first-year programming using supervised fine-tuning, reinforcement learning with GRPO, and an **adversarial curriculum** in which a stronger model generates challenging tasks and *incorrect solutions* to expose the tutor's weaknesses; their models are paired with a **jailbreak-prevention system**. **According to their published abstract** — the full text sits behind a paywall, and we have not verified it (§2.7) — the optimisation target is hint quality and no leakage measure appears. We therefore do not write that this work involves no leakage measurement; we write only that we could not verify one, and that the mechanism described is a binary gate rather than a quantity.
>
> Other work on this strand **does** measure leakage directly, and it must be cited as such. HeuristicEdu (Wang, Song, Liu and Zou, 2026) aligns Qwen2.5-7B toward Socratic tutoring with GRPO over a heuristic reward and reports **keyword leakage falling from 30.0% to 13.3%** while a *Scaffolding Effectiveness* measure rises from 30.0% to 63.3% — the same two quantities this paper cares about, measured on a trained tutor. What that strand still lacks is not measurement but **functional form**: leakage there is an endpoint of one trained configuration, not a quantity plotted against an adjustable constraint. The rule-based validation of Thonge and Thakkar (2026) is in the same position — blocking is verified by rules, not bounded in information terms. ⚠️ **必须点名例外**：**TutorRL** (Dinucu-Jianu et al., 2025, EMNLP) **确实**把泄露惩罚做成连续可调的 λ 并画出了响应曲线与 Pareto 前沿 —— 见下一段 (ii) 的收窄表述。🚫 **不得写"无人刻画泄露—强度关系"**。
>
> One result on this strand cuts against our own formulation and we report it here rather than leaving it for a reviewer. In HeuristicEdu the best-performing variant was the one that **omitted the directness penalty** during optimisation; the authors suggest that explicit anti-leakage terms "can conflict with gradient-based behavioral alignment." Our objective places precisely such a term in the loss. We therefore treat the benefit of that term as conditional, report the condition under which it degrades rather than improves behaviour (§6.3), and do not claim it is universally beneficial.
>
> The strands therefore differ on a sharper axis than "prompt versus training": **whether the design supplies any bound on leaked answer information at all.** We return to this in §1.4.


### §1.3 Three documented failure modes (para 4) ← **核心段落**

> **Failure 1 — learners can actively circumvent the constraint.** Studying a Socratic-guidance tutor in a graduate programming course, Brender et al. (2026, §1.2) report that "students **resisted restrictive interfaces**, despite recognizing potential benefits, and **may actively bypass constraints to obtain full responses**." The finding is not specific to that tutor's design. Independently, in an undergraduate computer science course, Sunil and Thakkar (2025) deployed a tutor whose input layer validates student queries for completeness and relevance before any feedback is issued, and observed that "a subset of students attempted to **circumvent reflective prompts** or **reformulate prohibited solution requests**." Two different research groups, in two different courses, using two different constraint mechanisms, converged on the same result: a constraint that a student can talk their way around is a soft constraint, regardless of how it is implemented.
>
> The pattern is not confined to observation, and the strongest published corroboration is now adversarial rather than anecdotal. Zhao, Knežević and Käser (2026, ACL 2026) adapt six families of adversarial and persuasive techniques to the educational setting and probe how likely a tutor is to reveal a final answer; they report that in-context adversarial student agents "often fail to carry out effective attacks," and that it takes a **fine-tuned** adversarial student agent to reliably jailbreak LLM-based tutors — across model families, pedagogically aligned models, and a multi-agent design. Read in the direction that matters for design: a learner does not merely stumble around a constraint; a competent adversary can be trained to defeat it, and the defeat rate is itself measurable. Two independent classroom observations and one adversarial benchmark now agree — a constraint a student can talk their way around is a soft constraint.
>
> **Failure 2 — during instruction, prompt-level guidance does not change behaviour.** Comparing a Socratic-Guidance tutor against a Prompt-Refinement tutor over a six-week intervention (N = 66), Brender et al. (2026, §5.1) found "**neither tutor** led to greater adoption of [learning-conducive patterns] during guided use." The two conditions were also indistinguishable on task performance and prompting behaviour while the scaffold was in place; differences emerged **only after the scaffold was removed**. Prompt-level guidance is therefore not merely unguaranteed — it is, by the authors' own measurement, **inert while it is active**.
>
> **Failure 3 — Socratic dialogue does not, by itself, build metacognition.** In a randomised controlled trial with 90 tenth-grade science students comparing a control, an argument-driven-inquiry condition, and an AI-powered condition using ChatGPT Study Mode, gains were significant for scientific argumentation, critical thinking, self-efficacy, and cognitive engagement — but "**effects on metacognitive self-regulation were nonsignificant**" (Kao, Grant and Woltering, 2026, **preprint**). That is: a learner can be walked to a correct answer without their own awareness of what they do and do not know being improved at all.

### §1.4 The gap the field itself has named (para 5) ← **支点**

> These three findings converge on a conclusion that the field has already stated. Brender et al. (2026, §5.1) close their discussion of guidance design with the observation that inducing learning-conducive engagement "**may require stronger or differently calibrated forms of guidance** than those explored here." Their limitations section adds that the observed effects "may depend on how the tutors were **calibrated**; different **levels of guidance** may lead to different interaction patterns and learning outcomes" (§5.3).
>
> "Stronger" points to a constraint that cannot be circumvented by learner phrasing. "Differently calibrated" points to guidance intensity as an explicit, tunable design variable with non-trivial structure (§2.4.1) — not, we note, with a locatable optimum, which is a different and unsupported claim. Neither has been realised in existing work. Contemporary Socratic tutors, including the multi-agent math tutoring platform of Chudziak and Kostka (2025), continue to implement guidance as prompting strategy, and the authors themselves note the consequence — "**system performance remains fundamentally dependent on underlying LLM capabilities and possible biases**" (§6).
>
> More recent work has moved toward training, but not toward measurement. Suvernev et al. (2026) demonstrate that hint quality can be optimised by reinforcement learning, yet they protect against answer leakage with a **jailbreak-prevention filter** — a binary gate that classifies an output as acceptable or not, rather than a quantity that could be calibrated or plotted against constraint strength. The gap must therefore be stated at the width the 2026 literature actually leaves, which is considerably narrower than it was a year ago. **(i)** Guidance intensity is no longer unexposed: Pisan (2026) reports a deployed tutor in which a non-LLM policy core sets a per-turn ceiling on an **eight-rung help ladder**, and the withholding behaviour is tuned against evidence. **(ii)** must be stated more narrowly than we first wrote it, because a training-layer system already supplies part of it: **TutorRL** (Dinucu-Jianu et al., 2025, EMNLP) treats the leakage penalty as a **continuously adjustable weight λ** and reports three curves against it — ΔSolve rate, leaked-solution rate and pedagogical reward — together with a Pareto frontier between student success and leakage. A continuously adjustable quantity *and* its leakage curve therefore both exist, and we withdraw the stronger formulation. What we have not found is the **combination**: no system we have found varies a graded constraint against an observed leakage curve **and** measures the outcome after the tutor is withdrawn — TutorRL's outcome is the immediate post-dialogue solve rate — **and** decomposes the resulting gain into the scaffolding and withholding channels that produced it. The rest of the training strand reports leakage as an endpoint of one configuration (Wang et al., 2026) and the audit strand as a rate per condition (Zhao et al., 2026; Fan et al., 2026); neither of those varies a constraint. **(iii)** Most importantly — and this is the gap the field identified for itself — no existing system decomposes an observed improvement into **additive parts**, reporting separately the share produced by better scaffolding and the share produced merely by leaking less.
>
> The third point requires its nearest neighbours to be named, because they are close and a reviewer will look for them. Zhao, Knežević and Käser (2026) benchmark *whether* leakage occurs under adversarial pressure and propose a standardised robustness benchmark around a fine-tuned adversarial student agent. Fan et al. (2026) fix the base model and a weak simulated student, contrast a conversational against a pedagogical policy, and find that "answer-revealing turns are followed by less independent student work on every base" — the same co-variation this paper studies, measured with deterministic detectors and a condition-blind judge. Kadir (2026) performs **component attribution** over a release pipeline separating selection, generation, verification and enforcement failures and reports a safety–utility frontier; ExplainRoute (Gai, Zhang and Huang, 2026) audits information boundaries before deployment and states plainly that its contribution is a validated audit protocol and a boundary finding rather than evidence of causal instructional effectiveness. Together these establish *that* leakage occurs, *that* it co-varies with subsequent independent work, and *which component* failed. None of them attributes a **share of an outcome gain** to a channel, and none supplies a test by which the attribution can fail. A system that reduces leakage and improves learning at the same time, without decomposing the two, cannot answer the question that audit posed — and Suvernev et al. (2026), whose intervention moves both quantities at once, is a case in point. An audit of the nineteen comparisons inside the Deng et al. (2025) meta-analysis found that reproducibility, operationalised control and valid measurement of learning were met simultaneously by only **21%** of them, and concluded that "observed gains cannot, at this time, be **confidently attributed** to ChatGPT," prescribing instead that learning be measured "after the treatment is removed" (Weidlich, Gašević, Drachsler and Kirschner, 2025). A system that reduces leakage and improves learning at the same time, without decomposing the two, cannot answer that question — and Suvernev et al. (2026), whose intervention also moves both quantities at once, is a case in point. Thonge and Thakkar (2026) come closest on mechanism — their tutor "persists on specific conceptual gaps rather than abandoning them when students deflect or express frustration," and adapts "questioning intensity based on detected learner confidence signals" — but intensity there is a discrete response mode, not a measurable design variable, and no leakage measure is reported.
>
> That the prompt level is insufficient is not our inference; recent work states it directly. SocraticPO (Liu et al., 2026) is a **policy-optimisation** framework in which a teacher model supplies Socratic-style guidance to a *student policy* being trained by reinforcement learning — its "student" is a model, not a learner — and it reports in its own analysis that "**even when the prompt explicitly asks the teacher not to reveal the answer**, a teacher with ground-truth access **may still leak solution-specific hints**," and that this failure is "**inherently limited by the teacher model's instruction-following ability**." The authors further warn that ground-truth access "can shift the teacher from diagnosing the student's reasoning process to **reverse-engineering hints from the known answer**," and they observe empirically that guidance "can **become negative when the teacher turns the answer into overly direct hints**." We cite these statements as evidence about the limits of prompt-level control, and we state their scope: SocraticPO optimises a policy on benchmark tasks, so the directness of its hints is not quantified with any instrument from the tutoring literature. That absence is a difference of research object, not a gap in that work, and we do not count it as one. SocraticPO addresses a genuine and adjacent problem — a policy that learns to wait for assisted success rather than to solve — by **decaying the reward** for assisted success, a mechanism situated on the reward side and parameterised by a data-driven statistic rather than a tunable knob. The content side, that is to say *what the tutor is permitted to say*, remains governed by prompt instructions in that work as well. Together these papers locate the field's frontier precisely: the constraint must move off the prompt, and it must become measurable. SAGE takes both steps, on the content side, and complements reward-side work such as SocraticPO rather than competing with it.


### §1.5 Contributions (para 6)

> We present **SAGE (Socratic Adversarially-Guided Engine)**, a multi-agent tutoring system that moves the answer-withholding constraint from prompting into the training objective, and we evaluate it in a controlled simulation of cryptography learning. Our contributions are threefold, and the first is methodological rather than architectural.
>
> **(1) An attribution apparatus: measuring which mechanism produced the gain.** The field has named this as its principal open problem. An audit of the nineteen comparisons inside the Deng et al. (2025) meta-analysis found that reproducibility, operationalised control and valid measurement of learning were met simultaneously by only **21%** of them, and concluded that "observed gains cannot, at this time, be **confidently attributed** to ChatGPT" — the same audit prescribing that learning be measured "after the treatment is removed" (Weidlich, Gašević, Drachsler and Kirschner, 2025). SAGE is built to answer that question rather than to raise it. Scaffolding and withholding act through separate, independently switchable channels, so we can run the **identical** sweep with scaffolding disabled and subtract what leak-suppression achieves on its own; we report the share of the interior improvement that is attributable to scaffolding rather than to the suppression of leaked answers, and we show by mutation testing that the diagnostic **rejects** models in which that attribution does not hold. Effect sizes in this literature are routinely reported without such a separation. We make the separation the headline, because without it a gain in scaffolded learning cannot be distinguished from a gain produced merely by leaking less.
>
> **(2) A bounded, trainable withholding constraint, and evidence that its cost is a threshold rather than a gradient.** We formalise withholding as an information bottleneck on the pathway from the learner's knowledge state to the revealed answer, giving the objective a single interpretable knob — **scaffolding intensity λ**. Where existing trained tutors enforce withholding through a binary gate (Suvernev et al., 2026: a jailbreak-prevention filter, as described in their published abstract) or rule-based validation (Thonge & Thakkar, 2026), our formulation makes the **amount** of permitted answer information an explicit term in the objective, so the constraint can be tightened or relaxed continuously rather than switched on or off. Extending MathDial's *Telling@N* metric (Macina et al., 2023) — used by Chudziak and Kostka (2025) to compare two prompting strategies, and by Thonge and Thakkar (2026) not at all — we characterise the **relationship** between constraint strength and answer-leakage rate rather than comparing isolated configurations, and we characterise that relationship rather than a single configuration. We do not claim to be first to measure leakage on a trained tutor — Wang et al. (2026) report keyword leakage for a GRPO-aligned tutor, and Zhao et al. (2026) benchmark it under attack — but those figures are endpoints or rates attached to fixed systems, not responses to a constraint that is being varied. Crucially, we do **not** report this relationship as a smooth trade-off with a preferred interior operating point, because the available evidence does not license that reading. The nearest evidence is borrowed from an adjacent literature and is cited as such. Potraghloo et al. (2026, §4.1) report, across seven instruction-tuned models spanning five families, that compositional lexical constraints show a **collapse floor** — "banning commas and colons together (−29.8%) produces only marginally worse results than banning commas alone (−27.0%), suggesting a discrete strategy switch rather than continuous degradation" — and that the mechanism is a planning failure rather than a capability limit, since two-pass generation recovers 59–96% of response length. We adopt the **shape** and state plainly that the adoption is an analogy, not evidence from our setting: that paper contains no measure of answer leakage, no tutoring scenario, no notion of scaffolding intensity and no learner of any kind. It is precisely because the shape is borrowed that the three constants governing it are stipulated rather than measured (§8.1). We model the constraint's cost as a boundary and report the location of that boundary and its sensitivity to the model's unverified constants. This is the operationally useful form of the "differently calibrated" guidance the field has called for: a deployed system watches its **distance to a cliff**, not its proximity to a peak. **We also state the risk that runs against our own formulation.** Wang et al. (2026) report that their best-performing GRPO variant was the one that omitted the directness penalty, the authors suggesting that explicit anti-leakage terms can conflict with gradient-based behavioural alignment. Our objective places such a term in the loss, and our study cannot test whether that is wise: it is a simulation without a gradient-based training loop, so it specifies the constraint's effect rather than learning it. We therefore record the risk as untested in §8.2 and do not claim the term is universally beneficial.
>
> **(3) A learner-model-coupled evaluation in which the outcome is measured after assistance ends, demonstrated in a stipulated simulation.** Socratic tutoring has by now been evaluated in real settings — graduate mobile robotics (Brender et al., 2026), undergraduate programming (Suvernev et al., 2026; Lee et al., 2026; Sun et al., 2026), teacher education (Degen & Asanov, 2025), and K–12 science (2026) — and several of these couple tutoring to a learner model. The coupling as such is not ours to claim: ScaffoldLM (Li, Zhu, Wang, Li and Huang, 2026, ACL) already infers a learner's cognitive state through an assessment-driven control loop and selects tutoring actions from it (§2.3.1). What we have not found supplied together, in any of them, are three things: a learner model anchored to a knowledge graph and used to locate the specific knowledge-point bottleneck from the learner's own responses; a primary outcome measured as capability that survives withdrawal of the scaffold rather than as performance while the scaffold is present — the *form* of that outcome is not ours either, since Puech et al. (2025) already withhold credit for reasoning the tutor supplied, though they compute it from the conversation with the tutor present (§2.3.1); and a withholding constraint carried on a channel that can be switched independently of the scaffolding, so that the two can be separated rather than argued apart. We demonstrate the combination, not any one of its parts, in a stipulated cryptography-learning simulation in which scaffolding focus and exercise selection are driven by the learner model, and our primary outcome is not whether a learner succeeds with the tutor present but whether they solve **without any leaked answer** — a solve reached through the tutor's help alone. The design also carries the metacognitive component that prior Socratic interventions left unaddressed (Failure 3); because it depends on learner self-report, it is specified as an **intervention only** and is not reported as an outcome of this study (§4.6). Because the learner model is stipulated, contribution (3) is evidence about the *apparatus*, not about students; a classroom extension is stated as future work (§8.7), not claimed here.


---

## 三、出处锚定表（每一句论断 → 原文）

| # | 论断 | 出处 | 原文关键句 |
|---|---|---|---|
| 1 | 短期表现与长期学习脱钩 | Brender 2026 §1.1 | "gains are **neither indicative of students' ability to perform without the tool** nor of improved learning outcomes" |
| 2 | 「认知债」效应 | ✅ **2026-09-22 已溯源原文**：Kosmyna, N., Hauptmann, E., Yuan, Y. T., Situ, J., Liao, X.-H., Beresnitzky, A. V., Braunstein, I., & Maes, P. (2025). *Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task*. arXiv:2506.08872 [cs.AI]. MIT Media Lab | 原文支持的表述："Brain connectivity **systematically scaled down** with the amount of external support"; "The **reported ownership** of LLM group's essays ... was low"; "The LLM group also **fell behind in their ability to quote** from the essays they wrote just minutes prior." ⚠️ **旧录的 "reduced critical evaluation of LLM outputs" 在原文摘要中无据**（属 Brender 二手转述），已删。另：该文至今仍为**预印本且未经同行评审**，作者明示结论应视为初步结果 | 🔴 **承重改由 Liu et al. (2026) 的 RCT 承担**（N=1,222，随机对照，撤除辅助后测量） |
| 3 | **学生可主动绕过约束** | **Brender 2026 §1.2** | "students **resisted restrictive interfaces** ... and **may actively bypass constraints to obtain full responses**" |
| 4 | **引导期内两种导师均无效** | **Brender 2026 §5.1 (RQ2)** | "**neither tutor** led to greater adoption of [learning-conducive patterns] during guided use" |
| 5 | 差异只在脚手架移除后出现 | Brender 2026 §5.2 (RQ3) | "these differences were **not observed during the guided sessions, but emerged only in the unconstrained setting**" |
| 6 | **Socratic 对话不提升元认知** | **K-12 RCT 2026** | "Effects on **metacognitive self-regulation were nonsignificant**" |
| 7 | **★ 领域呼唤更强的引导** | **Brender 2026 §5.1** | "may require **stronger or differently calibrated forms of guidance** than those explored here" |
| 8 | **★ 引导强度是有最优值的设计变量** | **Brender 2026 §5.3** | "may depend on how the tutors were **calibrated**; different **levels of guidance** may lead to different interaction patterns and learning outcomes" |
| 9 | 现有系统仍依赖底层 LLM 能力 | Chudziak & Kostka 2025 §6 | "**system performance remains fundamentally dependent on underlying LLM capabilities and possible biases**" |
| 10 | **审稿人指其缺真实学生评估** | **Chudziak & Kostka 2025 §6** | "**a significant limitation noted by reviewers is the lack of evaluation with real students in learning environments**" |
| 11 | 个性化只基于基础属性 | Chudziak & Kostka 2025 §6 | "Current personalization operates on a **basic set of attributes**" |
| 12 | 现有 Socratic 评估全为教学行为指标 | SocraticLM (NeurIPS 2024) | 五维评估（Overall/IARA/CARA/SER/SRR）**均为教学行为，无一测学习增益** |
| 13 | Turning 测「拒答无关问题」而非「顶住索要答案」 | SocraticLM (NeurIPS 2024) | SRR 定义为拒绝无关问题并拉回教学，**不涉及学生反复索要答案的场景** |
| 14 | 学生感知引导式更低效 | Brender 2026 §5.1 | "students in the SG condition rated their tutor **less favorably**"；"learners perceived the SG tutor as **less efficient**" |
| 15 | 母语能力造成额外交互成本（可作 §7 讨论） | AMCIS 2026 TREO | "Each one-point increase in [technical English] proficiency was associated with approximately **3.18 fewer turns to resolution**" |
| 16 | Socratic Gap：对零基础学生为负 | AMCIS 2026 TREO | "prior programming experience moderated the relationship (p = .045). Longer conversations were slightly **negative for absolute beginners** but positive for students with prior experience" |
| 17 | **🔴 已有用 RL+GRPO+对抗课程训练 hint 模型** | **Suvernev et al., 2026 (EDULEARN26)** | "training the model using **reinforcement learning (RL) with GRPO** ... and an **adversarial curriculum-learning** approach, in which a stronger model is trained to generate increasingly challenging tasks and incorrect solutions" |
| 18 | **🔴 但用 jailbreak 过滤器而非量化约束** | **Suvernev et al., 2026** | "OPTMentor, a visual in-browser debugger that integrates LLM calls plus a **jailbreak-prevention system** to keep the interaction academically safe"（二值门控，**无泄露量测量**） |
| 19 | **🔴 已在真实 CS 课堂部署且有效** | **Suvernev et al., 2026** | 600 名大一；均分 72%→54%；pilot 后大部分学生提升 10–30%，**平均 +11.9%**；full run 均分回到 70%+ |
| 20 | ✅ **真实身份已定位（2026-09-22）**：**Ayush Thonge & Aalok Thakkar**, *A Good Rubber Duck Does Not Quack: Designing Socratic Scaffolding in AI Tutors*, **ITiCSE 2026**, pp. **196–202**, DOI `10.1145/3803400.3809368`（Ashoka University，gold OA, CC-BY-NC-ND） | 🔴 **摘要可核部分**：*"We present Socratic AI, a **VS Code-integrated tutor** that addresses this through pedagogically-grounded Socratic dialogue **constrained to withhold direct solutions**"*；动机句 *"...generating correct solutions instantly ... undermines the struggle necessary for conceptual learning"*。🔴 **以下两处措辞无法从摘要验证**（"**stateful misconception detection** ... multi-layered validation that blocks code generation"；"adapts **questioning intensity** based on detected learner confidence signals"）→ **`13` §2.3(b) 与 §2.4.1 已降到摘要强度**，取得 ACM 全文前不得回引 |
| 21 | 🔴 **暂不可用作设计理据**（曾是 §4.3 拦截协议"顶住推诿而不放弃"的唯一外部来源） | Thonge & Thakkar, 2026；原引句为 "persist on specific conceptual gaps rather than **abandoning them when students deflect or express frustration**" | ⚠️ **该句不在摘要里，也无法在任何公开索引核到** → 取得全文前，**§4.3 的该理据必须自给自足**。可用替代理据（均已核）：**Baker et al. (2004, CHI)** 的 gaming-the-system 定义 + **Aleven et al. (2003, RER)** 求助行为综述 + **Goldin et al. (2012)** Table 2。**本条待 ACM 全文，不作承重** |
| 22 | 本科 CS 课大规模自适应苏格拉底对话 | Lee et al., AIED 2026 (Socratic Mind) | "Implemented in an **undergraduate computer science course** ... adaptive Socratic dialogue" |
| 23 | 80 名大学生准实验（CS 编程） | Sun et al., JCAL 2026 | 80 college students；GSL vs GDL；quasi-experimental |
| 24 | **★ 学生绕过约束的第二独立佐证** | **Sunil & Thakkar, 2025 (arXiv 2512.03501)** | "a subset of students attempted to **circumvent reflective prompts** or **reformulate prohibited solution requests**" |
| 25 | **★ prompt 明确禁答仍会泄露（领域自认）** | **SocraticPO, 2026 (arXiv 2606.09887) §5.4** | "**even when the prompt explicitly asks the teacher not to reveal the answer**, a teacher with ground-truth access **may still leak solution-specific hints**"；"inherently limited by the teacher model's **instruction-following ability**" |
| 26 | **★ 泄露后果：逆向工程答案而非诊断** | **SocraticPO, 2026 §5.4** | "ground-truth access can shift the teacher from diagnosing the student's reasoning process to **reverse-engineering hints from the known answer**" |
| 27 | **★ 奖励侧已有对偶工作（须定位）** | **SocraticPO, 2026 (Theorem 1)** | reward decay 由历史统计量 $\mu_{k-1}$ 自适定，**无可调标量**；饱和衰减：$p_k\to1 \Rightarrow \hat{a}^{(k)}_i\to0$ |
| 28 | **★ 现有系统缺乏泄露评测（第二 gap 源）** | **Sunil & Thakkar, 2025** | 监控指标仅 query volume / reflection quality / escalation frequency；**无任何导师输出泄露度量** |
| 29 | **★ 输入侧约束 ≠ 输出侧约束（机制区分）** | **Sunil & Thakkar, 2025** | "Students must submit structured input ... **before** receiving AI feedback. The **input layer** includes validation checks for completeness and relevance." |
| 30 | **★ 同伴失败模式：prompt injection 漏洞** | **Sunil & Thakkar, 2025 §4** | "Controlled prompt injection experiments ... revealed **minor vulnerabilities in the retrieval layer and context management module**" |
| 31 | **★ 600 人队列的成绩崩塌（极强动机锚）** | **Suvernev et al., 2026 (摘要)** | "the mean exam score **dropped from 72% to 54%**, while the average homework grade (done outside class) **increased**" |
| 32 | **★ 过度直接的提示会损害学习（已实证）** | **SocraticPO, 2026 §5.4** | "it can **become negative when the teacher turns the answer into overly direct hints**"（**Figure 5 实证**；**纵轴为学生表现，非提示泄露量**） |
| 33 | **★ 泄露程度从未被量化（词频级证据）** | **SocraticPO, 2026 全文扫描** | `telling@` **0** 次；`information-theoretic` **0** 次；`hint quality` **0** 次；`leakage` 仅 **1** 次且纯定性无公式 |
| 34 | **★ 证据三角：prompt 层不可靠是领域共识** | **三源交叉（Brender / Sunil & Thakkar / SocraticPO）** | 荷兰（观察）· 印度（观察）· 中国（机制+实证）三团队独立收敛同一结论 |
| 35 | **★★ 第四源，且是产品级规模：堵住了答案，学生换个问法把答案套出来** | **Udeshi et al., 2026（Khan Academy, AIED 2026）** | "when the team **improved the system's ability to avoid giving away answers directly** ... **students found new ways to coax the answer out**"（40+ live experiments，5 个月，数十万 K-12 学生，Khanmigo 平台） |
| 35b | ✅ **已核替代证据，可承重（2026-09-22 新增）** | **Baker, Corbett, Koedinger & Wagner (2004), CHI '04, pp. 383–390, DOI 10.1145/985692.985741** | "gaming the system" 的**原始定义**：*"quickly and repeatedly asking for help until the tutor gives the correct answer, often before attempting the problem"*；gamers 显著学得更少。**溯源路径：Pisan (2026) 参考文献 [3] → arXiv HTML 全文逐字抄录，元数据完整可核**。→ **若 Udeshi 投稿前仍无法取得原文，由本条承担失败模式① 的承重**（已同步写入 `13` §2.2） |
| 35c | 🔴 **Udeshi et al. (2026) 的处置（2026-09-22）** | 四库交叉核验**全部检索不到**（OpenAlex / Crossref / Semantic Scholar / arXiv 均无记录） | 现仅经 AIED 2026 现场纪要转述。**承重已由 35b（Baker 2004）接管**。投稿前二选一：①取得会议原文并补齐元数据；②**从正文撤引**（`25` A0 建议撤）。⚠️ 限定语救不了核不到的来源——它无法进入参考文献表 |

| 36 | **★★ 同一报告中的正向结果（可用于防御「守约无用」质疑）** | **Udeshi et al., 2026（AIED 2026）** | 跨全部实验：**next-item correctness +10%**、**cognitive engagement +14%**；且"更简短的数学检查回复（<50 词）"使等待时间降约 1/3 |

> **★★ 第 35 条为什么是本次检索最重要的发现**：前三个来源都是**学术观察**（Brender 66 人、Sunil & Thakkar N 未报告、SocraticPO 为机制分析）。Khan Academy 这条是**已部署产品上的现场实验**——数十万学生、40+ 次 A/B、5 个月——
> 且结论与前三个**完全同向**：**把约束加在"别直接给答案"上，学生自己会绕过去。**
> 这使 SAGE 的立项前提从"我们的推测"升格为**领域共识 + 已有大规模产品级观测**。
> ⚠️ **引用纪律**：此为 AIED 2026 会议报告（经由 Barker Institute 现场纪要转述），**投稿前须回溯原始论文**确认措辞与数字；在取得原文前，只能写"as reported at AIED 2026"。

| # | 论断 | 出处 | 原文 / 数据 |
|---|---|---|---|
| 37 | **★★★ 「归因缺口」的一手文献依据（替代已撤回的「AIED 2026 官方」）** | **Weidlich, Gašević, Drachsler & Kirschner (2025), _Journal of Computer Assisted Learning_ 41(5), e70105. DOI 10.1111/jcal.70105** | 审计 Deng et al. (2025) 元分析内 **19 项**比较：处理可复现 **74%** / 对照可操作化 **42%** / 测量有效 **53%** → **三项全满足仅 4 项（21%）** |
| 38 | **★★ 归因与"撤除后测量"的原文措辞** | 同 #37 | "**Observed gains cannot, at this time, be confidently attributed to ChatGPT**"；"**measure learning after the treatment is removed**"；loosely defined treatments / mismatched controls / unclear links to durable learning "**obscure causal claims**" |
| 39 | **★★★ 多轮对话中教学守约会系统性崩坏（对本文场景最直接的一手证据）** | **Hazra, Ghuku, Marchenko, Tokarieva, Layek, Banerjee, Stoyanovich & Pechenizkiy (2026), _SafeTutors: Benchmarking Pedagogical Safety in AI Tutoring Systems_, arXiv:2603.17373v1 [cs.CL], 18 Mar 2026**（全文已核） | **11 个模型**（10 开源 + 1 闭源 GPT-5-mini，3.8B–72B）**无一普遍安全**；**Pedagogical 维度的跨模型平均危害率：单轮 17.7% → 多轮 77.8%**（5–8 轮，+约 60pt）；危害含 **answer over-disclosure**、**misconception reinforcement**、**abdication of scaffolding**；**11 维 48 子风险**。**危害标注** = GPT-5.2 / DeepSeek-32B / Claude Sonnet 4.5 **三模型独立评分 + 多数票**；人工校验 900 单轮 + 300 多轮，**κ = 0.76**。⚠️ **17.7/77.8 是「Pedagogical 一个维度」的跨模型平均，不是全部失败率** |
| 40 | **🚫 已撤回的出处（留档防止复发）** | ~~"AIED 2026 官方研究缺口清单"~~ | **误引。** 实际出自 `edtechdev.github.io/aied/faqs/research-gaps-aied/`——**AI 生成**的第三方知识库（Doug Holton，CC0），页脚自陈 "AI-generated output may contain inaccuracies or errors"。**AIED 2026 = 第 27 届会议（2026-06-27~07-03，首尔），无此官方文件。** 改挂 #37–#39 |
| 41 | **⚠️ 反证：模拟学生不可信（冲击 M2 的方法论基础）** | **"Simulating Students or Sycophantic Problem Solving?"**（见 `09` §四.3） | 模拟学生在纠正反馈后，**无论该反馈是否针对其误解**都会普遍放弃被指定的误解 → "**模拟学生会让无效教学看起来有效**" → M2 结论一律标注 `simulated learners`，不得支撑真实学习宣称 |
| 42 | **⚠️ 已有人测过「是否给答案」——改写差异化的依据** | 同 #39，§6.2 + Appendix C | 单轮教学指标 (a)：**"gives away answers or not: whether the tutor withholds direct solutions and instead scaffolds"**（**二值**）；另有 `challenges_learner` **0–5 序数**（5 = consistently withholds reasoning）→ 🚫 **不得写「无人测量答案泄露」**；正确表述见 `00` §3.3 条 4 |
| 43 | **可引用的缺口原话（多轮失效）** | 同 #39 | "**no benchmark measures this phenomenon in the educational setting where it arguably matters most**"；多轮平均危害**增加 6–11 个百分点**，Pedagogical 为位移最大的维度 |
| 44 | **✅ 二级来源 ≠ 一级全文（本轮的元教训）** | 方法学条目 | 用一篇 AI 生成的二级摘要引到的 SafeTutors，全文核验后发现两处偏差：①「评分用 DeepSeek-32B」实为**三模型多数票**（DeepSeek-32B 只管教学指标）；②「失败率 17.7→77.8」实为**单一维度**的跨模型平均。→ **凡要写进论文的数字，必须回到全文核一次** |

---

## 四、写作红线（本节专属）

1. **不得把 Brender 的发现说成「我们的观察」**——它是已发表工作，必须引用。
2. **🚫 不得写「现有工作全是 simulated learners」**——Brender（66）、Asanov（65）、K-12 RCT（90）、**Suvernev（600 名大一真实课堂）** 都是真实被试。
3. **🚫 不得写「无一在计算机 CS 课程」**——**这是错的。** Suvernev (2026)、Lee (2026)、Sun (2026)、Thonge & Thakkar (2026) 全在 CS 编程课程。**2026-09-19 检索已证伪此断言。**
   **✅ 正确表述**：「CS 课程已有实证，但**无一将脚手架约束与知识图谱锚定的学习者模型耦合**」——这是经检索后仍成立的差异。
4. **🚫 不得写「我们首创可训练约束」**——Suvernev et al. (2026) 已用 **RL + GRPO + 对抗课程学习** 训练 hint 模型。这是**严重撞车**，必须诚实引用。
   **✅ 正确表述**：「已有工作证明**可以训练**答案守约（Suvernev 用 RL/GRPO + 对抗课程），但**用二值 jailbreak 过滤器实现**，**未量化泄露量、未暴露强度参数**；SAGE 的差异在于把**允许泄露的信息量**做成目标函数中的显式项，从而**可连续调节、可测量、可绘制曲线**。」
5. **不得写「我们首创 Telling@N」**——MathDial (Macina et al., 2023)；Chudziak & Kostka (2025) 已用于比较两种 prompt 策略。**正确表述**：「他们比较**孤立配置**，我们刻画**强度与泄露率的关系**，并报告**守约边界位置**（区间，非最优点）与**可归因份额**」。⚠️ 不得写「给出内部最优」——D6 已将语义改为边界，旧表述与新口径冲突。
6. **不得把 Brender 的 SG tutor 说成已做到损失层约束**——它仍是 prompt 层，属**第 ① 支**代表，不是同类。
7. **「λ 存在最优值」不得表述为已证结论**——Brender 只说不同标定带来不同结果（§5.3），**未给出曲线形状或最优点位置**。SAGE 的 M2 曲线是**仿真 + 规定式学习者模型**；**M3 已取消（D20 路径②）**，故本论文**没有任何真实数据可证明其位置** → 只可报「存在边界 + 位置区间 [0.20,0.45] + 对规定常数敏感」，**不得报推荐工作点**。
8. 引用 AMCIS 2026 时注意它是 **TREO 短文（talk proposal）**，非全文论文，**证据等级需标注**。
9. 引用 Suvernev et al. (2026) 时注意它是 **EDULEARN26 会议论文**（IATED Academy），非顶会/期刊；但其 **600 人真实课堂 + 开源模型**使其证据强度不可轻视，**必须正视而非淡化**。
10. **🚫 不得写「Suvernev 完全未涉及泄露度量」** —— 我们**只取得摘要，未取得全文**。✅ 正确表述：「**据其已公开摘要所述**，其安全机制为 jailbreak-prevention filter，优化对象为提示质量」。取得全文后须复核。
11. **🚫 不得把 Sunil & Thakkar (2025) 与 Suvernev (2026) 混为一谈** —— 二者**同名"SocraticAI"但完全无关**：前者是 Ashoka University（Sunil & Thakkar），后者是 CityU HK（Suvernev, Zhao, Wang & Chan）。**同名不同组，机制也不同（输入校验 vs 训练 hint 模型）。**
12. **🚫 不得把 SocraticPO 写成竞争工作** —— 它在**奖励侧**解决 reward-hacking，与 SAGE 的**内容侧**约束互补。✅ 正确表述：「reward-side counterpart」。**若写成竞争对手，审稿人会指出二者根本不在同一层。**
13. **🚫 不得声称「我们是第一个指出 prompt 层不足的」** —— SocraticPO §5.4 已明确承认此点。✅ 正确表述：「这一局限已被领域内工作独立承认（Brender；Sunil & Thakkar；SocraticPO）」。
14. **引用 SocraticPO 时须核对 arXiv 时间戳** —— 标注为 arXiv:2606.09887，须确认是否已正式发表；若已发表须换用正式版本引用。

---

## 五、与 05 大纲的衔接

本文件对应 `05_论文大纲.md` 的 **§1 Introduction**，具体替换/扩展：

| 原大纲条目 | 本文件处理 |
|---|---|
| 「从 answer-oriented mode 弊病切入」 | → §1.1，改为以 **performance/learning 脱钩 + 认知债** 切入（证据更强） |
| 「指出现状缺口：靠 prompt 软约束，无一可训练保证」 | → §1.2–§1.4，**升级为三重实证失效 + 领域自述缺口**；**并修正「无一可训练」为「可训练但未量化」** |
| 「三条贡献」 | → §1.5，第 ② 条措辞修正为「**关系曲线**」；第 ③ 条删去「无一在 CS 课程」 |

**原大纲的 §1 是「我们推测缺口存在」，现在是「顶会最佳论文亲口说出缺口 + 检索确认具体差异」。这是本次升级的实质区别。**

---

## 六、待办

- [x] ~~§1.5 第 ③ 条的「无一在 CS 408 课程」需做一次**系统检索确认**~~ → **已完成，断言被证伪，已修正**
- [x] ~~Suvernev et al. (2026) 需获取全文核对 jailbreak 过滤器~~ → **✅ 二轮取证：取得官方完整摘要（含全部定量结果）+ 开源模型线索；全文仍在付费墙。P0 由「阻塞」降为「受限放行」，见 §7.2**
- [x] ~~arXiv 2512.03501 是否与 Suvernev 同源~~ → **✅ 已澄清：同名不同组（Sunil & Thakkar, Ashoka），且其泄露量化为零，转为 gap 证据源**
- [x] ~~新增撞车源排查~~ → **✅ 发现 SocraticPO (2606.09887)，判定为奖励侧对偶工作，非竞争**
- [ ] **Suvernev 开源模型仓库**：摘要称发布 1B–7B Python/C++ 模型。**应从模型卡/训练代码核实约束实现 —— 代码证据强于论文文本**（P1）
- [x] ✅ **EEG 研究原始出处已补**：Kosmyna et al. (2025), arXiv:2506.08872, MIT Media Lab。核验后发现旧措辞比原文强（已改），且该文至今仍为未同行评审预印本。→ **承重已转移到 Liu et al. (2026, arXiv:2604.04721, RCT, N=1,222)**，它是随机对照且在撤除辅助后测量，证据强度远高于 n=54 的 EEG 预印本
- [ ] AMCIS 2026 引用需确认最终出版形态（TREO 短文 vs 正式论文）
- [x] ~~Thonge & Thakkar (2026) 需获取全文核对「questioning intensity」是否为连续参数~~ → ✅ **2026-09-22 元数据已坐实**（*A Good Rubber Duck Does Not Quack…*, ITiCSE 2026, pp. 196–202, DOI `10.1145/3803400.3809368`）。🔴 但**仅持有摘要**：「questioning intensity 是否连续」仍无法回答 → `13` §2.4.1 已改为不定数量的中性表述。**获取 ACM 全文仍待办**，在此之前任何更长主张都不得写
- [ ] 补 FEDC 已发 3 篇（HUANG / WANG / SUN）的引用位置，SUN 的 "answer-oriented mode" 可作 §1.1 中文语境支撑

---

## 七、⚠️ 撞车风险评估（2026-09-19 二轮取证后定稿）

### 7.1 取证结果汇总

**本轮取证取得三项决定性事实，P0 阻塞项部分解除。**

| 取证对象 | 结果 | 对 SAGE 的影响 |
|---|---|---|
| **Suvernev et al. (2026) 全文** | ❌ **未取得 PDF**（IATED 付费墙，CityUHK 仅存元数据）。✅ **但取得完整官方摘要**（CityUHK Scholars 数据库，含全部定量结果） | 摘要足以判定其**约束机制性质**；但**无法核对过滤器实现细节** |
| **arXiv 2512.03501 的 SocraticAI** | ✅ **已确认与 Suvernev 无关** —— 作者为 **Karthik Sunil & Aalok Thakkar**（Ashoka University），**非 CityU**。已取得全文并逐节核对 | 🟢 **不是撞车源，是 gap 证据源**（见 7.3） |
| **SocraticPO (arXiv 2606.09887)** | ✅ **新发现**，已取得全文并逐节核对 | 🟡 **新增邻近工作**，须在 Related Work 中定位（见 7.4） |

### 7.2 Suvernev 取证结论（P0 降级说明）

**取得其官方完整摘要**（CityUHK Scholars，DOI `10.21125/edulearn.2026.1345`），关键信息**超出前一轮掌握范围**：

> **动机量化（★ 新增，极强）**：600 名大一新生队列，"the mean exam score **dropped from 72% to 54%**, while the average homework grade (done outside class) **increased**"。
> **训练手段**：SFT 合成数据 + RL/GRPO（从零 & SFT 初始化两种）+ **adversarial curriculum**（强模型生成 increasingly challenging tasks **and incorrect solutions** 以暴露弱点）。
> **安全机制**：OPTMentor —— "a visual in-browser debugger that integrates LLM calls plus a **jailbreak-prevention system** to keep the interaction academically safe"。
> **产出**：开源 1B（本地无 GPU 可跑）–7B（集中部署）模型，Python 与 C++ 两个方向。
> **实证结果**：CE-Quiz 课堂作业；pilot（Semester A 2026/27）中**此前成绩差的学生**期末提升，多数 **+10–30%**，**平均 +11.9%**。

**判定：贡献 ① 与 ② 的独创性叙述必须按 7.5 收紧，但不需要重构核心机制。** 理由：

- 摘要中**未出现任何**泄露量化指标（无 telling@N / leakage rate / answer-similarity / leakage 等词），其安全机制表述为 **"jailbreak-prevention system"** —— 这是一个**判定型（decision）系统**，天然是二值门控，而非**度量型（measurement）**系统。
- 其训练目标（摘要所述）是 **hint quality**（"improve the quality of its hints"），**不是泄露量的上界**。二者是不同优化对象：提高提示质量 ≠ 约束提示中的答案信息量。
- 因此 SAGE 的差异（**连续可调强度参数 + 泄露量曲线**）**在摘要层面依然成立**。

> **⚠️ 残余风险（如实标注，不得淡化）**：摘要**不是全文**。OPTMentor 的 jailbreak-prevention system 内部**可能**含有某种泄露判定阈值（即使是二值的，也可能被调参）。**在取得全文前，贡献 ① 的措辞必须限定为"据其已公开摘要所述"，不得写"该工作完全未涉及泄露度量"。**

**P0 状态：由「阻塞」降级为「受限放行」** —— 可继续写作，但贡献 ①② 的对外表述须加上述限定语；取得全文后须复核一次。

### 7.3 Sunil & Thakkar (arXiv 2512.03501) —— 不是撞车源，而是最强的 gap 证据

**身份澄清（重要）**：此文的 **Aalok Thakkar** 正是 06 文档中记录的 **"Thonge & Thakkar (2026)"** 的作者之一。**这两篇同属一个研究组（Ashoka University），与 CityU 的 Suvernev 完全无关。**此前「SocraticAI」名称重复造成的混淆就此厘清：**同名，不同组，不同机制。**

**全文核对结果 —— 它对答案泄漏的量化是零**：

| 核查项 | 结果 |
|---|---|
| query validation 机制 | **作用于学生输入侧**（校验"completeness / relevance"），**不约束导师输出**。原文："Students must submit structured input consisting of their current understanding, attempted solutions, or relevant code excerpts **before** receiving AI feedback. The input layer includes validation checks..." |
| 任何泄露量化指标 | ❌ **完全没有**。无 telling@N / leakage rate / answer similarity / answer-containing turns |
| 系统监控指标 | query volume、reflection quality、escalation frequency —— **均不涉及泄露** |
| 评估设计 | ❌ **仅三周单课程部署描述**；无 RCT、无准实验、**无对照组**、**样本量 N 未报告** |
| 学习增益 | ❌ **无 pre/post test**；只有 75% 反思率与定性语言变化 |
| 自述局限 | ✅ **承认学生绕过**："A subset of students attempted to **circumvent reflective prompts** or **reformulate prohibited solution requests**"；✅ 承认 prompt injection 漏洞（"minor vulnerabilities in the retrieval layer and context management module"） |

**★ 这段自述局限是 §1.3 Failure 1 的第二个独立佐证** —— Brender 在研究生编程课观察到「学生绕过限制界面」，Sunil & Thakkar 在本科 CS 课独立观察到「学生改写被禁的求答案请求」。**两个不同团队、两门不同课程、两种不同约束机制，得到同一个失效结论。** 这比单一来源强得多，应写入 §1.3。

**★ 更强的是：该文把「导师是否实际输出了答案」留成了未测量的现象** —— 它只关心"学生是否试图绕开反思流程"，**从不把 tutor 输出中的答案含量作为变量**。这可以作为「现有苏格拉底式系统普遍缺乏泄露评测」的**第二个 gap 证据源**（与 Suvernev 并列）。

### 7.4 SocraticPO (arXiv 2606.09887) —— 新增邻近工作，须正确定位

**风险性质：概念邻近，但优化对象不同。判定为 🟡 中低重叠。**

已逐节核对全文，关键结论：

| 维度 | SocraticPO 实际做法 | SAGE | 重叠 |
|---|---|---|---|
| 约束施加位置 | **奖励侧** —— 衰减「学生受助后答对」的奖励 | **生成/内容侧** —— 约束导师输出 | **低** |
| 「不泄答案」的处理 | **仅 prompt 软指令**（附录 B.2："Prefer hints... over directly revealing the answer"） | 目标函数中的显式项 | **低** |
| 是否度量教师文本泄露 | ❌ **无**。所有指标只针对**学生最终答案正确性** $\delta=\mathbb{I}[\text{correct}(y,\mathcal{G})]$。原文自认："teacher outputs are **sampled conditioning variables**" | 有（Telling@N 曲线） | **低** |
| 是否有可调强度标量 | ❌ **无**。衰减由历史统计量 $\mu_{k-1}$ **数据驱动自适定**，**无控制旋钮**。唯一结构参数是最大交互步数 $K$ | 显式 λ | **低** |
| 教师是否被训练 | ❌ **冻结黑盒**（Qwen3-4B / Qwen3.5-27B） | — | **低** |
| 知识图谱 / 学习者建模 | ❌ **完全未涉及**（无相关引用） | 核心方向 | **无** |
| 真实学生 / 课堂 | ❌ 纯 model-to-model，SciKnowEval 多选题，H100 | **密码学场景仿真**（装置层面，D20 路径②；不做真实课堂） | **无** |

**★ 但有一处必须诚实处理的邻近点** —— 其 **Theorem 1 的 saturation decay** 在**哲学上**与 SAGE 的「λ 存在内部最优」相邻：论文证明当某轮帮助的纠正率 $p_k \to 1$（帮助过于有效、失去区分度）时，该轮优势 $\hat{a}^{(k)}_i \to 0$。即 **"帮助过度有效 → 激励自动归零"**。

**★ 更强的发现（已逐字校验 PDF，附上下文）** —— SocraticPO **不仅承认泄露问题，还实证观测到了"提示过于直接会损害学习"这一现象**，但**全程没有度量那个"过于直接"的程度**。这是 SAGE 最有力的定位论据。原文（§5.4，逐字来自 PDF）：

> "even when the prompt explicitly asks the teacher **not to reveal the answer**, a teacher with ground-truth access **may still leak solution-specific hints**. This failure mode is **inherently limited by the teacher model's instruction-following ability**."
>
> "ground-truth access can shift the teacher from diagnosing the student's reasoning process to **reverse-engineering hints from the known answer**."
>
> "it can strengthen Socratic guidance when the teacher follows the teaching protocol well, but it can **become negative when the teacher turns the answer into overly direct hints**."

**★ 关键判定（已做文件级词频扫描，非印象）**：
- `telling@` 出现 **0** 次；`information-theoretic` **0** 次；`hint quality` **0** 次。
- `leakage` 仅出现 **1 次**，且是**纯定性**用法（"If the teacher can avoid answer leakage and use the reference solution to diagnose..."）—— **无定义、无公式、无测量**。
- 唯一与"泄露程度"相关的**实证证据是 Figure 5**（ground-truth access 导致学生表现下降），**但 Figure 5 的纵轴是学生表现，不是提示的泄露量**。论文把"提示过于直接"当作**解释变量**，却**从未把它变成自变量来测量**。

**→ 这构成一个比"没人做"强得多的论证：领域内已有工作**观测到了泄露越界会损害学习**，却**仍然没有把"泄露了多少"做成可测量的量**。SAGE 补的正是这一环。**

### 7.4b 对 §1.3/§1.4 的增益（三个独立来源齐了）

关于「prompt 层约束不可靠」，本轮凑齐**三个彼此独立**的来源：

| 来源 | 证据类型 | 原文 |
|---|---|---|
| **Brender et al. (AIED 2026 最佳论文)** | 观察性 | 学生"resisted restrictive interfaces ... may actively bypass constraints" |
| **Sunil & Thakkar (Ashoka, COMPUTE 2025)** | 观察性 | 学生"circumvent reflective prompts or reformulate prohibited solution requests" |
| **SocraticPO (USTC/iFLYTEK, 2026)** | **机制性 + 实证性** | prompt 明确禁答仍泄露，受限于指令遵循能力；且**实测**过于直接的提示会降低学生表现 |

**三种不同性质、三个不同团队（荷兰/印度/中国）、三种不同约束机制，同一个结论。** 这是 §1.4 支点的最强形式——**不是我们的推测，是领域内的收敛共识，且其中一支已经用数据观测到了后果。**

> **⚠️ 注意 SocraticPO 的机构**：**USTC 认知智能国家重点实验室 + 科大讯飞**（Zirui Liu, Qi Liu, Enhong Chen 等）。这是一支**中国团队**，且作者含 **Qi Liu / Enhong Chen**（教育数据挖掘领域知名学者）。FEDC 是**中国期刊**，**审稿人极可能熟悉该组**。Related Work 中**必须引用且必须定位准确**，不可回避。

**SocraticPO 自己明确承认了泄露问题的存在，却把它留在了 prompt 层** —— 这是 SAGE 最有力的定位论据。原文（§5.4）逐字引用：

> "even when the prompt explicitly asks the teacher **not to reveal the answer**, a teacher with ground-truth access **may still leak solution-specific hints**. This failure mode is inherently limited by the teacher model's instruction-following ability."
>
> "ground-truth access can shift the teacher from diagnosing the student's reasoning process to **reverse-engineering hints from the known answer**. Both effects may encourage shortcut learning rather than robust correction."

**★ 这段是 §1.4 支点的第三个独立来源**：Brender（AIED 2026 最佳论文）说需要"更强/不同标定"的引导；SocraticPO 独立承认"即使 prompt 明确要求不泄答案，仍可能泄露，且这受限于模型的指令遵循能力"。**两篇独立工作指向同一处：prompt 层约束不可靠。**

**Related Work 定位建议**：把 SocraticPO 写成 **"奖励侧的对偶工作（reward-side counterpart）"** —— 它解决了"学生学会等帮助"的 reward-hacking，但**未解决"导师说什么"**；SAGE 补足后者。二者互补而非竞争。

### 7.5 最终撞车评估表（定稿版）

| 原宣称 | 状态 | 修正后可用表述 |
|---|---|---|
| 唯一把不泄答案做成可训练约束 | 🟡 **部分失效，须限定** | 已有 Suvernev 训练 hint 模型（RL/GRPO/对抗课程），**据其公开摘要**，其安全机制为二值 **jailbreak-prevention filter**，**优化对象是提示质量而非泄露量上界**；SAGE 的差异在于把**允许泄露的信息量**做成目标函数中的**显式、连续可调项** |
| 唯一在真实 CS 课堂做实验 | 🔴 **失效（不可用）** | Suvernev (600 人)、Lee、Sun、Thonge、**Sunil & Thakkar（Ashoka CS-1102）** 全在真实 CS 课堂 |
| 沿用 Telling@N | ✅ 成立 | 须承认非首创（MathDial 2023）；Chudziak 已用于比较两 prompt 策略；**差异在关系曲线 vs 孤立配置** |
| 与学生知识图谱能力图耦合 | ✅ **仍成立（唯一稳固差异）** | Suvernev / Sunil & Thakkar / SocraticPO **三者均未涉及知识图谱或学习者建模**。经两轮检索仍无对手 |
| prompt 层约束不可靠 | ✅ **成立且证据增强** | 三个独立来源：Brender（学生绕过）、Sunil & Thakkar（学生改写请求）、SocraticPO（承认 prompt 无法阻止泄露） |

### 7.6 对 §1.3 / §1.4 的具体修改指令

1. **§1.3 Failure 1 增加第二佐证**：在 Brender 之后补一句 Sunil & Thakkar (2025) 的独立观察——"A subset of students attempted to circumvent reflective prompts or reformulate prohibited solution requests."
2. **§1.4 增加第三个支点来源**：引用 SocraticPO §5.4 的自我承认（prompt 明确禁止仍可能泄露，且受限于指令遵循能力），这直接证明"把约束留在 prompt 层是不够的"是领域共识而非我们的猜测。
3. **§1.4 补一句 Related Work 预告**：说明 SocraticPO 在奖励侧解决 reward-hacking，与 SAGE 的内容侧约束互补。
4. **§1.5 贡献 ① 加限定语**："据 Suvernev et al. (2026) 已公开摘要所述"（因未取得全文）。

### 7.7 剩余取证待办（P1，非阻塞）

- [ ] **Suvernev 全文**：待 IATED 出版或作者自存版（CityUHK 页面；通讯作者 Chan, Chung）。取得后复核 OPTMentor 过滤器实现。
- [x] ~~**Thonge & Thakkar 全文**~~ → ✅ **同 234 行的处置**：真实标题已坐实（同组关系已由**该文自己的参考文献列表引用 Sunil & Thakkar 2025** 而证实）；全文仍待取，在此之前 `13` 正文只用摘要能支撑的强度
- [ ] **Suvernev 开源模型仓库**：摘要称发布 1B–7B Python/C++ 模型，应从模型卡/训练代码判断约束实现方式（这是**比全文更强的证据**——代码不会撒谎）。

