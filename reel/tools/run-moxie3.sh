#!/bin/bash
# Re-capture the hair salon after the per-letter name swap fix, then re-shoot its before frame and rebuild the manifest.
cd /home/user/-character-/reel
node -e "
import('./tools/capture.mjs').then(async (m) => { const s = await import('./tools/sites.mjs'); const cfg = s.EXTRAS.find((c) => c.id === 'moxie-hair'); try { await m.captureSite(cfg); } catch (e) { console.error('moxie-hair FAILED', e); } });
" >> raw/capture.log 2>&1
node tools/before.mjs moxie-hair >> raw/capture.log 2>&1
node tools/manifest.mjs >> raw/capture.log 2>&1
echo "MOXIE3 DONE" >> raw/capture.log
