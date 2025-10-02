from __future__ import annotations


class CenterImage:
    def __init__(self, path: str | None = None) -> None:
        self.path = path

    def set_image(self, path: str) -> None:
        self.path = path

    def render(self) -> None:  # pragma: no cover - placeholder
        pass
