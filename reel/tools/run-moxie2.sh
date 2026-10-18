#!/bin/bash
cd /home/user/-character-/reel
while ! grep -q "ADAMS DONE" raw/capture.log; do sleep 5; done
node -e "
import('./tools/capture.mjs').then(async (m) => { const s = await import('./tools/sites.mjs'); const cfg = s.EXTRAS.find((c) => c.id === 'moxie-hair'); try { await m.captureSite(cfg); } catch (e) { console.error('moxie-hair FAILED', e); } });
" >> raw/capture.log 2>&1
echo "MOXIE2 DONE" >> raw/capture.log
