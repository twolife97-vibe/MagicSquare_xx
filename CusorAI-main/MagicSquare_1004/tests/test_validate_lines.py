from src.validate_lines import validate_lines


def test_t2_fail_r2_and_c2_when_intersection_cell_changed_from_10_to_11():
    # Arrange: 완성 격자에서 R2·C2 교차 셀 (1-index (2,2) = grid[1][1]) 10→11
    grid = [
        [16,  3,  2, 13],
        [ 5, 11, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  1],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "R2" in result["failed_lines"]
    assert "C2" in result["failed_lines"]
