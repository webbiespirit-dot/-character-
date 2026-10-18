#!/bin/bash
# Extract QA frames from the final render: one per shot (+8 frames in), the hook, the ending, and strips around cuts.
set -e
cd /home/user/-character-/reel
rm -rf out/qa && mkdir -p out/qa
V=webbiespirit-reel.mp4
frames="40 68 128 188 248 308 353 398 428 458 488 548 608 668 713 760 800 830"
for f in $frames; do ffmpeg -y -loglevel error -ss $(python3 -c "print($f/30)") -i $V -frames:v 1 out/qa/frame-$f.png; done
# strips: 8 consecutive frames around five cuts, scaled down, side by side
python3 - <<'PY'
import subprocess, os
from PIL import Image
cuts={'drop':60,'whip':120,'glitch':180,'break':450,'slam':480,'outro':750}
for name,c in cuts.items():
    ims=[]
    for f in range(c-3,c+5):
        p=f'/tmp/qa_{f}.png'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(f/30),'-i','webbiespirit-reel.mp4','-frames:v','1',p],check=True)
        ims.append(Image.open(p).convert('RGB').resize((270,480), Image.LANCZOS)); os.remove(p)
    S=Image.new('RGB',(len(ims)*274,480),(30,30,30))
    for i,im in enumerate(ims): S.paste(im,(i*274,0))
    S.save(f'out/qa/strip-{name}-f{c-3}-to-f{c+4}.jpg',quality=85)
print('strips ok')
PY
ls out/qa | wc -l
