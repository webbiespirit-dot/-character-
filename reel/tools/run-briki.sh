#!/bin/bash
cd /home/user/-character-/reel
while ! grep -q "EXTRAS DONE" raw/capture.log; do sleep 5; done
node tools/capture.mjs tools/sites.mjs briki >> raw/capture.log 2>&1
echo "BRIKI DONE" >> raw/capture.log
