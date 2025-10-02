from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class AudioPanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.button_load_audio = QPushButton("Cargar audio", self)
        self.label_sample_rate = QLabel("Sample rate: --", self)
        self.label_waveform_placeholder = QLabel("Waveform preview (TODO)", self)
        self.label_waveform_placeholder.setStyleSheet("color: gray; font-style: italic;")

        layout.addWidget(self.button_load_audio)
        layout.addWidget(self.label_sample_rate)
        layout.addWidget(self.label_waveform_placeholder)
        layout.addStretch(1)
