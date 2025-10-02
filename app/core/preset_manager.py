from __future__ import annotations
from pathlib import Path
from typing import List, Literal, Optional
import json
from pydantic import BaseModel, field_validator, ValidationError

SCHEMA_VERSION = 1

# -----------------------------
# Modelos pydantic (schema v1)
# -----------------------------

HexColor = str  # validamos por regex en validators

class Resolution(BaseModel):
    width: int
    height: int

    @field_validator("width", "height")
    @classmethod
    def positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("width/height must be positive")
        return v

class OutputConfig(BaseModel):
    resolution: Resolution
    fps: int = 24
    aspect_mode: Literal["fit", "fill", "stretch"] = "fit"
    profile: str = "youtube_1080p24"

    @field_validator("fps")
    @classmethod
    def fps_supported(cls, v: int) -> int:
        if v not in (24, 25, 30, 50, 60):
            raise ValueError("fps must be one of 24,25,30,50,60 for MVP")
        return v

class BackgroundAnim(BaseModel):
    speed: float = 0.2
    keyframes: List[dict] = []

class BackgroundReactivity(BaseModel):
    target: Literal["bass", "mid", "treble", "global"] = "bass"
    intensity: float = 0.6

class BackgroundConfig(BaseModel):
    type: Literal["solid", "gradient", "gradient_anim", "gradient_dynamic"] = "gradient_dynamic"
    colors: List[HexColor] = ["#0f0f1a", "#101a2b", "#192a56"]
    angle: float = 45.0
    anim: BackgroundAnim = BackgroundAnim()
    reactivity: Optional[BackgroundReactivity] = BackgroundReactivity()

    @field_validator("colors")
    @classmethod
    def color_list_len(cls, v: List[str]) -> List[str]:
        if not (1 <= len(v) <= 4):
            raise ValueError("colors must have between 1 and 4 entries")
        return v

    @field_validator("colors", each_item=True)
    @classmethod
    def color_hex(cls, v: str) -> str:
        import re
        if not re.fullmatch(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})", v):
            raise ValueError("color must be #RRGGBB or #RRGGBBAA")
        return v

class RingConfig(BaseModel):
    base_radius: float = 0.35
    thickness: float = 0.02
    glow: float = 0.4

class BarsConfig(BaseModel):
    count: int = 96
    scale: float = 0.25
    distribution: Literal["log", "linear"] = "log"
    roundness: float = 0.4

class VisualMode(BaseModel):
    ring: bool = True
    bars: bool = True

class VisualColor(BaseModel):
    palette: str = "auto"
    gamma: float = 1.2

class VisualMapping(BaseModel):
    attack_ms: int = 80
    release_ms: int = 220
    sensitivity: float = 0.8
    threshold: float = 0.15

class VisualConfig(BaseModel):
    mode: VisualMode = VisualMode()
    ring: RingConfig = RingConfig()
    bars: BarsConfig = BarsConfig()
    color: VisualColor = VisualColor()
    mapping: VisualMapping = VisualMapping()

class CenterImageReactivity(BaseModel):
    scale_on_beat: float = 0.15
    rotate_per_sec: float = 5.0
    shake: float = 0.0
    bloom: float = 0.2

class CenterImageConfig(BaseModel):
    path: str = "assets/logo.png"
    reactivity: CenterImageReactivity = CenterImageReactivity()

class AnalysisConfig(BaseModel):
    sr: int = 44100
    n_fft: int = 2048
    hop: int = 512
    bands: List[List[int]] = [[20,160],[160,2000],[2000,16000]]
    beat_track: bool = True

class AudioConfig(BaseModel):
    normalize: bool = True
    analysis: AnalysisConfig = AnalysisConfig()

class MetaInfo(BaseModel):
    name: str = "Untitled Preset"
    author: str = ""
    created: str = "2025-01-01"

class Preset(BaseModel):
    schema_version: int = SCHEMA_VERSION
    meta: MetaInfo = MetaInfo()
    output: OutputConfig = OutputConfig(resolution=Resolution(width=1920, height=1080))
    background: BackgroundConfig = BackgroundConfig()
    visual: VisualConfig = VisualConfig()
    center_image: CenterImageConfig = CenterImageConfig()
    audio: AudioConfig = AudioConfig()

# -----------------------------
# Gestor de presets
# -----------------------------

class PresetManager:
    def __init__(self, presets_dir: Optional[Path] = None) -> None:
        self.presets_dir = Path(presets_dir) if presets_dir else Path(__file__).resolve().parents[2] / "assets" / "presets"
        self.presets_dir.mkdir(parents=True, exist_ok=True)

    # --- Migración (stub para futuras versiones) ---
    def migrate(self, data: dict) -> dict:
        """Ajusta el diccionario de preset a la versión de esquema soportada.
        Para v1: garantiza 'schema_version' y corrige defaults mínimos.
        """
        sv = data.get("schema_version", 1)
        if sv > SCHEMA_VERSION:
            raise ValueError(f"Preset schema_version {sv} is newer than supported {SCHEMA_VERSION}")
        # Si faltan claves críticas, aplicar defaults
        data.setdefault("schema_version", SCHEMA_VERSION)
        data.setdefault("visual", {})
        data.setdefault("background", {})
        data.setdefault("output", {})
        data.setdefault("audio", {})
        data.setdefault("center_image", {})
        return data

    # --- Validación ---
    def validate_dict(self, data: dict) -> Preset:
        try:
            migrated = self.migrate(data)
            return Preset(**migrated)
        except ValidationError as e:
            raise ValueError(f"Invalid preset: {e}") from e

    # --- IO ---
    def load(self, path: Path | str) -> Preset:
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.validate_dict(data)

    def save(self, preset: Preset, path: Path | str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            json.dump(json.loads(preset.model_dump_json(indent=2)), f, indent=2, ensure_ascii=False)

    # --- Utilidades ---
    def list_builtin(self) -> List[Path]:
        return sorted(self.presets_dir.glob("*.json"))

    def get_builtin(self, name: str) -> Optional[Path]:
        cand = self.presets_dir / f"{name}.json"
        return cand if cand.exists() else None

    def ensure_example_presets(self) -> None:
        """Crea 2 presets de ejemplo si la carpeta está vacía."""
        if any(self.presets_dir.glob("*.json")):
            return
        minimal = {
          "schema_version": 1,
          "meta": { "name": "Minimal Ring", "author": "", "created": "2025-08-30" },
          "output": {
            "resolution": { "width": 1920, "height": 1080 },
            "fps": 24,
            "aspect_mode": "fit",
            "profile": "youtube_1080p24"
          },
          "background": {
            "type": "gradient_dynamic",
            "colors": ["#0f0f1a", "#101a2b", "#192a56"],
            "angle": 45,
            "anim": { "speed": 0.2, "keyframes": [] },
            "reactivity": { "target": "bass", "intensity": 0.6 }
          },
          "visual": {
            "mode": { "ring": True, "bars": True },
            "ring": { "base_radius": 0.35, "thickness": 0.02, "glow": 0.4 },
            "bars": { "count": 96, "scale": 0.25, "distribution": "log", "roundness": 0.4 },
            "color": { "palette": "auto", "gamma": 1.2 },
            "mapping": { "attack_ms": 80, "release_ms": 220, "sensitivity": 0.8, "threshold": 0.15 }
          },
          "center_image": {
            "path": "assets/logo.png",
            "reactivity": { "scale_on_beat": 0.15, "rotate_per_sec": 5, "shake": 0.0, "bloom": 0.2 }
          },
          "audio": {
            "normalize": True,
            "analysis": { "sr": 44100, "n_fft": 2048, "hop": 512, "bands": [ [20,160],[160,2000],[2000,16000] ], "beat_track": True }
          }
        }
        clean_spectrum = {
          "schema_version": 1,
          "meta": { "name": "Clean Spectrum", "author": "", "created": "2025-08-30" },
          "output": { "resolution": { "width": 1080, "height": 1920 }, "fps": 24, "aspect_mode": "fit", "profile": "vertical_1080x1920_24" },
          "background": { "type": "gradient", "colors": ["#141414", "#222222"], "angle": 90, "anim": { "speed": 0.0, "keyframes": [] }, "reactivity": { "target": "global", "intensity": 0.0 } },
          "visual": {
            "mode": { "ring": False, "bars": True },
            "ring": { "base_radius": 0.32, "thickness": 0.02, "glow": 0.2 },
            "bars": { "count": 128, "scale": 0.30, "distribution": "log", "roundness": 0.3 },
            "color": { "palette": "auto", "gamma": 1.15 },
            "mapping": { "attack_ms": 70, "release_ms": 240, "sensitivity": 0.85, "threshold": 0.12 }
          },
          "center_image": { "path": "", "reactivity": { "scale_on_beat": 0.0, "rotate_per_sec": 0.0, "shake": 0.0, "bloom": 0.0 } },
          "audio": { "normalize": True, "analysis": { "sr": 44100, "n_fft": 2048, "hop": 512, "bands": [ [20,160],[160,2000],[2000,16000] ], "beat_track": True } }
        }
        (self.presets_dir / "minimal_ring.json").write_text(json.dumps(minimal, indent=2), encoding="utf-8")
        (self.presets_dir / "clean_spectrum.json").write_text(json.dumps(clean_spectrum, indent=2), encoding="utf-8")

# Helper CLI mínimo (útil para pruebas manuales)
if __name__ == "__main__":
    pm = PresetManager()
    pm.ensure_example_presets()
    builtins = pm.list_builtin()
    print("Presets disponibles:", [p.name for p in builtins])
    # Cargar uno y validar
    if builtins:
        preset = pm.load(builtins[0])
        print("Cargado:", preset.meta.name, "| resolución:", preset.output.resolution.width, "x", preset.output.resolution.height)
