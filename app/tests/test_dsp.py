import numpy as np

from app.core.analysis import analyze_mono


def test_band_energy_distribution():
    sr = 44100
    t = np.linspace(0, 2.0, int(sr * 2.0), endpoint=False)
    y = 0.8 * np.sin(2 * np.pi * 100 * t) + 0.2 * np.sin(2 * np.pi * 500 * t)
    res = analyze_mono(y.astype(np.float32), sr, n_fft=2048, hop=512)
    eb = res.energy_bands
    assert np.mean(eb["bass"]) > np.mean(eb["mid"]) * 1.3
    assert np.mean(eb["bass"]) > np.mean(eb["treble"]) * 2.0


def test_tempo_detection_approx():
    sr = 44100
    dur = 4.0
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    y = np.zeros_like(t, dtype=np.float32)
    for k in range(int(dur / 0.5)):
        idx = int(k * 0.5 * sr)
        y[idx : idx + 200] = 1.0
    res = analyze_mono(y, sr, n_fft=1024, hop=256)
    assert 115 <= res.tempo_bpm <= 125
