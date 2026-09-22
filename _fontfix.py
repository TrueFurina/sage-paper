# -*- coding: utf-8 -*-
"""Replace glyphs that the embedded CJK subset lacks, across the markdown set.

The renderer's font has no ⑬/⑭ (circled digits stop at ⑫) and none of
the small decorative emoji used in the internal notes; leaving them in the
text makes PyMuPDF embed a 3.4 MB fallback font into every affected PDF.

Writes each file via a .tmp + os.replace so a failure can never truncate
the destination (the earlier accident).
"""
import glob
import io
import os

# char -> replacement ("x " forms are consumed as char+space to avoid
# leaving a double space behind)
RULES = [
    ('\u246c', '(13)'),
    ('\u246d', '(14)'),
    ('\U0001f3af ', ''),
    ('\U0001f4cc ', ''),
    ('\U0001f511 ', ''),
    ('\U0001f527 ', ''),
    ('\U0001f3af', ''),
    ('\U0001f4cc', ''),
    ('\U0001f511', ''),
    ('\U0001f527', ''),
]

log = []
for p in sorted(glob.glob('*.md')):
    T = io.open(p, encoding='utf-8').read()
    orig = T
    hits = []
    for old, new in RULES:
        n = T.count(old)
        if n:
            T = T.replace(old, new)
            hits.append('U+%04X x%d' % (ord(old[0]), n))
    if T != orig:
        io.open(p + '.tmp', 'w', encoding='utf-8', newline='\n').write(T)
        os.replace(p + '.tmp', p)
        log.append('%-46s %s' % (p, ', '.join(hits)))

io.open('logs/_fontfix_hits.txt', 'w', encoding='utf-8').write('\n'.join(log) if log else 'no file changed')
print('\n'.join(log) if log else 'no file changed')
