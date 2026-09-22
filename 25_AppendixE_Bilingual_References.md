# SAGE · Appendix E — References (bilingual, 双语著录)

> **Status (2026-09-21)**: first build. FEDC requires **non-English sources to be given bilingually**; this appendix is
> therefore not a plain bibliography — every Chinese-language source carries its original entry *and* an English rendering.
>
> ## ★ 本附录的第一纪律：**不编造元数据**
>
> 编造卷期页码／DOI 与编造结论同样严重，且更容易被审稿人当场查获。因此本表**逐条标注核验状态**：
>
> | 标记 | 含义 | 可否进正文参考文献表 |
> |---|---|---|
> | ✅ **已核验** | 已联网核真（期刊官网 / ERIC / DOI / 全文 PDF） | ✅ 可直接用 |
> | ⚠️ **元数据待补** | 作者与年份可信，但卷/期/页/DOI 未核 | ⚠️ 提交前必须补齐，否则删引 |
> | 🔴 **仅摘要 / 二手转述** | 未取得全文，或系他人转述 | 🔴 正文措辞**必须带限定语**（见 `07` 红线 10、13 §2.7） |
> | 🚫 **禁引** | 出处已撤回或系伪造来源 | 🚫 不得出现 |
>
> **未核验字段一律写 `[待核]`，禁止凭印象填数字。** 本轮已联网核真 6 条（见 §A），其中 1 条是**回原文 PDF 逐字核验**（Goldin 2012）。

---

## A0 · 四库核验批注（2026-09-22，源 `26_四库交叉核验与方向锐评.md`）

> OpenAlex / Crossref / Semantic Scholar / arXiv API 交叉核验的结果。**PubMed 本轮两度 IP 封禁且对本课题结构性不适用，未参与任何判定。**

**✅ 元数据坐实，A/B 组按此改写：**

| 引用 | 更正后著录关键信息 |
|---|---|
| Brender et al. (2026) | 真题 *Reflective Dialogue or Prompt Refinement? Effects of Tutor Scaffolding on Students' Independent LLM Use for Programming*。**7 位作者**：Brender, J., El-Hamamsy, L., Uittenhove, K., Pérez, A., Jermann, P., Mondada, F., & Bumbacher, E. Springer **LNCS, pp. 546–561**, DOI `10.1007/978-3-032-29763-1_37`。🚫 **删除 "AIED 2026 best paper"**（奖项不进任何书目库，不可核）；且其标题已明写 *Effects of Tutor Scaffolding* → §2.4.1 措辞须相应回退 |
| Suvernev et al. (2026) | 真题 *SOCRATICAI: ON TRAINING MODELS THAT MAKE STUDENTS THINK*。作者全 4 位：**Suvernev, B., Zhao, C., Wang, Z., & Chan, C.** EDULEARN Proceedings 1, DOI `10.21125/edulearn.2026.1345`（closed access，付费墙属实）。B 组该行删除"作者待补" |
| Asanov & Degen (2025) | **作者顺序更正为 Degen, P.-B., & Asanov, I.**（arXiv 2508.05116 记录 first=Degen, last=Asanov）。真题 *Beyond Automation: Socratic AI, Epistemic Agency…*。⚠️ 因变量为**自陈感知**，非学习结局，不得当作 RCT 有效性证据 |
| MathDial (2023) | 首作者拼写 **Mačina**（非 Macina）；已核 pp. 5602–5621, DOI `10.18653/v1/2023.findings-emnlp.372`, cited 35 |
| SafeTutors (2026) | arXiv `2603.17373`，8 位作者，**预印本未正式发表**。✅ **`17.7% → 77.8%` 摘要原文逐字命中**；可补 11 harm dimensions / 48 sub-risks |
| Weidlich et al. (2025) | ✅ JCAL 41(5) e70105, DOI `10.1111/jcal.70105`, **cited 40**（本文最硬的一条） |

**🔴 原判「四库核不到，补 / 撤待定」的四条 —— ✅ 2026-09-22 第五轮全部结案（其中三条不需要撤）：**

| 引用 | 旧判 | ✅ 结案结果 |
|---|---|---|
| ~~Thonge & Thakkar (2026, ITiCSE)~~ | OpenAlex `count: 0`（同组其它论文能查到，唯独这篇不能） | **该文存在，不需要撤**：真实标题是 *A Good Rubber Duck Does Not Quack: Designing Socratic Scaffolding in AI Tutors*（见 **A7-①**）。旧检索之所以 count=0，是因为**我们按自己内部的功能描述去搜**（"stateful misconception detection" / "questioning intensity"），而这两个词**从未出现在该文标题或摘要里**。🔴 **本轮最重要的教训**（与 `MEMORY` §5 相反方向的同类坑）：**按内部简称搜不到 ≠ 该文不存在，也不等于我们对它的陈述是错的**。当按标题／关键词检索得不到结果时，正确动作是**换一个维度反向检索**（用 OpenAlex `authorships.author.id` 直接列出该作者的全部作品），而不是据此判定"该文不存在"并撤引。若照旧判断执行，我们会删掉一条真实、可用、且恰好能承重的 ITiCSE 2026 论文 |
| ~~Chudziak & Kostka (2025, AIED)~~ | 未定位该标题 | **已定位**（见 **A7-②**）。年份是 **AIED 2025** 而非 2026：此前把届次记成了 2026。且它的 MathDial 对比（Tutor Prompt vs Base Prompt，`Telling@N` 更低）**恰好是 §2.4.2 最合适的已核用例** —— 撤掉反而赔本 |
| ~~SocraticLM (Liu et al., 2024)~~ | 本轮未能定位该标题 | **已定位**（见 **A7-③**）。NeurIPS **Spotlight** 属实；8 位作者；**与 SocraticPO (Liu et al., 2026) 同属 USTC / Enhong Chen 体系但年份与 venue 都不同**，切勿合并著录 |
| **Udeshi et al. (2026)** | 四库全无 | ✅ **已从所有英文正文撤引**（`07` §1.3、`13` §2.3、`13` §2.4.3、`14` §8.5）。承重由 **Zhao et al. (2026, ACL 2026)** 与 **Bastani et al. (2025, PNAS)** 接管；升为 🚫 禁引（见 D3）。**唯四条里真正被撤的一条** |

**🚫 口径错误（优先于以上全部）：**

1. **arXiv 2604.13006：引文属实，但领域类比未声明。** ✅ **2026-09-22 二次核实更正**：我们所引那句（"Compositional constraints show a collapse floor… discrete strategy switch rather than continuous degradation"，−29.8% / −27.0%）**逐字属实，出自全文 §4.1，不在摘要里** → **保留引文，不得删除**（只查摘要会误删真引用）。🔴 但全文检索确认该文**无** leakage / tutoring / scaffolding / pedagogy 任一术语，与教学无关 → `01` §3.2.2 已改为明示 **"an analogy, not evidence from our setting"** 并新增说明段。
2. **SocraticPO 被读错领域**：它是 RL 策略优化方法（Reinforce++ / SciKnowEval），其 student 为**被训练的策略网络**，不是人类学习者。移出"教育邻近工作"位；**删除以"其全文无 telling@N"充当 gap 证据的写法**（RL 论文里当然没有该指标）。
3. **🔴 P0 撞车 Pisan (2026), arXiv `2608.12292`** —— *Teaching a LLM Tutor to Withhold the Answer: A Supervisor Architecture and an Evidence-Driven Method for Tuning Socratic Behavior*（Univ. of Washington Bothell）。已部署、逐轮机检合同、八级帮助阶梯、**无人类被试**。
   ✅ **2026-09-22 已处置**：`13` §2.3(b) 单列点名（并写入"即便最强 (b) 类也只给 bound、不给 decomposition"的结构性理由）；
   `22` **新增 §7.3.1** 正面区分并明确让步（守约/机检/部署三项都让；只保留归因分解一句；并把"拿我们的装置跑它的日志"写成下一步）；
   原 7.3.1–7.3.3 顺延为 7.3.2–7.3.4；`22` §7.4 的"下一步跑谁的数据"由 Mukherjee 改为 **Pisan**。
   ⚠️ 元数据（卷期页 / 是否已正式发表）仍待补 —— 该条是全文**最承重**的相邻工作，不得留 [待核]。

## A. 已核验（可直接进参考文献表）

**A1** Weidlich, J., Gašević, D., Drachsler, H., & Kirschner, P. A. (2025). *ChatGPT in education: An effect in search of a cause*. **Journal of Computer Assisted Learning, 41**(5), Article e70105. https://doi.org/10.1111/jcal.70105
— ✅ 2026-09-21 核（ERIC EJ1484305；Wiley；作者机构：苏黎世大学 / Monash / DIPF / 开放大学荷兰 / Thomas More）。**10 页**。
— 正文用途：§1.4 支点、§2.4.3、§7.5（"observed gains cannot, at this time, be confidently attributed to ChatGPT"；"measure learning after the treatment is removed"）。

**A2** Deng, R., Jiang, M., Yu, X., Lu, Y., & Liu, S. (2025). *Does ChatGPT enhance student learning? A systematic review and meta-analysis of experimental studies*. **Computers & Education, 227**, 105224. https://doi.org/10.1016/j.compedu.2024.105224
— ✅ 2026-09-21 核（ScienceDirect / dblp）。**注意**：DOI 年份段为 2024，卷期年 2025，著录以 **2025** 为准。
— 正文用途：§1.4 / §2.4.3 / §7（Weidlich 审计的 19 项比较即出自此元分析）。

**A3** Macina, J., Daheim, N., Chowdhury, S. P., Sinha, T., Kapur, M., Gurevych, I., & Sachan, M. (2023). *MathDial: A dialogue tutoring dataset with rich pedagogical properties grounded in math reasoning problems*. In H. Bouamor, J. Pino, & K. Bali (Eds.), **Findings of the Association for Computational Linguistics: EMNLP 2023** (pp. 5602–5621). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.findings-emnlp.372
— ✅ 2026-09-21 核（arXiv 2305.14536 / ACL Anthology / ETH / NIE）。
— 正文用途：*Telling@N* 的出处（§2.4.2、§5.4）。**不得写"我们首创 Telling@N"**（`07` 红线 5）。

**A4** Mukherjee, M., Le, J., & Chow, Y.-W. (2025). *Generative AI-enhanced intelligent tutoring system for graduate cybersecurity programs*. **Future Internet, 17**(4), 154. https://doi.org/10.3390/fi17040154
— ✅ 2026-09-21 核（MDPI，开放获取，**19 页**；Institute of Cybersecurity and Cryptology, University of Wollongong）。
— ⚠️ **重要修正（供 §7.3.2 使用）**：该文自述其评估为**问卷式**的内容质量 / 平台可用性 / 感知有效性评价，并明确 "**Empirical validation remains a task for future research**"。
  → 因此 §7.3.2 不得说他们"在课程中验证了学习效果"；准确说法是"**他们报告的是感知有效性与内容质量，未报告学习结局，也未做归因分解**"。这比我们原先的写法更准确，也更不容易被原作者反驳。

**A5** Goldin, I. M., Koedinger, K. R., & Aleven, V. (2012). *Learner differences in hint processing*. In **Proceedings of the 5th International Conference on Educational Data Mining (EDM 2012)** (8 pp.; 页码 [待核]，据 PDF 页脚推为 73–80). Chania, Greece. ERIC ED537206.
— ✅ **2026-09-21 回原文 PDF 逐字核验**（非二手摘要）：
  - "the next action that they are most likely to perform in the tutor is to ask for a second hint (**87%** of the time) … a third (**88%** of the time)" ✅
  - Table 2 成功率 **78% / 21% / 37% / 82%**（C/(C+I+H)）✅
  - "neither short nor long hint reading times are positively associated with learning" ✅
  - ⚠️ 措辞已按原文**降级**：原文是"最可能的下一步动作"，不是"87% 的学习者都会继续"——`21` §4.3 与 `22` §7.2 已同步改准。

**A5-b** Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakçı, Ö., & Mariman, R. (2025). *Generative AI without guardrails can harm learning: Evidence from high school mathematics*. **Proceedings of the National Academy of Sciences, 122**(26), Article e2422633122. https://doi.org/10.1073/pnas.2422633122
— ✅ **2026-09-22 二轮回源核真**：**Crossref 记录**（`api.crossref.org/works/10.1073/pnas.2422633122`）＋ **PNAS 全文页**逐条对上。
  元数据坐实：**PNAS 122(26), Article e2422633122, 2025-06-25**；六作者顺序 **Hamsa / Osbert Bastani, Sungu, Ge, Kabakçı, Mariman** ✅
— 🔴 **本条是全文最承重的实证来源**。⚠️ **2026-09-22 更正一处实质表述错误**：
  **随机化单位是 classroom，不是 student** —— 原文 "students are randomly assigned to classrooms" / "SEs are clustered at the classroom level **(which is the unit of randomization)**"；
  规模 = **约 50 个 9–11 年级班 / 近 1000 人 / 4×90 分钟**；**主样本排除 honors-designated classrooms**。
  → `13` §2.2、§2.4.3、§2.6 与 `22` §7、`14` §8.4 **五处已改**。
— ✅ **Correction 已核**：该文有 correction（**2025-08-20，DOI 10.1073/pnas.2518204122**，PNAS 122(34)）。
  内容经逐字核对：**仅更正 Osbert Bastani 的 affiliation（production error）**，**不涉及任何数字、样本或结论** → **正文无需标注**。
— 🔴 **GPT Tutor 护栏的真实构成（回原文核，三条）**：① 提示词指示 *"provide hints to the student **without directly giving them the answer**"*；
  ② *"guide them in a **step-by-step** fashion"*；③ **提示词注入教师提供的正确解法、常见错误与反馈话术**（因 *"GPT Base often provides incorrect answers due to hallucinations"*）。
  → 因此 guarded 组相对 unguarded 组同时变了 **三样**（引导 / 不给答案 / **反馈正确性**），
  **不得再描述为只变了"引导 + 不给答案"两样**；`13` §2.4.3 与 `22` §7 已升级为三通道。
  → 且**护栏全在提示词层**，即最强 guardrail 证据落在 §2.3(a) 提示词层（`13` §2.4.3 已明写）。
— 数字（摘要逐字）：练习 +**48%**（GPT Base）/ +**127%**（GPT Tutor）；撤除后考试 **−17%**（GPT Base），GPT Tutor 与控制组**无统计显著差异**。
— 三处用途：① `13` §2.2 作为"表现/学习分离"的**最强证据**（班级随机而非观察），并已划清它**只比较"有无护栏"、不分解护栏内部**；
  ② `14` §8.1.1 作为 `leak_durable` 的**方向性外部锚**（买来的收益不持久）——仅方向，非量级；
  ③ `22` §7 须正面区分（它分离的是 treatment vs control，本文分离的是 treatment 内部两条通道）。
— ⚠️ 不得写成"它证明了引导是有效成分"——那正是本文要拦的推断。

**A5-c** Pisan, Y. (2026). *Teaching a large language model tutor to withhold the answer: A supervisor architecture and an evidence-driven method for tuning Socratic behavior*. arXiv:2608.12292 [cs.CY]. https://doi.org/10.48550/arXiv.2608.12292
— ✅ **2026-09-22 核**（arXiv abs 页）。**独著**；University of Washington Bothell；submitted 2026-08-12；**预印本，未见正式发表记录**（无 "accepted at" 注释）。
— 摘要要点（逐字）：逐轮机检合同 + **非 LLM 策略核心**设定**八级帮助阶梯**的每轮上限 + 确定性检测器剥离 solution code + 独立 LLM 裁判逐条检查；
  自动评估**无人类被试**（脚本化 persona 走真实管线、更强模型重打分），记录每次拒绝的 stated reason；四项验收标准全部达标。
— 用途：`13` §2.3(b)（最强 (b) 类，只给 bound 不给 decomposition）+ `22` **§7.3.1**（正面区分并让步）。
— ⚠️ 元数据仍缺：若后续正式发表须换正式版本；**机构名建议再核一次**（现据 `26` 的记录）。

**A5-d ~ A5-g** · 经 **Pisan (2026) 参考文献 [1]–[3]、[5]** 溯源获得（arXiv HTML 全文版逐字抄录，元数据完整）

| 编号 | 著录 | 用途与纪律 |
|---|---|---|
| **A5-d** | Aleven, V., Stahl, E., Schworm, S., Fischer, F., & Wallace, R. (2003). *Help seeking and help design in interactive learning environments*. **Review of Educational Research, 73**(3), 277–320. https://doi.org/10.3102/00346543073003277 | ✅ 求助行为领域的**权威综述**（RER）。**比 `12` D11 现用的 Aleven et al. (2004, ITS) 更适合作为"求助行为重要"的引用** → 已写入 `17` §5.4。⚠️ 不得与 2004 ITS 版混为一条 |
| **A5-e** | Baker, R. S. J. d., Corbett, A. T., Koedinger, K. R., & Wagner, A. Z. (2004). Off-task behavior in the Cognitive Tutor classroom: When students "game the system." In *Proceedings of SIGCHI Conference on Human Factors in Computing Systems (CHI '04)* (pp. 383–390). https://doi.org/10.1145/985692.985741 | ✅ **与 `12` D10 的 ITS 2004 版是同年两篇不同论文，非同一篇的两个版本** → 可并存互补。已写入 `13` §2.2 |
| **A5-f** | Anderson, J. R., Corbett, A. T., Koedinger, K. R., & Pelletier, R. (1995). Cognitive tutors: Lessons learned. **The Journal of the Learning Sciences, 4**(2), 167–207. https://doi.org/10.1207/s15327809jls0402_2 | ✅ ITS / 知识追踪的传统基础。已写入 `13` §2.5 |
| **A5-g** | Bloom, B. S. (1984). The 2 sigma problem: The search for methods of group instruction as effective as one-to-one tutoring. **Educational Researcher, 13**(6), 4–16. https://doi.org/10.3102/0013189X013006004 | ✅ 一对一辅导效果的经典基线。已写入 `13` §2.1。⚠️ **只可作"辅导为何值得做"的动机**，不得当作 SAGE 效果的类比或预期 |

**A6** 本刊（FEDC）已发论文 —— ✅ 2026-09-21 于 journal.hep.com.cn/fed 核真（见 `13` §2.7）

| 页码 | 著录 | DOI |
|---|---|---|
| 21(2): 105–125 | Huang, C., Zhong, Y., Wang, X., Han, Z., & Wei, T. (2026). From single-agent system to multi-agent system: Design and empirical study on motivational learning activities supported by LLM-based agents. *Frontiers of Education in China, 21*(2). | 10.3868/s110-021-026-0006-5 |
| 21(2): 126–149 | Wang, Z., Wu, F., Guo, Z., & Zhang, M. (2026). Advancing creative thinking: Construction and application of a GenAI-based multi-agent collaborative system. *FEDC, 21*(2). | 10.3868/s110-021-026-0007-2 |
| 21(2): 150–174 | Ma, L., Zheng, X., & Zhou, X. (2026). Portraits of student types using GenAI-assisted learning: An empirical study based on a survey of undergraduates from 20 higher education institutions in China. *FEDC, 21*(2). | 10.3868/s110-021-026-0008-9 |
| 21(2): 175–198 | Sun, Y., Huang, Y., & Wen, S. (2026). The analysis of interaction modes in human–machine collaborative learning supported by generative artificial intelligence. *FEDC, 21*(2). | 10.3868/s110-021-026-0009-6 |
| 20(4): 377–397 | Lu, Y., Yu, J., & Chen, P. (2025). Design and application of pedagogical agent with foundation models. *FEDC, 20*(4). | 10.3868/s110-020-025-0020-3 |

**A6-b 双语著录（Sun et al. — 已有中文原版，必须双语）**
- 英文版：Sun, Y., Huang, Y., & Wen, S. (2026). The analysis of interaction modes in human–machine collaborative learning supported by generative artificial intelligence. *Frontiers of Education in China, 21*(2), 175–198. （译自中文原版）
- 中文原版：孙艳艳, 黄英芬, 文思帆. 生成式人工智能支持下人机协同学习的交互模式分析[J]. *现代远程教育研究*, 2025(3): 102–112.
- ⚠️ 其余四篇（Huang / Wang / Ma / Lu）**是否有中文原版待查**；若有，须同样双语著录。

---

## B0 · 2026-09-22 四库新核实（可直接落表；B 组对应行按此更新）

> 以下均为 OpenAlex / Crossref / arXiv API 取到**标题 + 作者 + ID** 三者齐备者。
> ⚠️ 除标注会议者外**全部为预印本**，投稿前须复查是否已正式发表。

**① 由 B 组升级（元数据已坐实）**

| 著录 | 状态 |
|---|---|
| Brender, J., El-Hamamsy, L., Uittenhove, K., Pérez, A., Jermann, P., Mondada, F., & Bumbacher, E. (2026). *Reflective dialogue or prompt refinement? Effects of tutor scaffolding on students' independent LLM use for programming*. In **AIED 2026** (LNCS), pp. **546–561**. Springer. https://doi.org/10.1007/978-3-032-29763-1_37 | ✅ 完整；机构 EPFL + HEP Vaud；🚫 **删 "best paper"** |
| Suvernev, B., Zhao, C., Wang, Z., & Chan, C. (2026). *SocraticAI: On training models that make students think*. **EDULEARN26 Proceedings**, 1. https://doi.org/10.21125/edulearn.2026.1345 | ✅ 完整；closed access；仍须带"据其已公开摘要所述" |
| Potraghloo, E. B., Azizi, S., Kundu, S., & Pedram, M. (2026). *One token away from collapse: The fragility of instruction-tuned helpfulness*. arXiv:2604.13006. | ✅ 完整；引文在 **§4.1**；**跨领域类比已声明** |
| Liu, Z., Pan, T., Ouyang, J., Liu, Q., Wang, X., Liu, J., Li, Q., Sha, J., Huang, Z., Wang, S., & Chen, E. (2026). *SocraticPO: Policy optimization via interactive guidance*. arXiv:2606.09887. | ✅ 完整；**student = 被训练的策略网络，非人类学习者** |
| Hazra, R., Ghuku, B., Marchenko, I., Tokarieva, Y., Layek, S., Banerjee, S., Stoyanovich, J., & Pechenizkiy, M. (2026). *SafeTutors: Benchmarking pedagogical safety in AI tutoring systems*. arXiv:2603.17373. | ✅ 完整；**预印本** |
| David, J., & Ghosh, S. (2025). *IntelliCode: A multi-agent LLM tutoring system with centralized learner modeling*. arXiv:2512.18669. | ✅ 完整；**demo paper**，证据层级低 |
| **Degen, P.-B., & Asanov, I.** (2025). *Beyond automation: Socratic AI, epistemic agency, and the implications of the emergence of orchestrated multi-agent learning architectures*. arXiv:2508.05116. | ✅ **作者顺序已更正（Degen 在前）** |

**② 新增（2026 年补检发现，§2.3(e) 与 §1.4 已引）**

| 著录 | 正文引用处 |
|---|---|
| Pisan, Y. (2026). *Teaching a large language model tutor to withhold the answer: A supervisor architecture and an evidence-driven method for tuning Socratic behavior*. arXiv:2608.12292 [cs.CY]. University of Washington Bothell. | §1.4(i)、§2.3(e)、§7.3.1（**P0 撞车**） |
| Zhao, J., Knežević, M., & Käser, T. (2026). *Evaluating answer leakage robustness of LLM tutors against adversarial student attacks*. arXiv:2604.18660. **ACL 2026**. | §1.3 失败1（替换 Udeshi）、§2.3(e) |
| Fan, S., Deng, B., Xu, M., Liu, J., Zhang, H., Yang, Q., & Gao, C. (2026). *Rethinking LLM-judged helpfulness as a pedagogy signal: A pre-registered audit across tutor models*. arXiv:2607.28128. | §1.4(iii)、§2.3(e) |
| Kadir, N. (2026). *Auditable release control for pedagogical leakage in LLM tutors*. arXiv:2608.00515. （自标 "not peer reviewed"） | §1.4(iii)、§2.3(e)、§2.4.3 |
| Wang, X., Song, S., Liu, W., & Zou, X. (2026). *Beyond direct answering: Aligning educational LLMs as Socratic guides via heuristic reinforcement learning*. arXiv:2607.22996.（HeuristicEdu） | §1.2、§1.5(2)、§2.4.2、§8.2（**对己不利证据**） |
| Gai, Y., Zhang, Y., & Huang, X. (2026). *ExplainRoute: A pre-deployment audit framework for non-answer-giving programming tutors*. arXiv:2609.03470. | §1.4(iii)、§2.3(e) |
| Hossain, S. M. A., Shayoni, R. K., Mridha, M. F., & Shin, J. (2026). *EduGuard: A safe RAG-based LLM tutor for programming education*. arXiv:2607.15738. **ICCA 2026**. | §2.3(e)、§2.4.2 |

**③ NLP 主线（2026-09-22 已写入 `13` §2.3.1，元数据齐备）**

| 著录 | 状态 |
|---|---|
| Xie, W., Shi, H., Li, Y., & Liu, J. (2025). *STAP: A Socratic tutor for adaptive programming with pedagogical scaffolding*. In **Proceedings of the 2025 2nd International Symposium on Artificial Intelligence for Education (ISAIE '25)** (pp. **584–587**). ACM. https://doi.org/10.1145/3775073.3775165 | ✅ **2026-09-22 二轮回源核验**（Crossref + Unpaywall + OpenAlex + Semantic Scholar + ACM DL）：正式发表，**4 页**系统论文（pp. 584–587）；四作者机构均为 **North China University of Technology（北方工业大学）**；**gold OA / CC-BY**。
🔴 **但全文四通道全封、取不到**：ACM 直连 PDF **403**；Unpaywall `url_for_pdf: null`；OpenAlex `has_fulltext:false`；fatcat 归档 API SSL 拒连；S2 的 `openAccessPdf` **只是落地页 DOI**（易误读为已拿到全文）。
→ **已按红线降档**：摘要逐字句 **"We also formalize key concepts (Socratic hints, MVH, and answer leakage)"** 是**正文唯一可采用的表述**；`13` §2.3.1 已删除"§3.2 *Terminology and Formalization*""operational definitions and compliance criteria for each""a turn complies or it does not"三处**无据断言**；此前记录的"引言贡献 (3) 含 operational definitions and compliance criteria"**本轮无法复现，已撤**。
⚠️ **日期打架**：Crossref / OpenAlex 记 **2025-09-19**，ACM DL 页面显示 **2025-12-10** → 著录年份取 **2025**，具体日期 **[待核]**。评估自述 scope-limited formative |
| 🔴 **Dinucu-Jianu, D., Macina, J., Daheim, N., Hakimi, I., Gurevych, I., & Sachan, M. (2025). *From problem-solving to teaching problem-solving: Aligning LLMs with pedagogy using reinforcement learning*（**TutorRL**）. In **Proceedings of EMNLP 2025** (pp. **272–292**), Suzhou. https://doi.org/10.18653/v1/2025.emnlp-main.15 | ✅ **2026-09-22 新增并回原文核（ACM/ACL Anthology PDF 全文，21 页）**：ETH Zürich + ETH AI Center + UKP Darmstadt（**Gurevych & Sachan 组**）。
   🚫 **本条是我们漏掉的最强训练层先例 —— 它直接证伪了旧版 §2.4.2 的那句加粗断言**：
   ① 用 **online RL** 在**模拟学生–导师交互**里训练 7B 导师；奖励 = 对话后学生解题率 + 教学评委分；
   ② 暴露**可连续调节的泄露惩罚权重 λ**，并**逐项画出** *Figure 4: (a) ∆Solve rate vs. λ、(b) Leak Solution Rate vs. λ、(c) Pedagogical Reward vs. λ*；
   ③ *Figure 1* 明确写成 **"multi-objective scenario"**，在 solve rate（y）与 leaked solutions（x）之间**描出 Pareto 前沿**；λ=0 → 最大化成功率但靠泄题；λ=0.75 均衡。
   → **"可调约束强度 ↔ 泄露率的关系"不是我们首创，2025 年就有了**。`13` §2.4.2 已按此收窄为"**分级约束 + 持久结果 + 通道分解**三者同时具备"。
   ⚠️ 它的结果是**对话后即时解题率**（非撤除工具后测得），且 λ 让泄露与成功率**沿前沿一起移动**，是**权衡刻画而非增益分解** —— 这两点是我们残存的差异，必须照此表述，不得含糊 | In **Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)** (pp. **7165–7188**), San Diego. https://doi.org/10.18653/v1/2026.acl-long.325 | ✅ **2026-09-22 回源核验（ACL Anthology）**：正式发表，页数已补。摘要要点：**"assessment-driven control loop that infers the learner's cognitive state, evaluates whether the current step target is met, and adaptively selects tutoring actions"** → 与贡献 (3) 的耦合最接近，故 `13` §2.5 与 `07` §1.5(3) **均不得宣称该耦合为新** |
| Petukhova, K., Nguyen, T. D., & Kochmar, E. (2026). *Towards pedagogically aligned LLM tutors for math mistake remediation*. In **Proceedings of the 21st Workshop on Innovative Use of NLP for Building Educational Applications (BEA 2026)** (pp. **118–140**), San Diego. https://doi.org/10.18653/v1/2026.bea-1.10 | ✅ **2026-09-22 回源核验（ACL Anthology）**：正式发表，页数已补。摘要首句即 **"guiding students without revealing final answers"**；**SFT + DPO**，偏好对沿 **scaffolding / factuality** 维度合成；末句自陈 "challenges in reliably evaluating tutoring quality" |
| Wei, S., Zhang, M., Lin, X., Jiang, B., Dai, Z., & Kuang, K. (2026). *EduDial: Constructing a large-scale multi-turn teacher–student dialogue corpus*. **Findings of EMNLP 2026**. arXiv:2510.12899. | ✅ **2026-09-22 回源核验（arXiv abs）**：comment 字段标注 **"Accepted to Findings of EMNLP 2026"**；34,250 对话 / 345 知识点 / **11 维评估框架**（含 ZPD 提问与元认知提问）；另训 EduDial-LLM 32B
  ✅✅ **2026-09-22 全文已取回并逐字复核（22 页 PDF，`_refs/edudial_2510.12899.pdf`）—— 正文陈述全部命中**：
  34,250 sessions / **345** core knowledge points / Bloom 分类 + **ten** questioning strategies（含 situational、ZPD、metacognitive）/ **11 维**（9 overall quality + 2 content quality，其 Table 3）/ EduDial-LLM **32B**。
  ⚠️ **补一条范围限定（已回写 `13` §2.3.1）**：该语料是 **K–12 数学**（345 知识点覆盖 173 章），**不是高等教育** → 我们场景为研究生密码学，引用时不得暗示其语料直接覆盖本场景。
  ➕ 另核到可用的硬事实：五阶段递进教学流程；**5 名数学教师**独立评分，**Cohen's κ = 0.76**；对 **17 个**主流 LLM 做了评测。 |
| Ling, F., & Yu, H. (2026). *ToST: A tree-of-thought Socratic teaching framework for multi-path guidance and parallel thinking*. arXiv:2608.25775. | ⚠️ **2026-09-22 回源核验：预印本**，arXiv 无 accepted 标注，正文已标 preprint；MPSG-Bench **31K** 多路径对话 + **SOLO 五维**评估；投稿前复查是否已发表 |
| Puech, R., Macina, J., Chatain, J., Sachan, M., & Kapur, M. (2025). *Towards the pedagogical steering of large language models for tutoring: A case study with modeling productive failure*（**StratL**）. In **Findings of the Association for Computational Linguistics: ACL 2025** (pp. **26291–26311**). https://doi.org/10.18653/v1/2025.findings-acl.1348 | ✅ **2026-09-22 第三轮新增，全文已取到**（ACL Anthology PDF，共 21 页）：ETH Zürich（+ École polytechnique），**与 TutorRL 同组**（Sachan / Kapur）；**Kapur 即 *Productive Failure* (2008) 原作者**。
   **全文逐字核出一项对己不利、但必须承认的事实**：其 **PF Score** 只给 *"the student found on their own"* 的关键推理步骤记分，并明写 *"we do not award the point if the tutor reveals it or directly hints to it"* → **这是我们 earned-solve 结果量的部分前身，结果量的"形式"不是我们引入的**；已写入 `13` §2.3.1（第四条）与 `01`。
   ✅ **但对 §2.4.1 无害**：全文 `strength` / `scalar` / `tunab` / `graded` / `sweep` / `leak` **均 0 命中** → 其 *pedagogical steering* 是**意图级**（按专家转移图在 intent 间选择），**不是可调约束强度**，也不报任何曲线；已作为"最易被误认为反例"的显式区分写入 `13` §2.4.1。
   ⚠️ **术语纪律**：***pedagogical steering* 是 Puech et al. 命名的问题，不是我们的说法**（已进入 `13` §2 红线清单）。
   另可核事实：现场研究 = **17 名新加坡九年级学生**、两项练习、随机分入两个 tutor 版本、人工按 rubric 评分；预研究用 **GPT-4 模拟学生**，作者**明确声明不假设 LLM 能建模学生学习** |

> ⚠️ **引用纪律**：`13` §2.3.1 已写明 **"answer leakage" 这一术语由 STAP (2025) 先行 formalise，不是本文引入**，
> 且**不得**任何位置写"本文首次命名/提出该概念"；该纪律已同步为 `13` §2.7 第 18 行，并进入 §2 的红线清单。
> ⚠️ **五条的发表状态**：STAP / ScaffoldLM / BEA / EduDial **均已正式发表**（可进正式参考文献表），**仅 ToST 为预印本**（正文须标 preprint）。
> 🚫 **"撞车"一词只留在 `26` 与 memory 里**：`13`、`25` 及任何正文字段一律按**正常相关文献**处理，不得出现该措辞。
> 🔴 **仍待办**：**仅 STAP 一条**为摘要级（四通道全封：ACM 403 / Unpaywall `url_for_pdf:null` / OpenAlex `has_fulltext:false` / fatcat 拒连），投稿前须再试一次取全文（尤其其 §3.2 formalization 原文）。
> ✅ **已结案（2026-09-22）**：ScaffoldLM（24 页）、BEA（23 页）、Puech/StratL（21 页）、**EduDial（22 页）** 全文均已取回并逐字复核；Puech 全文另核出对己不利但必须承认的事实（见上表第 181–185 行）。
> ⚙️ **取全文的可复用经验**：arXiv PDF 通道**并非不可用**——此前 "SSL 拒连" 属瞬时/客户端问题；**加 `User-Agent` 头 + 依次回退 `arxiv.org/pdf/<id>` → `export.arxiv.org/pdf/<id>` → 版本化 URL** 即可取到（见 `_refcheck_edudial.py`）。取到后**先验 `%PDF` 魔数**再落盘，避免把 HTML 错误页当 PDF。

---

## A7 · 2026-09-22 第五轮：四条悬案的真实身份（其中三条差点被我们误撤）

> 本组是**反结论**的产物：此前按标题／关键词检索判为"四库核不到"、已进入「补 / 撤」待定的三条，
> 全部能用**作者反查**定位，且元数据完整可核。
> 处置纪律：**悬案必须逐条结案，不得靠"看着不像真的"就删** —— 反过来，也有一条（Udeshi）是真的撤了。

| 编号 | 著录 | 旧内部简称 → 真实身份 | 引用纪律 |
|---|---|---|---|
| **A7-①** | Thonge, A., & Thakkar, A. (2026). *A good rubber duck does not quack: Designing Socratic scaffolding in AI tutors*. In **Proceedings of the 31st ACM Conference on Innovation and Technology in Computer Science Education V. 1 (ITiCSE 2026)** (pp. **196–202**). ACM. https://doi.org/10.1145/3803400.3809368 | 旧称"ITiCSE 2026 · 有状态误解检测 + 多层校验" → **真实标题完全不同，一字不差对不上**。Ashoka University（Sonipat, India）；两位作者 ORCID 均已在索引登记；gold OA, CC-BY-NC-ND；资助方 Mphasis Foundation；会议地 Madrid | 🔴 **仅持有摘要，ACM 全文未取得**。摘要原文确认：*"We present Socratic AI, a VS Code-integrated tutor that addresses this through pedagogically-grounded Socratic dialogue constrained to withhold direct solutions."*；动机句 *"...doing so undermines the struggle necessary for conceptual learning"* 亦为真。→ 正文只能用**摘要能支撑的强度**；我们曾使用的 "stateful misconception detection" / "questioning intensity" / "persist on conceptual gaps" **三条内部表述无法从摘要验证**，`13` §2.3(b) 与 §2.4.1 已就地降级。该文参考文献含 Kapur (2008)、Koedinger et al. (1997)、Liu & Malan (2023, CS50 Duck) 及 **Sunil & Thakkar (2025)** → **同组关系由其自身参考文献确认** |
| **A7-②** | Chudziak, J. A., & Kostka, A. (2025). *AI-powered math tutoring: Platform for personalized and adaptive education*. In **Artificial Intelligence in Education — 26th International Conference, AIED 2025, Proceedings, Part VI** (pp. **462–469**). Springer. https://doi.org/10.1007/978-3-031-98465-5_58 | 旧记录只有"AIED"，未记届次与页码 → **实为 AIED 2025**（Palermo，2025-07-22~26）；Warsaw University of Technology | ✅ 其摘要自陈在 **MathDial** 上 Tutor Prompt 相对 Base Prompt 取得更高 Success@N 与更低 `Telling@N` → `13` §2.4.2 的用例**无需再核**；🚫 由此更不得写"无人测 Telling@N" |
| **A7-③** | Liu, J., Huang, Z., Xiao, T., Sha, J., Wu, J., Liu, Q., Wang, S., & Chen, E. (2024). *SocraticLM: Exploring Socratic personalized teaching with large language models*. In **Advances in Neural Information Processing Systems 37 (NeurIPS 2024)** (pp. **85693–85721**). https://doi.org/10.52202/079017-2721 | 旧记录只有"SocraticLM / NeurIPS Spotlight / 35K" → **8 位作者**齐全（USTC + 认知智能全国重点实验室 + 讯飞）。SocraTeach：35K 多轮（等价 208K 单轮） | 🔴 **与 SocraticPO (Liu et al., 2026, arXiv 2606.09887) 同为 Enhong Chen 体系，但年份与 venue 不同** → 任何场合**不得合并著录**。⚠️ 页码取自作者仓库自附 citation，投稿前建议再核一次 |
| **A7-④** | Sunil, K., & Thakkar, A. (2025). *SocraticAI: Transforming LLMs into guided CS tutors through scaffolded interaction*. arXiv:2512.03501 [cs.CY]. https://arxiv.org/abs/2512.03501 | "COMPUTE 2025 的 SocraticAI" → arXiv API 已核（2025-12-03），comment 自陈 *"Presented in the Best Practices Track of COMPUTE 2025"* | ✅ 摘要逐字可用。⚠️ 作为正式条目应优先取 COMPUTE 2025 正式版；**在取得前一律标 preprint** |
| **A7-⑤** | Kao, S., Grant, P., & Woltering, S. (2026). *Socratic AI in K–12 science classrooms: Effects on critical thinking, motivation, and self-regulation in a randomized controlled trial*. **Research Square preprint**. https://doi.org/10.21203/rs.3.rs-8118546/v1 | "K-12 RCT (2026)" 此前**无作者、无出处**，只是个描述性标签 → 现已定位：Texas A&M University，**90 名十年级**，三臂（对照 / ADI / AI 驱动 ADI 用 ChatGPT Study Mode），2025-12-15 上线 | 🔴 **预印本，未见同行评审版本**（OpenAlex type = preprint）。关键句逐字命中：*"Effects on metacognitive self-regulation were nonsignificant."* → **§1.3 失败模式③ 可以保留，但必须标注为 preprint**；若需它承担较重论证，须先寻得正式版 |

> **元教训（应写入 `MEMORY` 级别）**：这批"核不到"里**至少三条是检索失败，不是来源不存在**。
> `MEMORY` §5 已记过"只查摘要→误判无法证实→误删真引用"；本轮的失败方向**正好相反**：
> **按内部简称/自己写的功能描述去查标题，查不到就当成"该文可能不存在"**。两边加起来是同一条完整纪律 ——
> **不得据一次"查不到"（negative result）就判定一篇文献不存在或不可用；必须换方向做反向检索（先定位作者，再取该作者全部作品列表）之后才下结论。**

---

## A8 · 2026-09-22 第六轮：B 组十四条全部坐实（含 **三处必须改正文** 的事实）

> 本轮方法要点：**B 组剩下的大多是"常识性引用"（Kapur / Tishby / Alemi）与"内部简称"（Socratic Mind / EduClaw / Wolfpack）**。
> 前者按标准题名一搜即中；后者再次踩中 A0 那条纪律 —— **按我们自己的功能描述搜，全军覆没**。
> 破题靠的办法是：**把内部简称还原成"系统名 + 会议"（Socratic Mind + AIED 2026）、或直接用方法名 + 领域（Wolfpack + MARL）**。

| 编号 | 真实著录 | 核验要点与动作 |
|---|---|---|
| **A8-①** | Lee, J., Yilmaz Soylu, M., Hung, J.-T., Grigoryan, G., Cui, C., & Forsyth, D. (2026). *Scaling Socratic Dialogue with Generative AI: Understanding Implications for Student Engagement and Learning Outcomes*. AIED 2026, **LNCS 16585, Part V, pp. 137–145**, DOI `10.1007/978-3-032-29770-9_16`（2026-06-29）；Georgia Tech + UCSD | ✅ 即旧录的"Socratic Mind"。⚠️ **另有前置同系统论文**：Hung, J.-T., Cui, C., Popescu, D. M., Chatterjee, S., & Starner, T. (2024). *Socratic Mind: Scalable oral assessment powered by AI*. Learning@Scale '24, pp. 340–345 —— **不是同一篇，不得互相替代** |
| **A8-②** | Kapur, M. (2008). *Productive Failure*. **Cognition and Instruction, 26(3), 379–424**, DOI `10.1080/07370000802212669`；ERIC `EJ800999` | ✅ 三源一致（ERIC + BibBase + 全文 PDF 首页逐字）。→ `01` §3 / `22` §7 的 "(Kapur, 2008)" **无需改动** |
| **A8-③** | Alemi, A. A., Fischer, I., Dillon, J. V., & Murphy, K. (2017). *Deep Variational Information Bottleneck*. **ICLR 2017**；arXiv `1612.00410`，DOI `10.48550/arXiv.1612.00410` | ✅ 4 位作者齐全。🟡 **Alemi 正文自己引的是 Tishby et al. (1999)**（Allerton 1999 / arXiv `physics/0004057`, 2000），我们 `01` §3 写 "Tishby et al., 2000" → **指向 arXiv 版站得住，但与权威引用惯例（1999）不一**，投稿前须二选一并全书统一 |
| **A8-④** | Lee, S., Hwang, J., Jo, Y., & Han, S. (2025). *Wolfpack Adversarial Attack for Robust Multi-Agent Reinforcement Learning*. **ICML 2025（42nd）, PMLR 267, pp. 33025–33056**；UNIST | ✅ 即 WALL 的技术 antecedent。🔴 **旧描述"逐次攻陷智能体直到合作崩溃"比原文强**：摘要原句是 *targets an initial agent and its assisting agents to disrupt cooperation* → `01` §5 已按原文收紧，citation key 由 "Lee et al., 2025" 改为 **Lee, Hwang, Jo and Han (2025)**（避免与 A8-① 混淆） |
| **A8-⑤** | Ji, S., Li, Y., & Hooi, B. (2026). *Memory is Reconstructed, Not Retrieved: Graph Memory for LLM Agents*（MRAgent）. **ICML 2026**；arXiv `2606.06036` | ✅ 即 cue–tag–content 记忆图。⚠️ arXivlens 的 BibTeX 把 **Hooi 排第一**（字母序自动化产出）→ **著录必须用 arXiv 正式顺序 Ji, Li, Hooi**。→ `01` §4 已改 citation key |
| **A8-⑥** | Duan, W., Lu, J., & Xuan, J. (2025). *Bayesian Ego-graph Inference for Networked Multi-Agent Reinforcement Learning*（BayesG）. **NeurIPS 2025（38）**, DOI `10.52202/085713-2451`；arXiv `2509.16606`；UTS | ✅ 即 ego-graph + ELBO 机制来源。🔴 **它是网络 MARL 论文，不是教育论文** —— 我们借的是机制，**正文不得暗示它研究学习者**。→ `01` §4 已改 citation key 为 Duan, Lu and Xuan (2025) |
| **A8-⑦** | Chen, Y., Li, J., Xu, Y., Herrera-Viedma, E., Yu, H., & Sun, J. (2026). *A comprehensive survey of deep learning-based cognitive diagnosis models in education*. **Neurocomputing, 697, 134160**, DOI `10.1016/j.neucom.2026.134160`（online 2026-06-02） | ✅ **6 位作者**（Glasgow Enlighten 权威记录）。→ `13` §2.5 现有写法 "*Neurocomputing* 697:134160" **数字准确，无需改动** |
| **A8-⑧** | Schuetze, B. A., Yan, V. X., & Carvalho, P. F. (2025). *Capturing Session-to-Session Dynamics of Learning and Forgetting: Testing the Limits of Knowledge Tracing Models*. **International Journal of Artificial Intelligence in Education, 35, 3559–3578** | ✅ **两个数字全部逐字对上**：回顾拟合 AUC = BKT 0.79 / BKT-F 0.77 / AFM 0.74；时间交叉验证下高估 **AFM ~58% / BKT ~51% / BKT-F ~47%**。→ `13` §2.5 的 "AUC ≈ 0.74–0.79" 与 "47–58%" **均无需改动**（少见的一处我们写对了） |
| **A8-⑨** | An, M., McLaren, B. M., & Stamper, J. (2026). *Deceptive Overgeneralization: When Adaptive Learning Enables Systematic Misapplication*. **Journal of Computer Assisted Learning, 42(5)**, DOI `10.1002/jcal.70311`；Carnegie Mellon HCII | ✅ **三作 2026 JCAL 版才是 `13` §2.5 引的那篇**。🔴 **同组还有两篇同主题前置论文**（不可混）：An & Stamper (2025) AIED 2025, DOI `10.1007/978-3-031-98465-5_22`；An & Stamper (2025) EC-TEL 2025 Part I, pp. 3–17, DOI `10.1007/978-3-032-03870-8_1`。实证：11 实验 / N=192 / 麻将 ITS；do-not-act 首测错用率 61.5%–100%（BKT 基线 12%、new-KC 基线 40%） |
| **A8-⑩** | Yasir, T., Li, W., Gilson, S., Tithi, S. D., Tian, X., & Barnes, T. (2026). *Confirming Correct, Missing the Rest: LLM Tutoring Agents Struggle Where Feedback Matters Most*. **BEA 2026**（21st Workshop on Innovative Use of NLP for Building Educational Applications）, **pp. 819–840**, DOI `10.18653/v1/2026.bea-1.56`；ACL Anthology `2026.bea-1.56` | 🔴 **`13` §2.5 原文写的 venue 是错的**：旧写 "Yasir et al. (**AIED** 2026)" → 实为 **BEA 2026**（ACL 旗下 workshop，非 AIED）。**已改为 "(2026, BEA 2026)"**。我们使用的那句 "accurate diagnosis did not reliably produce pedagogically actionable feedback" 是摘要逐字句 ✅ |
| **A8-⑪** | Lee, U., Lee, S., Jeong, Y., Lee, E., Shin, M., & Kwon, H. (2026). *EduClaw-Bench: A Long-Horizon Benchmark for Pedagogical LLM Agents with Simulated Learners*. arXiv `2608.03206` | 🔴 **内部记录一度把它挂在 Boyapati 名下 —— 错**；真实作者是 **Unggi Lee 等 6 人**。关键设定：30 天 / 55 scenarios / KT-grounded simulated learner / ECE=0.049 / 自述 *negligible answer leakage* / 现场课堂 helpfulness 6.02 vs 模拟 6.19。→ `13` §2.5 已补真实作者。⚠️ **它是目前与我们方法最相近的一篇（KT + 模拟学习者 + 长程），建议在 §2.6 单独做一段对比** |
| **A8-⑫** | Boyapati, Y. M., Yu, C., Jiang, T., & Zhan, J. (2026). *Privacy-Preserving Heterogeneous Multi-LLM Federated Inference for Cognitive Diagnosis*. arXiv `2609.02947` | ✅ 这才是 §2.5 的"隐私维度"那条（ε-local DP + residual aggregation + honest-but-curious）。**Boyapati 与 A8-⑪ 是两篇不同论文，切勿再混淆** |
| **A8-(13)** | García, C. A., Recio-Colmenares, C. L., Recio-Colmenares, R. B., Mejia-Lucatero, E. F., & Fernández-Robles, J. L. (2026). *Integrating Generative AI for Personalized Learning in Cryptography Education: A Case Study With LLM-Driven Learning Activities*. In D. Bonilla Carranza, A. Peña Pérez Negrón, & M. Pérez-Cisneros (Eds.), *Interdisciplinary Approaches to Game Design in Healthcare and Education* (pp. **425–446**). IGI Global Scientific Publishing. DOI `10.4018/979-8-3373-4657-1.ch013` | 🔴 **旧录年份 "2024/2025" 是错的 → 实为 2026**；且它**自陈 exploratory design、无对照组**，结果为"初期下滑后趋稳"而非因果效应；样本为 Universidad de Guadalajara 本科 IH063 密码学课程、**八个学期 2022A–2025A**。→ `13` §2.4.4 与 `22` §7 已补作者并标"不主张因果" |
| **A8-(14)** | ✅ Al Foori, Y. K. H., & Oyelere, S. S. (2026). *AI-integrated interactive learning system for enhancing cybersecurity education*. **Frontiers in Computer Science, 8:1826732**. DOI `10.3389/fcomp.2026.1826732`（AI-CES）；University of Exeter | ✅ **2026-09-22 全文已读，身份完全确认**：期刊页明标 **ORIGINAL RESEARCH article**（**不是综述** —— 旧录称"综述"是错的）；开放获取（CC BY）。设计为 **design-and-development + cross-sectional**，n=30（10 讲师 + 20 学生），作者自陈 *"positioned as an exploratory pilot rather than as a controlled effectiveness trial"*、*"does not establish causal effects on learning outcomes"*，局限明写 *"without incorporating a control group or longitudinal pre and post-testing"*。→ `13` §2.4.4 已改为点明"原创研究、非综述"+ 逐字限定语。🔴 **旧文另有半句"并引用上述密码学子域 agent"——无从核证，已删（本轮唯一删掉的正文论断）** |
| **A8-(15)** | Tweed, R. G., & Lehman, D. R. (2002). *Learning considered within a cultural context: Confucian and Socratic approaches*. **American Psychologist, 57**(2), 89–99. DOI `10.1037/0003-066X.57.2.89`；PMID `11899565`；ERIC `EJ646499`；ISSN 0003-066X | ✅ **2026-09-22 新增，四源一致**（PubMed / ERIC / Ethnos Bibliography / Google Scholar；被引 ~1002）。**用途**：`13` §2.1 的苏格拉底–孔子对比框架，取代原先核不到的 C5（刘俊俊）。🔴 **方向纪律**：该文主旨是两传统的**差异**（Western exemplar = questioning & evaluating others' beliefs；Eastern exemplar = effortful, respectful, pragmatic acquisition），**不得用来支持"两传统趋同"**；§2.1 已据此把趋同限缩到**时机条件**（不愤不启／不悱不发）一项。 |

### 本轮小结：三类错误一次性暴露

1. **作者张冠李戴**（EduClaw→Boyapati）—— 若不核会直接写错条目。
2. **venue 说错**（Yasir：AIED→BEA）—— 审稿人一查即破。
3. **把"内部简称/内置描述"当检索词**（Socratic Mind / Wolfpack / cuetagcontent）—— 又踩了第五轮那条：**搜不到 ≠ 不存在**。

---

## A9 · 2026-09-22 第七轮：EEG “认知债”溯源 + 一条更强的新证据

| # | 著录 | 核验说明 |
|---|---|---|
| **A9-①** | Kosmyna, N., Hauptmann, E., Yuan, Y. T., Situ, J., Liao, X.-H., Beresnitzky, A. V., Braunstein, I., & Maes, P. (2025). *Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task*. **arXiv:2506.08872 [cs.AI]**. MIT Media Lab. （216 页；v1 2025-06-10，v2 2025-12-31） | ✅ **EEG “认知债”的原始出处**——此前仅从 Brender et al. (2026) 二手转引，`13` §2.7 第 1 项与 `07` 待办均指向此条。设计：三组（LLM / 搜索引擎 / 无工具），前三会话 N=54，第四会话交叉**仅 18 人**，为期四个月。摘要支持的表述：*"Brain connectivity **systematically scaled down** with the amount of external support"*; *"The reported ownership of LLM group's essays ... was low"*; *"The LLM group also fell behind in their ability to quote from the essays they wrote just minutes prior."* ⚠️ **原文未支持我们旧稿的“**reduced critical evaluation of model output**”**（属 Brender 转述）——已从 `13` §2.2 与 `07` §1.1 删除。🔴 **至今仍为预印本**（无 journal_ref / DOI），作者明示**未经同行评审**、结论应视为初步结果；样本来自波士顿地区五所高校。→ **不得单独承重本文因果链** |
| **A9-②** | Liu, G., Christian, B., Dumbalska, T., Bakker, M. A., & Dubey, R. (2026). *AI Assistance Reduces Persistence and Hurts Independent Performance*. **arXiv:2604.04721 [cs.AI]**. （v1 2026-04-06，v4 2026-08-05） | ✅ **本轮最重要的新增证据**：一系列随机对照试验 **N = 1,222**，任务含数学推理与阅读理解。发现：AI 辅助**提升短期表现**，但受试者**在无 AI 时显著变差、且更容易放弃**；效应在仅**约 10 分钟**接触后即出现。→ 这正是本文核心论点（“有辅助时的表现 ≠ 撤去辅助后的能力”）的**因果形式**：设计随机化、且在撤除辅助后测量。**已立即写入 `13` §2.2 与 `07` §1.1 承担**，取代 n=54 且未同行评审的 EEG 预印本 |

> ⚠️ **当心大众传播层**：媒体广为流传的“CHATGPT 让大脑萎缩 47%”是**误读**——MIT 测量的是**任务中的神经连接强度**，而非大脑结构的物理萎缩（见科普中国《你的大脑真的在被 AI “腐蚀”吗？》）。**本文不得采用该说法**。

---

## B. 元数据待补（⚠️ 提交前必须补齐，否则删引）

| 引用标签 | 已知信息 | 正文引用处 | 待补字段 |
|---|---|---|---|
| ~~Brender et al. (2026)~~ → **升入 A 组（元数据已齐）** | ✅ **2026-09-22 已核**：**7 位作者** Brender, J., El-Hamamsy, L., Uittenhove, K., Pérez, A., Jermann, P., Mondada, F., & Bumbacher, E.；Springer **LNCS, pp. 546–561**，DOI `10.1007/978-3-032-29763-1_37`。真题 *Reflective Dialogue or Prompt Refinement? Effects of Tutor Scaffolding on Students' Independent LLM Use for Programming*。66 人、6 周准实验 | §1.3 失败2、§1.4 支点、§2.2、§2.4.1、§5.2.1、§7.2 | ✅ 齐。🚫 **必须从正文删除 "AIED 2026 best paper"**（奖项不入任何书目库，不可核）；且其标题已明写 *Effects of Tutor Scaffolding* → §2.4.1 措辞须相应回退（不得写"没人研究过脚手架效应"） |
| ~~Suvernev et al. (2026)~~ → **升入 A 组** | ✅ 元数据已核：**4 位作者** Suvernev, B., Zhao, C., Wang, Z., & Chan, C.；**EDULEARN Proceedings 1**，DOI `10.21125/edulearn.2026.1345`；真题 *SOCRATICAI: ON TRAINING MODELS THAT MAKE STUDENTS THINK*；closed access（付费墙属实） | §1.5(2)、§2.3(d)、§2.4.1、§7.3.4 | 🔴 仅摘要 → 措辞须带"据其已公开摘要所述"；**不得写"该工作完全未涉及泄露度量"**（`07` 红线 10） |
| ~~Chudziak & Kostka (2025)~~ → **升入 A7-②** | ✅ 完整：AIED **2025** Part VI, pp. **462–469**, DOI `10.1007/978-3-031-98465-5_58`；Warsaw University of Technology。⚠️ **年份是 2025 不是 2026** | §1.4、§2.3(a)(c)、§2.4.2 | ✅ 齐 |
| ~~Lee et al. (2026)~~ → **升入 A8-①** | ✅ 已坐实：Lee, J., Yilmaz Soylu, M., Hung, J.-T., Grigoryan, G., Cui, C., & Forsyth, D.；AIED 2026, LNCS 16585 Part V, pp. 137–145, DOI `10.1007/978-3-032-29770-9_16` | §1.5(3)、§2.3(a) | ✅ 齐。⚠️ **另有 2024 Learning@Scale 同名系统的前置论文**（Hung, Cui, Popescu, Chatterjee & Starner, pp. 340–345），勿混 |
| ~~Thonge & Thakkar (2026)~~ → **升入 A7-①** | ✅ 完整：ITiCSE 2026, pp. **196–202**, DOI `10.1145/3803400.3809368`。🔴 **旧记录里的"有状态误解检测 / 多层校验 / questioning intensity"是我们自己的内部描述，不是该文标题或摘要里的任何一句话** | §1.4、§2.3(b)、§2.4.1 | ✅ 齐。🔴 **仅持有摘要** → 正文措辞已限到摘要强度（`13` §2.3(b)、§2.4.1 已改） |
| ~~Sunil & Thakkar (2025)~~ → **升入 A7-④** | ✅ Ashoka University；arXiv **2512.03501**；COMPUTE 2025 Best Practices Track | §1.3 失败1、§2.3(b)、§2.4.2 | ✅ 齐（按 preprint 处理）。🔴 **与 Thonge & Thakkar 同组（Ashoka）已由后者参考文献证实**，且**与 Suvernev 同名 SocraticAI 但不同组**（CityU），切勿混淆 |
| ~~Liu et al. (2024) SocraticLM~~ → **升入 A7-③** | ✅ 完整：NeurIPS **37**, pp. **85693–85721**, DOI `10.52202/079017-2721`；**8 位作者**齐全 | §2.3(a) | ✅ 齐。⚠️ 页码源为作者仓库自附 citation，投稿前再核一次 |
| IntelliCode (2025) | ✅ 已核：arXiv 2512.18669；**仅 2 位作者** Jones, D., & Ghosh, S.；自定位 **demo paper**；六智能体 + 集中 learner model；graduated hinting；**仅 simulated learners** | §2.3(c)、`00` 口径表 | ⚠️ 仅剩『是否已正式发表』。🚫 **证据层级偏低**：不可用它代表「学习者建模」整支文献 |
| SocraticPO (2026) | ✅ 已核：arXiv `2606.09887`；**11 位作者**（末位 Enhong Chen）；reward decay for assisted success（Theorem 1）；§5.4 承认泄露 | §1.4、§2.3(d)、§7.3.1 | ⚠️ 仅剩『是否已正式发表』。🔴 **领域曾被误读**：它是 **RL 策略优化**方法，student 是**被训练的策略网络**，不是人类学习者 → 措辞已回退 |
| Hazra et al. (2026) SafeTutors | arXiv **2603.17373**；11 模型、3,135 单轮 + 2,820 多轮；κ=0.76 | §1.3、§2.3 | 是否已发表于 AIED 2026 论文集 |
| ~~Udeshi et al. (2026)~~ | 🚫 **2026-09-22 已从全部英文正文撤引**（`07` §1.3、`13` §2.3、`13` §2.4.3、`14` §8.5） | ~~§1.3 失败1、§2.3、§2.4.3~~ → 承重由 **Zhao et al. (2026, ACL 2026)** 与 **Bastani et al. (2025, PNAS)** 接管 | 🚫 见 D3。**限定语救不了核不到的来源**：它进不了参考文献表 |
| ~~Kapur (2008)~~ → **升入 A8-②** | ✅ 已核（三源一致）：*Productive Failure*. **Cognition and Instruction, 26(3), 379–424**, DOI `10.1080/07370000802212669`；ERIC `EJ800999` | §3.1、§7.2 | ✅ 齐 |
| ~~Tishby et al. (2000) / Alemi et al. (2017)~~ → **升入 A8-③** | ✅ 已核：Alemi, A. A., Fischer, I., Dillon, J. V., & Murphy, K. (2017). *Deep Variational Information Bottleneck*. **ICLR 2017**; arXiv `1612.00410` | §3.2 | 🟡 **唯一遗留决策**：Alemi 自己引的是 **Tishby et al. (1999)**（Allerton 1999；arXiv `physics/0004057` = 2000 版），我们正文写「2000」 → 投稿前须二选一并全书统一 |
| ~~arXiv 2604.13006~~ → **元数据已齐** | ✅ *One Token Away from Collapse: The Fragility of Instruction-Tuned Helpfulness*；**Potraghloo, E. B., Azizi, S., Kundu, S., & Pedram, M.**（2026-04-14，v2 04-27）；约束诱导坍缩；7 模型 / 5 家族 / 7B–70B | §3.2、§4.2、§8.1 | ⚠️ 仅剩『是否已正式发表』。口径已改为**跨领域类比**而非同领域证据 |
| ~~Lee et al. (2025)~~ → **升入 A8-④** | ✅ 已坐实：Lee, S., Hwang, J., Jo, Y., & Han, S.；*Wolfpack Adversarial Attack for Robust MARL*；**ICML 2025, PMLR 267, pp. 33025–33056**；UNIST | §3.3 | ✅ 齐。🔴 **`01` §5 原文描述比原摘要强，已按原文收紧** |
| ~~Ji et al. (2026)~~ → **升入 A8-⑤** | ✅ 已坐实：Ji, S., Li, Y., & Hooi, B.；*Memory is Reconstructed, Not Retrieved: Graph Memory for LLM Agents*；**ICML 2026**；arXiv `2606.06036` | §3.4 | ✅ 齐。⚠️ **著录须用 Ji, Li, Hooi 顺序**（部分 BibTeX 按字母序把 Hooi 排第一，那是自动产出错误） |
| ~~Duan et al. (2025)~~ → **升入 A8-⑥** | ✅ 已坐实：Duan, W., Lu, J., & Xuan, J.；*Bayesian Ego-graph Inference for Networked MARL*（BayesG）；**NeurIPS 2025（38）**, DOI `10.52202/085713-2451`；arXiv `2509.16606`；UTS | §3.5 | ✅ 齐。🔴 **它是网络 MARL 论文不是教育论文**，我们只借机制，正文不得暗示它研究学习者 |
| ~~Chen et al. (2026)~~ → **升入 A8-⑦** | ✅ 已核：Chen, Y., Li, J., Xu, Y., Herrera-Viedma, E., Yu, H., & Sun, J.；*A comprehensive survey of deep learning-based cognitive diagnosis models in education*；**Neurocomputing, 697, 134160**, DOI `10.1016/j.neucom.2026.134160` | §2.5 | ✅ 齐（**6 位作者**） |
| ~~Schuetze, Yan & Carvalho (2025)~~ → **升入 A8-⑧** | ✅ 已核：Schuetze, B. A., Yan, V. X., & Carvalho, P. F.；*Capturing Session-to-Session Dynamics of Learning and Forgetting*；**Int. J. Artif. Intell. Educ. 35, 3559–3578** | §2.5 | ✅ 齐。**两个数字全部逐字命中**（AUC 0.74–0.79；高估 AFM 58% / BKT 51% / BKT-F 47%）→ 正文无需改动 |
| ~~An, McLaren & Stamper (2026)~~ → **升入 A8-⑨** | ✅ 已坐实：An, M., McLaren, B. M., & Stamper, J.；*Deceptive Overgeneralization: When Adaptive Learning Enables Systematic Misapplication*；**J. Computer Assisted Learning, 42(5)**, DOI `10.1002/jcal.70311`；CMU HCII | §2.5 | ✅ 齐。🔴 **同组另有两篇同主题前置论文**（AIED 2025 / EC-TEL 2025，均 **An & Stamper 两人**），**不得互相替代** |
| ~~Yasir et al. (2026 / AIED 2026)~~ → **升入 A8-⑩** | ✅ 已坐实：Yasir, T., Li, W., Gilson, S., Tithi, S. D., Tian, X., & Barnes, T.；*Confirming Correct, Missing the Rest*；**BEA 2026, pp. 819–840**, DOI `10.18653/v1/2026.bea-1.56` | §2.5 | ✅ 齐。🔴 **venue 曾被写错**：旧写「AIED 2026」→ 实为 **BEA 2026（ACL 旗下 workshop）**，`13` §2.5 已改 |
| ~~EduClaw-Bench (2026) / Boyapati et al. (2026)~~ → **升入 A8-⑪ / A8-⑫** | ✅ 已坐实，且**内部记录曾把两者混为一条**：EduClaw-Bench = **Lee, U., Lee, S., Jeong, Y., Lee, E., Shin, M., & Kwon, H.**, arXiv `2608.03206`；隐私维度 = **Boyapati, Y. M., Yu, C., Jiang, T., & Zhan, J.**, arXiv `2609.02947` | §2.5 | ✅ 齐。⚠️ **EduClaw 是目前与我们方法最相近的一篇**（KT + 模拟学习者 + 30 天长程），建议 §2.6 单列对比 |
| ~~Asanov & Degen (2025)~~ → **作者顺序已更正** | ✅ **Degen, P.-B., & Asanov, I.**（arXiv 2508.05116 记录 first=Degen, last=Asanov）；65 名德国师范生；因变量为**自陈感知**非学习结局 | §1.5(3) | ⚠️ 仅剩『是否已正式发表』。🚫 **不得当作有效性证据** |
| ~~K-12 RCT (2026)~~ → **升入 A7-⑤** | ✅ 已定位作者与出处：**Kao, S., Grant, P., & Woltering, S.**（Texas A&M University）；90 名十年级；三臂 RCT；逐字句 *"Effects on metacognitive self-regulation were nonsignificant."* | §1.3 失败3 | ✅ 齐。🔴 **但它是 Research Square 预印本（DOI `10.21203/rs.3.rs-8118546/v1`），未见同行评审版本** → 正文一律须标 **preprint** |
| ~~IGI Global (2024/2025) 章节~~ → **升入 A8-(13)** | ✅ 已坐实：**García, C. A., Recio-Colmenares, C. L., Recio-Colmenares, R. B., Mejia-Lucatero, E. F., & Fernández-Robles, J. L. (2026)**；*Interdisciplinary Approaches to Game Design in Healthcare and Education* (Bonilla Carranza, Peña Pérez Negrón & Pérez-Cisneros, Eds.), **pp. 425–446**；DOI `10.4018/979-8-3373-4657-1.ch013` | §2.4.4、§7.3.2 | ✅ 齐。🔴 **旧录年份「2024/2025」是错的 → 实为 2026**；自陈 exploratory、**无对照组** → 正文已标「不主张因果」 |
| *Frontiers in Computer Science* (2026) → **见 A8-(14)** | 🟡 **候选人之一**：Al Foori, Y. K. H., & Oyelere, S. S. (2026). *AI-integrated interactive learning system for enhancing cybersecurity education*（AI-CES）. **Front. Comput. Sci. 8**, DOI `10.3389/fcomp.2026.1826732` | §2.4.4 | ⚠️ **身份未完全确认**：旧录称「综述」，命中记录为**原创系统论文 + n=30 试点**。🔴 旧文那句『并引用上述密码学子域 agent』**无从核证，已删** |

### ★ B 组 2026-09-22 核验状态更新（按 `26` 四库核验结果归位）

| 标签 | 更新后状态 | 动作 |
|---|---|---|
| **Brender (2026)** / **Suvernev (2026)** | ✅ **已升入 A 组**（见上） | 从 B 组移出 |
| **Asanov & Degen (2025)** | ✅ 作者顺序**更正为 Degen, P.-B., & Asanov, I.**（arXiv 2508.05116 记录 first=Degen, last=Asanov）；真题 *Beyond Automation: Socratic AI, Epistemic Agency…*；65 名德国师范生 | 改作者顺序。⚠️ 因变量为**自陈感知**，非学习结局 → **不得当作有效性证据** |
| **SocraticPO (2026)** | ✅ arXiv `2606.09887`；**11 位作者**（末位 Enhong Chen）；**预印本** | 🔴 **领域被误读须改**（见 `26` §1.3④）：它是 **RL 策略优化**方法，student 是**被训练的策略网络**，不是人类学习者 → §2.3(d) / §7.3.2 措辞须回退；**不得以"其全文无 telling@N"充当 gap 证据** |
| **IntelliCode (2025)** | ✅ arXiv `2512.18669`；**仅 2 位作者**（Jones, D., & Ghosh, S.）；**自定位为 demo paper** | ⚠️ 以它代表"学习者建模"整支，**证据层级偏低**，措辞须相应收敛 |
| **Hazra et al. (2026) SafeTutors** | ✅ arXiv `2603.17373`；**8 位作者**（含 Stoyanovich, Pechenizkiy）；**预印本未正式发表**；`17.7% → 77.8%` **摘要逐字命中** | 否已发表于 AIED 2026 论文集；可补 11 harm 维度 / 48 子风险 |
| **arXiv 2604.13006** | ✅ 真题 *One Token Away from Collapse: The Fragility of Instruction-Tuned Helpfulness*；**Potraghloo, E. B., Azizi, S., Kundu, S., & Pedram, M.**（2026-04-14，v2 04-27） | 元数据已齐。⚠️ **口径已改**：跨领域**类比**而非证据（见 A0 第 1 条，已修正） |
| **Thonge & Thakkar (2026)** | ✅ **2026-09-22 第五轮：不是撤引，是不该被判死刑**（详见 A0 修订后的结案表与 A7-①）。真实著录已坐实：ITiCSE 2026, pp. 196–202, DOI `10.1145/3803400.3809368` | 🔴 **旧的"从 §1.4 / §2.3(b) / §2.4.1 全部撤引"这条处置作废** —— 若照它执行，会删掉一条真实且与 §2.3(b) 高度贴合的 ITiCSE 论文。改为：**保留引用 + 把措辞降到摘要强度**（`13` §2.3(b)、§2.4.1 已执行） |
| **Udeshi et al. (2026)** | ✅ **2026-09-22 已撤**（四条悬案里唯一真撤的一条） | `07` §1.3 / `13` §2.3 / `13` §2.4.3 / `14` §8.5 **全部清除**；承重由 Zhao et al. (2026, ACL 2026) 与 Bastani et al. (2025, PNAS) 接管；D3 由 🔴 升 **🚫 禁引** |
| **Chudziak & Kostka (2025)** | ✅ **已定位**（A7-②）：AIED 2025 Part VI, pp. 462–469, DOI `10.1007/978-3-031-98465-5_58` | 🚫 旧的"由 `refs/` PDF 人工抄录"待办**作废**（`_refs/` 里其实只有 ED537206 一份 PDF，从来抄不了）。且它比我们以为的更有用：**其摘要自陈在 MathDial 上把 `Telling@N` 压低**，正合 §2.4.2 |
| **SocraticLM (Liu et al., 2024)** | ✅ **已定位**（A7-③）：NeurIPS 37, pp. 85693–85721，**8 位作者** | 🚫 "由 `refs/` PDF 补齐"待办同样作废。🔴 新纪律：**不得与 SocraticPO (2026) 合并著录** —— 同末位作者 Enhong Chen、同属 USTC 体系，但年份与 venue 都不同 |
| **K-12 RCT (2026)** | ✅ **已定位**（A7-⑤）：**Kao, Grant & Woltering**（Texas A&M），Research Square 预印本 | 🔴 关键句逐字命中，所以**论据可以留**；但它**不是同行评审文献**，正文必须标 preprint，不能当作"已发表 RCT"来抬论证强度 |
| **Sunil & Thakkar (2025)** | ✅ **已核**：arXiv **2512.03501**（2025-12-03），comment 自陈 *Presented in the Best Practices Track of COMPUTE 2025* | 见 A7-④。⚠️ 若做正式条目应取 COMPUTE 2025 正式版；取得前标 preprint。**它与 Thonge & Thakkar 的同组关系已由后者的参考文献列表直接证实** |

> ⚠️ **一类必须区分的同名/同组文献（已踩过）**：
> - **Baker 2004 有两篇**：CHI '04（Baker, Corbett, Koedinger **& Wagner**，pp. 383–390，= A5-e）与 ITS 2004（Baker, Corbett & Koedinger，LNCS 3220:531–540，= `12` D10）。**同年两篇不同论文，不是同一篇的两个版本**，可并存。
> - **Aleven 有 2003 / 2004 / 2016 三篇**：2003 RER 综述（= A5-d，本文用作权威综述）、2004 ITS（`12` D11）、2016 IJAIED（Help Tutor）。**不得合并著录**。
> - **Suvernev 与 Sunil & Thakkar 都涉及 "SocraticAI" 字样但为不同组**，勿混。
> - 🔴 **三方同名 "Socratic AI"（2026-09-22 新增，此前只辨析了两方）**：① **Thonge & Thakkar (2026, ITiCSE)** 的 *Socratic AI*（VS Code 集成，摘要逐字 *constrained to withhold direct solutions*）；② **Sunil & Thakkar (2025, arXiv 2512.03501)** 的同名系统（输入侧校验）—— ①与②**同组（Ashoka University, Aalok Thakkar）**，且 ① 的参考文献含 ②；③ **Suvernev et al. (2026, EDULEARN)** 的 *SOCRATICAI*（CityU HK，训练 hint 模型）—— 与 ①② **无关**。
>   ⚠️ 还有第四处易混：**Degen & Asanov (2025)** 真题含 "Socratic AI" 字样（*Beyond Automation: Socratic AI, Epistemic Agency…*），是**师范生自陈感知**研究，与上述机制类工作不是一回事。
>   **著录纪律**：正文出现 "Socratic AI" 时必须**带作者年份消歧**，不得裸用系统名。
> - **Kao, Grant & Woltering (2026) ≠ Bastani et al. (2025) ≠ Kestin et al.**：三篇都做过 RCT / 准实验，勿互指。
> - **Macina ≠ Mačina**：首作者正确拼写为 **Mačina**（已在 A3 修正）。

---

## C. 中文文献（2026-09-22 全条核验；🔴 两条核不到，不得入表）

> 🔴 **本轮最重要的发现：本组七条的**旧录标题几乎全是错的**——我们此前按“功能描述”记下的篇名，与实际篇名无一相同。
> 教训与英文条目完全一致（`MEMORY` §5）：**内部描述 ≠ 篇名**，按内部描述检索必然查不到，进而误判“该文不存在”。
> 双语格式：先中文原版，后英文译名（*English translation*）。

| # | 状态 | 中文著录（已核） | English rendering | 正文引用 | 核验说明与旧录更正 |
|---|---|---|---|---|---|
| C1 | ✅ 已核 | 孙立会, 许丰年 (2026). 生成式人工智能之于教育的过量肯定风险及其规避. *现代教育技术*, **36**(4), 5–14. | Sun, L., & Xu, F. (2026). The risk of excessive affirmation in generative AI for education and its avoidance. *Modern Educational Technology*, **36**(4), 5–14. | §2.2 | 旧录标题「「过量肯定」与生成式人工智能的教育隐忧」**不存在**；作者记 1 人，实为 **2 人**。来源：期刊官网目次（2026 年 04 期 v.36; No.300, 5-14 页）+杂志社公众号引文格式。作者单位：中央民族大学教育学院。★ **内容与本文直接同向**：三条表征——解疑答惑中的过分认同、资源推荐中的绩效导向、表现评价中的唯标准论；并实引 Walczak 例（向 ChatGPT 4.0 追问“这不是真的”即不断承认错误）与 Tassoti 例（首次答对、追问后编造事实） |
| C2 | ✅ 已核 | 李晶晶, 王天健 (2026). 教育应对生成式人工智能的四维倾向及其超越. *河北大学学报（哲学社会科学版）*, **51**(3), 108–119. | Li, J., & Wang, T. (2026). Four orientations in education's response to generative AI and their transcendence. *Journal of Hebei University (Philosophy and Social Science)*, **51**(3), 108–119. | §2.2 | 旧录标题「人工智能依赖与认知禁锢」**不存在**；作者少记一人。来源：学报 2026 年第 3 期目次（第 51 卷第 3 期）。🔴 **术语撞词预警**：该文四维框架中的“规避”对应英文正是 **Circumvention**，与本文论的 *circumvention of leakage*（绕过泄露措施）撞词但含义完全不同（它指对技术的节制性使用）—— **引用时必须区分，否则审稿人会读混**。李晶晶：北京师范大学未来教育学院博士生，广东开放大学副教授 |
| C3 | ✅ 已核 | 王一岩, 朱陶, 杨淑豪, 等 (2024). 人机协同教学：动因、本质与挑战. *电化教育研究*, **45**(8), 51–57. | Wang, Y., Zhu, T., Yang, S., et al. (2024). Human–machine collaborative teaching: Motivations, essence and challenges. *e-Education Research*, **45**(8), 51–57. | §2.2 | 旧录标题「师—机—生三元结构中的智能体定位」**不存在**（系内容概括）。★ **王一岩同主题多篇，禁合并著录**：人机协同学习：实践逻辑与典型模式（开放教育研究 30(1), 65–72, 与刘涇、郑永和）；对话式人机协同学习（中国电化教育 2024(11), 21–27）；智能时代的人机协同学习（中国电化教育 2022(9), 90–97） |
| C4 | 🔴 核不到 | ~~胡晓红 (2026). "AI+"政策与能力为本的课堂转向. [刊名待核].~~ | ~~Hu, X. (2026). "AI+" policy instruments and the shift to capability-oriented classroom practice. [journal TBD].~~ | §2.2、§7.4 | 🔴 **两轮检索（标题词 + 作者 + 主题）均未命中**。推测为内部杜撰或记录失真。→ `13` §2.2 已把该处改为**不署个人名的政策背景陈述**（“从知识传授转向能力提升为本是既定国家方向，我们遵循而非论证”）。**投稿前必须换成可核的政策文件**（如教育部等五部门《“人工智能+教育”行动计划》）或删除 |
| C5 | ✅ **2026-09-22 已闭合（结论：不替换成另一条中文二手源，改用一手文献）** | ~~刘俊俊 (2026). 苏格拉底与孔子对话传统比较. *教育研究与实验*.~~ → **永久删除** | — | §2.1 | 🔴 两轮检索（作者+主题、期刊+主题、产婆术+作者）**均未命中**，不得入表。<br>✅ **处置**：§2.1 论的是《论语》**7.8 的时机条件**，该章原文即为充分依据 —— 原文已逐字核（"子曰：不愤不启，不悱不发。举一隅不以三隅反，则不复也。"，**述而第七之第八章**，章次经多源一致）。**二手转述在此本就不必要**。<br>✅ 另补一条**可核的英文对比框架文献**：**Tweed, R. G., & Lehman, D. R. (2002)**, *American Psychologist*, **57**(2), 89–99, DOI `10.1037/0003-066X.57.2.89`, PMID 11899565（见 A8-(15)）。🔴 **并据此把"趋同"限缩为"时机条件趋同"** —— 该文主旨恰是两传统的**差异**（苏格拉底＝诘问／孔子＝勉力获知），拿它支持"趋同"即属措辞强于原文。 |
| C6 | ✅ 已核 | 熊晓莉, 周维, 艾洁 (2026). AI赋能基础教育教师教学技能培训智能体设计与开发. *渭南师范学院学报*, **41**(5), 41–48. | Xiong, X., Zhou, W., & Ai, J. (2026). Design and development of an AI-enabled agent for basic-education teachers' teaching-skill training. *Journal of Weinan Normal University*, **41**(5), 41–48. | §2.5 | 旧录标题「教师实训诊断—训练—反馈—优化闭环」是**内容概括**，非篇名；作者记 1 人，实为 3 人。系统名**“WEI 师”**。单位：渭南师范学院教育科学学院；陕西理工大学教师教育学院。基金：陕西省教师教育改革与教师发展研究项目 SJS2025YB091 等 |
| C7 | ✅ 已核（页码待核） | 王常吉, 甘庆晴, 刘宁, 刘珍 (2025). 基于生成式人工智能的密码学教学新模式. *计算机教育*, 2025(9), 159–164. ISSN 1672-5913 | Wang, C., Gan, Q., Liu, N., & Liu, Z. (2025). A new model for cryptography teaching based on generative artificial intelligence. *Computer Education*, 2025(9), 159–164. | §2.4.4 | 旧录缺作者、年份。单位：广东外语外贸大学信息科学与技术学院 / 数据安全治理与隐私计算广东省工程研究中心。⚠️ **页码据该期目次推定**（本文起始页 159，下一篇起始 165），投稿前请核一次 CNKI 引文格式。🔴 **同名陷阱**：另有**一篇完全同名**的论文（ArtTech Press, *TACS*, DOI `10.61369/TACS.2025140007`，作者 周婉祎 / 孙敏杰 / 赵苗苗）——引用时必须带刊名+年份区分。★ **内容要点**：以 **ECC 椭圆曲线加密**为案例，含 GAI 生成的 **CTF 挑战**；评估为**问卷调查**（81 名学生、有效 76 份），报告的是满意度与主观感受，**不是学习成效** → 它**不能**作为“GAI 提升密码学学习效果”的证据，而恰恰是本文论点的一个实例 |

| C8 | 🟡 待核（**未进正文，不阻塞**） | 高琳琦 (2023). *[篇名待核]* —— 个性化学习三步「构造提示→生成推荐→结果评价」 | — | **未进正文**；仅见于内部立项稿 `FEDC投稿_引导式多智能体_深度研究报告.md` 第 6 条 | 🟡 **2026-09-22 清点内部稿时发现此条此前未被收录**。因其从未进正文，暂不处理；**若将来要写入，必须回原文核篇名与卷期页**。 |

🔴 **C6 的引用纪律**（`13` §2.5 已写）：该文诊断的是**教师**的教学设计与授课表现，SAGE 诊断的是**学生**知识点；机制可类比，**主体不同，不得混谈**。

🔴 **C2 的术语纪律**（本轮新增，已同步到 `13`）：该文的“规避”对应英文 **Circumvention**，与本文的 *circumvention of leakage* 撞词而意义不同；引用时必须显式区分。

---

## D. 🚫 禁引与高危项

| # | 项 | 状态 | 处置 |
|---|---|---|---|
| D1 | **AIED 2026 research-gap synthesis**（"whether particular educational designs produce durable benefits, for whom, through which mechanisms…"） | 🚫 **出处已撤回**：实为某第三方 AI 生成教育知识库，非 AIED 2026 官方文件 | **已从 `07` §1.4 与 §1.5(1) 全部移除**，改挂 Weidlich et al. (2025)（A1）。`10` 已向导师书面更正。**任何位置不得再出现** |
| D2 | EEG「cognitive debt」研究 | 🔴 **二次引用**（现经 Brender et al. 2026 §1.1 转引） | 须溯源原文；**二次引用在 FEDC 审稿中难以存活**。若无法取得，删除该论据 |
| D3 | Udeshi et al. (2026) | 🚫 **禁引 —— 2026-09-22 已从所有英文正文撤下**（原为 🔴 仅会议纪要转述） | ✅ 已执行：`07` §1.3 / `13` §2.3 / `13` §2.4.3 / `14` §8.5。**取得可独立核验的原文前不得恢复** —— 限定语救不了四库核不到的来源：它无法进入参考文献表 |
| D4 | Suvernev et al. (2026) | 🔴 仅摘要（IATED 付费墙） | 一律带"据其已公开摘要所述"；**不得写"该工作完全未涉及泄露度量"**（`07` 红线 10） |
| D5 | 一切"无一／首创／首个"类断言 | 🚫 | 见 `07` 红线 3/4/6/13；本轮已清掉 `01` 附段的三处 "the first" |

---

## Honest-status notes（本附录自身的状态）

| # | 项 | 状态 |
|---|---|---|
| 1 | 本轮联网核真 | ✅ 6 条（A1–A5 + A6 五篇 FEDC）；其中 **A5 系回原文 PDF 逐字核验**，非二手摘要 |
| 1b | 2026-09-22 第二轮回源核验（B0③ NLP 主线；该组现共 **7 条**，TutorRL 见 2c、Puech 见 2e） | ✅ **5 条（第二轮的 5 条）**：STAP 见 ACM DL（ISAIE '25, pp. 584–587，全文免费）；ScaffoldLM / BEA 见 ACL Anthology（pp. 7165–7188 / 118–140）；EduDial / ToST 见 arXiv abs。**页数已补齐**；🔴 措辞仍据公开摘要与可访问章节 → 投稿前取 PDF 全文复核 |
| 1c | **2026-09-22 第五轮「悬案结案」（A7 五条）** | ✅ **四条原判"四库核不到"里，三条救回来了、一条真撤**：Thonge & Thakkar = *A Good Rubber Duck Does Not Quack…*（ITiCSE 2026, pp. 196–202）；Chudziak & Kostka = *AI-Powered Math Tutoring…*（AIED **2025** Part VI, pp. 462–469）；SocraticLM = NeurIPS 37, pp. 85693–85721（8 作者）；Sunil & Thakkar = arXiv 2512.03501；**Kao, Grant & Woltering (2026)** = §1.3 失败模式③ 的真实身份（Research Square 预印本）。🚫 **只有 Udeshi 真撤**。→ 见下方「防止误撤的检索纪律」 |
| 1d | **2026-09-22 第六/第七轮「B 组总攻」（A8 十四条）** | ✅ **剩余待补条目全部坐实，B 组元数据缺口清零**。同时挖出 **三处必须改正文的事实错误**：① **Yasir et al. 的 venue 写错**（旧写 AIED 2026 → 实为 **BEA 2026**，ACL 旗下 workshop）；② **IGI Global 章节年份写错**（旧写 2024/2025 → 实为 **2026**）；③ **EduClaw-Bench 作者张冠李戴**（旧挂在 Boyapati 名下 → 实为 **Unggi Lee 等 6 人**）。另有 **一处身份改判**：*Frontiers in Computer Science* 那篇不是「综述」，是 **ORIGINAL RESEARCH**（A8-(14)，全文已读）。→ 见 A8 表 |
| 1e | **2026-09-22 第八轮「摘要逐字 + 污染源铲除」** | ✅ Thonge & Thakkar **摘要逐字取得**（46 词，OpenAlex 出版方元数据），据此**证伪三条内部杜撰**（"stateful misconception detection" / "questioning intensity" / "**48 名学生部署**"）；并把这些杜撰**从其滋生处铲掉**——`00` §3.1 口径表、`06` 精读、`FEDC` 深度报告（三处均留更正留痕）。🔴 **这是本轮最值钱的动作**：先前只改了 `13` 正文，杜撰仍留在**口径文件**里，随时会被重新抄回论文。另：`13` §2.3(b) 的归类此前建立在**我们自己的推断**上（"约束由周边工具承载"），摘要并不支持 → 已显式标为**未证实的暂定归类** |
| 2 | 核验中发现的一处**必须改正文**的事实 | A4（Mukherjee）：其评估为问卷式感知有效性、**实证验证自述为未来工作** → `22` §7.3.2 与 `13` §2.4.4 须按此改写（见下"待办"） |
| 2b | **2026-09-22 第二轮核真：第二处必须改正文的事实（本轮最重要）** | **A5-b（Bastani）**：① 正文原写"随机化约 1000 名**学生**"，实为**按班级随机化**（约 50 个班 / 近 1000 人 / 4×90 分钟 / **honors 班排除**）；② GPT Tutor 的护栏**全在提示词层**，且**同时注入教师给的正确解法与常见错误反馈** → guarded 组相对 unguarded 组变了**三样**（引导 / 不给答案 / **反馈正确性**）而非两样。已改 `13` §2.2・§2.4.3・§2.6 ＋ `22` §7 ＋ `14` §8.4 **共 5 处**。另核到该文有 **correction（2025-08-20）**，逐字核对为**仅改 affiliation** → **不影响任何数字，正文无需标注** |
| 2c | 🔴 **2026-09-22 第三轮：挖出一条漏掉的、且直接证伪旧断言的先例** | **TutorRL** (Dinucu-Jianu et al., **2025, EMNLP**, pp. 272–292, ETH Zürich / UKP)。由 **ScaffoldLM 全文的参考文献反查**挖出（ScaffoldLM 的泄露协议即沿用其 released testing data）。**全文已取到**（21 页 PDF）。
   → 它**已经**做了我们 §2.4.2 声称无人做的事：连续可调 λ + 三条响应曲线（∆Solve rate / Leak Solution % / Ped-RM vs λ）+ **Pareto 前沿**。
   → 已改 **6 处**：`13` §2.3.1（Five→**Six items**，新增该条）、§2.3(d)（训练层**最强成员**，并明写"二值 vs 分级"差异轴在训练层**已不存在**）、§2.4.2（**撤回**旧加粗断言，收窄为"分级约束 + 持久结果 + 通道分解"三者同时具备）、§2.3.1 收尾、`07` §1.4 (ii) 与 §1.4 HeuristicEdu 段、`22` §7.3.1 两处。
   🚫 **全局禁令**：不得再写"无人刻画泄露—强度关系""no existing system varies a constraint and plots the response"。残存差异只有两条：其结果为**对话后即时解题率**（非撤除后），且 λ 使两目标**沿前沿一起移动**（权衡刻画 ≠ 增益分解） |
| 2d | ✅ **2026-09-22 同轮：ScaffoldLM / BEA 全文逐字复核** | 两份 PDF 均已取到（24 页 / 23 页）。**措辞与原文一致，无需降级**：ScaffoldLM 的 "assessment-driven control loop that infers the learners cognitive state, evaluates whether the current step target is met, and adaptively selects tutoring actions" 逐字属实（作者 **Zechen Li, Qiannan Zhu, Mei Wang, Jia Li, Hua Huang**，**北京师范大学**）；BEA 的 "guiding students without revealing final answers"、"competitive with a strong proprietary baseline"、"challenges in reliably evaluating tutoring quality" 均逐字属实。
   ⚠️ **两处此前未写进正文的事实已补入**
| 1f | **2026-09-22 第九轮「C 组中文文献攻坚 + EEG 溯源」** | ✅ **C 组七条全部核完**。🔴 **四条此前标题/作者是错的**（与英文条目同一老毛病：拿"功能描述"当篇名）：C1 实为**孙立会、许丰年**两人《生成式人工智能之于教育的过量肯定风险及其规避》；C2 实为**李晶晶、王天健**《教育应对生成式人工智能的四维倾向及其超越》；C3 实为《人机协同教学：动因、本质与挑战》；C6 实为三人《AI 赋能基础教育教师教学技能培训智能体设计与开发》。C7 补齐为**王常吉等，《计算机教育》2025(9): 159–164**。⚠️ **引申纪律**：C2 的"规避"对应英文正是 **Circumvention**，与本文 *circumvention of leakage* 撞词但含义不同，**引用时必须显式区分**；C7 **同标题论文有两篇**（另一篇在 ArtTech Press），引用须带刊名+年份。🔴 **C4（胡晓红）、C5（刘俊俊）两轮检索均核不到** → 不得进正式文献表；C4 的个人归属已从 `13` §2.2 删除（改为不署名的政策背景陈述）。**EEG「认知债」已溯源到原文**：Kosmyna et al. (2025), arXiv:2506.08872, MIT Media Lab（**A9-①**）。🔴 **溯源暴露我们自己的措辞比原文强**：旧稿的 "reduced critical evaluation of model output" 在原文摘要中**无据**（属 Brender 二手转述），已从 `13` §2.2 与 `07` §1.1 删除。★ **同时挖到一条更强的新证据**：Liu et al. (2026), arXiv:2604.04721, **RCT, N = 1,222**，其设计与结论（有辅助时更好、撤除后更差且更易放弃，约 10 分钟即出现）**恰是本文核心论点的因果形式** → 承重已从 n=54 的 EEG 预印本转移到它（**A9-②**） |
：① ScaffoldLM **确实报了泄露指标**（∆Solve Rate + **Leaked Solution (%)**）；② BEA 的 **"Revealing Answer" 是加权 DPO 目标里的一个显式维度（权重 1，与 Factuality / Mistake Identification / Targetedness 同权，Clarity 为 0.5）** | A5（Goldin）：87% 是"最可能的下一步动作"，非"87% 的学习者都会" → `21` §4.3 / `22` §7.2 已改准 |
| 4 | ⚠️ 待补元数据的条目数 | ✅ **B 组缺口已清零**（见 1d）；**C 组七条已全部核完**——五条补齐卷期页（五条中四条此前标题/作者记错），**两条核不到不得入表**（见 1f）。🔴 **唯一残留：C7 页码据该期目次推定**（本文起始页 159、下一篇 165），投稿前建议核一次 CNKI 引文格式 |
| 5 | 🔴 仅摘要 / 二手 | **2 条正文来源**（Suvernev / **Thonge & Thakkar**）—— ~~EEG~~ 已于 2026-09-22 溯源到原文（Kosmyna et al., 2025），但该文至今仍**未经同行评审**且交叉对照仅 18/54 人，因此**不单独承重**（见 A9-① 与 1f）**＋ B0③ 中仅剩的两条无全文**（**STAP**：四通道封闭；**ToST**：arXiv PDF 端点 SSL 拒连）→ 措辞只可停在摘要强度。**ScaffoldLM / BEA / TutorRL / Puech / EduDial 的全文均已取到并逐字复核**（2026-09-22 第四轮），措辞已回原文对齐。~~Udeshi~~ 已转 🚫 禁引（见第 6 行） |
| 6 | 🚫 禁引 | **2 条**：① AIED 2026 research-gap synthesis；② **Udeshi et al. (2026, Khanmigo)**（四库核不到）—— 均已从正文清除，**勿再引入** |
| 7 | 待办（下一步，按阻塞程度排序） | ✅ **原 A 类两条均已解决**：~~C 组卷期页~~ → 已补齐（五条）；~~EEG 溯源~~ → 已溯到原文（并顺带回一条更强的 RCT）。✅ **原唯一阻塞项已闭合（2026-09-22）**：~~C4（胡晓红）与 C5（刘俊俊）核不到~~ → **C5 不替换成另一条中文二手源，改引一手文献**（《论语》7.8 原文，章次已核）**＋可核的 Tweed & Lehman (2002)**，见 A8-(15)；**C4 的个人归属已从 `13` §2.2 删除**（改为不署名的政策背景陈述）。⚠️ **残留**：内部稿 `FEDC投稿_引导式多智能体_深度研究报告.md` L59 仍以"胡晓红 2026"作政策依据 —— 该文**不属论文正文**，已就地标注待换可核政策文件。<br>🟡 **B 类（等价可选，不阻塞）**：③ **Thonge & Thakkar ACM 全文**——只影响 §2.3(b) 的**归类**能否从"暂定"改为"已证实"，以及第 21 条理据能否恢复（现由 Baker 2004 CHI + Aleven 2003 RER + Goldin 2012 顶上）；④ 5 条预印本的**正式发表状态**（等 venue 公布，按 preprint 著录不阻塞）。<br>✅ **已完成**：~~按 A4 改写 `22` §7.3.2 与 `13` §2.4.4~~；~~EEG 溯源~~（文献已补 + 承重转移；`13` §2.2 / §2.7 第 1、6 项、`07` §1.1 与待办清单、`14` §8.5 共 8 处已改）；~~C 组卷期页~~；~~逐条补 B 组元数据~~（**缺口已清零**）；~~K-12 RCT 补作者~~（A7-⑤）；~~Udeshi 处置~~（撤引 + 承重转移）。<br>**内容增强待办（非核验类）**：⑤ **EduClaw-Bench 在 §2.6 单列一段对比**——它是目前已核文献中**与我们方法最相近的一篇**（KT-grounded 模拟学习者 + 30 天长程 + 自陈 negligible leakage），不单独对比会显得我们没看见它 |

---

## ★ 可复用的核验方法（本轮实证有效）

1. **承重的引用必须回原文，不靠二手摘要。** 本轮对 Goldin 2012 的做法：搜索只拿到摘要（摘要里**没有** 87%/88%）→
   用 `files.eric.ed.gov/fulltext/<ERIC号>.pdf` 直接抓 PDF → PyMuPDF 取文本 → 正则定位数字并打印上下文。
   **结论：数字属实，但我们的措辞比原文强一档** → 两处正文已改准。若只查摘要就会得出"数字无法证实"的错误结论，也可能反过来误删真引用。
2. **核验结果要回写正文，不只写进附录。** 本轮核验直接改了 `21` §4.3、`22` §7.2 的措辞，并修正了 A4 的事实陈述。
3. **顺带产物**：核验 Weidlich 时一并拿到了 Deng 元分析的准确出处（*Computers & Education* 227, 105224）——**核一条常顺带确认相邻一条**。
4. 🔴 **反向检索（本轮最值钱的一条）：查不到 ≠ 不存在，先做作者反查再谈撤引。**
   本轮四条悬案里三条由此救回，而它们原本已进入"建议撤引"清单。失败形态是：
   **拿着我们自己写的功能描述（"stateful misconception detection"、"questioning intensity"、"multi-agent math tutor + GraphRAG"）去搜标题/摘要**——
   这些词从未出现在原文里，于是 OpenAlex / Crossref 一致 `count: 0`，结论就朝"该文可能不存在"滑过去。
   有效动作是**换维度**：
   `api.openalex.org/authors?search=<最不可能拼错的那位作者>` → 取 `id` →
   `api.openalex.org/works?filter=authorships.author.id:<id>&per-page=30` → 直接读该作者全部作品列表。
   Thonge & Thakkar 就是在这张列表里一眼找到的（同一 Ashoka 条目下并与 Sunil & Thakkar 相邻）。
   **配套纪律**：得到 `count: 0` 时只能写"按该检索式未命中"，**禁止写"该文不存在 / 该文没有 X"** ——
   与 `MEMORY` §5（只查摘要会误删真引用）互为镜像，两边合起来才是完整规则。
