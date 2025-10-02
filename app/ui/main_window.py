from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QToolBar,
)

from app.core.render.preview import PreviewSurface
from app.ui.panels.audio_panel import AudioPanel
from app.ui.panels.background_panel import BackgroundPanel
from app.ui.panels.center_image_panel import CenterImagePanel
from app.ui.panels.output_panel import OutputPanel
from app.ui.panels.visual_panel import VisualPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NCS Visualizer")

        self._create_actions()
        self._create_toolbar()
        self._create_central_widget()
        self._create_status_bar()
        self._register_shortcuts()

    def _create_actions(self) -> None:
        self.action_open_audio = QAction("Abrir audio", self)
        self.action_open_preset = QAction("Abrir preset", self)
        self.action_save_preset = QAction("Guardar preset", self)
        self.action_export = QAction("Exportar", self)

        self.action_open_audio.triggered.connect(self.on_open_audio)
        self.action_open_preset.triggered.connect(self.on_open_preset)
        self.action_save_preset.triggered.connect(self.on_save_preset)
        self.action_export.triggered.connect(self.on_export)

    def _create_toolbar(self) -> None:
        toolbar = QToolBar("Principal", self)
        toolbar.setMovable(False)
        toolbar.addAction(self.action_open_audio)
        toolbar.addAction(self.action_open_preset)
        toolbar.addAction(self.action_save_preset)
        toolbar.addAction(self.action_export)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def _create_central_widget(self) -> None:
        splitter = QSplitter(Qt.Horizontal, self)

        self.tab_widget = QTabWidget(splitter)
        self.tab_widget.addTab(BackgroundPanel(self), "Fondo")
        self.tab_widget.addTab(VisualPanel(self), "Visual")
        self.tab_widget.addTab(CenterImagePanel(self), "Imagen")
        self.tab_widget.addTab(AudioPanel(self), "Audio/Análisis")
        self.tab_widget.addTab(OutputPanel(self), "Salida")

        self.preview = PreviewSurface(splitter)
        splitter.addWidget(self.tab_widget)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

    def _create_status_bar(self) -> None:
        status_bar = QStatusBar(self)
        status_bar.showMessage("Listo")
        self.setStatusBar(status_bar)

    def _register_shortcuts(self) -> None:
        self.action_export.setShortcut(QKeySequence("Ctrl+E"))
        self.action_save_preset.setShortcut(QKeySequence.Save)
        undo_action = QAction("Deshacer", self)
        undo_action.setShortcut(QKeySequence.Undo)
        redo_action = QAction("Rehacer", self)
        redo_action.setShortcut(QKeySequence.Redo)
        play_pause_action = QAction("Play/Pause", self)
        play_pause_action.setShortcut(QKeySequence(Qt.Key_Space))

        undo_action.triggered.connect(self.on_undo)
        redo_action.triggered.connect(self.on_redo)
        play_pause_action.triggered.connect(self.on_toggle_play)

        self.addAction(undo_action)
        self.addAction(redo_action)
        self.addAction(play_pause_action)

    def on_open_audio(self) -> None:  # pragma: no cover - placeholder
        self.statusBar().showMessage("Abrir audio (TODO)")

    def on_open_preset(self) -> None:  # pragma: no cover - placeholder
        self.statusBar().showMessage("Abrir preset (TODO)")

    def on_save_preset(self) -> None:  # pragma: no cover - placeholder
        self.statusBar().showMessage("Guardar preset (TODO)")

    def on_export(self) -> None:  # pragma: no cover - placeholder
        self.statusBar().showMessage("Exportar (TODO)")

    def on_toggle_play(self) -> None:  # pragma: no cover - placeholder
        self.statusBar().showMessage("Toggle play (TODO)")

    def on_undo(self) -> None:  # pragma: no cover - placeholder
        self.statusBar().showMessage("Deshacer (TODO)")

    def on_redo(self) -> None:  # pragma: no cover - placeholder
        self.statusBar().showMessage("Rehacer (TODO)")
