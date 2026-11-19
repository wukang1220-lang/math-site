"""Wrap key phrases in **…** (red) inside bullets that have no red mark yet.  python -I apply_red.py [--dry]"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
dry = '--dry' in sys.argv
want = {}
for ln in open(os.path.join(HERE, 'red_map.txt'), encoding='utf-8'):
    ln = ln.rstrip('\n')
    if not ln.strip():
        continue
    k, ph = ln.split(' | ', 1)
    want.setdefault(k, []).append([p.strip() for p in ph.split('||')])
miss, total = [], 0
for b in range(1, 7):
    p = os.path.join(HERE, 'content', f'b{b}.txt')
    lines = open(p, encoding='utf-8').read().split('\n')
    sec = {}
    key = None
    for i, ln in enumerate(lines):
        m = re.match(r'@ (\S+)', ln)
        if m:
            key = m.group(1)
        elif ln.startswith('- ') and key:
            sec.setdefault(key, []).append(i)
    for key, idxs in sec.items():
        used = set()
        for phrases in want.get(key, []):
            hit = None
            for i in idxs:
                ln = lines[i]
                if i in used or '**' in ln or ln.startswith('- 例'):
                    continue
                if all(ph in ln for ph in phrases):
                    hit = i
                    break
            if hit is None:
                miss.append(f'{key}: {" || ".join(phrases)}')
                continue
            ln = lines[hit]
            for ph in phrases:
                j = ln.index(ph, 2)
                ln = ln[:j] + '**' + ph + '**' + ln[j + len(ph):]
            if '****' in ln:
                miss.append(f'{key}: adjacent marks in {ln[:30]}')
                continue
            lines[hit] = ln
            used.add(hit)
            total += 1
    if not dry:
        open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('marked', total, 'bullets')
for m in miss:
    print('MISS', m)
left = []
for b in range(1, 7):
    key = None
    for ln in open(os.path.join(HERE, 'content', f'b{b}.txt'), encoding='utf-8'):
        m = re.match(r'@ (\S+)', ln)
        if m:
            key = m.group(1)
        elif ln.startswith('- ') and '**' not in ln and not ln.startswith('- 例'):
            left.append(f'{key}: {ln[2:40].strip()}')
print('still unmarked (non-example):', len(left))
for x in left:
    print('  ', x)
