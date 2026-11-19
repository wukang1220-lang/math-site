"""Build structure.json (books → chapters → sections) from the 會考 course map.

python -I make_structure.py
"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
cap = json.load(open(os.path.join(HERE, 'data', 'capmap.json'), encoding='utf-8'))
items, SEC = cap['items'], cap['sec']

BOOKS = {1: ('七上', '第一冊'), 2: ('七下', '第二冊'), 3: ('八上', '第三冊'),
         4: ('八下', '第四冊'), 5: ('九上', '第五冊'), 6: ('九下', '第六冊')}
# chapter key -> (翰林, 康軒, 南一)
CHAP = {
    '1-1': ('數與數線', '整數的運算', '整數運算與科學記號'),
    '1-2': ('標準分解式與分數運算', '分數的運算', '因數分解與分數運算'),
    '1-3': ('一元一次方程式', '一元一次方程式', '一元一次方程式'),
    '2-1': ('二元一次聯立方程式', '二元一次聯立方程式', '二元一次聯立方程式'),
    '2-2': ('直角坐標與二元一次方程式的圖形', '直角坐標與二元一次方程式的圖形', '平面直角坐標系'),
    '2-3': ('比例', '比與比例式', '比例'),
    '2-4': ('一元一次不等式', '一元一次不等式', '一元一次不等式'),
    '2-5': ('統計圖表與統計數據', '統計', '統計圖表與資料分析'),
    '2-6': ('線對稱與三視圖', '生活中的幾何', '生活中的幾何圖形'),
    '3-1': ('乘法公式與多項式', '乘法公式與多項式', '乘法公式與多項式'),
    '3-2': ('平方根與畢氏定理', '平方根與畢氏定理', '平方根與畢氏定理'),
    '3-3': ('因式分解', '因式分解', '因式分解'),
    '3-4': ('一元二次方程式', '一元二次方程式', '一元二次方程式'),
    '3-5': ('統計資料處理', '統計資料處理', '統計資料處理與圖表'),
    '4-1': ('數列與級數', '數列與級數', '數列與等差級數'),
    '4-2': ('線型函數與其圖形', '函數', '函數及其圖形'),
    '4-3': ('三角形的基本性質', '三角形的基本性質', '三角形的性質與尺規作圖'),
    '4-4': ('平行與四邊形', '平行與四邊形', '平行與四邊形'),
    '5-1': ('相似形與三角比', '相似形', '比例線段與相似形'),
    '5-2': ('圓形', '圓', '圓的性質'),
    '5-3': ('推理證明與三角形的心', '幾何與證明', '推理證明與三角形的心'),
    '6-1': ('二次函數', '二次函數', '二次函數'),
    '6-2': ('統計與機率', '統計與機率', '統計與機率'),
    '6-3': ('立體圖形', '生活中的立體圖形', '立體幾何圖形'),
}
# nicer section titles where the course-map name was shortened
TITLE = {'1-3-3': '一元一次方程式的應用', '2-1-3': '聯立方程式的應用', '3-4-3': '一元二次方程式的應用',
         '5-2-1': '點、線、圓', '6-1-2': '二次函數的最大值與最小值', '3-3-1': '提公因式與乘法公式',
         '3-3-2': '十字交乘法', '1-2-2': '最大公因數與最小公倍數'}
BIG = {'N': 'N', 'A': 'A', 'F': 'A', 'S': 'G', 'G': 'G', 'D': 'D'}


def stars(n):
    return 1 if n == 0 else 2 if n <= 2 else 3 if n <= 4 else 4 if n <= 7 else 5


bysec = collections.defaultdict(list)
for i in items:
    bysec[i['k']].append(i)

books = []
for b in range(1, 7):
    chs = []
    for ck in sorted(c for c in CHAP if c.startswith(f'{b}-')):
        secs = []
        for sk in sorted(k for k in SEC if k.startswith(ck + '-')):
            name, th, codes = SEC[sk]
            its = sorted(bysec[sk], key=lambda i: (-i['y'], i['n']))
            sn = sk.split('-')[2]
            secs.append({
                'k': sk, 'no': '' if sn == '0' else f"{ck.split('-')[1]}-{sn}",
                't': TITLE.get(sk, name), 'th': th, 'st': BIG[th], 'codes': codes,
                'cap': [f"{i['y']}-{i['n']}" + ('非' if i['t'] == '非' else '組' if i['t'] == '組' else '') for i in its],
                'imp': stars(len(its)),
            })
        main = collections.Counter(s['st'] for s in secs for _ in range(max(1, len(s['cap'])))).most_common(1)[0][0]
        chs.append({'k': ck, 'no': int(ck.split('-')[1]), 'pub': CHAP[ck], 'st': main,
                    'n': sum(len(s['cap']) for s in secs), 'secs': secs})
    books.append({'b': b, 'sem': BOOKS[b][0], 'vol': BOOKS[b][1], 'chs': chs})

json.dump(books, open(os.path.join(HERE, 'structure.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(len(c['secs']) for b in books for c in b['chs']), 'sections,',
      sum(c['n'] for b in books for c in b['chs']), 'exam items')
