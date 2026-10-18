"""Fit a music file to the reel grid: estimate the tempo precisely, time-stretch to exactly 120 BPM
(two passes), put the strongest drop on a beat at 2.0 s, trim to 28.5 s, fade the tail, normalise loudness.
Usage: python3 tools/fit_track.py <input audio> [--out audio/track.wav]"""
import sys, json, subprocess, numpy as np, librosa, soundfile as sf, warnings
warnings.filterwarnings('ignore')
src = sys.argv[1]
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'audio/track.wav'
SR = 44100

def stretch(path_in, rate, path_out):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', path_in, '-af', f'atempo={rate:.6f}', '-ar', str(SR), path_out], check=True)

def period(y, bpm_hint=None):
    kw = {'bpm': bpm_hint} if bpm_hint else {}
    _, b = librosa.beat.beat_track(y=y, sr=SR, units='time', **kw)
    k = np.arange(len(b)); p = np.polyfit(k, b, 1)[0]
    return p, b

y, _ = librosa.load(src, sr=SR, mono=True)
sf.write('/tmp/fit0.wav', y, SR)
p0, _ = period(y)
bpm0 = 60 / p0
bpm_use = min([bpm0, bpm0 * 2, bpm0 / 2], key=lambda c: abs(c - 120))
rate = 120.0 / bpm_use
print(f'tempo {bpm0:.2f} (using {bpm_use:.2f}), rate {rate:.4f}')
stretch('/tmp/fit0.wav', rate, '/tmp/fit1.wav')
y1, _ = librosa.load('/tmp/fit1.wav', sr=SR, mono=True)
p1, _ = period(y1, 120)
corr = p1 / 0.5
print(f'after pass 1: period {p1*1000:.1f} ms, correction {corr:.4f}')
if abs(corr - 1) > 0.0005:
    stretch('/tmp/fit1.wav', corr, '/tmp/fit2.wav')
    y1, _ = librosa.load('/tmp/fit2.wav', sr=SR, mono=True)
    p1, _ = period(y1, 120)
    print(f'after pass 2: period {p1*1000:.1f} ms')
hop = 512
# beat phase: the offset within a 0.5 s beat where onsets are strongest
oe = librosa.onset.onset_strength(y=y1, sr=SR, hop_length=hop)
ot = librosa.frames_to_time(np.arange(len(oe)), sr=SR, hop_length=hop)
def grid_score(sig, tt, phase, step):
    g = np.arange(phase, tt[-1], step)
    return float(np.interp(g, tt, sig).mean())
phases = np.arange(0, 0.5, 0.004)
phi = float(phases[np.argmax([grid_score(oe, ot, f, 0.5) for f in phases])])
# drop: biggest rise of short-term energy, snapped to the beat phase
rms = librosa.feature.rms(y=y1, frame_length=2048, hop_length=hop)[0]
times = librosa.frames_to_time(np.arange(len(rms)), sr=SR, hop_length=hop)
w = int(1.0 / (hop / SR))
rise = np.array([rms[i:i + w].mean() - rms[max(0, i - w):i].mean() if i >= w else 0 for i in range(len(rms))])
rise[(times < 2.0) | (times > len(y1) / SR - 27)] = 0
t_rise = times[int(np.argmax(rise))]
drop_t = phi + round((t_rise - phi) / 0.5) * 0.5
start = drop_t - 2.0
seg = y1[int(start * SR): int((start + 28.5) * SR)]
seg = np.pad(seg, (0, max(0, int(28.5 * SR) - len(seg))))
fi = int(0.06 * SR); seg[:fi] *= np.linspace(0, 1, fi)
fo = int(1.2 * SR); seg[-fo:] *= np.linspace(1, 0, fo) ** 1.5
sf.write('/tmp/fit_raw.wav', seg, SR)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/tmp/fit_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', str(SR), out], check=True)
# verify: onset phase of the result against the 0.5 s grid (0 = on the grid)
yo, _ = librosa.load(out, sr=SR, mono=True)
oeo = librosa.onset.onset_strength(y=yo, sr=SR, hop_length=hop)
oto = librosa.frames_to_time(np.arange(len(oeo)), sr=SR, hop_length=hop)
sc = [grid_score(oeo, oto, f, 0.5) for f in phases]
pho = float(phases[np.argmax(sc)]); err = min(pho, 0.5 - pho) * 1000
print(f'drop at {drop_t:.2f}s (start {start:.2f}s); result onset phase off grid by {err:.0f} ms; on-grid/off-grid onset ratio {max(sc)/np.mean(sc):.2f}')
json.dump({'source': src, 'tempo': bpm0, 'rate': rate, 'start_s': start, 'grid_error_ms': err}, open(out.rsplit('.', 1)[0] + '_fit.json', 'w'), indent=1)
