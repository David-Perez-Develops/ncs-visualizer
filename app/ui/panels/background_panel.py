from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget


class BackgroundPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Tipo de fondo", self))
        self.combo_background_type = QComboBox(self)
        self.combo_background_type.addItems(
            ["solid", "gradient", "gradient_anim", "gradient_dynamic"]
        )
        layout.addWidget(self.combo_background_type)

        self.label_color_controls = QLabel("Controles de color (TODO)", self)
        self.label_color_controls.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.label_color_controls)

        layout.addStretch(1)
