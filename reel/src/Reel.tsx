import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { beat, prog, easeOut, easeIn } from './lib/theme';
import { ensureFonts } from './lib/fonts';
import clipsJson from './data/clips.json';
import { SHOTS, CAPTIONS, HOOK, ENDING, DEMOS, type Shot } from './data/storyboard';
import { Hook } from './components/Hook';
import { Ending } from './components/Ending';
import { Label } from './components/Label';
import { Captions } from './components/Captions';
import { PhoneMockup } from './components/treatments/PhoneMockup';
import { FullBleed } from './components/treatments/FullBleed';
import { SplitBeforeAfter } from './components/treatments/SplitBeforeAfter';
import { ZoomPunch } from './components/treatments/ZoomPunch';
import { Hold } from './components/treatments/Hold';
import { Glitch } from './components/transitions/Glitch';
import { MotionBlurX } from './components/transitions/MotionBlur';
import { Sky } from './components/Sky';

type ClipInfo = { hero: string; cta: string; scroll: string; before: string; pressFrame: number; target: { x: number; y: number }; heroFrames: number; scrollFrames: number; ctaFrames: number };
const CLIPS = clipsJson as Record<string, ClipInfo>;
const resolve = (demo: string): ClipInfo => CLIPS[demo] ?? CLIPS['agency-test'];
const PRE = (s?: Shot) => (s?.transitionIn === 'whip' ? 3 : 0);

const Treat: React.FC<{ shot: Shot; dur: number }> = ({ shot, dur }) => {
  const c = resolve(shot.demo);
  const src = shot.footage === 'hero' ? c.hero : shot.footage === 'scroll' ? c.scroll : c.cta;
  const o = shot.opts ?? {};
  const n = (k: string, d: number) => (typeof o[k] === 'number' ? (o[k] as number) : d);
  switch (shot.treatment) {
    case 'mockup': return (
      <Sky intensity={0.9} drift={1} stars={70}>
        <PhoneMockup src={src} startFrom={shot.startFrom} playbackRate={shot.playbackRate} duration={dur} width={580} y={70} tiltFrom={n('tiltFrom', -14)} tiltTo={n('tiltTo', 8)} push={n('push', 0.06)} />
      </Sky>);
    case 'bleed': return <FullBleed src={src} startFrom={shot.startFrom} playbackRate={shot.playbackRate} duration={dur} driftTo={n('driftTo', -120)} zoomFrom={n('zoomFrom', 1)} zoomTo={n('zoomTo', 1.04)} />;
    case 'split': return <SplitBeforeAfter before={c.before} after={src} startFrom={shot.startFrom} wipeAt={n('wipeAt', 30)} duration={dur} />;
    case 'punch': return <ZoomPunch src={src} startFrom={shot.startFrom} pressFrame={c.pressFrame - (shot.startFrom ?? 0)} target={c.target} duration={dur} punch={n('punch', 1.55)} />;
    case 'hold': return <Hold src={src} startFrom={shot.startFrom} duration={dur} />;
  }
};

/** Handles the transition in (and the next shot's transition out) for one shot. Local frame 0 = cut - PRE. */
const ShotFrame: React.FC<{ shot: Shot; next?: Shot; dur: number; children: React.ReactNode }> = ({ shot, next, dur, children }) => {
  const f = useCurrentFrame();
  const pre = PRE(shot);
  const cutIn = pre, cutOut = pre + dur;
  const xAt = (fr: number) => {
    let x = 0;
    if (shot.transitionIn === 'whip') x += (1 - prog(fr, cutIn - 3, cutIn + 3, easeOut)) * 1080 * (shot.whipDir ?? 1);
    if (next?.transitionIn === 'whip') x += -prog(fr, cutOut - 3, cutOut + 3, easeIn) * 1080 * (next.whipDir ?? 1);
    return x;
  };
  const x = xAt(f), vel = x - xAt(f - 1);
  let glitch = 0;
  if (shot.transitionIn === 'glitch') glitch = Math.max(glitch, f >= cutIn ? 1 - prog(f, cutIn, cutIn + 4, (t) => t) : 0);
  if (next?.transitionIn === 'glitch') glitch = Math.max(glitch, f >= cutOut - 2 ? 0.7 : 0);
  const opacity = shot.transitionIn === 'dissolve' ? prog(f, cutIn, cutIn + 8) : 1;
  return (
    <AbsoluteFill style={{ opacity }}>
      <MotionBlurX x={x} velocity={vel}><Glitch strength={glitch} seed={shot.start}>{children}</Glitch></MotionBlurX>
    </AbsoluteFill>
  );
};

export const Reel: React.FC = () => {
  ensureFonts();
  const sfx: { src: string; at: number; vol?: number }[] = [];
  SHOTS.forEach((s) => {
    if (s.transitionIn === 'whip') sfx.push({ src: 'whoosh.wav', at: beat(s.start) - 4, vol: 0.5 });
    if (s.transitionIn === 'glitch') sfx.push({ src: 'glitch.wav', at: beat(s.start), vol: 0.35 });
    if (s.footage === 'cta') sfx.push({ src: 'tap.wav', at: beat(s.start) + resolve(s.demo).pressFrame - (s.startFrom ?? 0), vol: 0.7 });
  });
  sfx.push({ src: 'tap.wav', at: ENDING.pressAt, vol: 0.6 });
  return (
    <AbsoluteFill style={{ background: '#0d0b1a' }}>
      <Audio src={staticFile('track.wav')} volume={0.95} />
      {sfx.map((s, i) => (s.at >= 0 ? <Sequence key={`sfx${i}`} from={s.at} durationInFrames={30} layout="none"><Audio src={staticFile(s.src)} volume={s.vol ?? 0.5} /></Sequence> : null))}

      <Sequence from={0} durationInFrames={beat(4)} layout="none"><Hook words={HOOK} /></Sequence>

      {SHOTS.map((shot, i) => {
        const next = SHOTS[i + 1];
        const dur = beat(shot.end) - beat(shot.start);
        const pre = PRE(shot), post = PRE(next);
        return (
          <Sequence key={shot.id} from={beat(shot.start) - pre} durationInFrames={dur + pre + post} layout="none">
            <ShotFrame shot={shot} next={next} dur={dur}>
              <Sequence from={pre} layout="none"><Treat shot={shot} dur={dur} /></Sequence>
            </ShotFrame>
            {shot.label !== false && (
              <Sequence from={pre} durationInFrames={dur} layout="none">
                <Label type={DEMOS[shot.demo]?.type ?? ''} align={shot.labelAlign ?? 'left'} y={268} hideFrom={next?.transitionIn === 'whip' ? dur - 4 : undefined} />
              </Sequence>
            )}
          </Sequence>
        );
      })}

      <Sequence from={0} durationInFrames={beat(50)} layout="none"><Captions words={CAPTIONS} /></Sequence>
      <Sequence from={beat(50)} layout="none">
        <Ending markAt={ENDING.markAt - beat(50)} nameAt={ENDING.nameAt - beat(50)} lineAt={ENDING.lineAt - beat(50)} ctaAt={ENDING.ctaAt - beat(50)} pressAt={ENDING.pressAt - beat(50)} line={ENDING.line} cta={ENDING.cta} handle={ENDING.handle} />
      </Sequence>
    </AbsoluteFill>
  );
};
