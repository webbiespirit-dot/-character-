#!/usr/bin/env python3
"""Procedural royalty-free track for the webbiespirit reel.
120 BPM (15 frames per beat at 30fps), 4/4, F minor. Writes audio/track.wav (stereo 44.1k)."""
import numpy as np, json, sys
from scipy import signal
import soundfile as sf

SR = 44100
BPM = 120.0
BEAT = 60.0 / BPM          # 0.5 s
BAR = 4 * BEAT             # 2.0 s
TOTAL = 28.5               # seconds incl. tail
N = int(TOTAL * SR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)

def sec(b): return b * BEAT
def place(buf, sig, start, gain=1.0):
    i = int(round(start * SR))
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    buf[i:i+n] += sig[:n] * gain

def exp_env(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))
def adsr(n, a, d, s_level, r, hold):
    """a,d,r in seconds; hold = time at sustain before release."""
    a_n, d_n, h_n, r_n = [int(x * SR) for x in (a, d, hold, r)]
    env = np.zeros(n)
    idx = 0
    seg = np.linspace(0, 1, max(a_n, 1)); k = min(len(seg), n - idx); env[idx:idx+k] = seg[:k]; idx += k
    seg = np.linspace(1, s_level, max(d_n, 1)); k = min(len(seg), n - idx); env[idx:idx+k] = seg[:k]; idx += k
    k = min(h_n, n - idx); env[idx:idx+k] = s_level; idx += k
    seg = s_level * np.exp(-np.arange(max(r_n, 1)) / (r / 4 * SR + 1)); k = min(len(seg), n - idx); env[idx:idx+k] = seg[:k]
    return env

def lp(x, fc, order=2):
    sos = signal.butter(order, min(fc, SR/2 - 100), 'low', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def hp(x, fc, order=2):
    sos = signal.butter(order, max(fc, 10), 'high', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [max(lo, 10), min(hi, SR/2 - 100)], 'band', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def sweep_lp(x, fc_start, fc_end, chunk=256):
    """Low-pass with cutoff moving exponentially from fc_start to fc_end over the signal."""
    out = np.zeros_like(x); zi = None; n = len(x); k = 0
    nchunks = int(np.ceil(n / chunk))
    fcs = np.geomspace(fc_start, fc_end, nchunks)
    for c in range(nchunks):
        sos = signal.butter(2, min(max(fcs[c], 30), SR/2 - 100), 'low', fs=SR, output='sos')
        if zi is None: zi = signal.sosfilt_zi(sos) * x[0]
        seg = x[k:k+chunk]
        y, zi = signal.sosfilt(sos, seg, zi=zi); out[k:k+chunk] = y; k += chunk
    return out

def saw(f, n, detune_cents=0.0, phase=0.0):
    f = f * 2 ** (detune_cents / 1200)
    ph = (phase + np.cumsum(np.full(n, f / SR))) % 1.0
    return 2 * ph - 1
def sine(f, n, phase=0.0):
    return np.sin(2 * np.pi * (phase + np.cumsum(np.full(n, f / SR))))

# ---------------- note tables (Hz) ----------------
def hz(name):
    names = {'C':0,'Db':1,'D':2,'Eb':3,'E':4,'F':5,'Gb':6,'G':7,'Ab':8,'A':9,'Bb':10,'B':11}
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o - 4) - 9) / 12)

# i - VI - III - v in F minor, one chord per bar
PROG = [
    (['F3','Ab3','C4','Eb4'], 'F2'),
    (['Db3','F3','Ab3','C4'], 'Db2'),
    (['Ab3','C4','Eb4','G4'], 'Ab2'),
    (['C3','Eb3','G3','Bb3'], 'C2'),
]

# ---------------- drums ----------------
def kick(n=int(0.45*SR)):
    tt = np.arange(n) / SR
    f = 42 + 140 * np.exp(-tt * 38)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    click = hp(rng.standard_normal(n) * np.exp(-tt * 900), 2000) * 0.5
    k = body * 0.8 + click * 1.2
    return np.tanh(k * 1.6) * 0.95
def clap(n=int(0.35*SR)):
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    env = np.zeros(n)
    for d in (0.0, 0.011, 0.023):           # three micro hits
        i = int(d * SR); env[i:] += np.exp(-(tt[:n-i]) * 70) * 0.7
    env += np.exp(-tt * 14) * 0.6            # tail
    return bp(noise * env, 1100, 8000) * 1.1
def snare(n=int(0.25*SR)):
    tt = np.arange(n) / SR
    tone = np.sin(2*np.pi*190*tt) * np.exp(-tt*35) * 0.5
    noise = bp(rng.standard_normal(n), 1500, 9000) * np.exp(-tt * 22)
    return (tone + noise) * 0.8
def hat(n=int(0.06*SR), open_=False):
    if open_: n = int(0.32 * SR)
    tt = np.arange(n) / SR
    env = np.exp(-tt * (12 if open_ else 95))
    return hp(rng.standard_normal(n), 6500) * env * (0.7 if open_ else 0.95)
def ride_tick(n=int(0.12*SR)):
    tt = np.arange(n) / SR
    return bp(rng.standard_normal(n), 4000, 12000) * np.exp(-tt * 40) * 0.5
def impact(n=int(1.6*SR)):
    tt = np.arange(n) / SR
    boom = np.sin(2*np.pi*np.cumsum(38 + 60*np.exp(-tt*6))/SR) * np.exp(-tt*2.2)
    crash = hp(rng.standard_normal(n), 3000) * np.exp(-tt*4.5) * 0.35
    return np.tanh(boom*1.4 + crash) * 0.9
def riser(dur, f0=300, f1=6000):
    n = int(dur * SR); tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n); chunk = 512; k = 0
    fcs = np.geomspace(f0, f1, int(np.ceil(n/chunk)))
    for c in range(len(fcs)):
        seg = noise[k:k+chunk]
        sos = signal.butter(2, [fcs[c]*0.6, min(fcs[c]*1.6, SR/2-100)], 'band', fs=SR, output='sos')
        out[k:k+chunk] = signal.sosfilt(sos, seg); k += chunk
    env = (tt / dur) ** 2.2
    return out * env * 0.8
def rev_cymbal(dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    c = hp(rng.standard_normal(n), 5000) * np.exp(-tt * 3)
    return c[::-1] * 0.4

# ---------------- synths ----------------
def chord_stab(freqs, dur, bright=1.0, hold=None):
    n = int(dur * SR)
    out = np.zeros(n)
    for f in freqs:
        for det in (-7, 0, 7):
            out += saw(f, n, det, rng.random()) / (3 * len(freqs))
    env = adsr(n, 0.012, 0.35, 0.55, 0.5, hold if hold is not None else max(dur - 0.9, 0.05))
    out = sweep_lp(out, 2600 * bright, 900 * bright)
    return out * env
def pad(freqs, dur):
    n = int(dur * SR)
    out = np.zeros(n)
    for f in freqs:
        for det in (-12, -4, 4, 12):
            out += saw(f / 2, n, det, rng.random()) / (4 * len(freqs))
        out += sine(f, n, rng.random()) / len(freqs) * 0.5
    env = adsr(n, 0.9, 0.1, 1.0, 2.2, max(dur - 3.2, 0.1))
    return lp(out, 1400) * env
def pluck(f, dur=0.28):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = (saw(f, n, 0, 0.1) * 0.5 + sine(f, n) * 0.5) * np.exp(-tt * 16)
    return lp(s, 3500)
def sub_bass(f, dur, duck_env=None):
    n = int(dur * SR)
    s = sine(f, n) * 0.9 + lp(saw(f, n), 420) * 0.5 + sine(2*f, n) * 0.18
    env = adsr(n, 0.006, 0.08, 0.85, 0.08, max(dur - 0.16, 0.02))
    return s * env

# ---------------- reverb & delay ----------------
def reverb(x, decay=1.4, wet=0.25, tone=4500):
    n = int(decay * SR); tt = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-tt * (6.9 / decay)); ir[0] = 0
    ir = lp(ir, tone); ir /= np.sqrt(np.sum(ir**2)) + 1e-9
    w = signal.fftconvolve(x, ir)[:len(x)]
    return x + w * wet
def delay(x, time, fb=0.38, wet=0.35, taps=6):
    d = int(time * SR); out = np.zeros_like(x); echo = x.copy()
    for k in range(1, taps + 1):
        echo = lp(echo, 3800) * fb
        s = np.zeros_like(x); s[k*d:] = echo[:len(x) - k*d]
        out += s
    return x + out * wet

# ---------------- arrangement ----------------
drums = np.zeros(N); bass = np.zeros(N); chords = np.zeros(N); arp = np.zeros(N); fx = np.zeros(N); outro = np.zeros(N)
duck = np.ones(N)   # sidechain envelope for bass/chords
kick_times = []

def add_kick(tm, g=1.0):
    place(drums, kick(), tm, g); kick_times.append(tm)

GROOVE_START_BAR = 1          # drop at 2.0 s
GROOVE_END = 25.0             # outro hit at 25.0 s
BREAK_BAR = 7                 # bar index whose beats 3-4 are the rhythm break (14.0 - 16.0 s)

# --- bar 0: hook (0-2 s): impact + four building kicks + snare roll + riser
place(fx, impact(), 0.0, 1.0)
for b in range(4):
    add_kick(sec(b), 0.6 + 0.12 * b)
for i in range(8):                       # 32nd roll in the last beat
    place(drums, snare(), sec(3) + i * BEAT / 8, 0.25 + 0.07 * i)
place(fx, riser(1.9), 0.1, 0.9)
place(fx, rev_cymbal(1.2), 0.8, 0.8)

# --- groove bars
bar = GROOVE_START_BAR
while sec(bar * 4) < GROOVE_END - 1e-6:
    t0 = sec(bar * 4)
    chord, root = PROG[(bar - GROOVE_START_BAR) % 4]
    cf = [hz(c) for c in chord]; rf = hz(root)
    in_break = (bar == BREAK_BAR)
    last_bar = sec((bar + 1) * 4) >= GROOVE_END - 1e-6
    # kicks: 4 on the floor, except break beats 3-4
    for b in range(4):
        if in_break and b >= 2: continue
        add_kick(t0 + sec(b), 1.0)
    # claps on 2 and 4 (skip during break beat 4)
    for b in (1, 3):
        if in_break and b == 3: continue
        place(drums, clap(), t0 + sec(b), 0.8)
        place(drums, snare(), t0 + sec(b), 0.35)
    # hats: closed 8ths with swing/humanize; open hat on offbeats from bar 3 on
    for e in range(8):
        tm = t0 + e * BEAT / 2 + (0.012 if e % 2 else 0) + rng.normal(0, 0.003)
        vel = 0.5 + 0.35 * (e % 2 == 0) + rng.normal(0, 0.05)
        if in_break and e >= 4: vel *= 0.6
        place(drums, hat(), tm, vel * 0.55)
        if bar >= GROOVE_START_BAR + 2 and e % 2 == 1 and not (in_break and e >= 4):
            place(drums, hat(open_=True), tm, 0.35)
    # 16th ride ticks for drive in later bars
    if bar >= GROOVE_START_BAR + 4:
        for s16 in range(16):
            if s16 % 4 == 2:
                place(drums, ride_tick(), t0 + s16 * BEAT / 4, 0.25)
    # bass: root on each beat, with octave pickup on the 'and' of 4
    for b in range(4):
        if in_break and b >= 2: continue
        place(bass, sub_bass(rf, BEAT * 0.9), t0 + sec(b), 0.9)
    if not in_break:
        place(bass, sub_bass(rf * 2, BEAT * 0.4), t0 + sec(3) + BEAT / 2, 0.5)
    # chords: stab on beat 1 and the 'and' of 2 (offbeat), brighter later
    bright = 0.8 + 0.35 * min(1.0, (bar - GROOVE_START_BAR) / 8)
    place(chords, chord_stab(cf, BAR * 0.9 if in_break else BEAT * 1.4, bright), t0, 0.7)
    if not in_break:
        place(chords, chord_stab(cf, BEAT * 0.9, bright), t0 + sec(1) + BEAT / 2, 0.5)
        place(chords, chord_stab(cf, BEAT * 0.7, bright), t0 + sec(3), 0.4)
    # arp from bar 5 on (16ths), skipped on the break
    if bar >= GROOVE_START_BAR + 4 and not in_break:
        pattern = [0, 2, 1, 3, 2, 0, 3, 1, 0, 2, 1, 3, 2, 3, 1, 0]
        for s16 in range(16):
            f = cf[pattern[s16]] * 2
            if s16 % 3 == 0: f *= 2
            place(arp, pluck(f), t0 + s16 * BEAT / 4 + rng.normal(0, 0.002), 0.22 + 0.06 * (s16 % 4 == 0))
    # break: filter-sweep riser + reverse cymbal into next bar
    if in_break:
        place(fx, riser(1.0, 400, 9000), t0 + sec(2), 0.8)
        place(fx, rev_cymbal(0.9), t0 + sec(3) + 0.1, 0.7)
    # final bar before outro: snare roll + riser on beats 3-4
    if last_bar:
        for i in range(16):
            place(drums, snare(), t0 + sec(2) + i * BEAT / 8, 0.2 + 0.05 * i)
        place(fx, riser(1.0, 500, 10000), t0 + sec(2), 0.9)
    bar += 1

# --- outro: hit at 25.0, pad sustain, soft chime for the CTA at 26.5, final tick at 27.5
place(fx, impact(), GROOVE_END, 0.9)
add_kick(GROOVE_END, 1.0)
place(outro, pad([hz(c) for c in PROG[0][0]], 3.5), GROOVE_END, 0.8)
place(bass, sub_bass(hz('F2'), 2.4), GROOVE_END, 0.8)
chime_notes = ['F5', 'Ab5', 'C6']
for i, nme in enumerate(chime_notes):
    place(arp, pluck(hz(nme), 0.6), GROOVE_END + 1.5 + i * 0.06, 0.45)
place(drums, hat(open_=True), GROOVE_END + 2.5, 0.3)

# ---------------- sidechain ----------------
for tm in kick_times:
    i = int(tm * SR); n = int(0.42 * SR)
    seg = 1 - 0.78 * np.exp(-np.arange(n) / (0.11 * SR))
    seg[:int(0.004*SR)] = 0.22
    k = min(n, N - i)
    if k > 0: duck[i:i+k] = np.minimum(duck[i:i+k], seg[:k])

bass *= duck
chords *= duck ** 0.7

# ---------------- mix ----------------
drums_w = reverb(drums, 0.9, 0.12, 6000)
chords_w = reverb(delay(chords, BEAT * 0.75, 0.3, 0.22), 1.6, 0.3, 4000)
arp_w = reverb(delay(arp, BEAT * 0.75, 0.42, 0.4), 1.2, 0.28, 5000)
outro_w = reverb(outro, 2.4, 0.45, 3500)
fx_w = reverb(fx, 1.8, 0.3, 5000)

def stereo(x, pan=0.0, width_ms=0.0):
    l = x * np.sqrt((1 - pan) / 2 * 2); r = x * np.sqrt((1 + pan) / 2 * 2)
    if width_ms:
        d = int(width_ms / 1000 * SR); r = np.concatenate([np.zeros(d), r[:-d]])
    return np.stack([l, r], axis=1)

mix = (stereo(drums_w, 0.0) * 1.15
       + stereo(hp(bass, 34), 0.0) * 0.62
       + stereo(chords_w, -0.1, 6) * 1.05
       + stereo(arp_w, 0.2, 4) * 1.0
       + stereo(outro_w, 0.0, 9) * 0.9
       + stereo(fx_w, 0.0, 3) * 0.8)

# gentle high-shelf air via mild high-pass blend and soft limiting
mix = np.tanh(mix * 1.15) * 0.92
peak = np.max(np.abs(mix)); mix = mix / peak * 0.98
# fade out tail
fade = np.ones(N); fs = int(27.6 * SR); fade[fs:] = np.linspace(1, 0, N - fs)
mix *= fade[:, None]

sf.write('audio/track.wav', mix.astype(np.float32), SR, subtype='PCM_16')
print('wrote audio/track.wav', N / SR, 's; kicks:', len(kick_times))
json.dump({'bpm': BPM, 'beat_sec': BEAT, 'bar_sec': BAR, 'groove_start': sec(4), 'break_start': sec(BREAK_BAR*4 + 2),
           'break_end': sec((BREAK_BAR + 1) * 4), 'outro_hit': GROOVE_END, 'kick_times': sorted(kick_times)},
          open('audio/grid.json', 'w'), indent=1)
