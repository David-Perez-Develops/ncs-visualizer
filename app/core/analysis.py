from __future__ import annotations
from pathlib import Path
from typing import Tuple, Optional
import numpy as np
import librosa

from .media_probe import run_ffprobe, parse_audio_info, is_aac_lc_passthrough_possible, AudioInfo


def load_audio(path: str | Path) -> tuple[np.ndarray, int, AudioInfo]:
    """Carga WAV/MP3/OGG a float32 [-1,1], mantiene SR y canales nativos; retorna (audio, sr, info)."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    # librosa usa audioread/ffmpeg para MP3/OGG si es necesario
    y, sr = librosa.load(str(p), sr=None, mono=False)  # shape: (n,) o (ch, n)
    if y.ndim == 1:
        y = y[None, :]  # (1, n) para consistencia
    y = y.astype(np.float32, copy=False)
    # Probe con ffprobe para metadatos y passthrough
    try:
        ffp = run_ffprobe(p)
        info = parse_audio_info(ffp)
    except Exception:
        info = AudioInfo()
        info.sample_rate = int(sr)
        info.channels = int(y.shape[0])
        info.codec_name = ""
    return y, int(sr), info


def normalize_sr(data: np.ndarray, sr: int, target: int = 44100, mono: Optional[str] = "mix") -> tuple[np.ndarray, int]:
    """Resample a target SR; maneja canales: mono='keep'|'mix'|'left'.
    - data: (ch, n)
    - retorna (data_resampled, target)
    """
    if data.ndim != 2:
        raise ValueError("Expected shape (ch, n)")
    ch, n = data.shape
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
    return is_aac_lc_passthrough_possible(info, target_sr=target_sr, target_channels=target_channels)
