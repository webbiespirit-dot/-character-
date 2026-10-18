import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { hash } from '../../lib/theme';

/** RGB split + sliced displacement. strength 0 renders children once (cheap). */
export const Glitch: React.FC<{ strength: number; seed?: number; children: React.ReactNode }> = ({ strength, seed = 0, children }) => {
  const f = useCurrentFrame();
  if (strength <= 0.001) return <AbsoluteFill>{children}</AbsoluteFill>;
  const k = strength;
  const off = 18 * k;
  const slices = 7;
  return (
    <AbsoluteFill style={{ background: '#000', overflow: 'hidden' }}>
      <svg width={0} height={0} style={{ position: 'absolute' }}>
        <filter id="chR"><feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" /></filter>
        <filter id="chG"><feColorMatrix type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" /></filter>
        <filter id="chB"><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" /></filter>
      </svg>
      <AbsoluteFill style={{ filter: 'url(#chR)', transform: `translateX(${-off}px)`, mixBlendMode: 'screen' }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ filter: 'url(#chG)', mixBlendMode: 'screen' }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ filter: 'url(#chB)', transform: `translateX(${off}px)`, mixBlendMode: 'screen' }}>{children}</AbsoluteFill>
      {Array.from({ length: slices }, (_, i) => {
        const top = Math.floor(hash(f, i, seed) * 1800);
        const hgt = 20 + Math.floor(hash(f, i + 50, seed) * 120);
        const dx = (hash(f, i + 100, seed) - 0.5) * 160 * k;
        if (hash(f, i + 150, seed) > 0.75 * k + 0.2) return null;
        return <AbsoluteFill key={i} style={{ clipPath: `inset(${top}px 0 ${Math.max(0, 1920 - top - hgt)}px 0)`, transform: `translateX(${dx}px)` }}>{children}</AbsoluteFill>;
      })}
      {/* scanline flash */}
      <AbsoluteFill style={{ background: `repeating-linear-gradient(180deg, rgba(245,239,226,${0.05 * k}) 0 2px, transparent 2px 6px)`, pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};
