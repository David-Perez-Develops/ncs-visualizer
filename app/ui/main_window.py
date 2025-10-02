from PySide6 import QtCore, QtGui, QtWidgets
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NCS Visualizer — MVP")
        self.resize(1200, 800)
        self._init_ui()
        self._apply_theme()

    def _init_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&Archivo")
        file_menu.addAction(QtGui.QAction("Abrir audio...", self))
        file_menu.addAction(QtGui.QAction("Exportar...", self))

        preset_menu = menubar.addMenu("&Preset")
        preset_menu.addAction(QtGui.QAction("Importar preset...", self))
        preset_menu.addAction(QtGui.QAction("Guardar preset...", self))

        layout = QtWidgets.QHBoxLayout(central)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(QtWidgets.QWidget(), "Fondo")
        self.tabs.addTab(QtWidgets.QWidget(), "Visual")
        self.tabs.addTab(QtWidgets.QWidget(), "Imagen")
        self.tabs.addTab(QtWidgets.QWidget(), "Audio/Análisis")
        self.tabs.addTab(QtWidgets.QWidget(), "Salida")

        self.preview = QtWidgets.QLabel("Viewport de preview (PyQtGraph próximamente)")
        self.preview.setAlignment(QtCore.Qt.AlignCenter)
        self.preview.setStyleSheet("background:#111; color:#bbb; border:1px solid #333;")

        right = QtWidgets.QTextEdit()
        right.setReadOnly(True)
        right.setPlaceholderText("Log / Eventos / Progreso")

        layout.addWidget(self.tabs, 2)
        layout.addWidget(self.preview, 5)
        layout.addWidget(right, 3)

        QtWidgets.QShortcut(QtGui.QKeySequence("Space"), self, activated=self._toggle_play)

    def _apply_theme(self):
        is_dark = QtGui.QGuiApplication.palette().color(QtGui.QPalette.Window).value() < 128
        if is_dark:
            self.setStyleSheet("QMainWindow{background:#121212;color:#e0e0e0}")
        else:
            self.setStyleSheet("QMainWindow{background:#f4f4f4;color:#222}")

    def _toggle_play(self):
        QtWidgets.QMessageBox.information(self, "Preview", "Play/Pause (placeholder)")


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
