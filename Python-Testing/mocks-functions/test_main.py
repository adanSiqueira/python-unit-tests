import pytest
from main import get_weather

"""Declaring 'mocker' as a parameter in test function
   pytest automatically injects the mocker fixture"""

def test_get_weather(mocker):
    mock_get = mocker.patch('main.requests.get')

    #Set return values
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temp": 20, "condition": "Sunny"}

    # Call the function
    result = get_weather("London")

    # Assertions
    assert result == {"temp": 20, "condition": "Sunny"}
    mock_get.assert_called_once_with("http://api.weatherapi.com/v1/London")