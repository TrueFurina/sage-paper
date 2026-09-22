# SAGE · Theoretical Framework (Section 3 — English draft)

> 用途：论文 Section 3「Theoretical Framework」的英文初稿骨架。所有 RL 黑话已按口径翻译为教育学语言；原始技术名（MIR3/WALL 等）仅在括号内作技术注记，投稿时可整体移入 Appendix。
> 公式用 LaTeX 内联/块，正文用教育学叙事。

---

> **★ 中文要略（仅供审读；非翻译源，非口径依据 —— 一切以英文正文为准）**
>
> §3 是理论框架，与场景无关。**§3.1–3.2**：把导师建模为脚手架策略 π(g | s, K(q))，把"不许泄露答案"写成目标函数里的**信息瓶颈项** λ·Î(s;a)，λ 即**脚手架强度**（单一可解释旋钮）。**§3.2 的关键不是用信息瓶颈，而是承认它不是测量工具**：在 M2 中该估计器作为测量是退化的（p_ans 是 em 的确定性单调函数 → ρ² 按构造 ≈1，实测 0.99988–0.99999，估计值全程钉在裁剪上限 3.0，泄露近乎必然与几乎为零时返回同一个值）。所以① **撤回"瓶颈界定了泄露上界"这一宣称**；② 仿真里的泄露量是**规定模型的性质，不是独立测量**；③ 该独立性**不会**由课堂研究补上（M3 已取消）→ 列为 limitation。
> **命题 1（边界，不是平滑最优）**：约束的代价是**阈值**而非梯度。这是对已发表实证的**功能性形式采纳**（arXiv 2604.13006：词汇约束损失 14–48% 的理解完整性，且表现为**带触底的离散策略切换**——禁逗号 −27.0% 与禁逗号加冒号 −29.8% 几乎无差别；机制是**规划失败而非能力上限**，两遍生成可恢复 59–96%，分歧在头 1–3 个 token 就可见）。因此 λ\* 的语义是**守约边界的下沿**，不是"最优强度"；操作含义是**监测离崖的距离**，而不是调向一个无法可靠定位的峰。
> 🚫 附段已于 2026-09-21 重写：原含三处 "the first" 首创宣称与"在真实课堂验证"，属虚假宣称，已全部移除，改为只宣称三条**可测量性**性质，并明示"可训练约束不是我们首创"（Suvernev 已有）。

## 3.1 From Answer-Oriented to Guidance-Oriented Tutoring

Let $s \in \mathcal{S}$ denote the (partially observable) knowledge state of a learner, and let $q$ denote a question that can be decomposed into a chain of knowledge points $K(q) = \{k_1, \dots, k_m\}$, where the edges among $k_i$ encode prerequisite relations. A conventional LLM tutor directly emits a complete answer $a$. Under such a regime, the mutual information $I(s; a)$ between the learner's state and the revealed answer is high: the learner's uncertainty is resolved *for* them, which short-circuits the productive struggle that underpins deep understanding (Kapur, 2008) and induces answer dependency.

We instead require a **guidance-oriented** tutor that emits a guidance utterance $g$ — a hint, a counter-question, or a sub-goal — while withholding $a$. The central design challenge is thus: *how to guarantee, in a trainable rather than ad hoc manner, that $g$ does not collapse into $a$?* Prior Socratic tutors enforce this via prompts or hard-coded validators (e.g., "do not reveal the answer"), which is a **soft constraint**: it is checked after generation and can be trivially circumvented. SAGE replaces this with an information-theoretic **hard constraint** embedded in the training objective.

## 3.2 The Answer-Leakage Gate (Information Bottleneck as a Scaffolding Control)

We formalize the tutor's behavior as a scaffolding policy $\pi(g \mid s, K(q))$. To prevent answer leakage, we impose an information bottleneck on the pathway from the learner state to the answer:

$$
\min_{\pi}\;\; \mathcal{L}_{\text{coop}} \;+\; \lambda \cdot \hat{I}(s; a),
$$

where $\mathcal{L}_{\text{coop}}$ is the cooperative learning-gain objective (the tutor should *help*, not merely withhold), $\hat{I}(s; a)$ is a variational estimate of the mutual information between learner state and the revealed answer, and $\lambda$ is the **scaffolding intensity** — the single tunable knob that trades off guidance utility against answer leakage.

The information-bottleneck view is what makes SAGE qualitatively different from prompt-based tutors: instead of *post-hoc* checking that the answer was not leaked, the objective *structurally* discourages the policy from routing answer-level information through its output, in the same way a bottleneck representation discards input detail beyond what the task requires (Tishby et al., 2000; Alemi et al., 2017).

> **★ Terminology note: $\hat{I}(s;a)$ is the *training* objective, not the *measurement* instrument (2026-09-20).** The penalty $\lambda \cdot \hat{I}(s;a)$ shapes the policy during training. It is **not** a measure of how much answer information a dialogue actually leaked, and the paper must not present it as one. In the M2 simulation the estimator implemented for $\hat{I}$ is degenerate as a measurement: because the modelled emit-probability is a deterministic monotone function of the learner's effective mastery, its squared correlation is ≈ 1 by construction (measured 0.99988–0.99999 across the whole $\lambda$ range), so the estimate pins to its clip ceiling (3.0) at every $\lambda$ — including $\lambda = 0.8$, where the empirical leak rate has fallen to 0.0003. An estimator that returns the same value when leaking is near-certain and when it is absent is measuring its own functional form.
>
> **Consequence for the paper.** Leakage is reported with the **empirical** measures only: answer-leakage rate (ALR) and *Telling@N*. Any claim of the form "the bottleneck bounds answer leakage" requires a measurement independent of the quantity being penalised, and in M2 that independence is absent.
>
> **★ 2026-09-21 update — this independence will not be supplied by a classroom study.** The study is now **simulation-only** (no classroom data; D20 path ②, see `09` §十三). The human-coded ALR that a classroom extension would have provided is therefore **not available**, and can no longer be relied on to close this gap. Two consequences follow, and both must be respected in §§5–8:
> 1. **We withhold the bounding claim.** Any statement that the bottleneck *bounds* answer leakage is not made, in the simulation or elsewhere. The objective penalises a quantity, and the penalised quantity is not an independent measurement of leakage.
> 2. **The simulation's leakage figures are properties of the stipulated model, not independent evidence.** ALR and *Telling@N* are computed within the simulation from the modelled emission probability; they are not an external estimate. Reported leakage values are therefore labelled as simulated throughout.
>
> This is stated as a **limitation of the present work** rather than resolved by it, and is carried in `14` §8.2. A real-classroom extension that would supply an independent ALR is listed as future work, not as a pending result.

**Proposition 1 (A withholding boundary, not a smooth optimum).** *The helpfulness a scaffold actually delivers to the learner is approximately intact up to a collapse threshold $\lambda_c$ and substantially degraded beyond it. Consequently the mapping $\lambda \mapsto$ earned-solve rate rises as the constraint suppresses answer leakage, then falls as the tutor's own output collapses — but the maximum is **not** an "optimal intensity" in the sense of a smooth trade-off. It is the **lower edge of a boundary**: the last constraint level at which the tutor can still teach.*

Two regimes therefore bound the useful range. For $\lambda$ too small, the policy leaks answers, so solves are bought rather than earned (leakage high, earned-solve rate low). For $\lambda$ beyond $\lambda_c$, the policy is over-constrained and guidance becomes vacuous: the learner is "locked out," and both earned-solve rate and cooperative utility degrade.

> **Why the functional form is a boundary and not a gradient.** The form is adopted from an adjacent literature rather than invented, and **the adoption is an analogy, not evidence from our setting** — we say so plainly, because the source studies a different phenomenon. Work on constraint-induced collapse (arXiv 2604.13006; seven instruction-tuned models across five families, 7B–70B) finds that lexical constraints cost 14–48% of response comprehensiveness and that the cost takes the form of a **discrete strategy switch rather than continuous degradation**:
>
> *"Compositional constraints show a collapse floor: banning commas and colons together (−29.8%) produces only marginally worse results than banning commas alone (−27.0%), suggesting a discrete strategy switch rather than continuous degradation."*
>
> The mechanism is a **planning failure, not a capability limit**: two-pass generation (unconstrained draft, then constrained rewrite) recovers 59–96% of length, and the divergence between constrained and unconstrained generation is already visible in the first 1–3 tokens. The model does not gradually become less able to teach; it switches templates, and the switch has a location. Proposition 1 is therefore stated over the **location of that switch**.
>
> **What this source does and does not establish.** It establishes the *shape*: under an output constraint, an instruction-tuned model's loss is not gradual in the strength of the constraint — it saturates at a floor, because the model switches templates rather than degrading smoothly. That is what we adopt. It does not establish anything about our setting. The paper concerns lexical and formatting constraints on general helpfulness, and it contains no measure of answer leakage, no tutoring scenario, no notion of scaffolding intensity, and no learner of any kind; a full-text search finds none of those terms. The analogy is substantive rather than cosmetic — a tutor under a withholding constraint is also a model producing output under a constraint, and we have no positive reason to expect the shape to be smooth in our case — but it remains an analogy, and it is precisely why the three constants governing this shape are stipulated rather than measured (§8.1). §3.2.2 should not be read as resting on an empirical finding about tutoring, because there is no such finding to rest on.
>
> **Operational consequence.** A deployed system should not tune toward a peak it cannot reliably locate. It should monitor its **distance to the boundary**. This is the practically useful form of the "differently calibrated" guidance the field has called for (Brender et al., 2026, §5.1).

> **Empirical anchor.** This proposition is also supported by our team's reproduction of the mutual-information-regularization framework: with the regularization weight set at the repository-default $0.1$ (above the collapse threshold), the learned policy collapsed under evaluation, whereas the paper-recommended $5\times10^{-4}$ restored both robustness and cooperative performance. A scaffolding intensity that is too strong locks the learner out of the problem; one that is too weak leaks the answer.

> **Simulation status (M2, threshold form, 40 seeds, 2026-09-20).** Under the stipulated learner model of `m2_lambda_sweep.py` (θ = 0.3578, 240 learners, 25 problems per learner), the boundary is located at $\lambda^\* \approx 0.30$, where the earned-solve rate reaches **0.5659**. The unconstrained tutor ($\lambda = 0$) gives **0.1279**, so the rising side is **+0.4380**; at $\lambda = 0.8$ the rate has fallen to **0.2651**, giving a falling side of **+0.3008**. Both branches therefore carry large, confidence-separated effects.
>
> **The collapse floor is visible in the data, not asserted.** Past the boundary the earned-solve rate does not continue to decay — it flattens:
>
> | $\lambda$ | 0.50 | 0.60 | 0.70 | 0.80 |
> |---|---|---|---|---|
> | earned-solve rate | 0.3117 | 0.2705 | **0.2642** | **0.2651** |
> | 95% CI | [0.310, 0.314] | [0.269, 0.272] | [0.263, 0.266] | [0.263, 0.267] |
>
> The last two intervals overlap and the final value ticks *up*, so the curve does not merely bend — it **saturates at a floor**, which is the signature the literature predicts for a discrete strategy switch rather than a continuous penalty. Concretely: beyond the boundary, tightening the constraint further buys nothing, and the learner is simply locked out.
>
> Finally, an **attribution control** — the identical sweep with scaffolding disabled — shows that **86%** of the rising-side improvement is attributable to scaffolding itself rather than to the suppression of answer leakage, **under the stipulation that a revealed answer confers almost no durable mastery** (`leak_durable` = 0.012; see §6.3.1 for the sensitivity of this figure to that stipulation). Without this control the curve cannot be credited to the mechanism it names.

>
> **Three mandatory caveats.** (i) This is a **simulated-learner** result and is illustrative only. **No classroom study is run in this paper** (D20 path ②), so there is no M3 to supply real-student claims: every claim about learners is deferred to future work (§8.7). (ii) The literature supplies the *form* of the constraint's cost (a step, with a floor) but **not the magnitude of any of its three constants**; the source studies measure general response comprehensiveness under lexical bans, not pedagogical quality under answer-withholding constraints. We therefore swept all three constants (`collapse_threshold` ∈ [0.20, 0.60], `delivery_damping` ∈ [0.25, 1.25], `collapse_sharpness` ∈ [0.02, 0.15]) and report what does and does not move. **The boundary's existence is retained in every one of the 15 non-degenerate settings, and the attributable share stays in 76–88% — exactly 86% across the whole depth sweep.** The **location** moves over **$\lambda^\* \in [0.20, 0.45]$ and is therefore reported as an interval, not a point**. Two further results bear on how the location should be read. First, when the grid is solved so that the *delivered* fraction is held constant, the depth sweep's spread collapses to **zero**, and the optimum sits at the **same delivered fraction (0.9431) regardless of collapse depth** — that is, $\lambda^\*$ is where delivery reaches roughly 94% of the scaffold's potential, and depth only changes which $\lambda$ that is; the covariate is delivery, not $\lambda$. Second, the threshold sweep accounts for most of the remaining movement, about 40% of which disappears once the grid is shifted into distance-to-boundary units. (iii) A control mutant in which leaked answers are made genuinely instructive (`leak_durable = 0.50`) drives the scaffolding-attributable share below the 50% bar and the diagnostic rejects. The response is smooth and monotone — the share falls from 86% at the baseline to 28% at that mutant, crossing the bar between `leak_durable` = 0.20 and 0.22 — so the 50% criterion sits on a measured curve rather than on a convenient number. This is the sharpest single argument for the paper's central claim: **without measuring leakage, one cannot tell whether a tutoring improvement came from better guidance or merely from less leaking.**

## 3.3 Answer-Seeking Robustness (Adversarial Pressure on Guidance)

Learners, when frustrated, escalate toward "just give me the answer." In a multi-agent tutor, this pressure can cascade: one agent yields a partial hint, the next yields more, and the pipeline eventually leaks the full answer — an analogue of the wolf-pack attack, which targets one agent together with the teammates that move to assist it and thereby disrupts cooperation rather than merely degrading a single agent (Lee, Hwang, Jo and Han, 2025). We therefore treat answer-seeking as an adversarial perturbation and require the scaffolding policy to be **robust**: it must maintain guidance (not capitulate) under repeated answer-seeking pressure.

Formally, we augment the objective with a worst-case term over an answer-seeking adversary $\pi_{\text{ask}}$ that perturbs the interaction to extract the answer:

$$
\min_{\pi} \max_{\pi_{\text{ask}}} \;\; \mathcal{L}_{\text{coop}}(\pi) \;+\; \lambda\, \hat{I}(s;a \mid \pi, \pi_{\text{ask}}).
$$

> **Empirical anchor.** Our reproduction of the adversarial-robustness framework shows that, across three backbones, the undefended policy's win rate collapses to ~39.8% under attack, while robustness training holds it at 86%–100%. Translated to education: without the robustness term, a tutor capitulates to answer-seeking; with it, the tutor sustains guidance even under sustained pressure. (This translation must be re-measured in the education setting, see §5/§Limitations.)

## 3.4 Knowledge-State Graph Memory (Locating the Stuck Point)

Effective guidance requires knowing *where* the learner is stuck, not merely the surface question. We model the learner's interaction history, errors, and mastered knowledge points as a **cue–tag–content** memory graph (Ji, Li and Hooi, 2026), and — instead of one-shot similarity retrieval — perform **active reconstruction**: the tutor iteratively refines which knowledge point is the true bottleneck, guided by accumulated evidence across turns. This yields a sparse, targeted scaffolding decision ("which prerequisite to revisit") rather than a diffuse re-explanation of everything.

## 3.5 Ego-Graph Knowledge Decomposition (Choosing the Next Step)

Decomposing a question into knowledge points and choosing the *next* scaffold or exercise is a graph-selection problem. Let $G = (V, E)$ be the knowledge-point graph ($V$ = knowledge points, $E$ = prerequisite/association edges). For a learner at state $s$, we consider an **ego-graph** — the local subgraph of knowledge points relevant to $q$ and $s$ — and infer a sparse, context-aware **scaffolding focus mask** over it via Bayesian variational inference (Duan, Lu and Xuan, 2025). The variational distribution is trained end-to-end with the scaffolding policy through an evidence-lower-bound objective, so that the system *jointly* learns (i) the knowledge-point decomposition and (ii) the guidance policy. Sparsity keeps scaffolding focused; context-awareness lets it adapt as the learner's state evolves.

## 3.6 Integrated Objective

Combining the above, SAGE optimizes:

$$
\mathcal{L}_{\text{SAGE}} = \underbrace{\mathcal{L}_{\text{coop}}}_{\text{learning gain}} \;+\; \lambda \cdot \underbrace{\hat{I}(s; a)}_{\text{answer leakage}} \;+\; \underbrace{\mathcal{R}_{\text{robust}}}_{\text{anti-dependency}} \;+\; \underbrace{\mathcal{L}_{\text{ELBO}}}_{\text{ego-graph decomposition}}
$$

with four pedagogical meanings: help the learner (**coop**), withhold the answer (**leakage gate**, $\lambda$ = scaffolding intensity), resist answer-seeking (**robust**), and target the right knowledge point (**ego-graph**). Each term has a measurable operationalization (learning gain, answer-leakage rate, dependency behavior, and knowledge-point hit rate), which we report in §Method/§Results.

---

### 附：本框架与已发工作的关系（可写入 related work 首段）

> **⚠️ 2026-09-21 重写**：原段含三处"the first"首创宣称 + 「validate it in a real classroom」，与 D20 路径②（全模拟、无课堂）**冲突且属虚假宣称**，已全部移除。

Existing Socratic tutors (OpenAI study mode; Socratic AI; Chudziak & Kostka; IntelliCode) constrain answer-giving through prompts, role instructions, or post-hoc validators — a **soft, unguaranteed** mechanism, and one that learners have been observed routing around (§2.3). Training-layer systems have since shown that withholding can be *trained*: Suvernev et al. (2026) train hint models with supervised fine-tuning, reinforcement learning with GRPO and an adversarial curriculum, so **a trainable withholding constraint is not claimed as novel here**.

What SAGE adds is measurability rather than mechanism. Three properties are claimed, and none of them is primacy: (i) the constraint enters the objective as an explicit scalar — scaffolding intensity λ — so the amount of permitted answer information is a quantity rather than a gate that is open or shut; the graded form itself is not the novelty, since a graded leakage penalty swept along a Pareto frontier already exists (§2.4.2); (ii) that quantity is reported against an observed leakage rate **together with** an outcome measured after the tutor is withdrawn, and the resulting gain is decomposed into the part produced by guidance and the part produced by leaking less (§3.2.4, §6.1.3) — reporting leakage beside an outcome, or tracing a trade-off, has been done; attributing the gain has not (§2.4.3); and (iii) the scaffolding and withholding channels are carried by separate components and can be switched independently, which is what makes (ii) possible. The *outcome form* is not ours to introduce either: Puech et al.'s (2025) PF Score already declines to credit progress the tutor supplied, though it is computed from the conversation with the tutor present (§2.3.1). **All three are validated in simulation under a stipulated learner model (D20 path ②); no classroom validation is claimed or implied.**
