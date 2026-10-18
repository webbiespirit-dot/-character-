#!/bin/bash
cd /home/user/-character-/reel
node -e "
import('./tools/capture.mjs').then(async (m) => { const s = await import('./tools/sites.mjs'); for (const cfg of s.EXTRAS) { try { await m.captureSite(cfg); } catch (e) { console.error(cfg.id, 'FAILED', e); } } });
" >> raw/capture.log 2>&1
echo "EXTRAS DONE" >> raw/capture.log
