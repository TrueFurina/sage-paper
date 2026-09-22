# MEMORY.md — SAGE 论文线（长期项目约定）

> 本文件只记**跨会话仍有效的约定与规则**。事故经过、当日进度写 `YYYY-MM-DD.md`。
> （2026-09-22 重整：原 §6c-2 的复原事故经过已移入当日日志，此处只留规则。）

## 0. 工作区隔离（重要）

本 workspace（`E:\Program\MARL\SAGE`）**只有 SAGE 论文**。以下线在**别的目录**，禁止把它们的文档/代码/口径套用过来：
- NetLearn / study-help-pro（408 考研多智能体；GOMARL / FrugalRAG 属该线）
  —— 408 期资产已于 2026-09-21 移交 `E:/Program/MARL/study-help-pro/archive/sage_408_handoff/`（已核实存在）
- 芒得很职（Spring Boot + Vue 职业培训平台，`E:\Code\Mangdehenzhi`）
- MARL-ECDSA 共识链（`E:\Program\MARL\【CCF】区块链AI协同…\marl-ecdsa-consensus-chain`，**只读核查，不改其代码**）
  - ⚠️ 其"1624 passed"在本机**不可复现**（自带 `.venv` 缺 numpy → 45 模块收集失败；换系统 Python 得 1526 collected / 10 errors，缺 scipy/matplotlib/dilithium_py）→ **不断言造假，也不背书**。
  - 服务器 `172.16.222.99`（Ubuntu 24.04 / 128 核 / RTX 5080）本机**密钥免密可通**；**只有 `~/miniconda3/envs/gomarl`（torch 2.8.0+cu128）在 Blackwell 实测可算**，`mappo`(cu118)/`marl`(cu121) 均不可用。长任务一律 **tmux 托管**（nohup/setsid 挡不住 systemd 清进程）。SOP：`E:\Program\MARL\AI连服务器跑实验SOP.md`。
  - 🔴 `deliverables/_d2d3/pull_new_results.py` 第 10–12 行**明文账号密码** → 进交付包即泄露凭据。
→ 只**借鉴方法论**（如"用既有数据主动证伪自己的旗舰结论"），**不搬运内容**。

## 0b. 版本控制（2026-09-22 建立）

- `git init -b main`；**基线提交 `d47dbb2`**（全量初始快照，含当时尚未清理的临时脚本）。此后本类事故可用 `git checkout d47dbb2 -- <path>` 取回。
- **提交身份为本地中性值** `SAGE Author <sage-author@localhost>`，**不继承本机全局身份**——本文双盲投稿，避免将来公开产物时泄露作者。
- `.gitattributes` → `* -text`：**关闭行尾转换**。本工作区曾因 CRLF/LF 差异把"文件被改坏"误判过一次。
- `.gitignore` 忽略：`pdf/`（可再生）、`refs/ _refs/ 核心论文（参考）/`（外部文献，约 215 MB）、`__pycache__/`。
  **白名单**：`!_sage_subset.ttf`（`md2pdf.py` 的运行依赖，非纯可再生品）、`!_refs_passwords_course_outline.docx`（密码学场景唯一一手来源）。
- 改任何 `.md` 后**必须**重渲染：`python md2pdf.py <file.md>`（否则交付件带着修前的字）。
- **远端（2026-09-22 建立）**：`origin = https://github.com/TrueFurina/sage-paper.git`（**private**），分支 `main`。
  推送用 `python C:\Users\Lenovo\.workbuddy\bin\gh_run.py -C <repo> push origin refs/heads/main:refs/heads/main`
  （token 从 `HKCU\Environment` 注入；bash 不继承 HKCU，直接跑 git 会报 could not read Password）。
  推送前**先 `--check`**：token 已注入 / local 与 remote 是否一致。
  🔴 **凭据中间产物必须落在仓库外**（如 `%TEMP%`）：曾把含 token 前 7 位的检查文件用 `git add -A` 一起提交（已 rm --cached 并加 ignore）。

## 1. 论文本体

- **题名（定稿，2026-09-21）**：*When Does Guidance Still Help? Separating Scaffolding Effects from Answer-Leakage Effects in Graduate Cryptography Instruction — A Simulation Study*
  - 末尾 "A Simulation Study" 是**诚实性要求**，不是措辞偏好。已同步六处：`05` / `07` 开头 / `10` §九 / `README` / `12` D8 / `09` §十。
- **第一宣称 = 归因测量装置**（不是"我们有新机制"）。机制不宣称首创（Suvernev 已用 GRPO + 对抗课程训练守约）。
- **研究形态 = 全模拟、无真实课堂**（D20 路径②）。密码学课程是**应用场景**，不是数据采集点。
- **场景 = 研究生密码学**（由 408 迁移而来）；迁移裁决 D21–D23 见 `09` §十三。

## 2. 语言约定（2026-09-21 定）

- **正文一律英文**（FEDC 是英文期刊）。**不写中文全文**——避免双倍工作量与口径漂移。
- 每个英文正文文件顶部挂一段 **「★ 中文要略（仅供审读；非翻译源，非口径依据 —— 一切以英文正文为准）」**，250–400 字。
- **口径单一真值 = 英文正文**；中文要略与英文冲突时，改中文。
- 决策/口径/素材类文件（`00`/`02`/`05`/`09`/`12`/`19`/`20`）保持中文，不受此约束。

## 3. 数字单一真值（★ 极易漂移）

一律用**阈值形式**，旧连续形式已作废：

| 量 | ~~旧（勿用）~~ | **现行** |
|---|---|---|
| λ\* | ~~0.35~~ | **0.30**，区间 **[0.20, 0.45]** |
| earned-solve 峰值 | ~~0.5204~~ | **0.5659** |
| 可归因份额 | ~~85%~~ | **86%**（敏感性 76–88%） |
| 对照臂贡献 | — | **+0.0594**（完整干预 +0.4380） |
| 有教益泄露变异体份额 | ~~≈43%~~ | **主配置 28%**（40/240/25，`leak_durable=0.50`）<br>⚠️ 43% **不是错的**，是**变异检查小配置**（10/120/12）读数 → **凡引用必须带配置标签**，两值不得并列不加限定 |
| leak_durable 基线 | — | **0.012**（规定值，无外部锚） |
| 缺口表述 | ~~"无人刻画泄露—强度关系"~~ | **"分级约束 + 持久结果（撤除后测）+ 通道分解"三者同时具备** |

**权威容器**（索引不是数据源；`data/README.md` 有完整表）：主 sweep + 校准门 → `logs/_main_threshold.log`；λ\* 区间与 76–88% → `logs/_a9_threshold.log`；"86% 在深度扫描下恒定" → `logs/_a9_damping.log`；主配置逐 λ 结果 → `data/leak_durable_sensitivity_0.012.json`。

## 3b. 承重引用的已核事实（改正文前必查）

> 完整清单（含 Bastani / Tweed & Lehman / OpenAlex 陷阱 / leak_durable / 86% 条件性 / λ\* 语义 / mi_hat 等逐条细节）
> 已拆到同目录 **`MEMORY-references.md`** —— **改引用相关句子前必须先读它**。此处只留最易犯的三条：

1. 🚫 **Bastani et al. (2025, PNAS 122(26), e2422633122)**：随机化单位是 **classroom 不是 student**（honors 班排除）；
   GPT Tutor 护栏**同时变了三样**（给 hints 不给答案 + 逐步引导 + 提示词注入教师正确解法与常见错误反馈）
   → **不得再写成只变了两样**；护栏**全在提示词层**。
2. 🔴 **Tweed & Lehman (2002)**：其主旨是两传统的**差异**，**不得用来支持"趋同"**（`13` §2.1 已把趋同限缩为时机条件）。
3. 🔴 **86% 是条件值**：必须带"在 `leak_durable=0.012`（泄露的答案不教人）的规定下"；且 `leak_durable` 是**唯一能推翻第一宣称**的规定常数，**一律引用 40/240/25 同配置值**。

## 4. 反"虚假宣称"红线（每次改动都要过一遍）

1. 🚫 不得暗示做过课堂研究／有真实学生数据。
2. 🚫 不得以"有无真实学生数据"评判他人工作（批评须落在**设计缺陷**：没有把脚手架与少泄题分开）。
3. 🚫 不得写"首创/第一个/无一"类断言（尤其：可训练约束、Telling@N、指出 prompt 层不足，三者皆非首创）。
4. 🚫 不得写"最优强度/内部最优"——已改边界语义。
4b. 🚫 **不得写"无人刻画泄露—强度关系"** / "no existing system varies a constraint and plots the response"
   （被 **TutorRL, Dinucu-Jianu et al., EMNLP 2025, pp. 272–292** 证伪：可变 λ + 三条 λ 响应曲线 + Pareto 前沿）。
   同理 **"二值 vs 分级"也不是我们的差异轴**。残存差异只有两条：① 其结果是**对话后即时解题率**，非撤除后测得；② λ 让泄露与成功率**沿前沿一起移动**（权衡刻画 ≠ 增益分解）。
5. 🚫 不得引 **AIED 2026 research-gap synthesis**（出处已撤回，实为 AI 生成知识库）→ 改挂 Weidlich et al. (2025)。
6. 🔴 未取得全文的引用必须带限定语：Suvernev "据其已公开摘要所述"；Thonge & Thakkar 亦仅摘要级。**OpenAlex/Crossref 的 `abstract_inverted_index` 为空 ≠ 该文没有该内容。**
7. 🚫 **不得编造参考文献元数据**（卷期页/DOI）。未核字段一律写 `[待核]`。
8. 🚫 **不得写"本文首次命名/提出 answer leakage"** —— STAP（Xie, Shi, Li & Liu, 2025，**北方工业大学**；ISAIE '25, pp. 584–587）已 formalise 该概念并给出 operational definitions + compliance criteria。只可说"术语非本文引入"。
9. 🚫 **不得把"学习者状态推断 + 脚手架耦合"当贡献** —— ScaffoldLM（Li et al., ACL 2026, pp. 7165–7188）已有该控制回路。`07` §1.5(3) 只声称"三件事同时具备"。
10. 🚫 **正文不得用"撞车/竞争"口吻评价相邻工作** —— 一律写成正常相关文献；该词只留在 `26` 与 memory。

## 5. 引用核验方法（本线已实证有效）

- **承重的引用必须回原文，不靠二手摘要**——Goldin 2012 的 87%/88% 只在全文里。只查摘要会误判"无法证实"进而**误删真引用**。
- 抓全文：`files.eric.ed.gov/fulltext/<ERIC号>.pdf`；脚本 `_refcheck.py`（下载 → PyMuPDF 取文本 → 正则定位数字 → 打印上下文 → **结果落盘**，因本机 stdout 不回传）。原文 PDF 存 `_refs/`。
- 核验两类产出：① 数字/元数据是否属实；② **我们的措辞是否比原文强**（后者放过即变相夸大）。结果必须**回写正文**，不能只写附录。
- 🔴 **"某引用没说过 X"的判定，前提是已取得全文**；只握摘要时只能写"未在摘要中核到 X"，**禁止写"该文没有 X"**。
- 🔴 **镜像方向**：**按内部简称／自己写的功能描述检索，`count: 0` 也不等于该文不存在。** 破局 = **作者反向检索**：`authors?search=<最不容易拼错的那位作者>` → 取 `id` → `works?filter=authorships.author.id:<id>&per-page=30` 读其全部作品。
  **合并纪律：`count: 0` 只支撑"按该检索式未命中"，禁止支撑"该文不存在"；决定撤引前必须先跑一次作者反查。**
- 🔴 **核不到的二手引用，优先换一手文献，而不是再找另一条二手源**（2026-09-22 实例：《论语》7.8 的时机条件，原文即依据）。
- 🔴 **可核替代文献必须与我们的论断同向**再引用：方向相反时引用即"措辞强于原文"（Tweed & Lehman 实例，见 §3b）。
- **找漏掉的先例：反查已核文献的参考文献列表，比正向搜索有效得多**（TutorRL 是靠 ScaffoldLM 全文一句 "Following the protocol in (Dinucu-Jianu et al., 2025)" 挖出来的）。
- **核的顺序**：优先核**最承重**的那条（本项目 = Bastani），不按待办清单顺序核。

## 6. 本机环境坑

- **PowerShell 工具的 stdout 不回传**（python 打印、`Out-String` 均为空）→ 一律 `> file` 落盘再 Read。
  控制台回显中文文件名出现 cp936 乱码（**仅显示层**，文件本身干净，勿据此误判损坏）。
- **bash 工具常整体失效**（`ls`/`head` command not found）→ 文件操作用 Glob/Read/Edit。
- **长文本/长提交信息不用 heredoc 或反引号**（会被静默改写）→ 用编辑工具写文件；`git commit -F <file>`。
- **命令行内联 Python 的反斜杠会被吃掉**（`'\\\\'` → SyntaxError）→ 复杂脚本一律写成 `.py` 文件再跑。

- 🔴 **PDF 工具链必须用 managed python**：`C:\Users\Lenovo\.workbuddy\binaries\python\versions\3.13.12\python.exe`
  （实测有 **fontTools + fitz**）。系统 `D:\miniconda3_new\python.exe` **没有 fontTools**（且**没有 scipy**）→ 跑 `_charcheck.py` 直接 `ModuleNotFoundError`。
  → 渲染/字符检查一律：`"<managed-py>" md2pdf.py <file.md>` 与 `"<managed-py>" _charcheck.py <file.md>`；
  纯统计脚本若要 scipy，需另找环境，否则手算 t 值。

## 6b. 并行会话（2026-09-22 实证，改动前必读）

- 本工作区**存在并行会话同时改 SAGE 的 md 文件**（当日在 `01`/`13`/`22`/`25`/`26` 上均撞到对方已写入的内容；`audit/` 目录与 `.gitignore` 亦疑为并行会话所建）。
- **硬规则**：改任何 SAGE 文件之前，先 **Grep 关键词 + Read 目标行**确认最新磁盘状态；不要凭本会话早前读到的内容下手。
- 发现对方已改且质量更好时：**保留对方的**，只补自己那部分，并在日志里记一句"该处由并行会话处理"。
- 自纠要**留痕**：自己判错了就在报告里写明"初判错误 + 成因 + 更正"，不得悄悄改掉。
- 🔴 **并发热点表不要手工挑编号**：`13` §2.7 这类表被多会话追加，手工写编号必撞 → 一律**追加到表尾**或用脚本按末尾编号**自动续号**。

## 6c. 🔴 写文件安全铁律（事故后立，级联优先级最高）

**事故**：`io.open(P,'w')` **先截断后写**，随后 `.write()` 抛 `UnicodeEncodeError` → `13_Section2_Literature_Review_en.md` 被清成 **0 字节**，payload 从未落盘（当时本工作区无 git、无备份）。

1. ❌ **永不** `io.open(path,'w')` 之后再执行可能抛异常的构造/写入。
   ✅ 先在内存构造完整 payload → 写 `path.tmp` → `os.replace(path.tmp, path)`。
   （批量改多文件同理：各自 tmp + replace，且**任一条替换不命中就整体中止、不落盘**。）
2. ❌ **不要用 `\ud83d\udd34` 这类代理对转义**写 emoji（Python str 里是两个孤立代理，UTF-8 编码必抛）。✅ 用 `\U0001F534` 或直接写字符。**这是本次事故的直接触发器。**
3. **替换式批改必须 `assert count==1`**；**每次改完立刻读回校验**。
4. ✅ **`md2pdf.py` 支持单文件渲染**：`python md2pdf.py <文件名.md>`（读 `sys.argv[1:]`）。**改了任何 md 必须重渲染**——曾发现 `pdf/13_*.html` 仍是含被证伪旧句的过期渲染件（= 交付物带错）。
5. 🔴 **"清单/表格声称已完成"处必须回正文抽查** —— 曾两次栽在这上面：复原时的"改动清单"漏掉整两轮正文改动，而 §2.7 表已记为 ✅ 完成（表格与正文脱节）。
6. 🔴 **清理/删除脚本必须把自己列入 KEEP** —— 否则按字母序删到自己 → 重跑报 "No such file" → **极易误判为"脚本从未执行"**。且 **manifest 必须在执行删除之前落盘**。
7. 🔴 **删除判据 = 引用反查，不是文件名直觉**：被正文或保留工具链引用者留；**"临时脚本引用临时脚本"不算承重引用**。
8. 🔴 **移动即破坏**：脚本用 `ROOT = dirname(__file__)` 时，把它移进子目录会**静默改坏所有相对路径** → 移动后必须**实跑**验证，不能只读代码判断"看着对"。
9. 🔴 **插入型编辑要把锚点一并写回** `new_string` —— 否则会把锚点行（如一个 `###` 标题）静默删掉。

**兜底与复原**：兜底副本唯一来源是 `pdf/<name>.html`（上次渲染件，保留全文含表格）；⚠️ **渲染件 ≠ 备份**。反解要点：`md2pdf.py` 开了 `nl2br` → HTML 的 `<br>` 全是**软换行**，还原成 `\n`，引用块每物理行补 `> `。先用 `T.count('关键词')` 探针判定缺什么再逐条重施加。**通用方法已固化为 `doc-truncation-recovery` 技能。**

**渲染字体坑**：`md2pdf.py` 的 CJK 子集**不含** `⑬⑭`（圈号止于 ⑫）与 `🎯📌🔑🔧`；用了会让 PyMuPDF 嵌入 3.4 MB 回退字体、PDF 膨胀约 5 倍（`_pdf_hygiene.py` 会报 fallback font）→ 用 `_fontfix.py` 换纯文本标记；**新增符号前先确认字体有该字形**。

## 7. 进度

唯一进度真值源 = `11_论文成稿进度地图.md`。正文 10 节 + Abstract 均有英文初稿。
2026-09-22：建立版本控制 + 清理临时产物 + 数字可追溯性审计（缺陷全在索引层，非数字错）+ 闭合两条核不到的引用（C4/C5）。
剩余缺口（均为真缺口）：① 文献元数据的尾项（4–5 条预印本的"是否已正式发表"；Tishby 年份 1999/2000 二选一并全书统一；C7 页码为推定）；② `15` §6 图表；③ 双盲处理；④ 100-seed 复核。STAP / ToST 全文仍未取得。
2026-09-22（晚）：**附录 A/B/C 英文初稿完成 → `28_AppendixABC_en.md`**（A 信息瓶颈 + 阈值/连续对照推导；B 阶梯按接近度 + 四套模板 + 拦截 + 主循环 + 埋点；C 题型/标注/9 道示例题/46 节点图谱/Telling@N 手册）。EduDial 全文已取回逐字复核（22 页，陈述全命中，补「K–12 数学」范围限定）。
