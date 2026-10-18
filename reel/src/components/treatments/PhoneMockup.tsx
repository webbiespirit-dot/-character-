import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { Clip, CLIP_W, CLIP_H } from '../Clip';
import { C, prog, lerp, easeSine } from '../../lib/theme';

/** A dark device floating in the night sky, tilted in 3D, with a gold rim light and a slow push-in. */
export const PhoneMockup: React.FC<{
  src: string; startFrom?: number; playbackRate?: number; width?: number; duration: number;
  tiltFrom?: number; tiltTo?: number; push?: number; y?: number; enter?: boolean;
}> = ({ src, startFrom = 0, playbackRate = 1, width = 620, duration, tiltFrom = -14, tiltTo = 8, push = 0.06, y = 0, enter = true }) => {
  const f = useCurrentFrame();
  const h = (width * CLIP_H) / CLIP_W;
  const t = prog(f, 0, duration, easeSine);
  const ry = lerp(tiltFrom, tiltTo, t);
  const rx = lerp(3, -2, t);
  const s = (1 + push * t) * (enter ? interpolate(prog(f, 0, 10), [0, 1], [0.94, 1]) : 1);
  const op = enter ? prog(f, 0, 6) : 1;
  const radius = width * 0.105;
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', perspective: 2400 }}>
      <div style={{ width, height: h, transform: `translateY(${y}px) rotateY(${ry}deg) rotateX(${rx}deg) scale(${s})`, transformStyle: 'preserve-3d', opacity: op, position: 'relative' }}>
        {/* body */}
        <div style={{ position: 'absolute', inset: -16, borderRadius: radius + 16, background: 'linear-gradient(160deg, #2b2a3a 0%, #121120 45%, #0a0a14 100%)',
          boxShadow: `0 70px 140px -50px rgba(0,0,0,.9), 0 30px 60px -30px rgba(0,0,0,.7), 0 0 0 1.5px rgba(232,188,76,.28), inset 0 0 0 1px rgba(255,255,255,.06)` }} />
        {/* side buttons */}
        <div style={{ position: 'absolute', left: -20, top: h * 0.22, width: 4, height: 70, borderRadius: 2, background: '#1a1928' }} />
        <div style={{ position: 'absolute', left: -20, top: h * 0.3, width: 4, height: 110, borderRadius: 2, background: '#1a1928' }} />
        <div style={{ position: 'absolute', right: -20, top: h * 0.26, width: 4, height: 140, borderRadius: 2, background: '#1a1928' }} />
        {/* screen */}
        <div style={{ position: 'absolute', inset: 0, borderRadius: radius, overflow: 'hidden', background: '#000' }}>
          <Clip src={src} startFrom={startFrom} playbackRate={playbackRate} />
          <div style={{ position: 'absolute', top: 14, left: '50%', width: width * 0.22, height: width * 0.058, marginLeft: -width * 0.11, borderRadius: 999, background: '#000' }} />
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(118deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,.03) 22%, transparent 40%)', pointerEvents: 'none' }} />
        </div>
      </div>
      <span style={{ display: 'none' }}>{C.gold}</span>
    </AbsoluteFill>
  );
};
