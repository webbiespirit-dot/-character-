import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { Clip, CLIP_W, CLIP_H } from '../Clip';
import { prog, lerp, easeSine, easeOut } from '../../lib/theme';

/** The capture fills the frame edge to edge; a slow drift and a night scrim at the foot for captions. */
export const FullBleed: React.FC<{ src: string; startFrom?: number; playbackRate?: number; duration: number; driftFrom?: number; driftTo?: number; zoomFrom?: number; zoomTo?: number; scrim?: number; origin?: string; enter?: 'none' | 'zoom' }> =
  ({ src, startFrom = 0, playbackRate = 1, duration, driftFrom = 0, driftTo = -120, zoomFrom = 1, zoomTo = 1.04, scrim = 0.55, origin = '50% 40%', enter = 'none' }) => {
    const f = useCurrentFrame();
    const t = prog(f, 0, duration, easeSine);
    const s = CLIP_W > 0 ? 1080 / CLIP_W : 1;
    const w = CLIP_W * s, h = CLIP_H * s;              // 1080 x 2337
    const y = lerp(driftFrom, driftTo, t);
    const z = lerp(zoomFrom, zoomTo, t) * (enter === 'zoom' ? lerp(1.12, 1, prog(f, 0, 8, easeOut)) : 1);
    return (
      <AbsoluteFill style={{ overflow: 'hidden', background: '#000' }}>
        <div style={{ position: 'absolute', left: 0, top: y, width: w, height: h, transform: `scale(${z})`, transformOrigin: origin }}>
          <Clip src={src} startFrom={startFrom} playbackRate={playbackRate} />
        </div>
        <AbsoluteFill style={{ background: `linear-gradient(180deg, rgba(13,11,26,0) 55%, rgba(13,11,26,${scrim}) 100%)`, pointerEvents: 'none' }} />
      </AbsoluteFill>
    );
  };
