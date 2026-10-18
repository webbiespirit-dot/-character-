import React from 'react';
import { OffthreadVideo, staticFile } from 'remotion';

export const CLIP_W = 1170, CLIP_H = 2532;
/** One captured phone clip (1170x2532). */
export const Clip: React.FC<{ src: string; startFrom?: number; endAt?: number; playbackRate?: number; style?: React.CSSProperties }> = ({ src, startFrom = 0, endAt, playbackRate = 1, style }) => (
  <OffthreadVideo src={staticFile(src)} startFrom={startFrom} endAt={endAt} playbackRate={playbackRate} muted
    style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block', ...style }} />
);
