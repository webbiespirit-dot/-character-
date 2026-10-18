#!/bin/bash
cd /home/user/-character-/reel
while ! grep -q "BRIKI DONE" raw/capture.log; do sleep 5; done
node tools/capture.mjs tools/sites.mjs adams >> raw/capture.log 2>&1
echo "ALL DONE" >> raw/capture.log
