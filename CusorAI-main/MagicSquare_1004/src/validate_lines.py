from __future__ import annotations

from typing import TypedDict

from src.entity.constants import BLANK_CELL, GRID_SIZE, MAGIC_CONSTANT


class ValidationResult(TypedDict):
    status: str
    failed_lines: list[str]


def validate_lines(grid: list[list[int]]) -> ValidationResult:
    for row in grid:
        for cell in row:
            if cell == BLANK_CELL:
                return {"status": "incomplete", "failed_lines": []}

    failed_lines: list[str] = []

    for i in range(GRID_SIZE):
        if sum(grid[i]) != MAGIC_CONSTANT:
            failed_lines.append(f"R{i + 1}")

    for j in range(GRID_SIZE):
        if sum(grid[i][j] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
            failed_lines.append(f"C{j + 1}")

    if sum(grid[i][i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
        failed_lines.append("D1")

    if sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
        failed_lines.append("D2")

    if failed_lines:
        return {"status": "fail", "failed_lines": failed_lines}

    return {"status": "pass", "failed_lines": []}
