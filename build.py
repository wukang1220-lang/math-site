"""Build the 數學方格簿 page.

python -I build.py            -> writes ../math-site.html (artifact) and docs/index.html
python -I build.py --check    -> parse and validate content only

Content files content/b1.txt … b6.txt use a small line format:

  @ 1-1-1                 start a section (key from structure.json)
  fig: m-perp m-views     figures from art/figs (space separated)
  widget: numline         interactive tool id (handled in tpl.html)
  # 標題                  a concept row (left label)
  - 內容                  a bullet in the current row
  ! 小叮嚀                a tip under the current row
  EX: 題目                a worked example; following "=> " lines are the solution steps
  Q: 題幹                 a practice question; then 4 lines "o: 選項" with exactly one "o*: 正確"
  E: 解析                 the explanation for the last question
  // comment

Inline markup: **重點詞**, x^2, a^{m+n}, x_1, \\f{分子}{分母}, \\r{被開方數}, \\seg{AB}, \\arc{AB},
\\sys{第一式}{第二式}. Single lowercase letters (a, x, n …) are set in italics.
"""
import html, json, os, re, sys, hashlib, random

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = {'sin', 'cos', 'tan', 'cm', 'km', 'kg', 'mm', 'ml', 'mg', 'kwh'}


class Bad(Exception):
    pass


def group(s, i):
    """s[i] == '{' -> (inner, index after closing brace)."""
    assert s[i] == '{'
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    raise Bad('unbalanced { in: ' + s)


NARG = {'f': 2, 'r': 1, 'seg': 1, 'arc': 1, 'sys': 2, 'sysx': 3}


def render(s):
    out, i, kw = [], 0, False
    n = len(s)
    while i < n:
        ch = s[i]
        if s.startswith('**', i):
            out.append('</strong>' if kw else '<strong class="kw">')
            kw = not kw
            i += 2
        elif ch == '\\':
            m = re.match(r'\\([a-z]+)', s[i:])
            if not m or m.group(1) not in NARG:
                raise Bad('unknown command in: ' + s)
            name = m.group(1)
            i += len(m.group(0))
            args = []
            for _ in range(NARG[name]):
                if i >= n or s[i] != '{':
                    raise Bad(f'\\{name} needs {NARG[name]} {{…}} in: ' + s)
                a, i = group(s, i)
                args.append(render(a))
            if name == 'f':
                out.append(f'<span class="fr"><span>{args[0]}</span><span>{args[1]}</span></span>')
            elif name == 'r':
                out.append(f'<span class="rt">√<span>{args[0]}</span></span>')
            elif name == 'seg':
                out.append(f'<span class="seg">{args[0]}</span>')
            elif name == 'arc':
                out.append(f'<span class="arc">{args[0]}</span>')
            else:
                out.append('<span class="sys"><span class="eqs">' + ''.join(f'<span>{a}</span>' for a in args) + '</span></span>')
        elif ch in '^_':
            i += 1
            if i < n and s[i] == '{':
                a, i = group(s, i)
            else:
                m = re.match(r'[0-9]+|[A-Za-z]|.', s[i:])
                if not m:
                    raise Bad('dangling ^/_ in: ' + s)
                a = m.group(0)
                i += len(a)
            tag = 'sup' if ch == '^' else 'sub'
            out.append(f'<{tag}>{render(a)}</{tag}>')
        elif 'a' <= ch <= 'z':
            m = re.match(r'[a-z]+', s[i:])
            word = m.group(0)
            prev = s[i - 1] if i else ''
            nxt = s[i + len(word)] if i + len(word) < n else ''
            if word in WORDS or len(word) > 3 or prev.isascii() and prev.isalpha() or nxt.isascii() and nxt.isalpha():
                out.append(html.escape(word))
            else:
                out.append(f'<i>{word}</i>')
            i += len(word)
        else:
            out.append(html.escape(ch, quote=False))
            i += 1
    if kw:
        raise Bad('odd number of ** in: ' + s)
    return ''.join(out)


def is_num(t):
    return re.fullmatch(r'[−\-]?\d+(\.\d+)?', t.strip()) is not None


def to_num(t):
    return float(t.strip().replace('−', '-'))


def parse(path, known, data):
    cur, row, q = None, None, None
    for ln, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.rstrip('\n').strip()
        if not line or line.startswith('//'):
            continue
        where = f'{os.path.basename(path)}:{ln}'
        try:
            if line.startswith('@+ '):
                key = line[3:].split()[0]
                if key not in data:
                    raise Bad('@+ for a section that does not exist yet: ' + key)
                cur, row, q = data[key], None, None
                continue
            if line.startswith('@ '):
                key = line[2:].split()[0]
                if key not in known:
                    raise Bad('unknown section ' + key)
                if key in data:
                    raise Bad('duplicate section ' + key)
                cur = data[key] = {'rows': [], 'ex': [], 'qs': [], 'fig': [], 'w': ''}
                row = q = None
                continue
            if cur is None:
                raise Bad('text before the first @ section')
            if line.startswith('sum:'):
                cur['sum'] = render(line[4:].strip())
            elif line.startswith('fig:'):
                cur['fig'] += line[4:].split()
            elif line.startswith('widget:'):
                parts = line[7:].split()
                cur['w'] = parts[0]
                cur['wo'] = ' '.join(parts[1:])
            elif line.startswith('# '):
                row = {'h': render(line[2:].strip()), 'li': [], 'tip': []}
                cur['rows'].append(row)
                q = None
            elif line.startswith('- '):
                if row is None:
                    raise Bad('bullet outside a # row')
                row['li'].append(render(line[2:].strip()))
            elif line.startswith('! '):
                if row is None:
                    raise Bad('tip outside a # row')
                row['tip'].append(render(line[2:].strip()))
            elif line.startswith('EX:'):
                cur['ex'].append({'q': render(line[3:].strip()), 'a': []})
                q = None
            elif line.startswith('=>'):
                if not cur['ex']:
                    raise Bad('=> before EX:')
                cur['ex'][-1]['a'].append(render(line[2:].strip()))
            elif line.startswith('Q:'):
                q = {'q': render(line[2:].strip()), 'o': [], 'raw': [], 'a': -1, 'e': ''}
                cur['qs'].append(q)
            elif line.startswith('o*:') or line.startswith('o:'):
                if q is None:
                    raise Bad('option outside a question')
                star = line.startswith('o*:')
                txt = line[3:].strip() if star else line[2:].strip()
                if star:
                    if q['a'] >= 0:
                        raise Bad('two correct options')
                    q['a'] = len(q['o'])
                q['o'].append(render(txt))
                q['raw'].append(txt)
            elif line.startswith('E:'):
                if q is None:
                    raise Bad('E: outside a question')
                q['e'] = render(line[2:].strip())
            else:
                raise Bad('unrecognised line: ' + line[:40])
        except Bad as e:
            sys.exit(f'{where}: {e}')
    # validate + order options
    for key, sec in data.items():
        for qi, q in enumerate(sec['qs']):
            if 'raw' not in q:
                continue  # validated with an earlier file
            tag = f'{key} Q{qi + 1}'
            if len(q['o']) != 4 or q['a'] < 0 or not q['e']:
                sys.exit(f'{tag}: needs 4 options, one o*, and an E:')
            if len(set(q['raw'])) != 4:
                sys.exit(f'{tag}: duplicate options')
            del q['raw']  # option order is shuffled in the page for every round
        for ex in sec['ex']:
            if not ex['a']:
                sys.exit(f'{key}: example without => lines')
    return data


def main():
    check = '--check' in sys.argv
    struct = json.load(open(os.path.join(HERE, 'structure.json'), encoding='utf-8'))
    known = {s['k'] for b in struct for c in b['chs'] for s in c['secs']}
    content = {}
    for name in [f'{p}{b}.txt' for p in 'bqe' for b in range(1, 7)]:
        p = os.path.join(HERE, 'content', name)
        if os.path.exists(p):
            parse(p, known, content)
    short = [k for k in sorted(content) if len(content[k]['qs']) != 15]
    if short:
        print('sections without exactly 15 questions:', len(short), ' '.join(f'{k}({len(content[k]["qs"])})' for k in short[:12]))
    fewex = [f'{k}({len(content[k]["ex"])})' for k in sorted(content) if not 2 <= len(content[k]['ex']) <= 3]
    if fewex:
        print('sections without 2–3 examples:', len(fewex), ' '.join(fewex[:12]))
    dup = [(k, i) for k in content for i, q in enumerate(content[k]['qs']) if [x['q'] for x in content[k]['qs']].index(q['q']) != i]
    if dup:
        sys.exit(f'duplicate question stems: {dup}')
    figs = {}
    figdir = os.path.join(HERE, 'art', 'figs')
    for sec in content.values():
        for f in sec['fig']:
            fp = os.path.join(figdir, f + '.svg')
            if not os.path.exists(fp):
                sys.exit(f'missing figure {f}.svg')
            svg = open(fp, encoding='utf-8').read()
            svg = re.sub(r'<\?xml[^>]*>\s*', '', svg).strip()
            figs[f] = svg
    nq = sum(len(s['qs']) for s in content.values())
    print(f'{len(content)}/{len(known)} sections written, {nq} questions, {len(figs)} figures')
    if check:
        return
    cap = json.load(open(os.path.join(HERE, 'data', 'capmap.json'), encoding='utf-8'))
    strand = {}
    for i in cap['items']:
        b = {'N': 'N', 'A': 'A', 'F': 'A', 'S': 'G', 'G': 'G', 'D': 'D'}[i['th']]
        strand.setdefault(b, [0, 0, 0])
        strand[b][0] += 1
        strand[b][1 if i['y'] <= 110 else 2] += 1
    data = {'books': struct, 'c': content, 'figs': figs, 'strand': strand}
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    tpl = open(os.path.join(HERE, 'tpl.html'), encoding='utf-8').read()
    page = tpl.replace('/*DATA*/null', blob)
    out = os.path.join(os.path.dirname(HERE), 'math-site.html')
    open(out, 'w', encoding='utf-8').write(page)
    os.makedirs(os.path.join(HERE, 'docs'), exist_ok=True)
    full = ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '</head>\n<body>\n' + page + '\n</body>\n</html>\n')
    open(os.path.join(HERE, 'docs', 'index.html'), 'w', encoding='utf-8').write(full)
    open(os.path.join(HERE, 'docs', '.nojekyll'), 'w', encoding='utf-8').write('')
    print('wrote', out, f'{len(page) // 1024} KB')


if __name__ == '__main__':
    main()
