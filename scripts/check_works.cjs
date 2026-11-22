// 检查 works/research_board.html：无脚本错误、卡片文字不越界、标签不压卡片、交互可用、窄屏不横向溢出。
const path = require('path');
const assert = require('assert');
const { chromium } = require('/home/dlts/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '..');
const url = 'file://' + path.join(root, 'works/research_board.html');
const shot = n => path.join(root, 'qa', 'works-' + n + '.png');

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(url); await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: shot('desktop-top') });
  await page.locator('.mapwrap').screenshot({ path: shot('map') });

  const geo = await page.evaluate(() => {
    const out = { overflow: [], overlap: [], vertical: [] };
    const cards = [...document.querySelectorAll('#map .card')].map(g => ({ id: g.dataset.w, r: g.querySelector('.card-bg').getBBox(), texts: [...g.querySelectorAll('text')] }));
    for (const c of cards) for (const t of c.texts) {
      const b = t.getBBox();
      if (b.x + b.width > c.r.x + c.r.width - 4 || b.y + b.height > c.r.y + c.r.height + 1) out.overflow.push(`${c.id}: ${t.textContent}`);
    }
    const hit = (a, b) => a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height;
    for (const t of document.querySelectorAll('#map .hlab, #map .llab, #map .vlab')) {
      const b = t.getBBox();
      for (const c of cards) if (hit(b, c.r)) out.overlap.push(`${t.textContent} × ${c.id}`);
      if (t.classList.contains('vlab')) out.vertical.push([t.textContent.slice(0, 8), Math.round(b.width), Math.round(b.height)]);
    }
    return out;
  });
  console.log('card text overflow:', geo.overflow);
  console.log('label/card overlap:', geo.overlap);
  console.log('vertical labels (w,h):', JSON.stringify(geo.vertical));

  await page.locator('#c-W10').click();
  await page.waitForTimeout(300);
  const st = await page.evaluate(() => ({
    open: document.getElementById('drawer').classList.contains('open'),
    ov: document.querySelectorAll('#overlay path').length,
    up: document.querySelectorAll('.card.up').length, down: document.querySelectorAll('.card.down').length,
    title: document.querySelector('#drawer .dt').textContent, hash: location.hash,
  }));
  console.log('select W10:', JSON.stringify(st));
  assert(st.open && st.ov === st.up + st.down && st.hash === '#W10');
  await page.screenshot({ path: shot('select-W10') });
  await page.locator('#drawer .rel a.wref').first().click();
  await page.waitForTimeout(200);
  console.log('chip in drawer ->', await page.locator('#drawer .dt').textContent());
  await page.locator('#map .loopbadge[data-loop="1"]').first().click();
  await page.waitForTimeout(300);
  const lp = await page.evaluate(() => ({ inloop: document.querySelectorAll('.card.inloop').length, on: document.querySelectorAll('.loop.on').length, t: document.querySelector('#drawer .dt').textContent }));
  console.log('loop 1:', JSON.stringify(lp));
  assert(lp.inloop > 0 && lp.on > 0);
  await page.screenshot({ path: shot('loop1') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  assert(!(await page.evaluate(() => document.getElementById('drawer').classList.contains('open'))));
  await page.locator('#loops').scrollIntoViewIfNeeded();
  await page.screenshot({ path: shot('loops') });
  await page.locator('#cross').scrollIntoViewIfNeeded();
  await page.screenshot({ path: shot('cross') });
  const dw = await page.evaluate(() => ({ vw: innerWidth, sw: document.documentElement.scrollWidth }));
  assert(dw.sw <= dw.vw, 'desktop horizontal overflow');

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('about:blank'); await page.goto(url + '#W05'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
  assert(await page.evaluate(() => document.getElementById('drawer').classList.contains('open')), 'hash 打开抽屉');
  await page.screenshot({ path: shot('mobile-drawer') });
  await page.keyboard.press('Escape');
  await page.screenshot({ path: shot('mobile-top') });
  const mw = await page.evaluate(() => ({ vw: innerWidth, sw: document.documentElement.scrollWidth, map: document.querySelector('.mapwrap').scrollWidth }));
  console.log('mobile widths:', JSON.stringify(mw));
  assert(mw.sw <= mw.vw, 'mobile horizontal overflow');
  console.log('errors:', errors);
  assert.equal(errors.length, 0);
  await browser.close();
  console.log('OK');
})().catch(e => { console.error(e); process.exit(1); });
