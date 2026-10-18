import React from 'react';
import { AbsoluteFill } from 'remotion';

/** Horizontal motion blur by stacking ghost copies along the velocity. */
export const MotionBlurX: React.FC<{ x: number; velocity: number; children: React.ReactNode; copies?: number }> = ({ x, velocity, children, copies = 5 }) => {
  if (Math.abs(velocity) < 4) return <AbsoluteFill style={{ transform: `translateX(${x}px)` }}>{children}</AbsoluteFill>;
  const n = copies;
  return (
    <AbsoluteFill>
      {Array.from({ length: n }, (_, i) => {
        const k = i / (n - 1) - 0.5;                       // -0.5 .. 0.5 along the velocity
        return <AbsoluteFill key={i} style={{ transform: `translateX(${x + velocity * k * 0.9}px)`, opacity: 1 / n + (i === Math.floor(n / 2) ? 0.15 : 0) }}>{children}</AbsoluteFill>;
      })}
    </AbsoluteFill>
  );
};
