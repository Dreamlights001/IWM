(() => {
  const D = JSON.parse(document.getElementById('board-data').textContent);
  const svg = document.getElementById('map');
  const ov = document.getElementById('overlay');
  const drawer = document.getElementById('drawer');
  const body = drawer.querySelector('.body');
  const dtitle = drawer.querySelector('.dt');
  const NS = 'http://www.w3.org/2000/svg';
  const CIRC = '①②③④⑤⑥';

  function closeDrawer() { drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); }
  function openDrawer(html, title) {
    body.innerHTML = html; body.scrollTop = 0; dtitle.textContent = title;
    drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false');
  }
  function clear(keepDrawer) {
    svg.classList.remove('focus');
    svg.querySelectorAll('.card').forEach(c => c.classList.remove('sel', 'up', 'down', 'inloop'));
    svg.querySelectorAll('.loop').forEach(p => p.classList.remove('on'));
    ov.replaceChildren();
    if (!keepDrawer) { closeDrawer(); history.replaceState(null, '', location.pathname); }
  }
  function edgePath(s, d) {
    const [sx, sy, sw, sh] = D.geom[s], [dx, dy, dw, dh] = D.geom[d];
    let x1, y1, x2, y2, vertical = true;
    if (dy >= sy + sh) { x1 = sx + sw / 2; y1 = sy + sh; x2 = dx + dw / 2; y2 = dy; }
    else if (dy + dh <= sy) { x1 = sx + sw / 2; y1 = sy; x2 = dx + dw / 2; y2 = dy + dh; }
    else { vertical = false; y1 = sy + sh / 2; y2 = dy + dh / 2; if (dx > sx) { x1 = sx + sw; x2 = dx; } else { x1 = sx; x2 = dx + dw; } }
    if (vertical) { const m = (y2 - y1) / 2; return `M${x1} ${y1} C${x1} ${y1 + m} ${x2} ${y2 - m} ${x2} ${y2}`; }
    const m = (x2 - x1) / 2; return `M${x1} ${y1} C${x1 + m} ${y1} ${x2 - m} ${y2} ${x2} ${y2}`;
  }
  function line(s, d, cls) {
    const e = document.createElementNS(NS, 'path');
    e.setAttribute('d', edgePath(s, d)); e.setAttribute('class', 'ov ' + cls); e.setAttribute('marker-end', 'url(#ah-g)');
    ov.appendChild(e);
  }
  function select(w) {
    if (!D.works[w]) return;
    clear(true); svg.classList.add('focus');
    document.getElementById('c-' + w).classList.add('sel');
    D.edges.forEach(([s, d]) => {
      if (s === w) { document.getElementById('c-' + d).classList.add('down'); line(s, d, 'down'); }
      if (d === w) { document.getElementById('c-' + s).classList.add('up'); line(s, d, 'up'); }
    });
    openDrawer(D.works[w].html, w + ' ' + D.works[w].name);
    history.replaceState(null, '', '#' + w);
  }
  function selectLoop(n) {
    if (!D.loops[n]) return;
    clear(true); svg.classList.add('focus');
    D.loops[n].members.forEach(m => document.getElementById('c-' + m).classList.add('inloop'));
    svg.querySelectorAll(`.loop[data-loop="${n}"]`).forEach(p => p.classList.add('on'));
    openDrawer(D.loops[n].html, '闭环 ' + CIRC[n - 1]);
    history.replaceState(null, '', '#loop' + n);
  }
  document.addEventListener('click', e => {
    const card = e.target.closest('.card');
    if (card) { select(card.dataset.w); return; }
    const badge = e.target.closest('.loopbadge, [data-loopchip]');
    if (badge) { e.preventDefault(); selectLoop(+(badge.dataset.loop || badge.dataset.loopchip)); return; }
    const a = e.target.closest('a.wref');
    if (a) {
      e.preventDefault(); select(a.dataset.w);
      if (!drawer.contains(a)) svg.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    if (e.target.closest('#drawer .x') || (svg.contains(e.target) && !e.target.closest('a'))) clear();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') clear();
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('.card, .loopbadge')) {
      e.preventDefault(); e.target.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }
  });
  function fromHash() {
    const h = decodeURIComponent(location.hash.slice(1));
    if (/^W\d\d$/.test(h)) select(h);
    else if (/^loop\d$/.test(h)) selectLoop(+h.slice(4));
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
