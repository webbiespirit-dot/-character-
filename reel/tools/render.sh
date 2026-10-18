#!/bin/bash
# Final render: mp4 (H.264 + AAC), cover frame, 5 verification frames, size check.
set -e
cd /home/user/-character-/reel
node tools/manifest.mjs && cp audio/track.wav public/track.wav
/home/user/-character-/reel/node_modules/.bin/remotion render src/index.ts Reel webbiespirit-reel.mp4 --codec=h264 --crf=17 --pixel-format=yuv420p --audio-codec=aac --audio-bitrate=192k --concurrency=3 --log=error
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate -of default=nw=1 webbiespirit-reel.mp4
/home/user/-character-/reel/node_modules/.bin/remotion still src/index.ts Reel cover.png --frame=${COVER_FRAME:-40} --log=error
mkdir -p out/verify
for f in 40 150 285 480 800; do ffmpeg -y -loglevel error -ss $(python3 -c "print($f/30)") -i webbiespirit-reel.mp4 -frames:v 1 out/verify/frame-$f.png; done
ls -la webbiespirit-reel.mp4 cover.png out/verify/
