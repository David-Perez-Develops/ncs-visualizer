from __future__ import annotations


class RadialBars:
    def __init__(self, count: int = 64) -> None:
        self.count = count
        self.values = [0.0] * count

    def update(self, spectrum: list[float]) -> None:  # pragma: no cover - placeholder
        self.values = spectrum[: self.count]

    def render(self) -> None:  # pragma: no cover - placeholder
        pass
