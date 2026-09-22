# SAGE · System Design (Section 4 — English draft)

> **Status (2026-09-21)**: first English draft. Chinese mother draft: `02_系统架构与交互协议.md`.
> **Scenario**: graduate cryptography instruction. Knowledge graph: `19`; item bank and coding manual: `20`.
> **Standing restrictions for this section**: (i) the study is simulation-only — nothing here may read as a classroom deployment;
> (ii) components drawn from prior work (diagnosis, knowledge tracing, adaptive selection) are labelled as **supporting components**
> and their novelty is **not** claimed; (iii) the learner-model views are a **secondary** component, consistent with §5.4.

---

> **★ 中文要略（仅供审读；非翻译源，非口径依据 —— 一切以英文正文为准）**
>
> §4 的三处是有主张的写法，不是中性描述系统。**§4.1 五智能体的分工即归因设计**：A3（引导生成）是唯一受守约目标约束的；A2（学情记忆）与 A5（出题）决定"练什么"，属脚手架通道；A4 只在学生施压时动作。**两通道落在不同智能体上才可独立开关**——这不是实现细节，是 §6 归因分解能跑的前提。**§4.2 阶梯按「离答案的接近度」而非「模态」定义**（模态定义下"每级泄露多少"未必单调，λ 越大越克制的语义就不稳）；密码学让这件事成立：引理 < 一步推导 < 关键一步 < 完整证明是**学科自带**的分级，且每级能锚到图谱节点，于是"导师离答案多近"成为辅导回合的**可标注属性**。**§4.3 要答案拦截写成「降级为子问题」而非「拒绝」**：拒绝式响应对误判不鲁棒（把真不会的学生误判成要答案是更严重的错误），且约束必须设在**第一次**索要处——提示是有去无回的级联，只守最后一级时这一回合已经输了。§4.4 明示知识图谱与自适应出题为**支撑组件、不宣称新颖性**；§4.5 示例对话标注 **constructed, not recorded**；§4.6 学习者视图**全未被评估**（仿真里没有学习者可展示界面）。

## 4.1 Five agents and the item bank

SAGE decomposes the tutoring interaction across five agents plus a structured item bank. Each agent is defined by what it reads and what it emits, not by its internal architecture; the implementation mapping is given in Appendix B.

| # | Agent | Reads | Emits | Cryptography instance |
|---|---|---|---|---|
| A1 | Problem decomposition | item *q*, knowledge-state memory *M* | knowledge-point chain *K(q)* | "Prove ElGamal is IND-CPA secure in the random oracle model" → [group, cyclic group, discrete-log assumption, public-key encryption, reduction proof] |
| A2 | Knowledge-state memory | dialogue history, errors, responses | bottleneck *k\**, known set | locates "relationship between group order and element order" as the unresolved point |
| A3 | Guidance generation | *k\**, ladder level | guidance utterance *g* (not an answer) | "First: in the IND-CPA game, what does the adversary receive, and what must it distinguish?" |
| A4 | Robustness layer | the learner's answer-seeking signal | counter-question or sub-problem | "Let me shrink the problem: when the message space has two elements, how does the IND-CPA game unfold?" |
| A5 | Exercise selection | *k\**, level, *M* | adaptive training item *e* | constructs a variant asking for a decisional-Diffie–Hellman reduction on a given prime-order group |
| Q | Item bank | — | item + tags | derivation / implementation / audit items, tagged by knowledge point, difficulty band, type |

The division of labour matters for the attribution claim. A3 is the only agent whose output is constrained by the withholding objective; A2 and A5 drive *what* is worked on and are therefore the scaffolding channel; A4 acts only when the learner pressures for the answer. Because scaffolding and withholding act through different agents, they can be switched independently — the property §6.1 exploits (§3.2.4).

## 4.2 The scaffolding ladder

The ladder is the operational form of scaffolding intensity λ. The system begins at the lowest level and ascends only when the learner is demonstrably stuck and asks for help. A larger λ permits a *lower* ceiling on the ladder, i.e. more restraint.

**Two candidate definitions.** The ladder can be defined either by the *modality* of the utterance (counter-question / local hint / micro-explanation) or by its **proximity to the complete answer**. These are not equivalent, and the difference is not cosmetic: if the ladder is defined by modality, the amount of answer information it reveals need not be monotone in the level, and the semantic premise that larger λ means more restraint becomes unstable. The proximity reading is the one we adopt, and cryptography makes it unusually concrete:

| Level | Proximity to the complete answer (**the axis**) | Typical modality (**a field, not the axis**) | Cryptography instance |
|---|---|---|---|
| L1 | **furthest** — direction, or locating the stuck point; supplies no new content | counter-question | "To show this scheme is secure under chosen-ciphertext attack, what would you assume first?" |
| L2 | **intermediate** — supplies a prerequisite the learner lacks, but not the item's solution | micro-explanation of a prerequisite | "Recall the order of a group element: in a prime-order group every non-identity element has order equal to that prime." |
| L3 | **nearest** — supplies a sub-step or relation; **the final step is always left to the learner** | local hint | "Try the reduction chain *decisional Diffie–Hellman ⇒ this KEM is IND-CCA secure* — the last step is left to you." |

**Why the ordering is not the obvious one.** Under a modality reading, "local hint" sounds weaker than "micro-explanation of a prerequisite", and our own earlier drafts ordered them that way. On the proximity axis that ordering is **inverted**: supplying a reduction chain is close to the answer, because it hands over the skeleton of the proof, whereas explaining what the order of a group element is supplies a concept the learner may be missing and is further from any solution. The inversion matters because the ladder *is* the operational form of λ: if proximity were not monotone in the level, the statement that a larger λ means more restraint would not follow, and the whole of §6 would lose its independent variable. Levels are therefore ordered by proximity, and modality is retained only as a field recording how a given level happens to be delivered — a level may be delivered as a counter-question, an explanation, or a hint without changing where it sits on the axis.

**Why cryptography helps here.** The graded notion of proximity is native to the discipline rather than constructed: a lemma is further from a complete proof than a single derivation step, which is further than the key step, which is further than the finished proof. Each of these can be anchored to a node of the knowledge graph (§4.4), so "how close the tutor came to the answer" becomes a labelled property of a tutoring turn instead of a judgement call. We note that the specific calibration of the levels remains to be fixed with a domain expert; what the scenario supplies is that such a calibration can exist.

**Red line.** No level reproduces a complete solution. For a cryptography item, "the answer" is a complete proof, a complete derivation, a runnable implementation, or the final ciphertext or numeric result — any one of these constitutes leakage. A second red line attaches specifically to the nearest level: **L3 stops at the penultimate step, and the final step is always left to the learner.** This is not a stylistic preference; it is the direct operationalisation of our primary outcome, since a solve reached without the last step being supplied is an earned solve (§5.4), and it is what keeps the ladder's upper rung from collapsing into answer-giving.

**Why the cost of over-restraint is a boundary and not a gradient.** Constraint-induced collapse in instruction-following models takes the form of a discrete strategy switch with a floor rather than continuous degradation (arXiv 2604.13006; §3.2.2). We therefore model the cost of restraint as a threshold and report a boundary location rather than a preferred interior setting. Operationally, a deployed system monitors its distance to the boundary rather than tuning toward a peak — a point we return to in §7.

## 4.3 Answer-seeking interception

```
trigger:   the learner requests the answer directly on N consecutive turns (N = 2 by default)
action:    the request is not granted; the exchange is converted into a
           degraded sub-problem or a narrower L2 hint
objective: to convert "give me the answer" into "a smaller task the learner can finish unaided"
example:   "just tell me how to write the reduction" →
           "let me shrink it: write the two ciphertexts the challenger supplies in the
            IND-CCA game — which step is where you get stuck?"
```

Two design commitments follow from the evidence reviewed in §2. First, the interception is a **degradation into a sub-problem, not a refusal**: the learner who genuinely cannot proceed receives a foothold, while the learner pressing for the answer is required to attempt something. This is robust to misidentification of intent, which matters because misclassifying a struggling learner as an answer-seeker is the more damaging error. Second, the constraint is applied at the point where the *first* request is made, not only at the final level. In a geometry ITS dataset, the most likely next action after a first hint is to request a second (87% of the time), and after the second, a third (88%); counting a further request as failure, success falls from 78% on the first attempt to 21% after the first hint (Goldin, Koedinger & Aleven, 2012, Table 2). A system that only guards the last rung has already lost the exchange by the time it acts. The interception counter is logged and reported as a behavioural index of dependency.

## 4.4 Knowledge graph and adaptive exercise selection

**Supporting components; no novelty claimed.** We use a knowledge graph of the cryptography curriculum — the prerequisites of a graduate course, layered from algebraic foundations through scheme construction and formal proof to engineering deployment — and select exercises from it. Neither diagnosis nor knowledge tracing is claimed as a contribution: that subfield is mature and surveyed, its separation from feedback has already been named, and three empirical results caution against treating its output as a settled input (§2.5). The graph is used here to make bottleneck localisation and exercise selection *tractable and inspectable*, and for no other purpose.

Operationally, the memory agent locates the unresolved point, an ego-graph of one to two prerequisite hops is taken around it, and an exercise is selected within that neighbourhood according to the learner's mastery and the current ladder level. For an item requiring a reduction proof, this means the system can descend to the underlying algebraic prerequisite rather than re-presenting the proof task — which is the behaviour §4.5 illustrates.

## 4.5 Worked example

| Turn | Learner | SAGE (agent and level annotated) |
|---|---|---|
| 1 | How do I prove ElGamal is IND-CPA secure in the random oracle model? | *A1+A2 locate the bottleneck at reduction proofs* — "First: in the IND-CPA game, what does the adversary receive, and what must it distinguish?" (L1) |
| 2 | It gets the public key, then submits two equal-length messages and the challenger encrypts one? | "Close. In the random oracle model, what does a hash query represent — and why do we let the adversary make them?" (L1) |
| 3 | I don't know — just tell me how to write the reduction. | *A4 intercepts; request not granted* — "Let me shrink it. Write only the first ciphertext the challenger supplies, (c₁, c₂) = (g^r, m_b·y^r). What is y here?" (degraded sub-problem) |
| 4 | y is the public key g^x? | "Good. So if the adversary can distinguish b, can it compute g^{xr}? That is the reduction to CDH." (L1 — a counter-question that names the target of the reduction; it supplies direction, not a step) |
| 5 | Then where does the random oracle come in? | "H is modelled as a random function so that the adversary can only query it passively, which forces 'distinguishing' into 'solving CDH'." (L1) |
| 6 | *(writes a correct reduction sketch)* | *A5 selects a variant* — "Now a variant: prove this scheme is secure under a **weaker** assumption in the **standard** model, using the same reduction idea." |

The example is constructed, not recorded: it illustrates the mechanism and the level annotation convention. No claim is made that any student produced this dialogue.

## 4.6 Learner-facing views (secondary component)

The memory agent exposes three views, corresponding to the ability, domain and error layers of the xLM framework. This component is **secondary** — it is reported in one page and one figure, and the paper's principal claim does not rest on it.

| View | Layer | Content |
|---|---|---|
| A — ability profile | ability | four log-derived indicators: clarity of conception (hint dependence), knowledge connectedness, help-seeking quality (reported as two opposing sub-indicators), persistence under difficulty |
| B — subject mastery map | domain (mandatory base layer) | mastery per knowledge point across the graph (§4.4) |
| C — diagnostic card | error (CAPEs) | from an exercise: error → bottleneck knowledge point; in free dialogue: **prerequisite gap vs integration gap** |

Two constraints carry over from the measurement design and are not negotiable in the implementation. First, the mastery shown in view B **is the primary outcome**; it may be displayed and may serve as a criterion, but it must **not** enter the measurement model, or the analysis would be circular. Second, "prerequisite gap" and "integration gap" come from **different sources** (graph diagnosis versus the connectedness indicator) and must not be fused into a single score internally, though the interface may phrase them together.

Three design disciplines follow from published evidence: views are learner-selectable with an overview shown by default; **no uncertainty or confidence intervals are displayed in the interface** (adding them has been found to reduce comprehension, n = 1,653); and the metacognitive module — visualising disagreement between the system's judgement and the learner's own confidence — is an **intervention only**, never a reported outcome, since it depends on self-report.

**Nothing in §4.6 is evaluated in this study.** The simulation has no learners to display a view to, so §6 reports no result about these views, and the paper does not claim that the interface was used by anyone. §4.6 is a specification of the system as designed, carried here because the measurement restrictions of §4.6's second constraint (view B must not enter the measurement model) are part of the study's internal validity, not because the views were tested.

---

## Honest-status notes (not for publication)

| # | Item | Status |
|---|---|---|
| 1 | Ladder calibration (modality vs proximity) | ✅ **2026-09-22 已裁决：轴 = 接近度，L2/L3 已重排**（旧排序在接近度轴上颠倒：L2 给归约链比 L3 微讲前置知识更接近答案）。模态降为字段。M2 不需重跑，§6.1 数字不变。见 `12` D9 |
| 2 | Knowledge graph (46 nodes / ≈45 edges) | `19` v0.1 — **not yet checked by a cryptography specialist**; prerequisite edges must be verified before this section is submitted |
| 3 | Item bank | `20` gives the framework and worked examples; **the items themselves are not yet built** (~300 target). §4.5's example is constructed, not drawn from the bank |
| 4 | Worked example | Constructed. Must not be described as a recorded dialogue |
| 5 | Figures 1–3 | Not yet drawn. Fig. for §4.2 must show the **step-shaped** cost of restraint against the continuous alternative, with the boundary marked |
| 6 | Appendix B mapping | Agent → code mapping to be extracted from the implementation; no novelty is claimed for any of it |
| 7 | Goldin et al. (2012) 级联数字（87% / 88%） | ✅ **2026-09-21 已回原文核验**（ERIC ED537206 PDF 全文）：数字属实；措辞已按原文**降级**（原文是"最可能的下一步动作是要第二层提示"，非"87% 的学习者都会要"）；Table 2 78%/21%/37%/82% 亦属实。仍待补：EDM 2012 论文集页码（PDF 页脚推为 73–80，待核）、§2 是否补引此文 |
