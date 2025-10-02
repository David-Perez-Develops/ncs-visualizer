from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtWidgets import QWidget


class PreviewSurface(QWidget):
    def paintEvent(self, event: QPaintEvent) -> None:  # pragma: no cover - GUI drawing
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.palette().window())
        painter.setPen(self.palette().text().color())
        painter.drawText(self.rect(), Qt.AlignCenter, "Preview")
        painter.end()
        super().paintEvent(event)
