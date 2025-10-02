import numpy as np
from app.core.analysis import normalize_sr, peak_normalize, aac_passthrough_ok
from app.core.media_probe import AudioInfo


def test_resample_and_mono_mix():
    sr = 48000
    t = np.linspace(0, 1.0, int(sr), endpoint=False)
    # Señal estéreo simple (izq=sin, der=sin*0.5)
    left = 0.5 * np.sin(2 * np.pi * 440 * t).astype(np.float32)
    right = 0.25 * np.sin(2 * np.pi * 880 * t).astype(np.float32)
    data = np.stack([left, right], axis=0)
    out, sr2 = normalize_sr(data, sr, target=44100, mono="mix")
    assert sr2 == 44100
    assert out.ndim == 2 and out.shape[0] == 1  # mezclado a mono
    assert np.isfinite(out).all()


def test_peak_normalize():
    x = np.array([[0.1, -0.5, 0.25]], dtype=np.float32)
    y = peak_normalize(x, peak=0.9)
    assert np.isclose(np.max(np.abs(y)), 0.9, atol=1e-3)


def test_aac_passthrough_rule():
    info = AudioInfo(codec_name="aac", sample_rate=44100, channels=2)
    assert aac_passthrough_ok(info, target_sr=44100, target_channels=2) is True
    info2 = AudioInfo(codec_name="aac", sample_rate=48000, channels=2)
    assert aac_passthrough_ok(info2, target_sr=44100, target_channels=2) is False
