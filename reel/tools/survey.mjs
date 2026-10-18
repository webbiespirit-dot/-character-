// Survey candidate demos: hero screenshot, full-page thumbnail, CTA candidates, title.
import { chromium } from 'playwright';
import fs from 'node:fs';
const BASE = 'https://webbiespirit.com/demo/';
const ids = process.argv.slice(2);
const browser = await chromium.launch({ headless: true, args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] });
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, locale: 'en-GB' });
fs.mkdirSync('out/survey', { recursive: true });
const report = [];
for (const id of ids) {
  const url = id === 'briki' ? 'https://briki.webbiespirit.com/' : BASE + id + '/';
  const page = await ctx.newPage();
  const t0 = Date.now();
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(2500);
    const info = await page.evaluate(() => {
      const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 20 && r.height > 20 && r.top < innerHeight * 1.2 && getComputedStyle(el).visibility !== 'hidden'; };
      const ctas = [...document.querySelectorAll('a,button')].filter(vis).map((el) => {
        const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return { text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40), href: el.getAttribute('href') || '', cls: el.className?.toString().slice(0, 60), id: el.id, top: Math.round(r.top), left: Math.round(r.left), w: Math.round(r.width), h: Math.round(r.height), bg: cs.backgroundColor, color: cs.color };
      }).filter((c) => c.text && c.h >= 36 && c.w >= 80).slice(0, 10);
      return { title: document.title, theme: document.querySelector('meta[name=theme-color]')?.content, h1: document.querySelector('h1')?.textContent?.trim().replace(/\s+/g, ' ').slice(0, 80), height: document.documentElement.scrollHeight, fonts: [...document.fonts].map((f) => f.family).filter((v, i, a) => a.indexOf(v) === i).slice(0, 6), ctas };
    });
    await page.screenshot({ path: `out/survey/${id}-hero.png` });
    await page.screenshot({ path: `out/survey/${id}-full.png`, fullPage: true });
    report.push({ id, url, ms: Date.now() - t0, ...info });
    console.log(id, 'ok', info.title, '|', info.height + 'px', '| ctas:', info.ctas.slice(0, 4).map((c) => `${c.text}[${c.cls || c.id}@${c.top}]`).join(' ; '));
  } catch (e) { console.log(id, 'FAILED', e.message.slice(0, 120)); report.push({ id, url, error: e.message }); }
  await page.close();
}
fs.writeFileSync('out/survey/report.json', JSON.stringify(report, null, 1));
await browser.close();
