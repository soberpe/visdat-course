"""Entry point for the Final Assignment GUI.

Run:
    python main.py
"""

from __future__ import annotations

import sys
from PyQt6.QtWidgets import QApplication

from ui_mainwindow import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1400, 780)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
