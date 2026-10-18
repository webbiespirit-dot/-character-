import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { Clip, CLIP_W, CLIP_H } from '../Clip';
import { prog, lerp, easeSine } from '../../lib/theme';

/** The rhythm break: one still-ish hero, a slow breath in, the sound drops out around it. */
export const Hold: React.FC<{ src: string; startFrom?: number; duration: number; zoomFrom?: number; zoomTo?: number; origin?: string; dim?: number }> =
  ({ src, startFrom = 0, duration, zoomFrom = 1.0, zoomTo = 1.08, origin = '50% 35%', dim = 0.18 }) => {
    const f = useCurrentFrame();
    const z = lerp(zoomFrom, zoomTo, prog(f, 0, duration, easeSine));
    const s = 1080 / CLIP_W, w = CLIP_W * s, h = CLIP_H * s;
    return (
      <AbsoluteFill style={{ overflow: 'hidden', background: '#000' }}>
        <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, transform: `scale(${z})`, transformOrigin: origin }}>
          <Clip src={src} startFrom={startFrom} playbackRate={0.5} />
        </div>
        <AbsoluteFill style={{ background: `rgba(13,11,26,${dim})` }} />
      </AbsoluteFill>
    );
  };
