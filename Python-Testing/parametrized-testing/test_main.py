import pytest
from main import is_prime

@pytest.mark.parametrize("input,expected", [
    (1, False), (2, True), (3, True),(4, False), 
    (5, True), (16, False), (17, True), (18, False),
    (19, True), (20, False), (23, True), (24, False), (25, False)])

def test_is_prime(input, expected):
    assert is_prime(input) == expected