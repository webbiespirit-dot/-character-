import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { C, F, beat, prog } from '../lib/theme';

export type CapWord = { word: string; beat: number; group: number };

/** Word-by-word captions in a night glass chip; the newest word lands in gold, then settles to ivory. */
export const Captions: React.FC<{ words: CapWord[]; bottom?: number; size?: number }> = ({ words, bottom = 1480, size = 70 }) => {
  const f = useCurrentFrame();
  const landed = words.filter((w) => beat(w.beat) <= f);
  if (!landed.length) return null;
  const group = landed[landed.length - 1].group;
  const phrase = words.filter((w) => w.group === group);
  const start = beat(phrase[0].beat);
  const next = words.find((w) => w.group === group + 1);
  const end = next ? beat(next.beat) : null;
  const life = Math.min(prog(f, start, start + 5), end === null ? 1 : 1 - prog(f, end - 4, end));
  const boxP = prog(f, start, start + 6);
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: 1920 - bottom, display: 'flex', justifyContent: 'center', pointerEvents: 'none', opacity: life }}>
      <div style={{ maxWidth: 960, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'baseline', gap: `0 ${size * 0.3}px`, padding: `${size * 0.22}px ${size * 0.5}px ${size * 0.3}px`, borderRadius: 18, background: 'rgba(13,11,26,0.74)', border: `1px solid ${C.line}`, backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)', transform: `scale(${interpolate(boxP, [0, 1], [0.96, 1])}) translateY(${(1 - boxP) * 10}px)`, transformOrigin: '50% 100%' }}>
        {phrase.map((w, i) => {
          const s = beat(w.beat);
          const p = prog(f, s, s + 6);
          const isLast = i === phrase.length - 1 || f < beat(phrase[i + 1].beat);
          const goldness = isLast ? 1 - prog(f, s + 10, s + 22) : 0;
          const color = goldness > 0.5 ? C.gold : C.ivory;
          return (
            <span key={i} style={{ display: 'inline-block', fontFamily: F.display, fontWeight: 800, fontSize: size, lineHeight: 1.08, letterSpacing: '-0.025em', color, opacity: f >= s ? p : 0, transform: `translateY(${(1 - p) * 18}px) scale(${interpolate(p, [0, 1], [0.86, 1])})`, transformOrigin: '50% 100%', whiteSpace: 'nowrap', textShadow: goldness > 0.5 ? '0 0 24px rgba(232,188,76,.45)' : 'none' }}>
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
