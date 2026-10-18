import { chromium } from 'playwright';
const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
for (const [id, url] of [['moxie-hair', 'https://webbiespirit.com/demo/moxie-hair/'], ['kafenio11', 'https://webbiespirit.com/demo/kafenio11/'], ['k2fit', 'https://webbiespirit.com/demo/k2fit/'], ['adams', 'https://webbiespirit.com/demo/adams/']]) {
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(2500);
  const rows = await page.evaluate(() => [...document.querySelectorAll('a,button')].map((el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return { tag: el.tagName, cls: el.className?.toString().slice(0, 40), text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30), top: Math.round(r.top), w: Math.round(r.width), vis: cs.visibility !== 'hidden' && cs.display !== 'none' && r.width > 0 && cs.opacity !== '0' }; }).filter((x) => /book|call|κλείσε|find|order|cup/i.test(x.text)));
  console.log(id, JSON.stringify(rows));
  await page.close();
}
await browser.close();
