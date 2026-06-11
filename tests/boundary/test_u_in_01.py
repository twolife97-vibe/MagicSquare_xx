import pytest

from src.validate_lines import validate_lines


def test_u_in_01_grid_none_raises():
    # Given
    grid = None

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail("RED: U-IN-01 — grid=None → TypeError, dict return forbidden")
