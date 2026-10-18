// Frame-by-frame phone captures with Playwright. Deterministic 30 fps motion: we drive scroll and the
// pointer ourselves per frame; CSS animations are slowed with CDP Animation.setPlaybackRate so that the
// real time between screenshots maps to ~1 frame of site time. Output: PNG frame sequences + mp4 clips.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const FPS = 30;
const VIEW = { width: 390, height: 844 };
const DSF = 3;
const OUT = path.resolve('raw');

const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);      // strong in-out
const easeOut = (t) => 1 - Math.pow(1 - t, 3);
const expoOut = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));
const lerp = (a, b, t) => a + (b - a) * t;

async function frameLoop(page, dir, n, step, opts = {}) {
  fs.mkdirSync(dir, { recursive: true });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    await step(i, i / Math.max(1, n - 1));
    await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
    await page.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95, animations: 'allow', caret: 'hide' });
  }
  const ms = (Date.now() - t0) / n;
  return ms;
}

function toMp4(dir, out) {
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
}

const CURSOR_CSS = `
#ws-cursor{position:fixed;left:0;top:0;z-index:2147483647;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;
  background:rgba(255,255,255,.28);box-shadow:0 0 0 2px rgba(255,255,255,.85),0 6px 18px rgba(0,0,0,.35);pointer-events:none;
  transform:translate3d(var(--x,0px),var(--y,0px),0) scale(var(--s,1));opacity:var(--o,0);will-change:transform;transition:none}
#ws-cursor::after{content:"";position:absolute;inset:14px;border-radius:50%;background:rgba(255,255,255,.95)}
#ws-ripple{position:fixed;left:0;top:0;z-index:2147483646;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;
  border:2px solid rgba(255,255,255,.9);pointer-events:none;opacity:var(--ro,0);transform:translate3d(var(--x,0px),var(--y,0px),0) scale(var(--rs,1))}
`;

async function installCursor(page) {
  await page.addStyleTag({ content: CURSOR_CSS });
  await page.evaluate(() => {
    for (const id of ['ws-ripple', 'ws-cursor']) { if (!document.getElementById(id)) { const d = document.createElement('div'); d.id = id; document.body.appendChild(d); } }
  });
}
async function setCursor(page, x, y, { s = 1, o = 1, ripple = 0, rippleScale = 1 } = {}) {
  await page.evaluate(([x, y, s, o, ro, rs]) => {
    const c = document.getElementById('ws-cursor'); const r = document.getElementById('ws-ripple');
    for (const el of [c, r]) { el.style.setProperty('--x', x + 'px'); el.style.setProperty('--y', y + 'px'); }
    c.style.setProperty('--s', s); c.style.setProperty('--o', o);
    r.style.setProperty('--ro', ro); r.style.setProperty('--rs', rs);
  }, [x, y, s, o, ripple, rippleScale]);
}

// Human-ish pointer path: eased, with a slight curve (control point offset) and tiny tremor.
function pointerPath(from, to, n, seed = 1) {
  const pts = [];
  const cx = (from.x + to.x) / 2 + (to.y - from.y) * 0.12 * (seed % 2 ? 1 : -1);
  const cy = (from.y + to.y) / 2 - (to.x - from.x) * 0.12;
  for (let i = 0; i < n; i++) {
    const t = easeInOut(i / (n - 1));
    const x = (1 - t) * (1 - t) * from.x + 2 * (1 - t) * t * cx + t * t * to.x;
    const y = (1 - t) * (1 - t) * from.y + 2 * (1 - t) * t * cy + t * t * to.y;
    const tremor = Math.sin(i * 1.7 + seed) * 0.6 * (1 - t);
    pts.push({ x: x + tremor, y: y + tremor * 0.7 });
  }
  return pts;
}

export async function captureSite(cfg) {
  const browser = await chromium.launch({ headless: true, args: ['--disable-gpu-vsync', '--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] });
  const context = await browser.newContext({ viewport: VIEW, deviceScaleFactor: DSF, isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1', colorScheme: 'light', reducedMotion: 'no-preference', locale: 'en-GB', timezoneId: 'Asia/Nicosia' });
  // WebGL pages render their canvases at devicePixelRatio; under software GL at 3x that can take seconds per frame.
  // Cap what scripts see (CSS and screenshots stay at 3x), so three.js canvases render at a lighter ratio.
  const canvasDpr = cfg.canvasDpr ?? 1.5;
  await context.addInitScript((dpr) => { try { Object.defineProperty(window, 'devicePixelRatio', { get: () => dpr, configurable: true }); } catch (e) {} }, canvasDpr);
  // Some WebGL pages render back-to-back on requestAnimationFrame and starve the main thread under software GL.
  // Throttle rAF so the page still animates (time-based) but leaves room for screenshots.
  if (cfg.rafThrottleMs) {
    await context.addInitScript((ms) => {
      const raf = window.requestAnimationFrame.bind(window);
      let last = 0;
      window.requestAnimationFrame = (cb) => { const now = performance.now(); const wait = Math.max(0, ms - (now - last)); return setTimeout(() => { last = performance.now(); raf(cb); }, wait); };
      window.cancelAnimationFrame = (id) => clearTimeout(id);
    }, cfg.rafThrottleMs);
  }
  const page = await context.newPage();
  page.setDefaultTimeout(120000);
  const cdp = await context.newCDPSession(page);
  await cdp.send('Animation.enable');
  const log = (m) => console.log(`[${cfg.id}] ${m}`);
  try { return await captureInner(cfg, { browser, context, page, cdp, log }); } finally { await browser.close().catch(() => {}); }
}
async function captureInner(cfg, { browser, context, page, cdp, log }) {
  const dir = path.join(OUT, cfg.id);
  fs.mkdirSync(dir, { recursive: true });
  const meta = { id: cfg.id, url: cfg.url, viewport: VIEW, dsf: DSF, fps: FPS, clips: {} };

  // ---- load
  await page.goto(cfg.url, { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(cfg.settleMs ?? 2500);
  if (cfg.prepare) await cfg.prepare(page);
  await page.evaluate(async () => { if (document.fonts) await document.fonts.ready; });
  const pageH = await page.evaluate(() => Math.max(document.documentElement.scrollHeight, document.body.scrollHeight));
  meta.pageHeight = pageH;
  log(`loaded, page height ${pageH}`);

  // ---- 0. "before": the same page with styles stripped (for the split before/after)
  if (cfg.before !== false) {
    const html = await page.content();
    const p2 = await context.newPage();
    await p2.route('**/*', (route) => {
      const t = route.request().resourceType();
      if (t === 'stylesheet' || t === 'font') return route.abort();
      return route.continue();
    });
    await p2.goto(cfg.url, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(() => {});
    await p2.waitForTimeout(1500);
    if (cfg.prepare) await cfg.prepare(p2).catch(() => {});
    await p2.evaluate(() => {
      for (const el of document.querySelectorAll('style, link[rel=stylesheet]')) el.remove();
      for (const el of document.querySelectorAll('[style]')) el.removeAttribute('style');
      for (const el of document.querySelectorAll('canvas, video, script')) el.remove();
      window.scrollTo(0, 0);
    });
    await p2.waitForTimeout(400);
    await p2.screenshot({ path: path.join(dir, 'before.png'), type: 'png' });
    await p2.close();
    log('before.png');
  }

  // ---- 1. hero hold: reload so the site's own load choreography plays, slowed to real-time per frame
  {
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 1 });
    await page.goto(cfg.url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.evaluate(async () => { if (document.fonts) await document.fonts.ready; });
    const n = cfg.heroFrames ?? 90;   // 3 s
    const frameMs = 1000 / FPS;
    // We time-slice: each loop iteration lets ~frameMs of site time pass by slowing animations
    // to match our real screenshot cadence (measured on the fly).
    let rate = 0.12; await cdp.send('Animation.setPlaybackRate', { playbackRate: rate });
    if (cfg.prepare) await cfg.prepare(page);
    await installCursor(page);
    const d = path.join(dir, 'hero'); fs.mkdirSync(d, { recursive: true });
    let last = Date.now();
    for (let i = 0; i < n; i++) {
      await page.evaluate(() => new Promise((r) => requestAnimationFrame(r)));
      await page.screenshot({ path: path.join(d, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95, animations: 'allow', caret: 'hide' });
      const now = Date.now(); const real = Math.max(40, now - last); last = now;
      rate = Math.min(1, Math.max(0.05, frameMs / real));
      await cdp.send('Animation.setPlaybackRate', { playbackRate: rate });
    }
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 1 });
    toMp4(d, path.join(dir, 'hero.mp4'));
    meta.clips.hero = { frames: n };
    log(`hero.mp4 (${n} frames)`);
  }
  await page.waitForTimeout(1200);

  // ---- 2. CTA tap: pointer eases in, presses, releases
  if (cfg.cta) {
    const el = page.locator(cfg.cta).filter({ visible: true }).first();
    await el.waitFor({ state: 'visible', timeout: 10000 });
    const box = await el.boundingBox();
    const target = { x: box.x + box.width * 0.52, y: box.y + box.height * 0.5 };
    const from = { x: VIEW.width * 0.78, y: VIEW.height * 0.92 };
    const approach = 26, hold = 6, release = 14, settle = 14;   // frames
    const n = approach + hold + release + settle;
    const pts = pointerPath(from, target, approach, 3);
    const d = path.join(dir, 'cta');
    let pressed = false;
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 0.2 });
    await frameLoop(page, d, n, async (i) => {
      if (i < approach) {
        const p = pts[i]; await page.mouse.move(p.x, p.y);
        await setCursor(page, p.x, p.y, { o: Math.min(1, i / 5), s: 1 });
      } else if (i < approach + hold) {
        if (!pressed) { await page.mouse.move(target.x, target.y); await page.mouse.down(); pressed = true; }
        const k = (i - approach) / hold;
        await setCursor(page, target.x, target.y, { s: lerp(1, 0.8, easeOut(k)), ripple: 0.9 * (1 - k * 0.3), rippleScale: lerp(1, 1.6, k) });
      } else if (i < approach + hold + release) {
        if (pressed) { await page.mouse.up(); pressed = false; }
        const k = (i - approach - hold) / release;
        await setCursor(page, target.x, target.y, { s: lerp(0.8, 1, expoOut(k)), ripple: 0.9 * (1 - k), rippleScale: lerp(1.6, 2.6, k) });
      } else {
        const k = (i - approach - hold - release) / settle;
        await setCursor(page, target.x, target.y, { o: 1 - k, s: 1 });
      }
    });
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 1 });
    toMp4(d, path.join(dir, 'cta.mp4'));
    meta.clips.cta = { frames: n, pressFrame: approach, target: { x: target.x * DSF, y: target.y * DSF }, box: { x: box.x * DSF, y: box.y * DSF, w: box.width * DSF, h: box.height * DSF } };
    log(`cta.mp4 (${n} frames), target ${Math.round(target.x)},${Math.round(target.y)}`);
    await setCursor(page, 0, 0, { o: 0 });
  }

  // ---- 3. smooth eased full-page scroll (top -> bottom), with scroll-driven effects playing
  {
    const maxY = Math.max(0, Math.min(pageH - VIEW.height, cfg.scrollMax ?? 1e9));
    const n = cfg.scrollFrames ?? 240;   // 8 s
    const d = path.join(dir, 'scroll');
    // fresh load: a CTA tap may have opened a sheet or dialog
    await page.goto(cfg.url, { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(cfg.settleMs ?? 2500);
    if (cfg.prepare) await cfg.prepare(page);
    await page.evaluate(async () => { if (document.fonts) await document.fonts.ready; window.scrollTo(0, 0); });
    await page.waitForTimeout(600);
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 0.2 });
    const ms = await frameLoop(page, d, n, async (i, t) => {
      // ease in-out with a brief pause plateau in the middle to feel human (thumb lifts)
      let e = easeInOut(t);
      const y = Math.round(lerp(0, maxY, e));
      await page.evaluate((y) => window.scrollTo(0, y), y);
      await page.mouse.move(VIEW.width * 0.5, VIEW.height * 0.55 + Math.sin(i / 7) * 6);
    });
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 1 });
    toMp4(d, path.join(dir, 'scroll.mp4'));
    meta.clips.scroll = { frames: n, maxY, msPerFrame: Math.round(ms) };
    log(`scroll.mp4 (${n} frames, ${Math.round(ms)} ms/frame)`);
  }
  if (cfg.extra) await cfg.extra(page, { dir, frameLoop, toMp4, cdp, meta, setCursor });

  fs.writeFileSync(path.join(dir, 'meta.json'), JSON.stringify(meta, null, 1));
  return meta;
}

// CLI: node tools/capture.mjs <config-module> [id...]
if (import.meta.url === `file://${process.argv[1]}`) {
  const mod = await import(path.resolve(process.argv[2]));
  const only = process.argv.slice(3);
  for (const cfg of mod.SITES) {
    if (only.length && !only.includes(cfg.id)) continue;
    try { await captureSite(cfg); } catch (e) { console.error(`[${cfg.id}] FAILED`, e); }
  }
}
