import pytest
from main import get_weather, add, divide

def test_get_weather():
    """Test that get_weather returns correct classification."""
    assert get_weather(25) == "Hot"
    assert get_weather(15) == "Cold"
    assert get_weather(20) == "Cold"
    assert get_weather(21) == "Hot"

def test_add():
    """Test addition results for various inputs."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2

def test_divide():
    """Test division function including zero division."""
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
