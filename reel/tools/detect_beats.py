#!/usr/bin/env python3
"""Detect beats/onsets in audio/track.wav and write audio/beats.json for the edit."""
import json, numpy as np, librosa, soundfile as sf
y, sr = sf.read('audio/track.wav', dtype='float32')
if y.ndim == 2: y = y.mean(axis=1)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, start_bpm=120, units='time', tightness=200)
tempo = float(np.atleast_1d(tempo)[0])
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
times = librosa.times_like(onset_env, sr=sr)
onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time', backtrack=False, delta=0.25)
# strength of each detected beat = onset envelope near it
def strength(t):
    i = int(np.argmin(np.abs(times - t))); lo, hi = max(0, i-2), min(len(onset_env), i+3)
    return float(onset_env[lo:hi].max())
beat_strength = [strength(t) for t in beats]
# compare with the 120 BPM grid used to synthesize the track
grid = np.arange(0, 28.5, 0.5)
err = [float(np.min(np.abs(grid - b))) for b in beats]
# downbeats: beats closest to multiples of 2.0 s
downbeats = [float(b) for b in beats if np.min(np.abs(np.arange(0, 30, 2.0) - b)) < 0.12]
strong = sorted(onsets, key=lambda t: -strength(t))[:20]
out = {
  'tempo_detected': tempo,
  'beats': [round(float(b), 4) for b in beats],
  'beat_strength': [round(s, 3) for s in beat_strength],
  'downbeats': [round(d, 4) for d in downbeats],
  'onsets': [round(float(o), 4) for o in onsets],
  'strong_hits': sorted(round(float(t), 4) for t in strong),
  'grid_mean_abs_error_ms': round(1000 * float(np.mean(err)), 1),
  'grid_max_abs_error_ms': round(1000 * float(np.max(err)), 1),
  'fps': 30, 'frames_per_beat': 15,
}
json.dump(out, open('audio/beats.json', 'w'), indent=1)
rms = float(np.sqrt(np.mean(y**2))); peak = float(np.max(np.abs(y)))
print(f"tempo={tempo:.2f} beats={len(beats)} first={beats[:6]} downbeats={len(downbeats)} onsets={len(onsets)}")
print(f"grid error mean={out['grid_mean_abs_error_ms']}ms max={out['grid_max_abs_error_ms']}ms  rms={20*np.log10(rms):.1f}dBFS peak={20*np.log10(peak):.1f}dBFS")
# spectral balance check (rough): energy in bands
S = np.abs(librosa.stft(y, n_fft=4096)); f = librosa.fft_frequencies(sr=sr, n_fft=4096)
def band(lo, hi): return 10*np.log10(np.mean(S[(f>=lo)&(f<hi)]**2) + 1e-12)
print('bands dB: sub<80', round(band(20,80),1), ' bass80-250', round(band(80,250),1), ' mid250-2k', round(band(250,2000),1), ' hi2k-8k', round(band(2000,8000),1), ' air>8k', round(band(8000,20000),1))
