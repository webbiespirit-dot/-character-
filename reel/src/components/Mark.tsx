import React from 'react';
import { useCurrentFrame } from 'remotion';
import { C, F } from '../lib/theme';

/** The live site's brand mark: globe ring with a breathing meridian, a spinning orbit, the gold W and its star. */
export const OrbitMark: React.FC<{ size?: number; draw?: number }> = ({ size = 120, draw = 1 }) => {
  const f = useCurrentFrame();
  const spin = (f / 30 / 14) * 360;
  const mer = Math.cos((f / 30 / 7) * Math.PI);
  const len = 330;
  return (
    <svg viewBox="0 0 200 200" width={size} height={size} style={{ overflow: 'visible', filter: 'drop-shadow(0 0 12px rgba(232,188,76,0.45))' }}>
      <defs>
        <linearGradient id="goldStroke" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#f8df8e" /><stop offset="0.5" stopColor="#e8bc4c" /><stop offset="1" stopColor="#a67d26" />
        </linearGradient>
      </defs>
      <circle cx="100" cy="100" r="62" fill="none" stroke={C.gold} strokeOpacity="0.5" strokeWidth="5" />
      <ellipse cx="100" cy="100" rx={Math.max(0.5, 62 * Math.abs(mer))} ry="62" fill="none" stroke={C.gold} strokeOpacity="0.5" strokeWidth="5" />
      <g transform={`rotate(${spin} 100 100)`}>
        <ellipse cx="100" cy="100" rx="88" ry="34" fill="none" stroke={C.gold} strokeOpacity="0.7" strokeWidth="5" transform="rotate(-22 100 100)" />
      </g>
      <path d="M40 70 L62 136 L100 82 L138 136 L160 70" fill="none" stroke="url(#goldStroke)" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - draw)} />
      <circle cx="160" cy="70" r="9" fill={C.gold2} opacity={draw} />
    </svg>
  );
};
export const Wordmark: React.FC<{ size?: number; color?: string }> = ({ size = 48, color = C.ivory }) => (
  <span style={{ fontFamily: F.display, fontWeight: 700, fontSize: size, letterSpacing: '-0.02em', color, lineHeight: 1 }}>webbiespirit</span>
);
