from src.boundary.input_handler import InputHandler


def test_u_in_01_none_grid_returns_e003():
    # Given: grid=None
    # When: InputHandler.validate(None)
    # Then: error_code == "E003"
    handler = InputHandler()
    result = handler.validate(None)
    assert result["error_code"] == "E003"
