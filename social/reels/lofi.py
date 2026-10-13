"""A short, original lofi track for the Briki reel: Rhodes-style chords, warm bass, soft drums, vinyl."""
import numpy as np, wave, sys

SR = 44100
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 36.8
BPM = 72.0
BEAT = 60.0 / BPM
N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.cos((pan + 1) * np.pi / 4)
    R[i:i + len(sig)] += sig * np.sin((pan + 1) * np.pi / 4)

def rhodes(m, dur, vel=1.0):
    t = np.arange(int(SR * dur)) / SR
    f = hz(m)
    idx = 1.6 * np.exp(-t * 6.0) + 0.15          # FM bark that fades into a round tone
    mod = np.sin(2 * np.pi * f * t) * idx
    tone = np.sin(2 * np.pi * f * t + mod) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)
    env = (1 - np.exp(-t * 300)) * np.exp(-t * 1.1)
    trem = 1 + 0.08 * np.sin(2 * np.pi * 4.2 * t)
    rel = np.minimum(1, (dur - t) / 0.08)        # short release at the end
    return tone * env * trem * rel * vel * 0.16

def bass(m, dur):
    t = np.arange(int(SR * dur)) / SR
    f = hz(m)
    tone = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * 2 * f * t)
    env = (1 - np.exp(-t * 80)) * np.exp(-t * 1.4) * np.minimum(1, (dur - t) / 0.06)
    return tone * env * 0.30

def pad(ms, dur):
    t = np.arange(int(SR * dur)) / SR
    s = np.zeros_like(t)
    for m in ms:
        for d in (-0.08, 0.08):
            f = hz(m) * 2 ** (d / 12)
            s += np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / 0.9) * np.minimum(1, (dur - t) / 0.9)
    return s * env * 0.012

def kick():
    t = np.arange(int(SR * 0.35)) / SR
    f = 45 + 70 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 11) * 0.55

def noise_hit(dur, decay, hp_steps):
    t = np.arange(int(SR * dur)) / SR
    n = rng.standard_normal(len(t))
    for _ in range(hp_steps):                      # crude high-pass: first difference
        n = np.diff(n, prepend=0)
    n /= np.max(np.abs(n)) + 1e-9
    return n * np.exp(-t * decay)

def snare():
    t = np.arange(int(SR * 0.22)) / SR
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 30) * 0.18
    return body + noise_hit(0.22, 26, 1) * 0.10

def hat():
    return noise_hit(0.05, 90, 3) * 0.035

# Fmaj7 · Em7 · Dm7 · Cmaj9, voiced around middle C (one bar each)
CHORDS = [
    (41, [57, 60, 64, 65]),      # F: A C E F
    (40, [55, 59, 62, 64]),      # Em7: G B D E
    (38, [53, 57, 60, 62]),      # Dm7: F A C D
    (36, [55, 59, 62, 64]),      # Cmaj9: G B D E over C
]
MELODY = {  # bar index in the 4-bar loop -> (beat offset, midi, length in beats)
    0: [(2.5, 72, 1.0), (3.5, 69, 0.5)],
    1: [(0.0, 67, 1.5), (2.0, 71, 1.0), (3.0, 74, 1.0)],
    2: [(0.5, 72, 1.0), (2.0, 69, 1.5)],
    3: [(1.0, 67, 2.5)],
}

bar = 4 * BEAT
nbars = int(np.ceil(DUR / bar))
swing = 0.06
for b in range(nbars):
    t0 = b * bar
    root, notes = CHORDS[b % 4]
    # chords: on 1 and a soft re-hit on the "and" of 2, slightly strummed
    for k, n in enumerate(notes):
        add(rhodes(n, bar * 0.95, 0.9), t0 + k * 0.012, pan=-0.25 + 0.17 * k)
    for k, n in enumerate(notes[1:]):
        add(rhodes(n, bar * 0.45, 0.45), t0 + 1.5 * BEAT + swing + k * 0.01, pan=0.2 - 0.15 * k)
    add(pad(notes, bar + 0.6), t0, pan=0.0)
    add(bass(root, 2.4 * BEAT), t0)
    add(bass(root + 7 if b % 2 else root, 1.2 * BEAT), t0 + 2.5 * BEAT + swing)
    intro = b == 0
    if b >= 1 and b < nbars - 1:      # drums come in after the first bar, drop for the last
        add(kick(), t0); add(kick(), t0 + 2.5 * BEAT + swing, gain=0.7)
        add(snare(), t0 + BEAT, pan=0.05); add(snare(), t0 + 3 * BEAT, pan=0.05)
        for e in range(8):
            add(hat(), t0 + e * BEAT / 2 + (swing if e % 2 else 0), pan=0.35, gain=0.6 + 0.4 * (e % 2))
    if b >= 2:                         # melody from bar 3 on, an octave-friendly register
        for off, m, ln in MELODY[b % 4]:
            add(rhodes(m, ln * BEAT + 0.4, 0.75), t0 + off * BEAT + (swing if off % 1 else 0), pan=0.15)

# vinyl: soft hiss + sparse crackle
hiss = rng.standard_normal(N)
hiss = np.convolve(hiss, np.ones(18) / 18, mode='same') * 0.006
crk = np.zeros(N)
for i in rng.integers(0, N - 50, int(DUR * 9)):
    crk[i:i + 3] += rng.uniform(-1, 1) * rng.uniform(0.02, 0.07)
L += hiss + crk; R += hiss + np.roll(crk, 37)

st = np.stack([L, R], 1)
st /= np.max(np.abs(st)) * 1.12
t = np.arange(N) / SR
st *= np.minimum(1, t / 1.2)[:, None] * np.minimum(1, (DUR - t) / 3.0)[:, None]
pcm = (st * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote', sys.argv[1], round(DUR, 2), 's')
