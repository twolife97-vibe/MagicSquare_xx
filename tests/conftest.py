import pytest

from src.validate_lines import MAGIC_CONSTANT


@pytest.fixture
def grid_pass():
    """Complete 4×4 magic square — all ten lines sum to MAGIC_CONSTANT."""
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  1],
    ]
    side = len(grid)
    assert side == len(grid[0])
    assert all(len(row) == side for row in grid)
    assert not any(cell == 0 for row in grid for cell in row)
    assert MAGIC_CONSTANT == 34
    return grid


@pytest.fixture
def grid_fail_d2(grid_pass):
    """grid_pass with (2,2) changed 7→8: D1=34, D2≠34."""
    grid = [row[:] for row in grid_pass]
    grid[2][2] = 8
    return grid


@pytest.fixture
def grid_fail_multi(grid_fail_d2):
    """Same as grid_fail_d2 — D2, R3, C3 fail; no blanks."""
    return [row[:] for row in grid_fail_d2]


@pytest.fixture
def grid_incomplete_r3():
    """Magic square with blank at (2,1) — R3, C2, D1 incomplete."""
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  0,  7, 12],
        [ 4, 15, 14,  1],
    ]
    side = len(grid)
    assert side == len(grid[0])
    assert all(len(row) == side for row in grid)
    assert sum(cell == 0 for row in grid for cell in row) == 1
    return grid
