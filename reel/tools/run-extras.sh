#!/bin/bash
# wait for the main capture to finish, then capture the extras (sequential, to keep CPU for one browser)
cd /home/user/-character-/reel
while pgrep -f "capture.mjs tools/sites.mjs hoa" >/dev/null; do sleep 5; done
node -e "
import('./tools/capture.mjs').then(async (m) => { const s = await import('./tools/sites.mjs'); for (const cfg of s.EXTRAS) { try { await m.captureSite(cfg); } catch (e) { console.error(cfg.id, 'FAILED', e); } } });
" >> raw/capture.log 2>&1
echo "EXTRAS DONE" >> raw/capture.log
