"""MagicSquare_1004 검증 GUI — InputHandler → validate_lines."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.boundary.grid_ui import GridUI
from src.boundary.input_handler import InputHandler
from src.boundary.result_display import ResultDisplay
from src.validate_lines import validate_lines

# SSOT: tests/conftest.py → GRID_G1, docs/PRD.md §10.2
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]


class ValidationWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare_1004 — 10선 검증")
        self._input_handler = InputHandler()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self._grid_ui = GridUI()
        self._grid_ui.set_grid(GRID_G1)
        layout.addWidget(self._grid_ui)

        validate_button = QPushButton("검증")
        validate_button.clicked.connect(self._on_validate)
        layout.addWidget(validate_button)

        self._result_display = ResultDisplay()
        layout.addWidget(self._result_display)

    def _on_validate(self) -> None:
        grid = self._grid_ui.get_grid()
        input_result = self._input_handler.validate(grid)
        if input_result["error_code"] is not None:
            self._result_display.show_input_error(input_result["error_code"])
            return

        validation_result = validate_lines(grid)
        self._result_display.show_validation(validation_result)


def main() -> None:
    app = QApplication(sys.argv)
    window = ValidationWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
