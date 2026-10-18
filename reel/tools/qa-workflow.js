export const meta = {
  name: 'reel-qa',
  description: 'Adversarial frame-by-frame QA of the rendered reel: safe zones, cut-offs, readability, centring, brand and pacing',
  phases: [
    { title: 'Inspect', detail: 'four lenses over the verification frames and strips' },
    { title: 'Verify', detail: 'refute or confirm each finding' },
  ],
}
const DIR = '/home/user/-character-/reel/out/qa'
const FINDINGS = {
  type: 'object',
  properties: {
    findings: { type: 'array', items: { type: 'object', properties: {
      frame: { type: 'number' }, severity: { type: 'string', description: 'blocker | should-fix | nit' },
      what: { type: 'string' }, where: { type: 'string', description: 'region, e.g. "caption chip, bottom edge y~1500"' }, fix: { type: 'string' } },
      required: ['frame', 'severity', 'what', 'where', 'fix'] } },
    overall: { type: 'string' },
  },
  required: ['findings', 'overall'],
}
const VERDICT = { type: 'object', properties: { confirmed: { type: 'boolean' }, reason: { type: 'string' } }, required: ['confirmed', 'reason'] }
const LENSES = [
  { key: 'safe-zones', brief: 'Instagram safe zones: NO text, label, caption or CTA may touch the top 250 px or the bottom 400 px (y > 1520) of the 1080x1920 frame. Measure pixel positions from the images (they are full-size PNGs; use Python/PIL to find bounding boxes of light text pixels in those bands if needed). Also check nothing important is cut off at any edge.' },
  { key: 'readability', brief: 'Readability on a phone at arm\'s length: caption words, labels and the hook must be legible (size, contrast against what is behind them, no overlaps between the label chip, the caption chip and site UI text). Flag any overlap of two text elements, any text clipped by its own container, and any frame where the gold word is unreadable.' },
  { key: 'composition', brief: 'Composition and centring: is the phone mockup centred and not cropped? Are full-bleed shots framed on something meaningful (not an empty area)? Are before/after halves balanced? Is the ending stack centred with even spacing? Flag awkward crops, dead space, and frames where the footage shows a broken page, missing image, or placeholder.' },
  { key: 'brand-pacing', brief: 'Brand and pacing: night sky, ivory type, gold used only for the action and the numeral/highlight, Syne display font, pill button. Flag anything that looks like a generic corporate promo, any em-dash or emoji in on-screen text, any business name visible in overlays (site footage may contain names; overlays must not), and any shot where the label text does not match the site shown.' },
]
phase('Inspect')
const found = (await parallel(LENSES.map((l) => () => agent(
`You QA a rendered 28 s Instagram reel (1080x1920, 30 fps). Frame images are in ${DIR}: files named frame-<n>.png are full-size frames at frame n; strip-*.jpg are rows of consecutive frames around cuts. Read ALL of them with the Read tool (view the images). Lens: ${l.brief}
Report only real problems you can point to in a specific frame with a specific region. Be adversarial: assume there are defects and look for them. Do not report compliments.`,
  { label: `inspect:${l.key}`, phase: 'Inspect', schema: FINDINGS })))).filter(Boolean)
const all = found.flatMap((r) => r.findings)
log(`${all.length} raw findings`)
phase('Verify')
const verified = await parallel(all.map((fnd) => () => agent(
`Verify this QA finding about a reel frame by viewing ${DIR}/frame-${fnd.frame}.png (and neighbouring strips in ${DIR} if relevant) with the Read tool. Finding: ${JSON.stringify(fnd)}. Safe zones: top 250 px and bottom 400 px must be free of text/UI overlays (site footage itself may extend there). Default to confirmed=false if you cannot see the problem at the stated place.`,
  { label: `verify:${fnd.frame}`, phase: 'Verify', schema: VERDICT }).then((v) => ({ ...fnd, ...v }))))
const confirmed = verified.filter(Boolean).filter((v) => v.confirmed)
return { confirmed, rejected: verified.filter(Boolean).filter((v) => !v.confirmed).length, overall: found.map((r) => r.overall) }
