#!/bin/bash
# Re-capture the café-bar with the app-script rewrite (vinyl label name), re-shoot its before frame, rebuild the manifest.
cd /home/user/-character-/reel
node -e "
import('./tools/capture.mjs').then(async (m) => { const s = await import('./tools/sites.mjs'); const cfg = s.EXTRAS.find((c) => c.id === 'kafenio11'); try { await m.captureSite(cfg); } catch (e) { console.error('kafenio11 FAILED', e); } });
" >> raw/capture.log 2>&1
node tools/before.mjs kafenio11 >> raw/capture.log 2>&1
node tools/manifest.mjs >> raw/capture.log 2>&1
echo "KAF2 DONE" >> raw/capture.log
