"""清理续跑（幂等）。接 _cleanup.py 中断处继续。

前一版的两个教训（已固化本脚本）：
  A. `_cleanup.py` 自身也匹配 `_*` → 删到它时把自己删了，导致重跑报 "No such file"，
     令人误判为"脚本从未执行"。→ 本脚本把自己的文件名加入 KEEP。
  B. manifest 原在删除**之后**写，进程一被打断就丢失执行记录。→ 本脚本开头先落盘。
"""
import io
import os
import glob
import shutil
import traceback

SELF = "_cleanup_finish.py"

KEEP = {
    "md2pdf.py", "_charcheck.py", "_pdf_hygiene.py", "_pdfverify.py",
    "_fontsub.py", "_fontfix.py", "_scan_mojibake.py", "_sage_subset.ttf",
    "_munge_charcheck.py", "_munge_pdf_hygiene.py", "_munge_subset_guard.py",
    "m2_lambda_sweep.py", "_a9_sensitivity.py", "_df_sensitivity.py",
    "_ld_sensitivity.py", "_ld_collect.py",
    "_check_threshold_mutants.py", "_audit_dead_params.py", "_power_calc.py",
    "_refcheck.py",
    "_refs_passwords_course_outline.docx", "_docx_text.txt",
    SELF,
}

DIRS_TO_DELETE = [
    "__pycache__",
    "_archive/snap_20260922_0845",
    "_archive/snap_20260922_0850",
    "_archive/408_assets_for_studyhelp",
]
FILES_TO_DELETE = [
    "_archive/05_论文大纲_v2.html",
    "_archive/05_论文大纲_v2.pdf",
]

os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
assert os.path.isfile(SELF)

targets = sorted(n for n in glob.glob("_*")
                 if os.path.isfile(n) and n not in KEEP)
for n in sorted(KEEP - {"md2pdf.py", "m2_lambda_sweep.py"}):
    if os.path.isfile(n) and os.path.basename(n) != n:
        pass

lines = ["# 清理续跑记录 (resume)", ""]
lines.append("待删文件: %d" % len(targets))
lines.append("待删目录: %d" % len(DIRS_TO_DELETE))
lines.append("")
io.open("_cleanup_manifest.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")

errors = []
for n in targets:
    try:
        size = os.path.getsize(n)
        os.remove(n)
        lines.append("DEL   %-34s %8d B" % (n, size))
    except Exception as e:
        errors.append("%s: %r" % (n, e))

lines.append("")
for d in DIRS_TO_DELETE:
    if not os.path.isdir(d):
        lines.append("SKIP  %-34s (不存在)" % d)
        continue
    try:
        nf = sum(len(f) for _, _, f in os.walk(d))
        sz = sum(os.path.getsize(os.path.join(r, f))
                 for r, _, fs in os.walk(d) for f in fs)
        shutil.rmtree(d)
        lines.append("RMDIR %-34s %3d 文件 / %.2f MB" % (d, nf, sz / 1048576))
    except Exception as e:
        errors.append("rmdir %s: %r" % (d, e))

for f in FILES_TO_DELETE:
    if os.path.isfile(f):
        try:
            sz = os.path.getsize(f)
            os.remove(f)
            lines.append("DEL   %-34s %8d B" % (f, sz))
        except Exception as e:
            errors.append("%s: %r" % (f, e))

# _archive 若已空则移除
if os.path.isdir("_archive") and not os.listdir("_archive"):
    os.rmdir("_archive")
    lines.append("RMDIR %-34s (已空)" % "_archive")

lines.append("")
missing_keep = sorted(n for n in KEEP if n != SELF and not os.path.exists(n))
left = sorted(n for n in glob.glob("_*") if os.path.isfile(n) and n not in KEEP)
lines.append("复核: 应删未删 = %d %s" % (len(left), left or ""))
lines.append("复核: 应留却缺 = %d %s" % (len(missing_keep), missing_keep or ""))
lines.append("异常 = %d %s" % (len(errors), errors or ""))
io.open("_cleanup_manifest.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")

print("deleted=%d rmdir=%d left=%d missing_keep=%d errors=%d"
      % (len(targets), len(DIRS_TO_DELETE), len(left), len(missing_keep), len(errors)))
