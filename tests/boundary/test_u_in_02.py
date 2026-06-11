import pytest

from src.validate_lines import validate_lines


def test_u_in_02_wrong_row_count_raises(grid_pass):
    # Given
    width = len(grid_pass[0])
    row = [1] * width
    grid = [row[:] for _ in range(width - 1)]
    assert len(grid) == width - 1

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: U-IN-02 — row count below GRID_SIZE → ValueError, dict return forbidden"
    )
