from __future__ import annotations

from pathlib import Path
from typing import Tuple

import librosa
import numpy as np


def load_audio(path: str | Path) -> Tuple[np.ndarray, int]:
    """Loads audio file returning waveform and sample rate."""
    data, sample_rate = librosa.load(Path(path), sr=None, mono=True)
    return data, sample_rate


def normalize_sr(data: np.ndarray, sample_rate: int, target: int = 44_100) -> Tuple[np.ndarray, int]:
    """Normalizes audio to target sample rate."""
    if sample_rate == target:
        return data, sample_rate
    resampled = librosa.resample(data, orig_sr=sample_rate, target_sr=target)
    return resampled, target
