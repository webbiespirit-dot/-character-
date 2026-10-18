// Build src/data/clips.json from raw/*/meta.json
import fs from 'node:fs'; import path from 'node:path';
const out = {};
for (const id of fs.readdirSync('raw')) {
  const mp = path.join('raw', id, 'meta.json'); if (!fs.existsSync(mp)) continue;
  const m = JSON.parse(fs.readFileSync(mp, 'utf8'));
  out[id] = { hero: `raw/${id}/hero.mp4`, cta: `raw/${id}/cta.mp4`, scroll: `raw/${id}/scroll.mp4`, before: `raw/${id}/before.png`,
    heroFrames: m.clips.hero?.frames ?? 0, scrollFrames: m.clips.scroll?.frames ?? 0, ctaFrames: m.clips.cta?.frames ?? 0,
    pressFrame: m.clips.cta?.pressFrame ?? 0, target: m.clips.cta?.target ?? { x: 585, y: 1800 }, pageHeight: m.pageHeight };
}
fs.mkdirSync('src/data', { recursive: true });
fs.writeFileSync('src/data/clips.json', JSON.stringify(out, null, 1));
console.log('manifest:', Object.keys(out).join(', '));
