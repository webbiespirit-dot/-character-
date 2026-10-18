import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { Clip, CLIP_W, CLIP_H } from '../Clip';
import { prog, lerp, easeOut, easeSine } from '../../lib/theme';

/** The CTA tap: full-bleed capture, and on the press the camera punches into the button. */
export const ZoomPunch: React.FC<{ src: string; startFrom?: number; pressFrame: number; target: { x: number; y: number }; duration: number; punch?: number; settle?: number }> =
  ({ src, startFrom = 0, pressFrame, target, duration, punch = 1.55, settle = 1.32 }) => {
    const f = useCurrentFrame();
    const s = 1080 / CLIP_W, w = CLIP_W * s, h = CLIP_H * s;
    // frame the target: keep the button around 62% down the screen before the punch
    const tx = target.x * s, ty = target.y * s;
    const baseY = Math.max(1920 - h, Math.min(0, 1180 - ty));
    const pre = lerp(1.0, 1.04, prog(f, 0, pressFrame, easeSine));
    const hit = prog(f, pressFrame, pressFrame + 4, easeOut);
    const back = prog(f, pressFrame + 10, duration, easeSine);
    const z = pre * lerp(1, lerp(punch, settle, back), hit);
    const flash = interpolate(f, [pressFrame, pressFrame + 5], [0.35, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) * (f >= pressFrame ? 1 : 0);
    return (
      <AbsoluteFill style={{ overflow: 'hidden', background: '#000' }}>
        <div style={{ position: 'absolute', left: 0, top: baseY, width: w, height: h, transform: `scale(${z})`, transformOrigin: `${tx}px ${ty}px` }}>
          <Clip src={src} startFrom={startFrom} />
        </div>
        <AbsoluteFill style={{ background: `radial-gradient(circle at ${tx}px ${ty + baseY}px, rgba(248,223,142,${flash}) 0%, rgba(248,223,142,0) 38%)`, pointerEvents: 'none' }} />
        <AbsoluteFill style={{ background: `linear-gradient(180deg, rgba(13,11,26,0) 58%, rgba(13,11,26,.5) 100%)`, pointerEvents: 'none' }} />
      </AbsoluteFill>
    );
  };
