from src.calc import add


def test_add_returns_sum():
    first = 2
    second = 3
    expected = 5

    result = add(first, second)

    assert result == expected
