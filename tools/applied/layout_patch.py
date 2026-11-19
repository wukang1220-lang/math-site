"""One-off: switch tpl.html to the two-column (sidebar + content) layout.  python -I layout_patch.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'tpl.html')
t = open(P, encoding='utf-8').read()


def swap(text, start, end, new, keep_end=True):
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + new + (text[b:] if keep_end else text[b + len(end):])


HEADER = '''<header class="top">
  <div class="top-in">
    <a class="brand" href="#home"><i></i><span>數學方格簿<small>國中數學 七・八・九年級</small></span></a>
    <div class="search"><input id="q" type="search" placeholder="搜尋單元或名詞" aria-label="搜尋單元或名詞" autocomplete="off"><div class="sres" id="sres" hidden></div></div>
    <button id="fzBtn" class="pill" type="button" title="切換字級">字級：標準</button>
    <a class="pill pill-ok" href="#home">我的進度</a>
  </div>
</header>
<div class="page">
  <nav class="tabs" id="tabs" aria-label="主要頁面">
    <button id="sideBtn" type="button" aria-controls="side" aria-expanded="false">☰ 課程地圖</button>
    <a id="mapTab" href="#s1-1-1" data-n="map">課程地圖</a><a href="#home" data-n="home">會考重點</a><a href="#wrong" data-n="wrong">錯題本</a>
  </nav>
  <div class="layout">
    <aside class="side" id="side" aria-label="課程地圖"></aside>
    <main id="main"></main>
  </div>
</div>
<div id="sideBack"></div>
<div class="modal" id="figModal" hidden><div class="modal-in" role="dialog" aria-modal="true" aria-label="放大圖解"><div class="modal-h"><b>放大圖解</b><button class="btn" type="button" id="figClose">關閉</button></div><div id="figBig"></div></div></div>
'''
t = swap(t, '<header class="top">', '\n<script>', HEADER)

SECTION = r'''function section(k){
  const s = BYK[k], c = s.c, B = DATA.books[s.b.b - 1], d = C[k];
  const i = s.i, prev = SECS[i - 1], next = SECS[i + 1], g = 6 + Math.ceil(B.b / 2), idx = c.secs.findIndex(x => x.k === k) + 1;
  let h = `<div class="stack"><div class="crumb"><a href="#b${B.b}">${'七八九'[g - 7]}年級</a><span>/</span><span>${esc(c.pub[0])}</span></div>
  <div class="hero2"><div class="hero-l">
    <div class="chips"><span class="chip"><i class="dot st-${s.st}" style="padding:0"></i># ${SNAME[s.st]}</span><span class="codes">${esc(s.codes)}</span></div>
    <h1>${esc(s.t)}</h1>
    <p class="secno">${B.sem}・第 ${c.no} 章　第 ${idx} 節／共 ${c.secs.length} 節</p>
    ${d && d.sum ? `<p class="sum">${d.sum}</p>` : ''}
  </div>
  <div class="hero-r"><div class="exam"><span class="exam-l">106–115 年會考</span><span class="exam-n"><b>${s.cap.length}</b> 題</span><span>重要度 ${starHTML(s.imp)}</span>
    ${s.cap.length ? `<details class="capd"><summary>看題號（115-4 是 115 年第 4 題）</summary><div class="capids">${s.cap.map(x => x.replace('非', '（非選）').replace('組', '（題組）')).join('、')}</div></details>` : '<span class="small muted">十年內沒有直接出題，但常是其他單元的基礎。</span>'}
  </div></div></div>
  <p class="pubs">翰林：第 ${c.no} 章 ${esc(c.pub[0])}｜康軒：${esc(c.pub[1])}｜南一：${esc(c.pub[2])}</p>`;
  if (!d) {
    h += `<section class="blk"><p class="empty">這個單元的重點整理還在製作中。</p></section>`;
  } else {
    h += `<section class="blk"><div class="blk-h"><h2>重點整理</h2></div><div class="rows">${d.rows.map(r => `<div class="row"><div class="lab">${r.h}</div><div class="body"><ul>${r.li.map(x => `<li>${x}</li>`).join('')}</ul>${r.tip.map(t => `<p class="tip">${t}</p>`).join('')}</div></div>`).join('')}</div></section>`;
    if (d.fig.length) h += `<section class="blk blk-fig"><div class="blk-h"><h2>圖解</h2><span class="muted small">點「放大」可以看大圖</span></div><div class="figs">${d.fig.map(f => `<figure class="fig"><button class="btn zoom" type="button" data-fig="${f}">放大</button>${DATA.figs[f]}</figure>`).join('')}</div></section>`;
    if (d.w && W[d.w]) h += `<section class="blk blk-tool"><div class="blk-h"><h2>動手試試</h2><span class="muted small">${esc(WN[d.w] || '')}</span></div><div class="tool" data-w="${d.w}" data-o="${esc(d.wo || '')}"></div></section>`;
    if (d.ex.length) h += `<section class="blk"><div class="blk-h"><h2>例題</h2></div>${d.ex.map((e, j) => `<div class="ex"><p><b>例 ${j + 1}</b>　${e.q}</p><details><summary>看解法</summary><ol class="sol">${e.a.map(x => `<li>${x}</li>`).join('')}</ol></details></div>`).join('')}</section>`;
    if (d.qs.length) h += `<section class="blk"><div class="blk-h"><h2>練習</h2><span class="muted small" id="qprog">答對 ${okCount(k)} / ${d.qs.length}</span><button class="btn" type="button" data-act="reset" style="margin-left:auto">重做這一節</button></div><div class="stack" style="gap:12px">${d.qs.map((q, j) => qHTML(k, j, q, j + 1)).join('')}</div></section>`;
  }
  h += `<div class="pager">${prev ? `<a href="#s${prev.k}">← ${esc(prev.t)}</a>` : '<span></span>'}${next ? `<a href="#s${next.k}">${esc(next.t)} →</a>` : ''}</div></div>`;
  return h;
}
'''
t = swap(t, 'function section(k){', 'function wrongView(){', SECTION)

ROUTER = r'''/* ---------- sidebar ---------- */
let sideG = 7, curKey = null;
function renderSide(act){
  const b1 = (sideG - 7) * 2 + 1, chs = [];
  [b1, b1 + 1].forEach(b => DATA.books[b - 1].chs.forEach(c => chs.push({c, b})));
  const actCh = act ? BYK[act].c : null, gn = '七八九'[sideG - 7];
  let h = `<div class="side-card"><div class="side-h"><span class="grid-ic" aria-hidden="true"></span><h2>課程地圖</h2></div>
  <div class="seg" role="group" aria-label="選擇年級">${[7, 8, 9].map(g => `<button type="button" data-g="${g}" class="${g === sideG ? 'on' : ''}" aria-pressed="${g === sideG}">${'七八九'[g - 7]}年級</button>`).join('')}</div>
  <div class="side-sub">${gn}年級 ・ ${chs.length} 章</div><ol class="chs">`;
  let lastB = 0;
  chs.forEach(({c, b}, n) => {
    if (b !== lastB) { h += `<li class="semh">${SEM[b]}・${DATA.books[b - 1].vol}</li>`; lastB = b; }
    const on = c === actCh, done = c.secs.every(s => isDone(s.k));
    h += `<li><a class="ch${on ? ' on' : ''}" href="#s${c.secs[0].k}"${on ? ' aria-current="true"' : ''}><span class="n">${n + 1}</span><span class="t">${esc(c.pub[0])}</span>${done ? '<span class="ok" title="全部完成">✓</span>' : ''}</a>`;
    if (on) h += `<ul class="secs">${c.secs.map(s => `<li><a class="${s.k === act ? 'on' : ''}" href="#s${s.k}"${s.k === act ? ' aria-current="page"' : ''}>${esc(s.t)}${isDone(s.k) ? ' <span class="ok">✓</span>' : ''}</a></li>`).join('')}</ul>`;
    h += '</li>';
  });
  $('#side').innerHTML = h + '</ol></div>';
}
$('#side').addEventListener('click', e => {
  const g = e.target.closest('.seg button');
  if (g) { sideG = +g.dataset.g; renderSide(curKey); return; }
  if (e.target.closest('a')) closeSide();
});
function closeSide(){ document.body.classList.remove('side-open'); $('#sideBtn').setAttribute('aria-expanded', 'false'); }
$('#sideBtn').addEventListener('click', () => { const o = document.body.classList.toggle('side-open'); $('#sideBtn').setAttribute('aria-expanded', String(o)); });
$('#sideBack').addEventListener('click', closeSide);

/* ---------- figure zoom ---------- */
const figModal = $('#figModal');
function closeFig(){ figModal.hidden = true; $('#figBig').innerHTML = ''; }
$('#figClose').addEventListener('click', closeFig);
figModal.addEventListener('click', e => { if (e.target === figModal) closeFig(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (!figModal.hidden) closeFig(); else closeSide(); } });

/* ---------- router ---------- */
function route(){
  const h = location.hash.slice(1) || 'home';
  let html, nav = 'home', act = null;
  if (/^b[1-6]$/.test(h)) { const b = +h[1]; html = book(b); nav = 'map'; sideG = 6 + Math.ceil(b / 2); }
  else if (h[0] === 's' && BYK[h.slice(1)]) { const s = BYK[h.slice(1)]; act = s.k; html = section(s.k); nav = 'map'; sideG = 6 + Math.ceil(s.b.b / 2); st.last = s.k; save(); }
  else if (h === 'wrong') { html = wrongView(); nav = 'wrong'; }
  else html = home();
  curKey = act;
  $('#main').innerHTML = html;
  renderSide(act);
  $('#mapTab').setAttribute('href', '#s' + (st.last && BYK[st.last] ? st.last : SECS[0].k));
  document.querySelectorAll('#tabs a[data-n]').forEach(a => a.classList.toggle('on', a.dataset.n === nav));
  closeSide(); closeFig();
  document.querySelectorAll('.tool[data-w]').forEach(el => { try { W[el.dataset.w](el); } catch (e) { el.textContent = '工具載入失敗'; } });
  window.scrollTo(0, 0);
}
window.addEventListener('hashchange', route);
'''
t = swap(t, '/* ---------- router ---------- */', "window.addEventListener('hashchange', route);", ROUTER, keep_end=False)

# answering: refresh sidebar ticks; zoom buttons
t = t.replace("    const p = $('#qprog'); if (p) p.textContent = `答對 ${okCount(k)} / ${qcount(k)}`;\n    return;",
              "    const p = $('#qprog'); if (p) p.textContent = `答對 ${okCount(k)} / ${qcount(k)}`;\n    renderSide(curKey);\n    return;")
t = t.replace("  const r = e.target.closest('[data-act=\"reset\"]');",
              "  const z = e.target.closest('.zoom');\n  if (z) { $('#figBig').innerHTML = DATA.figs[z.dataset.fig]; figModal.hidden = false; $('#figClose').focus(); return; }\n  const r = e.target.closest('[data-act=\"reset\"]');")

CSS = r'''/* ===== two-column layout ===== */
:root{--hero:#e4f0ef;--on-accent:#ffffff;--r-lg:18px}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--hero:#14292a;--on-accent:#0e1413}}
:root[data-theme="dark"]{--hero:#14292a;--on-accent:#0e1413}
.top-in{max-width:1320px;gap:8px 12px}
.brand span{display:grid;line-height:1.25}
.brand small{font-size:.72rem;color:var(--accent);font-weight:500}
.pill{border:1px solid var(--line);background:var(--paper);border-radius:10px;padding:5px 12px;cursor:pointer;font-size:.9rem;text-decoration:none;color:var(--ink-2);white-space:nowrap}
.pill:hover{border-color:var(--accent)}
.pill-ok{background:var(--ok-soft);border-color:transparent;color:var(--ok);font-weight:700}
.page{max-width:1320px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:16px 72px}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.tabs a,.tabs button{border:1px solid var(--line);background:var(--paper);border-radius:12px;padding:7px 16px;text-decoration:none;color:var(--ink);font-weight:500;cursor:pointer}
.tabs a:hover,.tabs button:hover{border-color:var(--accent)}
.tabs a.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent)}
#sideBtn{display:none}
.layout{display:grid;grid-template-columns:280px minmax(0,1fr);gap:28px;align-items:start}
#main{min-width:0}
.side{position:sticky;top:calc(env(safe-area-inset-top,0px) + 84px);max-height:calc(100vh - 100px);overflow:auto;overscroll-behavior:contain}
.side-card{background:var(--paper);border:1px solid var(--line);border-radius:var(--r-lg);padding:18px 14px}
.side-h{display:flex;align-items:center;gap:10px;margin:0 6px 12px}
.side-h h2{font-size:1.15rem}
.grid-ic{width:18px;height:18px;flex:none;border:1.5px solid var(--accent);border-radius:3px;background-image:linear-gradient(var(--accent) 1px,transparent 1px),linear-gradient(90deg,var(--accent) 1px,transparent 1px);background-size:5px 5px;background-position:1px 1px;opacity:.85}
.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;background:var(--bg);border-radius:12px;padding:4px}
.seg button{border:0;background:none;border-radius:9px;padding:7px 0;cursor:pointer;color:var(--ink-2);font-weight:500}
.seg button.on{background:var(--accent);color:var(--on-accent)}
.side-sub{font-size:.86rem;color:var(--ink-2);font-weight:700;margin:16px 8px 4px}
.chs{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.chs .semh{font-size:.76rem;color:var(--muted);letter-spacing:.08em;margin:10px 8px 2px}
.ch{display:flex;align-items:center;gap:10px;padding:7px 8px;border-radius:12px;text-decoration:none;color:var(--ink);font-weight:500}
.ch .n{width:26px;height:26px;border-radius:8px;background:var(--bg);display:grid;place-items:center;font-family:var(--f-mono);font-size:.82rem;color:var(--ink-2);flex:none}
.ch .t{min-width:0}
.ch:hover{background:var(--accent-soft)}
.ch.on{background:var(--accent-soft)}
.ch.on .n{background:var(--accent);color:var(--on-accent)}
.secs{list-style:none;margin:2px 0 6px 21px;padding:0 0 0 10px;border-left:2px solid var(--line);display:grid;gap:1px}
.secs a{display:flex;gap:6px;padding:6px 10px;border-radius:9px;text-decoration:none;color:var(--ink-2);font-size:.92rem}
.secs a:hover{background:var(--bg)}
.secs a.on{background:var(--accent-soft);color:var(--ink);font-weight:700}
.ok{color:var(--ok);font-weight:700;margin-left:auto}
.crumb a{text-decoration:none}
.hero2{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(220px,1fr);gap:22px;align-items:center;border:1px solid var(--line);border-radius:var(--r-lg);padding:30px;
  background-color:var(--hero);background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:20px 20px;background-position:right top}
.hero-l{display:grid;gap:8px;min-width:0}
.hero2 h1{font-size:clamp(1.9rem,4.2vw,2.8rem);letter-spacing:.03em}
.codes{font-family:var(--f-mono);color:var(--ink-2);font-size:.86rem;align-self:center}
.secno{color:var(--ink-2);font-size:.92rem}
.sum{font-size:1.04rem;color:var(--ink)}
.exam{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:18px 20px;display:grid;gap:6px;box-shadow:0 8px 24px rgba(15,82,87,.08)}
.exam-l{font-size:.82rem;color:var(--muted);letter-spacing:.06em}
.exam-n{font-size:1rem}
.exam-n b{font-family:var(--f-mono);font-size:2.6rem;line-height:1;margin-right:4px}
.pubs{font-size:.86rem;color:var(--muted);margin-top:-6px}
.blk{background:var(--paper);border:1px solid var(--line);border-radius:var(--r-lg);padding:22px}
.blk>.blk-h h2{font-size:1.2rem}
.blk .ex{border-left:3px solid var(--accent)}
.blk-tool{background:var(--paper)}
.fig{position:relative;margin:0;padding:12px}
.zoom{position:absolute;top:8px;right:8px;font-size:.8rem;padding:2px 10px;z-index:1}
.q{background:var(--bg)}
.opts button{background:var(--paper)}
.modal{position:fixed;inset:0;z-index:40;background:rgba(0,0,0,.55);display:grid;place-items:center;padding:16px}
.modal[hidden]{display:none}
.modal-in{background:var(--paper);border-radius:16px;padding:16px;width:min(980px,100%);max-height:100%;overflow:auto;display:grid;gap:10px}
.modal-h{display:flex;justify-content:space-between;align-items:center}
#figBig svg{display:block;width:100%;height:auto}
#figBig svg text{font-family:var(--f-body)}
#sideBack{display:none}
@media (max-width:960px){
  .layout{grid-template-columns:1fr}
  .side{position:fixed;top:0;bottom:0;left:0;width:min(330px,88vw);max-height:none;z-index:30;transform:translateX(-105%);transition:transform .2s ease;background:var(--bg);
    padding:calc(env(safe-area-inset-top,0px) + 12px) 12px calc(env(safe-area-inset-bottom,0px) + 12px) max(12px,env(safe-area-inset-left,0px))}
  body.side-open .side{transform:none;box-shadow:8px 0 30px rgba(0,0,0,.2)}
  body.side-open #sideBack{display:block;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:25}
  #sideBtn{display:inline-flex}
  #mapTab{display:none}
  .hero2{grid-template-columns:1fr;padding:22px}
}
@media (max-width:700px){.top-in{display:grid;grid-template-columns:1fr auto auto}.top-in .search{grid-column:1 / -1;grid-row:2}.blk{padding:16px}.hero2{padding:18px}}
'''
t = t.replace('</style>', CSS + '</style>', 1)
open(P, 'w', encoding='utf-8').write(t)
print('patched', len(t))
