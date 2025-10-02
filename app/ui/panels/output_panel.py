from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class OutputPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.combo_presets = QComboBox(self)
        self.combo_presets.addItems(["YouTube 1080p", "YouTube 4K", "Instagram Reel"])

        form_layout = QFormLayout()
        self.spin_resolution_width = QSpinBox(self)
        self.spin_resolution_width.setRange(320, 7680)
        self.spin_resolution_width.setValue(1920)
        self.spin_resolution_height = QSpinBox(self)
        self.spin_resolution_height.setRange(240, 4320)
        self.spin_resolution_height.setValue(1080)
        self.spin_fps = QSpinBox(self)
        self.spin_fps.setRange(1, 240)
        self.spin_fps.setValue(60)

        form_layout.addRow("Preset", self.combo_presets)
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(self.spin_resolution_width)
        resolution_layout.addWidget(QLabel("x", self))
        resolution_layout.addWidget(self.spin_resolution_height)
        form_layout.addRow("Resolución", resolution_layout)
        form_layout.addRow("FPS", self.spin_fps)

        layout.addLayout(form_layout)

        self.button_export = QPushButton("Exportar", self)
        self.button_export.setEnabled(False)
        layout.addWidget(self.button_export)
        layout.addStretch(1)
