"""pytest 픽스처 — 로직 없음, G1 격자 SSOT만."""

import pytest

from src.entity.constants import BLANK_COUNT, GRID_SIZE

# G1: 빈칸 2개 (0-index (1,2), (3,3)) → 1-index row-major [(2,3), (4,4)]
# SSOT: docs/PRD.md §11
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]

G1_BLANK_COORDS_1INDEX: list[tuple[int, int]] = [(2, 3), (4, 4)]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1 격자 — 0이 정확히 2개."""
    grid = [row[:] for row in GRID_G1]
    blank_count = sum(cell == 0 for row in grid for cell in row)
    assert blank_count == BLANK_COUNT
    assert len(grid) == GRID_SIZE
    assert all(len(row) == GRID_SIZE for row in grid)
    return grid
