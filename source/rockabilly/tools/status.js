const { chromium } = require('/opt/node-tools/node_modules/playwright');
const file = 'file://' + process.argv[2];
const cases = [['Mon 12:00','2026-10-12T12:00:00+03:00'],['Tue 09:00','2026-10-13T09:00:00+03:00'],['Tue 10:00','2026-10-13T10:00:00+03:00'],['Tue 19:30','2026-10-13T19:30:00+03:00'],['Sat 08:30','2026-10-17T08:30:00+03:00'],['Sat 15:59','2026-10-17T15:59:00+03:00'],['Sat 16:00','2026-10-17T16:00:00+03:00'],['Sun 12:00','2026-10-18T12:00:00+03:00']];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const lang of ['en-GB','el-GR']) for (const [label, iso] of cases) {
    const ctx = await b.newContext({ locale: lang, timezoneId: 'America/New_York' }); // device tz deliberately wrong: logic must use Cyprus time
    const p = await ctx.newPage();
    await p.clock.setFixedTime(new Date(iso));
    await p.goto(file);
    const r = await p.evaluate(() => {
      const badge = document.querySelector('[class*="status"], #status, .badge');
      const today = document.querySelector('.today, [aria-current], tr.is-today, li.is-today');
      return { badge: badge && badge.textContent.replace(/\s+/g,' ').trim(), today: today && today.textContent.replace(/\s+/g,' ').trim().slice(0,40) };
    });
    console.log(lang, label, '|', r.badge, '|', r.today);
    await ctx.close();
  }
  await b.close();
})();
