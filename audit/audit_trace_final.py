# -*- coding: utf-8 -*-
"""SAGE 数字回溯：对每个承重数字，在权威容器中做数字边界检索并打印上下文。
输出 audit/traceability_report.txt
"""
import re, os, glob, io

HERE = os.path.dirname(os.path.abspath(__file__))      # audit/
ROOT = os.path.dirname(HERE)                          # 仓库根

CONTAINERS = {
    'MAIN_LOG': 'logs/_main_threshold.log',
    'LD012': 'data/leak_durable_sensitivity_0.012.json',
    'LD_SWEEP_ALL': 'data/leak_durable_sensitivity_*.json',
    'A9_THRESHOLD': 'logs/_a9_threshold.log',
    'A9_DAMPING': 'logs/_a9_damping.log',
    'A9_SHARPNESS': 'logs/_a9_sharpness.log',
    'DF': 'data/m2_durable_factor_sensitivity.json',
    'SELFTEST': 'logs/_selftest_threshold.log',
    'SUMMARY16': 'data/m2_lambda_alr_summary.json',
}

TARGETS = [
    ('theta', '0.3578'),
    ('lam*', '0.30'),
    ('lam* interval lo', '0.20'),
    ('lam* interval hi', '0.45'),
    ('gain* peak', '0.5659'),
    ('left_effect', '0.438'),
    ('right_effect', '0.3008'),
    ('control_left', '0.0594'),
    ('share', '0.8645'),
    ('share %', '86'),
    ('share lo', '76'),
    ('share hi', '88'),
    ('instr-leak share', '43'),
    ('leak_durable base', '0.012'),
    ('gain beyond bnd', '0.265'),
    ('mutants', '13'),
]

text = {}
for k, pat in CONTAINERS.items():
    if '*' in pat:
        s = []
        for p in sorted(glob.glob(os.path.join(ROOT, pat))):
            s.append(open(p, encoding='utf-8', errors='replace').read())
        text[k] = '\n'.join(s)
    else:
        p = os.path.join(ROOT, pat)
        text[k] = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else '<<MISSING>>'

out = []
for label, tok in TARGETS:
    out.append('=' * 100)
    out.append('TARGET: %-20s token=%s' % (label, tok))
    rx = re.compile(r'(?<![\d.\-])' + re.escape(tok) + r'(?![\d])')
    for cname, body in text.items():
        hits = list(rx.finditer(body))
        if not hits:
            continue
        out.append('  --- %s : %d hit(s)' % (cname, len(hits)))
        for m in hits[:4]:
            ctx = body[max(0, m.start() - 110):m.end() + 110].replace('\n', ' / ')
            out.append('      %s' % ctx)
    if not any(rx.search(b) for b in text.values()):
        out.append('  !! NO SOURCE IN ANY CONTAINER')
    out.append('')

io.open(os.path.join(HERE, 'traceability_report.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('done', sum(len(v) for v in text.values()))
