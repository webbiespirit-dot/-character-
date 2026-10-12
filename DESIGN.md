---
name: webbiespirit
description: A sponsor page printed as a cyanotype. Prussian-cobalt emulsion coats on cool cotton paper, type exposed in white, sunlight only on the action.
colors:
  deep: "#0B2559"
  field: "#163F94"
  mid: "#2F63C7"
  light: "#8FB0E6"
  sun: "#E0E46A"
  sun-press: "#C9CF48"
  sun-lift: "#EAEC86"
  sensitizer: "#DAD69C"
  paper: "#F3F6F9"
  ink: "#0B2559"
  ink-soft: "#3A5486"
  on-field: "#FFFFFF"
  on-field-soft: "#D3DFF5"
typography:
  display:
    fontFamily: '"Piazzolla", "Iowan Old Style", Georgia, serif'
    fontSize: "clamp(36px, 10.4vw, 96px)"
    fontWeight: 560
    lineHeight: 0.98
    letterSpacing: "-0.022em"
  headline:
    fontFamily: '"Piazzolla", "Iowan Old Style", Georgia, serif'
    fontSize: "clamp(30px, 7.6vw, 64px)"
    fontWeight: 520
    lineHeight: 1.02
    letterSpacing: "-0.018em"
  numeral:
    fontFamily: '"Piazzolla", "Iowan Old Style", Georgia, serif'
    fontSize: "clamp(56px, 15vw, 96px)"
    fontWeight: 300
    lineHeight: 0.8
    fontFeature: '"lnum"'
  title:
    fontFamily: '"Piazzolla", "Iowan Old Style", Georgia, serif'
    fontSize: "clamp(22px, 5.6vw, 32px)"
    fontWeight: 460
    lineHeight: 1.15
  address:
    fontFamily: '"Piazzolla", "Iowan Old Style", Georgia, serif'
    fontSize: "clamp(22px, 6.4vw, 40px)"
    fontWeight: 480
    lineHeight: 1.1
  wordmark:
    fontFamily: '"Piazzolla", "Iowan Old Style", Georgia, serif'
    fontSize: "22px"
    fontWeight: 520
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontVariation: '"opsz" 24'
  lead:
    fontFamily: '"Sofia Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "clamp(17px, 4.4vw, 21px)"
    fontWeight: 400
    lineHeight: 1.45
  body:
    fontFamily: '"Sofia Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  button:
    fontFamily: '"Sofia Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "17px"
    fontWeight: 720
    letterSpacing: "0.01em"
  control:
    fontFamily: '"Sofia Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "15.5px"
    fontWeight: 700
  caption:
    fontFamily: '"Sofia Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "clamp(15px, 4.1vw, 18px)"
    fontWeight: 560
    lineHeight: 1.35
  label:
    fontFamily: '"Sofia Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "15px"
    fontWeight: 600
    letterSpacing: "0.04em"
  note:
    fontFamily: '"Sofia Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "13.5px"
    fontWeight: 400
rounded:
  none: "0px"
spacing:
  gutter: "clamp(10px, 3.2vw, 40px)"
  pad: "clamp(16px, 4.6vw, 56px)"
  edge: "16px"
  edge-wide: "34px"
  section: "clamp(64px, 14vw, 140px)"
  "8": "8px"
  "10": "10px"
  "14": "14px"
  "22": "22px"
  "26": "26px"
  "30": "30px"
  "34": "34px"
components:
  button-primary:
    backgroundColor: "{colors.sun}"
    textColor: "{colors.deep}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "0 22px"
    height: "54px"
  button-primary-hover:
    backgroundColor: "{colors.sun-lift}"
  button-primary-active:
    backgroundColor: "{colors.sun-press}"
  button-primary-wide:
    padding: "0 30px"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.on-field}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "0 22px"
    height: "54px"
  button-line-paper:
    backgroundColor: "transparent"
    textColor: "{colors.field}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "0 22px"
    height: "54px"
  button-line-hover:
    backgroundColor: "rgba(143, 176, 230, 0.16)"
  sound-control:
    backgroundColor: "rgba(243, 246, 249, 0.94)"
    textColor: "{colors.deep}"
    typography: "{typography.control}"
    rounded: "{rounded.none}"
    padding: "0 14px 0 11px"
    height: "46px"
  sound-control-hover:
    backgroundColor: "{colors.on-field}"
  icon-control:
    backgroundColor: "rgba(11, 37, 89, 0.72)"
    textColor: "{colors.on-field}"
    rounded: "{rounded.none}"
    size: "46px"
  icon-control-off:
    backgroundColor: "rgba(11, 37, 89, 0.45)"
    textColor: "{colors.on-field-soft}"
  icon-control-hover:
    backgroundColor: "rgba(11, 37, 89, 0.9)"
  caption-line:
    backgroundColor: "rgba(11, 37, 89, 0.82)"
    textColor: "{colors.on-field}"
    typography: "{typography.caption}"
    rounded: "{rounded.none}"
    padding: "6px 10px 7px"
  language-switch:
    textColor: "{colors.ink-soft}"
    typography: "{typography.label}"
    padding: "0 8px"
    height: "44px"
    width: "44px"
  language-switch-active:
    textColor: "{colors.ink}"
  top-bar:
    textColor: "{colors.ink}"
    height: "56px"
  top-bar-wide:
    height: "72px"
  coat:
    backgroundColor: "{colors.field}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.none}"
    padding: "22px 22px 30px"
  strip-band-1:
    backgroundColor: "{colors.light}"
    textColor: "{colors.deep}"
    rounded: "{rounded.none}"
    padding: "26px 26px 30px"
  strip-band-2:
    backgroundColor: "{colors.mid}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.none}"
    padding: "26px 26px 30px"
  strip-band-3:
    backgroundColor: "{colors.deep}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.none}"
    padding: "26px 26px 30px"
  strip-band-latent:
    backgroundColor: "{colors.sensitizer}"
    textColor: "{colors.deep}"
  strip-band-wide:
    padding: "34px 32px 38px"
  email-address:
    textColor: "{colors.field}"
    typography: "{typography.address}"
  skip-link:
    backgroundColor: "{colors.deep}"
    textColor: "{colors.on-field}"
    rounded: "{rounded.none}"
    padding: "10px 14px"
---

# Design System: webbiespirit

## Overview

**Creative North Star: "The Daylight Sun-Print"**

The page is a cyanotype made in sunlight. Every blue surface is a coat of Prussian emulsion brushed onto cool cotton paper. A coat has three layers: a flat colour from a four-step exposure scale, a tiled mottle of brush streaks inside it, and a ragged hand-coated edge cut by an alpha mask. Type and drawings read as what the light left behind: white exposures on the coats and Prussian ink on the paper.

Density is low and the page is built for the phone first. It has one column, one coat that fills the first screen, large serif statements and one action within reach of the thumb. Tone changes in hard steps and never blends. The test strip, the step wedge and the exposure scale are all banded like a printer's test exposure. Motion is development: surfaces start latent, in unwashed sensitizer, and develop to their exposure on one slow exponential ease-out. Where the browser supports scroll timelines, the photograms expose with scroll position.

There is one warm colour, a yellow-green sunlight, and it falls only on the primary action. The page is light-only (no dark scheme). It refuses the category default of a dark studio hero with a gradient blob over a grid of laptop mockups. So it has no gradient fields, no shadows and no card grid.

**Key Characteristics:**
- A four-step Prussian exposure scale on cool cotton paper, where tone changes in hard steps.
- Every coat has three layers: flat exposure colour, a 384px emulsion mottle tile, and a brushed mask-border edge.
- Type is a white exposure on the coats and Prussian ink on the paper.
- One warm accent, sunlight, used only on the primary action.
- Square corners and no shadows. Depth comes from exposure, edge and grain.
- Development motion: latent sensitizer develops to its exposure over 1400ms on an exponential ease-out.
- Phone first: 54px actions, 46px video controls, and a thumb dock below 900px.

## Colors

The palette is a cold monochrome of Prussian blues on blue-white paper. It has one warm yellow-green for sunlight and a pale khaki that only appears while a surface develops.

### Primary
- **Deep Prussian** (#0B2559): the fullest exposure. It is the third test-strip band, the backing behind the presenter and olive videos, the skip link, and the text colour on sunlight and on the pale band. As a translucent veil over video it sits under the caption line (at .82) and the icon controls (at .72, at .45 when off, and at .9 on hover).
- **Cobalt Field** (#163F94): the brand cobalt, matched to the presenter's clothes. It fills the hero coat and the mark's disc. It is also the email address, the text and ring of the line button on paper, the underline under the selected language, and the ring of the sound control while sound is on.
- **Mid Exposure** (#2F63C7): the second test-strip band. It is the default focus ring on paper and the text-selection fill, and it sets "spirit" in the wordmark. At .45 it underlines the email address.
- **Pale Exposure** (#8FB0E6): the first test-strip band, with deep text. At .16 it is the hover wash on line buttons.

### Secondary
- **Sunlight** (#E0E46A): the fill of the primary action ("Say hello"), with deep text at 10.87:1. It also draws the keyboard focus ring inside dark coats.
- **Sunlight Pressed** (#C9CF48): the primary action while it is pressed.
- **Sunlight Lifted** (#EAEC86): the primary action on hover, for fine pointers only.

### Tertiary
- **Unwashed Sensitizer** (#DAD69C): the latent state, and nothing else. Test-strip and step-wedge bands wait in it, with deep text (9.89:1), until they develop. The olive print's latent state is the matching warm cast made with a filter (sepia .6, saturate .5, brightness 1.28) rather than this colour.

### Neutral
- **Cotton Paper** (#F3F6F9): the page ground, under a 160px paper-grain tile of faint light and dark fibres (alpha at most 34/255). It is also the browser theme colour, the first band of the step wedge, the sound control (at .94) and the phone dock's fade (at .97).
- **Ink** (#0B2559): the deepest exposure used as text on paper (13.6:1). It is the same pigment as Deep Prussian under a text role.
- **Faded Ink** (#3A5486): secondary text on paper, at 6.93:1. It sets the unselected language, the closing lead, the photo caption and the footer.
- **White Exposure** (#FFFFFF): text, icons and photograms on the field, mid and deep surfaces.
- **Soft Exposure** (#D3DFF5): the hero lead on the field, and the icon of a control that is switched off.

### Named Rules
**The Sunlight Rule.** Sunlight fills one thing: the primary action, "Say hello", in the hero, in the closing section and in the phone dock. Its only other use is the 2px keyboard focus ring inside dark coats, where a mid-blue ring would sit at 1.72:1 against the field. Controls, links, headings, the mark and the sound control never take it. The sound control is paper.

**The Hard Step Rule.** Tone moves between exposure steps in hard bands, never in blends. Bands meet edge to edge, with no gap and no gradient between them.

**The Worst Pixel Rule.** Each surface gets the mottle strength that keeps its text at WCAG AA on the tile's most extreme pixel, not just on the flat colour. The strong tile, which lightens by up to 43/255 white and darkens by up to 84/255 deep as shipped, sits under the hero field (white text no lower than 6.20:1, soft lead no lower than 4.62:1) and the deep band. The soft tile (23/255 and 54/255) sits under the pale and mid bands and the step wedge's pale, mid and deep steps; the wedge's paper step is bare paper. The mid band carries white text on the soft tile (no lower than 4.70:1), because the strong tile would drop it to 4.04:1.

## Typography

**Display Font:** Piazzolla (with Iowan Old Style, Georgia, serif). Self-hosted variable font, weight 100–900, optical size 8–30, with Latin, Latin Extended and Greek subsets.
**Body Font:** Sofia Sans (with system-ui, -apple-system, Segoe UI, sans-serif). Self-hosted variable font, weight 1–1000, with the same three subsets.

**Character:** A crisp, slightly inky book serif carries everything the page states: the headline, the steps, the numerals and the address. A narrow, upright sans carries reading text and every control. Both fonts carry Greek, so the English and Greek pages set the same way.

### Hierarchy
- **Display** (560, clamp(36px, 10.4vw, 96px), from 900px clamp(44px, min(7.2vw, 21cqi), 96px) in English and clamp(44px, min(7.2vw, 15.4cqi), 96px) in Greek, against its own column (clamp(60px, 7.2vw, 96px) without container queries): it never grows past the 7.2vw size and shrinks only where its two lines would not fit, line height 0.98, tracking -0.022em, word spacing .08em, balanced wrap): the hero headline only, white on the field.
- **Headline** (520, clamp(30px, 7.6vw, 64px), line height 1.02, tracking -0.018em, word spacing .08em, balanced wrap): section heads, in ink on paper. From 900px the "where" headline grows to clamp(44px, 4.8vw, 70px), within 16ch.
- **Numeral** (300, clamp(56px, 15vw, 96px), line height 0.8, lining figures, opacity .9): the test-strip step numbers.
- **Title** (460, clamp(22px, 5.6vw, 32px), line height 1.15, word spacing .07em, max 22ch, balanced wrap): test-strip step text.
- **Address** (480, clamp(22px, 6.4vw, 40px), line height 1.1): the email address in field blue, with a 2px underline and breaks allowed anywhere.
- **Wordmark** (520, 22px, 26px from 900px, line height 1, tracking -0.01em, optical size 24): lowercase "webbiespirit" in the bar, with "spirit" at 360 in mid.
- **Lead** (400, clamp(17px, 4.4vw, 21px), line height 1.45, max 36ch, pretty wrap): the hero support line, in soft exposure. The closing lead uses clamp(17px, 4.4vw, 20px) at body leading, max 40ch, in faded ink.
- **Body** (400, 17px, line height 1.55): base text.
- **Button** (720, 17px, tracking +0.01em): every action label.
- **Control** (700, 15.5px): the sound control's label.
- **Caption** (560, clamp(15px, 4.1vw, 18px), line height 1.35, centred, max 40ch): the captions the page draws over the video.
- **Label** (600, 15px, tracking +0.04em): the language switch. The photogram's "Illustration" caption uses the same weight and tracking at 13px.
- **Note** (400, 13.5px): the sun-print caption, in faded ink. The footer is 14.5px.

### Named Rules
**The Two Voices Rule.** Piazzolla states and Sofia Sans instructs. Headlines, step text, numerals, the address and the wordmark are serif. Reading text, captions and every control label are sans.

**The Optical Ceiling Rule.** The shipped Piazzolla subsets end their optical-size axis at 30, so every display role renders at optical size 30. Only the wordmark (24) sits inside the axis. A larger optical size changes nothing unless a font that carries it is shipped.

## Layout

The page is built for the phone first and runs in one column. The top bar is 56px tall (72px from 900px) plus the safe-area inset. It is plain paper, inset by the gutter plus 8px, with the mark on the left and the language switch on the right.

**Hero.** One coat fills the first screen, inset by the gutter on both sides and padded 22px, 22px and 30px. The 9:16 print is centred and sized from the viewport height: min(100%, (100svh − bar − 300px) × 9/16), never narrower than min(100%, 240px). This leaves the lower third for the headline, a 14px gap, the lead, a 22px gap and the actions. Actions wrap with 10px gaps. The sun button grows from a 200px basis, so on a phone it takes the full width.

**Sections.** The how, where and hello sections are inset by the gutter plus half the pad. The how and where sections open with the section spacing. Hello opens with clamp(72px, 15vw, 150px) and closes with clamp(56px, 10vw, 110px). Inner gaps are fluid: the strip sits clamp(26px, 6vw, 48px) below its head, "where" uses clamp(22px, 5vw, 40px) and "hello" uses clamp(26px, 6vw, 56px). Fixed spacing comes from a short ladder of 8, 10, 14, 22, 26, 30 and 34px.

**Test strip on a phone.** Three bands stack, each with its numeral and text side by side (auto and 1fr, 16px apart) and a minimum height of 150px. The photogram spans the full band beneath them.

**From 900px, the landscape sheet.** The hero coat becomes a two-column grid (auto, then minmax(0, 1fr)) with a column gap of clamp(36px, 5vw, 88px), padding 34px clamp(28px, 4vw, 64px) 40px 34px, and a maximum width of 1320px. The print sits off-centre at the left, width min(84svh, 860px) × 9/16, capped at 40vw so a narrow, tall window still leaves the copy room. Sun buttons stop stretching and take 0 30px padding. All sections cap at 1320px. The strip becomes three columns: each band is at least 300px tall, padded 34px, 32px and 38px, stacked inside with a 24px gap, and the photogram is pushed to the bottom. "Where" and "hello" split 5fr to 6fr. The olive print moves right, up to 420px wide, and the presenter's sun-print grows to 440px.

**From 1200px, the step wedge.** Four bands, from paper through pale and mid to deep, stand at the coat's right edge: 26px from the top, 30px from the bottom, the edge width less 10px from the right, and clamp(92px, 7.2vw, 132px) wide (--wedge-w), of which the brushed coat shows about 70%. The coat's right padding is the edge width plus the wedge plus clamp(4px, 1vw, 18px), and its column gap tightens to clamp(36px, 4.2vw, 72px).

**Thumb reach.** Below 900px the phone dock is fixed to the bottom and holds a full-width sun button. The footer adds 104px plus the safe-area inset at its foot, so the dock never covers it. Touch targets are at least 44px (mark and language switch), 46px for video controls and 54px for actions. The bar, dock, footer and skip link respect the safe-area insets.

## Elevation & Depth

The system is flat. Nothing on the page casts a drop shadow. Depth comes from the material: the paper-grain tile on the ground, the mottle inside every coat, and the brushed mask edge that lets paper show through a coat's ragged border. Darker means more exposed, not nearer. Only two layers stack: the phone dock (z 30) and the skip link when it has focus (z 50). The dock arrives by sliding up over a paper fade, not by casting a shadow.

### Shadow Vocabulary
- **Line ring** (`box-shadow: inset 0 0 0 1.5px currentColor`): the outline of the line button. It takes the text colour, so it reads white on coats and field blue on paper.
- **Pressed ring** (`box-shadow: inset 0 0 0 2px var(--field)`): the sound control while sound is on.

### Named Rules
**The Contact Print Rule.** Nothing floats. A coat lies on the paper as emulsion does, and an element changes state through rings, washes and tone, never a lift. Glow exists only as halation inside a photogram exposure.

## Shapes

**Square corners.** Every control, coat, band, print and caption has 0 radius. The only circle in the interface is the mark's 16px sun disc: paper at the centre out to 32%, then the field from 33%. Drawn subjects inside a photogram may have their own curves, such as the phone silhouette in step two.

**Brushed edges.** Coats get their edge from a generated 480px alpha mask (emulsion-edge.png), applied as a mask border with a 64px slice, filled and stretched. The edge width is 16px on phones and 34px from 900px on the hero coat and the strip. The olive print uses a fixed 22px edge. The step wedge has its own mask (wedge-coat.png, 160 × 1200), drawn at the wedge's proportions and stretched to it with mask-size 100% 100%, so its brushed sides keep their size on screen instead of shrinking into a mask-border slice. Because mask-image is fetched with CORS, the page must be served over http(s) for it to show; opened from file:// the wedge is masked out. The strip is masked as one object, so its three bands share one ragged outline. Browsers without mask-border show clean rectangles, which still read as fields. The presenter's sun-print is a finished image and is shown without a CSS edge.

**Icons.** One stroke family: 22px, drawn on a 24-unit grid, stroke 1.75, square caps and miter joins. Their rectangles are square-cornered, and only the play triangle is filled.

**Lines.** Links underline at 1px with a .18em offset. The email address underlines at 2px. The footer sits under a 1px rule of deep at .14.

## Components

### Buttons
Confident, square slabs that answer the moment they are pressed.
- **Shape:** square (0 radius), at least 54px tall, padded 0 22px (0 30px for sun buttons from 900px), with a 10px gap before the icon. Labels never wrap.
- **Primary (sun):** deep text on sunlight, with the mail icon. It appears three times, all as "Say hello": in the hero, in the closing section and in the phone dock.
- **Hover / Active:** sunlight lifts to Sunlight Lifted on hover (fine pointers only) and drops to Sunlight Pressed when pressed. Every button scales to .97 on press over 120ms. Colour, background and ring changes take 160ms on the press ease.
- **Line (secondary):** transparent, with the 1.5px inset line ring in the text colour. It is white on the hero coat ("How it works") and field blue on paper ("Copy email", with the copy icon). On hover it takes a wash of Pale Exposure at .16. After a copy, the label briefly reads "Copied" for 2.2s, and a polite status region announces it.
- **Focus:** a 2px ring offset 3px, in mid on paper and in sunlight inside the coats.

### The print and its controls
The 9:16 print sits on a deep backing inside the hero coat. It carries no label or badge. Only its control row and captions sit on it.
- **Control row:** inset 10px from the print's bottom and sides, with 8px gaps. The sound control sits bottom-left, then pause/play and captions sit at the right.
- **Sound control:** paper at .94 with deep text, 46px tall, padded 0 14px 0 11px, with an icon and a label that changes ("Sound on", "Sound off", "Replay"). While sound is on it shows the pressed ring. On hover the paper turns fully white. Pressed, it scales to .95.
- **Icon controls:** 46px squares, with white icons on deep at .72. When off (captions hidden) the veil drops to .45 and the icon turns soft exposure. On hover the veil deepens to .9.
- **Captions:** drawn by the page 66px above the print's bottom, centred, at most 40ch. White caption type sits on a deep veil at .82, padded 6px 10px 7px, and the veil repeats on every wrapped line. Captions never overlap the controls.

### Language switch
- **Style:** two 44px targets, "EN" and "ΕΛ", in the label voice, padded 0 8px.
- **States:** unselected is faded ink with a transparent 2px bottom border. Selected is ink with a field-blue underline. Hover turns to ink and press to field blue, over 160ms.

### Mark
The 16px sun disc and the lowercase wordmark, 10px apart, in a 44px-tall link. "webbie" is set at 520 in ink and "spirit" at 360 in mid.

### Emulsion coat (signature)
The base surface of the world: a field fill, the strong mottle tile at 384px and the brushed edge at the edge width. Text on a coat is white, and leads are soft exposure. The hero coat is the main example.

### Test strip (signature)
The three steps of the free preview are three exposures on one strip: pale, mid and deep, in that order. They form a single masked object with no gaps. The pale and mid bands carry the soft mottle tile, and the deep band carries the strong one.
- **Develop:** when script and motion are allowed, each band starts latent (sensitizer with deep text). Once 35% of a band is in view (the bottom of the viewport is pulled up 8%), it develops after 180ms plus 260ms per earlier sibling. Background and text colour change over 1400ms on the exponential ease-out. Without script, or with reduced motion, the bands show their exposure from the start.

### Photogram
The step-two drawing is a filled SVG exposure, 84px wide, in white (deep at .45 while its band is latent), and has no strokes. It is a phone silhouette filled with a currentColor glass gradient (.56 to .38 to .26 opacity), holding solid and .9/.8/.7-opacity blocks. A contact filter roughens the shapes with fractal noise (a 2.6 displacement) and softens them with a 1.1 blur, like a contact print. Under that it lays halation outside the outline only: the solid silhouette, dilated by 2 and blurred by 7, cut out by the silhouette softened by the same 1.1 blur (so no seam opens at the outline) and set at .62 alpha, so light spreads past the edge without washing out the glass inside. A 13px white "Illustration" caption labels it. Where CSS scroll timelines exist and motion is allowed, the drawing exposes with scroll position as its band enters: it goes from .3 opacity and a 2px blur to full, on a linear timeline.

### Olive print
A 3:4 print on a deep backing with a 22px brushed edge. Its looping video is scaled to 1.14 from 40% 32%, which crops past the sheet's cream margin. It develops from the warm latent filter to clean. Where scroll timelines exist, that change follows scroll position as the print enters the viewport. Elsewhere it is a 1400ms transition triggered when the print comes into view.

### Step wedge
From 1200px, four bands (bare paper, then pale, mid and deep on the soft mottle) stand at the coat's right edge as one narrow brushed coat with its own mask. They develop from sensitizer in turn when the hero loads.

### Email address
Set in the address voice in field blue, with a 2px underline in mid at .45. On hover (fine pointers) the underline turns solid mid.

### Phone dock
Below 900px, a full-width sun button rides at the bottom of the screen. It sits over a paper fade (.97 out to 62%, then clear), padded 10px with safe-area insets. It appears only while neither in-page "Say hello" is fully on screen. It slides in from translateY(110%) over 320ms on the exponential ease-out, and leaves the focus order while hidden.

### Skip link
Deep with white text, weight 600, padded 10px 14px. It is hidden above the bar until it receives focus.

## Do's and Don'ts

### Do:
- **Do** keep Sunlight (#E0E46A) as the fill of the primary action only: "Say hello" in the hero, in the closing section and in the phone dock.
- **Do** lay every cobalt surface as a coat: an exposure-step fill, the 384px mottle tile, and the brushed mask-border at the edge width (16px, or 34px from 900px).
- **Do** choose the mottle tile by worst-pixel contrast: strong under the field and the deep band, soft under the pale and mid bands.
- **Do** step tone in hard bands through paper, pale, mid, field and deep.
- **Do** set statements in Piazzolla (300–560, negative tracking on display and headline) and reading text and every control in Sofia Sans.
- **Do** give actions at least 54px of height, video controls 46px and every other target 44px.
- **Do** develop surfaces from sensitizer over 1400ms on cubic-bezier(.16, 1, .3, 1), and answer presses with a 120ms scale (.97 for buttons, .95 for controls).
- **Do** remove the latent state, the transitions and the autoplay when reduced motion is requested.

### Don't:
- **Don't** give sunlight to controls, links, headings, the mark or decoration. The sound control is paper (#F3F6F9 at .94) with deep text.
- **Don't** round interface corners. The only circle is the mark's sun disc.
- **Don't** add drop shadows or glows to the interface. Halation belongs to photogram exposures only.
- **Don't** blend between exposure steps or add colours outside the tokens.
- **Don't** put white text on the strong mottle over the mid band; it falls to 4.04:1.
- **Don't** break the test strip into separate cards. Its bands share one masked outline with no gaps.
- **Don't** put a label or badge about how the presenter was made on the print or anywhere else on the page (the owner's decision, 2026-10-12, recorded in PRODUCT.md).
- **Don't** tune Piazzolla's optical size above 30. The shipped font stops there.
