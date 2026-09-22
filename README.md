# SAGE 论文项目 — 目录索引

> 目标期刊：*Frontiers of Education in China*（FEDC）｜主题：反答案依赖的引导式多智能体教学系统（研究生层次密码学）
> 项目根目录：`E:\Program\MARL\SAGE`
> **题名（★ 2026-09-21 定稿，用户已批准）**：*When Does Guidance Still Help? Separating Scaffolding Effects from Answer-Leakage Effects in Graduate Cryptography Instruction — A Simulation Study*
> （场景于 2026-09-21 由 408 改为研究生密码学；研究形态为**全模拟**，故题名末尾明示 "A Simulation Study"）
> **决策点**：D1=反答案依赖主轴｜D2=完全模拟（无真实实证；方法论论文，D20 路径②）｜D3=密码学（研究生层次）｜D4=SAGE｜D5=重瞄｜D6=A9 改阈值模型｜D7=诊断/KT 降为次要｜D8=题名定稿（详见 `09`；场景迁移裁决见 `12` D21–D23 / `09` §十三 / `18`）

## 目录结构

```
SAGE/
├── *.md              编号文档（项目主干：正文初稿 / 素材 / 内部记录）
├── *.py              脚本（PDF 管线 / 实验 / 门禁 / 自检）
├── pdf/              渲染产物（.pdf + .html sidecar，由 md2pdf 生成）★ 可再生，未入 git
├── data/             实验数据（csv/json，由实验脚本写入）—— 见 data/README.md
├── audit/            数字可追溯性审计（脚本 + 声明清单 + 回溯报告）—— 见 audit/README.md
├── logs/             运行日志与实验证据（数字出处的原始记录；渲染日志亦在此）
├── figs/             手工可视化 html（早期图）
├── refs/ _refs/      参考文献 PDF ★ 外部来源，未入 git
├── 核心论文（参考）/   中文教育 AI 文献库 ★ 外部来源，未入 git
└── .git/             版本控制（2026-09-22 建立）
```

## 版本控制（2026-09-22 建立）

- 分支 `main`，**基线提交 `d47dbb2`**（全量初始快照，含当时尚未清理的临时脚本）。
- 未入 git 的仅上述 ★ 三类：可由 `md2pdf.py` 从 `.md` 再生的渲染件，以及可再次获取的外部文献 PDF（约 215 MB）。
- `.gitattributes` 设 `* -text`：**关闭行尾转换**。本工作区曾因 CRLF/LF 差异把"文件被改坏"误判过一次。
- 提交身份为本地中性值 `SAGE Author <sage-author@localhost>`，**不继承本机全局身份**——本文为双盲投稿，避免将来公开代码产物时泄露作者。
- 历史教训：`13_Section2_Literature_Review_en.md` 曾在无版本控制时被并行写操作截断为 0 字节，只能靠渲染件 HTML 反解。方法已固化为 `doc-truncation-recovery` 技能。

## 文档（★ 先看「角色」列：只有 2 个是论文正文）

| 文件 | 角色 | 内容 | 状态 |
|---|---|---|---|
| `07_Introduction动机链_原文证据锚定.md` | **✅ 论文正文初稿（Section 1）** | Introduction 英文初稿 + 每句论断的原文出处锚定表 | ✅ |
| `01_theoretical_framework_en.md` | **✅ 论文正文初稿（Section 3）** | 理论框架英文初稿（信息瓶颈 / 对抗鲁棒 / 图记忆 / 自我图；Proposition 1 已按**边界**语义改写） | ✅ |
| `05_论文大纲.md` | **骨架（非正文）** | 论文结构与写作纪律（9 节 + Appendix） | ✅ |
| `11_论文成稿进度地图.md` | **进度地图** | 逐节对齐「应有 vs 现有」，**回答「现在离可投还差什么」** | ✅ |
| `27_投稿前检查清单_双盲.md` | **投稿门禁** | 双盲检查：稿件 vs 内部记录的边界、投稿前必做项、可复跑的身份扫描 | ✅（2026-09-22 新建） |
| `20_密码学题库与测量.md` | **素材**（Section 5） | 密码学题库建设 + 自适应出题 + Telling@N 编码手册 | ✅（新建，替代已归档的 `04`） |
| `02_系统架构与交互协议.md` | **素材**（Section 4） | 五智能体 + 三级脚手架 + 要答案拦截 + 伪代码 + 密码学示例对话 | ✅ |
| `19_密码学知识图谱骨架.md` | **素材**（Section 4 / Appendix C） | 密码学知识点层级（L0–L3）+ 先修硬边 | ✅（替代已归档的 `03`） |
| `06_苏格拉底引导代表作精读与缺口分析.md` | **素材**（Section 2） | 代表作全文精读 + **缺口清单 G1–G12** | ✅ |
| `08_M2实验审计记录.md` | **素材**（Section 6 数据源） | M2 实验审计：缺陷记录 / 变异检验 / M3 重标定 / A9 残余风险 | ✅ |
| `00_定位与口径_术语翻译表.md` | **内部规范** | 定位 + 术语对照 + 撞车检查 + 测量口径 | ✅ |
| `09_方向决策备忘.md` | **内部记录** | 换向提案取证（为何不换）+ 重瞄方案 + A9 敏感性 + 缺陷清单 | ✅ |
| `10_汇报_选题过程_微信版.md` | **汇报稿** | 对导师的口头汇报（纯文字，可直接发微信） | ✅ |
| `FEDC投稿_引导式多智能体_深度研究报告.md` | **立项调研** | 期刊适配 + 技术映射 + 准实验设计 + 风险/里程碑 | ✅ |

## 脚本

| 脚本 | 用途 | 提交前必跑 |
|---|---|---|
| `m2_lambda_sweep.py` | M2 主实验（λ−泄露率关系 / 守约边界 / 归因对照）+ `--selftest` 变异检验 | ✅ 须 13/13 |
| `_audit_dead_params.py` | 死参数审计（每个字段都必须被计算读取，且变异后数值须变） | ✅ 须 17/17 live |
| `_a9_sensitivity.py` | A9 三常数敏感性（各配等价性检验） | 建议 |
| `_df_sensitivity.py` | `durable_factor`（A3）敏感性 | 建议 |
| `_check_threshold_mutants.py` | 阈值机制快速变异检查（~3 分钟，7 项） | 建议 |
| `md2pdf.py` / `_fontsub.py` | Markdown→PDF 管线（CJK 子集化 + 前置/后置双重守卫） | — |
| `_pdfverify.py` / `_pdf_hygiene.py` | 交付门禁：内容校验（含**覆盖率守卫**）/ 回退字体与体积 | ✅ 须 14/14 |
| `_munge_subset_guard.py` / `_munge_pdf_hygiene.py` | 上面两个守卫的**变异验证**（证明守卫真会 FAIL） | 建议 |

## 参考文献（`refs/`）

| 文件 | 说明 |
|---|---|
| `Brender2026_..._AIED_bestpaper.pdf` | **AIED 2026 最佳论文**：真实准实验；自述「需更强/不同标定的引导」← **Introduction 收束句来源** |
| `Chudziak_Kostka_AIED2025_...pdf` | **撞车最狠**：已用 Telling@N；审稿人指其缺真实学生评估 |
| `SocraticPO_arXiv2606.09887.pdf` | **奖励侧对偶工作**；§5.4 自认 prompt 禁答仍会泄露 |
| `SocraticAI_SunilThakkar_COMPUTE2025.pdf` | **同名不同组**（Ashoka）：输入侧校验，**泄露量化为零** → 最强 gap 证据源 |
| `SocraticLM_NeurIPS2024.pdf`（+ 仅译文） | ① 支代表作 |
| `K12_Socratic_AI_RCT_2026.pdf` | 90 名十年级 RCT：**元认知自我调节不显著** |
| `Asanov_Degen2025_...pdf` | 65 名师范生 RCT |
| `GAI_Socratic_JCAL2026_quasiexperimental.pdf` | CS 编程课准实验（**已证伪「无一在 CS 课程」断言**） |
| `SocraticLLM_DiscernMinds_arXiv2508.06583.pdf` | 相关邻近工作 |
| `AI赋能基础教育教师教学技能培训智能体设计与开发_熊晓莉(1).pdf` | 中文文献；引用须说明主体差异（其服务**教师**，SAGE 服务**学生**） |

## 下一步（按优先级）

0. **🟡 P0 已降级为「受限放行」（2026-09-19 二轮取证后更新）**
   前一轮列为「必须获取 Suvernev 全文，否则不得宣称贡献 ①② 独创性」。**本轮已取得决定性替代证据，可继续写作，但须加限定语。**

   **取证结果**：
   - **✅ 取得 Suvernev et al. (2026) 官方完整摘要**（CityUHK Scholars，DOI `10.21125/edulearn.2026.1345`），含全部定量结果：
     600 名大一队列 **均分 72%→54%**（而课外作业分**上升**）；SFT + RL/GRPO + **对抗课程**；OPTMentor = "integrates LLM calls plus a **jailbreak-prevention system**"；
     开源 1B–7B Python/C++ 模型；pilot 后**多数学生 +10–30%，平均 +11.9%**。
   - **判定**：摘要中**无任何泄露量化指标**，其安全机制为 **jailbreak-prevention（判定型 → 二值门控）**，训练目标为 **hint quality** 而非**泄露量上界**。→ **贡献 ①② 的核心机制差异依然成立。**
   - **⚠️ 残余风险**：摘要 ≠ 全文。**贡献 ① 措辞必须限定为"据其已公开摘要所述"**；取得全文后须复核一次。
   - **全文仍在 IATED 付费墙**，待出版或作者自存版（通讯作者 Chan, Chung @ CityUHK）。

   **本轮另有两项重要发现（均写入 `07` §七）**：
   - **🟢 arXiv 2512.03501「SocraticAI」与 Suvernev 无关** —— 作者是 **Sunil & Thakkar（Ashoka University）**，**同名不同组**。已取得全文核对：**泄露量化为零、无对照组、无 pre/post、样本量未报告**，且**自认学生"改写被禁的求答案请求"**。→ **它是最强的 gap 证据源，不是撞车源。**
   - **🟡 新增邻近工作 SocraticPO (arXiv 2606.09887)** —— 奖励侧对偶工作：用 **reward decay** 让学生"不依赖帮助"，但**约束在奖励端、由数据统计量自适定、无可调标量**；其 §5.4 **自认 prompt 明确禁答仍会泄露**。→ **定位为互补（reward-side counterpart），不得写成竞争。**

   详见 `07_Introduction动机链_原文证据锚定.md` §7.1–7.6。
1. **✅ M2 已完成**（2026-09-20）。`m2_lambda_sweep.py` 可复现，变异检验通过。
   - **A9 的功能形式已改为「阈值/边界」**（D6）。旧式连续线性 `damp = 1 − D·min(1,λ)` 与实测的**阶跃崩塌**机制不符；
     新式采纳 arXiv 2604.13006 的 **collapse floor**（"a **discrete strategy switch rather than continuous degradation**"）。
     文献依据：Brender §5.3（引导强度是设计变量）／§5.1（"may require **stronger or differently calibrated** forms of guidance"）／
     AMCIS 2026「Socratic Gap」(p=.045)／认知负荷理论。
   - **★ 命题语义已随形式改变**：λ\* 不再表示「最优引导强度」，而表示**守约边界下沿**。
     **禁止再写「最优值存在 / 内部最优 / sweet spot」**；正确表述是「**存在一条守约强度边界，λ\* 位于其下沿**」。
   - **残余风险**：文献给**形态**（阶跃+地板）不给**量级**；三个 A9 常数（深度/λ_c/锐度）均为**规定值**。
     论文须把 λ\* 报成**区间**，并说明其**存在性**与**归因份额**不随 A9 改变。
   - **变异检验状态**：9 个变异体 + **新机制专属 M8/M9** + 泛化的 3 字段 liveness，**全部按预期行为**
     （早期「5 个变异体全返回 SUPPORTED」的缺陷已修复，那是由两个真实 bug 造成的 —— 死参数 `durable_factor` 与缺失的归因对照）。
   - 详见 `08_M2实验审计记录.md`（含 §5.4 M3 重标定、§六 A9 残余风险）、`09_方向决策备忘.md`。
2. **M1 系统原型**：用现有 MIR3/WALL/MRAgent/BayesG 代码做**密码学**教育场景改装，先跑通「拆题→定位→引导→出题」闭环。
3. **M3 真实准实验**：**已取消**（D20 路径②，全模拟方法论论文）。真实课堂验证列为未来工作（§8.7）；原 M3 设计母稿已于 2026-09-21 移交 study-help-pro，落地位置 `E:/Program/MARL/study-help-pro/archive/sage_408_handoff/`（本工作区仅留指针，2026-09-22 清理时按「已核实目的地存在」原则移除）。
4. **M4 成稿**：把 01–06 的中文母稿转英文 + APA 6th 排版 + 双语参考文献。

## 口径红线（写作时不得违反）

- λ−泄露率曲线**不得**表述为"团队 MIR3 复现的教育版"。它是**明确标注假设的仿真结果**，且对 A9 敏感；真实学生证据须待未来课堂扩展（§8.7）。
- 仿真结论一律标注 `simulated learners`；本文不做真实课堂研究（D20 路径②），所有证据均为装置层面的仿真结果。
- **不得说"苏格拉底引导就是我们这个方向"**——它只是四支中的一支（prompt 层），SAGE 在损失层（详见 06 文档 §0）。
- **🚫 不得说"第 ④ 支无人占据 / 我们首创可训练约束"**——**Suvernev et al. (2026, EDULEARN26) 已用 RL+GRPO+对抗课程学习训练守约 hint 模型**。正确表述：「已有工作证明**可以训练**答案守约，但用**二值 jailbreak 过滤器**实现（**据其已公开摘要所述**），**未量化泄露量、未暴露强度参数**；SAGE 的差异在于把允许泄露的信息量做成目标函数中的显式项，**可连续调节、可测量、可绘制曲线**」。
  - **附加红线**：**不得写「Suvernev 完全未涉及泄露度量」**——我们只有摘要。须用「据其已公开摘要所述」限定。取得全文后复核。
- **🚫 不得说"无一在 CS 课程做实证"**——**已证伪**。Suvernev（600 名大一）、Lee（AIED 2026, Socratic Mind）、Sun（JCAL 2026, 80 人）、Thonge & Thakkar（ITiCSE 2026）、**Sunil & Thakkar（Ashoka CS-1102）全在 CS 编程课**。正确表述：「CS 课程已有实证，但**无一将脚手架约束与知识图谱锚定的学习者模型耦合**」。
- **🚫 不得把 Sunil & Thakkar (2025, arXiv 2512.03501) 与 Suvernev et al. (2026) 混为一谈**——**同名「SocraticAI」但完全无关**：前者 Ashoka University（输入侧校验），后者 CityU HK（训练 hint 模型）。混用会被审稿人抓到。
- **🚫 不得把 SocraticPO (2026, arXiv 2606.09887) 写成竞争工作**——它在**奖励侧**用 reward decay 解决"学生等帮助"，SAGE 在**内容侧**约束导师输出。二者**互补**。✅ 正确表述：「reward-side counterpart」。
- **🚫 不得声称"我们第一个指出 prompt 层不足"**——SocraticPO §5.4 已独立承认（"even when the prompt explicitly asks the teacher not to reveal the answer … may still leak solution-specific hints"，且"inherently limited by the teacher model's instruction-following ability"）。✅ 正确表述：「该局限已被领域内多项工作独立承认（Brender；Sunil & Thakkar；SocraticPO）」。
- **不得说"我们首创 Telling@N"**——那是 MathDial 的指标，Chudziak & Kostka (AIED 2025) 已在用。只能说「刻画 λ 与 Telling@N 的**关系**并报告**守约边界位置**」。
- **🚫 不得把互信息估计 `mi_hat` 当作泄露量度量**——该估计器**已证明退化**（λ 全程恒为裁剪上限 3.0，即使泄露率已降到 0.0003；根因是 `p_ans` 为 `em` 的确定性单调函数 → ρ² 按构造 ≈1）。泄露量**只用** ALR / Telling@N；互信息项只作为**训练目标**出现。详见 `08` §3.4。
- **🚫 不得声称「信息瓶颈给出泄露上界」**——M2 中该独立性不存在，须由人工编码提供（未来课堂扩展 §8.7）。
- 引用熊晓莉（渭南师范学院学报 2026, 41(5)）时**必须说明主体差异**（其 WEI 师服务**教师**，SAGE 服务**学生**），否则属不当类比。
- 引用 Suvernev et al. (2026) 时注意是 **EDULEARN26 会议论文**（IATED Academy），非顶会/期刊；但其 **600 人真实课堂 + 开源模型**使证据强度不可轻视，**必须正视而非淡化**。

## 相关参考
- 全部文档均在本目录内，无外部路径依赖。
- 代表作全文与缺口对照见 `06_苏格拉底引导代表作精读与缺口分析.md`。
