from __future__ import annotations


class BackgroundSolid:
    def __init__(self, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.color = color

    def render(self) -> None:  # pragma: no cover - placeholder
        pass


class BackgroundGradient:
    def __init__(self, colors: list[tuple[int, int, int]] | None = None) -> None:
        self.colors = colors or [(0, 0, 0), (255, 255, 255)]

    def render(self) -> None:  # pragma: no cover - placeholder
        pass
