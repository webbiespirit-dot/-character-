// Render the Instagram logo kit from the SVG and the reveal page that scripts/make-logo.py writes.
//
//   node scripts/render-logo.mjs [outdir]        (default: social/logo)
//
// Needs Playwright with Chromium (npm i playwright && npx playwright install chromium) and ffmpeg.
// Writes:
//   profile-1080.png          the profile picture (upload this one)
//   preview-sizes.png         the mark as the circles a phone shows: 320, 150, 110, 64, 40 and 28 px
//   reveal-1080x1920.mp4      the signature writing itself, 9:16 for a Reel or a story (6 s, 30 fps)
//   reveal-1080x1080.mp4      the same, square, for the feed
import { chromium } from 'playwright';
import { mkdtempSync, mkdirSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { execFileSync } from 'node:child_process';

const out = resolve(process.argv[2] || 'social/logo');
mkdirSync(out, { recursive: true });
const svg = readFileSync(join(out, 'w-signature.svg'), 'utf8');
const browser = await chromium.launch();

async function shotSvg(size, file) {
  const page = await browser.newPage({ viewport: { width: size, height: size } });
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}svg{display:block;width:${size}px;height:${size}px}</style>${svg}`, { waitUntil: 'load' });
  await page.screenshot({ path: file });
  await page.close();
}

// the profile picture, plus the size ladder (circle-cropped, as Instagram shows it)
await shotSvg(1080, join(out, 'profile-1080.png'));
{
  const sizes = [320, 150, 110, 64, 40, 28];
  const gap = 36, pad = 48;
  const width = pad * 2 + sizes.reduce((a, b) => a + b, 0) + gap * (sizes.length - 1);
  const height = pad * 2 + 320 + 40;
  let x = pad;
  const cells = sizes.map((s) => {
    const y = pad + (320 - s) / 2;
    const cell = `<div style="position:absolute;left:${x}px;top:${y}px;width:${s}px;height:${s}px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 1px #e1e1e1">${svg.replace('<svg ', `<svg style="width:${s}px;height:${s}px" `)}</div>
      <div style="position:absolute;left:${x}px;top:${pad + 320 + 12}px;width:${s}px;text-align:center;font:12px system-ui;color:#777">${s}</div>`;
    x += s + gap;
    return cell;
  });
  const page = await browser.newPage({ viewport: { width, height } });
  await page.setContent(`<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff;position:relative;width:${width}px;height:${height}px">${cells.join('')}</body>`, { waitUntil: 'load' });
  await page.screenshot({ path: join(out, 'preview-sizes.png') });
  await page.close();
}

// the reveal: scrub the page's animations frame by frame, then let ffmpeg join them
async function video(width, height, file, fps = 30, seconds = 6) {
  const dir = mkdtempSync(join(tmpdir(), 'ws-reveal-'));
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto('file://' + join(out, 'reveal.html'), { waitUntil: 'load' });
  await page.evaluate(() => { for (const a of document.getAnimations()) a.pause(); });
  const n = fps * seconds;
  for (let i = 0; i < n; i++) {
    await page.evaluate((t) => { for (const a of document.getAnimations()) a.currentTime = t; }, (i / fps) * 1000);
    await page.screenshot({ path: join(dir, `f${String(i).padStart(4, '0')}.png`) });
  }
  await page.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', join(dir, 'f%04d.png'),
    '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', file]);
  rmSync(dir, { recursive: true, force: true });
  console.log('wrote', file);
}
await video(1080, 1920, join(out, 'reveal-1080x1920.mp4'));
await video(1080, 1080, join(out, 'reveal-1080x1080.mp4'));
await browser.close();
console.log('wrote', join(out, 'profile-1080.png'), 'and', join(out, 'preview-sizes.png'));
