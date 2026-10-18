import { Easing, interpolate } from 'remotion';

/** webbiespirit live-site palette (night theme); gold is the only action colour. */
export const C = {
  night: '#0d0b1a', night2: '#15122a', night3: '#1d1936',
  ivory: '#f5efe2', muted: '#b9b1c9', faint: '#8f889f',
  gold: '#e8bc4c', gold2: '#f8df8e', goldDeep: '#a67d26', goldInk: '#15100a',
  line: 'rgba(245,239,226,0.12)', line2: 'rgba(245,239,226,0.22)',
  violet: '#5a3fa8', rose: '#b4647a', teal: '#3f8fa8',
};
export const F = {
  display: '"Syne", "Avenir Next", "Helvetica Neue", sans-serif',
  text: '"Instrument Sans", "Helvetica Neue", Arial, sans-serif',
};
export const W = 1080, H = 1920, FPS = 30, FPB = 15;           // 120 BPM
export const beat = (b: number) => Math.round(b * FPB);
export const SAFE = { top: 250, bottom: 1520 };
export const R = { pill: 999, card: 28, device: 64 };

export const easeOut = Easing.bezier(0.23, 1, 0.32, 1);
export const easeInOut = Easing.bezier(0.77, 0, 0.175, 1);
export const easeSine = Easing.bezier(0.37, 0, 0.63, 1);
export const easeIn = Easing.bezier(0.5, 0, 0.75, 0);

export const prog = (frame: number, from: number, to: number, ease: (t: number) => number = easeOut) =>
  interpolate(frame, [from, to], [0, 1], { easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const hash = (...n: number[]) => {
  let h = 2166136261;
  for (const v of n) { h ^= Math.floor(v * 1000003) & 0xffffffff; h = Math.imul(h, 16777619); }
  return ((h >>> 0) % 100000) / 100000;
};
