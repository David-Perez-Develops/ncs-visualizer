from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError


class Preset(BaseModel):
    name: str
    data: dict[str, Any]


class PresetManager:
    def __init__(self, base_path: str | Path | None = None) -> None:
        self.base_path = Path(base_path) if base_path else None

    def load(self, path: str | Path) -> Preset:
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        try:
            return Preset(**payload)
        except ValidationError as exc:  # pragma: no cover - placeholder
            raise ValueError("Invalid preset data") from exc

    def save(self, preset: Preset, path: str | Path | None = None) -> Path:
        file_path = Path(path) if path else self._resolve_path(preset.name)
        if file_path is None:
            raise ValueError("No path provided for preset save")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as fh:
            json.dump(preset.dict(), fh, indent=2, ensure_ascii=False)
        return file_path

    def _resolve_path(self, name: str) -> Path | None:
        if not self.base_path:
            return None
        return self.base_path / f"{name}.json"

    def validate(self, data: dict[str, Any]) -> None:  # pragma: no cover - TODO
        """Validates preset data."""
        raise NotImplementedError
