import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { C, F, beat, prog, hash, easeOut } from '../lib/theme';
import { Sky } from './Sky';

export type HookWord = { text: string; beat: number; kind?: 'word' | 'numeral' | 'small' };

/** Kinetic hook over the night sky. Words land on their beats; the numeral is gold and blooms; the roll into the drop shakes the frame. */
export const Hook: React.FC<{ words: HookWord[] }> = ({ words }) => {
  const f = useCurrentFrame();
  const roll = prog(f, beat(3), beat(4), (t) => t);
  const sx = roll > 0 ? (hash(f, 1) - 0.5) * 14 * roll : 0;
  const sy = roll > 0 ? (hash(f, 2) - 0.5) * 10 * roll : 0;
  const numeral = words.find((w) => w.kind === 'numeral');
  const nb = numeral ? beat(numeral.beat) : 0;
  const np = prog(f, nb, nb + 8);
  const bloom = interpolate(f, [nb, nb + 2, nb + 14], [0, 0.9, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) * (f >= nb ? 1 : 0);
  const line = (ws: HookWord[], fontSize: number, weight: number, family = F.display, color = C.ivory, lh = 0.96) => (
    <div style={{ display: 'flex', gap: fontSize * 0.24, alignItems: 'baseline', flexWrap: 'wrap' }}>
      {ws.map((w, i) => {
        const s = beat(w.beat);
        const p = prog(f, s, s + 6, easeOut);
        return (
          <span key={i} style={{ display: 'inline-block', fontFamily: family, fontSize, fontWeight: weight, lineHeight: lh, letterSpacing: family === F.display ? '-0.035em' : '0', color, opacity: p, transform: `translateY(${(1 - p) * 34}px) scale(${interpolate(p, [0, 1], [1.22, 1])})`, transformOrigin: '0% 85%', whiteSpace: 'nowrap' }}>
            {w.text}
          </span>
        );
      })}
    </div>
  );
  const first = words.filter((w) => w.kind === 'word' && w.beat < (numeral?.beat ?? 99));
  const after = words.filter((w) => w.kind === 'word' && w.beat > (numeral?.beat ?? -1));
  const small = words.filter((w) => w.kind === 'small');
  return (
    <Sky intensity={1} drift={1.4} stars={110}>
      <AbsoluteFill style={{ transform: `translate(${sx}px, ${sy}px)` }}>
        <div style={{ position: 'absolute', left: 64, right: 40, top: 430, display: 'flex', flexDirection: 'column', gap: 6 }}>
          {line(first, 136, 800)}
          {numeral && (
            <div style={{ position: 'relative', height: 560, marginTop: -8 }}>
              <div style={{ position: 'absolute', left: -14, top: 0, fontFamily: F.display, fontSize: 680, fontWeight: 800, lineHeight: 0.8, letterSpacing: '-0.06em',
                background: `linear-gradient(160deg, ${C.gold2} 0%, ${C.gold} 48%, ${C.goldDeep} 100%)`, WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent',
                opacity: np, transform: `translateY(${(1 - np) * 70}px) scale(${interpolate(np, [0, 1], [1.2, 1])})`, transformOrigin: '20% 70%', filter: `drop-shadow(0 0 ${30 * bloom + 10}px rgba(232,188,76,${0.25 + bloom * 0.5}))` }}>
                {numeral.text}
              </div>
            </div>
          )}
          {line(after, 136, 800)}
          <div style={{ marginTop: 22 }}>{line(small, 60, 500, F.text, C.muted, 1.15)}</div>
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(circle at 36% 48%, rgba(248,223,142,${bloom * 0.35}) 0%, rgba(248,223,142,0) 45%)`, pointerEvents: 'none' }} />
    </Sky>
  );
};
