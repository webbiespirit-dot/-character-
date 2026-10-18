import React, { useMemo } from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, hash } from '../lib/theme';

/** The site's living night sky: deep night, a slow pastel nebula, and sparkles that twinkle. */
export const Sky: React.FC<{ children?: React.ReactNode; intensity?: number; drift?: number; stars?: number; style?: React.CSSProperties }> =
  ({ children, intensity = 1, drift = 1, stars = 90, style }) => {
    const f = useCurrentFrame();
    const t = f / 30;
    const pts = useMemo(() => Array.from({ length: stars }, (_, i) => ({ x: hash(i, 11) * 1080, y: hash(i, 23) * 1920, r: 1 + hash(i, 5) * 2.2, ph: hash(i, 7) * 6.283, sp: 0.6 + hash(i, 9) * 1.4, gold: hash(i, 13) > 0.8 })), [stars]);
    const nx = Math.sin(t * 0.21) * 60 * drift, ny = Math.cos(t * 0.17) * 40 * drift;
    return (
      <AbsoluteFill style={{ background: C.night, overflow: 'hidden', ...style }}>
        <AbsoluteFill style={{
          opacity: intensity,
          background: [
            `radial-gradient(42% 30% at ${34 + nx / 20}% ${28 + ny / 20}%, rgba(90,63,168,0.42), transparent 70%)`,
            `radial-gradient(36% 26% at ${72 - nx / 25}% ${62 + ny / 30}%, rgba(166,125,38,0.26), transparent 70%)`,
            `radial-gradient(50% 34% at ${55 + nx / 30}% ${88 - ny / 25}%, rgba(180,100,122,0.22), transparent 70%)`,
            `radial-gradient(30% 22% at ${18 - nx / 30}% 78%, rgba(63,143,168,0.16), transparent 70%)`,
          ].join(','),
        }} />
        <svg width={1080} height={1920} style={{ position: 'absolute', inset: 0 }}>
          {pts.map((p, i) => {
            const tw = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * p.sp * 2.1 + p.ph));
            return <circle key={i} cx={p.x} cy={p.y + Math.sin(t * 0.1 + p.ph) * 6 * drift} r={p.r} fill={p.gold ? C.gold2 : C.ivory} opacity={tw * (p.gold ? 0.9 : 0.55) * intensity} />;
          })}
        </svg>
        {children}
      </AbsoluteFill>
    );
  };
