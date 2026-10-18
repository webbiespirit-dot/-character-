import { continueRender, delayRender, staticFile } from 'remotion';
const LATIN_EXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF';
const GREEK = 'U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF';
const face = (fam: string, file: string, weight: string, style = 'normal', range?: string) =>
  `@font-face{font-family:"${fam}";font-style:${style};font-weight:${weight};font-display:block;${range ? `unicode-range:${range};` : ''}src:url(${staticFile('fonts/' + file)}) format("woff2")}`;
const css = [
  face('Syne', 'syne-normal-latin.woff2', '400 800'),
  face('Syne', 'syne-normal-latin-ext.woff2', '400 800', 'normal', LATIN_EXT),
  face('Syne', 'syne-normal-greek.woff2', '400 800', 'normal', GREEK),
  face('Instrument Sans', 'instrumentsans-normal-latin.woff2', '400 700'),
  face('Instrument Sans', 'instrumentsans-normal-latin-ext.woff2', '400 700', 'normal', LATIN_EXT),
  face('Instrument Sans', 'instrumentsans-italic-latin.woff2', '400', 'italic'),
].join('\n');
let installed = false;
export const ensureFonts = () => {
  if (installed || typeof document === 'undefined') return;
  installed = true;
  const handle = delayRender('fonts');
  const style = document.createElement('style'); style.textContent = css; document.head.appendChild(style);
  Promise.all([document.fonts.load('800 40px "Syne"'), document.fonts.load('700 40px "Syne"'), document.fonts.load('600 40px "Instrument Sans"'), document.fonts.load('400 40px "Instrument Sans"')])
    .then(() => continueRender(handle)).catch(() => continueRender(handle));
};
