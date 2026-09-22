# -*- coding: utf-8 -*-
"""SAGE 正文数字可回溯性审计 —— 步骤1-4
1) 抽取英文正文全部数字声明（数字边界正则 + 上下文）
2) 汇总权威容器的 config 指纹
3) 逐条回溯
输出: audit/claim_inventory.txt / audit/container_inventory.txt / audit/trace_rough.txt
"""
import json, re, os, glob, io

HERE = os.path.dirname(os.path.abspath(__file__))      # audit/
ROOT = os.path.dirname(HERE)                          # 仓库根（本脚本在 audit/ 子目录内）
OUT = []

BODY = [
    ('01_theoretical_framework_en.md', 'S1..?'),
    ('13_Section2_Literature_Review_en.md', 'S2'),
    ('07_Introduction\u52a8\u673a\u94fe_\u539f\u6587\u8bc1\u636e\u951a\u5b9a.md', 'S1-Intro?'),
    ('21_Section4_System_Design_en.md', 'S4'),
    ('17_Section5_Method_en.md', 'S5'),
    ('15_Section6_Results_en.md', 'S6'),
    ('22_Section7_Discussion_en.md', 'S7'),
    ('14_Section8_Limitations_en.md', 'S8'),
    ('24_Section9_Conclusion_en.md', 'S9'),
    ('23_Abstract_en.md', 'Abstract'),
]

NUM = re.compile(r'(?<![\w.])(\d+\.\d+|\d+)%?(?![\w])')

# ---------- 1) 抽取正文数字声明 ----------
claims = []
for fn, tag in BODY:
    p = os.path.join(ROOT, fn)
    if not os.path.exists(p):
        OUT.append('!! MISSING %s' % fn); continue
    lines = open(p, encoding='utf-8').read().split('\n')
    for i, ln in enumerate(lines, 1):
        # 跳过中文要略块（行内以 ★ 或中文为主的不算正文声明）
        for m in NUM.finditer(ln):
            tok = m.group(0)
            # 只要"有意义"的数字：带小数点、或带% 、或 >=10 的整数
            val = tok.rstrip('%')
            if '.' not in tok and '%' not in tok:
                try:
                    if abs(float(val)) < 10:
                        continue
                except ValueError:
                    pass
            ctx = ln[max(0, m.start()-70):m.end()+70]
            claims.append((fn, tag, i, tok, ctx))

with io.open(os.path.join(HERE, 'claim_inventory.txt'), 'w', encoding='utf-8') as f:
    f.write('抽取到数字声明 %d 条\n\n' % len(claims))
    cur = None
    for fn, tag, i, tok, ctx in claims:
        if fn != cur:
            cur = fn
            f.write('\n########## %s  (%s) ##########\n' % (fn, tag))
        f.write('L%-4d %-10s | %s\n' % (i, tok, ctx.replace('\n', ' ')))

# ---------- 2) 权威容器 + config 指纹 ----------
containers = []
for p in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json'))):
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception as e:
        containers.append((os.path.basename(p), 'LOAD-ERR %r' % e)); continue
    cfg = d.get('config') if isinstance(d, dict) else None
    fp = {}
    if isinstance(d, dict):
        fp['keys'] = len(d.keys())
        for k in ('seeds', 'learners', 'problems', 'problems_per_learner', 'theta',
                  'optimum_lambda_by_gain', 'contrast_grid'):
            if k in d:
                fp[k] = d[k]
        if cfg:
            fp['cfg'] = cfg
        res = d.get('results')
        if isinstance(res, list) and res and isinstance(res[0], dict):
            fp['res0_keys'] = sorted(res[0].keys())
            fp['n_res'] = len(res)
    containers.append((os.path.basename(p), json.dumps(fp, ensure_ascii=False)))

with io.open(os.path.join(HERE, 'container_inventory.txt'), 'w', encoding='utf-8') as f:
    for name, fp in containers:
        f.write('%-52s %s\n\n' % (name, fp))

# ---------- 3) 主结果抽取 ----------
trace = []
ld_files = sorted(glob.glob(os.path.join(ROOT, 'data', 'leak_durable_sensitivity_*.json')))
rows = []
for p in ld_files:
    d = json.load(open(p, encoding='utf-8'))
    cfg = d.get('config', {})
    r = d['results'][0]
    rows.append((cfg.get('values'), cfg.get('seeds'), cfg.get('problems'),
                 r.get('lambda_star'), r.get('gain_star'), r.get('left_effect'),
                 r.get('right_effect'), r.get('control_left_effect'),
                 r.get('attributable_share'), r.get('verdict')))
rows.sort(key=lambda x: float(x[0]))
trace.append('===== leak_durable 13-value sweep (authoritative) =====')
trace.append('%-8s %-6s %-9s %-7s %-8s %-8s %-8s %-9s %-9s %s' % (
    'ld', 'seeds', 'problems', 'lam*', 'gain*', 'left', 'right', 'ctrl_lft', 'share', 'verdict'))
for r in rows:
    trace.append('%-8s %-6s %-9s %-7s %-8s %-8s %-8s %-9s %-9.4f %s' % (
        r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]))

shares = [r[8] for r in rows if isinstance(r[8], (int, float))]
lams = set(r[3] for r in rows)
trace.append('')
trace.append('share min/max over 13 values = %.4f / %.4f' % (min(shares), max(shares)))
trace.append('lambda_star set over 13 values = %s' % sorted(lams))
trace.append('n_ld_files = %d' % len(rows))

# ---------- 4) 主 summary 的 λ 网格（找峰值与近优带） ----------
p = os.path.join(ROOT, 'data', 'm2_lambda_alr_summary.json')
d = json.load(open(p, encoding='utf-8'))
trace.append('')
trace.append('===== m2_lambda_alr_summary.json (seeds=%s, problems_per_learner=%s) ====='
             % (d.get('seeds'), d.get('problems_per_learner')))
trace.append('optimum_lambda_by_gain = %s' % d.get('optimum_lambda_by_gain'))
trace.append('min_alr_lambda = %s' % d.get('min_alr_lambda'))
trace.append('proposition1_supported = %s' % d.get('proposition1_supported'))
s = d.get('summary', [])
trace.append('%-8s %-12s %-12s %-14s %-14s' % ('lambda', 'alr_mean', 'earned_gain', 'leak_solve', 'dep'))
for row in (s if isinstance(s, list) else []):
    trace.append('%-8s %-12.4f %-12.4f %-14.4f %-14.4f' % (
        row.get('lambda'), row.get('alr_mean', float('nan')),
        row.get('earned_gain_mean', float('nan')),
        row.get('leak_solve_mean', float('nan')), row.get('dep_mean', float('nan'))))

with io.open(os.path.join(HERE, 'trace_rough.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(str(x) for x in trace))
print('claims=%d containers=%d ld=%d' % (len(claims), len(containers), len(rows)))
