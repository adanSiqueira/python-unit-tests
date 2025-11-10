from main import get_weather

def test_get_weather(mocker):
    """Test get_weather using a mock of the requests.get call."""
    mock_get = mocker.patch('main.requests.get')

    # Configure mock response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temp": 20, "condition": "Sunny"}

    result = get_weather("London")

    assert result == {"temp": 20, "condition": "Sunny"}
    mock_get.assert_called_once_with("http://api.weatherapi.com/v1/London")
