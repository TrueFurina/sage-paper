"""Verify PDFs really contain the rendered content (not blank / not glyph-less).

Checks per PDF:
  - page count
  - extracted text length
  - presence of distinctive CJK keywords from the source doc
  - presence of the ASCII/technical tokens (lambda, Telling@N)
  - fallback: if text extraction is empty, scan page for drawn content
"""
import os, sys, re, unicodedata

try:
    import pymupdf as fitz
except Exception:
    import fitz


def norm(s: str) -> str:
    """Normalise for keyword matching: NFKC folds ligatures (ﬀ->ff, ﬁ->fi)
    so that renderer-level ligature substitution does not cause false
    negatives, and strip whitespace so line-wrapping does not either."""
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", "", s)

PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf")

EXPECT = {
    "FEDC投稿_引导式多智能体_深度研究报告": ["脚手架", "答案泄露", "SAGE", "Telling@N", "准实验", "MIR3"],
    "README": ["SAGE", "下一步", "论文大纲"],
    "00_定位与口径_术语翻译表": ["术语翻译", "答案泄露闸门", "禁写清单", "TuringMate",
                            # 2026-09-20 出处更正后新增断言
                            "Weidlich", "SafeTutors"],
    "01_theoretical_framework_en": ["Scaffolding", "leakage", "bottleneck", "Proposition"],
    "02_系统架构与交互协议": ["脚手架", "要答案拦截", "SAGE_Main", "408",
                                "SMILI", "xLM", "诊断卡", "GuidedToLevel"],
    "03_408知识图谱骨架": ["数据结构", "先修", "Dijkstra", "跨科"],
    "04_题库方案与测量": ["Telling@N", "题库", "ZPD", "伦理"],
    "05_论文大纲": ["Introduction", "Appendix", "教育学为体", "Abstract",
                       # the paper title is a deliverable: assert it renders
                       "When Does Guidance Still Help",
                       "Attributing Learning Gains to Scaffolding"],
    "06_苏格拉底引导代表作精读与缺口分析": ["苏格拉底", "缺口", "Brender", "Telling@N", "元认知",
                                        "Weidlich", "SafeTutors"],
    "07_Introduction动机链_原文证据锚定": ["Introduction", "Brender", "Suvernev", "Telling@N", "scaffolding",
                                            "SocraticPO", "Sunil", "jailbreak",
                                            # title must appear in the draft too
                                            "When Does Guidance Still Help"],
    "08_M2实验审计记录": ["变异检验", "durable_factor", "死参数", "归因", "SUPPORTED",
                          "阈值", "边界"],
    "09_方向决策备忘": ["换向", "归因测量", "阈值", "边界", "A9", "敏感性", "mi_hat",
                              "Weidlich", "SafeTutors", "出处更正"],
    "10_汇报_选题过程_微信版": ["换方向", "归因", "守约边界", "When Does Guidance Still Help",
                                "86%", "变异检验",
                                # 2026-09-20 补入「动摇之前」的选题过程，必须断言它真被渲染出来
                                "四项技术", "四支", "损失函数", "408", "SAGE",
                                # 2026-09-20 出处更正：必须断言更正后的措辞已渲染
                                "误引", "Weidlich", "SafeTutors"],
    "11_论文成稿进度地图": ["完整版", "成稿率", "英文初稿", "未成稿",
                            "Results", "双盲"],
    "12_待决策清单": ["待决策", "阻塞", "D9", "D12", "伦理审查",
                        "gaming", "六维", "Suvernev",
                        "D19", "SMILI", "Demmans", "提示依赖度", "87%"],
}

# ---------------------------------------------------------------------------
# COVERAGE GUARD (fail-closed) -- 2026-09-20
# EXPECT is a hand-maintained list, so a NEW document silently escapes the
# content gate: its PDF gets produced, `_pdf_hygiene` clears it, and `_pdfverify`
# simply never looks at it -- reporting "N/N pass" over a set that quietly
# excludes the newest artifact. That is the same failure class as any hardcoded
# allow-list: the gate cannot notice what it does not list.
# So: every PDF present on disk must appear in EXPECT. If one does not, the
# gate FAILS and says which. Adding a document now requires adding its
# assertions -- which is the point.
# ---------------------------------------------------------------------------
_pdf_stems = {os.path.splitext(f)[0] for f in os.listdir(PDF_DIR)
              if f.lower().endswith(".pdf")}
_uncovered = sorted(s for s in _pdf_stems if s not in EXPECT)
if _uncovered:
    print("!! UNCOVERED PDFs (on disk but absent from EXPECT):")
    for s in _uncovered:
        print(f"     - {s}.pdf")
    print("   A gate that does not cover an artifact cannot vouch for it.")
    print("   Add each to EXPECT with distinctive keywords from its source.\n")

fails = []
for name, kws in EXPECT.items():
    p = os.path.join(PDF_DIR, name + ".pdf")
    if not os.path.exists(p):
        print(f"MISSING  {name}.pdf")
        fails.append(name)
        continue
    d = fitz.open(p)
    n_pages = d.page_count
    raw = "".join(d[i].get_text() for i in range(n_pages))
    text = norm(raw)
    hits = [k for k in kws if norm(k) in text]
    miss = [k for k in kws if norm(k) not in text]
    # count images/drawings as a sanity signal for non-text content
    drawings = sum(len(d[i].get_drawings()) for i in range(min(n_pages, 5)))
    status = "OK  " if not miss else "WARN"
    print(f"{status} {name:<44} pages={n_pages:<3} chars={len(raw):<7} "
          f"draw={drawings:<5} hits={len(hits)}/{len(kws)}")
    if miss:
        print(f"       MISSING KEYWORDS: {miss}")
        fails.append(name)
    if len(raw) < 200:
        print(f"       !! text too short -> likely blank render")
        fails.append(name)
    d.close()

fails.extend(_uncovered)

print()
print(f"[verify] {len(EXPECT)-len(set(fails))}/{len(EXPECT)} PDFs pass content check")
if _uncovered:
    print(f"[verify] FAIL: {len(_uncovered)} PDF(s) not covered by EXPECT "
          f"-> the gate cannot vouch for them.")
if fails:
    print("  problematic:", ", ".join(sorted(set(fails))))
    sys.exit(1)
