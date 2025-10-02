from __future__ import annotations


class ReactiveRing:
    def __init__(self, radius: float = 100.0, thickness: float = 10.0) -> None:
        self.radius = radius
        self.thickness = thickness

    def update(self, value: float) -> None:  # pragma: no cover - placeholder
        pass

    def render(self) -> None:  # pragma: no cover - placeholder
        pass
