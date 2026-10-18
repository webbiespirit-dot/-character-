// Per-demo capture configs. `prepare` runs after load: it swaps business names for neutral words
// (the agency did not do business with these shops), leaving the design untouched.
const setText = (sel, text) => [sel, text];
const run = async (page, edits) => page.evaluate((edits) => {
  for (const [sel, text] of edits) for (const el of document.querySelectorAll(sel)) {
    if (text === null) { el.remove(); continue; }
    // keep child elements (icons, <small>), replace only direct text nodes
    const textNodes = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim());
    if (textNodes.length) { textNodes[0].textContent = text; for (const n of textNodes.slice(1)) n.textContent = ''; } else el.textContent = text;
  }
}, edits);

export const SITES = [
  {
    id: 'hoa', label: 'Nail & lash studio', url: 'https://webbiespirit.com/demo/hoa/', cta: '.hero-actions .btn-light', settleMs: 3000,
    prepare: async (page) => run(page, [
      setText('.wordmark b', 'Nails'), setText('.wordmark span', 'Nail & Eyelash Studio'), setText('h1.hero__title, h1#hero-title', 'Nail Studio'),
      setText('.site-footer .wrap span:first-child', 'Nail & Eyelash Studio, Larnaca'),
      setText('.team', 'Booking is recommended. Call, or send a message on Instagram.'),
    ]).then(() => page.evaluate(() => { for (const b of document.querySelectorAll('.quotes blockquote')) b.textContent = b.textContent.replace('Hoa is', 'She is'); })),
  },
  {
    id: 'briki', label: 'Coffee chain', url: 'https://briki.webbiespirit.com/', cta: 'a.btn--copper:has-text("Find your cup")', settleMs: 3500, scrollMax: 9000, scrollFrames: 170,
  },
  {
    id: 'bowtie', label: 'Barbershop', url: 'https://webbiespirit.com/demo/bowtie/', cta: '#heroCtas .btn-primary', settleMs: 3000,
    prepare: async (page) => { await page.evaluate(() => {
      const letters = 'BARBER'.split('');
      document.querySelectorAll('.letters .ch').forEach((el, i) => { el.querySelector('svg')?.remove(); el.textContent = letters[i] ?? el.textContent; el.classList.remove('ch-o'); });
      const set = (sel, t) => document.querySelectorAll(sel).forEach((el) => { el.textContent = t; });
      set('.mark', 'Barber'); set('.plaque', 'Larnaca'); set('#regTitle', 'The regulars'); set('#findTitle', 'Find the shop');
      set('.motto small', "From the shop's Instagram"); set('footer strong', 'Demo site by Webbiespirit');
      set('.ring-src', 'Photos from the shop’s Google Maps listing.');
      document.querySelectorAll('.ring-cap').forEach((el) => { el.textContent = el.textContent.replace(/The Bowtie Barbers/g, 'The barbershop').replace(/Bowtie’s|Bowtie's/g, 'the shop’s').replace(/Bowtie/g, 'Barber'); });
      const intro = document.querySelector('.reg-intro p'); if (intro) intro.textContent = 'Across the Google reviews the same things keep coming up: a friendly barber, sharp fades and clean lines, good music and real conversation while you wait.';
      document.querySelectorAll('.quotes blockquote').forEach((b) => { b.textContent = b.textContent.replace(' Highly recommend Pany.', ' Highly recommend.'); });
      document.querySelectorAll('.hero-copy .btn-primary, .bar .btn-primary').forEach((b) => { const n = [...b.childNodes].find((n) => n.nodeType === 3); if (n) n.textContent = 'Call to book'; });
    });
      await replaceText(page, [['The Bowtie Barbers', 'The barbershop'], ['Bowtie’s', 'the shop’s'], ["Bowtie's", "the shop's"], ['Bowtie Barbers', 'the barbershop'], ['Bowtie', 'Barber']]);
    },
  },
  {
    id: 'adams', label: 'Old-town barber', url: 'https://webbiespirit.com/demo/adams/', cta: '.hero .ctas .btn.solid', settleMs: 3000, canvasDpr: 1, rafThrottleMs: 120, scrollFrames: 170,
    prepare: async (page) => page.evaluate(() => {
      const set = (sel, t) => document.querySelectorAll(sel).forEach((el) => { el.textContent = t; });
      set('nav .word', 'Κουρείο');
      const l2 = document.querySelector('h1 .l:nth-child(2) span'); if (l2) l2.textContent = 'ΛΑΡΝΑΚΑ';
      set('.addr', 'Old town, Larnaca 6026');
      const lead = document.querySelector('.story .lead'); if (lead) lead.textContent = "The owner's grandfather opened this shop fifty years ago. The hand-painted sign has come down; the doors and the chairs stayed. Tap the card to turn it over.";
      document.querySelectorAll('footer.site span:first-child').forEach((el) => { el.textContent = 'Old-town barber, Larnaca'; });
      document.querySelectorAll('.hero .ctas .btn.solid').forEach((b) => { const n = [...b.childNodes].find((n) => n.nodeType === 3); if (n) n.textContent = 'Call the shop'; });
    }),
  },
];

// Generic text-node replacer for names that appear in many places.
const replaceText = (page, map) => page.evaluate((map) => {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const n of nodes) { let t = n.textContent; for (const [a, b] of map) t = t.split(a).join(b); if (t !== n.textContent) n.textContent = t; }
}, map);


// Replace a word that a site splits into one span per letter (for staggered reveals). Same length only.
// Tolerates extra non-letter children such as a trailing full stop ("M O X I E .").
const replaceLetters = (page, from, to) => page.evaluate(([from, to]) => {
  const cands = [...document.querySelectorAll('h1, h2, .word, .display, [class*=title], [class*=word], [class*=brand], [class*=logo], span, div')];
  for (const el of cands) {
    const kids = [...el.children];
    if (kids.length < from.length || kids.length > from.length + 2) continue;
    const letters = kids.filter((k) => /\p{L}/u.test(k.textContent));
    if (letters.length !== from.length) continue;
    if (letters.map((k) => k.textContent.trim()).join('') !== from) continue;
    letters.forEach((k, i) => { const n = [...k.childNodes].find((n) => n.nodeType === 3 && n.textContent.trim()); if (n) n.textContent = n.textContent.replace(from[i], to[i]); else k.textContent = to[i]; });
  }
}, [from, to]);

export const EXTRAS = [
  {
    id: 'moxie-hair', scrollFrames: 170, label: 'Hair salon', url: 'https://webbiespirit.com/demo/moxie-hair/', cta: 'button.btn-primary:has-text("Book a cut")', settleMs: 3000,
    prepare: async (page) => { await replaceText(page, [['MOXIE', 'SALON'], ['Moxie', 'Salon'], ['moxie', 'salon'], ['M O X I E', 'S A L O N']]); await replaceLetters(page, 'MOXIE', 'SALON'); },
  },
  {
    id: 'kafenio11', scrollFrames: 170, label: 'Café-bar', url: 'https://webbiespirit.com/demo/kafenio11/', cta: 'a.btn-call', settleMs: 3000,
    prepare: async (page) => { await replaceText(page, [['Kafenio 11', 'Kafenio'], ['ΚΑΦΕΝΕΙΟ 11', 'ΚΑΦΕΝΕΙΟ'], ['Καφενείο 11', 'Καφενείο'], ['kafenio11', 'kafenio'], ['Kafeneio11', 'Kafeneio']]);
      // the number sits in its own element next to the word in the header mark
      // the number sits in its own element or text node next to the word (header mark, vinyl label "ΚΑΦΕΝΕΙΟ<br>11")
      await page.evaluate(() => {
        for (const el of document.querySelectorAll('body *')) { if (el.children.length === 0 && el.textContent.trim() === '11') el.textContent = ''; }
        const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
        for (const n of nodes) if (n.textContent.trim() === '11') n.textContent = '';
      });
    },
  },
  {
    id: 'k2fit', scrollFrames: 170, label: 'Fitness studio', url: 'https://webbiespirit.com/demo/k2fit/', cta: 'a.btn:has-text("Κλείσε δωρεάν")', settleMs: 3000,
    prepare: (page) => replaceText(page, [['K2FIT', 'FIT STUDIO'], ['K2 FIT', 'FIT STUDIO'], ['k2fit', 'fitstudio'], ['K2Fit', 'Fit Studio']]),
  },
];
