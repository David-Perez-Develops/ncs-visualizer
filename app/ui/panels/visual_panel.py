from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QSlider, QVBoxLayout, QWidget


class VisualPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.checkbox_ring = QCheckBox("Activar anillo", self)
        self.checkbox_bars = QCheckBox("Activar barras", self)
        layout.addWidget(self.checkbox_ring)
        layout.addWidget(self.checkbox_bars)

        self.slider_base_radius = self._add_slider(layout, "Base radius")
        self.slider_thickness = self._add_slider(layout, "Thickness")
        self.slider_glow = self._add_slider(layout, "Glow")
        self.slider_bar_count = self._add_slider(layout, "Bars count")
        self.slider_bar_scale = self._add_slider(layout, "Bars scale")

        layout.addWidget(QLabel("Distribución de barras", self))
        self.combo_distribution = QComboBox(self)
        self.combo_distribution.addItems(["linear", "log", "custom"])
        layout.addWidget(self.combo_distribution)

        layout.addStretch(1)

    def _add_slider(self, layout: QVBoxLayout, label_text: str) -> QSlider:
        layout.addWidget(QLabel(label_text, self))
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 100)
        layout.addWidget(slider)
        return slider
