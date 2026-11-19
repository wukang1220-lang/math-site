"""One-off: random 8-question rounds, shuffled options, petal showers.  python -I quiz_patch.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'tpl.html')
t = open(P, encoding='utf-8').read()


def swap(text, start, end, new):
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + new + text[b:]


STATE = r'''/* ---------- state ---------- */
const KEY = 'mathGrid.v1', ROUND = 8;
let st = {first:{}, wrong:{}, cor:{}, done:{}, best:{}, round:{}, fz:0};
try { const raw = localStorage.getItem(KEY); if (raw) st = Object.assign(st, JSON.parse(raw)); } catch (e) {}
if (st.ans) { for (const id in st.ans) if (st.ans[id] && st.ans[id].ok) st.cor[id] = 1; delete st.ans; }
function save(){ try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
function qcount(k){ return C[k] ? C[k].qs.length : 0; }
function okCount(k){ let n = 0; for (let i = 0; i < qcount(k); i++) if (st.cor[k + '.' + i]) n++; return n; }
function isDone(k){ return !!st.done[k]; }
function shuffle(a){ for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function newRound(k){
  const n = qcount(k), pick = shuffle([...Array(n).keys()]).slice(0, Math.min(ROUND, n)), p = {};
  pick.forEach(i => { p[i] = shuffle([...Array(C[k].qs[i].o.length).keys()]); });
  return (st.round[k] = {q: pick, p, a: {}});
}
function getRound(k){
  const r = st.round[k], n = qcount(k);
  if (!r || !Array.isArray(r.q) || r.q.length !== Math.min(ROUND, n) || r.q.some(i => i >= n || !r.p[i])) { newRound(k); save(); }
  return st.round[k];
}
function roundStat(k){ const r = getRound(k), done = r.q.filter(i => r.a[i]).length, ok = r.q.filter(i => r.a[i] && r.a[i].ok).length; return {r, done, ok, all: r.q.length}; }
'''
t = swap(t, '/* ---------- state ---------- */', 'function starHTML(n)', STATE)

# home progress line
t = t.replace("const qAll = SECS.reduce((a, s) => a + qcount(s.k), 0), qOk = SECS.reduce((a, s) => a + okCount(s.k), 0);",
              "const qAll = SECS.reduce((a, s) => a + qcount(s.k), 0), qOk = SECS.reduce((a, s) => a + okCount(s.k), 0);")
old_prog = t[t.index('<p>完成 <b class="num">'):]
old_prog = old_prog[:old_prog.index('</p>') + 4]
t = t.replace(old_prog, '<p>完成 <b class="num">${doneN}</b> / ${written} 個單元（隨機 8 題全對才算完成）；題庫 ${qAll} 題中答對過 <b class="num">${qOk}</b> 題。${Object.keys(st.wrong).length ? `錯題本還有 <a href="#wrong">${Object.keys(st.wrong).length} 題</a>。` : \'\'}</p>')
# book view meta
t = t.replace("C[s.k] ? okCount(s.k) + ' / ' + qcount(s.k) + ' 題' : '整理中'", "C[s.k] ? '答對過 ' + okCount(s.k) + ' / ' + qcount(s.k) + ' 題' : '整理中'")

QHTML = r'''const CHEER = ['答對了！', '太棒了！', '好厲害！', '完全正確！', '漂亮！', '繼續保持！'];
function qHTML(k, i, q, n, perm, a, mode){
  const id = k + '.' + i, disp = perm.map(o => o);
  return `<div class="q${a ? ' locked' : ''}" data-q="${id}" data-m="${mode}" data-p="${perm.join('')}"><p><span class="qn">${n}.</span>${q.q}</p>
  <div class="opts">${disp.map((o, j) => `<button type="button" data-i="${o}"${a ? ' disabled' : ''} class="${a ? (o === a.c ? (a.ok ? 'ok' : 'no') : (!a.ok && o === q.a ? 'ans' : '')) : ''}"><span class="L">(${L4[j]})</span><span>${q.o[o]}</span></button>`).join('')}</div>
  <div class="fb${a ? (a.ok ? ' ok' : ' no') : ''}"${a ? '' : ' hidden'}>${a ? fbHTML(q, a.ok, perm) : ''}</div></div>`;
}
function fbHTML(q, ok, perm){ return ok ? `<b>${CHEER[Math.floor(Math.random() * CHEER.length)]}</b>${q.e}` : `<b>再想想。</b>正確答案是 (${L4[perm.indexOf(q.a)]})。${q.e}`; }
function quizHTML(k){
  const {r, done, ok, all} = roundStat(k), d = C[k];
  return `<div class="blk-h"><h2>練習</h2><span class="muted small">題庫 ${d.qs.length} 題，每次隨機抽 ${all} 題</span><button class="btn" type="button" data-act="new" style="margin-left:auto">換一組題目</button></div>
  <div class="qbar"><span id="qprog">${progText(done, ok, all)}</span>${isDone(k) ? '<span class="chip okchip">✓ 曾經 8 題全對</span>' : ''}</div>
  <div class="stack" style="gap:12px">${r.q.map((i, j) => qHTML(k, i, d.qs[i], j + 1, r.p[i], r.a[i], 'r')).join('')}</div>
  <div id="qsum">${done === all ? sumHTML(ok, all) : ''}</div>`;
}
function progText(done, ok, all){ return `本輪已作答 ${done} / ${all} 題，答對 ${ok} 題`; }
function sumHTML(ok, all){
  return ok === all ? `<div class="qsum win"><b>${all} 題全對！太厲害了！</b><span>這個單元完成了，可以換一組題目再挑戰。</span><button class="btn" type="button" data-act="new">再挑 ${all} 題</button></div>`
    : `<div class="qsum"><b>本輪答對 ${ok} / ${all} 題</b><span>答錯的題目已收進錯題本。再挑一組，目標 ${all} 題全對！</span><button class="btn" type="button" data-act="new">再挑 ${all} 題</button></div>`;
}
'''
t = swap(t, 'function qHTML(k, i, q, n){', 'function section(k){', QHTML)

# section practice block
a = t.index("    if (d.qs.length) h += `<section class=\"blk\"><div class=\"blk-h\"><h2>練習</h2>")
b = t.index('\n', a)
t = t[:a] + "    if (d.qs.length) h += `<section class=\"blk\" id=\"quiz\">${quizHTML(k)}</section>`;" + t[b:]

WRONG = r'''function wrongView(){
  const ids = Object.keys(st.wrong).filter(id => { const [k, i] = id.split('.'); return C[k] && C[k].qs[+i]; });
  if (!ids.length) return `<div class="stack col"><h1>錯題本</h1><div class="card"><p>目前沒有錯題。答錯的題目會自動收進來，之後答對就會移出。</p></div></div>`;
  const by = {};
  ids.forEach(id => { const k = id.split('.')[0]; (by[k] = by[k] || []).push(+id.split('.')[1]); });
  return `<div class="stack col"><h1>錯題本</h1><p class="muted">共 ${ids.length} 題。重新作答，答對的題目會移出錯題本（重新整理頁面後消失）。</p>
  ${SECS.filter(s => by[s.k]).map(s => `<section class="blk stack" style="gap:10px"><h2><a href="#s${s.k}">${SEM[s.b.b]} ${s.no} ${esc(s.t)}</a></h2>${by[s.k].sort((a, b) => a - b).map((i, j) => { const q = C[s.k].qs[i]; return qHTML(s.k, i, q, j + 1, shuffle([...Array(q.o.length).keys()]), null, 'w'); }).join('')}</section>`).join('')}</div>`;
}
'''
t = swap(t, 'function wrongView(){', '\n/* ---------- sidebar ---------- */', WRONG)

ANSWER = r'''/* ---------- answering ---------- */
$('#main').addEventListener('click', e => {
  const btn = e.target.closest('.opts button');
  if (btn) {
    const box = btn.closest('.q');
    if (box.classList.contains('locked')) return;
    const id = box.dataset.q, [k, si] = id.split('.'), i = +si, q = C[k].qs[i], c = +btn.dataset.i, ok = c === q.a, perm = box.dataset.p.split('').map(Number);
    if (!(id in st.first)) st.first[id] = ok;
    if (ok) { st.cor[id] = 1; delete st.wrong[id]; } else st.wrong[id] = 1;
    box.classList.add('locked');
    box.querySelectorAll('.opts button').forEach(b => { const o = +b.dataset.i; b.disabled = true; b.className = o === c ? (ok ? 'ok' : 'no') : (!ok && o === q.a ? 'ans' : ''); });
    const fb = box.querySelector('.fb'); fb.hidden = false; fb.className = 'fb ' + (ok ? 'ok' : 'no'); fb.innerHTML = fbHTML(q, ok, perm);
    if (box.dataset.m === 'r') {
      const r = getRound(k); r.a[i] = {c, ok};
      const {done, ok: okn, all} = roundStat(k);
      const p = $('#qprog'); if (p) p.textContent = progText(done, okn, all);
      st.best[k] = Math.max(st.best[k] || 0, okn);
      if (done === all) {
        if (okn === all) st.done[k] = 1;
        $('#qsum').innerHTML = sumHTML(okn, all);
        if (okn === all) { setTimeout(() => petals('big'), 350); toast(`${all} 題全對！太厲害了！`); }
      }
      renderSide(curKey);
    }
    save();
    if (ok) petals('small', btn.getBoundingClientRect());
    return;
  }
  const z = e.target.closest('.zoom');
  if (z) { $('#figBig').innerHTML = DATA.figs[z.dataset.fig]; figModal.hidden = false; $('#figClose').focus(); return; }
  const nw = e.target.closest('[data-act="new"]');
  if (nw) { const k = location.hash.slice(2); if (!C[k]) return; newRound(k); save(); const box = $('#quiz'); box.innerHTML = quizHTML(k); box.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start'}); }
});

/* ---------- petals ---------- */
const PCOL = ['#ff8fab', '#ffb3c6', '#ffd166', '#f4a261', '#90e0ef', '#b5e48c', '#cdb4db', '#ff6b6b'];
let pcv = null, pctx = null, plist = [], prun = false;
function petals(kind, rect){
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!pcv) { pcv = document.createElement('canvas'); pcv.id = 'petalCv'; pcv.setAttribute('aria-hidden', 'true'); document.body.appendChild(pcv); pctx = pcv.getContext('2d'); }
  const dpr = Math.min(2, window.devicePixelRatio || 1), W = innerWidth, H = innerHeight;
  if (pcv.width !== Math.round(W * dpr) || pcv.height !== Math.round(H * dpr)) { pcv.width = Math.round(W * dpr); pcv.height = Math.round(H * dpr); }
  pctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const mk = (x, y, vx, vy, s) => ({x, y, vx, vy, s, r: Math.random() * 6.28, vr: (Math.random() - .5) * .25, ph: Math.random() * 6.28, c: PCOL[Math.floor(Math.random() * PCOL.length)], t: 0});
  if (kind === 'big') {
    for (let n = 0; n < 170; n++) plist.push(mk(Math.random() * W, -20 - Math.random() * H * .8, (Math.random() - .5) * 1.2, 1 + Math.random() * 2.2, 6 + Math.random() * 6));
    for (let n = 0; n < 40; n++) { const L = n % 2 === 0; plist.push(mk(L ? 10 : W - 10, H - 10, (L ? 1 : -1) * (2 + Math.random() * 4), -(7 + Math.random() * 6), 5 + Math.random() * 5)); }
  } else if (rect) {
    const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
    for (let n = 0; n < 30; n++) { const a = -Math.PI / 2 + (Math.random() - .5) * 2.4, v = 3 + Math.random() * 4.5; plist.push(mk(cx, cy, Math.cos(a) * v, Math.sin(a) * v, 4 + Math.random() * 4)); }
  }
  if (plist.length > 420) plist = plist.slice(-420);
  if (!prun) { prun = true; requestAnimationFrame(pstep); }
}
function pstep(){
  const W = innerWidth, H = innerHeight;
  pctx.clearRect(0, 0, W, H);
  plist = plist.filter(p => p.y < H + 30 && p.t < 420);
  for (const p of plist) {
    p.t++; p.vy = Math.min(p.vy + .07, 2.6); p.vx *= .985; p.x += p.vx + Math.sin(p.t / 18 + p.ph) * .6; p.y += p.vy; p.r += p.vr;
    pctx.save(); pctx.globalAlpha = p.t > 340 ? Math.max(0, (420 - p.t) / 80) : 1; pctx.translate(p.x, p.y); pctx.rotate(p.r);
    pctx.fillStyle = p.c; pctx.beginPath(); pctx.ellipse(0, 0, p.s, p.s * .55, 0, 0, 6.283); pctx.fill(); pctx.restore();
  }
  if (plist.length) requestAnimationFrame(pstep); else { prun = false; pctx.clearRect(0, 0, W, H); }
}
let toastT = 0;
function toast(msg){
  let el = $('#toast'); if (!el) { el = document.createElement('div'); el.id = 'toast'; el.setAttribute('role', 'status'); document.body.appendChild(el); }
  el.textContent = msg; el.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('on'), 2600);
}

'''
t = swap(t, '/* ---------- answering ---------- */', '/* ---------- search ---------- */', ANSWER)

CSS = r'''/* ===== quiz rounds & petals ===== */
.qbar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:-2px 0 12px;font-size:.92rem;color:var(--ink-2)}
.okchip{border-color:transparent;background:var(--ok-soft);color:var(--ok);font-weight:700}
.opts button:disabled{cursor:default;opacity:1;color:inherit}
.opts button.ans{border-color:var(--ok);border-style:dashed}
.q.locked .opts button:not(.ok):not(.no):not(.ans){opacity:.6}
.qsum{margin-top:14px;border-radius:14px;padding:14px 16px;background:var(--bg);display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px}
.qsum b{font-size:1.1rem}
.qsum.win{background:var(--ok-soft)}
.qsum.win b{color:var(--ok);font-size:1.3rem}
.qsum .btn{margin-left:auto}
#petalCv{position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:60}
#toast{position:fixed;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 28px);transform:translate(-50%,20px);opacity:0;pointer-events:none;z-index:61;
  background:var(--ok);color:var(--on-accent);font-weight:700;font-size:1.15rem;padding:12px 24px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.2);transition:opacity .25s,transform .25s}
#toast.on{opacity:1;transform:translate(-50%,0)}
'''
t = t.replace('</style>', CSS + '</style>', 1)
open(P, 'w', encoding='utf-8').write(t)
print('patched', len(t))
