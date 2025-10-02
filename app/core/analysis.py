from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, List
import numpy as np
import librosa

# Reusar utilidades previas
try:
    from .media_probe import run_ffprobe, parse_audio_info, is_aac_lc_passthrough_possible, AudioInfo
except Exception:  # pragma: no cover - fallback si faltan dependencias
    run_ffprobe = None
    parse_audio_info = None
    is_aac_lc_passthrough_possible = None

    class AudioInfo:  # type: ignore[no-redef]
        ...


# --------- Carga básica (ya implementada en Tarea 03; mantener) ---------
def load_audio(path: str | Path) -> tuple[np.ndarray, int, AudioInfo]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    y, sr = librosa.load(str(p), sr=None, mono=False)
    if y.ndim == 1:
        y = y[None, :]
    y = y.astype(np.float32, copy=False)
    if parse_audio_info is None or run_ffprobe is None:
        info = AudioInfo()
    else:
        info = parse_audio_info(run_ffprobe(p))
        if info is None:  # pragma: no cover - defensive
            info = AudioInfo()
    if getattr(info, "sample_rate", 0) == 0:
        # fallback si no hay ffprobe
        try:
            info.sample_rate = int(sr)
            info.channels = int(y.shape[0])
        except Exception:  # pragma: no cover - best effort
            pass
    return y, int(sr), info


def normalize_sr(data: np.ndarray, sr: int, target: int = 44100, mono: Optional[str] = "mix") -> tuple[np.ndarray, int]:
    if data.ndim != 2:
        raise ValueError("Expected shape (ch, n)")
    ch, _ = data.shape
    out = []
    for c in range(ch):
        out.append(librosa.resample(y=data[c], orig_sr=sr, target_sr=target))
    res = np.stack(out, axis=0)
    if mono == "mix":
        res = np.mean(res, axis=0, keepdims=True)
    elif mono == "left":
        res = res[:1, :]
    elif mono == "keep":
        pass
    else:
        raise ValueError("mono must be one of 'mix','left','keep'")
    return res.astype(np.float32, copy=False), target


def peak_normalize(data: np.ndarray, peak: float = 0.98) -> np.ndarray:
    m = np.max(np.abs(data)) + 1e-12
    return (data / m * peak).astype(np.float32, copy=False)


def aac_passthrough_ok(info: AudioInfo, target_sr: int = 44100, target_channels: int | None = 2) -> bool:
    if is_aac_lc_passthrough_possible is None:
        return False
    return is_aac_lc_passthrough_possible(info, target_sr=target_sr, target_channels=target_channels)


# --------- Nuevas utilidades DSP ---------
@dataclass
class AnalysisResult:
    sr: int
    hop: int
    n_fft: int
    times: np.ndarray                  # (T,)
    S_mag: np.ndarray                  # (F, T) magnitud (opcional para depurar)
    freqs: np.ndarray                  # (F,)
    energy_global: np.ndarray          # (T,) 0..1
    energy_bands: Dict[str, np.ndarray]  # {'bass':(T,), 'mid':(T,), 'treble':(T,)}
    onset_envelope: np.ndarray         # (T,)
    onset_frames: np.ndarray           # (K,)
    onset_times: np.ndarray            # (K,)
    tempo_bpm: float
    beat_frames: np.ndarray            # (M,)
    beat_times: np.ndarray             # (M,)


def stft_mag(y_mono: np.ndarray, sr: int, n_fft: int = 2048, hop: int = 512) -> tuple[np.ndarray, np.ndarray]:
    S = librosa.stft(y=y_mono, n_fft=n_fft, hop_length=hop, window="hann", center=True)
    S_mag = np.abs(S)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    return S_mag, freqs


def _band_indices(freqs: np.ndarray, band: List[int]) -> np.ndarray:
    fmin, fmax = band
    return np.where((freqs >= fmin) & (freqs < fmax))[0]


def band_energies(S_mag: np.ndarray, freqs: np.ndarray, bands: List[List[int]]) -> Dict[str, np.ndarray]:
    names = ["bass", "mid", "treble"]
    out: Dict[str, np.ndarray] = {}
    P = (S_mag ** 2)
    for name, band in zip(names, bands):
        idx = _band_indices(freqs, band)
        if idx.size == 0:
            out[name] = np.zeros(S_mag.shape[1], dtype=np.float32)
        else:
            e = np.sum(P[idx, :], axis=0)
            scale = np.percentile(e, 99) + 1e-9
            out[name] = (e / scale).astype(np.float32)
    return out


def global_energy(S_mag: np.ndarray) -> np.ndarray:
    P = (S_mag ** 2).sum(axis=0)
    scale = np.percentile(P, 99) + 1e-9
    return (P / scale).astype(np.float32)


def analyze_mono(
    y_mono: np.ndarray,
    sr: int,
    *,
    n_fft: int = 2048,
    hop: int = 512,
    bands: Optional[List[List[int]]] = None,
    compute_beats: bool = True,
) -> AnalysisResult:
    if bands is None:
        bands = [[20, 160], [160, 2000], [2000, 16000]]
    S_mag, freqs = stft_mag(y_mono, sr, n_fft=n_fft, hop=hop)
    times = librosa.frames_to_time(np.arange(S_mag.shape[1]), sr=sr, hop_length=hop)
    e_bands = band_energies(S_mag, freqs, bands)
    e_global = global_energy(S_mag)
    onset_env = librosa.onset.onset_strength(y=y_mono, sr=sr, hop_length=hop)
    onset_frames = np.flatnonzero(
        librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, hop_length=hop, units="frames")
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop)
    tempo_bpm = 0.0
    beat_frames = np.array([], dtype=int)
    beat_times = np.array([], dtype=float)
    if compute_beats:
        tempo_bpm, beat_frames = librosa.beat.beat_track(
            onset_envelope=onset_env, sr=sr, hop_length=hop, units="frames"
        )
        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop)
    return AnalysisResult(
        sr=sr,
        hop=hop,
        n_fft=n_fft,
        times=times,
        S_mag=S_mag.astype(np.float32),
        freqs=freqs.astype(np.float32),
        energy_global=e_global,
        energy_bands=e_bands,
        onset_envelope=onset_env.astype(np.float32),
        onset_frames=onset_frames.astype(int),
        onset_times=onset_times.astype(np.float32),
        tempo_bpm=float(tempo_bpm),
        beat_frames=beat_frames.astype(int),
        beat_times=beat_times.astype(np.float32),
    )


def analyze_file(
    path: str | Path,
    *,
    target_sr: int = 44100,
    mono: str = "mix",
    n_fft: int = 2048,
    hop: int = 512,
    bands: Optional[List[List[int]]] = None,
    compute_beats: bool = True,
) -> AnalysisResult:
    y, sr, _ = load_audio(path)
    y44, _ = normalize_sr(y, sr, target=target_sr, mono=mono)
    y_mono = y44[0]
    return analyze_mono(y_mono, target_sr, n_fft=n_fft, hop=hop, bands=bands, compute_beats=compute_beats)


# CLI simple para depurar
if __name__ == "__main__":  # pragma: no cover - CLI manual
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m app.core.analysis <audio.(wav|mp3|ogg)>")
        raise SystemExit(1)
    res = analyze_file(sys.argv[1])
    print(
        f"SR={res.sr} hop={res.hop} n_fft={res.n_fft} frames={res.S_mag.shape[1]} tempo≈{res.tempo_bpm:.1f} BPM, beats={len(res.beat_frames)}"
    )
    print("Energía medias:", {k: float(np.mean(v)) for k, v in res.energy_bands.items()})
