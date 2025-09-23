from main import get_weather, add, divide
import pytest

def test_get_weather():
    assert get_weather(25) == "Hot"
    assert get_weather(15) == "Cold"
    assert get_weather(20) == "Cold"
    assert get_weather(21) == "Hot"

def test_add():
    assert add(2, 3) == 5, "Should be 5"
    assert add(-1, 1) == 0, "Should be 0"
    assert add(-1, -1) == -2, "Should be -2"

def test_divide():
    assert divide(6, 3) == 2, "Should be 2"
    assert divide(5, 2) == 2.5, "Should be 2.5"
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)