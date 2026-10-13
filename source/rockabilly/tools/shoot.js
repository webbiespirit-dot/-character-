// Usage: node shoot.js <html-file> <out-prefix> [lang]
// Screenshots full page at 375x812 and 1280x900, reports horizontal overflow + console errors.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [file, prefix, lang] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
  const report = {};
  for (const [name, w, h] of [['phone', 375, 812], ['desktop', 1280, 900]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: name === 'phone' ? 2 : 1, locale: lang === 'el' ? 'el-GR' : 'en-GB', timezoneId: 'Asia/Nicosia' });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto('file://' + require('path').resolve(file), { waitUntil: 'networkidle' }).catch(e => errors.push('goto: ' + e));
    await page.waitForTimeout(800);
    const m = await page.evaluate(() => {
      const de = document.documentElement;
      const wide = [...document.querySelectorAll('body *')].filter(el => { const r = el.getBoundingClientRect(); return r.right > de.clientWidth + 1 && getComputedStyle(el).position !== 'fixed'; }).slice(0, 8).map(el => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').join('.') : '')); 
      return { scrollWidth: de.scrollWidth, clientWidth: de.clientWidth, height: de.scrollHeight, overflowingElements: wide, fontsLoaded: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family) };
    });
    await page.screenshot({ path: `${prefix}-${name}.png`, fullPage: true });
    report[name] = { ...m, horizontalOverflow: m.scrollWidth > m.clientWidth, errors };
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(report, null, 1));
})();
