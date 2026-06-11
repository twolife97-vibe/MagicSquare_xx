from src.boundary.input_handler import InputHandler


def test_u_in_02_cell_value_17_returns_e002():
    # Given: 4×4 격자, 셀 하나가 17 (허용 범위 0 또는 1~16 위반)
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 17],
    ]

    # When: InputHandler.validate(grid)
    # Then: error_code == "E002"
    handler = InputHandler()
    result = handler.validate(grid)
    assert result["error_code"] == "E002"
