// Re-shoot the unstyled "before" screenshots with the name swaps applied.
import { chromium } from 'playwright';
import path from 'node:path';
const { SITES, EXTRAS } = await import(path.resolve('tools/sites.mjs'));
const ids = process.argv.slice(2);
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, locale: 'en-GB' });
for (const cfg of [...SITES, ...EXTRAS]) {
  if (ids.length && !ids.includes(cfg.id)) continue;
  const p2 = await context.newPage();
  await p2.route('**/*', (route) => { const t = route.request().resourceType(); return (t === 'stylesheet' || t === 'font') ? route.abort() : route.continue(); });
  await p2.goto(cfg.url, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
  await p2.waitForTimeout(1500);
  if (cfg.prepare) await cfg.prepare(p2).catch((e) => console.log(cfg.id, 'prepare failed', e.message));
  await p2.evaluate(() => {
    for (const el of document.querySelectorAll('style, link[rel=stylesheet]')) el.remove();
    for (const el of document.querySelectorAll('[style]')) el.removeAttribute('style');
    for (const el of document.querySelectorAll('canvas, video, script')) el.remove();
    window.scrollTo(0, 0);
  });
  await p2.waitForTimeout(400);
  await p2.screenshot({ path: path.join('raw', cfg.id, 'before.png'), type: 'png' });
  console.log(cfg.id, 'before.png re-shot');
  await p2.close();
}
await browser.close();
