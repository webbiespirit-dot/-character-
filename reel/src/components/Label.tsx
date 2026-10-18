import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { C, F, prog } from '../lib/theme';

/** The site's "chip": night glass, hairline, a pulsing gold dot. Business type in Syne, "built in 1 day" in Instrument Sans. */
export const Label: React.FC<{ type: string; sub?: string; delay?: number; x?: number; y?: number; align?: 'left' | 'right'; hideFrom?: number }> =
  ({ type, sub = 'built in 1 day', delay = 3, x = 48, y = 300, align = 'left', hideFrom }) => {
    const f = useCurrentFrame();
    const p = prog(f, delay, delay + 10);
    const out = hideFrom !== undefined ? 1 - prog(f, hideFrom, hideFrom + 5) : 1;
    const pulse = 0.75 + 0.25 * Math.sin((f / 30) * Math.PI * 1.11);
    return (
      <div style={{ position: 'absolute', top: y, [align]: x, opacity: p * out, transform: `translateY(${(1 - p) * 16}px) scale(${interpolate(p, [0, 1], [0.97, 1])})`, transformOrigin: align === 'left' ? '0% 50%' : '100% 50%' } as React.CSSProperties}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 16, padding: '14px 22px 14px 18px', borderRadius: 14, background: 'rgba(13,11,26,0.9)', border: `1px solid ${C.line2}`, boxShadow: '0 14px 34px -14px rgba(0,0,0,.65)', backdropFilter: 'blur(10px)', WebkitBackdropFilter: 'blur(10px)' }}>
          <span style={{ width: 12, height: 12, borderRadius: '50%', background: C.gold, boxShadow: `0 0 ${10 + pulse * 10}px ${C.gold}`, opacity: pulse, flex: 'none' }} />
          <span style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <span style={{ fontFamily: F.display, fontWeight: 700, fontSize: 36, lineHeight: 1.05, letterSpacing: '-0.02em', color: C.ivory, whiteSpace: 'nowrap' }}>{type}</span>
            <span style={{ fontFamily: F.text, fontWeight: 500, fontSize: 24, lineHeight: 1.1, color: C.muted, whiteSpace: 'nowrap' }}>{sub}</span>
          </span>
        </div>
      </div>
    );
  };
