import pytest

from src.validate_lines import validate_lines


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given
    grid = grid_g1
    side = len(grid)
    assert side == len(grid[0])

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-D-LOC-01 — G1 blanks (1,2)(3,2) row-major → status==incomplete"
    )


def test_d_loc_02_g1_failed_lines_superset(grid_g1):
    # Given
    grid = grid_g1

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-D-LOC-02 — G1 → failed_lines ⊇ {R2,R4,C3,D1}"
    )


def test_d_loc_03_g1_failed_lines_exact_order(grid_g1):
    # Given
    grid = grid_g1

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-D-LOC-03 — G1 → failed_lines==[R2,R4,C3,D1] in LINE_IDS order"
    )
