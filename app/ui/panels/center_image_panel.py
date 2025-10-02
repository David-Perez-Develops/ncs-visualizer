from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QSlider, QVBoxLayout, QWidget


class CenterImagePanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.button_select_image = QPushButton("Seleccionar imagen", self)
        layout.addWidget(self.button_select_image)

        self.slider_scale_on_beat = self._add_slider(layout, "Scale on beat")
        self.slider_rotate_per_sec = self._add_slider(layout, "Rotate per sec")
        self.slider_shake = self._add_slider(layout, "Shake")
        self.slider_bloom = self._add_slider(layout, "Bloom")

        layout.addStretch(1)

    def _add_slider(self, layout: QVBoxLayout, label_text: str) -> QSlider:
        layout.addWidget(QLabel(label_text, self))
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 100)
        layout.addWidget(slider)
        return slider
