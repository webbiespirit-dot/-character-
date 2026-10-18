import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { C, F, prog, easeOut, easeInOut } from '../lib/theme';
import { Sky } from './Sky';
import { OrbitMark } from './Mark';

/** The sign-off: the orbit mark draws itself, the name, the line, and the one gold action with its shine. */
export const Ending: React.FC<{ markAt: number; nameAt: number; lineAt: number; ctaAt: number; pressAt: number; line: string; cta: string; handle: string }> =
  ({ markAt, nameAt, lineAt, ctaAt, pressAt, line, cta, handle }) => {
    const f = useCurrentFrame();
    const draw = prog(f, markAt, markAt + 16);
    const markIn = prog(f, markAt, markAt + 10);
    const nameP = prog(f, nameAt, nameAt + 10);
    const lineP = prog(f, lineAt, lineAt + 10);
    const ctaP = prog(f, ctaAt, ctaAt + 10);
    const press = f >= pressAt ? interpolate(f, [pressAt, pressAt + 3, pressAt + 9], [1, 0.965, 1], { extrapolateRight: 'clamp' }) : 1;
    const shine = prog(f, pressAt - 2, pressAt + 16, easeInOut);
    const rise = (p: number) => `translateY(${(1 - p) * 26}px)`;
    return (
      <Sky intensity={1} drift={0.8} stars={120}>
        <AbsoluteFill style={{ alignItems: 'center' }}>
          <div style={{ position: 'absolute', top: 560, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0 }}>
            <div style={{ opacity: markIn, transform: `scale(${interpolate(markIn, [0, 1], [0.9, 1])})` }}><OrbitMark size={230} draw={draw} /></div>
            <div style={{ marginTop: 38, opacity: nameP, transform: rise(nameP), fontFamily: F.display, fontWeight: 800, fontSize: 100, letterSpacing: '-0.035em', color: C.ivory, lineHeight: 1 }}>webbiespirit</div>
            <div style={{ marginTop: 26, opacity: lineP, transform: rise(lineP), fontFamily: F.text, fontWeight: 500, fontSize: 44, color: C.muted, lineHeight: 1.2, textAlign: 'center' }}>{line}</div>
            <div style={{ marginTop: 64, opacity: ctaP, transform: `${rise(ctaP)} scale(${press})`, transformOrigin: '50% 50%' }}>
              <div style={{ position: 'relative', overflow: 'hidden', display: 'inline-flex', alignItems: 'center', gap: 18, padding: '30px 54px', borderRadius: 999, background: C.gold, color: C.goldInk, fontFamily: F.text, fontWeight: 700, fontSize: 46, boxShadow: '0 1px 0 rgba(255,255,255,0.4) inset, 0 24px 60px -24px rgba(166,125,38,0.8)' }}>
                <svg width={40} height={40} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.6 8.6 0 0 1-3.9-.9L3 21l1.9-4.6A8.4 8.4 0 0 1 3 11.5a8.4 8.4 0 0 1 9-8.4 8.4 8.4 0 0 1 9 8.4z" /></svg>
                <span>{cta}</span>
                <span style={{ position: 'absolute', inset: 0, background: 'linear-gradient(105deg, transparent 35%, rgba(255,255,255,0.55) 50%, transparent 65%)', transform: `translateX(${interpolate(shine, [0, 1], [-130, 130])}%)`, pointerEvents: 'none' }} />
              </div>
            </div>
            <div style={{ marginTop: 30, opacity: ctaP * 0.9, fontFamily: F.text, fontWeight: 500, fontSize: 32, color: C.faint, letterSpacing: '0.02em' }}>{handle}</div>
          </div>
        </AbsoluteFill>
        <span style={{ display: 'none' }}>{easeOut(0)}</span>
      </Sky>
    );
  };
