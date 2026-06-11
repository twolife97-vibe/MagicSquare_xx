"""FR-LOC-01 — 빈칸(0) 좌표를 1-index row-major 순으로 반환."""

from src.entity.constants import BLANK_CELL, GRID_SIZE


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    coords: list[tuple[int, int]] = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == BLANK_CELL:
                coords.append((row + 1, col + 1))
    return coords
