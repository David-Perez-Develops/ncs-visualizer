from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import shutil
import subprocess
from typing import Optional, Dict, Any


def _ffbin_candidates(name: str) -> list[str]:
    """Devuelve candidatos de ruta para ffmpeg/ffprobe (embebido o del sistema)."""
    here = Path(__file__).resolve()
    root = here.parents[2]  # .../app/
    embedded = root / "ffmpeg" / (name + (".exe" if __import__('platform').system() == "Windows" else ""))
    return [str(embedded), name]


def run_ffprobe(path: str | Path) -> Dict[str, Any]:
    """Ejecuta ffprobe -v error -print_format json -show_streams -show_format y retorna el dict JSON."""
    src = str(path)
    cmd = ["-v", "error", "-print_format", "json", "-show_streams", "-show_format", src]
    last_err = None
    for bin_name in ("ffprobe",):
        for cand in _ffbin_candidates(bin_name):
            exe = shutil.which(cand) if not Path(cand).exists() else str(cand)
            if not exe:
                continue
            try:
                out = subprocess.check_output([exe, *cmd], stderr=subprocess.STDOUT)
                return json.loads(out.decode("utf-8", errors="ignore"))
            except subprocess.CalledProcessError as e:
                last_err = e
                continue
    raise RuntimeError(f"ffprobe not found or failed to run: {last_err}")


@dataclass
class AudioInfo:
    codec_name: str = ""
    sample_rate: int = 0
    channels: int = 0
    channel_layout: str = ""
    duration: float = 0.0
    format_name: str = ""


def parse_audio_info(ffp: Dict[str, Any]) -> AudioInfo:
    streams = ffp.get("streams", [])
    fmt = ffp.get("format", {})
    a = AudioInfo()
    for s in streams:
        if s.get("codec_type") == "audio":
            a.codec_name = s.get("codec_name", "") or ""
            try:
                a.sample_rate = int(s.get("sample_rate") or 0)
            except Exception:
                a.sample_rate = 0
            a.channels = int(s.get("channels") or 0)
            a.channel_layout = s.get("channel_layout", "") or ""
            break
    a.duration = float(fmt.get("duration") or 0.0)
    a.format_name = fmt.get("format_name", "") or ""
    return a


def is_aac_lc_passthrough_possible(info: AudioInfo, target_sr: int = 44100, target_channels: int | None = None) -> bool:
    """Regla MVP: passthrough si codec es 'aac' (perfil LC asumido) y sample_rate == target_sr y canales coinciden (si se especifica)."""
    if info.codec_name.lower() != "aac":
        return False
    if info.sample_rate != target_sr:
        return False
    if target_channels is not None and info.channels and info.channels != target_channels:
        return False
    return True
