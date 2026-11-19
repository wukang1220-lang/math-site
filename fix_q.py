"""Apply exact-line replacements from a fix list.  python -I fix_q.py <fixfile>
Fix file: blocks separated by a line '====', each block 'FILE\\nOLD LINE\\n----\\nNEW LINE'."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
blocks = open(sys.argv[1], encoding='utf-8').read().split('\n====\n')
bad = 0
for b in blocks:
    b = b.strip('\n')
    if not b:
        continue
    fn, rest = b.split('\n', 1)
    old, new = rest.split('\n----\n')
    p = os.path.join(HERE, 'content', fn.strip())
    t = open(p, encoding='utf-8').read()
    n = t.count(old)
    if n != 1:
        print('NOT UNIQUE/FOUND', n, fn, old[:50])
        bad += 1
        continue
    open(p, 'w', encoding='utf-8').write(t.replace(old, new))
print('applied', len([b for b in blocks if b.strip()]) - bad, 'failed', bad)
