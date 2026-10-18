import type { HookWord } from '../components/Hook';
import type { CapWord } from '../components/Captions';

export type Treatment = 'mockup' | 'bleed' | 'split' | 'punch' | 'hold';
export type Transition = 'cut' | 'whip' | 'glitch' | 'dissolve';
export type Shot = {
  id: string; start: number; end: number;            // beats
  demo: string; treatment: Treatment; footage: 'hero' | 'scroll' | 'cta';
  startFrom?: number; playbackRate?: number;
  transitionIn: Transition; whipDir?: 1 | -1;
  label?: boolean; labelAlign?: 'left' | 'right';
  opts?: Record<string, number | string>;
};

export const DEMOS: Record<string, { type: string }> = {
  hoa: { type: 'Nail & lash studio' }, briki: { type: 'Coffee chain' }, bowtie: { type: 'Barbershop' }, adams: { type: 'Old-town barber' },
  'moxie-hair': { type: 'Hair salon' }, kafenio11: { type: 'Café-bar' }, k2fit: { type: 'Fitness studio' }, 'agency-test': { type: 'Web studio' },
};

export const HOOK: HookWord[] = [
  { text: 'I built', beat: 0, kind: 'word' }, { text: '7', beat: 1, kind: 'numeral' }, { text: 'websites', beat: 1.5, kind: 'word' },
  { text: 'with AI', beat: 2.25, kind: 'small' }, { text: 'this week', beat: 2.85, kind: 'small' },
];

// Body: beats 4..50. Cuts on beats. Two deliberate rhythm breaks: the stutter run at 26-30 and the hold at 30-32 (the music drops out there).
export const SHOTS: Shot[] = [
  { id: 's01', start: 4, end: 8, demo: 'hoa', treatment: 'mockup', footage: 'hero', startFrom: 0, transitionIn: 'cut', label: true, opts: { tiltFrom: -16, tiltTo: 6 } },
  { id: 's02', start: 8, end: 12, demo: 'briki', treatment: 'bleed', footage: 'scroll', startFrom: 30, transitionIn: 'whip', whipDir: 1, label: true },
  { id: 's03', start: 12, end: 16, demo: 'bowtie', treatment: 'bleed', footage: 'scroll', startFrom: 62, transitionIn: 'glitch', label: true, opts: { driftTo: -60, zoomFrom: 1.02, zoomTo: 1.0 } },
  { id: 's04', start: 16, end: 20, demo: 'adams', treatment: 'punch', footage: 'cta', startFrom: 0, transitionIn: 'cut', label: true },
  { id: 's05', start: 20, end: 23, demo: 'moxie-hair', treatment: 'mockup', footage: 'hero', startFrom: 10, transitionIn: 'whip', whipDir: -1, label: true, opts: { tiltFrom: 12, tiltTo: -6 } },
  { id: 's06', start: 23, end: 26, demo: 'kafenio11', treatment: 'bleed', footage: 'scroll', startFrom: 20, transitionIn: 'cut', label: true },
  { id: 's07', start: 26, end: 28, demo: 'k2fit', treatment: 'mockup', footage: 'hero', startFrom: 20, transitionIn: 'glitch', label: true, opts: { tiltFrom: -6, tiltTo: 10, push: 0.1 } },
  { id: 's08', start: 28, end: 30, demo: 'hoa', treatment: 'bleed', footage: 'scroll', startFrom: 80, transitionIn: 'cut', label: false, opts: { zoomFrom: 1.06, zoomTo: 1.0 } },
  { id: 's09', start: 30, end: 32, demo: 'moxie-hair', treatment: 'hold', footage: 'hero', startFrom: 60, transitionIn: 'dissolve', label: false },
  { id: 's10', start: 32, end: 36, demo: 'bowtie', treatment: 'punch', footage: 'cta', startFrom: 0, transitionIn: 'glitch', label: true },
  { id: 's11', start: 36, end: 40, demo: 'briki', treatment: 'mockup', footage: 'scroll', startFrom: 90, transitionIn: 'whip', whipDir: 1, label: true, opts: { tiltFrom: 10, tiltTo: -12, push: 0.04 } },
  { id: 's12', start: 40, end: 44, demo: 'adams', treatment: 'split', footage: 'hero', startFrom: 30, transitionIn: 'cut', label: true, opts: { wipeAt: 22 } },
  { id: 's13', start: 44, end: 47, demo: 'kafenio11', treatment: 'split', footage: 'hero', startFrom: 50, transitionIn: 'glitch', label: true, opts: { wipeAt: 18 } },
  { id: 's14', start: 47, end: 50, demo: 'k2fit', treatment: 'punch', footage: 'cta', startFrom: 0, transitionIn: 'cut', label: true, opts: { punch: 1.7 } },
];

export const CAPTIONS: CapWord[] = [
  { word: 'Built', beat: 4.5, group: 1 }, { word: 'with AI.', beat: 5.5, group: 1 },
  { word: 'For real', beat: 8.5, group: 2 }, { word: 'small', beat: 9.5, group: 2 }, { word: 'businesses.', beat: 10, group: 2 },
  { word: 'Scroll', beat: 12.5, group: 3 }, { word: 'to walk in.', beat: 13.5, group: 3 },
  { word: 'One tap', beat: 16.5, group: 4 }, { word: 'to call.', beat: 17.6, group: 4 },
  { word: 'Hair.', beat: 20.5, group: 5 },
  { word: 'Coffee.', beat: 23.5, group: 6 },
  { word: 'Fitness.', beat: 26.5, group: 7 },
  { word: 'Nails.', beat: 28.5, group: 8 },
  { word: '', beat: 30, group: 9 },                      // silence during the hold
  { word: 'Each one', beat: 32.5, group: 10 }, { word: 'in a day.', beat: 33.5, group: 10 },
  { word: 'No templates.', beat: 36.5, group: 11 },
  { word: 'Same page.', beat: 40.5, group: 12 }, { word: 'New design.', beat: 42, group: 12 },
  { word: 'Free preview', beat: 44.5, group: 13 }, { word: 'first.', beat: 45.5, group: 13 },
  { word: 'Pay when', beat: 47.5, group: 14 }, { word: 'you love it.', beat: 48.5, group: 14 },
  { word: '', beat: 50, group: 15 },
];

export const ENDING = { markAt: 750, nameAt: 757, lineAt: 771, ctaAt: 780, pressAt: 795, line: 'Websites for small businesses', cta: "DM us 'WEBSITE'", handle: '@webbiespirit' };
