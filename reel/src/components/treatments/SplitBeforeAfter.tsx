import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from 'remotion';
import { Clip, CLIP_W, CLIP_H } from '../Clip';
import { C, F, prog, lerp, easeInOut, easeOut } from '../../lib/theme';

/** Left: the same page with its CSS stripped. Right: the finished site. Holds the split, then the design wipes across. */
export const SplitBeforeAfter: React.FC<{ before: string; after: string; startFrom?: number; wipeAt: number; duration: number }> =
  ({ before, after, startFrom = 0, wipeAt, duration }) => {
    const f = useCurrentFrame();
    const s = 1080 / CLIP_W, w = CLIP_W * s, h = CLIP_H * s;
    const split = lerp(540, 1120, prog(f, wipeAt, wipeAt + 9, easeInOut));          // divider x
    const intro = prog(f, 0, 8, easeOut);
    const lineX = Math.min(split, 1080);
    const chip = (text: string, x: number, align: 'left' | 'right', show: boolean) => (
      <div style={{ position: 'absolute', top: 1240, [align]: x, opacity: show ? intro : 0, transform: `translateY(${(1 - intro) * 12}px)`, padding: '10px 16px', borderRadius: 12, background: 'rgba(13,11,26,0.72)', border: `1px solid ${C.line2}`, color: C.ivory, fontFamily: F.text, fontWeight: 600, fontSize: 26, letterSpacing: '0.12em', textTransform: 'uppercase' } as React.CSSProperties}>{text}</div>
    );
    return (
      <AbsoluteFill style={{ overflow: 'hidden', background: '#fff' }}>
        {/* before: raw HTML */}
        <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, clipPath: `inset(0 ${1080 - split}px 0 0)` }}>
          <Img src={staticFile(before)} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top', filter: 'grayscale(1) contrast(.95)' }} />
        </div>
        {/* after: the site */}
        <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, clipPath: `inset(0 0 0 ${Math.max(0, split)}px)` }}>
          <Clip src={after} startFrom={startFrom} />
        </div>
        {/* divider */}
        {split < 1081 && <div style={{ position: 'absolute', top: 0, bottom: 0, left: lineX - 2, width: 4, background: C.gold, boxShadow: '0 0 24px rgba(232,188,76,.8)' }} />}
        {chip('before', 40, 'left', split < 1000)}
        {chip('after', 40, 'right', split < 1000)}
        <AbsoluteFill style={{ background: `linear-gradient(180deg, rgba(13,11,26,0) 60%, rgba(13,11,26,.5) 100%)`, pointerEvents: 'none' }} />
        <span style={{ display: 'none' }}>{duration}</span>
      </AbsoluteFill>
    );
  };
