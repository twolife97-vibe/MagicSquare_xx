"""4×4 격자 입력 위젯 — Boundary GridUI 프로토타입."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QSpinBox, QWidget

from src.entity.constants import GRID_SIZE, MAX_CELL_VALUE


class GridUI(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._cells: list[list[QSpinBox]] = []
        layout = QGridLayout(self)
        layout.setSpacing(4)

        for row in range(GRID_SIZE):
            row_cells: list[QSpinBox] = []
            for col in range(GRID_SIZE):
                spin = QSpinBox()
                spin.setRange(0, MAX_CELL_VALUE)
                spin.setSpecialValueText("")
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setMinimumWidth(48)
                layout.addWidget(spin, row, col)
                row_cells.append(spin)
            self._cells.append(row_cells)

    def set_grid(self, grid: list[list[int]]) -> None:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self._cells[row][col].setValue(grid[row][col])

    def get_grid(self) -> list[list[int]]:
        return [[cell.value() for cell in row] for row in self._cells]
