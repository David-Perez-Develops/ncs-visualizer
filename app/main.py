from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def apply_system_palette(app: QApplication) -> None:
    palette = app.style().standardPalette()
    app.setPalette(palette)


def main() -> None:
    app = QApplication(sys.argv)
    apply_system_palette(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
